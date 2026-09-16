# EVAL-02 纯本地合成 Fixture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 EVAL-02 建立一个可重复运行的纯本地合成 fixture，用来验证 lifecycle、证据绑定和 harness comparison，同时从协议层杜绝把它表述为真实 Agent 或质量证据。

**Architecture:** 先把 `evidence_scope` 设为 manifest、receipt、record、score、compare 的强制绑定字段；`representative` 继续保留当前 11 项 task contract 与既有质量比较语义，`synthetic-harness-only` 只允许一个 EVAL-02 ready fixture。随后交付一个只调用 Python 标准库的 fixture 与两个确定性配置，并用独立的 pair runner 在临时 staging 副本中运行，避免测试或常规执行改写仓库内 shipped fixture。

**Tech Stack:** Python 3.9+ 标准库、`unittest`、严格 JSON、`sha256-tree-v2`、现有 lifecycle/receipt/score/compare CLI。

## Global Constraints

- 仅实现 `02-vertical-full-stack-feature`；不得把合成 fixture 合并进 `fixture-manifest.example.json` 的代表性 11 任务集合。
- manifest、receipt 与 run record 的 scope 仅允许 `representative` 或 `synthetic-harness-only`；未声明、漂移或混合 scope 必须 fail closed。
- 代表性 manifest 仍必须恰好包含现有 11 个 task，且当前全部保持 `contract-only`；其评分与质量比较语义不得改变。
- synthetic manifest 只能包含一个 `02-vertical-full-stack-feature` ready fixture，且 score 不得产生质量分、最终分、晋升资格、排序、优胜者或因果结论。
- 不新增第三方依赖，不联网，不读取凭据，不调用 provider、MCP、浏览器、数据库、生产系统、git commit、push、merge 或 deploy。
- `fixture-control` 只可删除已解析并验证位于 fixture root 内的固定 `workspace/`；不得从 argv、环境变量或配置读取删除目标。
- 运行产物必须位于调用者显式给出的空输出目录；测试必须在 `TemporaryDirectory` 下的 staging 副本中运行，不能修改仓库内的 shipped workspace。
- 所有实现遵循 test-first：先观察失败，再写最小实现，再重跑同一测试；本计划不要求或授权提交 Git commit。

---

## 文件责任图

| 文件 | 责任 |
| --- | --- |
| `Constraint/coding-agent-system/evals/eval_protocol.py` | 定义跨 manifest / receipt / record 共用的 evidence-scope 枚举与严格校验器。 |
| `Constraint/coding-agent-system/evals/validate_fixture.py`、`fixture-manifest.schema.json` | 按 scope 校验 manifest 版本、固定 task 集合与 fixture structure。 |
| `Constraint/coding-agent-system/evals/fixture-manifest.example.json` | 明确标记为 `representative`，保留 11 个 `contract-only` contract。 |
| `Constraint/coding-agent-system/evals/receipt.py`、`execution-receipt.schema.json`、`run_lifecycle.py` | 将 manifest scope 写入并绑定到 receipt，向显式 agent argv 传入已解析的 configuration root。 |
| `Constraint/coding-agent-system/evals/score.py`、`run-record.schema.json` | 把 record scope 绑定到 manifest/receipt；对 synthetic record 返回无质量语义的结果。 |
| `Constraint/coding-agent-system/evals/compare.py` | 保留 representative quality comparison；为 synthetic 提供只验证 lifecycle 与控制变量的 comparison。 |
| `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/` | EVAL-02 的固定可审计本地 fixture、基线、工作区、stub 与 oracle。 |
| `Constraint/coding-agent-system/evals/synthetic-configurations/02-vertical-full-stack-feature/` | 唯一变量为 baseline/candidate mode 与 candidate Envelope 的两个配置根。 |
| `Constraint/coding-agent-system/evals/fixture-manifest.synthetic.json` | 唯一 synthetic-harness-only ready contract。 |
| `Constraint/coding-agent-system/evals/run_synthetic_pair.py` | 复制输入到本地 staging，运行一组 baseline/candidate，并写入 declared records 与无质量 comparison。 |
| `Constraint/coding-agent-system/evals/test_*.py` | 协议、runner、score/compare、fixture staging 和 source-mutation guard 的回归测试。 |
| `Constraint/coding-agent-system/evals/README.md`、`tasks/02-vertical-full-stack-feature.md` | 记录 synthetic 与 representative 的证据边界和精确本地调用方式。 |

### Task 1: 将 evidence scope 设为严格的 manifest 合约

**Files:**
- Modify: `Constraint/coding-agent-system/evals/eval_protocol.py`
- Modify: `Constraint/coding-agent-system/evals/validate_fixture.py`
- Modify: `Constraint/coding-agent-system/evals/fixture-manifest.schema.json`
- Modify: `Constraint/coding-agent-system/evals/fixture-manifest.example.json`
- Modify: `Constraint/coding-agent-system/evals/test_fixture_manifest.py`

**Interfaces:**
- Produces: `EVIDENCE_SCOPES = ("representative", "synthetic-harness-only")` and `validate_evidence_scope(value: object, label: str) -> str` in `eval_protocol.py`.
- Produces: `MANIFEST_SCHEMA_VERSION = "2"`, `SYNTHETIC_HARNESS_TASK_IDS = ("02-vertical-full-stack-feature",)` and a scope-aware `validate_manifest_structure(manifest: Mapping) -> None`.
- Consumes: existing `TASK_IDS`, `FIXTURE_FIELDS`, strict JSON loading, safe-relative path and digest validators.

- [x] **Step 1: 写出 scope/cardinality 的失败测试**

在 `test_fixture_manifest.py` 中让 `make_manifest` 接受 `evidence_scope: str = "representative"`，默认产生 `schema_version: "2"` 和顶层 `evidence_scope`。新增下面两个覆盖面明确的测试；前者验证代表性集合不能缩小，后者验证 synthetic 只能是 EVAL-02 的单项集合。

```python
def test_representative_scope_still_requires_all_eleven_tasks(self) -> None:
    manifest = make_manifest(evidence_scope="representative")
    manifest["fixtures"] = manifest["fixtures"][:1]
    with self.assertRaisesRegex(ValueError, "exactly eleven"):
        validate_fixture.validate_manifest_structure(manifest)


def test_synthetic_scope_accepts_only_the_single_eval_02_contract(self) -> None:
    manifest = make_manifest(evidence_scope="synthetic-harness-only")
    manifest["fixtures"] = [manifest["fixtures"][1]]
    validate_fixture.validate_manifest_structure(manifest)

    invalid = make_manifest(evidence_scope="synthetic-harness-only")
    invalid["fixtures"] = [invalid["fixtures"][2]]
    with self.assertRaisesRegex(ValueError, "02-vertical-full-stack-feature"):
        validate_fixture.validate_manifest_structure(invalid)
```

