from __future__ import annotations

import subprocess
import sys
import json
import os
import tempfile
import unittest
from pathlib import Path

import validate_fixture
import receipt
from test_fixture_manifest import make_manifest


EVALS_DIR = Path(__file__).resolve().parent


class LifecycleRunnerTests(unittest.TestCase):
    def test_runner_requires_explicit_agent_argv(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(EVALS_DIR / "run_lifecycle.py"), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        for option in (
            "--agent",
            "--agent-version",
            "--model",
            "--reasoning-effort",
            "--profile",
            "--permissions-digest",
            "--toolset-digest",
            "--agent-command",
        ):
            with self.subTest(option=option):
                self.assertIn(option, completed.stdout)

    def test_contract_only_manifest_is_rejected_before_agent_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            manifest_path = base / "manifest.json"
            manifest_path.write_text(json.dumps(make_manifest()), encoding="utf-8")
            configuration_root = base / "configuration"
            configuration_root.mkdir()
            marker = base / "agent-ran"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(EVALS_DIR / "run_lifecycle.py"),
                    "--manifest",
                    str(manifest_path),
                    "--task-id",
                    "03-systematic-debugging",
                    "--configuration-revision",
                    "config-a",
                    "--configuration-root",
                    str(configuration_root),
                    "--repetition-index",
                    "1",
                    "--output-dir",
                    str(base / "run"),
                    "--agent-timeout-seconds",
                    "30",
                    "--agent",
                    "codex",
                    "--agent-version",
                    "local-test-agent-v1",
                    "--model",
                    "local-no-model-command",
                    "--reasoning-effort",
                    "not-applicable",
                    "--profile",
                    "custom",
                    "--permissions-digest",
                    "sha256:" + ("b" * 64),
                    "--toolset-digest",
                    "sha256:" + ("c" * 64),
                    "--agent-command",
                    sys.executable,
                    "-c",
                    "from pathlib import Path; Path({!r}).write_text('ran')".format(str(marker)),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertFalse(marker.exists())

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("contract-only", completed.stderr)

    def test_receipt_schema_and_runtime_expose_the_same_object_contracts(self) -> None:
        schema = json.loads(
            (EVALS_DIR / "execution-receipt.schema.json").read_text(encoding="utf-8")
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), set(receipt.RECEIPT_FIELDS))
        self.assertEqual(set(schema["properties"]), set(receipt.RECEIPT_FIELDS))
        self.assertEqual(schema["properties"]["artifact_root"]["const"], "artifacts")
        steps = schema["properties"]["steps"]
        self.assertEqual(set(steps["required"]), set(receipt.STEP_NAMES))
        step = schema["$defs"]["step"]
        self.assertEqual(set(step["required"]), set(receipt.STEP_FIELDS))
        output = schema["$defs"]["output"]
        self.assertEqual(set(output["required"]), set(receipt.OUTPUT_FIELDS))
        control = schema["$defs"]["controlSnapshot"]
        self.assertFalse(control["additionalProperties"])
        self.assertEqual(
            set(control["required"]), set(receipt.CONTROL_SNAPSHOT_FIELDS)
        )

    def test_runner_executes_fixed_lifecycle_and_writes_local_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            order_log = base / "order.log"
            manifest = make_manifest(readiness="ready")
            for index, fixture in enumerate(manifest["fixtures"], start=1):
                root = base / "fixture-{}".format(index)
                root.mkdir()
                control = root / "fixture-control"
                control.write_text(
                    "#!/bin/sh\n"
                    "set -eu\n"
                    "printf '%s\\n' \"$1\" >> {!r}\n"
                    "if [ \"$1\" = oracle ]; then\n"
                    "  printf '{{\"passed\":true}}\\n' > \"$3/oracle.json\"\n"
                    "fi\n".format(str(order_log)),
                    encoding="utf-8",
                )
                control.chmod(0o755)
                fixture["root"] = root.name
                fixture["initial_state_digest"] = validate_fixture.tree_digest(root)

            manifest_path = base / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            configuration_root = base / "configuration"
            configuration_root.mkdir()
            (configuration_root / "AGENTS.md").write_text("candidate-a\n", encoding="utf-8")
            agent = base / "agent.py"
            agent.write_text(
                "from pathlib import Path\n"
                "import os\n"
                "Path({!r}).open('a', encoding='utf-8').write('agent\\n')\n"
                "root = Path(os.environ['EVAL_ARTIFACT_ROOT'])\n"
                "Path(root, 'agent.txt').write_text('done\\n')\n"
                "Path(root, 'parent-env.txt').write_text(str(os.environ.get('EVAL_PARENT_SECRET_TEST')))\n".format(
                    str(order_log)
                ),
                encoding="utf-8",
            )
            output_dir = base / "run"

            completed = subprocess.run(
                [
                    sys.executable,
                    str(EVALS_DIR / "run_lifecycle.py"),
                    "--manifest",
                    str(manifest_path),
                    "--task-id",
                    "03-systematic-debugging",
                    "--configuration-revision",
                    "config-a",
                    "--configuration-root",
                    str(configuration_root),
                    "--repetition-index",
                    "1",
                    "--output-dir",
                    str(output_dir),
                    "--agent-timeout-seconds",
                    "30",
                    "--agent",
                    "codex",
                    "--agent-version",
                    "local-test-agent-v1",
                    "--model",
                    "local-no-model-command",
                    "--reasoning-effort",
                    "not-applicable",
                    "--profile",
                    "custom",
                    "--permissions-digest",
                    "sha256:" + ("b" * 64),
                    "--toolset-digest",
                    "sha256:" + ("c" * 64),
                    "--agent-command",
                    sys.executable,
                    str(agent),
                ],
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "EVAL_PARENT_SECRET_TEST": "DUMMY_REVIEW_VALUE"},
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            receipt_path = output_dir / "receipt.json"
            self.assertTrue(receipt_path.is_file())
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            fixture = manifest["fixtures"][2]
            self.assertEqual(receipt["pre_run_digest"], fixture["initial_state_digest"])
            self.assertEqual(receipt["oracle_outcome"], "pass")
            self.assertEqual(receipt["artifact_root"], "artifacts")
            self.assertIn("control_snapshot", receipt)
            snapshot = receipt["control_snapshot"]
            self.assertEqual(snapshot["agent"], "codex")
            self.assertEqual(snapshot["agent_version"], "local-test-agent-v1")
            self.assertEqual(snapshot["model"], "local-no-model-command")
            self.assertEqual(snapshot["reasoning_effort"], "not-applicable")
            self.assertEqual(snapshot["profile"], "custom")
            self.assertEqual(snapshot["configuration_revision"], "config-a")
            self.assertEqual(snapshot["configuration_digest"], receipt["configuration_digest"])
            self.assertEqual(snapshot["permissions_digest"], "sha256:" + ("b" * 64))
            self.assertEqual(snapshot["toolset_digest"], "sha256:" + ("c" * 64))
            self.assertEqual(snapshot["repetition_index"], 1)
            self.assertGreaterEqual(snapshot["duration_seconds"], 0)
            self.assertIsNone(snapshot["input_tokens"])
            self.assertIsNone(snapshot["output_tokens"])
            self.assertEqual(snapshot["token_source"], "unavailable")
            self.assertEqual(
                order_log.read_text(encoding="utf-8").splitlines(),
                ["reset", "setup", "agent", "oracle"],
            )
            self.assertTrue((output_dir / "artifacts" / "oracle.json").is_file())
            self.assertEqual(
                (output_dir / "artifacts/parent-env.txt").read_text(encoding="utf-8"),
                "None",
            )


if __name__ == "__main__":
    unittest.main()
