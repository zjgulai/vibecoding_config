#!/usr/bin/env python3
"""Shared fail-closed helpers for the local evaluation control plane."""

from __future__ import annotations

import hashlib
import json
import math
import re
import stat
from pathlib import Path, PurePosixPath
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
EVIDENCE_SCOPES = ("representative", "synthetic-harness-only")


def _object_without_duplicate_keys(pairs: Iterable[Tuple[str, object]]) -> Dict:
    result: Dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {!r}".format(key))
        result[key] = value
    return result


def load_json(path: Path) -> object:
    """Load strict JSON, rejecting duplicate object keys at every depth."""

    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError("invalid JSON numeric constant: {}".format(value))
            ),
        )
    except json.JSONDecodeError as error:
        raise ValueError("{}: {}".format(path, error)) from error


def exact_fields(
    value: Mapping, required: Sequence[str], allowed: Sequence[str], label: str
) -> None:
    missing = [field for field in required if field not in value]
    if missing:
        raise ValueError("{} missing required fields: {}".format(label, ", ".join(missing)))
    unexpected = sorted(str(field) for field in value if field not in allowed)
    if unexpected:
        raise ValueError("{} has unexpected fields: {}".format(label, ", ".join(unexpected)))


def nonblank(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("{} must be a non-blank string".format(label))
    return value


def validate_evidence_scope(value: object, label: str) -> str:
    """Return one explicitly declared evidence scope or fail closed."""

    scope = nonblank(value, label)
    if scope not in EVIDENCE_SCOPES:
        raise ValueError(
            "{} must be one of: {}".format(label, ", ".join(EVIDENCE_SCOPES))
        )
    return scope


def safe_relative_posix_path(value: object, label: str) -> str:
    """Return a portable relative path that cannot switch drive or traverse parents."""

    path = nonblank(value, label)
    raw_parts = path.split("/")
    if (
        PurePosixPath(path).is_absolute()
        or "\\" in path
        or ":" in path
        or "\x00" in path
        or any(part in ("", ".", "..") for part in raw_parts)
    ):
        raise ValueError("{} must be a safe relative POSIX path".format(label))
    return path


def validate_digest(value: object, label: str, allow_zero: bool = True) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise ValueError("{} must use sha256:<64 lowercase hex>".format(label))
    if not allow_zero and value == "sha256:" + ("0" * 64):
        raise ValueError("{} must not use the all-zero sentinel digest".format(label))
    return value


def nonnegative_integer(value: object, label: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError("{} must be an integer >= {}".format(label, minimum))
    return value


def optional_number(value: object, label: str) -> Optional[float]:
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


def optional_integer(value: object, label: str) -> Optional[int]:
    if value is None:
        return None
    return nonnegative_integer(value, label)


def argv(value: object, label: str) -> List[str]:
    if not isinstance(value, list) or not value:
        raise ValueError("{} must be a non-empty argv array".format(label))
    for index, argument in enumerate(value):
        nonblank(argument, "{}[{}]".format(label, index))
    return value


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError("path is not a regular file: {}".format(path))
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return "sha256:" + hasher.hexdigest()


def _entry_mode(path: Path) -> str:
    return "{:03o}".format(stat.S_IMODE(path.lstat().st_mode) & 0o111)


def tree_entries(
    root: Path, *, exclude_git: bool = True
) -> List[Tuple[str, str, str, Optional[str]]]:
    """Return sorted sha256-tree-v2 entries below *root*."""

    if root.is_symlink():
        raise ValueError("tree root must not be a symlink: {}".format(root))
    if not root.exists() or not root.is_dir():
        raise ValueError("tree root is not a directory: {}".format(root))

    entries: List[Tuple[str, str, str, Optional[str]]] = []
    for path in root.rglob("*"):
        relative_path = path.relative_to(root)
        if exclude_git and ".git" in relative_path.parts:
            continue
        relative = relative_path.as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError("tree contains symlink: {}".format(relative))
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", _entry_mode(path), None))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", _entry_mode(path), sha256_file(path)))
        else:
            raise ValueError("tree contains non-regular entry: {}".format(relative))
    return sorted(entries, key=lambda item: item[0])


def tree_digest_v2(root: Path, *, exclude_git: bool = True) -> str:
    """Hash path, entry type, executable bits, empty directories, and file contents."""

    hasher = hashlib.sha256()
    hasher.update(b"sha256-tree-v2\0")
    for relative, kind, executable_bits, content_digest in tree_entries(
        root, exclude_git=exclude_git
    ):
        hasher.update(kind.encode("ascii"))
        hasher.update(b"\0")
        hasher.update(relative.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(executable_bits.encode("ascii"))
        hasher.update(b"\0")
        if content_digest is not None:
            hasher.update(content_digest.encode("ascii"))
        hasher.update(b"\0")
    return "sha256:" + hasher.hexdigest()


def artifact_tree_digest_v2(root: Path) -> str:
    """Hash the complete artifact tree, including every `.git` path."""

    return tree_digest_v2(root, exclude_git=False)


def _artifact_is_non_empty(path: Path) -> bool:
    if path.is_file() and not path.is_symlink():
        return path.stat().st_size > 0
    if path.is_dir() and not path.is_symlink():
        return next(path.iterdir(), None) is not None
    return False


def verify_artifact_contract(contract: Mapping, artifact_root: Path) -> List[str]:
    """Return current artifact contract violations without trusting a receipt flag."""

    errors: List[str] = []
    for item in contract["required"]:
        declared = item["path"]
        if item["kind"] == "glob":
            matches = list(artifact_root.glob(declared))
            if not matches:
                errors.append("required glob has no matches: {}".format(declared))
            elif any(path.is_symlink() for path in matches):
                errors.append("required glob contains a symlink: {}".format(declared))
            elif item["non_empty"] and any(
                not _artifact_is_non_empty(path) for path in matches
            ):
                errors.append("required glob contains an empty entry: {}".format(declared))
            continue
        path = artifact_root.joinpath(*declared.split("/"))
        expected_kind = path.is_file() if item["kind"] == "file" else path.is_dir()
        if path.is_symlink() or not expected_kind:
            errors.append("required {} is missing: {}".format(item["kind"], declared))
        elif item["non_empty"] and not _artifact_is_non_empty(path):
            errors.append("required artifact is empty: {}".format(declared))
    for pattern in contract["forbidden"]:
        if list(artifact_root.glob(pattern)):
            errors.append("forbidden artifact exists: {}".format(pattern))
    return errors


def resolve_relative_without_symlinks(base: Path, relative: str, label: str) -> Path:
    safe_relative_posix_path(relative, label)
    current = base.resolve()
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("{} path contains symlink: {}".format(label, current))
    try:
        current.resolve().relative_to(base.resolve())
    except ValueError as error:
        raise ValueError("{} escapes its declared root".format(label)) from error
    return current
