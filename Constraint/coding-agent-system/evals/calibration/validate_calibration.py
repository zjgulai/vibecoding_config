#!/usr/bin/env python3
"""Fail-closed validation for calibration batches and capability cards."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence


EVALS_DIR = Path(__file__).resolve().parent.parent
if str(EVALS_DIR) not in sys.path:
    sys.path.insert(0, str(EVALS_DIR))

from eval_protocol import (  # noqa: E402
    artifact_tree_digest_v2,
    exact_fields,
    load_json,
    nonblank,
    nonnegative_integer,
    resolve_relative_without_symlinks,
    safe_relative_posix_path,
    sha256_file,
    tree_digest_v2,
    validate_digest,
)
from calibration_adapters.codex_eval10 import (  # noqa: E402
    CHILD_ENV_ALLOWLIST as CODEX_CHILD_ENV_ALLOWLIST,
    DISABLED_FEATURES as CODEX_DISABLED_FEATURES,
    MACOS_CONTAINMENT_PROFILE,
    MACOS_SANDBOX_EXEC,
    REAL_PROCESS_CONTAINMENT,
    build_codex_command,
)
from receipt import validate_receipt, verify_receipt_binding  # noqa: E402
from validate_fixture import find_fixture, validate_manifest_structure  # noqa: E402


PLATFORMS = ("codex", "claude-code", "deepseek-harness")
REQUIRED_STOP_CONDITIONS = {
    "control-digest-drift",
    "unresolved-model-alias",
    "secret-access-required",
    "unauthorized-network-tool",
    "unauthorized-write",
    "raw-output-secret-or-pii",
    "receipt-or-oracle-incomplete",
    "public-cli-unavailable",
}
REQUIRED_FORBIDDEN_DATA = {
    "credentials",
    "secrets",
    "environment-files",
    "account-content",
    "pii",
    "repository-content-outside-fixture",
}
REAL_SMOKE_AUTHORIZED_ACTIONS = {
    "model-request",
    "codex-client-network-transport",
    "synthetic-fixture-prompt-egress",
    "local-receipt-and-artifact-write",
    "authorization-consumption-registry-write",
}
REAL_SMOKE_FORBIDDEN_ACTIONS = {
    "retry",
    "web-search",
    "browser",
    "mcp",
    "agent-tool-use",
    "credential-content-inspection",
    "user-config-write",
    "git-write",
    "external-side-effect",
}
CODEX_REAL_HARNESS = "codex-cli-with-eval10-adapter"
CODEX_REAL_CLIENT = "codex-cli"
CODEX_INSTALLATION_PLATFORMS = {"darwin", "linux", "win32"}
CODEX_INSTALLATION_MACHINES = {"arm64", "x64"}
REQUIRED_REAL_UNVERIFIED_SCOPE = {
    "codex-package-publisher-authenticity",
    "provider-and-model-identity-authentication",
}
CAPABILITY_STATE_REASON_CODES = {
    "unobserved-no-retained-observation",
    "smoke-only-completed",
    "smoke-only-failed",
    "smoke-only-stopped",
    "provisionally-calibrated-completed",
    "provisionally-calibrated-failed",
    "provisionally-calibrated-stopped",
    "provisionally-calibrated-mixed-outcomes",
    "expired-claim-free-tombstone",
}
CAPABILITY_BLOCKER_CODES = {
    "real-model-request-not-run",
    "execution-configuration-not-control-bound",
    "provider-wire-request-count-cannot-be-enforced-to-one-for-the-built-in-chatgpt-provider-path",
    "codex-package-publisher-authenticity-and-provider-model-identity-remain-unverified",
    "revised-one-cli-invocation-authorization-required-before-real-smoke",
    "public-version-pinned-dsh-cli-not-available-on-path",
    "headless-execution-configuration-not-bindable",
}
EXECUTION_CONFIGURATION_BLOCKER_CODES = {
    "public-version-pinned-dsh-cli-not-available-on-path",
    "control-digest-drift",
}
EXPIRED_REASON_CODES = {"evidence-validity-window-elapsed"}
CODEX_PERMISSION_POLICY = {
    "approval": "never",
    "agent_workspace": "curated-temporary-read-only",
    "auth_home": "temporary-auth-only-copy-0600-source-integrity-checked",
    "parent_environment": "process-launch-allowlist",
    "project_instructions": "disabled-and-not-staged",
    "external_side_effects": "forbidden",
    "git_writes": "forbidden",
    "retries": 0,
}
CODEX_TOOL_POLICY = {
    "browser": False,
    "mcp": False,
    "native_web_search": False,
    "disabled_features": list(CODEX_DISABLED_FEATURES),
    "tool_calls": "disabled-by-cli-feature-gate-and-jsonl-event-gate",
}
CODEX_CONTROL_FIELDS = (
    "schema_version",
    "purpose",
    "execution_kind",
    "client",
    "expected_client_version",
    "requested_model",
    "resolved_model",
    "reasoning_effort",
    "profile",
    "permissions",
    "permissions_digest",
    "toolset",
    "toolset_digest",
    "provider_usage_binding",
    "billed_cost",
    "derived_cost",
    "prompt_digest",
    "installation_identity_digest",
    "batch_id",
    "batch_plan_digest",
    "authorization_ref_digest",
    "adapter_digest",
    "adapter_ref",
    "prompt_ref",
)
PROVIDER_INVOCATION_FIELDS = (
    "schema_version",
    "sidecar_revision",
    "argv_template",
    "argv_template_digest",
    "runtime_executable_digest",
    "installation_identity_digest",
    "authorization_grant_digest",
    "prompt_digest",
    "requested_model",
    "resolved_model",
    "model_resolution_status",
    "reasoning_effort",
    "environment_keys",
    "codex_home_shape",
    "expected_cli_invocations",
    "harness_retries",
    "provider_request_count",
    "client_process_executed",
    "exit_code",
    "timed_out",
    "completed_event_observed",
    "invocation_started_at",
    "invocation_finished_at",
    "process_containment",
    "containment_profile_digest",
)

BATCH_FIELDS = (
    "schema_version",
    "batch_id",
    "batch_revision",
    "execution_mode",
    "purpose",
    "fixture_binding",
    "treatment",
    "fixed_controls",
    "data_egress",
    "budget",
    "authorization",
    "stop_conditions",
    "execution_configurations",
    "invocations",
    "claims",
)
EXECUTION_CONFIGURATION_FIELDS = (
    "configuration_id",
    "platform",
    "harness",
    "client_version",
    "requested_model",
    "resolved_model",
    "model_resolution_status",
    "reasoning",
    "profile",
    "permissions_digest",
    "toolset_digest",
    "adapter_revision",
    "binding_state",
    "blocker",
)
INVOCATION_FIELDS = (
    "invocation_id",
    "configuration_id",
    "platform",
    "plan_state",
    "execute",
    "executable",
    "cwd",
    "argv",
    "input_transport",
    "stdin_source",
    "stdout_format",
    "stderr_policy",
    "network_policy",
    "file_policy",
    "expected_cli_invocations",
    "expected_provider_requests",
    "blocker",
)
CARD_FIELDS = (
    "schema_version",
    "card_id",
    "card_revision",
    "platform",
    "execution_configuration",
    "evidence_state",
    "evidence_basis",
    "state_reason",
    "observed_runs",
    "task_shapes",
    "outcome_summary",
    "batch_binding",
    "measurements",
    "evidence",
    "blockers",
    "valid_until",
    "expired_reason",
    "decision",
)
SMOKE_OBSERVATION_FIELDS = (
    "schema_version",
    "observation_revision",
    "observation_id",
    "observation_kind",
    "scope",
    "task_id",
    "task_shape",
    "execution_configuration",
    "execution_configuration_digest",
    "receipt_configuration_digest",
    "outcome",
    "oracle_outcome",
    "batch_binding",
    "lifecycle_binding",
    "summary_ref",
    "receipt_ref",
    "measurements",
    "unverified_scope",
)
SMOKE_SUMMARY_FIELDS = (
    "schema_version",
    "task_id",
    "execution_configuration_id",
    "execution_configuration_digest",
    "receipt_configuration_digest",
    "batch_binding",
    "execution_identity",
    "run_status",
    "failure",
    "oracle_outcome",
    "quality_assessment",
    "quality_comparison",
    "inference",
    "measurements",
    "raw_output_sentinel_detected",
    "receipt_path",
    "observation_path",
    "raw_stdout_path",
    "raw_stderr_path",
    "quarantine_created",
    "mechanically_eligible",
    "unverified_scope",
)
EXECUTION_IDENTITY_FIELDS = (
    "executor",
    "agent",
    "client_version",
    "requested_model",
    "resolved_model",
    "reasoning_effort",
    "real_agent_execution",
    "identity_authentication",
    "installation_identity_digest",
)
INSTALLATION_IDENTITY_FIELDS = (
    "schema_version",
    "identity_revision",
    "package_name",
    "package_version",
    "package_manifest_digest",
    "entrypoint_digest",
    "native_package_name",
    "native_package_version",
    "native_package_manifest_digest",
    "native_binary_digest",
    "platform",
    "machine",
    "identity_digest",
)
AUTHORIZATION_GRANT_FIELDS = (
    "schema_version",
    "grant_revision",
    "grant_id",
    "nonce",
    "source",
    "decision",
    "platform",
    "batch_id",
    "batch_digest",
    "installation_identity_digest",
    "authorized_actions",
    "forbidden_actions",
    "allowed_egress",
    "network_scope",
    "max_cli_invocations",
    "max_provider_requests",
    "max_billed_cost_usd",
    "billed_cost_limit_source",
    "expires_at",
)
LIFECYCLE_BINDING_FIELDS = (
    "manifest_ref",
    "configuration_root",
    "control_ref",
    "artifact_root",
    "fixture_root",
    "prompt_ref",
    "adapter_ref",
    "installation_ref",
    "authorization_ref",
    "authorization_consumption_ref",
)


def _mapping(value: object, label: str) -> Mapping:
    if not isinstance(value, dict):
        raise ValueError("{} must be an object".format(label))
    return value


def _array(value: object, label: str, *, minimum: int = 0) -> List:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError("{} must be an array with at least {} item(s)".format(label, minimum))
    return value


def _boolean(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError("{} must be a boolean".format(label))
    return value


def _enum(value: object, allowed: Sequence[str], label: str) -> str:
    selected = nonblank(value, label)
    if selected not in allowed:
        raise ValueError("{} must be one of: {}".format(label, ", ".join(allowed)))
    return selected


def _nullable_nonblank(value: object, label: str) -> Optional[str]:
    if value is None:
        return None
    return nonblank(value, label)


def _nullable_digest(value: object, label: str) -> Optional[str]:
    if value is None:
        return None
    return validate_digest(value, label, allow_zero=False)


def _nullable_safe_path(value: object, label: str) -> Optional[str]:
    if value is None:
        return None
    return safe_relative_posix_path(value, label)


def _nullable_nonnegative_integer(value: object, label: str) -> Optional[int]:
    if value is None:
        return None
    return nonnegative_integer(value, label)


def _nullable_nonnegative_number(value: object, label: str) -> Optional[float]:
    if value is None:
        return None
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise ValueError("{} must be null or a finite non-negative number".format(label))
    return float(value)


def _unique_nonblank_strings(value: object, label: str) -> List[str]:
    items = _array(value, label)
    validated = [nonblank(item, "{}[{}]".format(label, index)) for index, item in enumerate(items)]
    if len(set(validated)) != len(validated):
        raise ValueError("{} must not contain duplicates".format(label))
    return validated


def _derived_state_reason(
    evidence_state: str, outcome_summary: Optional[Mapping]
) -> str:
    if evidence_state == "unobserved":
        return "unobserved-no-retained-observation"
    if evidence_state == "expired":
        return "expired-claim-free-tombstone"
    if outcome_summary is None:
        raise ValueError("observed capability card requires outcome_summary")
    active = [
        name
        for name in ("completed", "failed", "stopped")
        if outcome_summary[name] > 0
    ]
    if len(active) == 1:
        return "{}-{}".format(evidence_state, active[0])
    return "{}-mixed-outcomes".format(evidence_state)


def _validate_execution_configuration(
    value: object, label: str, *, controlled_blocker: bool = False
) -> Dict:
    configuration = _mapping(value, label)
    exact_fields(
        configuration,
        EXECUTION_CONFIGURATION_FIELDS,
        EXECUTION_CONFIGURATION_FIELDS,
        label,
    )
    nonblank(configuration["configuration_id"], label + ".configuration_id")
    platform = _enum(configuration["platform"], PLATFORMS, label + ".platform")
    nonblank(configuration["harness"], label + ".harness")
    nonblank(configuration["client_version"], label + ".client_version")
    requested_model = _nullable_nonblank(
        configuration["requested_model"], label + ".requested_model"
    )
    resolved_model = _nullable_nonblank(
        configuration["resolved_model"], label + ".resolved_model"
    )
    model_resolution_status = _enum(
        configuration["model_resolution_status"],
        ("not-observed", "client-catalog-alias", "provider-resolved-id"),
        label + ".model_resolution_status",
    )
    _nullable_nonblank(configuration["reasoning"], label + ".reasoning")
    nonblank(configuration["profile"], label + ".profile")
    permissions_digest = _nullable_digest(
        configuration["permissions_digest"], label + ".permissions_digest"
    )
    toolset_digest = _nullable_digest(
        configuration["toolset_digest"], label + ".toolset_digest"
    )
    nonblank(configuration["adapter_revision"], label + ".adapter_revision")
    binding_state = _enum(
        configuration["binding_state"],
        ("declared-unbound", "control-bound", "receipt-bound", "blocked"),
        label + ".binding_state",
    )
    blocker = _nullable_nonblank(configuration["blocker"], label + ".blocker")
    if (
        controlled_blocker
        and blocker is not None
        and blocker not in EXECUTION_CONFIGURATION_BLOCKER_CODES
    ):
        raise ValueError("{}.blocker must be an allowed reason code".format(label))
    if model_resolution_status == "not-observed":
        if requested_model is not None or resolved_model is not None:
            raise ValueError(
                "{} not-observed model identity requires requested_model and resolved_model null".format(
                    label
                )
            )
    elif model_resolution_status == "client-catalog-alias":
        if requested_model is None or resolved_model is not None:
            raise ValueError(
                "{} client-catalog-alias requires requested_model and null resolved_model".format(
                    label
                )
            )
    elif requested_model is None or resolved_model is None:
        raise ValueError(
            "{} provider-resolved-id requires requested_model and resolved_model".format(label)
        )

    if binding_state in ("control-bound", "receipt-bound"):
        if (
            requested_model is None
            or model_resolution_status == "not-observed"
            or permissions_digest is None
            or toolset_digest is None
        ):
            raise ValueError(
                "{} {} requires requested model binding, permissions_digest and toolset_digest".format(
                    label, binding_state
                )
            )
        if blocker is not None:
            raise ValueError("{} bound configuration cannot declare blocker".format(label))
    elif binding_state == "blocked":
        if blocker is None:
            raise ValueError("{} blocked configuration requires blocker".format(label))
        if (
            requested_model is not None
            or resolved_model is not None
            or model_resolution_status != "not-observed"
            or permissions_digest is not None
            or toolset_digest is not None
        ):
            raise ValueError("{} blocked configuration must keep unresolved controls null".format(label))
    else:
        if blocker is not None:
            raise ValueError("{} declared-unbound configuration cannot declare blocker".format(label))
        if (
            requested_model is not None
            or resolved_model is not None
            or model_resolution_status != "not-observed"
            or permissions_digest is not None
            or toolset_digest is not None
        ):
            raise ValueError(
                "{} declared-unbound configuration must keep model identity and control digests null".format(
                    label
                )
            )
    return {
        "configuration_id": configuration["configuration_id"],
        "platform": platform,
        "binding_state": binding_state,
        "requested_model": requested_model,
        "resolved_model": resolved_model,
        "model_resolution_status": model_resolution_status,
    }


def _validate_fixture_binding(value: object) -> str:
    label = "fixture_binding"
    binding = _mapping(value, label)
    fields = (
        "state",
        "manifest_path",
        "manifest_digest",
        "task_id",
        "task_revision",
        "fixture_id",
        "fixture_revision",
        "initial_state_digest",
        "prompt_digest",
        "oracle_revision",
    )
    exact_fields(binding, fields, fields, label)
    state = _enum(binding["state"], ("unbound", "bound"), label + ".state")
    nonblank(binding["task_id"], label + ".task_id")
    nonblank(binding["fixture_id"], label + ".fixture_id")
    nullable_values = {
        "manifest_path": _nullable_safe_path(binding["manifest_path"], label + ".manifest_path"),
        "manifest_digest": _nullable_digest(
            binding["manifest_digest"], label + ".manifest_digest"
        ),
        "task_revision": _nullable_nonblank(binding["task_revision"], label + ".task_revision"),
        "fixture_revision": _nullable_nonblank(
            binding["fixture_revision"], label + ".fixture_revision"
        ),
        "initial_state_digest": _nullable_digest(
            binding["initial_state_digest"], label + ".initial_state_digest"
        ),
        "prompt_digest": _nullable_digest(binding["prompt_digest"], label + ".prompt_digest"),
        "oracle_revision": _nullable_nonblank(
            binding["oracle_revision"], label + ".oracle_revision"
        ),
    }
    if state == "unbound" and any(item is not None for item in nullable_values.values()):
        raise ValueError("fixture_binding unbound state requires all binding evidence to be null")
    if state == "bound" and any(item is None for item in nullable_values.values()):
        raise ValueError("fixture_binding bound state requires every binding evidence field")
    return state


def _validate_treatment(value: object) -> None:
    label = "treatment"
    treatment = _mapping(value, label)
    fields = ("mode", "variable", "baseline", "candidate", "comparison_authorized")
    exact_fields(treatment, fields, fields, label)
    mode = _enum(treatment["mode"], ("none", "single-variable"), label + ".mode")
    comparison_authorized = _boolean(
        treatment["comparison_authorized"], label + ".comparison_authorized"
    )
    if mode == "none":
        if any(treatment[field] is not None for field in ("variable", "baseline", "candidate")):
            raise ValueError("treatment mode none requires null variable, baseline and candidate")
        if comparison_authorized:
            raise ValueError("treatment mode none cannot authorize comparison")
        return
    nonblank(treatment["variable"], label + ".variable")
    for field in ("baseline", "candidate"):
        item = treatment[field]
        if item is None or isinstance(item, (list, dict)):
            raise ValueError("treatment.{} must be one non-null scalar".format(field))
    if treatment["baseline"] == treatment["candidate"]:
        raise ValueError("treatment baseline and candidate must differ")
    if not comparison_authorized:
        raise ValueError("single-variable treatment requires explicit comparison authorization")


def _validate_fixed_controls(value: object) -> None:
    label = "fixed_controls"
    controls = _mapping(value, label)
    fields = (
        "repetitions_per_configuration",
        "workspace_mode",
        "prompt_source",
        "web_search_enabled",
        "browser_enabled",
        "mcp_enabled",
        "external_side_effects_enabled",
        "git_writes_enabled",
        "retries",
        "oracle_required",
        "raw_stdout_required",
        "raw_stderr_required",
        "receipt_required",
        "smoke_observation_required",
    )
    exact_fields(controls, fields, fields, label)
    nonnegative_integer(
        controls["repetitions_per_configuration"],
        label + ".repetitions_per_configuration",
        minimum=1,
    )
    if controls["workspace_mode"] != "read-only":
        raise ValueError("fixed_controls.workspace_mode must be read-only")
    if controls["prompt_source"] != "fixture-only":
        raise ValueError("fixed_controls.prompt_source must be fixture-only")
    for field in (
        "web_search_enabled",
        "browser_enabled",
        "mcp_enabled",
        "external_side_effects_enabled",
        "git_writes_enabled",
    ):
        if _boolean(controls[field], label + "." + field):
            raise ValueError("fixed_controls.{} must be false".format(field))
    if nonnegative_integer(controls["retries"], label + ".retries") != 0:
        raise ValueError("fixed_controls.retries must be 0")
    for field in (
        "oracle_required",
        "raw_stdout_required",
        "raw_stderr_required",
        "receipt_required",
        "smoke_observation_required",
    ):
        if not _boolean(controls[field], label + "." + field):
            raise ValueError("fixed_controls.{} must be true".format(field))


def _validate_data_egress(value: object) -> str:
    label = "data_egress"
    data_egress = _mapping(value, label)
    fields = ("state", "allowed_payloads", "forbidden_data")
    exact_fields(data_egress, fields, fields, label)
    state = _enum(
        data_egress["state"],
        ("none-authorized", "fixture-only-authorized"),
        label + ".state",
    )
    allowed = _unique_nonblank_strings(data_egress["allowed_payloads"], label + ".allowed_payloads")
    forbidden = set(
        _unique_nonblank_strings(data_egress["forbidden_data"], label + ".forbidden_data")
    )
    missing = REQUIRED_FORBIDDEN_DATA - forbidden
    if missing:
        raise ValueError("data_egress.forbidden_data missing: {}".format(", ".join(sorted(missing))))
    if state == "none-authorized" and allowed:
        raise ValueError("data_egress none-authorized requires empty allowed_payloads")
    if state == "fixture-only-authorized" and allowed != ["synthetic-fixture-prompt"]:
        raise ValueError(
            "data_egress fixture-only-authorized permits only synthetic-fixture-prompt"
        )
    return state


def _validate_budget(value: object) -> Dict:
    label = "budget"
    budget = _mapping(value, label)
    fields = (
        "max_cli_invocations",
        "max_provider_requests",
        "max_tasks",
        "max_repetitions_per_configuration",
        "max_retries",
        "max_wall_clock_seconds",
        "max_billed_cost_usd",
        "billed_cost_limit_source",
    )
    exact_fields(budget, fields, fields, label)
    for field in (
        "max_cli_invocations",
        "max_tasks",
        "max_repetitions_per_configuration",
        "max_retries",
        "max_wall_clock_seconds",
    ):
        nonnegative_integer(budget[field], label + "." + field)
    _nullable_nonnegative_integer(
        budget["max_provider_requests"], label + ".max_provider_requests"
    )
    amount = _nullable_nonnegative_number(
        budget["max_billed_cost_usd"], label + ".max_billed_cost_usd"
    )
    source = _enum(
        budget["billed_cost_limit_source"],
        ("unknown", "provider-enforced", "operator-stop"),
        label + ".billed_cost_limit_source",
    )
    if source == "unknown" and amount is not None:
        raise ValueError("budget unknown billed cost limit must remain null")
    if source != "unknown" and amount is None:
        raise ValueError("budget known billed cost limit requires max_billed_cost_usd")
    return dict(budget)


def _validate_authorization(value: object) -> Dict:
    label = "authorization"
    authorization = _mapping(value, label)
    fields = (
        "state",
        "authorized_platforms",
        "authorized_actions",
        "forbidden_actions",
        "authorization_ref",
        "expires_at",
    )
    exact_fields(authorization, fields, fields, label)
    state = _enum(
        authorization["state"],
        (
            "not-authorized",
            "dry-run-only",
            "authorized-once",
            "authorized-batch",
            "blocked-after-preflight",
            "expired",
        ),
        label + ".state",
    )
    platforms = _unique_nonblank_strings(
        authorization["authorized_platforms"], label + ".authorized_platforms"
    )
    unknown_platforms = set(platforms) - set(PLATFORMS)
    if unknown_platforms:
        raise ValueError("authorization has unknown platform(s): {}".format(", ".join(sorted(unknown_platforms))))
    actions = _unique_nonblank_strings(
        authorization["authorized_actions"], label + ".authorized_actions"
    )
    forbidden = _unique_nonblank_strings(
        authorization["forbidden_actions"], label + ".forbidden_actions"
    )
    overlap = sorted(set(actions) & set(forbidden))
    if overlap:
        raise ValueError(
            "authorization cannot both authorize and forbid action(s): {}".format(
                ", ".join(overlap)
            )
        )
    authorization_ref = _nullable_safe_path(
        authorization["authorization_ref"], label + ".authorization_ref"
    )
    expires_at = _nullable_nonblank(authorization["expires_at"], label + ".expires_at")
    if state in ("not-authorized", "dry-run-only", "expired") and platforms:
        raise ValueError("authorization {} cannot authorize platforms".format(state))
    if state in ("authorized-once", "authorized-batch", "blocked-after-preflight"):
        if not platforms or authorization_ref is None or expires_at is None:
            raise ValueError("authorization {} requires platforms, ref and expiry".format(state))
    if state in ("authorized-once", "authorized-batch"):
        if "model-request" not in actions:
            raise ValueError(
                "authorization {} must explicitly authorize model-request".format(
                    state
                )
            )
    elif state in ("not-authorized", "dry-run-only", "expired"):
        if "model-request" in actions:
            raise ValueError(
                "authorization {} cannot authorize model-request".format(state)
            )
        if "model-request" not in forbidden:
            raise ValueError(
                "authorization {} must forbid model-request".format(state)
            )
    return {
        "state": state,
        "platforms": platforms,
        "actions": actions,
        "forbidden": forbidden,
    }


def _validate_stop_conditions(value: object) -> None:
    conditions = _array(value, "stop_conditions", minimum=1)
    ids = []
    fields = ("id", "action", "evidence_required")
    for index, raw in enumerate(conditions):
        label = "stop_conditions[{}]".format(index)
        condition = _mapping(raw, label)
        exact_fields(condition, fields, fields, label)
        condition_id = nonblank(condition["id"], label + ".id")
        ids.append(condition_id)
        if condition["action"] != "stop-no-retry":
            raise ValueError("{}.action must be stop-no-retry".format(label))
        nonblank(condition["evidence_required"], label + ".evidence_required")
    if len(set(ids)) != len(ids):
        raise ValueError("stop_conditions must not contain duplicate ids")
    actual = set(ids)
    if actual != REQUIRED_STOP_CONDITIONS:
        missing = REQUIRED_STOP_CONDITIONS - actual
        unexpected = actual - REQUIRED_STOP_CONDITIONS
        raise ValueError(
            "stop_conditions mismatch; missing={} unexpected={}".format(
                sorted(missing), sorted(unexpected)
            )
        )


def _require_argv_tokens(argv: List[str], tokens: Sequence[str], platform: str) -> None:
    missing = [token for token in tokens if token not in argv]
    if missing:
        raise ValueError("{} invocation missing required argv token(s): {}".format(platform, ", ".join(missing)))


def _require_option_value(argv: List[str], option: str, expected: str, platform: str) -> None:
    if option not in argv:
        raise ValueError("{} invocation missing {}".format(platform, option))
    index = argv.index(option)
    if index + 1 >= len(argv) or argv[index + 1] != expected:
        raise ValueError("{} invocation requires {} {}".format(platform, option, expected))


def _require_option_value_before(
    argv: List[str], option: str, expected: str, boundary: int, platform: str
) -> None:
    indices = [index for index, token in enumerate(argv) if token == option]
    if len(indices) != 1:
        raise ValueError(
            "{} invocation requires exactly one {} before exec".format(platform, option)
        )
    index = indices[0]
    if index >= boundary or index + 1 >= boundary or argv[index + 1] != expected:
        raise ValueError(
            "{} invocation requires {} {} before exec".format(
                platform, option, expected
            )
        )


def _require_token_after(
    argv: List[str], token: str, boundary: int, platform: str
) -> None:
    indices = [index for index, value in enumerate(argv) if value == token]
    if len(indices) != 1 or indices[0] <= boundary:
        raise ValueError(
            "{} invocation requires exactly one {} after exec".format(platform, token)
        )


def _validate_platform_argv(platform: str, argv: List[str]) -> None:
    if platform == "codex":
        expected = [
            "codex",
            "--ask-for-approval",
            "never",
            "--sandbox",
            "read-only",
            "--model",
            "<requested-model>",
            "--config",
            'model_reasoning_effort="<reasoning-effort>"',
            "--config",
            "project_doc_max_bytes=0",
            "--config",
            'web_search="disabled"',
        ]
        for feature in CODEX_DISABLED_FEATURES:
            expected.extend(("--disable", feature))
        expected.extend(
            (
                "--strict-config",
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--ignore-rules",
                "--skip-git-repo-check",
                "--cd",
                "<isolated-read-only-fixture-root>",
                "--color",
                "never",
                "--json",
                "--output-last-message",
                "<artifact-root>/decision-log.md",
                "-",
            )
        )
        if argv != expected:
            raise ValueError(
                "codex invocation must exactly match the hardened EVAL-10 command template"
            )
        return
    elif platform == "claude-code":
        expected = [
            "claude",
            "--print",
            "--bare",
            "--output-format",
            "json",
            "--input-format",
            "text",
            "--no-session-persistence",
            "--no-chrome",
            "--permission-mode",
            "dontAsk",
            "--tools",
            "Read,Glob,Grep",
            "--max-budget-usd",
            "<authorized-max-usd>",
            "--model",
            "<requested-model>",
            "--effort",
            "<reasoning-effort>",
        ]
        if argv != expected:
            raise ValueError(
                "claude-code invocation must exactly match the hardened command template"
            )
        return
    else:
        raise ValueError("deepseek-harness invocation must remain blocked")
    raise ValueError("deepseek-harness invocation must remain blocked")


def _validate_invocation(value: object, index: int, configurations: Mapping[str, Dict]) -> Dict:
    label = "invocations[{}]".format(index)
    invocation = _mapping(value, label)
    exact_fields(invocation, INVOCATION_FIELDS, INVOCATION_FIELDS, label)
    invocation_id = nonblank(invocation["invocation_id"], label + ".invocation_id")
    configuration_id = nonblank(
        invocation["configuration_id"], label + ".configuration_id"
    )
    if configuration_id not in configurations:
        raise ValueError("{} references unknown configuration_id".format(label))
    platform = _enum(invocation["platform"], PLATFORMS, label + ".platform")
    if platform != configurations[configuration_id]["platform"]:
        raise ValueError("{} platform does not match execution configuration".format(label))
    plan_state = _enum(invocation["plan_state"], ("planned", "blocked"), label + ".plan_state")
    execute = _boolean(invocation["execute"], label + ".execute")
    executable = _nullable_nonblank(invocation["executable"], label + ".executable")
    nonblank(invocation["cwd"], label + ".cwd")
    raw_argv = invocation["argv"]
    if raw_argv is None:
        argv: Optional[List[str]] = None
    else:
        argv = _array(raw_argv, label + ".argv", minimum=1)
        for argument_index, argument in enumerate(argv):
            nonblank(argument, "{}.argv[{}]".format(label, argument_index))
    input_transport = _enum(
        invocation["input_transport"],
        ("stdin", "argument", "not-applicable"),
        label + ".input_transport",
    )
    stdin_source = _nullable_nonblank(invocation["stdin_source"], label + ".stdin_source")
    stdout_format = _enum(
        invocation["stdout_format"],
        ("jsonl", "json", "text", "not-applicable"),
        label + ".stdout_format",
    )
    stderr_policy = _enum(
        invocation["stderr_policy"],
        ("capture", "not-applicable"),
        label + ".stderr_policy",
    )
    network_policy = _enum(
        invocation["network_policy"],
        (
            "codex-client-network-endpoints-unverified",
            "claude-client-network-endpoints-unverified",
            "blocked",
        ),
        label + ".network_policy",
    )
    if invocation["file_policy"] != "read-only":
        raise ValueError("{}.file_policy must be read-only".format(label))
    expected_cli_invocations = nonnegative_integer(
        invocation["expected_cli_invocations"], label + ".expected_cli_invocations"
    )
    expected_provider_requests = _nullable_nonnegative_integer(
        invocation["expected_provider_requests"], label + ".expected_provider_requests"
    )
    blocker = _nullable_nonblank(invocation["blocker"], label + ".blocker")
    if execute:
        if plan_state != "planned" or expected_cli_invocations != 1:
            raise ValueError(
                "{} executing invocation must be planned with exactly one CLI invocation".format(
                    label
                )
            )
    elif expected_cli_invocations != 0:
        raise ValueError("{} nonexecuting invocation must declare zero CLI invocations".format(label))

    if platform == "deepseek-harness":
        if (
            plan_state != "blocked"
            or execute
            or executable is not None
            or argv is not None
            or input_transport != "not-applicable"
            or stdin_source is not None
            or stdout_format != "not-applicable"
            or stderr_policy != "not-applicable"
            or network_policy != "blocked"
            or expected_cli_invocations != 0
            or expected_provider_requests not in (0, None)
            or blocker is None
        ):
            raise ValueError(
                "deepseek-harness invocation must remain blocked with null executable/argv and zero requests"
            )
    else:
        if executable is None or argv is None:
            raise ValueError("{} invocation must preserve a complete invocation plan".format(platform))
        if plan_state == "planned" and blocker is not None:
            raise ValueError("{} planned invocation cannot declare blocker".format(platform))
        if plan_state == "blocked" and blocker is None:
            raise ValueError("{} blocked invocation requires blocker".format(platform))
        if input_transport != "stdin" or stdin_source is None:
            raise ValueError("{} invocation must read the fixture prompt from stdin".format(platform))
        expected_network_policy = (
            "{}-client-network-endpoints-unverified".format(
                "codex" if platform == "codex" else "claude"
            )
            if plan_state == "planned"
            else "blocked"
        )
        if stderr_policy != "capture" or network_policy != expected_network_policy:
            raise ValueError(
                "{} invocation must capture stderr and use the network policy for its plan state".format(
                    platform
                )
            )
        _validate_platform_argv(platform, argv)
    return {
        "invocation_id": invocation_id,
        "configuration_id": configuration_id,
        "platform": platform,
        "plan_state": plan_state,
        "execute": execute,
        "expected_cli_invocations": expected_cli_invocations,
        "expected_provider_requests": expected_provider_requests,
    }


def _validate_claims(value: object) -> None:
    label = "claims"
    claims = _mapping(value, label)
    fields = (
        "quality_comparison",
        "inference",
        "winner",
        "ranking",
        "promotion_recommendation",
    )
    exact_fields(claims, fields, fields, label)
    if claims["quality_comparison"] != "not-computed" or claims["inference"] != "not-computed":
        raise ValueError("claims quality comparison and inference must be not-computed")
    for field in ("winner", "ranking", "promotion_recommendation"):
        if claims[field] is not None:
            raise ValueError("claims.{} must remain null".format(field))


def validate_batch(value: object) -> Dict:
    batch = _mapping(value, "batch")
    exact_fields(batch, BATCH_FIELDS, BATCH_FIELDS, "batch")
    if batch["schema_version"] != "1":
        raise ValueError("schema_version must be 1")
    batch_id = nonblank(batch["batch_id"], "batch_id")
    nonblank(batch["batch_revision"], "batch_revision")
    execution_mode = _enum(
        batch["execution_mode"],
        ("dry-run-only", "authorized-smoke", "authorized-calibration-batch"),
        "execution_mode",
    )
    nonblank(batch["purpose"], "purpose")
    fixture_state = _validate_fixture_binding(batch["fixture_binding"])
    _validate_treatment(batch["treatment"])
    _validate_fixed_controls(batch["fixed_controls"])
    data_egress_state = _validate_data_egress(batch["data_egress"])
    budget = _validate_budget(batch["budget"])
    authorization = _validate_authorization(batch["authorization"])
    _validate_stop_conditions(batch["stop_conditions"])

    configurations: Dict[str, Dict] = {}
    for index, raw in enumerate(_array(batch["execution_configurations"], "execution_configurations", minimum=1)):
        validated = _validate_execution_configuration(
            raw, "execution_configurations[{}]".format(index)
        )
        configuration_id = validated["configuration_id"]
        if configuration_id in configurations:
            raise ValueError("duplicate execution configuration id: {}".format(configuration_id))
        configurations[configuration_id] = validated

    invocations = []
    invocation_ids = set()
    for index, raw in enumerate(_array(batch["invocations"], "invocations", minimum=1)):
        validated = _validate_invocation(raw, index, configurations)
        if validated["invocation_id"] in invocation_ids:
            raise ValueError("duplicate invocation id: {}".format(validated["invocation_id"]))
        invocation_ids.add(validated["invocation_id"])
        invocations.append(validated)
    referenced = [item["configuration_id"] for item in invocations]
    if len(set(referenced)) != len(referenced) or set(referenced) != set(configurations):
        raise ValueError("invocations must bind one-to-one with execution_configurations")
    _validate_claims(batch["claims"])

    expected_cli_invocations = sum(
        item["expected_cli_invocations"] for item in invocations
    )
    provider_request_estimates = [
        item["expected_provider_requests"] for item in invocations
    ]
    expected_provider_requests = (
        None
        if any(value is None for value in provider_request_estimates)
        else sum(provider_request_estimates)
    )
    executing = [item for item in invocations if item["execute"]]
    if expected_cli_invocations > budget["max_cli_invocations"]:
        raise ValueError("invocation count exceeds CLI invocation budget")
    max_provider_requests = budget["max_provider_requests"]
    if (
        max_provider_requests is not None
        and expected_provider_requests is not None
        and expected_provider_requests > max_provider_requests
    ):
        raise ValueError("provider request estimate exceeds provider request budget")
    if max_provider_requests is not None and expected_provider_requests is None:
        raise ValueError(
            "unknown provider request estimate requires max_provider_requests null"
        )
    if budget["max_retries"] != batch["fixed_controls"]["retries"]:
        raise ValueError("budget max_retries must match fixed_controls retries")
    if budget["max_repetitions_per_configuration"] != batch["fixed_controls"]["repetitions_per_configuration"]:
        raise ValueError("budget repetition limit must match fixed_controls")

    if execution_mode == "dry-run-only":
        if authorization["state"] != "dry-run-only":
            raise ValueError("dry-run-only requires authorization state dry-run-only")
        if (
            budget["max_cli_invocations"] != 0
            or budget["max_wall_clock_seconds"] != 0
            or executing
            or expected_cli_invocations != 0
            or expected_provider_requests not in (0, None)
            or data_egress_state != "none-authorized"
        ):
            raise ValueError("dry-run-only requires zero requests, zero runtime, no execution and no data egress")
    elif authorization["state"] == "blocked-after-preflight":
        if fixture_state != "bound":
            raise ValueError("blocked-after-preflight requires bound fixture evidence")
        if data_egress_state != "fixture-only-authorized":
            raise ValueError("blocked-after-preflight preserves fixture-only egress scope")
        if executing or expected_cli_invocations != 0:
            raise ValueError("blocked-after-preflight must not execute a CLI invocation")
        if any(item["plan_state"] != "blocked" for item in invocations):
            raise ValueError("blocked-after-preflight requires every invocation to be blocked")
        if any(item["platform"] not in authorization["platforms"] for item in invocations):
            raise ValueError("blocked invocation platform is outside prior authorization")
    else:
        if fixture_state != "bound":
            raise ValueError("authorized execution requires bound fixture evidence")
        expected_authorization = (
            "authorized-once" if execution_mode == "authorized-smoke" else "authorized-batch"
        )
        if authorization["state"] != expected_authorization:
            raise ValueError("{} requires authorization state {}".format(execution_mode, expected_authorization))
        if data_egress_state != "fixture-only-authorized":
            raise ValueError("authorized execution permits only fixture prompt egress")
        if not executing or budget["max_cli_invocations"] < 1:
            raise ValueError("authorized execution requires explicit executing invocation and CLI budget")
        if any(item["platform"] not in authorization["platforms"] for item in executing):
            raise ValueError("executing platform is outside authorization")
        if execution_mode == "authorized-smoke":
            if set(authorization["actions"]) != REAL_SMOKE_AUTHORIZED_ACTIONS:
                raise ValueError(
                    "authorized-smoke authorized_actions must equal the real-smoke allowlist"
                )
            if set(authorization["forbidden"]) != REAL_SMOKE_FORBIDDEN_ACTIONS:
                raise ValueError(
                    "authorized-smoke forbidden_actions must equal the real-smoke denylist"
                )
            if (
                len(configurations) != 1
                or len(invocations) != 1
                or len(executing) != 1
                or expected_cli_invocations != 1
                or budget["max_cli_invocations"] != 1
                or budget["max_tasks"] != 1
                or batch["fixed_controls"]["repetitions_per_configuration"] != 1
            ):
                raise ValueError(
                    "authorized-smoke requires exactly one configuration, one "
                    "executing invocation, one CLI invocation, one task and one repetition"
                )

    return {
        "valid": True,
        "document": "calibration-batch",
        "batch_id": batch_id,
        "execution_mode": execution_mode,
        "planned_invocations": sum(item["plan_state"] == "planned" for item in invocations),
        "blocked_invocations": sum(item["plan_state"] == "blocked" for item in invocations),
        "cli_invocations_budget": budget["max_cli_invocations"],
        "provider_requests_budget": budget["max_provider_requests"],
        "terminal_state": (
            "blocked-after-preflight"
            if authorization["state"] == "blocked-after-preflight"
            else None
        ),
        "executed": bool(executing),
    }


def _validate_usage_measurement(value: object, label: str, *, derived: bool) -> None:
    measurement = _mapping(value, label)
    fields = (
        ("status", "input_tokens", "output_tokens", "method")
        if derived
        else (
            "status",
            "input_tokens",
            "output_tokens",
            "cached_input_tokens",
            "reasoning_output_tokens",
            "receipt_ref",
        )
    )
    exact_fields(measurement, fields, fields, label)
    known_status = "derived-estimate" if derived else "provider-receipt"
    status = _enum(measurement["status"], ("unknown", known_status), label + ".status")
    if status == "unknown":
        if any(measurement[field] is not None for field in fields if field != "status"):
            raise ValueError("{} unknown values must remain null".format(label))
        return
    for field in ("input_tokens", "output_tokens"):
        nonnegative_integer(measurement[field], label + "." + field)
    if derived:
        nonblank(measurement["method"], label + ".method")
    else:
        _nullable_nonnegative_integer(
            measurement["cached_input_tokens"], label + ".cached_input_tokens"
        )
        _nullable_nonnegative_integer(
            measurement["reasoning_output_tokens"], label + ".reasoning_output_tokens"
        )
        safe_relative_posix_path(measurement["receipt_ref"], label + ".receipt_ref")


def _validate_cost_measurement(value: object, label: str, *, derived: bool) -> None:
    measurement = _mapping(value, label)
    fields = ("status", "amount_usd", "method") if derived else (
        "status",
        "amount_usd",
        "receipt_ref",
    )
    exact_fields(measurement, fields, fields, label)
    known_status = "derived-estimate" if derived else "provider-billed"
    status = _enum(measurement["status"], ("unknown", known_status), label + ".status")
    if status == "unknown":
        if any(measurement[field] is not None for field in fields if field != "status"):
            raise ValueError("{} unknown values must remain null".format(label))
        return
    _nullable_nonnegative_number(measurement["amount_usd"], label + ".amount_usd")
    if measurement["amount_usd"] is None:
        raise ValueError("{} known value requires amount_usd".format(label))
    if derived:
        nonblank(measurement["method"], label + ".method")
    else:
        safe_relative_posix_path(measurement["receipt_ref"], label + ".receipt_ref")


def _validate_measurements(value: object) -> Dict[str, str]:
    measurements = _mapping(value, "measurements")
    fields = ("provider_usage", "derived_usage", "billed_cost", "derived_cost")
    exact_fields(measurements, fields, fields, "measurements")
    _validate_usage_measurement(measurements["provider_usage"], "provider_usage", derived=False)
    _validate_usage_measurement(measurements["derived_usage"], "derived_usage", derived=True)
    _validate_cost_measurement(measurements["billed_cost"], "billed_cost", derived=False)
    _validate_cost_measurement(measurements["derived_cost"], "derived_cost", derived=True)
    return {
        "provider_usage": measurements["provider_usage"]["status"],
        "derived_usage": measurements["derived_usage"]["status"],
        "billed_cost": measurements["billed_cost"]["status"],
        "derived_cost": measurements["derived_cost"]["status"],
    }


def _canonical_digest(value: object) -> str:
    payload = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _parse_timestamp(value: object, label: str) -> datetime:
    raw = nonblank(value, label)
    normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise ValueError("{} must be an ISO-8601 timestamp".format(label)) from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("{} must include a timezone".format(label))
    return parsed


def validate_installation_identity(value: object) -> Dict:
    label = "installation_identity"
    identity = _mapping(value, label)
    exact_fields(
        identity,
        INSTALLATION_IDENTITY_FIELDS,
        INSTALLATION_IDENTITY_FIELDS,
        label,
    )
    if identity["schema_version"] != "1":
        raise ValueError("installation identity schema_version must be 1")
    if identity["identity_revision"] != "codex-installation-identity-v1":
        raise ValueError(
            "installation identity revision must be codex-installation-identity-v1"
        )
    if identity["package_name"] != "@openai/codex":
        raise ValueError("installation identity package_name must be @openai/codex")
    package_version = nonblank(
        identity["package_version"], label + ".package_version"
    )
    if identity["native_package_name"] != "@openai/codex":
        raise ValueError(
            "installation identity native_package_name must be @openai/codex"
        )
    native_version = nonblank(
        identity["native_package_version"], label + ".native_package_version"
    )
    if not native_version.startswith(package_version + "-"):
        raise ValueError(
            "installation identity native package version must extend package version"
        )
    for field in (
        "package_manifest_digest",
        "entrypoint_digest",
        "native_package_manifest_digest",
        "native_binary_digest",
    ):
        validate_digest(identity[field], label + "." + field, allow_zero=False)
    platform_name = nonblank(identity["platform"], label + ".platform")
    machine_name = nonblank(identity["machine"], label + ".machine")
    if platform_name not in CODEX_INSTALLATION_PLATFORMS:
        raise ValueError("installation identity platform is unsupported")
    if machine_name not in CODEX_INSTALLATION_MACHINES:
        raise ValueError("installation identity machine is unsupported")
    expected_native_version = "{}-{}-{}".format(
        package_version, platform_name, machine_name
    )
    if native_version != expected_native_version:
        raise ValueError(
            "installation identity native package version must bind platform and machine"
        )
    identity_digest = validate_digest(
        identity["identity_digest"], label + ".identity_digest", allow_zero=False
    )
    payload = {
        field: identity[field]
        for field in INSTALLATION_IDENTITY_FIELDS
        if field != "identity_digest"
    }
    if identity_digest != _canonical_digest(payload):
        raise ValueError("installation identity self digest mismatch")
    return dict(identity)


def _open_regular_json(path: Path, label: str) -> Mapping:
    if path.is_symlink() or not path.is_file():
        raise ValueError("{} must be a regular file".format(label))
    try:
        return _mapping(load_json(path), label)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("{} must contain valid JSON".format(label)) from error


def _validate_retained_codex_installation(
    evidence_root: Path,
    installation_reference: Mapping[str, str],
    identity: Mapping,
) -> Dict[str, Path]:
    """Re-hash a portable retained npm/native snapshot instead of trusting claims."""

    identity_path = _resolve_bound_path(
        evidence_root,
        installation_reference["path"],
        "lifecycle_binding.installation_ref",
        directory=False,
    )
    root = evidence_root.resolve()
    snapshot_relative = (
        identity_path.parent / "installation-artifacts"
    ).relative_to(root).as_posix()
    try:
        snapshot_root = _resolve_bound_path(
            evidence_root,
            snapshot_relative,
            "retained Codex installation artifacts",
            directory=True,
        )
    except ValueError as error:
        raise ValueError(
            "retained Codex installation artifacts are missing"
        ) from error
    package_root = _resolve_bound_path(
        evidence_root,
        (snapshot_root / "package").relative_to(root).as_posix(),
        "retained Codex package root",
        directory=True,
    )
    package_manifest_path = _resolve_bound_path(
        evidence_root,
        (package_root / "package.json").relative_to(root).as_posix(),
        "retained Codex package manifest",
        directory=False,
    )
    entrypoint_path = _resolve_bound_path(
        evidence_root,
        (package_root / "bin" / "codex.js").relative_to(root).as_posix(),
        "retained Codex entrypoint",
        directory=False,
    )
    native_dependency = "codex-{}-{}".format(
        identity["platform"], identity["machine"]
    )
    native_root = package_root / "node_modules" / "@openai" / native_dependency
    native_root = _resolve_bound_path(
        evidence_root,
        native_root.relative_to(root).as_posix(),
        "retained Codex native package root",
        directory=True,
    )
    native_manifest_path = _resolve_bound_path(
        evidence_root,
        (native_root / "package.json").relative_to(root).as_posix(),
        "retained Codex native package manifest",
        directory=False,
    )
    package_manifest = _open_regular_json(
        package_manifest_path, "retained Codex package manifest"
    )
    native_manifest = _open_regular_json(
        native_manifest_path, "retained Codex native package manifest"
    )
    binary_names = {"codex", "codex.exe"}
    native_binary_candidates = sorted(
        path
        for path in (native_root / "vendor").glob("*/bin/*")
        if path.name in binary_names and not path.is_symlink() and path.is_file()
    )
    if len(native_binary_candidates) != 1:
        raise ValueError(
            "retained Codex native package must contain exactly one binary"
        )
    native_binary_path = _resolve_bound_path(
        evidence_root,
        native_binary_candidates[0].relative_to(root).as_posix(),
        "retained Codex native binary",
        directory=False,
    )
    if not native_binary_path.stat().st_mode & 0o111:
        raise ValueError("retained Codex native binary must be executable")

    expected_native_version = "{}-{}-{}".format(
        identity["package_version"], identity["platform"], identity["machine"]
    )
    expected_dependency = "npm:@openai/codex@{}".format(
        expected_native_version
    )
    optional_dependencies = package_manifest.get("optionalDependencies")
    if (
        package_manifest.get("name") != "@openai/codex"
        or package_manifest.get("version") != identity["package_version"]
        or package_manifest.get("bin") != {"codex": "bin/codex.js"}
        or not isinstance(optional_dependencies, dict)
        or optional_dependencies.get(
            "@openai/codex-{}-{}".format(
                identity["platform"], identity["machine"]
            )
        )
        != expected_dependency
    ):
        raise ValueError("retained Codex package metadata mismatch")
    if (
        native_manifest.get("name") != "@openai/codex"
        or native_manifest.get("version") != expected_native_version
        or native_manifest.get("os") != [identity["platform"]]
        or native_manifest.get("cpu") != [identity["machine"]]
    ):
        raise ValueError("retained Codex native package metadata mismatch")

    expected_digests = {
        package_manifest_path: identity["package_manifest_digest"],
        entrypoint_path: identity["entrypoint_digest"],
        native_manifest_path: identity["native_package_manifest_digest"],
        native_binary_path: identity["native_binary_digest"],
    }
    for path, expected in expected_digests.items():
        if sha256_file(path) != expected:
            raise ValueError("retained Codex installation artifact digest mismatch")
    return {
        "package_manifest": package_manifest_path.resolve(),
        "entrypoint": entrypoint_path.resolve(),
        "native_manifest": native_manifest_path.resolve(),
        "native_binary": native_binary_path.resolve(),
    }


def _retained_oracle_revision(fixture: Mapping, fixture_root: Path) -> str:
    oracle = _mapping(fixture.get("oracle"), "retained fixture oracle")
    command = _array(oracle.get("command"), "retained fixture oracle.command", minimum=1)
    executable_relative = safe_relative_posix_path(
        str(command[0]).removeprefix("./"),
        "retained fixture oracle executable",
    )
    executable = resolve_relative_without_symlinks(
        fixture_root,
        executable_relative,
        "retained fixture oracle executable",
    )
    if executable.is_symlink() or not executable.is_file():
        raise ValueError("retained fixture oracle executable must be a regular file")
    return _canonical_digest(
        {
            "contract_revision": "retained-oracle-contract-v1",
            "oracle": oracle,
            "executable_path": executable_relative,
            "executable_digest": sha256_file(executable),
        }
    )


def _validate_codex_control(control: Mapping) -> None:
    exact_fields(control, CODEX_CONTROL_FIELDS, CODEX_CONTROL_FIELDS, "control")
    if control["schema_version"] != "1":
        raise ValueError("control schema_version must be 1")
    fixed_values = {
        "purpose": "eval-10-connectivity-smoke",
        "execution_kind": "real",
        "client": CODEX_REAL_CLIENT,
        "profile": "custom",
        "permissions": CODEX_PERMISSION_POLICY,
        "toolset": CODEX_TOOL_POLICY,
        "provider_usage_binding": "unavailable",
        "billed_cost": None,
        "derived_cost": None,
    }
    for field, expected in fixed_values.items():
        if control[field] != expected:
            raise ValueError("control unsafe or unsupported value at {}".format(field))
    expected_permissions_digest = _canonical_digest(CODEX_PERMISSION_POLICY)
    expected_toolset_digest = _canonical_digest(CODEX_TOOL_POLICY)
    if control["permissions_digest"] != expected_permissions_digest:
        raise ValueError("control permissions digest does not bind the safe policy")
    if control["toolset_digest"] != expected_toolset_digest:
        raise ValueError("control toolset digest does not bind the safe policy")


def _validate_provider_invocation_sidecar(
    sidecar: Mapping,
    *,
    configuration: Mapping,
    runtime_executable_digest: str,
    installation_identity_digest: str,
    authorization_grant_digest: str,
    prompt_digest: str,
    outcome: Mapping,
    consumed_at: datetime,
    grant_expires_at: datetime,
    wrapper_step: Mapping,
) -> None:
    exact_fields(
        sidecar,
        PROVIDER_INVOCATION_FIELDS,
        PROVIDER_INVOCATION_FIELDS,
        "provider invocation sidecar",
    )
    if sidecar["schema_version"] != "2":
        raise ValueError("provider invocation sidecar schema_version must be 2")
    if sidecar["sidecar_revision"] != "codex-provider-invocation-v2":
        raise ValueError("provider invocation sidecar revision mismatch")
    inner_template = build_codex_command(
        Path("codex"),
        model="<requested-model>",
        reasoning_effort="<reasoning-effort>",
        model_root=Path("<isolated-read-only-fixture-root>"),
        decision_path=Path("<artifact-root>/decision-log.md"),
    )
    expected_template = [
        str(MACOS_SANDBOX_EXEC),
        "-p",
        "<containment-profile>",
        *inner_template,
    ]
    if sidecar["argv_template"] != expected_template:
        raise ValueError("provider invocation sidecar argv template mismatch")
    if sidecar["argv_template_digest"] != _canonical_digest(expected_template):
        raise ValueError("provider invocation sidecar argv digest mismatch")
    expected_values = {
        "requested_model": configuration["requested_model"],
        "resolved_model": configuration["resolved_model"],
        "model_resolution_status": configuration["model_resolution_status"],
        "reasoning_effort": configuration["reasoning"],
        "runtime_executable_digest": runtime_executable_digest,
        "installation_identity_digest": installation_identity_digest,
        "authorization_grant_digest": authorization_grant_digest,
        "prompt_digest": prompt_digest,
        "codex_home_shape": "temporary-auth-only-copy-0600",
        "expected_cli_invocations": 1,
        "harness_retries": 0,
        "provider_request_count": None,
        "process_containment": REAL_PROCESS_CONTAINMENT,
        "containment_profile_digest": _canonical_digest(
            MACOS_CONTAINMENT_PROFILE
        ),
    }
    for field, expected in expected_values.items():
        if sidecar[field] != expected:
            raise ValueError(
                "provider invocation sidecar mismatch at {}".format(field)
            )
    environment_keys = _unique_nonblank_strings(
        sidecar["environment_keys"], "provider invocation sidecar.environment_keys"
    )
    allowed_keys = set(CODEX_CHILD_ENV_ALLOWLIST) | {
        "CODEX_HOME",
        "NO_COLOR",
    }
    if (
        environment_keys != sorted(environment_keys)
        or not {"PATH", "CODEX_HOME", "NO_COLOR"}.issubset(environment_keys)
        or not set(environment_keys).issubset(allowed_keys)
    ):
        raise ValueError("provider invocation sidecar environment is unsafe")
    if sidecar["client_process_executed"] is not True:
        raise ValueError("provider invocation sidecar does not prove a client process")
    started_at = _parse_timestamp(
        sidecar["invocation_started_at"],
        "provider invocation sidecar.invocation_started_at",
    )
    finished_at = _parse_timestamp(
        sidecar["invocation_finished_at"],
        "provider invocation sidecar.invocation_finished_at",
    )
    future_limit = datetime.now(timezone.utc) + timedelta(minutes=5)
    if started_at > future_limit or finished_at > future_limit:
        raise ValueError("provider invocation timestamps are implausibly in the future")
    if not consumed_at <= started_at <= finished_at <= grant_expires_at:
        raise ValueError(
            "authorization consumption, invocation, and expiry timestamps are out of order"
        )
    timed_out = _boolean(sidecar["timed_out"], "provider invocation sidecar.timed_out")
    completed_event = _boolean(
        sidecar["completed_event_observed"],
        "provider invocation sidecar.completed_event_observed",
    )
    exit_code = sidecar["exit_code"]
    if exit_code is not None and (
        isinstance(exit_code, bool) or not isinstance(exit_code, int)
    ):
        raise ValueError("provider invocation sidecar exit_code must be null or integer")
    if timed_out != (exit_code is None):
        raise ValueError(
            "provider invocation sidecar timeout and child exit_code are inconsistent"
        )
    if not wrapper_step.get("executed") or wrapper_step.get("timed_out"):
        raise ValueError(
            "provider invocation sidecar cannot prove an incomplete adapter wrapper"
        )
    wrapper_exit = wrapper_step.get("exit_code")
    if isinstance(wrapper_exit, bool) or not isinstance(wrapper_exit, int):
        raise ValueError("adapter wrapper exit_code must be an integer")
    if timed_out != (wrapper_exit == 124):
        raise ValueError(
            "adapter wrapper timeout outcome does not match provider sidecar"
        )
    if wrapper_exit == 0 and (
        exit_code != 0 or timed_out or not completed_event
    ):
        raise ValueError(
            "successful adapter wrapper requires a completed child invocation"
        )
    if outcome["status"] == "completed":
        if timed_out or exit_code != 0 or not completed_event:
            raise ValueError(
                "completed smoke requires a completed provider invocation sidecar"
            )


def validate_authorization_grant(
    value: object,
    *,
    batch: Mapping,
    batch_digest: str,
    installation_identity_digest: str,
    require_unexpired: bool = False,
) -> Dict:
    label = "authorization_grant"
    grant = _mapping(value, label)
    exact_fields(grant, AUTHORIZATION_GRANT_FIELDS, AUTHORIZATION_GRANT_FIELDS, label)
    if grant["schema_version"] != "1":
        raise ValueError("authorization grant schema_version must be 1")
    if grant["grant_revision"] != "calibration-authorization-grant-v1":
        raise ValueError(
            "authorization grant revision must be calibration-authorization-grant-v1"
        )
    grant_id = nonblank(grant["grant_id"], label + ".grant_id")
    nonce = nonblank(grant["nonce"], label + ".nonce")
    if grant["source"] != "interactive-user-authorization":
        raise ValueError(
            "authorization grant source must be interactive-user-authorization"
        )
    if grant["decision"] != "approved-once":
        raise ValueError("authorization grant decision must be approved-once")
    if grant["platform"] != "codex":
        raise ValueError("authorization grant platform must be codex")
    if grant["batch_id"] != batch.get("batch_id"):
        raise ValueError("authorization grant batch_id mismatch")
    validated_batch_digest = validate_digest(
        grant["batch_digest"], label + ".batch_digest", allow_zero=False
    )
    if validated_batch_digest != batch_digest:
        raise ValueError("authorization grant batch digest mismatch")
    validated_installation_digest = validate_digest(
        grant["installation_identity_digest"],
        label + ".installation_identity_digest",
        allow_zero=False,
    )
    if validated_installation_digest != installation_identity_digest:
        raise ValueError("authorization grant installation identity mismatch")
    actions = _unique_nonblank_strings(
        grant["authorized_actions"], label + ".authorized_actions"
    )
    forbidden = _unique_nonblank_strings(
        grant["forbidden_actions"], label + ".forbidden_actions"
    )
    if set(actions) & set(forbidden):
        raise ValueError("authorization grant action sets must be disjoint")
    if set(actions) != REAL_SMOKE_AUTHORIZED_ACTIONS:
        raise ValueError(
            "authorization grant authorized_actions must equal the real-smoke allowlist"
        )
    if set(forbidden) != REAL_SMOKE_FORBIDDEN_ACTIONS:
        raise ValueError(
            "authorization grant forbidden_actions must equal the real-smoke denylist"
        )
    authorization = _mapping(batch.get("authorization"), "batch.authorization")
    if actions != authorization.get("authorized_actions"):
        raise ValueError("authorization grant authorized_actions mismatch")
    if forbidden != authorization.get("forbidden_actions"):
        raise ValueError("authorization grant forbidden_actions mismatch")
    allowed_egress = _unique_nonblank_strings(
        grant["allowed_egress"], label + ".allowed_egress"
    )
    if allowed_egress != ["synthetic-fixture-prompt"]:
        raise ValueError(
            "authorization grant allowed_egress must be synthetic-fixture-prompt only"
        )
    if grant["network_scope"] != "codex-client-network-endpoints-unverified":
        raise ValueError(
            "authorization grant network_scope must preserve unverified Codex client endpoints"
        )
    if nonnegative_integer(
        grant["max_cli_invocations"], label + ".max_cli_invocations"
    ) != 1:
        raise ValueError("authorization grant permits exactly one CLI invocation")
    if grant["max_provider_requests"] is not None:
        raise ValueError(
            "authorization grant provider request count must remain unknown/null"
        )
    if grant["max_billed_cost_usd"] is not None:
        raise ValueError(
            "authorization grant billed cost cap must remain unknown/null"
        )
    if grant["billed_cost_limit_source"] != "unknown-no-verifiable-cap":
        raise ValueError(
            "authorization grant must disclose that no billed-cost cap is verifiable"
        )
    if batch.get("budget", {}).get("max_cli_invocations") != 1:
        raise ValueError("authorization grant requires a one-invocation batch")
    if batch.get("budget", {}).get("max_provider_requests") is not None:
        raise ValueError(
            "authorization grant requires unknown/null batch provider requests"
        )
    if (
        batch.get("budget", {}).get("max_billed_cost_usd") is not None
        or batch.get("budget", {}).get("billed_cost_limit_source") != "unknown"
    ):
        raise ValueError(
            "authorization grant requires unknown/null batch billed-cost enforcement"
        )
    if grant["expires_at"] != authorization.get("expires_at"):
        raise ValueError("authorization grant expiry mismatch")
    expiry = _parse_timestamp(grant["expires_at"], label + ".expires_at")
    if require_unexpired and datetime.now(timezone.utc) >= expiry.astimezone(timezone.utc):
        raise ValueError("authorization grant has expired")
    return {
        "grant_id": grant_id,
        "nonce": nonce,
        "expires_at": grant["expires_at"],
        "actions": actions,
        "forbidden": forbidden,
    }


def _validate_file_reference(value: object, label: str) -> Dict[str, str]:
    reference = _mapping(value, label)
    fields = ("path", "digest")
    exact_fields(reference, fields, fields, label)
    return {
        "path": safe_relative_posix_path(reference["path"], label + ".path"),
        "digest": validate_digest(
            reference["digest"], label + ".digest", allow_zero=False
        ),
    }


def _validate_smoke_batch_binding(value: object) -> Dict:
    label = "batch_binding"
    binding = _mapping(value, label)
    fields = ("state", "batch_id", "batch_ref")
    exact_fields(binding, fields, fields, label)
    state = _enum(binding["state"], ("none", "receipt-bound"), label + ".state")
    batch_id = _nullable_nonblank(binding["batch_id"], label + ".batch_id")
    batch_ref = (
        None
        if binding["batch_ref"] is None
        else _validate_file_reference(binding["batch_ref"], label + ".batch_ref")
    )
    if state == "none":
        if batch_id is not None or batch_ref is not None:
            raise ValueError("batch_binding none requires null batch identity")
    elif batch_id is None or batch_ref is None:
        raise ValueError("batch_binding receipt-bound requires batch identity and ref")
    return {"state": state, "batch_id": batch_id, "batch_ref": batch_ref}


def _validate_lifecycle_binding(value: object) -> Dict:
    label = "lifecycle_binding"
    binding = _mapping(value, label)
    exact_fields(
        binding,
        LIFECYCLE_BINDING_FIELDS,
        LIFECYCLE_BINDING_FIELDS,
        label,
    )
    result = {}
    for field in LIFECYCLE_BINDING_FIELDS:
        if field in (
            "installation_ref",
            "authorization_ref",
            "authorization_consumption_ref",
        ) and binding[field] is None:
            result[field] = None
        else:
            result[field] = _validate_file_reference(
                binding[field], label + "." + field
            )
    return result


def _validate_smoke_summary(value: object) -> Dict:
    label = "summary"
    summary = _mapping(value, label)
    exact_fields(summary, SMOKE_SUMMARY_FIELDS, SMOKE_SUMMARY_FIELDS, label)
    if summary["schema_version"] != "1":
        raise ValueError("summary schema_version must be 1")
    nonblank(summary["task_id"], label + ".task_id")
    nonblank(
        summary["execution_configuration_id"],
        label + ".execution_configuration_id",
    )
    validate_digest(
        summary["execution_configuration_digest"],
        label + ".execution_configuration_digest",
        allow_zero=False,
    )
    validate_digest(
        summary["receipt_configuration_digest"],
        label + ".receipt_configuration_digest",
        allow_zero=False,
    )
    batch_binding = _validate_smoke_batch_binding(summary["batch_binding"])
    identity = _mapping(summary["execution_identity"], label + ".execution_identity")
    exact_fields(
        identity,
        EXECUTION_IDENTITY_FIELDS,
        EXECUTION_IDENTITY_FIELDS,
        label + ".execution_identity",
    )
    nonblank(identity["executor"], label + ".execution_identity.executor")
    _enum(identity["agent"], PLATFORMS, label + ".execution_identity.agent")
    nonblank(
        identity["client_version"], label + ".execution_identity.client_version"
    )
    _nullable_nonblank(
        identity["requested_model"], label + ".execution_identity.requested_model"
    )
    _nullable_nonblank(
        identity["resolved_model"], label + ".execution_identity.resolved_model"
    )
    _nullable_nonblank(
        identity["reasoning_effort"], label + ".execution_identity.reasoning_effort"
    )
    real_execution = _boolean(
        identity["real_agent_execution"],
        label + ".execution_identity.real_agent_execution",
    )
    authentication = _enum(
        identity["identity_authentication"],
        (
            "local-package-shape-and-digest-consistency",
            "invocation-declared-not-cryptographically-authenticated",
        ),
        label + ".execution_identity.identity_authentication",
    )
    installation_digest = _nullable_digest(
        identity["installation_identity_digest"],
        label + ".execution_identity.installation_identity_digest",
    )
    if real_execution:
        if (
            authentication != "local-package-shape-and-digest-consistency"
            or installation_digest is None
        ):
            raise ValueError(
                "real summary identity requires a locally verified installation digest"
            )
    elif (
        authentication != "invocation-declared-not-cryptographically-authenticated"
        or installation_digest is not None
    ):
        raise ValueError(
            "test-double summary identity cannot claim a verified installation"
        )
    outcome = _validate_outcome(
        {"status": summary["run_status"], "stop_reason": summary["failure"]},
        label + ".outcome",
    )
    oracle_outcome = _enum(
        summary["oracle_outcome"],
        ("pass", "fail", "not-run"),
        label + ".oracle_outcome",
    )
    if summary["quality_assessment"] is not False:
        raise ValueError("summary quality_assessment must remain false")
    if summary["quality_comparison"] != "not-applicable":
        raise ValueError("summary quality_comparison must remain not-applicable")
    if summary["inference"] != "not-computed":
        raise ValueError("summary inference must remain not-computed")
    measurement_states = _validate_measurements(summary["measurements"])
    if any(state != "unknown" for state in measurement_states.values()):
        raise ValueError("summary measurements must remain unknown")
    raw_sentinel = _boolean(
        summary["raw_output_sentinel_detected"],
        label + ".raw_output_sentinel_detected",
    )
    paths = {
        field: safe_relative_posix_path(summary[field], label + "." + field)
        for field in (
            "receipt_path",
            "observation_path",
            "raw_stdout_path",
            "raw_stderr_path",
        )
    }
    quarantine_created = _boolean(
        summary["quarantine_created"], label + ".quarantine_created"
    )
    if summary["mechanically_eligible"] is not False:
        raise ValueError("summary mechanically_eligible must remain false")
    unverified_scope = _unique_nonblank_strings(
        summary["unverified_scope"], label + ".unverified_scope"
    )
    if real_execution and not REQUIRED_REAL_UNVERIFIED_SCOPE.issubset(
        unverified_scope
    ):
        raise ValueError(
            "real summary must disclose unverified package publisher and provider/model identity"
        )
    return {
        "batch_binding": batch_binding,
        "identity": dict(identity),
        "outcome": outcome,
        "oracle_outcome": oracle_outcome,
        "raw_output_sentinel_detected": raw_sentinel,
        "quarantine_created": quarantine_created,
        "unverified_scope": unverified_scope,
        **paths,
    }


def _resolve_bound_path(
    evidence_root: Path, relative: str, label: str, *, directory: bool
) -> Path:
    if evidence_root.is_symlink() or not evidence_root.is_dir():
        raise ValueError("evidence-root must be a regular directory")
    root = evidence_root.resolve()
    path = resolve_relative_without_symlinks(root, relative, label)
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
    except FileNotFoundError as error:
        raise ValueError("{} evidence path is missing: {}".format(label, relative)) from error
    except ValueError as error:
        raise ValueError("{} escapes evidence-root".format(label)) from error
    if directory:
        if path.is_symlink() or not resolved.is_dir():
            raise ValueError("{} must reference a regular directory".format(label))
    elif path.is_symlink() or not resolved.is_file():
        raise ValueError("{} must reference a regular file".format(label))
    return resolved


def _open_bound_json(
    evidence_root: Path, reference: Mapping[str, str], label: str
) -> Mapping:
    relative = safe_relative_posix_path(reference["path"], label + ".path")
    path = _resolve_bound_path(evidence_root, relative, label, directory=False)
    actual_digest = sha256_file(path)
    if actual_digest != reference["digest"]:
        raise ValueError("{} digest mismatch".format(label))
    loaded = load_json(path)
    return _mapping(loaded, label + " document")


def _validate_outcome(value: object, label: str = "outcome") -> Dict[str, Optional[str]]:
    outcome = _mapping(value, label)
    fields = ("status", "stop_reason")
    exact_fields(outcome, fields, fields, label)
    status = _enum(
        outcome["status"], ("completed", "failed", "stopped"), label + ".status"
    )
    stop_reason = _nullable_nonblank(outcome["stop_reason"], label + ".stop_reason")
    if status == "completed" and stop_reason is not None:
        raise ValueError("{} completed status requires null stop_reason".format(label))
    if status != "completed" and stop_reason is None:
        raise ValueError("{} {} status requires stop_reason".format(label, status))
    return {"status": status, "stop_reason": stop_reason}


def _receipt_failure_reason(receipt: Mapping) -> str:
    agent = receipt["steps"]["agent"]
    oracle = receipt["steps"]["oracle"]
    if not agent["executed"]:
        return "agent_not_run"
    if agent["timed_out"]:
        return "agent_runner_timeout"
    if agent["exit_code"] == 124:
        return "agent_client_timeout"
    if agent["exit_code"] != agent["expected_exit_code"]:
        return "agent_failed"
    if not oracle["executed"]:
        return "oracle_not_run"
    if oracle["timed_out"]:
        return "oracle_timeout"
    if oracle["exit_code"] != oracle["expected_exit_code"]:
        return "oracle_failed"
    return "artifact_contract_failed"


def _derive_receipt_outcome(
    receipt: Mapping, artifact_root: Path, evidence_root: Path
) -> Dict[str, Optional[str]]:
    guard_path = artifact_root / "_runner" / "output-guard.json"
    if not guard_path.exists():
        raise ValueError("receipt-bound smoke requires output guard evidence")
    if guard_path.is_symlink() or not guard_path.is_file():
        raise ValueError("output guard evidence must be a regular file")
    guard = _mapping(load_json(guard_path), "output guard")
    required = (
        "schema_version",
        "guard_revision",
        "status",
        "failure",
        "sanitized_artifacts",
        "quarantine_scope",
    )
    exact_fields(guard, required, required, "output guard")
    if guard["schema_version"] != "1" or guard["guard_revision"] != "calibration-output-guard-v1":
        raise ValueError("unsupported output guard contract")
    status = _enum(guard["status"], ("pass", "failed"), "output guard.status")
    sanitized = _array(guard["sanitized_artifacts"], "output guard.sanitized_artifacts")
    seen_paths = set()
    for index, raw in enumerate(sanitized):
        label = "output guard.sanitized_artifacts[{}]".format(index)
        item = _mapping(raw, label)
        exact_fields(
            item,
            ("artifact_path", "quarantined_digest"),
            ("artifact_path", "quarantined_digest"),
            label,
        )
        artifact_path = safe_relative_posix_path(
            item["artifact_path"], label + ".artifact_path"
        )
        if artifact_path in seen_paths:
            raise ValueError("output guard sanitized artifact paths must be unique")
        seen_paths.add(artifact_path)
        validate_digest(
            item["quarantined_digest"], label + ".quarantined_digest", allow_zero=False
        )
    if status == "failed":
        if (
            guard["failure"] != "raw_output_sentinel_detected"
            or not sanitized
            or guard["quarantine_scope"]
            != "restricted-output-root-outside-receipt-artifact-tree"
        ):
            raise ValueError(
                "failed output guard requires sentinel failure and quarantined artifacts"
            )
        quarantine_root = evidence_root.resolve() / "quarantine"
        if quarantine_root.is_symlink() or not quarantine_root.is_dir():
            raise ValueError("failed output guard requires a regular quarantine root")
        if quarantine_root.stat().st_mode & 0o077:
            raise ValueError("quarantine root permissions must be owner-only")
        expected_paths = set(seen_paths)
        actual_paths = set()
        actual_directories = set()
        for path in quarantine_root.rglob("*"):
            if path.is_symlink():
                raise ValueError("quarantine tree must not contain symlinks")
            if path.is_file():
                if path.stat().st_mode & 0o077:
                    raise ValueError(
                        "quarantine artifact permissions must be owner-only"
                    )
                actual_paths.add(path.relative_to(quarantine_root).as_posix())
            elif path.is_dir():
                if path.stat().st_mode & 0o077:
                    raise ValueError(
                        "quarantine directory permissions must be owner-only"
                    )
                actual_directories.add(
                    path.relative_to(quarantine_root).as_posix()
                )
            else:
                raise ValueError("quarantine tree contains an unsupported entry")
        expected_directories = set()
        for relative in expected_paths:
            parent = Path(relative).parent
            while parent != Path("."):
                expected_directories.add(parent.as_posix())
                parent = parent.parent
        if (
            actual_paths != expected_paths
            or actual_directories != expected_directories
        ):
            raise ValueError(
                "quarantine file set and directory tree do not exactly match sanitized_artifacts"
            )
        for index, raw in enumerate(sanitized):
            relative = raw["artifact_path"]
            target = _resolve_bound_path(
                quarantine_root,
                relative,
                "output guard quarantine artifact {}".format(index),
                directory=False,
            )
            if sha256_file(target) != raw["quarantined_digest"]:
                raise ValueError("output guard quarantined artifact digest mismatch")
        return {
            "status": "failed",
            "stop_reason": "raw_output_sentinel_detected",
        }
    if (
        guard["failure"] is not None
        or sanitized
        or guard["quarantine_scope"] is not None
    ):
        raise ValueError("passing output guard must not claim failure or quarantine")

    if receipt["lifecycle_timed_out"]:
        return {
            "status": "failed" if receipt["steps"]["agent"]["executed"] else "stopped",
            "stop_reason": "lifecycle_wall_clock_exceeded",
        }

    agent = receipt["steps"]["agent"]
    if (
        agent["executed"]
        and not agent["timed_out"]
        and agent["exit_code"] == agent["expected_exit_code"]
        and receipt["oracle_outcome"] == "pass"
    ):
        return {"status": "completed", "stop_reason": None}
    return {
        "status": "stopped" if not agent["executed"] else "failed",
        "stop_reason": _receipt_failure_reason(receipt),
    }


def _validate_outcome_summary(value: object) -> Dict:
    summary = _mapping(value, "outcome_summary")
    fields = ("completed", "failed", "stopped", "stop_reasons")
    exact_fields(summary, fields, fields, "outcome_summary")
    counts = {
        name: nonnegative_integer(summary[name], "outcome_summary." + name)
        for name in ("completed", "failed", "stopped")
    }
    reasons = _array(summary["stop_reasons"], "outcome_summary.stop_reasons")
    reason_counts: Dict[str, int] = {}
    for index, raw in enumerate(reasons):
        label = "outcome_summary.stop_reasons[{}]".format(index)
        item = _mapping(raw, label)
        exact_fields(item, ("reason", "count"), ("reason", "count"), label)
        reason = nonblank(item["reason"], label + ".reason")
        if reason in reason_counts:
            raise ValueError("outcome_summary stop reasons must be unique")
        reason_counts[reason] = nonnegative_integer(
            item["count"], label + ".count", minimum=1
        )
    if sum(reason_counts.values()) != counts["failed"] + counts["stopped"]:
        raise ValueError(
            "outcome_summary stop reason counts must equal failed plus stopped runs"
        )
    return {**counts, "stop_reasons": reason_counts}


def _validate_batch_binding(value: object) -> Dict:
    binding = _mapping(value, "batch_binding")
    fields = (
        "state",
        "batch_id",
        "batch_path",
        "batch_digest",
        "planned_runs",
        "retained_runs",
        "observed_runs",
        "planned_task_shapes",
        "retained_task_shapes",
        "observed_task_shapes",
    )
    exact_fields(binding, fields, fields, "batch_binding")
    state = _enum(binding["state"], ("none", "receipt-bound"), "batch_binding.state")
    batch_id = _nullable_nonblank(binding["batch_id"], "batch_binding.batch_id")
    batch_path = _nullable_safe_path(binding["batch_path"], "batch_binding.batch_path")
    batch_digest = _nullable_digest(
        binding["batch_digest"], "batch_binding.batch_digest"
    )
    counts = {
        name: nonnegative_integer(binding[name], "batch_binding." + name)
        for name in ("planned_runs", "retained_runs", "observed_runs")
    }
    shapes = {
        name: _unique_nonblank_strings(binding[name], "batch_binding." + name)
        for name in (
            "planned_task_shapes",
            "retained_task_shapes",
            "observed_task_shapes",
        )
    }
    if state == "none":
        if any(item is not None for item in (batch_id, batch_path, batch_digest)):
            raise ValueError("batch_binding none requires null batch identity")
        if any(counts.values()) or any(shapes.values()):
            raise ValueError("batch_binding none requires zero coverage")
    else:
        if batch_id is None or batch_path is None or batch_digest is None:
            raise ValueError("batch_binding receipt-bound requires batch identity and digest")
        if not (counts["planned_runs"] == counts["retained_runs"] == counts["observed_runs"]):
            raise ValueError("batch coverage requires planned=retained=observed runs")
        if not (
            shapes["planned_task_shapes"]
            == shapes["retained_task_shapes"]
            == shapes["observed_task_shapes"]
        ):
            raise ValueError("batch coverage requires planned=retained=observed task shapes")
    return {
        "state": state,
        "batch_id": batch_id,
        "batch_path": batch_path,
        "batch_digest": batch_digest,
        **counts,
        **shapes,
    }


def validate_smoke_observation(
    value: object, *, evidence_root: Optional[Path] = None
) -> Dict:
    observation = _mapping(value, "smoke_observation")
    exact_fields(
        observation,
        SMOKE_OBSERVATION_FIELDS,
        SMOKE_OBSERVATION_FIELDS,
        "smoke_observation",
    )
    if observation["schema_version"] != "2":
        raise ValueError("smoke observation schema_version must be 2")
    if observation["observation_revision"] != "smoke-observation-v2":
        raise ValueError("observation_revision must be smoke-observation-v2")
    observation_id = nonblank(observation["observation_id"], "observation_id")
    if observation["observation_kind"] != "connectivity-smoke":
        raise ValueError("observation_kind must be connectivity-smoke")
    if observation["scope"] != "connectivity-only":
        raise ValueError("smoke observation scope must be connectivity-only")
    task_id = nonblank(observation["task_id"], "task_id")
    task_shape = nonblank(observation["task_shape"], "task_shape")
    task_match = re.fullmatch(r"\d{2}-(.+)", task_id)
    if task_match is None or task_shape != task_match.group(1):
        raise ValueError("task_shape must be derived from the bound task_id")
    configuration_value = _mapping(
        observation["execution_configuration"], "execution_configuration"
    )
    configuration = _validate_execution_configuration(
        configuration_value, "execution_configuration"
    )
    if configuration["binding_state"] != "receipt-bound":
        raise ValueError("smoke observation requires receipt-bound execution configuration")
    if configuration["platform"] == "codex":
        if configuration_value["harness"] != CODEX_REAL_HARNESS:
            raise ValueError(
                "receipt-bound Codex evidence requires the canonical EVAL-10 harness"
            )
    execution_configuration_digest = validate_digest(
        observation["execution_configuration_digest"],
        "execution_configuration_digest",
        allow_zero=False,
    )
    if execution_configuration_digest != _canonical_digest(configuration_value):
        raise ValueError("execution configuration digest mismatch")
    receipt_configuration_digest = validate_digest(
        observation["receipt_configuration_digest"],
        "receipt_configuration_digest",
        allow_zero=False,
    )
    outcome = _validate_outcome(observation["outcome"])
    oracle_outcome = _enum(
        observation["oracle_outcome"],
        ("pass", "fail", "not-run"),
        "oracle_outcome",
    )
    if outcome["status"] == "completed" and oracle_outcome != "pass":
        raise ValueError("completed smoke observation requires oracle_outcome pass")
    batch_binding = _validate_smoke_batch_binding(observation["batch_binding"])
    lifecycle_binding = _validate_lifecycle_binding(observation["lifecycle_binding"])
    summary_ref = _validate_file_reference(observation["summary_ref"], "summary_ref")
    receipt_ref = _validate_file_reference(observation["receipt_ref"], "receipt_ref")
    observation_measurement_states = _validate_measurements(
        observation["measurements"]
    )
    if any(state != "unknown" for state in observation_measurement_states.values()):
        raise ValueError(
            "smoke-observation-v2 measurements must remain unknown until "
            "digest-bound measurement evidence is implemented"
        )
    _unique_nonblank_strings(observation["unverified_scope"], "unverified_scope")

    if batch_binding["state"] != "receipt-bound":
        raise ValueError(
            "smoke-observation-v2 requires a receipt-bound authorization batch"
        )
    if evidence_root is None:
        raise ValueError("smoke-observation-v2 requires --evidence-root")

    if evidence_root is not None:
        summary = _open_bound_json(evidence_root, summary_ref, "summary_ref")
        summary_validation = _validate_smoke_summary(summary)
        receipt = _open_bound_json(evidence_root, receipt_ref, "receipt_ref")
        validate_receipt(receipt)
        receipt_path = _resolve_bound_path(
            evidence_root, receipt_ref["path"], "receipt_ref", directory=False
        )

        manifest_ref = lifecycle_binding["manifest_ref"]
        manifest = _open_bound_json(
            evidence_root, manifest_ref, "lifecycle_binding.manifest_ref"
        )
        manifest_path = _resolve_bound_path(
            evidence_root,
            manifest_ref["path"],
            "lifecycle_binding.manifest_ref",
            directory=False,
        )
        validate_manifest_structure(manifest)
        fixture = find_fixture(manifest, task_id, receipt["fixture_id"])

        fixture_reference = lifecycle_binding["fixture_root"]
        fixture_root = _resolve_bound_path(
            evidence_root,
            fixture_reference["path"],
            "lifecycle_binding.fixture_root",
            directory=True,
        )
        actual_fixture_digest = tree_digest_v2(fixture_root)
        if (
            actual_fixture_digest != fixture_reference["digest"]
            or actual_fixture_digest != fixture["initial_state_digest"]
            or actual_fixture_digest != receipt["fixture_initial_digest"]
        ):
            raise ValueError("lifecycle fixture root digest mismatch")
        manifest_fixture_root = resolve_relative_without_symlinks(
            manifest_path.parent,
            safe_relative_posix_path(
                fixture["root"], "manifest fixture root"
            ),
            "manifest fixture root",
        ).resolve()
        if manifest_fixture_root != fixture_root:
            raise ValueError(
                "lifecycle fixture root does not match the staged manifest"
            )

        prompt_reference = lifecycle_binding["prompt_ref"]
        prompt_path = _resolve_bound_path(
            evidence_root,
            prompt_reference["path"],
            "lifecycle_binding.prompt_ref",
            directory=False,
        )
        if sha256_file(prompt_path) != prompt_reference["digest"]:
            raise ValueError("lifecycle prompt digest mismatch")

        adapter_reference = lifecycle_binding["adapter_ref"]
        adapter_path = _resolve_bound_path(
            evidence_root,
            adapter_reference["path"],
            "lifecycle_binding.adapter_ref",
            directory=False,
        )
        if sha256_file(adapter_path) != adapter_reference["digest"]:
            raise ValueError("lifecycle adapter digest mismatch")

        configuration_reference = lifecycle_binding["configuration_root"]
        configuration_root = _resolve_bound_path(
            evidence_root,
            configuration_reference["path"],
            "lifecycle_binding.configuration_root",
            directory=True,
        )
        actual_configuration_digest = tree_digest_v2(configuration_root)
        if actual_configuration_digest != configuration_reference["digest"]:
            raise ValueError("lifecycle configuration root digest mismatch")
        if (
            actual_configuration_digest != receipt_configuration_digest
            or receipt["configuration_digest"] != receipt_configuration_digest
        ):
            raise ValueError("lifecycle configuration is not bound to the receipt")

        control_ref = lifecycle_binding["control_ref"]
        control = _open_bound_json(
            evidence_root, control_ref, "lifecycle_binding.control_ref"
        )
        if configuration["platform"] == "codex":
            _validate_codex_control(control)
        control_path = _resolve_bound_path(
            evidence_root,
            control_ref["path"],
            "lifecycle_binding.control_ref",
            directory=False,
        )
        if control_path != (configuration_root / "control.json").resolve():
            raise ValueError(
                "lifecycle control_ref must exactly reference configuration_root/control.json"
            )

        artifact_reference = lifecycle_binding["artifact_root"]
        artifact_root = _resolve_bound_path(
            evidence_root,
            artifact_reference["path"],
            "lifecycle_binding.artifact_root",
            directory=True,
        )
        expected_artifact_root = (receipt_path.parent / receipt["artifact_root"]).resolve()
        if artifact_root != expected_artifact_root:
            raise ValueError("lifecycle artifact root is not the receipt run artifact root")
        actual_artifact_digest = artifact_tree_digest_v2(artifact_root)
        if (
            actual_artifact_digest != artifact_reference["digest"]
            or actual_artifact_digest != receipt["artifact_inventory_digest"]
        ):
            raise ValueError("lifecycle artifact root digest mismatch")
        verify_receipt_binding(
            receipt, manifest_path, manifest, fixture, artifact_root
        )
        receipt_outcome = _derive_receipt_outcome(
            receipt, artifact_root, evidence_root
        )
        execution_identity = summary_validation["identity"]
        if execution_identity["real_agent_execution"] is not True:
            raise ValueError(
                "receipt-bound smoke evidence requires real_agent_execution=true"
            )
        expected_identity = {
            "executor": CODEX_REAL_CLIENT,
            "agent": configuration["platform"],
            "client_version": configuration_value["client_version"],
            "requested_model": configuration_value["requested_model"],
            "resolved_model": configuration_value["resolved_model"],
            "reasoning_effort": configuration_value["reasoning"],
            "identity_authentication": "local-package-shape-and-digest-consistency",
        }
        for field, expected in expected_identity.items():
            if execution_identity[field] != expected:
                raise ValueError(
                    "summary execution identity mismatch at {}".format(field)
                )
        if batch_binding["state"] != "receipt-bound":
            raise ValueError(
                "real receipt-bound smoke evidence requires a receipt-bound batch"
            )
        summary_batch_binding = summary_validation["batch_binding"]
        if summary_batch_binding != batch_binding:
            raise ValueError("summary and observation batch binding mismatch")
        if summary["receipt_path"] != receipt_ref["path"]:
            raise ValueError("summary receipt_path does not match observation receipt_ref")
        if summary["measurements"] != observation["measurements"]:
            raise ValueError("summary and observation measurements mismatch")
        if summary["unverified_scope"] != observation["unverified_scope"]:
            raise ValueError("summary and observation unverified_scope mismatch")
        if summary["task_id"] != task_id or receipt["task_id"] != task_id:
            raise ValueError("task binding mismatch across summary, receipt and observation")
        if (
            summary["execution_configuration_id"]
            != configuration["configuration_id"]
            or summary["execution_configuration_digest"]
            != execution_configuration_digest
            or summary["receipt_configuration_digest"]
            != receipt_configuration_digest
            or receipt["configuration_digest"] != receipt_configuration_digest
        ):
            raise ValueError(
                "configuration binding mismatch across summary, receipt and observation"
            )
        if (
            summary["run_status"] != outcome["status"]
            or summary["failure"] != outcome["stop_reason"]
            or summary["oracle_outcome"] != oracle_outcome
            or receipt["oracle_outcome"] != oracle_outcome
        ):
            raise ValueError("outcome binding mismatch across summary, receipt and observation")
        if outcome != receipt_outcome:
            raise ValueError(
                "observation outcome does not match lifecycle receipt execution"
            )

        snapshot = receipt["control_snapshot"]
        expected_snapshot = {
            "agent": configuration["platform"],
            "agent_version": "codex-cli-{}".format(
                configuration_value["client_version"]
            ),
            "model": configuration_value["requested_model"],
            "reasoning_effort": configuration_value["reasoning"] or "not-applicable",
            "profile": configuration_value["profile"],
            "permissions_digest": configuration_value["permissions_digest"],
            "toolset_digest": configuration_value["toolset_digest"],
        }
        for field, expected in expected_snapshot.items():
            if snapshot[field] != expected:
                raise ValueError(
                    "receipt control_snapshot does not match execution configuration at {}".format(
                        field
                    )
                )

        batch_ref = batch_binding["batch_ref"]
        if batch_ref is None:
            raise ValueError("receipt-bound batch reference is missing")
        batch_document = _open_bound_json(
            evidence_root, batch_ref, "batch_binding.batch_ref"
        )
        batch_result = validate_batch(batch_document)
        if batch_result["terminal_state"] is not None or not batch_result["executed"]:
            raise ValueError("smoke observation requires an executed nonterminal batch")
        if batch_document["batch_id"] != batch_binding["batch_id"]:
            raise ValueError("smoke observation batch id mismatch")
        if batch_document["execution_mode"] not in (
            "authorized-smoke",
            "authorized-calibration-batch",
        ):
            raise ValueError("smoke observation batch execution_mode is not authorized")
        if (
            receipt["lifecycle_timeout_seconds"]
            != batch_document["budget"]["max_wall_clock_seconds"]
        ):
            raise ValueError(
                "receipt lifecycle timeout does not match batch wall-clock budget"
            )
        if (
            receipt["lifecycle_duration_seconds"]
            > batch_document["budget"]["max_wall_clock_seconds"]
        ):
            raise ValueError("receipt exceeds batch wall-clock budget")

        batch_fixture = batch_document["fixture_binding"]
        if prompt_reference["digest"] != batch_fixture["prompt_digest"]:
            raise ValueError("retained prompt does not match batch prompt digest")
        if batch_fixture["manifest_path"] != manifest_ref["path"]:
            raise ValueError(
                "batch fixture manifest_path does not match retained manifest_ref"
            )
        expected_oracle_revision = _retained_oracle_revision(
            fixture, fixture_root
        )
        if batch_fixture["oracle_revision"] != expected_oracle_revision:
            raise ValueError(
                "batch fixture oracle_revision does not bind the retained oracle"
            )
        expected_fixture_binding = {
            "manifest_digest": receipt["manifest_digest"],
            "task_id": receipt["task_id"],
            "task_revision": receipt["task_revision"],
            "fixture_id": receipt["fixture_id"],
            "fixture_revision": receipt["fixture_revision"],
            "initial_state_digest": receipt["fixture_initial_digest"],
        }
        for field, expected in expected_fixture_binding.items():
            if batch_fixture[field] != expected:
                raise ValueError(
                    "batch fixture binding does not match receipt at {}".format(field)
                )

        matching_configurations = [
            item
            for item in batch_document["execution_configurations"]
            if item["configuration_id"] == configuration["configuration_id"]
        ]
        if len(matching_configurations) != 1:
            raise ValueError(
                "observation batch must contain exactly one matching configuration"
            )
        expected_configuration = dict(configuration_value)
        expected_configuration["binding_state"] = "control-bound"
        if matching_configurations[0] != expected_configuration:
            raise ValueError(
                "observation batch and execution configuration mismatch"
            )

        control_required = (
            "execution_kind",
            "client",
            "expected_client_version",
            "requested_model",
            "resolved_model",
            "reasoning_effort",
            "profile",
            "permissions_digest",
            "toolset_digest",
            "prompt_digest",
            "batch_id",
            "batch_plan_digest",
            "adapter_digest",
            "prompt_ref",
            "adapter_ref",
            "installation_identity_digest",
            "authorization_ref_digest",
        )
        missing_control = [field for field in control_required if field not in control]
        if missing_control:
            raise ValueError(
                "control file missing binding fields: {}".format(
                    ", ".join(missing_control)
                )
            )
        expected_control = {
            "execution_kind": "real",
            "expected_client_version": configuration_value["client_version"],
            "requested_model": configuration_value["requested_model"],
            "resolved_model": configuration_value["resolved_model"],
            "reasoning_effort": configuration_value["reasoning"],
            "profile": configuration_value["profile"],
            "permissions_digest": configuration_value["permissions_digest"],
            "toolset_digest": configuration_value["toolset_digest"],
            "prompt_digest": batch_fixture["prompt_digest"],
            "batch_id": batch_binding["batch_id"],
            "batch_plan_digest": batch_ref["digest"],
            "prompt_ref": prompt_reference,
            "adapter_ref": adapter_reference,
        }
        for field, expected in expected_control.items():
            if control[field] != expected:
                raise ValueError(
                    "control file does not match bound evidence at {}".format(field)
                )
        adapter_digest = validate_digest(
            control["adapter_digest"], "control.adapter_digest", allow_zero=False
        )
        if adapter_digest != adapter_reference["digest"]:
            raise ValueError("control adapter digest does not match retained adapter")
        if not configuration_value["adapter_revision"].endswith("@" + adapter_digest):
            raise ValueError(
                "control adapter digest does not match execution configuration"
            )
        canonical_adapter = EVALS_DIR / "calibration_adapters" / "codex_eval10.py"
        if canonical_adapter.is_symlink() or not canonical_adapter.is_file():
            raise ValueError("canonical Codex EVAL-10 adapter is unavailable")
        if adapter_digest != sha256_file(canonical_adapter):
            raise ValueError(
                "retained adapter does not match the canonical Codex EVAL-10 adapter"
            )
        expected_adapter_revision = "codex-eval10-v2@{}".format(
            adapter_digest
        )
        if configuration_value["adapter_revision"] != expected_adapter_revision:
            raise ValueError("Codex adapter revision is not canonical")

        installation_reference = lifecycle_binding["installation_ref"]
        if installation_reference is None:
            raise ValueError(
                "real receipt-bound smoke requires installation identity evidence"
            )
        installation_identity = validate_installation_identity(
            _open_bound_json(
                evidence_root,
                installation_reference,
                "lifecycle_binding.installation_ref",
            )
        )
        if installation_identity["platform"] != "darwin":
            raise ValueError(
                "real Codex smoke evidence requires a darwin installation identity"
            )
        installation_digest = installation_identity["identity_digest"]
        retained_installation = _validate_retained_codex_installation(
            evidence_root,
            installation_reference,
            installation_identity,
        )
        if (
            control["installation_identity_digest"] != installation_digest
            or execution_identity["installation_identity_digest"]
            != installation_digest
        ):
            raise ValueError("installation identity binding mismatch")
        if configuration_value["client_version"] != installation_identity[
            "package_version"
        ]:
            raise ValueError(
                "execution client_version does not match retained Codex package version"
            )

        authorization_reference = lifecycle_binding["authorization_ref"]
        if authorization_reference is None:
            raise ValueError(
                "real receipt-bound smoke requires retained authorization grant"
            )
        authorization_path = _resolve_bound_path(
            evidence_root,
            authorization_reference["path"],
            "lifecycle_binding.authorization_ref",
            directory=False,
        )
        if sha256_file(authorization_path) != authorization_reference["digest"]:
            raise ValueError("authorization grant digest mismatch")
        grant = load_json(authorization_path)
        grant_result = validate_authorization_grant(
            grant,
            batch=batch_document,
            batch_digest=batch_ref["digest"],
            installation_identity_digest=installation_digest,
        )
        if control["authorization_ref_digest"] != authorization_reference["digest"]:
            raise ValueError("control authorization grant digest mismatch")

        consumption_reference = lifecycle_binding["authorization_consumption_ref"]
        if consumption_reference is None:
            raise ValueError(
                "real receipt-bound smoke requires authorization consumption evidence"
            )
        consumption = _open_bound_json(
            evidence_root,
            consumption_reference,
            "lifecycle_binding.authorization_consumption_ref",
        )
        consumption_fields = (
            "schema_version",
            "grant_id",
            "grant_digest",
            "batch_digest",
            "installation_identity_digest",
            "consumed_at",
            "evidence_root",
            "state",
        )
        exact_fields(
            consumption,
            consumption_fields,
            consumption_fields,
            "authorization consumption",
        )
        if consumption["schema_version"] != "1":
            raise ValueError("authorization consumption schema_version must be 1")
        if consumption["grant_id"] != grant_result["grant_id"]:
            raise ValueError("authorization consumption grant_id mismatch")
        if consumption["grant_digest"] != authorization_reference["digest"]:
            raise ValueError("authorization consumption grant digest mismatch")
        if consumption["batch_digest"] != batch_ref["digest"]:
            raise ValueError("authorization consumption batch digest mismatch")
        if consumption["installation_identity_digest"] != installation_digest:
            raise ValueError(
                "authorization consumption installation identity mismatch"
            )
        consumed_at = _parse_timestamp(
            consumption["consumed_at"], "authorization consumption.consumed_at"
        )
        grant_expires_at = _parse_timestamp(
            grant_result["expires_at"], "authorization grant.expires_at"
        )
        if consumed_at > grant_expires_at:
            raise ValueError(
                "authorization consumption occurred after grant expiry"
            )
        if consumed_at > datetime.now(timezone.utc) + timedelta(minutes=5):
            raise ValueError(
                "authorization consumption timestamp is implausibly in the future"
            )
        if consumption["evidence_root"] != str(evidence_root.resolve()):
            raise ValueError("authorization consumption evidence_root mismatch")
        if consumption["state"] != "consumed-before-invocation":
            raise ValueError(
                "authorization consumption must be recorded before invocation"
            )

        agent_argv = receipt["agent_argv"]
        expected_flags = (
            "--codex-executable",
            "--expected-client-version",
            "--auth-file",
            "--prompt-file",
            "--expected-prompt-digest",
            "--model",
            "--reasoning-effort",
            "--client-timeout-seconds",
            "--installation-identity-file",
            "--expected-installation-identity-digest",
            "--installation-entrypoint",
            "--authorization-grant-file",
            "--expected-authorization-grant-digest",
            "--authorization-expires-at",
            "--session-root",
        )
        if (
            len(agent_argv) != 3 + len(expected_flags) * 2
            or Path(agent_argv[0]).resolve() != Path(sys.executable).resolve()
            or agent_argv[1] != "-B"
            or Path(agent_argv[2]).resolve() != adapter_path
            or tuple(agent_argv[3::2]) != expected_flags
        ):
            raise ValueError("receipt agent argv does not match the canonical Codex adapter template")
        argv_values = dict(zip(expected_flags, agent_argv[4::2]))
        try:
            client_timeout = int(argv_values["--client-timeout-seconds"])
        except ValueError as error:
            raise ValueError("Codex adapter client timeout must be an integer") from error
        if client_timeout < 1 or client_timeout > 1800:
            raise ValueError("Codex adapter client timeout is out of bounds")
        auth_path = Path(argv_values["--auth-file"])
        if not auth_path.is_absolute():
            raise ValueError("Codex adapter auth path must be absolute")
        try:
            auth_path.resolve().relative_to(evidence_root.resolve())
        except ValueError:
            pass
        else:
            raise ValueError("Codex adapter auth source must not be retained as evidence")
        session_root = Path(argv_values["--session-root"])
        if not session_root.is_absolute():
            raise ValueError("Codex adapter session root must be absolute")
        try:
            session_root.resolve().relative_to(evidence_root.resolve())
        except ValueError:
            pass
        else:
            raise ValueError("Codex adapter session root must remain outside evidence")
        if session_root.exists() or session_root.is_symlink():
            raise ValueError(
                "Codex adapter session root must be removed before evidence validation"
            )
        expected_argv_values = {
            "--expected-client-version": installation_identity["package_version"],
            "--expected-prompt-digest": prompt_reference["digest"],
            "--model": configuration_value["requested_model"],
            "--reasoning-effort": configuration_value["reasoning"],
            "--expected-installation-identity-digest": installation_digest,
            "--expected-authorization-grant-digest": authorization_reference[
                "digest"
            ],
            "--authorization-expires-at": grant["expires_at"],
        }
        for flag, expected in expected_argv_values.items():
            if argv_values[flag] != expected:
                raise ValueError(
                    "Codex adapter argv binding mismatch at {}".format(flag)
                )
        expected_path_values = {
            "--codex-executable": retained_installation["native_binary"],
            "--prompt-file": prompt_path,
            "--installation-identity-file": _resolve_bound_path(
                evidence_root,
                installation_reference["path"],
                "lifecycle_binding.installation_ref",
                directory=False,
            ),
            "--installation-entrypoint": retained_installation["entrypoint"],
            "--authorization-grant-file": authorization_path,
        }
        for flag, expected_path in expected_path_values.items():
            try:
                actual_path = Path(argv_values[flag]).resolve(strict=True)
            except (FileNotFoundError, OSError) as error:
                raise ValueError(
                    "Codex adapter argv path is unavailable at {}".format(flag)
                ) from error
            if actual_path != expected_path.resolve():
                raise ValueError(
                    "Codex adapter argv binding mismatch at {}".format(flag)
                )

        provider_sidecar_path = artifact_root / "_runner" / "provider-invocation.json"
        provider_sidecar = _open_regular_json(
            provider_sidecar_path, "provider invocation sidecar"
        )
        _validate_provider_invocation_sidecar(
            provider_sidecar,
            configuration=configuration_value,
            runtime_executable_digest=installation_identity[
                "native_binary_digest"
            ],
            installation_identity_digest=installation_digest,
            authorization_grant_digest=authorization_reference["digest"],
            prompt_digest=prompt_reference["digest"],
            outcome=outcome,
            consumed_at=consumed_at,
            grant_expires_at=grant_expires_at,
            wrapper_step=receipt["steps"]["agent"],
        )

        expected_raw_paths = {
            "raw_stdout_path": artifact_root / "_runner" / "agent.stdout",
            "raw_stderr_path": artifact_root / "_runner" / "agent.stderr",
        }
        for field, expected_path in expected_raw_paths.items():
            actual_path = _resolve_bound_path(
                evidence_root,
                summary_validation[field],
                "summary." + field,
                directory=False,
            )
            if actual_path != expected_path.resolve():
                raise ValueError("summary {} is not the receipt raw artifact".format(field))
        sentinel_path = fixture_root / "workspace" / "secret-sentinel.txt"
        if sentinel_path.is_symlink() or not sentinel_path.is_file():
            raise ValueError("bound fixture is missing the synthetic sentinel")
        sentinel = sentinel_path.read_text(encoding="utf-8").strip()
        if not sentinel:
            raise ValueError("synthetic sentinel must be non-empty")
        scan_paths = tuple(expected_raw_paths.values()) + (
            artifact_root / "decision-log.md",
        )
        for scan_path in scan_paths:
            if scan_path.is_symlink() or not scan_path.is_file():
                raise ValueError("receipt-bound smoke is missing guarded raw output")
            if sentinel in scan_path.read_text(encoding="utf-8", errors="replace"):
                raise ValueError(
                    "raw output sentinel detected independently of output guard"
                )
        guard_failed = receipt_outcome.get("stop_reason") == "raw_output_sentinel_detected"
        if summary_validation["raw_output_sentinel_detected"] != guard_failed:
            raise ValueError("summary output guard status mismatch")
        quarantine_root = evidence_root.resolve() / "quarantine"
        if guard_failed:
            if not summary_validation["quarantine_created"] or not quarantine_root.is_dir():
                raise ValueError("failed output guard requires bound quarantine evidence")
        elif summary_validation["quarantine_created"] or quarantine_root.exists():
            raise ValueError(
                "passing output guard forbids any quarantine claim or quarantine tree"
            )

    return {
        "valid": True,
        "document": "smoke-observation",
        "observation_id": observation_id,
        "task_id": task_id,
        "task_shape": task_shape,
        "configuration_id": configuration["configuration_id"],
        "execution_configuration": dict(configuration_value),
        "batch_binding": batch_binding,
        "measurements": observation["measurements"],
        "outcome": outcome,
        "oracle_outcome": oracle_outcome,
        "summary_observation_path": (
            summary_validation["observation_path"]
            if evidence_root is not None
            else None
        ),
    }


def _validate_evidence(value: object) -> List[Dict]:
    evidence = _array(value, "evidence")
    fields = ("type", "observation_id", "path", "digest")
    result = []
    paths = set()
    observation_ids = set()
    for index, raw in enumerate(evidence):
        label = "evidence[{}]".format(index)
        item = _mapping(raw, label)
        exact_fields(item, fields, fields, label)
        if item["type"] != "smoke-observation":
            raise ValueError("{}.type must be smoke-observation".format(label))
        observation_id = nonblank(item["observation_id"], label + ".observation_id")
        path = safe_relative_posix_path(item["path"], label + ".path")
        digest = validate_digest(item["digest"], label + ".digest", allow_zero=False)
        if path in paths:
            raise ValueError("evidence paths must be unique")
        if observation_id in observation_ids:
            raise ValueError("evidence observation ids must be unique")
        paths.add(path)
        observation_ids.add(observation_id)
        result.append(
            {
                "type": "smoke-observation",
                "observation_id": observation_id,
                "path": path,
                "digest": digest,
            }
        )
    return result


def _validate_decision(value: object) -> None:
    decision = _mapping(value, "decision")
    fields = ("routing", "winner", "ranking", "promotion_recommendation")
    exact_fields(decision, fields, fields, "decision")
    if decision["routing"] != "undecided":
        raise ValueError("decision.routing must remain undecided")
    for field in ("winner", "ranking", "promotion_recommendation"):
        if decision[field] is not None:
            raise ValueError("decision.{} must remain null".format(field))


def validate_capability_card(
    value: object, *, evidence_root: Optional[Path] = None
) -> Dict:
    card = _mapping(value, "capability_card")
    exact_fields(card, CARD_FIELDS, CARD_FIELDS, "capability_card")
    if card["schema_version"] != "1":
        raise ValueError("schema_version must be 1")
    card_id = nonblank(card["card_id"], "card_id")
    nonblank(card["card_revision"], "card_revision")
    platform = _enum(card["platform"], PLATFORMS, "platform")
    configuration = _validate_execution_configuration(
        card["execution_configuration"],
        "execution_configuration",
        controlled_blocker=True,
    )
    if configuration["platform"] != platform:
        raise ValueError("capability card platform must match execution configuration")
    evidence_state = _enum(
        card["evidence_state"],
        ("unobserved", "smoke-only", "provisionally-calibrated", "expired"),
        "evidence_state",
    )
    evidence_basis = _enum(
        card["evidence_basis"],
        ("none", "single-smoke", "preregistered-calibration-batch", "expired-tombstone"),
        "evidence_basis",
    )
    state_reason = _enum(
        card["state_reason"],
        tuple(sorted(CAPABILITY_STATE_REASON_CODES)),
        "state_reason",
    )
    observed_runs = nonnegative_integer(card["observed_runs"], "observed_runs")
    task_shapes = _unique_nonblank_strings(card["task_shapes"], "task_shapes")
    outcome_summary = (
        None
        if card["outcome_summary"] is None
        else _validate_outcome_summary(card["outcome_summary"])
    )
    batch_binding = _validate_batch_binding(card["batch_binding"])
    measurement_states = _validate_measurements(card["measurements"])
    evidence = _validate_evidence(card["evidence"])
    blockers = _unique_nonblank_strings(card["blockers"], "blockers")
    unknown_blockers = sorted(set(blockers) - CAPABILITY_BLOCKER_CODES)
    if unknown_blockers:
        raise ValueError(
            "blockers contain unsupported reason codes: {}".format(
                ", ".join(unknown_blockers)
            )
        )
    valid_until = _nullable_nonblank(card["valid_until"], "valid_until")
    if valid_until is not None and re.fullmatch(r"\d{4}-\d{2}-\d{2}", valid_until) is None:
        raise ValueError("valid_until must be null or YYYY-MM-DD")
    expired_reason = _nullable_nonblank(card["expired_reason"], "expired_reason")
    if expired_reason is not None and expired_reason not in EXPIRED_REASON_CODES:
        raise ValueError("expired_reason must be an allowed reason code")
    _validate_decision(card["decision"])

    expected_basis = {
        "unobserved": "none",
        "smoke-only": "single-smoke",
        "provisionally-calibrated": "preregistered-calibration-batch",
        "expired": "expired-tombstone",
    }[evidence_state]
    if evidence_basis != expected_basis:
        raise ValueError(
            "{} evidence state requires evidence_basis {}; {} is not sufficient".format(
                evidence_state, expected_basis, evidence_basis
            )
        )
    expected_state_reason = _derived_state_reason(evidence_state, outcome_summary)
    if state_reason != expected_state_reason:
        raise ValueError(
            "state_reason must be derived from evidence_state and outcome_summary: {}".format(
                expected_state_reason
            )
        )
    if evidence_state == "unobserved":
        if observed_runs != 0 or task_shapes or evidence:
            raise ValueError("unobserved card cannot contain observed runs, task shapes or run evidence")
        if any(state != "unknown" for state in measurement_states.values()):
            raise ValueError("unobserved card measurements must remain unknown")
        if expired_reason is not None:
            raise ValueError("unobserved card cannot declare expired_reason")
        if outcome_summary is not None:
            raise ValueError("unobserved card cannot declare an outcome")
        if batch_binding["state"] != "none":
            raise ValueError("unobserved card requires batch_binding state none")
    elif evidence_state in ("smoke-only", "provisionally-calibrated"):
        if configuration["binding_state"] != "receipt-bound":
            raise ValueError("{} card requires receipt-bound execution configuration".format(evidence_state))
        if observed_runs < 1 or not task_shapes or not evidence:
            raise ValueError("{} card requires observed runs, task shapes and evidence".format(evidence_state))
        if valid_until is None:
            raise ValueError("{} card requires valid_until".format(evidence_state))
        if date.fromisoformat(valid_until) < datetime.now(timezone.utc).date():
            raise ValueError(
                "active capability card valid_until must not be before the current UTC date"
            )
        if expired_reason is not None:
            raise ValueError("active capability card cannot declare expired_reason")
        if outcome_summary is None:
            raise ValueError("observed capability card requires outcome_summary")
        if sum(outcome_summary[name] for name in ("completed", "failed", "stopped")) != observed_runs:
            raise ValueError("outcome_summary counts must equal observed_runs")
        if batch_binding["state"] != "receipt-bound":
            raise ValueError("observed capability card requires receipt-bound batch_binding")
        if batch_binding["observed_runs"] != observed_runs:
            raise ValueError("batch_binding observed_runs must match card observed_runs")
        if set(batch_binding["observed_task_shapes"]) != set(task_shapes):
            raise ValueError("batch_binding task shapes must match card task_shapes")
        if len(evidence) != observed_runs:
            raise ValueError("one retained smoke observation is required per observed run")
        if any(state != "unknown" for state in measurement_states.values()):
            raise ValueError(
                "observed capability card measurements must remain unknown until "
                "digest-bound measurement evidence is implemented"
            )
        if evidence_state == "smoke-only":
            if observed_runs != 1 or len(task_shapes) != 1:
                raise ValueError("smoke-only requires exactly one run and one task shape")
        else:
            raise ValueError(
                "provisionally-calibrated is fail-closed until the batch schema "
                "preregisters every planned run and task-shape cell"
            )
        if evidence_root is None:
            raise ValueError("observed capability card requires --evidence-root")
    else:
        if expired_reason is None:
            raise ValueError("expired card requires expired_reason")
        if valid_until is None:
            raise ValueError("expired card requires valid_until")
        expiry_date = date.fromisoformat(valid_until)
        if expiry_date >= datetime.now(timezone.utc).date():
            raise ValueError("expired card valid_until must be before today (UTC)")
        if observed_runs != 0 or task_shapes or evidence:
            raise ValueError(
                "expired tombstone cannot retain observed runs, task shapes or evidence"
            )
        if outcome_summary is not None:
            raise ValueError("expired tombstone cannot retain an outcome summary")
        if batch_binding["state"] != "none":
            raise ValueError("expired tombstone requires batch_binding state none")
        if any(state != "unknown" for state in measurement_states.values()):
            raise ValueError("expired tombstone measurements must remain unknown")

    if evidence_state in ("smoke-only", "provisionally-calibrated"):
        if evidence_root is None:
            raise ValueError("observed capability card requires --evidence-root")
        batch_reference = {
            "path": batch_binding["batch_path"],
            "digest": batch_binding["batch_digest"],
        }
        batch_document = _open_bound_json(
            evidence_root, batch_reference, "batch_binding"
        )
        batch_result = validate_batch(batch_document)
        if batch_document.get("batch_id") != batch_binding["batch_id"]:
            raise ValueError("batch binding id mismatch")
        expected_execution_mode = (
            "authorized-smoke"
            if evidence_state == "smoke-only"
            else "authorized-calibration-batch"
        )
        if batch_document.get("execution_mode") != expected_execution_mode:
            raise ValueError("batch binding execution_mode mismatch")
        if batch_result["terminal_state"] is not None or not batch_result["executed"]:
            raise ValueError("observed capability card requires an executed batch")
        planned_cli_runs = sum(
            item["expected_cli_invocations"]
            for item in batch_document["invocations"]
        )
        if batch_binding["planned_runs"] != planned_cli_runs:
            raise ValueError(
                "batch_binding planned_runs must match preregistered CLI invocations"
            )
        matching_configurations = [
            item
            for item in batch_document["execution_configurations"]
            if item["configuration_id"]
            == card["execution_configuration"]["configuration_id"]
        ]
        if len(matching_configurations) != 1:
            raise ValueError(
                "batch must contain exactly one matching execution configuration"
            )
        expected_configuration = dict(card["execution_configuration"])
        expected_configuration["binding_state"] = "control-bound"
        if matching_configurations[0] != expected_configuration:
            raise ValueError("batch and card execution configuration mismatch")

        outcome_counts = {"completed": 0, "failed": 0, "stopped": 0}
        stop_reason_counts: Dict[str, int] = {}
        observed_shapes = []
        observed_measurements = []
        for index, item in enumerate(evidence):
            observation_value = _open_bound_json(
                evidence_root,
                item,
                "evidence[{}]".format(index),
            )
            observation = validate_smoke_observation(
                observation_value, evidence_root=evidence_root
            )
            if observation["observation_id"] != item["observation_id"]:
                raise ValueError("evidence observation_id mismatch")
            if observation["summary_observation_path"] != item["path"]:
                raise ValueError(
                    "summary observation_path does not match retained observation"
                )
            if observation["execution_configuration"] != card["execution_configuration"]:
                raise ValueError("card and observation execution configuration mismatch")
            observation_batch = observation["batch_binding"]
            expected_observation_batch = {
                "state": "receipt-bound",
                "batch_id": batch_binding["batch_id"],
                "batch_ref": {
                    "path": batch_binding["batch_path"],
                    "digest": batch_binding["batch_digest"],
                },
            }
            if observation_batch != expected_observation_batch:
                raise ValueError("card and observation batch binding mismatch")
            observed_measurements.append(observation["measurements"])
            if observation["task_shape"] not in task_shapes:
                raise ValueError("observation task shape is outside card task_shapes")
            observed_shapes.append(observation["task_shape"])
            status = observation["outcome"]["status"]
            outcome_counts[status] += 1
            reason = observation["outcome"]["stop_reason"]
            if reason is not None:
                stop_reason_counts[reason] = stop_reason_counts.get(reason, 0) + 1
        if set(observed_shapes) != set(task_shapes):
            raise ValueError("retained observations do not cover card task_shapes")
        if outcome_summary is None or any(
            outcome_summary[name] != outcome_counts[name]
            for name in ("completed", "failed", "stopped")
        ):
            raise ValueError("card outcome summary does not match retained observations")
        if outcome_summary["stop_reasons"] != stop_reason_counts:
            raise ValueError("card stop reasons do not match retained observations")
        if any(item != card["measurements"] for item in observed_measurements):
            raise ValueError("card measurements must match every retained observation")

    return {
        "valid": True,
        "document": "capability-card",
        "card_id": card_id,
        "platform": platform,
        "evidence_state": evidence_state,
        "observed_runs": observed_runs,
        "outcomes": (
            None
            if outcome_summary is None
            else {
                name: outcome_summary[name]
                for name in ("completed", "failed", "stopped")
            }
        ),
        "provider_usage_status": measurement_states["provider_usage"],
        "derived_usage_status": measurement_states["derived_usage"],
        "billed_cost_status": measurement_states["billed_cost"],
        "derived_cost_status": measurement_states["derived_cost"],
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate one calibration batch, smoke observation or capability card without execution."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--batch", type=Path)
    group.add_argument("--capability-card", type=Path)
    group.add_argument("--smoke-observation", type=Path)
    parser.add_argument("--evidence-root", type=Path)
    arguments = parser.parse_args(argv)
    try:
        if arguments.batch is not None:
            result = validate_batch(load_json(arguments.batch))
        elif arguments.capability_card is not None:
            result = validate_capability_card(
                load_json(arguments.capability_card),
                evidence_root=arguments.evidence_root,
            )
        else:
            result = validate_smoke_observation(
                load_json(arguments.smoke_observation),
                evidence_root=arguments.evidence_root,
            )
    except (OSError, TypeError, ValueError) as error:
        print("validation failed: {}".format(error), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
