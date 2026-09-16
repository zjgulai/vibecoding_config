from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from calibration.validate_calibration import (
    CAPABILITY_BLOCKER_CODES,
    CAPABILITY_STATE_REASON_CODES,
    EXECUTION_CONFIGURATION_BLOCKER_CODES,
    EXPIRED_REASON_CODES,
    LIFECYCLE_BINDING_FIELDS,
    SMOKE_OBSERVATION_FIELDS,
    SMOKE_SUMMARY_FIELDS,
    _derived_state_reason,
)


CALIBRATION_DIR = Path(__file__).resolve().parent
VALIDATOR = CALIBRATION_DIR / "validate_calibration.py"
CAPABILITY_CARD_SCHEMA = CALIBRATION_DIR / "capability-card.schema.json"
PLATFORM_INVOCATIONS = CALIBRATION_DIR / "platform-invocations.json"
SMOKE_OBSERVATION_SCHEMA = CALIBRATION_DIR / "smoke-observation.schema.json"
SMOKE_SUMMARY_SCHEMA = CALIBRATION_DIR / "smoke-summary.schema.json"
CODEX_ADAPTER = CALIBRATION_DIR.parent / "calibration_adapters" / "codex_eval10.py"
SHA_A = "sha256:" + ("a" * 64)
SHA_B = "sha256:" + ("b" * 64)


def make_execution_configuration(
    configuration_id: str = "codex-dry-run-v1",
    platform: str = "codex",
) -> dict:
    return {
        "configuration_id": configuration_id,
        "platform": platform,
        "harness": "codex-cli",
        "client_version": "0.147.0",
        "requested_model": None,
        "resolved_model": None,
        "model_resolution_status": "not-observed",
        "reasoning": "high",
        "profile": "calibration-read-only-v1",
        "permissions_digest": None,
        "toolset_digest": None,
        "adapter_revision": "codex-jsonl-dry-run-v1",
        "binding_state": "declared-unbound",
        "blocker": None,
    }


