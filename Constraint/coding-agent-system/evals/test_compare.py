from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Tuple

import eval_protocol

from test_binding import (
    create_bound_run,
    create_ready_manifest,
    synchronize_bound_record,
)


EVALS_DIR = Path(__file__).resolve().parent


def make_bound_records(base: Path, specifications: List[Tuple[str, int, Dict]]):
    manifest = create_ready_manifest(base)
    bindings = []
    for index, (configuration, repetition, overrides) in enumerate(specifications, start=1):
        _, receipt, artifacts, record_path, record = create_bound_run(
            base,
            configuration,
            repetition,
            manifest_path=manifest,
            bundle_name="bundle-{}".format(index),
        )
        for key, value in overrides.items():
            if key == "scores":
                record["scores"].update(value)
            else:
                record[key] = value
        synchronize_bound_record(receipt, artifacts, record)
        record_path.write_text(json.dumps(record), encoding="utf-8")
        bindings.append((receipt, artifacts, record_path))
    return manifest, bindings


def run_compare(manifest: Path, bindings):
    command = [sys.executable, str(EVALS_DIR / "compare.py"), "--manifest", str(manifest)]
    for receipt, _, _ in bindings:
        command.extend(["--receipt", str(receipt)])
    for _, artifacts, _ in bindings:
        command.extend(["--artifact-root", str(artifacts)])
    command.extend(str(record) for _, _, record in bindings)
    return subprocess.run(command, capture_output=True, text=True, check=False)


class CompareCliTests(unittest.TestCase):
    def test_rejects_assessor_control_drift_between_paired_groups(self) -> None:
        drift_cases = {
            "assessor": "different-independent-reviewer",
            "assessor_version": "reviewer-v2",
            "assessor_independence": "human",
        }
        for field, value in drift_cases.items():
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as directory:
                    manifest, bindings = make_bound_records(
                        Path(directory),
                        [("config-a", 1, {}), ("config-b", 1, {})],
                    )
                    second_record_path = bindings[1][2]
                    second_record = json.loads(
                        second_record_path.read_text(encoding="utf-8")
                    )
                    assessment_path = (
                        second_record_path.parent / second_record["assessment_path"]
                    )
                    assessment = json.loads(
                        assessment_path.read_text(encoding="utf-8")
                    )
                    assessment[field] = value
                    assessment_path.write_text(
                        json.dumps(assessment, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                    second_record["assessment_digest"] = eval_protocol.sha256_file(
                        assessment_path
                    )
                    second_record_path.write_text(
                        json.dumps(second_record), encoding="utf-8"
                    )
                    completed = run_compare(manifest, bindings)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("control variable drift", completed.stderr)
                self.assertIn(field, completed.stderr)

    def test_rejects_declared_only_assessment_from_quality_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            manifest = create_ready_manifest(base)
            first = create_bound_run(
                base,
                "config-a",
                1,
                manifest_path=manifest,
                bundle_name="declared-a",
                assessment_bound=False,
            )
            second = create_bound_run(
                base,
                "config-b",
                1,
                manifest_path=manifest,
                bundle_name="bound-b",
            )
            completed = run_compare(
                manifest,
                [(first[1], first[2], first[3]), (second[1], second[2], second[3])],
            )

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("assessor-bound", completed.stderr)

    def test_reports_paired_descriptive_quality_and_available_efficiency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, bindings = make_bound_records(
                Path(directory),
                [
                    ("config-a", 1, {"duration_seconds": 10}),
                    ("config-a", 2, {"duration_seconds": 20, "rework_count": 1}),
                    ("config-b", 1, {"duration_seconds": 12, "unverified_claims": 1}),
                    ("config-b", 2, {"duration_seconds": 22}),
                ],
            )
            completed = run_compare(manifest, bindings)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["statistics_scope"], "descriptive_paired_only")
        self.assertEqual(result["inference"], "not_computed")
        self.assertEqual([group["n"] for group in result["groups"]], [2, 2])
        self.assertEqual([pair["repetition_index"] for pair in result["paired"]], [1, 2])
        self.assertEqual(result["paired_delta"]["n"], 2)
        self.assertEqual(result["groups"][1]["efficiency"]["duration_seconds"]["n"], 2)
        self.assertEqual(
            result["control"]["assessor_control"]["assessor"],
            "synthetic-independent-test-assessor",
        )

    def test_rejects_unpaired_repetition_sets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, bindings = make_bound_records(
                Path(directory),
                [("config-a", 1, {}), ("config-a", 2, {}), ("config-b", 1, {})],
            )
            completed = run_compare(manifest, bindings)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("paired repetition_index", completed.stderr)

    def test_requires_exactly_two_configuration_revisions(self) -> None:
        cases = [
            [("config-a", 1, {})],
            [("config-a", 1, {}), ("config-b", 1, {}), ("config-c", 1, {})],
        ]
        for specifications in cases:
            with self.subTest(group_count=len(specifications)):
                with tempfile.TemporaryDirectory() as directory:
                    manifest, bindings = make_bound_records(Path(directory), specifications)
                    completed = run_compare(manifest, bindings)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("exactly two", completed.stderr)

    def test_rejects_duplicate_repetition_within_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, bindings = make_bound_records(
                Path(directory),
                [("config-a", 1, {}), ("config-a", 1, {}), ("config-b", 1, {})],
            )
            completed = run_compare(manifest, bindings)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("duplicate repetition_index", completed.stderr)

    def test_rejects_control_variable_drift(self) -> None:
        drift_cases = {
            "agent": "claude-code",
            "agent_version": "other-version",
            "model": "other-model",
            "reasoning_effort": "medium",
            "profile": "quality",
            "permissions_digest": "sha256:" + ("e" * 64),
            "toolset_digest": "sha256:" + ("f" * 64),
        }
        for field, value in drift_cases.items():
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as directory:
                    manifest, bindings = make_bound_records(
                        Path(directory),
                        [("config-a", 1, {}), ("config-b", 1, {field: value})],
                    )
                    completed = run_compare(manifest, bindings)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("control variable drift", completed.stderr)
                self.assertIn(field, completed.stderr)

    def test_noncompleted_record_is_not_in_completed_quality_or_paired_outcome(self) -> None:
        failed_scores = {key: 4 for key in (
            "requirements", "correctness", "verification", "code_quality", "scope_discipline", "product_quality",
            "instruction_fidelity", "context_governance"
        )}
        with tempfile.TemporaryDirectory() as directory:
            manifest, bindings = make_bound_records(
                Path(directory),
                [
                    ("config-a", 1, {}),
                    ("config-b", 1, {
                        "run_status": "failed",
                        "stop_reason": "agent_failed",
                        "scores": failed_scores,
                    }),
                ],
            )
            completed = run_compare(manifest, bindings)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        failed_group = result["groups"][1]
        self.assertEqual(failed_group["completed_quality"]["n"], 0)
        self.assertEqual(result["paired"][0]["configuration_b_outcome_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
