#!/usr/bin/env python3
"""Validate local execution receipts and bind them to current files.

SHA-256 checks provide local integrity consistency only. They do not authenticate
who created a receipt and do not prevent an editor from rewriting files and
recomputing every digest.
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping, Optional, Sequence

from eval_protocol import (
    artifact_tree_digest_v2,
    argv,
    exact_fields,
    nonblank,
    nonnegative_integer,
    optional_integer,
    optional_number,
    resolve_relative_without_symlinks,
    safe_relative_posix_path,
    sha256_file,
    validate_digest,
    validate_evidence_scope,
    verify_artifact_contract,
)


RECEIPT_REVISION = "execution-receipt-v4"
RECEIPT_SCHEMA_VERSION = "4"
INTEGRITY_SCOPE = "local-digest-consistency-only"
CONTROL_SNAPSHOT_REVISION = "control-snapshot-v1"
CONTROL_SOURCE_SCOPE = "runner-observed-plus-invocation-declared"
AGENTS = ("codex", "claude-code", "deepseek-harness")
PROFILES = ("quality", "balanced", "economy", "custom")
REASONING_EFFORTS = (
    "none",
    "minimal",
    "low",
    "medium",
    "high",
    "xhigh",
    "max",
    "ultra",
    "not-applicable",
)
STEP_NAMES = ("reset", "setup", "agent", "oracle")
RECEIPT_FIELDS = (
    "schema_version",
    "runner_revision",
    "integrity_scope",
    "evidence_scope",
    "manifest_revision",
    "manifest_digest",
    "task_id",
    "task_revision",
    "fixture_id",
    "fixture_revision",
    "fixture_initial_digest",
    "pre_run_digest",
    "configuration_revision",
    "configuration_digest",
    "repetition_index",
    "lifecycle_duration_seconds",
    "lifecycle_timeout_seconds",
    "lifecycle_timed_out",
    "control_snapshot",
    "agent_argv",
    "artifact_root",
    "artifact_inventory_digest",
    "artifact_contract_valid",
    "oracle_outcome",
    "steps",
)
STEP_FIELDS = (
    "argv",
    "executed",
    "expected_exit_code",
    "exit_code",
    "timed_out",
    "stdout",
    "stderr",
)
OUTPUT_FIELDS = ("path", "digest")
CONTROL_DECLARATION_FIELDS = (
    "agent",
    "agent_version",
    "model",
    "reasoning_effort",
    "profile",
    "permissions_digest",
    "toolset_digest",
)
CONTROL_SNAPSHOT_FIELDS = (
    "snapshot_revision",
    "source_scope",
    "agent",
    "agent_version",
    "model",
    "reasoning_effort",
    "profile",
    "configuration_revision",
    "configuration_digest",
    "permissions_digest",
    "toolset_digest",
    "repetition_index",
    "duration_seconds",
    "input_tokens",
    "output_tokens",
    "token_source",
)


def validate_control_declaration(value: object) -> None:
    """Validate invocation-declared controls before any lifecycle command runs."""

    if not isinstance(value, Mapping):
        raise ValueError("control declaration must be an object")
    exact_fields(
        value,
        CONTROL_DECLARATION_FIELDS,
        CONTROL_DECLARATION_FIELDS,
        "control declaration",
    )
    for field in ("agent_version", "model"):
        nonblank(value[field], field)
    if value["agent"] not in AGENTS:
        raise ValueError("agent must be one of: {}".format(", ".join(AGENTS)))
    if value["reasoning_effort"] not in REASONING_EFFORTS:
        raise ValueError(
            "reasoning_effort must be one of: {}".format(", ".join(REASONING_EFFORTS))
        )
    if value["profile"] not in PROFILES:
        raise ValueError("profile must be one of: {}".format(", ".join(PROFILES)))
    for field in ("permissions_digest", "toolset_digest"):
        validate_digest(value[field], field, allow_zero=False)


def _validate_control_snapshot(value: object, agent_executed: bool) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("control_snapshot must be an object")
    exact_fields(
        value,
        CONTROL_SNAPSHOT_FIELDS,
        CONTROL_SNAPSHOT_FIELDS,
        "control_snapshot",
    )
    if value["snapshot_revision"] != CONTROL_SNAPSHOT_REVISION:
        raise ValueError("unsupported control_snapshot.snapshot_revision")
    if value["source_scope"] != CONTROL_SOURCE_SCOPE:
        raise ValueError("control_snapshot.source_scope is unsupported")
    validate_control_declaration(
        {field: value[field] for field in CONTROL_DECLARATION_FIELDS}
    )
    nonblank(value["configuration_revision"], "control_snapshot.configuration_revision")
    validate_digest(
        value["configuration_digest"],
        "control_snapshot.configuration_digest",
        allow_zero=False,
    )
    nonnegative_integer(
        value["repetition_index"], "control_snapshot.repetition_index", minimum=1
    )
    duration = optional_number(
        value["duration_seconds"], "control_snapshot.duration_seconds"
    )
    if agent_executed != (duration is not None):
        raise ValueError(
            "control_snapshot.duration_seconds presence must match agent execution"
        )
    input_tokens = optional_integer(
        value["input_tokens"], "control_snapshot.input_tokens"
    )
    output_tokens = optional_integer(
        value["output_tokens"], "control_snapshot.output_tokens"
    )
    if value["token_source"] != "unavailable":
        raise ValueError("control_snapshot.token_source must be 'unavailable' in v1")
    if input_tokens is not None or output_tokens is not None:
        raise ValueError("unavailable token_source requires null token counts")


def _validate_output_reference(value: object, label: str) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("{} must be an object".format(label))
    exact_fields(value, OUTPUT_FIELDS, OUTPUT_FIELDS, label)
    safe_relative_posix_path(value["path"], "{}.path".format(label))
    validate_digest(value["digest"], "{}.digest".format(label), allow_zero=False)


def _validate_step(value: object, label: str) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("{} must be an object".format(label))
    exact_fields(value, STEP_FIELDS, STEP_FIELDS, label)
    argv(value["argv"], "{}.argv".format(label))
    if not isinstance(value["executed"], bool):
        raise ValueError("{}.executed must be boolean".format(label))
    expected = value["expected_exit_code"]
    if expected != 0 or isinstance(expected, bool):
        raise ValueError("{}.expected_exit_code must be 0".format(label))
    if not isinstance(value["timed_out"], bool):
        raise ValueError("{}.timed_out must be boolean".format(label))

    if value["executed"]:
        if value["timed_out"]:
            if value["exit_code"] is not None:
                raise ValueError("{}.exit_code must be null after timeout".format(label))
        elif isinstance(value["exit_code"], bool) or not isinstance(value["exit_code"], int):
            raise ValueError("{}.exit_code must be an integer when executed".format(label))
        _validate_output_reference(value["stdout"], "{}.stdout".format(label))
        _validate_output_reference(value["stderr"], "{}.stderr".format(label))
    elif (
        value["exit_code"] is not None
        or value["timed_out"]
        or value["stdout"] is not None
        or value["stderr"] is not None
    ):
        raise ValueError("{} has execution output despite executed=false".format(label))


def _step_succeeded(step: Mapping) -> bool:
    return (
        step["executed"]
        and not step["timed_out"]
        and step["exit_code"] == step["expected_exit_code"]
    )


def validate_receipt(receipt: Mapping) -> None:
    if not isinstance(receipt, Mapping):
        raise ValueError("execution receipt must be an object")
    exact_fields(receipt, RECEIPT_FIELDS, RECEIPT_FIELDS, "execution receipt")
    if receipt["schema_version"] != RECEIPT_SCHEMA_VERSION:
        raise ValueError(
            "receipt schema_version must be {!r}".format(RECEIPT_SCHEMA_VERSION)
        )
    if receipt["runner_revision"] != RECEIPT_REVISION:
        raise ValueError("unsupported runner_revision")
    if receipt["integrity_scope"] != INTEGRITY_SCOPE:
        raise ValueError("receipt integrity_scope must describe local digest consistency only")
    validate_evidence_scope(receipt["evidence_scope"], "receipt evidence_scope")
    for field in (
        "manifest_revision",
        "task_id",
        "task_revision",
        "fixture_id",
        "fixture_revision",
        "configuration_revision",
    ):
        nonblank(receipt[field], field)
    for field in (
        "manifest_digest",
        "fixture_initial_digest",
        "configuration_digest",
        "artifact_inventory_digest",
    ):
        validate_digest(receipt[field], field, allow_zero=False)
    if receipt["pre_run_digest"] is not None:
        validate_digest(receipt["pre_run_digest"], "pre_run_digest", allow_zero=False)
    nonnegative_integer(receipt["repetition_index"], "repetition_index", minimum=1)
    lifecycle_duration = optional_number(
        receipt["lifecycle_duration_seconds"], "lifecycle_duration_seconds"
    )
    if lifecycle_duration is None:
        raise ValueError("lifecycle_duration_seconds must be observed")
    lifecycle_timeout = optional_number(
        receipt["lifecycle_timeout_seconds"], "lifecycle_timeout_seconds"
    )
    lifecycle_timed_out = receipt["lifecycle_timed_out"]
    if not isinstance(lifecycle_timed_out, bool):
        raise ValueError("lifecycle_timed_out must be boolean")
    if lifecycle_timed_out and lifecycle_timeout is None:
        raise ValueError("lifecycle_timed_out requires a declared timeout")
    if lifecycle_timeout is not None:
        if lifecycle_timed_out and lifecycle_duration < lifecycle_timeout:
            raise ValueError("timed-out lifecycle duration is below declared timeout")
        if not lifecycle_timed_out and lifecycle_duration > lifecycle_timeout:
            raise ValueError("non-timeout lifecycle duration exceeds declared timeout")
    argv(receipt["agent_argv"], "agent_argv")
    safe_relative_posix_path(receipt["artifact_root"], "artifact_root")
    if receipt["artifact_root"] != "artifacts":
        raise ValueError("artifact_root must be the runner-managed 'artifacts' directory")
    if not isinstance(receipt["artifact_contract_valid"], bool):
        raise ValueError("artifact_contract_valid must be boolean")
    if receipt["oracle_outcome"] not in ("pass", "fail", "not-run"):
        raise ValueError("oracle_outcome must be pass, fail, or not-run")

    steps = receipt["steps"]
    if not isinstance(steps, Mapping):
        raise ValueError("steps must be an object")
    exact_fields(steps, STEP_NAMES, STEP_NAMES, "steps")
    for name in STEP_NAMES:
        _validate_step(steps[name], "steps.{}".format(name))

    _validate_control_snapshot(receipt["control_snapshot"], steps["agent"]["executed"])
    snapshot = receipt["control_snapshot"]
    for field in (
        "configuration_revision",
        "configuration_digest",
        "repetition_index",
    ):
        if snapshot[field] != receipt[field]:
            raise ValueError(
                "control_snapshot.{} must match receipt {}".format(field, field)
            )

    if receipt["agent_argv"] != steps["agent"]["argv"]:
        raise ValueError("agent_argv must match steps.agent.argv")
    if not steps["reset"]["executed"]:
        raise ValueError("runner receipt requires an executed reset step")
    reset_succeeded = _step_succeeded(steps["reset"])
    if (
        steps["setup"]["executed"] != reset_succeeded
        and not (lifecycle_timed_out and reset_succeeded and not steps["setup"]["executed"])
    ):
        raise ValueError("setup execution must follow reset success exactly")
    setup_succeeded = _step_succeeded(steps["setup"])
    pre_run_ready = receipt["pre_run_digest"] is not None
    if pre_run_ready != (reset_succeeded and setup_succeeded):
        raise ValueError("pre_run_digest presence must follow reset and setup success")
    should_execute_candidate = (
        pre_run_ready
        and receipt["pre_run_digest"] == receipt["fixture_initial_digest"]
    )
    if (
        steps["agent"]["executed"] != should_execute_candidate
        and not (
            lifecycle_timed_out
            and should_execute_candidate
            and not steps["agent"]["executed"]
        )
    ):
        raise ValueError("agent execution must follow a matching pre-run digest")
    if (
        steps["oracle"]["executed"] != should_execute_candidate
        and not (
            lifecycle_timed_out
            and should_execute_candidate
            and not steps["oracle"]["executed"]
        )
    ):
        raise ValueError("oracle execution must follow a matching pre-run digest")
    if receipt["artifact_contract_valid"] and not steps["oracle"]["executed"]:
        raise ValueError("artifact_contract_valid requires an executed oracle step")

    expected_outcome = (
        "pass"
        if _step_succeeded(steps["oracle"])
        and receipt["artifact_contract_valid"]
        else "fail"
        if steps["oracle"]["executed"]
        else "not-run"
    )
    if receipt["oracle_outcome"] != expected_outcome:
        raise ValueError("oracle_outcome is inconsistent with the recorded lifecycle")

    if receipt["oracle_outcome"] == "pass":
        if not receipt["artifact_contract_valid"]:
            raise ValueError("oracle pass requires artifact_contract_valid=true")
        oracle = steps["oracle"]
        if (
            not oracle["executed"]
            or oracle["timed_out"]
            or oracle["exit_code"] != oracle["expected_exit_code"]
        ):
            raise ValueError("oracle pass requires a successful executed oracle step")


def verify_output_references(receipt: Mapping, artifact_root: Path) -> None:
    for name in STEP_NAMES:
        step = receipt["steps"][name]
        if not step["executed"]:
            continue
        for stream in ("stdout", "stderr"):
            reference = step[stream]
            path = resolve_relative_without_symlinks(
                artifact_root, reference["path"], "{}.{}".format(name, stream)
            )
            if sha256_file(path) != reference["digest"]:
                raise ValueError("{} {} digest mismatch".format(name, stream))


def verify_receipt_binding(
    receipt: Mapping,
    manifest_path: Path,
    manifest: Mapping,
    fixture: Mapping,
    artifact_root: Path,
) -> None:
    """Verify current local files agree with a receipt; this is not authentication."""

    validate_receipt(receipt)
    expected_fields = {
        "evidence_scope": manifest["evidence_scope"],
        "manifest_revision": manifest["manifest_revision"],
        "task_id": fixture["task_id"],
        "task_revision": fixture["task_revision"],
        "fixture_id": fixture["fixture_id"],
        "fixture_revision": fixture["fixture_revision"],
        "fixture_initial_digest": fixture["initial_state_digest"],
    }
    for field, expected in expected_fields.items():
        if receipt[field] != expected:
            raise ValueError("receipt {} does not match manifest".format(field))
    if receipt["manifest_digest"] != sha256_file(manifest_path):
        raise ValueError("receipt manifest_digest mismatch")
    if receipt["pre_run_digest"] != fixture["initial_state_digest"]:
        raise ValueError("receipt pre_run_digest does not match fixture initial digest")
    expected_step_argv = {
        "reset": list(fixture["reset"]["command"]),
        "setup": list(fixture["setup"]["command"]),
        "oracle": [
            str(artifact_root.resolve()) if argument == "<artifact-root>" else argument
            for argument in fixture["oracle"]["command"]
        ],
    }
    for name, expected_argv in expected_step_argv.items():
        if receipt["steps"][name]["argv"] != expected_argv:
            raise ValueError("receipt steps.{}.argv does not match manifest".format(name))
    if artifact_root.is_symlink() or not artifact_root.is_dir():
        raise ValueError("artifact root is not a regular directory")
    if receipt["artifact_inventory_digest"] != artifact_tree_digest_v2(artifact_root):
        raise ValueError("artifact inventory digest mismatch")
    artifact_errors = verify_artifact_contract(fixture["artifacts"], artifact_root)
    current_contract_valid = not artifact_errors
    if current_contract_valid != receipt["artifact_contract_valid"]:
        raise ValueError(
            "artifact contract no longer matches receipt: {}".format(
                "; ".join(artifact_errors) if artifact_errors else "receipt reported invalid"
            )
        )
    if receipt["oracle_outcome"] == "pass" and artifact_errors:
        raise ValueError("artifact contract is invalid: {}".format("; ".join(artifact_errors)))
    verify_output_references(receipt, artifact_root)
