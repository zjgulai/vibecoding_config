# 有界前沿工程融合 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将经过来源审计的 Frontier Engineering 方法融合进现有 AI-Native SDLC 控制面，使 Agent 能在明确的本地任务边界内持续实现、验证和自我修正，同时不新增状态机、权限或生产自治。

**Architecture:** `08-AI-Native-SDLC控制面规范.md` 继续是唯一语义源。新增的 `Autonomy Envelope` 是每个既有 `Control Contract` 的可选字段，不是新 artifact、Gate、Skill、权限或运行时调度器；下游 Prompt、模板和工作流只投影其职责。所有“长时间自主”的价值主张保持为待评测假设，先用现有 EVAL-02/EVAL-03 的同任务、同环境、单变量成对比较校准。

**Tech Stack:** Markdown、JSON、现有 Python 3.9 标准库校验器、`rg`、`git diff --check`；不新增依赖、不运行真实模型、不调用生产或外部写工具。

**Approved decision:** 采用「Bounded Frontier Engineering（有界前沿工程）」：人定义可观察目标、持久决策、验收、风险和授权；Agent 只在任务级 `Autonomy Envelope` 内执行。`R0/R1` 可在明确边界内使用 `bounded_async`；`R2` 保持 Review 与独立审证；`R3` 保持 Human `Own` 与当次对象级 `R3_ACTION_AUTHORIZATION`。

## Global Constraints

- 保留 M00–M13、A00–A13、G0–G6、R0–R3、`R3_ACTION_AUTHORIZATION`、`Delegate / Review / Own`、单一责任链和当前回退语义；不得新建平行状态机、审批门或 artifact 链。
- `Autonomy Envelope` 不能扩大文件、工具、网络、凭据、数据、依赖、外部动作或生产权限。自然语言 Envelope、Prompt、Skill、Hook、MCP、subagent 和 Gate 都不是安全边界。
- 不把 Kiro 的「少于 1% 手写代码」「90% 覆盖率」「30 分钟」「通宵」「最大化 Agent 时间」写成跨项目阈值、KPI 或效果结论。优化目标是「从可执行意图到可信验证结果」和人工 Review 负荷，而不是 Agent 在线时长。
- `bounded_async` 只允许在已声明的 `write_scope`、`tool_scope`、验证、停止条件和交接责任内运行。R2 不因运行时间更长而变成 R1；R3 永远不因自动化而免除对象级授权。
- “代码可丢弃”只适用于可替换实现、原型和缺少独特行为证据的实现耦合细节。外部行为、API/schema、迁移、权限、安全、可观测性、回滚和风险所需的 E2E/integration/property/load 契约必须保留。
- 用户级常驻内核只新增短小、跨平台稳定的行为约束；任务流程进入 Prompt/Skill；可确定阻断进入现有 hook/CI/permissions。不得把十条原则逐字复制进所有模板。
- `prompts/` 与 `prompts_ask/` 只镜像触发条件、输入、禁止结论、停止条件和 Axx 字段语义，不要求字节级相同，也不重复控制面全文。
- 更新共享模板时只编辑 `templates/shared/user-core.md` 或 `templates/shared/project-core.md`，再由 `tools/agent_system.py render-templates --apply` 渲染平台快照；不得手改已渲染的 shared core。
- `Constraint/coding-agent-system/templates.zip` 没有可复现构建脚本且当前包含历史 macOS 元数据。它不作为本次权威或生成目标；不得静默覆盖、删除或宣称已同步。若未来要作为发布包，单独立项建立可复现打包流程。
- 本计划只覆盖仓库内 R1 文档、模板、Skill 文本和评测契约变更。不得 commit、push、安装、调用真实 provider、启动后台 Agent、访问生产或改变用户主目录配置。

## File Responsibility Map

| 区域 | 权威职责 | 本次最小变更 |
| --- | --- | --- |
| `全栈开发Prompt Chain/report-source.md` | Prompt Chain 的来源与主张账本 | 登记 Kiro 原文及其证据边界。 |
| `全栈开发Prompt Chain/08-AI-Native-SDLC控制面规范.md` | 控制面唯一语义源 | 定义 `Autonomy Envelope`、持久行为契约和采纳度量。 |
| `全栈开发Prompt Chain/prompts/00-*.md`、`99-*.md` | 任务入口与端到端控制器 | 传入、校验和回传 Envelope，不授予新权限。 |
| `全栈开发Prompt Chain/prompts/05,07–11,13-*.md` | 阶段执行方法 | 在正确阶段投影方向、反馈、契约、独立验证、观测和演进职责。 |
| `全栈开发Prompt Chain/prompts_ask/05,07–11,13-*.md` | 人机对话版阶段方法 | 以单问题协议镜像相同的语义和停止边界。 |
| `全栈开发Prompt Chain/04-*.md`、`06-*.md` | 模块职责和使用手册 | 给出最小运行说明与入口，不复制规则正文。 |
| `Constraint/coding-agent-system/templates/shared/*.md` | 可渲染的跨平台稳定内核 | 增加短常驻原则和项目级路由。 |
| `Constraint/coding-agent-system/docs/workflow.md`、`docs/skills-governance.md`、`skills/implementation-orchestration/SKILL.md` | 操作方法、能力分层和显式编排 | 定义有界批次、Agent-ready module pack 和候选晋升边界。 |
| `Constraint/coding-agent-system/evals/README.md`、`evals/tasks/02-*.md`、`evals/tasks/03-*.md` | 真实收益的未来验证协议 | 用现有任务设计 baseline/candidate 成对对照；保持 `contract-only`。 |
| `Constraint/coding-agent-system/sources/rule-traceability.json` | 机器可解析的规则来源与评测映射 | 新增可追溯规则记录，不能把 contract-only 升级为行为证据。 |
| `Constraint/coding-agent-system/tools/agent_system.py`、`tools/tests/test_agent_system.py` | 追溯来源解析与回归证明 | 允许规则引用已登记的 `RSP-*` 外部研究来源，同时不改变 `LOC`/`REF` 计数语义。 |

