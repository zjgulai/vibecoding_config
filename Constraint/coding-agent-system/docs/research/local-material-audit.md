---
title: Coding Agent 系统本地 Tips 深度萃取审计
doc_type: analysis
module: coding-agent-system
topic: local-material-audit
status: stable
created: 2026-08-29
updated: 2026-09-02
owner: self
source: human+ai
---

# Coding Agent 系统本地 Tips 深度萃取审计

## 范围、方法与证据边界

**[事实｜高]** 本轮逐文件只读检查 `Constraint/coding-agent-system/` 之外的 29 个内容文件：`Codex_AGENTS.md`、`CLAUDE.md`、17 个 `cursor_rules` 文件、`ref_links.txt`，以及 `andrej-karpathy-skills-main/` 中的 **9 个**文档、规则、skill 和 plugin 元数据文件，即 `2 + 17 + 1 + 9 = 29`。3 个 `.DS_Store` 仅作为操作系统元数据忽略。没有执行材料中的命令，没有读取 `.env`，也没有安装任何 plugin 或第三方 skill。逐文件来源行、去留、规则 ID、落点和评测见 [本地 Tips 逐文件账本](local-tip-ledger.md)。

**[事实｜高]** 当前 `/Users/lute/Project/vibecoding_config` 不是 Git repository，因此本审计没有 branch、commit 或 `git diff` 证据。本地文件内容是 tips 输入证据，不自动成为 Codex、DSH Desktop、Claude Code 或 Cursor 的平台事实；平台行为仍由官方来源账本支撑。

## 后续来源

**[事实｜高]** `LOC-030` 是用户于 2026-09-02 会话中新增并确认采用的 UI 设计经验。它不属于本文件对原始 29 个本地内容文件的逐文件审计；原始计数仍为 29，`LOC-030` 仅增加后续来源追踪。

**[事实｜高]** `LOC-031` 是用户于 2026-09-02 确认采用的消融式删减检查实战方法。它同样不属于原始 29 个本地内容文件；方法被条件化改写为受限、逐项、同验收复验的检查，未固定模型或 fixture 的效果因果结论不纳入。

萃取时每条规则只允许进入一个主要层级：

1. 所有项目普遍需要的稳定边界进入用户或项目 shared core。
2. Codex / DSH 的发现、预算和 skill 差异进入平台 adapter。
3. 多步骤方法进入 skill；语言、框架和数据库约定进入按需 module。
4. 可确定判定的检查进入 permissions、sandbox、hook 或 CI。
5. 冲突、未经验证、环境私有或高维护规则排除，不用“先放进去再说”。

## 逐文件萃取矩阵

