---
title: 多 Coding Agent 开发系统设计
doc_type: design
module: coding-agent-system
topic: architecture
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# 多 Coding Agent 开发系统设计

## 目标

构建一套可直接审查、安装和演进的 Coding Agent 基础配置。本轮直接配置交付聚焦 Codex 与 DSH Desktop / 官方 DeepSeek Harness；仓库保留既有 Claude Code adapter 作为兼容层。系统同时提供用户级配置、项目级配置、产品研发 skills、项目初始化流程、模型路由、MCP 与 hooks 策略，以及可重复的质量评测方法。

本成果不覆盖 `Constraint/` 中的原始资料，也不修改真实的 `~/.codex/`、`~/.claude/` 或 `~/.dsh/`。

## 已确认的设计决策

1. Cursor 不属于正式目标平台，仅作为规则拆分和路径作用域的经验来源。
2. DeepSeek Harness 仅以官方 `@deepseek-ai/dsh` 为正式基线。
3. Agent 对实现类任务采用风险分级自治：可自主搜索、编辑和验证；破坏性操作、外部副作用、重大架构选择和权限扩大需要确认。
4. 默认不执行 commit、push、merge、发布或部署。
5. 用户级配置针对 macOS；项目级配置保持团队可提交和跨 macOS、Linux、Windows 使用。
6. 用户级短常驻内核与项目级隐性知识路由器分别维护一份规范化源文件，再生成三平台适配文件并检测漂移；项目 core 不复制用户级通用行为。
7. 用户级规则保持技术栈无关；项目级 core 只路由存在且相关的项目画像、局部规则、Memory、controls 与受管模块；项目初始化为每个选中模块生成可达的路径和触发条件。
8. 模型采用任务分层路由，文档提供质量、均衡和经济三类 profile 设计；当前安装器不生成或安装这些 profile。
9. 长期经验先进入 `.agents/memory/candidates.jsonl`，经人工审核后才能晋升为正式规则；工具不自动晋升、删除或改写正式规则。
10. MCP 默认关闭并采用白名单；凭据不进入仓库、提示词或示例配置。
11. “系统提示词”以可移植的行为契约和任务编排提示词交付，不替换 Codex 内置 base instructions。
12. 第三方 skills 不整包安装。固定来源版本、保留许可证和署名，经过重写后再纳入。

## 分层架构

```text
用户意图与验收标准
        |
        v
共享行为契约 ────────────────┐
        |                    |
        v                    v
平台适配器              按需能力层
Codex / Claude / DSH     skills / stack modules
        |                    |
        └─────────┬──────────┘
                  v
       permissions / sandbox / hooks / CI
                  |
                  v
          测试、运行验证与审查证据
```

用户级短常驻内核只保存所有任务都需要的稳定规则，例如请求授权、证据要求、工作区安全、范围控制和目标驱动验证。项目级 core 是隐性知识路由器：它把 Agent 引向项目画像、局部规则、Memory 候选和确定性 controls，不再重复通用宪法。多步骤方法进入 Skill；框架约定进入技术栈模块；确定性限制进入 hook、permissions、script 或 CI；实时外部能力进入 MCP。

## 配置生成模型

### 用户级

`templates/shared/user-core.md` 是短常驻 canonical 内核。它只承载请求授权、Karpathy 四项决策内核、证据与安全边界，以及能力与记忆路由。`render-templates` 将该内核与平台差异确定性组合为受版本控制的平台快照：

- Codex：`~/.codex/AGENTS.md` 和 `config.toml` 参考配置。
- Claude Code：`~/.claude/CLAUDE.md` 和 `settings.json` 参考配置。
- DeepSeek Harness：`~/.dsh/AGENTS.md` 和版本化配置说明。

`install-user` 安装已渲染快照，而不是在目标 home 中临时拼接正文。默认模式只输出目标清单；`--apply` 前会运行完整结构校验，缺件或漂移时 fail closed。允许覆盖的目标已存在时必须提供独立备份目录；已有且不同的 `.codex/config.toml` 或 `.claude/settings.json` 不走覆盖路径，即使有备份也要求人工合并，相同内容则 no-op。`--target` 选择平台入口，不表示 Skill 根隔离：目标包含 Codex 或 DeepSeek Harness 时，共享 `.agents/skills/` 与七个 DSH explicit-only overlay 始终同步；同机多平台建议使用 `--target all`。

