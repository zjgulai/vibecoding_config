---
title: EVAL-02 纯本地合成 Fixture 设计
status: approved
created: 2026-09-11
updated: 2026-09-11
owner: lute
scope: synthetic-eval-fixture
---

# EVAL-02 纯本地合成 Fixture 设计

## 1. 目标

为 `Constraint/coding-agent-system/evals/` 构建一个纯本地、仅依赖 Python 标准库的 EVAL-02 合成 fixture。它用于验证 lifecycle runner、reset/setup/oracle、artifact contract、receipt、record 和比较器的连接与边界。

该 fixture 不模拟真实 Codex、DSH、Next.js、PostgreSQL 或浏览器。它不能证明 Agent 质量、产品质量、生产率、模型优劣或 Skill behavior validation。

## 2. 已确认决策

| 决策 | 结果 | 原因 |
| --- | --- | --- |
| 首个任务范围 | 仅覆盖 `02-vertical-full-stack-feature`。 | EVAL-02 的 R1 垂直切片与 EVAL-03 的不收敛调试 oracle 是独立问题。 |
| 代表性 manifest | 保持 `fixture-manifest.example.json` 的 11 项 `contract-only` 状态。 | 合成实现不能替代真实 Next.js、PostgreSQL 和浏览器环境。 |
| 运行方式 | 使用两个确定性的本地 stub，分别读取 baseline/candidate 配置。 | 用同一可审计命令验证 lifecycle 与控制变量绑定，不调用真实 Agent。 |
| 比较方式 | 合成记录可以进入专用 harness comparison，但不能产生质量分、晋升资格或行为结论。 | 现有 `score.py` 与 `compare.py` 对任何 ready fixture 都能执行，必须增加机器可判定的证据边界。 |
| 外部依赖 | 不新增依赖、不联网、不读取凭据、不启动真实浏览器或数据库。 | fixture 的价值是验证本地协议与隔离，不是复刻生产技术栈。 |

## 3. 当前约束

现有 `validate_fixture.py` 只接受恰好 11 个固定 task 的 manifest。现有 `run_lifecycle.py` 不向 agent argv 传递 configuration root。现有 `score.py` 与 `compare.py` 只根据 `ready`、receipt、record 和 assessment 绑定判断是否进入质量比较，无法区分合成运行与代表性运行。

因此，若只新增一个 ready fixture 而不调整协议，合成结果可能被错误表述为真实 Agent 证据。本设计先补足 scope binding，再构建 fixture。

## 4. 证据范围协议

### 4.1 `evidence_scope`

fixture manifest 新增顶层字段 `evidence_scope`，且必须为以下二者之一：

- `representative`：真实代表性 fixture。manifest 仍必须包含 11 个固定 task contract。
- `synthetic-harness-only`：仅验证评测 harness。manifest 只能包含一个已知 task contract，且该 task 当前为 EVAL-02。

`fixture-manifest.example.json` 显式标记为 `representative`，其 11 个 fixture 继续保持 `contract-only`。新建的 `fixture-manifest.synthetic.json` 标记为 `synthetic-harness-only`，只包含 EVAL-02 的一个 `ready` fixture。

### 4.2 Receipt、record、score 和 compare

`evidence_scope` 必须从 manifest 写入 receipt，并被 record 绑定。运行记录不能自行声明不同 scope。

对于 `synthetic-harness-only`：

- `score.py` 继续校验 manifest、receipt、artifact、record 和已声明的 assessment 结构；
- 输出 `quality_score: null`、`final_score: null`、`promotion_eligible: false`；
- 输出明确的 `scope_result: synthetic-harness-only`，不得使用质量分作为结果；
- `compare.py` 只比较 lifecycle/receipt/控制变量/停机记录/产物契约的一致性，输出 `statistics_scope: synthetic_harness_only`、`quality_comparison: not-applicable` 和 `inference: not_computed`；
- synthetic 与 representative record 不得混合比较，scope 漂移必须 fail closed。

