---
title: Coding Agent 系统 ref_links 外链正文账本
doc_type: knowledge
module: coding-agent-system
topic: ref-links-ledger
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# Coding Agent 系统 ref_links 外链正文账本

外链的逐条方法决定已进一步拆入 [Tips 原子决策矩阵](tip-decision-matrix.md)；本文件继续作为正文摘要、证据等级与官方复核的来源账本。

## 读取方法与证据等级

`Constraint/ref_links.txt` 有 8 个 URL 条目，其中 `ai_suxiaole` 的同一 URL 重复一次，因此本账本登记 7 个唯一 URL。GitHub 仓库页可直接访问；6 个 X 链接在 2026-08-29 的登录浏览器会话中逐篇核对了作者、标题与页面主张。X 页面可能需要登录且内容可变，因此本账本保留 canonical URL 和释义摘要，不把浏览器会话、搜索缓存或第三方转录写成可复现的一方证据。作者页面只能支撑“该作者这样主张”；效果断言仍需可复现实验，平台机制仍必须由对应平台第一方资料复核。

- **A级**：对应平台的第一方官方文档或固定官方源码；可支撑明确写出的平台事实。
- **B级**：作者/仓库直接页面，包括本轮登录后可见的 X 作者页面；可支撑“该作者或仓库这样主张”，但页面可变且不是 Codex/Claude/DSH 平台事实。
- **C级**：只有第三方 API、转录或缓存、没有作者直接页面核对的正文；只作研究线索和方法输入，不能单独进入平台事实账本。
- **D级**：经验、营销或未给出可复现实验的效果断言；不得支撑质量或平台能力结论。

`规则 ID` 对应 [`sources/rule-traceability.json`](../../sources/rule-traceability.json)。官方复核中的 `RSP-*` 见 [研究来源索引](../../report-source.md) 和 [Claim-to-Source Ledger](source-ledger.md)。

## 七个唯一 URL

