# VibeCoding Config

面向 AI 全栈开发的可维护配置、研究与工作流资料库。仓库将 Coding Agent 的用户级/项目级指令、Skills 治理、项目初始化与验证工具，与从需求调研到上线复盘的 Prompt Chain 放在同一套可追溯的文档体系中。

直接配置目标是 **Codex** 与 **DSH Desktop / DeepSeek Harness**。仓库保留 Claude Code 兼容资料；Cursor 仅作为规则设计经验来源，不作为直接交付平台。

> 本仓库交付的是经过来源追踪的配置、模板、流程和静态验证契约。它不自动安装 Skill、读取凭据、连接生产环境，也不把文档存在或本地校验通过表述为真实平台行为保证。

## 仓库定位

这里包含两条互补主线：

1. **Coding Agent 配置系统**：将用户级短常驻规则、项目级上下文路由、Skills、模板、生成器、验证与评测契约组织成可直接配置的基础设施。
2. **AI 产品全生命周期 Prompt Chain**：将产品调研、规格、原型、架构、实现、质量、发布、观测、实验和复盘连接为 M00–M13 的可恢复产物链。

两条主线共享证据分层、最小授权、显式验收、独立验证、消融检查与可追溯来源等工程原则，但分别保留各自的文档入口与使用方式。

## 内容地图

| 内容 | 入口 | 适合何时使用 |
|---|---|---|
| Coding Agent 配置系统 | [Constraint/coding-agent-system/README.md](Constraint/coding-agent-system/README.md) | 配置 Codex 或 DSH Desktop / DeepSeek Harness，初始化项目，治理 Skills，运行结构校验与评测。 |
| AI 产品全生命周期 Prompt Chain | [全栈开发Prompt Chain/README.md](全栈开发Prompt%20Chain/README.md) | 按 M00–M13、A00–A13、G0–G6 组织需求、实现、验证、发布和复盘。 |
| 既有原始经验与对照材料 | [Constraint/](Constraint/) | 查阅 Codex/Claude/Cursor 历史材料、规则原子化决策和研究链接。 |
| 本次仓库治理规格 | [设计规格](docs/superpowers/specs/2026-09-06-repository-initialization-design.md) / [实施计划](docs/superpowers/plans/2026-09-06-repository-initialization.md) | 了解首次初始化、目录边界、忽略规则、验证和推送约束。 |

## 从哪里开始

### 我想直接配置 Coding Agent

从 [Coding Agent 配置系统 README](Constraint/coding-agent-system/README.md) 开始。它提供：

- Codex 用户级与项目级 AGENTS.md；
- DSH Desktop / DeepSeek Harness 用户级与项目级 AGENTS.md；
- Claude Code 的兼容性 adapter；
- 共享模板、技术栈模块、Skills、初始化器与验证工具；
- 安装、隔离验证、项目生命周期 SOP、模型配置与 Skills 治理说明。

若要在空目录中建立项目，依次阅读：

1. [安装与隔离验证](Constraint/coding-agent-system/docs/installation.md)
2. [项目生命周期 SOP](Constraint/coding-agent-system/docs/sop/project-lifecycle.md)
3. [工作流与可移植行为契约](Constraint/coding-agent-system/docs/workflow.md)

### 我想按全生命周期开发 AI 产品

从 [Prompt Chain 使用手册](全栈开发Prompt%20Chain/06-Prompt-Chain使用手册.md) 选择适合当前任务的场景链；也可以直接复制 [prompts/](全栈开发Prompt%20Chain/prompts/) 下对应阶段的 Prompt。

完整链从 [99-端到端 Prompt Chain](全栈开发Prompt%20Chain/prompts/99-端到端Prompt-Chain.md) 开始。控制器会基于现有 A00–A13 选择最小必要模块，而不会在 Gate 或对象级授权前自动跨阶段执行。

对 AI-Native 控制面、责任分级、独立验证、能力资产、认知债与回退语义，阅读 [控制面规范](全栈开发Prompt%20Chain/08-AI-Native-SDLC控制面规范.md)。

### 我想审查研究依据或已有取舍

- [深度研究报告](Constraint/coding-agent-system/docs/research/deep-research-report.md)
- [本地 Tips 深度萃取审计](Constraint/coding-agent-system/docs/research/local-material-audit.md)
- [Tips 原子决策矩阵](Constraint/coding-agent-system/docs/research/tip-decision-matrix.md)
- [Claim-to-Source Ledger](Constraint/coding-agent-system/docs/research/source-ledger.md)
- [Prompt Chain 来源账本](全栈开发Prompt%20Chain/report-source.md)