| 文件 | 主要价值 | 决定 | 落点或排除原因 |
| --- | --- | --- | --- |
| `Constraint/Codex_AGENTS.md` | 指令读取、证据分层、工作区安全、最小实现、debug 停止条件、验证与开发记录。 | 深度改写吸收 | 进入 user/project core；原文件正文完整重复一次、frontmatter 破损，不能原样交付。 |
| `Constraint/CLAUDE.md` | 目标澄清、根因、文件治理、安全、反顺从、语言与栈经验。 | 分层吸收 | 最小 diff、证据、权威文件和条件化文档治理进入 core；固定栈、强制目录、强制 frontmatter、commit 语言和 checkpoint 承诺排除或下沉。文件开头围栏与末尾追加规则造成多重正文。 |
| `cursor_rules/00-core.mdc` | 目标、真实动机、更优路径、根因、先复用、结构优先。 | 改写吸收 | “实质歧义才澄清”“已有实现优先”“根因修复”进入 core；不保留默认先问和固定表达模板。 |
| `cursor_rules/10-structure.mdc` | 根目录克制、正式/草稿/临时/归档分类。 | 条件吸收 | 只保留“遵循仓库已有结构”；固定顶层目录树不进入通用 core。文件存在未闭合围栏。 |
| `cursor_rules/20-python.mdc` | Python/FastAPI 质量、类型、错误和配置建议。 | Module | 仅在仓库真实使用 Python/FastAPI 时加载；版本、包管理器和命令从项目发现，不采用 `alwaysApply`。frontmatter 与围栏结构无效。 |
| `cursor_rules/24-skill-authoring.mdc` | skill 自包含、量表和边界不可缩水、证据档位、术语同步、description 可发现、交付检查。 | Skill 治理重点吸收 | 进入 skill authoring / writing-for-agents 能力层；确定性格式检查交给 validator，不常驻根规则。 |
| `cursor_rules/30-docs.mdc` | 文档分类与元数据。 | Docs module / hook | 只有项目已有规范时应用 frontmatter；日期、索引和字段完整性宜由模板或 CI 检查。文件围栏未闭合。 |
| `cursor_rules/40-frontend.mdc` | React / Next.js / Tailwind 工程与视觉偏好。 | Module | 进入 TypeScript/Next.js 与视觉质量模块；不把 React 19、Next.js 15、Zustand、pnpm 等偏好写入通用规则。frontmatter 与围栏结构无效。 |
| `cursor_rules/50-database.mdc` | migration 风险、回滚、验证和性能测量。 | Module + 项目核心触发门 | core 只保留 migration 安全门；SQL、索引和 `EXPLAIN` 细节进入数据库模块。原 glob 含不可见 `U+200B`，不能复用。 |
| `cursor_rules/90-safety.mdc` | 保护既有变更、破坏性操作、scope 和恢复。 | 改写吸收 | 进入 user/project core；“每次编辑都备份”改为使用项目真实存在且已验证的回退机制。 |
| `cursor_rules/anti-sycophancy.mdc` | 事实 / 推断 / 未知、证据优先、发现错误直接指出。 | 改写吸收 | 进入 user core；排除每句话贴标签、连续同意后强制反驳、无新证据却锁定立场等仪式。 |
| `cursor_rules/code-change-minimalism.mdc` | 只改相关逻辑、复用、稳定接口、连锁影响先说明。 | 项目核心必选 | 与 Karpathy 四原则合并为最小、可追溯 diff；不单独复制一份重复规则。 |
| `cursor_rules/code-line-count-tagging.mdc` | 统计 AI 生成代码行数。 | 排除正文，需求存在时改为 hook | 模型手工计数不可重复、污染输出；应从 diff / AST / 脚本确定性生成。 |
| `cursor_rules/common_rules.mdc` | RIPER-5 调研、计划、执行、审核状态机。 | 排除常驻状态机 | 只吸收调查、验证计划和需求复审；固定 mode 头、逐步确认、自动写任务文件、内部思考输出和延迟目标排除。 |
| `cursor_rules/dataverse-query-protocol.mdc` | Dataverse connector 查询步骤。 | 条件 Skill | 只有目标环境真实提供对应 connector / tool 时启用；当前材料没有工具存在性证据。 |
| `cursor_rules/implementation-workflow.mdc` | RIPER-6 的 research / plan / execute / review 分工。 | 按需 workflow skill | core 只保留复杂任务阶段与偏离方案时报告；完整门禁不常驻。 |
| `cursor_rules/mode-gating.mdc` | RIPER-6 口令门。 | 排除 | 与 `common_rules.mdc` 的默认模式、自动流转和响应头直接冲突，也会阻断明确的低风险实现请求。 |
| `cursor_rules/python.mdc` | `common.lute_logger`、`lute_file`、`mysql_instance` 等个人 wrapper。 | 项目私有 adapter | 仅当目标仓库能检索到这些符号时使用；否则会编造依赖和个人约定。 |
| `cursor_rules/zh-collaboration.md` | 中文协作、讨论与实施边界。 | 用户级吸收 | 保留用户语言和不扩大 scope；把“未授权不修改”按请求类型消歧，避免用户重复说“执行”。 |
| `Constraint/ref_links.txt` | 外部研究 URL 清单。 | 改写为来源索引输入 | 8 个 URL 条目只有 7 个唯一 URL；原文件本身不含标题、主张、日期或可靠性，不能直接支撑配置事实。逐篇正文摘要、证据等级、去留和官方复核已登记在 [外链正文账本](ref-links-ledger.md)。 |
| `andrej-karpathy-skills-main/CLAUDE.md` | 先暴露假设、简洁、精准修改、目标驱动。 | 语义改写 | 四原则进入 shared core；不复制长段原文，不维护 Claude 专属副本。 |
| `andrej-karpathy-skills-main/CURSOR.md` | Cursor 安装与三副本同步说明。 | 排除平台部署内容 | “三副本需同步”反证手工复制的 drift 风险；本系统改用 canonical + renderer。 |
| `andrej-karpathy-skills-main/EXAMPLES.md` | 过度假设、抽象、scope creep 和验收正反例。 | 评测 / 培训素材 | 不常驻上下文；其中 duplicate-score 示例不能单独证明排序不稳定，因此不当作平台或语言事实。 |
| `andrej-karpathy-skills-main/README.md` | 英文说明、安装、定制与谨慎权衡。 | 方法说明 | 吸收“非琐碎任务更严格、琐碎任务不拖慢”；安装命令不进入配置。 |
| `andrej-karpathy-skills-main/README.zh.md` | README 中文译本。 | 仅作对照 | 不与英文版同时作为权威规则源，避免重复维护。 |
| `andrej-karpathy-skills-main/skills/karpathy-guidelines/SKILL.md` | 四原则的可调用 skill。 | 语义改写，避免双重自动加载 | “单次使用不建抽象”“只清理自己造成的 orphan”“目标转验收”进入 core；若 root 已包含，不再自动加载重复 skill。 |
| `andrej-karpathy-skills-main/.cursor/rules/karpathy-guidelines.mdc` | 四原则的 Cursor 包装。 | 不生成 Cursor 产物 | 只用于核对语义一致性，丢弃 Cursor frontmatter。 |
| `andrej-karpathy-skills-main/.claude-plugin/plugin.json` | plugin 名称、版本与作者声明。 | 只作本地 provenance 线索 | 本地目录无可核 commit 与独立 `LICENSE`；不据此复制代码或长文本。 |
| `andrej-karpathy-skills-main/.claude-plugin/marketplace.json` | marketplace 打包信息。 | 排除行为规则 | 只描述分发，不影响 Agent 工作契约。 |

