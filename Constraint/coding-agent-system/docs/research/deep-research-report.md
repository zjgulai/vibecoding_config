---
title: Codex 与 DSH Desktop 基础配置深度研究报告
doc_type: analysis
module: coding-agent-system
topic: platform-and-skill-research
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# Codex 与 DSH Desktop 基础配置深度研究报告

## 结论

**[事实｜高]** 本轮直接目标平台只有 Codex 与 DSH Desktop / DeepSeek Harness；Cursor 仅作为经验来源，既有 Claude Code adapter 只保留作兼容性回归。Codex 与 DSH 可以共享一份项目行为契约正文，但不能共享同一套发现、权限或 Skill 配置：Codex 读取 `AGENTS.md` 链；DeepSeek Harness 在默认 spine 启用 `agent-instructions` plugin 时，把多个候选文件按预算渲染。见 [OpenAI 官方文档](https://developers.openai.com/codex/guides/agents-md/) 与 [DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/context/agent-instructions/README.md)。

**[推断｜高]** 设计中的「共同规则一份、平台适配器分别生成」是当前最低维护成本的实现路径。共同层只保留跨平台稳定的行为要求；路径、文件名、配置键、权限和发现机制留给平台适配器。`render-templates` 可重放渲染平台快照，`validate` 检测漂移；项目或用户 apply 在校验失败时 fail closed。

**[事实｜高]** 本项目初始化器已在隔离临时目录完成生成 smoke test，包括 dry-run、备份、symlink 越界保护、模块路由和平台 Skill frontmatter 适配；该证据不涉及真实用户目录或付费模型调用。见 [CLM-020](source-ledger.md)。

**[不确定项｜中]** 本轮没有用 Codex 或 DeepSeek Harness 启动一个生成后的项目。因此，平台“会加载并按预期执行”的结论仍停留在官方机制与本地生成物两层，不能写成端到端实测。

## 官方机制对照

| 维度 | Codex | Claude Code | DeepSeek Harness |
| --- | --- | --- | --- |
| 项目指令入口 | `AGENTS.md`；同目录优先 `AGENTS.override.md`。 | `CLAUDE.md` 或 `.claude/CLAUDE.md`；`AGENTS.md` 不会自动读取。 | 默认 spine 启用 `agent-instructions` 时，候选为 `AGENTS.md`、`CLAUDE.md`；本地覆盖候选为 `AGENTS.local.md`、`CLAUDE.local.md`。 |
| 层级与优先级 | 从项目根到当前目录拼接；更近的文件位于后面。 | 从根到当前目录拼接；更近的文件位于后面，`CLAUDE.local.md` 在同目录后追加。 | 首请求包含用户全局文件后再放项目链；广到窄，重复内容会折叠。 |
| 共享正文的正确接法 | 项目根 `AGENTS.md` 作为共同入口。 | `.claude/CLAUDE.md` 使用 `@../AGENTS.md` 导入，之后追加 Claude 专属增量。 | 只保留根 `AGENTS.md`，避免初始根候选冲突；访问 `.claude/` 后仍可能动态发现 Claude 入口，且不解释其中的 `@` import。 |
| 文本预算 | `project_doc_max_bytes` 默认 32 KiB；达到上限停止添加。 | 保持简洁并移走非必要常驻内容；本轮未找到可支持“通用 200 行硬上限”的一方依据。 | `maxBytes` 是必填配置；默认 spine 示例使用 65,536 字节，优先保留最具体文件。 |
| 规则与 skill | canonical skill 放在 `.agents/skills`；Codex 专属 UI/调用策略放 `agents/openai.yaml`。 | `.claude/rules/` 可按路径生效；Claude Skill 副本放 `.claude/skills`，显式流程使用其调用字段。 | 可从项目 `.dsh/skills`、`.agents/skills`、用户目录等发现；名称为 kebab-case，高优先级副本只覆盖显式流程。 |

## 不能合并的部分

三平台只能共享“行为语义”，不能共享全部文件。下面这些差异若强行塞进一份 Markdown，会产生看似统一、实际失效的配置：

| 差异 | 为什么不能放进共同正文 | 本系统的处理 |
| --- | --- | --- |
| 发现入口 | Claude Code 不自动加载 `AGENTS.md`；默认 spine 启用 `agent-instructions` 时，DeepSeek Harness 同时把根 `AGENTS.md` 与根 `CLAUDE.md` 视为初始候选。 | 项目 `AGENTS.md` 为 canonical；Claude `.claude/CLAUDE.md` 只做 `@../AGENTS.md` 导入与增量说明，项目根不生成 `CLAUDE.md`。 |
| 权限与 sandbox | 每个平台的权限键、审批流程和强制能力不同。 | 共同正文只声明授权原则；确定性限制留在各平台 settings、sandbox、hook 或 CI。 |
| Skill 调用字段 | 三个平台的调用控制字段语义不同；Codex 当前解析器会忽略未知 Skill frontmatter，不能把「未报错」当作该字段生效。 | `metadata.invocation: explicit-only` 只作为本项目渲染器的内部 marker；Codex 使用 `agents/openai.yaml` 的 `policy.allow_implicit_invocation`。Claude 与 DSH 副本注入 `disable-model-invocation`；DSH 省略该字段时默认允许模型调用。 |
| 模型选择 | 模型名、alias、reasoning 参数和账户可用性持续变化。 | 行为契约不写模型；模型路由集中在 [模型配置](../model-configuration.md) 并要求 eval。 |
| MCP 生命周期 | MCP 可能连接不同传输、凭据和外部权限域。 | 默认关闭；逐 server、逐工具、逐环境启用，不把“已连接”等同于“获准写入”。 |

## 信息应该放在哪一层

**[推断｜高]** 规则效果不取决于文档越长，而取决于信息是否出现在正确层级。OpenAI 当前模型指导也建议减少重复指令和无关工具，并用代表性 eval 验证变化。[OpenAI 官方模型指导](https://developers.openai.com/api/docs/guides/latest-model)

| 信息类型 | 正确载体 | 反例 |
| --- | --- | --- |
| 所有任务都需要的授权、范围、证据规则 | 用户/项目共同契约 | 把完整 TDD 或数据库教程常驻注入。 |
| 只在特定任务使用的多步方法 | Skill | 在根 `AGENTS.md` 中强制每个响应走十阶段状态机。 |
| 框架、语言、数据库、视觉质量约定 | 按需 stack module 或近目录规则 | 用户级规则默认指定 Next.js、FastAPI 或 PostgreSQL。 |
| 必须确定执行的检查 | Hook、CI、permissions、sandbox | 只写“禁止”并假设模型绝不会违反。 |
| 实时外部数据和操作 | MCP 或专用工具 | 把会过期的外部状态复制进常驻提示词。 |
| 跨版本质量判断 | Eval 与运行记录 | 仅凭一次主观体验宣布某模型或配置最好。 |

## 自主执行与确认边界

本系统采用已确认的风险分级，而不是“每步都问”或“完全放权”。

| 请求/动作 | 默认行为 | 需要确认的转折点 |
| --- | --- | --- |
| 回答、解释、审查、诊断、规划 | 只读检查并报告，不自动实现。 | 用户随后要求修改，或诊断需要真实生产探针。 |
| 修改、构建、修复 | 自主搜索、在范围内编辑、运行非破坏性验证。 | 架构/数据/权限/UX 的重大未决选择。 |
| 本地测试、lint、typecheck、build | 项目已有命令可确认时直接运行。 | 会产生付费调用、真实发送或共享环境写入。 |
| 删除、迁移、覆盖关键配置 | 先说明影响、回滚与验证，再等待确认。 | 任何不可逆或广范围目标。 |
| commit、push、merge、发布、部署 | 默认不执行。 | 当前任务对具体动作给出明确授权。 |

这种边界减少了低风险任务中的无效停顿，同时保留了外部副作用与重大决策的人类控制点。它是行为策略，不是权限实现；平台强制控制仍要单独配置。

### Codex

**[事实｜高]** Codex 在每次运行开始时读取指令文件：全局层从 `CODEX_HOME`（默认 `~/.codex`）读取 `AGENTS.override.md` 或 `AGENTS.md`；项目层从项目根向当前工作目录逐层发现，每层最多取一个候选文件，近目录内容随后拼接并覆盖早期指导。[OpenAI 官方说明](https://developers.openai.com/codex/guides/agents-md/)

**[事实｜高]** Codex 会受 `project_doc_max_bytes` 限制，官方说明其默认值为 32 KiB。共同规则应短小且稳定；长步骤应放进按需 Skill 或模块，不能假设所有规则都会无限制注入。[OpenAI 官方说明](https://developers.openai.com/codex/guides/agents-md/)

### Claude Code

**[事实｜高]** Claude Code 的项目指令入口是 `CLAUDE.md` 或 `.claude/CLAUDE.md`，而不是自动读取 `AGENTS.md`；其 import 语法可以复用其他文件。本系统选择 `.claude/CLAUDE.md`，并以相对该文件的 `@../AGENTS.md` 导入共同正文，从而避免在项目根产生 DeepSeek Harness 默认 `agent-instructions` plugin 也会发现的初始候选。[Anthropic 官方说明](https://code.claude.com/docs/en/memory)

**[事实｜高]** `CLAUDE.md` 是行为上下文，不是强制执行机制；需要无条件阻止工具、命令或路径时，应使用受管设置、sandbox 或 hook 等平台机制。把禁止性要求仅写进自然语言规则不能构成可靠控制。[Anthropic 官方说明](https://code.claude.com/docs/en/memory)

**[事实｜高]** Claude Code 把规则和任务型知识区分开：无条件规则可在 `.claude/rules/` 中组织，按路径规则只在处理匹配文件时加载；任务特定内容适合 skill，减少常驻上下文。[Anthropic 官方说明](https://code.claude.com/docs/en/memory)

**[事实｜高]** `CLAUDE_CONFIG_DIR` 会替代默认 `~/.claude` 用户配置根；Claude Code 的 settings、session history 和 plugins 随该目录移动。Linux 与 Windows 的 credential storage 也随之移动，但 macOS 凭据仍保存在 System Keychain。因此在 macOS 上，不能仅凭配置目录不同就断言认证已在文件系统层隔离；多账户行为仍需按当前客户端单独验证。本系统安装器不读取该变量，使用自定义根时必须先隔离生成，再人工审查迁移。[Anthropic 环境变量说明](https://code.claude.com/docs/en/env-vars)

### DeepSeek Harness

**[事实｜高]** `dsh-agent-instructions` 在默认 `dsh-agent-spine-demo` bundle 中启用，也可以由 bundle config 禁用。启用时，它将用户全局 `$DSH_HOME/AGENTS.md` 与项目链放入模型上下文；默认项目候选是 `AGENTS.md`、`CLAUDE.md`，默认本地增量候选是 `AGENTS.local.md`、`CLAUDE.local.md`。相同内容会按目录去重。[DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/context/agent-instructions/README.md)

**[事实｜高]** 首次请求只包含项目根到当前 cwd 的候选链；成功的第一方 `read`、`write` 或 `edit` 触达更深目录后，plugin 会在后续请求动态加入新适用的指令文件。Harness 不实现 Claude 的 `@path` import 语义。因此 `.claude/CLAUDE.md` 只避免初始根候选冲突，不能保证 Harness 永远不接收该文件。[DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/context/agent-instructions/README.md)

**[事实｜高]** Harness 的项目指令受显式 `maxBytes` 预算限制；超过预算时先丢弃较宽范围的文件，再截断最具体文件，并产生可见预算提示。因此生成器必须把共同核心保持紧凑，而不是依赖「完整大提示词」保证效果。[DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/context/agent-instructions/README.md)

**[事实｜高]** Harness 本地 skill provider 的项目优先根包括 `<projectRoot>/.dsh/skills` 与 `<projectRoot>/.agents/skills`，并要求 skill 名称符合 kebab-case；该机制支持本设计使用项目级 `.agents/skills` 作为共享正文的载体之一。[DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/docs/subsystems/skills.md)

**[事实｜高]** 本地 Skill filesystem provider 省略 `disable-model-invocation` 或 `user-invocable` 时，默认允许对应调用面；`.dsh/skills` 的低 rank 同名副本可覆盖 `.agents/skills` canonical 版本。为避免共享根更新后显式调用限制失效，用户安装 target 包含 Codex 或 Harness 时，安装器把 canonical Skills 与七个 DSH explicit-only overlay 作为同一同步单元。[DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/skill/skill-filesystem/README.md)

**[事实｜高]** Harness 的 skill 根可受 `DSH_AGENTS_HOME` 影响；无可识别 Git 根时，项目 skill 发现会退化到当前工作目录。本系统安装器只生成默认 `<home>/.agents/skills` 布局，不自动跟随自定义环境变量。无 Git 项目应从项目根启动；从嵌套 cwd 启动可能遗漏根 `AGENTS.md` 或 `.agents/skills`。[DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/skill/skill-filesystem/README.md) 本轮未运行真实 Harness 客户端 smoke。

**[事实｜高]** `agent-instructions` 对最终路径组件使用真实路径并允许 symlink 指向更深或项目外目录；shell `cd` 本身又不会触发动态发现。因此不能把“进入目录”或自然语言规则当作信任边界，生成器与安装器必须自行拒绝受管目标上的 symlink。[DeepSeek 固定 commit 文档](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/context/agent-instructions/README.md)

**[事实｜高]** Harness 的 MCP 客户端当前是 opt-in，并把 server 能力暴露为 tools，不暴露 resources 或 prompts；官方 Codex/Claude hook bridge 只实现部分 command-hook 兼容，不等于完整复刻另一平台生命周期。本系统因此不生成臆测 MCP 或 Hook 配置。[MCP client](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/mcp/mcp-client/README.md)；[Codex hook bridge](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/hooks/hooks-codex/README.md)；[Claude Code hook bridge](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/hooks/hooks-claude-code/README.md)

**[事实｜高]** Harness 仍处于 developer preview，核心插件与 API 会继续演进；因此本系统不生成臆测的项目 settings，只交付已核实的指令与 Skill 布局。[DeepSeek 官方页面](https://www.deepseek.com/harness/en/)

## 模型路由研究结论

**[事实｜高]** OpenAI 当前把 GPT-5.6 家族分为 `sol`、`terra`、`luna` 三档，并明确建议从代表性任务评测 reasoning effort，而不是默认把最高 effort 用于全部任务。[OpenAI 官方模型指导](https://developers.openai.com/api/docs/guides/latest-model)

**[事实｜高]** Claude Code 的 `best`、`opus`、`sonnet`、`haiku` 等 alias 会随 provider 与客户端演进；官方建议需要可复现部署时使用完整模型 ID。用户级个人配置适合 alias，团队基准必须记录实际解析模型和客户端版本。[Anthropic 官方模型配置](https://code.claude.com/docs/en/model-config)

**[事实｜高]** DeepSeek Harness 的官方模型设置把凭据单独保存，普通 settings 只保留引用；已发送请求的 session 保留记录的模型，新选择影响新 session。[DeepSeek 官方 provider 指南](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md)

**[推断｜高]** 三档 profile 应表达服务目标，而不是永久绑定型号。当前三档仅存在于文档和 opt-in 示例中，`init-project` 与 `install-user` 不生成这些模型配置：

- `quality`：复杂架构、疑难调试、高价值审查和跨模块改造；使用旗舰模型与较高 effort，但仍需 eval 证明收益。
- `balanced`：大多数功能开发、测试和日常 review；使用中档模型与中高 effort，作为默认基线。
- `economy`：机械查找、明确小改、格式整理和高吞吐辅助任务；使用快速模型与低 effort，失败或不确定时升级。

路由必须允许升级：出现跨模块因果链、多轮失败、重要安全/数据风险、规格冲突或验证证据不足时，从 economy/balanced 升到 quality。任务完成不因使用更贵模型而自动更可信，仍以测试和可审查证据为准。

## 本地材料审计后的取舍

**[事实｜高]** 输入材料中存在完整重复：`Constraint/Codex_AGENTS.md` 在第 1—140 行和第 142 行之后重复一份行为契约；`Constraint/CLAUDE.md` 也在第 864 行之后拼接了另一份英文规则。重复使后续修订无法判断哪一份是权威。详细位置见[本地材料审计](local-material-audit.md)。

**[事实｜高]** Cursor 规则把 RIPER-5、RIPER-6、默认模式和「每次响应必须带模式头」并存，其中部分限制彼此冲突；并且其说明明确针对 Cursor。它们不能作为 Codex、Claude Code 或 Harness 的共享硬规则。

**[事实｜高]** 当前官方 Claude Code 资料确认 `~/.claude/file-history/<session>/` 保存编辑前快照并用于 checkpoint restore，当前入口是 `/rewind`；本轮未在官方资料中核实本地材料所写的 `/restore` 命令。该能力不跟踪 Bash、外部编辑与多数 subagent 改动，也不是版本控制替代品；本系统因此不依赖或承诺它作为通用恢复机制。[目录说明](https://code.claude.com/docs/en/claude-directory)；[Checkpointing](https://code.claude.com/docs/en/checkpointing)

**[事实｜高]** 扩展审计逐文件覆盖了 29 个本地 tips 内容文件，包括 `andrej-karpathy-skills-main/`；`ref_links.txt` 的 8 个条目去重为 7 个来源。文件级结论见[本地 Tips 深度萃取审计](local-material-audit.md)，76 条可执行建议的采用、改写、条件采用或排除及原因见[原子 Tips 决策矩阵](tip-decision-matrix.md)。其中可迁移的四个 Karpathy 约束是：先公开会影响方案的假设、单一用例不提前建抽象、只清理由自身改动造成的 orphan、把目标转成可验证成功标准；它们已独立改写进入 shared core。

**[事实｜高]** 方案 B 修复了上一版“文档里提到但生成物不可达”的关键缺口：初始化器现在把所选 stack / 文件治理模块写入根 `AGENTS.md` 的受管路由块；项目画像只阻塞当前任务相关的未知高风险域，并允许带范围与来源的 `Not applicable`；受管 Skill 以完整目录树生成，项目还可新增不覆盖受管名称的合规 Skill。静态校验可检查结构与来源格式，但不会替代人类判断 `Not applicable` 的真实性。

**[推断｜高]** 适合进入共享核心的内容包括：请求类型与写入边界、范围纪律、凭据保护、事实与推断分层、不可信外部内容、对象/环境特定的授权、最小且可追溯的改动、根因调试、验证证据和不默认提交。它们不依赖单个平台的文件路径或命令。

**[推断｜高]** RIPER 的完整会话门禁不应进入共享核心。原因是它要求固定响应头和逐步用户确认，会与「目标明确时直接执行」「低风险修改可自主验证」的设计决策冲突，并持续占用上下文。保留其有普适价值的元素（明确验收、计划与执行分界、审计）即可。

**[推断｜高]** Codex 与 DSH Desktop 的项目行为正文应共享一个 canonical core，但可各自交付带平台说明的完整快照。两份快照部署时都复制为项目根 `AGENTS.md`，因此互斥；同一仓库同时使用两个平台时采用平台中立根入口，不能并存两份不同的根文件。

## 第三方 skill 的分级

**[事实｜高]** 锁文件已固定 `mattpocock/skills` 与中文仓库的来源 commit；两个固定来源 commit 中的 `LICENSE` 均为 MIT。本轮没有安装、执行脚本或复制完整 skill 正文；具体版本与决定见[锁文件](../../sources/third-party-skills.lock.json)。

| 分级 | 候选方法 | 本项目决定 | 原因 |
| --- | --- | --- | --- |
| 改写吸收 | `tdd`、`diagnosing-bugs`、`code-review`、`writing-for-agents` | adapt | 与测试、调试、审查和 agent 文档目标相符；只保留可迁移方法，重写为本项目的安全边界与中文术语。 |
| 改写吸收 | `grilling`/`grill-with-docs`、`to-spec`、`to-tickets`、`prototype` | adapt | 可分别支撑产品发现、规格、垂直切片和安全原型；删除问题追问、issue tracker 写入、提交或分支等不获授权的副作用。 |
| 改写吸收 | `research`、`domain-modeling`、`codebase-design` | adapt | 分别形成一手证据研究、领域语言/ADR 判断与 seam/deep-module 设计方法；去掉自动后台委派、自动写研究文件、全库扫描与强制产物。 |
| 改写吸收 | `improve-codebase-architecture`、`implement` | adapt | 分别形成显式只读的 `architecture-review` 与显式的 `implementation-orchestration`；保留受限热点审查和小批次实现编排，删除自动 HTML、commit、tracker、分支和越权执行。 |
| 不采用 | `setup-matt-pocock-skills`、`triage`、`wizard`、`setup-pre-commit`、`git-guardrails-claude-code` | exclude | 依赖外部 tracker、安装器、hooks、提交或具体生态；超出本轮的无安装、无真实外部写入边界。 |

**[推断｜高]** 不存在「不经改写直接 adopt」的完整第三方 skill。设计已明确要求第三方 skill 经过重写后才纳入；因此锁文件中的 `adopt` 集合为空是有意约束，不是遗漏。

## Auto Research 方法来源与取舍

**[事实｜高]** 已将 Karpathy 官方仓库固定为 [`karpathy/autoresearch@228791f`](https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117)。其方法把可变文件、运行预算和评价指标固定下来，先建立 baseline，再记录每次实验，并根据结果保留或丢弃改动。

| 决定 | 吸收或排除的内容 | 边界 |
| --- | --- | --- |
| adapt | 固定可变范围、固定度量、baseline、逐次实验记录、失败记录、保留/丢弃与停止条件。 | 独立改写为 Coding Agent 配置比较协议；不继承单 GPU 训练假设。 |
| exclude | `prepare.py`、`train.py`、`program.md` 原文、数据集、日志、性能结论、无限循环和自动 Git branch/commit/reset 行为。 | 本轮没有安装、运行或复制这些材料，也不据其结果宣称本项目质量提升。 |

固定 commit 的 README 写有 `MIT`，但仓库没有 `LICENSE`、`COPYING` 或等价许可证文件，GitHub license 元数据也为空。本项目因此只引用抽象方法，不把 README 标签当作代码或长文本复用许可。证据与 adapt/exclude 映射见[研究方法锁文件](../../sources/research-methods.lock.json)。

## Skill 兼容与产品研发闭环

当前 15 个 Skill 不是工具合集，而是由产品闭环和按需专家能力组成的路由层：

```text
product-discovery
        ↓ 已确认的产品决定
domain-modeling / technical-research / codebase-design
        ↓ 可追踪事实、领域边界与设计 seams
specification
        ↓ 可验收合同
vertical-ticketing
        ↓ 可独立验证的垂直切片
tdd / systematic-debugging / safe-prototyping
        ↓ 实现与证据
implementation-orchestration（显式）
        ↓ 已确认规格的小批次编排
two-axis-code-review
        ↓ Standards + Spec findings
architecture-review（显式、只读）
        ↓ 受限热点候选与风险
writing-for-agents
        ↓ 只沉淀经验证且长期有效的规则
project-profile / memory-governance（显式）
        ↓ 人工治理的长期项目知识
```

`product-discovery`、`specification`、`vertical-ticketing`、`project-profile`、`memory-governance`、`architecture-review` 与 `implementation-orchestration` 共七个 Skill 只能显式调用，避免普通小任务被宽泛 description 自动触发。其余 Skill 可按任务语义发现，但调用也不扩大授权：例如 TDD 不授权安装依赖，review 不授权修代码，prototype 不授权访问生产数据。

## Hook 与 MCP 策略

**[事实｜高]** Claude Code hooks 在会话生命周期之外执行，可按用户、项目和本地 settings 分层；MCP tools 也能进入 hook matcher。[Anthropic Hooks 官方文档](https://code.claude.com/docs/en/hooks)

**[事实｜高]** Claude Code 与 DeepSeek Harness 的 MCP 都会把外部 server 能力暴露成模型工具；Harness 当前 MCP client 仅消费 tools。[Claude MCP](https://code.claude.com/docs/en/mcp)、[Harness MCP client](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/mcp/mcp-client/README.md)

**[安全推断｜高]** MCP server 暴露的实际工具与权限决定真实风险；“提示词要求只读”不会把具备写能力的工具强制变成只读，因此连接和写入授权必须分开治理。

本系统由此采用以下最小策略：

1. 没有稳定重复需求时不启用 MCP。
2. 优先只读、窄作用域 server；凭据只从平台安全存储或环境引用获取。
3. 项目配置采用 server allowlist，不自动批准所有项目 MCP。
4. Hook 只承担可判定、快速、幂等的检查；复杂语义仍由测试或人工 review 处理。
5. Hook 失败必须显式可见；不能用 fail-open 伪装安全控制。
6. 新增 MCP 或 Hook 先在隔离项目 smoke，再记录平台版本、作用域、权限和回滚方式。

## 主要失败模式与对策

| 失败模式 | 症状 | 对策 |
| --- | --- | --- |
| 提示词堆叠 | 重复规则、上下文膨胀、Agent 频繁误停。 | 每条原则只保留一处；任务方法迁往 Skill。 |
| 平台语法伪统一 | 一个文件能被某平台解析，却被另一平台忽略或拒绝。 | canonical + 生成适配器 + drift test。 |
| 模型永久写死 | alias、模型或能力变化后配置静默过期。 | profile 表达目标；运行记录保存解析后的实际模型。 |
| MCP 权限漂移 | 新 server 暴露写工具，项目默认自动批准。 | allowlist、最小凭据、逐工具审计和隔离 smoke。 |
| Hook 变成黑盒 | 检查变慢、吞错或阻塞所有开发。 | 快速、确定、可观察；保留手工恢复路径。 |
| 记忆自动晋升 | 一次失败或模型猜测变成永久规则。 | candidate → 人工审核 → promoted，并记录证据与回滚。 |
| 评测只看一次成功 | 简单任务表现好就宣布配置最优。 | 固定 fixture、多任务 rubric、质量与效率分开记录。 |

Auto Research 评测协议/控制面只把运行记录、成对比较、停止条件和缺失值协议变得严格。其方法来源、吸收项与许可证边界见前文「Auto Research 方法来源与取舍」。本轮没有运行真实 Agent、付费模型或代表性 fixture，因此不能从 schema、示例记录或本地评分器推断模型质量提升。

## 稳定维护约束

1. 模板使用共享 Markdown 正文作为单一事实源，但仅将来源台账已核验的键和文件路径写入平台适配器。
2. 每个 Skill 必须重新编写，明确触发与不触发条件，不复制第三方长段文字；需要保留的 MIT 署名按 `NOTICE.md` 处理。
3. 渲染器必须从 canonical shared core 生成平台快照；校验器必须验证可重渲染一致性、引用、解析和危险默认值，apply 前校验失败必须 fail closed。它不能宣称自然语言规则等同于平台权限控制。
4. 一切平台行为的测试结论必须标注为隔离目录 smoke test、dry-run、平台加载测试或已授权真实副作用之一，不能把文档描述写成实测结果。
