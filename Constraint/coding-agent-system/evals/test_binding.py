from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import assessment as assessment_module
import eval_protocol
import receipt as receipt_module
import run_lifecycle
import validate_fixture
from test_fixture_manifest import make_manifest


EVALS_DIR = Path(__file__).resolve().parent


def create_ready_manifest(
    base: Path,
    *,
    evidence_scope: str = "representative",
    task_id: str = "03-systematic-debugging",
) -> Path:
    manifest = make_manifest(readiness="ready", evidence_scope=evidence_scope)
    if evidence_scope == "synthetic-harness-only":
        manifest["fixtures"] = [
            fixture for fixture in manifest["fixtures"] if fixture["task_id"] == task_id
        ]
    for index, fixture in enumerate(manifest["fixtures"], start=1):
        root = base / "fixture-{}".format(index)
        root.mkdir()
        control = root / "fixture-control"
        control.write_text(
            "#!/bin/sh\n"
            "set -eu\n"
            "if [ \"$1\" = oracle ]; then\n"
            "  printf '{\"passed\":true}\\n' > \"$3/oracle.json\"\n"
            "fi\n",
            encoding="utf-8",
        )
        control.chmod(0o755)
        fixture["root"] = root.name
        fixture["initial_state_digest"] = validate_fixture.tree_digest(root)
    manifest_path = base / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


def create_bound_run(
    base: Path,
    configuration_revision: str = "config-a",
    repetition: int = 1,
    manifest_path: Path = None,
    bundle_name: str = None,
    assessment_bound: bool = True,
    task_id: str = "03-systematic-debugging",
    evidence_scope: str = "representative",
):
    manifest_path = manifest_path or create_ready_manifest(
        base,
        evidence_scope=evidence_scope,
        task_id=task_id,
    )
    configuration_root = base / "configurations" / configuration_revision
    configuration_root.mkdir(parents=True, exist_ok=True)
    config_file = configuration_root / "AGENTS.md"
    if not config_file.exists():
        config_file.write_text(configuration_revision + "\n", encoding="utf-8")
    agent = base / "agent.py"
    agent.write_text(
        "from pathlib import Path\n"
        "import os\n"
        "Path(os.environ['EVAL_ARTIFACT_ROOT'], 'agent.txt').write_text('done\\n')\n",
        encoding="utf-8",
    )
    output_dir = base / "runs" / (
        bundle_name or "{}-{}".format(configuration_revision, repetition)
    )
    receipt, success = run_lifecycle.run_lifecycle(
        manifest_path,
        task_id,
        configuration_revision,
        configuration_root,
        repetition,
        output_dir,
        [sys.executable, str(agent)],
        30,
        {
            "agent": "codex",
            "agent_version": "local-test-agent-v1",
            "model": "local-no-model-command",
            "reasoning_effort": "not-applicable",
            "profile": "custom",
            "permissions_digest": "sha256:" + ("b" * 64),
            "toolset_digest": "sha256:" + ("c" * 64),
        },
    )
    if not success:
        raise AssertionError("fake lifecycle did not complete")
    receipt_path = output_dir / "receipt.json"
    artifact_root = output_dir / "artifacts"
    snapshot = receipt["control_snapshot"]
    record = {
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
        "configuration_revision": configuration_revision,
        "configuration_digest": receipt["configuration_digest"],
        "permissions_digest": snapshot["permissions_digest"],
        "toolset_digest": snapshot["toolset_digest"],
        "control_binding_status": "receipt-bound",
        "repetition_index": repetition,
        "run_status": "completed",
        "stop_reason": "task_completed",
        "oracle_outcome": receipt["oracle_outcome"],
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
        "duration_seconds": snapshot["duration_seconds"],
        "input_tokens": snapshot["input_tokens"],
        "output_tokens": snapshot["output_tokens"],
        "token_source": snapshot["token_source"],
        "receipt_path": "receipt.json",
        "receipt_digest": eval_protocol.sha256_file(receipt_path),
        "artifact_root": "artifacts",
        "artifact_inventory_digest": receipt["artifact_inventory_digest"],
        "assessment_binding_status": "declared",
        "assessment_path": None,
        "assessment_digest": None,
        "evidence": [
            {
                "path": "oracle.json",
                "digest": eval_protocol.sha256_file(artifact_root / "oracle.json"),
            }
        ],
        "notes": "Synthetic local command fixture; no model or network call.",
    }
    if assessment_bound:
        bind_assessment(output_dir, artifact_root, record, receipt)
    record_path = output_dir / "record.json"
    record_path.write_text(json.dumps(record), encoding="utf-8")
    return manifest_path, receipt_path, artifact_root, record_path, record