## Canonical Semantics to Implement

### Optional `Autonomy Envelope`

完整字段定义只保留在 `08-AI-Native-SDLC控制面规范.md`。本计划仅要求：`interactive` 为默认；只有当前任务范围、风险、工具、数据、验收和交接均明确且使用者选择时，R0/R1 才可使用 `bounded_async`；其字段必须绑定目标/DoD、写入与工具/数据范围、反馈、停止条件、任务级预算、enforcement evidence 与 handoff。`interactive` 省略该节或写 `Not applicable`，不能因此推断获准连续执行。

### Risk-specific behavior

| 风险 | `bounded_async` 可以做什么 | 必须停止的位置 |
| --- | --- | --- |
| R0 | 批量阅读、检索、dry-run、分析与只读验证。 | 数据边界、来源或任务范围不清。 |
| R1 | 在明确 `write_scope` 内执行实现 → 验证 → 修复 → 证据回传。 | 需要新依赖、超出范围、架构/权限/数据影响扩大，或验证不收敛。 |
| R2 | `bounded_async` 不适用；可在 `interactive` 下准备方案、作者验证、审证材料和有明确 G3/G4 的局部工作。 | 任何高影响决定、范围变化、独立审证缺失或实现者试图自我放行。 |
| R3 | `bounded_async` 不适用；只可在 `interactive` 下形成 proposal、runbook、dry-run 或获授权的只读证据。 | 任何真实外部、生产、不可逆或商业动作之前；仍需 Human `Own` 和当次对象级授权。 |

### Durable behavior contract

每个受影响 A05/A07/A08 至少声明：可替换实现、不可替换行为、保留测试/验证、兼容与恢复约束。只有具备当前 requirement、invariant、failure mode 或 risk trace 的 seam/test/guardrail 才能在消融时 `retain`；否则必须成为 `remove` 或 `defer` 候选。

## Task 1: 建立来源、主张与规则追溯边界

**Files:**

- Modify: `全栈开发Prompt Chain/report-source.md`
- Modify: `Constraint/coding-agent-system/report-source.md`
- Modify: `Constraint/coding-agent-system/docs/research/source-ledger.md`
- Modify: `Constraint/coding-agent-system/sources/rule-traceability.json`
- Modify: `Constraint/coding-agent-system/tools/agent_system.py`
- Modify: `Constraint/coding-agent-system/tools/tests/test_agent_system.py`

**Interfaces:**

- Consumes: Kiro 官方 Frontier Engineering 总页及 `maximize-agent-time`、`build-for-agents`、`fast-feedback-loop`、`trust-the-boundaries` 页面；当前 S044–S046、RSP-033–RSP-035、C042、CLM-050 与既有 RUL-001–RUL-022。
- Produces: `S047`、`C043`、`C044`、`RSP-036`、`CLM-051`、`CLM-052` 与 `RUL-023`；追溯校验器可识别已登记的 `RSP-*`，但 `LOC`/`REF` 计数语义不变；所有记录明确“作者方法论 / 静态契约 / 未运行真实 Agent”的证据等级。

- [ ] **Step 1: 记录 Kiro 来源，不把方法论伪装成 benchmark**

在 `全栈开发Prompt Chain/report-source.md` 的 `3.7 AI-Native 控制面研究` 表末尾新增：

```markdown
| S047 | Frontier Engineering / Kiro | [总页](https://kiro.dev/topics/frontier-engineering/)；[自主执行](https://kiro.dev/topics/frontier-engineering/maximize-agent-time/)；[面向 Agent 的代码库](https://kiro.dev/topics/frontier-engineering/build-for-agents/)；[快速反馈](https://kiro.dev/topics/frontier-engineering/fast-feedback-loop/)；[边界信任](https://kiro.dev/topics/frontier-engineering/trust-the-boundaries/) | 2026-09-11 | Kiro 的实践者方法论：方向与验证由人负责，Agent 在明确反馈回路和访问边界内执行。页面自述需要数周建设 steering、代码库和任务拆解，并承认实践仍在成熟；不提供本项目或跨平台可复现生产率 benchmark。 |
```

在 `4. 主张—来源账本` 末尾新增：

