# GitHub 候选与替代审计

本文评估可补充 `mattpocock-skills-zh-CN` 基线的外部 Agent Skill、工作流和工具适配器。
评估范围对应 M00–M13。事实来源、固定版本、许可证依据、冲突和未验证边界统一记录在
[report-source.md](report-source.md)。

## 1. 结论摘要

- 现有目标 Skill 继续承担方法层 `Core`。外部高关注度仓库不因 stars 较高而自动升级为
  `Core`。
- 建议吸收的方法片段包括：持久化计划、机会证据与反证、概念选项与 kill gate、规格歧义表、
  有界 UI 复核、held-out eval、供应链覆盖边界、发布 PR、只读生产诊断和单指标实验循环。
- 工具型候选统一作为 `Adapter`：只有项目已选用相应平台、凭证范围明确、目标环境可恢复时才启用。
- `Niche` 表示适用面窄或 stars 低于 1,000，不表示内容质量差。
- 不建议整包安装任何候选。采用单位是固定 commit 下的单个 `SKILL.md`、单份模板、单项规则或
  已批准的工具适配器。
- 本研究没有安装或运行候选，没有执行真实浏览器测试、安全扫描、模型 eval、发布、生产查询、
  用户联系、实验或 Skill 自优化。因此没有 E5 实测证据。

## 2. 评估口径

### 2.1 等级

| 等级 | 本文含义 |
|---|---|
| `Core` | 本项目默认方法。除特别说明外，由目标仓库 Skill 或 Prompt 契约承担。 |
| `Supplement` | 增加检查表、证据类型或专项方法，不接管主流程。 |
| `Alternative` | 同一职责的另一套完整流程，只能二选一。 |
| `Adapter` | 连接特定框架、服务或命令行工具；启用取决于项目技术栈和授权。 |
| `Niche` | 适用范围窄、强耦合特定产品，或生态关注度较低。 |
| `Exclude` | 仅保留为反例或研究来源，不进入执行基线。 |

### 2.2 stars 和活动日期

所有 stars 均为 2026-08-30 的 GitHub API 快照。stars 只能说明当日生态关注度，不能证明方法正确、
安全、可维护或适合本项目。表中的「活动」是仓库 `pushed_at` 日期；固定 commit 才是可复核的内容
版本。快照使用 `GET https://api.github.com/repos/<owner>/<repo>` 获取；未保存原始响应或哈希，之后重跑只能得到当前值，不能重建历史计数。完整记录和边界见 `report-source.md` 的「时间和 stars」与「固定版本与仓库元数据」。

### 2.3 通用采用规则

1. 先读取固定版本内容，再人工改写为本项目规则；不执行远端一键安装。
2. 不复制与本项目无关的 hooks、脚本、安装器、遥测或平台配置。
3. 许可证按单个文件和所在目录判断；仓库 API 的 `NOASSERTION` 不等于没有许可证。
4. 浏览器、扫描、eval、发布、生产查询和远端写入分别设置审批门，不因 Skill 已安装而自动授权。
5. 输出区分事实、工具测量、模型判断和未知项；「未发现」不得改写成「不存在」。

## 3. M00 全局上下文与流程控制

