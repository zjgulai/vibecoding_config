# Codex UI 视觉克制经验分层融合设计

## 目标

将用户于 2026-09-02 提供的 UI 开发经验转成可执行、可验证、可追溯的 Codex CLI 规则，并融入现有 Coding Agent 配置与全栈开发 Prompt Chain。

本次融合不把某种审美风格设为普遍真理。目标是建立一条判断链：识别界面类型与任务层级，复用项目设计语言，按上下文控制视觉显著性，完成真实同屏检查，并在不损害可用性和可访问性的前提下修正突兀实现。

## 已确认范围

- 当前目标平台只有 Codex CLI。
- 不修改 Claude Code、DSH Desktop / DeepSeek Harness 或 Cursor 配置。
- 保留现有用户级短常驻内核、项目级路由器和条件模块分层。
- 同步更新原始 Prompt 与 `prompts_ask` 对话版，避免两套语义漂移。
- 不安装 Skill、MCP、依赖或浏览器工具，不修改真实用户目录，不执行部署或其他外部动作。
- 当前工作目录不是 Git 仓库，因此不能提交 commit；使用文件清单、静态校验、内容哈希和独立审查作为变更证据。

## 价值分析

这段经验主要纠正四类 Coding Agent UI 偏差：

1. **无依据地放大和装饰。** 为了制造「高级感」而使用夸张尺寸、重色块、大圆角、厚边框、强阴影、渐变或营销页式构图。
2. **脱离同屏环境设计。** 单独看组件似乎合理，但放回页面后破坏层级、节奏和信息密度。
3. **为差异化重造通用图标。** 标准动作使用陌生隐喻，迫使用户重新学习。
4. **用统一规格替代场景判断。** 忽略界面类型、平台惯例、输入方式、信息密度、使用频率和任务优先级。

其最高价值是把视觉质量从一次性的审美判断，转成「发现事实—形成约束—实现—实际渲染—同屏复核—继续调整」的证据闭环。

## 需要改写的绝对化表达

- 「默认克制」仅是任务型产品、工具、设置和后台界面的默认偏置，不能覆盖营销、品牌、展示、安全警告和不可逆操作的真实职责。
- 视觉显著性由当前任务的重要性、后果和紧迫性决定。设置、开关和工具按钮只有在当前任务中确属次要时才应弱化。
- 视觉尺寸与交互命中区是两个维度。图标可以视觉收敛，但不能同步缩小可点击区域、文字、focus 或对比度。
- `hover`、`tooltip`、颜色和动效只能补充层级或说明，不能承载核心语义。歧义、低频或高后果动作需要可见文字和正确的 accessible name。
- 「不写死统一规格」不等于绕过项目 design tokens、组件规格、平台惯例或可访问性最低要求。
- 同屏复核发现「突兀」时不能机械缩小。应先判断任务影响，再调整填充、对比、字重、边框、阴影和留白，并复验可读性、命中区和 focus。
- 产品规格、任务优先级、错误状态和安全风险本身可以构成强调依据，无需等待用户额外说「请强调」。

## 核心不变量

> 视觉显著性应与当前任务的重要性、后果和紧迫性匹配。任务型产品界面默认收敛、克制并遵循成熟惯例，但不得牺牲可发现性、可读性、可访问性、交互命中区或风险表达。

## 架构方案

采用分层融合，避免将原文复制到每个文件。

### 1. Codex 用户级常驻偏置

在 `Constraint/coding-agent-system/templates/user/codex/AGENTS.md` 的共享块之外增加一个紧凑的条件章节：

- 仅当任务改变用户可见 UI 时生效。
- 要求优先读取项目可达的 `frontend-visual-quality` 规则。
- 项目规则不存在时，仍应用核心不变量、复用既有设计语言并要求真实渲染证据。
- 不在用户级文件复制完整检查清单。

这样只影响 Codex 用户模板，不会通过 canonical shared core 传播到其他平台。

### 2. Codex 项目级路由

在 `Constraint/coding-agent-system/templates/project/codex/AGENTS.md` 中增加条件路由：

- UI 任务且 `.agents/rules/frontend-visual-quality.md` 存在时，必须读取并遵循。
- 文件不存在时不得声称已加载；沿用用户级最小基线和项目既有规范，并把完整模块缺失记录为验证边界。
- 不在项目根文件复制完整 UI 规则。

平台中立 `templates/project/AGENTS.md` 的受管路由已由 `init-project --stack frontend-visual-quality` 生成，不手改该受管块。

### 3. 条件模块单一事实源

`Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md` 承载完整操作规则：

- 在「先发现项目事实」中增加界面类型、主次操作、高风险操作、输入方式、信息密度、使用频率、同屏基准和图标来源。
- 新增「视觉显著性、尺寸与图标」章节，写入带适用边界的完整规则。
- 在「验证命令与视觉检查」中增加静止态、同屏相对尺度、视觉重量、信息密度、图标理解和命中区检查。
- 若调整后可读性、focus、命中区或风险表达回退，则视为未通过。
- 没有实际查看渲染结果时，只能标记视觉未验证。

### 4. 生命周期 Prompt 投影

完整规则不重复进入每份 Prompt。M05–M09 只承载各阶段需要的决策和证据：

