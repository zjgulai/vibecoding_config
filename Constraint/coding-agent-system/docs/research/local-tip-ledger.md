---
title: Coding Agent 系统本地 Tips 逐文件账本
doc_type: knowledge
module: coding-agent-system
topic: local-tip-ledger
status: stable
created: 2026-08-29
updated: 2026-09-02
owner: self
source: human+ai
---

# Coding Agent 系统本地 Tips 逐文件账本

## 范围与判定口径

本账本覆盖 `Constraint/coding-agent-system/` 之外实际存在的 29 个内容文件：2 个根指令文件、17 个 `cursor_rules` 文件、1 个 `ref_links.txt`，以及本地 Karpathy 包中的 9 个内容或元数据文件。实际存在的 3 个 `.DS_Store` 不属于内容输入。行号基于 2026-08-29 的本地只读快照；原文件变化后必须重新核对。

逐文件账本回答“每个输入文件如何处理”；更细的“每条经验为什么采用或不采用”见 [Tips 原子决策矩阵](tip-decision-matrix.md)。

`可靠性` 只评价该文件能否证明“本地材料确实这样写”，不把本地建议升级为 Codex、Claude Code、Cursor 或 DeepSeek Harness 的平台事实。平台机制必须回到 [Claim-to-Source Ledger](source-ledger.md) 的第一方资料复核。`规则 ID` 对应 [`sources/rule-traceability.json`](../../sources/rule-traceability.json)。Task 10 新增五个评测 contract：`EVAL-07` instruction audit、`EVAL-08` project profile、`EVAL-09` memory governance、`EVAL-10` instruction conflict / prompt injection、`EVAL-11` local rule / linked change；当前全部是 `contract-only`，不表示已有可运行 representative fixture 或真实 Agent 结果。最小变更、根因与 scope 继续由既有 `EVAL-02`、`EVAL-03`、`EVAL-06` 覆盖。

## 逐文件账本