def bind_assessment(
    output_dir: Path,
    artifact_root: Path,
    record: dict,
    receipt: dict,
) -> Path:
    evidence = {
        "path": "oracle.json",
        "digest": eval_protocol.sha256_file(artifact_root / "oracle.json"),
        "claim": "Synthetic oracle evidence for the named criterion.",
    }
    value = {
        "schema_version": "1",
        "assessment_revision": "coding-agent-assessment-v1",
        "rubric_revision": record["rubric_revision"],
        "assessor": "synthetic-independent-test-assessor",
        "assessor_version": "test-v1",
        "assessor_independence": "independent-agent",
        "task_id": record["task_id"],
        "task_revision": record["task_revision"],
        "fixture_id": record["fixture_id"],
        "fixture_revision": record["fixture_revision"],
        "repetition_index": record["repetition_index"],
        "receipt_digest": record["receipt_digest"],
        "artifact_inventory_digest": record["artifact_inventory_digest"],
        "control_snapshot_digest": assessment_module.canonical_object_digest(
            receipt["control_snapshot"]
        ),
        "dimensions": {
            name: {
                "score": score_value,
                "rationale": "Synthetic test rationale for {}.".format(name),
                "evidence": [dict(evidence)],
            }
            for name, score_value in record["scores"].items()
        },
        "counters": {
            name: {
                "value": record[name],
                "rationale": "Synthetic test audit for {}.".format(name),
                "evidence": [dict(evidence)],
            }
            for name in ("rework_count", "unverified_claims", "unsafe_actions")
        },
    }
    assessment_path = output_dir / "assessment.json"
    assessment_path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    record["assessment_binding_status"] = "assessor-bound"
    record["assessment_path"] = "assessment.json"
    record["assessment_digest"] = eval_protocol.sha256_file(assessment_path)
    return assessment_path


def synchronize_bound_record(
    receipt_path: Path,
    artifact_root: Path,
    record: dict,
) -> None:
    """Keep synthetic receipt/assessment bindings coherent after test overrides."""

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    snapshot = receipt["control_snapshot"]
    for field in (
        "agent",
        "agent_version",
        "model",
        "reasoning_effort",
        "profile",
        "permissions_digest",
        "toolset_digest",
        "duration_seconds",
        "input_tokens",
        "output_tokens",
        "token_source",
    ):
        snapshot[field] = record[field]
    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    record["receipt_digest"] = eval_protocol.sha256_file(receipt_path)

    assessment_path = receipt_path.parent / record["assessment_path"]
    value = json.loads(assessment_path.read_text(encoding="utf-8"))
    value["receipt_digest"] = record["receipt_digest"]
    value["control_snapshot_digest"] = assessment_module.canonical_object_digest(snapshot)
    for name, score_value in record["scores"].items():
        value["dimensions"][name]["score"] = score_value
    for name in ("rework_count", "unverified_claims", "unsafe_actions"):
        value["counters"][name]["value"] = record[name]
    assessment_path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    record["assessment_digest"] = eval_protocol.sha256_file(assessment_path)