代表性 manifest 的现有结构、评分和比较路径保持不变。没有 ready representative fixture 时，任何 Skill 仍是 `static-baseline`。

## 5. Fixture 架构

```text
Constraint/coding-agent-system/evals/
├── fixture-manifest.synthetic.json
├── fixtures/synthetic/02-vertical-full-stack-feature/
│   ├── fixture-control
│   ├── fixture_control.py
│   ├── baseline/
│   ├── workspace/
│   ├── synthetic_agent.py
│   └── README.md
├── synthetic-configurations/02-vertical-full-stack-feature/
│   ├── baseline-interactive-v1/
│   └── candidate-bounded-async-v1/
├── run_synthetic_pair.py
└── test_synthetic_fixture.py
```

`baseline/` 是不可变的初始快照。`fixture-control reset` 只删除并重建 fixture 内的 `workspace/`。`setup` 只检查本地基线和输入边界。每次 agent run 前，runner 计算的 `sha256-tree-v2` 必须与 synthetic manifest 的 `initial_state_digest` 一致。

`workspace/` 是唯一允许由 stub 修改的产品区域。fixture-control 会拒绝范围外改动、符号链接、凭据路径与未声明 artifact。所有删除目标都固定在 fixture root 内的 `workspace/`，不得接受命令行路径或环境变量作为删除对象。

## 6. 合成 R1 垂直切片

初始 workspace 使用一个最小 Python 域模型，包含客户风险备注的缺失实现。两个本地 stub 均完成相同行为：

1. 管理员可以设置和读取内部风险备注；
2. 普通成员只能读取，不能通过服务层、API 模拟层或渲染层写入；
3. migration 模拟层声明前向与恢复路径；
4. 渲染模拟层产生管理员可编辑、成员只读的结构化结果；
5. 本地 unittest 验证授权、API、migration、渲染与范围限制。

这不是浏览器测试。产物使用 `render-evidence.json`，其中固定写明 `evidence_kind: synthetic-rendering` 和 `browser_execution: not-run`。

## 7. Baseline 与 Candidate

两个 run 使用相同 `synthetic_agent.py` argv、相同 agent/client/model 声明、相同权限 digest、相同 toolset digest、相同 fixture、相同 reset/setup/oracle 和相同 artifact contract。

runner 新增 `EVAL_CONFIGURATION_ROOT`，用于传递当前 configuration root 的绝对路径。该环境变量本身不是文件系统只读控制；synthetic stub 只读取其中的 `control.json`，而写入范围仍由 fixture-control、artifact contract 和 oracle 检查：

- `baseline-interactive-v1`：`mode` 为 `interactive`，不包含 Envelope；
- `candidate-bounded-async-v1`：`mode` 为 `bounded_async`，包含完整任务级 Envelope。

stub 将实际 mode、允许写入集合、本地重试、停止条件检查和未验证范围写入 `synthetic-execution-receipt.json`。candidate configuration 只额外改变 mode 与 Envelope 字段；两份 configuration root 的 tree digest 必须不同。除 configuration revision/digest 与由配置决定的 synthetic receipt 外，比较器要求控制变量相同，并额外核对两个 receipt 的 `agent_argv` 完全一致。

## 8. Oracle 与 Artifact Contract

`fixture-control oracle --artifacts <artifact-root>` 必须在 fixture 内执行以下检查：

1. 只修改声明的 workspace 文件；
2. unittest 通过管理员编辑、成员只读、服务端写入拒绝、API 返回、migration 恢复与渲染模拟检查；
3. `synthetic-execution-receipt.json` 与 configuration 中的 mode 一致；
4. `final.diff`、`test-output.txt`、`render-evidence.json`、`synthetic-execution-receipt.json` 与 `oracle.json` 均存在且非空；
5. artifact 不包含 `.env`、`credentials/**` 或 `production-write.log`。

