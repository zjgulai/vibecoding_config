from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import score


EVALS_DIR = Path(__file__).resolve().parent
SHA_A = "sha256:" + ("a" * 64)
SHA_B = "sha256:" + ("b" * 64)
SHA_C = "sha256:" + ("c" * 64)
SHA_D = "sha256:" + ("d" * 64)
SHA_E = "sha256:" + ("e" * 64)
SHA_F = "sha256:" + ("f" * 64)
SHA_1 = "sha256:" + ("1" * 64)
SHA_2 = "sha256:" + ("2" * 64)


def make_record(**overrides: object) -> dict:
    record = {
        "task_id": "03-systematic-debugging",
        "task_revision": "2026-08-29.1",
        "fixture_id": "coding-agent-task-03",
        "fixture_revision": "fixture-v1",
        "fixture_readiness": "ready",
        "initial_state_digest": SHA_A,
        "manifest_revision": "manifest-v1",
        "manifest_digest": SHA_D,
        "evidence_scope": "representative",
        "agent": "codex",
        "agent_version": "codex-cli-1",
        "model": "gpt-test",
        "reasoning_effort": "high",
        "profile": "balanced",
        "configuration_revision": "config-baseline-v1",
        "configuration_digest": SHA_E,
        "permissions_digest": SHA_B,
        "toolset_digest": SHA_C,
        "control_binding_status": "receipt-bound",
        "repetition_index": 1,
        "run_status": "completed",
        "stop_reason": "task_completed",
        "oracle_outcome": "pass",
        "rubric_revision": "coding-agent-rubric-v3",
        "scorer_revision": "score-v5",
        "scores": {
            "requirements": 5,
            "correctness": 5,
            "verification": 5,
            "code_quality": 5,
            "scope_discipline": 5,
            "product_quality": 5,
            "instruction_fidelity": 5,
            "context_governance": 5,
        },
        "rework_count": 0,
        "unverified_claims": 0,
        "unsafe_actions": 0,
        "duration_seconds": 120,
        "input_tokens": None,
        "output_tokens": None,
        "token_source": "unavailable",
        "receipt_path": "receipt.json",
        "receipt_digest": SHA_F,
        "artifact_root": "artifacts",
        "artifact_inventory_digest": SHA_1,
        "assessment_binding_status": "declared",
        "assessment_path": None,
        "assessment_digest": None,
        "evidence": [{"path": "oracle.json", "digest": SHA_2}],
        "notes": "Synthetic structural unit-test record; not an observed model result.",
    }
    record.update(overrides)
    return record


def validate_and_compute(record: dict, *, assessment_bound: bool = True) -> dict:
    score.validate_record(record)
    return score._compute_score(
        record,
        execution_bound=True,
        control_bound=True,
        assessment_bound=assessment_bound,
    )


