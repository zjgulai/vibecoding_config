from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List, Optional

import validate_fixture


EVALS_DIR = Path(__file__).resolve().parent
TASK_IDS = [
    "01-product-discovery",
    "02-vertical-full-stack-feature",
    "03-systematic-debugging",
    "04-postgresql-migration",
    "05-frontend-visual-quality",
    "06-two-axis-review",
    "07-instruction-audit",
    "08-project-profile",
    "09-memory-governance",
    "10-instruction-conflict",
    "11-local-rule-linked-change",
]
KNOWN_TREE_DIGEST = (
    "sha256:6872ec32dca3716eb26386ea2844f56f09da954c9fccbcd71b0b3aa0f4d3d35f"
)


def make_fixture(
    task_id: str,
    index: int,
    readiness: str = "contract-only",
    root: Optional[str] = None,
    digest: Optional[str] = None,
) -> dict:
    return {
        "task_id": task_id,
        "task_revision": "2026-08-29.1",
        "fixture_id": "coding-agent-task-{:02d}".format(index),
        "fixture_revision": "fixture-v1",
        "readiness": readiness,
        "root": root or "fixtures/representative/{}".format(task_id),
        "setup": {
            "command": ["./fixture-control", "setup"],
            "expected_exit_code": 0,
            "timeout_seconds": 900,
            "success_condition": "Command exits 0 and creates only declared fixture state.",
        },
        "reset": {
            "command": ["./fixture-control", "reset"],
            "expected_exit_code": 0,
            "timeout_seconds": 900,
            "success_condition": "Command exits 0 and removes all prior run mutations.",
        },
        "oracle": {
            "command": [
                "./fixture-control",
                "oracle",
                "--artifacts",
                "<artifact-root>",
            ],
            "expected_exit_code": 0,
            "timeout_seconds": 900,
            "pass_condition": "All task assertions pass and oracle.json records raw results.",
        },
        "artifacts": {
            "root_template": "artifacts/<task-id>/<configuration-revision>/<repetition-index>",
            "required": [
                {
                    "path": "oracle.json",
                    "kind": "file",
                    "non_empty": True,
                    "description": "Machine-readable oracle result and command evidence.",
                }
            ],
            "forbidden": [".env", "credentials/**", "production-write.log"],
        },
        "initial_state_digest": digest if readiness == "ready" else None,
    }


def make_manifest(readiness: str = "contract-only", digest: Optional[str] = None) -> dict:
    return {
        "schema_version": "1",
        "manifest_revision": "2026-08-29.1",
        "digest_contract": {
            "algorithm": "sha256-tree-v2",
            "excluded_paths": [".git/**"],
            "generation_command": [
                "python3",
                "evals/validate_fixture.py",
                "--digest",
                "<fixture-root>",
            ],
            "validation_command": [
                "python3",
                "evals/validate_fixture.py",
                "<manifest-path>",
            ],
            "validation_timing": "after_reset_and_setup_before_each_repetition",
        },
        "fixtures": [
            make_fixture(task_id, index, readiness=readiness, digest=digest)
            for index, task_id in enumerate(TASK_IDS, start=1)
        ],
    }


def run_validator(arguments: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(EVALS_DIR / "validate_fixture.py")] + arguments,
        capture_output=True,
        text=True,
        check=False,
    )