## 规则落点摘要

本节只保留主题级摘要，不再作为无映射的完成结论。29 个文件逐项到规则 ID、目标层、产物和评测的映射以 [本地 Tips 逐文件账本](local-tip-ledger.md) 为准；原始 76 条可执行建议及后续 `TIP-077`、`TIP-078` 的去留与原因见[原子 Tips 决策矩阵](tip-decision-matrix.md)；机器可解析的规则级追踪以 [`sources/rule-traceability.json`](../../sources/rule-traceability.json) 为准。项目画像、Memory、controls、15 个 Skills 与五个新增评测 contract 已实现；`EVAL-07` 至 `EVAL-11` 仍为 `contract-only`，没有真实 Agent 行为运行证据。

| 萃取主题 | 用户级共同层 | 项目级共同层 | 平台 adapter |
| --- | --- | --- | --- |
| 请求类型 | Explain / Review / Diagnose 默认只读；Change / Build / Fix 授权本地直接相关改动。 | 同一语义落到项目边界，并加入复杂任务与快速路径。 | 无平台差异。 |
| 认知纪律 | 事实 / 推断 / 未知、证据优先、不编造、截断输出重取。 | 外部网页、issue、日志、仓库文本和工具输出按不可信数据处理。 | 无平台差异。 |
| 最小实现 | 不投机抽象、不顺手重构、只清理自己的 orphan。 | 每一行可追溯、单一用例不建层级、权威文件优先。 | 无平台差异。 |
| 风险授权 | 破坏性与外部副作用需对象明确的授权。 | read→write、local→remote、test→production、free→paid 时重新确认。 | 配置文件不降低平台 permissions / sandbox。 |
| Debug | 先复现、可证伪根因、三次失败停止叠 patch。 | 加入架构、数据流、状态、依赖和失败边界复审。 | 无平台差异。 |
| 验证 | 完成必须有新鲜、完整输出；证据层级不能冒充。 | 窄验证后按公共接口、数据、权限、安全、UX 风险扩大，并对照需求复审。 | 无平台差异。 |
| 能力分层 | Skill / MCP 不扩大授权。 | 根规则、skill、module、hook / CI、MCP 各归其层。 | Codex 用 `.agents/skills`；DSH 可用 `.agents/skills` + `.dsh/skills` overlay。 |
| 加载与预算 | 用户文件只提供跨项目行为。 | 项目 shared core 保持单一事实源。 | Codex 32 KiB 默认预算与根到 cwd；DSH `maxBytes`、动态发现、无 Git cwd 回退。 |

## 明确冲突与处理

