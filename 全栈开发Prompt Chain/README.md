# 全栈开发 Prompt Chain

这是一套面向 Codex、Claude Code 与 DeepSeek Harness 的 AI 产品全生命周期工作包。它不是一组“魔法提示词”，而是把 Skill 选择、事实证据、决策门、产物契约和验证要求连接成可恢复的工作流。

在既有 M00–M13、A00–A13、G0–G6 和 R3 之上，本工作包采用“AI-Native 控制面”增强：每个非琐碎 artifact 记录状态、人类责任、授权、权威输入、验证、未验证范围和回退路径。它不增加第二套状态机，也不把 Agent 的完成陈述当作生产放行。

研究对象是 [`vinvcn/mattpocock-skills-zh-CN`](https://github.com/vinvcn/mattpocock-skills-zh-CN/tree/9fe7e7a3bb352851b986725bab1c7cfb17610a97) 的固定版本；同时吸收本工作区 `Constraint/coding-agent-system` 已完成的 Tips 审计、平台机制研究和安全治理。Cursor 不作为目标平台，只吸收规则分层、路径作用域、最小改动和验证纪律。

## 先看结论

- 原仓库擅长 `grilling → domain-modeling → spec/tickets → implement/TDD → code-review`。
- 它不能独立覆盖真实用户研究、产品指标、AI Eval、安全、E2E、发布、可观测性、增长实验和 Skill 自进化。
- 仓库实际有 36 个 `SKILL.md`：29 个公开稳定 Skill、6 个 in-progress Skill、1 个内部翻译 Skill。
- 多个 Skill 会自动 commit、创建或关闭 Issue、修改标签、启动后台 Agent、写 `.env` 或操作外部系统。本文档将这些行为拆到独立审批门之后。
- 外部候选按单 Skill、固定版本、许可证和副作用评估；stars 只是发现信号，不是质量证明。

## 三种使用方式

### 1. 单模块复制

进入 [`prompts/`](prompts/)，选择当前阶段的 Prompt，填写顶部输入变量后粘贴给 Agent。适合已有项目、功能迭代、故障诊断或独立审查。

### 2. 场景链

根据 [`06-Prompt-Chain使用手册.md`](06-Prompt-Chain使用手册.md) 选择以下链之一：

- 新想法到 MVP。
- 既有产品新增功能。
- Bug 或生产事故。
- 上线后的反馈与增长迭代。

### 3. 完整链

从 [`prompts/99-端到端Prompt-Chain.md`](prompts/99-端到端Prompt-Chain.md) 开始。控制 Prompt 会逐阶段选择 M00–M13，但不会在审批门前自动跨阶段执行。

## 模块地图

| 模块 | Prompt | 标准产物 |
|---|---|---|
| M00 全局上下文与流程控制 | [`00`](prompts/00-全局上下文与流程控制.md) | `A00-context-pack.md` |
| M01 项目初始化与治理 | [`01`](prompts/01-项目初始化与治理.md) | `A01-project-charter.md` |
| M02 机会与市场调研 | [`02`](prompts/02-机会与市场调研.md) | `A02-opportunity-brief.md` |
| M03 用户研究与问题定义 | [`03`](prompts/03-用户研究与问题定义.md) | `A03-problem-evidence.md` |
| M04 产品策略与范围决策 | [`04`](prompts/04-产品策略与范围决策.md) | `A04-product-strategy.md` |
| M05 领域模型与产品规格 | [`05`](prompts/05-领域模型与产品规格.md) | `A05-product-spec.md` |
| M06 原型与 UX 验证 | [`06`](prompts/06-原型与UX验证.md) | `A06-prototype-evidence.md` |
| M07 架构设计与任务拆解 | [`07`](prompts/07-架构设计与任务拆解.md) | `A07-architecture-and-tickets.md` |
| M08 全栈实现与 TDD | [`08`](prompts/08-全栈实现与TDD.md) | `A08-implementation-report.md` |
| M09 AI Eval、质量与安全 | [`09`](prompts/09-AI-Eval与质量安全.md) | `A09-quality-evidence.md` |
| M10 发布与上线 | [`10`](prompts/10-发布与上线.md) | `A10-release-readiness.md` |
| M11 可观测性与反馈闭环 | [`11`](prompts/11-可观测性与反馈闭环.md) | `A11-production-learning.md` |
| M12 增长与实验 | [`12`](prompts/12-增长与实验.md) | `A12-experiment-decision.md` |
| M13 复盘与 Skill 自进化 | [`13`](prompts/13-复盘与Skill自进化.md) | `A13-retrospective.md` |

## 默认安全模式

所有 Prompt 默认使用：

```text
MODE=PLAN
EXTERNAL_EFFECTS=DENY
SECRETS_ACCESS=DENY
PRODUCTION_ACCESS=DENY
```

`MODE=APPLY` 只授权当前工作区内、范围明确、可逆的修改。它不自动授权依赖安装、commit、push、Issue/PR 写入、发送消息、付费调用、凭据读取、部署或生产写入。

## 文档导航

- [`00-研究方法与设计说明.md`](00-研究方法与设计说明.md)：范围、证据等级、模块和验收计划。
- [`01-目标仓库36个Skills逐项审计.md`](01-目标仓库36个Skills逐项审计.md)：每个 Skill 的功能、调用、输入输出和风险。
- [`02-Skills调用方法与关系图.md`](02-Skills调用方法与关系图.md)：依赖图、主链、on-ramp 和冲突。
- [`03-AI产品全生命周期映射.md`](03-AI产品全生命周期映射.md)：36 个 Skill 到 M00–M13 的完整分类。
- [`04-模块化Skills工作流.md`](04-模块化Skills工作流.md)：模块流程和四条场景链。
- [`05-GitHub候选与替代审计.md`](05-GitHub候选与替代审计.md)：高关注度与第一方候选的采用、替代和排除依据。
- [`06-Prompt-Chain使用手册.md`](06-Prompt-Chain使用手册.md)：变量、产物交接和恢复方法。
- [`07-平台适配与安全边界.md`](07-平台适配与安全边界.md)：Codex、Claude Code、DSH 调用差异和审批边界。
- [`08-AI-Native-SDLC控制面规范.md`](08-AI-Native-SDLC控制面规范.md)：跨模块 Control Contract、状态语义、独立验证、能力资产与回退规则。
- [`09-故事线驱动与编译式交付模式.md`](09-故事线驱动与编译式交付模式.md)：把故事假设、能力 spike、多目标交付与 claim 审证映射到既有控制面，并记录采用/拒绝边界。
- [`report-source.md`](report-source.md)：研究主张与来源账本。

## 证据边界

本交付完成的是固定版本静态审计、官方文档核验、方法整合和 Prompt 契约设计。它没有安装或真实运行候选 Skill，没有连接 tracker、MCP、生产环境或付费模型，也没有因此产生行为质量基准。任何“候选有效”均表示方法适配判断，不表示已在你的项目上实测优于现状。