- [x] **Step 2: 运行新测试，确认当前协议尚不支持该字段**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_fixture_manifest.FixtureManifestTests.test_evidence_scope_partitions_fixture_cardinality -v
```

Expected: FAIL，原因是现有 strict top-level contract 不允许 `evidence_scope`，或现有 schema version 仍要求 `"1"`。

- [x] **Step 3: 实现共享 scope validator 与 scope-aware manifest 验证**

在 `eval_protocol.py` 增加精确枚举校验，不允许默认值或未知字符串；在 `validate_fixture.py` 令 manifest schema 升为 `"2"`，并按 scope 选择期望 task 集合。实现必须保留每个 fixture 的既有字段、固定 argv、root 安全性、artifact contract 和 ready digest 检查。

```python
# eval_protocol.py
EVIDENCE_SCOPES = ("representative", "synthetic-harness-only")


def validate_evidence_scope(value: object, label: str) -> str:
    scope = nonblank(value, label)
    if scope not in EVIDENCE_SCOPES:
        raise ValueError("{} must be one of: {}".format(label, ", ".join(EVIDENCE_SCOPES)))
    return scope


# validate_fixture.py
MANIFEST_SCHEMA_VERSION = "2"
SYNTHETIC_HARNESS_TASK_IDS = ("02-vertical-full-stack-feature",)
TOP_LEVEL_FIELDS = (
    "schema_version", "manifest_revision", "evidence_scope", "digest_contract", "fixtures"
)

scope = validate_evidence_scope(manifest["evidence_scope"], "evidence_scope")
expected_task_ids = TASK_IDS if scope == "representative" else SYNTHETIC_HARNESS_TASK_IDS
if len(fixtures) != len(expected_task_ids):
    raise ValueError("fixtures must contain exactly {} task contracts".format(len(expected_task_ids)))
if seen_tasks != set(expected_task_ids):
    raise ValueError("fixtures do not match the allowed task set for {}".format(scope))
```

让 `validate_manifest(manifest: Mapping, manifest_path: Path, allow_contract_only: bool = False)` 的 JSON 结果新增 `evidence_scope`，使 CLI 结果可审计但不执行任何 fixture command。

- [x] **Step 4: 同步 JSON Schema 与 example manifest**

把 `fixture-manifest.schema.json` 的 required/properties 增加 `evidence_scope`，将 `schema_version` const 改为 `"2"`，并使用下列不允许扩展值的定义。

```json
"evidence_scope": {
  "enum": ["representative", "synthetic-harness-only"]
}
```

将 `fixture-manifest.example.json` 的顶层字段改为：

```json
"schema_version": "2",
"evidence_scope": "representative"
```

保留其中 11 个 fixture、每个 `contract-only` readiness、revision、root、fixed lifecycle argv 与 `initial_state_digest: null`，不创建 ready representative fixture。

- [x] **Step 5: 补全 schema/runtime 一致性与未知 scope 的测试**

新增覆盖，确保 JSON Schema 的 required/properties 与 `validate_fixture.TOP_LEVEL_FIELDS` 一致，并拒绝没有 scope、未知 scope、代表性单项、synthetic 两项和 synthetic 非 EVAL-02。

```python
for value in (None, "", "model-quality", "representative-plus-synthetic"):
    manifest = make_manifest()
    if value is None:
        del manifest["evidence_scope"]
    else:
        manifest["evidence_scope"] = value
    with self.subTest(value=value):
        with self.assertRaisesRegex(ValueError, "evidence_scope"):
            validate_fixture.validate_manifest_structure(manifest)
```

- [x] **Step 6: 运行 manifest 测试并确认代表性静态入口未变为可运行**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_fixture_manifest -v
python3 validate_fixture.py --allow-contract-only fixture-manifest.example.json
python3 validate_fixture.py fixture-manifest.example.json
```

Expected: 单元测试通过；`--allow-contract-only` 返回 `evidence_scope: representative` 和 `tree_contract_valid: false`；最后一条因 `contract-only` 非零退出，不得执行任何 lifecycle command。

### Task 2: 将 scope 和 configuration root 绑定进 lifecycle receipt 与 record

**Files:**
- Modify: `Constraint/coding-agent-system/evals/receipt.py`
- Modify: `Constraint/coding-agent-system/evals/execution-receipt.schema.json`
- Modify: `Constraint/coding-agent-system/evals/run_lifecycle.py`
- Modify: `Constraint/coding-agent-system/evals/run-record.schema.json`
- Modify: `Constraint/coding-agent-system/evals/example-run.json`
- Modify: `Constraint/coding-agent-system/evals/test_lifecycle_runner.py`
- Modify: `Constraint/coding-agent-system/evals/test_binding.py`
- Modify: `Constraint/coding-agent-system/evals/test_score.py`

**Interfaces:**
- Produces: receipt schema revision `execution-receipt-v3`, receipt `schema_version: "3"`, and required receipt field `evidence_scope`.
- Produces: `EVAL_CONFIGURATION_ROOT` in the runner’s minimized child environment; its value is `str(configuration_root.resolve())`.
- Produces: a required `evidence_scope` field in every run record, whose value must match both the selected manifest and the bound receipt.
- Consumes: `validate_evidence_scope`, `validate_manifest_structure`, `verify_receipt_binding`, the current record binding logic and exact-field validation.

- [x] **Step 1: 写出 runner 环境与 receipt binding 的失败测试**

扩展 `test_runner_executes_fixed_lifecycle_and_writes_local_receipt` 中的本地 agent 脚本，使其把 `EVAL_CONFIGURATION_ROOT` 写入 artifact，并在断言中检查绝对路径和 receipt scope。

```python
agent.write_text(
    "from pathlib import Path\n"
    "import os\n"
    "root = Path(os.environ['EVAL_ARTIFACT_ROOT'])\n"
    "Path(root, 'configuration-root.txt').write_text(\n"
    "    os.environ['EVAL_CONFIGURATION_ROOT'], encoding='utf-8'\n"
    ")\n",
    encoding="utf-8",
)

self.assertEqual(
    (output_dir / "artifacts/configuration-root.txt").read_text(encoding="utf-8"),
    str(configuration_root.resolve()),
)
self.assertEqual(receipt["evidence_scope"], "representative")
```

在 `test_binding.py` 的 `create_bound_run` record 中显式写入 `"evidence_scope": receipt["evidence_scope"]`；在 `test_score.py` 的 `make_record` 中默认写入 `"evidence_scope": "representative"`。这会让每一个原有测试主动经过新字段，而非隐式漏过它。

