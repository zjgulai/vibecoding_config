# AI-Native SDLC 控制面规范

## 1. 目的、范围与不做什么

本规范在既有 `M00–M13`、`A00–A13`、`G0–G6` 和 `R3_ACTION_AUTHORIZATION` 之上，定义一层可恢复、可审计的控制面。它吸收“阶段产物链、独立验证、知识资产复利、认知债治理和生产门人工负责”的工程原则，但不替换现有工作流。

本规范的目标是缩短“可执行意图 → 可信验证结果”的周期，而不是最大化生成代码量、并行 Agent 数量或文档数量。

它明确不做以下事情：

- 不新建与 `A00–A13` 平行的 `intent/spec/plan` 状态机；既有 artifact 是唯一交接载体。
- 不把 `G5`、`G6`、Prompt、Skill、Hook、MCP 或子 Agent 解释为真实外部动作授权；R3 仍须逐对象、当次、未过期地批准。
- 不要求模型输出隐藏思维链，不设跨项目的固定 token、代码行数、重试次数或模型等级阈值。
- 不将单次成功、stars、作者背书、静态文档或工具通过写成真实平台行为或生产质量证明。

## 2. 核心术语

| 术语 | 定义 |
|---|---|
| **控制契约（Control Contract）** | 嵌入每个 Axx 的最小状态、授权、证据和回退信息；不是另一个任务台账。 |
| **artifact** | A00–A13 中任一持久产物；下游只能消费状态、新鲜度和输入都合格的 artifact。 |
| **人类责任级别** | `Delegate`、`Review`、`Own`。它说明谁完成工作、谁评审证据、谁承担不可转移的产品/生产决策。 |
| **作者验证** | 由实现者或其执行上下文运行的测试、静态检查、fixture 或 smoke。它必要但在 R2/R3 时不足以单独放行。 |
| **独立验证** | 与实现上下文分离的审证；可由另一 Agent、另一会话、CI 或人完成，但必须记录方法和局限。 |
| **能力资产（Capability Asset）** | 已验证、可复验、带适用边界的示例、fixture、命令、原型或决策模式。它不是未经核验的代码片段或网页收藏。 |
| **认知债** | Agent 产生的复杂度或关键行为已超过团队可解释、可预测、可安全修改的程度。 |
| **有界自主信封（Autonomy Envelope）** | 仅在当前任务明确选择 `bounded_async` 时填入的可选 Control Contract 字段组。它限定工作范围、反馈、停止和交接，不是新 artifact、Gate、Skill、权限或运行时调度器。 |

## 3. 控制契约

### 3.1 适用规则

每个非琐碎 Axx 都应包含下列 `Control Contract`。琐碎任务可在 A00/A08 的 Handoff 中以简版记录，但不得省略当前授权、证据层级和下一安全动作。

未知值必须写 `Unknown`、`Not applicable` 或 `Not authorized` 并附依据；不得用看似合理的内容填补。

```markdown
## Control Contract
- Contract version: 1
- Artifact / module: Axx / Mxx
- Status: draft | reviewed | approved | superseded | released | observed
- Objective and scope: <用户可观察目标；in/out of scope>
- Human responsibility: Delegate | Review | Own
- Risk and authority: R0–R3；Gates；允许/禁止动作；R3 status
- Authoritative inputs: <artifact、代码、来源、版本/日期、新鲜度>
- Context compatibility: <项目/平台/技术栈/数据边界；冲突或 supersedes>
- Acceptance and evidence: <criterion、作者/验证者、证据层级、未验证范围>
- AI behavior contract: <仅适用时填写模型/Prompt/工具/知识源/Eval 版本与边界>
- Cost and latency: <目标、观测值或 Unknown；不得编造预算>
- Recovery and route: <回滚/恢复前提、失效条件、唯一下一安全动作>
```

#### 可选的 Autonomy Envelope

默认模式为 `interactive`。只有当前任务的范围、风险、工具、数据和验收均已明确，且使用者明确选择时，才可使用 `bounded_async`。完整字段只在本规范中定义：

