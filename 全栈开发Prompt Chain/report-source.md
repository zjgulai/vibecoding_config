# Canonical Claim Ledger：来源、版本与研究边界

本文是 `全栈开发Prompt Chain` 的外部研究事实账本。其他文档可以压缩结论，但不得改变本文记录的
来源版本、确定程度、许可证边界和未验证项。候选采用判断见
[05-GitHub候选与替代审计.md](05-GitHub候选与替代审计.md)。

## 1. 研究范围

### 1.1 固定基线

- 目标仓库基线：[`vinvcn/mattpocock-skills-zh-CN@9fe7e7a3bb352851b986725bab1c7cfb17610a97`](https://github.com/vinvcn/mattpocock-skills-zh-CN/tree/9fe7e7a3bb352851b986725bab1c7cfb17610a97)。
- 生命周期范围：M00 全局控制至 M13 复盘与 Skill 自进化。
- 外部候选范围：Agent Skill、官方工作流、测试/安全工具、发布工具、可观测性 MCP、产品分析与
  实验平台、自优化研究实现。
- 排除：只列链接的聚合站、无法追溯维护主体的转载、没有固定版本的二次摘要、与目标仓库内容
  重复的镜像。

### 1.2 时间和 stars

- GitHub 元数据采集日期：2026-08-30，时区 Asia/Shanghai。
- 采集方式：已认证 `gh api repos/<owner>/<repo>`（等价于 `GET https://api.github.com/repos/<owner>/<repo>`）和只读的文件/commit 查询。
- stars 是动态快照。本文保存的数字不能用于证明质量，也不能保证以后仍相同。
- 本交付没有保留当时的 API 原始响应或响应哈希；因此表中的历史 stars 只能复核为“2026-08-30 的记录值”，不能由稍后重跑上述端点重建。重跑端点只会返回当时刻的当前值。
- `pushed_at` 表示仓库任一 ref 的最近 push，不一定等于默认分支或引用文件的最近修改日期。

### 1.3 证据等级

| 等级 | 本账本中的使用方式 |
|---|---|
| E1 | 固定 commit 的 `SKILL.md`、README、源码、配置或 LICENSE。用于陈述功能、调用和副作用。 |
| E2 | GitHub API 元数据、官方仓库说明。用于陈述 stars、维护主体和活动日期。 |
| E3 | 多个 E1/E2 来源的结构化比较。用于陈述 overlap、gap 和冲突。 |
| E4 | 本项目采用判断。必须写成建议、风险或推断。 |
| E5 | 实际安装、方法效果运行、真实 Agent、benchmark 或生产证据。本轮没有这类 E5；仅在隔离临时副本运行了 fable-method 的结构检查，该结果只证明固定快照的结构检查可通过。 |

## 2. 固定版本与仓库元数据

| Repo ID | 仓库 / 维护主体 | 2026-08-30 stars | 许可证事实 | 活动日期 | 本研究固定版本 |
|---|---|---:|---|---|---|
| R01 | `OthmanAdi/planning-with-files` / OthmanAdi | 26,422 | MIT | 2026-08-30 | `d5d35e6a2316459418e7381faa2682b2894d02c1` |
| R02 | `github/spec-kit` / GitHub | 132,250 | MIT | 2026-08-28 | `16cfab77`、`208d3869`、`39f2ac3c`、`756d6321`，按文件固定 |
| R03 | `addyosmani/agent-skills` / Addy Osmani 与贡献者 | 90,851 | MIT | 2026-08-28 | `c4ad4492`、`ce89b03c`、`91d4d075`，按 Skill 固定 |
| R04 | `PostHog/skills` / PostHog | 60（niche） | MIT | 2026-08-29 | `870cdf070c94f2bf39d8b2a9d4916cfd44779cce` |
| R05 | `NTCoding/living-architecture` / NTCoding | 138（niche） | Apache-2.0 | 2026-08-29 | `2060523fbad15582d726cdd83aaa0d50f0b1268e` |
| R06 | `anthropics/skills` / Anthropic | 172,547 | repo API `NOASSERTION`；本研究涉及的两个 Skill 各有 Apache-2.0 LICENSE | 2026-08-21 | frontend `2235be7c`；webapp testing `3b3fad96` |
| R07 | `vercel-labs/agent-skills` / Vercel Labs | 30,628 | repo API `NOASSERTION`；README 声明 MIT | 2026-08-28 | guidelines `ba469388`；React `805687f3` |
| R08 | `nextlevelbuilder/ui-ux-pro-max-skill` / nextlevelbuilder | 123,080 | MIT | 2026-08-27 | `8bd29e775453ebcae52b6e6514fbf134df0c5770` |
| R09 | `pbakaus/impeccable` / Paul Bakaus | 63,902 | Apache-2.0 | 2026-08-29 | `b0594c72d18006b5865c70eb3a97e8b04064e600` |
| R10 | `wshobson/agents` / wshobson | 39,256 | MIT | 2026-08-26 | architecture `be57c0b2`；RAG `511f8345` |
| R11 | `microsoft/skills` / Microsoft | 2,972 | MIT | 2026-08-28 | `277bb9865832cd182d28ca2300922ee4acdec406` |
| R12 | `supabase/agent-skills` / Supabase | 2,561 | MIT | 2026-08-12 | `32912161e2732c3e5001c6811a76c1f8308ed0da` |
| R13 | `obra/superpowers` / Jesse Vincent、Prime Radiant | 279,511 | MIT | 2026-08-29 | TDD `b9e75ddd`；debug `c74782ea` |
| R14 | `The-PR-Agent/pr-agent` / 社区维护组织 | 12,764 | MIT | 2026-08-30 | `3ac78d979e2b5ebc38e731333bdf082899a11ab0` |
| R15 | `microsoft/playwright-cli` / Microsoft | 12,957 | Apache-2.0 | 2026-08-27 | `cbc09311c468e10fba47964e9b3830fe625c9b01` |
| R16 | `promptfoo/promptfoo` / Promptfoo | 24,672 | MIT | 2026-08-30 | `c5e4097042458801977688ead2372b3c14963afb` |
| R17 | `openai/openai-cookbook` / OpenAI | 75,618 | MIT | 2026-08-28 | `5a49d2a28a2779b1928d9cee988510e85e014910` |
| R18 | `trailofbits/skills` / Trail of Bits | 6,911 | CC-BY-SA-4.0 | 2026-08-28 | `d1f1575cff97816e5cc08af66cd2506099c681d3` |
| R19 | `aquasecurity/trivy` / Aqua Security | 37,693 | Apache-2.0 | 2026-08-28 | `5ae0bb10645f08e6ec81fc257d4dc7e51c15ba69` |
| R20 | `GoogleChrome/lighthouse` / Chrome 团队 | 30,709 | Apache-2.0 | 2026-08-28 | `f9cbf2bbdde9d10dd097304357974fd4c8e0f197` |
| R21 | `dequelabs/axe-core` / Deque Systems | 7,455 | MPL-2.0 | 2026-08-28 | `d50cdf6ea7c6f4cff426b6f3da7850b8c0b32eb6` |
| R22 | `actions/starter-workflows` / GitHub Actions | 11,998 | repo API `NOASSERTION`；固定 LICENSE 为 MIT | 2026-08-03 | `e3c451d60f119b71caebf13c98ac45da6e15b4b7` |
| R23 | `googleapis/release-please` / Google APIs 团队 | 7,418 | Apache-2.0 | 2026-08-24 | `05c6a4f71022304d4edad24ea90c1c16324503d5` |
| R24 | `grafana/mcp-grafana` / Grafana Labs | 3,402 | Apache-2.0 | 2026-08-30 | `dcca5f171e760770b9c57107c39484b3c4a5b813` |
| R25 | `getsentry/sentry-mcp` / Sentry | 834（niche） | FSL-1.1-Apache-2.0 Future | 2026-08-28 | `77c8b1a89538266ef0d04f7e0a4ed07c954c9899` |
| R26 | `PagerDuty/pagerduty-mcp-server` / PagerDuty | 77（niche） | Apache-2.0 | 2026-08-27 | `74707cebf9db2232d148ad7c1367ad1247287df6` |
| R27 | `PostHog/posthog` / PostHog | 39,478 | `ee/` 之外 MIT；`ee/` 另有许可证 | 2026-08-30 | `c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0` |
| R28 | `growthbook/growthbook` / GrowthBook | 8,174 | 大部分 MIT；列明 enterprise 目录为商业许可证 | 2026-08-30 | `de4ff6b5256c13764239f9ed3560e281c5728592` |
| R29 | `microsoft/SkillOpt` / Microsoft | 16,481 | MIT | 2026-08-29 | `db46cd9ae7ce12f1dbd73c945185816aa738751d` |
| R30 | `garrytan/gstack` / Garry Tan 与贡献者 | 130,381 | MIT | 2026-08-29 | `07b59e396c6be5a86619a43151cb9ed62a15ae69` |
| R31 | `sickn33/agentic-awesome-skills` / 社区维护 | 45,682 | 工具代码 MIT；原创非代码内容 CC-BY-4.0；第三方内容沿用上游许可 | 2026-08-30 | `d91ed427d91596da3fcab6dd26ff3306c8003ce5` |

说明：短 SHA 仅用于表格可读性。下面每个来源都使用完整 SHA URL。

### 2.1 C010 有限候选检索记录

- 日期：2026-08-30，Asia/Shanghai。
- 范围：通过 `GET https://api.github.com/search/code?q=<query>&per_page=20` 对每个查询只读取前 20 个结果；查询词为 `filename:SKILL.md "domain modeling"`、`filename:SKILL.md "domain-driven design"`、`filename:SKILL.md "domain model"`。这是候选发现，不是对 GitHub 或其他 Skill catalog 的穷尽检索。
- 筛选标准：候选须是独立仓库中的直接 `SKILL.md`，聚焦领域建模/DDD 方法；再按通用性、近期活动和当日 stars（超过 1,000）筛选。排除目标仓库及其上游、聚合/镜像仓库、与领域建模不直接相关的泛架构条目、项目或框架专用条目，以及未达到 stars 门槛的候选。
- 候选结果：搜索结果包含目标仓库上游 `mattpocock/skills`（非独立）、`sickn33/agentic-awesome-skills` 的镜像/聚合项（排除）和泛架构条目；额外人工审阅的 `NTCoding/living-architecture` `ddd` 是直接 DDD 候选，但当日为 138★，因此保留为 R05 `Niche`，不满足门槛。
- 结论边界：本记录只支持“本次有限候选集中未发现同时满足独立、通用、活跃且超过 1,000★ 的领域建模 Skill”；不支持“生态中不存在”这一更强结论。

## 3. 固定一方来源目录

### 3.1 M00–M05：研究、治理与规格

| Source ID | 标题 / 维护者 | 固定来源 | 来源日期 | 可支持的事实 |
|---|---|---|---|---|
| S001 | Planning with Files / OthmanAdi | [`SKILL.md`](https://github.com/OthmanAdi/planning-with-files/blob/d5d35e6a2316459418e7381faa2682b2894d02c1/.agents/skills/planning-with-files/SKILL.md)；[`LICENSE`](https://github.com/OthmanAdi/planning-with-files/blob/d5d35e6a2316459418e7381faa2682b2894d02c1/LICENSE) | 快照提交 OthmanAdi，2026-08-30 | 三文件计划、hooks、会话 catch-up、完成 gate、文件写入和 MIT。 |
| S002 | Spec Kit Constitution / GitHub | [`constitution.md`](https://github.com/github/spec-kit/blob/16cfab7724a02da6e35fb842f34da70ab883b355/templates/commands/constitution.md) | 文件提交 mnriem，2026-08-10 | scope guard、语义版本、写 constitution、解析模板和执行 hooks。 |
| S003 | Research an Idea / GitHub | [`speckit.assess.research.md`](https://github.com/github/spec-kit/blob/208d38695fc88d8eaec7855c96e5098a852927cf/extensions/assess/commands/speckit.assess.research.md) | 文件提交 mnriem，2026-07-17 | 用户/需求证据、先例、反方证据、URL trust 和 research artifact 写入。 |
| S004 | Shape a Concept + Decide / GitHub | [`shape`](https://github.com/github/spec-kit/blob/208d38695fc88d8eaec7855c96e5098a852927cf/extensions/assess/commands/speckit.assess.shape.md)；[`decide`](https://github.com/github/spec-kit/blob/208d38695fc88d8eaec7855c96e5098a852927cf/extensions/assess/commands/speckit.assess.decide.md) | 文件提交 mnriem，2026-07-17 | 2–3 个概念选项、appetite、rabbit holes、go/clarify/kill 和文件写入。 |
| S005 | Interview Me / Addy Osmani Agent Skills | [`SKILL.md`](https://github.com/addyosmani/agent-skills/blob/c4ad44928cd535fcfee1972988f97309d4cebf9f/skills/interview-me/SKILL.md) | 文件提交 danielart，2026-05-20 | 一问一答、复述确认、confidence/停止阈值和 GUESS。 |
| S006 | Planning User Interviews / PostHog | [`SKILL.md`](https://github.com/PostHog/skills/blob/870cdf070c94f2bf39d8b2a9d4916cfd44779cce/skills/omnibus/planning-user-interviews/SKILL.md)；[`LICENSE`](https://github.com/PostHog/skills/blob/870cdf070c94f2bf39d8b2a9d4916cfd44779cce/LICENSE) | 快照提交 danieldanilov，2026-08-21 | cohort/PII targeting、question plan、voice-agent topic 创建及产品专属限制。 |
| S007 | Clarify + Specification Template / GitHub | [`clarify.md`](https://github.com/github/spec-kit/blob/39f2ac3c63eb23f6f4ffb622acb26ddc01a641f4/templates/commands/clarify.md)；[`spec-template.md`](https://github.com/github/spec-kit/blob/756d63212987152564ed0a52ddfd7f8e9b504e09/templates/spec-template.md) | clarify：orize，2026-07-28；template：WOLIKIMCHENG，2026-05-12 | 歧义分类、即时回写、user journeys、GWT 验收和 edge cases。 |
| S008 | DDD / Living Architecture | [`SKILL.md`](https://github.com/NTCoding/living-architecture/blob/2060523fbad15582d726cdd83aaa0d50f0b1268e/.agents/skills/ddd/SKILL.md) | 文件提交 NTCoding，2026-08-27 | 领域观察分层、domain-expert test、项目专属依赖和限制。 |

### 3.2 M06–M08：UX、架构与工程实现

| Source ID | 标题 / 维护者 | 固定来源 | 来源日期 | 可支持的事实 |
|---|---|---|---|---|
| S009 | Frontend Design / Anthropic | [`SKILL.md`](https://github.com/anthropics/skills/blob/2235be7c60b551f5de82ade908fd3816455afcda/skills/frontend-design/SKILL.md)；[`LICENSE`](https://github.com/anthropics/skills/blob/3b3fad96af16a10759d930941b4520ba0c40edae/skills/frontend-design/LICENSE.txt) | 文件提交 williamqian12，2026-06-09 | 视觉 brief、差异化实现、截图复核和单 Skill Apache-2.0。 |
| S010 | Web Design Guidelines / Vercel Labs | [`SKILL.md`](https://github.com/vercel-labs/agent-skills/blob/ba46938889d4e58635362fb8f618e1178ac3ec46/skills/web-design-guidelines/SKILL.md)；[README 许可证声明](https://github.com/vercel-labs/agent-skills/blob/ba46938889d4e58635362fb8f618e1178ac3ec46/README.md#license) | 文件提交 tmustier，2026-01-16 | `file:line` UI 审查和每次从浮动 URL 取规则。 |
| S011 | UI/UX Pro Max / nextlevelbuilder | [`SKILL.md`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/8bd29e775453ebcae52b6e6514fbf134df0c5770/.claude/skills/ui-ux-pro-max/SKILL.md)；[`LICENSE`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/8bd29e775453ebcae52b6e6514fbf134df0c5770/LICENSE) | 快照提交 binyangzhu000-sudo，2026-08-27 | 本地搜索数据、design-system 持久化、`--force` 边界和 MIT。 |
| S012 | Impeccable v4.1.2 / Paul Bakaus | [`SKILL.md`](https://github.com/pbakaus/impeccable/blob/b0594c72d18006b5865c70eb3a97e8b04064e600/.agents/skills/impeccable/SKILL.md)；[`LICENSE`](https://github.com/pbakaus/impeccable/blob/b0594c72d18006b5865c70eb3a97e8b04064e600/LICENSE) | 快照提交 github-actions[bot]，2026-08-29 | UI 命令路由、context script、持久设计文件、hooks 和 Apache-2.0。 |
| S013 | Architecture Patterns / wshobson | [`SKILL.md`](https://github.com/wshobson/agents/blob/be57c0b2e3c05c528ca6132b87410b385718775f/plugins/backend-development/skills/architecture-patterns/SKILL.md) | 文件提交 wshobson，2026-05-22 | Clean/Hexagonal/DDD 结构和接口倾向。 |
| S014 | Cloud Solution Architect / Microsoft | [`SKILL.md`](https://github.com/microsoft/skills/blob/277bb9865832cd182d28ca2300922ee4acdec406/.github/skills/cloud-solution-architect/SKILL.md) | 文件提交 thegovind，2026-03-02 | Azure WAF、ADR、架构模式和 Azure 专属性。 |
| S015 | React Best Practices / Vercel Labs | [`SKILL.md`](https://github.com/vercel-labs/agent-skills/blob/805687f34e8c10b420e3d11335a0ca2c3c90d992/skills/react-best-practices/SKILL.md) | 文件提交 shuding，2026-04-14 | React/Next.js 性能、server/client boundary 和框架版本依赖。 |
| S016 | API and Interface Design / Addy Osmani Agent Skills | [`SKILL.md`](https://github.com/addyosmani/agent-skills/blob/ce89b03cbd768d4c9f512beedae46c20822a6bf6/skills/api-and-interface-design/SKILL.md) | 文件提交 abhisheksharma2411，2026-08-13 | contract-first、错误、兼容性和 idempotency 方法。 |
| S017 | Supabase Postgres Best Practices / Supabase | [`SKILL.md`](https://github.com/supabase/agent-skills/blob/32912161e2732c3e5001c6811a76c1f8308ed0da/skills/supabase-postgres-best-practices/SKILL.md) | 文件提交 Rodriguespn，2026-07-30 | PostgreSQL/Supabase 查询、安全、schema、锁和诊断规则。 |
| S018 | Test-Driven Development / Superpowers | [`SKILL.md`](https://github.com/obra/superpowers/blob/b9e75dddec7a384f42ce08532ec17bb1ef5d9459/skills/test-driven-development/SKILL.md) | 文件提交 obra，2026-07-05 | 先见证失败、最小通过、删除先写代码和强制触发。 |
| S019 | Systematic Debugging / Superpowers | [`SKILL.md`](https://github.com/obra/superpowers/blob/c74782ead66b8ded584d9b9cf64dcba95457f320/skills/systematic-debugging/SKILL.md) | 文件提交 obra，2026-07-05 | 根因阶段、边界 instrument、三次修复后转架构审查。 |
| S020 | Code Review and Quality / Addy Osmani Agent Skills | [`SKILL.md`](https://github.com/addyosmani/agent-skills/blob/91d4d07522de9577caf5d213e5bf1acc38fa3df2/skills/code-review-and-quality/SKILL.md) | 文件提交 coolTheWorld，2026-08-07 | 五类审查维度、阈值启发式和依赖审查。 |
| S021 | PR Reviewer / PR-Agent | [`review.md`](https://github.com/The-PR-Agent/pr-agent/blob/3ac78d979e2b5ebc38e731333bdf082899a11ab0/docs/docs/tools/review.md) | 文件提交 oleksii-tumanov，2026-08-26 | `/review`、PR 评论/labels、自动触发和模型审查边界。 |
| S022 | Web Application Testing / Anthropic | [`SKILL.md`](https://github.com/anthropics/skills/blob/3b3fad96af16a10759d930941b4520ba0c40edae/skills/webapp-testing/SKILL.md)；[`LICENSE`](https://github.com/anthropics/skills/blob/3b3fad96af16a10759d930941b4520ba0c40edae/skills/webapp-testing/LICENSE.txt) | 快照提交 cj-ant，2026-08-21 | 本地 server helper、Python Playwright、DOM 侦察和 Apache-2.0。 |
| S023 | Playwright CLI Skill / Microsoft | [`SKILL.md`](https://github.com/microsoft/playwright-cli/blob/cbc09311c468e10fba47964e9b3830fe625c9b01/skills/playwright-cli/SKILL.md)；[`LICENSE`](https://github.com/microsoft/playwright-cli/blob/cbc09311c468e10fba47964e9b3830fe625c9b01/LICENSE) | 快照提交 yury-s，2026-08-27 | browser action、state/cookie、file upload、run-code、snapshot 和 Apache-2.0。 |

### 3.3 M09：AI Eval、质量与安全

| Source ID | 标题 / 维护者 | 固定来源 | 来源日期 | 可支持的事实 |
|---|---|---|---|---|
| S024 | Promptfoo Evals / Promptfoo | [`SKILL.md`](https://github.com/promptfoo/promptfoo/blob/c5e4097042458801977688ead2372b3c14963afb/plugins/promptfoo/skills/promptfoo-evals/SKILL.md) | 文件提交 mldangelo-oai，2026-05-06 | eval case、assertion、grader、命令、写配置和 provider 调用。 |
| S025 | Moving from OpenAI Evals to Promptfoo / OpenAI | [Cookbook](https://github.com/openai/openai-cookbook/blob/5a49d2a28a2779b1928d9cee988510e85e014910/examples/evaluation/moving-from-openai-evals-to-promptfoo.md) | 文件提交 kkahadze-oai，2026-08-24 | OpenAI 当前迁移建议、配置迁移和验证步骤。 |
| S026 | RAG Implementation / wshobson | [`SKILL.md`](https://github.com/wshobson/agents/blob/511f8345cf42f84676e0ad56ddfdee33c90a666f/plugins/llm-application-dev/skills/rag-implementation/SKILL.md) | 文件提交 wshobson，2026-07-07 | RAG 模式、供应商依赖和示例栈。 |
| S027 | Supply Chain Risk Auditor / Trail of Bits | [`SKILL.md`](https://github.com/trailofbits/skills/blob/d1f1575cff97816e5cc08af66cd2506099c681d3/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SKILL.md)；[`LICENSE`](https://github.com/trailofbits/skills/blob/d1f1575cff97816e5cc08af66cd2506099c681d3/LICENSE) | 快照提交 kz-tob，2026-08-28 | 支持的生态、脚本测量、coverage、unassessable 和 CC-BY-SA-4.0。 |
| S028 | Agentic Actions Auditor / Trail of Bits | [`SKILL.md`](https://github.com/trailofbits/skills/blob/d1f1575cff97816e5cc08af66cd2506099c681d3/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SKILL.md) | 快照提交 kz-tob，2026-08-28 | GitHub AI Action 数据流、sandbox/allowlist 风险和静态审查边界。 |
| S029 | Trivy / Aqua Security | [README](https://github.com/aquasecurity/trivy/blob/5ae0bb10645f08e6ec81fc257d4dc7e51c15ba69/README.md)；[`LICENSE`](https://github.com/aquasecurity/trivy/blob/5ae0bb10645f08e6ec81fc257d4dc7e51c15ba69/LICENSE) | 快照提交 nikpivkin，2026-08-28 | targets、scanner 类型、安装/集成入口和 Apache-2.0。 |
| S030 | Lighthouse / Chrome | [`readme.md`](https://github.com/GoogleChrome/lighthouse/blob/f9cbf2bbdde9d10dd097304357974fd4c8e0f197/readme.md)；[`LICENSE`](https://github.com/GoogleChrome/lighthouse/blob/f9cbf2bbdde9d10dd097304357974fd4c8e0f197/LICENSE) | 快照提交 lusayaa，2026-08-25 | audit 类别、浏览器/报告写入、throttling、error reporting 和 secret Gist 分享。 |
| S031 | axe-core / Deque | [README](https://github.com/dequelabs/axe-core/blob/d50cdf6ea7c6f4cff426b6f3da7850b8c0b32eb6/README.md)；[`LICENSE`](https://github.com/dequelabs/axe-core/blob/d50cdf6ea7c6f4cff426b6f3da7850b8c0b32eb6/LICENSE) | 快照提交 chutchins25，2026-08-25 | 自动 accessibility 覆盖、incomplete/manual review 和 MPL-2.0。 |

### 3.4 M10–M12：发布、可观测性与增长

| Source ID | 标题 / 维护者 | 固定来源 | 来源日期 | 可支持的事实 |
|---|---|---|---|---|
| S032 | Starter Workflows / GitHub Actions | [README](https://github.com/actions/starter-workflows/blob/e3c451d60f119b71caebf13c98ac45da6e15b4b7/README.md)；[`LICENSE`](https://github.com/actions/starter-workflows/blob/e3c451d60f119b71caebf13c98ac45da6e15b4b7/LICENSE) | 快照提交 cannist，2026-08-03 | 模板类别、维护说明、变量和 MIT。 |
| S033 | Release Please / Google APIs | [README](https://github.com/googleapis/release-please/blob/05c6a4f71022304d4edad24ea90c1c16324503d5/README.md)；[`LICENSE`](https://github.com/googleapis/release-please/blob/05c6a4f71022304d4edad24ea90c1c16324503d5/LICENSE) | 快照提交 release-please[bot]，2026-08-24 | release PR、changelog/version/tag/GitHub Release 及不发布包的边界。 |
| S034 | Grafana MCP Server / Grafana Labs | [README](https://github.com/grafana/mcp-grafana/blob/dcca5f171e760770b9c57107c39484b3c4a5b813/README.md)；[`LICENSE`](https://github.com/grafana/mcp-grafana/blob/dcca5f171e760770b9c57107c39484b3c4a5b813/LICENSE) | 快照提交 sd2k，2026-08-28 | 查询、写 dashboard/alert/incident、tool filtering、RBAC 和 Apache-2.0。 |
| S035 | Sentry MCP / Sentry | [README](https://github.com/getsentry/sentry-mcp/blob/77c8b1a89538266ef0d04f7e0a4ed07c954c9899/README.md)；[`LICENSE.md`](https://github.com/getsentry/sentry-mcp/blob/77c8b1a89538266ef0d04f7e0a4ed07c954c9899/LICENSE.md) | 快照提交 shayna-ch，2026-08-28 | MCP/AI search、token scopes、provider keys、remote data flow 和 FSL。 |
| S036 | PagerDuty MCP Server / PagerDuty | [README](https://github.com/PagerDuty/pagerduty-mcp-server/blob/74707cebf9db2232d148ad7c1367ad1247287df6/README.md)；[`write-tools.md`](https://github.com/PagerDuty/pagerduty-mcp-server/blob/74707cebf9db2232d148ad7c1367ad1247287df6/docs/configuration/write-tools.md)；[`LICENSE`](https://github.com/PagerDuty/pagerduty-mcp-server/blob/74707cebf9db2232d148ad7c1367ad1247287df6/LICENSE) | 快照提交 vvasylkovskyi，2026-08-27 | 默认只读、显式 write flag、具体写工具和 Apache-2.0。 |
| S037 | PostHog Product Platform / PostHog | [README](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/README.md)；[`LICENSE`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/LICENSE) | 快照提交 JakeRuth，2026-08-30 | analytics、replay、flags、experiments、observability、workflow 和混合许可证边界。 |
| S038 | GrowthBook / GrowthBook | [README](https://github.com/growthbook/growthbook/blob/de4ff6b5256c13764239f9ed3560e281c5728592/README.md)；[`LICENSE`](https://github.com/growthbook/growthbook/blob/de4ff6b5256c13764239f9ed3560e281c5728592/LICENSE) | 快照提交 jdorn，2026-08-29 | flags、experiments、统计方法、MCP 写能力和 open-core 许可证。 |

### 3.5 M13：Skill 自进化

| Source ID | 标题 / 维护者 | 固定来源 | 来源日期 | 可支持的事实 |
|---|---|---|---|---|
| S039 | SkillOpt / Microsoft | [README](https://github.com/microsoft/SkillOpt/blob/db46cd9ae7ce12f1dbd73c945185816aa738751d/README.md)；[Codex `skillopt-sleep`](https://github.com/microsoft/SkillOpt/blob/db46cd9ae7ce12f1dbd73c945185816aa738751d/plugins/codex/skills/skillopt-sleep/SKILL.md)；[`LICENSE`](https://github.com/microsoft/SkillOpt/blob/db46cd9ae7ce12f1dbd73c945185816aa738751d/LICENSE) | 快照提交 Yif-Yang，2026-08-29 | optimization loop、held-out gate、session harvest、staging/adopt/schedule 和 MIT。 |
| S040 | Improving MCP Tools / PostHog | [`SKILL.md`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/mcp_analytics/skills/improving-mcp-tools/SKILL.md)；[eval README](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/services/mcp/evals/README.md) | 快照提交 JakeRuth，2026-08-30 | baseline/after、单改动、benchmark integrity、PR/auto-merge guardrail 和 production evidence。 |
| S041 | PostHog Desktop Autoresearch | [`flags.ts`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/desktop/packages/shared/src/flags.ts)；[`schemas.ts`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/desktop/packages/core/src/autoresearch/schemas.ts)；[`prompts.ts`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/desktop/packages/core/src/autoresearch/prompts.ts) | 快照提交 JakeRuth，2026-08-30 | staff-gated 标志、迭代上限、状态恢复、机器可解析报告和 PR convention。 |

### 3.6 横向排除来源

| Source ID | 标题 / 维护者 | 固定来源 | 来源日期 | 可支持的事实 |
|---|---|---|---|---|
| S042 | gstack Design Review / Garry Tan | [`design-review/SKILL.md`](https://github.com/garrytan/gstack/blob/07b59e396c6be5a86619a43151cb9ed62a15ae69/design-review/SKILL.md)；[`LICENSE`](https://github.com/garrytan/gstack/blob/07b59e396c6be5a86619a43151cb9ed62a15ae69/LICENSE) | 快照提交 garrytan，2026-08-29 | clean git、stash/commit、Bun build、browser、analytics 和 MIT。 |
| S043 | Agentic Awesome Skills / sickn33 | [README](https://github.com/sickn33/agentic-awesome-skills/blob/d91ed427d91596da3fcab6dd26ff3306c8003ce5/README.md)；[`LICENSE`](https://github.com/sickn33/agentic-awesome-skills/blob/d91ed427d91596da3fcab6dd26ff3306c8003ce5/LICENSE)；[`LICENSE-CONTENT`](https://github.com/sickn33/agentic-awesome-skills/blob/d91ed427d91596da3fcab6dd26ff3306c8003ce5/LICENSE-CONTENT) | 快照提交 sickn33，2026-08-30 | 聚合规模、安装面、preview 边界和混合上游许可证。 |

### 3.7 AI-Native 控制面研究（2026-09）

| Source ID | 标题 / 维护者 | 固定来源 | 来源日期 | 可支持的事实 |
|---|---|---|---|---|
| S044 | Shao Meng 的三条 AI-Native SDLC 短帖 | [产物链与人工门](https://x.com/shao__meng/status/2095034431614677320)（[公开镜像](https://api.fxtwitter.com/status/2095034431614677320)）；[代码便宜、知识资产与认知债](https://x.com/shao__meng/status/2094027833505144919)（[公开镜像](https://api.fxtwitter.com/status/2094027833505144919)）；[AI Native SDLC](https://x.com/shao__meng/status/2093990789584236857)（[公开镜像](https://api.fxtwitter.com/status/2093990789584236857)） | 2026-09-06 | 本轮通过公开镜像读取三条短帖正文；原始 X 页面及其链接长文未作为正文证据。仅支持作者提出的产物链、人工审阅门、验证闭环与认知债框架，不支持平台行为或效果承诺。 |
| S045 | Agentic engineering 系列 / Simon Willison | [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)；[What is agentic engineering?](https://simonwillison.net/2025/Jun/6/what-is-agentic-engineering/)；[Code is cheap](https://simonwillison.net/2025/Mar/11/cheaper-than-human-thinking/)；[Hoard things you know how to do](https://simonwillison.net/2025/Mar/11/hoard-things-you-know-how-to-do/)；[Better code](https://simonwillison.net/2025/Mar/15/better-code/)；[Anti-patterns](https://simonwillison.net/2025/Jun/7/agentic-engineering-anti-patterns/) | 2026-09-06 | Agent 使用工具、执行与验证循环；人类保留目标、取舍与核验；已验证样例可成为后续任务输入；代码生成变便宜不等于高质量代码成本消失。仅支持该作者的方法论，不支持本项目收益。 |
| S046 | Claude Code current mechanism docs / Anthropic | [Features overview](https://code.claude.com/docs/en/features-overview)；[Hooks](https://code.claude.com/docs/en/hooks)；[Configure permissions](https://code.claude.com/docs/en/permissions) | 2026-09-06 | Claude Code 将项目上下文、hooks 与 permissions 作为不同机制描述。该资料支持能力与权限边界的区分，不支持跨平台等价性或本项目运行时效果。 |
| S047 | Frontier Engineering / Kiro | [总页](https://kiro.dev/topics/frontier-engineering/)；[自主执行](https://kiro.dev/topics/frontier-engineering/maximize-agent-time/)；[面向 Agent 的代码库](https://kiro.dev/topics/frontier-engineering/build-for-agents/)；[快速反馈](https://kiro.dev/topics/frontier-engineering/fast-feedback-loop/)；[边界信任](https://kiro.dev/topics/frontier-engineering/trust-the-boundaries/) | 2026-09-11 | Kiro 的实践者方法论：方向与验证由人负责，Agent 在明确反馈回路和访问边界内执行。页面自述需要数周建设 steering、代码库和任务拆解，并承认实践仍在成熟；不提供本项目或跨平台可复现生产率 benchmark。 |
| S048 | 用户提供、受访问控制的飞书 AI 智能纪要 revision 6 | 公开仓库省略 tenant URL、文档 ID 与完整内容摘要 | 2026-09-15 | 主纪要提出 `Chat → Prompt → Skill → Workflow → RAG`、TUI/CLI 先验能力验证、重复工作 Skill 化及多模型分工等经验。主文为 AI 纪要，关联原始 transcript 无权限；只能支持“纪要这样叙述”，不能证明原始语境、固定模型优势或因果效果。 |
| S049 | Fable compiler / Fable contributors | [仓库 @ `5d62380`](https://github.com/fable-compiler/Fable/tree/5d62380cb30dc1080c6943445a256e27db6246f8)；[`AGENTS.md`](https://github.com/fable-compiler/Fable/blob/5d62380cb30dc1080c6943445a256e27db6246f8/AGENTS.md)；[`Pipeline.fs`](https://github.com/fable-compiler/Fable/blob/5d62380cb30dc1080c6943445a256e27db6246f8/src/Fable.Cli/Pipeline.fs)；[`build.yml`](https://github.com/fable-compiler/Fable/blob/5d62380cb30dc1080c6943445a256e27db6246f8/.github/workflows/build.yml)；[`LICENSE`](https://github.com/fable-compiler/Fable/blob/5d62380cb30dc1080c6943445a256e27db6246f8/LICENSE) | 固定提交 2026-09-14；访问 2026-09-15 | 共享表示/转换、target adapter/printer、reference + target-native test、quicktest/矩阵、生成物和 lockfile 纪律；MIT。只支持工程事实，不支持把 F# 或编译器技术作为通用产品选型。 |
| S050 | fable-method / Sahir619 | [仓库 @ `88b5cf3`](https://github.com/Sahir619/fable-method/tree/88b5cf36b10ee3679e08ee0f0181b9774d481508)；[`fable-method`](https://github.com/Sahir619/fable-method/blob/88b5cf36b10ee3679e08ee0f0181b9774d481508/skills/fable-method/SKILL.md)；[`fable-judge`](https://github.com/Sahir619/fable-method/blob/88b5cf36b10ee3679e08ee0f0181b9774d481508/skills/fable-judge/SKILL.md)；[`fable-domain`](https://github.com/Sahir619/fable-method/blob/88b5cf36b10ee3679e08ee0f0181b9774d481508/skills/fable-domain/SKILL.md)；[`RESULTS.md`](https://github.com/Sahir619/fable-method/blob/88b5cf36b10ee3679e08ee0f0181b9774d481508/eval/RESULTS.md)；[`LICENSE`](https://github.com/Sahir619/fable-method/blob/88b5cf36b10ee3679e08ee0f0181b9774d481508/LICENSE) | 固定提交 2026-07-15；访问 2026-09-15 | 社区萃取、非 Anthropic 官方；ask-shape、named done/verification、intent/twin、只读 judge、adapter + trap + smoke。MIT；小样本、合成 fixture、LLM judge 与负结果限制跨模型推断。 |

## 4. 主张—来源账本

「类型」中的事实可由来源直接复核；判断是本项目的 E4 结论。

| Claim ID | 类型 | 主张 | 主要来源 | 置信 |
|---|---|---|---|---|
| C001 | 事实 | `planning-with-files` 通过 hooks 和三个持久文件维持任务状态，并提供可选会话 replay。 | S001 | 高 |
| C002 | 判断 | M00 只应采用持久状态思想，不应并行建立第二套计划状态机。 | S001 + 本项目 A00–A13 契约 | 高 |
| C003 | 事实 | Spec Kit constitution、assessment、clarify 会写自己的 artifact；部分命令可以执行 extension hooks。 | S002–S004、S007 | 高 |
| C004 | 判断 | Spec Kit 适合提供字段和 gate，不适合作为本项目整包运行时。 | S002–S004、S007 | 高 |
| C005 | 事实 | `interview-me` 使用一问一答和复述确认，同时使用数字 confidence 和停止阈值。 | S005 | 高 |
| C006 | 判断 | 数字 confidence 没有观测校准，不能进入正式需求证据。 | S005 | 中 |
| C007 | 事实 | PostHog 用户访谈 Skill 会解析 cohort/person/email/distinct ID 并创建 voice-agent topic。 | S006 | 高 |
| C008 | 判断 | 该 Skill 只能在 PostHog 已部署且获得 PII/真实联系授权时启用。 | S006 | 高 |
| C009 | 事实 | Spec Kit shape/decide 明确允许「不做」与 kill，并禁止在该阶段写实现设计。 | S004 | 高 |
| C010 | 判断 | 本次有限候选集中未发现同时满足独立、通用、活跃且超过 1,000★ 的领域建模 Skill；这不是对生态的穷尽性结论。 | §2.1 有限候选检索记录、R05 | 中 |
| C011 | 事实 | Anthropic、UI UX Pro Max、Impeccable 均能直接影响 UI；后两者还包含持久文件或 hooks/脚本。 | S009、S011、S012 | 高 |
| C012 | 判断 | UI UX Pro Max 与 Impeccable 应二选一，且不能替代真实 UX 研究。 | S011、S012 | 高 |
| C013 | 事实 | Vercel web-design-guidelines 从浮动远端路径读取最新版规则。 | S010 | 高 |
| C014 | 判断 | 若需要可复现审查，应把实际规则固定到 commit，而不是只固定路由 Skill。 | S010 | 高 |
| C015 | 事实 | React、Supabase、Playwright 候选分别强耦合框架、数据库和浏览器执行环境。 | S015、S017、S022、S023 | 高 |
| C016 | 判断 | 这些候选是 Adapter，不能因通用实现请求自动启用。 | S015、S017、S022、S023 | 高 |
| C017 | 事实 | PR-Agent 可以自动写 PR 评论/labels；Sentry 文档也明确自动 review 可能误报，不建议作为 required check。 | S021、S035 | 高 |
| C018 | 判断 | 模型 code review 只能补充本地双轴审查，不能成为唯一 merge gate。 | S020、S021、S035 | 高 |
| C019 | 事实 | OpenAI 2026-08-24 Cookbook 指向从 OpenAI Evals 迁移到 Promptfoo。 | S025 | 高 |
| C020 | 判断 | 新增 eval 时优先评估 Promptfoo，而不是继续扩展旧 OpenAI Evals 工作流。 | S024、S025 | 高 |
| C021 | 事实 | Trail of Bits 供应链 Skill 把 measured、flagged 和 unassessable 分开，并列明不支持的生态。 | S027 | 高 |
| C022 | 判断 | 安全报告必须同时呈现覆盖率和未知项；无 finding 不是安全证明。 | S027、S029 | 高 |
| C023 | 事实 | Trivy 可扫描 CVE、misconfiguration、secret、license 和 SBOM；扫描目标包括 image、filesystem、repo、VM、Kubernetes。 | S029 | 高 |
| C024 | 事实 | axe-core 官方 README 称平均自动发现约 57% WCAG 问题，并要求对 incomplete 人工复核。 | S031 | 高 |
| C025 | 判断 | Lighthouse/axe 分数只能作为有版本和环境说明的辅助证据，不能声明完整性能或 accessibility 合规。 | S030、S031 | 高 |
| C026 | 事实 | release-please 创建 release PR，合并后写版本/changelog、tag 和 GitHub Release，但不发布 package。 | S033 | 高 |
| C027 | 判断 | release PR merge 和 package/deploy 必须是独立审批，不可由 workflow 成功隐式授权。 | S032、S033 | 高 |
| C028 | 事实 | Grafana MCP、Sentry MCP、PagerDuty MCP 都能访问生产信息；前者和后者还公开了远端写工具。 | S034–S036 | 高 |
| C029 | 判断 | M11 默认只读、最小 token 和 tool allowlist；通知、incident mutation、dashboard/alert mutation 分开批准。 | S034–S036 | 高 |
| C030 | 事实 | PostHog 和 GrowthBook 都支持 feature flags 与 experiments；两者也提供可能改变远端状态的工作流或 MCP。 | S037、S038 | 高 |
| C031 | 判断 | 实验平台不能替代预注册假设、指标、样本单位、guardrail 和停止规则。 | S037、S038 | 高 |
| C032 | 事实 | SkillOpt-Sleep 读取历史 session，支持真实 model backend、staging、adopt、schedule 和 auto-adopt。 | S039 | 高 |
| C033 | 判断 | SkillOpt 只能在脱敏、held-out 数据和人工 adoption gate 下进行隔离试验；作者 benchmark 不是本项目 E5。 | S039 | 高 |
| C034 | 事实 | PostHog improving-mcp-tools 要求 baseline/after、一次一个改动、固定 benchmark version 和 no-regression，并可在明确开启时 auto-merge。 | S040 | 高 |
| C035 | 事实 | PostHog Desktop autoresearch 当前标为 staff-gated，配置最多允许 200 次迭代。 | S041 | 高 |
| C036 | 判断 | PostHog autoresearch 尚不适合作为通用 Skill；只保留单指标、有界迭代和可恢复状态作为设计参考。 | S040、S041 | 高 |
| C037 | 事实 | gstack design review 包含 clean-git、commit/stash、browser build 和 telemetry；AAS 是大规模聚合与分发仓库。 | S042、S043 | 高 |
| C038 | 判断 | 高 stars 的整包副作用或聚合属性不能形成质量证据；两者均不进入默认执行基线。 | S042、S043 | 高 |
| C039 | 事实 + 证据边界 | 三条短帖分别提出「阶段产物链 + 人工审阅门」「代码成本下降下的知识资产、验证闭环与认知债」「AI-Native SDLC」的作者框架；短帖正文已由公开镜像读取，原始 X 页面和外链长文没有被当作可复核正文。 | S044 | 中 |
| C040 | 事实 | Simon Willison 的方法论把 Agent 表述为工具调用、执行与验证循环；人保留目标、取舍和核验责任；有验证的工作样例可作为后续 Agent 的输入。 | S045 | 高 |
| C041 | 事实 + 设计边界 | Anthropic 的当前资料将项目上下文、hooks 与 permissions 分为不同机制；因此自然语言工作流不能被当成权限或确定性控制的替代物。跨平台是否等价仍需各平台一手资料和实测。 | S046 | 高（机制区分）；未证明（跨平台效果） |
| C042 | 设计取舍 | 以既有 A00–A13 作为唯一产物链，在每个非琐碎产物内嵌 Control Contract，并把 R2/R3 分别绑定独立验证与人工 Own，可避免再造平行状态机，同时保留人类责任和回退路径。该结论是设计选择，不是运行时收益证明。 | S044–S046、[08-AI-Native-SDLC控制面规范.md](08-AI-Native-SDLC控制面规范.md) | 高（结构）；未证明（行为收益） |
| C043 | 事实 + 证据边界 | Kiro 将长任务、自测、仓库准备、边界控制与持续调优作为作者方法论；其总页明确将该方法称为需要长期工程投入、仍在成熟的实践指南。文中时间、覆盖率和生产率表达不能作为本项目通用阈值或效果证明。 | S047 | 高（作者页面所述）；未证明（跨平台、本项目或因果收益） |
| C044 | 设计取舍 | 本项目将上述方法改写为既有 Control Contract 内的可选 `Autonomy Envelope`：以范围、证据和风险决定自主程度，保留 R0–R3、独立验证和 Human Own，不把「更长 Agent 时间」变为权限、KPI 或并行写入策略。 | S047、S044–S046、[08-AI-Native-SDLC控制面规范.md](08-AI-Native-SDLC控制面规范.md) | 高（结构）；未证明（真实 Agent 收益） |
| C045 | 事实 + 证据边界 | 飞书主纪要将 AI 产品能力演进叙述为从 Chat 到 Prompt、Skill、Workflow、RAG，并建议先用 TUI/通用 Agent + Skill/RAG 验证问题求解路径；原始 transcript 无权限，纪要不能提供逐字上下文或因果证据。 | S048 | 中（纪要所述）；未证明（效果） |
| C046 | 事实 | Fable compiler 把共享语义、转换、target adapter、target AST/printer 与原生 runtime 验证分层，并以 quicktest 和 CI matrix 提供不同速度/范围的反馈。 | S049 | 高（固定仓库事实）；未证明（迁移收益） |
| C047 | 事实 + 反例 | Fable 的薄平台入口和统一 build 入口能减少重复，但其 README、manifest、target maturity 文档和 agent workflow 仍可出现规则漂移；因此来源成熟度不能替代 SSOT 冲突检查。 | S049 | 高（已核对差异）；未证明（普遍频率） |
| C048 | 事实 + 证据边界 | fable-method 提供请求分类、完成定义、intent/twin、只读 claim 裁决和 trap-first domain bundle，同时公开完整 loop 在简单任务上的空结果、skill discovery 失败及小样本/合成/LLM-judge 局限。 | S050 | 高（仓库所述）；未证明（跨模型或泛化效果） |
| C049 | 设计取舍 | 本项目把故事视为可证伪假设，只在多目标表示或可测漂移成立时使用 `canonical contract → shared transforms → target adapters → native validators`；该模式映射到 A03–A09，不新增 artifact、Gate 或默认 IR 框架。 | S048–S050、[09-故事线驱动与编译式交付模式.md](09-故事线驱动与编译式交付模式.md) | 高（结构）；未证明（行为收益） |
| C050 | 设计取舍 | “重复三次”只作 Skill 候选发现信号；候选必须有稳定输入输出、adapter、trap fixture、answer/oracle、同模型 smoke A/B 和人工采纳门。固定模型分工、完成后补 PRD、每任务全量 Fable Loop 与原样安装不进入默认链。 | S048、S050 | 高（取舍）；未证明（效果） |

## 5. 冲突与处理

### 5.1 OpenAI Evals 的状态冲突

- 较旧 `openai/evals` README 仍描述 Dashboard/package 使用方式。
- 更新的 OpenAI Cookbook（S025，2026-08-24）明确描述向 Promptfoo 迁移。
- 处理：把 S025 作为当前迁移信号；不宣称 `openai/evals` 仓库已停止维护，也不把旧 README 当成
  新项目首选路径。

### 5.2 GitHub API 与许可证文件不一致

- `actions/starter-workflows` 的 API 为 `NOASSERTION`，固定 `LICENSE` 是 MIT。
- `getsentry/sentry-mcp` 的 API 为 `NOASSERTION`，固定 `LICENSE.md` 是
  FSL-1.1-Apache-2.0 Future。
- `PostHog/posthog` 和 `growthbook/growthbook` 是按目录划分的 open-core 许可证。
- `anthropics/skills` 没有统一顶层许可证字段；相关 Skill 各自提供 Apache-2.0 LICENSE。
- `vercel-labs/agent-skills` 没有 API license；README 声明 MIT。
- 处理：以固定文件和目录边界为准，不能把 API 空值改写成 MIT，也不能把 future license 改写成
  当前 Apache-2.0。

### 5.3 stars 与质量

- stars 数字在同一天的不同采集时刻也可能变化。
- stars 不测量正确性、安全性、benchmark 质量、维护者响应时间或许可证可用性。
- 处理：stars 仅在候选筛选中用于发现生态关注度；采用结论由 E1 行为、风险和本项目契约决定。

### 5.4 安全默认值与潜在写能力

- PagerDuty MCP 默认只读，但 `--enable-write-tools` 会增加真实 incident、schedule、team 和 status
  page 写入。
- Grafana MCP 可配置 tool set，但完整服务包含 dashboard、alert、incident、annotation 和 eval 写入。
- Sentry MCP 面向 human-in-the-loop，但示例 token 含 write scopes，AI search 还依赖第三方模型。
- 处理：审计以「完整能力上限」评估风险，不以默认只读推断未来调用安全。

### 5.5 自动化测量的覆盖边界

- axe-core 自己声明自动覆盖有限；Lighthouse 是受环境影响的 lab measurement；Trivy 结果依赖当时
  database 和扫描范围；LLM judge 具有随机性和偏差。
- 处理：所有工具报告必须记录版本、环境、输入范围、重复次数和未知项，并与人工验收组合。

### 5.6 作者 benchmark 与本项目证据

- SkillOpt README 报告了跨 benchmark 的收益；PostHog eval harness 说明其生产使用意图。
- 本研究没有复现这些结果。
- 处理：作者报告属于 E1/E2 的「项目自述」，只能说明存在 benchmark 和作者结论，不能升级为
  本项目 E5 或跨任务保证。

## 6. 未验证边界

1. 未安装任何候选 Skill、CLI、MCP、SDK 或依赖。
2. 未运行 Playwright、Lighthouse、axe-core、Trivy、Trail of Bits collectors 或 Promptfoo。
3. 未调用任何付费模型、LLM judge、embedding、vector database 或远端 RAG 服务。
4. 未连接 Grafana、Sentry、PagerDuty、PostHog、GrowthBook、Supabase 或生产数据库。
5. 未创建 PR、Issue、comment、label、release、tag、deployment、incident、schedule、feature flag、
   experiment、survey 或 interview topic。
6. 未读取 `.env`、token、cookie、session transcript、PII 或生产日志。
7. 未验证候选在 Codex、Claude Code 和 DeepSeek Harness 三个平台上的实际兼容性；只根据文件结构和
   官方说明评估可移植性。
8. 未进行法律审查。许可证记录是固定源文件的技术事实，不是法律意见。
9. 未验证 SaaS 当前价格、配额、地区可用性、保留期或数据处理条款。
10. 未证明 UI guideline、架构模式、统计方法或安全检查适合任一具体项目；启用前仍需项目证据。
11. 本轮只完成控制面静态文档整合，未在 Codex、Claude Code 或 DeepSeek Harness 上进行基线/改后代表性任务对照，也未验证人工责任分级的运行时执行效果。

## 7. 仍存在的证据缺口

- 通用用户研究：高 stars Skill 多数聚焦需求澄清，而非招募、抽样、访谈伦理和研究分析。
  PostHog 候选是产品专属且含真实联系副作用。
- 通用领域建模：未找到满足独立、通用、活跃、超过 1,000★ 且非目标内容镜像的成熟 Skill。
- AI RAG：常见候选强耦合供应商和 SDK，缺少统一的数据治理、检索 eval、成本和隐私契约。
- 可观测性：工具仓库证明可查询或写入，不证明项目已定义正确 SLI、alert ownership 或 incident
  runbook。
- Skill 自进化：现有项目证明了方法和局部 benchmark，不证明从真实会话自动改 Skill 的长期稳定性、
  无数据泄露或无 reward hacking。
- AI-Native 控制面：还没有真实任务的基线/改后对照、跨平台兼容性验证或人工审阅负荷数据；因此当前仅把它作为可审查的静态契约与后续校准假设。

## 8. 可复核性说明

- 所有正文引用使用完整 commit SHA；没有用 `main`、`master`、`HEAD`、`@latest` 或 `@main` 支持
  固定事实。
- stars 和 `pushed_at` 是日期化 API 快照，无法通过固定 commit 重建；本表是其 canonical 记录。
- 采用标签 `Core/Supplement/Alternative/Adapter/Niche/Exclude` 是 E4 判断，不是仓库作者声明。
- 后续如果更新任一候选，必须新增快照日期、固定 commit、许可证复核和 claim 变更记录；不得静默
  替换本文 SHA。