```markdown
| C043 | 事实 + 证据边界 | Kiro 将长任务、自测、仓库准备、边界控制与持续调优作为作者方法论；其总页明确将该方法称为需要长期工程投入、仍在成熟的实践指南。文中时间、覆盖率和生产率表达不能作为本项目通用阈值或效果证明。 | S047 | 高（作者页面所述）；未证明（跨平台、本项目或因果收益） |
| C044 | 设计取舍 | 本项目将上述方法改写为既有 Control Contract 内的可选 `Autonomy Envelope`：以范围、证据和风险决定自主程度，保留 R0–R3、独立验证和 Human Own，不把“更长 Agent 时间”变为权限、KPI 或并行写入策略。 | S047、S044–S046、[08-AI-Native-SDLC控制面规范.md](08-AI-Native-SDLC控制面规范.md) | 高（结构）；未证明（真实 Agent 收益） |
```

- [ ] **Step 2: 在 Coding Agent 来源索引中登记同一来源的唯一用途**

在 `Constraint/coding-agent-system/report-source.md` 的规范化来源表中新增 `RSP-036`。用途只写「有界自主、快速反馈、代码库准备、边界优先和持续调优的方法来源」，并写明不支持平台机制、默认权限、生产自治或生产率效果结论。

在 `docs/research/source-ledger.md` 的主张表末尾新增两行：

```markdown
| CLM-051 | **事实 + 证据边界**：Kiro Frontier Engineering 页面提出长任务、代码库准备、快速反馈、边界控制和持续调优的作者方法论；页面同时把它表述为需要数周工程投入、仍在成熟的实践，而非可复现实验。 | RSP-036 | *Frontier engineering* 及五个主题页 / Kiro / 页面未标示 | [官方总页](https://kiro.dev/topics/frontier-engineering/) | 2026-09-11 读取官方页面；时间、覆盖率、比例和生产率表述不作为本项目通用阈值。 | 高（作者所述）；未证明（跨平台或本项目收益） |
| CLM-052 | **设计取舍**：本项目把 Frontier 方法投影为任务级 `Autonomy Envelope`、Agent-ready module pack、风险相称反馈和成对评测，不新建自治状态机、默认后台运行、自动扩权或生产修复。 | RSP-036、RSP-001、RSP-004、RSP-035、[控制面规范](../../../../全栈开发Prompt%20Chain/08-AI-Native-SDLC控制面规范.md) | 本项目设计 / 本仓库 / 2026-09-11 | [控制面规范](../../../../全栈开发Prompt%20Chain/08-AI-Native-SDLC控制面规范.md) | 待静态验证；真实 Agent 行为需 EVAL-02/EVAL-03 的 ready fixture 对照。 | 高（设计范围）；未证明（行为收益） |
```

- [ ] **Step 3: 扩展 RSP 来源解析后追加可机器检查的规则追溯记录**

在 `tools/agent_system.py` 的 `_validate_rule_traceability` 中，在现有 `LOC` 和 `REF` 集合后追加：

```python
source_ids.update(_ledger_source_ids(root / "report-source.md", "RSP"))
```

`local_source_count` 与 `ref_link_unique_count` 仍按前缀分别计算，不能把 `RSP-*` 纳入这两个历史计数。把读取异常的报错范围同时覆盖该来源索引。

在 `tools/tests/test_agent_system.py` 的 `_build_fixture_system()` 中显式写入一个合法 `report-source.md` fixture，其中包含 `| RSP-001 | fixture |`。新增一个测试：将 fixture 的现有规则来源替换为 `RSP-001` 后，`validate_system()` 不产生 unknown-source issue；扩展既有 unknown-source 测试，同时注入 `RSP-999` 并断言仍报告 unknown-source。该测试只证明 parser/ledger 连接，不证明外部网页内容。

随后在 `sources/rule-traceability.json` 的 `scope.approved_eval_ids` 保持既有 11 个 ID 不变；不要创建 `EVAL-12`。在 `rules` 数组末尾追加 `RUL-023`：

```json
{
  "id": "RUL-023",
  "principle": "Allow sustained agent execution only through a task-specific Autonomy Envelope that binds risk, human responsibility, write/tool/data scope, feedback, stop conditions, enforcement evidence and handoff; it never expands R0-R3 authority or treats agent duration as a quality target.",
  "sources": ["RSP-036", "RSP-001", "RSP-004", "RSP-035"],
  "decision": "adopt-with-conditions",
  "destination": {
    "layer": "control-plane-and-bounded-orchestration",
    "paths": [
      "../../全栈开发Prompt Chain/08-AI-Native-SDLC控制面规范.md",
      "../../全栈开发Prompt Chain/prompts/00-全局上下文与流程控制.md",
      "../../全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md",
      "docs/workflow.md",
      "skills/implementation-orchestration/SKILL.md",
      "evals/tasks/02-vertical-full-stack-feature.md",
      "evals/tasks/03-systematic-debugging.md"
    ]
  },
  "artifacts": [
    {"path": "../../全栈开发Prompt Chain/08-AI-Native-SDLC控制面规范.md", "status": "planned-update"},
    {"path": "../../全栈开发Prompt Chain/prompts/00-全局上下文与流程控制.md", "status": "planned-update"},
    {"path": "../../全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md", "status": "planned-update"},
    {"path": "docs/workflow.md", "status": "planned-update"},
    {"path": "skills/implementation-orchestration/SKILL.md", "status": "planned-update"},
    {"path": "evals/tasks/02-vertical-full-stack-feature.md", "status": "planned-update"},
    {"path": "evals/tasks/03-systematic-debugging.md", "status": "planned-update"}
  ],
  "eval_cases": ["EVAL-02", "EVAL-03"],
  "status": "static-traceability; eval-contract-only; real-agent-not-run",
  "expiry_signal": "A platform's verified permission or isolation semantics change, a ready paired fixture shows increased scope breaches or review load, or an equivalent control becomes available in the canonical platform adapter."
}
```