| 模块 | 职责 | 融合内容 |
| --- | --- | --- |
| M05 产品规格 | 定义可观察约束 | 记录界面类型、密度、平台/输入方式、主次和风险层级；将相对显著性、图标可识别性和状态反馈写成 acceptance，不规定跨场景统一像素或新依赖。 |
| M06 原型验证 | 验证高价值不确定性 | 读取同屏页面、tokens、组件和图标家族；备选方向主要在结构或流程上不同；实际比较静止态层级、图标理解和视觉重量。 |
| M07 架构与拆票 | 传递已确认约束 | UI ticket 追溯 A05/A06 的约束、例外、目标 viewport/状态、复用来源和同屏验证方法；不在本阶段重新设计。 |
| M08 实现 | 执行与自检 | 复用 tokens、组件和单一图标家族；实现后在目标 viewport/状态进行真实同屏复核；突兀或损害密度时继续调整并复验。 |
| M09 质量审查 | 独立验证 | 检查显著性是否匹配任务、核心语义是否依赖 hover/tooltip、危险动作保护、同屏密度和视觉重量；finding 必须追溯到规格、适用规则、设计系统或可观察任务影响。 |

同时更新：

- `全栈开发Prompt Chain/prompts/05–09`
- `全栈开发Prompt Chain/prompts_ask/05–09`

普通版是事实与安全边界来源；对话版镜像相同语义，并继续遵守每轮一个问题、完成摘要和确认后生成 Axx 的协议。

### 5. 工作流、控制器与行为评测

- `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md` 增加可失败 oracle：次要控件压过主任务、陌生图标只靠 tooltip、视觉缩小同时损害命中区、无同屏证据却宣称完成。
- `Constraint/coding-agent-system/docs/sop/project-lifecycle.md` 增加同屏比较、静止态层级和调整后的可访问性回归。
- `全栈开发Prompt Chain/04-模块化Skills工作流.md` 增加 M05 定义、M06 验证、M07 传递、M08 实现、M09 审查的 UI 跨模块契约。
- `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md` 明确 Codex CLI 只使用项目已有或当前环境可用的本地浏览器、截图或视觉回归工具；工具不可用时标记未验证，不依赖 Codex Desktop 右侧面板。
- `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md` 只增加控制器不变量：用户可见 UI 变更必须携带上游视觉约束，并在 M08/M09 提供真实同屏渲染证据。

### 6. 来源与规则追踪

为保持现有审计结构一致：

- 在 `docs/research/local-tip-ledger.md` 新增 `LOC-030`，标记为 2026-09-02 用户明确提供并确认采用的 UI 经验。
- 在 `docs/research/tip-decision-matrix.md` 新增原子决策，记录保留、条件化和排除的理由。
- 在 `sources/rule-traceability.json` 新增对应聚合规则，关联 Codex 用户偏置、视觉模块、M05–M09 Prompt 投影和 `EVAL-05`，并将本地来源计数更新为 30。
- 在 `docs/research/local-material-audit.md` 添加后续来源说明，明确 `LOC-030` 不属于原始 29 文件审计，避免改写历史事实。

## 计划修改的文件

### Codex 与条件模块

- `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`
- `Constraint/coding-agent-system/templates/project/codex/AGENTS.md`
- `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`

### Coding Agent 工作流、评测与追踪

- `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md`
- `Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
- `Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
- `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
- `Constraint/coding-agent-system/docs/research/local-material-audit.md`
- `Constraint/coding-agent-system/sources/rule-traceability.json`

### Prompt Chain

- `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`

## 明确不修改

- `Constraint/Codex_AGENTS.md`：旧材料已被萃取，正文重复且不参与当前安装工具链。
- `templates/shared/user-core.md` 与 `templates/shared/project-core.md`：避免把条件 UI 偏好传播到其他平台或污染项目路由职责。
- `templates/project/AGENTS.md` 的受管模块块：由生成器维护。
- Claude、DSH、Cursor 相关模板与配置。
- `templates.zip` 和 `全栈开发Prompt Chain.zip`：不是本次工具链的规范源或自动派生产物。
- 真实 `~/.codex/AGENTS.md`：本次只更新可配置模板，不覆盖用户当前配置。

## 验收标准

### 语义与边界

- Codex 用户级规则只保存条件触发和最小默认偏置，完整规则只有一个事实源。
- Claude、DSH 和 Cursor 文件没有变化。
- 规则没有把克制解释为缩小文字、focus、对比度或命中区。
- `hover`、`tooltip`、颜色和动效没有成为核心语义的唯一通道。
- 图标优先复用项目已有家族；规则不隐式授权新增 dependency。
- 营销、品牌、安全、无障碍和当前主任务存在明确例外，不被任务型界面的默认风格覆盖。

### Prompt 一致性

- `prompts` 与 `prompts_ask` 的 M05–M09 语义成对存在。
- M05 不写死跨场景统一规格；M07 不重新做视觉决策。
- M08 要求目标 viewport、状态和同屏基准的实际渲染检查。
- M09 finding 必须有规格、规则、设计系统或可观察任务影响作为证据，不能只写个人审美。
- 对话版保留单问题协议、公共八段、确认后生成和原有 Gate/R3 边界。

### 静态与工具验证

- 运行 `python3 tools/agent_system.py render-templates`，确认共享快照无意外漂移。
- 运行 `python3 tools/agent_system.py validate .` 和现有相关单元测试。
- 在临时空目录中 dry-run 或生成带 `frontend-visual-quality` stack 的项目，验证根路由和模块可达性；不写真实项目。
- 检查 Markdown 围栏、UTF-8、旧授权字段、A05–A09 产物结构和 13 份 `prompts_ask` 公共契约。
- 比较写后 native size 与可读字节数，并记录最终内容哈希。
- 由独立审查者分别检查规则边界、Prompt 同步和 fail-open 风险。

## 未验证边界

- 本次只能验证静态规则、生成器、文档结构和隔离生成结果。
- 不安装或调用真实浏览器工具，不执行页面视觉回放。
- 不运行真实 Codex CLI 行为基准，`EVAL-05` 仍是行为评测契约而非已经获得的模型效果证据。
- 不证明该审美偏置适合所有产品；项目规格、品牌系统、平台约定和可访问性要求始终可以覆盖默认偏置。
