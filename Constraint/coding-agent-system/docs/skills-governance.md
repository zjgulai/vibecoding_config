---
title: Coding Agent Skills 与能力层治理
doc_type: governance
module: coding-agent-system
topic: skills-and-capability-governance
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# Coding Agent Skills 与能力层治理

本文规定 15 个 Skill 的路由、Codex / DSH 适配、既有 Claude 兼容副本、第三方来源治理、晋升与回滚流程，以及用户级短常驻内核、项目画像、Memory、技术栈模块、controls、hook 与 MCP 的职责边界。目标不是增加尽可能多的提示词，而是让 Agent 在需要时获得恰好足够的方法，同时保持授权、安全和验证边界不变。

本文件是治理规范，不是权限配置，也不自动安装、更新或发布任何 skill。实际生成与安装行为以 [`tools/agent_system.py`](../tools/agent_system.py) 和对应测试为准。

## 15 个 Skill 的路由

| Skill | 何时使用 | 不应使用 | 默认路由 |
| --- | --- | --- | --- |
| `product-discovery` | 产品目标、用户、数据、权限或取舍尚未收敛，并且用户明确要求需求发现或方案压力测试时。 | 低风险且边界清楚的小修改；已经确认的规格进入实现时。 | 显式调用。 |
| `specification` | 需求已讨论清楚，需要整理为可实现、可验收的规格，并且用户明确要求产出或更新 spec 时。 | 仍需产品访谈的模糊需求；直接写代码的简单任务。 | 显式调用。 |
| `vertical-ticketing` | 已批准的规格或计划需要拆成可独立验收的垂直 tickets 与依赖图，并且用户明确要求拆票时。 | 用技术层横切工作；规格关键决定仍未解决时。 | 显式调用。 |
| `tdd` | 新增行为或修复缺陷需要自动化反馈约束，或用户要求 red-green-refactor 时。 | 没有稳定测试 seam、纯文档修改，或测试成本明显高于风险的小改动。 | 可隐式路由。 |
| `systematic-debugging` | 根因不明、跨模块、flaky、性能回退或需要可证伪假设的故障。 | 根因已有直接证据、只需机械修正的任务。 | 可隐式路由。 |
| `two-axis-code-review` | 审查 branch、PR、工作区 diff 或指定比较范围，并需分别检查 Standards 与 Spec 时。 | 用户已经授权实施修复的编码任务；没有可确定审查范围时。 | 可隐式路由。 |
| `writing-for-agents` | 创建或精简 `AGENTS.md`、`CLAUDE.md`、rules、skills 或其他 Agent 指针文档。 | 普通面向人的技术文档；只需修正代码注释时。 | 可隐式路由。 |
| `safe-prototyping` | 需要用隔离、一次性的逻辑或 UI 原型回答一个明确设计问题。 | 生产实现、真实数据试验、完整功能开发或无停止条件的开放探索。 | 可隐式路由。 |
| `project-profile` | 用户明确要求初始化、补全或审计长期项目画像时。 | 普通代码探索、产品发现、规格编写或直接实现。 | 显式调用。 |
| `memory-governance` | 用户明确要求审查 Memory 候选、晋升建议、冲突、过期或隐私风险时。 | 自动写正式规则、保存原始对话、单次成功经验或秘密。 | 显式调用。 |
| `technical-research` | 需要核实技术事实、API、标准或版本行为，且一手来源会改变结论时。 | 只需一般建议、二手材料摘要或无明确问题的泛化调研。 | 可隐式路由，限强匹配。 |
| `domain-modeling` | 领域术语冲突、概念边界不清，或需要判断是否值得记录 CONTEXT/ADR 时。 | 仅消费既有术语、纯实现细节或没有共享语言问题的编码任务。 | 可隐式路由，限强匹配。 |
| `codebase-design` | 模块 interface、seam、adapter、可测试性或 locality 的设计取舍需要分析时。 | 单实现的假想抽象、纯格式重构或无需设计判断的小修正。 | 可隐式路由，限强匹配。 |
| `architecture-review` | 用户明确指定热点、模块或痛点并要求只读架构审查时。 | 自动全库扫描、直接实施、没有范围的泛化重构建议。 | 显式调用。 |
| `implementation-orchestration` | 已确认 spec/tickets 需要组织为小批次实施与验证时。 | 需求、权限、数据或架构决定尚未确认时；自动 tracker/Git 工作流。 | 显式调用。 |