def make_batch() -> dict:
    return {
        "schema_version": "1",
        "batch_id": "model-capability-card-dry-run-2026-09-16",
        "batch_revision": "2026-09-16.1",
        "execution_mode": "dry-run-only",
        "purpose": "Pre-register a zero-request calibration plan.",
        "fixture_binding": {
            "state": "unbound",
            "manifest_path": None,
            "manifest_digest": None,
            "task_id": "10-instruction-conflict",
            "task_revision": None,
            "fixture_id": "coding-agent-task-10",
            "fixture_revision": None,
            "initial_state_digest": None,
            "prompt_digest": None,
            "oracle_revision": None,
        },
        "treatment": {
            "mode": "none",
            "variable": None,
            "baseline": None,
            "candidate": None,
            "comparison_authorized": False,
        },
        "fixed_controls": {
            "repetitions_per_configuration": 1,
            "workspace_mode": "read-only",
            "prompt_source": "fixture-only",
            "web_search_enabled": False,
            "browser_enabled": False,
            "mcp_enabled": False,
            "external_side_effects_enabled": False,
            "git_writes_enabled": False,
            "retries": 0,
            "oracle_required": True,
            "raw_stdout_required": True,
            "raw_stderr_required": True,
            "receipt_required": True,
            "smoke_observation_required": True,
        },
        "data_egress": {
            "state": "none-authorized",
            "allowed_payloads": [],
            "forbidden_data": [
                "credentials",
                "secrets",
                "environment-files",
                "account-content",
                "pii",
                "repository-content-outside-fixture",
            ],
        },
        "budget": {
            "max_cli_invocations": 0,
            "max_provider_requests": 0,
            "max_tasks": 1,
            "max_repetitions_per_configuration": 1,
            "max_retries": 0,
            "max_wall_clock_seconds": 0,
            "max_billed_cost_usd": None,
            "billed_cost_limit_source": "unknown",
        },
        "authorization": {
            "state": "dry-run-only",
            "authorized_platforms": [],
            "authorized_actions": [
                "inspect-local-cli-metadata",
                "render-invocation-plan",
                "validate-local-contracts",
            ],
            "forbidden_actions": [
                "model-request",
                "network-request",
                "credential-read",
                "user-config-write",
                "workspace-write",
                "git-write",
                "external-side-effect",
            ],
            "authorization_ref": None,
            "expires_at": None,
        },
        "stop_conditions": [
            {
                "id": condition_id,
                "action": "stop-no-retry",
                "evidence_required": "Record the condition without weakening controls.",
            }
            for condition_id in (
                "control-digest-drift",
                "unresolved-model-alias",
                "secret-access-required",
                "unauthorized-network-tool",
                "unauthorized-write",
                "raw-output-secret-or-pii",
                "receipt-or-oracle-incomplete",
                "public-cli-unavailable",
            )
        ],
        "execution_configurations": [make_execution_configuration()],
        "invocations": [
            {
                "invocation_id": "codex-dry-run-plan-v1",
                "configuration_id": "codex-dry-run-v1",
                "platform": "codex",
                "plan_state": "planned",
                "execute": False,
                "executable": "codex",
                "cwd": "<isolated-read-only-fixture-root>",
                "argv": [
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
                    "--disable",
                    "apps",
                    "--disable",
                    "browser_use",
                    "--disable",
                    "browser_use_external",
                    "--disable",
                    "code_mode",
                    "--disable",
                    "code_mode_host",
                    "--disable",
                    "computer_use",
                    "--disable",
                    "goals",
                    "--disable",
                    "image_generation",
                    "--disable",
                    "in_app_browser",
                    "--disable",
                    "memories",
                    "--disable",
                    "multi_agent",
                    "--disable",
                    "plugin_sharing",
                    "--disable",
                    "remote_plugin",
                    "--disable",
                    "shell_tool",
                    "--disable",
                    "skill_mcp_dependency_install",
                    "--disable",
                    "skill_search",
                    "--disable",
                    "tool_suggest",
                    "--disable",
                    "unified_exec",
                    "--disable",
                    "view_image",
                    "--disable",
                    "workspace_dependencies",
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
                ],
                "input_transport": "stdin",
                "stdin_source": "<fixture-prompt>",
                "stdout_format": "jsonl",
                "stderr_policy": "capture",
                "network_policy": "codex-client-network-endpoints-unverified",
                "file_policy": "read-only",
                "expected_cli_invocations": 0,
                "expected_provider_requests": 0,
                "blocker": None,
            }
        ],
        "claims": {
            "quality_comparison": "not-computed",
            "inference": "not-computed",
            "winner": None,
            "ranking": None,
            "promotion_recommendation": None,
        },
    }


def make_card() -> dict:
    return {
        "schema_version": "1",
        "card_id": "codex-unobserved-v1",
        "card_revision": "2026-09-16.1",
        "platform": "codex",
        "execution_configuration": make_execution_configuration(),
        "evidence_state": "unobserved",
        "evidence_basis": "none",
        "state_reason": "unobserved-no-retained-observation",
        "observed_runs": 0,
        "task_shapes": [],
        "outcome_summary": None,
        "batch_binding": {
            "state": "none",
            "batch_id": None,
            "batch_path": None,
            "batch_digest": None,
            "planned_runs": 0,
            "retained_runs": 0,
            "observed_runs": 0,
            "planned_task_shapes": [],
            "retained_task_shapes": [],
            "observed_task_shapes": [],
        },
        "measurements": {
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
        },
        "evidence": [],
        "blockers": ["real-model-request-not-run"],
        "valid_until": None,
        "expired_reason": None,
        "decision": {
            "routing": "undecided",
            "winner": None,
            "ranking": None,
            "promotion_recommendation": None,
        },
    }


def run_validator(flag: str, payload: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "input.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), flag, str(path)],
            capture_output=True,
            text=True,
            check=False,
        )