**Core（现有）：** `A00-context-pack.md`、模块状态机、审批门和确定的 A00–A13 文件交接契约。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Supplement` | `OthmanAdi/planning-with-files` | 26,422★；MIT；活动 2026-08-30；[v3.12.0 `SKILL.md`](https://github.com/OthmanAdi/planning-with-files/blob/d5d35e6a2316459418e7381faa2682b2894d02c1/.agents/skills/planning-with-files/SKILL.md) | 借用 `task_plan.md`、`findings.md`、`progress.md` 的职责分离、恢复测试和完成门。只把模式映射到本项目既有 A00–A13 产物，不另建第二套计划文件。 | 完整插件注册 `UserPromptSubmit`、`PreToolUse`、`Stop`、`PreCompact` hooks，可读取同项目会话记录，并持续写计划文件。`--replay` 可能暴露会话片段。整包会与本项目控制器争夺状态源。 |

**采用判断：** 采用「文件是持久状态、对话只是临时缓存」这一方法；不采用 hooks、session replay、
自动 stop gate 和每两次查看即写文件的硬编码频率。

## 4. M01 项目初始化与治理

**Core（现有）：** 项目 `AGENTS.md`、用户约束、风险边界和 `A01-project-charter.md`。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Supplement` | `github/spec-kit` 的 constitution 方法 | 132,250★；MIT；活动 2026-08-28；[`constitution.md`](https://github.com/github/spec-kit/blob/16cfab7724a02da6e35fb842f34da70ab883b355/templates/commands/constitution.md) | 借用原则必须可测试、治理变更使用语义化版本、非治理请求延期处理和 Sync Impact Report。以人工模板写入 `A01-project-charter.md`，不调用命令。 | 原命令会解析模板、覆盖 `.specify/memory/constitution.md`，允许保留未解决占位符，还可自动执行 mandatory pre/post hooks。完整 Spec Kit 会建立自己的目录和状态机。 |

**采用判断：** 只吸收 scope guard、版本决策和变更影响清单。项目治理日期或事实未知时必须提问，
不以占位符伪装完成。

## 5. M02 机会与市场调研

**Core（现有）：** `technical-research` + `product-discovery`，输出证据、反证、假设和未知项。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Supplement` | `github/spec-kit` assess research | 132,250★；MIT；活动 2026-08-28；[`speckit.assess.research.md`](https://github.com/github/spec-kit/blob/208d38695fc88d8eaec7855c96e5098a852927cf/extensions/assess/commands/speckit.assess.research.md) | 补充需求证据、先例、约束和「Evidence Against Idea」。把字段写入 `A02-opportunity-brief.md`，不调用 `/speckit.assess.*`。 | 原流程会抓取外部 URL，并写 `.specify/assessments/<slug>/research.md`。案头研究不能替代直接用户研究；搜索结果可能含 prompt injection。 |

**采用判断：** 将「支持证据、反方证据、来源、证据强度、仍属假设」设为必填字段。市场规模和
竞争结论没有第一方数据时保持未知，不用 stars 或搜索热度代替需求证据。

## 6. M03 用户研究与问题定义

**Core（现有）：** `product-discovery` 的一问一答、Fact/Decision/Assumption/Open question 和用户确认。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Supplement` | `addyosmani/agent-skills` `interview-me` | 90,851★；MIT；活动 2026-08-28；[`SKILL.md`](https://github.com/addyosmani/agent-skills/blob/c4ad44928cd535fcfee1972988f97309d4cebf9f/skills/interview-me/SKILL.md) | 借用 Outcome、User、Why now、Success、Constraint、Out of scope 的复述确认，以及一轮只问一个问题。显式请求访谈时触发。 | `0–100` confidence、`95%` 停止和预测用户后续回答属于伪精确，GUESS 容易形成诱导问题。整包规则由多位贡献者编写，证据密度不一致。 |
| `Niche` | `PostHog/skills` `planning-user-interviews` | 60★，明确标记 niche；MIT；活动 2026-08-29；[`SKILL.md`](https://github.com/PostHog/skills/blob/870cdf070c94f2bf39d8b2a9d4916cfd44779cce/skills/omnibus/planning-user-interviews/SKILL.md) | 仅在项目已经使用 PostHog User Interviews 时，参考 audience、topic、agent context、开放问题和样本确认。 | 会读取 cohort、person、email、distinct ID，创建访谈 topic，并把用户交给 voice agent。涉及 PII、抽样偏差和真实联系；必须逐次批准。硬编码 500 人、60 天、样本比例只适用于该产品流程。 |

**采用判断：** `interview-me` 只补结构，不采用 confidence 数字。PostHog 候选只能作为真实访谈
适配器；默认流程仍先产出招募标准和访谈提纲，不接触用户或 PII。

## 7. M04 产品策略与范围决策

**Core（现有）：** `product-discovery` + `safe-prototyping`，由明确证据决定继续、澄清或停止。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Alternative` | `github/spec-kit` assess shape + decide | 132,250★；MIT；活动 2026-08-28；[`shape`](https://github.com/github/spec-kit/blob/208d38695fc88d8eaec7855c96e5098a852927cf/extensions/assess/commands/speckit.assess.shape.md)、[`decide`](https://github.com/github/spec-kit/blob/208d38695fc88d8eaec7855c96e5098a852927cf/extensions/assess/commands/speckit.assess.decide.md) | 可选择性采用「最小可行、购买/不做、第三方案」「appetite 而非承诺工期」「go / needs-clarification / kill」和 risk posture。 | 原流程写 `concept.md`、`decision.md`，依赖 `.specify` 状态和先行产物。`small/medium/large` 仍是定性预算，不是估算证据；不能自动批准进入实现。 |

**采用判断：** 把三类 verdict 和「不做也是成功结论」写入 `A04-product-strategy.md`。任何 `go`
仍需产品负责人确认，不能由分数表自动决定。

## 8. M05 领域模型与产品规格

**Core（现有）：** `domain-modeling` + `specification` + `vertical-ticketing`。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Supplement` | `github/spec-kit` clarify + spec template | 132,250★；MIT；活动 2026-08-28；[`clarify.md`](https://github.com/github/spec-kit/blob/39f2ac3c63eb23f6f4ffb622acb26ddc01a641f4/templates/commands/clarify.md)、[`spec-template.md`](https://github.com/github/spec-kit/blob/756d63212987152564ed0a52ddfd7f8e9b504e09/templates/spec-template.md) | 补充 scope、domain/data、UX、NFR、依赖、edge cases、术语和完成信号的歧义检查；采用独立可测 user journey 和 GWT 验收格式。 | `clarify` 会即时回写 spec，并可执行 extension hooks；部分空白允许用 best-practice guess 补齐，可能把未知项伪装成事实。 |
| `Niche` | `NTCoding/living-architecture` `ddd` | 138★，明确标记 niche；Apache-2.0；活动 2026-08-29；[`SKILL.md`](https://github.com/NTCoding/living-architecture/blob/2060523fbad15582d726cdd83aaa0d50f0b1268e/.agents/skills/ddd/SKILL.md) | 参考 observations/interpretation/assumptions/decisions 分层、domain-expert test、多个模型方案和 abuse 场景。 | 强耦合生成的 domain guide、Contextive glossary、Rivière 角色和 400 行限制。本次有限候选集中未发现同时独立、通用、活跃且超过 1,000★ 的领域建模 Skill；这不是生态穷尽性结论，检索边界见 `report-source.md` 的「C010 有限候选检索记录」。 |

**采用判断：** 现有 `domain-modeling` 保持 Core。Spec Kit 仅提供覆盖表和规格格式；DDD 候选只
提供检查问题，不复制项目专属约定。

## 9. M06 原型与 UX 验证

**Core（现有）：** `safe-prototyping`。原型必须回答单一问题，并与生产数据和真实外部副作用隔离。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Supplement` | `anthropics/skills` `frontend-design` | 172,547★；该 Skill 为 Apache-2.0；活动 2026-08-21；[`SKILL.md`](https://github.com/anthropics/skills/blob/2235be7c60b551f5de82ade908fd3816455afcda/skills/frontend-design/SKILL.md) | 补充 audience、single job、视觉方向、signature、可访问性底线和截图复核。用于已确认 brief 后的原型实现。 | 会直接创建或重塑 UI；brief 不完整时可能自行确定主题。强调视觉差异化，但不提供用户任务成功率或可用性研究方法。仓库没有统一顶层许可证，必须按单 Skill 判断。 |
| `Supplement` | `vercel-labs/agent-skills` `web-design-guidelines` | 30,628★；README 声明 MIT；活动 2026-08-28；[`SKILL.md`](https://github.com/vercel-labs/agent-skills/blob/ba46938889d4e58635362fb8f618e1178ac3ec46/skills/web-design-guidelines/SKILL.md) | 用于实现后的 `file:line` UX、accessibility 和 interaction 审查。 | Skill 每次从 `main` 上的浮动 URL 拉取最新规则，无法仅靠固定 Skill commit 保证可复现。整包还含部署和网络副作用能力。 |
| `Adapter` | `nextlevelbuilder/ui-ux-pro-max-skill` | 123,080★；MIT；活动 2026-08-27；[`SKILL.md`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/8bd29e775453ebcae52b6e6514fbf134df0c5770/.claude/skills/ui-ux-pro-max/SKILL.md) | 项目需要本地可搜索的 style、palette、type、chart、UX 和 stack 规则时使用。只运行单域查询；持久化设计系统必须另行授权。 | 数据库规模和 stars 不证明建议适合具体用户。`--persist` 会写 `design-system/**`，`--force` 会覆盖；整包含多个设计、品牌、slides Skill 和脚本。部分阈值是启发式，必须再用真实测试验证。 |
| `Alternative` | `pbakaus/impeccable` | 63,902★；Apache-2.0；活动 2026-08-29；[`SKILL.md` v4.1.2](https://github.com/pbakaus/impeccable/blob/b0594c72d18006b5865c70eb3a97e8b04064e600/.agents/skills/impeccable/SKILL.md) | 当项目需要完整的 shape/init/document/critique/audit/polish/harden 路由时，可作为一套独立 UI 工作流。 | 会运行 `context.mjs`、写 `PRODUCT.md`/`DESIGN.md`、修改 UI、管理 hooks 并进行浏览器迭代。其「go all out」和广泛自动触发会扩大 scope；不能与其他 UI Skill 同时主导。 |

**采用判断：** 默认组合是 `safe-prototyping` + Anthropic 的视觉 brief + 固定版审查清单。UI UX
Pro Max 和 Impeccable 二选一，且仅在用户明确要求高强度 UI 工作时启用。

## 10. M07 架构设计与任务拆解

**Core（现有）：** `codebase-design` + `architecture-review` + `vertical-ticketing`。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Supplement` | `wshobson/agents` `architecture-patterns` | 39,256★；MIT；活动 2026-08-26；[`SKILL.md`](https://github.com/wshobson/agents/blob/be57c0b2e3c05c528ca6132b87410b385718775f/plugins/backend-development/skills/architecture-patterns/SKILL.md) | 已确认需要 Clean、Hexagonal 或 DDD 时，用作依赖方向和测试 seam 的参考。 | 倾向「每个边界都抽象接口」，会与现有 Skill 的 locality、deep module 和避免投机抽象原则冲突。整包包含大量语言、云和代理角色。 |
| `Niche` | `microsoft/skills` `cloud-solution-architect` | 2,972★；MIT；活动 2026-08-28；[`SKILL.md`](https://github.com/microsoft/skills/blob/277bb9865832cd182d28ca2300922ee4acdec406/.github/skills/cloud-solution-architect/SKILL.md) | 仅用于 Azure 项目的 WAF、ADR、架构风格和 cloud patterns 检查。 | Azure 产品偏向明显，部分可用性数字是通用模板而非本项目 SLO。不得把云服务目录当成架构需求。 |

**采用判断：** 外部模式只能解释已出现的约束，不能先选模式再寻找问题。任务仍按可独立验收的
vertical slice 拆分。

## 11. M08 全栈实现与 TDD

**Core（现有）：** `implementation-orchestration` + `tdd` + `systematic-debugging` +
`two-axis-code-review`。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Adapter` | `vercel-labs/agent-skills` `react-best-practices` | 30,628★；README 声明 MIT；活动 2026-08-28；[`SKILL.md`](https://github.com/vercel-labs/agent-skills/blob/805687f34e8c10b420e3d11335a0ca2c3c90d992/skills/react-best-practices/SKILL.md) | React/Next.js 项目补充 waterfall、bundle、SSR/client boundary、rerender 和 Server Action auth。 | 框架与版本专用，规则会随 React/Next.js 演进；整包含其他框架和部署 Skill。 |
| `Supplement` | `addyosmani/agent-skills` `api-and-interface-design` | 90,851★；MIT；活动 2026-08-28；[`SKILL.md`](https://github.com/addyosmani/agent-skills/blob/ce89b03cbd768d4c9f512beedae46c20822a6bf6/skills/api-and-interface-design/SKILL.md) | API 专项补充 contract-first、错误语义、兼容演化和幂等键、请求哈希、原子约束及 unknown outcome。 | TypeScript/REST 偏向；`always paginate` 等表述不能脱离规模和协议套用。多数规则没有逐条标准引用。 |
| `Adapter` | `supabase/agent-skills` `supabase-postgres-best-practices` | 2,561★；MIT；活动 2026-08-12；[`SKILL.md`](https://github.com/supabase/agent-skills/blob/32912161e2732c3e5001c6811a76c1f8308ed0da/skills/supabase-postgres-best-practices/SKILL.md) | PostgreSQL/Supabase 项目补充 query、connection、RLS、schema、lock 和 diagnostics。 | 整包可调用 Supabase CLI/MCP 并写真实数据库。migration、DDL、RLS 和数据修复必须有回滚和独立审批。 |
| `Supplement` | `obra/superpowers` `test-driven-development` | 279,511★；MIT；活动 2026-08-29；[`SKILL.md`](https://github.com/obra/superpowers/blob/b9e75dddec7a384f42ce08532ec17bb1ef5d9459/skills/test-driven-development/SKILL.md) | 只借用先见证失败、最小通过和 anti-rationalization。 | 要求删除先写的生产代码，若未确认所有权会破坏用户变更；完整插件还会写设计文档、commit、worktree 和触发遥测。现有 `tdd` 更适合本项目。 |
| `Supplement` | `obra/superpowers` `systematic-debugging` | 279,511★；MIT；活动 2026-08-29；[`SKILL.md`](https://github.com/obra/superpowers/blob/c74782ead66b8ded584d9b9cf64dcba95457f320/skills/systematic-debugging/SKILL.md) | 借用边界 instrumentation 和 reference comparison。 | 「所有技术问题都必须触发」过宽；完整插件副作用与本项目授权边界冲突。现有 `systematic-debugging` 保持 Core。 |
| `Supplement` | `addyosmani/agent-skills` `code-review-and-quality` | 90,851★；MIT；活动 2026-08-28；[`SKILL.md`](https://github.com/addyosmani/agent-skills/blob/91d4d07522de9577caf5d213e5bf1acc38fa3df2/skills/code-review-and-quality/SKILL.md) | correctness、readability、architecture、security、performance 可纳入现有 review 的 Standards 轴。 | 约 100/300/1,000 行等阈值是启发式；不能合并掉独立 Spec 轴，也不能替代逐行证据。 |
| `Alternative` | `The-PR-Agent/pr-agent` | 12,764★；MIT；活动 2026-08-30；[`review.md`](https://github.com/The-PR-Agent/pr-agent/blob/3ac78d979e2b5ebc38e731333bdf082899a11ab0/docs/docs/tools/review.md) | 已批准的远端 PR 可用 `/review` 或 GitHub Action 生成辅助意见。 | 会把代码发送给模型，并写 PR 评论、labels 或 merge checks；示例使用浮动 `@main`。模型意见不能成为唯一 merge gate。不得替代本地双轴审查。 |
| `Adapter` | `anthropics/skills` `webapp-testing` | 172,547★；该 Skill 为 Apache-2.0；活动 2026-08-21；[`SKILL.md`](https://github.com/anthropics/skills/blob/3b3fad96af16a10759d930941b4520ba0c40edae/skills/webapp-testing/SKILL.md) | 本地 Web 应用 smoke/E2E：管理本地 server、编写 Python Playwright 脚本、先侦察 DOM 再操作。 | 会启动项目服务、执行页面 JavaScript、写测试脚本和截图；固定 `networkidle` 不适用于持续连接页面。只能针对本地或明确批准的测试环境。 |
| `Adapter` | `microsoft/playwright-cli` `playwright-cli` | 12,957★；Apache-2.0；活动 2026-08-27；[`SKILL.md`](https://github.com/microsoft/playwright-cli/blob/cbc09311c468e10fba47964e9b3830fe625c9b01/skills/playwright-cli/SKILL.md) | 需要低上下文开销、可复现 browser action 和 snapshot 时优先于 MCP；显式调用 CLI。 | 能上传文件、保存认证状态、读写 cookies/storage、连接真实 Chrome、执行 `run-code` 并操作真实网站。必须使用测试账号、限定域名并禁止未批准的提交/购买/发送。整包 CLI 权限过宽。 |

**采用判断：** TDD、debug 和 review 继续使用本地 Core。框架、数据库、浏览器和 PR automation
全部是条件适配器；执行前检查依赖是否已存在，不通过候选自动安装依赖。

## 12. M09 AI Eval、质量与安全

**Core（现有）：** 规格验收、TDD、双轴审查、人工安全边界和 `A09-quality-evidence.md`。目标仓库
缺少完整 AI eval、供应链扫描和 Web 质量工具，因此本模块的外部补充最多。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Adapter` | `promptfoo/promptfoo` `promptfoo-evals` | 24,672★；MIT；活动 2026-08-30；[`SKILL.md`](https://github.com/promptfoo/promptfoo/blob/c5e4097042458801977688ead2372b3c14963afb/plugins/promptfoo/skills/promptfoo-evals/SKILL.md) | 设计一个产品问题、3–10 个 starter cases、deterministic assertions 优先、固定 grader，并以 `--no-cache --no-share` 运行。OpenAI Cookbook 的[迁移说明](https://github.com/openai/openai-cookbook/blob/5a49d2a28a2779b1928d9cee988510e85e014910/examples/evaluation/moving-from-openai-evals-to-promptfoo.md)提供第二一方来源。 | 原 Skill 使用 `npx promptfoo@latest`，会写 eval 配置并调用付费 provider；red-team 会主动访问 endpoint。必须固定版本、脱敏数据、设置费用上限，并分开批准「设计」与「真实运行」。 |
| `Niche` | `wshobson/agents` `rag-implementation` | 39,256★；MIT；活动 2026-08-26；[`SKILL.md`](https://github.com/wshobson/agents/blob/511f8345cf42f84676e0ad56ddfdee33c90a666f/plugins/llm-application-dev/skills/rag-implementation/SKILL.md) | RAG 技术栈已确认后，参考 dense/sparse/hybrid、reranking 和基本检索管线。 | 示例强耦合 LangGraph、Anthropic、Voyage、Pinecone，依赖 API keys 和外部付费调用；模型表会过时，且没有完整数据治理和 eval 闭环。 |
| `Supplement` | `trailofbits/skills` `supply-chain-risk-auditor` | 6,911★；CC-BY-SA-4.0；活动 2026-08-28；[`SKILL.md`](https://github.com/trailofbits/skills/blob/d1f1575cff97816e5cc08af66cd2506099c681d3/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SKILL.md) | 借用「脚本测量、模型只做判断」「unassessable 不是风险，也不是 clean」和 coverage table。适用于 npm、PyPI、Go manifest/lockfile。 | 会运行 `uv` 脚本、访问 GitHub/registry/advisory 服务并写报告；不支持 yarn、pnpm、poetry 等部分 lockfile，也不扫描自身源码。CC-BY-SA 内容不能无归属复制。 |
| `Supplement` | `trailofbits/skills` `agentic-actions-auditor` | 同仓库 6,911★；CC-BY-SA-4.0；[`SKILL.md`](https://github.com/trailofbits/skills/blob/d1f1575cff97816e5cc08af66cd2506099c681d3/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SKILL.md) | 审查 GitHub Actions 中 AI agent 的 attacker-controlled input、env intermediary、危险 sandbox、wildcard allowlist 和跨文件 action。 | 只覆盖 GitHub Actions 和已知 agent actions，是静态检查，不做运行时攻击验证。远端 YAML 必须作为不可信数据读取，不能执行。 |
| `Adapter` | `aquasecurity/trivy` | 37,693★；Apache-2.0；活动 2026-08-28；[README](https://github.com/aquasecurity/trivy/blob/5ae0bb10645f08e6ec81fc257d4dc7e51c15ba69/README.md) | 项目已有 Trivy 时，扫描 image/filesystem/repo/Kubernetes 的 CVE、misconfiguration、secret、license 和 SBOM，并保存结构化报告。 | 可能下载漏洞数据库、访问 registry/Kubernetes、读取 secret-like 内容并产生 cache/SARIF；结果受数据库时间影响且可能误报。不能把「无 finding」写成「安全」。不自动安装或扫描生产集群。 |
| `Adapter` | `GoogleChrome/lighthouse` | 30,709★；Apache-2.0；活动 2026-08-28；[`readme.md`](https://github.com/GoogleChrome/lighthouse/blob/f9cbf2bbdde9d10dd097304357974fd4c8e0f197/readme.md) | 在固定 Chrome、throttling、URL 和多次运行条件下采集 performance、accessibility、best-practices、SEO 的实验室证据。 | 结果受硬件、网络、缓存和页面状态影响；会启动浏览器并写 HTML/JSON/trace。Online Viewer 的 share 会创建 secret Gist。单次分数不能作为发布真值。 |
| `Adapter` | `dequelabs/axe-core` | 7,455★；MPL-2.0；活动 2026-08-28；[README](https://github.com/dequelabs/axe-core/blob/d50cdf6ea7c6f4cff426b6f3da7850b8c0b32eb6/README.md) | 集成到单元、集成或 Playwright 测试，检查 WCAG 规则和常见 ARIA 问题。 | 官方 README 明确平均只能自动发现约 57% 的 WCAG 问题，并会返回需要人工检查的 incomplete。不得据此声明完整合规；复制修改 MPL 文件需保留文件级许可。 |

**采用判断：** 默认质量证据是「需求验收 + 测试 + review」。Promptfoo、Trivy、Lighthouse、axe
只有在项目已有依赖或获得安装批准时运行；每种工具必须保存版本、输入范围、环境和未覆盖项。

## 13. M10 发布与上线

**Core（现有）：** `A10-release-readiness.md`、G5 上线与生产门、回滚方案和人工确认。目标仓库没有完整
发布自动化 Skill。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Adapter` | `actions/starter-workflows` | 11,998★；仓库 API 为 `NOASSERTION`，固定 [`LICENSE`](https://github.com/actions/starter-workflows/blob/e3c451d60f119b71caebf13c98ac45da6e15b4b7/LICENSE) 为 MIT；活动 2026-08-03；[README](https://github.com/actions/starter-workflows/blob/e3c451d60f119b71caebf13c98ac45da6e15b4b7/README.md) | 仅用作 GitHub Actions CI、deployment、code-scanning 模板起点；复制后按项目收紧 permissions、events、environment 和 action SHA。 | 仓库当前不接受一般贡献，只承诺安全和重大破坏修复。模板不是项目安全审计；浮动 action refs、`pull_request_target`、write token 或 deploy secret 都需重新审查。 |
| `Adapter` | `googleapis/release-please` | 7,418★；Apache-2.0；活动 2026-08-24；[README](https://github.com/googleapis/release-please/blob/05c6a4f71022304d4edad24ea90c1c16324503d5/README.md) | 项目采用 Conventional Commits 且希望通过 release PR 管理 changelog、版本、tag 和 GitHub Release 时启用。 | 会创建/更新 PR、写 changelog/版本文件、打 tag、创建 GitHub Release。它不发布包，也不处理复杂分支。merge release PR 是不可隐含的发布批准。整包配置可能改变版本策略。 |

**采用判断：** starter workflow 只生成草案；release-please 只管理 release PR。部署、包发布、数据库
变更和流量切换仍分别经过审批，不能把 workflow 成功等同于上线成功。

## 14. M11 可观测性与反馈闭环

**Core（现有）：** 先定义用户可见 SLI、日志/指标/trace 关联键、告警责任人和只读诊断流程，再选平台。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Adapter` | `grafana/mcp-grafana` | 3,402★；Apache-2.0；活动 2026-08-30；[README](https://github.com/grafana/mcp-grafana/blob/dcca5f171e760770b9c57107c39484b3c4a5b813/README.md) | 已有 Grafana 时，默认只暴露查询 dashboard、Prometheus、Loki 和 alert 状态的最小工具集；先用 summary/property，避免加载完整 dashboard。 | 服务器还包含 dashboard、alert、incident、annotation、snapshot、evaluator 等写工具，部分数据源查询可读取敏感日志或昂贵数据。必须 `--disable-write`/tool allowlist 和最小 service-account token。整包工具 schema 会占用大量上下文。 |
| `Niche` | `getsentry/sentry-mcp` | 834★，明确标记 niche；FSL-1.1-Apache-2.0 Future；活动 2026-08-28；[README](https://github.com/getsentry/sentry-mcp/blob/77c8b1a89538266ef0d04f7e0a4ed07c954c9899/README.md)、[LICENSE](https://github.com/getsentry/sentry-mcp/blob/77c8b1a89538266ef0d04f7e0a4ed07c954c9899/LICENSE.md) | 已有 Sentry 时，用于 human-in-the-loop 的 issue、trace、performance 查询和调试。只启用 inspect/triage 类工具。 | token 示例包含 project/team/event write scope；AI search 还会把查询交给 OpenAI、Azure、Anthropic 或 OpenRouter。事件可能含 PII、源码和用户输入。FSL 不是当前即刻的 Apache-2.0。不得整包启用 Seer 或写工具。 |
| `Niche` | `PagerDuty/pagerduty-mcp-server` | 77★，明确标记 niche；Apache-2.0；活动 2026-08-27；[README](https://github.com/PagerDuty/pagerduty-mcp-server/blob/74707cebf9db2232d148ad7c1367ad1247287df6/README.md)、[`write-tools.md`](https://github.com/PagerDuty/pagerduty-mcp-server/blob/74707cebf9db2232d148ad7c1367ad1247287df6/docs/configuration/write-tools.md) | 已有 PagerDuty 时默认 read-only，用于 incident investigation、on-call handoff 和 service health 查询。 | `--enable-write-tools` 可创建/修改 incident、service、team、schedule、status page 并启动 workflow，可能通知真实人员。必须保持默认只读；任何写工具逐项审批。 |
| `Adapter` | `PostHog/posthog` | 39,478★；`ee/` 之外 MIT；活动 2026-08-30；[README](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/README.md) | 已有 PostHog 时，关联 product analytics、session replay、error、logs、survey 和 AI observability，形成 `A11-production-learning.md`。 | 自动采集、session replay 和用户属性可能包含 PII；data pipeline/workflow 可向第三方发送数据；self-driving mode 会生成 PR。只启用已批准事件和只读查询，不执行 README 中的远端 `curl | bash` 部署。 |

**采用判断：** Grafana、Sentry、PagerDuty、PostHog 是互补平台，不是四选一 Skill。默认只读，先查再改；
远端写入、通知和自动修复分别需要批准。

## 15. M12 增长与实验

**Core（现有）：** `A12-experiment-decision.md` 的单一假设、主指标、guardrail、样本/窗口、停止规则和
人工决策。工具不能替代实验设计。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Adapter` | `PostHog/posthog` experiments + feature flags | 39,478★；`ee/` 之外 MIT；活动 2026-08-30；[README](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/README.md) | 项目已经正确埋点时，用 feature flags 分流，以 experiments 测量目标指标，并用 session replay/analytics 解释异常。 | 创建或修改 flag 会改变真实用户体验；自动采集事件不等于正确指标。实验、survey、workflow 和 CDP 可能处理 PII 或发送外部消息。 |
| `Adapter` | `growthbook/growthbook` | 8,174★；大部分 MIT，enterprise 目录使用 GrowthBook Enterprise License；活动 2026-08-30；[README](https://github.com/growthbook/growthbook/blob/de4ff6b5256c13764239f9ed3560e281c5728592/README.md)、[LICENSE](https://github.com/growthbook/growthbook/blob/de4ff6b5256c13764239f9ed3560e281c5728592/LICENSE) | 已有 warehouse metric 和 feature flag 基础时，使用其 targeting、gradual rollout、CUPED/Sequential/Bayesian/SRM 等能力。 | MCP 可创建 feature、启动 experiment 和清理 flag；错误分流会影响用户。统计方法丰富不等于设计正确，必须预先固定指标、样本单位、多重比较和停止规则。整包含 enterprise 代码和 24 个 SDK。 |

**采用判断：** PostHog 适合产品分析一体化，GrowthBook 适合 feature flag/experiment 专项。项目只选
已有平台；不为获得 Agent Skill 而引入新的数据平台。

## 16. M13 复盘与 Skill 自进化

**Core（现有）：** 失败、用户纠正或测试失败才产生候选经验；人工审核后才能修改正式 Skill。

| 等级 | 候选 | 固定证据与元数据 | 适用与启用方式 | 风险及不整包采用原因 |
|---|---|---|---|---|
| `Niche` | `microsoft/SkillOpt` / `skillopt-sleep` | 16,481★；MIT；活动 2026-08-29；[README](https://github.com/microsoft/SkillOpt/blob/db46cd9ae7ce12f1dbd73c945185816aa738751d/README.md)、[Codex `SKILL.md`](https://github.com/microsoft/SkillOpt/blob/db46cd9ae7ce12f1dbd73c945185816aa738751d/plugins/codex/skills/skillopt-sleep/SKILL.md) | 只有具备代表性 replay/held-out 数据、明确目标 Skill 和人工 adoption gate 时，试验 harvest → mine → replay → consolidate → gate → stage。首先只能用 mock dry-run。 | 会读取本地 session transcript，真实 backend 会把截断内容发给 provider；可改 Skill/`CLAUDE.md`、设置 schedule 和 `--auto-adopt`。README benchmark 是作者报告，不是本项目复现。不得启用自动 adoption。 |
| `Niche` | `PostHog/posthog` `improving-mcp-tools` | 同仓库 39,478★；该文件位于 MIT 区域；[`SKILL.md`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/mcp_analytics/skills/improving-mcp-tools/SKILL.md)、[eval harness](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/services/mcp/evals/README.md) | 适用于已有稳定 MCP benchmark 的团队：baseline、生产失败证据、一次一个 bounded fix、同版本复测、无回归后 draft PR。 | 强耦合 PostHog monorepo、live MCP、production analytics 和 PR labels；agent mode 需要 LLM judge。流程允许在显式开启后 auto-merge。仅借用控制论结构，不调用原 Skill。 |
| `Exclude` | PostHog Desktop autoresearch engine | 同仓库 39,478★；MIT 区域；[`flags.ts`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/desktop/packages/shared/src/flags.ts)、[`schemas.ts`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/desktop/packages/core/src/autoresearch/schemas.ts)、[`prompts.ts`](https://github.com/PostHog/posthog/blob/c6e2e5834bcf1cf3176c4f68356c7ce1bc967ee0/products/desktop/packages/core/src/autoresearch/prompts.ts) | 作为「单指标、单改动、测量报告、迭代上限、暂停/恢复」的实现参考。 | 第一方代码明确写着 `Staff-gated while it bakes`，最多 200 次迭代，可驱动代码修改和 PR，并依赖 PostHog Desktop 会话状态。尚不是通用、稳定 Skill，排除直接采用。 |

**采用判断：** M13 只采用「候选编辑 → held-out 验证 → staging → 人工 adoption」。会话原文不进入
长期记忆；没有可判定 oracle 时，不启动自动优化。

## 17. 横向排除项

| 等级 | 候选与固定证据 | 元数据 | 排除原因 |
|---|---|---|---|
| `Exclude` | `garrytan/gstack` 整包；[`design-review/SKILL.md`](https://github.com/garrytan/gstack/blob/07b59e396c6be5a86619a43151cb9ed62a15ae69/design-review/SKILL.md) | 130,381★；MIT；活动 2026-08-29 | 虽有高 stars，但 design review 会要求 clean git、允许 stash/commit、一次性构建 Bun browser，并写 `~/.gstack/analytics` 遥测。副作用边界与本项目冲突。 |
| `Exclude` | `sickn33/agentic-awesome-skills`；[README](https://github.com/sickn33/agentic-awesome-skills/blob/d91ed427d91596da3fcab6dd26ff3306c8003ce5/README.md)、[`LICENSE-CONTENT`](https://github.com/sickn33/agentic-awesome-skills/blob/d91ed427d91596da3fcab6dd26ff3306c8003ce5/LICENSE-CONTENT) | 45,682★；工具代码 MIT、原创非代码内容 CC-BY-4.0、第三方内容沿用上游许可证；活动 2026-08-30 | 聚合 2,000 余个 Skill 并保留多种上游内容，包含 mattpocock 和 Anthropic 镜像。适合发现候选，不是独立方法证据或第二一方来源；整包安装还有上下文和高风险 Skill 暴露问题。 |
| `Exclude` | `obra/superpowers` 整包；固定证据：[TDD `SKILL.md`](https://github.com/obra/superpowers/blob/b9e75dddec7a384f42ce08532ec17bb1ef5d9459/skills/test-driven-development/SKILL.md) | 279,511★；MIT；活动 2026-08-29 | 单个 TDD/debug 方法可参考；完整包自动触发范围过宽，并包含设计文档、commit、worktree 和遥测。 |
| `Exclude` | `github/spec-kit` 整包；固定证据：[assessment research](https://github.com/github/spec-kit/blob/208d38695fc88d8eaec7855c96e5098a852927cf/extensions/assess/commands/speckit.assess.research.md) | 132,250★；MIT；活动 2026-08-28 | 可参考 assessment/spec 模板；完整包建立 `.specify` 状态机、写多个产物、创建分支并执行 hooks。 |

所有 `@latest`、`@main` 或浮动 branch 安装示例均排除为固定执行依据。若未来获准启用，必须固定
release、package version、action SHA 和权限。

## 18. 推荐的最小组合

| 场景 | 默认组合 | 条件适配器 |
|---|---|---|
| 新 AI 产品从机会到规格 | `product-discovery` + `technical-research` + `domain-modeling` + `specification` + `vertical-ticketing` | Spec Kit 的 evidence/shape/decide/clarify 字段。 |
| Web MVP | `safe-prototyping` + `codebase-design` + `tdd` + `systematic-debugging` + `two-axis-code-review` | Anthropic frontend brief；固定 UI 审查规则；项目已用 React/PostgreSQL 时再加 Vercel/Supabase。 |
| AI/RAG 功能 | 上述 Web MVP + 明确 dataset、oracle 和安全边界 | Promptfoo；RAG 参考；已批准时运行 Trivy、Lighthouse、axe、Playwright。 |
| 发布与生产学习 | release readiness + 回滚 + SLI/alert + 人工发布门 | starter workflow、release-please、已有 Grafana/Sentry/PagerDuty/PostHog。 |
| 增长实验 | 单假设 + 预注册指标/guardrail/停止规则 + 人工结论 | 已有 PostHog 或 GrowthBook，二者不因本审计自动引入。 |
| Skill 改进 | 失败触发候选经验 + 独立测试集 + 人工审阅 | SkillOpt 仅做隔离试验；PostHog 方法只借鉴单指标 campaign。 |