### 路由规则

1. 用户明确点名某个 skill 时，优先使用该 skill，并遵守用户为当前任务给出的更具体边界。
2. 未点名时，只根据 `description` 与任务事实选择可隐式路由的 skill。不要因为关键词相似而一次加载全部 skill。
3. `product-discovery`、`specification` 与 `vertical-ticketing` 是连续但独立的产品阶段；`project-profile` 与 `memory-governance` 管理长期项目上下文。它们及 `architecture-review`、`implementation-orchestration` 都是 user-invoked orchestrator/review skill，不能被 model 自动注入，也不能组成每个任务都执行的固定流水线。
4. `technical-research`、`domain-modeling` 与 `codebase-design` 是 model-invoked discipline：只有任务事实与 description 强匹配时才可加载；它们提供证据、语言或设计判断，不夺取流程控制权，也不把辅助记录变成默认产物。
5. 可以组合互补 skill，例如 `systematic-debugging` 确认根因后，在已授权修复任务中使用 `tdd` 建立回归测试；`implementation-orchestration` 只在已确认的 spec/tickets 上按 seam 组织这些调用。组合时仍保持每个 skill 的停止条件和授权边界。
6. Skill 只提供方法，不授予权限。调用任何 skill 都不自动授权网络范围扩张、安装依赖、真实外部写入、写仓库文件、commit、push、merge、发布、部署或危险操作。

## Canonical Skill 与三平台适配

### 单一事实源

规范化源位于 `skills/<name>/`。每个目录的 `SKILL.md` 保存跨平台正文，`agents/openai.yaml` 保存 Codex 专属界面元数据。只修改规范化源，不直接维护初始化器生成的 `.claude/skills/` 或 `.dsh/skills/` 副本。

显式编排型 skill 在规范化 `SKILL.md` 中使用嵌套标记：

```yaml
metadata:
  invocation: "explicit-only"
```

该标记是本系统的生成输入，不是假定所有平台都原生理解的共同字段。平台适配规则如下。

