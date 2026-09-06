#!/usr/bin/env python3
"""Validate explicit changed paths against an opt-in project policy."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


POLICY_FIELDS = frozenset(
    {"schema_version", "protected_paths", "linked_change_groups"}
)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: {}".format(key))
        result[key] = value
    return result


def reject_symlink_ancestors(path):
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[len(current.parts) :]:
        current = current / part
        if os.path.lexists(os.fspath(current)) and current.is_symlink():
            raise ValueError("policy must not contain a symlink: {}".format(current))


def valid_path(value):
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


def load_policy(path):
    try:
        reject_symlink_ancestors(path)
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError("invalid policy: {}".format(error))
    if not isinstance(value, dict) or set(value) != POLICY_FIELDS:
        raise ValueError("policy has unexpected fields")
    if value["schema_version"] != "1":
        raise ValueError("unsupported schema_version")
    protected = value["protected_paths"]
    groups = value["linked_change_groups"]
    if not isinstance(protected, list) or not isinstance(groups, list):
        raise ValueError("policy paths must be lists")
    normalized_protected = [valid_path(item) for item in protected]
    if len(set(normalized_protected)) != len(normalized_protected):
        raise ValueError("policy contains duplicate paths")
    seen_paths = set(normalized_protected)
    normalized_groups = []
    for group in groups:
        if not isinstance(group, list) or len(group) < 2:
            raise ValueError("linked group must contain at least two paths")
        normalized = [valid_path(item) for item in group]
        if len(set(normalized)) != len(normalized):
            raise ValueError("linked group contains duplicate paths")
        if seen_paths.intersection(normalized):
            raise ValueError("policy contains duplicate paths")
        seen_paths.update(normalized)
        normalized_groups.append(normalized)
    return normalized_protected, normalized_groups


def matches(path, prefix):
    return path == prefix or path.startswith(prefix + "/")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("changed_paths", nargs="+")
    args = parser.parse_args(argv)
    try:
        protected, groups = load_policy(args.policy)
        changed = [valid_path(item) for item in args.changed_paths]
        if len(set(changed)) != len(changed):
            raise ValueError("changed paths contain duplicates")
        violations = []
        for path in changed:
            if any(matches(path, prefix) for prefix in protected):
                violations.append("protected path: {}".format(path))
        for group in groups:
            present = [prefix for prefix in group if any(matches(path, prefix) for path in changed)]
            if present and len(present) != len(group):
                violations.append(
                    "linked change group incomplete: {}".format(", ".join(group))
                )
        print(
            json.dumps(
                {"allowed": not violations, "violations": violations},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0 if not violations else 1
    except ValueError as error:
        print(
            json.dumps(
                {"allowed": False, "error": str(error), "violations": []},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