这些账本区分事实、设计判断和未验证项。来源中的作者经验、高 stars、静态结构或单次工具输出，不应被升级为跨平台效果结论。

## 直接支持的平台与边界

| 平台 | 状态 | 使用边界 |
|---|---|---|
| Codex | 直接支持 | 使用用户级与项目级 AGENTS.md、项目模板与适配后的 Skills；真实平台发现与 sandbox 行为仍需按本机版本 smoke。 |
| DSH Desktop / DeepSeek Harness | 直接支持 | 使用 Harness 对应的 AGENTS.md、Skills adapter 和项目模板；Harness 的发布版本与固定研究 commit 需单独核验。 |
| Claude Code | 兼容资料 | 保留 adapter、模板和对照文档，但不是本仓库当前的新增直接配置目标。 |
| Cursor | 经验来源 | 只吸收规则分层、作用域、最小改动和验证纪律；不生成或维护 Cursor 运行时规则。 |

自然语言指令、Prompt 和 Skill 不是权限边界。涉及外部系统、付费模型、依赖安装、Git 写入、发布、生产读写或敏感数据时，必须经过当前平台、项目和人工授权流程。

## 验证与安全边界

Constraint/coding-agent-system 提供可在本地运行的渲染、结构校验与单元测试。可从该目录执行：

~~~bash
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py validate .
python3 -m unittest discover -s tools/tests -v
~~~

这些检查能证明模板、生成器和本地契约的结构行为；不能证明目标 Agent 已加载配置，也不能证明未测试的平台、模型、仓库或生产环境上的质量。

默认安全模式包括：

- 不读取或提交 .env、token、密码、私钥、cookie、session transcript、PII 或生产日志；
- 不自动安装第三方 Skills、Plugin、MCP、SDK 或依赖；
- 不自动 commit、push、merge、发布、部署、发送消息、创建 Issue/PR 或写生产数据；
- 不把 PLAN、Gate、Prompt、Skill、Hook 或 MCP 当成真实外部动作授权；
- 高风险或 R3 动作需要对象级、当次、未过期的人工授权及可复核 receipt。

## 仓库结构

~~~text
.
├── Constraint/
│   ├── coding-agent-system/       # 模板、Skills、工具、评测、研究与来源账本
│   ├── cursor_rules/              # 仅作经验与规则设计来源
│   └── ref_links.txt              # 外部研究链接输入
├── 全栈开发Prompt Chain/
│   ├── prompts/                   # 面向 Agent 的模块 Prompt
│   ├── prompts_ask/               # 面向人机对话的 Prompt 版本
│   └── 00–08 研究、工作流与控制面文档
├── archive/
│   └── 全栈开发Prompt Chain.zip    # 版本化便携快照；Markdown 正文仍是权威版本
└── docs/superpowers/
    ├── specs/                     # 已确认的仓库治理设计
    └── plans/                     # 可复核的实施计划
~~~

为保护现有引用，Constraint/ 与 全栈开发Prompt Chain/ 保持原路径。请不要只为美化目录而批量改名或移动其中的文件；先搜索现有引用、来源账本、模板与测试，再决定是否做受控迁移。

## 版本管理与贡献约定

- 使用 Git 历史记录可追溯变更；本仓库首次快照采用 main 分支。
- 对模板、平台适配、Skills、研究结论或 Prompt Chain 的非琐碎修改，应同时更新受影响的来源账本、验证证据和相应导航入口。
- 先以最小范围修改并完成可执行校验；不要通过删除、跳过或弱化测试来制造“通过”。
- 不提交系统垃圾、缓存、构建产物、日志或本地敏感配置；根 .gitignore 已覆盖常见路径。
- 需要真实外部副作用时，先清楚记录目标、授权范围、预期效果、回滚与验证；用户授权一个 Gate 不等于授权后续全部动作。

当前仓库没有声明统一的再分发许可证。使用或再分发第三方来源、Skills 或资料前，请核对各自的固定来源、LICENSE/NOTICE 与 [来源账本](Constraint/coding-agent-system/report-source.md)。

## 归档快照

[全栈开发Prompt Chain.zip](archive/%E5%85%A8%E6%A0%88%E5%BC%80%E5%8F%91Prompt%20Chain.zip) 是本次初始化时保留并版本化的便携快照。它方便离线分发与对照；日常维护、审阅和引用以仓库中的 Markdown 正文为准。