安装器不会打印既有配置内容；受保护平台设置只做字节比较，允许覆盖的其他目标在备份时会被原样复制。既有目标若含凭据或 PII，备份也会包含这些信息，因此备份目录必须采用与原文件相同或更严格的访问保护，不得进入同步目录或版本库。生成画像、Memory 动态字段和项目自定义 Skill 还会接受 secret-like 内容与敏感路径扫描，错误只暴露字段或路径。用户安装逐文件原子替换；多个文件组成的整次安装不是原子操作或全局事务。中途失败时安装器会尝试补偿回滚已写入项，但回滚失败仍需依据错误、备份和目标状态人工恢复。

### 项目级

项目根 `AGENTS.md` 是规范化入口。Claude Code 使用 `.claude/CLAUDE.md`，其首个逻辑行以 `@../AGENTS.md` 导入共同契约。项目根不再放置 `CLAUDE.md`，避免 DeepSeek Harness 的初始根候选同时包含共同入口与 Claude 专属入口。这不是绝对隔离：默认 `agent-instructions` plugin 在 Harness 成功访问 `.claude/` 后仍可能动态发现该文件，且不解释 Claude 的 `@` import。Codex 的项目 `.codex/config.toml` 保持为注释型入口，不设置 `approval_policy`、`sandbox_mode` 或模型；行为规则放在 `AGENTS.md`，强制安全基线放在用户或组织层。

`templates/project/codex/AGENTS.md` 与 `templates/project/deepseek-harness/AGENTS.md` 是两份可直接复制的单平台发行快照。它们共享同一个 `templates/shared/project-core.md`，只在共享块外保留发现、预算、skill 与版本边界。两者部署时都必须复制为目标项目根 `AGENTS.md`，因此互斥，不能在同一项目中作为两个真实入口并存；同一项目同时使用 Codex 与 DSH Desktop 时采用平台中立的 `templates/project/AGENTS.md`。

`templates/shared/project-core.md` 不是第二份通用行为契约，而是项目画像路由器。初始化器生成以下项目治理层：

- `.agents/project-profile.md`：默认 `profile_status: draft`。普通校验允许 draft，且项目 core 只阻塞当前任务相关的实质缺口；`active` 状态触发结构校验，七个规定 H2 必须唯一且无未知 H2，每域使用带受控 `Source` 的结构化 `Fact`、`Decision` 或说明边界的 `Not applicable`。`--require-ready-profile` 还会要求状态必须是 `active`。
- `.agents/memory/candidates.jsonl`：默认空文件，每行只能是满足固定八字段契约的候选；人工审核前不得晋升。
- `.agents/controls/change-policy.example.json`：仅供审查。实际策略的唯一可选路径是 `.agents/controls/change-policy.json`；初始化器不创建该文件，controls 也不会自动接入 hook 或 CI。
- `.agents/rules/`：按初始化参数复制技术栈或文件治理模块；生成器同时在根 `AGENTS.md` 的受管路由块列出路径与触发范围，避免“文件已生成但平台不可达”。

## Skills 架构

当前 15 个 Skills：

1. `product-discovery`
2. `specification`
3. `vertical-ticketing`
4. `tdd`
5. `systematic-debugging`
6. `two-axis-code-review`
7. `writing-for-agents`
8. `safe-prototyping`
9. `project-profile`
10. `memory-governance`
11. `technical-research`
12. `domain-modeling`
13. `codebase-design`
14. `architecture-review`
15. `implementation-orchestration`

其中 `product-discovery`、`specification`、`vertical-ticketing`、`project-profile`、`memory-governance`、`architecture-review` 与 `implementation-orchestration` 是 explicit-only；它们涉及产品决策、长期项目知识、长期架构或流程控制，不能根据相似关键词自动触发。`technical-research`、`domain-modeling` 与 `codebase-design` 只在任务与 description 强匹配时按需加载；`writing-for-agents` 同时提供 Create 与 Audit 模式，不另建重复的 instruction-audit Skill。

