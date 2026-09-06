from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import assessment


EVALS_DIR = Path(__file__).resolve().parent
SHA_A = "sha256:" + ("a" * 64)


def make_assessment() -> dict:
    evidence = {
        "path": "oracle.json",
        "digest": SHA_A,
        "claim": "The cited artifact supports this synthetic criterion.",
    }
    return {
        "schema_version": "1",
        "assessment_revision": "coding-agent-assessment-v1",
        "rubric_revision": "coding-agent-rubric-v3",
        "assessor": "independent-reviewer",
        "assessor_version": "reviewer-v1",
        "assessor_independence": "independent-agent",
        "task_id": "03-systematic-debugging",
        "task_revision": "2026-08-29.1",
        "fixture_id": "coding-agent-task-03",
        "fixture_revision": "fixture-v1",
        "repetition_index": 1,
        "receipt_digest": SHA_A,
        "artifact_inventory_digest": SHA_A,
        "control_snapshot_digest": SHA_A,
        "dimensions": {
            name: {
                "score": 4,
                "rationale": "Synthetic rationale for {}.".format(name),
                "evidence": [copy.deepcopy(evidence)],
            }
            for name in assessment.SCORE_DIMENSIONS
        },
        "counters": {
            name: {
                "value": 0,
                "rationale": "Synthetic audit for {}.".format(name),
                "evidence": [copy.deepcopy(evidence)],
            }
            for name in assessment.COUNTER_NAMES
        },
    }


class AssessmentTests(unittest.TestCase):
    def test_complete_dimension_and_counter_evidence_contract_is_valid(self) -> None:
        assessment.validate_assessment(make_assessment())

    def test_missing_or_empty_criterion_evidence_is_rejected(self) -> None:
        cases = []
        missing_dimension = make_assessment()
        del missing_dimension["dimensions"]["correctness"]
        cases.append((missing_dimension, "correctness"))
        empty_dimension_evidence = make_assessment()
        empty_dimension_evidence["dimensions"]["verification"]["evidence"] = []
        cases.append((empty_dimension_evidence, "verification"))
        empty_counter_evidence = make_assessment()
        empty_counter_evidence["counters"]["unsafe_actions"]["evidence"] = []
        cases.append((empty_counter_evidence, "unsafe_actions"))
        for value, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, expected):
                    assessment.validate_assessment(value)

    def test_assessment_schema_and_runtime_have_matching_closed_contracts(self) -> None:
        schema = json.loads(
            (EVALS_DIR / "assessment.schema.json").read_text(encoding="utf-8")
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), set(assessment.ASSESSMENT_FIELDS))
        self.assertEqual(set(schema["properties"]), set(assessment.ASSESSMENT_FIELDS))
        dimension = schema["$defs"]["dimension"]
        counter = schema["$defs"]["counter"]
        evidence = schema["$defs"]["evidence"]
        self.assertEqual(set(dimension["required"]), set(assessment.DIMENSION_FIELDS))
        self.assertEqual(set(counter["required"]), set(assessment.COUNTER_FIELDS))
        self.assertEqual(set(evidence["required"]), set(assessment.EVIDENCE_FIELDS))

    def test_control_snapshot_digest_is_canonical_across_key_order(self) -> None:
        first = {"agent": "codex", "model": "gpt-test"}
        second = {"model": "gpt-test", "agent": "codex"}

        self.assertEqual(
            assessment.canonical_object_digest(first),
            assessment.canonical_object_digest(second),
        )


if __name__ == "__main__":
    unittest.main()