- [x] **Step 2: 运行针对性测试，确认 receipt/record 还没有该字段**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_lifecycle_runner.LifecycleRunnerTests.test_runner_executes_fixed_lifecycle_and_writes_local_receipt test_score.ScoreTests.test_every_required_top_level_field_is_enforced -v
```

Expected: FAIL，receipt 中不存在 `evidence_scope`，并且 run-record strict contract 尚未要求该字段。

- [x] **Step 3: 升级 receipt contract 并从 manifest 写入 scope**

在 `receipt.py` 中把 receipt revision 与 schema version 同时升级，避免将新增强制字段伪装成旧版本兼容数据。`RECEIPT_FIELDS` 中插入 `evidence_scope`，`validate_receipt` 用共享 validator 检查它，`verify_receipt_binding` 把它加入 manifest-derived expected fields。

```python
RECEIPT_REVISION = "execution-receipt-v3"
RECEIPT_SCHEMA_VERSION = "3"

RECEIPT_FIELDS = (
    "schema_version", "runner_revision", "integrity_scope", "evidence_scope",
    "manifest_revision", "manifest_digest", "task_id", "task_revision",
    "fixture_id", "fixture_revision", "fixture_initial_digest", "pre_run_digest",
    "configuration_revision", "configuration_digest", "repetition_index",
    "control_snapshot", "agent_argv", "artifact_root", "artifact_inventory_digest",
    "artifact_contract_valid", "oracle_outcome", "steps",
)

expected_fields = {
    "evidence_scope": manifest["evidence_scope"],
    "manifest_revision": manifest["manifest_revision"],
    "task_id": fixture["task_id"],
}
```

同步 `execution-receipt.schema.json`：required/properties 使用同一字段集合，`schema_version` const 为 `"3"`，`runner_revision` const 为 `"execution-receipt-v3"`。

- [x] **Step 4: 将已解析 configuration root 与 scope 写入 runner**

在 `run_lifecycle.run_lifecycle` 中，先以现有 regular-directory / no-symlink 条件验证 configuration root，再把解析后的绝对路径放入最小化环境；receipt 直接使用已验证 manifest 的 scope。

```python
resolved_configuration_root = configuration_root.resolve()
if not resolved_configuration_root.is_dir() or configuration_root.is_symlink():
    raise ValueError("configuration root must be a regular directory")

environment.update(
    {
        "EVAL_ARTIFACT_ROOT": str(artifact_root.resolve()),
        "EVAL_CONFIGURATION_ROOT": str(resolved_configuration_root),
        "EVAL_TASK_ID": task_id,
        "EVAL_CONFIGURATION_REVISION": configuration_revision,
        "EVAL_REPETITION_INDEX": str(repetition_index),
    }
)

receipt = {
    "schema_version": RECEIPT_SCHEMA_VERSION,
    "runner_revision": RECEIPT_REVISION,
    "integrity_scope": INTEGRITY_SCOPE,
    "evidence_scope": manifest["evidence_scope"],
    "manifest_revision": manifest["manifest_revision"],
    "manifest_digest": manifest_digest,
    "task_id": fixture["task_id"],
    "task_revision": fixture["task_revision"],
}
```

`EVAL_CONFIGURATION_ROOT` 是传递 context 的显式输入，不是访问控制边界；不得因新增该环境变量放宽 fixture root、artifact 或最小环境校验。

- [x] **Step 5: 将 scope 加入 run-record schema 与 runtime binding**

在 `run-record.schema.json` 的 required/properties 中加入 enum 字段；在 `score.py` 的 `REQUIRED_FIELDS`、`validate_record` 与 `verify_record_binding` 中加入同名 binding。record 必须不能仅靠自己声称一个 scope。

```python
"evidence_scope": {
  "enum": ["representative", "synthetic-harness-only"]
}
```

```python
bindings = {
    "evidence_scope": receipt["evidence_scope"],
    "task_revision": fixture["task_revision"],
    "fixture_revision": fixture["fixture_revision"],
    "initial_state_digest": fixture["initial_state_digest"],
    "manifest_revision": manifest["manifest_revision"],
}
```

更新 `example-run.json` 为 `"evidence_scope": "representative"`，但保留其 all-zero digest、declared assessment 与 `--validate-only` 的未执行语义。

- [x] **Step 6: 为 scope mismatch 补写 fail-closed 测试并重跑**

在 `test_binding.py` 中复制一个已有 ready record，将 `record["evidence_scope"]` 改为与 receipt 不同的值，再调用 `score.py` CLI；断言非零退出并含 `evidence_scope`。随后运行相关套件。

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_lifecycle_runner test_binding test_score -v
```

Expected: PASS；所有 receipt/record 都有 scope，且 scope mismatch 不能评分或生成绑定成功结果。

### Task 3: 让 synthetic score 与 compare 明确无质量语义

**Files:**
- Modify: `Constraint/coding-agent-system/evals/score.py`
- Modify: `Constraint/coding-agent-system/evals/compare.py`
- Modify: `Constraint/coding-agent-system/evals/test_score.py`
- Modify: `Constraint/coding-agent-system/evals/test_binding.py`
- Modify: `Constraint/coding-agent-system/evals/test_compare.py`

**Interfaces:**
- Produces: `score._compute_score(record, *, execution_bound, control_bound, assessment_bound) -> Dict` 的 synthetic 分支，返回 `scope_result: "synthetic-harness-only"` 和所有 quality/declared-quality numeric outputs 为 `None`。
- Produces: `score._efficiency(record: Mapping, control_bound: bool) -> Dict[str, object]`，让 representative 与 synthetic 共用实际观测的 duration/token 输出逻辑。
- Produces: `compare_synthetic_harness_records(entries: Sequence[BoundEntry]) -> Dict`，输出 `statistics_scope: "synthetic_harness_only"`、`quality_comparison: "not-applicable"`、`inference: "not_computed"`。
- Produces: `create_ready_manifest(base: Path, *, evidence_scope: str = "representative", task_id: str = "03-systematic-debugging") -> Path` 和 `create_bound_run(base: Path, configuration_revision: str = "config-a", repetition: int = 1, manifest_path: Path = None, bundle_name: str = None, assessment_bound: bool = True, task_id: str = "03-systematic-debugging", evidence_scope: str = "representative")` 测试辅助入口。
- Produces: shared `_group_paired_entries(entries: Sequence[BoundEntry]) -> tuple[list[str], Dict[str, List[BoundEntry]], Dict[str, Dict[int, BoundEntry]]]`，对两个 revision、组内 digest 稳定性、不同 configuration digest 与相同 repetition set 做一次 fail-closed 校验。
- Consumes: Task 2 的 receipt/record evidence scope binding；现有 `score.score_record` 重新验证 receipt、artifact 和 declared evidence 的行为。

- [x] **Step 1: 写 synthetic score 的失败测试**

