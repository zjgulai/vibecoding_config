#!/usr/bin/env python3
"""Validate eleven-task fixture contracts and sha256-tree-v2 state digests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Mapping, Optional, Sequence

from eval_protocol import (
    exact_fields,
    load_json,
    nonblank,
    resolve_relative_without_symlinks,
    safe_relative_posix_path,
    tree_digest_v2,
    validate_digest,
    validate_evidence_scope,
)


TASK_IDS = (
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
)
MANIFEST_SCHEMA_VERSION = "2"
SYNTHETIC_HARNESS_TASK_IDS = ("02-vertical-full-stack-feature",)
TOP_LEVEL_FIELDS = (
    "schema_version",
    "manifest_revision",
    "evidence_scope",
    "digest_contract",
    "fixtures",
)
FIXTURE_FIELDS = (
    "task_id",
    "task_revision",
    "fixture_id",
    "fixture_revision",
    "readiness",
    "root",
    "setup",
    "reset",
    "oracle",
    "artifacts",
    "initial_state_digest",
)
COMMAND_FIELDS = ("command", "expected_exit_code", "timeout_seconds", "success_condition")
ORACLE_FIELDS = ("command", "expected_exit_code", "timeout_seconds", "pass_condition")
ARTIFACT_FIELDS = ("root_template", "required", "forbidden")
ARTIFACT_ITEM_FIELDS = ("path", "kind", "non_empty", "description")
ARTIFACT_ROOT_TEMPLATE = "artifacts/<task-id>/<configuration-revision>/<repetition-index>"
EXPECTED_COMMANDS = {
    "setup": ["./fixture-control", "setup"],
    "reset": ["./fixture-control", "reset"],
    "oracle": ["./fixture-control", "oracle", "--artifacts", "<artifact-root>"],
}
DIGEST_CONTRACT = {
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
}


def _command_contract(value: object, label: str, command_name: str) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("{} must be an object".format(label))
    condition_field = "pass_condition" if command_name == "oracle" else "success_condition"
    fields = ORACLE_FIELDS if command_name == "oracle" else COMMAND_FIELDS
    exact_fields(value, fields, fields, label)
    if value["command"] != EXPECTED_COMMANDS[command_name]:
        raise ValueError(
            "{}.command must use the fixed ./fixture-control {} argv".format(label, command_name)
        )
    if value["expected_exit_code"] != 0 or isinstance(value["expected_exit_code"], bool):
        raise ValueError("{}.expected_exit_code must be 0".format(label))
    timeout = value["timeout_seconds"]
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 3600:
        raise ValueError("{}.timeout_seconds must be an integer from 1 to 3600".format(label))
    nonblank(value[condition_field], "{}.{}".format(label, condition_field))


def _artifact_contract(value: object, label: str) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("{} must be an object".format(label))
    exact_fields(value, ARTIFACT_FIELDS, ARTIFACT_FIELDS, label)
    if value["root_template"] != ARTIFACT_ROOT_TEMPLATE:
        raise ValueError("{}.root_template must use the fixed run isolation template".format(label))

    required = value["required"]
    if not isinstance(required, list) or not required:
        raise ValueError("{}.required must be a non-empty array".format(label))
    required_paths = set()
    for index, artifact in enumerate(required, start=1):
        item_label = "{}.required[{}]".format(label, index)
        if not isinstance(artifact, Mapping):
            raise ValueError("{} must be an object".format(item_label))
        exact_fields(artifact, ARTIFACT_ITEM_FIELDS, ARTIFACT_ITEM_FIELDS, item_label)
        path = safe_relative_posix_path(artifact["path"], "{}.path".format(item_label))
        if path in required_paths:
            raise ValueError("{} contains duplicate artifact path {!r}".format(label, path))
        required_paths.add(path)
        if artifact["kind"] not in ("file", "directory", "glob"):
            raise ValueError("{}.kind must be file, directory, or glob".format(item_label))
        if not isinstance(artifact["non_empty"], bool):
            raise ValueError("{}.non_empty must be boolean".format(item_label))
        nonblank(artifact["description"], "{}.description".format(item_label))

    forbidden = value["forbidden"]
    if not isinstance(forbidden, list) or not forbidden:
        raise ValueError("{}.forbidden must be a non-empty array".format(label))
    forbidden_paths = set()
    for index, path_value in enumerate(forbidden, start=1):
        path = safe_relative_posix_path(
            path_value, "{}.forbidden[{}]".format(label, index)
        )
        if path in forbidden_paths:
            raise ValueError("{} contains duplicate forbidden path {!r}".format(label, path))
        forbidden_paths.add(path)
    overlap = sorted(required_paths & forbidden_paths)
    if overlap:
        raise ValueError("{} requires and forbids the same paths: {}".format(label, ", ".join(overlap)))


def validate_manifest_structure(manifest: Mapping) -> None:
    if not isinstance(manifest, Mapping):
        raise ValueError("fixture manifest must be an object")
    exact_fields(manifest, TOP_LEVEL_FIELDS, TOP_LEVEL_FIELDS, "fixture manifest")
    if manifest["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise ValueError("schema_version must be {!r}".format(MANIFEST_SCHEMA_VERSION))
    nonblank(manifest["manifest_revision"], "manifest_revision")
    evidence_scope = validate_evidence_scope(manifest["evidence_scope"], "evidence_scope")

    digest_contract = manifest["digest_contract"]
    if not isinstance(digest_contract, Mapping):
        raise ValueError("digest_contract must be an object")
    exact_fields(digest_contract, tuple(DIGEST_CONTRACT), tuple(DIGEST_CONTRACT), "digest_contract")
    for field, expected in DIGEST_CONTRACT.items():
        if digest_contract[field] != expected:
            raise ValueError("digest_contract.{} must be {!r}".format(field, expected))

    fixtures = manifest["fixtures"]
    expected_task_ids = (
        TASK_IDS if evidence_scope == "representative" else SYNTHETIC_HARNESS_TASK_IDS
    )
    if not isinstance(fixtures, list) or len(fixtures) != len(expected_task_ids):
        if evidence_scope == "representative":
            raise ValueError("fixtures must contain exactly eleven task contracts")
        raise ValueError(
            "synthetic-harness-only fixtures must contain exactly one EVAL-02 task contract"
        )

    seen_tasks = set()
    seen_fixture_ids = set()
    for index, fixture in enumerate(fixtures, start=1):
        label = "fixtures[{}]".format(index)
        if not isinstance(fixture, Mapping):
            raise ValueError("{} must be an object".format(label))
        exact_fields(fixture, FIXTURE_FIELDS, FIXTURE_FIELDS, label)
        task_id = fixture["task_id"]
        if task_id not in expected_task_ids:
            if evidence_scope == "representative":
                raise ValueError("{}.task_id is not one of the eleven eval tasks".format(label))
            raise ValueError(
                "{}.task_id must be 02-vertical-full-stack-feature for synthetic-harness-only"
                .format(label)
            )
        if task_id in seen_tasks:
            raise ValueError("duplicate task_id {!r}".format(task_id))
        seen_tasks.add(task_id)
        for field in ("task_revision", "fixture_id", "fixture_revision"):
            nonblank(fixture[field], "{}.{}".format(label, field))
        fixture_id = fixture["fixture_id"]
        if fixture_id in seen_fixture_ids:
            raise ValueError("duplicate fixture_id {!r}".format(fixture_id))
        seen_fixture_ids.add(fixture_id)

        readiness = fixture["readiness"]
        if readiness not in ("ready", "contract-only"):
            raise ValueError("{}.readiness must be ready or contract-only".format(label))
        safe_relative_posix_path(fixture["root"], "{}.root".format(label))
        _command_contract(fixture["setup"], "{}.setup".format(label), "setup")
        _command_contract(fixture["reset"], "{}.reset".format(label), "reset")
        _command_contract(fixture["oracle"], "{}.oracle".format(label), "oracle")
        _artifact_contract(fixture["artifacts"], "{}.artifacts".format(label))

        initial_digest = fixture["initial_state_digest"]
        if readiness == "ready":
            validate_digest(initial_digest, "{}.initial_state_digest".format(label), allow_zero=False)
        elif initial_digest is not None:
            raise ValueError("{}.initial_state_digest must be null while contract-only".format(label))

    if seen_tasks != set(expected_task_ids):
        missing = sorted(set(expected_task_ids) - seen_tasks)
        raise ValueError("fixtures missing task_id values: {}".format(", ".join(missing)))


def tree_digest(root: Path) -> str:
    return tree_digest_v2(root)


def fixture_root(manifest_path: Path, fixture: Mapping) -> Path:
    return resolve_relative_without_symlinks(
        manifest_path.resolve().parent,
        fixture["root"],
        "fixture root for {}".format(fixture["fixture_id"]),
    )


def find_fixture(manifest: Mapping, task_id: str, fixture_id: Optional[str] = None) -> Mapping:
    matches = [fixture for fixture in manifest["fixtures"] if fixture["task_id"] == task_id]
    if fixture_id is not None:
        matches = [fixture for fixture in matches if fixture["fixture_id"] == fixture_id]
    if len(matches) != 1:
        raise ValueError("manifest must contain exactly one matching fixture")
    return matches[0]


def validate_ready_fixture(manifest: Mapping, manifest_path: Path, fixture: Mapping) -> Path:
    if fixture["readiness"] != "ready":
        raise ValueError("fixture {!r} is contract-only and cannot run".format(fixture["fixture_id"]))
    root = fixture_root(manifest_path, fixture)
    actual = tree_digest(root)
    if actual != fixture["initial_state_digest"]:
        raise ValueError(
            "initial_state_digest mismatch for {}: expected {}, got {}".format(
                fixture["fixture_id"], fixture["initial_state_digest"], actual
            )
        )
    return root


def validate_manifest(
    manifest: Mapping, manifest_path: Path, allow_contract_only: bool = False
) -> Dict:
    validate_manifest_structure(manifest)
    contract_only = [
        fixture["fixture_id"]
        for fixture in manifest["fixtures"]
        if fixture["readiness"] == "contract-only"
    ]
    if contract_only and not allow_contract_only:
        raise ValueError("contract-only fixtures cannot run: {}".format(", ".join(contract_only)))
    for fixture in manifest["fixtures"]:
        if fixture["readiness"] == "ready":
            validate_ready_fixture(manifest, manifest_path, fixture)
    return {
        "structure_valid": True,
        "tree_contract_valid": not contract_only,
        "contract_only_fixture_count": len(contract_only),
        "fixture_count": len(manifest["fixtures"]),
        "manifest_revision": manifest["manifest_revision"],
        "evidence_scope": manifest["evidence_scope"],
        "digest_algorithm": "sha256-tree-v2",
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate fixture structure/tree contracts or generate sha256-tree-v2 digests."
    )
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument(
        "--allow-contract-only",
        action="store_true",
        help="check declared contract structure without declaring it runnable",
    )
    parser.add_argument("--digest", type=Path, help="print a sha256-tree-v2 digest")
    arguments = parser.parse_args(argv)

    try:
        if arguments.digest is not None:
            if arguments.manifest is not None or arguments.allow_contract_only:
                raise ValueError("--digest cannot be combined with manifest validation options")
            print(tree_digest(arguments.digest))
            return 0
        if arguments.manifest is None:
            raise ValueError("manifest path is required unless --digest is used")
        manifest = load_json(arguments.manifest)
        result = validate_manifest(
            manifest, arguments.manifest, allow_contract_only=arguments.allow_contract_only
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
