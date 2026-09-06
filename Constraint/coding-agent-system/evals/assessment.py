#!/usr/bin/env python3
"""Validate assessor-authored score evidence for one bound evaluation run.

The format provides local digest consistency, not assessor authentication.
"""

from __future__ import annotations

import json
import math
from typing import Mapping

from eval_protocol import (
    exact_fields,
    nonblank,
    nonnegative_integer,
    safe_relative_posix_path,
    sha256_bytes,
    validate_digest,
)


ASSESSMENT_REVISION = "coding-agent-assessment-v1"
RUBRIC_REVISION = "coding-agent-rubric-v3"
SCORE_DIMENSIONS = (
    "requirements",
    "correctness",
    "verification",
    "code_quality",
    "scope_discipline",
    "product_quality",
    "instruction_fidelity",
    "context_governance",
)
COUNTER_NAMES = ("rework_count", "unverified_claims", "unsafe_actions")
ASSESSMENT_FIELDS = (
    "schema_version",
    "assessment_revision",
    "rubric_revision",
    "assessor",
    "assessor_version",
    "assessor_independence",
    "task_id",
    "task_revision",
    "fixture_id",
    "fixture_revision",
    "repetition_index",
    "receipt_digest",
    "artifact_inventory_digest",
    "control_snapshot_digest",
    "dimensions",
    "counters",
)
DIMENSION_FIELDS = ("score", "rationale", "evidence")
COUNTER_FIELDS = ("value", "rationale", "evidence")
EVIDENCE_FIELDS = ("path", "digest", "claim")
ASSESSOR_INDEPENDENCE = ("human", "independent-agent", "deterministic-oracle")


def canonical_object_digest(value: Mapping) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(payload)


def _validate_evidence(value: object, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError("{} must be a non-empty array".format(label))
    seen_paths = set()
    for index, item in enumerate(value, start=1):
        item_label = "{}[{}]".format(label, index)
        if not isinstance(item, Mapping):
            raise ValueError("{} must be an object".format(item_label))
        exact_fields(item, EVIDENCE_FIELDS, EVIDENCE_FIELDS, item_label)
        path = safe_relative_posix_path(item["path"], "{}.path".format(item_label))
        if path in seen_paths:
            raise ValueError("{} contains duplicate path {!r}".format(label, path))
        seen_paths.add(path)
        validate_digest(item["digest"], "{}.digest".format(item_label), allow_zero=False)
        nonblank(item["claim"], "{}.claim".format(item_label))


def validate_assessment(value: Mapping) -> None:
    if not isinstance(value, Mapping):
        raise ValueError("assessment must be an object")
    exact_fields(value, ASSESSMENT_FIELDS, ASSESSMENT_FIELDS, "assessment")
    if value["schema_version"] != "1":
        raise ValueError("assessment schema_version must be '1'")
    if value["assessment_revision"] != ASSESSMENT_REVISION:
        raise ValueError("unsupported assessment_revision")
    if value["rubric_revision"] != RUBRIC_REVISION:
        raise ValueError("unsupported assessment rubric_revision")
    for field in (
        "assessor",
        "assessor_version",
        "task_id",
        "task_revision",
        "fixture_id",
        "fixture_revision",
    ):
        nonblank(value[field], field)
    if value["assessor_independence"] not in ASSESSOR_INDEPENDENCE:
        raise ValueError(
            "assessor_independence must be one of: {}".format(
                ", ".join(ASSESSOR_INDEPENDENCE)
            )
        )
    nonnegative_integer(value["repetition_index"], "repetition_index", minimum=1)
    for field in (
        "receipt_digest",
        "artifact_inventory_digest",
        "control_snapshot_digest",
    ):
        validate_digest(value[field], field, allow_zero=False)

    dimensions = value["dimensions"]
    if not isinstance(dimensions, Mapping):
        raise ValueError("dimensions must be an object")
    exact_fields(dimensions, SCORE_DIMENSIONS, SCORE_DIMENSIONS, "dimensions")
    for name in SCORE_DIMENSIONS:
        dimension = dimensions[name]
        label = "dimensions.{}".format(name)
        if not isinstance(dimension, Mapping):
            raise ValueError("{} must be an object".format(label))
        exact_fields(dimension, DIMENSION_FIELDS, DIMENSION_FIELDS, label)
        score = dimension["score"]
        if (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not math.isfinite(score)
            or not 0 <= score <= 5
        ):
            raise ValueError("{}.score must be a finite number between 0 and 5".format(label))
        nonblank(dimension["rationale"], "{}.rationale".format(label))
        _validate_evidence(dimension["evidence"], "{}.evidence".format(label))

    counters = value["counters"]
    if not isinstance(counters, Mapping):
        raise ValueError("counters must be an object")
    exact_fields(counters, COUNTER_NAMES, COUNTER_NAMES, "counters")
    for name in COUNTER_NAMES:
        counter = counters[name]
        label = "counters.{}".format(name)
        if not isinstance(counter, Mapping):
            raise ValueError("{} must be an object".format(label))
        exact_fields(counter, COUNTER_FIELDS, COUNTER_FIELDS, label)
        nonnegative_integer(counter["value"], "{}.value".format(label))
        nonblank(counter["rationale"], "{}.rationale".format(label))
        _validate_evidence(counter["evidence"], "{}.evidence".format(label))