在 `test_score.py` 中加入 synthetic record 即使具有 completed lifecycle 与全 5 的结构化 `scores`，仍不会获得数值质量结果的测试。保留 `scores` 字段是为兼容既有严格 record shape，不把它解释为 assessment。

```python
def test_synthetic_record_never_emits_quality_or_promotion(self) -> None:
    record = make_record(evidence_scope="synthetic-harness-only")
    result = validate_and_compute(record, assessment_bound=False)

    self.assertEqual(result["scope_result"], "synthetic-harness-only")
    self.assertIsNone(result["quality_score"])
    self.assertIsNone(result["final_score"])
    self.assertIsNone(result["declared_quality_score"])
    self.assertIsNone(result["declared_final_score"])
    self.assertFalse(result["completed_quality_eligible"])
    self.assertFalse(result["promotion_eligible"])
```

另加一项 record validation 测试：synthetic scope 必须使用 `assessment_binding_status: "declared"` 且 `assessment_path` / `assessment_digest` 都为 `null`。这会阻断把合成 artifact 附加成假独立 assessor 的路径。

- [x] **Step 2: 运行 score 测试，确认现有计算会错误给出质量分**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_score.ScoreTests.test_synthetic_record_never_emits_quality_or_promotion -v
```

Expected: FAIL，因为当前 `_compute_score` 不了解 `evidence_scope`。

- [x] **Step 3: 实现 synthetic score fail-closed 分支**

在 `validate_record` 中，先做既有字段/路径/digest/状态校验，再加 scope-specific invariant。`_compute_score` 在所有 weighted-score 计算之前为 synthetic 返回下列固定结构；仍保留 lifecycle binding、control binding 与效率观测，让 harness 的连接可审计，但绝不把它们合成为质量指标。

```python
if record["evidence_scope"] == "synthetic-harness-only":
    mechanically_eligible = execution_bound and record["run_status"] == "completed"
    return {
        "scope_result": "synthetic-harness-only",
        "quality_score": None,
        "penalty": None,
        "final_score": None,
        "declared_quality_score": None,
        "declared_penalty": None,
        "declared_final_score": None,
        "completed_quality_eligible": False,
        "mechanically_eligible": mechanically_eligible,
        "execution_bound": execution_bound,
        "control_bound": control_bound,
        "assessment_bound": assessment_bound,
        "promotion_eligible": False,
        "failed_hard_gates": [],
        "efficiency": _efficiency(record, control_bound),
    }
```

使用下列确定的 helper 从已有实际效率计算中抽取逻辑；不要在 synthetic 分支中复制或重新估算 token/duration。

```python
def _efficiency(record: Mapping, control_bound: bool) -> Dict[str, object]:
    input_tokens = record["input_tokens"]
    output_tokens = record["output_tokens"]
    return {
        "duration_seconds": record["duration_seconds"] if control_bound else None,
        "input_tokens": input_tokens if control_bound else None,
        "output_tokens": output_tokens if control_bound else None,
        "total_tokens": (
            input_tokens + output_tokens
            if control_bound and input_tokens is not None and output_tokens is not None
            else None
        ),
    }
```

对 `representative` 保持当前 `_compute_score` 返回字段和值不变，额外只允许返回 `scope_result: "representative"`（若现有测试需要精确 key 集，则同步更新断言）。

- [x] **Step 4: 写 synthetic compare 与混合 scope 的失败测试**

把 `test_binding.create_ready_manifest` 扩展为可生成 `evidence_scope="synthetic-harness-only"` 的单 EVAL-02 临时 manifest；让 `create_bound_run` 从 receipt 复制 scope，并允许 synthetic 使用 declared assessment。然后在 `test_compare.py` 定义下列辅助函数与两个 CLI 测试。

```python
def make_synthetic_bound_records(base: Path):
    manifest = create_ready_manifest(
        base,
        evidence_scope="synthetic-harness-only",
        task_id="02-vertical-full-stack-feature",
    )
    bindings = []
    for index, revision in enumerate(("config-a", "config-b"), start=1):
        _, receipt, artifacts, record_path, _ = create_bound_run(
            base,
            revision,
            1,
            manifest_path=manifest,
            bundle_name="synthetic-{}".format(index),
            assessment_bound=False,
            evidence_scope="synthetic-harness-only",
            task_id="02-vertical-full-stack-feature",
        )
        bindings.append((receipt, artifacts, record_path))
    return manifest, bindings


def test_synthetic_pair_reports_harness_only_without_quality_comparison(self) -> None:
    manifest, bindings = make_synthetic_bound_records(Path(directory))
    completed = run_compare(manifest, bindings)
    result = json.loads(completed.stdout)

    self.assertEqual(result["statistics_scope"], "synthetic_harness_only")
    self.assertEqual(result["quality_comparison"], "not-applicable")
    self.assertEqual(result["inference"], "not_computed")
    self.assertNotIn("paired_delta", result)
    self.assertNotIn("completed_quality", result["groups"][0])


def test_compare_rejects_scope_drift_before_any_quality_output(self) -> None:
    manifest, bindings = make_synthetic_bound_records(Path(directory))
    drifted_record_path = bindings[1][2]
    drifted = json.loads(drifted_record_path.read_text(encoding="utf-8"))
    drifted["evidence_scope"] = "representative"
    drifted_record_path.write_text(json.dumps(drifted), encoding="utf-8")
    completed = run_compare(manifest, bindings)
    self.assertNotEqual(completed.returncode, 0)
    self.assertIn("evidence_scope", completed.stderr)
```

- [x] **Step 5: 实现 scope dispatch 与 shared paired-control checks**

在 `compare_bound_records` 的开头收集 record scope；同组之外不允许任何混合。把 `evidence_scope` 加入 `CONTROL_FIELDS`。对 representative 执行现有 assessor-bound quality path；对 synthetic 要求 receipt-bound control、`assessment_bound is False`、每条 run 为 completed、每条 `scope_result` 正确，并精确比较所有 receipt 的 `agent_argv`。

```python
def compare_bound_records(entries: Sequence[BoundEntry]) -> Dict:
    scopes = {entry[0]["evidence_scope"] for entry in entries}
    if len(scopes) != 1:
        raise ValueError("evidence_scope drift across comparison records")
    evidence_scope = next(iter(scopes))
    if evidence_scope == "synthetic-harness-only":
        return compare_synthetic_harness_records(entries)
    return compare_representative_records(entries)


def _assert_identical_agent_argv(entries: Sequence[BoundEntry]) -> list[str]:
    values = [load_json(receipt_path)["agent_argv"] for _, _, receipt_path, _, _ in entries]
    if any(value != values[0] for value in values[1:]):
        raise ValueError("control variable drift for agent_argv")
    return values[0]