class CalibrationBatchContractTests(unittest.TestCase):
    def test_repository_dry_run_plan_validates_without_execution(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(VALIDATOR), "--batch", str(PLATFORM_INVOCATIONS)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["execution_mode"], "dry-run-only")
        self.assertEqual(result["planned_invocations"], 2)
        self.assertEqual(result["blocked_invocations"], 1)
        self.assertEqual(result["cli_invocations_budget"], 0)
        self.assertEqual(result["provider_requests_budget"], 0)
        self.assertFalse(result["executed"])

    def test_dry_run_rejects_execution_or_nonzero_request_budget(self) -> None:
        for mutate, expected_error in (
            (
                lambda value: value["invocations"][0].update(execute=True),
                "exactly one CLI invocation",
            ),
            (
                lambda value: value["invocations"][0].update(expected_cli_invocations=1),
                "nonexecuting invocation",
            ),
            (lambda value: value["budget"].update(max_cli_invocations=1), "dry-run-only"),
            (
                lambda value: value["authorization"].update(state="authorized-once"),
                "requires platforms",
            ),
        ):
            with self.subTest(expected_error=expected_error):
                batch = make_batch()
                mutate(batch)
                completed = run_validator("--batch", batch)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)

    def test_platform_plan_requires_codex_and_claude_safety_controls(self) -> None:
        batch = make_batch()
        codex = batch["invocations"][0]
        for required in (
            "--ephemeral",
            "--ignore-user-config",
            "--sandbox",
            "read-only",
            "--ask-for-approval",
            "never",
            "--strict-config",
            "--ignore-rules",
            "--skip-git-repo-check",
            "project_doc_max_bytes=0",
            'web_search="disabled"',
            "shell_tool",
            "--json",
        ):
            with self.subTest(platform="codex", required=required):
                mutated = copy.deepcopy(batch)
                mutated["invocations"][0]["argv"].remove(required)
                completed = run_validator("--batch", mutated)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("codex", completed.stderr)

        wrong_order = make_batch()
        argv = wrong_order["invocations"][0]["argv"]
        approval_index = argv.index("--ask-for-approval")
        approval_pair = argv[approval_index : approval_index + 2]
        del argv[approval_index : approval_index + 2]
        exec_index = argv.index("exec")
        argv[exec_index + 1 : exec_index + 1] = approval_pair
        completed = run_validator("--batch", wrong_order)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("hardened EVAL-10 command template", completed.stderr)

        claude_config = make_execution_configuration("claude-dry-run-v1", "claude-code")
        claude_config.update(
            harness="claude-code",
            client_version="2.1.119",
            profile="calibration-bare-read-only-v1",
            adapter_revision="claude-json-dry-run-v1",
        )
        batch["execution_configurations"] = [claude_config]
        batch["invocations"] = [
            {
                "invocation_id": "claude-dry-run-plan-v1",
                "configuration_id": "claude-dry-run-v1",
                "platform": "claude-code",
                "plan_state": "planned",
                "execute": False,
                "executable": "claude",
                "cwd": "<isolated-read-only-fixture-root>",
                "argv": [
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
                ],
                "input_transport": "stdin",
                "stdin_source": "<fixture-prompt>",
                "stdout_format": "json",
                "stderr_policy": "capture",
                "network_policy": "claude-client-network-endpoints-unverified",
                "file_policy": "read-only",
                "expected_cli_invocations": 0,
                "expected_provider_requests": 0,
                "blocker": None,
            }
        ]
        for required in (
            "--print",
            "--bare",
            "--output-format",
            "json",
            "--no-session-persistence",
            "--no-chrome",
            "--permission-mode",
            "dontAsk",
            "--max-budget-usd",
        ):
            with self.subTest(platform="claude-code", required=required):
                mutated = copy.deepcopy(batch)
                mutated["invocations"][0]["argv"].remove(required)
                completed = run_validator("--batch", mutated)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("claude-code", completed.stderr)

    def test_dsh_requires_blocked_plan_without_internal_bundle_argv(self) -> None:
        batch = make_batch()
        config = make_execution_configuration("dsh-blocked-v1", "deepseek-harness")
        config.update(
            harness="dsh-headless",
            client_version="desktop-2.0.9+dsh-cli-0.1.5-rc.1",
            reasoning=None,
            profile="headless-pending-pinned-profile",
            adapter_revision="not-available",
            binding_state="blocked",
            blocker="Public version-pinned dsh CLI is not available on PATH.",
        )
        invocation = {
            "invocation_id": "dsh-blocked-plan-v1",
            "configuration_id": "dsh-blocked-v1",
            "platform": "deepseek-harness",
            "plan_state": "blocked",
            "execute": False,
            "executable": None,
            "cwd": "<isolated-read-only-fixture-root>",
            "argv": None,
            "input_transport": "not-applicable",
            "stdin_source": None,
            "stdout_format": "not-applicable",
            "stderr_policy": "not-applicable",
            "network_policy": "blocked",
            "file_policy": "read-only",
            "expected_cli_invocations": 0,
            "expected_provider_requests": 0,
            "blocker": "Public version-pinned dsh CLI is not available on PATH.",
        }
        batch["execution_configurations"] = [config]
        batch["invocations"] = [invocation]
        self.assertEqual(run_validator("--batch", batch).returncode, 0)

        for field, value in (
            ("plan_state", "planned"),
            ("execute", True),
            ("executable", "dsh"),
            ("argv", ["dsh", "--profile", "headless", "task"]),
            ("blocker", None),
        ):
            with self.subTest(field=field):
                mutated = copy.deepcopy(batch)
                mutated["invocations"][0][field] = value
                completed = run_validator("--batch", mutated)
                self.assertNotEqual(completed.returncode, 0)
                self.assertTrue(
                    "deepseek-harness" in completed.stderr
                    or "executing invocation" in completed.stderr,
                    completed.stderr,
                )

    def test_batch_fails_closed_on_unknown_fields_duplicate_ids_and_missing_stops(self) -> None:
        mutations = []
        unknown = make_batch()
        unknown["unexpected"] = True
        mutations.append(unknown)
        duplicate = make_batch()
        duplicate["execution_configurations"].append(
            copy.deepcopy(duplicate["execution_configurations"][0])
        )
        mutations.append(duplicate)
        wrong_reference = make_batch()
        wrong_reference["invocations"][0]["configuration_id"] = "missing"
        mutations.append(wrong_reference)
        missing_stop = make_batch()
        missing_stop["stop_conditions"].pop()
        mutations.append(missing_stop)
        for payload in mutations:
            with self.subTest(payload=payload):
                self.assertNotEqual(run_validator("--batch", payload).returncode, 0)

    def test_treatment_is_none_or_one_preregistered_variable(self) -> None:
        invalid = make_batch()
        invalid["treatment"].update(
            mode="single-variable",
            variable="profile",
            baseline="balanced",
            candidate=None,
            comparison_authorized=True,
        )
        completed = run_validator("--batch", invalid)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("treatment", completed.stderr)

    def test_provider_request_budget_may_be_unknown_but_cli_invocations_remain_bounded(self) -> None:
        batch = make_batch()
        batch["budget"]["max_provider_requests"] = None
        batch["invocations"][0]["expected_provider_requests"] = None
        completed = run_validator("--batch", batch)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["cli_invocations_budget"], 0)
        self.assertIsNone(result["provider_requests_budget"])

        batch["invocations"][0]["expected_cli_invocations"] = 1
        completed = run_validator("--batch", batch)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("nonexecuting invocation", completed.stderr)

    def test_blocked_after_preflight_is_a_terminal_nonexecuting_state(self) -> None:
        batch = make_batch()
        batch["execution_mode"] = "authorized-smoke"
        batch["fixture_binding"].update(
            state="bound",
            manifest_path="fixtures/manifest.json",
            manifest_digest=SHA_A,
            task_revision="task-v1",
            fixture_revision="fixture-v1",
            initial_state_digest=SHA_A,
            prompt_digest=SHA_B,
            oracle_revision="oracle-v1",
        )
        batch["data_egress"].update(
            state="fixture-only-authorized",
            allowed_payloads=["synthetic-fixture-prompt"],
        )
        batch["budget"].update(
            max_cli_invocations=0,
            max_provider_requests=None,
            max_wall_clock_seconds=30,
        )
        batch["authorization"].update(
            state="blocked-after-preflight",
            authorized_platforms=["codex"],
            authorization_ref="authorization.md",
            expires_at="2026-09-17T00:00:00+08:00",
        )
        invocation = batch["invocations"][0]
        invocation.update(
            plan_state="blocked",
            execute=False,
            network_policy="blocked",
            expected_cli_invocations=0,
            expected_provider_requests=None,
            blocker="control-digest-drift",
        )

        completed = run_validator("--batch", batch)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["terminal_state"], "blocked-after-preflight")
        self.assertFalse(result["executed"])

    def test_authorized_execution_requires_nonconflicting_model_request_scope(self) -> None:
        batch = make_batch()
        batch["execution_mode"] = "authorized-smoke"
        batch["fixture_binding"].update(
            state="bound",
            manifest_path="fixtures/manifest.json",
            manifest_digest=SHA_A,
            task_revision="task-v1",
            fixture_revision="fixture-v1",
            initial_state_digest=SHA_A,
            prompt_digest=SHA_B,
            oracle_revision="oracle-v1",
        )
        batch["data_egress"].update(
            state="fixture-only-authorized",
            allowed_payloads=["synthetic-fixture-prompt"],
        )
        batch["budget"].update(
            max_cli_invocations=1,
            max_provider_requests=None,
            max_wall_clock_seconds=30,
        )
        batch["authorization"].update(
            state="authorized-once",
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
            authorization_ref="authorization.md",
            expires_at="2026-09-17T00:00:00+08:00",
        )
        batch["execution_configurations"][0].update(
            requested_model="gpt-5.6-sol",
            model_resolution_status="client-catalog-alias",
            permissions_digest=SHA_A,
            toolset_digest=SHA_B,
            binding_state="control-bound",
        )
        batch["invocations"][0].update(
            execute=True,
            expected_cli_invocations=1,
            expected_provider_requests=None,
        )

        completed = run_validator("--batch", batch)
        self.assertEqual(completed.returncode, 0, completed.stderr)

        multiple_cells = copy.deepcopy(batch)
        extra_configuration = copy.deepcopy(
            multiple_cells["execution_configurations"][0]
        )
        extra_configuration["configuration_id"] = "codex-second-smoke-cell"
        multiple_cells["execution_configurations"].append(extra_configuration)
        extra_invocation = copy.deepcopy(multiple_cells["invocations"][0])
        extra_invocation.update(
            invocation_id="codex-second-smoke-invocation",
            configuration_id="codex-second-smoke-cell",
        )
        multiple_cells["invocations"].append(extra_invocation)
        multiple_cells["budget"]["max_cli_invocations"] = 2
        completed = run_validator("--batch", multiple_cells)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("exactly one configuration", completed.stderr)

        missing_allow = copy.deepcopy(batch)
        missing_allow["authorization"]["authorized_actions"] = []
        completed = run_validator("--batch", missing_allow)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("model-request", completed.stderr)

        allow_deny_overlap = copy.deepcopy(batch)
        allow_deny_overlap["authorization"]["forbidden_actions"].append(
            "model-request"
        )
        completed = run_validator("--batch", allow_deny_overlap)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("both authorize and forbid", completed.stderr)

        dry_run_authorizes_model = make_batch()
        dry_run_authorizes_model["authorization"]["authorized_actions"].append(
            "model-request"
        )
        dry_run_authorizes_model["authorization"]["forbidden_actions"].remove(
            "model-request"
        )
        completed = run_validator("--batch", dry_run_authorizes_model)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("cannot authorize model-request", completed.stderr)