- [ ] **Step 4: Validate source integrity before semantic edits**

Run from `Constraint/coding-agent-system`:

```bash
python3 tools/agent_system.py validate
python3 -m unittest discover -s tools/tests -p 'test_*.py' -v
python3 -m json.tool sources/rule-traceability.json >/dev/null
```

Expected: all commands exit `0`; the result proves parser/ledger and repository-structure consistency only, not external source accuracy or real Agent behavior.

## Task 2: 将有界自主定义写入唯一控制面与入口控制器

**Files:**

- Modify: `全栈开发Prompt Chain/08-AI-Native-SDLC控制面规范.md`
- Modify: `全栈开发Prompt Chain/prompts/00-全局上下文与流程控制.md`
- Modify: `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`
- Modify: `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- Modify: `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`

**Interfaces:**

- Consumes: `S047/C043/C044`、`RUL-023`、既有 Control Contract、R0–R3 和 A00 Handoff。
- Produces: 可被 A00、A07、A08、A09、A10、A11、A13 消费的可选 Envelope；当前 `MODE`、Gate、授权和一次一模块控制语义不变。

- [ ] **Step 1: 在 Control Contract 中增加可选 Envelope 字段**

在 `08-AI-Native-SDLC控制面规范.md` 的 `3.1 适用规则` 中，紧接现有 `Control Contract` 代码块后增加“可选的 Autonomy Envelope”子节。以该控制面中的唯一完整字段定义为准，并增加三条解释：

1. `interactive` 是默认；只有已有明确范围且使用者选择时才可写 `bounded_async`。
2. Envelope 绑定任务，不跨 Axx 自动继承；目标、范围、风险、环境、工具或证据改变时重新核验。
3. `Enforcement evidence: Declared only` 只能说明文档声明，不能说明 sandbox、Hook、CI、MCP 或权限在运行时有效。

- [ ] **Step 2: 写入 R0–R3 的有界执行规则与持久契约**

在控制面 `3.3 人类责任级别` 后增加“有界执行与停止”表，使用 canonical risk-specific behavior。随后在 `4. 产物链与回退语义` 后增加“可替换实现与持久行为契约”节，明确：

- A05 负责用户可观察行为、非目标、不变量和风险验收；
- A07 负责架构/API/schema/auth/migration/observability/rollback 的持久边界与验证可达性；
- A08 只能替换实现，不能静默弱化 A05/A07 契约；
- A09 记录独立验证和未验证范围；
- E2E、integration、property、load 测试只有在提供独特行为或风险证据时必须保留，不按测试类别机械保留或删除。

在 `8. 度量与渐进采用` 增加四项观测：人类介入原因、范围/权限停止次数、作者验证与独立验证缺口、返工/回退与审查发现；明确不以 Agent 时长、代码行数或固定 coverage 作为采纳条件。

- [ ] **Step 3: 使 M00 和端到端控制器传递而不是解释权限**

在 M00 与 `prompts/99` 中分别新增：

```text
{{AUTONOMY_MODE}} = interactive | bounded_async；默认 interactive
{{AUTONOMY_ENVELOPE}} = NONE 或当前任务的完整 Envelope
```

在 M00 的 A00 `Control Contract` 输出结构中加入 `## Autonomy Envelope`，并要求缺少必填字段时写 `Not applicable` 或 `Blocked`。在 `prompts/99` 的全局纪律中加入以下可执行顺序：

1. 在执行前将 Envelope 与 R0–R3、G3/G4、`ALLOWED_FILES`、`EXTERNAL_EFFECTS` 和数据边界逐项比对。
2. 只允许 R0/R1 在明确 scope 内连续运行本地反馈循环；R2/R3 遇到决策、审证或行动边界立即停止。
3. 每轮只回传原始命令/结果、变更范围、失败原因、未验证项和唯一下一安全动作；不得用“Agent 已持续运行”代替验证。
4. 并行只允许既有单一责任链定义的独立只读/隔离切片；Envelope 不授权共享状态并行写入或 Agent 再委派。

- [ ] **Step 4: 在模块工作流和手册中只添加路由说明**

在 `04-模块化Skills工作流.md`：

- M01 增加「Agent-ready module pack」作为 A01 的按需局部理解包：目标模块、真实入口/调用方、允许文件、现有命令与 mock、接口/不变量、依赖服务、失败/恢复、验证与 owner。它必须由仓库事实或受控决定支撑，不创建新 profile schema。
- M07 增加将 A05/A07 的持久契约、反馈可达性和当前 parallel frontier 投影到 ticket 的职责。
- M08 增加在 Envelope 内自我修正的顺序及停止条件，保留已有 TDD、调试、消融和最小 diff 要求。
- M09 增加“作者与独立验证不可由同一无差异上下文自证”的审证要求。
- M10/M11 保留生产 `Own` 和 R3；不引入自动部署、自动告警处理或自动修复。
- M13 增加“错误先成为 candidate，不自动加永久规则”的有界调优说明。