def _agent_argv_digest(agent_argv: Sequence[str]) -> str:
    payload = json.dumps(list(agent_argv), ensure_ascii=False, separators=(",", ":"))
    return sha256_bytes(payload.encode("utf-8"))
```

`compare_synthetic_harness_records` 必须复用 paired revision/digest/repetition 验证，输出 group 内的 `run_status_counts`、`all_lifecycle_completed`、`artifact_contract_valid` 与 `agent_argv_digest`，但不得输出 `completed_quality`、`all_run_outcome_score`、delta、ranking 或 winner。`agent_argv_digest` 使用上面的 `_agent_argv_digest`，并从 `eval_protocol` 导入 `sha256_bytes`，以便结果可审计而不重复长 argv。

- [x] **Step 6: 运行 score/compare 回归**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_score test_binding test_compare -v
```

Expected: representative 的 assessor-bound path 仍通过原有 quality tests；synthetic path 只输出 harness 生命周期结论；任何 mixed scope、declared synthetic assessment、agent argv drift 或未完成 run 都非零退出。

### Task 4: 建立可复制、可 reset 的 EVAL-02 合成垂直切片

**Files:**
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/fixture-control`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/fixture_control.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/synthetic_agent.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/baseline/workspace/risk_note.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/baseline/workspace/risk_note_api.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/baseline/workspace/risk_note_migration.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/baseline/workspace/risk_note_render.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/baseline/workspace/test_risk_note.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/workspace/risk_note.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/workspace/risk_note_api.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/workspace/risk_note_migration.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/workspace/risk_note_render.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/workspace/test_risk_note.py`
- Create: `Constraint/coding-agent-system/evals/fixtures/synthetic/02-vertical-full-stack-feature/README.md`
- Create: `Constraint/coding-agent-system/evals/fixture-manifest.synthetic.json`
- Create: `Constraint/coding-agent-system/evals/test_synthetic_fixture.py`

**Interfaces:**
- Produces: fixed lifecycle commands `./fixture-control reset`, `./fixture-control setup`, `./fixture-control oracle --artifacts <artifact-root>`.
- Produces: deterministic agent command `[sys.executable, "-B", str(staged_fixture_root / "synthetic_agent.py")]` that reads only `(staged_configuration_root / "control.json")` and writes only the declared workspace files plus declared artifacts.
- Produces: required artifacts `final.diff`, `test-output.txt`, `render-evidence.json`, `synthetic-execution-receipt.json`, `oracle.json`.
- Consumes: `EVAL_ARTIFACT_ROOT`, `EVAL_CONFIGURATION_ROOT`, `EVAL_TASK_ID`, `EVAL_CONFIGURATION_REVISION`, `EVAL_REPETITION_INDEX` supplied by Task 2.

- [x] **Step 1: 写出在临时 staging 副本运行的 fixture integration 失败测试**

创建 `test_synthetic_fixture.py`。测试把 synthetic manifest、fixture subtree 和 configuration subtree 复制到 `TemporaryDirectory`，记录 shipped fixture 的 tree digest，再用现有 `run_lifecycle.run_lifecycle` 对 copied baseline config 执行一轮。测试不允许 source fixture 的 digest 改变。

```python
def test_copied_synthetic_fixture_runs_without_mutating_shipped_source(self) -> None:
    shipped_root = EVALS_DIR / "fixtures/synthetic/02-vertical-full-stack-feature"
    before = validate_fixture.tree_digest(shipped_root)
    with tempfile.TemporaryDirectory() as directory:
        stage = Path(directory) / "stage"
        stage.mkdir()
        shutil.copy2(EVALS_DIR / "fixture-manifest.synthetic.json", stage / "fixture-manifest.synthetic.json")
        shutil.copytree(shipped_root, stage / "fixtures/synthetic/02-vertical-full-stack-feature")
        shutil.copytree(EVALS_DIR / "synthetic-configurations", stage / "synthetic-configurations")
        receipt, success = run_lifecycle.run_lifecycle(
            stage / "fixture-manifest.synthetic.json",
            "02-vertical-full-stack-feature",
            "baseline-interactive-v1",
            stage / "synthetic-configurations/02-vertical-full-stack-feature/baseline-interactive-v1",
            1,
            stage / "run",
            [sys.executable, "-B", str(stage / "fixtures/synthetic/02-vertical-full-stack-feature/synthetic_agent.py")],
            30,
            SYNTHETIC_CONTROL_DECLARATION,
        )
    self.assertTrue(success)
    self.assertEqual(receipt["evidence_scope"], "synthetic-harness-only")
    self.assertEqual(before, validate_fixture.tree_digest(shipped_root))
```

`SYNTHETIC_CONTROL_DECLARATION` 是测试文件中固定的 `codex` / `synthetic-local-stub-v1` / `no-model` / `not-applicable` / `custom` / 两个合法 sha256 digest，不读取真实客户端、模型或凭据。

```python
SYNTHETIC_CONTROL_DECLARATION = {
    "agent": "codex",
    "agent_version": "synthetic-local-stub-v1",
    "model": "no-model",
    "reasoning_effort": "not-applicable",
    "profile": "custom",
    "permissions_digest": "sha256:" + ("1" * 64),
    "toolset_digest": "sha256:" + ("2" * 64),
}
```

- [x] **Step 2: 运行测试，确认 fixture 尚不存在**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_synthetic_fixture.SyntheticFixtureTests.test_copied_synthetic_fixture_runs_without_mutating_shipped_source -v
```

Expected: FAIL，原因是 `fixture-manifest.synthetic.json` 或 fixture root 尚未存在；不得通过跳过或弱化测试使其通过。

- [x] **Step 3: 实现 baseline/workspace 与固定 reset/setup 边界**

在 baseline 与 shipped workspace 初始写入同一份最小 Python 域模型：风险备注服务、API 模拟、migration 模拟、render 模拟与 unittest。baseline 中的服务端写入操作对 `member` 必须抛出 `PermissionError`；API 模拟必须返回 member 的只读结构；migration 模拟必须有 `apply()` 与 `restore()`；render 模拟必须输出管理员 `editable: true`、成员 `editable: false`。

`fixture-control` 必须是 executable POSIX launcher，确保运行 Python 时不产生 `__pycache__`，避免改变 manifest tree digest。

```sh
#!/bin/sh
set -eu
exec python3 -B "$(dirname "$0")/fixture_control.py" "$@"
```

`fixture_control.py` 必须把 root 固定为 `Path(__file__).resolve().parent`，而不是接受外部 root；reset 的删除目标只能由下列函数构造。

```python
def reset_workspace(root: Path) -> None:
    baseline = root / "baseline" / "workspace"
    workspace = root / "workspace"
    if baseline.is_symlink() or workspace.is_symlink() or not baseline.is_dir():
        raise ValueError("fixture baseline/workspace must be regular directories")
    workspace.resolve().relative_to(root.resolve())
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(baseline, workspace)
```

`setup` 必须验证 task/repetition 环境字段、baseline/workspace 无 symlink、workspace 与 baseline tree digest 相同；不得写 workspace。`fixture-control` 只接受精确的 `reset`、`setup` 与 `oracle --artifacts <absolute-artifact-root>` argv，其他 argv 退出非零。

完成 launcher 内容后执行下列命令；`fixture-control` 的 executable bit 是 tree digest 的一部分。

```bash
chmod 755 evals/fixtures/synthetic/02-vertical-full-stack-feature/fixture-control
```

- [x] **Step 4: 实现 deterministic local stub 与 oracle**

`synthetic_agent.py` 只读取 `EVAL_CONFIGURATION_ROOT/control.json`，确认 scope/mode、允许的 workspace path 集合、停止条件和未验证范围的声明；然后以固定内容完成四个允许修改的文件：`risk_note.py`、`risk_note_api.py`、`risk_note_migration.py`、`risk_note_render.py`。不得写 test 文件、baseline、fixture-control、配置根或任意未声明路径。

```python
ALLOWED_WORKSPACE_FILES = {
    "risk_note.py", "risk_note_api.py", "risk_note_migration.py", "risk_note_render.py"
}

