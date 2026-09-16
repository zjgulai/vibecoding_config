# Prompt Chain 使用手册

## 1. 核心原则

Prompt Chain 的价值来自稳定的产物接口，而不是把全部阶段塞进一次超长对话。每个模块只解决一个主要决策，并把结果写成 `A00–A13` 之一；下一模块先核验文件是否新鲜、完整、与当前工作区一致，再使用它。

控制面字段、artifact 状态、人类责任和回退语义以 [08-AI-Native-SDLC控制面规范.md](08-AI-Native-SDLC控制面规范.md) 为准。它是既有 A00–A13 的统一交接语义，不是要求额外维护一套任务台账。

默认按「单一责任链」工作：一个主责任 Agent/人类整合者维护当前 Axx 的完整性、衔接与回退；只读研究、测试、审计或隔离切片只有在输入、文件、状态和验收都独立时才并行，且必须把结果交回同一个 Axx。

如果当前 Agent 没有文件写权限，让它在回复中按同名标题输出内容，再由你保存。不要因为不能写文件就省略 schema。

## 2. 通用输入变量

每个 Prompt 顶部都有变量表。复制时至少提供以下内容：

| 变量 | 含义 | 默认处理 |
|---|---|---|
| `{{PROJECT_ROOT}}` | 项目绝对路径或明确说明“无项目目录” | 缺失时只做无仓库的产品工作 |
| `{{PRODUCT_OR_TASK}}` | 产品、功能、故障或实验目标 | 缺失且无法从上下文确定时停止 |
| `{{MODE}}` | `PLAN` 或 `APPLY` | 默认 `PLAN` |
| `{{EXTERNAL_EFFECTS}}` | `DENY` 或列出精确授权动作 | 默认 `DENY` |
| `{{DATA_BOUNDARY}}` | 可读取的数据类型和禁止范围 | 默认不读 secrets、PII、`.env`、生产数据 |
| `{{TIME_OR_BUDGET}}` | 时间、token、成本或样本上限 | 缺失时提出有依据的最小范围，不伪造预算 |
| `{{KNOWN_ARTIFACTS}}` | 已存在的 Axx 文件、PRD、Issue、设计或测试 | 先验证存在性和新鲜度 |
| `{{HUMAN_RESPONSIBILITY}}` | `Delegate`、`Review` 或 `Own` | 未指定时由 R0–R3 与当前门建议；R3 保持 `Own` |
| `{{AUTONOMY_MODE}}` | `interactive` 或 `bounded_async` | 默认 `interactive`；后者必须有当前任务完整 Envelope |
| `{{AUTONOMY_ENVELOPE}}` | 当前任务范围、反馈、停止和交接的记录 | 默认 `NONE`；不是权限、Gate 或后台运行授权 |

变量不是要求全部手工填写。能从工作区和已确认产物查明的事实由 Agent 自行读取；只有会实质改变产品、架构、数据、权限、UX 或成本的缺口才询问。

## 3. 两种模式

### `MODE=PLAN`

- 允许读取授权范围内的文件和公开资料。
- 允许在回复中生成分析、计划、草稿、文件内容或拟落盘内容预览，但不写任何文件；Prompt 中的输出文件名只定义 artifact schema，不构成写入授权。
- 不修改产品代码、依赖、tracker、云资源或生产状态。
- 默认不 commit、push、发布或部署。

### `MODE=APPLY`

- 只有适用的 G3 决定、G4 本地写入授权、工作区与精确文件范围彼此匹配时，才允许完成可逆本地修改并运行已有验证；缺少任一项就退回 PLAN。
- 遇到 R2 架构、数据、权限、兼容性或核心 UX 决策时先展示方案和回滚。
- R3 外部或破坏性动作仍需对象级、当次明确的 `R3_ACTION_AUTHORIZATION`；G5/G6 的 readiness/design 决定不能替代它。

### 何时使用 `bounded_async`

完整字段语义以 [控制面规范](08-AI-Native-SDLC控制面规范.md) 的 `Autonomy Envelope` 为准；本手册不复制该字段表。