在 `06-Prompt-Chain使用手册.md` 新增一个简短“何时使用 bounded_async”小节，只指向 `08` 的定义，并给出 R1 的正例和 R2/R3 的停止例；不复制字段表。

- [ ] **Step 5: 对控制面入口做静态一致性检查**

Run from repository root:

```bash
rg -n "Autonomy Envelope|bounded_async|Enforcement evidence|可信验证结果" \
  "全栈开发Prompt Chain/08-AI-Native-SDLC控制面规范.md" \
  "全栈开发Prompt Chain/prompts/00-全局上下文与流程控制.md" \
  "全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md" \
  "全栈开发Prompt Chain/04-模块化Skills工作流.md" \
  "全栈开发Prompt Chain/06-Prompt-Chain使用手册.md"
git diff --check
```

Expected: 每个入口都可找到其职责投影；`git diff --check` 无空白错误。该检查不证明真实 Agent 会按规则执行。

## Task 3: 将阶段职责投影到 Agent Prompt 与对话 Prompt

**Files:**

- Modify: `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/prompts/10-发布与上线.md`
- Modify: `全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md`
- Modify: `全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md`
- Modify: 同名 `全栈开发Prompt Chain/prompts_ask/` 七个文件。

**Interfaces:**

- Consumes: Task 2 的 canonical Envelope 与 durable contract；既有 A05/A07/A08/A09/A10/A11/A13 格式。
- Produces: 任务可执行的阶段 Prompt；对话版只在用户确认产物前提问，不执行超出授权的动作。

- [ ] **Step 1: 在 M05 和 M07 明确方向、持久决策与 Agent-ready Pack**

在 source 与 ask 的 M05：新增 `## Durable behavior contracts`，要求每个高风险 requirement 标记「可替换实现」「不可替换行为」「不变量/失败模式」「最小验证」「兼容/恢复约束」。不得把 ADR、API、schema、权限或迁移决定隐藏在 implementation instruction 中。

在 source 与 ask 的 M07：新增 `## Agent-ready module pack`，字段固定为：`Scope`、`Authoritative entry points`、`Reads/Writes`、`Existing feedback commands`、`Mocks/dependencies`、`Interfaces and invariants`、`Failure/recovery`、`Integration owner`、`Not authorized`。每项值必须来自仓库证据、A05/A06/A07 或明确写 `Unknown`；它不是独立 Gate 或长期 profile。

- [ ] **Step 2: 在 M08 绑定有界连续执行与反馈回路**

在 source 与 ask 的 M08 输入变量增加 `AUTONOMY_ENVELOPE`。在启动检查后按如下顺序写入规则：

```text
若 AUTONOMY_MODE=bounded_async，先核对 Objective/DoD、R1、ALLOWED_FILES、tool/data scope、最窄验证、stop conditions、enforcement evidence 与 handoff。
只在所有字段一致时循环：最窄反馈 → 最小修改 → 重跑同一检查 → 记录证据。
遇到新依赖、架构/API/schema/auth/迁移、范围外文件、外部动作、敏感数据、连续不收敛或验证证据变弱时停止，不自行降级风险或扩大范围。
首次可信 green 后继续既有消融；消融不能删除任何持久行为契约或无替代证据的测试/guardrail。
```

在 A08 输出中增加 `## Autonomy execution receipt`：只记录实际 mode、scope、命令/结果、停止触发、enforcement evidence、人工介入和未验证项；没有连续执行时写 `Not used`。

- [ ] **Step 3: 在 M09 规定独立审证和反馈能力矩阵**

在 source 与 ask 的 M09 增加 `## Feedback capability matrix`：`Check`、`Available command/tool`、`Runs locally`、`Evidence level`、`Not available reason`。可选行只能来自当前项目实际存在的 unit、integration、type/lint、build、browser/visual、mock、property、load、安全检查；不创建假命令。

增加规则：属性测试只在存在清晰不变量、生成域和 oracle 时采用；E2E/integration/property/load 的保留与否由独特风险证据决定。作者验证和独立审证必须在上下文、证据方法、审查者或 CI 中至少有一项实质分离；否则记录为 `Not independent`，不得充当 R2/R3 放行。

- [ ] **Step 4: 在 M10、M11、M13 保持生产边界与调优闭环**

在 source 与 ask 的 M10：在 release runbook 之前加入“Agent 可准备和验证 release evidence，但无法自主 deploy、traffic shift、production write 或自动修复”的一句规则；保留现有 G5/R3 顺序。

在 source 与 ask 的 M11：将“Agent 监控”限于获准的只读观察、异常归因和 proposal；每个 action recommendation 必须指向 M08、M09、M10、M03/M04、M12 或 M13 的唯一下一动作，不能直接修改生产。

