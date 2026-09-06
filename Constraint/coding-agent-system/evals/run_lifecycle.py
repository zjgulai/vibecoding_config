#!/usr/bin/env python3
"""Run a local fixture lifecycle only when an explicit agent argv is supplied."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

from eval_protocol import (
    artifact_tree_digest_v2,
    load_json,
    sha256_file,
    tree_digest_v2,
    verify_artifact_contract,
)
from receipt import (
    CONTROL_SNAPSHOT_REVISION,
    CONTROL_SOURCE_SCOPE,
    INTEGRITY_SCOPE,
    RECEIPT_REVISION,
    validate_control_declaration,
    validate_receipt,
)
from validate_fixture import (
    find_fixture,
    fixture_root,
    validate_manifest_structure,
)


def _output_reference(path: Path, artifact_root: Path) -> Dict:
    return {
        "path": path.relative_to(artifact_root).as_posix(),
        "digest": sha256_file(path),
    }


def _not_run(argv: List[str], expected_exit_code: int = 0) -> Dict:
    return {
        "argv": argv,
        "executed": False,
        "expected_exit_code": expected_exit_code,
        "exit_code": None,
        "timed_out": False,
        "stdout": None,
        "stderr": None,
    }


def _run_step(
    name: str,
    argv: List[str],
    expected_exit_code: int,
    timeout_seconds: int,
    cwd: Path,
    artifact_root: Path,
    environment: Mapping[str, str],
) -> Dict:
    log_root = artifact_root / "_runner"
    log_root.mkdir(parents=True, exist_ok=True)
    stdout_path = log_root / "{}.stdout".format(name)
    stderr_path = log_root / "{}.stderr".format(name)
    timed_out = False
    exit_code: Optional[int]
    try:
        completed = subprocess.run(
            argv,
            cwd=str(cwd),
            env=dict(environment),
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        exit_code = None
        stdout = error.stdout or b""
        stderr = error.stderr or b""
    stdout_path.write_bytes(stdout)
    stderr_path.write_bytes(stderr)
    return {
        "argv": argv,
        "executed": True,
        "expected_exit_code": expected_exit_code,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "stdout": _output_reference(stdout_path, artifact_root),
        "stderr": _output_reference(stderr_path, artifact_root),
    }


def _step_succeeded(step: Mapping) -> bool:
    return (
        step["executed"]
        and not step["timed_out"]
        and step["exit_code"] == step["expected_exit_code"]
    )


def _minimal_environment() -> Dict[str, str]:
    """Forward only process-launch essentials, never arbitrary parent variables."""

    allowed = (
        "PATH",
        "LANG",
        "LC_ALL",
        "LC_CTYPE",
        "TMPDIR",
        "TEMP",
        "TMP",
        "SYSTEMROOT",
        "WINDIR",
        "COMSPEC",
        "PATHEXT",
    )
    return {name: os.environ[name] for name in allowed if name in os.environ}


def _canonical_receipt_bytes(receipt: Mapping) -> bytes:
    return (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def run_lifecycle(
    manifest_path: Path,
    task_id: str,
    configuration_revision: str,
    configuration_root: Path,
    repetition_index: int,
    output_dir: Path,
    agent_argv: List[str],
    agent_timeout_seconds: int,
    control_declaration: Mapping,
) -> Tuple[Dict, bool]:
    validate_control_declaration(control_declaration)
    manifest = load_json(manifest_path)
    validate_manifest_structure(manifest)
    fixture = find_fixture(manifest, task_id)
    if fixture["readiness"] != "ready":
        raise ValueError("fixture {!r} is contract-only and cannot run".format(fixture["fixture_id"]))
    if not configuration_root.is_dir() or configuration_root.is_symlink():
        raise ValueError("configuration root must be a regular directory")
    manifest_digest = sha256_file(manifest_path)
    configuration_digest = tree_digest_v2(configuration_root)
    if output_dir.exists() and (not output_dir.is_dir() or any(output_dir.iterdir())):
        raise ValueError("output directory must not exist or must be empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_root = output_dir / "artifacts"
    artifact_root.mkdir()
    root = fixture_root(manifest_path, fixture)
    if not root.is_dir():
        raise ValueError("fixture root is not a directory")

    environment = _minimal_environment()
    environment.update(
        {
            "EVAL_ARTIFACT_ROOT": str(artifact_root.resolve()),
            "EVAL_TASK_ID": task_id,
            "EVAL_CONFIGURATION_REVISION": configuration_revision,
            "EVAL_REPETITION_INDEX": str(repetition_index),
        }
    )
    reset_argv = list(fixture["reset"]["command"])
    setup_argv = list(fixture["setup"]["command"])
    oracle_argv = [
        str(artifact_root.resolve()) if argument == "<artifact-root>" else argument
        for argument in fixture["oracle"]["command"]
    ]
    steps = {
        "reset": _not_run(reset_argv),
        "setup": _not_run(setup_argv),
        "agent": _not_run(agent_argv),
        "oracle": _not_run(oracle_argv),
    }
    pre_run_digest: Optional[str] = None
    agent_duration_seconds: Optional[float] = None
    artifact_contract_valid = False

    steps["reset"] = _run_step(
        "reset",
        reset_argv,
        fixture["reset"]["expected_exit_code"],
        fixture["reset"]["timeout_seconds"],
        root,
        artifact_root,
        environment,
    )
    if _step_succeeded(steps["reset"]):
        steps["setup"] = _run_step(
            "setup",
            setup_argv,
            fixture["setup"]["expected_exit_code"],
            fixture["setup"]["timeout_seconds"],
            root,
            artifact_root,
            environment,
        )
    if _step_succeeded(steps["setup"]):
        pre_run_digest = tree_digest_v2(root)
    if pre_run_digest == fixture["initial_state_digest"]:
        agent_started = time.monotonic()
        steps["agent"] = _run_step(
            "agent",
            agent_argv,
            0,
            agent_timeout_seconds,
            root,
            artifact_root,
            environment,
        )
        agent_duration_seconds = round(time.monotonic() - agent_started, 6)
        steps["oracle"] = _run_step(
            "oracle",
            oracle_argv,
            fixture["oracle"]["expected_exit_code"],
            fixture["oracle"]["timeout_seconds"],
            root,
            artifact_root,
            environment,
        )
        artifact_errors = verify_artifact_contract(fixture["artifacts"], artifact_root)
        artifact_contract_valid = not artifact_errors
        if artifact_errors:
            (artifact_root / "_runner" / "artifact-contract.errors").write_text(
                "\n".join(artifact_errors) + "\n", encoding="utf-8"
            )

    oracle_outcome = (
        "pass"
        if _step_succeeded(steps["oracle"]) and artifact_contract_valid
        else "fail" if steps["oracle"]["executed"] else "not-run"
    )
    receipt = {
        "schema_version": "2",
        "runner_revision": RECEIPT_REVISION,
        "integrity_scope": INTEGRITY_SCOPE,
        "manifest_revision": manifest["manifest_revision"],
        "manifest_digest": manifest_digest,
        "task_id": fixture["task_id"],
        "task_revision": fixture["task_revision"],
        "fixture_id": fixture["fixture_id"],
        "fixture_revision": fixture["fixture_revision"],
        "fixture_initial_digest": fixture["initial_state_digest"],
        "pre_run_digest": pre_run_digest,
        "configuration_revision": configuration_revision,
        "configuration_digest": configuration_digest,
        "repetition_index": repetition_index,
        "control_snapshot": {
            "snapshot_revision": CONTROL_SNAPSHOT_REVISION,
            "source_scope": CONTROL_SOURCE_SCOPE,
            "agent": control_declaration["agent"],
            "agent_version": control_declaration["agent_version"],
            "model": control_declaration["model"],
            "reasoning_effort": control_declaration["reasoning_effort"],
            "profile": control_declaration["profile"],
            "configuration_revision": configuration_revision,
            "configuration_digest": configuration_digest,
            "permissions_digest": control_declaration["permissions_digest"],
            "toolset_digest": control_declaration["toolset_digest"],
            "repetition_index": repetition_index,
            "duration_seconds": agent_duration_seconds,
            "input_tokens": None,
            "output_tokens": None,
            "token_source": "unavailable",
        },
        "agent_argv": agent_argv,
        "artifact_root": "artifacts",
        "artifact_inventory_digest": artifact_tree_digest_v2(artifact_root),
        "artifact_contract_valid": artifact_contract_valid,
        "oracle_outcome": oracle_outcome,
        "steps": steps,
    }
    validate_receipt(receipt)
    (output_dir / "receipt.json").write_bytes(_canonical_receipt_bytes(receipt))
    success = (
        pre_run_digest == fixture["initial_state_digest"]
        and _step_succeeded(steps["agent"])
        and oracle_outcome == "pass"
    )
    return receipt, success


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run reset, setup, digest validation, an explicitly supplied local agent argv, "
            "and oracle. Receipts provide local digest consistency, not authenticity."
        )
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--configuration-revision", required=True)
    parser.add_argument("--configuration-root", required=True, type=Path)
    parser.add_argument("--repetition-index", required=True, type=int)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--agent-timeout-seconds", required=True, type=int)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--agent-version", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--permissions-digest", required=True)
    parser.add_argument("--toolset-digest", required=True)
    parser.add_argument(
        "--agent-command",
        nargs=argparse.REMAINDER,
        required=True,
        help="explicit local argv to execute; no shell is used",
    )
    arguments = parser.parse_args(argv)
    try:
        if not arguments.agent_command:
            raise ValueError("--agent-command requires at least one argv item")
        if arguments.repetition_index < 1:
            raise ValueError("--repetition-index must be >= 1")
        if not 1 <= arguments.agent_timeout_seconds <= 86400:
            raise ValueError("--agent-timeout-seconds must be from 1 to 86400")
        receipt, success = run_lifecycle(
            arguments.manifest,
            arguments.task_id,
            arguments.configuration_revision,
            arguments.configuration_root,
            arguments.repetition_index,
            arguments.output_dir,
            arguments.agent_command,
            arguments.agent_timeout_seconds,
            {
                "agent": arguments.agent,
                "agent_version": arguments.agent_version,
                "model": arguments.model,
                "reasoning_effort": arguments.reasoning_effort,
                "profile": arguments.profile,
                "permissions_digest": arguments.permissions_digest,
                "toolset_digest": arguments.toolset_digest,
            },
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