class FixtureManifestTests(unittest.TestCase):
    def test_contract_only_example_passes_explicit_structure_check_but_not_baseline(self) -> None:
        manifest_path = EVALS_DIR / "fixture-manifest.example.json"

        allowed = run_validator(["--allow-contract-only", str(manifest_path)])
        rejected = run_validator([str(manifest_path)])

        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        result = json.loads(allowed.stdout)
        self.assertTrue(result["structure_valid"])
        self.assertFalse(result["tree_contract_valid"])
        self.assertNotIn("baseline_eligible", result)
        self.assertEqual(result["fixture_count"], 11)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("contract-only", rejected.stderr)

        schema = json.loads(
            (EVALS_DIR / "fixture-manifest.schema.json").read_text(encoding="utf-8")
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            set(schema["required"]),
            {"schema_version", "manifest_revision", "digest_contract", "fixtures"},
        )
        self.assertEqual(
            schema["properties"]["digest_contract"]["properties"]["algorithm"]["const"],
            "sha256-tree-v2",
        )
        fixture_properties = schema["$defs"]["fixture"]["properties"]
        self.assertEqual(
            fixture_properties["setup"]["allOf"][1]["properties"]["command"]["const"],
            ["./fixture-control", "setup"],
        )
        self.assertEqual(
            fixture_properties["reset"]["allOf"][1]["properties"]["command"]["const"],
            ["./fixture-control", "reset"],
        )
        self.assertEqual(
            fixture_properties["oracle"]["allOf"][1]["properties"]["command"]["const"],
            ["./fixture-control", "oracle", "--artifacts", "<artifact-root>"],
        )

    def test_safe_path_mutation_corpus_is_rejected_by_schema_and_runtime(self) -> None:
        schema = json.loads(
            (EVALS_DIR / "fixture-manifest.schema.json").read_text(encoding="utf-8")
        )
        path_pattern = re.compile(schema["$defs"]["safeRelativePath"]["pattern"])
        mutations = (
            "../outside",
            "/absolute",
            "C:/windows-drive",
            "directory\\windows-separator",
            "directory//empty-segment",
            "directory/./dot",
            "directory/../parent",
            "trailing/",
            "   ",
            "colon:name",
        )
        for value in mutations:
            with self.subTest(value=value):
                self.assertIsNone(path_pattern.fullmatch(value))
                manifest = make_manifest()
                manifest["fixtures"][0]["root"] = value
                with self.assertRaisesRegex(ValueError, "root"):
                    validate_fixture.validate_manifest_structure(manifest)

    def test_tree_digest_is_deterministic_and_ignores_git_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nested").mkdir()
            (root / ".git").mkdir()
            (root / "a.txt").write_bytes(b"alpha\n")
            (root / "nested" / "b.bin").write_bytes(b"\x00\xff")
            (root / ".git" / "ignored").write_bytes(b"changes do not count")

            completed = run_validator(["--digest", str(root)])

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), KNOWN_TREE_DIGEST)

    def test_tree_digest_rejects_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.txt").write_text("target", encoding="utf-8")
            (root / "link.txt").symlink_to(root / "target.txt")

            completed = run_validator(["--digest", str(root)])

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("symlink", completed.stderr)

    def test_tree_digest_changes_for_executable_bits_and_empty_directories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            control = root / "fixture-control"
            control.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            control.chmod(0o644)
            initial = run_validator(["--digest", str(root)])

            control.chmod(0o755)
            executable = run_validator(["--digest", str(root)])
            (root / "required-empty-directory").mkdir()
            with_directory = run_validator(["--digest", str(root)])

        self.assertEqual(initial.returncode, 0, initial.stderr)
        self.assertEqual(executable.returncode, 0, executable.stderr)
        self.assertEqual(with_directory.returncode, 0, with_directory.stderr)
        self.assertNotEqual(initial.stdout, executable.stdout)
        self.assertNotEqual(executable.stdout, with_directory.stdout)

    def test_ready_manifest_validates_digest_and_detects_state_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            manifest = make_manifest(readiness="ready", digest=KNOWN_TREE_DIGEST)
            for index, fixture in enumerate(manifest["fixtures"], start=1):
                root = base / "fixture-{}".format(index)
                (root / "nested").mkdir(parents=True)
                (root / "a.txt").write_bytes(b"alpha\n")
                (root / "nested" / "b.bin").write_bytes(b"\x00\xff")
                fixture["root"] = root.name

            manifest_path = base / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            valid = run_validator([str(manifest_path)])

            (base / "fixture-3" / "a.txt").write_bytes(b"changed\n")
            drifted = run_validator([str(manifest_path)])

        self.assertEqual(valid.returncode, 0, valid.stderr)
        result = json.loads(valid.stdout)
        self.assertTrue(result["structure_valid"])
        self.assertTrue(result["tree_contract_valid"])
        self.assertNotIn("baseline_eligible", result)
        self.assertNotEqual(drifted.returncode, 0)
        self.assertIn("initial_state_digest mismatch", drifted.stderr)
        self.assertIn("coding-agent-task-03", drifted.stderr)

    def test_manifest_rejects_missing_duplicate_and_extra_protocol_data(self) -> None:
        cases = []

        missing_task = make_manifest()
        missing_task["fixtures"].pop()
        cases.append((missing_task, "exactly eleven"))

        duplicate_task = make_manifest()
        duplicate_task["fixtures"][-1]["task_id"] = TASK_IDS[0]
        cases.append((duplicate_task, "task_id"))

        extra_field = make_manifest()
        extra_field["fixtures"][0]["setup"]["shell"] = True
        cases.append((extra_field, "unexpected"))

        unsafe_root = make_manifest()
        unsafe_root["fixtures"][0]["root"] = "../outside"
        cases.append((unsafe_root, "root"))

        windows_drive = make_manifest()
        windows_drive["fixtures"][0]["root"] = "C:/outside"
        cases.append((windows_drive, "root"))

        duplicate_forbidden = make_manifest()
        duplicate_forbidden["fixtures"][0]["artifacts"]["forbidden"].append(".env")
        cases.append((duplicate_forbidden, "duplicate"))

        wrong_setup = make_manifest()
        wrong_setup["fixtures"][0]["setup"]["command"] = ["true"]
        cases.append((wrong_setup, "fixture-control"))

        with tempfile.TemporaryDirectory() as directory:
            for index, (manifest, message) in enumerate(cases, start=1):
                path = Path(directory) / "invalid-{}.json".format(index)
                path.write_text(json.dumps(manifest), encoding="utf-8")
                completed = run_validator(["--allow-contract-only", str(path)])
                with self.subTest(message=message):
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertIn(message, completed.stderr)

    def test_manifest_loader_rejects_duplicate_json_keys(self) -> None:
        manifest_path = EVALS_DIR / "fixture-manifest.example.json"
        text = manifest_path.read_text(encoding="utf-8").replace(
            '"schema_version": "1",',
            '"schema_version": "1",\n  "schema_version": "1",',
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text(text, encoding="utf-8")
            completed = run_validator(["--allow-contract-only", str(path)])

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("duplicate JSON key", completed.stderr)

    def test_all_declared_task_contracts_have_a_task_document(self) -> None:
        manifest = json.loads(
            (EVALS_DIR / "fixture-manifest.example.json").read_text(encoding="utf-8")
        )

        self.assertEqual(
            [fixture["task_id"] for fixture in manifest["fixtures"]],
            TASK_IDS,
        )
        for task_id in TASK_IDS:
            with self.subTest(task_id=task_id):
                self.assertTrue((EVALS_DIR / "tasks" / (task_id + ".md")).is_file())
        self.assertTrue(
            all(fixture["readiness"] == "contract-only" for fixture in manifest["fixtures"])
        )

    def test_ready_fixture_requires_a_real_digest(self) -> None:
        manifest = make_manifest(readiness="ready", digest=None)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            completed = run_validator([str(path)])

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("initial_state_digest", completed.stderr)

    def test_ready_fixture_root_cannot_escape_through_a_parent_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            base = Path(directory)
            outside_root = Path(outside)
            (outside_root / "fixture").mkdir()
            (outside_root / "fixture" / "a.txt").write_text("outside", encoding="utf-8")
            (base / "linked").symlink_to(outside_root, target_is_directory=True)

            manifest = make_manifest(readiness="ready", digest=KNOWN_TREE_DIGEST)
            for fixture in manifest["fixtures"]:
                fixture["root"] = "linked/fixture"
            path = base / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            completed = run_validator([str(path)])

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("symlink", completed.stderr)


if __name__ == "__main__":
    unittest.main()
