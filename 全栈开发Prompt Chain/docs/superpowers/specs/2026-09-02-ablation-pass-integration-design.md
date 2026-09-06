# Codex 消融式删减检查融合设计

## 目标

将用户于 2026-09-02 提供并确认采用的实战方法，改写为可执行、可验证、可追溯的「消融式删减检查」，并融入 Codex 用户规则与全栈开发 Prompt Chain。

本次不把「删得更多」当作目标。目标是在设计或实现首次满足验收后，使用反事实检查识别本轮新增但没有当前需求、不变量、失败模式或风险依据的抽象和设计，且只在同一组验收仍然成立时保留删减结果。

## 价值判断

这条经验与现有「单一用例不预建抽象」和「最小可追溯修改」一致，但有一个独立增量：现有规则主要在实现前约束设计，消融式删减在得到可运行或可评审的结果后，再做一次有基线的删减验证。

该方法可以纠正 Coding Agent 常见的三类偏差：

1. 为可能的未来需求预建 layer、interface、adapter、registry、config 或 extension point。
2. 将「结构看起来完整」误当成「当前产品目标需要」。
3. 首次 green 后直接结束，未再检查间接层、配置、依赖、通用性和 UI 设计元素是否真正承载需求。

用户观察到这条提示对 `gpt-5.6-sol` 尤其有效。该结论作为用户实战证据记录，不写成已经固定 fixture、模型、reasoning、权限和评分器的跨模型比较结论。

## 术语与核心不变量

本系统使用「消融式删减检查」作为首选术语。只有在固定控制变量、对照、评测和重复次数时，才把模型效果评价称为严格的「消融实验」。用户可继续用「进行消融实验」触发该检查，Agent 不需因术语差异要求用户改口令。

> 非琐碎设计或实现首次满足验收后，执行一次受限消融：固定当前验收、不变量和风险边界，只对本轮新增内容逐项尝试移除缺少当前需求、不变量、失败模式或风险依据的抽象与设计；每次只移除一个候选，并使用同一组验收和回归检查复验。只有在必要质量不退化时，才保留删减结果。

「必要质量」至少包含正确性、安全、权限、数据完整性、兼容性、并发和失败语义、可访问性、可观测性、性能约束、迁移/恢复/回滚能力以及已批准的用户体验。「代码更少」、「文件更少」或「局部测试仍为 green」都不能单独证明方案更优。

## 规模与触发

- 凡本轮形成可取舍的产品范围、原型、架构、UI 方案或代码实现，都执行一次删减检查。M04 现有的「最小可验证价值链 + non-goals + no-build 基线」视为产品范围消融；M05 是对已批准需求的忠实规格化，不另设删需求步骤。
- 琐碎任务可只记录「无可安全删减候选」及判断依据，不为了仪式创建表格、文件或候选数量。
- 非琐碎任务必须保留 baseline、候选、`remove | defer | retain`、依据和复验结果。
- 只有用户明确要求跳过，或当前环境无法安全建立基线时才不执行。未执行时记录原因和未验证范围，不宣称已通过。

## 执行协议

### 设计消融

设计消融只改设计产物或已批准的隔离原型，不隐式授权代码、项目配置或外部系统写入。

1. 固定已批准的 acceptance、不变量、风险、用户流程和当前设计基线。
2. 只从本轮新增设计中提取候选，例如无当前调用方的 seam/interface/adapter/layer、推测性扩展点、可延后 ticket、原型中与学习问题无关的流程或 UI 元素。
3. 每次只假设移除一个候选，在同一 acceptance、fixture、viewport、不变量和风险边界下比较。
4. 能移除时将其删除或延后；不能移除时，记录它承载的具体需求、不变量、失败模式或风险。
5. 生成删减后的最小设计、保留理由、未解决风险和下游验证要求。

### 实现消融

实现消融只在当前 slice 首次取得可信 green 证据后执行，且不扩大 G4、`ALLOWED_FILES` 或 `DEPENDENCY_CHANGES` 授权。

1. 固定首次 green 的验收、命令、结果、变更范围和必要质量边界。
2. 只从本次 diff 提取候选：一次性 wrapper、无当前调用方的 abstraction、间接层、推测性 genericity、无依据 config/flag、可避免 dependency、重复状态层以及本轮造成的 orphan。
3. 每次只移除一个候选，立即重跑覆盖其的最窄验收或回归。若失败、证据变弱或风险上升，恢复该候选并记录保留理由。
4. 候选处理完成后，重跑与当前风险匹配的相关回归、type/lint/build 和必要的运行验证。
5. 报告删除项、保留项、对应依据、验证命令和未验证范围；不用行数、文件数或自评「更简单」替代行为证据。

### 独立审查

