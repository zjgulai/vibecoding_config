#!/usr/bin/env python3
"""Run one EVAL-10 Codex connectivity smoke without producing a quality comparison."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timedelta, timezone
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Mapping, Optional, Sequence

from calibration.validate_calibration import (
    validate_authorization_grant,
    validate_batch,
    validate_installation_identity,
    validate_smoke_observation,
)
from calibration_adapters.codex_eval10 import (
    ALLOWED_INPUTS,
    DISABLED_FEATURES,
    MACOS_CONTAINMENT_PROFILE,
    MACOS_SANDBOX_EXEC,
    _prompt,
    build_codex_command,
)
from eval_protocol import (
    artifact_tree_digest_v2,
    load_json,
    sha256_bytes,
    sha256_file,
    tree_digest_v2,
)
from run_lifecycle import run_lifecycle


SOURCE_ROOT = Path(__file__).resolve().parent
SOURCE_MANIFEST = SOURCE_ROOT / "fixture-manifest.calibration.json"
SOURCE_FIXTURE = (
    SOURCE_ROOT / "fixtures" / "representative" / "10-instruction-conflict"
)
SOURCE_ADAPTER = SOURCE_ROOT / "calibration_adapters" / "codex_eval10.py"
TASK_ID = "10-instruction-conflict"
TASK_SHAPE = "instruction-conflict"
OBSERVATION_REVISION = "smoke-observation-v2"
AUTHORIZATION_CONSUMPTION_REGISTRY = (
    SOURCE_ROOT / "calibration" / ".authorization-consumption-v1"
)
REAL_SMOKE_REQUIRED_AUTHORIZED_ACTIONS = frozenset(
    {
        "model-request",
        "codex-client-network-transport",
        "synthetic-fixture-prompt-egress",
        "local-receipt-and-artifact-write",
        "authorization-consumption-registry-write",
    }
)
REAL_SMOKE_REQUIRED_FORBIDDEN_ACTIONS = frozenset(
    {
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
)


def _canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _unknown_measurements() -> Dict:
    return {
        "provider_usage": {
            "status": "unknown",
            "input_tokens": None,
            "output_tokens": None,
            "cached_input_tokens": None,
            "reasoning_output_tokens": None,
            "receipt_ref": None,
        },
        "derived_usage": {
            "status": "unknown",
            "input_tokens": None,
            "output_tokens": None,
            "method": None,
        },
        "billed_cost": {
            "status": "unknown",
            "amount_usd": None,
            "receipt_ref": None,
        },
        "derived_cost": {
            "status": "unknown",
            "amount_usd": None,
            "method": None,
        },
    }


def _canonical_digest(value: object) -> str:
    return sha256_bytes(_canonical_bytes(value))


def _file_reference(path: Path, evidence_root: Path) -> Dict[str, str]:
    return {
        "path": path.resolve().relative_to(evidence_root.resolve()).as_posix(),
        "digest": sha256_file(path),
    }


def _tree_reference(
    path: Path, evidence_root: Path, *, artifact_tree: bool = False
) -> Dict[str, str]:
    digest = (
        artifact_tree_digest_v2(path) if artifact_tree else tree_digest_v2(path)
    )
    return {
        "path": path.resolve().relative_to(evidence_root.resolve()).as_posix(),
        "digest": digest,
    }


def _regular_file(path: Path, label: str) -> Path:
    if path.is_symlink() or not path.is_file():
        raise ValueError("{} must be a regular file".format(label))
    return path.resolve()


def _runtime_platform() -> tuple[str, str]:
    platform_name = {
        "darwin": "darwin",
        "linux": "linux",
        "win32": "win32",
    }.get(sys.platform)
    machine_name = {
        "aarch64": "arm64",
        "arm64": "arm64",
        "amd64": "x64",
        "x86_64": "x64",
    }.get(platform.machine().lower())
    if platform_name is None or machine_name is None:
        raise ValueError("unsupported Codex installation platform")
    return platform_name, machine_name


def _verify_macos_process_containment() -> None:
    if sys.platform != "darwin" or os.name != "posix":
        raise ValueError("real Codex smoke requires macOS sandbox containment")
    sandbox_exec = _regular_file(MACOS_SANDBOX_EXEC, "macOS sandbox-exec")
    if not os.access(sandbox_exec, os.X_OK):
        raise ValueError("macOS sandbox-exec must be executable")
    probe = (
        "import subprocess,sys; "
        "\ntry: subprocess.run(['/bin/true'], check=True)"
        "\nexcept PermissionError: print('fork-denied'); raise SystemExit(0)"
        "\nraise SystemExit(42)"
    )
    completed = subprocess.run(
        [
            str(sandbox_exec),
            "-p",
            MACOS_CONTAINMENT_PROFILE,
            sys.executable,
            "-c",
            probe,
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=5,
        env={"PATH": os.defpath},
    )
    if completed.returncode != 0 or completed.stdout.strip() != "fork-denied":
        raise ValueError("macOS sandbox containment self-test failed")


def _verify_official_codex_installation(
    executable: Path, expected_version: str
) -> Dict[str, str]:
    requested_entrypoint = _regular_file(
        executable.resolve(), "resolved Codex entrypoint"
    )
    path_candidate = shutil.which("codex")
    if path_candidate is None:
        raise ValueError("PATH does not resolve an installed codex executable")
    path_entrypoint = _regular_file(
        Path(path_candidate).resolve(), "PATH-resolved Codex entrypoint"
    )
    if requested_entrypoint != path_entrypoint:
        raise ValueError(
            "real execution Codex entrypoint must equal the PATH-resolved installation"
        )
    if requested_entrypoint.name != "codex.js" or requested_entrypoint.parent.name != "bin":
        raise ValueError("real execution requires the official Codex npm entrypoint")

    package_root = requested_entrypoint.parent.parent
    package_manifest_path = _regular_file(
        package_root / "package.json", "Codex package manifest"
    )
    package_manifest = load_json(package_manifest_path)
    if package_manifest.get("name") != "@openai/codex":
        raise ValueError("Codex package name must be @openai/codex")
    if package_manifest.get("version") != expected_version:
        raise ValueError("Codex package version does not match the expected client version")
    if package_manifest.get("bin") != {"codex": "bin/codex.js"}:
        raise ValueError("Codex package bin.codex must be bin/codex.js")

    platform_name, machine_name = _runtime_platform()
    native_dependency = "@openai/codex-{}-{}".format(
        platform_name, machine_name
    )
    expected_native_version = "{}-{}-{}".format(
        expected_version, platform_name, machine_name
    )
    optional_dependencies = package_manifest.get("optionalDependencies")
    if not isinstance(optional_dependencies, dict) or optional_dependencies.get(
        native_dependency
    ) != "npm:@openai/codex@{}".format(expected_native_version):
        raise ValueError("Codex package does not bind the current native package")

    native_root = package_root / "node_modules" / Path(native_dependency)
    native_manifest_path = _regular_file(
        native_root / "package.json", "Codex native package manifest"
    )
    native_manifest = load_json(native_manifest_path)
    if native_manifest.get("name") != "@openai/codex":
        raise ValueError("Codex native package name must be @openai/codex")
    if native_manifest.get("version") != expected_native_version:
        raise ValueError("Codex native package version mismatch")
    if native_manifest.get("os") != [platform_name]:
        raise ValueError("Codex native package operating-system binding mismatch")
    if native_manifest.get("cpu") != [machine_name]:
        raise ValueError("Codex native package architecture binding mismatch")

    binary_names = {"codex", "codex.exe"}
    native_binaries = sorted(
        path
        for path in (native_root / "vendor").glob("*/bin/*")
        if path.name in binary_names and not path.is_symlink() and path.is_file()
    )
    if len(native_binaries) != 1:
        raise ValueError("Codex native package must contain exactly one platform binary")
    native_binary = native_binaries[0]
    if not os.access(native_binary, os.X_OK):
        raise ValueError("Codex native binary must be executable")

    identity: Dict[str, str] = {
        "schema_version": "1",
        "identity_revision": "codex-installation-identity-v1",
        "package_name": "@openai/codex",
        "package_version": expected_version,
        "package_manifest_digest": sha256_file(package_manifest_path),
        "entrypoint_digest": sha256_file(requested_entrypoint),
        "native_package_name": "@openai/codex",
        "native_package_version": expected_native_version,
        "native_package_manifest_digest": sha256_file(native_manifest_path),
        "native_binary_digest": sha256_file(native_binary),
        "platform": platform_name,
        "machine": machine_name,
    }
    identity["identity_digest"] = _canonical_digest(identity)
    validate_installation_identity(identity)
    return identity


def _native_codex_binary(
    entrypoint: Path, identity: Mapping[str, str]
) -> Path:
    package_root = entrypoint.resolve().parent.parent
    native_dependency = "@openai/codex-{}-{}".format(
        identity["platform"], identity["machine"]
    )
    native_root = package_root / "node_modules" / Path(native_dependency)
    candidates = sorted(
        path.resolve()
        for path in (native_root / "vendor").glob("*/bin/*")
        if path.name in {"codex", "codex.exe"}
        and not path.is_symlink()
        and path.is_file()
    )
    if len(candidates) != 1 or not os.access(candidates[0], os.X_OK):
        raise ValueError("Codex native package binary binding is invalid")
    if sha256_file(candidates[0]) != identity["native_binary_digest"]:
        raise ValueError("Codex native binary digest drifted")
    return candidates[0]


def _snapshot_official_codex_installation(
    entrypoint: Path,
    identity: Mapping[str, str],
    evidence_root: Path,
) -> tuple[Path, Path]:
    """Retain the exact minimum package files needed for later digest revalidation."""

    source_entrypoint = _regular_file(entrypoint, "Codex installation entrypoint")
    source_package_root = source_entrypoint.parent.parent
    source_package_manifest = _regular_file(
        source_package_root / "package.json", "Codex package manifest"
    )
    native_dependency = "@openai/codex-{}-{}".format(
        identity["platform"], identity["machine"]
    )
    source_native_root = source_package_root / "node_modules" / Path(native_dependency)
    source_native_manifest = _regular_file(
        source_native_root / "package.json", "Codex native package manifest"
    )
    source_native_binary = _native_codex_binary(source_entrypoint, identity)

    retained_package_root = evidence_root / "installation-artifacts" / "package"
    retained_entrypoint = retained_package_root / "bin" / "codex.js"
    retained_package_manifest = retained_package_root / "package.json"
    retained_native_root = retained_package_root / "node_modules" / Path(
        native_dependency
    )
    retained_native_manifest = retained_native_root / "package.json"
    retained_native_binary = retained_native_root / source_native_binary.relative_to(
        source_native_root
    )
    for source, target in (
        (source_entrypoint, retained_entrypoint),
        (source_package_manifest, retained_package_manifest),
        (source_native_manifest, retained_native_manifest),
        (source_native_binary, retained_native_binary),
    ):
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if target.is_symlink() or not target.is_file():
            raise ValueError("retained Codex installation artifact is not a regular file")

    expected_digests = {
        retained_entrypoint: identity["entrypoint_digest"],
        retained_package_manifest: identity["package_manifest_digest"],
        retained_native_manifest: identity["native_package_manifest_digest"],
        retained_native_binary: identity["native_binary_digest"],
    }
    for path, expected_digest in expected_digests.items():
        if sha256_file(path) != expected_digest:
            raise ValueError("retained Codex installation artifact digest mismatch")
    if not os.access(retained_native_binary, os.X_OK):
        raise ValueError("retained Codex native binary must remain executable")
    return retained_entrypoint.resolve(), retained_native_binary.resolve()


def _oracle_revision(fixture: Mapping, fixture_root: Path) -> str:
    oracle = fixture.get("oracle")
    if not isinstance(oracle, Mapping):
        raise ValueError("fixture oracle contract must be an object")
    command = oracle.get("command")
    if not isinstance(command, list) or not command or command[0] != "./fixture-control":
        raise ValueError("calibration oracle must use ./fixture-control")
    executable = _regular_file(fixture_root / "fixture-control", "fixture oracle")
    return _canonical_digest(
        {
            "contract_revision": "retained-oracle-contract-v1",
            "oracle": dict(oracle),
            "executable_path": "fixture-control",
            "executable_digest": sha256_file(executable),
        }
    )


def _repository_file(root: Path, relative: str, label: str) -> Path:
    cursor = root.resolve()
    for part in Path(relative).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("{} must not traverse a symlink".format(label))
    try:
        resolved = cursor.resolve(strict=True)
        resolved.relative_to(root.resolve())
    except (FileNotFoundError, ValueError) as error:
        raise ValueError("{} must remain inside the repository".format(label)) from error
    if not resolved.is_file():
        raise ValueError("{} must be a regular file".format(label))
    return resolved


def _parse_expiry(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        expiry = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise ValueError("authorization expires_at must be an ISO-8601 timestamp") from error
    if expiry.tzinfo is None or expiry.utcoffset() is None:
        raise ValueError("authorization expires_at must include a timezone")
    return expiry


def _require_authorization_window(
    expires_at: str, minimum_seconds: int, *, label: str
) -> None:
    if isinstance(minimum_seconds, bool) or not isinstance(minimum_seconds, int):
        raise ValueError("{} minimum window must be an integer".format(label))
    if minimum_seconds < 1:
        raise ValueError("{} minimum window must be positive".format(label))
    minimum_expiry = datetime.now(timezone.utc) + timedelta(seconds=minimum_seconds)
    if _parse_expiry(expires_at).astimezone(timezone.utc) <= minimum_expiry:
        raise ValueError(
            "{} expires before the bounded lifecycle can finish".format(label)
        )


def _authorization_marker_path(batch_digest: str) -> Path:
    return AUTHORIZATION_CONSUMPTION_REGISTRY / "{}.consumed.json".format(
        batch_digest.removeprefix("sha256:"),
    )


def _consume_authorization_once(
    *,
    grant_id: str,
    grant_digest: str,
    batch_digest: str,
    installation_identity_digest: str,
    output_root: Path,
) -> Path:
    registry = AUTHORIZATION_CONSUMPTION_REGISTRY
    if registry.exists():
        if registry.is_symlink() or not registry.is_dir():
            raise ValueError("authorization consumption registry must be a regular directory")
    else:
        registry.mkdir(parents=True, mode=0o700)
    marker = _authorization_marker_path(batch_digest)
    payload = _canonical_bytes(
        {
            "schema_version": "1",
            "grant_id": grant_id,
            "grant_digest": grant_digest,
            "batch_digest": batch_digest,
            "installation_identity_digest": installation_identity_digest,
            "consumed_at": datetime.now(timezone.utc).isoformat(),
            "evidence_root": str(output_root),
            "state": "consumed-before-invocation",
        }
    )
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        descriptor = os.open(marker, flags, 0o600)
    except FileExistsError as error:
        raise ValueError("authorized-once batch has already been consumed") from error
    try:
        os.write(descriptor, payload)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return marker


def _write_blocked_batch(
    output_root: Path, batch_path: Path, stop_reason: str
) -> Optional[Path]:
    try:
        batch = load_json(batch_path)
        validate_batch(batch)
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return None
    if (
        batch.get("execution_mode") != "authorized-smoke"
        or batch.get("authorization", {}).get("state") != "authorized-once"
    ):
        return None
    blocked = copy.deepcopy(batch)
    blocked["batch_revision"] = "{}.blocked-after-preflight".format(
        blocked["batch_revision"]
    )
    blocked["purpose"] = "{} Preflight stopped before any model-bearing CLI invocation.".format(
        blocked["purpose"]
    )
    blocked["budget"]["max_cli_invocations"] = 0
    blocked["authorization"]["state"] = "blocked-after-preflight"
    for invocation in blocked["invocations"]:
        invocation.update(
            plan_state="blocked",
            execute=False,
            network_policy="blocked",
            expected_cli_invocations=0,
            blocker=stop_reason,
        )
    validate_batch(blocked)
    path = output_root / "blocked-after-preflight-batch.json"
    _write_json(path, blocked)
    return path


def _prepare_output_root(root: Path) -> Path:
    if not root.is_absolute():
        raise ValueError("output root must be absolute")
    if root.exists():
        if root.is_symlink() or not root.is_dir() or any(root.iterdir()):
            raise ValueError("output root must not exist or must be an empty regular directory")
    else:
        root.mkdir(parents=True, exist_ok=False)
    return root.resolve()


def _stage_inputs(
    output_root: Path, control: Dict, *, prompt: str
) -> Dict[str, Path]:
    staged = output_root / "staged-inputs"
    staged.mkdir()
    manifest_path = staged / SOURCE_MANIFEST.name
    shutil.copy2(SOURCE_MANIFEST, manifest_path)

    fixture_root = staged / "fixtures" / "representative" / TASK_ID
    fixture_root.parent.mkdir(parents=True)
    shutil.copytree(SOURCE_FIXTURE, fixture_root)

    adapter_root = staged / "adapters"
    adapter_root.mkdir()
    adapter_path = adapter_root / SOURCE_ADAPTER.name
    shutil.copy2(SOURCE_ADAPTER, adapter_path)

    prompt_path = staged / "prompt.txt"
    prompt_path.write_bytes(prompt.encode("utf-8"))

    configuration_root = staged / "configuration"
    configuration_root.mkdir()
    control = dict(control)
    control["adapter_digest"] = sha256_file(adapter_path)
    control["adapter_ref"] = _file_reference(adapter_path, output_root)
    control["prompt_ref"] = _file_reference(prompt_path, output_root)
    _write_json(configuration_root / "control.json", control)
    return {
        "manifest": manifest_path,
        "fixture": fixture_root,
        "adapter": adapter_path,
        "prompt": prompt_path,
        "configuration": configuration_root,
    }


def _verify_staged_real_inputs(
    output_root: Path,
    staged: Mapping[str, Path],
    *,
    batch_control: Mapping,
    expected_control: Mapping,
) -> Dict:
    batch_path = _regular_file(output_root / "batch.json", "staged batch")
    if sha256_file(batch_path) != batch_control["batch_plan_digest"]:
        raise ValueError("staged batch digest drifted before authorization consumption")
    staged_batch = load_json(batch_path)
    if staged_batch != batch_control["batch"]:
        raise ValueError("staged batch content drifted before authorization consumption")
    validate_batch(staged_batch)

    fixture_binding = staged_batch["fixture_binding"]
    manifest_path = _regular_file(staged["manifest"], "staged manifest")
    if sha256_file(manifest_path) != fixture_binding["manifest_digest"]:
        raise ValueError("staged manifest digest drifted before authorization consumption")
    manifest = load_json(manifest_path)
    manifest_fixtures = [
        item for item in manifest.get("fixtures", []) if item.get("task_id") == TASK_ID
    ]
    if len(manifest_fixtures) != 1:
        raise ValueError("staged manifest must contain exactly one EVAL-10 fixture")
    manifest_fixture = manifest_fixtures[0]
    fixture_root = staged["fixture"]
    expected_fixture_fields = {
        "manifest_path": manifest_path.resolve().relative_to(
            output_root.resolve()
        ).as_posix(),
        "task_id": TASK_ID,
        "task_revision": manifest_fixture.get("task_revision"),
        "fixture_id": manifest_fixture.get("fixture_id"),
        "fixture_revision": manifest_fixture.get("fixture_revision"),
        "initial_state_digest": manifest_fixture.get("initial_state_digest"),
        "oracle_revision": _oracle_revision(manifest_fixture, fixture_root),
    }
    for field, expected in expected_fixture_fields.items():
        if fixture_binding.get(field) != expected:
            raise ValueError("staged fixture binding drifted at {}".format(field))

    if fixture_root.is_symlink() or not fixture_root.is_dir():
        raise ValueError("staged fixture must be a regular directory")
    if tree_digest_v2(fixture_root) != fixture_binding["initial_state_digest"]:
        raise ValueError("staged fixture tree drifted before authorization consumption")
    workspace = fixture_root / "workspace"
    prompt_contents = {
        name: _regular_file(workspace / name, "staged prompt input " + name).read_text(
            encoding="utf-8"
        )
        for name in ALLOWED_INPUTS
    }
    staged_prompt = _regular_file(staged["prompt"], "staged prompt")
    prompt_bytes = _prompt(prompt_contents).encode("utf-8")
    if staged_prompt.read_bytes() != prompt_bytes:
        raise ValueError("staged prompt content does not match the staged fixture")
    if sha256_file(staged_prompt) != fixture_binding["prompt_digest"]:
        raise ValueError("staged prompt digest drifted before authorization consumption")

    staged_adapter = _regular_file(staged["adapter"], "staged adapter")
    adapter_digest = sha256_file(staged_adapter)
    expected_adapter_revision = "codex-eval10-v2@{}".format(adapter_digest)
    if (
        batch_control["execution_configuration"].get("adapter_revision")
        != expected_adapter_revision
    ):
        raise ValueError("staged adapter digest does not match the authorized configuration")

    control_path = _regular_file(
        staged["configuration"] / "control.json", "staged control"
    )
    control = load_json(control_path)
    enriched_control = dict(expected_control)
    enriched_control["adapter_digest"] = adapter_digest
    enriched_control["adapter_ref"] = _file_reference(staged_adapter, output_root)
    enriched_control["prompt_ref"] = _file_reference(staged_prompt, output_root)
    if control != enriched_control:
        raise ValueError("staged control drifted before authorization consumption")
    if control["prompt_digest"] != fixture_binding["prompt_digest"]:
        raise ValueError("staged control prompt digest mismatch")

    installation_path = _regular_file(
        output_root / "installation-identity.json", "installation identity"
    )
    installation_identity = validate_installation_identity(load_json(installation_path))
    if (
        installation_identity["identity_digest"]
        != control["installation_identity_digest"]
    ):
        raise ValueError("installation identity digest does not match staged control")

    authorization_path = _regular_file(
        output_root / "authorization-grant.json", "staged authorization grant"
    )
    if sha256_file(authorization_path) != batch_control["authorization_ref_digest"]:
        raise ValueError("staged authorization grant digest drifted before consumption")
    staged_grant = load_json(authorization_path)
    if staged_grant != batch_control["authorization_grant"]:
        raise ValueError("staged authorization grant content drifted before consumption")
    grant_validation = validate_authorization_grant(
        staged_grant,
        batch=staged_batch,
        batch_digest=batch_control["batch_plan_digest"],
        installation_identity_digest=installation_identity["identity_digest"],
        require_unexpired=True,
    )
    _require_authorization_window(
        grant_validation["expires_at"],
        batch_control["max_wall_clock_seconds"],
        label="authorization grant",
    )
    return control


def _real_batch_control(
    batch_path: Path,
    *,
    expected_client_version: str,
    model: str,
    reasoning_effort: str,
    client_timeout_seconds: int,
    permissions_digest: str,
    toolset_digest: str,
    adapter_digest: str,
    prompt_digest: str,
    installation_identity_digest: str,
) -> Dict:
    batch = load_json(batch_path)
    result = validate_batch(batch)
    if result["execution_mode"] != "authorized-smoke":
        raise ValueError("real smoke requires an authorized-smoke batch")
    if result["terminal_state"] is not None or not result["executed"]:
        raise ValueError("real smoke batch is a nonexecuting terminal state")
    authorization = batch["authorization"]
    authorized_actions = set(authorization["authorized_actions"])
    forbidden_actions = set(authorization["forbidden_actions"])
    if authorized_actions != REAL_SMOKE_REQUIRED_AUTHORIZED_ACTIONS:
        raise ValueError(
            "real smoke authorization actions must exactly equal: {}".format(
                ", ".join(sorted(REAL_SMOKE_REQUIRED_AUTHORIZED_ACTIONS))
            )
        )
    if forbidden_actions != REAL_SMOKE_REQUIRED_FORBIDDEN_ACTIONS:
        raise ValueError(
            "real smoke forbidden actions must exactly equal: {}".format(
                ", ".join(sorted(REAL_SMOKE_REQUIRED_FORBIDDEN_ACTIONS))
            )
        )
    if result["cli_invocations_budget"] != 1:
        raise ValueError("real smoke requires exactly one model-bearing CLI invocation")
    if result["provider_requests_budget"] is not None:
        raise ValueError(
            "Codex built-in provider wire request count must remain unknown/null"
        )
    if len(batch["execution_configurations"]) != 1 or len(batch["invocations"]) != 1:
        raise ValueError("real smoke batch must contain exactly one configuration and invocation")
    configuration = batch["execution_configurations"][0]
    expected_configuration = {
        "platform": "codex",
        "harness": "codex-cli-with-eval10-adapter",
        "client_version": expected_client_version,
        "requested_model": model,
        "resolved_model": None,
        "model_resolution_status": "client-catalog-alias",
        "reasoning": reasoning_effort,
        "profile": "custom",
        "permissions_digest": permissions_digest,
        "toolset_digest": toolset_digest,
        "adapter_revision": "codex-eval10-v2@{}".format(adapter_digest),
        "binding_state": "control-bound",
        "blocker": None,
    }
    for field, expected in expected_configuration.items():
        if configuration[field] != expected:
            raise ValueError("authorized batch configuration drifted at {}".format(field))
    invocation = batch["invocations"][0]
    if (
        invocation["configuration_id"] != configuration["configuration_id"]
        or invocation["platform"] != "codex"
        or invocation["execute"] is not True
        or invocation["plan_state"] != "planned"
        or invocation["expected_cli_invocations"] != 1
        or invocation["expected_provider_requests"] is not None
    ):
        raise ValueError("authorized batch invocation does not bind the Codex smoke")
    expected_argv = build_codex_command(
        Path("codex"),
        model="<requested-model>",
        reasoning_effort="<reasoning-effort>",
        model_root=Path("<isolated-read-only-fixture-root>"),
        decision_path=Path("<artifact-root>/decision-log.md"),
    )
    expected_invocation = {
        "executable": "codex",
        "cwd": "<isolated-read-only-fixture-root>",
        "argv": expected_argv,
        "input_transport": "stdin",
        "stdin_source": "<fixture-prompt>",
        "stdout_format": "jsonl",
        "stderr_policy": "capture",
        "network_policy": "codex-client-network-endpoints-unverified",
        "file_policy": "read-only",
    }
    for field, expected in expected_invocation.items():
        if invocation[field] != expected:
            raise ValueError("authorized batch invocation drifted at {}".format(field))
    fixture = batch["fixture_binding"]
    manifest = load_json(SOURCE_MANIFEST)
    manifest_fixture = next(
        item for item in manifest["fixtures"] if item["task_id"] == TASK_ID
    )
    expected_fixture = {
        "state": "bound",
        "manifest_path": "staged-inputs/fixture-manifest.calibration.json",
        "manifest_digest": sha256_file(SOURCE_MANIFEST),
        "task_id": TASK_ID,
        "task_revision": manifest_fixture["task_revision"],
        "fixture_id": manifest_fixture["fixture_id"],
        "fixture_revision": manifest_fixture["fixture_revision"],
        "initial_state_digest": tree_digest_v2(SOURCE_FIXTURE),
        "prompt_digest": prompt_digest,
        "oracle_revision": _oracle_revision(manifest_fixture, SOURCE_FIXTURE),
    }
    for field, expected in expected_fixture.items():
        if fixture[field] != expected:
            raise ValueError("authorized batch fixture binding drifted at {}".format(field))
    if batch["budget"]["max_retries"] != 0:
        raise ValueError("real smoke batch must forbid retries")
    lifecycle_declared_seconds = sum(
        manifest_fixture[step]["timeout_seconds"]
        for step in ("reset", "setup", "oracle")
    )
    wrapper_timeout_seconds = client_timeout_seconds + 30
    minimum_wall_clock_seconds = (
        lifecycle_declared_seconds + wrapper_timeout_seconds
    )
    if batch["budget"]["max_wall_clock_seconds"] < minimum_wall_clock_seconds:
        raise ValueError(
            "real smoke batch wall-clock budget is below the declared lifecycle bound"
        )
    if batch["authorization"]["authorized_platforms"] != ["codex"]:
        raise ValueError("real smoke authorization must be limited to Codex")
    _require_authorization_window(
        batch["authorization"]["expires_at"],
        batch["budget"]["max_wall_clock_seconds"],
        label="real smoke authorization",
    )
    repository_root = SOURCE_ROOT.parents[2]
    authorization_ref = _repository_file(
        repository_root,
        batch["authorization"]["authorization_ref"],
        "real smoke authorization_ref",
    )
    batch_digest = sha256_file(batch_path)
    authorization_grant = load_json(authorization_ref)
    grant_validation = validate_authorization_grant(
        authorization_grant,
        batch=batch,
        batch_digest=batch_digest,
        installation_identity_digest=installation_identity_digest,
        require_unexpired=True,
    )
    return {
        "batch_id": batch["batch_id"],
        "batch_plan_digest": batch_digest,
        "authorization_ref": authorization_ref,
        "authorization_ref_digest": sha256_file(authorization_ref),
        "authorization_grant": authorization_grant,
        "grant_id": grant_validation["grant_id"],
        "authorization_expires_at": grant_validation["expires_at"],
        "max_wall_clock_seconds": batch["budget"]["max_wall_clock_seconds"],
        "execution_configuration": dict(configuration),
        "batch": batch,
    }


def _failure_reason(receipt: Dict) -> str:
    if receipt["lifecycle_timed_out"]:
        return "lifecycle_wall_clock_exceeded"
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


def _quarantine_output_guard(
    output_root: Path, artifact_root: Path, sentinel: str
) -> bool:
    candidates = (
        artifact_root / "_runner" / "agent.stdout",
        artifact_root / "_runner" / "agent.stderr",
        artifact_root / "decision-log.md",
    )
    contaminated = []
    for path in candidates:
        if path.is_symlink() or not path.is_file():
            continue
        if sentinel not in path.read_text(encoding="utf-8", errors="replace"):
            continue
        contaminated.append(path)

    report_path = artifact_root / "_runner" / "output-guard.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    sanitized = []
    if contaminated:
        quarantine_root = output_root / "quarantine"
        quarantine_root.mkdir(mode=0o700, exist_ok=False)
        for source in contaminated:
            relative = source.relative_to(artifact_root)
            target = quarantine_root / relative
            target.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
            os.replace(source, target)
            target.chmod(0o600)
            source.write_text(
                "[REDACTED: synthetic sentinel detected by pre-receipt output guard]\n",
                encoding="utf-8",
            )
            source.chmod(0o600)
            sanitized.append(
                {
                    "artifact_path": relative.as_posix(),
                    "quarantined_digest": sha256_file(target),
                }
            )
    _write_json(
        report_path,
        {
            "schema_version": "1",
            "guard_revision": "calibration-output-guard-v1",
            "status": "failed" if contaminated else "pass",
            "failure": "raw_output_sentinel_detected" if contaminated else None,
            "sanitized_artifacts": sanitized,
            "quarantine_scope": (
                "restricted-output-root-outside-receipt-artifact-tree"
                if contaminated
                else None
            ),
        },
    )
    report_path.chmod(0o600)
    return not contaminated


def _run_prepared(
    arguments: argparse.Namespace,
    output_root: Path,
    execution_state: Dict[str, object],
) -> Dict:
    permission_policy = {
        "approval": "never",
        "agent_workspace": "curated-temporary-read-only",
        "auth_home": "temporary-auth-only-copy-0600-source-integrity-checked",
        "parent_environment": "process-launch-allowlist",
        "project_instructions": "disabled-and-not-staged",
        "external_side_effects": "forbidden",
        "git_writes": "forbidden",
        "retries": 0,
    }
    tool_policy = {
        "browser": False,
        "mcp": False,
        "native_web_search": False,
        "disabled_features": list(DISABLED_FEATURES),
        "tool_calls": "disabled-by-cli-feature-gate-and-jsonl-event-gate",
    }
    permissions_digest = sha256_bytes(_canonical_bytes(permission_policy))
    toolset_digest = sha256_bytes(_canonical_bytes(tool_policy))
    execution_kind = arguments.execution_kind
    if execution_kind == "real" and arguments.batch_plan is None:
        raise ValueError("real execution requires --batch-plan")
    if execution_kind == "test-double" and arguments.batch_plan is not None:
        raise ValueError("test-double execution must not consume a real authorization batch")
    workspace = SOURCE_FIXTURE / "workspace"
    prompt_contents = {
        name: (workspace / name).read_text(encoding="utf-8")
        for name in ALLOWED_INPUTS
    }
    prompt_text = _prompt(prompt_contents)
    prompt_digest = sha256_bytes(prompt_text.encode("utf-8"))
    requested_executable = _regular_file(
        arguments.codex_executable.resolve(), "codex executable"
    )
    auth_file = _regular_file(arguments.auth_file, "auth file")

    batch_control: Dict = {}
    installation_identity: Optional[Dict[str, str]] = None
    installation_entrypoint = requested_executable
    runtime_executable = requested_executable
    if execution_kind == "real":
        _verify_macos_process_containment()
        installation_identity = _verify_official_codex_installation(
            requested_executable, arguments.expected_client_version
        )
        installation_entrypoint, runtime_executable = (
            _snapshot_official_codex_installation(
                requested_executable, installation_identity, output_root
            )
        )
        _write_json(output_root / "installation-identity.json", installation_identity)
        batch_path = _regular_file(arguments.batch_plan, "batch plan")
        batch_control = _real_batch_control(
            batch_path,
            expected_client_version=arguments.expected_client_version,
            model=arguments.model,
            reasoning_effort=arguments.reasoning_effort,
            client_timeout_seconds=arguments.client_timeout_seconds,
            permissions_digest=permissions_digest,
            toolset_digest=toolset_digest,
            adapter_digest=sha256_file(SOURCE_ADAPTER),
            prompt_digest=prompt_digest,
            installation_identity_digest=installation_identity["identity_digest"],
        )
        shutil.copy2(batch_path, output_root / "batch.json")
        shutil.copy2(
            batch_control["authorization_ref"],
            output_root / "authorization-grant.json",
        )
    control = {
        "schema_version": "1",
        "purpose": "eval-10-connectivity-smoke",
        "execution_kind": execution_kind,
        "client": "codex-cli",
        "expected_client_version": arguments.expected_client_version,
        "requested_model": arguments.model,
        "resolved_model": None,
        "reasoning_effort": arguments.reasoning_effort,
        "profile": "custom",
        "permissions": permission_policy,
        "permissions_digest": permissions_digest,
        "toolset": tool_policy,
        "toolset_digest": toolset_digest,
        "provider_usage_binding": "unavailable",
        "billed_cost": None,
        "derived_cost": None,
        "prompt_digest": prompt_digest,
        "installation_identity_digest": (
            installation_identity["identity_digest"]
            if installation_identity is not None
            else None
        ),
        "batch_id": batch_control.get("batch_id"),
        "batch_plan_digest": batch_control.get("batch_plan_digest"),
        "authorization_ref_digest": batch_control.get("authorization_ref_digest"),
    }
    staged = _stage_inputs(output_root, control, prompt=prompt_text)
    if execution_kind == "real":
        _verify_staged_real_inputs(
            output_root,
            staged,
            batch_control=batch_control,
            expected_control=control,
        )
        consumption_marker = _consume_authorization_once(
            grant_id=batch_control["grant_id"],
            grant_digest=batch_control["authorization_ref_digest"],
            batch_digest=batch_control["batch_plan_digest"],
            installation_identity_digest=installation_identity["identity_digest"],
            output_root=output_root,
        )
        execution_state.update(
            phase="authorization-consumed-before-lifecycle",
            authorization_consumed=True,
        )
        shutil.copy2(consumption_marker, output_root / "authorization-consumption.json")
        _verify_staged_real_inputs(
            output_root,
            staged,
            batch_control=batch_control,
            expected_control=control,
        )
    run_root = output_root / "run"
    agent_version = "codex-cli-{}".format(arguments.expected_client_version)
    if execution_kind == "test-double":
        agent_version += "-test-double"
    declaration = {
        "agent": "codex",
        "agent_version": agent_version,
        "model": arguments.model,
        "reasoning_effort": arguments.reasoning_effort,
        "profile": "custom",
        "permissions_digest": permissions_digest,
        "toolset_digest": toolset_digest,
    }
    adapter_argv = [
        sys.executable,
        "-B",
        str(staged["adapter"]),
        "--codex-executable",
        str(runtime_executable),
        "--expected-client-version",
        arguments.expected_client_version,
        "--auth-file",
        str(auth_file),
        "--prompt-file",
        str(staged["prompt"]),
        "--expected-prompt-digest",
        prompt_digest,
        "--model",
        arguments.model,
        "--reasoning-effort",
        arguments.reasoning_effort,
        "--client-timeout-seconds",
        str(arguments.client_timeout_seconds),
    ]
    if execution_kind == "real":
        adapter_argv.extend(
            (
                "--installation-identity-file",
                str(output_root / "installation-identity.json"),
                "--expected-installation-identity-digest",
                installation_identity["identity_digest"],
                "--installation-entrypoint",
                str(installation_entrypoint),
                "--authorization-grant-file",
                str(output_root / "authorization-grant.json"),
                "--expected-authorization-grant-digest",
                batch_control["authorization_ref_digest"],
                "--authorization-expires-at",
                batch_control["authorization_expires_at"],
            )
        )
    sentinel = (staged["fixture"] / "workspace" / "secret-sentinel.txt").read_text(
        encoding="utf-8"
    ).strip()
    session_root_path: Optional[Path] = None
    with tempfile.TemporaryDirectory(
        prefix="eval10-codex-parent-owned-session-"
    ) as session_directory:
        session_root_path = Path(session_directory).resolve()
        session_root_path.chmod(0o700)
        adapter_argv.extend(("--session-root", str(session_root_path)))
        if execution_kind == "real":
            execution_state.update(
                phase="lifecycle-dispatched-after-authorization-consumption",
                model_execution_may_have_started=True,
            )
        receipt, success = run_lifecycle(
            staged["manifest"],
            TASK_ID,
            "codex-eval10-{}-v1".format(execution_kind),
            staged["configuration"],
            1,
            run_root,
            adapter_argv,
            arguments.client_timeout_seconds + 30,
            declaration,
            pre_receipt_artifact_guard=lambda artifact_root: _quarantine_output_guard(
                output_root, artifact_root, sentinel
            ),
            lifecycle_timeout_seconds=(
                batch_control["max_wall_clock_seconds"]
                if execution_kind == "real"
                else None
            ),
        )
        if execution_kind == "real":
            execution_state.update(
                phase="post-lifecycle-evidence-finalization",
                model_execution_may_have_started=receipt["steps"]["agent"]["executed"],
            )
    if session_root_path.exists():
        raise ValueError("parent-owned Codex session root cleanup failed")
    receipt_path = run_root / "receipt.json"
    artifact_root = run_root / "artifacts"
    guard_report = load_json(artifact_root / "_runner" / "output-guard.json")
    raw_output_sentinel_detected = guard_report["status"] == "failed"
    failure_reason = (
        "raw_output_sentinel_detected"
        if raw_output_sentinel_detected
        else None if success else _failure_reason(receipt)
    )
    run_status = (
        "completed"
        if success
        else "stopped"
        if not receipt["steps"]["agent"]["executed"]
        else "failed"
    )
    if execution_kind == "real":
        execution_configuration = dict(batch_control["execution_configuration"])
    else:
        execution_configuration = {
            "configuration_id": "codex-eval10-test-double-v2",
            "platform": "codex",
            "harness": "codex-cli-with-eval10-adapter-test-double",
            "client_version": arguments.expected_client_version,
            "requested_model": arguments.model,
            "resolved_model": None,
            "model_resolution_status": "client-catalog-alias",
            "reasoning": arguments.reasoning_effort,
            "profile": "custom",
            "permissions_digest": permissions_digest,
            "toolset_digest": toolset_digest,
            "adapter_revision": "codex-eval10-v2@{}".format(
                sha256_file(SOURCE_ADAPTER)
            ),
            "binding_state": "control-bound",
            "blocker": None,
        }
    execution_configuration["binding_state"] = "receipt-bound"
    execution_configuration_digest = _canonical_digest(execution_configuration)
    receipt_configuration_digest = receipt["configuration_digest"]
    measurements = _unknown_measurements()
    batch_binding = (
        {
            "state": "receipt-bound",
            "batch_id": batch_control["batch_id"],
            "batch_ref": _file_reference(output_root / "batch.json", output_root),
        }
        if execution_kind == "real"
        else {"state": "none", "batch_id": None, "batch_ref": None}
    )
    lifecycle_binding = {
        "manifest_ref": _file_reference(staged["manifest"], output_root),
        "configuration_root": _tree_reference(
            staged["configuration"], output_root
        ),
        "control_ref": _file_reference(
            staged["configuration"] / "control.json", output_root
        ),
        "artifact_root": _tree_reference(
            artifact_root, output_root, artifact_tree=True
        ),
        "fixture_root": _tree_reference(staged["fixture"], output_root),
        "prompt_ref": _file_reference(staged["prompt"], output_root),
        "adapter_ref": _file_reference(staged["adapter"], output_root),
        "installation_ref": (
            _file_reference(
                output_root / "installation-identity.json", output_root
            )
            if execution_kind == "real"
            else None
        ),
        "authorization_ref": (
            _file_reference(output_root / "authorization-grant.json", output_root)
            if execution_kind == "real"
            else None
        ),
        "authorization_consumption_ref": (
            _file_reference(
                output_root / "authorization-consumption.json", output_root
            )
            if execution_kind == "real"
            else None
        ),
    }

    observation_filename = (
        "observation.json"
        if execution_kind == "real"
        else "test-double-observation.json"
    )
    summary = {
        "schema_version": "1",
        "task_id": TASK_ID,
        "execution_configuration_id": execution_configuration["configuration_id"],
        "execution_configuration_digest": execution_configuration_digest,
        "receipt_configuration_digest": receipt_configuration_digest,
        "batch_binding": batch_binding,
        "execution_identity": {
            "executor": "codex-cli-test-double" if execution_kind == "test-double" else "codex-cli",
            "agent": "codex",
            "client_version": arguments.expected_client_version,
            "requested_model": arguments.model,
            "resolved_model": None,
            "reasoning_effort": arguments.reasoning_effort,
            "real_agent_execution": execution_kind == "real",
            "identity_authentication": (
                "local-package-shape-and-digest-consistency"
                if execution_kind == "real"
                else "invocation-declared-not-cryptographically-authenticated"
            ),
            "installation_identity_digest": (
                installation_identity["identity_digest"]
                if installation_identity is not None
                else None
            ),
        },
        "run_status": run_status,
        "failure": failure_reason,
        "oracle_outcome": receipt["oracle_outcome"],
        "quality_assessment": False,
        "quality_comparison": "not-applicable",
        "inference": "not-computed",
        "measurements": measurements,
        "raw_output_sentinel_detected": raw_output_sentinel_detected,
        "receipt_path": "run/receipt.json",
        "observation_path": observation_filename,
        "raw_stdout_path": "run/artifacts/_runner/agent.stdout",
        "raw_stderr_path": "run/artifacts/_runner/agent.stderr",
        "quarantine_created": (output_root / "quarantine").is_dir(),
        "mechanically_eligible": False,
        "unverified_scope": [
            "model-quality",
            "cross-model-comparison",
            "production-safety",
            "general-prompt-injection-resistance",
            "provider-billed-cost",
            "resolved-provider-model-id",
            "codex-package-publisher-authenticity",
            "provider-and-model-identity-authentication",
        ],
    }
    summary_path = output_root / "summary.json"
    _write_json(summary_path, summary)
    if execution_kind == "real":
        observation = {
            "schema_version": "2",
            "observation_revision": OBSERVATION_REVISION,
            "observation_id": "codex-eval10-real-v2",
            "observation_kind": "connectivity-smoke",
            "scope": "connectivity-only",
            "task_id": TASK_ID,
            "task_shape": TASK_SHAPE,
            "execution_configuration": execution_configuration,
            "execution_configuration_digest": execution_configuration_digest,
            "receipt_configuration_digest": receipt_configuration_digest,
            "outcome": {"status": run_status, "stop_reason": failure_reason},
            "oracle_outcome": receipt["oracle_outcome"],
            "batch_binding": batch_binding,
            "lifecycle_binding": lifecycle_binding,
            "summary_ref": _file_reference(summary_path, output_root),
            "receipt_ref": _file_reference(receipt_path, output_root),
            "measurements": measurements,
            "unverified_scope": list(summary["unverified_scope"]),
        }
        validate_smoke_observation(observation, evidence_root=output_root)
    else:
        observation = {
            "schema_version": "1",
            "observation_revision": "calibration-test-double-observation-v1",
            "observation_kind": "test-double-contract-check",
            "scope": "local-contract-only",
            "task_id": TASK_ID,
            "run_status": run_status,
            "failure": failure_reason,
            "oracle_outcome": receipt["oracle_outcome"],
            "batch_binding": batch_binding,
            "lifecycle_binding": lifecycle_binding,
            "summary_ref": _file_reference(summary_path, output_root),
            "receipt_ref": _file_reference(receipt_path, output_root),
            "mechanically_eligible": False,
        }
    _write_json(output_root / observation_filename, observation)
    return summary


def run(arguments: argparse.Namespace) -> Dict:
    output_root = _prepare_output_root(arguments.output_root)
    execution_state: Dict[str, object] = {
        "phase": "preflight-before-authorization-consumption",
        "authorization_consumed": False,
        "model_execution_may_have_started": False,
    }
    try:
        return _run_prepared(arguments, output_root, execution_state)
    except (KeyError, OSError, ValueError, subprocess.SubprocessError) as error:
        authorization_consumed = bool(execution_state["authorization_consumed"])
        report_kind = "execution" if authorization_consumed else "preflight"
        stop_reason = "{}-{}".format(report_kind, type(error).__name__.lower())
        blocked_batch = None
        if (
            arguments.execution_kind == "real"
            and arguments.batch_plan is not None
            and not authorization_consumed
        ):
            blocked_batch = _write_blocked_batch(
                output_root, arguments.batch_plan, stop_reason
            )
        sidecar_path = output_root / "run" / "artifacts" / "_runner" / "provider-invocation.json"
        sidecar_ref = None
        model_execution_observed = None
        if not sidecar_path.is_symlink() and sidecar_path.is_file():
            try:
                sidecar = load_json(sidecar_path)
                observed = sidecar.get("client_process_executed")
                if isinstance(observed, bool):
                    model_execution_observed = observed
                sidecar_ref = _file_reference(sidecar_path, output_root)
            except (OSError, ValueError, json.JSONDecodeError):
                pass
        model_execution_may_have_started = bool(
            execution_state["model_execution_may_have_started"]
        ) or model_execution_observed is True
        report_path = output_root / (
            "execution-failure-report.json"
            if authorization_consumed
            else "preflight-report.json"
        )
        if not report_path.exists():
            _write_json(
                report_path,
                {
                    "schema_version": "1",
                    "status": "failed" if authorization_consumed else "stopped",
                    "phase": execution_state["phase"],
                    "reason": stop_reason,
                    "message": str(error),
                    "authorization_consumed": authorization_consumed,
                    "model_execution_may_have_started": model_execution_may_have_started,
                    "model_execution_observed": model_execution_observed,
                    "provider_invocation_sidecar": sidecar_ref,
                    "smoke_observation_created": (
                        (output_root / "observation.json").is_file()
                        and not (output_root / "observation.json").is_symlink()
                    ),
                    "blocked_batch": (
                        _file_reference(blocked_batch, output_root)
                        if blocked_batch is not None
                        else None
                    ),
                },
            )
        raise


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--execution-kind", required=True, choices=("test-double", "real"))
    parser.add_argument("--batch-plan", type=Path)
    parser.add_argument("--codex-executable", required=True, type=Path)
    parser.add_argument("--expected-client-version", required=True)
    parser.add_argument("--auth-file", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--reasoning-effort",
        required=True,
        choices=("none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra"),
    )
    parser.add_argument("--client-timeout-seconds", type=int, default=240)
    arguments = parser.parse_args(argv)
    if arguments.client_timeout_seconds < 1 or arguments.client_timeout_seconds > 1800:
        parser.error("--client-timeout-seconds must be between 1 and 1800")
    try:
        summary = run(arguments)
    except (KeyError, OSError, ValueError, subprocess.SubprocessError) as error:
        print("calibration-smoke: {}".format(error), file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if summary["run_status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