| Source ID | 文件与来源行 | 独特经验或问题 | 决定与改写边界 | 规则 ID | 目标层 | 实际或计划产物 | 评测 | 可靠性 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-001 | `Constraint/Codex_AGENTS.md:7-123,125-137,141-278` | 证据分层、工作区保护、最小 diff、三次失败停止、条件基础设施和人工审核的 Memory 候选；后半正文重复前半且 frontmatter 破损。 | **改写采用**稳定的认知、风险、debug、验证与 Memory 治理约束；排除重复、绝对分支策略和不存在基础设施的默认假设。 | `RUL-001`、`RUL-002`、`RUL-003`、`RUL-004`、`RUL-005`、`RUL-009`、`RUL-019` | user/project shared core；条件能力 | `templates/shared/user-core.md`、`templates/shared/project-core.md`、`.agents/memory/` 模板；本账本记录排除项 | `EVAL-03`、`EVAL-06`、`EVAL-09` | 高（本地全文；平台事实需另证） |
| LOC-002 | `Constraint/CLAUDE.md:31-58,96-159,162-219,513-549,683-747,808-928` | 目标澄清、目录治理、技术栈偏好、备份主张、反谄媚，以及末尾追加的四项 Karpathy 原则。 | **分层改写**：稳定约束进入 core；栈偏好进入条件 module；固定目录/frontmatter 仅沿用项目既有规范；未经核实的 `/restore`、保留数量与自动备份排除。 | `RUL-002`、`RUL-004`、`RUL-007`、`RUL-011`、`RUL-012`、`RUL-019` | shared core；module；排除 | `templates/shared/*.md`、`templates/modules/*.md`、`docs/research/local-material-audit.md` | `EVAL-02`、`EVAL-05`、`EVAL-07` | 高（本地全文）；低（其中平台机制主张） |
| LOC-003 | `Constraint/cursor_rules/00-core.mdc:28-54,84-97` | 从目标出发、澄清实质歧义、给出更低维护路径、修根因，以及默认路由 skill。 | **改写采用**；把“默认先澄清”收窄为会改变结果的实质歧义，把固定目录默认值下沉。 | `RUL-001`、`RUL-005`、`RUL-007` | shared core；能力路由 | `templates/shared/user-core.md`、`templates/shared/project-core.md` | `EVAL-01`、`EVAL-03` | 高（本地全文） |
| LOC-004 | `Constraint/cursor_rules/10-structure.mdc:10-40,43-97` | 根目录克制和正式/草稿/临时/归档隔离，但强制一套目录树。 | **条件改写**：只保留“遵循仓库已有结构”；没有项目证据时不创建固定目录树。 | `RUL-006`、`RUL-007` | project profile / local rule | `templates/shared/project-core.md`；`templates/project/.agents/project-profile.md`（已实现） | `EVAL-08`、`EVAL-11` | 高（本地全文） |
| LOC-005 | `Constraint/cursor_rules/20-python.mdc:14-73` | Python 类型、错误、性能测量、测试和固定 FastAPI/PostgreSQL 工具偏好。 | **条件采用**；通用错误/测量原则留 core，版本、框架、包管理器只在仓库证实时加载。 | `RUL-005`、`RUL-011` | Python/FastAPI module | `templates/modules/python-fastapi.md` | `EVAL-03`、`EVAL-11` | 高（本地全文）；中（技术偏好适用性） |
| LOC-006 | `Constraint/cursor_rules/24-skill-authoring.mdc:14-53` | Skill 自包含、量表不可缩水、证据档位、术语一致、可发现 description，以及 skill 与 hook 边界。 | **改写采用**：保留完整判据、渐进披露和分层；不复制 Cursor/Kimi 路径，也不沿用 RIPER 写入门。 | `RUL-007`、`RUL-008`、`RUL-010` | instruction routing / skill governance / deterministic control | `docs/skills-governance.md`；`writing-for-agents` Create/Audit 扩展（已实现） | `EVAL-07` | 高（本地全文） |
| LOC-007 | `Constraint/cursor_rules/30-docs.mdc:10-42` | 文档分类与 frontmatter 模板；原文件围栏未闭合。 | **条件采用**：只有项目已有同类规范时执行；字段和日期完整性应由模板/validator 校验。 | `RUL-007`、`RUL-008` | docs local rule / control | `templates/shared/project-core.md`；opt-in controls（已实现、默认关闭） | `EVAL-07`、`EVAL-11` | 高（本地全文） |
| LOC-008 | `Constraint/cursor_rules/40-frontend.mdc:18-59` | React/Next/Tailwind 工程偏好、组件克制与文件放置；原 frontmatter 被代码围栏包裹。 | **条件采用**：视觉与最小抽象进入相应 module/core；版本和状态库偏好必须由仓库证实。 | `RUL-004`、`RUL-011` | frontend modules | `templates/modules/frontend-visual-quality.md`、`templates/modules/typescript-nextjs.md` | `EVAL-02`、`EVAL-05`、`EVAL-11` | 高（本地全文）；中（栈偏好适用性） |
| LOC-009 | `Constraint/cursor_rules/50-database.mdc:20-43` | SQL 先测量、索引关联 workload、migration 回滚与影响说明；glob 含不可见 `U+200B`。 | **改写采用**数据库安全门和测量原则；具体 ORM/数据库偏好条件化；不复用损坏 glob。 | `RUL-008`、`RUL-012` | database module / control | `templates/modules/postgresql-migrations.md`、`templates/shared/project-core.md` | `EVAL-04` | 高（本地全文） |
| LOC-010 | `Constraint/cursor_rules/90-safety.mdc:10-34,38-67` | 破坏性操作确认、恢复路径、不做顺手修改；“每次编辑都备份”过度绝对。 | **改写采用**精确目标、确认、可回滚和 scope；备份只在项目存在可靠机制或高风险操作时使用。 | `RUL-003`、`RUL-004`、`RUL-019` | shared core；条件 control | `templates/shared/user-core.md`、`templates/shared/project-core.md` | `EVAL-06` | 高（本地全文） |
| LOC-011 | `Constraint/cursor_rules/anti-sycophancy.mdc:16-70,74-99` | 证据优先、直接指出错误、区分事实/推断/推测；含每句贴标签和连续同意后强制反驳的仪式。 | **改写采用**认知诚实；排除机械标签、一致性锁定和强制唱反调。 | `RUL-002`、`RUL-014` | user shared core / conflict policy | `templates/shared/user-core.md` | `EVAL-01`、`EVAL-10` | 高（本地全文） |
| LOC-012 | `Constraint/cursor_rules/code-change-minimalism.mdc:9-20` | 未授权不写、局部修复、保持接口、复用既有实现、多文件连锁先说明。 | **改写采用**：按请求类型判定写权限，不要求 Change/Build 请求重复说“执行”；保留最小且可追溯 diff。 | `RUL-001`、`RUL-004` | shared core | `templates/shared/user-core.md`、`templates/shared/project-core.md` | `EVAL-02`、`EVAL-06` | 高（本地全文） |
| LOC-013 | `Constraint/cursor_rules/code-line-count-tagging.mdc:9-36` | 要求模型为每个代码块手工统计并标记改动行数。 | **排除**自然语言手工计数；如有业务需求，改由 diff/AST/脚本确定性产生。 | `RUL-017` | deterministic control（仅有需求时） | `docs/research/local-material-audit.md`；现有 control 仅提供受保护路径/联动检查，不实现无需求的行数统计 | `EVAL-07` | 高（本地全文）；低（模型手工计数可靠性） |
| LOC-014 | `Constraint/cursor_rules/common_rules.mdc:22-40,62-318,381-444` | RIPER-5 自动状态机、任务文件、逐步确认、固定响应头、隐藏思考输出与延迟/token 目标。 | **排除常驻状态机**；仅改写采用调查—计划—实现—验证—复审及按风险缩放。隐藏思考、固定头、自动写日志和 token/延迟承诺排除。 | `RUL-007`、`RUL-016`、`RUL-018`、`RUL-021` | workflow skill；排除 | `templates/shared/project-core.md`、`docs/workflow.md`、本账本 | `EVAL-01`、`EVAL-06`、`EVAL-10` | 高（本地全文）；低（性能与强制流程主张） |
| LOC-015 | `Constraint/cursor_rules/dataverse-query-protocol.mdc:9-28` | 先发现知识源、读背景、读 schema 再查询；依赖四个特定工具名。 | **条件采用**为 Dataverse skill 候选；只有目标环境能发现这些工具时启用，否则不生成依赖。 | `RUL-007`、`RUL-019` | project-private skill / adapter | `docs/research/local-material-audit.md`；未生成默认 skill | `EVAL-07`、`EVAL-11` | 高（本地全文）；低（工具存在性） |
| LOC-016 | `Constraint/cursor_rules/implementation-workflow.mdc:9-131` | RIPER-6 的研究、创新、计划、执行、审核、快速分工与原子检查项。 | **改写采用**复杂/快速双路径和偏离计划时报告；排除固定 mode 头、二值审核文案与逐模式口令。 | `RUL-007`、`RUL-016` | workflow skill / shared core | `docs/workflow.md`、`templates/shared/project-core.md` | `EVAL-01`、`EVAL-06` | 高（本地全文） |
| LOC-017 | `Constraint/cursor_rules/mode-gating.mdc:9-22` | 默认快速模式，但所有写入仍要求用户显式说“执行”，并与 RIPER-5 自动流转冲突。 | **排除门禁协议**；改为请求语义和高风险转折确认。 | `RUL-001`、`RUL-016` | user shared core；排除 | `templates/shared/user-core.md`、`docs/research/local-material-audit.md` | `EVAL-01`、`EVAL-06` | 高（本地全文） |
| LOC-018 | `Constraint/cursor_rules/python.mdc:1-10` | 强制个人 `common.lute_logger`、`lute_file`、`mysql_instance` wrapper 和特殊命名。 | **排除默认规则**；仅当目标仓库可检索到符号并有项目证据时作为 private adapter。 | `RUL-011`、`RUL-019` | project-private module | `docs/research/local-material-audit.md` | `EVAL-11` | 高（本地全文）；低（跨项目适用性） |
| LOC-019 | `Constraint/cursor_rules/zh-collaboration.md:6-13` | 使用用户语言、讨论与实施分界、不扩大架构和目录范围。 | **改写采用**语言与 scope；按请求类型消除“所有修改都要二次授权”的歧义。 | `RUL-001`、`RUL-004` | user shared core | `templates/shared/user-core.md` | `EVAL-01`、`EVAL-06` | 高（本地全文） |
| LOC-020 | `Constraint/ref_links.txt:1-9` | 8 个条目中 1 个重复，共 7 个唯一 URL；原文件只有链接，没有标题、主张、正文证据等级或去留映射。 | **改写为来源索引**；逐篇正文与官方复核见 `ref-links-ledger.md`，原文件自身不支撑平台事实。 | `RUL-020` | research provenance | `docs/research/ref-links-ledger.md`、`sources/rule-traceability.json` | `EVAL-07` | 高（本地清单）；无（仅凭清单不能评价正文） |
| LOC-021 | `Constraint/andrej-karpathy-skills-main/CLAUDE.md:3-65` | 明示假设、一次用例不抽象、只清理由自身改动产生的 orphan、把目标转成验证标准。 | **语义改写采用**，避免复制长文本和 Claude 专属副本。 | `RUL-004`、`RUL-005`、`RUL-015`、`RUL-020` | shared core / eval | `templates/shared/user-core.md`、`templates/shared/project-core.md`、`evals/rubrics/coding-agent-rubric.md` | `EVAL-02`、`EVAL-03`、`EVAL-06` | 高（本地全文）；中（来源归属由包自述） |
| LOC-022 | `Constraint/andrej-karpathy-skills-main/CURSOR.md:3-28` | 三份正文需手工同步，反向说明复制会漂移；同时包含 Cursor/Claude 安装建议。 | **采用 drift 教训，排除安装方案**；使用 canonical + renderer，不生成 Cursor 目标。 | `RUL-013`、`RUL-020` | renderer / provenance | `templates/shared/*.md`、`docs/design.md` | `EVAL-07` | 高（本地全文）；低（平台安装事实） |
| LOC-023 | `Constraint/andrej-karpathy-skills-main/EXAMPLES.md:9-93,97-221,225-366,370-520` | 用正反例呈现隐含假设、过度抽象、顺手重构和可验证目标；duplicate-score 示例本身没有证明不稳定。 | **改写为既有评测素材**；不作为平台事实，不采用该排序示例的错误根因结论。 | `RUL-004`、`RUL-005`、`RUL-015` | eval / training material | `evals/rubrics/coding-agent-rubric.md`、`evals/tasks/02-vertical-full-stack-feature.md`、`evals/tasks/03-systematic-debugging.md`、`evals/tasks/06-two-axis-review.md` | `EVAL-02`、`EVAL-03`、`EVAL-06` | 高（本地示例）；中/低（示例的经验性主张） |
| LOC-024 | `Constraint/andrej-karpathy-skills-main/README.md:11-97,132-167,169-171` | 四原则的背景、验收信号与“非琐碎任务谨慎、琐碎任务快速”的权衡；末行仅声明 MIT。 | **方法改写采用**；安装命令不进入配置；许可证声明只作 provenance 线索，不能替代独立许可证核验。 | `RUL-004`、`RUL-015`、`RUL-020` | shared core / eval / provenance | `templates/shared/*.md`、`sources/NOTICE.md` | `EVAL-02`、`EVAL-03`、`EVAL-06` | 高（本地全文）；中（许可证仅自述） |
| LOC-025 | `Constraint/andrej-karpathy-skills-main/README.zh.md:11-97,132-167,169-171` | README 中文译本，语义与英文版大体对应。 | **仅作翻译对照**；英文正文作为该本地包的主要语义参考，避免双重权威。 | `RUL-020` | research provenance | `docs/research/local-tip-ledger.md`、`sources/NOTICE.md` | `EVAL-07` | 高（本地全文）；中（译文等价性） |
| LOC-026 | `Constraint/andrej-karpathy-skills-main/skills/karpathy-guidelines/SKILL.md:1-67` | 把四原则包装成可发现 skill，并声明 license；与根指令内容重复。 | **采用 description/触发边界作为 skill 设计参考**；若 shared core 已包含原则，不再自动加载重复 skill；不复制全文。 | `RUL-010`、`RUL-013`、`RUL-020` | skill governance / renderer | `docs/skills-governance.md`、`sources/NOTICE.md` | `EVAL-07` | 高（本地全文）；中（许可证仅元数据） |
| LOC-027 | `Constraint/andrej-karpathy-skills-main/.cursor/rules/karpathy-guidelines.mdc:1-70` | 同四原则的 Cursor `alwaysApply` 包装，证明多副本高度重复。 | **仅作语义一致性检查**；排除 Cursor 产物与 `alwaysApply` 部署。 | `RUL-013`、`RUL-020` | renderer / excluded target | `docs/design.md`、`docs/research/local-tip-ledger.md` | `EVAL-07` | 高（本地全文） |
| LOC-028 | `Constraint/andrej-karpathy-skills-main/.claude-plugin/plugin.json:1-11` | 声明 plugin 名称、版本、作者、MIT 和 skill 路径。 | **只作本地 provenance**；当前本地包没有固定 commit 与独立许可证文件，元数据不能授权复制代码或长文本。 | `RUL-020` | provenance only | `sources/NOTICE.md`、`docs/research/local-tip-ledger.md` | `EVAL-07` | 高（元数据存在）；低（独立许可证与版本可复核性） |
| LOC-029 | `Constraint/andrej-karpathy-skills-main/.claude-plugin/marketplace.json:1-29` | marketplace 打包、分类和版本信息，不包含新的行为规则。 | **排除行为层**，只保留 provenance 记录。 | `RUL-020` | provenance only | `sources/NOTICE.md`、`docs/research/local-tip-ledger.md` | `EVAL-07` | 高（元数据存在）；低（行为价值） |