| 平台 | 项目级发现位置 | 用户级发现位置 | 显式调用适配 |
| --- | --- | --- | --- |
| Codex | `.agents/skills/<name>/` | `~/.agents/skills/<name>/` | Codex 不依赖本项目的 `metadata.invocation` marker；对应 `agents/openai.yaml` 设置 `policy.allow_implicit_invocation: false`。 |
| Claude Code | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` | 生成器只对显式编排型 skill 的副本增加顶层 `disable-model-invocation: true`；其他 skill 不增加该字段。 |
| DeepSeek Harness | 共同正文位于 `.agents/skills/<name>/`；显式编排型适配副本位于 `.dsh/skills/<name>/` | 共同正文位于 `~/.agents/skills/<name>/`；显式编排型适配副本位于 `~/.dsh/skills/<name>/` | `.dsh/skills/` 中的高优先级同名副本增加顶层 `disable-model-invocation: true`。只为显式编排型 skill 生成该副本。 |

生成器不会把 Codex 的 `agents/openai.yaml` 复制到 Claude Code 或 DeepSeek Harness 的平台副本。除 `agents/openai.yaml` 外，规范化 skill 可携带由 `SKILL.md` 明确链接的 supporting resources（如 `references/`、`scripts/`、`assets/`）；生成时保留这些相对路径和内容，不为其推断或执行额外权限。禁止在生成副本中手工添加未受管资源。Codex 字段见 [OpenAI Build skills](https://developers.openai.com/codex/skills/)，Claude 调用字段见 [Anthropic Skills](https://code.claude.com/docs/en/skills)。DeepSeek Harness 省略 `disable-model-invocation` 或 `user-invocable` 时，默认允许对应调用面；`.dsh/skills/` 的高优先级副本因此是 explicit-only 安全控制，不只是格式转换。该语义与单层发现约束见 [DeepSeek Harness 固定审计 commit](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/skill/skill-filesystem/README.md)。

用户安装的 `--target` 选择平台入口，不隔离 Codex 与 Harness 共用的 `.agents/skills/`。只要 target 包含 `codex` 或 `deepseek-harness`，安装器就同步 canonical skills 与七个 DSH explicit-only overlay；Codex-only dry-run 因此也会显示 `.dsh/skills/` 路径。同机使用多个目标平台时，建议使用 `--target all`，统一审查入口和副本版本。该行为以默认 spine 已启用 skill registry、tool consumer 与 skill filesystem plugins 为前提。

### 生成与漂移控制

1. 在 `skills/<name>/` 修改规范化正文、引用或 Codex 元数据。
2. 运行结构校验，确认名称、frontmatter、引用、JSON、TOML 与危险默认值检查通过：

   ```bash
   python3 tools/agent_system.py validate .
   ```

3. 运行初始化器单元测试。测试覆盖三平台目标路径、显式调用字段转换和 DeepSeek Harness 仅生成显式适配副本的行为：

   ```bash
   python3 -m unittest discover -s tools/tests -v
   ```

4. 在新的空目录中执行 dry-run，再执行隔离生成。不要在生成目录中手工修补平台副本；需要修正时回到规范化源或生成器。
5. 任何平台字段变化都必须先核对该平台当前官方文档，再更新适配器和测试。DeepSeek Harness 仍处于开发者预览阶段，不能把当前字段当作长期稳定接口。

## 第三方来源：固定版本、选择性重写

本系统只吸收高价值方法，不按 star 数量整包安装。第三方输入固定在 [`sources/third-party-skills.lock.json`](../sources/third-party-skills.lock.json)：

| 来源 | 固定 commit | 用途 | 处理方式 |
| --- | --- | --- | --- |
| [`mattpocock/skills`](https://github.com/mattpocock/skills) | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | 上游方法来源。 | 逐项审查后独立重写。 |
| [`vinvcn/mattpocock-skills-zh-CN`](https://github.com/vinvcn/mattpocock-skills-zh-CN) | `9fb0161ac2be0c45c59cbea0878eb77d92cc24b5` | 中文表达与本地化对照。 | 作为参考，不作为权威上游替代。 |

15 个 Skill 的方法映射如下：

| 本系统 Skill | 参考方法 |
| --- | --- |
| `product-discovery` | `grilling`、`grill-with-docs` 的依赖感知访谈。 |
| `specification` | `to-spec` 的需求、决定、测试和非目标结构。 |
| `vertical-ticketing` | `to-tickets` 的垂直切片与阻塞边。 |
| `tdd` | `tdd` 的 red-green 反馈纪律。 |
| `systematic-debugging` | `diagnosing-bugs` 的可复现信号与证据优先诊断。 |
| `two-axis-code-review` | `code-review` 的 Standards 与 Spec 双轴审查。 |
| `writing-for-agents` | `writing-for-agents` 的上下文预算与渐进披露。 |
| `safe-prototyping` | `prototype` 的问题驱动、一次性实验。 |
| `project-profile` | 本地 tips 与外链中关于项目隐性知识、权威入口、联动关系、受保护区域和精确 DoD 的方法，经官方平台机制复核后独立重写。 |
| `memory-governance` | 本地 tips 与外链中关于候选来源、作用域、冲突、过期、隐私和人工晋升的治理方法，经证据分级后独立重写。 |
| `technical-research` | `research` 的一手证据追溯，改为默认回答内汇报且不自动委派或写文件。 |
| `domain-modeling` | `domain-modeling` 的共享语言、情景检验和 ADR 三条件，改为按授权范围记录。 |
| `codebase-design` | `codebase-design` 的 deep module、interface、seam、adapter、leverage 与 locality 词汇。 |
| `architecture-review` | `improve-codebase-architecture` 的热点优先与候选强度，改为用户指定范围的只读报告。 |
| `implementation-orchestration` | `implement` 的小批次实施编排，移除自动 commit、tracker 写入和无确认执行。 |

`writing-for-agents` 同时支持 Create 与 Audit。Audit 以「是否改变 Agent 决策、是否属于正确层级、是否有足够证据」三个准入问题，把候选规则判为 retain、rewrite、move、delete 或 needs-evidence；这项能力没有被拆成第 11 个重复 Skill。

重写时移除了不适合共同基础配置的行为，包括自动 commit、外部 issue 写入、隐式依赖安装、凭据配置、真实 Git 状态变更，以及把特定工具生态当作普遍前提。`setup-matt-pocock-skills`、`triage`、`wizard`、`setup-pre-commit` 与 `git-guardrails-claude-code` 等候选未进入首批能力层。

### 许可证要求

两个固定来源 commit 中的 `LICENSE` 均为 MIT，并记录了 Copyright (c) 2026 Matt Pocock。本轮交付是独立撰写的规则和方法重组，没有逐字采用完整第三方 skill；处理说明见 [`sources/NOTICE.md`](../sources/NOTICE.md)。

未来若复制第三方代码或大量原文，必须在复制物附近保留适用的 MIT 版权与许可声明，并更新 lock 与 NOTICE。仅有链接或灵感来源不免除来源记录，也不应把中文仓库的 commit 误当作上游最新状态。

### 禁止整包安装

- 不执行第三方仓库提供的安装脚本或自动更新器。
- 不把整个第三方 `skills/` 目录复制进用户级或项目级目录。
- 不根据 star 数、README 宣传或译文完整度直接晋升能力。
- 不在未审查的 skill 中继承 hook、MCP、Git、issue tracker、网络或凭据行为。
- 上游更新先形成新的固定 commit 与差异审查，再逐项决定 `adapt` 或 `exclude`；不得让浮动分支直接进入生产配置。

## Skill 的评审、晋升与回滚

### 状态

每项新增或重大修改依次经过以下状态；“进入规范化源并可分发”与“行为收益已验证”是两个不同门：

1. **Candidate**：记录问题、证据、来源、适用范围和提议行为。候选尚未影响 Agent。
2. **Reviewed**：人工确认路由边界、安全边界、许可证、平台可移植性和与现有规则的冲突。
3. **Static baseline**：人工批准后写入规范化源，可随初始化器分发；来源、结构、调用边界、生成器与安全回归已通过，但不宣称行为质量提升。
4. **Behavior trial**：在隔离目录和代表性任务上运行；保存原始输出、diff、测试证据与评分，不连接生产系统。
5. **Behavior-validated**：代表性 fixture、对照运行与人工评审通过后，才可声明对应范围内的行为证据。
6. **Deprecated / Rolled back**：触发失准、质量回退、平台不兼容或安全风险时，停止推荐并恢复上一个已批准版本。

自动化可以收集证据、运行结构校验和计算评测分数，但不能代替人工的 static-baseline 或 behavior-validated 决定。当前 15 个 Skills 都是 `static-baseline`，没有一个完成真实 Agent 代表性评测；11 个 `contract-only` 任务不构成 behavior validation。

### Static baseline 与行为晋升门槛

进入 static baseline 前逐项确认：

- 目标行为和非目标行为均可描述，`description` 不会吸引大量相邻任务。
- 方法提供模型本身不明显的决策价值，不只是重复「写好代码」「充分测试」等空泛要求。
- 完成条件可观察，失败时有停止条件，不鼓励无期限重试。
- 不包含隐藏授权、真实凭据、生产写入、自动提交或平台权限绕过。
- 规范化正文可供 Codex 与 DSH 直接目标复用，并保留 Claude 兼容适配；确需平台差异时由生成器处理，而不是把互斥字段塞进同一 frontmatter。
- 第三方来源、固定版本、许可证与重写决定已经记录。
- 结构校验和单元测试通过；未运行真实模型时保持 `static-baseline`，不把评测 contract 或静态检查当成行为证明。
- 人工评审者批准触发范围、正文、来源和安全边界。

从 static baseline 晋升为 behavior-validated 还必须满足：至少一个相关 ready fixture 的真实 Agent 对照评测通过；运行记录绑定模型、客户端、权限、配置 digest 与原始 evidence；关键安全项无回退；人工评审者批准结论适用范围。缺任一项都保持 static baseline。

评测使用 [`evals/`](../evals/README.md) 中的共同任务与 rubric。一次只改变一个变量；质量分与耗时、token、返工次数分开看。单次高分不能证明普遍有效，持续低误触发和可复现的质量改善才支持保留。

### 回滚

出现以下任一情况时进入回滚评审：误触发造成范围膨胀；遗漏关键安全或授权边界；平台升级后无法发现或解析；代表性任务质量下降；正文与共同规则冲突；来源或许可证记录不完整。

回滚步骤：

1. 停止分发有问题的 static baseline 或撤销 behavior-validated 标记，不继续修改生成副本。
2. 保存失败任务、触发条件、平台版本、diff 和验证输出；删除其中的 secrets 与 PII。
3. 从仓库版本历史或项目保存的「上一已批准版本」恢复规范化源。若采用环境没有可恢复历史，先建立备份机制，再执行覆盖。
4. 重新生成两个直接目标与兼容 adapter 的副本，并运行结构校验、单元测试和导致回滚的代表性任务。
5. 将失败原因记录为新的 Candidate。只有经过新一轮人工评审后才能再次晋升。

本系统不提供自动回滚守护进程，也不假定任何特定 Git 分支策略。采用团队必须使用可恢复的版本历史或审查快照保存每个 static baseline 与 behavior-validated 版本。

## 候选到正式规则的记忆治理

Agent 在任务中学到的经验默认不是长期记忆。成功一次、用户随口偏好、单个报错、对话摘要或模型推断都不能直接写入用户级或项目级规则。

### Candidate 记录

`.agents/memory/candidates.jsonl` 默认是空文件。每行必须是一个 JSON object，且只含以下八个非空字符串字段；`status` 固定为 `candidate`：

- `id`：项目内唯一、可追踪的候选标识。
- `observation`：观察到的可复现现象，不写成已证明的普遍规律。
- `evidence`：任务、测试、日志或用户纠正；只保存必要且已脱敏的内容。
- `scope`：用户级、项目级、目录级、技术栈或单一 workflow。
- `destination`：常驻规则、skill、stack module、hook、MCP 配置、测试或不晋升。
- `conflicts_and_risks`：与现有规则、权限、兼容性和上下文预算的冲突。
- `expiry_signal`：版本升级、架构迁移或其他需要复审的条件。
- `status`：固定为 `candidate`。

校验器拒绝重复 ID、缺失或多余字段、非字符串、空白值和其他 status。`memory-governance` 只提出拒绝、补证据、隔离试验或请求人工批准四类建议；它不会自动写正式规则、删除候选或晋升 Memory，也不采集原始聊天记录。

### 人工审核

审核者依次判断：证据是否可复现；是否只是一次性环境问题；适用范围是否足够窄；现有规则或测试是否已覆盖；自然语言是否真是正确控制面；是否含 secrets、PII 或第三方受限内容；是否需要过期条件。

审核结果只有四种：拒绝、请求更多证据、进入隔离试验、批准晋升。没有人工决定时，候选保持非激活状态。

### 正式晋升

- 跨项目且几乎每个任务都适用的稳定行为进入用户级短常驻内核；门槛最高。
- 本仓库长期稳定的事实、命令入口与安全边界进入项目画像或就近规则；项目 core 只保留路由，不堆叠这些事实。
- 多步骤、按任务触发的方法进入 skill。
- 仅特定框架、语言或路径需要的约束进入 stack module 或 path-scoped rule。
- 必须确定性执行或阻止的本地事件进入 hook、permissions 或 CI，而不是只写自然语言。
- 需要实时外部数据或服务工具时才考虑 MCP，并单独完成权限与凭据评审。
- 能由测试或静态检查可靠表达的规则优先进入测试或 CI，不再重复成长篇提示词。

晋升后更新相关规范化源、生成器测试、来源记录与评测基线。不要把同一规则复制到多个常驻文件；平台差异由适配器承载。

## 能力应放在哪里

| 载体 | 选择条件 | 典型内容 | 不应承担 |
| --- | --- | --- | --- |
| 常驻规则 | 几乎每项任务都必须知道，内容稳定、短小，且依赖当前作用域。 | 授权边界、凭据保护、最小改动、完成证据、项目真实命令入口。 | 多步骤教程、框架百科、实时数据、仅偶尔触发的方法。 |
| Skill | 一个任务类型需要可复用的多步骤方法，并能由清晰 description 路由。 | 需求发现、TDD、系统调试、双轴审查。 | 无条件安全强制、单一项目事实、永远常驻的短规则。 |
| Stack module / path-scoped rule | 只在特定语言、框架、数据库或路径生效。 | Next.js、FastAPI、PostgreSQL migration、前端视觉质量检查。 | 跨项目共同行为；与仓库实际版本或命令冲突的通用配方。 |
| Hook / permissions / CI | 事件和判断可以确定性表达，必须在模型之外执行或阻止。 | 格式化检查、禁止命令、变更后校验、提交前质量门。 | 需要产品判断的开放任务；把 hook 当作完整安全沙箱。 |
| MCP | 任务确实需要实时外部能力、结构化数据或远程工具。 | 查询文档、设计系统、issue tracker 或观测平台。 | 静态知识、可由本地 CLI 完成的工作、默认开启的广泛写权限。 |

### 判定顺序

1. 先问「能否用测试、类型系统、lint、permissions 或 CI 确定性表达？」能则优先使用确定性控制。
2. 再问「是否几乎每个任务都必须知道？」是则写短常驻规则。
3. 再问「是否只与某类任务有关，并且包含多步骤判断？」是则写 skill。
4. 再问「是否只与某个技术栈或路径有关？」是则写 stack module 或 path-scoped rule。
5. 最后问「是否必须连接实时外部系统？」只有答案为是时才引入 MCP。

Hook 不能自动证明命令安全，MCP 也不能因为工具描述存在就获得外部写权限。MCP 默认关闭，采用白名单和最小权限；凭据只从受控环境注入，不进入 skill、常驻规则、仓库示例或评测产物。

## 维护检查清单

- 修改发生在 `skills/` 规范化源，而不是生成副本。
- 路由 description 同时写清适用与不适用范围。
- 显式编排标记在三平台生成结果中保持等价语义。
- 所有相对引用存在，目录保持单层 skill 发现结构。
- 没有新增真实凭据、自动外部写入、隐式 Git 动作或依赖安装。
- 第三方更新使用固定 commit，lock、NOTICE 与重写决定同步更新。
- Candidate 未经人工审核不会进入正式规则。
- 结构校验、单元测试和相关评测证据已记录；未运行项明确标注。
- 每项 Promoted 变更都有可恢复的上一版本和明确回滚触发条件。