共同可移植部分只使用 `name`、`description`、Markdown 正文和相对引用。Codex 的 `agents/openai.yaml`、Claude Code 的调用字段以及 DeepSeek Harness 的发现限制由生成器或平台适配层处理。

每个 skill 必须满足以下条件：

- description 能区分适用与不适用任务。
- 正文只保留会改变 Agent 决策的非显然规则。
- 任何外部写入、提交或高风险动作均不从 skill 调用中推导授权。
- 支持材料按需加载；`references/`、`scripts/`、`assets/` 和 Codex `agents/openai.yaml` 作为完整 Skill 树受校验与复制，不复制官方手册。
- 进入 canonical 分发前必须通过结构校验与生成器回归；只有完成隔离代表性任务评测后，才可标记为 `behavior-validated`。

当前 15 个 Skills 均为可分发的 `static-baseline`：结构、来源、调用边界和生成路径已校验，但 11 个评测仍为 `contract-only`，所以没有任何 Skill 被标记为 `behavior-validated`。这一区分不阻止用户显式试用，但禁止把静态通过写成质量提升证据。

## 初始化器

初始化器使用 Python 标准库，避免新增项目依赖。它提供五类命令：

- `render-templates`：从 canonical shared core 渲染平台快照；默认列出完整目标映射且不写文件，`--apply` 才更新快照。漂移由 `validate` 判定。
- `init-project`：在空白目录中生成项目级配置、已选技术栈模块和 skills。
- `install-user`：预览或安装用户级配置，默认不写入。
- `validate`：检查模板渲染漂移、skill frontmatter、路径、占位符和危险默认值。
- `validate-generated`：按 project 或 user 形状校验实际生成树。项目 `.agents/generated-manifest.json` 绑定生成器拥有的 stack modules 与 managed Skills；用户树可按目标平台收窄。项目新增的合规 Skill 和 supporting resources 可以保留，但不能覆盖、伪装或绕过 managed artifacts 的内容与安全校验；项目自定义 Skill 不得使用只对 canonical registry 有完整平台适配的内部 `metadata.invocation: explicit-only`。项目校验默认允许 draft 画像；任何 active 画像都必须通过 canonical preamble、七域结构、来源和 secret-like 内容校验，`--require-ready-profile` 再把 active 状态作为正式启动门。

所有写入操作先计算目标清单。`init-project --apply` 与 `install-user --apply` 在写入前执行完整 `validate`；canonical core 与平台快照有漂移、缺件或安全检查失败时不写入。单文件先以 chunked stream 写入同目录中性临时名，按实际长度和 SHA-256 核验并 `fsync` 后移动；Darwin 使用系统 `/bin/mv`，避免当前工作区对最终 `.md` 名直接写入造成的延迟 native-size 偏差，其他平台使用 `os.replace`。项目初始化再以 staging tree 整体替换空目标；用户安装整批操作不是全局事务。

## 验证策略

验证分为四层：

1. 结构验证：目录、frontmatter、引用和机器可读配置可解析。
2. 单元测试：初始化器的 dry-run、空目录生成、覆盖保护和备份行为。
3. 静态语义检查：共享核心无重复，平台快照可重渲染且无漂移，平台差异不包含凭据或未解析占位符。
4. Agent 评测：Auto Research 评测协议/控制面定义 11 个任务契约、最小子进程环境、完整 artifact digest、receipt-v2 control snapshot、逐维 assessor evidence、运行记录和 `coding-agent-rubric-v3` / `score-v5`。Record 自报 score、unsafe action 或控制变量不会被当作观测事实；缺少 assessment 时质量分为空且禁止晋升。Unsafe action、低指令忠实度和低上下文治理会触发 hard gate。11 个任务当前都为 `contract-only`，07–11 也未运行真实 Codex 或 DSH Desktop；结构测试不能证明行为效果。

## 非目标

- 不创建 Cursor 专属配置。
- 不自动安装或更新第三方 skill 包。
- 不连接真实 MCP 服务，不写入凭据。
- 不自动安装快速变化的模型 profile、provider 或模型 ID；模型文档中的片段均为 opt-in 示例。
- 不运行付费模型基准。
- 不初始化 Git 仓库，不创建 commit。
- 不声称自然语言规则可以替代权限、安全边界或 CI。