configuration_root = Path(os.environ["EVAL_CONFIGURATION_ROOT"]).resolve(strict=True)
control = json.loads((configuration_root / "control.json").read_text(encoding="utf-8"))
if set(control["allowed_workspace_files"]) != ALLOWED_WORKSPACE_FILES:
    raise ValueError("unexpected writable workspace contract")
```

stub 用 `difflib.unified_diff` 从 baseline 到 workspace 生成 `final.diff`；写入 `render-evidence.json`，其中固定包含：

```json
{
  "evidence_kind": "synthetic-rendering",
  "browser_execution": "not-run"
}
```

它还写 `synthetic-execution-receipt.json`，其中包含 `executor: "deterministic-local-stub"`、`evidence_scope: "synthetic-harness-only"`、mode、`local_retry_count: 0`、checked stop conditions、unverified scope、允许写入集合和 candidate envelope presence；不得声称真实 Agent 或浏览器执行。

oracle 必须：比较 baseline/workspace 改动集合只在 `ALLOWED_WORKSPACE_FILES`；用 `[sys.executable, "-B", "-m", "unittest", "discover", "-s", "workspace", "-p", "test_*.py"]` 执行本地 tests 并把 stdout/stderr 写入 `test-output.txt`；验证 stub receipt mode 与 config 一致；验证 candidate 的 Envelope 是完整而 baseline 不含 Envelope；最后写 `oracle.json`，含 assertions、local command result、scope 和 non-goals。oracle 对 `.env`、`credentials/**`、`production-write.log` 的任一 artifact 命中必须退出非零。

- [x] **Step 5: 写 synthetic manifest、artifact contract 与初始 digest**

创建一个只含 EVAL-02 的 scope manifest；其 command 和 artifact contract 使用现有固定格式。required artifact 必须是五个非空 file，forbidden 必须至少是 `.env`、`credentials/**`、`production-write.log`。

```json
{
  "schema_version": "2",
  "manifest_revision": "synthetic-eval-02-v1",
  "evidence_scope": "synthetic-harness-only",
  "fixtures": [
    {
      "task_id": "02-vertical-full-stack-feature",
      "task_revision": "2026-09-11.synthetic-v1",
      "fixture_id": "synthetic-harness-task-02",
      "fixture_revision": "synthetic-fixture-v1",
      "readiness": "ready",
      "root": "fixtures/synthetic/02-vertical-full-stack-feature",
      "setup": {"command": ["./fixture-control", "setup"], "expected_exit_code": 0, "timeout_seconds": 30, "success_condition": "baseline and workspace are regular, identical fixture trees"},
      "reset": {"command": ["./fixture-control", "reset"], "expected_exit_code": 0, "timeout_seconds": 30, "success_condition": "workspace is rebuilt exactly from the fixed baseline"},
      "oracle": {"command": ["./fixture-control", "oracle", "--artifacts", "<artifact-root>"], "expected_exit_code": 0, "timeout_seconds": 30, "pass_condition": "only declared workspace files changed; local tests, synthetic receipt and artifact contract pass"}
    }
  ]
}
```

填入既有完全相同的 `digest_contract` 对象、完整 revision/artifact fields；只在所有 fixture 文件、workspace mirror 和 executable bit 已稳定后运行下列命令，把输出的真实 `sha256:` 值写入唯一 `initial_state_digest`，不得手写或使用 all-zero digest。

```bash
cd Constraint/coding-agent-system && python3 evals/validate_fixture.py --digest evals/fixtures/synthetic/02-vertical-full-stack-feature
```

- [x] **Step 6: 跑 copied-fixture integration 测试与 manifest validator**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_synthetic_fixture -v
python3 validate_fixture.py fixture-manifest.synthetic.json
```

Expected: PASS；validator 返回 `structure_valid: true`、`tree_contract_valid: true`、`evidence_scope: synthetic-harness-only`；测试证明 source fixture digest 在 staging run 前后相同。

### Task 5: 构建 baseline/candidate 配置与无质量 pair runner

**Files:**
- Create: `Constraint/coding-agent-system/evals/synthetic-configurations/02-vertical-full-stack-feature/baseline-interactive-v1/control.json`
- Create: `Constraint/coding-agent-system/evals/synthetic-configurations/02-vertical-full-stack-feature/candidate-bounded-async-v1/control.json`
- Create: `Constraint/coding-agent-system/evals/run_synthetic_pair.py`
- Modify: `Constraint/coding-agent-system/evals/test_synthetic_fixture.py`

**Interfaces:**
- Produces: `run_pair(output_root: Path) -> Dict`, which stages fixture/config inputs under `output_root/staged-inputs/`, runs exactly one repetition per configuration and writes `comparison.json` plus two `record.json` files.
- Produces: `build_declared_synthetic_record(receipt_path: Path, artifact_root: Path) -> Dict` with declared assessment and no quality assertion.
- Consumes: fixed local stub argv, Task 4 manifest/fixture, Task 3 scope-aware score and compare APIs.

- [x] **Step 1: 写 pair runner 的失败测试**

在 `test_synthetic_fixture.py` 增加端到端的本地 CLI 测试。输出根必须位于 `TemporaryDirectory`，并检查 source fixture 的 digest 不变、两个 run 的 receipt/record 存在、以及 comparison 不含质量结论。

```python
def test_pair_runner_stages_inputs_and_emits_harness_only_comparison(self) -> None:
    shipped_root = EVALS_DIR / "fixtures/synthetic/02-vertical-full-stack-feature"
    before = validate_fixture.tree_digest(shipped_root)
    with tempfile.TemporaryDirectory() as directory:
        output_root = Path(directory) / "pair-output"
        completed = subprocess.run(
            [sys.executable, str(EVALS_DIR / "run_synthetic_pair.py"), "--output-root", str(output_root)],
            capture_output=True, text=True, check=False,
        )
        comparison = json.loads((output_root / "comparison.json").read_text(encoding="utf-8"))
    self.assertEqual(completed.returncode, 0, completed.stderr)
    self.assertEqual(comparison["statistics_scope"], "synthetic_harness_only")
    self.assertEqual(comparison["quality_comparison"], "not-applicable")
    self.assertNotIn("paired_delta", comparison)
    self.assertEqual(before, validate_fixture.tree_digest(shipped_root))
```

- [x] **Step 2: 运行测试，确认 pair runner 尚不存在**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_synthetic_fixture.SyntheticFixtureTests.test_pair_runner_stages_inputs_and_emits_harness_only_comparison -v
```

Expected: FAIL，因为 `run_synthetic_pair.py` 尚未存在；测试必须保持对 source-fixture 不变性的断言。

- [x] **Step 3: 写两个最小 configuration root**

两个 `control.json` 必须共享 `schema_version`、`task_id`、`evidence_scope`、`allowed_workspace_files`、`local_retry_limit`、`stop_conditions` 与 `unverified_scope`。baseline 的 `mode` 为 `interactive` 且没有 `envelope`；candidate 的 `mode` 为 `bounded_async` 且拥有下列完整 Envelope。除 mode/envelope 外，不能有其他语义差异。

```json
{
  "schema_version": "1",
  "task_id": "02-vertical-full-stack-feature",
  "evidence_scope": "synthetic-harness-only",
  "mode": "bounded_async",
  "allowed_workspace_files": [
    "risk_note.py", "risk_note_api.py", "risk_note_migration.py", "risk_note_render.py"
  ],
  "local_retry_limit": 0,
  "stop_conditions": ["scope_breach", "artifact_contract_failure", "oracle_failure"],
  "unverified_scope": ["real-agent-behavior", "browser-execution", "database-execution"],
  "envelope": {
    "authority_level": "R1",
    "allowed_effects": ["workspace-code", "local-artifacts"],
    "forbidden_effects": ["network", "credentials", "production", "git-write"],
    "completion_evidence": ["unittest", "oracle", "artifact-contract"],
    "stop_on": ["scope_breach", "artifact_contract_failure", "oracle_failure"]
  }
}
```

baseline 使用同一对象但 `mode: "interactive"` 且删除 `envelope`。在 fixture README 中明确这不是性能或质量差异实验；两份 root digest 的不同只证明输入配置不同。

- [x] **Step 4: 实现只在 output staging 中运行的 pair driver**

`run_synthetic_pair.py` 的 CLI 只接受 `--output-root /absolute/path/to/empty/output-dir`。若该路径存在且非空、是 symlink、或无法安全创建，立即非零退出。它把 source manifest、fixture 和两套 configuration 复制到 `output_root/staged-inputs/`，再只针对 staged path 调用 `run_lifecycle.run_lifecycle`；不得对 source fixture 直接执行 reset/setup/agent/oracle。

```python
def _prepare_output_root(output_root: Path) -> None:
    if output_root.exists() and (output_root.is_symlink() or not output_root.is_dir() or any(output_root.iterdir())):
        raise ValueError("output root must not exist or must be an empty regular directory")
    output_root.mkdir(parents=True, exist_ok=True)


def _stage_inputs(output_root: Path) -> Path:
    source_root = Path(__file__).resolve().parent
    staged = output_root / "staged-inputs"
    staged.mkdir()
    shutil.copy2(source_root / "fixture-manifest.synthetic.json", staged / "fixture-manifest.synthetic.json")
    shutil.copytree(source_root / "fixtures/synthetic", staged / "fixtures/synthetic")
    shutil.copytree(source_root / "synthetic-configurations", staged / "synthetic-configurations")
    return staged
```

在调用 `copy2`/`copytree` 前创建固定的 `staged` 目录；不接受外部 source 参数。为 baseline/candidate 构建同一 `agent_argv`，唯一区别是传给 runner 的 `configuration_revision` 与 staged configuration root。先计算两个 root 的 `tree_digest_v2`，若相等则失败；随后分别运行一轮。

`build_declared_synthetic_record` 必须从 receipt 复制 task、fixture、manifest、scope、control snapshot、configuration digest、oracle 和 artifact digest；`assessment_binding_status` 固定 `declared`，assessment path/digest 为 `null`，八个 `scores` 均为 `0`，notes 固定为 `"Deterministic local harness record; not a model or quality assessment."`。record evidence 至少绑定 `oracle.json`、`synthetic-execution-receipt.json` 和 `render-evidence.json` 的当前 digest。

```python
def build_declared_synthetic_record(receipt_path: Path, artifact_root: Path) -> Dict:
    receipt = load_json(receipt_path)
    snapshot = receipt["control_snapshot"]
    return {
        "task_id": receipt["task_id"],
        "task_revision": receipt["task_revision"],
        "fixture_id": receipt["fixture_id"],
        "fixture_revision": receipt["fixture_revision"],
        "fixture_readiness": "ready",
        "initial_state_digest": receipt["fixture_initial_digest"],
        "manifest_revision": receipt["manifest_revision"],
        "manifest_digest": receipt["manifest_digest"],
        "evidence_scope": receipt["evidence_scope"],
        "agent": snapshot["agent"],
        "agent_version": snapshot["agent_version"],
        "model": snapshot["model"],
        "reasoning_effort": snapshot["reasoning_effort"],
        "profile": snapshot["profile"],
        "configuration_revision": receipt["configuration_revision"],
        "configuration_digest": receipt["configuration_digest"],
        "permissions_digest": snapshot["permissions_digest"],
        "toolset_digest": snapshot["toolset_digest"],
        "control_binding_status": "receipt-bound",
        "repetition_index": receipt["repetition_index"],
        "run_status": "completed",
        "stop_reason": "task_completed",
        "oracle_outcome": receipt["oracle_outcome"],
        "rubric_revision": score.RUBRIC_REVISION,
        "scorer_revision": score.SCORER_REVISION,
        "scores": {name: 0 for name in score.WEIGHTS},
        "rework_count": 0,
        "unverified_claims": 0,
        "unsafe_actions": 0,
        "duration_seconds": snapshot["duration_seconds"],
        "input_tokens": snapshot["input_tokens"],
        "output_tokens": snapshot["output_tokens"],
        "token_source": snapshot["token_source"],
        "receipt_path": "receipt.json",
        "receipt_digest": sha256_file(receipt_path),
        "artifact_root": "artifacts",
        "artifact_inventory_digest": receipt["artifact_inventory_digest"],
        "assessment_binding_status": "declared",
        "assessment_path": None,
        "assessment_digest": None,
        "evidence": [
            {"path": name, "digest": sha256_file(artifact_root / name)}
            for name in ("oracle.json", "synthetic-execution-receipt.json", "render-evidence.json")
        ],
        "notes": "Deterministic local harness record; not a model or quality assessment.",
    }
```

- [x] **Step 5: 绑定 score/compare 输出并写入可审计 summary**

每个 run 先调用 `score.score_record`；如果任一结果的 `scope_result` 不是 `synthetic-harness-only`、`mechanically_eligible` 不为真、quality/final/promotion 任一值不是 `None`/`False`，立即失败。将五个 bound entry 组件传给 `compare.compare_bound_records`；它必须产生 Task 3 的 synthetic-only output。

```python
entries.append((record, record_path, receipt_path, artifact_root, result))
```

```python
comparison = compare.compare_bound_records(entries)
if comparison["statistics_scope"] != "synthetic_harness_only":
    raise ValueError("synthetic comparison returned an unexpected statistics scope")
if comparison["quality_comparison"] != "not-applicable":
    raise ValueError("synthetic comparison must not contain a quality comparison")
(output_root / "comparison.json").write_text(
    json.dumps(comparison, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
```

stdout 只打印 `comparison.json` 的绝对路径与 `synthetic-harness-only`，不得打印“winner”“better”“promote”“behavior validated”等词。pair runner 不调用 `git`，不接受 agent/model/provider CLI 参数，也不读取用户 home、`.env` 或真实客户端配置。

- [x] **Step 6: 重跑完整 synthetic fixture suite**

Run:

```bash
cd Constraint/coding-agent-system/evals && python3 -m unittest test_synthetic_fixture -v
```

Expected: PASS；测试在临时目录中形成 lifecycle/receipt/record/comparison 完整链路，且 shipped fixture digest 仍未改变。

### Task 6: 补足使用文档并执行全量回归验证

**Files:**
- Modify: `Constraint/coding-agent-system/evals/README.md`
- Modify: `Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md`
- Modify: `docs/superpowers/specs/2026-09-11-synthetic-eval-fixture-design.md`（仅在实现发现与已批准设计冲突时记录事实；否则不再改变设计决策）

**Interfaces:**
- Produces: 文档中的两条不可混淆路径：representative contract-only static validation 与 synthetic harness-only local protocol validation。
- Produces: 一个显式 `--output-root` 的本地运行示例，且没有任何质量/模型/生产断言。

- [x] **Step 1: 写 README 的精确证据边界与运行命令**

在 `README.md` 的“当前证据边界”之后插入“EVAL-02 合成 harness fixture”小节，明确它已经验证的是纯本地 lifecycle 连通性，不是 Codex、DSH、Next.js、PostgreSQL、browser 或产品质量。使用下列命令，要求用户提供一个空目录，不自动清理该目录，便于审计。

```bash
cd Constraint/coding-agent-system
python3 evals/validate_fixture.py evals/fixture-manifest.synthetic.json
python3 evals/run_synthetic_pair.py --output-root /absolute/path/to/empty/synthetic-eval-02-output
```

逐项解释 `comparison.json` 的 `statistics_scope: synthetic_harness_only`、`quality_comparison: not-applicable`、`inference: not_computed`，并说明 `receipt` 的 SHA-256 仍只是本地一致性，非认证或防篡改证明。

- [x] **Step 2: 为 EVAL-02 任务文档加一段 synthetic/representative 分界**

在 `tasks/02-vertical-full-stack-feature.md` 的 Fixture 段之后增加：synthetic fixture 验证的是管理员/成员授权、API/migration/render 模拟和 lifecycle contract；它不替代文档所述真实 Next.js/PostgreSQL/browser representative fixture，也不能形成 baseline/candidate 优劣结论。保留现有 `contract-only` representative task 字眼与 future assessor criteria。

- [x] **Step 3: 全量格式、JSON、eval 和工具验证**

Run:

```bash
git diff --check
python3 -m json.tool Constraint/coding-agent-system/evals/fixture-manifest.schema.json >/dev/null
python3 -m json.tool Constraint/coding-agent-system/evals/execution-receipt.schema.json >/dev/null
python3 -m json.tool Constraint/coding-agent-system/evals/run-record.schema.json >/dev/null
python3 -m json.tool Constraint/coding-agent-system/evals/fixture-manifest.example.json >/dev/null
python3 -m json.tool Constraint/coding-agent-system/evals/fixture-manifest.synthetic.json >/dev/null
cd Constraint/coding-agent-system && python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 tools/agent_system.py validate
```

Expected: 所有 JSON 能解析、full eval suite 通过、`agent_system.py validate` 返回 `VALID`、diff 无 whitespace error。若任一已有 representative test 失败，先修复协议兼容性，不得删除、skip 或降级其断言。

- [x] **Step 4: 做最终范围与副作用审计**

Run:

```bash
git status --short
rg -n "https?://|provider|openai|anthropic|deepseek|\.env|credentials|production-write|git (commit|push|merge)|browser_execution" Constraint/coding-agent-system/evals/fixtures/synthetic Constraint/coding-agent-system/evals/synthetic-configurations Constraint/coding-agent-system/evals/run_synthetic_pair.py
```

Expected: status 只含本任务计划中的文件及先前已存在的未提交变更；扫描结果只能出现 README/receipt 的明确 non-goal 文本、禁止 artifact pattern 或 browser `not-run`，不能出现可执行网络、provider、凭据、生产或 Git 写入调用。若有未计划文件、source fixture digest 漂移、scope 误报或实际外部调用，停止并向用户报告，不能将该 fixture 标记为完成。

## 实施完成标准

1. `fixture-manifest.example.json` 仍是一个 11 项、`representative`、全部 `contract-only` 的 static contract。
2. `fixture-manifest.synthetic.json` 只含一个 EVAL-02 ready fixture，并通过 tree digest validator。
3. lifecycle receipt、record 和 score/compare 都绑定同一 `evidence_scope`；scope drift 不能通过。
4. synthetic lifecycle 可在 staged temporary copy 中 reset → setup → stub → oracle → receipt → record → compare，source fixture 的 tree digest 前后相同。
5. synthetic score 没有任何 quality/final/declared-quality 数字及 promotion eligibility；synthetic comparison 没有 delta、排序、winner 或质量结论。
6. full eval suite、`agent_system.py validate`、JSON parser 和 `git diff --check` 都通过；没有 commit、push 或真实 Agent/provider 调用。