- R1 正例：一个已获 G4 批准的本地 ticket 已明确目标文件、允许命令、最窄测试、停止条件和交接责任。Agent 可以在这些范围内连续执行实现、验证、修复和证据回传。
- R2 停止例：任务需要选择公开 API、schema、auth、迁移或核心 UX 方案时，Agent 停在方案和作者验证材料，等待独立审证与相应 G3/G4 决定。
- R3 停止例：发布、生产读写、外部发送、付费调用或不可逆动作只允许形成 proposal、runbook、dry-run 或获授权的只读证据；实际动作仍需要 Human `Own` 与当次 `R3_ACTION_AUTHORIZATION`。

### 何时启用故事追踪与编译式交付

详细方法见 [09-故事线驱动与编译式交付模式.md](09-故事线驱动与编译式交付模式.md)。这两项是既有 Chain 的条件能力，不是必走的新阶段。

- 当产品决定依赖用户从现状到目标状态的转变时，在 M03–M05 启用故事追踪。故事必须写成可证伪假说，并绑定观察、可观察预测、反证、适用边界及 `SH -> FR/RISK -> AC`；叙事完整不是证据。
- 当最大不确定性是 Agent 与工具能否解决问题时，在 M06 使用 capability spike，以最小 TUI/CLI 和 deterministic fixture 验证闭环。当最大不确定性是交互、理解、信任、可用性或视觉层级时，使用 UI prototype；TUI 通过不能替代 UX 验证。
- Shared transform 与 target adapter 使用两道独立门：前者仅在至少两个真实目标共享同一 approved canonical semantics 时启用，并可进入目标矩阵；后者可用于多目标的目标原生差异，或单目标中不可忽略且不能由简单配置表达的平台差异。任何 adapter 进入实施前必须已有 native validator。
- 单目标 adapter 只形成该目标的 adapter 边界与 native 证据，不自动触发 shared transform、intermediate/reference contract、parity 或目标矩阵。没有真实差异时继续使用单路径，不为未来目标预建抽象。
- M11 必须比较预期用户转变与实际行为，统一使用 `Verified | Verified with caveats | Refuted | Unverified`；verdict 只判断 observation 是否支持预测，不证明因果。若两者冲突，保留反证和混杂因素，回到 M03 修订问题/工作流证据，或回到 M05 修订行为/验收规格。

## 4. 审批门 G0–G6

本节只作操作速查。完整的模块与 Gate 规范映射以 [04-模块化Skills工作流.md](04-模块化Skills工作流.md) 为准；`Control Contract`、artifact 状态、Human responsibility、证据、回退与 R3 动作授权语义以 [08-AI-Native-SDLC控制面规范.md](08-AI-Native-SDLC控制面规范.md) 为准。

| Gate | 决定 | 未通过时允许做什么 |
|---|---|---|
| G0 数据与任务边界 | 项目、数据、隐私、成本和允许动作 | 只读公开资料与不含敏感数据的本地事实 |
| G1 问题证据 | 目标用户、痛点、现有替代和证据是否足够 | 继续调研，不承诺解决方案 |
| G2 产品承诺 | 范围、成功指标、非目标和优先级 | 保持草案，不进入正式规格 |
| G3 架构与风险 | 数据模型、权限、安全、依赖、兼容和回滚 | 只做 prototype/ADR 备选，不实施高影响改动 |
| G4 实现授权 | 当前 slice、工作区写入、依赖和验证范围 | 保持 plan，不改代码或 tracker |
| G5 上线与生产 readiness | 环境、发布对象、凭据、回滚、观测和责任人是否就绪 | 只做 readiness/dry-run，不部署或访问生产 |
| G6 实验/晋升 design | 实验设计、流量、停止规则、Memory/Skill 采纳方案是否可进入动作提案 | 只生成实验或候选提案，不 launch/publish/adopt |

审批门不是一句“继续”就永久生效。G5/G6 的通用“通过”只表示 readiness/design；真实发布、生产读写或实验 launch 必须另列 `R3_ACTION_AUTHORIZATION`，逐项写 Target、Action、Expected effect、Credential scope（不含值）、Cost、Rollback、Verification、Idempotency/duplicate guard、Expiry。目标环境、数据集、仓库、分支、成本或副作用变化后必须重新确认。

## 5. Skill 调用规则