```markdown
## Autonomy Envelope
- Mode: interactive | bounded_async
- Risk and human responsibility: R0–R3 / Delegate | Review | Own
- Objective and Definition of Done: <当前可观察目标与验收>
- Write scope: <允许修改的路径；R0 写 Not applicable>
- Tool and data scope: <允许的本地命令、浏览器或 MCP；禁止项与数据边界>
- Required feedback loop: <最窄测试、type/lint、build、mock、browser 或其他实际可运行检查>
- Stop conditions: <范围、权限、失败、证据、依赖或风险升级>
- Budget and checkpoint: <任务级时间/重试/成本依据；非固定全局阈值>
- Enforcement evidence: Not available | Declared only | Verified by <sandbox/hook/CI/command evidence>
- Handoff: <主责任人、artifact、原始证据、未验证范围、唯一下一安全动作>
```

- `interactive` 可省略该节或写 `Not applicable`；不能因省略而推断获准连续执行。
- Envelope 只绑定当前任务，不能跨 Axx 自动继承。目标、范围、风险、环境、工具或证据变化时，必须重新核验。
- `Enforcement evidence: Declared only` 只表示文档声明，不能说明 sandbox、Hook、CI、MCP 或权限在运行时有效。

### 3.2 状态语义

| 状态 | 可表达的事实 | 不可表达的含义 |
|---|---|---|
| `draft` | 产物正在形成，结论尚待核验或批准。 | 已被产品、架构或生产放行。 |
| `reviewed` | 指定审查已完成，finding 和未验证范围已记录。 | 已获得行动授权。 |
| `approved` | 有命名决策者、范围、日期和失效条件的决定。 | 相邻目标、环境或副作用也获批准。 |
| `superseded` | 存在更新的权威 artifact、代码事实或决定。 | 可继续作为默认输入。 |
| `released` | 有已授权真实发布的 receipt 和验证层级。 | 已证明长期生产质量。 |
| `observed` | 有经授权的真实运行、反馈或指标证据。 | 已证明因果、永久有效或可推广。 |

### 3.3 人类责任级别

| 级别 | 适用场景 | Agent 可以做什么 | 必须由人做什么 |
|---|---|---|---|
| `Delegate` | R0/R1、局部可逆且验收清晰的工作 | 在获准范围内实现、验证、形成证据。 | 审阅异常、范围变更或结果采纳。 |
| `Review` | R2、关键设计、公共接口、AI 行为、权限或数据边界变更 | 提出方案、运行作者验证、准备独立审证材料。 | 审查取舍、残余风险和是否进入下一门。 |
| `Own` | R3、生产、外部动作、不可逆数据/权限/商业决定 | 只形成 proposal、runbook、dry-run 或只读证据。 | 批准具体行动，承担发布/事故/业务判断。 |

### 3.4 有界执行与停止

`bounded_async` 只描述任务内的连续本地工作，不改变责任级别、Gate 或对象级授权。

| 风险 | `bounded_async` 可以做什么 | 必须停止的位置 |
|---|---|---|
| R0 | 批量阅读、检索、dry-run、分析与只读验证。 | 数据边界、来源或任务范围不清。 |
| R1 | 在明确 `write_scope` 内执行实现、验证、修复和证据回传。 | 需要新依赖、超出范围、架构/权限/数据影响扩大，或验证不收敛。 |
| R2 | `bounded_async` 不适用。可在 `interactive` 下准备方案、作者验证、审证材料和有明确 G3/G4 的局部工作。 | 任何高影响决定、范围变化、独立审证缺失或实现者试图自我放行。 |
| R3 | `bounded_async` 不适用。只可在 `interactive` 下形成 proposal、runbook、dry-run 或获授权的只读证据。 | 任何真实外部、生产、不可逆或商业动作之前；仍需 Human `Own` 和当次对象级授权。 |

## 4. 产物链与回退语义

既有 artifact 与控制面角色的映射如下；名称不变：