M09 只读核对 A07/A08 和固定 diff，不自动执行删减或修复。

- 检查基线、候选、`remove | defer | retain`、依据、命令和结果是否可追溯。
- 检查保留的新抽象是否有当前调用方或具体风险依据，删除的边界是否仍由验收和回归支持。
- 无证据时写 finding 或 `Unverified scope`，不以 Agent 自述或最终测试 green 替代过程证据。
- 消融 finding 仍归入现有两轴：范围外设计归 Spec，无依据复杂度或删除质量边界归 Standards；不新增第三个审查轴。

## 证据结构

非琐碎任务在对应 A06、A07 或 A08 产物中增加如下字段：

```text
## Ablation evidence
- Baseline: 首次满足的验收、不变量、风险和命令/方法。
- Candidate: 仅本轮新增的可删减设计或实现。
- Trace: 候选对应的需求、不变量、失败模式或风险；无则写 NONE。
- Decision: remove | defer | retain。
- Verification: 同一验收/回归的方法、结果与证据层级。
- Limitations: 未执行检查、不可重建的编辑时序或残余风险。
```

M09 使用 `## Ablation evidence review` 核对该记录与实际 diff，不重写一份执行报告。

## 生命周期落点

| 模块 | 职责 | 消融投影 |
| --- | --- | --- |
| M06 原型与 UX 验证 | 设计消融 | 在原型方向形成后、`Accept | Revise | Reject` 之前，移除不能帮助回答当前学习问题的交互、流程和 UI 元素。 |
| M07 架构与垂直切片 | 设计消融 | 在冻结架构、ticket 和 G3/G4 请求前，检查新增 abstraction、interface、seam、adapter、layer、dependency、config 和 ticket。 |
| M08 实现与 TDD | 实现消融 | 当前 slice 首次 green 后、最终相关回归前，只对本轮 diff 逐项删减并复验。 |
| M09 AI Eval、质量与安全 | 独立审证 | 核对消融候选、删减/保留决定、追溯和复验；不自动修复。 |

M00–M03 是上下文、研究和问题证据阶段，不是设计/实现收尾。M04 已用「最小可验证价值链」、non-goals 和 no-build 基线执行产品范围删减。M05 必须忠实转译已批准需求，不得借消融静默删除需求。M10 不在发布前改变已审查的 review range。M11 负责生产证据，M12 的 experiment 为产品因果实验，M13 已有人工晋升治理；这些模块不重复添加删减动作。

## 配置与文档分层

### Codex 用户规则

在 `Constraint/coding-agent-system/templates/user/codex/AGENTS.md` 的 shared core 之外增加紧凑常驻触发，不写入模型优劣结论。不修改 `templates/shared/user-core.md`，避免将尚未完成跨模型对照的执行方法自动传播给 Claude 或 DeepSeek Harness。

项目级 `AGENTS.md` 不复制用户工作偏好，也不为这个短协议新建 module 或 Skill。项目事实、局部约束和更严格的验收仍可覆盖候选与保留边界。

### 前端模块

`templates/modules/frontend-visual-quality.md` 增加 UI 专用投影：对本轮新增的容器、装饰、强调、控件和交互步骤逐项隐藏或移除，在相同 viewport、状态和任务下比较。可发现性、可读性、可访问性、命中区和风险表达仍是不可删除边界。

### SOP、工作流与控制器

- `docs/sop/project-lifecycle.md` 定义一次完整协议，并在阶段 5、6、10 和 11 投影设计、实现、审证和最终报告职责。
- `04-模块化Skills工作流.md` 只在 M06–M09 增加角色与验收，不复制协议全文。
- `06-Prompt-Chain使用手册.md` 集中说明触发语句、执行步骤、证据格式、琐碎任务缩放和不可删除边界。
- `prompts/99-端到端Prompt-Chain.md` 只增加一条路由纪律：M06/M07 负责设计消融，M08 负责实现消融，M09 独立审证，不跨模块扩大写入权限。

### Prompt 投影

同步修改 `prompts/06–09` 与 `prompts_ask/06–09`。普通版承载阶段动作与证据；对话版镜像相同语义，但保留 `MODE=PLAN`、每轮一个问题、确认后生成 Axx 和原有 Gate/R3/文件范围边界。

### 来源与评测

追溯链复用现有规则与评测：

```text
LOC-031 → TIP-078 → RUL-004 → EVAL-02 + EVAL-06
```