oracle 写入的 `oracle.json` 必须包含断言、原始本地命令结果、`evidence_scope` 和明确的非目标说明。它不能把合成渲染写成 browser evidence，也不能将 stub 写成真实 Agent。fixture 的固定脚本不含 provider、网络或生产调用；这只能说明受控 stub 没有该代码路径，不能证明任意外部命令绝不会产生副作用。

## 9. 确定性 assessment 与 harness comparison

合成 pair 的运行辅助脚本只创建声明型 record，并把 assessment binding 标记为 `declared`。它不生成或伪装独立质量 assessment。

synthetic comparison 必须验证：

- 两组具有相同 repetition index 集合；
- receipt、配置、artifact inventory 和 scope 全部可绑定；
- control fields 除 configuration revision/digest 外没有漂移；
- 两组均通过 lifecycle 与 oracle；
- candidate receipt 包含完整 Envelope 的实际回执字段；
- 输出不含质量分、排序、优胜者、推广建议或因果结论。

如果任一 digest、scope、artifact、stop evidence 或控制变量不匹配，脚本必须失败，不生成比较成功结论。

## 10. 测试策略

实现遵循 test-first：先为新增 scope schema、runner environment、synthetic score/compare 分支和 fixture integration 写失败测试，再写最小实现。

至少覆盖：

1. `representative` manifest 仍要求 11 项 task；
2. `synthetic-harness-only` manifest 只允许一个已知 EVAL-02 task；
3. synthetic 与 representative record 不能混合；
4. synthetic record 不能得到 quality score、final score 或 promotion eligibility；
5. runner 向 stub 提供正确的 `EVAL_CONFIGURATION_ROOT`；
6. reset 后 digest 与 manifest 相等，stub 后 oracle 与 artifact contract 通过；
7. baseline/candidate 一轮比较输出 `synthetic_harness_only`，且不输出质量结论；
8. 原有 `tools/tests` 和 `evals` 回归保持通过。

fixture integration test 必须在临时目录复制 fixture 和 manifest 后运行。测试不得修改仓库中的 shipped workspace、运行产物或用户目录。

## 11. 非目标与停止条件

- 不把 synthetic manifest 写入或合并到代表性 example manifest；
- 不将 manifest 改为真实 Agent、真实浏览器、真实数据库或生产服务；
- 不安装 Python、Node、数据库、浏览器或任何第三方依赖；
- 不调用 provider、网络、MCP、凭据、用户主目录或生产系统；
- 不自动执行 synthetic pair；运行必须由明确的本地命令触发，输出目录必须为空或不存在；
- 不提交、push、merge、发布或修改远端。

如果实现需要改变现有 representative scoring 语义、放宽 artifact/path/digest 校验，或使 synthetic 输出可晋升为 `behavior-validated`，必须停止并重新取得用户确认。

## 12. 验收标准

| 验收项 | 证据 |
| --- | --- |
| 合成 manifest 可运行 | `validate_fixture.py` 对 synthetic manifest 输出 `structure_valid: true` 和 `tree_contract_valid: true`。 |
| 生命周期闭环 | 一轮 baseline/candidate 均生成 receipt，reset/setup/agent/oracle 均有本地原始输出与 digest 绑定。 |
| 合成范围不会被误报 | synthetic score 没有 quality/final score 或晋升资格；synthetic compare 标记 `synthetic_harness_only`。 |
| 控制变量可审计 | candidate 只因 configuration root 的 mode/Envelope 字段而变化；混合 scope 或 control drift 被拒绝。 |
| 原有协议不回退 | 代表性 manifest 仍为 11 个 `contract-only` contract，所有现有 eval 与工具测试通过。 |
| 无外部副作用 | shipped fixture 与 stub 不含 provider、网络、凭据、用户目录、生产、commit 或 push 调用；runner 的最小环境和本地日志可验证受控路径，但不把该检查表述为任意外部命令的绝对安全证明。 |
