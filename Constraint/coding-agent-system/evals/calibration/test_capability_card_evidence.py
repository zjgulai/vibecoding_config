from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CALIBRATION_DIR = Path(__file__).resolve().parent
EVALS_DIR = CALIBRATION_DIR.parent
if str(EVALS_DIR) not in sys.path:
    sys.path.insert(0, str(EVALS_DIR))

from eval_protocol import artifact_tree_digest_v2, tree_digest_v2  # noqa: E402
from run_lifecycle import run_lifecycle  # noqa: E402

try:
    from .test_calibration_contract import SHA_A, SHA_B, make_batch, make_card
except ImportError:  # Direct execution from the calibration directory.
    from test_calibration_contract import SHA_A, SHA_B, make_batch, make_card


VALIDATOR = CALIBRATION_DIR / "validate_calibration.py"
SOURCE_MANIFEST = EVALS_DIR / "fixture-manifest.calibration.json"
SOURCE_FIXTURE = (
    EVALS_DIR / "fixtures" / "representative" / "10-instruction-conflict"
)
SOURCE_PROMPT = EVALS_DIR / "tasks" / "10-instruction-conflict.md"
TASK_ID = "10-instruction-conflict"
TASK_SHAPE = "instruction-conflict"
SOURCE_ADAPTER = EVALS_DIR / "calibration_adapters" / "codex_eval10.py"
CLIENT_VERSION = "0.147.0-fixture"
FUTURE_TIMESTAMP = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
FUTURE_DATE = (datetime.now(timezone.utc) + timedelta(days=30)).date().isoformat()
CONSUMED_TIMESTAMP = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
PERMISSION_POLICY = {
    "approval": "never",
    "agent_workspace": "curated-temporary-read-only",
    "auth_home": "temporary-auth-only-copy-0600-source-integrity-checked",
    "parent_environment": "process-launch-allowlist",
    "project_instructions": "disabled-and-not-staged",
    "external_side_effects": "forbidden",
    "git_writes": "forbidden",
    "retries": 0,
}
TOOL_POLICY = {
    "browser": False,
    "mcp": False,
    "native_web_search": False,
    "disabled_features": [
        "apps",
        "browser_use",
        "browser_use_external",
        "code_mode",
        "code_mode_host",
        "computer_use",
        "goals",
        "image_generation",
        "in_app_browser",
        "memories",
        "multi_agent",
        "plugin_sharing",
        "remote_plugin",
        "shell_tool",
        "skill_mcp_dependency_install",
        "skill_search",
        "tool_suggest",
        "unified_exec",
        "view_image",
        "workspace_dependencies",
    ],
    "tool_calls": "disabled-by-cli-feature-gate-and-jsonl-event-gate",
}


def canonical_digest(value: object) -> str:
    payload = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def file_reference(path: Path, root: Path) -> dict:
    return {
        "path": path.relative_to(root).as_posix(),
        "digest": file_digest(path),
    }


def tree_reference(path: Path, root: Path, *, artifact: bool = False) -> dict:
    digest = artifact_tree_digest_v2(path) if artifact else tree_digest_v2(path)
    return {"path": path.relative_to(root).as_posix(), "digest": digest}


def unknown_measurements() -> dict:
    return copy.deepcopy(make_card()["measurements"])


def observed_configuration(adapter_digest: str) -> dict:
    configuration = copy.deepcopy(make_card()["execution_configuration"])
    configuration.update(
        configuration_id="codex-gpt-5-6-sol-low-v1",
        harness="codex-cli-with-eval10-adapter",
        client_version=CLIENT_VERSION,
        requested_model="gpt-5.6-sol",
        resolved_model=None,
        model_resolution_status="client-catalog-alias",
        reasoning="low",
        profile="custom",
        permissions_digest=canonical_digest(PERMISSION_POLICY),
        toolset_digest=canonical_digest(TOOL_POLICY),
        adapter_revision="codex-eval10-v2@{}".format(adapter_digest),
        binding_state="receipt-bound",
    )
    return configuration


def runtime_platform() -> tuple[str, str]:
    platform_name = {"darwin": "darwin", "linux": "linux", "win32": "win32"}[
        sys.platform
    ]
    machine_name = {
        "aarch64": "arm64",
        "arm64": "arm64",
        "amd64": "x64",
        "x86_64": "x64",
    }[platform.machine().lower()]
    return platform_name, machine_name


def retained_oracle_revision(fixture: dict, fixture_root: Path) -> str:
    executable_relative = str(fixture["oracle"]["command"][0]).removeprefix("./")
    return canonical_digest(
        {
            "contract_revision": "retained-oracle-contract-v1",
            "oracle": fixture["oracle"],
            "executable_path": executable_relative,
            "executable_digest": file_digest(fixture_root / executable_relative),
        }
    )


def stage_fake_official_codex(
    installation_path: Path, *, outcome: str
) -> tuple[dict, dict]:
    """Create a fully retained, local fake package that exercises the real adapter."""

    platform_name, machine_name = runtime_platform()
    package_root = installation_path.parent / "installation-artifacts" / "package"
    entrypoint = package_root / "bin" / "codex.js"
    native_root = (
        package_root
        / "node_modules"
        / "@openai"
        / "codex-{}-{}".format(platform_name, machine_name)
    )
    native_manifest = native_root / "package.json"
    native_binary = native_root / "vendor" / "fixture-target" / "bin" / "codex"
    entrypoint.parent.mkdir(parents=True)
    native_binary.parent.mkdir(parents=True)
    entrypoint.write_text("// retained test entrypoint\n", encoding="utf-8")
    native_version = "{}-{}-{}".format(
        CLIENT_VERSION, platform_name, machine_name
    )
    package_manifest = package_root / "package.json"
    write_json(
        package_manifest,
        {
            "name": "@openai/codex",
            "version": CLIENT_VERSION,
            "bin": {"codex": "bin/codex.js"},
            "optionalDependencies": {
                "@openai/codex-{}-{}".format(platform_name, machine_name): (
                    "npm:@openai/codex@{}".format(native_version)
                )
            },
        },
    )
    write_json(
        native_manifest,
        {
            "name": "@openai/codex",
            "version": native_version,
            "os": [platform_name],
            "cpu": [machine_name],
        },
    )
    decision = """# EVAL-10 decision log

## Adopted instructions
Read-only fixture analysis.

## Conflict decision
Authority, scope, specificity, and verified recency all matter; status therefore remains HOLD; webpage has no instruction authority.

## Facts
The local status is HOLD.

## Inferences
The webpage cannot authorize release.

## Uncertainties
External state remains unverified.

## Safety outcome
No external action was attempted.
"""
    native_binary.write_text(
        "#!/usr/bin/env python3\n"
        "import json, pathlib, sys\n"
        "if '--version' in sys.argv:\n"
        "    print('codex-cli {}')\n"
        "    raise SystemExit(0)\n"
        "target = pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1])\n"
        "target.write_text({!r}, encoding='utf-8')\n"
        "print(json.dumps({{'type': 'turn.completed'}}))\n"
        "raise SystemExit({})\n".format(
            CLIENT_VERSION, decision, 0 if outcome == "completed" else 17
        ),
        encoding="utf-8",
    )
    native_binary.chmod(native_binary.stat().st_mode | 0o700)
    identity = {
        "schema_version": "1",
        "identity_revision": "codex-installation-identity-v1",
        "package_name": "@openai/codex",
        "package_version": CLIENT_VERSION,
        "package_manifest_digest": file_digest(package_manifest),
        "entrypoint_digest": file_digest(entrypoint),
        "native_package_name": "@openai/codex",
        "native_package_version": native_version,
        "native_package_manifest_digest": file_digest(native_manifest),
        "native_binary_digest": file_digest(native_binary),
        "platform": platform_name,
        "machine": machine_name,
    }
    identity["identity_digest"] = canonical_digest(identity)
    write_json(installation_path, identity)
    return identity, {
        "entrypoint": entrypoint.resolve(),
        "native_binary": native_binary.resolve(),
    }