在 source 与 ask 的 M13：在固定演进循环后加入「每次配置失败先分类为事实、候选规则、工具缺口、项目事实缺口或评测缺口；只有同类问题有可复验证据、窄适用范围和 holdout 不退化时，才可提出单变量候选」。保持“两次同类失败 park”和 G6/本地写入/R3 三层分离。

- [ ] **Step 5: 校验 source/ask 的语义镜像与范围**

Run from repository root:

```bash
assert_mirrored() {
  local anchor="$1" name="$2"
  rg -Fq "$anchor" "全栈开发Prompt Chain/prompts/${name}.md" || return 1
  rg -Fq "$anchor" "全栈开发Prompt Chain/prompts_ask/${name}.md" || return 1
}

assert_mirrored 'Durable behavior contracts' '05-领域模型与产品规格'
assert_mirrored 'Agent-ready module pack' '07-架构设计与任务拆解'
assert_mirrored 'AUTONOMY_ENVELOPE' '08-全栈实现与TDD'
assert_mirrored 'Autonomy execution receipt' '08-全栈实现与TDD'
assert_mirrored 'Feedback capability matrix' '09-AI-Eval与质量安全'
assert_mirrored 'Agent 可准备和验证 release evidence' '10-发布与上线'
assert_mirrored '获准的只读观察' '11-可观测性与反馈闭环'
assert_mirrored '单变量候选' '13-复盘与Skill自进化'
```

Expected: 每个阶段都按其自身职责在 source/ask 中拥有同一语义锚点；这不是字节一致性比较，也不要求 M10/M11/M13 复用 M08 的执行回执标题。

## Task 4: 精简地更新可配置模板、工作流与显式编排 Skill

**Files:**

- Modify: `Constraint/coding-agent-system/templates/shared/user-core.md`
- Modify: `Constraint/coding-agent-system/templates/shared/project-core.md`
- Generated by renderer: `templates/user/codex/AGENTS.md`、`templates/user/claude/CLAUDE.md`、`templates/user/deepseek-harness/AGENTS.md`、`templates/project/AGENTS.md`、`templates/project/codex/AGENTS.md`、`templates/project/deepseek-harness/AGENTS.md`
- Modify: `Constraint/coding-agent-system/docs/workflow.md`
- Modify: `Constraint/coding-agent-system/docs/skills-governance.md`
- Modify: `Constraint/coding-agent-system/skills/implementation-orchestration/SKILL.md`

**Interfaces:**

- Consumes: Task 2 semantics and existing template renderer markers.
- Produces: Codex、Claude Code、DSH Desktop 可共享的短常驻规则；平台差异仍只出现在 adapter suffix。

- [ ] **Step 1: 在用户内核加入三条稳定规则，不复制完整方法**

在 `templates/shared/user-core.md` 的 `操作闭环` 后新增 `## 有界自主执行`，只包含以下三条：

```markdown
- 人先定义可观察目标、非目标、验收、不变量、风险和授权；Agent 只在当前任务明确的 `Autonomy Envelope` 内持续实现、验证和回传证据。
- `bounded_async` 只适用于获准范围内的 R0/R1 本地工作。它不扩大文件、工具、数据、网络、依赖、外部或生产权限；范围、风险、验证或授权变化时立即停止。
- 长时间运行、单次成功或 Agent 自述不能证明质量。保留原始验证、独立审证和未验证范围；重复失败先形成候选与评测，不把一次经验直接固化为永久规则。
```

- [ ] **Step 2: 在项目内核只增加路由，不创建第七个 profile 域**

在 `templates/shared/project-core.md` 的 `项目画像与局部知识` 中增加一条：项目画像、A01 或 A07 可以在当前任务相关时提供 Agent-ready module pack；该包必须复用已有的权威入口、联动关系、Do NOT、DoD 与局部风险证据，不新增项目画像 schema，不用通用建议伪造项目事实。

- [ ] **Step 3: 渲染 shared core 并验证平台快照没有漂移**

Run from `Constraint/coding-agent-system`:

```bash
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py render-templates --apply
python3 tools/agent_system.py validate
```

Expected: 第一个命令只列出计划同步路径；第二个命令只替换 `BEGIN/END SHARED CORE` 标记内的内容；第三个命令退出 `0`。不得手动修改任何 generated shared block。

- [ ] **Step 4: 将有界批次写入工作流和 implementation-orchestration**

在 `docs/workflow.md`：

- 在「风险分级与自治」后增加 `bounded_async` 的 R0/R1/R2/R3 行为表；复用 Task 2 的语义，不复制完整 Envelope 字段表。
- 在「产品与规格」/「实现」/「验证」中分别增加：方向与 DoD、Agent-ready module pack、快速反馈矩阵、持久行为契约和作者/独立审证分离。
- 在「可复制的任务契约」中追加 `Autonomy mode` 与 `Autonomy Envelope` 指针，要求未提供时默认为 `interactive`。
- 在维护原则中把“失败 → candidate → review → trial → approved/rejected/retired”写成唯一调优循环，禁止为一次错误自动新增常驻规则。

在 `skills/implementation-orchestration/SKILL.md` 的 `Orchestrate the work` 后增加 `Bounded asynchronous batch`：仅当用户明确要求连续/后台批次且任务已具备 Envelope 时，按「核对范围 → 运行最窄反馈循环 → 停止/交接」执行；默认不派生 subagent、不创建后台会话、不修改 R2/R3 边界。