Prompt 中会列出“推荐 Skill”。使用规则：

1. Skill 已安装时，按平台支持方式显式加载 exact identifier。
2. Skill 未安装时，执行 Prompt 中已写明的方法，不声称调用成功。
3. `disable-model-invocation: true` 或 Codex `allow_implicit_invocation: false` 的 Skill 必须由用户显式选择，不能由另一个 Prompt 悄悄代替授权。
4. 调用 Skill 只选择方法，不扩大文件、网络、Git、tracker、凭据或生产权限。
5. 同职责 Skill 采用“一主一辅”，避免同时加载多个重叠的大型规则包。

## 6. 标准产物契约

每个 `Axx` 文件都必须包含规范定义的 `Control Contract`。以下是可复制的最小结构；完整字段语义和状态约束见 [控制面规范](08-AI-Native-SDLC控制面规范.md)。

```markdown
# <Artifact title>

## Metadata
- Module: Mxx
- Status: draft | reviewed | approved | superseded | released | observed
- Created/updated: YYYY-MM-DD
- Inputs: <文件和版本>
- Evidence level: static | dry-run | fixture | local-smoke | external-read | real-side-effect
- Mode: PLAN | APPLY

## Control Contract
- Human responsibility: Delegate | Review | Own
- Risk and authority: R0–R3；Gate；允许/禁止动作；R3 status
- Authoritative inputs and freshness: <来源、版本/日期、冲突或 supersedes>
- Acceptance and evidence: <作者/验证者、方法、未验证范围>
- AI behavior contract: <仅适用时填写模型/Prompt/工具/知识源/Eval 版本>
- Recovery and route: <失效条件、回滚前提、唯一下一安全动作>

## Facts
## Decisions
## Assumptions
## Open questions
## Risks and reversibility
## Acceptance evidence
## Handoff
```

模块可以增加专用章节，但不得删除 Facts/Decisions/Assumptions/Open questions 的区分。

`approved` 必须有命名决策者、范围和失效条件；`released` 和 `observed` 必须有对应的真实 receipt 或经授权运行证据。没有证据时使用 `draft`、`reviewed`、`Not authorized` 或 `Not run`，而不是提前声明完成。

## 7. 产物交接

```text
A00 Context Pack
  -> A01 Project Charter
  -> A02 Opportunity Brief
  -> A03 Problem Evidence
  -> A04 Product Strategy
  -> A05 Product Spec
  -> A06 Prototype Evidence
  -> A07 Architecture and Tickets
  -> A08 Implementation Report
  -> A09 Quality Evidence
  -> A10 Release Readiness
  -> A11 Production Learning
  -> A12 Experiment Decision
  -> A13 Retrospective
  -> 下一轮 A02/A03 或规则候选池
```

后一模块必须检查：输入是否存在、状态是否允许消费、是否晚于相关代码或决策、是否存在相互矛盾的 superseding artifact。不能只因文件名存在就继续。

新证据否定上游假设时，回到最小正确模块：问题/目标回 M03/M04，规格或 AI 行为回 M05，架构/并行/兼容回 M07，可复现实现缺陷回 M08。保留旧 artifact 为 `superseded` 并记录触发证据，不在下游静默补假设。

## 8. 四条推荐场景链

### Idea to MVP

`M00 → M01 → M02 → M03 → G1 → M04 → G2 → M05 → M06 → M07 → G3/G4 → M08 → M09 → M10 → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → receipt → M11 → M13`

资源有限时可以缩小调研样本和原型范围，但不能跳过 G2、G3、G5。

### Existing product feature

`M00 → M03（利用现有反馈）→ M04 → M05 → M07 → G3/G4 → M08 → M09 → M10 → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → receipt → M11 → M13`

若需求与架构已由新鲜、已批准的产物覆盖，可跳过重复访谈，但必须记录复用依据。

### Bug or incident

`M00 → M11（只读现象）→ M08 systematic-debugging → M09 regression/security review → M10 release-readiness → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → receipt → M11 verify → M13`

没有稳定复现，或缺少限定 provider、project、时间窗、数据范围和查询动作的 `R3_ACTION_AUTHORIZATION` 时，停在诊断，不用猜测 patch。

### Post-launch iteration