class CapabilityCardContractTests(unittest.TestCase):
    def test_repository_cards_validate_with_structured_reason_codes(self) -> None:
        for card_path in sorted((CALIBRATION_DIR / "cards").glob("*.json")):
            with self.subTest(card=card_path.name):
                card = json.loads(card_path.read_text(encoding="utf-8"))
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(VALIDATOR),
                        "--capability-card",
                        str(card_path),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if card["evidence_state"] in (
                    "smoke-only",
                    "provisionally-calibrated",
                ):
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertIn(
                        "observed capability card requires --evidence-root",
                        completed.stderr,
                    )
                else:
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(
                    card["state_reason"], CAPABILITY_STATE_REASON_CODES
                )
                self.assertEqual(
                    card["state_reason"],
                    _derived_state_reason(
                        card["evidence_state"], card["outcome_summary"]
                    ),
                )
                self.assertFalse(
                    set(card["blockers"]) - CAPABILITY_BLOCKER_CODES
                )
                configuration_blocker = card["execution_configuration"]["blocker"]
                if configuration_blocker is not None:
                    self.assertIn(
                        configuration_blocker,
                        EXECUTION_CONFIGURATION_BLOCKER_CODES,
                    )
                if card["expired_reason"] is not None:
                    self.assertIn(card["expired_reason"], EXPIRED_REASON_CODES)
                if card["platform"] == "codex":
                    adapter_digest = hashlib.sha256(CODEX_ADAPTER.read_bytes()).hexdigest()
                    self.assertEqual(
                        card["execution_configuration"]["adapter_revision"],
                        "codex-eval10-v2@sha256:" + adapter_digest,
                    )

    def test_capability_card_schema_reason_codes_match_runtime(self) -> None:
        schema = json.loads(CAPABILITY_CARD_SCHEMA.read_text(encoding="utf-8"))
        definitions = schema["$defs"]
        self.assertEqual(
            set(definitions["stateReasonCode"]["enum"]),
            CAPABILITY_STATE_REASON_CODES,
        )
        self.assertEqual(
            set(definitions["capabilityBlockerCode"]["enum"]),
            CAPABILITY_BLOCKER_CODES,
        )
        self.assertEqual(
            set(definitions["executionConfigurationBlockerCode"]["enum"]),
            EXECUTION_CONFIGURATION_BLOCKER_CODES,
        )
        self.assertEqual(
            {definitions["expiredReasonCode"]["const"]},
            EXPIRED_REASON_CODES,
        )

    def test_smoke_observation_schema_matches_the_runtime_v2_contract(self) -> None:
        schema = json.loads(SMOKE_OBSERVATION_SCHEMA.read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), set(SMOKE_OBSERVATION_FIELDS))
        self.assertEqual(set(schema["properties"]), set(SMOKE_OBSERVATION_FIELDS))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2")
        self.assertEqual(
            schema["properties"]["observation_revision"]["const"],
            "smoke-observation-v2",
        )
        lifecycle = schema["$defs"]["lifecycleBinding"]
        self.assertEqual(
            set(lifecycle["required"]), set(LIFECYCLE_BINDING_FIELDS)
        )

    def test_smoke_summary_schema_matches_the_runtime_contract(self) -> None:
        schema = json.loads(SMOKE_SUMMARY_SCHEMA.read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), set(SMOKE_SUMMARY_FIELDS))
        self.assertEqual(set(schema["properties"]), set(SMOKE_SUMMARY_FIELDS))

    def test_expired_card_is_a_claim_free_tombstone(self) -> None:
        card = make_card()
        card.update(
            evidence_state="expired",
            evidence_basis="expired-tombstone",
            state_reason="expired-claim-free-tombstone",
            expired_reason="evidence-validity-window-elapsed",
            valid_until="2026-09-15",
        )
        completed = run_validator("--capability-card", card)
        self.assertEqual(completed.returncode, 0, completed.stderr)

        fabricated = copy.deepcopy(card)
        fabricated["measurements"]["billed_cost"].update(
            status="provider-billed",
            amount_usd=999,
            receipt_ref="missing/billing.json",
        )
        completed = run_validator("--capability-card", fabricated)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("measurements must remain unknown", completed.stderr)

        future = copy.deepcopy(card)
        future["valid_until"] = "2999-01-01"
        completed = run_validator("--capability-card", future)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("before today", completed.stderr)

    def test_unobserved_card_keeps_all_usage_and_cost_values_unknown(self) -> None:
        completed = run_validator("--capability-card", make_card())
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["evidence_state"], "unobserved")
        self.assertEqual(result["observed_runs"], 0)
        self.assertEqual(result["billed_cost_status"], "unknown")
        self.assertEqual(result["derived_cost_status"], "unknown")

    def test_capability_card_narrative_channels_accept_only_reason_codes(self) -> None:
        mutations = (
            (
                "state_reason",
                lambda card: card.update(
                    state_reason="Codex is the best choice and should ship everywhere."
                ),
                "state_reason",
            ),
            (
                "blockers",
                lambda card: card.update(
                    blockers=["Codex should receive all production traffic."]
                ),
                "blockers contain unsupported reason codes",
            ),
            (
                "execution_configuration.blocker",
                lambda card: card["execution_configuration"].update(
                    binding_state="blocked",
                    blocker="Codex is the preferred production default.",
                ),
                "execution_configuration.blocker must be an allowed reason code",
            ),
            (
                "expired_reason",
                lambda card: card.update(
                    evidence_state="expired",
                    evidence_basis="expired-tombstone",
                    state_reason="expired-claim-free-tombstone",
                    valid_until="2026-09-15",
                    expired_reason="Codex won before this evidence expired.",
                ),
                "expired_reason must be an allowed reason code",
            ),
        )
        for field, mutate, expected_error in mutations:
            with self.subTest(field=field):
                card = make_card()
                mutate(card)
                completed = run_validator("--capability-card", card)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)

    def test_state_reason_code_is_derived_from_evidence_state_and_outcome(self) -> None:
        card = make_card()
        card["state_reason"] = "smoke-only-completed"

        completed = run_validator("--capability-card", card)

        self.assertNotEqual(completed.returncode, 0)
        self.assertIn(
            "state_reason must be derived from evidence_state and outcome_summary",
            completed.stderr,
        )

    def test_unknown_measurements_must_remain_null(self) -> None:
        paths = (
            ("provider_usage", "input_tokens", 1),
            ("derived_usage", "output_tokens", 1),
            ("billed_cost", "amount_usd", 0.01),
            ("derived_cost", "amount_usd", 0.01),
        )
        for section, field, value in paths:
            with self.subTest(section=section, field=field):
                card = make_card()
                card["measurements"][section][field] = value
                completed = run_validator("--capability-card", card)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(section, completed.stderr)

    def test_provider_billed_and_derived_evidence_cannot_be_substituted(self) -> None:
        card = make_card()
        card["measurements"]["billed_cost"].update(
            status="derived-estimate", amount_usd=0.01
        )
        completed = run_validator("--capability-card", card)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("billed_cost", completed.stderr)

        card = make_card()
        card["measurements"]["derived_cost"].update(
            status="provider-billed", amount_usd=0.01
        )
        completed = run_validator("--capability-card", card)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("derived_cost", completed.stderr)

    def test_single_smoke_cannot_claim_provisional_calibration(self) -> None:
        card = make_card()
        card.update(
            evidence_state="provisionally-calibrated",
            evidence_basis="single-smoke",
            state_reason="provisionally-calibrated-completed",
            observed_runs=1,
            task_shapes=["10-instruction-conflict"],
            outcome_summary={
                "completed": 1,
                "failed": 0,
                "stopped": 0,
                "stop_reasons": [],
            },
            batch_binding={
                "state": "receipt-bound",
                "batch_id": "calibration-batch-v1",
                "batch_path": "batches/calibration-batch-v1.json",
                "batch_digest": SHA_A,
                "planned_runs": 1,
                "retained_runs": 1,
                "observed_runs": 1,
                "planned_task_shapes": ["10-instruction-conflict"],
                "retained_task_shapes": ["10-instruction-conflict"],
                "observed_task_shapes": ["10-instruction-conflict"],
            },
            evidence=[{
                "type": "smoke-observation",
                "observation_id": "codex-smoke-v1",
                "path": "runs/codex-smoke/observation.json",
                "digest": SHA_A,
            }],
            blockers=[],
        )
        completed = run_validator("--capability-card", card)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("single-smoke", completed.stderr)

    def test_smoke_only_requires_bound_configuration_and_run_evidence(self) -> None:
        card = make_card()
        card.update(
            evidence_state="smoke-only",
            evidence_basis="single-smoke",
            state_reason="smoke-only-completed",
            observed_runs=1,
            task_shapes=["10-instruction-conflict"],
            outcome_summary={
                "completed": 1,
                "failed": 0,
                "stopped": 0,
                "stop_reasons": [],
            },
            batch_binding={
                "state": "receipt-bound",
                "batch_id": "codex-smoke-batch-v1",
                "batch_path": "batches/codex-smoke-batch-v1.json",
                "batch_digest": SHA_A,
                "planned_runs": 1,
                "retained_runs": 1,
                "observed_runs": 1,
                "planned_task_shapes": ["10-instruction-conflict"],
                "retained_task_shapes": ["10-instruction-conflict"],
                "observed_task_shapes": ["10-instruction-conflict"],
            },
            evidence=[{
                "type": "smoke-observation",
                "observation_id": "codex-smoke-v1",
                "path": "runs/codex-smoke/observation.json",
                "digest": SHA_A,
            }],
            blockers=[],
            valid_until="2026-10-16",
        )
        completed = run_validator("--capability-card", card)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("receipt-bound", completed.stderr)

        card["execution_configuration"].update(
            requested_model="gpt-example-client-catalog-alias",
            resolved_model=None,
            model_resolution_status="client-catalog-alias",
            permissions_digest=SHA_A,
            toolset_digest=SHA_B,
            binding_state="receipt-bound",
        )
        completed = run_validator("--capability-card", card)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("evidence-root", completed.stderr)

    def test_decision_fields_cannot_create_ranking_or_promotion(self) -> None:
        for field, value in (
            ("routing", "codex-default"),
            ("winner", "codex"),
            ("ranking", ["codex", "claude-code"]),
            ("promotion_recommendation", "promote"),
        ):
            with self.subTest(field=field):
                card = make_card()
                card["decision"][field] = value
                completed = run_validator("--capability-card", card)
                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("decision", completed.stderr)

    def test_card_rejects_unknown_fields_and_invalid_digest(self) -> None:
        card = make_card()
        card["unexpected"] = True
        self.assertNotEqual(run_validator("--capability-card", card).returncode, 0)
        card = make_card()
        card["evidence"] = [{
            "type": "smoke-observation",
            "observation_id": "bad",
            "path": "observation.json",
            "digest": "sha256:not-a-digest",
        }]
        self.assertNotEqual(run_validator("--capability-card", card).returncode, 0)

    def test_receipt_bound_configuration_allows_unobserved_provider_id_for_catalog_alias(self) -> None:
        card = make_card()
        configuration = card["execution_configuration"]
        configuration.update(
            requested_model="gpt-5.6-sol",
            resolved_model=None,
            model_resolution_status="client-catalog-alias",
            permissions_digest=SHA_A,
            toolset_digest=SHA_B,
            binding_state="receipt-bound",
        )
        card.update(
            evidence_state="smoke-only",
            evidence_basis="single-smoke",
            state_reason="smoke-only-failed",
            observed_runs=1,
            task_shapes=["10-instruction-conflict"],
            outcome_summary={
                "completed": 0,
                "failed": 1,
                "stopped": 0,
                "stop_reasons": [{"reason": "agent_failed", "count": 1}],
            },
            batch_binding={
                "state": "receipt-bound",
                "batch_id": "codex-smoke-v1",
                "batch_path": "batch.json",
                "batch_digest": SHA_A,
                "planned_runs": 1,
                "retained_runs": 1,
                "observed_runs": 1,
                "planned_task_shapes": ["10-instruction-conflict"],
                "retained_task_shapes": ["10-instruction-conflict"],
                "observed_task_shapes": ["10-instruction-conflict"],
            },
            evidence=[{
                "type": "smoke-observation",
                "observation_id": "codex-smoke-v1",
                "path": "observation.json",
                "digest": SHA_A,
            }],
            valid_until="2026-10-16",
        )
        completed = run_validator("--capability-card", card)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("evidence-root", completed.stderr)

    def test_unobserved_and_blocked_configurations_keep_model_identity_null(self) -> None:
        for mutate in (
            lambda config: config.update(requested_model="gpt-5.6-sol"),
            lambda config: config.update(resolved_model="provider-model-id"),
            lambda config: config.update(model_resolution_status="client-catalog-alias"),
        ):
            card = make_card()
            mutate(card["execution_configuration"])
            completed = run_validator("--capability-card", card)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("model", completed.stderr)

        blocked = make_card()
        blocked["platform"] = "deepseek-harness"
        blocked["execution_configuration"].update(
            platform="deepseek-harness",
            harness="dsh-headless",
            client_version="desktop-2.0.9+dsh-cli-0.1.5-rc.1",
            reasoning=None,
            adapter_revision="not-available",
            binding_state="blocked",
            blocker="public-version-pinned-dsh-cli-not-available-on-path",
        )
        self.assertEqual(run_validator("--capability-card", blocked).returncode, 0)
        blocked["execution_configuration"]["requested_model"] = "deepseek-alias"
        completed = run_validator("--capability-card", blocked)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("model", completed.stderr)

    def test_unobserved_card_cannot_claim_an_outcome(self) -> None:
        card = make_card()
        card["outcome_summary"] = {
            "completed": 0,
            "failed": 1,
            "stopped": 0,
            "stop_reasons": [{"reason": "not-run", "count": 1}],
        }
        completed = run_validator("--capability-card", card)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("outcome", completed.stderr)


if __name__ == "__main__":
    unittest.main()