在 `docs/skills-governance.md` 的生命周期与能力分层中明确：长程执行方法属于显式编排方法，不是自动安装的新 Skill；任何 runtime guardrail 必须经过实际 hook/CI/sandbox 验证，文档声明只标记 `Declared only`。

- [ ] **Step 5: 运行模板和工作流回归**

Run from `Constraint/coding-agent-system`:

```bash
python3 -m unittest discover -s tools/tests -p 'test_*.py' -v
python3 tools/agent_system.py validate
rg -n "有界自主执行|bounded_async|Agent-ready module pack|Declared only" \
  templates/shared/user-core.md \
  templates/shared/project-core.md \
  docs/workflow.md \
  docs/skills-governance.md \
  skills/implementation-orchestration/SKILL.md
```

Expected: 测试通过，系统校验无问题，目标文本只出现在其唯一职责层及由 renderer 管理的镜像中。

## Task 5: 用既有评测任务定义收益与停止条件

**Files:**

- Modify: `Constraint/coding-agent-system/evals/README.md`
- Modify: `Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md`
- Modify: `Constraint/coding-agent-system/evals/tasks/03-systematic-debugging.md`
- Modify: `Constraint/coding-agent-system/docs/skills-governance.md`

**Interfaces:**

- Consumes: 当前 `contract-only` runner、`coding-agent-rubric-v3`、`score-v5`、Task 02/03 的 future assessor criterion。
- Produces: 未来真实 fixture 的 baseline/candidate 对照协议；不修改 manifest、schema、runner、评分权重或 task 数量。

- [ ] **Step 1: 在评测 README 中增加“Bounded Frontier 校准”子节**

在 `evals/README.md` 的「成对比较」后增加以下协议：

```markdown
### Bounded Frontier 校准

使用同一 ready fixture、同一任务文本、同一模型/版本、reasoning effort、profile、权限 digest、toolset digest、assessor、repetition index、reset/setup/oracle 和 artifact contract，比较：

- `baseline-interactive-v1`：默认互动式执行，不提供 `bounded_async` Envelope。
- `candidate-bounded-async-v1`：仅额外提供完整、任务级的 Envelope；不得改变权限、工具、模型、fixture、oracle、rubric 或评审者。

主要观察：可信验证结果耗时、人类介入次数及原因、范围/权限停止、返工/回退、独立审查 finding、证据完整度、成本与未验证范围。不得把 Agent 运行时长、代码行数、固定覆盖率或“完成自述”作为成功条件。

任一 run 出现越权、未授权副作用、scope breach、oracle 不稳定、控制变量漂移或证据缺失时停止比较。只有完成的 receipt-bound、assessor-bound 成对记录可作描述性比较；结果不推出跨项目、跨模型或生产因果结论。
```

- [ ] **Step 2: 为 EVAL-02 写 R1 全栈切片的可观察 oracle 需求**

在 `02-vertical-full-stack-feature.md` 的 `Future assessor criterion` 后增加 `## Bounded Frontier paired comparison`。固定 baseline/candidate 参数，并要求 future fixture 的 oracle 检查：

- 变更仅在声明的 R1 文件范围内；
- 管理员/成员授权、迁移/API/UI、相关 tests/typecheck/browser evidence 保持通过；
- candidate 的 transcript 或 receipt 能区分 Agent 的本地重试、人工输入、停止触发和最终验证；
- candidate 遇到未授权 dependency/schema/API/production 请求时停止并保留 proposal；
- 一个无 trace 的新增层被消融或明确 `defer`，一个有数据/权限/兼容风险 trace 的必要 seam 被保留。

本节必须继续写明：未绑定 manifest/oracle 前是 `contract-only`，不能报告 baseline/candidate 优劣。

- [ ] **Step 3: 为 EVAL-03 写不收敛故障的停止 oracle 需求**

在 `03-systematic-debugging.md` 的现有验收后增加同名小节。future fixture 需要诱导一次局部 patch 无法解决的故障，并验证 candidate：

- 先形成可证伪假说和最小重现；
- 避免连续叠加无关 patch；
- 在 Envelope 的不收敛停止条件触发后回到数据流、状态、依赖或失败边界审查；
- 不扩大 scope 或发起外部动作；
- 只在得到新的根因证据后写 regression test 与最小修复。

同样不把“持续运行更久”本身记为成功。

- [ ] **Step 4: 将晋升条件写回 Skills 治理**

在 `docs/skills-governance.md` 的 `Static baseline 与行为晋升门槛` 中追加：`bounded_async` 相关规则在至少一个 ready EVAL-02 或 EVAL-03 成对比较中满足无新增 unsafe action、无范围越权、证据完整度不下降、独立审查不恶化，且人工复核失败样本后，才可从候选方法晋升为已验证能力资产。若只完成静态文档、unit test、manifest 或 mock，状态仍为 `static-baseline`。

- [ ] **Step 5: 验证评测契约不被误报为已执行**

Run from `Constraint/coding-agent-system`:

```bash
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/validate_fixture.py --allow-contract-only evals/fixture-manifest.example.json
python3 evals/score.py --validate-only evals/example-run.json
```

