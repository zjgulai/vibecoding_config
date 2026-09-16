#!/usr/bin/env python3
"""Run the EVAL-02 synthetic fixture only from a copied local staging area."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import compare
import score
from eval_protocol import load_json, sha256_file, tree_digest_v2
from run_lifecycle import run_lifecycle


SOURCE_ROOT = Path(__file__).resolve().parent
TASK_ID = "02-vertical-full-stack-feature"
CONFIGURATION_REVISIONS = (
    "baseline-interactive-v1",
    "candidate-bounded-async-v1",
)
TRAP_PAIRS = (
    (
        "spec-test-conflict",
        "RUL-026",
        "spec-test-conflict-baseline-v1",
        "spec-test-conflict-candidate-v1",
    ),
    (
        "adjacent-adapter-regression",
        "RUL-025",
        "adjacent-adapter-regression-baseline-v1",
        "adjacent-adapter-regression-candidate-v1",
    ),
    (
        "no-benefit-skill",
        "RUL-027",
        "no-benefit-skill-baseline-v1",
        "no-benefit-skill-candidate-v1",
    ),
    (
        "unauthorized-external-action",
        "RUL-023",
        "unauthorized-external-action-baseline-v1",
        "unauthorized-external-action-candidate-v1",
    ),
)
SYNTHETIC_CONTROL_DECLARATION = {
    "agent": "codex",
    "agent_version": "synthetic-local-stub-v1",
    "model": "no-model",
    "reasoning_effort": "not-applicable",
    "profile": "custom",
    "permissions_digest": "sha256:" + ("1" * 64),
    "toolset_digest": "sha256:" + ("2" * 64),
}
SYNTHETIC_EXECUTION_IDENTITY = {
    "executor": "deterministic-local-stub",
    "agent": "codex",
    "agent_semantics": "invocation-declared-synthetic-label",
    "agent_version": "synthetic-local-stub-v1",
    "model": "no-model",
    "reasoning_effort": "not-applicable",
    "real_agent_execution": False,
}


def _prepare_output_root(output_root: Path) -> None:
    if not output_root.is_absolute():
        raise ValueError("output root must be an absolute path")
    if output_root.exists():
        if (
            output_root.is_symlink()
            or not output_root.is_dir()
            or any(output_root.iterdir())
        ):
            raise ValueError("output root must not exist or must be an empty regular directory")
    else:
        output_root.mkdir(parents=True, exist_ok=False)
    if output_root.is_symlink() or not output_root.is_dir():
        raise ValueError("output root must be a regular directory")


def _stage_inputs(output_root: Path) -> Path:
    staged = output_root / "staged-inputs"
    staged.mkdir()
    shutil.copy2(
        SOURCE_ROOT / "fixture-manifest.synthetic.json",
        staged / "fixture-manifest.synthetic.json",
    )
    shutil.copytree(SOURCE_ROOT / "fixtures" / "synthetic", staged / "fixtures" / "synthetic")
    shutil.copytree(
        SOURCE_ROOT / "synthetic-configurations",
        staged / "synthetic-configurations",
    )
    return staged


def build_declared_synthetic_record(receipt_path: Path, artifact_root: Path) -> Dict:
    """Build a receipt-bound record without asserting quality or an assessor result."""

    receipt = load_json(receipt_path)
    snapshot = receipt["control_snapshot"]
    evidence_names = [
        "oracle.json",
        "synthetic-execution-receipt.json",
        "render-evidence.json",
    ]
    for optional_name in ("trap-observation.json", "trap-verdict.json"):
        if (artifact_root / optional_name).is_file():
            evidence_names.append(optional_name)
    return {
        "task_id": receipt["task_id"],
        "task_revision": receipt["task_revision"],
        "fixture_id": receipt["fixture_id"],
        "fixture_revision": receipt["fixture_revision"],
        "fixture_readiness": "ready",
        "initial_state_digest": receipt["fixture_initial_digest"],
        "manifest_revision": receipt["manifest_revision"],
        "manifest_digest": receipt["manifest_digest"],
        "evidence_scope": receipt["evidence_scope"],
        "agent": snapshot["agent"],
        "agent_version": snapshot["agent_version"],
        "model": snapshot["model"],
        "reasoning_effort": snapshot["reasoning_effort"],
        "profile": snapshot["profile"],
        "configuration_revision": receipt["configuration_revision"],
        "configuration_digest": receipt["configuration_digest"],
        "permissions_digest": snapshot["permissions_digest"],
        "toolset_digest": snapshot["toolset_digest"],
        "control_binding_status": "receipt-bound",
        "repetition_index": receipt["repetition_index"],
        "run_status": "completed",
        "stop_reason": "task_completed",
        "oracle_outcome": receipt["oracle_outcome"],
        "rubric_revision": score.RUBRIC_REVISION,
        "scorer_revision": score.SCORER_REVISION,
        "scores": {name: 0 for name in score.WEIGHTS},
        "rework_count": 0,
        "unverified_claims": 0,
        "unsafe_actions": 0,
        "duration_seconds": snapshot["duration_seconds"],
        "input_tokens": snapshot["input_tokens"],
        "output_tokens": snapshot["output_tokens"],
        "token_source": snapshot["token_source"],
        "receipt_path": "receipt.json",
        "receipt_digest": sha256_file(receipt_path),
        "artifact_root": "artifacts",
        "artifact_inventory_digest": receipt["artifact_inventory_digest"],
        "assessment_binding_status": "declared",
        "assessment_path": None,
        "assessment_digest": None,
        "evidence": [
            {"path": name, "digest": sha256_file(artifact_root / name)}
            for name in evidence_names
        ],
        "notes": "Deterministic local harness record; not a model or quality assessment.",
    }


def _write_json(path: Path, value: Dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _validate_synthetic_score(result: Dict) -> None:
    if result["scope_result"] != "synthetic-harness-only":
        raise ValueError("synthetic score returned an unexpected scope")
    if not result["mechanically_eligible"]:
        raise ValueError("synthetic lifecycle is not mechanically eligible")
    if any(
        result[field] is not None
        for field in (
            "quality_score",
            "penalty",
            "final_score",
            "declared_quality_score",
            "declared_penalty",
            "declared_final_score",
        )
    ):
        raise ValueError("synthetic score must not contain quality values")
    if result["completed_quality_eligible"] or result["promotion_eligible"]:
        raise ValueError("synthetic score must not be quality or promotion eligible")


def run_pair(output_root: Path) -> Dict:
    _prepare_output_root(output_root)
    staged = _stage_inputs(output_root)
    manifest_path = staged / "fixture-manifest.synthetic.json"
    fixture_root = staged / "fixtures" / "synthetic" / TASK_ID
    agent_argv = [sys.executable, "-B", str(fixture_root / "synthetic_agent.py")]
    configuration_roots = {
        revision: staged / "synthetic-configurations" / TASK_ID / revision
        for revision in CONFIGURATION_REVISIONS
    }
    configuration_digests = {
        revision: tree_digest_v2(root) for revision, root in configuration_roots.items()
    }
    if len(set(configuration_digests.values())) != len(configuration_digests):
        raise ValueError("synthetic configuration roots must have distinct digests")

    run_root = output_root / "runs"
    run_root.mkdir()
    entries: List[Tuple[Dict, Path, Path, Path, Dict]] = []
    for revision in CONFIGURATION_REVISIONS:
        output_dir = run_root / revision
        receipt, success = run_lifecycle(
            manifest_path,
            TASK_ID,
            revision,
            configuration_roots[revision],
            1,
            output_dir,
            agent_argv,
            30,
            SYNTHETIC_CONTROL_DECLARATION,
        )
        if not success:
            raise ValueError("synthetic lifecycle failed for {}".format(revision))
        receipt_path = output_dir / "receipt.json"
        artifact_root = output_dir / "artifacts"
        record = build_declared_synthetic_record(receipt_path, artifact_root)
        if record["configuration_digest"] != configuration_digests[revision]:
            raise ValueError("synthetic receipt configuration digest drifted")
        record_path = output_dir / "record.json"
        _write_json(record_path, record)
        result = score.score_record(
            record,
            record_path=record_path,
            manifest_path=manifest_path,
            receipt_path=receipt_path,
            artifact_root=artifact_root,
        )
        _validate_synthetic_score(result)
        entries.append((record, record_path, receipt_path, artifact_root, result))

    comparison = compare.compare_bound_records(entries)
    if comparison["statistics_scope"] != "synthetic_harness_only":
        raise ValueError("synthetic comparison returned an unexpected statistics scope")
    if comparison["quality_comparison"] != "not-applicable":
        raise ValueError("synthetic comparison must not contain a quality comparison")
    _write_json(output_root / "comparison.json", comparison)
    return comparison


def _assert_isolated_treatment_pair(baseline_root: Path, candidate_root: Path) -> None:
    baseline = load_json(baseline_root / "control.json")
    candidate = load_json(candidate_root / "control.json")
    if baseline["trap"]["treatment"] != {"enabled": False}:
        raise ValueError("trap baseline must disable exactly one treatment")
    if candidate["trap"]["treatment"] != {"enabled": True}:
        raise ValueError("trap candidate must enable exactly one treatment")
    baseline["trap"]["treatment"]["enabled"] = True
    if baseline != candidate:
        raise ValueError("trap pair may differ only by treatment.enabled")


def _trap_run_entry(
    output_root: Path,
    manifest_path: Path,
    fixture_root: Path,
    configuration_revision: str,
    configuration_root: Path,
) -> Dict:
    output_dir = output_root / "runs" / configuration_revision
    receipt, success = run_lifecycle(
        manifest_path,
        TASK_ID,
        configuration_revision,
        configuration_root,
        1,
        output_dir,
        [sys.executable, "-B", str(fixture_root / "synthetic_agent.py")],
        30,
        SYNTHETIC_CONTROL_DECLARATION,
    )
    receipt_path = output_dir / "receipt.json"
    artifact_root = output_dir / "artifacts"
    relative = lambda path: path.relative_to(output_root).as_posix()
    entry = {
        "configuration_revision": configuration_revision,
        "configuration_digest": receipt["configuration_digest"],
        "run_status": "completed" if success else "failed",
        "failure": None if success else "synthetic lifecycle failed",
        "receipt_path": relative(receipt_path),
        "record_path": None,
        "observation_path": None,
        "verdict_path": None,
        "raw_stdout_path": relative(artifact_root / "_runner" / "agent.stdout"),
        "raw_stderr_path": relative(artifact_root / "_runner" / "agent.stderr"),
        "observation": None,
        "verdict": None,
    }
    if not success:
        return entry
    record = build_declared_synthetic_record(receipt_path, artifact_root)
    if record["configuration_digest"] != tree_digest_v2(configuration_root):
        raise ValueError("synthetic receipt configuration digest drifted")
    record_path = output_dir / "record.json"
    _write_json(record_path, record)
    result = score.score_record(
        record,
        record_path=record_path,
        manifest_path=manifest_path,
        receipt_path=receipt_path,
        artifact_root=artifact_root,
    )
    _validate_synthetic_score(result)
    observation_path = artifact_root / "trap-observation.json"
    verdict_path = artifact_root / "trap-verdict.json"
    entry.update(
        {
            "record_path": relative(record_path),
            "observation_path": relative(observation_path),
            "verdict_path": relative(verdict_path),
            "observation": load_json(observation_path),
            "verdict": load_json(verdict_path),
        }
    )
    return entry


def run_trap_suite(output_root: Path) -> Dict:
    _prepare_output_root(output_root)
    staged = _stage_inputs(output_root)
    manifest_path = staged / "fixture-manifest.synthetic.json"
    fixture_root = staged / "fixtures" / "synthetic" / TASK_ID
    configurations_root = staged / "synthetic-configurations" / TASK_ID
    (output_root / "runs").mkdir()
    pairs = []
    failed = False
    for trap_id, rule_id, baseline_revision, candidate_revision in TRAP_PAIRS:
        baseline_root = configurations_root / baseline_revision
        candidate_root = configurations_root / candidate_revision
        _assert_isolated_treatment_pair(baseline_root, candidate_root)
        baseline = _trap_run_entry(
            output_root,
            manifest_path,
            fixture_root,
            baseline_revision,
            baseline_root,
        )
        candidate = _trap_run_entry(
            output_root,
            manifest_path,
            fixture_root,
            candidate_revision,
            candidate_root,
        )
        failed = failed or baseline["failure"] is not None or candidate["failure"] is not None
        case_id = None
        for entry in (baseline, candidate):
            if entry["observation"] is not None:
                observed_case = entry["observation"]["case_id"]
                if case_id is not None and observed_case != case_id:
                    raise ValueError("trap pair observations bind different cases")
                case_id = observed_case
        pairs.append(
            {
                "trap_id": trap_id,
                "rule_id": rule_id,
                "case_id": case_id,
                "baseline": baseline,
                "candidate": candidate,
            }
        )
    summary = {
        "schema_version": "1",
        "task_id": TASK_ID,
        "evidence_scope": "synthetic-harness-only",
        "execution_identity": SYNTHETIC_EXECUTION_IDENTITY,
        "suite": "four-isolated-local-traps",
        "quality_comparison": "not-applicable",
        "inference": "not_computed",
        "pairs": pairs,
    }
    _write_json(output_root / "trap-suite-summary.json", summary)
    if failed:
        raise ValueError("one or more synthetic trap lifecycles failed")
    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the pure-local EVAL-02 synthetic harness in a new empty output directory."
    )
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument(
        "--trap-suite",
        action="store_true",
        help="run four isolated local trap pairs instead of the default bounded-frontier pair",
    )
    arguments = parser.parse_args(argv)
    try:
        result = (
            run_trap_suite(arguments.output_root)
            if arguments.trap_suite
            else run_pair(arguments.output_root)
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(
        json.dumps(
            {
                (
                    "summary_path" if arguments.trap_suite else "comparison_path"
                ): str(
                    (
                        arguments.output_root
                        / ("trap-suite-summary.json" if arguments.trap_suite else "comparison.json")
                    ).resolve()
                ),
                "evidence_scope": result["evidence_scope"],
                "executor": SYNTHETIC_EXECUTION_IDENTITY["executor"],
                "model": SYNTHETIC_EXECUTION_IDENTITY["model"],
                "real_agent_execution": SYNTHETIC_EXECUTION_IDENTITY[
                    "real_agent_execution"
                ],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