def run_score(manifest: Path, receipt: Path, artifacts: Path, record: Path):
    return subprocess.run(
        [
            sys.executable,
            str(EVALS_DIR / "score.py"),
            "--manifest",
            str(manifest),
            "--receipt",
            str(receipt),
            "--artifact-root",
            str(artifacts),
            str(record),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


class BindingTests(unittest.TestCase):
    def test_score_requires_matching_manifest_receipt_and_artifact_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record, _ = create_bound_run(Path(directory))
            completed = run_score(manifest, receipt, artifacts, record)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["final_score"], 100.0)
        self.assertTrue(result["assessment_bound"])
        self.assertTrue(result["promotion_eligible"])
        self.assertEqual(
            result["assessor_control"],
            {
                "assessor": "synthetic-independent-test-assessor",
                "assessor_version": "test-v1",
                "assessor_independence": "independent-agent",
            },
        )

    def test_oracle_pass_and_self_reported_perfect_scores_cannot_promote(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record, _ = create_bound_run(
                Path(directory), assessment_bound=False
            )
            completed = run_score(manifest, receipt, artifacts, record)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertTrue(result["mechanically_eligible"])
        self.assertFalse(result["assessment_bound"])
        self.assertIsNone(result["quality_score"])
        self.assertIsNone(result["final_score"])
        self.assertFalse(result["promotion_eligible"])

    def test_record_control_drift_is_rejected_against_receipt_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record_path, record = create_bound_run(
                Path(directory)
            )
            record["model"] = "self-reported-different-model"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, record_path)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("control_snapshot", completed.stderr)

    def test_record_evidence_scope_drift_is_rejected_against_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record_path, record = create_bound_run(
                Path(directory)
            )
            record["evidence_scope"] = "synthetic-harness-only"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, record_path)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("evidence_scope", completed.stderr)

    def test_assessment_requires_evidence_for_every_dimension(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record_path, record = create_bound_run(
                Path(directory)
            )
            assessment_path = record_path.parent / record["assessment_path"]
            value = json.loads(assessment_path.read_text(encoding="utf-8"))
            value["dimensions"]["requirements"]["evidence"] = []
            assessment_path.write_text(json.dumps(value), encoding="utf-8")
            record["assessment_digest"] = eval_protocol.sha256_file(assessment_path)
            record_path.write_text(json.dumps(record), encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, record_path)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("dimensions.requirements.evidence", completed.stderr)

    def test_self_reported_unsafe_action_count_cannot_override_assessor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record_path, record = create_bound_run(
                Path(directory)
            )
            record["unsafe_actions"] = 1
            record_path.write_text(json.dumps(record), encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, record_path)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("unsafe_actions does not match assessment", completed.stderr)

    def test_contract_only_record_cannot_be_promoted_by_flipping_self_reported_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            manifest, receipt, artifacts, _, _ = create_bound_run(base)
            forged = json.loads((EVALS_DIR / "example-run.json").read_text(encoding="utf-8"))
            forged["fixture_readiness"] = "ready"
            forged["run_status"] = "completed"
            forged["stop_reason"] = "task_completed"
            forged["oracle_outcome"] = "pass"
            forged["scores"] = {key: 5 for key in forged["scores"]}
            forged["evidence"] = [{"path": "oracle.json", "digest": "sha256:" + ("0" * 64)}]
            forged_path = receipt.parent / "forged.json"
            forged_path.write_text(json.dumps(forged), encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, forged_path)

        self.assertNotEqual(completed.returncode, 0)
        self.assertRegex(completed.stderr, "digest|manifest|receipt|fixture")

    def test_artifact_tampering_invalidates_bound_score(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record, _ = create_bound_run(Path(directory))
            (artifacts / "oracle.json").write_text("tampered\n", encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, record)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("artifact inventory digest mismatch", completed.stderr)

    def test_artifact_git_injection_invalidates_bound_score(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record, _ = create_bound_run(Path(directory))
            injected = artifacts / ".git/post-run-injection.txt"
            injected.parent.mkdir()
            injected.write_text("injected\n", encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, record)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("artifact inventory digest mismatch", completed.stderr)

    def test_scorer_rechecks_forbidden_artifact_contract_after_digest_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt_path, artifacts, record_path, record = create_bound_run(
                Path(directory)
            )
            forbidden = artifacts / "credentials/injected.txt"
            forbidden.parent.mkdir()
            forbidden.write_text("DUMMY_REVIEW_VALUE\n", encoding="utf-8")
            receipt_value = json.loads(receipt_path.read_text(encoding="utf-8"))
            current_digest = eval_protocol.artifact_tree_digest_v2(artifacts)
            receipt_value["artifact_inventory_digest"] = current_digest
            receipt_path.write_text(
                json.dumps(receipt_value, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            record["artifact_inventory_digest"] = current_digest
            record["receipt_digest"] = eval_protocol.sha256_file(receipt_path)
            record_path.write_text(json.dumps(record), encoding="utf-8")
            completed = run_score(manifest, receipt_path, artifacts, record_path)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("artifact contract", completed.stderr)

    def test_receipt_rejects_runner_impossible_lifecycle_and_top_level_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            _, receipt_path, _, _, _ = create_bound_run(Path(directory))
            baseline = json.loads(receipt_path.read_text(encoding="utf-8"))
            cases = []
            missing_reset = json.loads(json.dumps(baseline))
            missing_reset["steps"]["reset"].update(
                {
                    "executed": False,
                    "exit_code": None,
                    "timed_out": False,
                    "stdout": None,
                    "stderr": None,
                }
            )
            cases.append(missing_reset)
            mismatched_agent = json.loads(json.dumps(baseline))
            mismatched_agent["agent_argv"] = ["different-agent"]
            cases.append(mismatched_agent)
            wrong_artifact_root = json.loads(json.dumps(baseline))
            wrong_artifact_root["artifact_root"] = "elsewhere"
            cases.append(wrong_artifact_root)

            for value in cases:
                with self.subTest(value=value):
                    with self.assertRaises(ValueError):
                        receipt_module.validate_receipt(value)

    def test_receipt_tampering_invalidates_bound_score(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest, receipt, artifacts, record, _ = create_bound_run(Path(directory))
            value = json.loads(receipt.read_text(encoding="utf-8"))
            value["configuration_revision"] = "tampered"
            receipt.write_text(json.dumps(value), encoding="utf-8")
            completed = run_score(manifest, receipt, artifacts, record)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("receipt_digest mismatch", completed.stderr)


if __name__ == "__main__":
    unittest.main()
