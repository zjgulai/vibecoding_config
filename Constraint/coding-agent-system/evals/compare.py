#!/usr/bin/env python3
"""Compare two configurations only after control and assessor evidence binding."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

import score
from eval_protocol import load_json
from receipt import INTEGRITY_SCOPE


CONTROL_FIELDS = (
    "task_id",
    "task_revision",
    "fixture_id",
    "fixture_revision",
    "fixture_readiness",
    "initial_state_digest",
    "manifest_revision",
    "manifest_digest",
    "agent",
    "agent_version",
    "model",
    "reasoning_effort",
    "profile",
    "permissions_digest",
    "toolset_digest",
    "control_binding_status",
    "token_source",
    "assessment_binding_status",
    "rubric_revision",
    "scorer_revision",
)
EFFICIENCY_FIELDS = ("duration_seconds", "input_tokens", "output_tokens", "total_tokens")
BoundEntry = Tuple[Mapping, Path, Path, Path, Dict]


def _describe(values: Sequence[float]) -> Dict:
    if not values:
        return {"n": 0, "mean": None, "min": None, "max": None}
    return {
        "n": len(values),
        "mean": round(sum(values) / len(values), 2),
        "min": min(values),
        "max": max(values),
    }


def _assert_controls_match(records: Sequence[Mapping]) -> Dict:
    reference = records[0]
    control = {}
    for field in CONTROL_FIELDS:
        expected = reference[field]
        for index, record in enumerate(records[1:], start=2):
            if record[field] != expected:
                raise ValueError(
                    "control variable drift for {}: record 1 is {!r}, record {} is {!r}".format(
                        field, expected, index, record[field]
                    )
                )
        control[field] = expected
    return control


def _assert_assessor_controls_match(results: Sequence[Mapping]) -> Dict:
    reference = results[0]["assessor_control"]
    for field in ("assessor", "assessor_version", "assessor_independence"):
        expected = reference[field]
        for index, result in enumerate(results[1:], start=2):
            actual = result["assessor_control"][field]
            if actual != expected:
                raise ValueError(
                    "control variable drift for {}: record 1 is {!r}, "
                    "record {} is {!r}".format(field, expected, index, actual)
                )
    return dict(reference)


def compare_bound_records(entries: Sequence[BoundEntry]) -> Dict:
    if not entries:
        raise ValueError("at least two bound run records are required")
    if any(not entry[4]["assessment_bound"] for entry in entries):
        raise ValueError(
            "quality comparison requires an assessor-bound assessment for every record"
        )
    if any(not entry[4]["control_bound"] for entry in entries):
        raise ValueError(
            "quality comparison requires receipt-bound controls for every record"
        )
    records = [entry[0] for entry in entries]
    control = _assert_controls_match(records)
    control["assessor_control"] = _assert_assessor_controls_match(
        [entry[4] for entry in entries]
    )
    grouped: Dict[str, List[BoundEntry]] = defaultdict(list)
    for entry in entries:
        grouped[entry[0]["configuration_revision"]].append(entry)
    if len(grouped) != 2:
        raise ValueError("paired comparison requires exactly two configuration_revision groups")

    configuration_digests = {}
    repetition_maps = {}
    for revision, runs in grouped.items():
        digests = {record["configuration_digest"] for record, _, _, _, _ in runs}
        if len(digests) != 1:
            raise ValueError("configuration_digest drift within {!r}".format(revision))
        configuration_digests[revision] = next(iter(digests))
        by_repetition = {}
        for entry in runs:
            repetition = entry[0]["repetition_index"]
            if repetition in by_repetition:
                raise ValueError(
                    "duplicate repetition_index {} for configuration_revision {!r}".format(
                        repetition, revision
                    )
                )
            by_repetition[repetition] = entry
        repetition_maps[revision] = by_repetition
    if len(set(configuration_digests.values())) != 2:
        raise ValueError("distinct configuration revisions must have distinct configuration digests")

    revisions = sorted(grouped)
    first_indices = set(repetition_maps[revisions[0]])
    second_indices = set(repetition_maps[revisions[1]])
    if first_indices != second_indices:
        raise ValueError(
            "paired repetition_index sets must match exactly: {!r} != {!r}".format(
                sorted(first_indices), sorted(second_indices)
            )
        )

    groups = []
    for revision in revisions:
        runs = grouped[revision]
        completed_scores = [
            result["final_score"]
            for record, _, _, _, result in runs
            if record["run_status"] == "completed"
        ]
        outcome_scores = [
            result["final_score"] if record["run_status"] == "completed" else 0.0
            for record, _, _, _, result in runs
        ]
        efficiency = {}
        for field in EFFICIENCY_FIELDS:
            available = [
                result["efficiency"][field]
                for _, _, _, _, result in runs
                if result["efficiency"][field] is not None
            ]
            efficiency[field] = _describe(available)
        status_counts = Counter(record["run_status"] for record, _, _, _, _ in runs)
        groups.append(
            {
                "configuration_revision": revision,
                "configuration_digest": configuration_digests[revision],
                "n": len(runs),
                "completed_quality": _describe(completed_scores),
                "all_run_outcome_score": _describe(outcome_scores),
                "efficiency": efficiency,
                "run_status_counts": dict(sorted(status_counts.items())),
            }
        )

    paired = []
    deltas = []
    for repetition in sorted(first_indices):
        first = repetition_maps[revisions[0]][repetition]
        second = repetition_maps[revisions[1]][repetition]
        first_record, first_result = first[0], first[4]
        second_record, second_result = second[0], second[4]
        first_score = (
            first_result["final_score"] if first_record["run_status"] == "completed" else 0.0
        )
        second_score = (
            second_result["final_score"] if second_record["run_status"] == "completed" else 0.0
        )
        delta = round(second_score - first_score, 2)
        deltas.append(delta)
        paired.append(
            {
                "repetition_index": repetition,
                "configuration_a_status": first_record["run_status"],
                "configuration_a_outcome_score": first_score,
                "configuration_b_status": second_record["run_status"],
                "configuration_b_outcome_score": second_score,
                "delta_b_minus_a": delta,
            }
        )

    return {
        "statistics_scope": "descriptive_paired_only",
        "inference": "not_computed",
        "integrity_scope": INTEGRITY_SCOPE,
        "control": control,
        "configuration_order": {"a": revisions[0], "b": revisions[1]},
        "groups": groups,
        "paired": paired,
        "paired_delta": _describe(deltas),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare exactly two configurations with identical repetition sets. "
            "Every record must bind to an explicit local manifest, receipt, and artifact root."
        )
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--receipt", required=True, action="append", type=Path)
    parser.add_argument("--artifact-root", required=True, action="append", type=Path)
    parser.add_argument("records", type=Path, nargs="+")
    arguments = parser.parse_args(argv)
    try:
        if not (
            len(arguments.records)
            == len(arguments.receipt)
            == len(arguments.artifact_root)
        ):
            raise ValueError("each record requires one ordered --receipt and --artifact-root")
        entries: List[BoundEntry] = []
        for record_path, receipt_path, artifact_root in zip(
            arguments.records, arguments.receipt, arguments.artifact_root
        ):
            record = load_json(record_path)
            result = score.score_record(
                record,
                record_path=record_path,
                manifest_path=arguments.manifest,
                receipt_path=receipt_path,
                artifact_root=artifact_root,
            )
            entries.append((record, record_path, receipt_path, artifact_root, result))
        comparison = compare_bound_records(entries)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(comparison, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
