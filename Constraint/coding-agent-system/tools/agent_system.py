#!/usr/bin/env python3
"""Safely render, install, and validate the coding-agent configuration kit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlsplit


SYSTEM_ROOT = Path(__file__).resolve().parents[1]
STACK_NAMES = (
    "typescript-nextjs",
    "python-fastapi",
    "postgresql-migrations",
    "frontend-visual-quality",
    "file-document-governance",
)
MODULE_ROUTE_TRIGGERS = {
    "typescript-nextjs": "任务涉及 TypeScript、Next.js、React 或相应前端工具链时读取并遵循",
    "python-fastapi": "任务涉及 Python、FastAPI、Python 测试或相应后端工具链时读取并遵循",
    "postgresql-migrations": "任务涉及 PostgreSQL、数据库 schema、migration、回填或回滚时读取并遵循",
    "frontend-visual-quality": "任务涉及前端视觉实现、响应式布局、可访问性或 UI 质量验收时读取并遵循",
    "file-document-governance": "任务涉及创建、移动、命名、归档或治理文档与项目文件时读取并遵循",
}
SKILL_NAMES = (
    "product-discovery",
    "specification",
    "vertical-ticketing",
    "tdd",
    "systematic-debugging",
    "two-axis-code-review",
    "writing-for-agents",
    "safe-prototyping",
    "project-profile",
    "memory-governance",
    "technical-research",
    "domain-modeling",
    "codebase-design",
    "architecture-review",
    "implementation-orchestration",
)
EXPLICIT_SKILL_NAMES = (
    "product-discovery",
    "specification",
    "vertical-ticketing",
    "project-profile",
    "memory-governance",
    "architecture-review",
    "implementation-orchestration",
)
IGNORED_SOURCE_FILE_NAMES = frozenset({".DS_Store"})
PROJECT_MANIFEST_REVISION = "project-layout-v4"
MODULE_ROUTES_START = "<!-- BEGIN MANAGED MODULE ROUTES -->"
MODULE_ROUTES_END = "<!-- END MANAGED MODULE ROUTES -->"
PROJECT_ROOT_SHADOW_FILES = (
    "AGENTS.override.md",
    "AGENTS.local.md",
    "CLAUDE.md",
    "CLAUDE.local.md",
)
PROJECT_TEMPLATE_FILES = (
    "AGENTS.md",
    ".agents/README.md",
    ".agents/project-profile.md",
    ".agents/memory/README.md",
    ".agents/memory/candidates.jsonl",
    ".agents/controls/README.md",
    ".agents/controls/change-policy.example.json",
    ".agents/controls/check_change_policy.py",
    ".claude/CLAUDE.md",
    ".claude/settings.json",
    ".codex/config.toml",
)
USER_TARGETS = {
    "codex": ("codex", ".codex"),
    "claude": ("claude", ".claude"),
    "deepseek-harness": ("deepseek-harness", ".dsh"),
}

REQUIRED_FILES = (
    "README.md",
    "docs/design.md",
    "docs/implementation-plan.md",
    "docs/installation.md",
    "docs/model-configuration.md",
    "docs/workflow.md",
    "docs/skills-governance.md",
    "docs/sop/project-lifecycle.md",
    "docs/research/deep-research-report.md",
    "docs/research/source-ledger.md",
    "docs/research/local-tip-ledger.md",
    "docs/research/ref-links-ledger.md",
    "docs/research/local-material-audit.md",
    "docs/verification-report.md",
    "report-source.md",
    "evals/README.md",
    "evals/assessment.py",
    "evals/eval_protocol.py",
    "evals/score.py",
    "evals/compare.py",
    "evals/receipt.py",
    "evals/run_lifecycle.py",
    "evals/example-run.json",
    "evals/assessment.schema.json",
    "evals/execution-receipt.schema.json",
    "evals/run-record.schema.json",
    "evals/fixture-manifest.schema.json",
    "evals/fixture-manifest.example.json",
    "evals/validate_fixture.py",
    "evals/test_score.py",
    "evals/test_assessment.py",
    "evals/test_binding.py",
    "evals/test_compare.py",
    "evals/test_fixture_manifest.py",
    "evals/test_lifecycle_runner.py",
    "evals/rubrics/coding-agent-rubric.md",
    "evals/tasks/01-product-discovery.md",
    "evals/tasks/02-vertical-full-stack-feature.md",
    "evals/tasks/03-systematic-debugging.md",
    "evals/tasks/04-postgresql-migration.md",
    "evals/tasks/05-frontend-visual-quality.md",
    "evals/tasks/06-two-axis-review.md",
    "evals/tasks/07-instruction-audit.md",
    "evals/tasks/08-project-profile.md",
    "evals/tasks/09-memory-governance.md",
    "evals/tasks/10-instruction-conflict.md",
    "evals/tasks/11-local-rule-linked-change.md",
    "sources/NOTICE.md",
    "sources/research-methods.lock.json",
    "sources/third-party-skills.lock.json",
    "sources/rule-traceability.json",
    "tools/agent_system.py",
    "tools/tests/test_agent_system.py",
    "templates/shared/user-core.md",
    "templates/shared/project-core.md",
    "templates/user/codex/AGENTS.md",
    "templates/user/codex/config.toml",
    "templates/user/claude/CLAUDE.md",
    "templates/user/claude/settings.json",
    "templates/user/deepseek-harness/AGENTS.md",
    "templates/user/deepseek-harness/README.md",
    "templates/project/AGENTS.md",
    "templates/project/codex/AGENTS.md",
    "templates/project/deepseek-harness/AGENTS.md",
    "templates/project/.claude/CLAUDE.md",
    "templates/project/.claude/settings.json",
    "templates/project/.codex/config.toml",
    "templates/project/.agents/README.md",
    "templates/project/.agents/project-profile.md",
    "templates/project/.agents/memory/README.md",
    "templates/project/.agents/memory/candidates.jsonl",
    "templates/project/.agents/controls/README.md",
    "templates/project/.agents/controls/change-policy.example.json",
    "templates/project/.agents/controls/check_change_policy.py",
    "templates/modules/typescript-nextjs.md",
    "templates/modules/python-fastapi.md",
    "templates/modules/postgresql-migrations.md",
    "templates/modules/frontend-visual-quality.md",
    "templates/modules/file-document-governance.md",
)

SHARED_ADAPTERS = (
    ("templates/shared/user-core.md", "templates/user/codex/AGENTS.md"),
    ("templates/shared/user-core.md", "templates/user/claude/CLAUDE.md"),
    (
        "templates/shared/user-core.md",
        "templates/user/deepseek-harness/AGENTS.md",
    ),
    ("templates/shared/project-core.md", "templates/project/AGENTS.md"),
    (
        "templates/shared/project-core.md",
        "templates/project/codex/AGENTS.md",
    ),
    (
        "templates/shared/project-core.md",
        "templates/project/deepseek-harness/AGENTS.md",
    ),
)

SENSITIVE_FILE_NAMES = {
    ".credentials.yaml",
    "credentials.json",
    "credentials.yaml",
    "id_dsa",
    "id_ed25519",
    "id_ecdsa",
    "id_rsa",
}
SENSITIVE_SUFFIXES = (".key", ".p12", ".pfx", ".pem")
SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"(?im)^\s*[\"']?(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|"
    r"client[_-]?secret|private[_-]?key|refresh[_-]?token|secret[_-]?key|"
    r"secret|token)[\"']?\s*[:=]\s*"
    r"(?P<value>[^#\r\n]+?)\s*$"
)
SENSITIVE_MAPPING_KEY_PATTERN = re.compile(
    r"(?im)(?:^|[.,{\[?&-])\s*[\"']?[A-Za-z0-9_-]*(?:api[_-]?key|access[_-]?token|"
    r"auth[_-]?token|authorization|proxy[_-]?authorization|password|client[_-]?secret|private[_-]?key|"
    r"refresh[_-]?token|secret[_-]?key|credentials?|secret|token)[\"']?\s*[:=]"
)
SENSITIVE_JSON_KEYS = {
    "apikey",
    "accesstoken",
    "authtoken",
    "authorization",
    "clientsecret",
    "password",
    "privatekey",
    "refreshtoken",
    "secret",
    "secretkey",
    "token",
    "credential",
    "credentials",
    "proxyauthorization",
}
DECLARED_TEMPLATE_FILES = frozenset(
    relative for relative in REQUIRED_FILES if relative.startswith("templates/")
)
DECLARED_SKILL_FILES = frozenset(
    relative
    for skill_name in SKILL_NAMES
    for relative in (
        "skills/{}/SKILL.md".format(skill_name),
        "skills/{}/agents/openai.yaml".format(skill_name),
    )
)
DECLARED_SOURCE_FILES = DECLARED_TEMPLATE_FILES | DECLARED_SKILL_FILES
SKILL_SUPPORT_DIRECTORIES = frozenset({"references", "scripts", "assets"})
PROFILE_SECTIONS = (
    "业务与安全不变量",
    "权威修改入口",
    "联动关系",
    "Do NOT 与受保护区域",
    "精确 Definition of Done",
    "权威资料与冲突顺序",
    "局部风险",
)
PROJECT_PROFILE_SECTIONS = PROFILE_SECTIONS
PROFILE_CORE_SECTIONS = frozenset(
    {
        "业务与安全不变量",
        "权威修改入口",
        "精确 Definition of Done",
        "权威资料与冲突顺序",
    }
)
CHANGE_POLICY_FIELDS = frozenset(
    {"schema_version", "protected_paths", "linked_change_groups"}
)
MEMORY_CANDIDATE_FIELDS = frozenset(
    {
        "id",
        "observation",
        "evidence",
        "scope",
        "destination",
        "conflicts_and_risks",
        "expiry_signal",
        "status",
    }
)
TRACEABILITY_FIELDS = frozenset(
    {
        "id",
        "principle",
        "sources",
        "decision",
        "destination",
        "artifacts",
        "eval_cases",
        "status",
        "expiry_signal",
    }
)
TASK_EVAL_IDS = frozenset("EVAL-{:02d}".format(index) for index in range(1, 12))
PLANNED_EVAL_MEANING = {
    "EVAL-07": "instruction audit",
    "EVAL-08": "project profile",
    "EVAL-09": "memory governance",
    "EVAL-10": "instruction conflict and prompt injection",
    "EVAL-11": "local rule and linked change",
}
APPROVED_EVAL_IDS = TASK_EVAL_IDS | frozenset(PLANNED_EVAL_MEANING)


class SafetyError(RuntimeError):
    """Raised when an operation would overwrite or escape its declared scope."""


@dataclass(frozen=True)
class PlannedFile:
    source: Path
    destination: Path
    display_path: str
    content: Optional[bytes] = None


@dataclass(frozen=True)
class OperationResult:
    planned_paths: Tuple[str, ...]
    applied: bool
    backup_paths: Tuple[str, ...] = ()
    destination_paths: Tuple[str, ...] = ()


def _is_sensitive_relative_path(relative: Path) -> bool:
    for part in relative.parts:
        lowered = part.lower()
        if lowered == ".env" or lowered.startswith(".env."):
            return True
        if lowered == "secrets" or lowered in SENSITIVE_FILE_NAMES:
            return True
        if lowered.endswith(SENSITIVE_SUFFIXES):
            return True
    return False


def _contains_secret_assignment(text: str) -> bool:
    if (
        SECRET_ASSIGNMENT_PATTERN.search(text) is not None
        or SENSITIVE_MAPPING_KEY_PATTERN.search(text) is not None
        or "-----BEGIN PRIVATE KEY-----" in text
        or "-----BEGIN RSA PRIVATE KEY-----" in text
        or "-----BEGIN OPENSSH PRIVATE KEY-----" in text
    ):
        return True
    try:
        parsed_json = json.loads(
            text, object_pairs_hook=_reject_duplicate_json_keys
        )
    except (json.JSONDecodeError, TypeError, ValueError):
        parsed_json = None
    if _contains_sensitive_mapping_key(parsed_json):
        return True

    # TOML quoted keys can hide sensitive names behind Unicode escapes, so a
    # semantic parse is required whenever the runtime provides tomllib. On
    # Python < 3.11 the deliberately narrow fallback rejects quoted/dotted TOML
    # before any source can be installed.
    try:
        parsed_toml = _parse_declared_toml_text(text)
    except (TypeError, ValueError):
        return False
    return _contains_sensitive_mapping_key(parsed_toml)


def _contains_sensitive_mapping_key(value: object) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())
            if any(
                normalized == sensitive or normalized.endswith(sensitive)
                for sensitive in SENSITIVE_JSON_KEYS
            ):
                return True
            if _contains_sensitive_mapping_key(nested):
                return True
    elif isinstance(value, list):
        return any(_contains_sensitive_mapping_key(item) for item in value)
    return False


def _reject_duplicate_json_keys(pairs: Iterable[Tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {!r}".format(key))
        result[key] = value
    return result


def _load_strict_json_text(text: str) -> object:
    return json.loads(
        text,
        object_pairs_hook=_reject_duplicate_json_keys,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError("invalid JSON numeric constant: {}".format(value))
        ),
    )


def _validate_repo_relative_path(value: object) -> str:
    """Accept only portable POSIX repository-relative paths."""

    if not isinstance(value, str) or not value:
        raise ValueError("path must be a non-empty string")
    if value.startswith("/"):
        raise ValueError("path must be relative")
    if "\\" in value:
        raise ValueError("path must not contain backslash")
    if ":" in value:
        raise ValueError("path must not contain colon")
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in value):
        raise ValueError("path must not contain control characters")
    segments = value.split("/")
    if any(segment == "" for segment in segments):
        raise ValueError("path must not contain empty segments")
    if any(segment in (".", "..") for segment in segments):
        raise ValueError("path must not contain parent or current-directory segments")
    return value


def _validate_change_policy_file(path: Path) -> Tuple[List[str], List[List[str]]]:
    """Load one policy using the same strict schema as the standalone checker."""

    try:
        _reject_symlink_ancestors(path, "Policy")
        value = _load_strict_json_text(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, SafetyError) as error:
        raise ValueError("invalid policy: {}".format(error))
    if not isinstance(value, dict) or set(value) != CHANGE_POLICY_FIELDS:
        raise ValueError("policy has unexpected fields")
    if value["schema_version"] != "1":
        raise ValueError("unsupported schema_version")
    protected = value["protected_paths"]
    groups = value["linked_change_groups"]
    if not isinstance(protected, list) or not isinstance(groups, list):
        raise ValueError("policy paths must be lists")
    normalized_protected = [_validate_repo_relative_path(item) for item in protected]
    if len(set(normalized_protected)) != len(normalized_protected):
        raise ValueError("policy contains duplicate paths")
    seen_paths = set(normalized_protected)
    normalized_groups: List[List[str]] = []
    for group in groups:
        if not isinstance(group, list) or len(group) < 2:
            raise ValueError("linked group must contain at least two paths")
        normalized = [_validate_repo_relative_path(item) for item in group]
        if len(set(normalized)) != len(normalized):
            raise ValueError("linked group contains duplicate paths")
        if seen_paths.intersection(normalized):
            raise ValueError("policy contains duplicate paths")
        seen_paths.update(normalized)
        normalized_groups.append(normalized)
    return normalized_protected, normalized_groups


def _absolute_path(path: Path) -> Path:
    """Return a lexical absolute path without following symlinks."""

    return Path(os.path.abspath(os.fspath(path)))


def _canonical_scope_path(path: Path, label: str) -> Path:
    """Resolve the deepest existing ancestor, preserving only missing suffix parts."""

    absolute = _absolute_path(path)
    if absolute.is_symlink():
        raise SafetyError("{} must not be a symlink: {}".format(label, absolute))
    current = absolute
    missing_parts = []
    while not os.path.lexists(str(current)) and current != current.parent:
        missing_parts.append(current.name)
        current = current.parent
    try:
        resolved = current.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise SafetyError("{} cannot be resolved safely: {}".format(label, error))
    for part in reversed(missing_parts):
        resolved = resolved / part
    return resolved


def _reject_symlink_ancestors(path: Path, label: str) -> None:
    """Reject every existing symlink component in one lexical absolute path."""

    absolute = _absolute_path(path)
    current = Path(absolute.anchor)
    anchor_parts = len(current.parts)
    for part in absolute.parts[anchor_parts:]:
        current = current / part
        if current.is_symlink():
            if current == absolute:
                raise SafetyError("{} must not be a symlink: {}".format(label, current))
            raise SafetyError("{} traverses a symlink ancestor: {}".format(label, current))
        if (
            current != absolute
            and os.path.lexists(str(current))
            and not current.is_dir()
        ):
            raise SafetyError("{} ancestor is not a directory: {}".format(label, current))


def _relative_path_within(root: Path, path: Path, label: str) -> Path:
    absolute_root = _absolute_path(root)
    absolute_path = _absolute_path(path)
    try:
        return absolute_path.relative_to(absolute_root)
    except ValueError:
        raise SafetyError("{} escapes its declared root: {}".format(label, path))


def _ensure_no_symlink_components(root: Path, path: Path, label: str) -> None:
    absolute_root = _absolute_path(root)
    relative = _relative_path_within(absolute_root, path, label)
    current = absolute_root
    if current.is_symlink():
        raise SafetyError("{} root must not be a symlink: {}".format(label, current))
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise SafetyError("{} traverses a symlink: {}".format(label, current))
    resolved_root = absolute_root.resolve(strict=False)
    resolved_path = _absolute_path(path).resolve(strict=False)
    if resolved_path != resolved_root and resolved_root not in resolved_path.parents:
        raise SafetyError("{} resolves outside its declared root: {}".format(label, path))


def _require_valid_system(system_root: Path) -> None:
    issues = validate_system(system_root)
    if issues:
        preview = "; ".join(issues[:8])
        if len(issues) > 8:
            preview += "; and {} more issue(s)".format(len(issues) - 8)
        raise SafetyError("System validation failed: {}".format(preview))


def _require_declared_source_trees(system_root: Path) -> None:
    issues, _unsafe_entry = _validate_declared_source_trees(system_root)
    if issues:
        preview = "; ".join(issues[:8])
        if len(issues) > 8:
            preview += "; and {} more issue(s)".format(len(issues) - 8)
        raise SafetyError("Source tree validation failed: {}".format(preview))


def _skill_relative_file_kind(relative: Path) -> Optional[str]:
    """Classify one file inside a Skill, rejecting undeclared locations."""

    parts = relative.parts
    if parts == ("SKILL.md",) or parts == ("agents", "openai.yaml"):
        return "instruction"
    if len(parts) >= 2 and parts[0] in SKILL_SUPPORT_DIRECTORIES:
        return "asset" if parts[0] == "assets" else "instruction"
    return None


def _skill_relative_directory_is_allowed(relative: Path) -> bool:
    parts = relative.parts
    if parts == ("agents",):
        return True
    return bool(parts) and parts[0] in SKILL_SUPPORT_DIRECTORIES


def _declared_skill_source_kind(relative_text: str) -> Optional[str]:
    relative = Path(relative_text)
    if len(relative.parts) < 3 or relative.parts[0] != "skills":
        return None
    if relative.parts[1] not in SKILL_NAMES:
        return None
    return _skill_relative_file_kind(Path(*relative.parts[2:]))


def _source_file_kind(relative_text: str) -> Optional[str]:
    if relative_text in DECLARED_TEMPLATE_FILES:
        return "instruction"
    return _declared_skill_source_kind(relative_text)


def _ensure_declared_source_root(system_root: Path, source_root: Path) -> None:
    _ensure_no_symlink_components(system_root, source_root, "Source root")
    if not source_root.is_dir():
        raise SafetyError("Missing template directory: {}".format(source_root))


def _ensure_regular_source(system_root: Path, path: Path) -> None:
    _ensure_no_symlink_components(system_root, path, "Source")
    if not path.is_file():
        raise SafetyError("Source is not a regular file: {}".format(path))
    relative = _absolute_path(path).relative_to(_absolute_path(system_root)).as_posix()
    if _source_file_kind(relative) is None:
        raise SafetyError("Refusing undeclared source file: {}".format(relative))


def _collect_tree(
    system_root: Path,
    source_root: Path,
    destination_root: Path,
    display_prefix: Path = Path(),
) -> List[PlannedFile]:
    _ensure_declared_source_root(system_root, source_root)
    operations: List[PlannedFile] = []
    for source in sorted(source_root.rglob("*")):
        if (
            source.name in IGNORED_SOURCE_FILE_NAMES
            and source.is_file()
            and not source.is_symlink()
        ):
            continue
        if source.is_symlink():
            _ensure_regular_source(system_root, source)
        if source.is_dir():
            continue
        relative = source.relative_to(source_root)
        if _is_sensitive_relative_path(relative):
            raise SafetyError("Refusing sensitive source path: {}".format(source))
        _ensure_regular_source(system_root, source)
        display = (display_prefix / relative).as_posix()
        operations.append(
            PlannedFile(
                source=source,
                destination=destination_root / relative,
                display_path=display,
            )
        )
    return operations


def _skill_uses_explicit_invocation(skill_file: Path) -> bool:
    """Return whether canonical frontmatter marks a skill as explicit-only."""

    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(?P<frontmatter>.*?)\n---(?:\s*\n|\Z)", text, re.DOTALL)
    if match is None:
        raise SafetyError("Invalid skill frontmatter: {}".format(skill_file))
    frontmatter = match.group("frontmatter")
    return re.search(
        r"(?m)^metadata:\s*$\n(?:^[ \t]+.*\n)*?^[ \t]+invocation:\s*[\"']?explicit-only[\"']?\s*$",
        frontmatter + "\n",
    ) is not None


def _render_explicit_skill_variant(skill_file: Path) -> bytes:
    """Add the Claude/DSH top-level explicit invocation control."""

    text = skill_file.read_text(encoding="utf-8")
    frontmatter_match = re.match(
        r"\A---\s*\n(?P<frontmatter>.*?)\n---(?:\s*\n|\Z)",
        text,
        re.DOTALL,
    )
    if frontmatter_match is None:
        raise SafetyError("Invalid skill frontmatter: {}".format(skill_file))
    if re.search(
        r"(?m)^disable-model-invocation:\s*true\s*$",
        frontmatter_match.group("frontmatter"),
    ):
        return text.encode("utf-8")
    lines = text.splitlines(keepends=True)
    closing_index = next(
        (
            index
            for index in range(1, len(lines))
            if lines[index].strip() == "---"
        ),
        None,
    )
    if closing_index is None:
        raise SafetyError("Invalid skill frontmatter: {}".format(skill_file))
    newline = "\r\n" if lines[0].endswith("\r\n") else "\n"
    lines.insert(closing_index, "disable-model-invocation: true" + newline)
    return "".join(lines).encode("utf-8")


def _collect_platform_skill_adapters(
    system_root: Path,
    skills_root: Path,
    destination_root: Path,
    display_prefix: Path,
    explicit_only: bool,
) -> List[PlannedFile]:
    """Render portable skill copies while keeping Codex canonical files valid."""

    _ensure_declared_source_root(system_root, skills_root)
    operations: List[PlannedFile] = []
    for skill_dir in sorted(skills_root.iterdir()):
        if (
            skill_dir.name in IGNORED_SOURCE_FILE_NAMES
            and skill_dir.is_file()
            and not skill_dir.is_symlink()
        ):
            continue
        if skill_dir.is_symlink() or not skill_dir.is_dir():
            raise SafetyError("Skill root contains an unsupported entry: {}".format(skill_dir))
        _ensure_declared_source_root(system_root, skill_dir)
        skill_file = skill_dir / "SKILL.md"
        _ensure_regular_source(system_root, skill_file)
        is_explicit = _skill_uses_explicit_invocation(skill_file)
        if explicit_only and not is_explicit:
            continue
        for source in sorted(skill_dir.rglob("*")):
            if (
                source.name in IGNORED_SOURCE_FILE_NAMES
                and source.is_file()
                and not source.is_symlink()
            ):
                continue
            if source.is_symlink():
                _ensure_regular_source(system_root, source)
            if source.is_dir():
                continue
            _ensure_regular_source(system_root, source)
            relative_in_skill = source.relative_to(skill_dir)
            if _is_sensitive_relative_path(relative_in_skill):
                raise SafetyError(
                    "Refusing sensitive source path: {}".format(source)
                )
            if relative_in_skill.parts[0] == "agents":
                continue
            relative = Path(skill_dir.name) / relative_in_skill
            content = (
                _render_explicit_skill_variant(source)
                if source == skill_file and is_explicit
                else None
            )
            operations.append(
                PlannedFile(
                    source=source,
                    destination=destination_root / relative,
                    display_path=(display_prefix / relative).as_posix(),
                    content=content,
                )
            )
    return operations


def _deduplicate_operations(operations: Iterable[PlannedFile]) -> List[PlannedFile]:
    result: List[PlannedFile] = []
    destinations = set()
    for operation in operations:
        key = str(_absolute_path(operation.destination))
        if key in destinations:
            raise SafetyError(
                "Multiple sources target the same file: {}".format(
                    operation.destination
                )
            )
        destinations.add(key)
        result.append(operation)
    return sorted(result, key=lambda item: item.display_path)


def _destination_must_be_empty(destination: Path) -> None:
    _reject_symlink_ancestors(destination, "Destination")
    current = destination.parent
    while not os.path.lexists(str(current)) and current != current.parent:
        current = current.parent
    if not current.is_dir():
        raise SafetyError(
            "Destination parent is not a directory: {}".format(current)
        )
    if destination.is_symlink():
        raise SafetyError("Destination must not be a symlink: {}".format(destination))
    if destination.exists() and not destination.is_dir():
        raise SafetyError("Destination is not a directory: {}".format(destination))
    if destination.is_dir() and next(destination.iterdir(), None) is not None:
        raise SafetyError("Destination must be empty: {}".format(destination))


def _stream_file_size_and_digest(path: Path) -> Tuple[int, str]:
    size = 0
    digest = hashlib.sha256()
    with path.open("rb", buffering=0) as stream:
        while True:
            chunk = stream.read(64 * 1024)
            if not chunk:
                return size, digest.hexdigest()
            size += len(chunk)
            digest.update(chunk)


def _atomic_install(operation: PlannedFile) -> None:
    """Stream verified bytes through a neutral same-directory temporary name."""

    destination = operation.destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=".agent-write-", dir=str(destination.parent)
    )
    temporary = Path(temporary_name)
    expected_size = 0
    expected_digest = hashlib.sha256()

    def write_chunk(stream, chunk: bytes) -> None:
        view = memoryview(chunk)
        while view:
            written = stream.write(view)
            if written is None or written <= 0:
                raise OSError("short write while installing {}".format(destination))
            view = view[written:]

    try:
        with os.fdopen(file_descriptor, "wb", buffering=0) as output:
            if operation.content is None:
                with operation.source.open("rb", buffering=0) as source:
                    while True:
                        chunk = source.read(64 * 1024)
                        if not chunk:
                            break
                        write_chunk(output, chunk)
                        expected_size += len(chunk)
                        expected_digest.update(chunk)
            else:
                write_chunk(output, operation.content)
                expected_size = len(operation.content)
                expected_digest.update(operation.content)
            output.flush()
            os.fsync(output.fileno())
        shutil.copymode(str(operation.source), str(temporary))
        actual_size, actual_digest = _stream_file_size_and_digest(temporary)
        if (
            actual_size != expected_size
            or actual_digest != expected_digest.hexdigest()
        ):
            raise SafetyError(
                "Generated file content verification failed: {}".format(destination)
            )
        if sys.platform == "darwin":
            try:
                subprocess.run(
                    [
                        "/bin/mv",
                        "-f",
                        "--",
                        str(temporary),
                        str(destination),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                )
            except (OSError, subprocess.CalledProcessError) as error:
                raise SafetyError(
                    "Atomic move failed for generated file: {}".format(destination)
                ) from error
        else:
            os.replace(str(temporary), str(destination))
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def _apply_new_tree(destination: Path, operations: Sequence[PlannedFile]) -> None:
    _destination_must_be_empty(destination)
    destination_parent = destination.parent
    destination_parent.mkdir(parents=True, exist_ok=True)
    stage = Path(
        tempfile.mkdtemp(
            prefix=".{}-agent-init-".format(destination.name),
            dir=str(destination_parent),
        )
    )
    try:
        for operation in operations:
            relative = operation.destination.relative_to(destination)
            staged_destination = stage / relative
            _atomic_install(
                PlannedFile(
                    source=operation.source,
                    destination=staged_destination,
                    display_path=operation.display_path,
                    content=operation.content,
                )
            )
        if destination.exists():
            destination.rmdir()
        os.replace(str(stage), str(destination))
    except Exception:
        if stage.exists():
            shutil.rmtree(str(stage))
        raise


def _render_managed_module_routes(template_file: Path, stacks: Sequence[str]) -> bytes:
    """Render the root-owned route block without disturbing template-owned text."""

    text = template_file.read_text(encoding="utf-8")
    start_count = text.count(MODULE_ROUTES_START)
    end_count = text.count(MODULE_ROUTES_END)
    if (start_count, end_count) not in ((0, 0), (1, 1)):
        raise SafetyError(
            "Project AGENTS.md must contain zero or one complete managed module route block"
        )

    selected = sorted(set(stacks))
    lines = [MODULE_ROUTES_START]
    if selected:
        lines.append("平台不会自动加载任意 `.agents/rules/` 文件；命中下列条件时必须显式读取对应模块：")
        lines.append("")
        for stack in selected:
            lines.append(
                "- `.agents/rules/{}.md` — {}。".format(
                    stack, MODULE_ROUTE_TRIGGERS[stack]
                )
            )
    else:
        lines.append("当前未选择项目模块；不要读取未生成的模块文件。")
    lines.append(MODULE_ROUTES_END)
    block = "\n".join(lines)

    if start_count == 0:
        separator = "" if not text or text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
        return (text + separator + block + "\n").encode("utf-8")
    start = text.index(MODULE_ROUTES_START)
    end_start = text.find(MODULE_ROUTES_END, start)
    if end_start < start:
        raise SafetyError(
            "Project AGENTS.md managed module route markers are reversed"
        )
    end = end_start + len(MODULE_ROUTES_END)
    return (text[:start] + block + text[end:]).encode("utf-8")


def init_project(
    system_root: Path,
    destination: Path,
    stacks: Sequence[str],
    apply_changes: bool = False,
) -> OperationResult:
    """Plan or create a project configuration in an empty destination."""

    system_root = _absolute_path(Path(system_root))
    destination = _canonical_scope_path(Path(destination), "Destination")
    _require_valid_system(system_root)
    _destination_must_be_empty(destination)

    unknown_stacks = sorted(set(stacks) - set(STACK_NAMES))
    if unknown_stacks:
        raise SafetyError("Unknown stack module(s): {}".format(", ".join(unknown_stacks)))

    operations: List[PlannedFile] = []
    project_template_root = system_root / "templates/project"
    _ensure_declared_source_root(system_root, project_template_root)
    for relative_text in PROJECT_TEMPLATE_FILES:
        relative = Path(relative_text)
        source = project_template_root / relative
        _ensure_regular_source(system_root, source)
        operations.append(
            PlannedFile(
                source=source,
                destination=destination / relative,
                display_path=relative.as_posix(),
                content=(
                    _render_managed_module_routes(source, stacks)
                    if relative == Path("AGENTS.md")
                    else None
                ),
            )
        )
    manifest_relative = Path(".agents/generated-manifest.json")
    manifest_source = system_root / "templates/project/.agents/README.md"
    operations.append(
        PlannedFile(
            source=manifest_source,
            destination=destination / manifest_relative,
            display_path=manifest_relative.as_posix(),
            content=(
                json.dumps(
                    {
                        "schema_version": "1",
                        "generator_revision": PROJECT_MANIFEST_REVISION,
                        "stacks": sorted(set(stacks)),
                    },
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8"),
        )
    )
    for stack in sorted(set(stacks)):
        source = system_root / "templates/modules/{}.md".format(stack)
        _ensure_regular_source(system_root, source)
        relative = Path(".agents/rules") / source.name
        operations.append(
            PlannedFile(source, destination / relative, relative.as_posix())
        )

    skills_root = system_root / "skills"
    if skills_root.is_dir():
        operations.extend(
            _collect_tree(
                system_root,
                skills_root,
                destination / ".agents/skills",
                Path(".agents/skills"),
            )
        )
        operations.extend(
            _collect_platform_skill_adapters(
                system_root,
                skills_root,
                destination / ".claude/skills",
                Path(".claude/skills"),
                explicit_only=False,
            )
        )
        operations.extend(
            _collect_platform_skill_adapters(
                system_root,
                skills_root,
                destination / ".dsh/skills",
                Path(".dsh/skills"),
                explicit_only=True,
            )
        )

    operations = _deduplicate_operations(operations)
    if apply_changes:
        _apply_new_tree(destination, operations)
    return OperationResult(
        planned_paths=tuple(item.display_path for item in operations),
        applied=apply_changes,
        destination_paths=tuple(str(item.destination) for item in operations),
    )


def _validate_user_destinations(home: Path, operations: Sequence[PlannedFile]) -> None:
    """Reject symlink traversal and destinations outside the selected home."""

    _reject_symlink_ancestors(home, "User home")
    if home.is_symlink():
        raise SafetyError("User home must not be a symlink: {}".format(home))
    existing_ancestor = home
    while (
        not os.path.lexists(str(existing_ancestor))
        and existing_ancestor != existing_ancestor.parent
    ):
        existing_ancestor = existing_ancestor.parent
    if not existing_ancestor.is_dir():
        raise SafetyError(
            "User home ancestor is not a directory: {}".format(
                existing_ancestor
            )
        )
    resolved_home = home.resolve(strict=False)
    for operation in operations:
        try:
            relative = operation.destination.relative_to(home)
        except ValueError:
            raise SafetyError(
                "User destination escapes the selected home: {}".format(
                    operation.destination
                )
            )
        current = home
        for part in relative.parts:
            current = current / part
            if current.is_symlink():
                raise SafetyError(
                    "User destination traverses a symlink: {}".format(current)
                )
        resolved_parent = operation.destination.parent.resolve(strict=False)
        if resolved_parent != resolved_home and resolved_home not in resolved_parent.parents:
            raise SafetyError(
                "User destination resolves outside the selected home: {}".format(
                    operation.destination
                )
            )


def _validate_new_backup_root(home: Path, backup_root: Path) -> None:
    """Require a new, non-symlink backup root outside managed target trees."""

    lexical_home = _absolute_path(home)
    lexical_backup = _absolute_path(backup_root)
    if os.path.lexists(str(backup_root)):
        if backup_root.is_symlink():
            raise SafetyError(
                "Backup root must not be a symlink: {}".format(backup_root)
            )
        raise SafetyError(
            "Backup root must be a new path: {}".format(backup_root)
        )

    current = Path(lexical_backup.anchor)
    anchor_parts = len(current.parts)
    for part in lexical_backup.parent.parts[anchor_parts:]:
        current = current / part
        if current.is_symlink():
            raise SafetyError(
                "Backup root traverses a symlink ancestor: {}".format(current)
            )
        if os.path.lexists(str(current)) and not current.is_dir():
            raise SafetyError("Backup parent is not a directory: {}".format(current))

    resolved_backup = lexical_backup.resolve(strict=False)
    for managed_name in (".codex", ".claude", ".dsh", ".agents"):
        lexical_managed = lexical_home / managed_name
        resolved_managed = lexical_managed.resolve(strict=False)
        lexically_inside = (
            lexical_backup == lexical_managed
            or lexical_managed in lexical_backup.parents
        )
        resolves_inside = (
            resolved_backup == resolved_managed
            or resolved_managed in resolved_backup.parents
        )
        if lexically_inside or resolves_inside:
            raise SafetyError(
                "Backup root must be outside managed user directories: {}".format(
                    backup_root
                )
            )


def _validate_backup_input_route(home: Path, lexical_backup: Path) -> None:
    """Reject a backup path whose resolution route enters a managed user tree."""

    canonical_home = _absolute_path(home)
    managed_roots = tuple(
        (canonical_home / name).resolve(strict=False)
        for name in (".codex", ".claude", ".dsh", ".agents")
    )

    def reject_if_managed(candidate: Path) -> None:
        for managed in managed_roots:
            if candidate == managed or managed in candidate.parents:
                raise SafetyError(
                    "Backup root resolution route enters managed user directory: {}".format(
                        lexical_backup
                    )
                )

    absolute_backup = _absolute_path(lexical_backup)
    current = Path(absolute_backup.anchor)
    try:
        resolved_parent = current.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise SafetyError("Backup root cannot be resolved safely: {}".format(error))
    anchor_parts = len(current.parts)
    for part in absolute_backup.parts[anchor_parts:]:
        current = current / part
        # Check the directory entry location before following a symlink, then
        # check the resolved prefix. This catches alias -> home -> .codex ->
        # outside routes without forbidding aliases that stay wholly outside.
        reject_if_managed(resolved_parent / part)
        try:
            resolved_current = current.resolve(strict=False)
        except (OSError, RuntimeError) as error:
            raise SafetyError("Backup root cannot be resolved safely: {}".format(error))
        reject_if_managed(resolved_current)
        resolved_parent = resolved_current


def _validate_backup_target(backup_root: Path, backup_path: Path) -> None:
    try:
        relative = backup_path.relative_to(backup_root)
    except ValueError:
        raise SafetyError("Backup path escapes backup root: {}".format(backup_path))
    current = backup_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise SafetyError(
                "Backup path traverses a symlink: {}".format(current)
            )
        if current != backup_path and current.exists() and not current.is_dir():
            raise SafetyError(
                "Backup parent is not a directory: {}".format(current)
            )
    if os.path.lexists(str(backup_path)):
        raise SafetyError(
            "Backup destination already exists: {}".format(backup_path)
        )


def install_user(
    system_root: Path,
    target: str,
    home_dir: Optional[Path] = None,
    backup_dir: Optional[Path] = None,
    apply_changes: bool = False,
) -> OperationResult:
    """Plan or install user templates without silently overwriting files."""

    system_root = _absolute_path(Path(system_root))
    requested_home = _absolute_path(
        Path(home_dir) if home_dir is not None else Path.home()
    )
    home = _canonical_scope_path(requested_home, "User home")
    _require_valid_system(system_root)
    selected = tuple(USER_TARGETS) if target == "all" else (target,)
    unknown = sorted(set(selected) - set(USER_TARGETS))
    if unknown:
        raise SafetyError("Unknown user target(s): {}".format(", ".join(unknown)))

    operations: List[PlannedFile] = []
    for selected_target in selected:
        template_name, home_name = USER_TARGETS[selected_target]
        operations.extend(
            _collect_tree(
                system_root,
                system_root / "templates/user" / template_name,
                home / home_name,
                Path(selected_target),
            )
        )

    skills_root = system_root / "skills"
    if skills_root.is_dir():
        if "codex" in selected or "deepseek-harness" in selected:
            operations.extend(
                _collect_tree(
                    system_root,
                    skills_root,
                    home / ".agents/skills",
                    Path("shared-skills"),
                )
            )
        if "claude" in selected:
            operations.extend(
                _collect_platform_skill_adapters(
                    system_root,
                    skills_root,
                    home / ".claude/skills",
                    Path("claude-skills"),
                    explicit_only=False,
                )
            )
        if "codex" in selected or "deepseek-harness" in selected:
            operations.extend(
                _collect_platform_skill_adapters(
                    system_root,
                    skills_root,
                    home / ".dsh/skills",
                    Path("deepseek-harness-skills"),
                    explicit_only=True,
                )
            )
    operations = _deduplicate_operations(operations)

    _validate_user_destinations(home, operations)

    unchanged_platform_configs = set()
    protected_platform_configs = {
        Path(".codex/config.toml"),
        Path(".claude/settings.json"),
    }
    for item in operations:
        relative = item.destination.relative_to(home)
        if relative not in protected_platform_configs or not os.path.lexists(
            str(item.destination)
        ):
            continue
        if item.destination.is_symlink() or not item.destination.is_file():
            raise SafetyError(
                "Existing user platform config is not a regular file; "
                "manual merge required: {}".format(item.destination)
            )
        desired_content = (
            item.source.read_bytes() if item.content is None else item.content
        )
        try:
            existing_content = item.destination.read_bytes()
        except OSError as error:
            raise SafetyError(
                "Cannot read existing user platform config for manual merge: {}: {}".format(
                    item.destination, error
                )
            )
        if existing_content != desired_content:
            raise SafetyError(
                "Existing user platform config differs; manual merge required: {}".format(
                    item.destination
                )
            )
        unchanged_platform_configs.add(item.destination)

    write_operations = [
        item for item in operations if item.destination not in unchanged_platform_configs
    ]

    existing = [item for item in write_operations if item.destination.exists()]
    if apply_changes and existing and backup_dir is None:
        paths = ", ".join(str(item.destination) for item in existing)
        raise SafetyError(
            "Existing user files require --backup-dir before overwrite: {}".format(
                paths
            )
        )

    backup_paths: List[str] = []
    if apply_changes:
        _validate_user_destinations(home, write_operations)
        backup_root = None
        if backup_dir is not None:
            lexical_backup = _absolute_path(Path(backup_dir))
            for lexical_home in (requested_home, home):
                for managed_name in (".codex", ".claude", ".dsh", ".agents"):
                    lexical_managed = lexical_home / managed_name
                    if (
                        lexical_backup == lexical_managed
                        or lexical_managed in lexical_backup.parents
                    ):
                        raise SafetyError(
                            "Backup root must be outside managed user directories: {}".format(
                                lexical_backup
                            )
                        )
            _validate_backup_input_route(home, lexical_backup)
            backup_root = _canonical_scope_path(lexical_backup, "Backup root")
        backup_plan: List[Tuple[PlannedFile, Path]] = []
        if existing:
            assert backup_root is not None
            _validate_new_backup_root(home, backup_root)
        for item in write_operations:
            if item.destination.exists():
                if not item.destination.is_file() or item.destination.is_symlink():
                    raise SafetyError(
                        "Refusing to overwrite non-regular user file: {}".format(
                            item.destination
                        )
                    )
                assert backup_root is not None
                backup_relative = Path(item.display_path)
                if backup_relative.is_absolute() or ".." in backup_relative.parts:
                    raise SafetyError(
                        "Unsafe backup path: {}".format(item.display_path)
                    )
                backup_path = backup_root / backup_relative
                _validate_backup_target(backup_root, backup_path)
                backup_plan.append((item, backup_path))

        for item, backup_path in backup_plan:
            _validate_user_destinations(home, (item,))
            _atomic_install(
                PlannedFile(
                    source=item.destination,
                    destination=backup_path,
                    display_path=item.display_path,
                )
            )
            backup_paths.append(str(backup_path))

        backup_by_destination = {
            str(item.destination): backup_path for item, backup_path in backup_plan
        }
        applied_items: List[PlannedFile] = []
        try:
            for item in write_operations:
                _validate_user_destinations(home, (item,))
                _atomic_install(item)
                applied_items.append(item)
        except Exception as install_error:
            rollback_errors = []
            for item in reversed(applied_items):
                backup_path = backup_by_destination.get(str(item.destination))
                try:
                    if backup_path is not None:
                        _atomic_install(
                            PlannedFile(
                                source=backup_path,
                                destination=item.destination,
                                display_path=item.display_path,
                            )
                        )
                    elif item.destination.is_symlink():
                        raise SafetyError(
                            "Refusing to remove symlink during rollback: {}".format(
                                item.destination
                            )
                        )
                    elif item.destination.is_file():
                        item.destination.unlink()
                except Exception as rollback_error:
                    rollback_errors.append(
                        "{}: {}".format(item.destination, rollback_error)
                    )
            if rollback_errors:
                raise SafetyError(
                    "User install failed and rollback was incomplete: {}; "
                    "rollback errors: {}".format(
                        install_error, "; ".join(rollback_errors)
                    )
                )
            raise SafetyError(
                "User install failed; applied files were rolled back: {}".format(
                    install_error
                )
            )

    return OperationResult(
        planned_paths=tuple(item.display_path for item in operations),
        applied=apply_changes,
        backup_paths=tuple(backup_paths),
        destination_paths=tuple(str(item.destination) for item in operations),
    )


def _parse_frontmatter(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        raise ValueError("missing closing frontmatter delimiter")
    values = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip("\"'")
    return values


def _parse_strict_profile_frontmatter(text: str) -> Tuple[dict, List[str]]:
    lines = text.splitlines()
    delimiters = [index for index, line in enumerate(lines) if line.strip() == "---"]
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    if len(delimiters) != 2:
        raise ValueError("profile frontmatter must contain exactly two delimiters")
    end = delimiters[1]
    values = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        match = re.fullmatch(r"([A-Za-z0-9_-]+):\s*(.*?)\s*", line)
        if match is None:
            raise ValueError("invalid frontmatter line {}".format(line_number))
        key, raw_value = match.groups()
        if key in values:
            raise ValueError("duplicate frontmatter key: {}".format(key))
        if key != "profile_status":
            raise ValueError("unknown frontmatter key: {}".format(key))
        values[key] = raw_value.strip("\"'")
    return values, lines[end + 1 :]


def _profile_section_bodies(lines: Sequence[str]) -> Tuple[dict, List[str]]:
    """Return real H2 bodies and unknown H2s, ignoring fences and comments."""

    headings = []
    in_fence = False
    in_comment = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if "<!--" in stripped:
            if "-->" not in stripped[stripped.index("<!--") + 4 :]:
                in_comment = True
            continue
        if re.match(r"^(?:`{3,}|~{3,})", stripped):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.fullmatch(r"##\s+(.+?)\s*", line)
        if match is not None:
            headings.append((index, match.group(1)))
    bodies = {}
    unknown_sections = []
    for position, (index, title) in enumerate(headings):
        if title not in PROFILE_SECTIONS:
            unknown_sections.append(title)
            continue
        if title in bodies:
            bodies[title] = None
            continue
        next_index = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        bodies[title] = "\n".join(lines[index + 1 : next_index])
    return bodies, unknown_sections


def _profile_preamble(lines: Sequence[str]) -> str:
    """Return content before the first real H2, ignoring fenced examples/comments."""

    in_fence = False
    in_comment = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if "<!--" in stripped:
            if "-->" not in stripped[stripped.index("<!--") + 4 :]:
                in_comment = True
            continue
        if re.match(r"^(?:`{3,}|~{3,})", stripped):
            in_fence = not in_fence
            continue
        if not in_fence and re.fullmatch(r"##\s+(.+?)\s*", line) is not None:
            return "\n".join(lines[:index]).strip()
    return "\n".join(lines).strip()


def _profile_value_is_low_information(value: str) -> bool:
    normalized = value.strip().strip("`*_~").strip()
    normalized = normalized.strip(".,;:!?，。；：！？()（）[]【】{}<>-—_").strip()
    folded = re.sub(r"\s+", "", normalized.casefold())
    low_information_values = {
        "",
        "-",
        "—",
        "x",
        "xx",
        "xxx",
        "n/a",
        "na",
        "none",
        "nil",
        "null",
        "notapplicable",
        "tbd",
        "todo",
        "unknown",
        "ok",
        "done",
        "yes",
        "no",
        "true",
        "false",
        "value",
        "test",
        "foo",
        "bar",
        "baz",
        "placeholder",
        "fixturevalue",
        "validatedfixturevalue",
        "examplevalue",
        "samplevalue",
        "loremipsum",
        "待定",
        "待确认",
        "未确认",
        "尚未确认",
        "暂无",
        "没有",
        "无",
        "占位",
        "占位值",
        "示例",
        "示例值",
        "样例",
        "样例值",
        "测试值",
    }
    if folded in low_information_values:
        return True
    if re.search(r"(?:尚未确认|未确认|待确认|待定)", normalized) is not None:
        return True
    if re.search(r"\b(?:tbd|todo|unknown|n\s*/\s*a|not\s+applicable)\b", normalized, re.IGNORECASE):
        return True
    meaningful = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]", "", normalized)
    return len(meaningful) < 4 or len(set(meaningful.casefold())) == 1


def _profile_source_is_traceable(value: str) -> bool:
    if _profile_value_is_low_information(value):
        return False
    if value.startswith("path:"):
        try:
            _validate_repo_relative_path(value[len("path:") :])
        except ValueError:
            return False
        return True
    if value.startswith("command:"):
        command = value[len("command:") :].strip()
        return not _profile_value_is_low_information(command) and not any(
            ord(character) < 0x20 or ord(character) == 0x7F
            for character in command
        )
    if value.startswith("url:"):
        parsed = urlsplit(value[len("url:") :].strip())
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and parsed.username is None
            and parsed.password is None
        )
    if value.startswith("user-confirmation:"):
        confirmation = value[len("user-confirmation:") :].strip()
        match = re.fullmatch(r"(\d{4}-\d{2}-\d{2}):(.+)", confirmation)
        if match is None or _profile_value_is_low_information(match.group(2)):
            return False
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            return False
        return True
    return False


def _profile_not_applicable_reason_is_scoped(value: str) -> bool:
    reason_without_label = re.sub(
        r"\bnot\s+applicable\b|不适用(?:于)?", "", value, flags=re.IGNORECASE
    )
    if _profile_value_is_low_information(reason_without_label):
        return False
    return re.search(
        r"(?:不包含|不涉及|未使用|不存在|不适用(?:于)?|范围(?:之)?外|"
        r"\bout\s+of\s+scope\b|\bdoes\s+not\b|\bdoesn't\b|"
        r"\bnot\s+applicable\s+to\b|\bwithout\b|"
        r"\bno\s+(?:database|deployment|runtime|path|domain|component)\b)",
        value,
        re.IGNORECASE,
    ) is not None


def _profile_ready_content_issue(
    value: str, section: Optional[str] = None
) -> Optional[str]:
    if re.search(r"(?m)^[ \t]*(?:`{3,}|~{3,})", value) is not None:
        return "section contains hidden fenced content"
    if "<!--" in value or "-->" in value:
        return "section contains a hidden HTML comment"
    if re.search(
        "[\u00ad\u034f\u061c\u115f\u1160\u17b4\u17b5\u180e"
        "\u200b-\u200f\u202a-\u202e\u2060-\u206f\u3164\ufeff\uffa0]",
        value,
    ) is not None:
        return "section contains hidden Unicode control characters"

    visible = value.strip()
    if not visible or re.search(r"[A-Za-z0-9\u4e00-\u9fff]", visible) is None:
        return "structured Fact/Decision entry is missing or is a placeholder"
    if _profile_value_is_low_information(visible) and re.match(
        r"-\s+(?:Not applicable|不适用):", visible, re.IGNORECASE
    ) is None:
        return "structured entry contains a low-information placeholder statement"
    if re.search(r"<[^>]+>", visible) is not None:
        return "structured entry contains unsupported markup"

    lines = [line.rstrip() for line in visible.splitlines() if line.strip()]
    index = 0
    entry_count = 0
    while index < len(lines):
        item = re.fullmatch(
            r"-\s+(Fact|Decision|Not applicable|不适用):\s+(.+?)\s*",
            lines[index],
            re.IGNORECASE,
        )
        if item is None:
            return "section must contain only structured Fact/Decision/Not applicable entries"
        entry_type = item.group(1).casefold()
        statement = item.group(2)
        if _profile_value_is_low_information(statement):
            return "structured entry contains a low-information placeholder statement"
        is_not_applicable = entry_type in ("not applicable", "不适用")
        if is_not_applicable:
            if section in PROFILE_CORE_SECTIONS:
                return "core section cannot be marked Not applicable"
            if not _profile_not_applicable_reason_is_scoped(statement):
                return "Not applicable entry must give a concrete out-of-scope reason"
        index += 1
        if index >= len(lines):
            return "structured entry is missing a controlled Source"
        source = re.fullmatch(r"\s{2,}Source:\s+(.+?)\s*", lines[index])
        if source is None or not _profile_source_is_traceable(source.group(1)):
            return "structured entry has an invalid controlled Source"
        index += 1
        entry_count += 1
    if entry_count == 0:
        return "structured Fact/Decision entry is missing"
    return None


def _profile_content_is_ready(value: str) -> bool:
    return _profile_ready_content_issue(value) is None


def _validate_project_profile(
    path: Path,
    require_ready: bool = False,
    expected_preamble: Optional[str] = None,
) -> List[str]:
    issues: List[str] = []
    try:
        text = path.read_text(encoding="utf-8")
        frontmatter, body_lines = _parse_strict_profile_frontmatter(text)
    except (OSError, UnicodeError, ValueError) as error:
        return ["invalid project profile: {}".format(error)]
    status = frontmatter.get("profile_status")
    if _contains_secret_assignment(text):
        issues.append(
            "project profile contains secret-like content: {}".format(path)
        )
    if status not in ("draft", "active"):
        issues.append("project profile profile_status must be draft or active")
    bodies, unknown_sections = _profile_section_bodies(body_lines)
    for section in unknown_sections:
        issues.append("project profile unknown section: {}".format(section))
    for section in PROFILE_SECTIONS:
        if section not in bodies:
            issues.append("project profile missing required section: {}".format(section))
        elif bodies[section] is None:
            issues.append("project profile duplicate section: {}".format(section))
    enforce_ready = require_ready or status == "active"
    if require_ready:
        if status != "active":
            issues.append("project profile must declare profile_status: active")
    if enforce_ready:
        if (
            expected_preamble is not None
            and _profile_preamble(body_lines) != expected_preamble
        ):
            issues.append("project profile preamble drift: {}".format(path))
        for section in PROFILE_SECTIONS:
            content = bodies.get(section)
            content_issue = (
                _profile_ready_content_issue(content, section)
                if content is not None
                else None
            )
            if content_issue is not None:
                issues.append(
                    "ready project profile section {}: {}".format(
                        section, content_issue
                    )
                )
    return issues


def _validate_memory_candidates(path: Path) -> List[str]:
    issues: List[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return ["invalid Memory candidates: {}".format(error)]
    seen_ids = set()
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = _load_strict_json_text(line)
        except (ValueError, json.JSONDecodeError) as error:
            issues.append("Memory candidate line {}: {}".format(number, error))
            continue
        if not isinstance(value, dict):
            issues.append("Memory candidate line {} must be an object".format(number))
            continue
        unknown = sorted(set(value) - MEMORY_CANDIDATE_FIELDS)
        missing = sorted(MEMORY_CANDIDATE_FIELDS - set(value))
        if unknown:
            issues.append("Memory candidate line {} has unknown field(s): {}".format(number, ", ".join(unknown)))
        if missing:
            issues.append("Memory candidate line {} missing field(s): {}".format(number, ", ".join(missing)))
        for field in MEMORY_CANDIDATE_FIELDS:
            field_value = value.get(field)
            if not isinstance(field_value, str) or not field_value.strip():
                issues.append(
                    "Memory candidate line {} field {} must be a non-empty string".format(
                        number, field
                    )
                )
            elif _contains_secret_assignment(field_value):
                issues.append(
                    "Memory candidate line {} field {} contains secret-like content".format(
                        number, field
                    )
                )
        candidate_id = value.get("id")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            issues.append("Memory candidate line {} has invalid id".format(number))
        elif candidate_id in seen_ids:
            issues.append("Memory candidate line {} has duplicate id: {}".format(number, candidate_id))
        else:
            seen_ids.add(candidate_id)
        if value.get("status") != "candidate":
            issues.append("Memory candidate line {} status must be candidate".format(number))
    return issues


def _validate_control_checker_template(path: Path) -> None:
    raw = path.read_bytes()
    if b"\x00" in raw:
        raise ValueError("control checker contains NUL byte")
    text = raw.decode("utf-8")
    if any(
        ord(character) < 0x20 and character not in "\t\n\r"
        or ord(character) == 0x7F
        for character in text
    ):
        raise ValueError("control checker contains control character")
    compile(text, str(path), "exec")


def _ledger_source_ids(path: Path, prefix: str) -> set:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"(?m)^\| ({}-\d{{3}}) \|".format(prefix), text))


def _validate_rule_traceability(root: Path) -> List[str]:
    path = root / "sources/rule-traceability.json"
    issues: List[str] = []
    try:
        value = _load_strict_json_text(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        return ["invalid rule traceability: {}".format(error)]
    if not isinstance(value, dict) or set(value) != {"schema_version", "verified_on", "scope", "rules"}:
        return ["invalid rule traceability schema"]
    scope = value.get("scope")
    rules = value.get("rules")
    if not isinstance(scope, dict) or not isinstance(rules, list):
        return ["invalid rule traceability scope or rules"]
    approved = scope.get("approved_eval_ids")
    meanings = scope.get("planned_eval_meaning")
    if set(approved or ()) != APPROVED_EVAL_IDS or meanings != PLANNED_EVAL_MEANING:
        issues.append("rule traceability approved eval boundary is invalid")
    try:
        source_ids = _ledger_source_ids(root / "docs/research/local-tip-ledger.md", "LOC")
        source_ids.update(_ledger_source_ids(root / "docs/research/ref-links-ledger.md", "REF"))
        source_ids.update(_ledger_source_ids(root / "report-source.md", "RSP"))
    except (OSError, UnicodeError) as error:
        return issues + ["cannot read traceability ledger: {}".format(error)]
    local_count = len([item for item in source_ids if item.startswith("LOC-")])
    ref_count = len([item for item in source_ids if item.startswith("REF-")])
    if scope.get("local_source_count") != local_count:
        issues.append("rule traceability local source count is invalid")
    if scope.get("ref_link_unique_count") != ref_count:
        issues.append("rule traceability ref source count is invalid")
    for index in range(1, 12):
        task = root / "evals/tasks/{:02d}-".format(index)
        if not any(task.parent.glob(task.name + "*.md")):
            issues.append("missing traceability task for EVAL-{:02d}".format(index))
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) != TRACEABILITY_FIELDS:
            issues.append("invalid traceability rule fields")
            continue
        for source in rule["sources"]:
            if source not in source_ids:
                issues.append("unknown traceability source: {}".format(source))
        for artifact in rule["artifacts"]:
            if not isinstance(artifact, dict) or set(artifact) != {"path", "status"}:
                issues.append("invalid traceability artifact")
                continue
            status = artifact["status"]
            if not isinstance(status, str) or status not in {
                "implemented",
                "planned",
                "planned-update",
                "implemented-with-planned-eval",
                "implemented-and-planned-expansion",
            }:
                issues.append("invalid traceability artifact status: {}".format(status))
            elif status.startswith("implemented") and not (root / artifact["path"]).exists():
                issues.append("implemented traceability artifact is missing: {}".format(artifact["path"]))
        for eval_case in rule["eval_cases"]:
            if eval_case not in APPROVED_EVAL_IDS:
                issues.append("unknown traceability eval: {}".format(eval_case))
    return issues


def _extract_shared_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start_marker = "<!-- BEGIN SHARED CORE -->"
    end_marker = "<!-- END SHARED CORE -->"
    if start_marker not in text or end_marker not in text:
        raise ValueError("missing shared-core markers")
    return text.split(start_marker, 1)[1].split(end_marker, 1)[0].strip()


def _canonical_shared_content(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if "<!-- BEGIN SHARED CORE -->" in text:
        return _extract_shared_block(path)
    return text.strip()


def _render_shared_adapter(canonical_path: Path, adapter_path: Path) -> bytes:
    canonical = _canonical_shared_content(canonical_path)
    if _contains_secret_assignment(canonical):
        raise SafetyError(
            "Refusing to render secret-like assignment from {}".format(
                canonical_path
            )
        )
    text = adapter_path.read_text(encoding="utf-8")
    start_marker = "<!-- BEGIN SHARED CORE -->"
    end_marker = "<!-- END SHARED CORE -->"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise SafetyError(
            "Adapter must contain exactly one shared-core block: {}".format(
                adapter_path
            )
        )
    prefix, remainder = text.split(start_marker, 1)
    _old_core, suffix = remainder.split(end_marker, 1)
    rendered = (
        prefix
        + start_marker
        + "\n"
        + canonical
        + "\n"
        + end_marker
        + suffix
    )
    return rendered.encode("utf-8")


def render_templates(
    system_root: Path, apply_changes: bool = False
) -> OperationResult:
    """Plan or refresh generated shared-core snapshots from canonical sources."""

    root = _absolute_path(Path(system_root))
    _require_declared_source_trees(root)
    operations: List[PlannedFile] = []
    for canonical_relative, adapter_relative in SHARED_ADAPTERS:
        canonical_path = root / canonical_relative
        adapter_path = root / adapter_relative
        _ensure_regular_source(root, canonical_path)
        _ensure_regular_source(root, adapter_path)
        operations.append(
            PlannedFile(
                source=adapter_path,
                destination=adapter_path,
                display_path=adapter_relative,
                content=_render_shared_adapter(canonical_path, adapter_path),
            )
        )
    operations = _deduplicate_operations(operations)
    if apply_changes:
        for operation in operations:
            _atomic_install(operation)
    return OperationResult(
        planned_paths=tuple(item.display_path for item in operations),
        applied=apply_changes,
        destination_paths=tuple(str(item.destination) for item in operations),
    )


def _validate_basic_toml_basic_string(raw_value: str, line_number: int) -> None:
    if len(raw_value) < 2 or not raw_value.endswith('"'):
        raise ValueError("invalid TOML string on line {}".format(line_number))
    body = raw_value[1:-1]
    index = 0
    simple_escapes = {"b", "t", "n", "f", "r", '"', "\\"}
    while index < len(body):
        character = body[index]
        if ord(character) < 0x20 or ord(character) == 0x7F:
            raise ValueError(
                "invalid control character in TOML string on line {}".format(
                    line_number
                )
            )
        if character == '"':
            raise ValueError("unescaped quote in TOML string on line {}".format(line_number))
        if character != "\\":
            index += 1
            continue
        if index + 1 >= len(body):
            raise ValueError("invalid TOML escape on line {}".format(line_number))
        escape = body[index + 1]
        if escape in simple_escapes:
            index += 2
            continue
        if escape not in ("u", "U"):
            raise ValueError("invalid TOML escape on line {}".format(line_number))
        width = 4 if escape == "u" else 8
        digits = body[index + 2 : index + 2 + width]
        if len(digits) != width or re.fullmatch(r"[0-9A-Fa-f]+", digits) is None:
            raise ValueError("invalid TOML unicode escape on line {}".format(line_number))
        codepoint = int(digits, 16)
        if (
            codepoint > 0x10FFFF
            or 0xD800 <= codepoint <= 0xDFFF
            or codepoint == 0x7F
        ):
            raise ValueError("invalid TOML unicode scalar on line {}".format(line_number))
        index += 2 + width


def _validate_basic_toml_fallback(text: str) -> dict:
    """Validate the deliberately flat TOML subset supported on Python 3.9/3.10."""

    seen_keys = set()
    parsed = {}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z0-9_-]+)\s*=\s*(.+)", line)
        if match is None:
            raise ValueError(
                "invalid or unsupported TOML line {}".format(line_number)
            )
        key, raw_value = match.groups()
        if key in seen_keys:
            raise ValueError("duplicate TOML key on line {}".format(line_number))
        seen_keys.add(key)
        if raw_value.startswith('"'):
            _validate_basic_toml_basic_string(raw_value, line_number)
            parsed[key] = None
            continue
        if re.fullmatch(r"'[^'\x00-\x1F\x7F]*'", raw_value):
            parsed[key] = None
            continue
        if raw_value in ("true", "false"):
            parsed[key] = None
            continue
        integer = r"(?:0|[1-9](?:_?[0-9])*)"
        fraction = r"[0-9](?:_?[0-9])*"
        if re.fullmatch(
            r"[+-]?{}(?:\.{})?".format(integer, fraction), raw_value
        ):
            parsed[key] = None
            continue
        raise ValueError(
            "unsupported TOML value on line {} under Python < 3.11".format(
                line_number
            )
        )
    return parsed


def _parse_declared_toml_text(text: str) -> dict:
    try:
        import tomllib  # type: ignore

        parsed = tomllib.loads(text)
        if not isinstance(parsed, dict):
            raise ValueError("TOML document root must be a table")
        return parsed
    except ImportError:
        return _validate_basic_toml_fallback(text)


def _validate_basic_toml(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    _parse_declared_toml_text(text)


def _validate_comments_only_toml(path: Path) -> None:
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if line and not line.startswith("#"):
            raise ValueError(
                "must be comments-only; statement on line {}".format(line_number)
            )


def _validate_openai_metadata_text(text: str) -> Tuple[dict, Optional[bool]]:
    """Parse the intentionally tiny, fixed schema used by agents/openai.yaml."""

    lines = text.splitlines()
    if not lines or lines[0] != "interface:":
        raise ValueError("metadata must start with literal 'interface:'")
    values = {}
    index = 1
    for key in ("display_name", "short_description", "default_prompt"):
        prefix = "  {}: ".format(key)
        if index >= len(lines) or not lines[index].startswith(prefix):
            raise ValueError("metadata must define {} in canonical order".format(key))
        raw_value = lines[index][len(prefix) :]
        try:
            parsed_value = _load_strict_json_text(raw_value)
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            raise ValueError(
                "metadata {} must be a JSON quoted string: {}".format(key, error)
            )
        if not isinstance(parsed_value, str) or not parsed_value.strip():
            raise ValueError("metadata {} must be a non-empty string".format(key))
        values[key] = parsed_value
        index += 1

    allow_implicit: Optional[bool] = None
    if index < len(lines):
        if lines[index] != "policy:":
            raise ValueError("unexpected metadata line: {}".format(index + 1))
        index += 1
        if (
            index >= len(lines)
            or lines[index] != "  allow_implicit_invocation: false"
        ):
            raise ValueError(
                "policy must contain literal allow_implicit_invocation: false"
            )
        allow_implicit = False
        index += 1
    if index != len(lines):
        raise ValueError("unexpected metadata line: {}".format(index + 1))
    return values, allow_implicit


def _validate_relative_links(skill_file: Path) -> List[str]:
    issues = []
    text = skill_file.read_text(encoding="utf-8")
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = raw_target.split("#", 1)[0].strip().strip("<>")
        if not target or "://" in target or target.startswith("#"):
            continue
        target_path = Path(target)
        if target_path.is_absolute():
            issues.append(
                "absolute skill reference in {}: {}".format(
                    skill_file, raw_target
                )
            )
            continue
        try:
            skill_root = skill_file.parent.resolve()
        except (OSError, RuntimeError):
            issues.append(
                "skill root cannot be resolved safely: {}".format(skill_file.parent)
            )
            continue
        unresolved = skill_file.parent / target_path
        try:
            resolved = unresolved.resolve(strict=False)
        except (OSError, RuntimeError):
            issues.append(
                "skill reference cannot be resolved safely in {}: {}".format(
                    skill_file, raw_target
                )
            )
            continue
        if resolved != skill_root and skill_root not in resolved.parents:
            issues.append(
                "skill reference escapes skill root in {}: {}".format(
                    skill_file, raw_target
                )
            )
        elif not resolved.exists():
            issues.append(
                "broken skill reference in {}: {}".format(skill_file, raw_target)
            )
        elif unresolved.is_symlink() or not resolved.is_file():
            issues.append(
                "skill reference is not a regular file in {}: {}".format(
                    skill_file, raw_target
                )
            )
    return issues


def _validate_declared_source_trees(root: Path) -> Tuple[List[str], bool]:
    """Validate template/skill membership before reading their contents."""

    issues: List[str] = []
    unsafe_entry = False
    absolute_root = _absolute_path(root)
    if absolute_root.is_symlink():
        return (["system root is a symlink: {}".format(absolute_root)], True)
    for name in ("templates", "skills"):
        base = absolute_root / name
        if base.is_symlink():
            issues.append("source tree contains symlink: {}".format(base))
            unsafe_entry = True
            continue
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            relative = path.relative_to(absolute_root).as_posix()
            if (
                path.name in IGNORED_SOURCE_FILE_NAMES
                and path.is_file()
                and not path.is_symlink()
            ):
                continue
            if path.is_symlink():
                issues.append("source tree contains symlink: {}".format(relative))
                unsafe_entry = True
            elif path.is_dir():
                if name == "skills":
                    relative_to_skills = path.relative_to(base)
                    parts = relative_to_skills.parts
                    allowed = (
                        len(parts) == 1 and parts[0] in SKILL_NAMES
                    ) or (
                        len(parts) >= 2
                        and parts[0] in SKILL_NAMES
                        and _skill_relative_directory_is_allowed(
                            Path(*parts[1:])
                        )
                    )
                    if not allowed:
                        issues.append(
                            "undeclared source directory: {}".format(relative)
                        )
                continue
            elif not path.is_file():
                issues.append("source tree contains non-regular entry: {}".format(relative))
                unsafe_entry = True
            elif _source_file_kind(relative) is None:
                issues.append("undeclared source file: {}".format(relative))
    return issues, unsafe_entry


def validate_system(system_root: Path) -> List[str]:
    """Return structural and safety issues; an empty list means validation passed."""

    root = _absolute_path(Path(system_root))
    issues, unsafe_source_entry = _validate_declared_source_trees(root)
    if unsafe_source_entry:
        return issues
    safe_required = set()
    for relative in REQUIRED_FILES:
        path = root / relative
        try:
            _ensure_no_symlink_components(root, path, "Required file")
        except SafetyError as error:
            issues.append("{}: {}".format(relative, error))
            continue
        if not path.is_file():
            issues.append("missing required file: {}".format(relative))
            continue
        safe_required.add(relative)
    for relative in REQUIRED_FILES:
        if not relative.endswith(".md") or relative.startswith(
            ("templates/", "skills/")
        ):
            continue
        if relative not in safe_required:
            continue
        path = root / relative
        try:
            frontmatter = _parse_frontmatter(path)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append("{}: invalid document frontmatter: {}".format(relative, error))
            continue
        if not frontmatter.get("title"):
            issues.append("{}: document title is missing".format(relative))

    core_path = root / "templates/shared/user-core.md"
    if core_path.is_file():
        try:
            expected_core = _canonical_shared_content(core_path)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append(
                "templates/shared/user-core.md: invalid UTF-8 text source: {}".format(
                    error
                )
            )
        else:
            for relative in (
                "templates/user/codex/AGENTS.md",
                "templates/user/claude/CLAUDE.md",
                "templates/user/deepseek-harness/AGENTS.md",
            ):
                path = root / relative
                if not path.is_file():
                    continue
                try:
                    actual_core = _extract_shared_block(path)
                except (OSError, UnicodeError, ValueError) as error:
                    issues.append("{}: {}".format(relative, error))
                    continue
                if actual_core != expected_core:
                    issues.append("shared core drift: {}".format(relative))

    project_claude = root / "templates/project/.claude/CLAUDE.md"
    if project_claude.is_file():
        try:
            logical_lines = [
                line.strip()
                for line in project_claude.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        except (OSError, UnicodeError) as error:
            issues.append(
                "templates/project/.claude/CLAUDE.md invalid UTF-8 text source: {}".format(
                    error
                )
            )
        else:
            if not logical_lines or logical_lines[0] != "@../AGENTS.md":
                issues.append(
                    "project .claude/CLAUDE.md must import @../AGENTS.md first"
                )

    project_codex = root / "templates/project/.codex/config.toml"
    if project_codex.is_file():
        try:
            _validate_comments_only_toml(project_codex)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append(
                "templates/project/.codex/config.toml {}".format(error)
            )

    user_codex = root / "templates/user/codex/config.toml"
    if user_codex.is_file():
        try:
            _validate_comments_only_toml(user_codex)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append(
                "templates/user/codex/config.toml {}".format(error)
            )

    project_core = root / "templates/shared/project-core.md"
    if project_core.is_file():
        for relative in (
            "templates/project/AGENTS.md",
            "templates/project/codex/AGENTS.md",
            "templates/project/deepseek-harness/AGENTS.md",
        ):
            project_agents = root / relative
            if not project_agents.is_file():
                continue
            try:
                actual_project_core = _extract_shared_block(project_agents)
                expected_project_core = _canonical_shared_content(project_core)
            except (OSError, UnicodeError, ValueError) as error:
                issues.append("{}: {}".format(relative, error))
            else:
                if actual_project_core != expected_project_core:
                    issues.append("shared project core drift: {}".format(relative))

    profile_source = root / "templates/project/.agents/project-profile.md"
    if profile_source.is_file():
        issues.extend(_validate_project_profile(profile_source))
    memory_source = root / "templates/project/.agents/memory/candidates.jsonl"
    if memory_source.is_file():
        issues.extend(_validate_memory_candidates(memory_source))
    control_example = root / "templates/project/.agents/controls/change-policy.example.json"
    if control_example.is_file():
        try:
            _validate_change_policy_file(control_example)
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
            issues.append("invalid change policy example: {}".format(error))
    control_checker = root / "templates/project/.agents/controls/check_change_policy.py"
    if control_checker.is_file():
        try:
            _validate_control_checker_template(control_checker)
        except (OSError, UnicodeError, ValueError, SyntaxError) as error:
            issues.append("invalid control checker template: {}".format(error))
    issues.extend(_validate_rule_traceability(root))

    skills_root = root / "skills"
    if skills_root.is_dir():
        discovered = {path.name for path in skills_root.iterdir() if path.is_dir()}
        missing_skills = sorted(set(SKILL_NAMES) - discovered)
        unexpected_skills = sorted(discovered - set(SKILL_NAMES))
        if missing_skills:
            issues.append("missing skills: {}".format(", ".join(missing_skills)))
        if unexpected_skills:
            issues.append(
                "unexpected skills: {}".format(", ".join(unexpected_skills))
            )
        actual_explicit_skills = set()
        metadata_policy_skills = set()
        for directory in sorted(path for path in skills_root.iterdir() if path.is_dir()):
            skill_file = directory / "SKILL.md"
            metadata_file = directory / "agents/openai.yaml"
            if not skill_file.is_file():
                issues.append("missing SKILL.md: {}".format(directory.name))
                continue
            if not metadata_file.is_file():
                issues.append("missing agents/openai.yaml: {}".format(directory.name))
            try:
                frontmatter = _parse_frontmatter(skill_file)
            except (OSError, UnicodeError, ValueError) as error:
                issues.append("{}: {}".format(skill_file, error))
                continue
            if frontmatter.get("name") != directory.name:
                issues.append(
                    "skill name does not match directory: {}".format(directory.name)
                )
            if not frontmatter.get("description"):
                issues.append("skill description is empty: {}".format(directory.name))
            try:
                skill_text = skill_file.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                issues.append(
                    "{}: invalid UTF-8 text source: {}".format(skill_file, error)
                )
                continue
            frontmatter_match = re.match(
                r"\A---\s*\n(?P<frontmatter>.*?)\n---(?:\s*\n|\Z)",
                skill_text,
                re.DOTALL,
            )
            if frontmatter_match and re.search(
                r"(?m)^disable-model-invocation:\s*",
                frontmatter_match.group("frontmatter"),
            ):
                issues.append(
                    "canonical portable skill contains platform-specific invocation field: {}".format(
                        directory.name
                    )
                )
            try:
                is_explicit = _skill_uses_explicit_invocation(skill_file)
            except (OSError, UnicodeError, SafetyError) as error:
                issues.append(str(error))
                is_explicit = False
            if is_explicit:
                actual_explicit_skills.add(directory.name)
            if metadata_file.is_file():
                try:
                    metadata_text = metadata_file.read_text(encoding="utf-8")
                    metadata_values, allow_implicit = _validate_openai_metadata_text(
                        metadata_text
                    )
                except (OSError, UnicodeError, ValueError) as error:
                    issues.append(
                        "{}: invalid OpenAI metadata: {}".format(
                            metadata_file, error
                        )
                    )
                    metadata_values = None
                    allow_implicit = None
                if allow_implicit is False:
                    metadata_policy_skills.add(directory.name)
                if metadata_values is not None and "${}".format(
                    directory.name
                ) not in metadata_values["default_prompt"]:
                    issues.append(
                        "Codex default prompt must invoke ${}: {}".format(
                            directory.name, directory.name
                        )
                    )
            issues.extend(_validate_relative_links(skill_file))
        expected_explicit_skills = set(EXPLICIT_SKILL_NAMES)
        if actual_explicit_skills != expected_explicit_skills:
            issues.append(
                "explicit skill markers must equal {}; actual {}".format(
                    ", ".join(EXPLICIT_SKILL_NAMES),
                    ", ".join(sorted(actual_explicit_skills)) or "none",
                )
            )
        if metadata_policy_skills != expected_explicit_skills:
            for missing_policy in sorted(
                expected_explicit_skills - metadata_policy_skills
            ):
                issues.append(
                    "explicit skill lacks Codex implicit-invocation policy: {}".format(
                        missing_policy
                    )
                )
            for unexpected_policy in sorted(
                metadata_policy_skills - expected_explicit_skills
            ):
                issues.append(
                    "non-explicit skill has Codex implicit-invocation policy: {}".format(
                        unexpected_policy
                    )
                )
            issues.append(
                "Codex explicit-skill policies must equal {}; actual {}".format(
                    ", ".join(EXPLICIT_SKILL_NAMES),
                    ", ".join(sorted(metadata_policy_skills)) or "none",
                )
            )
    else:
        issues.append("missing skills directory: skills")

    for relative in sorted(
        item for item in REQUIRED_FILES if Path(item).suffix == ".json"
    ):
        if relative not in safe_required:
            continue
        path = root / relative
        try:
            _load_strict_json_text(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
            issues.append("invalid JSON {}: {}".format(relative, error))
    for relative in sorted(
        item
        for item in REQUIRED_FILES
        if item.startswith("evals/") and Path(item).suffix == ".py"
    ):
        if relative not in safe_required:
            continue
        path = root / relative
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, relative, "exec")
        except (OSError, UnicodeError, ValueError, SyntaxError) as error:
            issues.append("invalid Python {}: {}".format(relative, error))
    for relative in sorted(
        item for item in REQUIRED_FILES if Path(item).suffix == ".toml"
    ):
        if relative not in safe_required:
            continue
        path = root / relative
        try:
            _validate_basic_toml(path)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append("invalid TOML {}: {}".format(relative, error))

    forbidden = {
        "model_instructions_file": "Codex base prompt replacement is forbidden",
        "bypassPermissions": "permission bypass is forbidden in templates",
        "danger-full-access": "full-access sandbox is forbidden in templates",
    }
    unresolved_placeholders = (
        re.compile(r"\bTODO\b"),
        re.compile(r"\bTBD\b"),
        re.compile(r"\bPLACEHOLDER\b"),
        re.compile(r"<REPLACE_ME>"),
    )
    for base in (root / "templates", root / "skills"):
        if not base.is_dir():
            continue
        for path in sorted(item for item in base.rglob("*") if item.is_file()):
            if (
                path.name in IGNORED_SOURCE_FILE_NAMES
                and not path.is_symlink()
            ):
                continue
            relative = path.relative_to(root)
            relative_to_base = path.relative_to(base)
            if _is_sensitive_relative_path(relative_to_base):
                issues.append("{}: sensitive source path".format(relative))
                continue
            source_kind = _source_file_kind(relative.as_posix())
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as error:
                if source_kind == "asset":
                    continue
                issues.append(
                    "{}: invalid UTF-8 text source: {}".format(relative, error)
                )
                continue
            if _contains_secret_assignment(text):
                issues.append("{}: secret-like assignment".format(relative))
            for needle, message in forbidden.items():
                if needle in text:
                    issues.append("{}: {}".format(relative, message))
            for pattern in unresolved_placeholders:
                match = pattern.search(text)
                if match:
                    issues.append(
                        "{}: unresolved placeholder {}".format(
                            relative, match.group(0)
                        )
                    )

    return issues


def _frontmatter_has_explicit_disable(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    match = re.match(
        r"\A---\s*\n(?P<frontmatter>.*?)\n---(?:\s*\n|\Z)",
        text,
        re.DOTALL,
    )
    if match is None:
        return False
    return re.search(
        r"(?m)^disable-model-invocation:\s*true\s*$",
        match.group("frontmatter"),
    ) is not None


def _generated_path_safety_issue(root: Path, path: Path) -> Optional[str]:
    absolute_root = _absolute_path(root)
    absolute_path = _absolute_path(path)
    try:
        relative = absolute_path.relative_to(absolute_root)
    except ValueError:
        return "generated path escapes root: {}".format(path)
    current = absolute_root
    for index, part in enumerate(relative.parts):
        current = current / part
        if current.is_symlink():
            return "generated path traverses a symlink: {}".format(current)
        if (
            index < len(relative.parts) - 1
            and os.path.lexists(str(current))
            and not current.is_dir()
        ):
            return "generated path ancestor is not a directory: {}".format(current)
    try:
        resolved_root = absolute_root.resolve(strict=False)
        resolved_path = absolute_path.resolve(strict=False)
    except (OSError, RuntimeError):
        return "generated path cannot be resolved safely: {}".format(path)
    if resolved_path != resolved_root and resolved_root not in resolved_path.parents:
        return "generated path resolves outside root: {}".format(path)
    return None


def _validate_generated_skill_tree(
    system_root: Path,
    generated_root: Path,
    tree_root: Path,
    expected_names: Sequence[str],
    mode: str,
    allow_project_extensions: bool = False,
) -> Tuple[List[str], List[Path]]:
    issues: List[str] = []
    checked_files: List[Path] = []
    expected = set(expected_names)
    tree_safety_issue = _generated_path_safety_issue(generated_root, tree_root)
    if tree_safety_issue is not None:
        return ([tree_safety_issue], [])
    if not tree_root.is_dir():
        return (["missing generated skill root: {}".format(tree_root)], [])
    actual = set()
    for path in tree_root.iterdir():
        path_issue = _generated_path_safety_issue(generated_root, path)
        if path_issue is not None:
            issues.append(path_issue)
        elif not path.is_dir():
            issues.append("invalid generated skill root entry: {}".format(path))
        else:
            actual.add(path.name)
    for missing in sorted(expected - actual):
        issues.append("missing generated skill: {}/{}".format(tree_root, missing))
    managed_names_folded = {name.casefold() for name in expected}
    extension_names = set()
    for unexpected in sorted(actual - expected):
        if unexpected.casefold() in managed_names_folded:
            issues.append(
                "project skill overrides managed Skill name: {}/{}".format(
                    tree_root, unexpected
                )
            )
        elif allow_project_extensions and mode == "canonical":
            extension_names.add(unexpected)
        else:
            issues.append(
                "unexpected generated skill: {}/{}".format(tree_root, unexpected)
            )

    def validate_skill_layout(skill_dir: Path) -> Tuple[set, dict]:
        actual_files = set()
        file_kinds = {}
        for entry in skill_dir.rglob("*"):
            entry_issue = _generated_path_safety_issue(generated_root, entry)
            relative_entry = entry.relative_to(skill_dir)
            if entry_issue is not None:
                issues.append(entry_issue)
                continue
            if _is_sensitive_relative_path(relative_entry):
                issues.append(
                    "generated skill uses sensitive path: {}".format(entry)
                )
                continue
            if entry.is_dir():
                if not _skill_relative_directory_is_allowed(relative_entry):
                    issues.append(
                        "unexpected generated skill directory: {}".format(entry)
                    )
                continue
            kind = _skill_relative_file_kind(relative_entry)
            if not entry.is_file() or kind is None:
                issues.append("unexpected generated skill file: {}".format(entry))
                continue
            actual_files.add(relative_entry)
            file_kinds[relative_entry] = kind
            try:
                text = entry.read_text(encoding="utf-8")
            except UnicodeDecodeError as error:
                if kind != "asset":
                    issues.append(
                        "invalid UTF-8 generated skill instruction {}: {}".format(
                            entry, error
                        )
                    )
                continue
            if _contains_secret_assignment(text):
                issues.append("generated skill contains secret-like assignment: {}".format(entry))
        return actual_files, file_kinds

    for name in sorted(expected & actual):
        skill_dir = tree_root / name
        actual_files, _file_kinds = validate_skill_layout(skill_dir)
        source_dir = system_root / "skills" / name
        source_files = {
            path.relative_to(source_dir): path
            for path in source_dir.rglob("*")
            if path.is_file()
            and path.name not in IGNORED_SOURCE_FILE_NAMES
            and (mode == "canonical" or path.relative_to(source_dir).parts[0] != "agents")
        }
        for missing_file in sorted(set(source_files) - actual_files, key=str):
            issues.append(
                "missing generated skill resource: {}".format(
                    skill_dir / missing_file
                )
            )
        for extra_file in sorted(actual_files - set(source_files), key=str):
            issues.append(
                "unexpected generated skill file: {}".format(skill_dir / extra_file)
            )
        source_skill_file = source_dir / "SKILL.md"
        source_is_explicit = _skill_uses_explicit_invocation(source_skill_file)
        for relative_file in sorted(set(source_files) & actual_files, key=str):
            generated_file = skill_dir / relative_file
            source_file = source_files[relative_file]
            expected_content = (
                _render_explicit_skill_variant(source_file)
                if relative_file == Path("SKILL.md")
                and mode != "canonical"
                and source_is_explicit
                else source_file.read_bytes()
            )
            if generated_file.read_bytes() != expected_content:
                message = (
                    "generated Codex metadata drift"
                    if relative_file == Path("agents/openai.yaml")
                    else "generated skill content drift"
                )
                issues.append("{}: {}".format(message, generated_file))
            checked_files.append(generated_file)

        skill_file = tree_root / name / "SKILL.md"
        skill_issue = _generated_path_safety_issue(generated_root, skill_file)
        if skill_issue is not None:
            issues.append(skill_issue)
            continue
        if not skill_file.is_file():
            issues.append("missing regular generated skill file: {}".format(skill_file))
            continue
        checked_files.append(skill_file)
        try:
            frontmatter = _parse_frontmatter(skill_file)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append("{}: {}".format(skill_file, error))
            continue
        if frontmatter.get("name") != name:
            issues.append("generated skill name mismatch: {}".format(skill_file))
        canonical_explicit = source_is_explicit
        has_disable = _frontmatter_has_explicit_disable(skill_file)
        if mode == "canonical":
            metadata = tree_root / name / "agents/openai.yaml"
            metadata_issue = _generated_path_safety_issue(generated_root, metadata)
            if metadata_issue is not None:
                issues.append(metadata_issue)
            elif not metadata.is_file():
                issues.append("missing generated Codex metadata: {}".format(metadata))
            if has_disable:
                issues.append(
                    "canonical generated skill has platform-specific invocation field: {}".format(
                        skill_file
                    )
                )
        else:
            if (tree_root / name / "agents").exists():
                issues.append(
                    "platform generated skill must not contain agents metadata: {}".format(
                        tree_root / name / "agents"
                    )
                )
            if canonical_explicit and not has_disable:
                issues.append(
                    "missing explicit invocation field: {}".format(skill_file)
                )
            if not canonical_explicit and has_disable:
                issues.append(
                    "unexpected explicit invocation field: {}".format(skill_file)
                )
        issues.extend(_validate_relative_links(skill_file))

    for name in sorted(extension_names):
        skill_dir = tree_root / name
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is None:
            issues.append("invalid project skill directory name: {}".format(skill_dir))
        actual_files, _file_kinds = validate_skill_layout(skill_dir)
        skill_file = skill_dir / "SKILL.md"
        if Path("SKILL.md") not in actual_files:
            issues.append("missing regular generated skill file: {}".format(skill_file))
            continue
        checked_files.append(skill_file)
        try:
            frontmatter = _parse_frontmatter(skill_file)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append("invalid project skill frontmatter {}: {}".format(skill_file, error))
            continue
        if frontmatter.get("name") != name:
            issues.append("generated skill name mismatch: {}".format(skill_file))
        if not frontmatter.get("description"):
            issues.append("generated skill description is empty: {}".format(skill_file))
        try:
            text = skill_file.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            text = ""
        match = re.match(
            r"\A---\s*\n(?P<frontmatter>.*?)\n---(?:\s*\n|\Z)",
            text,
            re.DOTALL,
        )
        if match is None:
            issues.append("invalid project skill frontmatter: {}".format(skill_file))
        elif re.search(
            r"(?m)^metadata:\s*$\n(?:^[ \t]+.*\n)*?"
            r"^[ \t]+invocation:\s*[\"']?explicit-only[\"']?\s*$",
            match.group("frontmatter") + "\n",
        ):
            issues.append(
                "project-owned Skill cannot use metadata.invocation: explicit-only: {}".format(
                    skill_file
                )
            )
        elif re.search(
            r"(?m)^disable-model-invocation:\s*", match.group("frontmatter")
        ):
            issues.append(
                "canonical generated skill has platform-specific invocation field: {}".format(
                    skill_file
                )
            )
        metadata = skill_dir / "agents/openai.yaml"
        if Path("agents/openai.yaml") in actual_files:
            checked_files.append(metadata)
            try:
                values, _allow_implicit = _validate_openai_metadata_text(
                    metadata.read_text(encoding="utf-8")
                )
                if "${}".format(name) not in values["default_prompt"]:
                    issues.append(
                        "Codex default prompt must invoke ${}: {}".format(name, name)
                    )
            except (OSError, UnicodeError, ValueError) as error:
                issues.append("{}: invalid OpenAI metadata: {}".format(metadata, error))
        try:
            issues.extend(_validate_relative_links(skill_file))
        except (OSError, UnicodeError) as error:
            issues.append("invalid project skill instructions {}: {}".format(skill_file, error))
    return issues, checked_files


def _expected_generated_managed_files(kind: str, selected: Sequence[str]) -> set:
    files = set()
    if kind == "project":
        files.update(
            {
                Path(".agents/README.md"),
                Path(".agents/generated-manifest.json"),
                Path(".agents/project-profile.md"),
                Path(".agents/memory/README.md"),
                Path(".agents/memory/candidates.jsonl"),
                Path(".agents/controls/README.md"),
                Path(".agents/controls/change-policy.example.json"),
                Path(".agents/controls/change-policy.json"),
                Path(".agents/controls/check_change_policy.py"),
                Path(".claude/CLAUDE.md"),
                Path(".claude/settings.json"),
                Path(".codex/config.toml"),
            }
        )
        files.update(Path(".agents/rules") / "{}.md".format(name) for name in STACK_NAMES)
        files.update(
            Path(".agents/skills") / name / relative
            for name in SKILL_NAMES
            for relative in (Path("SKILL.md"), Path("agents/openai.yaml"))
        )
        files.update(
            Path(".claude/skills") / name / "SKILL.md" for name in SKILL_NAMES
        )
        files.update(
            Path(".dsh/skills") / name / "SKILL.md" for name in EXPLICIT_SKILL_NAMES
        )
        return files

    if "codex" in selected:
        files.update({Path(".codex/AGENTS.md"), Path(".codex/config.toml")})
    if "claude" in selected:
        files.update({Path(".claude/CLAUDE.md"), Path(".claude/settings.json")})
        files.update(
            Path(".claude/skills") / name / "SKILL.md" for name in SKILL_NAMES
        )
    if "deepseek-harness" in selected:
        files.update({Path(".dsh/AGENTS.md"), Path(".dsh/README.md")})
    if "codex" in selected or "deepseek-harness" in selected:
        files.update(
            Path(".agents/skills") / name / relative
            for name in SKILL_NAMES
            for relative in (Path("SKILL.md"), Path("agents/openai.yaml"))
        )
        files.update(
            Path(".dsh/skills") / name / "SKILL.md" for name in EXPLICIT_SKILL_NAMES
        )
    return files


def _validate_generated_managed_allowlist(
    root: Path, kind: str, selected: Sequence[str]
) -> List[str]:
    allowed_files = _expected_generated_managed_files(kind, selected)
    allowed_directories = {
        parent
        for relative in allowed_files
        for parent in relative.parents
        if parent != Path(".")
    }
    issues: List[str] = []
    skill_roots = set()
    if kind == "project" or "codex" in selected or "deepseek-harness" in selected:
        skill_roots.add(Path(".agents/skills"))
        skill_roots.add(Path(".dsh/skills"))
    if kind == "project" or "claude" in selected:
        skill_roots.add(Path(".claude/skills"))

    def is_inside_skill_tree(relative: Path) -> bool:
        return any(
            relative == skill_root or skill_root in relative.parents
            for skill_root in skill_roots
        )

    for managed_name in (".agents", ".claude", ".codex", ".dsh"):
        managed_root = root / managed_name
        if not os.path.lexists(str(managed_root)):
            continue
        relative_root = Path(managed_name)
        if relative_root not in allowed_directories:
            issues.append(
                "unexpected generated managed directory: {}".format(managed_root)
            )
            continue
        for path in managed_root.rglob("*"):
            path_issue = _generated_path_safety_issue(root, path)
            if path_issue is not None:
                issues.append(path_issue)
                continue
            relative = path.relative_to(root)
            if is_inside_skill_tree(relative):
                continue
            if path.is_dir():
                if relative not in allowed_directories:
                    issues.append(
                        "unexpected generated managed directory: {}".format(path)
                    )
            elif not path.is_file() or relative not in allowed_files:
                issues.append("unexpected generated managed file: {}".format(path))
    return issues


def validate_generated(
    system_root: Path,
    kind: str,
    generated_root: Path,
    target: str = "all",
    require_ready_profile: bool = False,
) -> List[str]:
    """Validate one generated project tree or simulated user home."""

    system = _absolute_path(Path(system_root))
    try:
        root = _canonical_scope_path(Path(generated_root), "Generated root")
    except SafetyError as error:
        return [str(error)]
    issues: List[str] = []
    source_issues = validate_system(system)
    if source_issues:
        return ["source system invalid: {}".format(issue) for issue in source_issues]
    if root.is_symlink() or not root.is_dir():
        return ["generated root must be a regular directory: {}".format(root)]
    if kind not in ("project", "user"):
        return ["unknown generated kind: {}".format(kind)]
    if target not in tuple(USER_TARGETS) + ("all",):
        return ["unknown generated target: {}".format(target)]

    managed_path_issues = []
    for managed_name in (".agents", ".claude", ".codex", ".dsh"):
        managed_path = root / managed_name
        if not os.path.lexists(str(managed_path)):
            continue
        path_issue = _generated_path_safety_issue(root, managed_path)
        if path_issue is not None:
            managed_path_issues.append(path_issue)
        elif not managed_path.is_dir():
            managed_path_issues.append(
                "generated managed path is not a directory: {}".format(
                    managed_path
                )
            )
    if managed_path_issues:
        return managed_path_issues

    required_sources = {}
    checked_files: List[Path] = []
    selected = tuple(USER_TARGETS) if target == "all" else (target,)
    issues.extend(_validate_generated_managed_allowlist(root, kind, selected))
    if kind == "project":
        for shadow_name in PROJECT_ROOT_SHADOW_FILES:
            shadow_path = root / shadow_name
            if os.path.lexists(str(shadow_path)):
                issues.append(
                    "generated project must not contain root instruction shadow {}: {}".format(
                        shadow_name, shadow_path
                    )
                )
        required_sources = {
            Path("AGENTS.md"): Path("templates/project/AGENTS.md"),
            Path(".agents/README.md"): Path(
                "templates/project/.agents/README.md"
            ),
            Path(".agents/project-profile.md"): Path(
                "templates/project/.agents/project-profile.md"
            ),
            Path(".agents/memory/README.md"): Path(
                "templates/project/.agents/memory/README.md"
            ),
            Path(".agents/memory/candidates.jsonl"): Path(
                "templates/project/.agents/memory/candidates.jsonl"
            ),
            Path(".agents/controls/README.md"): Path(
                "templates/project/.agents/controls/README.md"
            ),
            Path(".agents/controls/change-policy.example.json"): Path(
                "templates/project/.agents/controls/change-policy.example.json"
            ),
            Path(".agents/controls/check_change_policy.py"): Path(
                "templates/project/.agents/controls/check_change_policy.py"
            ),
            Path(".claude/CLAUDE.md"): Path(
                "templates/project/.claude/CLAUDE.md"
            ),
            Path(".claude/settings.json"): Path(
                "templates/project/.claude/settings.json"
            ),
            Path(".codex/config.toml"): Path(
                "templates/project/.codex/config.toml"
            ),
        }
        generated_manifest = root / ".agents/generated-manifest.json"
        generated_stacks = None
        manifest_issue = _generated_path_safety_issue(root, generated_manifest)
        if manifest_issue is not None:
            issues.append(manifest_issue)
        elif not generated_manifest.is_file():
            issues.append("missing generated file: .agents/generated-manifest.json")
        else:
            checked_files.append(generated_manifest)
            try:
                manifest_value = _load_strict_json_text(
                    generated_manifest.read_text(encoding="utf-8")
                )
                if not isinstance(manifest_value, dict) or set(manifest_value) != {
                    "schema_version",
                    "generator_revision",
                    "stacks",
                }:
                    raise ValueError("unexpected project manifest fields")
                if manifest_value["schema_version"] != "1":
                    raise ValueError("unsupported project manifest schema_version")
                if manifest_value["generator_revision"] != PROJECT_MANIFEST_REVISION:
                    raise ValueError("unsupported project generator_revision")
                generated_stacks = manifest_value["stacks"]
                if (
                    not isinstance(generated_stacks, list)
                    or any(not isinstance(item, str) for item in generated_stacks)
                    or generated_stacks != sorted(set(generated_stacks))
                    or not set(generated_stacks).issubset(STACK_NAMES)
                ):
                    raise ValueError("project manifest stacks must be sorted known names")
            except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
                issues.append("invalid generated project manifest: {}".format(error))
                generated_stacks = None
        if generated_stacks is not None:
            rules_root = root / ".agents/rules"
            actual_stacks = set()
            if rules_root.is_dir() and not rules_root.is_symlink():
                actual_stacks = {
                    path.stem
                    for path in rules_root.iterdir()
                    if path.is_file()
                    and not path.is_symlink()
                    and path.suffix == ".md"
                    and path.stem in STACK_NAMES
                }
            if actual_stacks != set(generated_stacks):
                issues.append(
                    "generated stack rules do not match manifest: expected {}; actual {}".format(
                        ", ".join(generated_stacks) or "none",
                        ", ".join(sorted(actual_stacks)) or "none",
                    )
                )
            for stack in generated_stacks:
                rule = root / ".agents/rules/{}.md".format(stack)
                if not rule.is_file() or rule.is_symlink():
                    issues.append("missing generated stack rule: {}".format(stack))
        agents_path = root / "AGENTS.md"
        if (
            _generated_path_safety_issue(root, agents_path) is None
            and agents_path.is_file()
        ):
            try:
                actual_core = _extract_shared_block(agents_path)
                expected_core = _canonical_shared_content(
                    system / "templates/shared/project-core.md"
                )
                if actual_core != expected_core:
                    issues.append("generated project shared core drift: AGENTS.md")
                if generated_stacks is not None:
                    expected_agents = _render_managed_module_routes(
                        system / "templates/project/AGENTS.md", generated_stacks
                    )
                    if agents_path.read_bytes() != expected_agents:
                        issues.append("generated managed module routes drift: AGENTS.md")
            except (OSError, UnicodeError, ValueError, SafetyError) as error:
                    issues.append("generated AGENTS.md: {}".format(error))
        profile_path = root / ".agents/project-profile.md"
        if (
            _generated_path_safety_issue(root, profile_path) is None
            and profile_path.is_file()
        ):
            expected_profile_preamble = None
            try:
                _template_frontmatter, template_body_lines = (
                    _parse_strict_profile_frontmatter(
                        (
                            system
                            / "templates/project/.agents/project-profile.md"
                        ).read_text(encoding="utf-8")
                    )
                )
                expected_profile_preamble = _profile_preamble(template_body_lines)
            except (OSError, UnicodeError, ValueError):
                pass
            issues.extend(
                _validate_project_profile(
                    profile_path,
                    require_ready_profile,
                    expected_profile_preamble,
                )
            )
        memory_path = root / ".agents/memory/candidates.jsonl"
        if (
            _generated_path_safety_issue(root, memory_path) is None
            and memory_path.is_file()
        ):
            issues.extend(_validate_memory_candidates(memory_path))
        actual_policy = root / ".agents/controls/change-policy.json"
        if os.path.lexists(str(actual_policy)):
            policy_issue = _generated_path_safety_issue(root, actual_policy)
            if policy_issue is not None:
                issues.append(policy_issue)
            elif not actual_policy.is_file():
                issues.append("generated actual change policy is not a regular file")
            else:
                try:
                    _validate_change_policy_file(actual_policy)
                except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
                    issues.append("invalid generated change-policy.json: {}".format(error))
        claude_path = root / ".claude/CLAUDE.md"
        if (
            _generated_path_safety_issue(root, claude_path) is None
            and claude_path.is_file()
        ):
            try:
                logical = [
                    line.strip()
                    for line in claude_path.read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
            except (OSError, UnicodeError) as error:
                issues.append("generated .claude/CLAUDE.md: {}".format(error))
            else:
                if not logical or logical[0] != "@../AGENTS.md":
                    issues.append(
                        "generated .claude/CLAUDE.md must import @../AGENTS.md first"
                    )
        skill_specs = (
            (root / ".agents/skills", SKILL_NAMES, "canonical"),
            (root / ".claude/skills", SKILL_NAMES, "adapter"),
            (
                root / ".dsh/skills",
                EXPLICIT_SKILL_NAMES,
                "adapter",
            ),
        )
        rules_root = root / ".agents/rules"
        if os.path.lexists(str(rules_root)):
            rules_issue = _generated_path_safety_issue(root, rules_root)
            if rules_issue is not None:
                issues.append(rules_issue)
            elif not rules_root.is_dir():
                issues.append("generated rules root is not a regular directory")
            else:
                allowed_rules = {"{}.md".format(name) for name in STACK_NAMES}
                for path in rules_root.iterdir():
                    path_issue = _generated_path_safety_issue(root, path)
                    if path_issue is not None:
                        issues.append(path_issue)
                    elif not path.is_file():
                        issues.append("invalid generated rule entry: {}".format(path))
                    elif path.name not in allowed_rules:
                        issues.append("unexpected generated rule: {}".format(path))
                    else:
                        checked_files.append(path)
                        source_rule = system / "templates/modules" / path.name
                        if path.read_bytes() != source_rule.read_bytes():
                            issues.append(
                                "generated rule content drift: {}".format(path)
                            )
    else:
        if "codex" in selected:
            required_sources.update(
                {
                    Path(".codex/AGENTS.md"): Path(
                        "templates/user/codex/AGENTS.md"
                    ),
                    Path(".codex/config.toml"): Path(
                        "templates/user/codex/config.toml"
                    ),
                }
            )
        if "claude" in selected:
            required_sources.update(
                {
                    Path(".claude/CLAUDE.md"): Path(
                        "templates/user/claude/CLAUDE.md"
                    ),
                    Path(".claude/settings.json"): Path(
                        "templates/user/claude/settings.json"
                    ),
                }
            )
        if "deepseek-harness" in selected:
            required_sources.update(
                {
                    Path(".dsh/AGENTS.md"): Path(
                        "templates/user/deepseek-harness/AGENTS.md"
                    ),
                    Path(".dsh/README.md"): Path(
                        "templates/user/deepseek-harness/README.md"
                    ),
                }
            )
        skill_specs_list = []
        if "codex" in selected or "deepseek-harness" in selected:
            skill_specs_list.append(
                (root / ".agents/skills", SKILL_NAMES, "canonical")
            )
        if "claude" in selected:
            skill_specs_list.append(
                (root / ".claude/skills", SKILL_NAMES, "adapter")
            )
        if "codex" in selected or "deepseek-harness" in selected:
            skill_specs_list.append(
                (
                    root / ".dsh/skills",
                    EXPLICIT_SKILL_NAMES,
                    "adapter",
                )
            )
        skill_specs = tuple(skill_specs_list)
        expected_core = _canonical_shared_content(
            system / "templates/shared/user-core.md"
        )
        for relative in (
            Path(".codex/AGENTS.md") if "codex" in selected else None,
            Path(".claude/CLAUDE.md") if "claude" in selected else None,
            Path(".dsh/AGENTS.md") if "deepseek-harness" in selected else None,
        ):
            if relative is None:
                continue
            generated_path = root / relative
            if (
                _generated_path_safety_issue(root, generated_path) is not None
                or not generated_path.is_file()
            ):
                continue
            try:
                if _extract_shared_block(generated_path) != expected_core:
                    issues.append("generated user shared core drift: {}".format(relative))
            except (OSError, UnicodeError, ValueError) as error:
                issues.append("generated {}: {}".format(relative, error))

    for relative, source_relative in required_sources.items():
        path = root / relative
        path_issue = _generated_path_safety_issue(root, path)
        if path_issue is not None:
            issues.append(path_issue)
        elif not path.is_file():
            issues.append("missing generated file: {}".format(relative.as_posix()))
        else:
            checked_files.append(path)
            dynamic_project_files = {
                Path("AGENTS.md"),
                Path(".agents/project-profile.md"),
                Path(".agents/memory/candidates.jsonl"),
            }
            if (
                not (kind == "project" and relative in dynamic_project_files)
                and path.read_bytes() != (system / source_relative).read_bytes()
            ):
                issues.append(
                    "generated file content drift: {}".format(
                        relative.as_posix()
                    )
                )
            if kind == "project" and relative == Path(".codex/config.toml"):
                try:
                    _validate_comments_only_toml(path)
                except (OSError, UnicodeError, ValueError) as error:
                    issues.append(
                        "generated .codex/config.toml {}".format(error)
                    )
    for tree_root, expected_names, mode in skill_specs:
        tree_issues, tree_files = _validate_generated_skill_tree(
            system,
            root,
            tree_root,
            expected_names,
            mode,
            allow_project_extensions=(kind == "project" and mode == "canonical"),
        )
        issues.extend(tree_issues)
        checked_files.extend(tree_files)
    for path in checked_files:
        if path.suffix == ".json":
            try:
                _load_strict_json_text(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
                issues.append("invalid generated JSON {}: {}".format(path, error))
        elif path.suffix == ".toml":
            try:
                _validate_basic_toml(path)
            except (OSError, UnicodeError, ValueError) as error:
                issues.append("invalid generated TOML {}: {}".format(path, error))
    return issues


def _print_result(result: OperationResult) -> None:
    print("APPLIED" if result.applied else "DRY-RUN")
    if result.destination_paths:
        for display_path, destination_path in zip(
            result.planned_paths, result.destination_paths
        ):
            print("{} -> {}".format(display_path, destination_path))
    else:
        for path in result.planned_paths:
            print(path)
    for path in result.backup_paths:
        print("BACKUP {}".format(path))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize and validate the coding-agent configuration kit."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-project")
    init_parser.add_argument("destination", type=Path)
    init_parser.add_argument("--stack", action="append", default=[], choices=STACK_NAMES)
    init_parser.add_argument("--apply", action="store_true")

    install_parser = subparsers.add_parser("install-user")
    install_parser.add_argument(
        "--target", required=True, choices=tuple(USER_TARGETS) + ("all",)
    )
    install_parser.add_argument("--home", type=Path)
    install_parser.add_argument("--backup-dir", type=Path)
    install_parser.add_argument("--apply", action="store_true")

    render_parser = subparsers.add_parser("render-templates")
    render_parser.add_argument("--apply", action="store_true")

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("path", nargs="?", type=Path, default=SYSTEM_ROOT)

    generated_parser = subparsers.add_parser("validate-generated")
    generated_parser.add_argument("--kind", required=True, choices=("project", "user"))
    generated_parser.add_argument("--root", required=True, type=Path)
    generated_parser.add_argument(
        "--target", choices=tuple(USER_TARGETS) + ("all",), default="all"
    )
    generated_parser.add_argument("--require-ready-profile", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "init-project":
            result = init_project(
                SYSTEM_ROOT,
                arguments.destination,
                arguments.stack,
                arguments.apply,
            )
            _print_result(result)
            return 0
        if arguments.command == "install-user":
            result = install_user(
                SYSTEM_ROOT,
                arguments.target,
                arguments.home,
                arguments.backup_dir,
                arguments.apply,
            )
            _print_result(result)
            return 0
        if arguments.command == "render-templates":
            result = render_templates(SYSTEM_ROOT, arguments.apply)
            _print_result(result)
            return 0
        if arguments.command == "validate-generated":
            issues = validate_generated(
                SYSTEM_ROOT,
                arguments.kind,
                arguments.root,
                arguments.target,
                arguments.require_ready_profile,
            )
            if issues:
                for issue in issues:
                    print("ERROR {}".format(issue))
                return 1
            print("VALID-GENERATED")
            return 0
        issues = validate_system(arguments.path)
        if issues:
            for issue in issues:
                print("ERROR {}".format(issue))
            return 1
        print("VALID")
        return 0
    except (SafetyError, OSError, ValueError) as error:
        print("ERROR {}".format(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