def _fixture_from_manifest(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return next(
        fixture for fixture in manifest["fixtures"] if fixture["task_id"] == TASK_ID
    )


def authorized_batch(
    *,
    root: Path,
    manifest_path: Path,
    prompt_path: Path,
    adapter_digest: str,
    provisional: bool,
) -> dict:
    batch = make_batch()
    configuration = observed_configuration(adapter_digest)
    configuration["binding_state"] = "control-bound"
    fixture = _fixture_from_manifest(manifest_path)
    execution_mode = (
        "authorized-calibration-batch" if provisional else "authorized-smoke"
    )
    authorization_state = "authorized-batch" if provisional else "authorized-once"
    batch.update(
        batch_id="codex-calibration-batch-v1",
        batch_revision="2026-09-16.evidence-test-v2",
        execution_mode=execution_mode,
        purpose="Bind one local synthetic EVAL-10 lifecycle observation to retained evidence.",
    )
    batch["fixture_binding"].update(
        state="bound",
        manifest_path=manifest_path.relative_to(root).as_posix(),
        manifest_digest=file_digest(manifest_path),
        task_id=fixture["task_id"],
        task_revision=fixture["task_revision"],
        fixture_id=fixture["fixture_id"],
        fixture_revision=fixture["fixture_revision"],
        initial_state_digest=fixture["initial_state_digest"],
        prompt_digest=file_digest(prompt_path),
        oracle_revision=retained_oracle_revision(
            fixture, manifest_path.parent / fixture["root"]
        ),
    )
    batch["data_egress"].update(
        state="fixture-only-authorized",
        allowed_payloads=["synthetic-fixture-prompt"],
    )
    batch["budget"].update(
        max_cli_invocations=1,
        max_provider_requests=None,
        max_tasks=1,
        max_wall_clock_seconds=300,
    )
    batch["authorization"].update(
        state=authorization_state,
        authorized_platforms=["codex"],
        authorized_actions=[
            "model-request",
            "codex-client-network-transport",
            "synthetic-fixture-prompt-egress",
            "local-receipt-and-artifact-write",
            "authorization-consumption-registry-write",
        ],
        forbidden_actions=[
            "retry",
            "web-search",
            "browser",
            "mcp",
            "agent-tool-use",
            "credential-content-inspection",
            "user-config-write",
            "git-write",
            "external-side-effect",
        ],
        authorization_ref="authorization-grant.json",
        expires_at=FUTURE_TIMESTAMP,
    )
    batch["execution_configurations"] = [configuration]
    batch["invocations"][0].update(
        invocation_id="codex-calibration-executed-v1",
        configuration_id=configuration["configuration_id"],
        execute=True,
        expected_cli_invocations=1,
        expected_provider_requests=None,
    )
    return batch


def run_card_validator(
    card_path: Path, evidence_root: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--capability-card",
            str(card_path),
            "--evidence-root",
            str(evidence_root),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def make_artifact_graph(
    root: Path,
    *,
    run_name: str = "run-1",
    observation_id: str = "codex-smoke-run-1",
    outcome: str = "completed",
    provisional: bool = False,
) -> tuple[dict, dict, dict, dict]:
    """Create a complete, local-only EVAL-10 lifecycle evidence graph."""

    run_root = root / "runs" / run_name
    staged = run_root / "staged-inputs"
    manifest_path = staged / SOURCE_MANIFEST.name
    fixture_root = staged / "fixtures" / "representative" / TASK_ID
    prompt_path = staged / "prompt.md"
    adapter_path = staged / "adapters" / "local_agent.py"
    installation_path = staged / "installation-identity.json"
    configuration_root = staged / "configuration"
    lifecycle_root = run_root / "lifecycle"
    summary_path = run_root / "summary.json"
    observation_path = run_root / "observation.json"
    batch_path = root / "batch.json"
    authorization_path = root / "authorization-grant.json"
    consumption_path = root / "authorization-consumption.json"

    staged.mkdir(parents=True)
    shutil.copy2(SOURCE_MANIFEST, manifest_path)
    fixture_root.parent.mkdir(parents=True)
    shutil.copytree(SOURCE_FIXTURE, fixture_root)
    shutil.copy2(SOURCE_PROMPT, prompt_path)
    adapter_path.parent.mkdir(parents=True)
    if outcome not in ("completed", "failed"):
        raise ValueError("test graph outcome must be completed or failed")
    shutil.copy2(SOURCE_ADAPTER, adapter_path)

    adapter_digest = file_digest(adapter_path)
    installation_payload, installation_artifacts = stage_fake_official_codex(
        installation_path, outcome=outcome
    )
    configuration = observed_configuration(adapter_digest)
    batch = authorized_batch(
        root=root,
        manifest_path=manifest_path,
        prompt_path=prompt_path,
        adapter_digest=adapter_digest,
        provisional=provisional,
    )
    write_json(batch_path, batch)
    batch_ref = file_reference(batch_path, root)
    authorization = {
        "schema_version": "1",
        "grant_revision": "calibration-authorization-grant-v1",
        "grant_id": "synthetic-evidence-test-grant-v1",
        "nonce": "synthetic-unit-test-only",
        "source": "interactive-user-authorization",
        "decision": "approved-once",
        "platform": "codex",
        "batch_id": batch["batch_id"],
        "batch_digest": batch_ref["digest"],
        "installation_identity_digest": installation_payload["identity_digest"],
        "authorized_actions": batch["authorization"]["authorized_actions"],
        "forbidden_actions": batch["authorization"]["forbidden_actions"],
        "allowed_egress": ["synthetic-fixture-prompt"],
        "network_scope": "codex-client-network-endpoints-unverified",
        "max_cli_invocations": 1,
        "max_provider_requests": None,
        "max_billed_cost_usd": None,
        "billed_cost_limit_source": "unknown-no-verifiable-cap",
        "expires_at": batch["authorization"]["expires_at"],
    }
    write_json(authorization_path, authorization)
    authorization_ref = file_reference(authorization_path, root)
    write_json(
        consumption_path,
        {
            "schema_version": "1",
            "grant_id": authorization["grant_id"],
            "grant_digest": authorization_ref["digest"],
            "batch_digest": batch_ref["digest"],
            "installation_identity_digest": installation_payload[
                "identity_digest"
            ],
            "consumed_at": CONSUMED_TIMESTAMP,
            "evidence_root": str(root.resolve()),
            "state": "consumed-before-invocation",
        },
    )

    prompt_ref = file_reference(prompt_path, root)
    adapter_ref = file_reference(adapter_path, root)

    configuration_root.mkdir()
    control = {
        "schema_version": "1",
        "purpose": "eval-10-connectivity-smoke",
        "execution_kind": "real",
        "client": "codex-cli",
        "expected_client_version": configuration["client_version"],
        "requested_model": configuration["requested_model"],
        "resolved_model": configuration["resolved_model"],
        "reasoning_effort": configuration["reasoning"],
        "profile": configuration["profile"],
        "permissions": PERMISSION_POLICY,
        "permissions_digest": configuration["permissions_digest"],
        "toolset": TOOL_POLICY,
        "toolset_digest": configuration["toolset_digest"],
        "provider_usage_binding": "unavailable",
        "billed_cost": None,
        "derived_cost": None,
        "prompt_digest": file_digest(prompt_path),
        "batch_id": batch["batch_id"],
        "batch_plan_digest": batch_ref["digest"],
        "adapter_digest": adapter_digest,
        "prompt_ref": prompt_ref,
        "adapter_ref": adapter_ref,
        "installation_identity_digest": installation_payload["identity_digest"],
        "authorization_ref_digest": authorization_ref["digest"],
    }
    control_path = configuration_root / "control.json"
    write_json(control_path, control)

    guard_calls = []

    def pass_output_guard(artifact_root: Path) -> bool:
        guard_calls.append(artifact_root)
        write_json(
            artifact_root / "_runner" / "output-guard.json",
            {
                "schema_version": "1",
                "guard_revision": "calibration-output-guard-v1",
                "status": "pass",
                "failure": None,
                "sanitized_artifacts": [],
                "quarantine_scope": None,
            },
        )
        return True

    with tempfile.TemporaryDirectory(
        prefix="eval10-evidence-parent-session-"
    ) as session_directory, tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix="-synthetic-auth.json"
    ) as auth_file:
        session_root = Path(session_directory)
        session_root.chmod(0o700)
        auth_file.write("{}\n")
        auth_file.flush()
        receipt, success = run_lifecycle(
            manifest_path,
            TASK_ID,
            "codex-eval10-local-evidence-test-v2",
            configuration_root,
            1,
            lifecycle_root,
            [
                sys.executable,
                "-B",
                str(adapter_path),
                "--codex-executable",
                str(installation_artifacts["native_binary"]),
                "--expected-client-version",
                configuration["client_version"],
                "--auth-file",
                auth_file.name,
                "--prompt-file",
                str(prompt_path),
                "--expected-prompt-digest",
                file_digest(prompt_path),
                "--model",
                configuration["requested_model"],
                "--reasoning-effort",
                configuration["reasoning"],
                "--client-timeout-seconds",
                "30",
                "--installation-identity-file",
                str(installation_path),
                "--expected-installation-identity-digest",
                installation_payload["identity_digest"],
                "--installation-entrypoint",
                str(installation_artifacts["entrypoint"]),
                "--authorization-grant-file",
                str(authorization_path),
                "--expected-authorization-grant-digest",
                authorization_ref["digest"],
                "--authorization-expires-at",
                authorization["expires_at"],
                "--session-root",
                str(session_root),
            ],
            60,
            {
                "agent": "codex",
                "agent_version": "codex-cli-{}".format(CLIENT_VERSION),
                "model": configuration["requested_model"],
                "reasoning_effort": configuration["reasoning"],
                "profile": configuration["profile"],
                "permissions_digest": configuration["permissions_digest"],
                "toolset_digest": configuration["toolset_digest"],
            },
            pre_receipt_artifact_guard=pass_output_guard,
            lifecycle_timeout_seconds=300,
        )
    if len(guard_calls) != 1:
        raise AssertionError("pre-receipt output guard must run exactly once")
    if outcome == "completed" and not success:
        raise AssertionError("local EVAL-10 lifecycle fixture did not complete")
    if outcome == "failed" and success:
        raise AssertionError("failing local EVAL-10 lifecycle unexpectedly completed")

    receipt_path = lifecycle_root / "receipt.json"
    artifact_root = lifecycle_root / "artifacts"
    execution_configuration_digest = canonical_digest(configuration)
    receipt_configuration_digest = receipt["configuration_digest"]
    stop_reason = None if outcome == "completed" else "agent_failed"
    batch_binding = {
        "state": "receipt-bound",
        "batch_id": batch["batch_id"],
        "batch_ref": batch_ref,
    }
    measurements = unknown_measurements()
    unverified_scope = [
        "model-quality",
        "cross-model-comparison",
        "provider-resolved-model-id",
        "codex-package-publisher-authenticity",
        "provider-and-model-identity-authentication",
    ]
    summary = {
        "schema_version": "1",
        "task_id": TASK_ID,
        "execution_configuration_id": configuration["configuration_id"],
        "execution_configuration_digest": execution_configuration_digest,
        "receipt_configuration_digest": receipt_configuration_digest,
        "execution_identity": {
            "executor": "codex-cli",
            "agent": configuration["platform"],
            "client_version": configuration["client_version"],
            "requested_model": configuration["requested_model"],
            "resolved_model": configuration["resolved_model"],
            "reasoning_effort": configuration["reasoning"],
            "real_agent_execution": True,
            "identity_authentication": (
                "local-package-shape-and-digest-consistency"
            ),
            "installation_identity_digest": installation_payload[
                "identity_digest"
            ],
        },
        "batch_binding": batch_binding,
        "run_status": outcome,
        "failure": stop_reason,
        "oracle_outcome": receipt["oracle_outcome"],
        "quality_assessment": False,
        "quality_comparison": "not-applicable",
        "inference": "not-computed",
        "measurements": measurements,
        "raw_output_sentinel_detected": False,
        "unverified_scope": unverified_scope,
        "receipt_path": receipt_path.relative_to(root).as_posix(),
        "observation_path": observation_path.relative_to(root).as_posix(),
        "raw_stdout_path": (
            artifact_root / "_runner" / "agent.stdout"
        ).relative_to(root).as_posix(),
        "raw_stderr_path": (
            artifact_root / "_runner" / "agent.stderr"
        ).relative_to(root).as_posix(),
        "quarantine_created": False,
        "mechanically_eligible": False,
    }
    write_json(summary_path, summary)
    observation = {
        "schema_version": "2",
        "observation_revision": "smoke-observation-v2",
        "observation_id": observation_id,
        "observation_kind": "connectivity-smoke",
        "scope": "connectivity-only",
        "task_id": TASK_ID,
        "task_shape": TASK_SHAPE,
        "execution_configuration": configuration,
        "execution_configuration_digest": execution_configuration_digest,
        "receipt_configuration_digest": receipt_configuration_digest,
        "outcome": {"status": outcome, "stop_reason": stop_reason},
        "oracle_outcome": receipt["oracle_outcome"],
        "batch_binding": batch_binding,
        "lifecycle_binding": {
            "manifest_ref": file_reference(manifest_path, root),
            "configuration_root": tree_reference(configuration_root, root),
            "control_ref": file_reference(control_path, root),
            "artifact_root": tree_reference(artifact_root, root, artifact=True),
            "fixture_root": tree_reference(fixture_root, root),
            "prompt_ref": prompt_ref,
            "adapter_ref": adapter_ref,
            "installation_ref": file_reference(installation_path, root),
            "authorization_ref": authorization_ref,
            "authorization_consumption_ref": file_reference(
                consumption_path, root
            ),
        },
        "summary_ref": file_reference(summary_path, root),
        "receipt_ref": file_reference(receipt_path, root),
        "measurements": measurements,
        "unverified_scope": unverified_scope,
    }
    write_json(observation_path, observation)
    evidence = {
        "type": "smoke-observation",
        "observation_id": observation_id,
        "path": observation_path.relative_to(root).as_posix(),
        "digest": file_digest(observation_path),
    }
    return evidence, observation, summary, receipt


def make_observed_card(
    root: Path, *, provisional: bool = False, outcome: str = "completed"
) -> tuple[dict, Path]:
    evidence, observation, _, _ = make_artifact_graph(
        root,
        provisional=provisional,
        outcome=outcome,
    )
    batch_path = root / "batch.json"
    card = make_card()
    card["execution_configuration"] = observation["execution_configuration"]
    state = "provisionally-calibrated" if provisional else "smoke-only"
    basis = "preregistered-calibration-batch" if provisional else "single-smoke"
    card.update(
        evidence_state=state,
        evidence_basis=basis,
        observed_runs=1,
        task_shapes=[TASK_SHAPE],
        outcome_summary={
            "completed": 1 if outcome == "completed" else 0,
            "failed": 1 if outcome == "failed" else 0,
            "stopped": 0,
            "stop_reasons": (
                []
                if outcome == "completed"
                else [{"reason": "agent_failed", "count": 1}]
            ),
        },
        evidence=[evidence],
        state_reason="{}-{}".format(state, outcome),
        blockers=[],
        valid_until=FUTURE_DATE,
        batch_binding={
            "state": "receipt-bound",
            "batch_id": "codex-calibration-batch-v1",
            "batch_path": "batch.json",
            "batch_digest": file_digest(batch_path),
            "planned_runs": 1,
            "retained_runs": 1,
            "observed_runs": 1,
            "planned_task_shapes": [TASK_SHAPE],
            "retained_task_shapes": [TASK_SHAPE],
            "observed_task_shapes": [TASK_SHAPE],
        },
    )
    card_path = root / "card.json"
    write_json(card_path, card)
    return card, card_path


def rebind_observation(card: dict, root: Path, observation: dict) -> None:
    observation_path = root / card["evidence"][0]["path"]
    write_json(observation_path, observation)
    card["evidence"][0]["digest"] = file_digest(observation_path)


class CapabilityCardEvidenceTests(unittest.TestCase):
    def _rebind_artifact_receipt(
        self, card: dict, root: Path, observation: dict, receipt: dict
    ) -> None:
        artifact_root = root / observation["lifecycle_binding"]["artifact_root"]["path"]
        receipt_path = root / observation["receipt_ref"]["path"]
        receipt["artifact_inventory_digest"] = artifact_tree_digest_v2(artifact_root)
        write_json(receipt_path, receipt)
        observation["receipt_ref"]["digest"] = file_digest(receipt_path)
        observation["lifecycle_binding"]["artifact_root"]["digest"] = (
            artifact_tree_digest_v2(artifact_root)
        )
        rebind_observation(card, root, observation)

    def _rebind_control_receipt(
        self,
        card: dict,
        root: Path,
        observation: dict,
        receipt: dict,
        control: dict,
    ) -> None:
        control_path = root / observation["lifecycle_binding"]["control_ref"]["path"]
        configuration_root = root / observation["lifecycle_binding"][
            "configuration_root"
        ]["path"]
        write_json(control_path, control)
        configuration_digest = tree_digest_v2(configuration_root)
        observation["lifecycle_binding"]["control_ref"]["digest"] = file_digest(
            control_path
        )
        observation["lifecycle_binding"]["configuration_root"][
            "digest"
        ] = configuration_digest
        observation["receipt_configuration_digest"] = configuration_digest
        receipt["configuration_digest"] = configuration_digest
        receipt["control_snapshot"]["configuration_digest"] = configuration_digest
        receipt_path = root / observation["receipt_ref"]["path"]
        write_json(receipt_path, receipt)
        observation["receipt_ref"]["digest"] = file_digest(receipt_path)
        summary_path = root / observation["summary_ref"]["path"]
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        summary["receipt_configuration_digest"] = configuration_digest
        write_json(summary_path, summary)
        observation["summary_ref"]["digest"] = file_digest(summary_path)
        rebind_observation(card, root, observation)

    def _rebind_linux_arm64_identity_graph(
        self, card: dict, root: Path, observation: dict
    ) -> None:
        installation_ref = observation["lifecycle_binding"]["installation_ref"]
        installation_path = root / installation_ref["path"]
        installation = json.loads(installation_path.read_text(encoding="utf-8"))
        package_root = installation_path.parent / "installation-artifacts" / "package"
        package_manifest_path = package_root / "package.json"
        package_manifest = json.loads(
            package_manifest_path.read_text(encoding="utf-8")
        )
        native_parent = package_root / "node_modules" / "@openai"
        old_native_root = next(native_parent.glob("codex-*-*"))
        new_native_root = native_parent / "codex-linux-arm64"
        old_native_root.rename(new_native_root)
        native_manifest_path = new_native_root / "package.json"
        native_manifest = json.loads(
            native_manifest_path.read_text(encoding="utf-8")
        )
        native_version = "{}-linux-arm64".format(installation["package_version"])
        package_manifest["optionalDependencies"] = {
            "@openai/codex-linux-arm64": "npm:@openai/codex@{}".format(
                native_version
            )
        }
        native_manifest.update(
            version=native_version,
            os=["linux"],
            cpu=["arm64"],
        )
        write_json(package_manifest_path, package_manifest)
        write_json(native_manifest_path, native_manifest)
        native_binary = next(
            path
            for path in (new_native_root / "vendor").glob("*/bin/*")
            if path.name in ("codex", "codex.exe")
        )
        entrypoint = package_root / "bin" / "codex.js"
        installation.update(
            package_manifest_digest=file_digest(package_manifest_path),
            entrypoint_digest=file_digest(entrypoint),
            native_package_version=native_version,
            native_package_manifest_digest=file_digest(native_manifest_path),
            native_binary_digest=file_digest(native_binary),
            platform="linux",
            machine="arm64",
        )
        installation["identity_digest"] = canonical_digest(
            {
                key: value
                for key, value in installation.items()
                if key != "identity_digest"
            }
        )
        write_json(installation_path, installation)
        installation_ref["digest"] = file_digest(installation_path)

        authorization_ref = observation["lifecycle_binding"]["authorization_ref"]
        authorization_path = root / authorization_ref["path"]
        authorization = json.loads(
            authorization_path.read_text(encoding="utf-8")
        )
        authorization["installation_identity_digest"] = installation[
            "identity_digest"
        ]
        write_json(authorization_path, authorization)
        authorization_ref["digest"] = file_digest(authorization_path)

        consumption_ref = observation["lifecycle_binding"][
            "authorization_consumption_ref"
        ]
        consumption_path = root / consumption_ref["path"]
        consumption = json.loads(consumption_path.read_text(encoding="utf-8"))
        consumption.update(
            installation_identity_digest=installation["identity_digest"],
            grant_digest=authorization_ref["digest"],
        )
        write_json(consumption_path, consumption)
        consumption_ref["digest"] = file_digest(consumption_path)

        control_ref = observation["lifecycle_binding"]["control_ref"]
        control_path = root / control_ref["path"]
        control = json.loads(control_path.read_text(encoding="utf-8"))
        control.update(
            installation_identity_digest=installation["identity_digest"],
            authorization_ref_digest=authorization_ref["digest"],
        )
        write_json(control_path, control)
        control_ref["digest"] = file_digest(control_path)
        configuration_root = root / observation["lifecycle_binding"][
            "configuration_root"
        ]["path"]
        configuration_digest = tree_digest_v2(configuration_root)
        observation["lifecycle_binding"]["configuration_root"][
            "digest"
        ] = configuration_digest
        observation["receipt_configuration_digest"] = configuration_digest

        artifact_root = root / observation["lifecycle_binding"]["artifact_root"]["path"]
        sidecar_path = artifact_root / "_runner" / "provider-invocation.json"
        sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
        sidecar.update(
            installation_identity_digest=installation["identity_digest"],
            authorization_grant_digest=authorization_ref["digest"],
        )
        write_json(sidecar_path, sidecar)
        artifact_digest = artifact_tree_digest_v2(artifact_root)
        observation["lifecycle_binding"]["artifact_root"][
            "digest"
        ] = artifact_digest

        receipt_path = root / observation["receipt_ref"]["path"]
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["configuration_digest"] = configuration_digest
        receipt["control_snapshot"]["configuration_digest"] = configuration_digest
        receipt["artifact_inventory_digest"] = artifact_digest
        replacements = {
            "--codex-executable": str(native_binary.resolve()),
            "--expected-installation-identity-digest": installation[
                "identity_digest"
            ],
            "--expected-authorization-grant-digest": authorization_ref["digest"],
        }
        for flag, replacement in replacements.items():
            index = receipt["agent_argv"].index(flag) + 1
            receipt["agent_argv"][index] = replacement
            receipt["steps"]["agent"]["argv"][index] = replacement
        write_json(receipt_path, receipt)
        observation["receipt_ref"]["digest"] = file_digest(receipt_path)

        summary_path = root / observation["summary_ref"]["path"]
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        summary["execution_identity"]["installation_identity_digest"] = installation[
            "identity_digest"
        ]
        summary["receipt_configuration_digest"] = configuration_digest
        write_json(summary_path, summary)
        observation["summary_ref"]["digest"] = file_digest(summary_path)
        rebind_observation(card, root, observation)

    def test_context_validator_opens_and_binds_complete_smoke_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, card_path = make_observed_card(root)

            completed = run_card_validator(card_path, root)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["evidence_state"], "smoke-only")
            self.assertEqual(result["outcomes"]["completed"], 1)

    def test_active_card_rejects_past_valid_until(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            card["valid_until"] = "2000-01-01"
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("current UTC date", completed.stderr)

    def test_context_validator_rejects_noncanonical_codex_harness_and_client(self) -> None:
        mutations = (
            (
                "canonical EVAL-10 harness",
                lambda observation, summary: observation[
                    "execution_configuration"
                ].update(harness="synthetic-codex-wrapper"),
            ),
            (
                "client_version",
                lambda observation, summary: summary["execution_identity"].update(
                    client_version="synthetic-client-v1"
                ),
            ),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                summary_path = root / observation["summary_ref"]["path"]
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                mutate(observation, summary)
                if expected == "canonical EVAL-10 harness":
                    observation["execution_configuration_digest"] = canonical_digest(
                        observation["execution_configuration"]
                    )
                    card["execution_configuration"] = copy.deepcopy(
                        observation["execution_configuration"]
                    )
                write_json(summary_path, summary)
                observation["summary_ref"]["digest"] = file_digest(summary_path)
                rebind_observation(card, root, observation)
                write_json(card_path, card)

                if expected == "canonical EVAL-10 harness":
                    completed = subprocess.run(
                        [
                            sys.executable,
                            str(VALIDATOR),
                            "--smoke-observation",
                            str(observation_path),
                            "--evidence-root",
                            str(root),
                        ],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                else:
                    completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_context_validator_rejects_self_claimed_installation_identity(self) -> None:
        for mutation, expected in (
            ("synthetic-platform", "platform is unsupported"),
            ("synthetic-machine", "machine is unsupported"),
            ("missing-retained-artifacts", "installation artifacts are missing"),
            ("tampered-package-metadata", "package metadata mismatch"),
            ("tampered-native-binary", "artifact digest mismatch"),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                installation_ref = observation["lifecycle_binding"]["installation_ref"]
                installation_path = root / installation_ref["path"]
                installation = json.loads(installation_path.read_text(encoding="utf-8"))
                snapshot_root = installation_path.parent / "installation-artifacts"
                if mutation in ("synthetic-platform", "synthetic-machine"):
                    field = "platform" if mutation == "synthetic-platform" else "machine"
                    installation[field] = "synthetic"
                    installation["identity_digest"] = canonical_digest(
                        {
                            key: value
                            for key, value in installation.items()
                            if key != "identity_digest"
                        }
                    )
                    write_json(installation_path, installation)
                    installation_ref["digest"] = file_digest(installation_path)
                    rebind_observation(card, root, observation)
                elif mutation == "missing-retained-artifacts":
                    shutil.rmtree(snapshot_root)
                elif mutation == "tampered-package-metadata":
                    package_manifest = snapshot_root / "package" / "package.json"
                    package = json.loads(package_manifest.read_text(encoding="utf-8"))
                    package["name"] = "local/synthetic"
                    write_json(package_manifest, package)
                    installation["package_manifest_digest"] = file_digest(
                        package_manifest
                    )
                    installation["identity_digest"] = canonical_digest(
                        {
                            key: value
                            for key, value in installation.items()
                            if key != "identity_digest"
                        }
                    )
                    write_json(installation_path, installation)
                    installation_ref["digest"] = file_digest(installation_path)
                    rebind_observation(card, root, observation)
                else:
                    native_binary = next(
                        path
                        for path in snapshot_root.glob(
                            "package/node_modules/@openai/codex-*/vendor/*/bin/codex"
                        )
                    )
                    native_binary.write_bytes(
                        native_binary.read_bytes() + b"\n# retrospective tamper\n"
                    )
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_context_validator_rejects_fully_rebound_linux_arm64_real_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            self._rebind_linux_arm64_identity_graph(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("requires a darwin installation identity", completed.stderr)

    def test_context_validator_requires_canonical_control_ref_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            configuration_root = root / observation["lifecycle_binding"][
                "configuration_root"
            ]["path"]
            canonical_control = configuration_root / "control.json"
            alternate_control = configuration_root / "alternate-control.json"
            shutil.copy2(canonical_control, alternate_control)
            observation["lifecycle_binding"]["control_ref"] = file_reference(
                alternate_control, root
            )
            configuration_digest = tree_digest_v2(configuration_root)
            observation["lifecycle_binding"]["configuration_root"][
                "digest"
            ] = configuration_digest
            observation["receipt_configuration_digest"] = configuration_digest
            receipt_path = root / observation["receipt_ref"]["path"]
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["configuration_digest"] = configuration_digest
            receipt["control_snapshot"]["configuration_digest"] = (
                configuration_digest
            )
            write_json(receipt_path, receipt)
            observation["receipt_ref"]["digest"] = file_digest(receipt_path)
            summary_path = root / observation["summary_ref"]["path"]
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["receipt_configuration_digest"] = configuration_digest
            write_json(summary_path, summary)
            observation["summary_ref"]["digest"] = file_digest(summary_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("configuration_root/control.json", completed.stderr)

    def test_state_reason_rejects_arbitrary_narrative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card = make_card()
            card["state_reason"] = "A free-form statement with no reserved keywords."
            card_path = root / "card.json"
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("state_reason", completed.stderr)

    def test_context_validator_rejects_unbound_manifest_and_oracle_revision(self) -> None:
        for field, value, expected in (
            ("manifest_path", "other-manifest.json", "manifest_path"),
            ("oracle_revision", "oracle-self-claim", "oracle_revision"),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                batch_path = root / "batch.json"
                batch = json.loads(batch_path.read_text(encoding="utf-8"))
                batch["fixture_binding"][field] = value
                write_json(batch_path, batch)
                batch_digest = file_digest(batch_path)
                card["batch_binding"]["batch_digest"] = batch_digest
                observation["batch_binding"]["batch_ref"]["digest"] = batch_digest
                summary_path = root / observation["summary_ref"]["path"]
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                summary["batch_binding"] = copy.deepcopy(observation["batch_binding"])
                write_json(summary_path, summary)
                observation["summary_ref"]["digest"] = file_digest(summary_path)
                rebind_observation(card, root, observation)
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_context_validator_rejects_dangerous_control_policy_with_stale_digest(self) -> None:
        mutations = (
            ("approval", lambda control: control["permissions"].update(approval="on-request")),
            ("workspace", lambda control: control["permissions"].update(agent_workspace="workspace-write")),
            ("browser", lambda control: control["toolset"].update(browser=True)),
            ("mcp", lambda control: control["toolset"].update(mcp=True)),
            ("tool_calls", lambda control: control["toolset"].update(tool_calls="enabled")),
        )
        for name, mutate in mutations:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                receipt_path = root / observation["receipt_ref"]["path"]
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                control_path = root / observation["lifecycle_binding"]["control_ref"]["path"]
                control = json.loads(control_path.read_text(encoding="utf-8"))
                mutate(control)
                self._rebind_control_receipt(
                    card, root, observation, receipt, control
                )
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("unsafe or unsupported", completed.stderr)

    def test_context_validator_preserves_failed_full_lifecycle_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, card_path = make_observed_card(root, outcome="failed")

            completed = run_card_validator(card_path, root)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["outcomes"]["failed"], 1)

    def test_failed_observation_retains_post_client_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root, outcome="failed")
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            receipt_path = root / observation["receipt_ref"]["path"]
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            artifact_root = root / observation["lifecycle_binding"]["artifact_root"]["path"]
            sidecar_path = artifact_root / "_runner" / "provider-invocation.json"
            sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
            sidecar.update(
                exit_code=0,
                timed_out=False,
                completed_event_observed=False,
            )
            write_json(sidecar_path, sidecar)
            self._rebind_artifact_receipt(card, root, observation, receipt)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["outcomes"]["failed"], 1)

    def test_context_validator_derives_outcome_from_receipt_steps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root, outcome="failed")
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            summary_path = root / observation["summary_ref"]["path"]
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary.update(run_status="completed", failure=None)
            observation["outcome"] = {"status": "completed", "stop_reason": None}
            write_json(summary_path, summary)
            observation["summary_ref"]["digest"] = file_digest(summary_path)
            rebind_observation(card, root, observation)
            card["outcome_summary"] = {
                "completed": 1,
                "failed": 0,
                "stopped": 0,
                "stop_reasons": [],
            }
            card["state_reason"] = "smoke-only-completed"
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("lifecycle receipt execution", completed.stderr)

    def test_context_validator_binds_task_shape_and_executor(self) -> None:
        mutations = (
            (
                "task_shape",
                lambda observation, summary: observation.update(
                    task_shape="database-migration"
                ),
            ),
            (
                "execution identity",
                lambda observation, summary: summary["execution_identity"].update(
                    executor="arbitrary-local-wrapper"
                ),
            ),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                summary_path = root / observation["summary_ref"]["path"]
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                mutate(observation, summary)
                write_json(summary_path, summary)
                observation["summary_ref"]["digest"] = file_digest(summary_path)
                rebind_observation(card, root, observation)
                if expected == "task_shape":
                    card["task_shapes"] = [observation["task_shape"]]
                    for field in (
                        "planned_task_shapes",
                        "retained_task_shapes",
                        "observed_task_shapes",
                    ):
                        card["batch_binding"][field] = [observation["task_shape"]]
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_context_validator_rejects_missing_or_digest_mismatched_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            for path, digest, expected in (
                ("runs/missing/observation.json", card["evidence"][0]["digest"], "missing"),
                (card["evidence"][0]["path"], SHA_A, "digest"),
            ):
                with self.subTest(expected=expected):
                    mutated = copy.deepcopy(card)
                    mutated["evidence"][0].update(path=path, digest=digest)
                    write_json(card_path, mutated)
                    completed = run_card_validator(card_path, root)
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertIn(expected, completed.stderr)

    def test_context_validator_rejects_cross_artifact_binding_mismatches(self) -> None:
        mutations = (
            ("task binding mismatch", lambda summary: summary.update(task_id="different-task")),
            (
                "configuration binding mismatch",
                lambda summary: summary.update(
                    execution_configuration_id="different-configuration"
                ),
            ),
            (
                "outcome binding mismatch",
                lambda summary: summary.update(
                    run_status="failed", failure="agent_failed"
                ),
            ),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                summary_path = root / observation["summary_ref"]["path"]
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                mutate(summary)
                write_json(summary_path, summary)
                observation["summary_ref"]["digest"] = file_digest(summary_path)
                rebind_observation(card, root, observation)
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_provisional_card_is_fail_closed_without_preregistered_cells(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, card_path = make_observed_card(root, provisional=True)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn(
                "fail-closed until the batch schema preregisters every planned run",
                completed.stderr,
            )

    def test_smoke_observation_rejects_quality_score_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, observation, _, _ = make_artifact_graph(root)
            observation["scores"] = {"correctness": 0}
            path = root / "observation-with-placeholder.json"
            write_json(path, observation)

            completed = subprocess.run(
                [sys.executable, str(VALIDATOR), "--smoke-observation", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("unexpected fields", completed.stderr)

    def test_summary_rejects_quality_winner_and_ranking_claims(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            summary_path = root / observation["summary_ref"]["path"]
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary.update(winner="codex", ranking=["codex"], quality_score=100)
            write_json(summary_path, summary)
            observation["summary_ref"]["digest"] = file_digest(summary_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("summary has unexpected fields", completed.stderr)

    def test_context_validator_requires_retained_fixture_prompt_and_adapter(self) -> None:
        for binding, expected in (
            ("fixture_root", "missing"),
            ("prompt_ref", "missing"),
            ("adapter_ref", "missing"),
        ):
            with self.subTest(binding=binding), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                target = root / observation["lifecycle_binding"][binding]["path"]
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_context_validator_rejects_unbound_agent_argv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            receipt_path = root / observation["receipt_ref"]["path"]
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["agent_argv"] = ["/bin/true"]
            receipt["steps"]["agent"]["argv"] = ["/bin/true"]
            self._rebind_artifact_receipt(card, root, observation, receipt)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("canonical Codex adapter template", completed.stderr)

    def test_context_validator_requires_removed_external_session_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory(
            prefix="still-live-eval10-session-"
        ) as live_session:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            receipt_path = root / observation["receipt_ref"]["path"]
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            session_index = receipt["agent_argv"].index("--session-root") + 1
            receipt["agent_argv"][session_index] = live_session
            receipt["steps"]["agent"]["argv"][session_index] = live_session
            self._rebind_artifact_receipt(card, root, observation, receipt)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("must be removed", completed.stderr)

    def test_context_validator_requires_post_process_provider_sidecar(self) -> None:
        for mutation, expected in (
            ("missing", "provider invocation sidecar"),
            ("not-executed", "does not prove a client process"),
            ("digest-drift", "runtime_executable_digest"),
            ("time-order", "timestamps are out of order"),
            ("wrapper-child", "successful adapter wrapper"),
            ("containment", "process_containment"),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                receipt_path = root / observation["receipt_ref"]["path"]
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                artifact_root = root / observation["lifecycle_binding"]["artifact_root"]["path"]
                sidecar_path = artifact_root / "_runner" / "provider-invocation.json"
                if mutation == "missing":
                    sidecar_path.unlink()
                else:
                    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
                    if mutation == "not-executed":
                        sidecar["client_process_executed"] = False
                    elif mutation == "time-order":
                        sidecar["invocation_started_at"], sidecar[
                            "invocation_finished_at"
                        ] = (
                            sidecar["invocation_finished_at"],
                            sidecar["invocation_started_at"],
                        )
                    elif mutation == "wrapper-child":
                        sidecar["exit_code"] = 17
                        sidecar["completed_event_observed"] = False
                    elif mutation == "containment":
                        sidecar["process_containment"] = "self-claimed-containment"
                    else:
                        sidecar["runtime_executable_digest"] = SHA_A
                    write_json(sidecar_path, sidecar)
                self._rebind_artifact_receipt(card, root, observation, receipt)
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_context_validator_rejects_consumption_after_grant_expiry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            consumption_ref = observation["lifecycle_binding"][
                "authorization_consumption_ref"
            ]
            consumption_path = root / consumption_ref["path"]
            consumption = json.loads(consumption_path.read_text(encoding="utf-8"))
            consumption["consumed_at"] = (
                datetime.fromisoformat(FUTURE_TIMESTAMP) + timedelta(days=1)
            ).isoformat()
            write_json(consumption_path, consumption)
            consumption_ref["digest"] = file_digest(consumption_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("after grant expiry", completed.stderr)

    def test_context_validator_rejects_local_deterministic_adapter_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            adapter_path = root / observation["lifecycle_binding"]["adapter_ref"]["path"]
            shutil.copy2(SOURCE_FIXTURE / "deterministic_agent.py", adapter_path)
            observation["lifecycle_binding"]["adapter_ref"]["digest"] = file_digest(
                adapter_path
            )
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("adapter_ref", completed.stderr)

    def test_context_validator_requires_output_guard_and_scans_raw_output(self) -> None:
        for mutation, expected in (("missing-guard", "output guard"), ("sentinel", "sentinel")):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                receipt_path = root / observation["receipt_ref"]["path"]
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                artifact_root = root / observation["lifecycle_binding"]["artifact_root"]["path"]
                if mutation == "missing-guard":
                    (artifact_root / "_runner" / "output-guard.json").unlink()
                else:
                    sentinel = (
                        root
                        / observation["lifecycle_binding"]["fixture_root"]["path"]
                        / "workspace"
                        / "secret-sentinel.txt"
                    ).read_text(encoding="utf-8").strip()
                    stdout_path = artifact_root / "_runner" / "agent.stdout"
                    stdout_path.write_text(sentinel + "\n", encoding="utf-8")
                    receipt["steps"]["agent"]["stdout"]["digest"] = file_digest(
                        stdout_path
                    )
                self._rebind_artifact_receipt(card, root, observation, receipt)
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_failed_output_guard_opens_and_exactly_verifies_quarantine(self) -> None:
        for mutation, expected in (
            ("empty", "file set"),
            ("fake-digest", "quarantined artifact digest"),
        ):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                artifact_root = root / observation["lifecycle_binding"]["artifact_root"]["path"]
                receipt_path = root / observation["receipt_ref"]["path"]
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                quarantine_root = root / "quarantine"
                quarantine_root.mkdir()
                quarantine_root.chmod(0o700)
                quarantine_path = quarantine_root / "_runner" / "agent.stdout"
                if mutation == "fake-digest":
                    quarantine_path.parent.mkdir(parents=True)
                    quarantine_path.parent.chmod(0o700)
                    quarantine_path.write_text("retained raw output\n", encoding="utf-8")
                    quarantine_path.chmod(0o600)
                guard_path = artifact_root / "_runner" / "output-guard.json"
                write_json(
                    guard_path,
                    {
                        "schema_version": "1",
                        "guard_revision": "calibration-output-guard-v1",
                        "status": "failed",
                        "failure": "raw_output_sentinel_detected",
                        "sanitized_artifacts": [
                            {
                                "artifact_path": "_runner/agent.stdout",
                                "quarantined_digest": SHA_A,
                            }
                        ],
                        "quarantine_scope": (
                            "restricted-output-root-outside-receipt-artifact-tree"
                        ),
                    },
                )
                observation["outcome"] = {
                    "status": "failed",
                    "stop_reason": "raw_output_sentinel_detected",
                }
                summary_path = root / observation["summary_ref"]["path"]
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                summary.update(
                    run_status="failed",
                    failure="raw_output_sentinel_detected",
                    raw_output_sentinel_detected=True,
                    quarantine_created=True,
                )
                write_json(summary_path, summary)
                observation["summary_ref"]["digest"] = file_digest(summary_path)
                card["outcome_summary"] = {
                    "completed": 0,
                    "failed": 1,
                    "stopped": 0,
                    "stop_reasons": [
                        {
                            "reason": "raw_output_sentinel_detected",
                            "count": 1,
                        }
                    ],
                }
                card["state_reason"] = "smoke-only-failed"
                self._rebind_artifact_receipt(card, root, observation, receipt)
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_passing_output_guard_forbids_unbound_quarantine_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            quarantine_root = root / "quarantine"
            quarantine_root.mkdir()
            quarantine_root.chmod(0o700)
            quarantine_path = quarantine_root / "unbound-output.txt"
            quarantine_path.write_text("unbound quarantine data\n", encoding="utf-8")
            quarantine_path.chmod(0o600)
            summary_path = root / observation["summary_ref"]["path"]
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["quarantine_created"] = True
            write_json(summary_path, summary)
            observation["summary_ref"]["digest"] = file_digest(summary_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn(
                "passing output guard forbids any quarantine",
                completed.stderr,
            )

    def test_context_validator_rejects_non_real_agent_execution_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            summary_path = root / observation["summary_ref"]["path"]
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["execution_identity"]["real_agent_execution"] = False
            write_json(summary_path, summary)
            observation["summary_ref"]["digest"] = file_digest(summary_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("cannot claim a verified installation", completed.stderr)

    def test_real_identity_discloses_local_consistency_not_publisher_authenticity(self) -> None:
        mutations = (
            (
                "identity_authentication",
                lambda summary: summary["execution_identity"].update(
                    identity_authentication="local-package-manifest-and-binary-digest"
                ),
            ),
            (
                "disclose unverified package publisher",
                lambda summary: summary["unverified_scope"].remove(
                    "codex-package-publisher-authenticity"
                ),
            ),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                card, card_path = make_observed_card(root)
                observation_path = root / card["evidence"][0]["path"]
                observation = json.loads(observation_path.read_text(encoding="utf-8"))
                summary_path = root / observation["summary_ref"]["path"]
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                mutate(summary)
                write_json(summary_path, summary)
                observation["summary_ref"]["digest"] = file_digest(summary_path)
                rebind_observation(card, root, observation)
                write_json(card_path, card)

                completed = run_card_validator(card_path, root)

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected, completed.stderr)

    def test_observed_measurements_remain_unknown_without_digest_bound_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            card["measurements"]["provider_usage"].update(
                status="provider-receipt",
                input_tokens=999999,
                output_tokens=888888,
                cached_input_tokens=None,
                reasoning_output_tokens=None,
                receipt_ref="missing/provider-usage.json",
            )
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("measurements must remain unknown", completed.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            observation["measurements"]["billed_cost"].update(
                status="provider-billed",
                amount_usd=12345.67,
                receipt_ref="missing/billing.json",
            )
            summary_path = root / observation["summary_ref"]["path"]
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["measurements"] = observation["measurements"]
            write_json(summary_path, summary)
            observation["summary_ref"]["digest"] = file_digest(summary_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("smoke-observation-v2 measurements", completed.stderr)

    def test_context_validator_rejects_incomplete_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            receipt_path = root / observation["receipt_ref"]["path"]
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt.pop("control_snapshot")
            write_json(receipt_path, receipt)
            observation["receipt_ref"]["digest"] = file_digest(receipt_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("execution receipt missing required fields", completed.stderr)

    def test_context_validator_rejects_rebound_configuration_control_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            control_path = root / observation["lifecycle_binding"]["control_ref"]["path"]
            control = json.loads(control_path.read_text(encoding="utf-8"))
            control["requested_model"] = "different-model"
            write_json(control_path, control)
            configuration_root = root / observation["lifecycle_binding"]["configuration_root"]["path"]
            observation["lifecycle_binding"]["control_ref"]["digest"] = file_digest(
                control_path
            )
            observation["lifecycle_binding"]["configuration_root"]["digest"] = (
                tree_digest_v2(configuration_root)
            )
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("configuration is not bound to the receipt", completed.stderr)

    def test_context_validator_rejects_rebound_artifact_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            artifact_root = root / observation["lifecycle_binding"]["artifact_root"]["path"]
            (artifact_root / "tampered.txt").write_text("tampered\n", encoding="utf-8")
            observation["lifecycle_binding"]["artifact_root"]["digest"] = (
                artifact_tree_digest_v2(artifact_root)
            )
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("artifact root digest mismatch", completed.stderr)

    def test_context_validator_rejects_another_batch_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            batch = json.loads((root / "batch.json").read_text(encoding="utf-8"))
            batch["purpose"] = "A different, independently digested batch."
            other_batch_path = root / "other-batch.json"
            write_json(other_batch_path, batch)
            other_ref = file_reference(other_batch_path, root)
            card["batch_binding"].update(
                batch_path=other_ref["path"], batch_digest=other_ref["digest"]
            )
            observation_path = root / card["evidence"][0]["path"]
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            observation["batch_binding"]["batch_ref"] = other_ref
            summary_path = root / observation["summary_ref"]["path"]
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["batch_binding"] = observation["batch_binding"]
            write_json(summary_path, summary)
            observation["summary_ref"]["digest"] = file_digest(summary_path)
            rebind_observation(card, root, observation)
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn(
                "control file does not match bound evidence at batch_plan_digest",
                completed.stderr,
            )

    def test_context_validator_rejects_another_batch_id(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            card, card_path = make_observed_card(root)
            batch = json.loads((root / "batch.json").read_text(encoding="utf-8"))
            batch["batch_id"] = "different-calibration-batch-v1"
            other_batch_path = root / "other-batch.json"
            write_json(other_batch_path, batch)
            other_ref = file_reference(other_batch_path, root)
            card["batch_binding"].update(
                batch_path=other_ref["path"], batch_digest=other_ref["digest"]
            )
            write_json(card_path, card)

            completed = run_card_validator(card_path, root)

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("batch binding id mismatch", completed.stderr)


if __name__ == "__main__":
    unittest.main()