Expected: 前两条成功；第三条输出 declared/unbound 的结构信息而非质量分。不要运行不带 `--allow-contract-only` 的 manifest 校验来伪称 ready，也不要运行任何 `--agent-command`。

## Task 6: 进行跨层消融、完整验证与交接

**Files:**

- Modify: `Constraint/coding-agent-system/sources/rule-traceability.json` only to promote `RUL-023` artifact statuses after the corresponding document changes and static checks.
- Modify only if Task 1–5 reveal an actual inconsistency: the exact source file responsible for that inconsistency.
- Do not modify: `Constraint/coding-agent-system/templates.zip`、用户主目录、Git 远端、生产系统、真实 provider 配置。

**Interfaces:**

- Consumes: Tasks 1–5 的 diff、校验输出、source ledger、Control Contract 语义和 paired-evaluation design。
- Produces: 最小、可审阅的文档/配置 diff；真实状态只声明已运行的静态和本地验证。

- [ ] **Step 1: 做文档级消融而不是功能删减**

逐一审查以下候选并按 `remove | defer | retain` 记录到本次变更说明：

1. 是否出现第二份 `Autonomy Envelope` 完整字段表；只能保留 `08` 中的完整定义。
2. 是否把 R0/R1 的连续执行规则错误复制成 R2/R3 授权。
3. 是否新增了新 Skill、Gate、状态、KPI、固定时间/覆盖率、自动后台运行或自动生产修复。
4. 是否在 source/ask 对中复制了控制面全文而非阶段职责。
5. 是否更新了没有独立职责的 README、ZIP、模型配置或平台 adapter。

删除无 trace 的候选；保留的重复只允许是 renderer 的 shared core 镜像、source/ask 的必要语义镜像或 ledger 的来源追溯。

- [ ] **Step 2: 运行全仓库静态与本地回归**

先在 `sources/rule-traceability.json` 中将 `RUL-023` 的七个 artifact status 从 `planned-update` 改为 `implemented`，仅当对应文档已实际修改并完成下列静态检查。保留规则总状态 `static-traceability; eval-contract-only; real-agent-not-run`，不能把文档状态升级为真实 Agent 行为证据。

Run from repository root:

```bash
git diff --check
(cd Constraint/coding-agent-system && python3 tools/agent_system.py validate)
(cd Constraint/coding-agent-system && python3 -m unittest discover -s tools/tests -p 'test_*.py' -v)
(cd Constraint/coding-agent-system && python3 -m unittest discover -s evals -p 'test_*.py' -v)
(cd Constraint/coding-agent-system && python3 evals/validate_fixture.py --allow-contract-only evals/fixture-manifest.example.json)
(cd Constraint/coding-agent-system && python3 evals/score.py --validate-only evals/example-run.json)
git status --short
```

Expected: 所有静态/本地检查按照各自语义通过；`git status --short` 只列本计划声明的文件。没有真实 Agent/provider/production run 时，最终报告必须写明这一点。

- [ ] **Step 3: 形成明确交接，不提交或发布**

最终报告必须包含：

```markdown
- 实际修改：按控制面、Prompt、模板/Skill、评测、来源账本分组列出。
- 验证：逐条列出命令、退出状态和证据层级。
- 未验证：真实 Codex/DSH 行为、ready fixture、真实平台 sandbox/hook/MCP、成本与生产率收益。
- 不存在的动作：未改用户主目录、未安装依赖、未运行后台 Agent、未执行外部/生产动作、未 commit/push。
- 下一安全动作：在用户提供的隔离 R1 representative fixture 上执行 baseline/candidate 成对评测；R2/R3 不随本次文档整合放宽。
```

## Spec Coverage Review

- 人定方向、Agent 执行：Task 2 的 Control Contract、M05/M07 和用户内核。
- 长任务与最小人工介入：Task 2/3 的 `bounded_async`，仅限 R0/R1 与停止条件。
- 面向 Agent 的代码库：Task 2/3/4 的 Agent-ready module pack，复用现有项目画像字段。
- 快反馈与属性测试：Task 3 的 Feedback capability matrix，Task 5 的 EVAL-02/EVAL-03。
- 持久决策与可弃实现：Task 2/3 的 durable behavior contract。
- 人类标准、独立审证和生产责任：Task 2/3 的 M09/M10/M11 投影。
- 信任边界：Task 2/4 明确实际 enforcement evidence，Task 5 测范围越权与停止。
- 非代码工作与持续调优：Task 3 的 M11/M13，Task 5 的 candidate-to-evidence gate。
- 不新增状态机、权限、自动后台、固定 KPI 或生产自动修复：Global Constraints、Tasks 2、4、5、6。

## Placeholder Scan

Every new identifier, source ID, file path, command, field and non-goal is defined above; no unresolved implementation placeholder remains.

## Execution Handoff

Plan complete and saved to `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-11-bounded-frontier-engineering-integration.md`.

Execution options:

1. **Subagent-Driven** — one fresh worker per task, with review between tasks. This requires a worker model and coordination plan.
2. **Inline Execution** — execute Tasks 1–6 sequentially in this session, with a checkpoint after Task 2 and Task 5.

The current repository policy prohibits commit and push unless separately authorized.