| 产物 | 控制面角色 | 主要下游 |
|---|---|---|
| A00 | Intent、任务控制基线与恢复快照 | 所有场景入口 |
| A01 | 项目治理、环境与能力边界 | M02–M13 |
| A02/A03 | 机会和问题证据 | G1、M04 |
| A04/A05 | 策略、规格、验收和 AI 行为契约 | G2、M06/M07/M09 |
| A06 | 原型和可复用能力候选证据 | M07、M13 |
| A07 | 架构、可执行切片、并行前沿和整合责任 | G3/G4、M08 |
| A08 | 实现和作者验证 receipt | M09 |
| A09 | 独立质量、安全与 AI Eval 证据 | M10 或 M08 |
| A10 | Release readiness、R3 proposal/receipt | M11 |
| A11/A12 | 运行学习、实验和因果判断 | M03/M04/M05/M07/M08/M13 |
| A13 | 复盘、能力资产与 Skill/Memory 生命周期 | 下一轮 M00 或候选试用 |

正常路径不是只能向前的流水线。收到新证据时，控制器必须选择最小正确回退点：

- 问题或目标错误：回 M03/M04；
- 规格、数据边界或 AI 行为定义不足：回 M05；
- 架构、兼容、权限、并行或可维护性问题：回 M07；
- 可复现实现缺陷：回 M08；
- 发布、运行或实验事实改变：先经 M11/M12，再回到相应上游模块。

任何回退都保留旧 artifact 为 `superseded`，并写出触发证据；不得在下游静默修补上游假设。

### 4.1 可替换实现与持久行为契约

「代码可丢弃」只适用于可替换实现、原型和缺少独特行为证据的实现细节。A05、A07 与 A08 必须共同区分可替换实现、不可替换行为、保留测试/验证，以及兼容和恢复约束：

- A05 定义用户可观察行为、非目标、不变量和风险验收。
- A07 定义架构、API、schema、auth、migration、observability 和 rollback 的持久边界，以及验证可达性。
- A08 可以替换实现，但不能静默弱化 A05/A07 的契约。
- A09 记录独立验证、未验证范围和残余风险。

E2E、integration、property 和 load 测试只有在提供独特行为或风险证据时必须保留；不得按测试类别机械保留或删除。消融时，只有具备当前 requirement、invariant、failure mode 或 risk trace 的 seam、test 或 guardrail 可以 `retain`；其余必须成为 `remove` 或 `defer` 候选。

### 4.2 故事假设与条件式多目标投影

用户故事或产品故事线是待验证假设，不是新 artifact 或事实来源。它在既有产物链中的唯一投影是：

```text
A03 观察与可证伪故事假设
→ A04 已批准的价值转变与范围
→ A05 canonical product contract
→ A07 shared rules + conditional target adapters
→ A08 target-native implementation
→ A09 reference contract + native verification
→ A10/A11 获授权发布与实际观察
```

- 只有同一 A05 需要产生两个以上真实目标表示，或已有可测量的跨目标语义漂移时，A07 才引入 shared transform、跨目标契约与目标矩阵。单一目标只有在存在不可忽略、不能由简单配置表达的平台/协议/provider 差异时，才可引入一个窄 target adapter，并且必须先有该目标的 native validator；这不自动触发 shared transform、中间表示或跨目标矩阵。其他单目标应用继续使用垂直 slice。
- A05 是共享行为语义，不是某个目标的施工清单；A07 只把共同规则实现一次，并隔离 Web、API、数据、模型 provider 或部署目标的真实差异。
- A09 先验证 reference contract，再运行受影响目标的原生检查。不得为让单一目标通过而削弱已批准的共同契约。
- 生产观察与故事假设冲突时，按第 4 节回退 M03/M05；不得润色故事或在下游静默改变规格。
- 完整方法、启用条件与来源边界见 [`09-故事线驱动与编译式交付模式.md`](09-故事线驱动与编译式交付模式.md)。

## 5. 验证与生产门

| 风险 | 最低验证要求 | 放行规则 |
|---|---|---|
| R0 | 事实来源或静态检查。 | 在 G0 边界内继续。 |
| R1 | 作者验证：直接测试、fixture、type/lint 或 local smoke。 | 当前工作区可逆变更可按 G4 范围继续。 |
| R2 | 作者验证 + M09 独立审证；记录验证者、范围、版本、未验证项和残余风险。 | 需相应 G3/G4 决定；实现者不能成为唯一放行者。 |
| R3 | R2 的所有证据 + 人类 `Own` 决策 + 精确 `R3_ACTION_AUTHORIZATION`。 | 只允许授权清单中的当次动作；结果必须有 receipt。 |