`M00 → M11 → M03 → M12 → G6 design → STOP → G5 readiness → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → receipt → M11 analyze → M04/M05 update → M07–M10 → M13`

实验结论必须包含样本、暴露、护栏、数据质量和停止条件；“指标上涨”不自动证明因果。未执行发布或 launch 时，receipt 与 M11 只能记录 `Not deployed / no production verification` 或 `Not launched / no production verification`。

## 9. 跨会话恢复

恢复时不要把整段历史重新粘贴。提供：

```markdown
## Goal
## Current module
## Approved gates
## Human responsibility
## Authoritative artifacts
## Latest evidence
## Unverified scope
## Open risks
## Next safe action
```

Agent 必须将该摘要与当前文件、代码和外部只读状态重新核对。摘要与事实冲突时，以新鲜证据为准，并记录修正。

## 10. 何时不使用完整链

- 文字修正、明确的小型代码改动：直接使用 M08/M09 的轻量路径。
- 只读解释：使用 M00 后回答，不创建多余产物。
- 已知根因的机械修复：可跳过完整 M03–M07，但仍需验收和验证。
- 单次架构咨询：使用 M07 的 `MODE=PLAN`，不自动进入实现。
- 生产事故：优先稳定、证据和回滚，不在事故中启动完整产品发现。

## 11. 消融式删减检查

用户说“进行消融实验”时，首选按“消融式删减检查”执行。它不是以删得更多为目标，而是在非琐碎设计或实现首次满足验收后，冻结 baseline：验收、不变量、风险和当前证据层级。

路由分工：M06/M07 在设计产物形成后分别做原型与架构/ticket 删减；M08 在首次可信 green 后只检查当前 diff；M09 只读独立审证，不自动修复。流程固定为 baseline → candidate → trace → 每次只处理一个候选并决定 `remove | defer | retain` → 同一验收/回归复验 → 最终相关回归。候选仅来自本轮新增设计或当前 diff，不清理历史无关内容。

所有非琐碎任务在相应 Axx 中使用：

```markdown
## Ablation evidence
- Baseline: 首次满足的验收、不变量、风险和命令/方法。
- Candidate: 仅本轮新增的可删减设计或实现。
- Trace: 当前 requirement、invariant、failure mode 或 risk；无则写 NONE。
- Decision: remove | defer | retain。
- Verification: 同一验收/回归的方法、结果和证据层级。
- Limitations: 未执行、不可重建时序或残余风险。
```

不得删去由安全、权限、数据完整性、兼容性、可访问性、可观测性、性能、migration、recovery、rollback 或已批准 UX 支撑的 seam；同样保护正确性、并发与失败语义。琐碎任务可只报告“无可安全删减候选”及依据；未执行时必须写明原因和未验证范围。该检查不扩大 Gate、文件写入、dependency、外部动作或生产权限。

静态或 contract-only 证据不能证明真实 Agent 行为，也不能证明 `gpt-5.6-sol` 的相对收益。

## 12. 质量检查

Prompt Chain 完成不等于产品完成。每一轮至少检查：

- 需求与验收是否双向可追溯。
- 事实和推断是否分开。
- 是否存在未授权副作用。
- 输出是否提供新鲜验证，而不是理论预期。
- 是否只修改当前 slice。
- 是否留下 secrets、PII、临时日志或不再使用的产物。
- Spec 与 Standards 两轴的重要 finding 是否关闭。
- 是否只检查本轮新增内容、是否逐项复验、保留/删除是否有 trace、M09 是否保持只读。
- 非琐碎 artifact 是否带有足够的 Control Contract；状态、授权、人类责任、验证者和回退路径是否与当前事实一致。
- R2/R3 是否同时有作者验证和独立验证；R3 是否仍停在人的对象级行动授权之前。
- UI 层级是否由界面类型、输入方式、信息密度、频率和任务优先级决定，而不是统一规格或装饰性放大。
- 用户可见改动是否有目标 viewport、主题和状态下的真实同屏证据。

Codex CLI 只使用项目已有或当前环境可用的本地浏览器、截图或视觉回归工具；工具不可用时写 `Visual verification: not run`，不依赖 Codex Desktop 右侧浏览器面板。