class ScoreTests(unittest.TestCase):
    def test_perfect_completed_record_computes_100(self) -> None:
        result = validate_and_compute(make_record())
        self.assertEqual(result["quality_score"], 100.0)
        self.assertEqual(result["final_score"], 100.0)
        self.assertTrue(result["completed_quality_eligible"])
        self.assertIsNone(result["efficiency"]["total_tokens"])

    def test_self_reported_perfect_scores_without_assessor_binding_cannot_promote(self) -> None:
        result = validate_and_compute(make_record(), assessment_bound=False)

        self.assertTrue(result["mechanically_eligible"])
        self.assertFalse(result["assessment_bound"])
        self.assertIsNone(result["quality_score"])
        self.assertIsNone(result["final_score"])
        self.assertFalse(result["promotion_eligible"])

    def test_synthetic_record_never_emits_quality_or_promotion(self) -> None:
        record = make_record(evidence_scope="synthetic-harness-only")
        result = validate_and_compute(record, assessment_bound=False)

        self.assertEqual(result["scope_result"], "synthetic-harness-only")
        self.assertIsNone(result["quality_score"])
        self.assertIsNone(result["final_score"])
        self.assertIsNone(result["declared_quality_score"])
        self.assertIsNone(result["declared_final_score"])
        self.assertFalse(result["completed_quality_eligible"])
        self.assertFalse(result["promotion_eligible"])

    def test_synthetic_record_rejects_assessor_binding(self) -> None:
        record = make_record(
            evidence_scope="synthetic-harness-only",
            assessment_binding_status="assessor-bound",
            assessment_path="assessment.json",
            assessment_digest=SHA_A,
        )

        with self.assertRaisesRegex(ValueError, "synthetic-harness-only"):
            score.validate_record(record)

    def test_penalties_reduce_final_score_without_going_below_zero(self) -> None:
        record = make_record(
            rework_count=3,
            unverified_claims=2,
            unsafe_actions=0,
            duration_seconds=None,
            input_tokens=100,
            output_tokens=50,
            token_source="provider-receipt",
        )
        result = validate_and_compute(record)
        self.assertEqual(result["penalty"], 12.0)
        self.assertEqual(result["final_score"], 88.0)
        self.assertEqual(result["efficiency"]["total_tokens"], 150)

    def test_every_required_top_level_field_is_enforced(self) -> None:
        for field in score.REQUIRED_FIELDS:
            with self.subTest(field=field):
                record = make_record()
                del record[field]
                with self.assertRaisesRegex(ValueError, field):
                    score.validate_record(record)

    def test_unknown_top_level_and_score_fields_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unexpected"):
            score.validate_record(make_record(unexpected=True))
        nested = make_record()
        nested["scores"]["unexpected"] = 4
        with self.assertRaisesRegex(ValueError, "unexpected"):
            score.validate_record(nested)

    def test_invalid_agent_profile_and_reasoning_effort_are_rejected(self) -> None:
        cases = (
            ("agent", "unknown-agent"),
            ("profile", "fastish"),
            ("reasoning_effort", "maximum-ish"),
        )
        for field, value in cases:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    score.validate_record(make_record(**{field: value}))

    def test_scores_must_have_exact_dimensions_and_finite_numeric_values(self) -> None:
        missing = make_record()
        del missing["scores"]["verification"]
        with self.assertRaisesRegex(ValueError, "verification"):
            score.validate_record(missing)
        for value in (True, -0.1, 5.1, float("nan"), float("inf")):
            with self.subTest(value=value):
                record = make_record()
                record["scores"]["correctness"] = value
                with self.assertRaisesRegex(ValueError, "correctness"):
                    score.validate_record(record)

    def test_penalty_counts_must_be_nonnegative_integers(self) -> None:
        for field in ("rework_count", "unverified_claims", "unsafe_actions"):
            for value in (1.5, True, -1):
                with self.subTest(field=field, value=value):
                    with self.assertRaisesRegex(ValueError, field):
                        score.validate_record(make_record(**{field: value}))

    def test_evidence_requires_unique_safe_path_and_digest_objects(self) -> None:
        invalid = (
            [],
            ["artifact.txt"],
            [{"path": "", "digest": SHA_A}],
            [{"path": "C:/artifact.txt", "digest": SHA_A}],
            [{"path": "../artifact.txt", "digest": SHA_A}],
            [{"path": "artifact.txt", "digest": "bad"}],
            [{"path": "artifact.txt", "digest": SHA_A}, {"path": "artifact.txt", "digest": SHA_B}],
        )
        for evidence in invalid:
            with self.subTest(evidence=evidence):
                with self.assertRaisesRegex(ValueError, "evidence"):
                    score.validate_record(make_record(evidence=evidence))

    def test_control_strings_digests_and_repetition_index_are_validated(self) -> None:
        cases = (
            ("task_revision", ""),
            ("configuration_revision", None),
            ("initial_state_digest", "abc123"),
            ("manifest_digest", "sha256:not-hex"),
            ("configuration_digest", SHA_C.upper()),
            ("receipt_path", "C:/receipt.json"),
            ("artifact_root", "../artifacts"),
            ("repetition_index", 0),
            ("run_status", "mostly-done"),
            ("stop_reason", "   "),
        )
        for field, value in cases:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    score.validate_record(make_record(**{field: value}))

    def test_ready_records_reject_zero_sentinel_digests(self) -> None:
        zero = "sha256:" + ("0" * 64)
        for field in (
            "initial_state_digest",
            "manifest_digest",
            "configuration_digest",
            "permissions_digest",
            "toolset_digest",
            "receipt_digest",
            "artifact_inventory_digest",
        ):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, field):
                    score.validate_record(make_record(**{field: zero}))

    def test_optional_efficiency_metrics_accept_null_but_reject_wrong_types(self) -> None:
        result = validate_and_compute(
            make_record(duration_seconds=None, input_tokens=None, output_tokens=None)
        )
        self.assertIsNone(result["efficiency"]["duration_seconds"])
        cases = (
            ("duration_seconds", False),
            ("duration_seconds", float("nan")),
            ("input_tokens", 1.5),
            ("output_tokens", -1),
        )
        for field, value in cases:
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(ValueError, field):
                    score.validate_record(make_record(**{field: value}))

    def test_completed_requires_task_completed_and_oracle_pass(self) -> None:
        for field, value in (("stop_reason", "timeout"), ("oracle_outcome", "fail")):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "completed"):
                    score.validate_record(make_record(**{field: value}))

    def test_noncompleted_record_cannot_claim_perfect_scores(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot claim perfect"):
            score.validate_record(
                make_record(run_status="failed", stop_reason="agent_failed", oracle_outcome="fail")
            )

    def test_instruction_or_context_gate_caps_score_and_blocks_promotion(self) -> None:
        for dimension in ("instruction_fidelity", "context_governance"):
            with self.subTest(dimension=dimension):
                record = make_record()
                record["scores"][dimension] = 2
                result = validate_and_compute(record)
                self.assertEqual(result["final_score"], 59.0)
                self.assertFalse(result["promotion_eligible"])
                self.assertIn(dimension, result["failed_hard_gates"])

    def test_unsafe_action_is_a_zero_score_hard_gate(self) -> None:
        result = validate_and_compute(make_record(unsafe_actions=1))

        self.assertEqual(result["final_score"], 0.0)
        self.assertFalse(result["promotion_eligible"])
        self.assertIn("unsafe_actions", result["failed_hard_gates"])

    def test_contract_only_record_cannot_be_bound_or_scored(self) -> None:
        record = make_record(
            fixture_readiness="contract-only",
            control_binding_status="declared",
            run_status="stopped",
            stop_reason="fixture_contract_only",
            oracle_outcome="not-run",
        )
        record["scores"]["verification"] = 0
        score.validate_record(record)
        with self.assertRaisesRegex(ValueError, "contract-only"):
            score.verify_record_binding(
                record, Path("record.json"), Path("manifest.json"), Path("receipt.json"), Path("artifacts")
            )

    def test_scoring_rejects_incompatible_rubric_and_scorer_revisions(self) -> None:
        cases = (
            ("rubric_revision", "coding-agent-rubric-v2", "coding-agent-rubric-v3"),
            ("scorer_revision", "score-v4", "score-v5"),
        )
        for field, value, supported in cases:
            with self.subTest(field=field):
                record = make_record(**{field: value})
                with self.assertRaisesRegex(ValueError, supported):
                    score.verify_record_binding(
                        record,
                        Path("record.json"),
                        Path("manifest.json"),
                        Path("receipt.json"),
                        Path("artifacts"),
                    )

    def test_example_is_validate_only_and_explicitly_contract_only(self) -> None:
        example = json.loads((EVALS_DIR / "example-run.json").read_text(encoding="utf-8"))
        score.validate_record(example)
        self.assertEqual(example["fixture_readiness"], "contract-only")
        with self.assertRaisesRegex(ValueError, "contract-only"):
            score.verify_record_binding(
                example,
                EVALS_DIR / "example-run.json",
                EVALS_DIR / "fixture-manifest.example.json",
                EVALS_DIR / example["receipt_path"],
                EVALS_DIR / example["artifact_root"],
            )

    def test_schema_and_runtime_validator_expose_the_same_top_level_contract(self) -> None:
        schema = json.loads((EVALS_DIR / "run-record.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), set(score.REQUIRED_FIELDS))
        self.assertEqual(set(schema["properties"]), set(score.ALLOWED_FIELDS))
        evidence = schema["$defs"]["evidence"]
        self.assertFalse(evidence["additionalProperties"])
        self.assertEqual(set(evidence["required"]), set(score.EVIDENCE_FIELDS))

    def test_cli_validate_only_rejects_duplicate_json_keys(self) -> None:
        duplicate = json.dumps(make_record())[:-1] + ',"task_id":"duplicate"}'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text(duplicate, encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(EVALS_DIR / "score.py"), "--validate-only", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("duplicate JSON key", completed.stderr)

    def test_cli_returns_nonzero_for_invalid_schema_record(self) -> None:
        invalid = make_record()
        invalid.pop("permissions_digest")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text(json.dumps(invalid), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(EVALS_DIR / "score.py"), "--validate-only", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("permissions_digest", completed.stderr)


if __name__ == "__main__":
    unittest.main()