| Source ID | URL、作者与正文标题 | 正文主张摘要 | 证据等级 | 采用 / 改写 / 排除 | 规则 ID、目标层与产物 | 平台官方复核 |
| --- | --- | --- | --- | --- | --- | --- |
| REF-001 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)，仓库 README 标题 *Karpathy-Inspired Claude Code Guidelines* | 用“显式假设、简洁实现、外科式修改、目标驱动验证”四原则降低常见 coding-agent 错误，并提供 Claude/Cursor 安装方式。 | B（仓库直接页面）；Karpathy 原始观察的转述仍是二手 | **语义改写采用**四原则与轻重任务权衡；**排除**整包安装、长文本复制和把 GitHub 热度当效果证据。 | `RUL-004`、`RUL-005`、`RUL-015`、`RUL-020`；shared core / eval / provenance；`templates/shared/*.md`、`evals/rubrics/coding-agent-rubric.md`、`sources/NOTICE.md` | Claude Skill/Plugin、Codex 与 Cursor 的发现机制不能由该 README 证明。Claude/Codex 入口和 Skill 字段分别回到 `RSP-001`、`RSP-002`、`RSP-018`、`RSP-019`；本项目不以 Cursor 为交付目标。 |
| REF-002 | [Vince 聊开发](https://x.com/vincemask/status/2052368318825402507)，*写好 CLAUDE.md 的 8 条经验：让 Claude Code 更懂你的项目* | 建议保持常驻文件短、写可判定规则与禁用项、把根文件作为文档路由器、给敏感模块局部规则、用 Hook 兜底，并维护跨会话 Memory。 | B（需登录的作者直接 Article，2026-08-29 核对）；“200 行上限”等效果/阈值为 D | **采用并改写**可操作规则、指针式上下文、局部规则和确定性控制分层；**排除**通用 200 行硬上限、未经核实 Hook JSON、自动写 Memory 的无审批回路和效果承诺。 | `RUL-006`、`RUL-007`、`RUL-008`、`RUL-009`、`RUL-021`；project profile / local rule / control / memory；`templates/shared/project-core.md` 与 Task 10 profile、memory、controls（已实现，control 默认关闭） | Claude 的规则组织、Hook 和精简上下文分别由 `RSP-002`、`RSP-013`、`RSP-024` 支撑；官方资料没有在本轮登记“200 行硬上限”。任何 Hook 字段必须按 `RSP-013`、`RSP-020` 当前结构重写并实测。 |
| REF-003 | [WquGuru](https://x.com/wquguru/status/2069641926752780384)，*Agent Memory 架构全景：从规则文件、会话检索到反思与技能沉淀* | 把 Memory 分为稳定规则、常驻画像、按需历史、证据/治理和反思/Skill；强调来源、置信度、过期、权限、删除与 prompt-injection 污染。 | B（需登录的作者直接 Article，2026-08-29 核对）；文中多个产品实现细节未逐项一方核验 | **改写采用**Memory 分层和治理字段；规则必须版本化，候选记忆需来源、状态、过期信号和人工晋升；**排除**把 OpenClaw/Hermes/EverOS/Codex 实现描述当成本项目或平台事实。 | `RUL-006`、`RUL-009`、`RUL-015`；project profile / memory governance / eval；Task 10 memory templates 已实现，`EVAL-09`、`EVAL-10` 已建 contract、未运行真实 Agent | Claude 的显式项目指令与 auto memory 区分由 `RSP-002` 复核；本轮已登记的 Codex/DSH 官方资料不足以支持文中所有 Memory 产品细节，因此只吸收架构方法，不下平台结论。 |
| REF-004 | [Vince 聊开发](https://x.com/vincemask/status/2056757482152960110)，*Claude Code 工程化指南：高效组织 .claude/ 目录* | 区分顶层指令、settings、局部 rules、自动 hooks、轻量 commands、多步骤 skills、专用 agents，以及团队/个人配置；主张按需求渐进增加结构。 | B（需登录的作者直接 Article，2026-08-29 核对） | **采用并改写**“稳定规则 / 路径规则 / Skill / deterministic control / platform adapter”分层和渐进增长；**排除**未经一方核验的目录、命令和 Hook 示例。 | `RUL-007`、`RUL-008`、`RUL-010`、`RUL-013`；instruction layers / controls / skill / adapter；`docs/design.md`、`docs/skills-governance.md` 与 Task 10 opt-in controls（已实现） | Claude 的 `.claude/rules`、Skill、settings 与 Hooks 分别回到 `RSP-002`、`RSP-019`、`RSP-020`、`RSP-013`。Codex/DSH 不复用 Claude 目录语义。 |
| REF-005 | [苏乐](https://x.com/ai_suxiaole/status/2092090376899199201)，*10分钟学会CLAUDE.md: 从入门到精通* | 用“能否从仓库发现、是否常用、三个月后是否仍有效”筛减规则；用业务不变量、唯一修改入口、联动关系、DoD 和权威资料提取隐性知识；建议路径下沉、Skill/control 分层、周期修剪和真实小任务评测。 | B（需登录的作者直接 Article，2026-08-29 核对） | **采用并改写**项目画像字段、规则生命周期、单一事实源和行为评测；**排除**未经当轮官方核实的特定 `/doctor` 版本断言、可直接复制的长审计提示词，以及“一套模板适配所有平台”。 | `RUL-006`、`RUL-007`、`RUL-008`、`RUL-013`、`RUL-014`、`RUL-015`；profile / routing / lifecycle / eval；Task 10 profile、traceability 与 `EVAL-07` 至 `EVAL-11` contract 已实现，真实行为仍未运行 | Codex/Claude 指令发现与导入由 `RSP-001`、`RSP-002` 复核；Skill、Hook 与 best practices 由 `RSP-013`、`RSP-018`、`RSP-019`、`RSP-023`、`RSP-024` 复核。具体客户端命令和版本未在本轮官方账本中证实，保持不确定。 |
| REF-006 | [JunEr](https://x.com/JunEr_Lab/status/2053547300639940887)，*有人把 Karpathy 的 4 条规则扩到了 12 条* | 在四原则之外加入“确定性逻辑交给代码”、固定 token budget、显式冲突、写前阅读、测试意图、阶段 checkpoint、遵循仓库约定与 fail loud，并声称个人试用有效。 | B（需登录的作者直接 Article，2026-08-29 核对）；未提供可复现实验，效果为 D | **采用并改写**写前阅读、显式冲突、仓库一致性、阶段状态和失败不可静默；**排除**每任务 4,000 / 每会话 30,000 token 固定值、无法验证的试用效果，以及把所有分类/摘要交给模型的绝对边界。 | `RUL-002`、`RUL-004`、`RUL-008`、`RUL-014`、`RUL-021`；shared core / control / conflict；`templates/shared/*.md`、`sources/rule-traceability.json` | OpenAI 模型资料 `RSP-009` 建议以代表性 eval 调节 effort，并未提供上述通用 token 配额。上下文预算遵循各平台官方机制：Codex `RSP-001`、Harness `RSP-004`，不采用帖子固定数值。 |
| REF-007 | [yaohui12138](https://x.com/yaohui12138/status/2070767053741707426)，无 Article 标题的独立帖子 | 罗列第一性原理、系统思维、显式思维链、思维树、自洽、多视角和反向质疑等关键词，并宣称可让输出质量提升 10 倍。 | B（登录后的作者直接帖子，证明作者主张）；“提升 10 倍”无实验、基线或评测，效果为 D | **排除**“关键词提升 10 倍”、强制展示隐藏思维链、多路径数量和通用魔法词；仅保留已由其他来源和项目规则独立支持的假设、风险、反例与取舍报告。 | `RUL-002`、`RUL-015`、`RUL-018`；epistemics / eval / exclusion；`templates/shared/user-core.md`、`evals/rubrics/coding-agent-rubric.md` | `RSP-009`、`RSP-023`、`RSP-024` 支持清晰目标、必要上下文、验证和精简工作流，不支持固定“10 倍”效果。本系统明确不要求输出隐藏推理过程。 |

## 去重、未验证项与结论

- `REF-005` 在 `ref_links.txt` 出现两次，本账本只保留一个 Source ID；原清单仍保持原样作为输入证据。
- **事实｜高**：7 个 canonical URL 已登记，作者/标题/页面主张曾在 2026-08-29 核对；X 页面需要登录且会变化，因此只把它们当作者经验来源，不当平台机制证据。
- **推断｜高**：外链最有价值的共同点是分层、隐性知识画像、Memory 治理、确定性控制和行为评测，而不是帖子给出的目录、阈值或宣传效果。
- **证据边界｜高**：本账本只保留释义摘要与 canonical URL，不把未保存 receipt 的浏览器过程、第三方转录或搜索缓存当作可复现实验证据。任何效果断言没有代表性实验时为 D 级，任何平台机制主张必须由 A 级官方资料复核。