- `LOC-031` 记录用户实战观察、条件化改写和「未运行固定模型成对评测」的边界，不计入原始 29 个本地内容文件。
- `TIP-078` 记录原子方法、采用理由、删减边界和未验证的模型效果。
- `RUL-004` 已覆盖最小可追溯修改、避免投机抽象和只清理本轮 orphan；本次只增加新来源与执行产物，不新建语义重叠的 `RUL-023`。
- `EVAL-02` 增加实现消融 oracle：一个无依据诱导性层级应被删除，一个承载安全/兼容风险的 seam 应被保留，且全部行为仍通过。
- `EVAL-06` 增加审查 oracle：检查审查者能否区分无依据复杂度、有必要风险边界与范围外清理。
- 不新建 `EVAL-12`。新增固定评测 ID 需同步扩大工具、schema、fixture manifest、测试与文档枚举，这个额外系统复杂度没有当前收益证据。

`EVAL-02` 与 `EVAL-06` 仍为 `contract-only`。本次不创造真实 Next.js/PostgreSQL/browser fixture，不将静态规则作为 Agent 已经执行过消融的证据。

## 计划修改的文件

### Codex 规则与专项模块

- `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`
- `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`

### Coding Agent SOP、评测与追溯

- `Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
- `Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md`
- `Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md`
- `Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
- `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
- `Constraint/coding-agent-system/docs/research/local-material-audit.md`
- `Constraint/coding-agent-system/sources/rule-traceability.json`

### Prompt Chain

- `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`

## 明确不修改

- `Constraint/coding-agent-system/templates/project/codex/AGENTS.md`：这是用户工作偏好，不是项目事实或项目局部路由。
- `Constraint/coding-agent-system/templates/shared/user-core.md` 和 `templates/shared/project-core.md`：不在未运行跨模型对照前传播到其他平台。
- Claude、DeepSeek Harness 和 Cursor 的配置、模板和历史材料。
- `Constraint/Codex_AGENTS.md`：它是已审计的旧输入材料，不是当前规范源。
- M00–M05 与 M10–M13 的普通/对话 Prompt，以及 `templates/modules/typescript-nextjs.md`。
- 现有 11 个评测 ID 的固定枚举、fixture schema 和 manifest。
- `templates.zip`、`全栈开发Prompt Chain.zip` 与前一轮 UI 视觉克制任务的历史报告。
- 真实 `~/.codex/AGENTS.md`、生产系统、外部 tracker、provider 或部署环境。

## 验收标准

### 语义与范围

- 「消融」只处理本轮新增的设计或 diff，不变成历史代码清理。
- 设计、实现和审证职责分离；M09 不自动修复。
- 实现消融在可信 green 之后运行，每次只移除一个候选，并复用同一验收。
- 删减不能扩大写入、dependency、外部动作或生产权限，也不能通过删除测试或降低验收制造 green。
- 安全、权限、数据完整性、兼容性、可访问性、可观测性、迁移/恢复/回滚和已批准用户体验只能根据对应需求或风险证据删改，不因「少一层」自动移除。
- 琐碎任务不强制创建长报告；非琐碎任务保留完整 `Ablation evidence`。

### Prompt 与控制契约

- M06–M09 普通版与对话版的角色语义成对存在，不复制整份协议。
- 对话版保留公共八段、单问题协议、生成确认门和原有 Gate/R3/写入范围语义。
- M06 不把原型学习结论写成生产实现；M07 不借删减绕过 G3；M08 不超出 `ALLOWED_FILES` 或修改未授权 dependency；M09 继续只读。
- M09 将范围外设计归 Spec，将无依据复杂度或错误删减必要边界归 Standards，不增加第三轴。

### 追溯与验证

- `LOC-031`、`TIP-078` 各恰好一条，并通过 `RUL-004` 连到实际产物与 `EVAL-02/EVAL-06`。
- `scope.local_source_count` 从 30 更新为 31；原始材料统计仍为 29 个文件、76 条 Tips。
- `rule-traceability.json` 保持结构有效；`implemented` artifact 必须真实存在。
- `EVAL-02/EVAL-06` 明确为 `contract-only`，不声称已验证 `gpt-5.6-sol` 相对其他模型的提升。
- 运行 Coding Agent system `render-templates`、`validate .`、eval 测试与 tools 测试；运行 Prompt 标题、围栏、阶段投影和授权边界的静态检查。
- 独立审查规则/边界、Prompt 普通/对话镜像、追溯/评测一致性；所有 Critical 和 Important finding 关闭后才可宣称完成。

## 未验证边界

- 本次只能验证静态规则、Prompt 结构、追溯 JSON、隔离生成和现有测试契约。
- 不运行真实代码删减 fixture、浏览器、外部 provider、生产环境或付费调用。
- 不能从最终文件系统状态重建「每次只移除一个候选」的真实编辑时序；该过程需执行 receipt 或 runner 证据。
- 「对 `gpt-5.6-sol` 尤其有效」仍是用户实战观察；如需升级为因果结论，需将相同 fixture、client、model、reasoning、permissions、toolset、assessor 和 repetition 固定后做成对比较。
