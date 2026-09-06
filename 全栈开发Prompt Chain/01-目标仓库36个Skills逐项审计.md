# 目标仓库 36 个 Skills 逐项审计

## 1. 审计边界

本文记录 `vinvcn/mattpocock-skills-zh-CN` 在固定 commit
[`9fe7e7a3bb352851b986725bab1c7cfb17610a97`](https://github.com/vinvcn/mattpocock-skills-zh-CN/commit/9fe7e7a3bb352851b986725bab1c7cfb17610a97)
中的事实。审计对象包括：

- 29 个公开稳定 Skill：18 个 `engineering`、7 个 `productivity`、4 个 `misc`。
- 6 个 `in-progress` Skill。它们是公开 beta，但不随 plugin 发布。
- 1 个仓库内部 Skill：`.skills/translate-skill`。

证据以固定 commit 的 `SKILL.md`、同目录 reference、script、config、README 和
plugin manifest 为准。本文没有安装或运行任何候选 Skill，没有调用真实 issue tracker、
修改 Git 历史、写入 secret、部署或操作生产系统，因此没有 E5 运行证据。

本文使用以下证据标记：

- **E1**：固定 commit 文件直接支持的事实。
- **E2**：README、GitHub API、PR 或维护者说明支持的事实。
- **E3**：对文件树、调用关系和上游差异的静态比较。
- **E4**：根据 E1–E3 作出的风险判断。

## 2. 仓库快照

| 项目 | 审计结果 | 证据 |
|---|---|---|
| 固定 commit | `9fe7e7a3bb352851b986725bab1c7cfb17610a97`，提交时间 2026-08-30 08:10:17 UTC | [commit](https://github.com/vinvcn/mattpocock-skills-zh-CN/commit/9fe7e7a3bb352851b986725bab1c7cfb17610a97) |
| 实际 Skill 数 | 36：29 stable + 6 in-progress + 1 internal | [固定 tree API](https://api.github.com/repos/vinvcn/mattpocock-skills-zh-CN/git/trees/9fe7e7a3bb352851b986725bab1c7cfb17610a97?recursive=1) |
| 公开索引 | README、公开目录和 `.claude-plugin/plugin.json` 的 29 项集合一致 | [README](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/README.md) · [plugin.json](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/.claude-plugin/plugin.json) |
| License | MIT；英文 `LICENSE` 是法律文本，`LICENSE.zh-CN.md` 明确标为非官方译本 | [LICENSE](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/LICENSE) |
| 生态快照 | 2026-08-30 采集时 GitHub API 为 3,800 stars、316 forks；stars 只表示关注度，不证明质量 | [repository API](https://api.github.com/repos/vinvcn/mattpocock-skills-zh-CN) |
| GitHub fork 状态 | API 的 `source` 和 `parent` 均为空；这是独立本地化仓库，不是 GitHub fork | [repository API](https://api.github.com/repos/vinvcn/mattpocock-skills-zh-CN) |

仓库有意保留英文目录名、Skill identifier 和 OpenAI `display_name`。下表中的中文名称是
审计释义，不是可调用 identifier。

## 3. 调用类型与副作用等级

| 标记 | 含义 |
|---|---|
| `U` | User-invoked。只有人类显式输入名称才能调用；frontmatter 有 `disable-model-invocation: true`，OpenAI policy 为 `allow_implicit_invocation: false`。 |
| `M` | Model-invoked。用户可以显式调用，模型也可以根据 `description` 自然触发。 |
| `Internal` | 仓库维护专用 Skill，不在公开 plugin inventory；其安装与 Codex UI discovery 未由仓库证明。 |
| `S0` | 只读分析或对话输出。 |
| `S1` | 写本地文档、报告、测试或临时 artifact。 |
| `S2` | 修改代码、依赖、配置、文件权限或本地 Git working tree。 |
| `S3` | commit、branch、rebase、真实 tracker、secret、外部消息、后台 agent、迁移或生产相关动作。 |

副作用等级描述 Skill 文本允许或要求的动作，不代表本次审计执行过这些动作。

## 4. 36/36 Inventory

| # | Identifier、英文名、中文释义、状态 | 功能与调用 | 输入 | 输出 | 直接依赖与关系 | 生命周期 | 直接副作用与风险 |
|---:|---|---|---|---|---|---|---|
| 1 | [`ask-matt`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/ask-matt/SKILL.md) · **Ask Matt** · 流程路由 · stable/`U` | 根据当前情境推荐 Skill 或 flow；显式调用。它只为人类提供路由，不直接触发其他 user-invoked Skill。 | 当前目标、工作目录状态、工作规模和阶段边界。 | 推荐的主链、on-ramp、standalone Skill 或 phase-boundary 动作。 | 读取 `PHASE-BOUNDARIES.md`；为其他 Skill 提供导航。 | 流程入口、阶段切换。 | `S0`。约 150k token 的 smart-zone 数字是启发式外链，不是仓库内 benchmark；复杂路由仍依赖用户继续调用。 |
| 2 | [`code-review`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/code-review/SKILL.md) · **Code Review** · 代码审查 · stable/`M` | 当用户要求 review branch、PR、进行中改动或 “review since X” 时，分别检查 Standards 与 Spec。 | 可解析且非空的 fixed point、HEAD diff、commit list、spec、repo standards。 | 两个并列报告及每轴 finding 数；没有 spec 时明确跳过 Spec 轴。 | Git；issue-tracker config；两个并行 sub-agent；是 `implement` 的收尾，也可独立使用。 | 质量审查、提交前检查。 | `S0`，但依赖 sub-agent。只报告、不自动修复；本地旧措辞可能让模型尝试调用只能由人运行的 setup。 |
| 3 | [`codebase-design`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/codebase-design/SKILL.md) · **Codebase Design** · 代码库设计 · stable/`M` | 在 module interface、deepening、seam、testability 或 AI navigation 设计问题上提供 deep-module 词汇和方法。 | 待设计的 module、现有 interface、dependencies、CONTEXT vocabulary。 | 设计判断；需要时由 3 个以上 sub-agent 提供不同 interface 方案。 | `DEEPENING.md`、`DESIGN-IT-TWICE.md`；被 `tdd`、`improve-codebase-architecture` 和 `setup-ts-deep-modules` 使用。 | 架构设计、重构设计。 | `S0`；设计结论属于判断，Design-It-Twice 有较高 token/agent 成本。两个 ASCII diagram code fence 与同步点上游不完全相同。 |
| 4 | [`diagnosing-bugs`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/diagnosing-bugs/SKILL.md) · **Diagnosing Bugs** · 缺陷诊断 · stable/`M` | 当用户说 diagnose/debug，或报告 broken、throwing、failing、slow 时，执行 feedback-loop-first 诊断。 | 用户精确症状、可运行环境、经脱敏的 logs/artifacts、代码与 ADR。 | red-capable command、最小复现、3–5 个可证伪假设、instrumentation、fix、regression test 和 post-mortem。 | 测试/CLI/browser/profiler；`scripts/hitl-loop.template.sh`；缺少正确 seam 时把后续建议交给 architecture improvement。 | Bug、flake、性能回退。 | `S2`；可能申请临时生产 instrumentation，必须另行批准。无 tight loop 时按 Skill 要求停止，不应继续猜测。 |
| 5 | [`domain-modeling`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/domain-modeling/SKILL.md) · **Domain Modeling** · 领域建模 · stable/`M` | 主动挑战术语、构造 edge-case scenario，并记录 glossary 和少量 ADR。 | 领域术语、代码事实、现有 `CONTEXT.md`/`CONTEXT-MAP.md`、相关 ADR。 | 内联更新或创建 CONTEXT 文档；满足三项门槛时创建 ADR。 | `CONTEXT-FORMAT.md`、`ADR-FORMAT.md`；被多项 grilling/architecture flow 调用。 | 需求澄清、领域设计、架构决策。 | `S1`。错误术语会被长期固化；必须由 domain expert 参与。两个 tree code fence 与上游同步点不完全相同。 |
| 6 | [`grill-with-docs`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/grill-with-docs/SKILL.md) · **Grill with Docs** · 带文档追问 · stable/`U` | 在 repo 中显式发起持续访谈，并同步构建 domain docs。 | 计划、设计、idea、working directory。 | 共享理解、更新后的 CONTEXT/ADR。 | 直接组合 `grilling` 与 `domain-modeling`；有 repo 时替代 stateless `grill-me`。 | 需求发现、设计澄清。 | `S1`。本体只有 wrapper，效果完全依赖两个 model-invoked primitive。 |
| 7 | [`implement`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/implement/SKILL.md) · **Implement** · 实现 · stable/`U` | 基于 spec 或 tickets 实现工作，在认可 seam 上尽可能执行 TDD，并在结束前 review。 | Spec 或 ticket、代码库、测试命令、当前 branch。 | 代码、tests、typecheck/test 结果、code-review 报告、commit。 | 直接组合 `tdd` 和 `code-review`；是主链实现器。 | 全栈实现。 | `S3`。SKILL 明确要求 commit，但没有 dirty-worktree、目标 branch 或 staged-files 安全门；调用不等于预先授权 commit。 |
| 8 | [`improve-codebase-architecture`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/improve-codebase-architecture/SKILL.md) · **Improve Codebase Architecture** · 改进代码库架构 · stable/`U` | 扫描 hot spot 和 architectural friction，形成 deepening candidates；用户选定后再 grilling。 | 指定 module/pain point，或 Git history、CONTEXT、ADR、codebase。 | OS temp 中的 HTML report、top recommendation、后续设计决策和可能的 CONTEXT/ADR 更新。 | `codebase-design`、`grilling`、`domain-modeling`、sub-agent、`HTML-REPORT.md`、Tailwind/Mermaid CDN。 | 架构维护、重构发现。 | `S1`。所谓 self-contained HTML 实际依赖 CDN；Mermaid 配置为 `securityLevel: "loose"`。本 Skill 只 survey，不负责实现。 |
| 9 | [`prototype`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/prototype/SKILL.md) · **Prototype** · 原型验证 · stable/`M` | 在 state/logic 或 UI 需要可运行答案时构建 throwaway prototype。 | 明确设计问题、周围代码、domain language；UI 分支还需要 router 和 component system。 | Logic：单一 HTML；UI：3–5 个可切换 variants；决策折入真实代码，完整 prototype 留在非 main branch。 | `LOGIC.md`、`UI.md`；主链中可用 `handoff` 跨目录桥接。 | 方案验证、UX 验证。 | `S3`。明确不写 tests、少 error handling；UI 分支会触碰真实 route；prototype branch/issue pointer 都需要审批。Engineering README 错称 logic 产物为 terminal app。 |
| 10 | [`research`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/research/SKILL.md) · **Research** · 调研 · stable/`M` | 当用户要求调研 topic、docs/API facts 或委托后台阅读时，使用一手来源收集事实。 | 研究问题、source scope、repo notes convention。 | Background agent 在 repo 中写带 claim-level source 的 Markdown findings。 | Background agent、official docs/source/spec/API；产物供 `grill-with-docs` 或 wayfinder ticket 使用。 | 技术调研、决策输入。 | `S1`，若启动后台 agent 则为 `S3`。SKILL 没有范围、反证、停止条件、引用格式或 artifact QA 细则。 |
| 11 | [`resolving-merge-conflicts`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/resolving-merge-conflicts/SKILL.md) · **Resolving Merge Conflicts** · 解决合并冲突 · stable/`M` | 在已经进行的 merge/rebase 中，根据双方 primary source intent 逐 hunk 解决冲突。 | 当前 merge/rebase 状态、conflicted files、commits、PR/issues、项目 checks。 | 已解决并 staged 的 files、checks、完成的 merge commit 或继续完成的 rebase。 | Git、历史与 issue/PR primary sources；standalone。 | 集成、合并。 | `S3`。明令不使用 `--abort` 并要求完成操作；当 intent 无法确认时没有明确停止门。 |
| 12 | [`setup-matt-pocock-skills`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/setup-matt-pocock-skills/SKILL.md) · **Setup Matt Pocock Skills** · 配置 Skills · stable/`U` | 每个 repo 一次，记录 issue tracker、triage labels 和 domain-doc layout。 | Repo remote、现有 AGENTS/CLAUDE/CONTEXT/docs、tracker 选择、用户确认。 | 更新一个 agent-instructions file；写 `docs/agents/issue-tracker.md`、`domain.md` 和可选 `triage-labels.md`。 | GitHub/GitLab/local/domain/labels 五个 seed templates；是 tracker/domain hard dependency 的前置。 | 项目初始化、治理。 | `S2`。只写 label 映射，不创建或验证真实 labels，也不验证 `gh`/`glab` auth。README 称原生支持 GitHub/Linear/local，实际原生模板是 GitHub/GitLab/local，Linear 属于 Other freeform。 |
| 13 | [`tdd`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/tdd/SKILL.md) · **TDD** · 测试驱动开发 · stable/`M` | 当用户要求 test-first、red-green-refactor、integration tests 或修复行为时，按 vertical slice 执行 red→green。 | 待实现行为、用户认可的 public seams、代码与 test runner。 | 每轮一个 failing test、minimal implementation 和通过信号。 | `tests.md`、`mocking.md`；interface 形状不清时使用 `codebase-design`；由 `implement` 组合。 | 实现、回归修复。 | `S2`。README 和 OpenAI metadata 写 red-green-refactor，但 SKILL 明确把 refactor 排除出 loop；`code-review` 又只报告、不执行重构。 |
| 14 | [`to-spec`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/to-spec/SKILL.md) · **To Spec** · 转成规格 · stable/`U` | 把当前 conversation 和 codebase understanding 综合成 spec；不重新访谈主题。 | 完整会话、codebase、CONTEXT/ADR、已确认 seams、tracker config。 | 发布到 tracker 的 spec，并应用 `ready-for-agent` role。 | setup 产物；主链中位于 grilling/wayfinder 后、`to-tickets` 前。 | 产品规格、技术规格。 | `S3`。虽然写“不访谈”，仍要求用户确认 seams；setup 不保证 label 已存在；发布真实 issue 必须审批。 |
| 15 | [`to-tickets`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/to-tickets/SKILL.md) · **To Tickets** · 拆成工单 · stable/`U` | 把 plan/spec/conversation 拆成 tracer-bullet vertical slices 和 blocking edges。 | 完整 reference、代码库、tracker config、用户批准的 granularity/edges。 | 多个 tracker issues，或 `.scratch/<feature>/issues/*.md`；每项有 acceptance criteria 和 blockers。 | setup tracker docs；后续每 ticket 进入 `implement`。 | 任务拆解、执行计划。 | `S3`。没有幂等、duplicate issue 检查或批量回滚；native blocker 能力随平台/tier 变化。 |
| 16 | [`triage`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/triage/SKILL.md) · **Triage** · Issue 分诊 · stable/`U` | 让 issue/外部 PR 通过 category + state role 状态机，并在需要时验证、grill 和写 agent brief。 | 自然语言 triage 请求、完整 issue/PR、labels、代码、tests、CONTEXT/ADR、out-of-scope KB。 | 查询摘要、role 变更、AI disclaimer comment、agent brief、close、可能的 `.out-of-scope` 文件。 | `AGENT-BRIEF.md`、`OUT-OF-SCOPE.md`、setup config、`grilling`、`domain-modeling`。 | 请求入口、backlog 治理。 | `S3`。可 checkout PR、改 label、comment 和 close；quick override 可跳过验证；需要先处理 dirty workspace 和外部审批。 |
| 17 | [`wayfinder`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/wayfinder/SKILL.md) · **Wayfinder** · 大型工作路径规划 · stable/`U` | 为单 session 装不下的模糊 effort 创建 decision-ticket map，并逐项消除 fog。 | Destination、tracker config、map/child tickets、CONTEXT/ADR、用户决策。 | Map issue/file、child tickets、blocking edges、claim、resolution、research branches；默认每 session 最多处理一个非 research ticket。 | setup tracker docs；按 ticket 类型组合 `research`、`prototype`、`grilling`、`domain-modeling`。 | 大型规划、多会话决策。 | `S3`。外部状态面大，并发 session 有竞态；setup 不创建 `wayfinder:*` labels；同段既要求缺配置时运行 setup，又写缺 tracker 时默认 local。 |
| 18 | [`wizard`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/engineering/wizard/SKILL.md) · **Wizard** · 人工流程向导 · stable/`M` | 当流程只能由人完成时，生成分阶段 bash wizard；普通 agent 可执行步骤不应触发。 | Repo env/CI/config、手动 journey、URL、每个值的来源/去向、secret 分类。 | Executable script；可能打开 URL、写 `.env`、写 GitHub secrets/variables；可临时删除或 commit。 | `template.sh`、bash、browser、`gh`、可选 shellcheck。 | Provisioning、release、migration/cutover。 | `S3`，涉及 secret 或生产时必须进入更高审批门。静态 tracing 不能证明第三方 UI 或不可逆操作可成功恢复。 |
| 19 | [`grill-me`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/productivity/grill-me/SKILL.md) · **Grill Me** · 追问我 · stable/`U` | 对没有 repo 承载的 plan/design/idea 发起 stateless 持续访谈。 | 计划、设计或 idea。 | 共享理解；不写本地 domain docs。 | 直接调用 `grilling`；是 `grill-with-docs` 的无工作目录替代。 | 需求发现、通用决策。 | `S0`。本体是极薄 wrapper，完成标准完全来自 `grilling`。 |
| 20 | [`grilling`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/productivity/grilling/SKILL.md) · **Grilling** · 持续追问 · stable/`M` | 当用户要求 stress-test idea 或使用 grill 措辞时，把 decisions 映射为 design tree，并按 frontier 分 rounds 提问。 | Idea、已有 facts、用户 decisions、可读取环境。 | 每轮编号问题和推荐答案；用户确认共享理解前不行动。 | 可派 sub-agent 查 facts；是多个 user-invoked flow 的共享 primitive。 | 发现、决策、澄清。 | `S0`。没有轮数上限，一轮可能包含多个问题；与 `loop-me` 的“一次一个问题”冲突。示例 code fence 被翻译，违反本地翻译规则。 |
| 21 | [`handoff`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/productivity/handoff/SKILL.md) · **Handoff** · 交接 · stable/`U` | 把当前 conversation 压缩成可移植 handoff document。 | 当前会话、可选的下一 session focus、已存在 artifacts。 | OS temp 目录中的脱敏 Markdown，包含 suggested skills 和 artifacts pointers。 | 用于跨 harness、directory、colleague 或阶段中途 side task。 | 阶段交接、上下文治理。 | `S1`。Temp 生命周期和命名未规定；脱敏完整性依赖模型判断。 |
| 22 | [`teach`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/productivity/teach/SKILL.md) · **Teach** · 教学工作区 · stable/`U` | 把当前目录作为跨 session 的 stateful teaching workspace。 | Topic、MISSION、学习记录、resources、用户偏好。 | MISSION/RESOURCES/NOTES、HTML lessons/reference/assets、learning records。 | 四个 format docs、高可信外部资料、browser、可复用 HTML components。 | 教学、知识管理，非软件产品主链。 | `S1`。在代码 repo 调用会写入大量文件；学习记录有隐私面；没有 visual QA。Bundled `GLOSSARY-FORMAT.md` 未被 workspace 清单直接链接。 |
| 23 | [`to-questionnaire`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/productivity/to-questionnaire/SKILL.md) · **To Questionnaire** · 转成问卷 · stable/`U` | 把用户无法独自回答的 decision 转成给特定 recipient 的 discovery questionnaire。 | Recipient role/expertise/relationship，以及用户需要取回的 facts/decisions。 | 当前目录中的 `to-questionnaire-<slug>.md`。 | 返回内容可进入 `grill-with-docs` 或 `to-spec`；不负责发送。 | 外部专家输入、异步发现。 | `S1`。模板要求 deadline 和预计耗时，但访谈步骤未明确采集；可能写入人员身份信息。 |
| 24 | [`wait-what`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/productivity/wait-what/SKILL.md) · **Wait What** · 重新解释 · stable/`U` | 对上一条未讲清楚的消息补充 context，并用受控英语和项目词汇重述。 | 上一条消息、`CONTEXT.md`。 | 更易理解的重述。 | 可在任何其他 flow 中作为事后纠正。 | 沟通修复。 | `S0`。中文版仍要求 ASD-STE100 Simplified Technical English；本地版不读取 `CONTEXT-MAP.md`，上游后续已修正。 |
| 25 | [`writing-for-agents`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/productivity/writing-for-agents/SKILL.md) · **Writing for Agents** · 为 Agent 写文档 · stable/`M` | 当用户创建/编辑 Skill、AGENTS.md、CLAUDE.md 或 pointer docs 时，提供 agent-facing 写作方法。 | 目标文档、目标读者、context/cognitive load、项目约定。 | 关于 pointer、information hierarchy、completion criterion、leading words 和 pruning 的文档或建议。 | 写 Skill 时读取 `SKILL-MECHANICS.md`；是共享 reference。 | Agent 治理、文档维护。 | 通常 `S0`，实际编辑时 `S1`。方法具有规范性，仍需项目级验证，不能替代目标仓库契约。 |
| 26 | [`git-guardrails-claude-code`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/misc/git-guardrails-claude-code/SKILL.md) · **Git Guardrails for Claude Code** · Git 护栏 · stable/`M` | 当用户要求在 Claude Code 阻止危险 Git command 时，安装 PreToolUse hook。 | Project/global scope、settings、blocked patterns。 | Hook script、settings merge、chmod、一次模拟验证。 | Claude Code hooks、bash、`jq`、bundled script。 | 项目治理、Claude 专项。 | `S2`。Regex 只查 command string，可能漏掉 `git -c ... push`、长参数、alias 等变体，也可能误报 quoted text；global scope 影响所有项目。 |
| 27 | [`migrate-to-shoehorn`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/misc/migrate-to-shoehorn/SKILL.md) · **Migrate to Shoehorn** · 迁移测试断言 · stable/`M` | 在测试代码中把 `as` assertion 迁移为 `@total-typescript/shoehorn`。 | 目标 test files、partial/wrong-shape data 需求。 | 新 dependency、imports、`fromPartial`/`fromAny` 替换、typecheck。 | npm、TypeScript、目标 test suite。 | 测试维护、专项迁移。 | `S2`。安装命令固定为 npm；搜索 pattern 较窄；只要求 typecheck，不要求 test；`fromAny` 仍绕过类型安全。 |
| 28 | [`scaffold-exercises`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/misc/scaffold-exercises/SKILL.md) · **Scaffold Exercises** · 搭建课程练习 · stable/`M` | 根据课程 plan 创建 section/exercise/variant 目录并通过专用 linter。 | Section、exercise、variant plan。 | 目录、stub `readme.md`、lint 结果、commit。 | `pnpm ai-hero-cli internal lint`、Git。 | 课程内容生产，非通用产品主链。 | `S3`。高度项目专属却允许自然触发；默认 placeholder 内容；自动 commit 前没有 working-tree 安全门。 |
| 29 | [`setup-pre-commit`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/misc/setup-pre-commit/SKILL.md) · **Setup Pre-Commit** · 配置提交前检查 · stable/`M` | 为 JavaScript/TypeScript repo 安装 Husky、lint-staged、Prettier、typecheck 和 tests。 | Lockfile、package scripts、已有 hooks/config。 | Dependencies、`.husky/pre-commit`、lint-staged/Prettier config、verify、commit。 | Package manager、Husky v9+、项目 scripts。 | 项目初始化、质量治理。 | `S3`。可能覆盖既有 hook 意图并引发格式化 diff；非 npm 项目仍使用 `npx`；明确 stage 所有改动并 commit，可能夹带用户文件。 |
| 30 | [`claude-handoff`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/in-progress/claude-handoff/SKILL.md) · **Claude Handoff** · Claude 后台交接 · in-progress/`U` | 把当前会话总结直接作为 prompt 启动新的 Claude background agent。 | Conversation、可选 focus、现有 artifacts。 | `claude --bg --name ...` 后台任务；不保存 handoff file。 | 支持 `--bg` 的 Claude CLI。 | 上下文交接、Claude 专项。 | `S3`。立即在当前 cwd 启动 agent；无隔离或二次确认；prompt 脱敏依赖模型。 |
| 31 | [`loop-me`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/in-progress/loop-me/SKILL.md) · **Loop Me** · 工作流访谈 · in-progress/`U` | 从用户生活/工作 loops 中持续访谈出 implementable workflow specs。 | Workflow idea，或允许 Skill 查找 loop；用户工具、channels、术语。 | 持续创建、编辑或删除 `workflows/*.md` 和 `NOTES.md`。 | `grilling`。 | 工作流设计，非默认产品主链。 | `S1`。要求“一次一个问题”，与 grilling 的整轮 frontier 冲突；同时要求边问边改文件，而 grilling 要确认理解后才行动。 |
| 32 | [`setup-ts-deep-modules`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/in-progress/setup-ts-deep-modules/SKILL.md) · **Setup TS Deep Modules** · TypeScript 深模块配置 · in-progress/`U` | 用 dependency-cruiser 强制 package 只能通过 root entry points 暴露 interface。 | TypeScript repo、package manager、packages root、既有 config。 | Dependency、config/scripts、example package、tests/docs、pass→fail→pass 证据、commit。 | `codebase-design`、bundled `dependency-cruiser.config.cjs`、test runner。 | TypeScript 架构治理。 | `S3`。Root heuristic 可能选错；自动增加示例和 commit；SKILL 多次称“四条 rules”，config 实际有五个 forbidden entries。 |
| 33 | [`writing-beats`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/in-progress/writing-beats/SKILL.md) · **Writing Beats** · 节拍式写作 · in-progress/`U` | 从固定 raw pile 提供 2–3 个可达 beats，用户每次选择一个，逐步形成文章。 | Raw-material Markdown、audience prerequisites、article path。 | 逐 beat 追加的文章，以及 grounded-concepts 状态。 | 通常承接 `writing-fragments`；与 `writing-shape` 是 exploit 阶段替代方案。 | 内容创作，非产品开发主链。 | `S1`。完成标准只有“自然结束”；没有事实或引用验证；多轮写入需持续保护用户编辑。 |
| 34 | [`writing-fragments`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/in-progress/writing-fragments/SKILL.md) · **Writing Fragments** · 写作碎片采集 · in-progress/`U` | 以 explore 模式访谈，不施加 outline，把异质 fragments 追加到一个 Markdown。 | 主题、保存路径、用户原话和后续 fragments。 | 单一 raw-material file，允许 append、rewrite、merge、cut。 | 后续交给 `writing-beats` 或 `writing-shape`。 | 内容探索，非产品开发主链。 | `S1`。从 initial prompt 开始捕获，可能保存隐私；不验证事实或来源。 |
| 35 | [`writing-shape`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/skills/in-progress/writing-shape/SKILL.md) · **Writing Shape** · 逐块塑造文章 · in-progress/`U` | 完整读取只读 raw pile，选择 opening 后逐 paragraph/block 讨论结构和格式。 | Raw-material Markdown、audience prerequisites、article path。 | 独立 article，按用户认可的 block 逐次追加。 | 通常承接 `writing-fragments`；与 `writing-beats` 替代。 | 内容成稿，非产品开发主链。 | `S1`。由用户决定何时完成；pile 缺材料时只报告 gap；不负责来源验证、发布或平台格式。 |
| 36 | [`translate-skill`](https://github.com/vinvcn/mattpocock-skills-zh-CN/blob/9fe7e7a3bb352851b986725bab1c7cfb17610a97/.skills/translate-skill/SKILL.md) · **Translate Skill** · 上游翻译刷新 · internal/`Internal` | 从 `mattpocock/skills` 翻译、刷新或复核内容，同时保护 identifiers、commands、paths 和 URLs。 | 固定 upstream、changed/new/removed files、本地 localization policy。 | Translation patch、changed/copied/removed/review flags、sync log 和验证摘要。 | `check-translation.mjs`、`audit-english.mjs`、tree/index/diff 检查。 | 仓库维护，不属于产品开发流程。 | `S2`。没有旁置 `agents/openai.yaml`；README 当前没有本 Skill 要求的 sync log。四个共同 SKILL 的 fenced code block 与同步点不完全一致，说明自动检查不足以证明全部保真 invariant。 |

## 5. 高副作用 Skill 汇总

以下分类是安全路由依据，不是执行授权：

| 副作用 | 相关 Skill | 必须在执行前确认的对象 |
|---|---|---|
| 自动 commit、merge、rebase 或 branch | `implement`、`resolving-merge-conflicts`、`prototype`、`scaffold-exercises`、`setup-pre-commit`、`setup-ts-deep-modules`、部分 `wayfinder`/`research` flow | branch、working tree、staged files、commit message、可回滚方式 |
| 创建或修改真实 issue/PR、label、comment、assignee、close 状态 | `to-spec`、`to-tickets`、`triage`、`wayfinder` | tracker、repo、issue 范围、预览内容、批量数量、回滚方式 |
| 写 dependency、hook、global config 或 chmod | `setup-matt-pocock-skills`、`git-guardrails-claude-code`、`migrate-to-shoehorn`、`setup-pre-commit`、`setup-ts-deep-modules` | target files、现有配置、package manager、全局/项目 scope |
| 读取或写入 secret、`.env`、GitHub secrets/variables | `wizard` | secret 名称、目标 repo/environment、存储位置、日志脱敏 |
| 启动后台 agent 或人机交互脚本 | `research`、`claude-handoff`、`wayfinder`、`wizard`、`diagnosing-bugs` HITL fallback | cwd、权限、prompt、并发限制、停止方式 |
| Migration、cutover 或生产操作 | `wizard` 的相应 branch | dry-run、备份、审批人、回滚、验证命令、生产窗口 |

## 6. 上游差异

本地化仓库最近一次明确同步见
[`PR #21`](https://github.com/vinvcn/mattpocock-skills-zh-CN/pull/21)，其上游固定为
[`mattpocock/skills@6acc160e4e0cd062dbbbd7a1b26ae92855edf07e`](https://github.com/mattpocock/skills/commit/6acc160e4e0cd062dbbbd7a1b26ae92855edf07e)。

访问时上游 `main` 固定为
[`6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`](https://github.com/mattpocock/skills/commit/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76)。
[固定 compare](https://github.com/mattpocock/skills/compare/6acc160e4e0cd062dbbbd7a1b26ae92855edf07e...6654f6b60cd9d5be8b54c6fafe44346dabeb3b76)
显示上游领先 39 commits，并新增两个未进入本地仓库的 beta Skill：

- [`implement-spec`](https://github.com/mattpocock/skills/blob/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76/skills/in-progress/implement-spec/SKILL.md)：按 ticket task graph 并行实现整份 spec，并形成单一 PR。
- [`retro`](https://github.com/mattpocock/skills/blob/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76/skills/in-progress/retro/SKILL.md)：审查 coding session 的 agent environment；上游 README 明确标为 stub。

这 39 commits 还包含以下与调用行为有关的变化：

- 把 operative cross-skill instruction 从裸 `/skill` prose 改为显式 Skill tool 调用。
- 把 user-invoked setup 前置条件改成“让用户运行”，避免其他 Skill 尝试调用它。
- 让 `wait-what` 通过 `CONTEXT-MAP.md` 选择正确 context。
- 调整 `grilling` 的问题分隔和若干 description/文档措辞。

这些是同步差异，不表示本地 Skill 在任何 harness 中已经实际失败。

## 7. 仓库内部冲突与证据缺口

1. **TDD 名称与过程冲突（E1/E2）**：README 和 OpenAI metadata 使用
   red-green-refactor；`tdd/SKILL.md` 排除 refactor；`code-review` 只报告、不执行重构。
2. **Misc 发布说明冲突（E1/E2）**：`skills/misc/README.md` 写“不在 plugin 中推广”，
   但本地 `plugin.json` 包含全部 4 个 misc Skill。PR #21 说明这是本地策略，但 bucket README
   没有同步改写。
3. **Prototype 索引冲突（E1/E2）**：Engineering README 称 logic prototype 为 terminal app；
   `prototype/SKILL.md` 和 `LOGIC.md` 规定产物是单一 HTML。
4. **Setup tracker 说明冲突（E1/E2）**：顶层 README 写 GitHub/Linear/local；实际 seed
   templates 是 GitHub/GitLab/local，Linear 只走 Other freeform。
5. **Setup provisioning 缺口（E1/E4）**：setup 写 label vocabulary，但不创建或验证真实
   triage/`wayfinder:*` labels，也不验证 CLI auth。
6. **Architecture report 自包含冲突（E1）**：文档称 self-contained HTML，但 scaffold
   依赖 Tailwind 和 Mermaid CDN。
7. **Deep-module rule 数量冲突（E1）**：Skill 反复写“四条 rules”，bundled config 实际
   有五个 `forbidden` entries。
8. **Grilling contract 冲突（E1）**：共享 primitive 要求一轮询问完整 frontier；
   `loop-me` 要求一次一个问题。
9. **Translation invariant 缺口（E1/E3）**：35 个同步 Skill 的 frontmatter name、
   invocation policy 和 link targets 与上游同步点一致，但 4 个 SKILL 的 fenced code
   blocks 不完全一致；当前 README 也没有 translate-skill 要求的 sync log。
10. **Internal metadata 缺口（E1）**：`translate-skill` 是实际 `SKILL.md`，但没有
    `agents/openai.yaml`；公开安装器是否发现它未由仓库证明。
11. **运行证据缺口（E5）**：本项目只做静态审计。任何“可运行”“能拦截”“能创建 native
    blocker”“可安全重入”等行为仍需在明确授权的隔离环境中验证。

## 8. 静态结论

- 目标仓库的实际 inventory 是 36，而不是 plugin 中的 29。
- 29 个公开稳定 Skill 的 README、公开目录和 plugin 索引集合一致；额外 7 项按仓库规则
  分别属于 beta 与 internal。
- 原仓库强项集中在需求澄清、规格化、ticket 拆解、TDD、调试、代码审查、领域建模和
  多会话决策。市场研究、用户研究、AI Eval、安全、部署验证、可观测性、增长实验和
  post-production learning 不应由这 36 项被推断为已完整覆盖。
- 调用 Skill 只代表选择方法，不代表授权 commit、外部 tracker、secret、部署、迁移或
  生产操作。关系与审批门见
  [`02-Skills调用方法与关系图.md`](./02-Skills调用方法与关系图.md)。