## 后续会话来源（不计入逐文件审计）

| Source ID | 来源与时间 | 独特经验或问题 | 决定与改写边界 | 规则 ID | 目标层 | 实际或计划产物 | 评测 | 可靠性 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOC-030 | 用户于 2026-09-02 明确提供并确认采用的 UI 设计经验。 | 任务型界面默认克制；视觉显著性随任务重要性、后果和紧迫性变化；熟悉图标与真实同屏证据优先。 | **条件采用并分层改写**：Codex 用户模板保留最小偏置，前端视觉模块保留完整规则，生命周期 Prompt 与 `EVAL-05` 承载阶段动作和证据。营销/品牌、安全、无障碍和当前主任务例外；tooltip 不承担核心语义；视觉图形尺寸与交互命中区分离。**排除**跨场景绝对禁止和“只有用户要求才可强调”。 | `RUL-022` | Codex UI 偏置 / frontend module / lifecycle Prompt / eval | `templates/user/codex/AGENTS.md`、`templates/project/codex/AGENTS.md`、`templates/modules/frontend-visual-quality.md`、`evals/tasks/05-frontend-visual-quality.md`、M05–M09 Prompt 投影 | `EVAL-05`（contract-only） | 高（用户当次明确确认）；未运行真实浏览器或 Agent 评测 |
| LOC-031 | 用户于 2026-09-02 确认采用的消融式删减检查实战方法。 | 以首次可信 baseline 为起点，只检查当前新增内容；逐项、单候选删减并以同一验收复验。 | **条件化改写采用**为受限、逐项、同验收复验的检查；排除“删得越多越好”和未固定模型 / fixture 的因果结论。 | `RUL-004` | lifecycle / eval | `docs/sop/project-lifecycle.md`、`evals/tasks/02-vertical-full-stack-feature.md`、`evals/tasks/06-two-axis-review.md` | `EVAL-02`、`EVAL-06`（contract-only） | 高（用户当次明确确认）；模型效果未验证 |

## 覆盖结论

- **事实｜高**：原始逐文件来源 `LOC-001`–`LOC-029` 恰好 29 个，并与 29 个本地内容文件一一对应；`LOC-030`、`LOC-031` 是后续会话来源，不计入原始 29 个。
- **事实｜高**：每项采用、改写或排除决定均给出规则 ID、目标层、产物和评测 ID；已实现 artifact 与 `contract-only` 评测边界分别标明，结构通过不等于行为有效。
- **边界**：本账本没有执行输入材料中的安装、Hook、数据库、Git 或外部写入命令，也没有把本地元数据中的许可证声明升级为已核许可。