| 冲突 | 证据 | 处理 |
| --- | --- | --- |
| RIPER-5 默认 `RESEARCH`，RIPER-6 默认快速模式。 | `common_rules.mdc` vs `mode-gating.mdc` | 两套完整状态机均不常驻；只保留复杂任务的调查、计划、实现、验证、复审。 |
| 一处允许自动流转到执行，另一处要求用户显式说“执行”。 | `common_rules.mdc` vs `mode-gating.mdc` / `implementation-workflow.mdc` | 改为请求类型语义：Change / Build / Fix 已授权本地实现；高风险转折另行确认。 |
| 响应头要求 `[MODE: ...]` 与 `[模式: ...]` 不一致。 | 两套 RIPER 文件 | 全部排除，避免固定格式占用上下文。 |
| 研究阶段自动写任务文件，与“未授权不修改”冲突。 | `common_rules.mdc` vs `zh-collaboration.md` / minimalism | 只读请求不写；实现请求可以在 scope 内写，任务日志仅在项目已有约定时创建。 |
| “始终显示完整代码上下文”与最小输出冲突。 | `common_rules.mdc` vs `00-core.mdc` / Karpathy | 默认给最小充分上下文，需要审查时再扩展。 |
| 无条件拒绝兼容代码可能破坏真实兼容要求。 | `CLAUDE.md` | 兼容性由规格与现有公开接口决定，不使用 blanket rule。 |
| “项目已有方向即可新增依赖”与 SOP 的依赖确认门冲突。 | 旧 project core vs `workflow.md` / SOP | 统一为：当前需求需要且用户同意，或项目规范已为当前任务明确指定。 |

## 明确排除或下沉的内容

- Cursor 不作为目标平台，不生成 `.cursor/rules`；只吸收其文档分层与局部作用域亮点。
- 不输出隐藏思考过程，不要求每次响应 mode header、逐步骤确认、30 秒延迟目标或最大 token 使用。
- 不把 Python 3.12、React 19、Next.js 15、FastAPI、Zustand、pnpm 等固定为所有项目默认值。
- 不强制固定目录树、全局命名公式、所有 Markdown frontmatter 或 `owner: self` / 手工 `updated` 字段。
- 不手工给代码块标 `ai-generated-code:<num>`；需要统计时由确定性工具完成。
- 不假设 Dataverse 工具、个人 Python wrapper、命令包装器、file-history、`/restore`、自动备份或 self-evolution 基础设施存在。
- 不把自然语言规则说成 permissions、sandbox、hook、CI 或 MCP 的强制权限边界。
- 不把 `ref_links.txt` 的裸 URL 清单当作正式证据；只有 [外链正文账本](ref-links-ledger.md) 中完成正文读取、证据分级和平台官方复核的摘要才可作为方法线索，平台事实仍回到第一方来源。

## 格式与维护缺陷

- `Codex_AGENTS.md` 的两个约 129 行行为区块完全重复，且 frontmatter 分隔破损。
- `CLAUDE.md` 开头存在 Markdown 围栏，末尾再追加英文 Karpathy 全文，形成多个正文起点。
- `10-structure.mdc`、`20-python.mdc`、`30-docs.mdc`、`40-frontend.mdc` 存在未闭合围栏；部分 frontmatter 不在首行或混入正文。
- `50-database.mdc` 的 migration glob 含 `U+200B`，不能可靠匹配预期路径。
- 多个技术栈规则设置 `alwaysApply: true`，即使格式修复也会把无关栈内容注入所有任务。
- `ref_links.txt` 有重复 URL；其正文与 claim-to-source 映射现由 [外链正文账本](ref-links-ledger.md) 和 [`rule-traceability.json`](../../sources/rule-traceability.json) 维护，原清单继续保留为输入证据。
- Karpathy 四原则同时存在于 Claude、Cursor、Skill、README 与示例文件；手工同步会持续漂移，因此本系统只维护 shared core 一份规范源。

## 结论与不确定项

**[推断｜高]** Codex 与 DSH 项目行为正文应共享一份 project core；本地 tips 中没有 DSH 专属规则，不能据此编造 DSH 能力。平台差异只能来自已经登记的官方 DeepSeek Harness 资料。

**[事实｜高]** 两个平台在目标项目中都使用根 `AGENTS.md`。`templates/project/codex/AGENTS.md` 与 `templates/project/deepseek-harness/AGENTS.md` 因此是互斥的发行快照，部署时都复制为根 `AGENTS.md`；同一项目同时使用两平台时采用 `templates/project/AGENTS.md` 共享入口，而不是并存两份根文件。

**[不确定｜中]** `andrej-karpathy-skills-main` 本地 plugin 元数据声明版本和 MIT，但当前目录缺少可核固定 commit 与独立许可证文件。本系统只独立改写抽象原则，不复制其代码或长文本，也不把该元数据升级为平台事实。

**[不确定｜中]** 本轮没有用四份配置启动真实 Codex 或 DSH Desktop / Harness 会话。文件结构、渲染一致性和本地测试通过只能证明工具包契约；实际 discovery、预算截断、skill 调用和模型效果仍需固定客户端版本的隔离 smoke 与代表性 eval。