对于含 AI 行为的工作，A05/A07/A09/A11 之间至少能追溯：模型/提供商、Prompt/规则、工具或 Skill、知识源/数据、评估集与 grader、质量/时延/成本护栏、fallback 和未覆盖风险。任一关键项变化都触发重新评估，而不是沿用旧结论。

## 6. 能力资产、认知债与并行

### 6.1 能力资产

候选先进入项目 Memory 的候选队列；只有经过真实可复验验证、脱敏和人工审查后，才可成为项目级能力资产。用户级索引只保存跨项目、脱敏的摘要与指针。

能力资产至少包含问题、环境/版本、可复验命令或 artifact、来源/许可证、适用边界、失败模式、数据与权限要求、owner、验证日期和过期条件。它不能因为一次成功自动进入全局 AGENTS、CLAUDE 或 Skill。

### 6.2 认知债检查

当修改触及陌生模块、复杂状态/并发、数据写入、权限/安全、关键 AI 行为、新依赖或高影响故障修复时，M07/M08 触发最小理解包：设计理由、关键数据/控制流、不变量、失败路径、真实文件/测试入口和恢复方式。

若阅读者仍无法预测主要失败模式，才升级为线性 walkthrough、架构图或交互式解释。普通小改不得被强制写成长篇文档；若理解成本超过未来价值，应回 M07/M08 进行消融、删减或重构。

### 6.3 单一责任链与并行

默认按**单一责任链**推进：只有一个主责任 Agent/人类整合者对当前 Axx 的完整性、衔接和回退负责。只有输入、文件、状态和验收真正独立的只读研究、测试、审计或隔离切片才可并行。每个并行任务必须有 `Owns / Reads / Returns / Must not / Done when`，并将结果交回 Axx；共享接口、数据迁移、权限、核心架构和生产动作不得并行写入。

## 7. Skill 与平台分层

Skill 采用 `candidate → trial → approved → retired` 生命周期。每个 Skill 必须说明触发条件、输入输出、禁止事项、权限/数据边界、依赖、验证方法、owner、版本和过期条件。

跨平台仅共享上述语义。Codex、Claude Code 和 DeepSeek Harness 的文件发现、Skill 调用、Hooks、sandbox 和权限实现由各自 Adapter 说明；Cursor 只作为规则设计参考，不是本规范的目标平台。

## 8. 度量与渐进采用

控制面效果只能通过代表性任务对照判断。默认记录：

- 从可执行意图到可信验证结果的时间；
- 首次通过率、返工/回退次数和逃逸问题；
- 验收项的证据完整度、未验证范围和人类 Review 负荷；
- 被接受变更的成本、时延与 AI 质量护栏；
- 能力资产/Skill 的试用成功率、过期率和退休原因。
- 人类介入的原因；
- 范围或权限停止的次数；
- 作者验证与独立验证之间的缺口；
- 返工、回退和审查发现。

不预设跨项目目标值，也不以 Agent 时长、代码行数或固定 coverage 作为采纳条件。先建立基线，再一次只变更一个控制面变量；只有静态文档控制经真实任务证明不足时，才讨论动态上下文、任务台账或自动证据收集等运行时编排。

## 9. 维护规则

- 本规范是 Control Contract、状态、人类责任、证据、回退与 R3 授权语义的单一真相源；`04-模块化Skills工作流.md` 是 M00–M13、A00–A13 与 G0–G6 模块/Gate 问题的规范映射，`06-Prompt-Chain使用手册.md` 只提供操作速查。09、M00、99 与平台 Adapter 只能引用或应用这两类既有语义，不再定义平行状态机、Gate 或授权规则。
- 平台、模型、Skill、Hook、MCP 或外部研究资料变更时，先更新来源账本和适用性判断，再更新规则。
- 任何实际写入用户级规则、项目规则、Memory 或 Skill 的晋升，仍须经过现有授权、备份/回滚和验证流程。
