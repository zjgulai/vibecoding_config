# PM-Skill 2.0 核心工作流受限融合 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将经过价值审计的 PM-Skill 2.0 方法作为受限 Adapter 写入现有全栈开发 Prompt Chain，同时保持 M00–M13、A00–A13、G0–G6 和 R3 为唯一流程、产物、决定与授权体系。

**Architecture:** 以产品决策图作为跨模块接口，在 M02–M09、M11–M13 中只投影各模块拥有的实体和检查；M00/M01/M10 不增加方法，`prompts/99` 最多增加一条 active ID 交接不变量，若与既有 Handoff 完全重复则经消融恢复为 preimage。普通 Prompt 是模块语义源，对话 Prompt 镜像同一触发、字段、禁止结论和停止条件；来源审计、生命周期说明和使用手册负责解释，不建立第二套运行时。

**Tech Stack:** Markdown、`rg`、Ruby 标准库、Python 3.9 标准库、macOS `/usr/bin/stat`、`/sbin/sha256sum`、`/bin/cat`、`/bin/cp` 与 `renamex_np(RENAME_SWAP | RENAME_EXCL)`；不新增依赖，不安装或运行 `pm-skills`，不调用真实模型、生产系统或外部 provider。

**Approved design:** `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md`

## Global Constraints

- 已批准方案是「分层 Adapter」。不安装、不 vendor、不复制 `SpaceZephyr/pm-skills` 的原始 Skill、提示词、模板或专家人格。
- 外部方法来源固定为 `SpaceZephyr/pm-skills@4c486c7a532de8890e88036533e0a48d578087ed`。X 帖子只作为来源入口，记录 2026-09-03 的取得状态；不能把无法匿名取得的 X Article 正文写成已审读。
- M00–M13、A00–A13、G0–G6 和现有 R3 语义保持不变。不新增 M14、A14、G7、第二控制器、第二状态机或新批准状态。
- `prompts/99` 仍是唯一控制器。产品决策图只传递 active ID、权威引用或显式关闭，不执行路由、批准或外部动作。
- M03 拥有 Opportunity 语义；M04 拥有 Outcome、Candidate 和 Hypothesis 语义，且只记录产品 Decision；Decision authority 始终属于现有人类决定者或 Gate，Agent 只能提出 `proposed`。M05 独占 Metric/Event 语义；M06/M12 创建各自 Test；M07 创建 Slice；M08 只实现已批准 Slice 和测量定义；M09 只读审查。
- 普通 Prompt 与对应 `prompts_ask` 必须镜像触发条件、最低证据、最小字段、不能得出的结论、停止条件和下游接口。对话版仍保持每轮一个高信息价值问题和生成前确认。
- 每个受影响的普通/对话 Prompt 都在既有 `## Handoff` 标题后的正文内保留且仅保留一条由本计划 `verify-chain.rb::LINEAGE_LINES` 定义的精确 `Decision lineage:` 行。该行的 `Consumes`、`Produces`、`Explicitly closed`、`Blockers`、`Consumers` 和 `Evidence_Refs` 六字段都不得为空；普通版与对话版使用同一模块值。它只索引本 Axx 的权威正文，不替代完整 Handoff。
- 竞品迁移、行为到机会、问卷、产品决策图/风险、优先级、旅程骨架、预实现评审、测量、假设测试、walking skeleton、Roadmap、实现追踪、风险/测量复核、行动登记、实验决定与复盘行动均按 Adapter 契约的条件触发。不满足触发条件时不生成空表格；若上游已有必须处理的 ID，不得用“未触发”静默丢弃，必须消费、传递或取得权威 `closed-not-applicable` Decision。
- 缺少事实时写 `Unknown`；未经验证的解释写入 `Assumptions`；会改变决定的未决问题写入 `Open questions`。不制造默认分数、样本量或统计阈值。
- 四类产品风险不能替代安全、隐私、合规、数据完整性、无障碍、可靠性、可运维性、兼容性或 AI 安全。
- 真实 launch/stop/extend/traffic/flag/publish 仅在 `MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION` 时发生；否则必须写 `Not launched / no production verification`。
- G0 只限定数据目的和范围；数据模型/隐私/架构取舍需 G3；代码和埋点实现需 G4 与精确 `ALLOWED_FILES`；生产查询/导出需 M11 的对象级、未过期 R3；外部 analytics/provider 配置变更另需匹配 R3。任一层不能代替其他层。
- 内容修改只使用 `apply_patch`。双读取规范化是已经单独批准后才允许执行的机械步骤，使用本计划固定的 `cp -p` staging 和原子替换协议。
- 执行期间不勾改本计划的 checkbox，也不改写已批准设计的正文；任务状态和短期验证证据记录在对话与固定 snapshot 中。因此这两份文档在最终验收中只允许发生双读取规范化，cat 内容必须与 Task 0 preimage 一致。
- 当前目录不是 Git repository。不要 commit，也不要创建 branch/worktree；以精确 preimage、四值 manifest、逐任务 oracle、独立审查和受保护文件 manifest 代替 Git 证据。
- 不修改 `全栈开发Prompt Chain.zip`、`Constraint/`、既有 `/private/tmp/vibecoding-ablation-pass-20260902-c58402c5` 或本计划外的任何文件。
- 如果基线、锚点、受保护 manifest、授权范围或用户并发修改任一不匹配，立即停止。不得恢复或覆盖用户修改。执行期间同一时刻只允许一个 implementer 写入，reviewer 全部只读；Task 0 授权提案必须请用户暂停对 32 个 allowlist 路径的手工编辑，任一漂移均使本次授权失效。
- `guard-workspace.zsh` 是 optimistic concurrency check，不是 filesystem lock。guard PASS 到 wrapper 封存 postimage 之间无法仅凭 hash 区分 `apply_patch` 与并发手工编辑；因此用户、implementer 和所有 reviewer 对当前 task target 的 quiescence 是每次写入尝试的硬前提。无法确认暂停写入时不得开始或继续；atomic swap 只保证 swap-time 版本被保留，不声称竞态版本始终留在原 pathname。
- `TASK1`–`TASK8` 每次尝试都显式设置全局唯一 `EVIDENCE_ID` 和实际 `PREVIOUS_SCOPE_TSV`。首次使用 `TASKn`，返工依次使用 `TASKn_R2`、`TASKn_R3`；下游必须消费最新已通过 wrapper 与 green oracle 的 `scope32-after.tsv`，不得按名义 Task 编号猜测前驱，也不得覆盖旧 manifest 或 `atomic-prior`。`verify-chain.rb` 始终运行对应语义模式 `taskn`。
- Tasks 1–8 不创建独立 review receipt。其阻断证据是该尝试封存的完整 scope、protected/ZIP evidence 和 executable green oracle；各 Task 末尾的 scoped review 是返工输入，不是可单独宣称 PASS 的 gate。三份不可变 Task 9 报告是唯一独立的 Critical/Important 阻断门。若 scoped review 发现问题，用新的 `EVIDENCE_ID` 重跑该 Task 的 guard、wrapper 和 green oracle，再向下游交接新 scope。
- 每个写入任务完成初稿后执行消融式删减检查：逐项删除不改变决定、证据、安全或下游消费的新增内容；与现有规则重复的内容合并；必要边界记录保留依据。

## File Structure and Exact Scope

本计划允许 32 个路径进入 snapshot/规范化 allowlist。其中 29 个现有正式文件是内容候选，1 个正式文档会新建，设计文档与本计划只做双读取规范化。`prompts/99` 的新增兼容项必须经过消融：若与既有 Handoff 完全重复，则其 cat 内容恢复为 Task 0 preimage，因此最终实际内容变化为 28 或 29 个，规范化但内容不变为 3 或 2 个；不得为满足固定计数而保留冗余文字。

### Research and navigation

- Modify: `全栈开发Prompt Chain/report-source.md` — 外部来源、版本、许可证与主张的单一事实源。
- Modify: `全栈开发Prompt Chain/05-GitHub候选与替代审计.md` — `pm-skills` 的采用、改写与排除判断。
- Create: `全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md` — 面向使用者的价值审计和模块映射。
- Modify: `全栈开发Prompt Chain/README.md` — 只增加新文档导航。

### Workflow documentation

- Modify: `全栈开发Prompt Chain/03-AI产品全生命周期映射.md` — 增加受限方法投影，不改变 36/36 归属。
- Modify: `全栈开发Prompt Chain/04-模块化Skills工作流.md` — 增加产品决策图交接和模块职责投影。
- Modify: `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md` — 增加 Adapter 和 active ID 使用说明。
- Modify: `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md` — 只增加一条兼容规则。

### Canonical module prompts

- Modify: `全栈开发Prompt Chain/prompts/02-机会与市场调研.md`
- Modify: `全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md`
- Modify: `全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md`
- Modify: `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md`
- Modify: `全栈开发Prompt Chain/prompts/12-增长与实验.md`
- Modify: `全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md`

### Human-dialogue mirrors

- Modify: `全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/12-增长与实验.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md`

### Normalization-only documents

- Normalize only: `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md`
- Normalize only: `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md`

M00、M01、M10 及其对话版不修改。不存在 `prompts_ask/00` 或 `prompts_ask/99`，也不创建。

## Frozen Input Gate

### Existing target baseline

以下 30 个现有文件按 `relative_path NUL pathname_size NUL pathname_sha256 NUL cat_size NUL cat_sha256 LF`、`LC_ALL=C` 排序后的 aggregate 必须为：

```text
TARGET_EXISTING_FILES=30
TARGET_BASELINE_MANIFEST_SHA256=71c6d4ce2b2d4e928965e604195ec17574d97c79062ad91432741c9141e88e8b
```

| Path | pathname bytes | pathname SHA-256 | cat bytes | cat SHA-256 |
| --- | ---: | --- | ---: | --- |
| `全栈开发Prompt Chain/README.md` | 5466 | `d4082efd3feac7fe7490c0193b35d975e82ab09b3a00459b1da1a92adaee4c59` | 5466 | `d4082efd3feac7fe7490c0193b35d975e82ab09b3a00459b1da1a92adaee4c59` |
| `全栈开发Prompt Chain/report-source.md` | 36041 | `796b405fdedde7c5f0161c1de77e71097d4f8a8096b98f6c192f4f43087181de` | 36041 | `796b405fdedde7c5f0161c1de77e71097d4f8a8096b98f6c192f4f43087181de` |
| `全栈开发Prompt Chain/03-AI产品全生命周期映射.md` | 21389 | `12663cf7ecab1e76292c268a63ee80f772fe2e4738eea406de485c67b1574a73` | 21389 | `12663cf7ecab1e76292c268a63ee80f772fe2e4738eea406de485c67b1574a73` |
| `全栈开发Prompt Chain/04-模块化Skills工作流.md` | 32705 | `2eb92244eeddbc5bb93abd9489857bf4190b1bc5271d00d5cf69c0c399bebdee` | 28609 | `9e44b5a2f3f223643a04c10d05abbf66e6f67e10f8791b1eb552c7f738576aa3` |
| `全栈开发Prompt Chain/05-GitHub候选与替代审计.md` | 37982 | `297f6dc748c9239121e2062bbc0b3de84337fb1c78e3910c6a7dc8c560eb408b` | 37982 | `297f6dc748c9239121e2062bbc0b3de84337fb1c78e3910c6a7dc8c560eb408b` |
| `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md` | 14771 | `33495b378acca8f3ffea0012b4b5ab721878c42e86b38007f0c3060bcb7aa7d8` | 10675 | `4bf2bb33ffe4cc81f48805bdffd73d5a1368c71376149fb870c32e573c27b623` |
| `全栈开发Prompt Chain/prompts/02-机会与市场调研.md` | 3377 | `8addf3ca181859f9505fac88b2e9f460defa3f65bb56c7baad03214c34037b85` | 3377 | `8addf3ca181859f9505fac88b2e9f460defa3f65bb56c7baad03214c34037b85` |
| `全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md` | 3448 | `7e922f02088391110b715717c8f41cfc521fc27cdbafc5d63b1d7a6a2592fff9` | 3448 | `7e922f02088391110b715717c8f41cfc521fc27cdbafc5d63b1d7a6a2592fff9` |
| `全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md` | 2970 | `7ff64918007f9bd62ffbcdded866265250c7905307a91d365cfd85196669243b` | 2970 | `7ff64918007f9bd62ffbcdded866265250c7905307a91d365cfd85196669243b` |
| `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md` | 4151 | `813932012a7c74d455cd7931a2c380e9320edaa45a7c89be1052e831e474f505` | 4151 | `813932012a7c74d455cd7931a2c380e9320edaa45a7c89be1052e831e474f505` |
| `全栈开发Prompt Chain/prompts/06-原型与UX验证.md` | 9380 | `3056ac4c207ee29a44be1825610c9aabba3eb045ded640f121d80a3a3854439d` | 5284 | `763b873fb5443d01211d86af6976a1d8809f8a55e055a8481c4dbd72497b3eed` |
| `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md` | 9234 | `9a33670be387c02d73e00bfe81e4783b8cc028abce54a315adf54d801ac67c29` | 5138 | `dd3b223e1a042e69b25e7d830c86c01d2d7786a5814f5bc98a5d9b39c87af481` |
| `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md` | 10203 | `2fc9db71f975f2b0d32eaa760cb528fc8d3b3861d67a46b8d5c9f1ebe795afc4` | 6107 | `d32b2f7681abd03b37f032522f13a55cd2d00de4a4dbc60bacaf26eb2c25cf76` |
| `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md` | 9756 | `6759715803ec869ba5bb4e1371334dc25995b6755eac4e5a7648434a438b8b5c` | 5660 | `1a329c82aae10bd4419a938c7e1f0c496f04de9b2a6184d33b1ad46aa9fd9d89` |
| `全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md` | 4683 | `948ef8d860f8c49eadeef8abbacbcd907e5c2ad2a6c3a2dcd5fcbb0cdc24c285` | 4683 | `948ef8d860f8c49eadeef8abbacbcd907e5c2ad2a6c3a2dcd5fcbb0cdc24c285` |
| `全栈开发Prompt Chain/prompts/12-增长与实验.md` | 5020 | `b9372d40666282fa320712bdfae0ef885b0e61d5b13acf375b17ef83f47c3e00` | 5020 | `b9372d40666282fa320712bdfae0ef885b0e61d5b13acf375b17ef83f47c3e00` |
| `全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md` | 5612 | `e948ced3cc85582c2db6764f83c66fa8ee245f7a76c034589ee3e7395a20fdf4` | 5612 | `e948ced3cc85582c2db6764f83c66fa8ee245f7a76c034589ee3e7395a20fdf4` |
| `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md` | 11125 | `631728e5f06c311de397c9f0302e8b932fb5c147d68259f127efdc92b9dbe520` | 7029 | `66680261a1a3c9a76fef6b2bb14b47c0d553bd25d660f1537d09115b56e9e381` |
| `全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md` | 4081 | `bcc3d37a66a14ab399470fa364a461f07c465b6369324ff4d3641a37ad869731` | 4081 | `bcc3d37a66a14ab399470fa364a461f07c465b6369324ff4d3641a37ad869731` |
| `全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md` | 8289 | `86c2a47ca1f3fbb7bd059f1d98b7431b6785143fb3fb9aeaa9014bc5fabdb493` | 4193 | `4ff504054e094d4ae28fa5980515a8c8af5acf0248e0b4fa55adef0110a0cd96` |
| `全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md` | 3681 | `7c6e862bd9e7ffe6aef3479e559e8551cf96c6b08eb5bd515b6b1a1f389a770d` | 3681 | `7c6e862bd9e7ffe6aef3479e559e8551cf96c6b08eb5bd515b6b1a1f389a770d` |
| `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md` | 5658 | `7204fc389a3adefe9cfa5044d0bbe82c0c43de218e9be16d0cdb0a0aaade60d0` | 5658 | `7204fc389a3adefe9cfa5044d0bbe82c0c43de218e9be16d0cdb0a0aaade60d0` |
| `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md` | 10314 | `73a004863dcd4098db0dbdeaa375420b3a81d470629b501bf3b9043d3b278935` | 6218 | `8259eb847f0405de9a90b196111e64e86859816a64c1476e5b55ef3262928f17` |
| `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md` | 10329 | `4b042e49b169866eb1449016201ed2685b061b9a61a599449371c48893cf9642` | 6233 | `5ab3867db6409e6fc361a6723c9a0bfe8cde7ad785c84f2467b27a23f6bfee01` |
| `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md` | 11574 | `0075aad185b4681f9231ee9bf06ea41f5f55be8f81f51f95686d63a58af24745` | 7478 | `fc9712fa801d0a6e55e7789a30ae386b7a509aa12a085f62910fe6a66ff2881f` |
| `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md` | 10970 | `9a57fdf2436bf6a7acfd7dffd013c93ec9724b88c31d9f1c1062777bdf1e7644` | 6874 | `ca93704f3e4bb876179160cfeb313fc52c625d5d7dcfe8346871581a315d7c21` |
| `全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md` | 9554 | `a34b69d631c73c7c3b77abda0042dab044e893afe97fb2690a5d0580440b6802` | 5458 | `64a658441fd4a8447205a562eb1a0acf1dfcba24525116e7df0ec50ccc883eef` |
| `全栈开发Prompt Chain/prompts_ask/12-增长与实验.md` | 9294 | `46e04dedfff557ade7891fa529bc2cc7666a685777cacf3a662305a23044c414` | 5198 | `7621c817651047192fa19a76dea1d762a09458a25de8dbd1e74b5af85f91b7bf` |
| `全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md` | 5787 | `6e1f960c83e75d6413652694d16b7e7d54ef216fe1441b2f8214f3728c72a6de` | 5787 | `6e1f960c83e75d6413652694d16b7e7d54ef216fe1441b2f8214f3728c72a6de` |
| `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md` | 46064 | `c2e393728507cda46f095fec1f2ff96bd478ace9179f752af5115d1efa379c86` | 41968 | `cec7f39912b54c319d37039726e579edd43c8d07a5c45d4fcbfb811a7a4ad11d` |

`08-PM-Skill-2.0核心工作流评估与融合.md` 在计划开始时必须不存在。本计划文件在执行时动态记录四值，不把自引用 hash 写进自身。

### Protected baseline

在 `全栈开发Prompt Chain/` 内排除上述 32 个 allowlist 路径与 `.DS_Store` 后，受保护 regular files 必须为：

```text
PROTECTED_FILES=44
PROTECTED_MANIFEST_SHA256=0da3840dbbdde2fb2c32bb77f0ea22723762e2468a0774fe698213fb3d34cdc9
```

`全栈开发Prompt Chain.zip` 必须保持：

```text
pathname_size=137195
pathname_sha256=af45e076a34778c10aab388d191a563df11694036fb25857ca629605732c5142
cat_size=137195
cat_sha256=af45e076a34778c10aab388d191a563df11694036fb25857ca629605732c5142
```

正式 snapshot 固定为 `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce`，后缀取正确 target aggregate 的前 8 位。该路径已存在时停止，不覆盖、不删除。诊断探针 `/private/tmp/pm-skill-backup-probe.K2D0eC` 不是正式 snapshot，不作为恢复源，也不在本计划中清理。

## Authorized Normalization Protocol

该协议只有在 Task 0 获得单独、精确的用户授权后才可运行。`cp -c -p` 用于 clone preimage，已在隔离探针中证明会保留 pathname/cat 两种读取与 mode；`cp -p` 用于生成只含 cat 可读内容的一致 staging 文件。目标替换使用 macOS `renamex_np(RENAME_SWAP)` 原子交换：交换瞬间的旧目标会落在 staging 路径，随后移入 snapshot 的 `atomic-prior/`，因此该版本不会静默丢失。协议依赖已确认的目标 quiescence，不声称提供 filesystem lock 或在违规竞态时保持原 pathname。每次执行仍须重新验证，不能只依赖探针结论。

Task 0 在 snapshot 中创建 `normalize-targets.zsh`。每个写入任务先以四值生成器封存该任务 `post-apply_patch.tsv`，其字段为 `relative_path<TAB>pathname_size<TAB>pathname_sha256<TAB>cat_size<TAB>cat_sha256<TAB>mode`。后续任务只以任务 ID、该已封存 TSV 和精确路径调用：

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/normalize-targets.zsh \
  TASK1 \
  /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/manifests/TASK1-post-apply-patch.tsv \
  '全栈开发Prompt Chain/report-source.md' \
  '全栈开发Prompt Chain/README.md'
```

脚本必须为每个文件执行：

1. 验证路径位于固定 allowlist、是 regular file 且不是 symlink。
2. 要求已封存 expected TSV 中每个目标恰好一行，并在 staging 前校验当前 mode 和 pathname/cat 四值与该行完全相同。
3. 在同目录创建唯一 staging 文件，使用 `/bin/cp -p` 复制当前文件。
4. 验证 staging 的 pathname/cat size 与 SHA-256 分别相等，并且 staging cat SHA-256 等于源文件修改后的 cat SHA-256。
5. 交换前再次校验当前目标六值与 expected TSV 相同；随后用 `renamex_np(RENAME_SWAP)` 原子交换 staging 与精确目标。
6. 使用 `renamex_np(RENAME_EXCL)` 将交换瞬间的旧目标从 staging 独占移动到 snapshot `atomic-prior/<TASK_ID>/<relative_path>`；已存在或跨卷失败都停止且保留 staging，不得覆盖。成功后验证 prior 与 expected TSV 一致；不一致表示竞态，必须停止，但不删除该冲突副本。
7. 验证新目标 pathname/cat 一致、内容 cat SHA-256 与 expected TSV 相同、mode 未变化。
8. 交换前失败保留 staging；交换后失败保留 `atomic-prior` 和 Task 0 preimage。不自动回滚，不覆盖任何其他版本。

---

### Task 0: Freeze evidence, create an exact clone preimage, and stop for normalization authorization

**Files:**

- Read: all 30 existing baseline files listed above.
- Read: `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md`
- Create outside workspace: `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/`
- Must not create yet: `全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md`

**Interfaces:**

- Consumes: approved design, 30-file frozen baseline, 44-file protected baseline, current dynamic plan bytes.
- Produces: verified clone preimage for 31 existing allowlist files; sealed `baseline/targets-30-before.{bin,tsv}`, `baseline/existing-31-before.{bin,tsv}`, Step-1-bound `baseline/plan-gate.{bin,tsv}`, `baseline/plan-before.{bin,tsv}`, `baseline/protected-44-before.{bin,tsv}`, `baseline/zip-before.{bin,tsv}`, `baseline/audit-absence.txt` and matching post-clone manifests; `four-value-manifest.rb`, `guard-workspace.zsh`, `normalize-targets.zsh`, `capture-and-normalize.zsh`, `rollback-target.zsh`, `seal-task9-generation.rb`; and a user-visible authorization proposal.
- Must preserve: workspace bytes, ZIP, prior ablation snapshot, and all non-target files.

- [ ] **Step 1: Run the complete read-only baseline gate before creating the snapshot**

Run from `/Users/lute/Project/vibecoding_config`. This command writes nothing. It parses the 30-row table and 32-path scope from this plan, recomputes every four-value record, rejects symlinks/special files, and validates the ZIP and snapshot absence.

```zsh
set -euo pipefail
cd /Users/lute/Project/vibecoding_config
/usr/bin/ruby <<'RUBY'
require 'base64'
require 'digest'
require 'find'
require 'open3'
require 'set'

ROOT = File.expand_path('.')
PLAN_REL = '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
PLAN = File.join(ROOT, PLAN_REL)
CHAIN = File.join(ROOT, '全栈开发Prompt Chain')
SNAPSHOT = '/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
TARGET_SHA = '71c6d4ce2b2d4e928965e604195ec17574d97c79062ad91432741c9141e88e8b'
PROTECTED_SHA = '0da3840dbbdde2fb2c32bb77f0ea22723762e2468a0774fe698213fb3d34cdc9'
ZIP_SHA = 'af45e076a34778c10aab388d191a563df11694036fb25857ca629605732c5142'
raise 'Task 0 snapshot quiescence was not confirmed' unless ENV['TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED'] == 'yes'

def run_command(*argv, stdin_data: nil)
  options = {}
  options[:stdin_data] = stdin_data unless stdin_data.nil?
  stdout, stderr, status = Open3.capture3(*argv, options)
  raise "command failed: #{argv.inspect}: #{stderr}" unless status.success?
  stdout
end

def stream_sha(bytes)
  run_command('/sbin/sha256sum', stdin_data: bytes).split.first
end

def record(root, relative_path)
  raise "unsafe path: #{relative_path.inspect}" if relative_path.empty? || relative_path.include?("\0") || relative_path.include?("\n") || relative_path.include?("\t")
  absolute = File.expand_path(relative_path, root)
  raise "path escapes root: #{relative_path}" unless absolute.start_with?(File.expand_path(root) + File::SEPARATOR)
  stat = File.lstat(absolute)
  raise "symlink target: #{relative_path}" if stat.symlink?
  raise "not regular: #{relative_path}" unless stat.file?
  pathname_size = run_command('/usr/bin/stat', '-f', '%z', absolute).strip
  pathname_sha = run_command('/sbin/sha256sum', absolute).split.first
  cat_bytes = run_command('/bin/cat', absolute)
  cat_size = cat_bytes.bytesize.to_s
  cat_sha = stream_sha(cat_bytes)
  mode = run_command('/usr/bin/stat', '-f', '%Lp', absolute).strip
  [relative_path, pathname_size, pathname_sha, cat_size, cat_sha, mode]
end

def stable_plan_record(root, relative_path)
  absolute = File.expand_path(relative_path, root)
  before = File.lstat(absolute)
  raise 'unsafe plan pathname' unless before.file? && !before.symlink?
  native_size_before = run_command('/usr/bin/stat', '-f', '%z', absolute).strip
  native_sha_before = run_command('/sbin/sha256sum', absolute).split.first
  mode_before = run_command('/usr/bin/stat', '-f', '%Lp', absolute).strip
  cat_bytes = run_command('/bin/cat', absolute).b
  after = File.lstat(absolute)
  native_size_after = run_command('/usr/bin/stat', '-f', '%z', absolute).strip
  native_sha_after = run_command('/sbin/sha256sum', absolute).split.first
  mode_after = run_command('/usr/bin/stat', '-f', '%Lp', absolute).strip
  raise 'plan pathname changed during logical capture' unless
    [before.dev, before.ino, native_size_before, native_sha_before, mode_before] ==
    [after.dev, after.ino, native_size_after, native_sha_after, mode_after]
  row = [relative_path, native_size_before, native_sha_before, cat_bytes.bytesize.to_s, stream_sha(cat_bytes), mode_before]
  [row, cat_bytes]
end

def aggregate(records)
  bytes = records.sort_by { |row| row[0].dup.force_encoding(Encoding::BINARY) }
                 .map { |row| row.first(5).join("\0") + "\n" }.join.b
  stream_sha(bytes)
end

plan, plan_bytes = stable_plan_record(ROOT, PLAN_REL)
plan_text = plan_bytes.dup.force_encoding(Encoding::UTF_8)
raise 'plan is not valid UTF-8' unless plan_text.valid_encoding?
expected_rows = []
plan_text.each_line do |line|
  match = line.match(/^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \| (\d+) \| `([0-9a-f]{64})` \|$/)
  expected_rows << [match[1], match[2], match[3], match[4], match[5]] if match
end
raise "baseline table count=#{expected_rows.length}" unless expected_rows.length == 30
actual_rows = expected_rows.map { |row| record(ROOT, row[0]) }
expected_rows.zip(actual_rows).each do |expected, actual|
  next if expected == actual.first(5)
  warn "BASELINE_DRIFT path=#{expected[0]} expected=#{expected.inspect} actual=#{actual.first(5).inspect}"
  raise 'target baseline drift'
end
target_sha = aggregate(actual_rows)
raise "target aggregate=#{target_sha}" unless target_sha == TARGET_SHA

scope = plan_text[/## File Structure and Exact Scope\n(.*?)\n## Frozen Input Gate/m, 1]
raise 'scope section missing' unless scope
allowlist = scope.scan(/^- (?:Modify|Create|Normalize only): `([^`]+)`/).flatten
raise "allowlist count=#{allowlist.length}" unless allowlist.length == 32 && allowlist.uniq.length == 32
allowed = allowlist.to_set
protected_rows = []
Find.find(CHAIN) do |absolute|
  stat = File.lstat(absolute)
  if stat.directory?
    next
  elsif stat.symlink?
    raise "symlink under chain: #{absolute}"
  elsif !stat.file?
    raise "special file under chain: #{absolute}"
  end
  relative = absolute.delete_prefix(ROOT + File::SEPARATOR)
  next if File.basename(absolute) == '.DS_Store' || allowed.include?(relative)
  protected_rows << record(ROOT, relative)
end
protected_sha = aggregate(protected_rows)
raise "protected count=#{protected_rows.length}" unless protected_rows.length == 44
raise "protected aggregate=#{protected_sha}" unless protected_sha == PROTECTED_SHA

audit = File.join(ROOT, '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md')
raise 'audit document already exists' if File.exist?(audit) || File.symlink?(audit)
raise 'snapshot path already exists' if File.exist?(SNAPSHOT) || File.symlink?(SNAPSHOT)
zip = record(ROOT, '全栈开发Prompt Chain.zip')
raise "zip bytes=#{zip[1]}/#{zip[3]}" unless zip[1] == '137195' && zip[3] == '137195'
raise "zip sha=#{zip[2]}/#{zip[4]}" unless zip[2] == ZIP_SHA && zip[4] == ZIP_SHA
plan_gate_tsv = (plan.join("\t") + "\n").b
plan_gate_tsv_sha = stream_sha(plan_gate_tsv)

puts "TARGET_EXISTING_FILES=#{actual_rows.length}"
puts "TARGET_BASELINE_MANIFEST_SHA256=#{target_sha}"
puts "PROTECTED_FILES=#{protected_rows.length}"
puts "PROTECTED_MANIFEST_SHA256=#{protected_sha}"
puts 'AUDIT_DOCUMENT=ABSENT'
puts "ZIP_PROTECTION=PASS bytes=#{zip[3]} sha256=#{zip[4]}"
puts "PLAN_DYNAMIC pathname_size=#{plan[1]} pathname_sha256=#{plan[2]} cat_size=#{plan[3]} cat_sha256=#{plan[4]} mode=#{plan[5]}"
puts "PLAN_GATE_TSV_SHA256=#{plan_gate_tsv_sha}"
puts "PLAN_GATE_TSV_B64=#{Base64.strict_encode64(plan_gate_tsv)}"
puts 'SNAPSHOT=ABSENT'
puts 'TASK0_READ_ONLY_GATE=PASS'
RUBY
```

Expected exit code: `0`. The fixed output lines are:

```text
TARGET_EXISTING_FILES=30
TARGET_BASELINE_MANIFEST_SHA256=71c6d4ce2b2d4e928965e604195ec17574d97c79062ad91432741c9141e88e8b
PROTECTED_FILES=44
PROTECTED_MANIFEST_SHA256=0da3840dbbdde2fb2c32bb77f0ea22723762e2468a0774fe698213fb3d34cdc9
AUDIT_DOCUMENT=ABSENT
ZIP_PROTECTION=PASS bytes=137195 sha256=af45e076a34778c10aab388d191a563df11694036fb25857ca629605732c5142
SNAPSHOT=ABSENT
TASK0_READ_ONLY_GATE=PASS
```

Before this command, the coordinator must obtain an explicit `TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED=yes` confirmation that all writers for the 31 targets, protected tree and ZIP remain paused through the end of Step 3. This is a snapshot-consistency pause only; it is not normalization or implementation authorization. `PLAN_DYNAMIC` records the native pathname values bracketing one `/bin/cat` logical capture; that same captured byte string drives scope parsing and the cat fields. `PLAN_GATE_TSV_SHA256` and `PLAN_GATE_TSV_B64` bind the complete six-field row. Retain both values from this same invocation and pass them unchanged to Step 2; recomputing replacements after a mismatch is forbidden. Any other exit or fixed-line mismatch is a stop condition; do not update the plan to bless unexplained drift.

- [ ] **Step 2: Create the snapshot and its deterministic manifest generator**

Only after Step 1 passes, create the exact directories:

```zsh
set -euo pipefail
: "${TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED:?}"
[[ "$TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED" == yes ]]
snapshot_path='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
[[ ! -e "$snapshot_path" && ! -L "$snapshot_path" ]]
/bin/mkdir -m 700 "$snapshot_path"
/bin/mkdir -m 700 "$snapshot_path/preimage" "$snapshot_path/baseline" "$snapshot_path/manifests" "$snapshot_path/atomic-prior" "$snapshot_path/reviews" "$snapshot_path/rollback-conflicts" "$snapshot_path/task9" "$snapshot_path/task9-staging" "$snapshot_path/task9-rework-reservations"
```

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/four-value-manifest.rb` with the complete content below. Generated `.bin` and `.tsv` files are mechanical verification artifacts, not hand-edited project files.

```ruby
#!/usr/bin/ruby
require 'find'
require 'open3'
require 'set'

def run_command(*argv, stdin_data: nil)
  options = {}
  options[:stdin_data] = stdin_data unless stdin_data.nil?
  stdout, stderr, status = Open3.capture3(*argv, options)
  raise "command failed: #{argv.inspect}: #{stderr}" unless status.success?
  stdout
end

def stream_sha(bytes)
  run_command('/sbin/sha256sum', stdin_data: bytes).split.first
end

def record(root, relative_path)
  raise "unsafe path: #{relative_path.inspect}" if relative_path.empty? || relative_path.include?("\0") || relative_path.include?("\n") || relative_path.include?("\t")
  absolute = File.expand_path(relative_path, root)
  raise "path escapes root: #{relative_path}" unless absolute.start_with?(File.expand_path(root) + File::SEPARATOR)
  stat = File.lstat(absolute)
  raise "symlink: #{relative_path}" if stat.symlink?
  raise "not regular: #{relative_path}" unless stat.file?
  pathname_size = run_command('/usr/bin/stat', '-f', '%z', absolute).strip
  pathname_sha = run_command('/sbin/sha256sum', absolute).split.first
  cat_bytes = run_command('/bin/cat', absolute)
  cat_size = cat_bytes.bytesize.to_s
  cat_sha = stream_sha(cat_bytes)
  mode = run_command('/usr/bin/stat', '-f', '%Lp', absolute).strip
  [relative_path, pathname_size, pathname_sha, cat_size, cat_sha, mode]
end

def plan_sets(plan_path)
  text = run_command('/bin/cat', plan_path).force_encoding(Encoding::UTF_8)
  raise 'plan is not valid UTF-8' unless text.valid_encoding?
  baseline = []
  text.each_line do |line|
    match = line.match(/^\| `([^`]+)` \| \d+ \| `[0-9a-f]{64}` \| \d+ \| `[0-9a-f]{64}` \|$/)
    baseline << match[1] if match
  end
  raise "baseline count=#{baseline.length}" unless baseline.length == 30 && baseline.uniq.length == 30
  scope = text[/## File Structure and Exact Scope\n(.*?)\n## Frozen Input Gate/m, 1]
  raise 'scope section missing' unless scope
  allowlist = scope.scan(/^- (?:Modify|Create|Normalize only): `([^`]+)`/).flatten
  raise "allowlist count=#{allowlist.length}" unless allowlist.length == 32 && allowlist.uniq.length == 32
  plan_relative = '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
  [baseline, (baseline + [plan_relative]).uniq, allowlist]
end

mode = ARGV.shift or abort 'missing mode'
root = File.expand_path(ARGV.shift || abort('missing root'))
plan_path = File.expand_path(ARGV.shift || abort('missing plan path'))
baseline, existing, allowlist = plan_sets(plan_path)

case mode
when 'plan-set'
  selector = ARGV.shift or abort 'missing selector'
  paths = { 'baseline30' => baseline, 'existing31' => existing, 'scope32' => allowlist }.fetch(selector)
when 'protected'
  chain_relative = ARGV.shift or abort 'missing chain path'
  chain = File.expand_path(chain_relative, root)
  allowed = allowlist.to_set
  paths = []
  Find.find(chain) do |absolute|
    stat = File.lstat(absolute)
    if stat.directory?
      next
    elsif stat.symlink?
      raise "symlink under chain: #{absolute}"
    elsif !stat.file?
      raise "special file under chain: #{absolute}"
    end
    relative = absolute.delete_prefix(root + File::SEPARATOR)
    next if File.basename(absolute) == '.DS_Store' || allowed.include?(relative)
    paths << relative
  end
when 'explicit'
  path_count = Integer(ARGV.shift || abort('missing path count'), 10)
  paths = ARGV.shift(path_count)
  raise "explicit path count=#{paths.length}" unless paths.length == path_count
else
  abort "unknown mode: #{mode}"
end

binary_path = File.expand_path(ARGV.shift || abort('missing binary output'))
tsv_path = File.expand_path(ARGV.shift || abort('missing TSV output'))
abort "unexpected arguments: #{ARGV.inspect}" unless ARGV.empty?
raise 'duplicate paths' unless paths.uniq.length == paths.length
records = paths.map { |relative| record(root, relative) }
records.sort_by! { |row| row[0].dup.force_encoding(Encoding::BINARY) }
binary = records.map { |row| row.first(5).join("\0") + "\n" }.join.b
tsv = records.map { |row| row.join("\t") + "\n" }.join
raise 'output paths collide' if binary_path == tsv_path
File.open(binary_path, 'xb', 0o600) { |file| file.write(binary) }
File.open(tsv_path, 'xb', 0o600) { |file| file.write(tsv) }
puts "MANIFEST files=#{records.length} sha256=#{stream_sha(binary)} bin=#{binary_path} tsv=#{tsv_path}"
```

Run `/usr/bin/ruby -c /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/four-value-manifest.rb`; expected exit code `0` and output `Syntax OK`. Every manifest output uses exclusive create and rejects an existing path or symlink. If the second member of a `.bin`/`.tsv` pair cannot be created, retain the first as failure evidence and abandon that evidence ID; never clean it up and retry under the same name.

Bind the plan version reviewed by Step 1 before creating or executing any other helper. `TASK0_PLAN_GATE_TSV_SHA256` must be supplied by the coordinator from the same Step 1 output; the required-parameter check deliberately stops instead of accepting a placeholder or a freshly substituted hash:

```zsh
set -euo pipefail
: "${TASK0_PLAN_GATE_TSV_SHA256:?set this to the exact PLAN_GATE_TSV_SHA256 printed by Task 0 Step 1}"
: "${TASK0_PLAN_GATE_TSV_B64:?set this to the exact PLAN_GATE_TSV_B64 printed by Task 0 Step 1}"
: "${TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED:?}"
[[ "$TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED" == yes ]]
[[ "$TASK0_PLAN_GATE_TSV_SHA256" != *[^0-9a-f]* && ${#TASK0_PLAN_GATE_TSV_SHA256} -eq 64 ]]
workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_path='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
manifest="$snapshot_path/four-value-manifest.rb"
plan="$workspace_root/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"
gate_bin="$snapshot_path/baseline/plan-gate.bin"
gate_tsv="$snapshot_path/baseline/plan-gate.tsv"
[[ ! -e "$gate_bin" && ! -L "$gate_bin" && ! -e "$gate_tsv" && ! -L "$gate_tsv" ]]
/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" 1 \
  '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md' \
  "$gate_bin" "$gate_tsv"
actual_plan_gate_tsv_sha=$(/bin/cat "$gate_tsv" | /sbin/sha256sum | /usr/bin/awk '{print $1}')
[[ "$actual_plan_gate_tsv_sha" == "$TASK0_PLAN_GATE_TSV_SHA256" ]] || {
  print -u2 "plan changed after Task 0 Step 1: expected=$TASK0_PLAN_GATE_TSV_SHA256 actual=$actual_plan_gate_tsv_sha"
  exit 74
}
TASK0_PLAN_GATE_TSV_B64="$TASK0_PLAN_GATE_TSV_B64" /usr/bin/ruby - "$gate_tsv" <<'RUBY'
require 'base64'
path = ARGV.fetch(0)
expected = Base64.strict_decode64(ENV.fetch('TASK0_PLAN_GATE_TSV_B64'))
raise 'non-canonical plan gate Base64' unless Base64.strict_encode64(expected) == ENV.fetch('TASK0_PLAN_GATE_TSV_B64')
raise 'plan gate full-row drift' unless File.binread(path) == expected
RUBY
/bin/chmod a-w "$gate_bin" "$gate_tsv"
print -r -- "PLAN_GATE_RECEIPT=SEALED sha256=$actual_plan_gate_tsv_sha"
```

Expected exit `0` and `PLAN_GATE_RECEIPT=SEALED` with the Step 1 hash. A mismatch leaves the exclusive receipt pair in place, invalidates this snapshot path and stops; never revise the expected value or reuse the snapshot.

- [ ] **Step 3: Seal the before manifests, clone all 31 existing targets, and prove one-point-in-time equivalence**

Run from `/Users/lute/Project/vibecoding_config`:

```zsh
set -euo pipefail
: "${TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED:?}"
[[ "$TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED" == yes ]]
snapshot_path='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
manifest="$snapshot_path/four-value-manifest.rb"
plan="$PWD/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"
test -d "$snapshot_path/preimage"

/usr/bin/ruby "$manifest" plan-set "$PWD" "$plan" baseline30 "$snapshot_path/baseline/targets-30-before.bin" "$snapshot_path/baseline/targets-30-before.tsv"
/usr/bin/ruby "$manifest" plan-set "$PWD" "$plan" existing31 "$snapshot_path/baseline/existing-31-before.bin" "$snapshot_path/baseline/existing-31-before.tsv"
/usr/bin/ruby "$manifest" protected "$PWD" "$plan" '全栈开发Prompt Chain' "$snapshot_path/baseline/protected-44-before.bin" "$snapshot_path/baseline/protected-44-before.tsv"
/usr/bin/ruby "$manifest" explicit "$PWD" "$plan" 1 '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md' "$snapshot_path/baseline/plan-before.bin" "$snapshot_path/baseline/plan-before.tsv"
/usr/bin/ruby "$manifest" explicit "$PWD" "$plan" 1 '全栈开发Prompt Chain.zip' "$snapshot_path/baseline/zip-before.bin" "$snapshot_path/baseline/zip-before.tsv"

/usr/bin/cmp -s "$snapshot_path/baseline/plan-gate.bin" "$snapshot_path/baseline/plan-before.bin"
/usr/bin/cmp -s "$snapshot_path/baseline/plan-gate.tsv" "$snapshot_path/baseline/plan-before.tsv"
print -r -- 'PLAN_GATE_TO_SNAPSHOT=PASS'

/usr/bin/ruby - "$snapshot_path/baseline/targets-30-before.tsv" "$snapshot_path/baseline/existing-31-before.tsv" "$snapshot_path/baseline/plan-before.tsv" <<'RUBY'
target_path, existing_path, plan_path = ARGV
load_rows = lambda do |path|
  rows = File.readlines(path, chomp: true).map { |line| line.split("\t", -1) }
  raise "malformed manifest: #{path}" unless rows.all? { |row| row.length == 6 }
  raise "duplicate path: #{path}" unless rows.map(&:first).uniq.length == rows.length
  rows.each_with_object({}) { |row, index| index[row[0]] = row }
end
targets = load_rows.call(target_path)
existing = load_rows.call(existing_path)
plan = load_rows.call(plan_path)
raise "target count=#{targets.length}" unless targets.length == 30
raise "existing count=#{existing.length}" unless existing.length == 31
targets.each { |relative, row| raise "cross-sample drift: #{relative}" unless existing.fetch(relative) == row }
raise 'plan manifest count drift' unless plan.length == 1
plan.each { |relative, row| raise "plan cross-sample drift: #{relative}" unless existing.fetch(relative) == row }
puts 'BASELINE_CROSS_SAMPLE=PASS targets=30 existing=31 plan=1'
RUBY

test "$(/sbin/sha256sum "$snapshot_path/baseline/targets-30-before.bin" | /usr/bin/awk '{print $1}')" = '71c6d4ce2b2d4e928965e604195ec17574d97c79062ad91432741c9141e88e8b'
test "$(/sbin/sha256sum "$snapshot_path/baseline/protected-44-before.bin" | /usr/bin/awk '{print $1}')" = '0da3840dbbdde2fb2c32bb77f0ea22723762e2468a0774fe698213fb3d34cdc9'
test ! -e '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md'
```

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/baseline/audit-absence.txt` with exactly:

```text
AUDIT_DOCUMENT=ABSENT
checked_before_snapshot=true
snapshot_quiescence_confirmed=yes
```

Then clone and reseal the same workspace state:

```zsh
set -euo pipefail
: "${TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED:?}"
[[ "$TASK0_SNAPSHOT_QUIESCENCE_CONFIRMED" == yes ]]
snapshot_path='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
manifest="$snapshot_path/four-value-manifest.rb"
plan="$PWD/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"

preimage_paths=(
  '全栈开发Prompt Chain/README.md'
  '全栈开发Prompt Chain/report-source.md'
  '全栈开发Prompt Chain/03-AI产品全生命周期映射.md'
  '全栈开发Prompt Chain/04-模块化Skills工作流.md'
  '全栈开发Prompt Chain/05-GitHub候选与替代审计.md'
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md'
  '全栈开发Prompt Chain/prompts/02-机会与市场调研.md'
  '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md'
  '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md'
  '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md'
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md'
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'
  '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md'
  '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md'
  '全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md'
  '全栈开发Prompt Chain/prompts/12-增长与实验.md'
  '全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md'
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
  '全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md'
  '全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md'
  '全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md'
  '全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md'
  '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md'
  '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md'
  '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md'
  '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md'
  '全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md'
  '全栈开发Prompt Chain/prompts_ask/12-增长与实验.md'
  '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md'
  '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md'
  '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
)

for relative_path in "${preimage_paths[@]}"; do
  source_path="$PWD/$relative_path"
  clone_path="$snapshot_path/preimage/$relative_path"
  /bin/mkdir -p "${clone_path:h}"
  [[ ! -e "$clone_path" && ! -L "$clone_path" ]]
  /bin/cp -c -p "$source_path" "$clone_path"
  test "$(/usr/bin/stat -f %z "$source_path")" = "$(/usr/bin/stat -f %z "$clone_path")"
  test "$(/sbin/sha256sum "$source_path" | /usr/bin/awk '{print $1}')" = "$(/sbin/sha256sum "$clone_path" | /usr/bin/awk '{print $1}')"
  test "$(/bin/cat "$source_path" | /usr/bin/wc -c | /usr/bin/tr -d ' ')" = "$(/bin/cat "$clone_path" | /usr/bin/wc -c | /usr/bin/tr -d ' ')"
  test "$(/bin/cat "$source_path" | /sbin/sha256sum | /usr/bin/awk '{print $1}')" = "$(/bin/cat "$clone_path" | /sbin/sha256sum | /usr/bin/awk '{print $1}')"
done

/usr/bin/ruby "$manifest" plan-set "$PWD" "$plan" existing31 "$snapshot_path/baseline/workspace-31-after-clone.bin" "$snapshot_path/baseline/workspace-31-after-clone.tsv"
/usr/bin/ruby "$manifest" plan-set "$snapshot_path/preimage" "$plan" existing31 "$snapshot_path/baseline/preimage-31.bin" "$snapshot_path/baseline/preimage-31.tsv"
/usr/bin/ruby "$manifest" protected "$PWD" "$plan" '全栈开发Prompt Chain' "$snapshot_path/baseline/protected-44-after-clone.bin" "$snapshot_path/baseline/protected-44-after-clone.tsv"
/usr/bin/ruby "$manifest" explicit "$PWD" "$plan" 1 '全栈开发Prompt Chain.zip' "$snapshot_path/baseline/zip-after-clone.bin" "$snapshot_path/baseline/zip-after-clone.tsv"

/usr/bin/cmp -s "$snapshot_path/baseline/existing-31-before.bin" "$snapshot_path/baseline/workspace-31-after-clone.bin"
/usr/bin/cmp -s "$snapshot_path/baseline/existing-31-before.tsv" "$snapshot_path/baseline/workspace-31-after-clone.tsv"
/usr/bin/cmp -s "$snapshot_path/baseline/existing-31-before.bin" "$snapshot_path/baseline/preimage-31.bin"
/usr/bin/cmp -s "$snapshot_path/baseline/existing-31-before.tsv" "$snapshot_path/baseline/preimage-31.tsv"
/usr/bin/cmp -s "$snapshot_path/baseline/protected-44-before.bin" "$snapshot_path/baseline/protected-44-after-clone.bin"
/usr/bin/cmp -s "$snapshot_path/baseline/protected-44-before.tsv" "$snapshot_path/baseline/protected-44-after-clone.tsv"
/usr/bin/cmp -s "$snapshot_path/baseline/zip-before.bin" "$snapshot_path/baseline/zip-after-clone.bin"
/usr/bin/cmp -s "$snapshot_path/baseline/zip-before.tsv" "$snapshot_path/baseline/zip-after-clone.tsv"
test ! -e '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md'
test "$('/bin/cat' "$snapshot_path/baseline/audit-absence.txt")" = $'AUDIT_DOCUMENT=ABSENT\nchecked_before_snapshot=true\nsnapshot_quiescence_confirmed=yes'

/usr/bin/find "$snapshot_path/baseline" -type f -exec /bin/chmod a-w {} +
/usr/bin/find "$snapshot_path/baseline" -type d -exec /bin/chmod a-w {} +
/usr/bin/find "$snapshot_path/preimage" -type d -exec /bin/chmod a-w {} +
print -r -- "PREIMAGE_CLONE=PASS files=${#preimage_paths[@]} path=$snapshot_path"
print -r -- 'BASELINE_MANIFESTS=SEALED target=30 existing=31 protected=44 plan_gate=1 plan=1 zip=1'
```

Expected exit code: `0`; expected final lines are `PREIMAGE_CLONE=PASS files=31 path=/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce` and `BASELINE_MANIFESTS=SEALED target=30 existing=31 protected=44 plan_gate=1 plan=1 zip=1`. Only after every post-clone comparison passes may the coordinator release the Task 0 snapshot quiescence pause. Baseline evidence files/directories and preimage directories become non-writable, while preimage file contents and modes remain byte-for-byte/mode-for-mode equal to their manifest so rollback can restore the original mode. Task 9 re-hashes every preimage file; do not treat directory permissions alone as immutability. Any mismatch leaves the snapshot in place and stops; never delete or overwrite it automatically.

- [ ] **Step 4: Create the fixed pre-task guard and normalization helper in the snapshot**

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh`. This guard seals a fresh full-scope view before every task, compares it with the previous accepted scope, and independently rechecks protected files and the ZIP. It refuses to overwrite evidence:

```zsh
#!/bin/zsh
set -euo pipefail

workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
manifest="$snapshot_root/four-value-manifest.rb"
plan="$workspace_root/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"

(( $# == 3 )) || { print -u2 'usage: guard-workspace.zsh TASK_ID existing31|scope32 EXPECTED_TSV'; exit 64; }
task_id=$1
selector=$2
expected_tsv=${3:A}
[[ -n "$task_id" && "$task_id" != *[^A-Z0-9_]* ]] || { print -u2 "invalid task id: $task_id"; exit 65; }
[[ "$selector" == 'existing31' || "$selector" == 'scope32' ]] || { print -u2 "invalid selector: $selector"; exit 66; }
task9_evidence=0
case "$expected_tsv" in
  "$snapshot_root"/baseline/*.tsv|"$snapshot_root"/manifests/*.tsv) ;;
  "$snapshot_root"/task9/run-[0-9][0-9][0-9]/10-input/input-scope.tsv|"$snapshot_root"/task9/run-[0-9][0-9][0-9]/10-input/guard-scope.tsv) task9_evidence=1 ;;
  *) print -u2 "expected TSV outside sealed snapshot evidence: $expected_tsv"; exit 67 ;;
esac
[[ -f "$expected_tsv" && ! -L "$expected_tsv" ]] || { print -u2 "missing expected TSV: $expected_tsv"; exit 68; }
expected_bin=${expected_tsv%.tsv}.bin
[[ -f "$expected_bin" && ! -L "$expected_bin" ]] || { print -u2 "missing expected binary manifest: $expected_bin"; exit 69; }
[[ ! -w "$expected_tsv" && ! -w "$expected_bin" ]] || { print -u2 'expected manifest pair is not sealed'; exit 70; }
if (( task9_evidence )); then
  /usr/bin/ruby - "$expected_tsv" "$task_id" <<'RUBY'
require 'digest'
expected, task_id = ARGV
run_root = File.dirname(File.dirname(expected))
run_id = File.basename(run_root)
terminal_path = File.join(run_root, 'TERMINAL.tsv')
intent_path = File.join(run_root, 'terminal-intent.tsv')
seal_path = File.join(run_root, 'generation-seal.tsv')
raise 'missing Task 9 terminal evidence' unless [terminal_path, intent_path, seal_path].all? { |path| File.file?(path) && !File.symlink?(path) && !File.writable?(path) }
raise 'terminal intent drift' unless File.binread(terminal_path) == File.binread(intent_path)
lines = File.readlines(terminal_path, chomp: true)
header = lines.shift&.split("\t", -1)
expected_header = %w[Schema Run_ID State Reason_Code Required_Action Owning_Task Candidate_ID Next_Evidence_ID Rework_Reservation_Path Rework_Reservation_SHA256 Artifact_Path Input_Scope_TSV Input_Scope_SHA256 Review_Input_SHA256 Target_Manifest_SHA256 Candidate_Universe_SHA256 Ablation_Ledger_SHA256 Generation_Seal_SHA256]
raise 'terminal schema drift' unless header == expected_header && lines.length == 1
values = lines.first.split("\t", -1)
raise 'terminal field-count drift' unless values.length == header.length
terminal = Hash[header.zip(values)]
raise 'terminal state drift' unless terminal['Schema'] == 'task9-terminal/v1' && terminal['Run_ID'] == run_id && terminal['State'] == 'INVALIDATED'
raise 'generation seal hash drift' unless terminal['Generation_Seal_SHA256'] == Digest::SHA256.file(seal_path).hexdigest
seal_lines = File.readlines(seal_path, chomp: true)
raise 'seal header drift' unless seal_lines.shift == "Relative_Path\tBytes\tSHA256"
seal_rows = seal_lines.map { |line| line.split("\t", -1) }
relative = expected.delete_prefix(run_root + File::SEPARATOR)
sealed = seal_rows.find { |row| row[0] == relative }
raise 'expected Task 9 scope is not sealed' unless sealed && sealed.length == 3 && sealed[1] == File.size(expected).to_s && sealed[2] == Digest::SHA256.file(expected).hexdigest
if task_id.match?(/\ATASK9_RUN_(\d{3})\z/)
  expected_number = Integer(Regexp.last_match(1), 10) - 1
  raise 'Task 9 rebuild lineage drift' unless terminal['Required_Action'] == 'REBUILD_EVIDENCE' && File.basename(expected) == 'input-scope.tsv' && run_id == format('run-%03d', expected_number)
elsif task_id.match?(/\ATASK[1-8]_R\d+\z/)
  owner = task_id.sub(/_R\d+\z/, '')
  raise 'Task rework lineage drift' unless terminal['Required_Action'] == 'REWORK_CONTENT' && terminal['Owning_Task'] == owner && terminal['Next_Evidence_ID'] == task_id && File.basename(expected) == 'guard-scope.tsv'
  snapshot = File.dirname(File.dirname(run_root))
  reservation = File.join(snapshot, 'task9-rework-reservations', "#{run_id}.tsv")
  raise 'Task rework reservation path drift' unless terminal['Rework_Reservation_Path'] == reservation
  raise 'unsafe Task rework reservation' unless File.file?(reservation) && !File.symlink?(reservation) && (File.lstat(reservation).mode & 0o777) == 0o400
  reservation_bytes = File.binread(reservation)
  raise 'Task rework reservation hash drift' unless Digest::SHA256.hexdigest(reservation_bytes) == terminal['Rework_Reservation_SHA256']
  expected_reservation = "Schema\tOwner\tEvidence_ID\tSource_Run\tCandidate_ID\n" +    "task9-rework-reservation/v1\t#{owner}\t#{task_id}\t#{run_id}\t#{terminal['Candidate_ID']}\n"
  raise 'Task rework reservation content drift' unless reservation_bytes == expected_reservation
else
  raise 'Task 9 evidence cannot seed this task ID'
end
puts 'TASK9_PREDECESSOR=PASS'
RUBY
fi

before_bin="$snapshot_root/manifests/${task_id}-before-scope.bin"
before_tsv="$snapshot_root/manifests/${task_id}-before-scope.tsv"
protected_bin="$snapshot_root/manifests/${task_id}-before-protected.bin"
protected_tsv="$snapshot_root/manifests/${task_id}-before-protected.tsv"
zip_bin="$snapshot_root/manifests/${task_id}-before-zip.bin"
zip_tsv="$snapshot_root/manifests/${task_id}-before-zip.tsv"
for evidence_path in "$before_bin" "$before_tsv" "$protected_bin" "$protected_tsv" "$zip_bin" "$zip_tsv"; do
  [[ ! -e "$evidence_path" && ! -L "$evidence_path" ]] || { print -u2 "evidence path exists: $evidence_path"; exit 70; }
done

if [[ "$selector" == 'existing31' ]]; then
  [[ ! -e "$workspace_root/全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md" ]] || { print -u2 'audit document should still be absent'; exit 71; }
  /usr/bin/ruby "$manifest" plan-set "$workspace_root" "$plan" existing31 "$before_bin" "$before_tsv"
else
  [[ -f "$workspace_root/全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md" && ! -L "$workspace_root/全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md" ]] || { print -u2 'audit document missing or not regular'; exit 72; }
  /usr/bin/ruby "$manifest" plan-set "$workspace_root" "$plan" scope32 "$before_bin" "$before_tsv"
fi
/usr/bin/cmp -s "$expected_bin" "$before_bin" || { print -u2 "scope binary drift before $task_id"; exit 73; }
/usr/bin/cmp -s "$expected_tsv" "$before_tsv" || { print -u2 "scope TSV drift before $task_id"; exit 74; }

/usr/bin/ruby "$manifest" protected "$workspace_root" "$plan" '全栈开发Prompt Chain' "$protected_bin" "$protected_tsv"
/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" 1 '全栈开发Prompt Chain.zip' "$zip_bin" "$zip_tsv"
/usr/bin/cmp -s "$snapshot_root/baseline/protected-44-before.bin" "$protected_bin" || { print -u2 "protected binary drift before $task_id"; exit 75; }
/usr/bin/cmp -s "$snapshot_root/baseline/protected-44-before.tsv" "$protected_tsv" || { print -u2 "protected TSV drift before $task_id"; exit 76; }
/usr/bin/cmp -s "$snapshot_root/baseline/zip-before.bin" "$zip_bin" || { print -u2 "ZIP binary drift before $task_id"; exit 77; }
/usr/bin/cmp -s "$snapshot_root/baseline/zip-before.tsv" "$zip_tsv" || { print -u2 "ZIP TSV drift before $task_id"; exit 78; }

/bin/chmod a-w "$before_bin" "$before_tsv" "$protected_bin" "$protected_tsv" "$zip_bin" "$zip_tsv"
print -r -- "WORKSPACE_GUARD=PASS task=$task_id selector=$selector"
```

Do not run this guard until the separate normalization authorization is granted. Initial Task 1 compares against `baseline/existing-31-before.tsv`; every other attempt receives the actual latest accepted sealed `*-scope32-after.tsv` through `PREVIOUS_SCOPE_TSV`. A mismatch stops before any task-owned `apply_patch`; the helper never guesses a predecessor from the nominal task number.

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/normalize-targets.zsh` with the following complete behavior:

```zsh
#!/bin/zsh
set -euo pipefail

workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
typeset -A allowed
while IFS= read -r allowed_path; do
  allowed[$allowed_path]=1
done <<'PATHS'
全栈开发Prompt Chain/README.md
全栈开发Prompt Chain/report-source.md
全栈开发Prompt Chain/03-AI产品全生命周期映射.md
全栈开发Prompt Chain/04-模块化Skills工作流.md
全栈开发Prompt Chain/05-GitHub候选与替代审计.md
全栈开发Prompt Chain/06-Prompt-Chain使用手册.md
全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md
全栈开发Prompt Chain/prompts/02-机会与市场调研.md
全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md
全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md
全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md
全栈开发Prompt Chain/prompts/06-原型与UX验证.md
全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md
全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md
全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md
全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md
全栈开发Prompt Chain/prompts/12-增长与实验.md
全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md
全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md
全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md
全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md
全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md
全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md
全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md
全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md
全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md
全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md
全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md
全栈开发Prompt Chain/prompts_ask/12-增长与实验.md
全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md
全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md
全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md
PATHS

capture_values() {
  local capture_path=$1
  CAPTURE_PATH_SIZE=$(/usr/bin/stat -f %z "$capture_path")
  CAPTURE_PATH_SHA=$(/sbin/sha256sum "$capture_path" | /usr/bin/awk '{print $1}')
  CAPTURE_CAT_SIZE=$(/bin/cat "$capture_path" | /usr/bin/wc -c | /usr/bin/tr -d ' ')
  CAPTURE_CAT_SHA=$(/bin/cat "$capture_path" | /sbin/sha256sum | /usr/bin/awk '{print $1}')
  CAPTURE_MODE=$(/usr/bin/stat -f %Lp "$capture_path")
}

(( $# >= 3 )) || { print -u2 'usage: normalize-targets.zsh TASK_ID EXPECTED_TSV PATH...'; exit 64; }
task_id=$1
expected_tsv=$2
shift 2
[[ -n "$task_id" && "$task_id" != *[^A-Z0-9_]* ]] || { print -u2 "invalid task id: $task_id"; exit 65; }
expected_abs=${expected_tsv:A}
expected_exact="$snapshot_root/manifests/${task_id}-post-apply-patch.tsv"
[[ "$expected_abs" == "$expected_exact" ]] || { print -u2 "expected manifest/task mismatch: $expected_abs"; exit 66; }
expected_bin=${expected_abs%.tsv}.bin
[[ -f "$expected_abs" && ! -L "$expected_abs" && -f "$expected_bin" && ! -L "$expected_bin" ]] || { print -u2 'missing sealed postimage manifest pair'; exit 67; }
[[ ! -w "$expected_abs" && ! -w "$expected_bin" ]] || { print -u2 'postimage manifest pair is not sealed'; exit 68; }

typeset -A preflight_seen
for relative_path in "$@"; do
  [[ -n ${allowed[$relative_path]-} ]] || { print -u2 "not allowlisted: $relative_path"; exit 69; }
  [[ -z ${preflight_seen[$relative_path]-} ]] || { print -u2 "duplicate target: $relative_path"; exit 70; }
  preflight_seen[$relative_path]=1
  target_path="$workspace_root/$relative_path"
  [[ -f "$target_path" && ! -L "$target_path" ]] || { print -u2 "not a regular target: $relative_path"; exit 71; }
done

/usr/bin/ruby - "$expected_abs" "$@" <<'RUBY'
manifest_path, *targets = ARGV
rows = File.readlines(manifest_path, chomp: true).map { |line| line.split("\t", -1) }
raise 'malformed expected manifest' unless rows.all? { |row| row.length == 6 }
paths = rows.map(&:first)
raise 'duplicate expected rows' unless paths.uniq.length == paths.length
raise 'expected/argv target set drift' unless paths.sort == targets.sort && targets.uniq.length == targets.length
puts "NORMALIZE_PREFLIGHT=PASS files=#{targets.length}"
RUBY

typeset -A seen

for relative_path in "$@"; do
  [[ -n ${allowed[$relative_path]-} ]] || { print -u2 "not allowlisted: $relative_path"; exit 68; }
  [[ -z ${seen[$relative_path]-} ]] || { print -u2 "duplicate target: $relative_path"; exit 69; }
  seen[$relative_path]=1
  target_path="$workspace_root/$relative_path"
  [[ -f "$target_path" && ! -L "$target_path" ]] || { print -u2 "not a regular target: $relative_path"; exit 70; }

  expected_line=$(LC_ALL=C /usr/bin/awk -F '\t' -v wanted="$relative_path" '
    $1 == wanted { print; matches += 1 }
    END { if (matches != 1) exit 1 }
  ' "$expected_abs") || { print -u2 "expected manifest row count is not one: $relative_path"; exit 71; }
  IFS=$'\t' read -r expected_path expected_path_size expected_path_sha expected_cat_size expected_cat_sha expected_mode <<< "$expected_line"
  [[ "$expected_path" == "$relative_path" && "$expected_path_size" == <-> && "$expected_cat_size" == <-> && "$expected_path_sha" != *[^0-9a-f]* && ${#expected_path_sha} -eq 64 && "$expected_cat_sha" != *[^0-9a-f]* && ${#expected_cat_sha} -eq 64 && "$expected_mode" == <-> ]] || { print -u2 "malformed expected row: $relative_path"; exit 72; }

  capture_values "$target_path"
  [[ "$CAPTURE_PATH_SIZE" == "$expected_path_size" && "$CAPTURE_PATH_SHA" == "$expected_path_sha" && "$CAPTURE_CAT_SIZE" == "$expected_cat_size" && "$CAPTURE_CAT_SHA" == "$expected_cat_sha" && "$CAPTURE_MODE" == "$expected_mode" ]] || { print -u2 "pre-stage drift: $relative_path"; exit 73; }
  print -r -- "NORMALIZE_EXPECTED $relative_path pathname_size=$expected_path_size pathname_sha256=$expected_path_sha cat_size=$expected_cat_size cat_sha256=$expected_cat_sha mode=$expected_mode"

  target_dir=${target_path:h}
  stage_path=$(/usr/bin/mktemp "$target_dir/.pm-skill-normalize.XXXXXX")
  /bin/cp -p "$target_path" "$stage_path"

  capture_values "$stage_path"
  [[ "$CAPTURE_PATH_SIZE" == "$CAPTURE_CAT_SIZE" ]] || { print -u2 "stage size mismatch: $stage_path"; exit 74; }
  [[ "$CAPTURE_PATH_SHA" == "$CAPTURE_CAT_SHA" ]] || { print -u2 "stage hash mismatch: $stage_path"; exit 75; }
  [[ "$CAPTURE_CAT_SHA" == "$expected_cat_sha" && "$CAPTURE_MODE" == "$expected_mode" ]] || { print -u2 "stage content or mode drift: $stage_path"; exit 76; }

  [[ -f "$target_path" && ! -L "$target_path" ]] || { print -u2 "target changed type before swap: $relative_path"; exit 77; }
  capture_values "$target_path"
  [[ "$CAPTURE_PATH_SIZE" == "$expected_path_size" && "$CAPTURE_PATH_SHA" == "$expected_path_sha" && "$CAPTURE_CAT_SIZE" == "$expected_cat_size" && "$CAPTURE_CAT_SHA" == "$expected_cat_sha" && "$CAPTURE_MODE" == "$expected_mode" ]] || { print -u2 "pre-swap drift: $relative_path"; exit 78; }

  prior_path="$snapshot_root/atomic-prior/$task_id/$relative_path"
  [[ ! -e "$prior_path" && ! -L "$prior_path" ]] || { print -u2 "prior path exists: $prior_path"; exit 79; }
  /bin/mkdir -p "${prior_path:h}"
  /usr/bin/python3 - "$stage_path" "$target_path" "$prior_path" <<'PY'
import ctypes
import os
import sys

RENAME_SWAP = 0x00000002
RENAME_EXCL = 0x00000004
libc = ctypes.CDLL(None, use_errno=True)
renamex_np = libc.renamex_np
renamex_np.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
renamex_np.restype = ctypes.c_int
source = os.fsencode(sys.argv[1])
target = os.fsencode(sys.argv[2])
if renamex_np(source, target, RENAME_SWAP) != 0:
    error_number = ctypes.get_errno()
    raise OSError(error_number, os.strerror(error_number), sys.argv[1], sys.argv[2])
prior = os.fsencode(sys.argv[3])
if renamex_np(source, prior, RENAME_EXCL) != 0:
    error_number = ctypes.get_errno()
    raise OSError(error_number, os.strerror(error_number), sys.argv[1], sys.argv[3])
PY

  capture_values "$prior_path"
  [[ "$CAPTURE_PATH_SIZE" == "$expected_path_size" && "$CAPTURE_PATH_SHA" == "$expected_path_sha" && "$CAPTURE_CAT_SIZE" == "$expected_cat_size" && "$CAPTURE_CAT_SHA" == "$expected_cat_sha" && "$CAPTURE_MODE" == "$expected_mode" ]] || { print -u2 "swap-time conflict preserved at: $prior_path"; exit 80; }

  capture_values "$target_path"
  [[ "$CAPTURE_PATH_SIZE" == "$CAPTURE_CAT_SIZE" ]] || { print -u2 "final size mismatch: $relative_path"; exit 81; }
  [[ "$CAPTURE_PATH_SHA" == "$CAPTURE_CAT_SHA" ]] || { print -u2 "final hash mismatch: $relative_path"; exit 82; }
  [[ "$CAPTURE_CAT_SIZE" == "$expected_cat_size" && "$CAPTURE_CAT_SHA" == "$expected_cat_sha" ]] || { print -u2 "final content drift: $relative_path"; exit 83; }
  [[ "$CAPTURE_MODE" == "$expected_mode" ]] || { print -u2 "final mode drift: $relative_path"; exit 84; }
  print -r -- "NORMALIZED $relative_path pathname_size=$CAPTURE_PATH_SIZE pathname_sha256=$CAPTURE_PATH_SHA cat_size=$CAPTURE_CAT_SIZE cat_sha256=$CAPTURE_CAT_SHA mode=$CAPTURE_MODE prior=$prior_path"
done
```

Do not run the helper in Task 0.

- [ ] **Step 5: Create the task wrapper and validate the helper toolchain without touching workspace targets**

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh`:

```zsh
#!/bin/zsh
set -euo pipefail

workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
manifest="$snapshot_root/four-value-manifest.rb"
normalizer="$snapshot_root/normalize-targets.zsh"
plan="$workspace_root/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"

(( $# >= 2 )) || { print -u2 'usage: capture-and-normalize.zsh TASK_ID PATH...'; exit 64; }
task_id=$1
shift
[[ -n "$task_id" && "$task_id" != *[^A-Z0-9_]* ]] || { print -u2 "invalid task id: $task_id"; exit 65; }
before_tsv="$snapshot_root/manifests/${task_id}-before-scope.tsv"
[[ -f "$before_tsv" && ! -L "$before_tsv" ]] || { print -u2 "missing pre-task guard evidence: $before_tsv"; exit 66; }
post_bin="$snapshot_root/manifests/${task_id}-post-apply-patch.bin"
post_tsv="$snapshot_root/manifests/${task_id}-post-apply-patch.tsv"
final_bin="$snapshot_root/manifests/${task_id}-normalized.bin"
final_tsv="$snapshot_root/manifests/${task_id}-normalized.tsv"
scope_bin="$snapshot_root/manifests/${task_id}-scope32-after.bin"
scope_tsv="$snapshot_root/manifests/${task_id}-scope32-after.tsv"
protected_bin="$snapshot_root/manifests/${task_id}-protected-after.bin"
protected_tsv="$snapshot_root/manifests/${task_id}-protected-after.tsv"
zip_bin="$snapshot_root/manifests/${task_id}-zip-after.bin"
zip_tsv="$snapshot_root/manifests/${task_id}-zip-after.tsv"
for evidence_path in "$post_bin" "$post_tsv" "$final_bin" "$final_tsv" "$scope_bin" "$scope_tsv" "$protected_bin" "$protected_tsv" "$zip_bin" "$zip_tsv"; do
  [[ ! -e "$evidence_path" && ! -L "$evidence_path" ]] || { print -u2 "evidence path exists: $evidence_path"; exit 67; }
done

/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" "$#" "$@" "$post_bin" "$post_tsv"
/bin/chmod a-w "$post_bin" "$post_tsv"
if [[ "$task_id" == 'TASK1' || "$task_id" == TASK1_R<-> ]]; then
  /usr/bin/ruby - "$before_tsv" "$post_tsv" <<'RUBY'
before_path, post_path = ARGV
load_rows = lambda do |path|
  rows = File.readlines(path, chomp: true).map { |line| line.split("\t", -1) }
  raise "malformed rows: #{path}" unless rows.all? { |row| row.length == 6 }
  raise "duplicate rows: #{path}" unless rows.map(&:first).uniq.length == rows.length
  rows.each_with_object({}) { |row, index| index[row[0]] = row }
end
before = load_rows.call(before_path)
post = load_rows.call(post_path)
normalization_only = [
  '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md',
  '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
]
normalization_only.each do |relative|
  raise "normalization-only six-value drift: #{relative}" unless post.fetch(relative) == before.fetch(relative)
end
puts "TASK1_NORMALIZATION_ONLY_SIX_VALUES=PASS files=#{normalization_only.length}"
RUBY
fi
/bin/zsh "$normalizer" "$task_id" "$post_tsv" "$@"
/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" "$#" "$@" "$final_bin" "$final_tsv"
/usr/bin/ruby "$manifest" plan-set "$workspace_root" "$plan" scope32 "$scope_bin" "$scope_tsv"
/usr/bin/ruby "$manifest" protected "$workspace_root" "$plan" '全栈开发Prompt Chain' "$protected_bin" "$protected_tsv"
/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" 1 '全栈开发Prompt Chain.zip' "$zip_bin" "$zip_tsv"

/usr/bin/ruby - "$post_tsv" "$final_tsv" "$before_tsv" "$scope_tsv" "$@" <<'RUBY'
expected_path, final_path, before_path, scope_path, *task_targets = ARGV
parse = lambda do |path|
  rows = File.readlines(path, chomp: true).map { |line| line.split("\t", -1) }
  raise "malformed rows in #{path}" unless rows.all? { |row| row.length == 6 }
  raise "duplicate rows in #{path}" unless rows.map(&:first).uniq.length == rows.length
  rows.each_with_object({}) { |row, index| index[row[0]] = row }
end
expected = parse.call(expected_path)
final = parse.call(final_path)
before = parse.call(before_path)
scope = parse.call(scope_path)
raise 'path set drift' unless expected.keys.sort == final.keys.sort
raise 'task target set drift' unless expected.keys.sort == task_targets.sort && task_targets.uniq.length == task_targets.length
raise "scope count=#{scope.length}" unless scope.length == 32
final.each do |relative, row|
  prior = expected.fetch(relative)
  raise "not normalized: #{relative}" unless row[1] == row[3] && row[2] == row[4]
  raise "content drift: #{relative}" unless row[3] == prior[3] && row[4] == prior[4]
  raise "mode drift: #{relative}" unless row[5] == prior[5]
  raise "scope/final drift: #{relative}" unless scope.fetch(relative) == row
end
new_audit = '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md'
expected_scope = before.keys | ([new_audit] & scope.keys)
raise 'full-scope path drift' unless scope.keys.sort == expected_scope.sort
(before.keys - task_targets).each do |relative|
  raise "non-task target drift: #{relative}" unless scope.fetch(relative) == before.fetch(relative)
end
puts "TASK_NORMALIZATION=PASS task=#{File.basename(expected_path).split('-post-apply-patch').first} files=#{final.length}"
puts "TASK_SCOPE=PASS files=#{scope.length} non_task_unchanged=#{before.keys.length - (before.keys & task_targets).length}"
RUBY

for suffix in bin tsv; do
  /usr/bin/cmp -s "$snapshot_root/baseline/protected-44-before.$suffix" "$snapshot_root/manifests/${task_id}-before-protected.$suffix" || { print -u2 "pre-task protected evidence drift: $suffix"; exit 68; }
  /usr/bin/cmp -s "$snapshot_root/baseline/protected-44-before.$suffix" "$snapshot_root/manifests/${task_id}-protected-after.$suffix" || { print -u2 "protected drift during task: $suffix"; exit 69; }
  /usr/bin/cmp -s "$snapshot_root/baseline/zip-before.$suffix" "$snapshot_root/manifests/${task_id}-before-zip.$suffix" || { print -u2 "pre-task ZIP evidence drift: $suffix"; exit 70; }
  /usr/bin/cmp -s "$snapshot_root/baseline/zip-before.$suffix" "$snapshot_root/manifests/${task_id}-zip-after.$suffix" || { print -u2 "ZIP drift during task: $suffix"; exit 71; }
done

/bin/chmod a-w "$final_bin" "$final_tsv" "$scope_bin" "$scope_tsv" "$protected_bin" "$protected_tsv" "$zip_bin" "$zip_tsv"
print -r -- "TASK_EVIDENCE=SEALED task=$task_id scope=32 protected=44 zip=1"
```

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/rollback-target.zsh`. This is a dormant, one-path-at-a-time recovery primitive. Creating and syntax-checking it does not authorize its execution; every rollback still needs a separate exact user authorization.

```zsh
#!/bin/zsh
set -euo pipefail

workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'

capture_values() {
  local capture_path=$1
  CAPTURE_PATH_SIZE=$(/usr/bin/stat -f %z "$capture_path")
  CAPTURE_PATH_SHA=$(/sbin/sha256sum "$capture_path" | /usr/bin/awk '{print $1}')
  CAPTURE_CAT_SIZE=$(/bin/cat "$capture_path" | /usr/bin/wc -c | /usr/bin/tr -d ' ')
  CAPTURE_CAT_SHA=$(/bin/cat "$capture_path" | /sbin/sha256sum | /usr/bin/awk '{print $1}')
  CAPTURE_MODE=$(/usr/bin/stat -f %Lp "$capture_path")
}

require_expected() {
  local tsv=$1
  local wanted=$2
  EXPECTED_LINE=$(LC_ALL=C /usr/bin/awk -F '\t' -v path="$wanted" '
    $1 == path { print; count += 1 }
    END { if (count != 1) exit 1 }
  ' "$tsv") || { print -u2 "expected row count is not one: $wanted"; exit 70; }
  IFS=$'\t' read -r EXPECTED_PATH EXPECTED_PATH_SIZE EXPECTED_PATH_SHA EXPECTED_CAT_SIZE EXPECTED_CAT_SHA EXPECTED_MODE <<< "$EXPECTED_LINE"
  [[ "$EXPECTED_PATH" == "$wanted" && "$EXPECTED_PATH_SIZE" == <-> && "$EXPECTED_CAT_SIZE" == <-> && "$EXPECTED_PATH_SHA" != *[^0-9a-f]* && ${#EXPECTED_PATH_SHA} -eq 64 && "$EXPECTED_CAT_SHA" != *[^0-9a-f]* && ${#EXPECTED_CAT_SHA} -eq 64 && "$EXPECTED_MODE" == <-> ]] || { print -u2 "malformed expected row: $wanted"; exit 71; }
}

require_current_equals_expected() {
  local current_path=$1
  local label=$2
  [[ -f "$current_path" && ! -L "$current_path" ]] || { print -u2 "$label is not a regular file: $current_path"; exit 72; }
  capture_values "$current_path"
  [[ "$CAPTURE_PATH_SIZE" == "$EXPECTED_PATH_SIZE" && "$CAPTURE_PATH_SHA" == "$EXPECTED_PATH_SHA" && "$CAPTURE_CAT_SIZE" == "$EXPECTED_CAT_SIZE" && "$CAPTURE_CAT_SHA" == "$EXPECTED_CAT_SHA" && "$CAPTURE_MODE" == "$EXPECTED_MODE" ]] || { print -u2 "$label drift: $current_path"; exit 73; }
}

(( $# == 5 )) || { print -u2 'usage: rollback-target.zsh existing|new ROLLBACK_ID EXPECTED_POSTIMAGE_TSV EXPECTED_POSTIMAGE_TSV_SHA256 RELATIVE_PATH'; exit 64; }
kind=$1
rollback_id=$2
expected_tsv=${3:A}
expected_tsv_sha=$4
relative_path=$5
[[ "${ROLLBACK_QUIESCENCE_CONFIRMED:-no}" == 'yes' ]] || { print -u2 'rollback requires separately authorized, currently confirmed target quiescence'; exit 65; }
[[ "$kind" == 'existing' || "$kind" == 'new' ]] || { print -u2 "invalid rollback kind: $kind"; exit 65; }
[[ -n "$rollback_id" && "$rollback_id" != *[^A-Z0-9_]* ]] || { print -u2 "invalid rollback id: $rollback_id"; exit 66; }
[[ "$relative_path" == '全栈开发Prompt Chain/'* && "$relative_path" != *'/../'* && "$relative_path" != '../'* && "$relative_path" != *$'\n'* && "$relative_path" != *$'\t'* ]] || { print -u2 "unsafe relative path: $relative_path"; exit 67; }
[[ "$expected_tsv" == "$snapshot_root/manifests/"* ]] || { print -u2 "postimage TSV outside sealed manifests: $expected_tsv"; exit 68; }
[[ -f "$expected_tsv" && ! -L "$expected_tsv" ]] || { print -u2 "invalid postimage TSV: $expected_tsv"; exit 69; }
[[ "$expected_tsv_sha" != *[^0-9a-f]* && ${#expected_tsv_sha} -eq 64 ]] || { print -u2 'invalid authorized postimage TSV hash'; exit 70; }
[[ ! -w "$expected_tsv" ]] || { print -u2 'postimage TSV is not sealed'; exit 71; }
actual_expected_tsv_sha=$(/bin/cat "$expected_tsv" | /sbin/sha256sum | /usr/bin/awk '{print $1}')
[[ "$actual_expected_tsv_sha" == "$expected_tsv_sha" ]] || { print -u2 "authorized postimage TSV hash drift: expected=$expected_tsv_sha actual=$actual_expected_tsv_sha"; exit 72; }

target_path="$workspace_root/$relative_path"
[[ "${target_path:A}" == "$workspace_root/"* ]] || { print -u2 "target escapes workspace: $relative_path"; exit 74; }
require_expected "$expected_tsv" "$relative_path"
require_current_equals_expected "$target_path" 'current postimage'
[[ "$(/usr/bin/stat -f %d "${target_path:h}")" == "$(/usr/bin/stat -f %d "$snapshot_root")" ]] || { print -u2 'workspace and snapshot are on different filesystems'; exit 75; }

if [[ "$kind" == 'new' ]]; then
  [[ "$relative_path" == '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md' ]] || { print -u2 'new rollback only permits the audit document'; exit 76; }
  rollback_path="$snapshot_root/new-file-rollback/$rollback_id/$relative_path"
  [[ ! -e "$rollback_path" && ! -L "$rollback_path" ]] || { print -u2 "rollback destination exists: $rollback_path"; exit 77; }
  /bin/mkdir -p "${rollback_path:h}"
  require_current_equals_expected "$target_path" 'pre-move postimage'
  /usr/bin/python3 - "$target_path" "$rollback_path" <<'PY'
import ctypes
import os
import sys

RENAME_EXCL = 0x00000004
libc = ctypes.CDLL(None, use_errno=True)
renamex_np = libc.renamex_np
renamex_np.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
renamex_np.restype = ctypes.c_int
if renamex_np(os.fsencode(sys.argv[1]), os.fsencode(sys.argv[2]), RENAME_EXCL) != 0:
    error_number = ctypes.get_errno()
    raise OSError(error_number, os.strerror(error_number), sys.argv[1], sys.argv[2])
PY
  [[ ! -e "$target_path" && ! -L "$target_path" ]] || { print -u2 "new target still exists after recoverable move: $relative_path"; exit 78; }
  require_current_equals_expected "$rollback_path" 'moved new-file postimage'
  print -r -- "ROLLBACK_NEW=PASS path=$relative_path retained=$rollback_path"
  exit 0
fi

[[ "$relative_path" != '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md' ]] || { print -u2 'audit document has no existing preimage'; exit 79; }
preimage_path="$snapshot_root/preimage/$relative_path"
[[ "${preimage_path:A}" == "$snapshot_root/preimage/"* ]] || { print -u2 "preimage escapes snapshot: $relative_path"; exit 80; }
[[ -f "$preimage_path" && ! -L "$preimage_path" ]] || { print -u2 "missing regular preimage: $relative_path"; exit 81; }

preimage_tsv="$snapshot_root/baseline/preimage-31.tsv"
post_path_size=$EXPECTED_PATH_SIZE
post_path_sha=$EXPECTED_PATH_SHA
post_cat_size=$EXPECTED_CAT_SIZE
post_cat_sha=$EXPECTED_CAT_SHA
post_mode=$EXPECTED_MODE
require_expected "$preimage_tsv" "$relative_path"
require_current_equals_expected "$preimage_path" 'sealed preimage'
pre_path_size=$EXPECTED_PATH_SIZE
pre_path_sha=$EXPECTED_PATH_SHA
pre_cat_size=$EXPECTED_CAT_SIZE
pre_cat_sha=$EXPECTED_CAT_SHA
pre_mode=$EXPECTED_MODE

EXPECTED_PATH_SIZE=$post_path_size
EXPECTED_PATH_SHA=$post_path_sha
EXPECTED_CAT_SIZE=$post_cat_size
EXPECTED_CAT_SHA=$post_cat_sha
EXPECTED_MODE=$post_mode
require_current_equals_expected "$target_path" 'pre-stage postimage'

stage_path=$(/usr/bin/mktemp "${target_path:h}/.pm-skill-rollback.XXXXXX")
/bin/cp -c -p "$preimage_path" "$stage_path"
EXPECTED_PATH_SIZE=$pre_path_size
EXPECTED_PATH_SHA=$pre_path_sha
EXPECTED_CAT_SIZE=$pre_cat_size
EXPECTED_CAT_SHA=$pre_cat_sha
EXPECTED_MODE=$pre_mode
require_current_equals_expected "$stage_path" 'rollback staging preimage'

EXPECTED_PATH_SIZE=$post_path_size
EXPECTED_PATH_SHA=$post_path_sha
EXPECTED_CAT_SIZE=$post_cat_size
EXPECTED_CAT_SHA=$post_cat_sha
EXPECTED_MODE=$post_mode
require_current_equals_expected "$target_path" 'pre-swap postimage'
conflict_path="$snapshot_root/rollback-conflicts/$rollback_id/$relative_path"
[[ ! -e "$conflict_path" && ! -L "$conflict_path" ]] || { print -u2 "rollback conflict destination exists: $conflict_path"; exit 82; }
/bin/mkdir -p "${conflict_path:h}"
/usr/bin/python3 - "$stage_path" "$target_path" "$conflict_path" <<'PY'
import ctypes
import os
import sys

RENAME_SWAP = 0x00000002
RENAME_EXCL = 0x00000004
libc = ctypes.CDLL(None, use_errno=True)
renamex_np = libc.renamex_np
renamex_np.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
renamex_np.restype = ctypes.c_int
stage, target, conflict = map(os.fsencode, sys.argv[1:4])
if renamex_np(stage, target, RENAME_SWAP) != 0:
    error_number = ctypes.get_errno()
    raise OSError(error_number, os.strerror(error_number), sys.argv[1], sys.argv[2])
if renamex_np(stage, conflict, RENAME_EXCL) != 0:
    error_number = ctypes.get_errno()
    raise OSError(error_number, os.strerror(error_number), sys.argv[1], sys.argv[3])
PY

EXPECTED_PATH_SIZE=$post_path_size
EXPECTED_PATH_SHA=$post_path_sha
EXPECTED_CAT_SIZE=$post_cat_size
EXPECTED_CAT_SHA=$post_cat_sha
EXPECTED_MODE=$post_mode
require_current_equals_expected "$conflict_path" 'retained swap-time postimage'
EXPECTED_PATH_SIZE=$pre_path_size
EXPECTED_PATH_SHA=$pre_path_sha
EXPECTED_CAT_SIZE=$pre_cat_size
EXPECTED_CAT_SHA=$pre_cat_sha
EXPECTED_MODE=$pre_mode
require_current_equals_expected "$target_path" 'restored preimage'
print -r -- "ROLLBACK_EXISTING=PASS path=$relative_path restored=$preimage_path retained=$conflict_path"
```

The script deliberately has no batch mode and no automatic invocation. Each authorization must name the exact target, rollback ID, sealed postimage TSV and its SHA-256, and must separately confirm `ROLLBACK_QUIESCENCE_CONFIRMED=yes` while all writers pause that target. A pre-check failure changes nothing. This helper is not a lock or compare-and-swap: a race after the final check can leave the swap-time version at the staging/conflict path instead of the original workspace pathname. Verification then fails and execution stops; do not claim the concurrent version stayed at its pathname, delete either version, or continue to another path.

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/seal-task9-generation.rb`. It is the only operation allowed to publish a Task 9 terminal state; `COMPLETED` and `INVALIDATED` compete for the same exclusive `TERMINAL.tsv` path:

```ruby
#!/usr/bin/ruby
require 'base64'
require 'digest'
require 'find'
require 'json'
require 'open3'

SNAPSHOT = '/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
CONTROL_FILES = %w[TERMINAL.tsv terminal-intent.tsv generation-seal.tsv].freeze
HEADER = %w[
  Schema Run_ID State Reason_Code Required_Action Owning_Task Candidate_ID Next_Evidence_ID
  Rework_Reservation_Path Rework_Reservation_SHA256 Artifact_Path
  Input_Scope_TSV Input_Scope_SHA256 Review_Input_SHA256 Target_Manifest_SHA256
  Candidate_Universe_SHA256 Ablation_Ledger_SHA256 Generation_Seal_SHA256
].freeze
INPUT_HEADER = %w[Schema Input_ID Kind Canonical_Path Bytes SHA256].freeze
IDENTITY_HEADER = %w[
  Schema Run_ID Coordinator_ID Review_Input_Path Review_Input_SHA256 Input_Count
  Target_Count Target_Manifest_SHA256 Candidate_Universe_SHA256 Ablation_Ledger_SHA256
].freeze
ORACLE_HEADER = %w[
  Schema Run_ID Review_Kind Reviewer_ID Reviewer_Instance_ID Oracle_ID Review_Input_Path
  Review_Input_SHA256 Exit_Status Stdout_B64 Stdout_SHA256 Stderr_Bytes
].freeze
REVIEW_INDEX_HEADER = %w[
  Review_Kind Report_Path Report_SHA256 Oracle_Receipt_Path Oracle_Receipt_SHA256
  Reviewer_ID Reviewer_Instance_ID Critical Important Minor Verdict
].freeze
CLOSEOUT_HEADER = %w[
  Schema Run_ID Review_Input_Path Review_Input_SHA256 Report_Count Review_Index_SHA256
  Distinct_Reviewer_ID_Count Distinct_Reviewer_Instance_Count Critical_Count
  Important_Count Minor_Count Oracle_ID Oracle_Output_SHA256
  Target_Manifest_SHA256 Protected_Manifest_SHA256 Zip_Manifest_SHA256
  Candidate_Universe_SHA256 Ablation_Ledger_SHA256 Completion_Eligible
].freeze
TOKEN_HEADER = %w[
  Schema Run_ID Review_Input_SHA256 Target_Manifest_SHA256 Candidate_Universe_SHA256
  Ablation_Ledger_SHA256 Report_Count Review_Index_SHA256 Distinct_Reviewer_ID_Count
  Distinct_Reviewer_Instance_Count Critical_Count Important_Count Closeout_SHA256 Eligible
].freeze
READY_HEADER = %w[
  Schema Run_ID Review_Input_SHA256 Closeout_SHA256 Oracle_ID Oracle_Output_SHA256 Eligible
].freeze
ROUTING_HEADER = %w[
  Schema Run_ID Reason_Code Required_Action Owning_Task Candidate_ID Artifact_Path Blocking_Findings_B64
].freeze

class StrictObject < Hash
  def []=(key, value)
    raise "duplicate JSON key: #{key}" if key?(key)
    super
  end
end

def strict_json(bytes, label)
  JSON.parse(bytes, object_class: StrictObject, create_additions: false, allow_nan: false)
rescue JSON::ParserError, TypeError => error
  raise "invalid JSON in #{label}: #{error.message}"
end
REVIEW_KEYS = %w[
  schema run_id review_kind reviewer_id reviewer_instance_id review_input_path
  review_input_sha256 oracle_id oracle_receipt_path oracle_receipt_sha256
  verdict counts summary findings
].freeze
FINDING_KEYS = %w[
  finding_id severity requirement_ref owning_task candidate_id artifact_path line
  required_action summary evidence minimal_fix
].freeze
ROLE_FILES = {
  'spec' => ['spec-oracle.tsv', 'spec-review.json'],
  'safety' => ['safety-oracle.tsv', 'safety-review.json'],
  'ablation' => ['ablation-oracle.tsv', 'ablation-review.json']
}.freeze
RECEIPT_KEYS = %w[
  Schema Run_ID Package_Status Universe_Valid Decisions_Valid Applied_Status
  Universe_SHA256 Oracle_SHA256 Hunk_SHA256 Crosswalk_SHA256 Ledger_SHA256
  Target_Manifest_SHA256 Diff_SHA256 Prior_History_SHA256 Pending_Count
  First_Pending_Candidate First_Pending_Owner Failure_Code Details_B64
].freeze
ORACLE_ID = 'TASK9_REVIEW_ORACLE_V1'

class StrictObject < Hash
  def []=(key, value)
    raise "duplicate JSON key: #{key}" if key?(key)
    super
  end
end

def strict_json(bytes, label)
  JSON.parse(bytes, object_class: StrictObject, create_additions: false, allow_nan: false)
rescue JSON::ParserError, TypeError => error
  raise "invalid JSON in #{label}: #{error.message}"
end

def sha(bytes)
  Digest::SHA256.hexdigest(bytes)
end

def read_regular(path, required_mode = nil)
  before = File.lstat(path)
  raise "unsafe regular file: #{path}" unless before.file? && !before.symlink? && before.nlink == 1
  raise "file mode drift: #{path}" if required_mode && (before.mode & 0o777) != required_mode
  flags = File::RDONLY
  flags |= File::NOFOLLOW if File.const_defined?(:NOFOLLOW)
  File.open(path, flags) do |file|
    opened = file.stat
    raise "opened inode drift: #{path}" unless [before.dev, before.ino] == [opened.dev, opened.ino]
    bytes = file.read.b
    after = File.lstat(path)
    raise "pathname replaced while reading: #{path}" unless [opened.dev, opened.ino] == [after.dev, after.ino]
    bytes
  end
end

def parse_tsv(bytes, header, label)
  text = bytes.dup.force_encoding(Encoding::UTF_8)
  raise "invalid TSV encoding/newline: #{label}" unless text.valid_encoding? && text.end_with?("\n")
  lines = text.lines(chomp: true)
  raise "TSV header drift: #{label}" unless lines.shift&.split("\t", -1) == header
  lines.map.with_index(2) do |line, number|
    fields = line.split("\t", -1)
    raise "TSV field-count drift: #{label}:#{number}" unless fields.length == header.length
    Hash[header.zip(fields)]
  end
end

def one_tsv(path, header, required_mode = nil)
  rows = parse_tsv(read_regular(path, required_mode), header, path)
  raise "TSV row-count drift: #{path}" unless rows.length == 1
  rows.first
end

def verify_helpers
  expected = %w[
    capture-and-normalize.zsh four-value-manifest.rb guard-workspace.zsh
    normalize-targets.zsh rollback-target.zsh seal-task9-generation.rb verify-chain.rb
  ]
  manifest = File.join(SNAPSHOT, 'helper-manifest.tsv')
  lines = read_regular(manifest, 0o400).lines(chomp: true)
  raise 'helper manifest header drift' unless lines.shift == "Schema\tName\tBytes\tSHA256\tMode"
  rows = lines.map { |line| line.split("\t", -1) }
  raise 'helper manifest set/order drift' unless rows.map { |row| row[1] } == expected
  rows.each do |schema, name, bytes, hash, mode|
    body = read_regular(File.join(SNAPSHOT, name))
    actual_mode = (File.lstat(File.join(SNAPSHOT, name)).mode & 0o777).to_s(8)
    raise "helper manifest binding drift: #{name}" unless schema == 'task0-helper-manifest/v1' &&
      body.bytesize.to_s == bytes && sha(body) == hash && actual_mode == mode
  end
end

def write_or_verify(path, bytes)
  begin
    File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
      file.write(bytes)
      file.flush
      file.fsync
    end
  rescue Errno::EEXIST
    stat = File.lstat(path)
    abort "unsafe recovery target: #{path}" unless stat.file? && !stat.symlink?
    abort "recovery content conflict: #{path}" unless File.binread(path) == bytes
  end
end

def collect_tree(run_root, require_sealed: false)
  rows = []
  paths = []
  Find.find(run_root) do |path|
    stat = File.lstat(path)
    raise "symlink in generation: #{path}" if stat.symlink?
    raise "mode drift after seal: #{path}" if require_sealed && (stat.mode & 0o777) != (stat.directory? ? 0o500 : 0o400)
    if stat.directory?
      paths << path
      next
    end
    raise "special file in generation: #{path}" unless stat.file?
    paths << path
    relative = path.delete_prefix(run_root + File::SEPARATOR)
    next if CONTROL_FILES.include?(relative)
    bytes = read_regular(path, require_sealed ? 0o400 : nil)
    rows << [relative, bytes.bytesize.to_s, sha(bytes)]
  end
  rows.sort_by! { |row| row[0].b }
  raise 'empty generation' if rows.empty?
  [rows, paths]
end

def seal_bytes_for(rows)
  "Relative_Path\tBytes\tSHA256\n" + rows.map { |row| row.join("\t") + "\n" }.join
end

def validate_manifests_set(run_root)
  set_path = File.join(run_root, '10-input', 'manifests-set.tsv')
  header = %w[Schema Relative_Path Bytes SHA256 Mode]
  rows = parse_tsv(read_regular(set_path, 0o400), header, set_path)
  root = File.join(SNAPSHOT, 'manifests')
  actual = []
  Find.find(root) do |path|
    next if path == root
    stat = File.lstat(path)
    raise "unsafe manifest node: #{path}" if stat.symlink? || !stat.file?
    bytes = read_regular(path)
    actual << {
      'Schema' => 'task9-manifests-set/v1',
      'Relative_Path' => path.delete_prefix(root + File::SEPARATOR),
      'Bytes' => bytes.bytesize.to_s,
      'SHA256' => sha(bytes),
      'Mode' => (stat.mode & 0o777).to_s(8)
    }
  end
  actual.sort_by! { |row| row['Relative_Path'].b }
  raise 'manifest directory set/content drift' unless rows == actual
end

def candidate_index(package)
  path = File.join(package, 'candidate-universe.tsv')
  lines = read_regular(path, 0o400).lines(chomp: true)
  header = lines.shift&.split("\t", -1)
  raise 'candidate universe header drift' unless header&.include?('Candidate_ID') && header.include?('Owning_task')
  rows = lines.map do |line|
    values = line.split("\t", -1)
    raise 'candidate universe field-count drift' unless values.length == header.length
    Hash[header.zip(values)]
  end
  raise 'candidate universe ID collision' unless rows.map { |row| row['Candidate_ID'] }.uniq.length == rows.length
  rows.each_with_object({}) { |row, index| index[row['Candidate_ID']] = row }
end

def validate_input_manifest(run_root)
  validate_manifests_set(run_root)
  path = File.join(run_root, '40-review-input', 'review-input.tsv')
  rows = parse_tsv(read_regular(path, 0o400), INPUT_HEADER, path)
  raise 'empty review input' if rows.empty?
  ids = rows.map { |row| row['Input_ID'] }
  paths = rows.map { |row| row['Canonical_Path'] }
  raise 'review input ID order/uniqueness drift' unless ids == ids.sort_by(&:b) && ids.uniq.length == ids.length
  raise 'review input path collision' unless paths.uniq.length == paths.length
  rows.each do |row|
    raise 'review input schema/kind drift' unless row['Schema'] == 'task9-review-input/v1' && %w[target evidence].include?(row['Kind'])
    pathname = row['Canonical_Path']
    raise "non-canonical review path: #{pathname}" unless File.absolute_path(pathname) == pathname && File.realpath(pathname) == pathname
    bytes = read_regular(pathname)
    raise "review input byte/hash drift: #{pathname}" unless row['Bytes'] == bytes.bytesize.to_s && row['SHA256'] == sha(bytes)
  end
  target_rows = rows.select { |row| row['Kind'] == 'target' }
  manifest_rows = read_regular(File.join(run_root, '20-final', 'targets-32-final.tsv'), 0o400).lines(chomp: true).map { |line| line.split("\t", -1) }
  raise 'target manifest shape drift' unless manifest_rows.length == 32 && manifest_rows.all? { |row| row.length == 6 }
  expected_targets = manifest_rows.sort_by { |row| row[0].b }.each_with_index.map do |row, index|
    target = File.realpath(File.join(run_root, '20-final', 'content', row[0]))
    bytes = read_regular(target, 0o400)
    raise "target frozen-content drift: #{row[0]}" unless [bytes.bytesize.to_s, sha(bytes)] == row[3, 2]
    {
      'Schema' => 'task9-review-input/v1', 'Input_ID' => format('T%03d:%s', index + 1, row[0]),
      'Kind' => 'target', 'Canonical_Path' => target, 'Bytes' => bytes.bytesize.to_s, 'SHA256' => sha(bytes)
    }
  end
  raise 'review target set drift' unless target_rows == expected_targets
  collect_files = lambda do |root|
    files = []
    Find.find(root) do |candidate|
      stat = File.lstat(candidate)
      raise "unsafe review evidence node: #{candidate}" if stat.symlink? || (!stat.directory? && !stat.file?)
      files << candidate if stat.file?
    end
    files
  end
  evidence = %w[
    four-value-manifest.rb guard-workspace.zsh normalize-targets.zsh
    capture-and-normalize.zsh rollback-target.zsh seal-task9-generation.rb verify-chain.rb
    helper-manifest.tsv
  ].map { |name| File.join(SNAPSHOT, name) }
  evidence.concat(collect_files.call(File.join(SNAPSHOT, 'baseline')))
  evidence.concat(collect_files.call(File.join(SNAPSHOT, 'manifests')))
  %w[00-meta 10-input].each { |name| evidence.concat(collect_files.call(File.join(run_root, name))) }
  final_root = File.join(run_root, '20-final')
  collect_files.call(final_root).each do |candidate|
    next if candidate.start_with?(File.join(final_root, 'content') + File::SEPARATOR)
    evidence << candidate
  end
  evidence.concat(collect_files.call(File.join(run_root, '30-ablation')))
  evidence << File.join(run_root, '40-review-input', 'review-contract.json')
  evidence << File.join(run_root, '40-review-input', 'task9-review-tools.rb')
  evidence = evidence.map { |candidate| File.realpath(candidate) }.uniq.sort_by(&:b)
  expected_evidence = evidence.each_with_index.map do |candidate, index|
    bytes = read_regular(candidate)
    {
      'Schema' => 'task9-review-input/v1',
      'Input_ID' => format('E%04d:%s', index + 1, candidate.delete_prefix(SNAPSHOT + File::SEPARATOR)),
      'Kind' => 'evidence', 'Canonical_Path' => candidate,
      'Bytes' => bytes.bytesize.to_s, 'SHA256' => sha(bytes)
    }
  end
  raise 'review evidence exact closure drift' unless rows.select { |row| row['Kind'] == 'evidence' } == expected_evidence
  rows
end

def validate_reviews(run_root, require_clear: false)
  rows = validate_input_manifest(run_root)
  allowed_paths = rows.map { |row| row['Canonical_Path'] }
  input_path = File.join(run_root, '40-review-input', 'review-input.tsv')
  identity = one_tsv(File.join(run_root, '40-review-input', 'review-input.identity.tsv'), IDENTITY_HEADER, 0o400)
  package = File.join(run_root, '30-ablation', 'published')
  raise 'published package missing or pending package coexists' unless File.directory?(package) && !File.symlink?(package) &&
    !File.exist?(File.join(run_root, '30-ablation', 'pending-history')) && !File.symlink?(File.join(run_root, '30-ablation', 'pending-history'))
  raise 'review identity drift' unless identity['Schema'] == 'task9-review-input-identity/v1' &&
    identity['Run_ID'] == File.basename(run_root) && identity['Review_Input_Path'] == input_path &&
    identity['Review_Input_SHA256'] == sha(read_regular(input_path, 0o400)) &&
    identity['Input_Count'] == rows.length.to_s && identity['Target_Count'] == rows.count { |row| row['Kind'] == 'target' }.to_s &&
    identity['Target_Manifest_SHA256'] == sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400)) &&
    identity['Candidate_Universe_SHA256'] == sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400)) &&
    identity['Ablation_Ledger_SHA256'] == sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
  raise 'invalid coordinator identity' unless identity['Coordinator_ID'].match?(/\A[A-Za-z0-9._:\/-]+\z/)

  reviews_root = File.join(run_root, '50-reviews')
  expected_files = ROLE_FILES.values.flatten.sort_by(&:b)
  raise 'review file-set drift' unless Dir.children(reviews_root).sort_by(&:b) == expected_files
  oracle_output = "TASK9_REVIEW_ORACLE=PASS run=#{File.basename(run_root)} review_input_sha256=#{identity['Review_Input_SHA256']}\n"
  candidates = candidate_index(package)
  reports = []
  finding_ids = []
  ROLE_FILES.each do |role, (oracle_name, report_name)|
    oracle_path = File.join(reviews_root, oracle_name)
    report_path = File.join(reviews_root, report_name)
    oracle = one_tsv(oracle_path, ORACLE_HEADER, 0o400)
    decoded = Base64.strict_decode64(oracle['Stdout_B64'])
    raise "non-canonical oracle base64: #{role}" unless Base64.strict_encode64(decoded) == oracle['Stdout_B64']
    raise "oracle receipt drift: #{role}" unless oracle['Schema'] == 'task9-review-oracle/v1' &&
      oracle['Run_ID'] == File.basename(run_root) && oracle['Review_Kind'] == role && oracle['Oracle_ID'] == ORACLE_ID &&
      oracle['Review_Input_Path'] == input_path && oracle['Review_Input_SHA256'] == identity['Review_Input_SHA256'] &&
      oracle['Exit_Status'] == '0' && oracle['Stderr_Bytes'] == '0' && decoded == oracle_output && oracle['Stdout_SHA256'] == sha(decoded)
    report = strict_json(read_regular(report_path, 0o400), report_path)
    raise "review keys drift: #{role}" unless report.is_a?(Hash) && report.keys.sort == REVIEW_KEYS.sort
    raise "review identity drift: #{role}" unless report['schema'] == 'task9-review-report/v1' &&
      report['run_id'] == File.basename(run_root) && report['review_kind'] == role &&
      report['reviewer_id'] == oracle['Reviewer_ID'] && report['reviewer_instance_id'] == oracle['Reviewer_Instance_ID'] &&
      report['review_input_path'] == input_path && report['review_input_sha256'] == identity['Review_Input_SHA256'] &&
      report['oracle_id'] == ORACLE_ID && report['oracle_receipt_path'] == oracle_path &&
      report['oracle_receipt_sha256'] == sha(read_regular(oracle_path, 0o400))
    raise "review summary drift: #{role}" unless report['summary'].is_a?(String) && !report['summary'].empty?
    counts = report['counts']
    raise "review count schema drift: #{role}" unless counts.is_a?(Hash) && counts.keys.sort == %w[Critical Important Minor].sort &&
      counts.values.all? { |value| value.is_a?(Integer) && value >= 0 }
    raise "findings schema drift: #{role}" unless report['findings'].is_a?(Array)
    derived = { 'Critical' => 0, 'Important' => 0, 'Minor' => 0 }
    report['findings'].each do |finding|
      raise "finding keys drift: #{role}" unless finding.is_a?(Hash) && finding.keys.sort == FINDING_KEYS.sort
      severity = finding['severity']
      action = finding['required_action']
      raise "finding severity drift: #{role}" unless derived.key?(severity)
      derived[severity] += 1
      raise "finding ID drift: #{role}" unless finding['finding_id'].is_a?(String) &&
        finding['finding_id'].match?(/\A#{Regexp.escape(File.basename(run_root))}:#{role}:#{Regexp.escape(report['reviewer_instance_id'])}:F\d{3}\z/)
      raise "finding artifact drift: #{role}" unless allowed_paths.include?(finding['artifact_path'])
      raise "finding line drift: #{role}" unless finding['line'].nil? || (finding['line'].is_a?(Integer) && finding['line'].positive?)
      raise "finding text drift: #{role}" unless %w[requirement_ref summary evidence minimal_fix].all? { |key| finding[key].is_a?(String) && !finding[key].empty? }
      raise "minor finding action drift: #{role}" if severity == 'Minor' && action != 'NONE'
      raise "blocking finding action drift: #{role}" if %w[Critical Important].include?(severity) && !%w[REWORK_CONTENT REBUILD_EVIDENCE STOP].include?(action)
      if action == 'REWORK_CONTENT' || finding['candidate_id'] != 'NONE'
        candidate = candidates.fetch(finding['candidate_id']) { raise "finding candidate missing: #{role}" }
        raise "finding owner mismatch: #{role}" unless finding['owning_task'] == candidate['Owning_task']
      else
        raise "finding owner/candidate drift: #{role}" unless finding['owning_task'] == 'NONE' && finding['candidate_id'] == 'NONE'
      end
      raise "non-rework routing fields drift: #{role}" if %w[REBUILD_EVIDENCE STOP].include?(action) &&
        (finding['owning_task'] != 'NONE' || finding['candidate_id'] != 'NONE')
    end
    expected_verdict = if derived['Critical'].positive? || derived['Important'].positive?
                         'BLOCKED'
                       elsif derived['Minor'].positive?
                         'PASS_WITH_MINOR'
                       else
                         'PASS'
                       end
    raise "review counts/verdict drift: #{role}" unless counts == derived && report['verdict'] == expected_verdict
    raise "blocking review in completion: #{role}" if require_clear && (derived['Critical'].positive? || derived['Important'].positive?)
    finding_ids.concat(report['findings'].map { |finding| finding['finding_id'] })
    reports << [role, report_path, oracle_path, report]
  end
  raise 'global finding ID collision' unless finding_ids.uniq.length == finding_ids.length
  reviewer_ids = reports.map { |entry| entry[3]['reviewer_id'] }
  instance_ids = reports.map { |entry| entry[3]['reviewer_instance_id'] }
  raise 'reviewer identity cardinality drift' unless reviewer_ids.uniq.length == 3 && instance_ids.uniq.length == 3
  raise 'coordinator reviewed own work' if reviewer_ids.include?(identity['Coordinator_ID'])
  [reports, identity, oracle_output]
end

def validate_completion(run_root, supplied, create_ready: false)
  reports, identity, oracle_output = validate_reviews(run_root, require_clear: true)
  package = File.join(run_root, '30-ablation', 'published')
  actual = [
    identity['Review_Input_SHA256'],
    sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400)),
    sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400)),
    sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
  ]
  raise 'completed hash argument drift' unless supplied == actual && supplied.all? { |value| value.match?(/\A[0-9a-f]{64}\z/) }
  closeout_root = File.join(run_root, '60-closeout')
  base_closeout = %w[
    closeout-oracle.txt closeout.tsv completion-token.tsv protected-44-closeout.bin
    protected-44-closeout.tsv review-index.tsv targets-32-closeout.bin
    targets-32-closeout.tsv zip-closeout.bin zip-closeout.tsv
  ].sort_by(&:b)
  actual_closeout = Dir.children(closeout_root).sort_by(&:b)
  full_closeout = (base_closeout + ['terminal-ready.tsv']).sort_by(&:b)
  raise 'completed closeout file-set drift' unless create_ready ? [base_closeout, full_closeout].include?(actual_closeout) : actual_closeout == full_closeout
  index_rows = reports.map do |role, report_path, oracle_path, report|
    [role, report_path, sha(read_regular(report_path, 0o400)), oracle_path,
     sha(read_regular(oracle_path, 0o400)), report['reviewer_id'], report['reviewer_instance_id'],
     report['counts']['Critical'].to_s, report['counts']['Important'].to_s,
     report['counts']['Minor'].to_s, report['verdict']]
  end
  index_bytes = REVIEW_INDEX_HEADER.join("\t") + "\n" + index_rows.map { |row| row.join("\t") + "\n" }.join
  raise 'review index drift' unless read_regular(File.join(closeout_root, 'review-index.tsv'), 0o400) == index_bytes
  index_sha = sha(index_bytes)
  minor = reports.inject(0) { |sum, entry| sum + entry[3]['counts']['Minor'] }
  reviewer_ids = reports.map { |entry| entry[3]['reviewer_id'] }
  instance_ids = reports.map { |entry| entry[3]['reviewer_instance_id'] }
  pairs = {
    'targets-32-closeout.bin' => 'targets-32-final.bin', 'targets-32-closeout.tsv' => 'targets-32-final.tsv',
    'protected-44-closeout.bin' => 'protected-44-final.bin', 'protected-44-closeout.tsv' => 'protected-44-final.tsv',
    'zip-closeout.bin' => 'zip-final.bin', 'zip-closeout.tsv' => 'zip-final.tsv'
  }
  pairs.each do |current, sealed|
    raise "completed manifest drift: #{current}" unless read_regular(File.join(closeout_root, current), 0o400) ==
      read_regular(File.join(run_root, '20-final', sealed), 0o400)
  end
  closeout_path = File.join(closeout_root, 'closeout.tsv')
  closeout_bytes = read_regular(closeout_path, 0o400)
  closeout = one_tsv(closeout_path, CLOSEOUT_HEADER, 0o400)
  expected_closeout_values = [
    'task9-closeout/v1', File.basename(run_root), identity['Review_Input_Path'], actual[0], '3', index_sha,
    reviewer_ids.uniq.length.to_s, instance_ids.uniq.length.to_s, '0', '0', minor.to_s,
    ORACLE_ID, sha(oracle_output), actual[1],
    sha(read_regular(File.join(closeout_root, 'protected-44-closeout.bin'), 0o400)),
    sha(read_regular(File.join(closeout_root, 'zip-closeout.bin'), 0o400)), actual[2], actual[3], 'true'
  ]
  raise 'closeout row drift' unless closeout == Hash[CLOSEOUT_HEADER.zip(expected_closeout_values)]
  raise 'closeout oracle drift' unless read_regular(File.join(closeout_root, 'closeout-oracle.txt'), 0o400) == oracle_output
  token = one_tsv(File.join(closeout_root, 'completion-token.tsv'), TOKEN_HEADER, 0o400)
  expected_token = [
    'task9-completion-token/v1', File.basename(run_root), *actual, '3', index_sha, '3', '3', '0', '0', sha(closeout_bytes), 'true'
  ]
  raise 'completion token drift' unless token == Hash[TOKEN_HEADER.zip(expected_token)]
  expected_ready = ['task9-terminal-ready/v1', File.basename(run_root), actual[0], sha(closeout_bytes), ORACLE_ID, sha(oracle_output), 'true']
  ready_path = File.join(closeout_root, 'terminal-ready.tsv')
  ready_bytes = READY_HEADER.join("\t") + "\n" + expected_ready.join("\t") + "\n"
  if create_ready
    write_or_verify(ready_path, ready_bytes)
    File.open(closeout_root, File::RDONLY) { |directory| directory.fsync }
    File.chmod(0o500, closeout_root)
  end
  raise 'terminal-ready file-set drift' unless Dir.children(closeout_root).sort_by(&:b) == full_closeout
  ready = one_tsv(ready_path, READY_HEADER, 0o400)
  raise 'terminal-ready receipt drift' unless ready == Hash[READY_HEADER.zip(expected_ready)]
  actual
end

def parse_receipt(path)
  pairs = read_regular(path, 0o400).lines(chomp: true).map do |line|
    key, value = line.split('=', 2)
    raise "malformed receipt: #{path}" unless key && value && !value.empty?
    [key, value]
  end
  raise "receipt key/order drift: #{path}" unless pairs.map(&:first) == RECEIPT_KEYS && pairs.map(&:first).uniq.length == pairs.length
  pairs.to_h
end

def decode_canonical_json(value, label)
  decoded = Base64.strict_decode64(value)
  raise "non-canonical base64: #{label}" unless Base64.strict_encode64(decoded) == value
  [decoded, strict_json(decoded, label)]
end

def expected_review_route(run_root, reports)
  blocking = reports.flat_map { |role, _report_path, _oracle_path, report| report['findings'].map { |finding| [role, finding] } }
                    .select { |_role, finding| %w[Critical Important].include?(finding['severity']) }
  raise 'review route has no blockers' if blocking.empty?
  severity_order = { 'Critical' => 0, 'Important' => 1 }
  role_order = { 'spec' => 0, 'safety' => 1, 'ablation' => 2 }
  ordered = blocking.sort_by { |role, finding| [severity_order.fetch(finding['severity']), role_order.fetch(role), finding['finding_id'].b] }
  reason_role = if blocking.any? { |role, _finding| role == 'ablation' }
                  'ablation'
                elsif blocking.any? { |role, _finding| role == 'safety' }
                  'safety'
                else
                  'spec'
                end
  actions = blocking.map { |_role, finding| finding['required_action'] }
  pairs = blocking.select { |_role, finding| finding['required_action'] == 'REWORK_CONTENT' }
                  .map { |_role, finding| [finding['owning_task'], finding['candidate_id']] }.uniq
  action, owner, candidate = if actions.include?('STOP')
                               ['STOP', 'NONE', 'NONE']
                             elsif actions.all? { |value| value == 'REBUILD_EVIDENCE' }
                               ['REBUILD_EVIDENCE', 'NONE', 'NONE']
                             elsif actions.all? { |value| value == 'REWORK_CONTENT' } && pairs.length == 1
                               ['REWORK_CONTENT', pairs.first[0], pairs.first[1]]
                             else
                               ['STOP', 'NONE', 'NONE']
                             end
  details = JSON.generate(ordered.map do |role, finding|
    { 'role' => role, 'finding_id' => finding['finding_id'], 'severity' => finding['severity'], 'required_action' => finding['required_action'] }
  end) + "\n"
  {
    'Schema' => 'task9-failure-routing/v1', 'Run_ID' => File.basename(run_root),
    'Reason_Code' => "#{reason_role.upcase}_REVIEW_BLOCKED", 'Required_Action' => action,
    'Owning_Task' => owner, 'Candidate_ID' => candidate,
    'Artifact_Path' => ordered.first[1]['artifact_path'], 'Blocking_Findings_B64' => Base64.strict_encode64(details)
  }
end

def validate_pending(run_root, values)
  root = File.join(run_root, '30-ablation')
  package = File.join(root, 'pending-history')
  raise 'pending package state drift' unless File.directory?(package) && !File.symlink?(package) &&
    !File.exist?(File.join(root, 'published')) && !File.symlink?(File.join(root, 'published'))
  receipt = parse_receipt(File.join(package, 'ablation-validation.txt'))
  raise 'pending receipt state drift' unless receipt['Schema'] == 'task9-ablation-validation/v1' &&
    receipt['Run_ID'] == File.basename(run_root) && receipt['Package_Status'] == 'PENDING_HISTORY' &&
    receipt['Universe_Valid'] == 'PASS' && receipt['Decisions_Valid'] == 'PASS' &&
    receipt['Applied_Status'] == 'PENDING' && receipt['Failure_Code'] == 'ABLATION_PENDING' &&
    Integer(receipt['Pending_Count'], 10).positive?
  details_bytes, details = decode_canonical_json(receipt['Details_B64'], 'pending receipt details')
  raise 'pending detail newline drift' unless details_bytes.end_with?("\n")
  raise 'pending detail artifact drift' unless details['Artifact_Path'] == File.join(package, 'phase-manifest.tsv')
  universe = File.join(package, 'candidate-universe.tsv')
  ledger = File.join(package, 'ablation-ledger.tsv')
  target = File.join(run_root, '20-final', 'targets-32-final.bin')
  raise 'pending receipt hash drift' unless receipt['Universe_SHA256'] == sha(read_regular(universe, 0o400)) &&
    receipt['Ledger_SHA256'] == sha(read_regular(ledger, 0o400)) && receipt['Target_Manifest_SHA256'] == sha(read_regular(target, 0o400))
  candidates = candidate_index(package)
  candidate = candidates.fetch(receipt['First_Pending_Candidate']) { raise 'pending candidate missing' }
  raise 'pending owner drift' unless candidate['Owning_task'] == receipt['First_Pending_Owner']
  ledger_lines = read_regular(ledger, 0o400).lines(chomp: true)
  ledger_header = ledger_lines.shift&.split("\t", -1)
  raise 'pending ledger header drift' unless ledger_header&.include?('Candidate_ID') && ledger_header.include?('Applied_State')
  pending_ids = ledger_lines.map do |line|
    fields = line.split("\t", -1)
    raise 'pending ledger field-count drift' unless fields.length == ledger_header.length
    row = Hash[ledger_header.zip(fields)]
    row['Candidate_ID'] if row['Applied_State'] == 'pending'
  end.compact
  raise 'pending ledger count/first drift' unless pending_ids.length == Integer(receipt['Pending_Count'], 10) && pending_ids.include?(receipt['First_Pending_Candidate'])
  expected = [receipt['First_Pending_Owner'], receipt['First_Pending_Candidate'], File.join(package, 'phase-manifest.tsv'),
              'NONE', receipt['Target_Manifest_SHA256'], receipt['Universe_SHA256'], receipt['Ledger_SHA256']]
  raise 'pending terminal argument drift' unless values == expected
  validator = File.join(root, 'validate-ablation.rb')
  stdout, stderr, status = Open3.capture3('/usr/bin/ruby', validator, run_root, 'check')
  phase_sha = sha(read_regular(File.join(package, 'phase-manifest.tsv'), 0o400))
  expected_output = "ABLATION_PACKAGE=PENDING_HISTORY phase_sha256=#{phase_sha}\nABLATION_ORACLE=PASS run=#{File.basename(run_root)} pending=#{pending_ids.length}\n"
  raise 'pending independent check drift' unless status.exitstatus == 3 && stderr.empty? && stdout.b == expected_output
end

def validate_invalidated(run_root, reason, action, owner, candidate, artifact, hashes)
  values = [reason, action, owner, candidate, artifact, *hashes]
  if reason == 'ABLATION_PENDING'
    raise 'pending action drift' unless action == 'REWORK_CONTENT'
    validate_pending(run_root, [owner, candidate, artifact, *hashes])
    return
  end
  if %w[SPEC_REVIEW_BLOCKED SAFETY_REVIEW_BLOCKED ABLATION_REVIEW_BLOCKED].include?(reason)
    reports, identity, = validate_reviews(run_root)
    route_path = File.join(run_root, '60-closeout', 'failure-routing.tsv')
    route = one_tsv(route_path, ROUTING_HEADER, 0o400)
    expected = expected_review_route(run_root, reports)
    raise 'review failure routing drift' unless route == expected
    raise 'review failure terminal drift' unless [route['Reason_Code'], route['Required_Action'], route['Owning_Task'],
      route['Candidate_ID'], route_path, identity['Review_Input_SHA256'],
      sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400)),
      sha(read_regular(File.join(run_root, '30-ablation', 'published', 'candidate-universe.tsv'), 0o400)),
      sha(read_regular(File.join(run_root, '30-ablation', 'published', 'ablation-ledger.tsv'), 0o400))] == values
    return
  end
  if reason == 'CLOSEOUT_VALIDATOR_FAIL'
    route_path = File.join(run_root, '60-closeout', 'failure-routing.tsv')
    route = one_tsv(route_path, ROUTING_HEADER, 0o400)
    _details_bytes, details = decode_canonical_json(route['Blocking_Findings_B64'], 'closeout failure details')
    raise 'closeout failure detail drift' unless details.is_a?(Hash) && details.keys.sort == %w[error_class message] &&
      details.values.all? { |value| value.is_a?(String) && !value.empty? }
    raise 'closeout failure route drift' unless route['Schema'] == 'task9-failure-routing/v1' &&
      route['Run_ID'] == File.basename(run_root) && route['Reason_Code'] == reason && route['Required_Action'] == 'STOP' &&
      route['Owning_Task'] == 'NONE' && route['Candidate_ID'] == 'NONE' &&
      route['Artifact_Path'] == File.join(run_root, '40-review-input', 'review-input.tsv')
    raise 'closeout failure terminal drift' unless [reason, action, owner, candidate, artifact] ==
      [reason, 'STOP', 'NONE', 'NONE', route_path]
    identity = one_tsv(File.join(run_root, '40-review-input', 'review-input.identity.tsv'), IDENTITY_HEADER, 0o400)
    package = File.join(run_root, '30-ablation', 'published')
    expected_hashes = [
      identity['Review_Input_SHA256'],
      sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400)),
      sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400)),
      sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
    ]
    raise 'closeout failure hash drift' unless hashes == expected_hashes
    return
  end
  matrix = {
    'INPUT_GUARD_FAIL' => ['REBUILD_EVIDENCE|STOP', '10-input/guard-output.txt'],
    'STATIC_ORACLE_FAIL' => ['STOP', '10-input/static-verifier.txt'],
    'PRE_DIFF_CONTENT_DRIFT' => ['STOP', '20-final/targets-32-final.tsv'],
    'DIFF_RACE' => ['STOP', '20-final/added-content.diff'],
    'ABLATION_PACKAGE_POISONED' => ['STOP', '30-ablation/validator-output.txt'],
    'ABLATION_PACKAGE_INVALID' => ['REBUILD_EVIDENCE', '30-ablation/validator-output.txt']
  }
  if %w[UNHANDLED_PHASE_FAILURE RECOVERY_PROOF_FAILED].include?(reason)
    raise 'recovery terminal fields drift' unless owner == 'NONE' && candidate == 'NONE' && hashes.all? { |value| value == 'NONE' }
    raise 'recovery artifact path drift' unless artifact.start_with?(File.join(run_root, '70-recovery', 'recovery.')) && File.basename(artifact) == 'recovery-verdict.tsv'
    verdict_header = %w[Schema Run_ID Quiescence_Confirmed First_Pass_Exits Second_Pass_Exits Scope_Stable Protected_Stable Zip_Stable Required_Action]
    verdict = one_tsv(artifact, verdict_header, 0o400)
    stable = %w[Scope_Stable Protected_Stable Zip_Stable].all? { |key| verdict[key] == 'yes' }
    expected_reason = stable ? 'UNHANDLED_PHASE_FAILURE' : 'RECOVERY_PROOF_FAILED'
    expected_action = stable ? 'REBUILD_EVIDENCE' : 'STOP'
    raise 'recovery verdict drift' unless verdict['Schema'] == 'task9-recovery-verdict/v1' &&
      verdict['Run_ID'] == File.basename(run_root) && verdict['Quiescence_Confirmed'] == 'yes' &&
      verdict['Required_Action'] == expected_action && reason == expected_reason && action == expected_action
    return
  end
  expected = matrix.fetch(reason) { raise "unapproved invalidation reason: #{reason}" }
  allowed_actions = expected[0].split('|')
  raise 'phase invalidation action/identity drift' unless allowed_actions.include?(action) && owner == 'NONE' && candidate == 'NONE'
  raise 'phase invalidation artifact drift' unless artifact == File.join(run_root, expected[1])
  read_regular(artifact)
  raise 'phase invalidation hash fields must be NONE' unless hashes.all? { |value| value == 'NONE' }
  package_root = File.join(run_root, '30-ablation')
  if reason == 'ABLATION_PACKAGE_POISONED'
    raise 'poisoned package reason without a package' unless %w[published pending-history].any? { |name| File.exist?(File.join(package_root, name)) || File.symlink?(File.join(package_root, name)) }
  elsif reason == 'ABLATION_PACKAGE_INVALID'
    raise 'invalid package reason with a package' if %w[published pending-history].any? { |name| File.exist?(File.join(package_root, name)) || File.symlink?(File.join(package_root, name)) }
  end
end

def prepare_reservation(run_id, owner, candidate)
  root = File.join(SNAPSHOT, 'task9-rework-reservations')
  begin
    Dir.mkdir(root, 0o700)
  rescue Errno::EEXIST
    # The single legal active generation may already have created it.
  end
  raise 'unsafe reservation root' unless File.directory?(root) && !File.symlink?(root)
  path = File.join(root, "#{run_id}.tsv")
  if File.exist?(path) || File.symlink?(path)
    bytes = read_regular(path, 0o400)
    fields = bytes.lines(chomp: true)
    raise 'reservation header/row drift' unless fields.length == 2 && fields[0] == "Schema\tOwner\tEvidence_ID\tSource_Run\tCandidate_ID"
    row = fields[1].split("\t", -1)
    raise 'reservation field drift' unless row.length == 5 && row[0] == 'task9-rework-reservation/v1' &&
      row[1] == owner && row[3] == run_id && row[4] == candidate && row[2].match?(/\A#{Regexp.escape(owner)}_R([2-9]|\d{2,})\z/)
    return [row[2], path, bytes]
  end
  used = Dir.children(File.join(SNAPSHOT, 'manifests')).map do |name|
    match = name.match(/\A#{Regexp.escape(owner)}_R(\d+)-/)
    Integer(match[1], 10) if match
  end.compact
  Dir.children(root).sort.each do |name|
    raise "reservation filename drift: #{name}" unless name.match?(/\Arun-\d{3}\.tsv\z/)
    row = read_regular(File.join(root, name), 0o400).lines(chomp: true)[1]&.split("\t", -1)
    raise "reservation row drift: #{name}" unless row && row.length == 5
    match = row[2].match(/\A#{Regexp.escape(owner)}_R(\d+)\z/) if row[1] == owner
    used << Integer(match[1], 10) if match
  end
  evidence_id = "#{owner}_R#{[1, *used].max + 1}"
  bytes = "Schema\tOwner\tEvidence_ID\tSource_Run\tCandidate_ID\n" +
          "task9-rework-reservation/v1\t#{owner}\t#{evidence_id}\t#{run_id}\t#{candidate}\n"
  [evidence_id, path, bytes]
end

def publish_reservation(path, bytes)
  write_or_verify(path, bytes)
  raise 'reservation publication drift' unless read_regular(path, 0o400) == bytes
  File.open(File.dirname(path), File::RDONLY) { |directory| directory.fsync }
end

def validate_reservation(row)
  if row['Required_Action'] != 'REWORK_CONTENT'
    raise 'unexpected terminal reservation' unless row['Next_Evidence_ID'] == 'NONE' &&
      row['Rework_Reservation_Path'] == 'NONE' && row['Rework_Reservation_SHA256'] == 'NONE'
    current_claim = File.join(SNAPSHOT, 'task9-rework-reservations', "#{row['Run_ID']}.tsv")
    raise 'orphan reservation for non-rework terminal' if File.exist?(current_claim) || File.symlink?(current_claim)
    return
  end
  expected_path = File.join(SNAPSHOT, 'task9-rework-reservations', "#{row['Run_ID']}.tsv")
  bytes = read_regular(expected_path, 0o400)
  expected = "Schema\tOwner\tEvidence_ID\tSource_Run\tCandidate_ID\n" +
             "task9-rework-reservation/v1\t#{row['Owning_Task']}\t#{row['Next_Evidence_ID']}\t#{row['Run_ID']}\t#{row['Candidate_ID']}\n"
  raise 'terminal reservation path/content/hash drift' unless row['Rework_Reservation_Path'] == expected_path &&
    bytes == expected && row['Rework_Reservation_SHA256'] == sha(bytes)
end

def parse_terminal(run_root)
  path = File.join(run_root, 'TERMINAL.tsv')
  row = one_tsv(path, HEADER)
  raise 'terminal schema/run drift' unless row['Schema'] == 'task9-terminal/v1' && row['Run_ID'] == File.basename(run_root)
  row
end

def validate_terminal_evidence(run_root, row)
  input_scope = File.join(run_root, '10-input', 'input-scope.tsv')
  raise 'terminal input binding drift' unless row['Input_Scope_TSV'] == input_scope && row['Input_Scope_SHA256'] == sha(read_regular(input_scope))
  hashes = %w[Review_Input_SHA256 Target_Manifest_SHA256 Candidate_Universe_SHA256 Ablation_Ledger_SHA256].map { |key| row[key] }
  hashes.each { |value| raise 'terminal hash syntax drift' unless value == 'NONE' || value.match?(/\A[0-9a-f]{64}\z/) }
  if row['State'] == 'COMPLETED'
    raise 'completed terminal control drift' unless %w[Reason_Code Required_Action Owning_Task Candidate_ID Artifact_Path].all? { |key| row[key] == 'NONE' }
    validate_completion(run_root, hashes)
  elsif row['State'] == 'INVALIDATED'
    validate_invalidated(run_root, row['Reason_Code'], row['Required_Action'], row['Owning_Task'], row['Candidate_ID'], row['Artifact_Path'], hashes)
  else
    raise 'terminal state drift'
  end
  validate_reservation(row)
end

def verify_generation_seal(run_root, row, require_sealed: false)
  seal_path = File.join(run_root, 'generation-seal.tsv')
  seal_bytes = read_regular(seal_path, require_sealed ? 0o400 : nil)
  raise 'generation seal hash drift' unless row['Generation_Seal_SHA256'] == sha(seal_bytes)
  sealed_rows = parse_tsv(seal_bytes, %w[Relative_Path Bytes SHA256], seal_path)
                       .map { |entry| [entry['Relative_Path'], entry['Bytes'], entry['SHA256']] }
  raise 'generation seal duplicate/order drift' unless sealed_rows.map(&:first).uniq.length == sealed_rows.length &&
    sealed_rows.map(&:first) == sealed_rows.map(&:first).sort_by(&:b)
  actual_rows, = collect_tree(run_root, require_sealed: require_sealed)
  raise 'generation seal file-set/content drift' unless actual_rows == sealed_rows
end

def finalize_existing(run_root)
  verify_helpers
  terminal_path = File.join(run_root, 'TERMINAL.tsv')
  intent_path = File.join(run_root, 'terminal-intent.tsv')
  raise 'terminal finalization requires all control files' unless CONTROL_FILES.all? { |name| File.file?(File.join(run_root, name)) && !File.symlink?(File.join(run_root, name)) }
  terminal_bytes = read_regular(terminal_path)
  raise 'terminal intent drift' unless read_regular(intent_path) == terminal_bytes
  row = parse_terminal(run_root)
  validate_terminal_evidence(run_root, row)
  verify_generation_seal(run_root, row)
  _rows, paths = collect_tree(run_root)
  paths.sort_by { |path| -path.count(File::SEPARATOR) }.each do |path|
    stat = File.lstat(path)
    File.chmod(stat.directory? ? 0o500 : 0o400, path)
  end
  raise 'terminal changed during finalization' unless read_regular(terminal_path, 0o400) == terminal_bytes && read_regular(intent_path, 0o400) == terminal_bytes
  row = parse_terminal(run_root)
  validate_terminal_evidence(run_root, row)
  verify_generation_seal(run_root, row, require_sealed: true)
  File.open(run_root, File::RDONLY) { |directory| directory.fsync }
  File.open(File.dirname(run_root), File::RDONLY) { |directory| directory.fsync }
  puts "TASK9_TERMINAL=#{row['State']} run=#{row['Run_ID']} sha256=#{sha(terminal_bytes)} seal_sha256=#{row['Generation_Seal_SHA256']}"
end

if ARGV.first == '--finalize-existing'
  abort 'usage: seal-task9-generation.rb --finalize-existing RUN_ID' unless ARGV.length == 2
  run_id = ARGV[1]
  abort "invalid run ID: #{run_id}" unless run_id.match?(/\Arun-\d{3}\z/)
  run_root = File.join(SNAPSHOT, 'task9', run_id)
  abort 'invalid run root' unless File.directory?(run_root) && !File.symlink?(run_root)
  finalize_existing(run_root)
  exit 0
end

abort 'usage: seal-task9-generation.rb RUN_ID STATE REASON ACTION OWNER CANDIDATE ARTIFACT REVIEW_SHA TARGET_SHA UNIVERSE_SHA LEDGER_SHA' unless ARGV.length == 11
run_id, state, reason, action, owner, candidate, artifact, review_sha, target_sha, universe_sha, ledger_sha = ARGV
abort "invalid run ID: #{run_id}" unless run_id.match?(/\Arun-\d{3}\z/)
abort "invalid state: #{state}" unless %w[COMPLETED INVALIDATED].include?(state)
run_root = File.join(SNAPSHOT, 'task9', run_id)
abort 'invalid run root' unless File.directory?(run_root) && !File.symlink?(run_root)
abort 'terminal already exists; use --finalize-existing with no caller-supplied state' if File.exist?(File.join(run_root, 'TERMINAL.tsv')) || File.symlink?(File.join(run_root, 'TERMINAL.tsv'))
verify_helpers
hashes = [review_sha, target_sha, universe_sha, ledger_sha]
if state == 'COMPLETED'
  abort 'completed terminal control drift' unless [reason, action, owner, candidate, artifact].all? { |value| value == 'NONE' }
  validate_completion(run_root, hashes, create_ready: true)
else
  validate_invalidated(run_root, reason, action, owner, candidate, artifact, hashes)
end

next_evidence_id = reservation_path = reservation_sha = 'NONE'
reservation_bytes = nil
if action == 'REWORK_CONTENT'
  next_evidence_id, reservation_path, reservation_bytes = prepare_reservation(run_id, owner, candidate)
  reservation_sha = sha(reservation_bytes)
end
rows, = collect_tree(run_root)
seal_bytes = seal_bytes_for(rows)
seal_sha = sha(seal_bytes)
input_scope = File.join(run_root, '10-input', 'input-scope.tsv')
input_sha = sha(read_regular(input_scope))
values = [
  'task9-terminal/v1', run_id, state, reason, action, owner, candidate, next_evidence_id,
  reservation_path, reservation_sha, artifact, input_scope, input_sha,
  review_sha, target_sha, universe_sha, ledger_sha, seal_sha
]
terminal_bytes = HEADER.join("\t") + "\n" + values.join("\t") + "\n"
intent_path = File.join(run_root, 'terminal-intent.tsv')
seal_path = File.join(run_root, 'generation-seal.tsv')
terminal_path = File.join(run_root, 'TERMINAL.tsv')
write_or_verify(intent_path, terminal_bytes)
publish_reservation(reservation_path, reservation_bytes) if reservation_bytes
verify_helpers
state == 'COMPLETED' ? validate_completion(run_root, hashes) : validate_invalidated(run_root, reason, action, owner, candidate, artifact, hashes)
current_rows, = collect_tree(run_root)
abort 'generation changed before terminal publication' unless current_rows == rows
write_or_verify(seal_path, seal_bytes)
write_or_verify(terminal_path, terminal_bytes)
File.open(run_root, File::RDONLY) { |directory| directory.fsync }
finalize_existing(run_root)
```

The normal interface derives authority from machine-validated phase evidence; arbitrary uppercase reasons or caller-supplied rework owners are rejected. `--finalize-existing RUN_ID` is the only crash recovery after `TERMINAL.tsv` exists: it accepts no caller-supplied state, rereads the terminal/intent/seal and phase evidence, freezes the complete tree, then performs a fresh exact path/hash/mode pass. If allocation, validation or publication fails before a terminal exists, preserve the poisoned run and use the declared recovery protocol; never delete it, repair it in place or reuse its run ID. A later run is legal only when the immediately previous generation has a valid `State=INVALIDATED` terminal and matching generation seal. A `COMPLETED` terminal forbids every later run.

Use `apply_patch` to create `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb` with this complete static oracle:

```ruby
#!/usr/bin/ruby
require 'open3'

ROOT = '/Users/lute/Project/vibecoding_config'
SNAPSHOT = '/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/preimage'
PLAN_REL = '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
FIXED_COMMIT = '4c486c7a532de8890e88036533e0a48d578087ed'
PUBLIC_HEADINGS = %w[Metadata Facts Decisions Assumptions Open\ questions Risks\ and\ reversibility Acceptance\ evidence Handoff].freeze

CANON = {
  '02' => '全栈开发Prompt Chain/prompts/02-机会与市场调研.md',
  '03' => '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md',
  '04' => '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md',
  '05' => '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md',
  '06' => '全栈开发Prompt Chain/prompts/06-原型与UX验证.md',
  '07' => '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md',
  '08' => '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md',
  '09' => '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md',
  '11' => '全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md',
  '12' => '全栈开发Prompt Chain/prompts/12-增长与实验.md',
  '13' => '全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md'
}.freeze
ASK = CANON.transform_values { |path| path.sub('/prompts/', '/prompts_ask/') }.freeze

REQUIREMENTS = {
  '02' => ['## Competitor transfer', '| Subject | Observable fact | Target context | Enabling constraints | Counterevidence | Transferable principle | Non-transferable context | Evidence refs |', '仅在用户要求竞品、替代方案或市场比较时生成；决策影响只决定研究深度和下一问题，不是附加触发条件。', 'Evidence_Ref fields: source, acquisition date, applicability, evidence level, limitation.', 'M03/M04', 'Opportunity_ID'],
  '03' => ['## Evidence-to-opportunity map', 'Created_by_Module', 'supports/refutes', 'Superseded_by', 'Every decision-stage Opportunity has at least one `Evidence_Ref -[supports]-> Opportunity_ID`.', 'Counterevidence uses a separate `Evidence_Ref -[refutes]-> Opportunity_ID` and must not be placed in `supports`.', 'Evidence_Ref and Opportunity_ID relations are many-to-many.', '## Optional survey plan', 'Response type', 'Decision affected', 'Consent/distribution boundary', 'Preregistered analysis', 'survey-plan'],
  '04' => ['## Product decision graph', 'Created_by_Module', 'Superseded_by', 'contributes_to', 'addresses', 'applies_to', 'governs', 'many-to-many', 'Authoritative_decision_ref', 'Decision_owner', 'Gate_or_authorization_ref', 'Decision_date', 'Expiry_or_invalidated_by', 'Decision authority:', '`superseded` is terminal and cannot be restored or silently overwritten.', 'Downstream remains blocked until the same existing human decision owner or Gate creates a successor Decision or supersedes the old record and re-decides.', 'M04 cannot create Metric/Event definitions', '## Product risk review', 'Cheapest reversible test', '## Prioritization sensitivity', 'Rank-reversal condition', 'closed-not-applicable', 'Status=approved', '`active`'],
  '05' => ['## Journey backbone', '## Measurement contract', 'Created_by_Module', 'Superseded_by', 'measures', 'derived_from', 'Identity + deduplication', 'Privacy/consent/retention/access', '## Pre-build review findings', 'product | design | engineering | data | security | privacy | legal | operations', 'blocker | major | minor', '`not executed`', '`0 blocker`', 'M05 does not create `Slice_ID`'],
  '06' => ['## Decision graph trace', 'Test_rev', 'Created_by_Module', 'tests', 'Priority: riskiest', 'Superseded_by', 'learning evidence', 'G4_APPROVAL', 'ALLOWED_FILES_OR_SANDBOX'],
  '07' => ['## Product slice and measurement trace', 'Slice_rev', 'Created_by_Module', 'realizes', 'Superseded_by', 'instrumentation ticket', 'M07 may create a Slice only when the referenced Candidate_ID or A05 Spec is current and has an applicable existing approval.', 'Otherwise omit the Product slice table', 'Metric/Event semantic/property changes return to M05; M07 only creates an instrumentation ticket.', '## Conditional delivery outline', 'Capacity assumption', 'Change trigger', 'tracker-preview'],
  '08' => ['## Product trace implemented', 'Slice_ID', 'Metric_ID/Event_ID', 'Semantic drift or new field', 'M05/M07', 'ALLOWED_FILES', 'DEPENDENCY_CHANGES'],
  '09' => ['## Product risk and measurement review', 'A07/A08/fixed-diff evidence', 'Closure evidence or Unverified scope', 'Do not query production'],
  '11' => ['## Action register', 'Finding_or_Evidence_ID', 'Causal hypothesis', 'Counterevidence/alternative', 'Destination module', 'proposed | accepted | in_progress | verified | rejected | superseded', 'G0', 'R3_ACTION_AUTHORIZATION', 'No production access'],
  '12' => ['## Decision graph trace', 'Test_rev', 'Created_by_Module', 'tests', 'Metric_ID/Event_ID', 'Recommended decision', 'Superseded_by', 'MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION', 'Not launched / no production verification'],
  '13' => ['## Action register', 'Finding_or_Evidence_ID', 'Causal hypothesis', 'Counterevidence/alternative', 'Destination module', 'proposed | accepted | in_progress | verified | rejected | superseded', 'Not adopted / no persistent change', 'R3_ACTION_AUTHORIZATION', 'mock/dry-run', 'auto-adopt/auto-publish']
}.freeze

CONFIRMATIONS = {
  '02' => '确认生成 A02-opportunity-brief.md 吗？',
  '03' => '确认生成 A03-problem-evidence.md 吗？',
  '04' => '确认生成 A04-product-strategy.md 吗？',
  '05' => '确认生成 A05-product-spec.md 吗？',
  '06' => '确认生成 A06-prototype-evidence.md 吗？',
  '07' => '确认生成 A07-architecture-and-tickets.md 吗？',
  '08' => '确认生成 A08-implementation-report.md 吗？',
  '09' => '确认生成 A09-quality-evidence.md 吗？',
  '11' => '确认生成 A11-production-learning.md 吗？',
  '12' => '确认生成 A12-experiment-decision.md 吗？',
  '13' => '确认生成 A13-retrospective.md 吗？'
}.freeze

LINEAGE_LINES = {
  '02' => 'Decision lineage: Consumes=[A00/A01 refs or NONE]; Produces=[Evidence_Ref or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[unverified source/transfer-limit ID or NONE]; Consumers=[M03/M04]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '03' => 'Decision lineage: Consumes=[A02 Evidence_Ref/current Opportunity_ID@rev or NONE]; Produces=[Opportunity_ID@rev + supports/refutes Evidence_Refs or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[unsupported Opportunity_ID@rev or NONE]; Consumers=[M04]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '04' => 'Decision lineage: Consumes=[current Opportunity_ID@rev + A00/A01 refs or NONE]; Produces=[Outcome_ID@rev/Candidate_ID@rev/Hypothesis_ID@rev/Decision_ID@rev or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[missing authority/evidence ID or NONE]; Consumers=[G2/M05/M06]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '05' => 'Decision lineage: Consumes=[active OUT/OPP/CAN/HYP/DEC refs from A04 or NONE]; Produces=[Metric_ID@rev/Event_ID@rev or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[undefined measurement ID or NONE]; Consumers=[M06/M07/M09]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '06' => 'Decision lineage: Consumes=[active Hypothesis_ID@rev + Decision_ID@rev or NONE]; Produces=[Test_ID@rev or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[inactive hypothesis/decision ID or NONE]; Consumers=[M04/M07]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '07' => 'Decision lineage: Consumes=[approved Candidate_ID@rev or approved A05 Spec + HYP/MET/EVT/DEC refs]; Produces=[Slice_ID@rev + instrumentation ticket or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[missing approval/current ID or NONE]; Consumers=[G4/M08]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '08' => 'Decision lineage: Consumes=[active Slice_ID@rev/Decision_ID@rev + G3/G4 + MET/EVT refs]; Produces=[implementation/test evidence or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[failed Gate/inactive ID or NONE]; Consumers=[M09]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '09' => 'Decision lineage: Consumes=[fixed review range + A04/A05/A07/A08 refs]; Produces=[findings/Unverified scope or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[unverified review scope or NONE]; Consumers=[M10/G5]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '11' => 'Decision lineage: Consumes=[authorized production evidence/user feedback/incident facts + active IDs or NONE]; Produces=[Evidence/action-register entries or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[unauthorized/unverified evidence ID or NONE]; Consumers=[M03/M04/M05/M12/M13]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '12' => 'Decision lineage: Consumes=[active HYP/MET/EVT/DEC refs]; Produces=[Test_ID@rev + recommended decision or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[missing active input ID or NONE]; Consumers=[M04/M11/M13]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].',
  '13' => 'Decision lineage: Consumes=[Axx/Evidence/ID refs or NONE]; Produces=[action-register/candidate-learning entries or NONE]; Explicitly closed=[known ID + closed-not-applicable Decision_ID@rev or NONE]; Blockers=[unrouted action/unknown authority ID or NONE]; Consumers=[destination module/human decision owner]; Evidence_Refs=[source + acquisition date + applicability + evidence level + limitation, or NONE].'
}.freeze

class Verify
  attr_reader :errors

  def initialize
    @errors = []
    @cache = {}
    @preimage_cache = {}
  end

  def read(relative, preimage: false)
    cache = preimage ? @preimage_cache : @cache
    return cache[relative] if cache.key?(relative)
    root = preimage ? SNAPSHOT : ROOT
    absolute = File.join(root, relative)
    unless File.file?(absolute) && !File.symlink?(absolute)
      @errors << "missing regular file: #{preimage ? 'preimage:' : ''}#{relative}"
      return cache[relative] = ''
    end
    stdout, stderr, status = Open3.capture3('/bin/cat', absolute)
    unless status.success?
      @errors << "cat failed: #{absolute}: #{stderr}"
      return cache[relative] = ''
    end
    cache[relative] = stdout.force_encoding(Encoding::UTF_8)
  end

  def tokens(relative, required)
    body = read(relative)
    required.each { |token| @errors << "#{relative}: missing #{token.inspect}" unless body.include?(token) }
  end

  def exactly_once(relative, literal)
    count = read(relative).scan(/^#{Regexp.escape(literal)}$/).length
    @errors << "#{relative}: #{literal.inspect} count=#{count}" unless count == 1
  end

  def regex_count(relative, regex, expected)
    count = read(relative).scan(regex).length
    @errors << "#{relative}: #{regex.inspect} count=#{count}, expected=#{expected}" unless count == expected
  end

  def common_artifact(relative)
    PUBLIC_HEADINGS.each { |heading| exactly_once(relative, "## #{heading}") }
  end

  def decision_lineage(relative, module_id)
    sections = read(relative).scan(/^## Handoff[ \t]*\n(.*?)(?=^## |\z)/m).flatten
    unless sections.length == 1
      @errors << "#{relative}: Handoff section count=#{sections.length}, expected=1"
      return
    end
    lines = sections.first.lines(chomp: true).select { |line| line.start_with?('Decision lineage:') }
    unless lines.length == 1
      @errors << "#{relative}: Decision lineage count in Handoff=#{lines.length}, expected=1"
      return
    end
    expected = LINEAGE_LINES.fetch(module_id)
    @errors << "#{relative}: Decision lineage format drift" unless lines.first == expected
  end

  def dialogue(module_id)
    path = ASK.fetch(module_id)
    tokens(path, REQUIREMENTS.fetch(module_id) + ['每轮只问一个', '不知道', CONFIRMATIONS.fetch(module_id)])
    common_artifact(path)
    decision_lineage(path, module_id)
  end

  def canonical(module_id)
    path = CANON.fetch(module_id)
    tokens(path, REQUIREMENTS.fetch(module_id))
    common_artifact(path)
    decision_lineage(path, module_id)
  end

  def unchanged_lines(relative, patterns)
    current = read(relative).lines.select { |line| patterns.any? { |pattern| line.match?(pattern) } }
    before = read(relative, preimage: true).lines.select { |line| patterns.any? { |pattern| line.match?(pattern) } }
    @errors << "#{relative}: protected lines changed" unless current == before
  end

  def task1
    source = '全栈开发Prompt Chain/report-source.md'
    audit = '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md'
    candidate = '全栈开发Prompt Chain/05-GitHub候选与替代审计.md'
    read(audit)
    (1..10).each { |number| regex_count(audit, /^## #{number}\. /, 1) }
    tokens(audit, ['受限 Adapter', '不安装', '无 E5', 'closed-not-applicable', 'MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION'])
    regex_count(source, /^\| R32 \|/, 1)
    (44..48).each { |id| regex_count(source, /^\| S#{format('%03d', id)} \|/, 1) }
    (39..44).each { |id| regex_count(source, /^\| C#{format('%03d', id)} \|/, 1) }
    unchanged_lines(source, [/^\| R(?:0[1-9]|[12][0-9]|3[01]) \|/, /^\| S(?:00[1-9]|0[1-3][0-9]|04[0-3]) \|/, /^\| C(?:00[1-9]|0[1-2][0-9]|03[0-8]) \|/])
    links = read(source).scan(%r{https://github\.com/SpaceZephyr/pm-skills/(?:blob|tree)/([^/\s)]+)})
    @errors << 'report-source: no fixed GitHub file/tree link' if links.empty?
    links.flatten.each { |revision| @errors << "unfixed pm-skills link revision=#{revision}" unless revision == FIXED_COMMIT }
    exactly_once(candidate, '### 2.4 PM-Skill 2.0 受限来源')
    tokens(candidate, ['GitHub API license=null', 'README says MIT', 'no root LICENSE', '不安装', '无 E5'])
    regex_count('全栈开发Prompt Chain/README.md', /08-PM-Skill-2\.0核心工作流评估与融合\.md/, 1)
  end

  def task2
    lifecycle = '全栈开发Prompt Chain/03-AI产品全生命周期映射.md'
    workflow = '全栈开发Prompt Chain/04-模块化Skills工作流.md'
    manual = '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md'
    controller = '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
    exactly_once(lifecycle, '### 4.1 PM-Skill 2.0 受限投影')
    exactly_once(workflow, '### 3.1 产品决策图交接契约')
    exactly_once(manual, '### 7.1 产品决策图交接')
    tokens(workflow, ['Evidence refs:', 'Opportunity evidence cardinality:', 'Evidence_Ref -[supports]-> Opportunity_ID', 'Evidence_Ref -[refutes]-> Opportunity_ID', 'must not be placed in `supports`', 'many-to-many', 'Cardinality:', 'Created_by_Module', 'Superseded_by', 'Status=`approved`', 'Authoritative_decision_ref', 'Expiry_or_invalidated_by', 'closed-not-applicable', 'Downstream remains blocked until the same existing human decision owner or Gate creates a successor Decision or supersedes the old record and re-decides.', 'M04=OUT/CAN/HYP semantics and product-Decision recording only'])
    tokens(manual, ['Decision active check', 'Status=`approved`', 'Authoritative_decision_ref', 'Expiry_or_invalidated_by', 'Evidence_Ref', 'Consumes', 'Produces', 'Explicitly closed', 'closed-not-applicable', 'Downstream remains blocked until the same existing human decision owner or Gate creates a successor Decision or supersedes the old record and re-decides.', '不生成空表'])
    tokens(controller, ['一次只执行一个当前模块', 'Target、Action、Expected effect、Credential scope', 'Cost、Rollback、Verification、Idempotency/duplicate guard、Expiry'])
    if read(controller) == read(controller, preimage: true)
      # Approved ablation branch: the existing Handoff/controller already carries the requirement.
    else
      exactly_once(controller, '13. 产品决策图兼容：当前 Axx 含产品实体或 Decision 时，下游只消费派生 `active` 检查为真的当前 rev：Decision Status 必须为 `approved`、`Authoritative_decision_ref` 仍指向当前版本、未到 expiry、`invalidated_by` 条件均未命中，且实体未被 supersede。`active` 只在消费时计算，不是持久状态。已存在但不适用的 ID 必须由现有决定者/Gate 以含 `Authoritative_decision_ref`、`Decision_owner`、`Decision_date`、`Expiry_or_invalidated_by`、`Evidence_Refs` 和适用 `Gate_or_authorization_ref` 的 `closed-not-applicable` Decision 关闭；从未创建的可选 ID 不生成空关闭记录。缺失、未批准、过期、被 invalidated/superseded 或所有权冲突时停止，不创建第二路由、Gate 或授权。')
    end
    unchanged_lines(controller, [/^模块注册表：$/, /^- M(?:0[0-9]|1[0-3]) -> A(?:0[0-9]|1[0-3])/, /^默认场景路由：$/, /^- (?:MVP|Feature|Bug\/Incident|Post-launch|Audit)：/])
    registry = read(controller).scan(/^- M(\d{2}) -> A(\d{2})/)
    expected_registry = (0..13).map { |number| id = format('%02d', number); [id, id] }
    @errors << "#{controller}: module registry drift=#{registry.inspect}" unless registry == expected_registry
    regex_count(lifecycle, /^\| 合计 \| 1–36，各出现一次 \| 36 \|$/, 1)
  end

  def task3
    %w[02 03 04].each { |id| canonical(id) }
  end

  def task4
    %w[05 06 07].each { |id| canonical(id) }
  end

  def task5
    %w[08 09 11 12 13].each { |id| canonical(id) }
  end

  def task6
    %w[02 03 04 05].each { |id| dialogue(id) }
  end

  def task7
    %w[06 07 08 09].each { |id| dialogue(id) }
  end

  def task8
    %w[11 12 13].each { |id| dialogue(id) }
  end

  def all
    (1..8).each { |number| public_send("task#{number}") }
    (CANON.values + ASK.values).each do |relative|
      body = read(relative)
      @errors << "invalid UTF-8: #{relative}" unless body.valid_encoding?
      @errors << "unbalanced fences: #{relative}" unless body.scan(/^```/).length.even?
    end
    ASK.keys.each { |id| dialogue(id) }
    runtime_contracts = [
      '全栈开发Prompt Chain/03-AI产品全生命周期映射.md',
      '全栈开发Prompt Chain/04-模块化Skills工作流.md',
      '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md',
      '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
    ] + CANON.values + ASK.values
    runtime_contracts.each do |relative|
      body = read(relative)
      %w[M14 A14 G7].each { |forbidden| @errors << "#{relative}: forbidden runtime definition token #{forbidden}" if body.include?(forbidden) }
    end
    scope_text = read(PLAN_REL)[/## File Structure and Exact Scope\n(.*?)\n## Frozen Input Gate/m, 1]
    if scope_text
      paths = scope_text.scan(/^- (?:Modify|Create|Normalize only): `([^`]+)`/).flatten
      @errors << "scope count=#{paths.length}" unless paths.length == 32 && paths.uniq.length == 32
      paths.each do |relative|
        body = read(relative)
        @errors << "invalid UTF-8: #{relative}" unless body.valid_encoding?
        @errors << "unbalanced fences: #{relative}" unless body.scan(/^```/).length.even?
      end
    else
      @errors << 'scope section missing'
    end
    combined = (CANON.values + ASK.values + ['全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md']).map { |path| read(path) }.join("\n")
    ['我是 Marty Cagan', '我是 Teresa Torres', '我是俞军'].each do |forbidden|
      @errors << "forbidden expert roleplay: #{forbidden}" if combined.include?(forbidden)
    end
  end
end

mode = ARGV.shift or abort 'usage: verify-chain.rb task1|task2|task3|task4|task5|task6|task7|task8|all'
abort "unexpected arguments: #{ARGV.inspect}" unless ARGV.empty?
verifier = Verify.new
if mode == 'all'
  verifier.all
elsif mode.match?(/^task[1-8]$/)
  verifier.public_send(mode)
else
  abort "unknown mode: #{mode}"
end

if verifier.errors.empty?
  puts "#{mode.upcase}_STATIC=PASS"
  exit 0
end
verifier.errors.uniq.each { |error| warn "FAIL #{error}" }
warn "#{mode.upcase}_STATIC=FAIL count=#{verifier.errors.uniq.length}"
exit 1
```

Run syntax checks:

```zsh
set -euo pipefail
snapshot_path='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
/bin/zsh -n "$snapshot_path/normalize-targets.zsh"
/bin/zsh -n "$snapshot_path/guard-workspace.zsh"
/bin/zsh -n "$snapshot_path/capture-and-normalize.zsh"
/bin/zsh -n "$snapshot_path/rollback-target.zsh"
/usr/bin/ruby -c "$snapshot_path/four-value-manifest.rb"
/usr/bin/ruby -c "$snapshot_path/seal-task9-generation.rb"
/usr/bin/ruby -c "$snapshot_path/verify-chain.rb"
/bin/chmod 400 "$snapshot_path/guard-workspace.zsh" "$snapshot_path/normalize-targets.zsh" "$snapshot_path/capture-and-normalize.zsh" "$snapshot_path/rollback-target.zsh" "$snapshot_path/four-value-manifest.rb" "$snapshot_path/seal-task9-generation.rb" "$snapshot_path/verify-chain.rb"
/usr/bin/ruby - "$snapshot_path" <<'RUBY'
require 'digest'
snapshot = ARGV.fetch(0)
names = %w[
  capture-and-normalize.zsh four-value-manifest.rb guard-workspace.zsh
  normalize-targets.zsh rollback-target.zsh seal-task9-generation.rb verify-chain.rb
]
rows = names.map do |name|
  path = File.join(snapshot, name)
  stat = File.lstat(path)
  raise "unsafe helper: #{path}" unless stat.file? && !stat.symlink? && (stat.mode & 0o777) == 0o400
  bytes = File.binread(path)
  [name, bytes.bytesize, Digest::SHA256.hexdigest(bytes)]
end
body = "Schema\tName\tBytes\tSHA256\tMode\n" +
  rows.map { |name, bytes, hash| ['task0-helper-manifest/v1', name, bytes, hash, '400'].join("\t") + "\n" }.join
path = File.join(snapshot, 'helper-manifest.tsv')
File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
  file.write(body)
  file.flush
  file.fsync
end
File.open(snapshot, File::RDONLY) { |directory| directory.fsync }
puts "TASK0_HELPERS=SEALED files=#{rows.length} sha256=#{Digest::SHA256.hexdigest(body)}"
RUBY
print -r -- 'TASK0_HELPER_SYNTAX=PASS'
```

Expected: three `Syntax OK` lines, `TASK0_HELPERS=SEALED files=7` and `TASK0_HELPER_SYNTAX=PASS`. `helper-manifest.tsv` is the byte-identity trust manifest. Task 9 allocation, recovery, review and terminal boundaries recheck it; Task 1–8 rely on the parent-directory lock applied after the isolated probe below. This is an integrity boundary against accidental or competing workflow writes, not protection from an operator who deliberately restores write permission. Do not run the guard, normalization, wrapper, rollback or Task 9 sealing helper against a workspace target in Task 0. Retain the earlier `/private/tmp/pm-skill-backup-probe.K2D0eC`.

Create the probe directory exactly once, then use `apply_patch` to create the absolute paths `$probe/left.txt` containing `LEFT` and `$probe/right.txt` containing `RIGHT`, each followed by one newline. Here `$probe` resolves literally to `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/swap-probe`; do not create `left.txt` or `right.txt` in the workspace:

```zsh
set -euo pipefail
probe='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/swap-probe'
test ! -e "$probe"
/bin/mkdir -m 700 "$probe"
```

Run this exact isolated primitive probe. It also proves that the project and snapshot are on the same filesystem, which is required for the exclusive prior move:

```zsh
set -euo pipefail
probe='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/swap-probe'
normalization_source='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/preimage/全栈开发Prompt Chain/04-模块化Skills工作流.md'
test "$(/usr/bin/stat -f %d /Users/lute/Project/vibecoding_config)" = "$(/usr/bin/stat -f %d "$probe")"
normalization_stage=$(/usr/bin/mktemp "$probe/.cp-p-stage.XXXXXX")
test -f "$normalization_stage" && test ! -L "$normalization_stage"
source_path_size=$(/usr/bin/stat -f %z "$normalization_source")
source_path_sha=$(/sbin/sha256sum "$normalization_source" | /usr/bin/awk '{print $1}')
source_cat_size=$(/bin/cat "$normalization_source" | /usr/bin/wc -c | /usr/bin/tr -d ' ')
source_cat_sha=$(/bin/cat "$normalization_source" | /sbin/sha256sum | /usr/bin/awk '{print $1}')
test "$(( source_path_size - source_cat_size ))" -eq 4096
test "$source_path_sha" != "$source_cat_sha"
clone_stage=$(/usr/bin/mktemp "$probe/.cp-c-stage.XXXXXX")
/bin/cp -c -p "$normalization_source" "$clone_stage"
test "$(/usr/bin/stat -f %z "$clone_stage")" = "$source_path_size"
test "$(/sbin/sha256sum "$clone_stage" | /usr/bin/awk '{print $1}')" = "$source_path_sha"
test "$(/bin/cat "$clone_stage" | /usr/bin/wc -c | /usr/bin/tr -d ' ')" = "$source_cat_size"
test "$(/bin/cat "$clone_stage" | /sbin/sha256sum | /usr/bin/awk '{print $1}')" = "$source_cat_sha"
test "$(/usr/bin/stat -f %Lp "$clone_stage")" = "$(/usr/bin/stat -f %Lp "$normalization_source")"
print -r -- 'TASK0_CP_C_ROLLBACK_STAGE_PROBE=PASS source=04-模块化Skills工作流.md delta=4096'
/bin/cp -p "$normalization_source" "$normalization_stage"
stage_path_size=$(/usr/bin/stat -f %z "$normalization_stage")
stage_path_sha=$(/sbin/sha256sum "$normalization_stage" | /usr/bin/awk '{print $1}')
stage_cat_size=$(/bin/cat "$normalization_stage" | /usr/bin/wc -c | /usr/bin/tr -d ' ')
stage_cat_sha=$(/bin/cat "$normalization_stage" | /sbin/sha256sum | /usr/bin/awk '{print $1}')
test "$stage_path_size" = "$stage_cat_size"
test "$stage_path_sha" = "$stage_cat_sha"
test "$stage_cat_size" = "$source_cat_size"
test "$stage_cat_sha" = "$source_cat_sha"
test "$(/usr/bin/stat -f %Lp "$normalization_stage")" = "$(/usr/bin/stat -f %Lp "$normalization_source")"
print -r -- 'TASK0_CP_P_STAGE_PROBE=PASS source=04-模块化Skills工作流.md delta=4096'
/usr/bin/python3 - "$probe/left.txt" "$probe/right.txt" "$probe/prior.txt" <<'PY'
import ctypes
import os
import sys

RENAME_SWAP = 0x00000002
RENAME_EXCL = 0x00000004
libc = ctypes.CDLL(None, use_errno=True)
renamex_np = libc.renamex_np
renamex_np.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
renamex_np.restype = ctypes.c_int
if renamex_np(os.fsencode(sys.argv[1]), os.fsencode(sys.argv[2]), RENAME_SWAP) != 0:
    error_number = ctypes.get_errno()
    raise OSError(error_number, os.strerror(error_number), sys.argv[1], sys.argv[2])
if renamex_np(os.fsencode(sys.argv[2]), os.fsencode(sys.argv[3]), RENAME_EXCL) != 0:
    error_number = ctypes.get_errno()
    raise OSError(error_number, os.strerror(error_number), sys.argv[2], sys.argv[3])
PY
test "$(/bin/cat "$probe/left.txt")" = 'RIGHT'
test ! -e "$probe/right.txt"
test "$(/bin/cat "$probe/prior.txt")" = 'LEFT'
print -r -- 'TASK0_RENAME_SWAP_EXCL_PROBE=PASS'
```

Expected exit code `0`, `TASK0_CP_C_ROLLBACK_STAGE_PROBE=PASS source=04-模块化Skills工作流.md delta=4096`, `TASK0_CP_P_STAGE_PROBE=PASS source=04-模块化Skills工作流.md delta=4096` and `TASK0_RENAME_SWAP_EXCL_PROBE=PASS`. A failure leaves all probe paths and the snapshot in place and blocks the authorization request; do not fall back to `mv -f` or a cross-volume copy.

Freeze the probe and then remove write permission from the snapshot root itself. All later writable namespaces were pre-created in Step 2; this prevents an ordinary rename replacement of a helper plus its manifest while still allowing evidence creation inside the designated subdirectories:

```zsh
set -euo pipefail
snapshot_path='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
/usr/bin/find "$snapshot_path/swap-probe" -type f -exec /bin/chmod 400 {} +
/usr/bin/find "$snapshot_path/swap-probe" -type d -exec /bin/chmod 500 {} +
/bin/chmod 500 "$snapshot_path"
test "$('/usr/bin/stat' -f %Lp "$snapshot_path")" = 500
test "$('/usr/bin/stat' -f %Lp "$snapshot_path/helper-manifest.tsv")" = 400
print -r -- 'TASK0_SNAPSHOT_ROOT=SEALED mode=500 helpers=7'
```

Expected: `TASK0_SNAPSHOT_ROOT=SEALED mode=500 helpers=7`. Do not restore root write permission during normal execution; a root-level namespace change requires a revised, independently reviewed plan.

- [ ] **Step 6: Present the separate normalization authorization and stop**

First print the exact anomalous inventory from the sealed manifest:

```zsh
set -euo pipefail
manifest='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/baseline/existing-31-before.tsv'
/usr/bin/awk -F '\t' '
  $2 != $4 || $3 != $5 {
    if (($2 - $4) != 4096) exit 2
    printf "ANOMALOUS\t%s\tpathname_size=%s\tpathname_sha256=%s\tcat_size=%s\tcat_sha256=%s\tmode=%s\tdelta=%d\n", $1, $2, $3, $4, $5, $6, $2-$4
    count += 1
  }
  END {
    if (count != 16) exit 3
    printf "ANOMALOUS_EXISTING=%d\n", count
  }
' "$manifest"
```

Expected exit code `0`, 16 `ANOMALOUS` rows, `delta=4096` on every row, and `ANOMALOUS_EXISTING=16`. Then ask the user to authorize exactly this action, embedding those 16 complete rows and all 32 literal allowlist paths rather than referring only to a range:

```text
Targets: the 32 allowlisted paths in this plan; enumerate all paths from the File Structure section and separately enumerate every path whose Task 0 before record has pathname_size != cat_size or pathname_sha256 != cat_sha256.
Action: while the user and all reviewers pause writes to the allowlist, run the full-scope/protected/ZIP guard before every task; edit only the 29 content candidates and create the one audit document with apply_patch; after each task, seal the exact post-apply_patch six values, create a cat-stream-consistent cp -p staging file, use renamex_np(RENAME_SWAP) plus RENAME_EXCL so the swap-time prior target is retained under atomic-prior/TASK_ID, then prove every non-task allowlist path, protected file and ZIP remained equal to the pre-task evidence.
Preimage: /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/preimage, cloned with cp -c and verified in both pathname and cat views.
Byte source/effect: normalized bytes are exactly each target's sealed post-apply_patch cat stream. For every anomalous before record, state its four values and that normalization discards the pathname view's unexplained extra 4096 bytes while preserving that exact prior version in both Task 0 preimage and atomic-prior.
Expected effect: all 32 final Markdown files have pathname_size == cat_size and pathname_sha256 == cat_sha256; design and plan cat text remain byte-identical to Task 0 preimage.
Rollback: never automatic and always one path per separate authorization. Use only snapshot/rollback-target.zsh with the exact current postimage TSV, its exact SHA-256, a fresh rollback ID and separately confirmed target quiescence. For an existing target, the helper requires current six values to equal that postimage, verifies the cp -c -p Task 0 preimage in both views, atomically swaps it in and exclusively retains the swap-time postimage under rollback-conflicts; any drift stops. For the new audit, the helper permits only a recoverable exclusive move into snapshot/new-file-rollback after the same exact-current check; the moved bytes are rechecked and never deleted. The helper is not a filesystem lock and makes no pathname-preservation claim if writers violate quiescence.
Verification: run the exact task oracles and four-value helpers in this plan, compare protected and ZIP manifests byte-for-byte, run source/ask parity plus UTF-8/fence checks, and obtain the three fixed independent review reports.
Expiry: this implementation run only; any target or protected baseline drift invalidates authorization.
```

Do not begin Task 1 in the same turn. No reply other than an explicit authorization of this exact proposal permits normalization.

---

## Task-attempt context for Tasks 1–8

Every zsh invocation in Tasks 1–8 must receive these three environment variables from the coordinator; they are execution inputs, not values inferred by a helper:

```text
EVIDENCE_ID=<globally unused TASKn or TASKn_Rk ID>
SCOPE_SELECTOR=<existing31 only for initial TASK1; scope32 otherwise>
PREVIOUS_SCOPE_TSV=<absolute sealed manifest that is the actual latest accepted workspace state>
```

For the no-rework path, the exact initial tuples are:

| Task | `EVIDENCE_ID` | `SCOPE_SELECTOR` | `PREVIOUS_SCOPE_TSV` |
| --- | --- | --- | --- |
| 1 | `TASK1` | `existing31` | `snapshot/baseline/existing-31-before.tsv` |
| 2 | `TASK2` | `scope32` | `snapshot/manifests/TASK1-scope32-after.tsv` |
| 3 | `TASK3` | `scope32` | `snapshot/manifests/TASK2-scope32-after.tsv` |
| 4 | `TASK4` | `scope32` | `snapshot/manifests/TASK3-scope32-after.tsv` |
| 5 | `TASK5` | `scope32` | `snapshot/manifests/TASK4-scope32-after.tsv` |
| 6 | `TASK6` | `scope32` | `snapshot/manifests/TASK5-scope32-after.tsv` |
| 7 | `TASK7` | `scope32` | `snapshot/manifests/TASK6-scope32-after.tsv` |
| 8 | `TASK8` | `scope32` | `snapshot/manifests/TASK7-scope32-after.tsv` |

Expand `snapshot` to `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce`. Before each command, use `export EVIDENCE_ID=... SCOPE_SELECTOR=... PREVIOUS_SCOPE_TSV=...` with the applicable literal values. For rework, choose the next unused `TASKn_Rk`, force `SCOPE_SELECTOR=scope32`, and point `PREVIOUS_SCOPE_TSV` to the exact latest sealed `scope32-after.tsv` supplied by the failed scoped check or invalidated Task 9 generation. Every command below fails under `set -u` if the coordinator omits these values. The wrapper's successful `TASK_EVIDENCE=SEALED task=$EVIDENCE_ID` plus the module green oracle makes that scope eligible as the next tuple; prose review alone never does.

### Task 1: Register the fixed source and publish the value audit

**Files:**

- Modify: `全栈开发Prompt Chain/report-source.md`
- Modify: `全栈开发Prompt Chain/05-GitHub候选与替代审计.md`
- Create: `全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md`
- Modify: `全栈开发Prompt Chain/README.md`
- Normalize only: approved design and this plan.

**Interfaces:**

- Consumes: fixed repo commit, 2026-09-03 GitHub API metadata, approved design, Task 0 snapshot and explicit normalization authorization.
- Produces: R32, S044–S048, C039–C044, one public audit document, and one README navigation entry.
- Must preserve: R01–R31, S001–S043, C001–C038, existing metadata, existing README module map and platform scope.

- [ ] **Step 1: Run the source-registration failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 1 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 1 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 1 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK1' || "$EVIDENCE_ID" == TASK1_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task1 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK1_STATIC=FAIL'* ]]
print -r -- 'TASK1_STATIC_RED=PASS'
```

Expected before edit: exit code `0` for this wrapper and final line `TASK1_STATIC_RED=PASS`; the nested verifier must exit exactly `1` and print at least one `FAIL` line. Do not weaken the oracle.

- [ ] **Step 2: Append R32 and the supplemental metadata evidence to `report-source.md`**

Use `apply_patch` after R31 and in section 1.2. Record these exact facts:

```text
R32 = SpaceZephyr/pm-skills / SpaceZephyr
stars = 1,033, collected 2026-09-03 Asia/Shanghai
forks = 208
GitHub API license = null
README license claim = MIT
fixed root LICENSE file = not found
pushed_at = 2026-07-09T06:05:41Z
fixed commit = 4c486c7a532de8890e88036533e0a48d578087ed
selected repository JSON SHA-256 = 5ccccb6eab2c3ebcce630bd24e60a2e2f16c9bdd2fe15a77e31509ee763d52d6
selected commit JSON SHA-256 = 94b66a29e1682fc83ecd6b70fc2a56197cfa70d5965b8381a69aafdfdf16d500
```

State that `updated_at` can change without a code push and that stars are a discovery signal, not quality evidence.

- [ ] **Step 3: Append S044–S048 and C039–C044 without renumbering old entries**

Use these source assignments:

```text
S044: X post https://x.com/kongge_space/status/2094622724924838322; oEmbed identifies publication on 2026-09-01; accessed 2026-09-03; oEmbed succeeded; linked X Article body unavailable anonymously.
S045: fixed README and fixed root tree at commit 4c486c7a532de8890e88036533e0a48d578087ed; supports package architecture, workflow list, disclaimer, README license claim, and absence of a root LICENSE in the snapshot.
S046: fixed pm-master/SKILL.md; supports automatic routing, prebuilt chains, and <=10-line handoff behavior.
S047: fixed advisory method files for Mom Test, Torres, Yujun, Story Mapping, Build Trap, and Cagan; supports behavior evidence, opportunity/solution/test, switching cost, journey slice, outcome and four-risk lenses.
S048: fixed execution files for PRD, review, tracking spec, prioritization, roadmap, experiment and postmortem; supports the optional deliverable interfaces and the rejected automatic/default behaviors.
```

Every GitHub file URL must use `blob/4c486c7a532de8890e88036533e0a48d578087ed/…` or `tree/4c486c7a532de8890e88036533e0a48d578087ed`.

Use these claims:

```text
C039 Fact: the README describes 21 Skills with one controller, 13 execution Skills and seven advisory/method Skills.
C040 Fact: pm-master provides automatic routing, prebuilt chains and compact handoffs but does not implement this Chain's Gate/R3 state.
C041 Judgment: retain M00/prompts-99 as the only controller; adopt methods only as module-local Adapters.
C042 Judgment: adopt the decision graph, behavior evidence, story backbone, measurement contract, review findings, sensitivity analysis and action register with rewritten boundaries.
C043 Judgment: reject expert impersonation, auto Web/subagent defaults, fake scores/thresholds, auto tracker/launch and full-package installation.
C044 Boundary: no Skill was installed or run; no E5 product-quality or cross-model benchmark exists.
```

- [ ] **Step 4: Add the PM-Skill candidate decision to `05-GitHub候选与替代审计.md`**

Insert `### 2.4 PM-Skill 2.0 受限来源` after section 2.3. Include one table with these columns and values:

```text
Level: Supplement / conditional Adapter
Candidate: SpaceZephyr/pm-skills@4c486c7a532de8890e88036533e0a48d578087ed
Adopt: decision graph; past-behavior evidence; current alternatives/switching friction; story backbone; four product-risk lenses; measurement contract; review findings; prioritization sensitivity; action register.
Rewrite: expert methods become non-personal lenses; scores become Unknown/ranges; review and experiment outputs remain recommendations.
Reject: pm-master controller; <=10-line authoritative handoff; living-expert impersonation; automatic Web/subagents; fixed RICE/sample/statistical defaults; automatic tracker/launch/publish; HTML/platform-specific output requirements.
License/source boundary: GitHub API license=null; README says MIT; no root LICENSE found; X Article body unavailable anonymously; paraphrase and attribution only.
Runtime: not installed; no E5 evidence.
```

- [ ] **Step 5: Create the public audit document with a complete, non-duplicated structure**

Create `08-PM-Skill-2.0核心工作流评估与融合.md` with this complete initial text; links and field names are part of the contract:

```markdown
# PM-Skill 2.0 核心工作流评估与融合

## 1. 结论

本项目只采用 PM-Skill 2.0 中有独立决策价值的方法，并将其改写为现有 M02–M13 内的受限 Adapter。不安装或运行原 Skill，不复制原提示词、人格或模板，不引入 `pm-master`、M14、A14、G7、第二控制器或第二状态机。M00–M13、A00–A13、G0–G6 和 R3 仍是唯一流程、产物、决定与授权体系。

## 2. 可复核来源与限制

| Source | Scope | Fixed reference | Limitation |
| --- | --- | --- | --- |
| S044 | [X 入口帖](https://x.com/kongge_space/status/2094622724924838322) | oEmbed 显示发布于 2026-09-01；2026-09-03 访问 | 链接的 X Article 正文无法匿名完整取得，不得声称已审读全文 |
| S045 | [README](https://github.com/SpaceZephyr/pm-skills/blob/4c486c7a532de8890e88036533e0a48d578087ed/README.md) 与 [root tree](https://github.com/SpaceZephyr/pm-skills/tree/4c486c7a532de8890e88036533e0a48d578087ed) | `4c486c7a532de8890e88036533e0a48d578087ed` | README 声称 MIT，但 GitHub API `license=null`，且固定快照未找到根 `LICENSE`；只做归纳与归因，不复制原文 |
| S046 | [`pm-master/SKILL.md`](https://github.com/SpaceZephyr/pm-skills/blob/4c486c7a532de8890e88036533e0a48d578087ed/pm-master/SKILL.md) | 同一 commit | 可审核自动路由、预置 chain 和紧凑交接，但原控制器没有本项目 Gate/R3 语义 |
| S047 | [advisory suite](https://github.com/SpaceZephyr/pm-skills/tree/4c486c7a532de8890e88036533e0a48d578087ed/pm-advisory-suite) | 同一 commit | 只吸收行为证据、机会、切换摩擦、旅程切片、Outcome 和四项产品风险视角，不扮演真实专家 |
| S048 | [execution Skills](https://github.com/SpaceZephyr/pm-skills/tree/4c486c7a532de8890e88036533e0a48d578087ed) | 同一 commit | 审核 PRD、review、tracking、prioritization、survey、roadmap、experiment 和 postmortem 的交接接口；排除自动/默认副作用 |

2026-09-03 采集的发现信号为 1,033 stars、208 forks、`pushed_at=2026-07-09T06:05:41Z`。stars 不是质量证据，`updated_at` 也可在没有 code push 时变化。完整证据链见 [`report-source.md`](report-source.md)。本次没有安装、运行或跨模型比较原 Skill，因此无 E5 产品质量或 benchmark 证据。

## 3. 原核心工作流

来源方法可压缩为两条互补的链：

1. 过去行为和当前替代证据 → Opportunity → 价值/切换摩擦 → journey thin slice → Outcome → Value/Usability/Feasibility/Viability 四项产品风险。
2. PRD → pre-build review → tracking specification → experiment → production evidence → postmortem/action。

这是对外部方法的归纳，不是本项目的执行顺序。本项目仍由 M00 和 `prompts/99` 选择当前模块，一次只运行一个模块，到 Gate 必须停止。

## 4. 价值审计

| Method | Independent value | Existing coverage | Decision | Rewrite boundary |
| --- | --- | --- | --- | --- |
| `pm-master` | 统一路由和链路可降低漏步 | M00 + `prompts/99` 已有更强 Gate/R3/恢复 | Reject | 不引入第二控制器 |
| compact handoff | 降低上下文成本 | Axx Handoff 已有完整证据/权限契约 | Rework | 紧凑索引可指向 Axx，不得代替完整 Handoff |
| Mom Test lens | 优先过去行为与已付出成本 | M03 已有证据/反例 | Adopt | 过去购买或承诺只能增强证据，不是通用硬 Gate |
| Torres lens | 把 Outcome、Opportunity、Candidate 和 Test 分开 | 现有模块语义已有，缺稳定 ID 边 | Adopt | 纳入产品决策图，不引入新 Agent |
| Yujun lens | 当前替代、获益与切换摩擦使价值更可检验 | M02/M03/M04 部分覆盖 | Adopt | 未知成本不伪量化 |
| Story Mapping | 用旅程和异常路径找端到端 thin slice | M05/M07 部分覆盖 | Adopt conditionally | 不强制 workshop 形式，不把地图当批准 |
| Build Trap lens | 以 Outcome 而不是功能数衡量进展 | M04/M11/M12 已有结果视角 | Adopt | Outcome 必须可观测，不自动推导因果 |
| Cagan four risks | 在构建前暴露价值/可用/可行/可持续性风险 | 现有安全/工程审查更广 | Adopt as product lens | 不覆盖安全、隐私、合规、无障碍、可靠性或 AI 安全 |
| PRD | 结构化问题、范围和验收 | A05 已更强 | Reject template; retain interfaces | 不复制 PRD 模板，不把假设填成需求 |
| review board | 构建前跨视角发现高代价问题 | M09 主要是实现后只读审查 | Adopt conditionally in M05 | finding 是建议；`0 blocker` 不是 Gate |
| tracking spec | 固定指标/事件语义和数据 QA | M05/M07/M08/M11/M12 交接缺口 | Adopt | M05 独占 MET/EVT 语义；定义不等于已埋点或可读生产 |
| prioritization | 暴露排序对未知输入的敏感性 | M04 有取舍，缺 rank reversal | Adopt conditionally | 不伪造 RICE/ICE 分数，不写 backlog |
| survey | 规模化、分群或定量补证据 | M03 有访谈，问卷契约不完整 | Adopt conditionally | 只写 plan，不发送、招募、虚构回答或套用通用样本量 |
| roadmap | 多 initiative 时显式表达依赖、容量和改向条件 | M07 有 DAG，缺组合视图 | Adopt conditionally | 只给情景/轮廓，不承诺日期或写 tracker |
| experiment | 预注册假设、暴露、护栏和决策规则 | M12 已强覆盖 | Retain existing; add lineage | 结果只产生 recommended decision，真实动作仍需四项合取 |
| postmortem | 将事实、因果假设、反证和行动连起来 | M11/M13 已有复盘，行动接口偏弱 | Adopt action register | 不归咎个人，不自动创建任务或写长期记忆 |

## 5. 产品决策图

| Entity | ID prefix | Semantic owner |
| --- | --- | --- |
| Outcome | `OUT` | M04 |
| Opportunity | `OPP` | M03 |
| Candidate | `CAN` | M04 |
| Hypothesis | `HYP` | M04 |
| Test | `TST` | M06 或 M12，两模块不复用同一 ID |
| Slice | `SLC` | M07 |
| Metric | `MET` | M05 |
| Event | `EVT` | M05 |
| Decision | `DEC` | 现有人类决定者或 Gate；Agent 只能 `proposed` |

合法边只有：`Evidence_Ref -[supports|refutes]-> Opportunity_ID`、`Opportunity_ID -[contributes_to]-> Outcome_ID`、`Candidate_ID -[addresses]-> Opportunity_ID`、`Hypothesis_ID -[applies_to]-> Candidate_ID`、`Test_ID -[tests]-> Hypothesis_ID`、`Slice_ID -[realizes]-> Candidate_ID or A05 Spec`、`Metric_ID -[measures]-> Outcome_ID | Opportunity_ID | Hypothesis_ID | safety_guardrail`、`Metric_ID -[derived_from]-> Event_ID` 和 `Decision_ID -[governs]-> Entity_ID`。

每个实体保存稳定 ID、`rev`、当前语义、`Created_by_Module` 和 `Superseded_by`。实质语义或范围改变时创建新 ID，不覆写旧语义。Decision 默认 `proposed`；只有现有决定者/Gate 提供当前权威引用、owner、日期、适用 Gate/授权范围、证据和失效条件时，才能记录非 proposed 状态。

`active` 不是持久状态；每次消费时重新派生。只有 `Status=approved`、`Authoritative_decision_ref` 仍指向当前版本、未过期、未命中 `invalidated_by`、实体 rev 当前且未 supersede 时才为 active。已存在但不适用的 ID 必须由同一权威体以完整 `closed-not-applicable` Decision 关闭；从未创建的可选 ID 不产生空关闭记录。完整 schema 见[2026-09-03 已批准设计](docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md)。

## 6. M02–M13 受限映射

| Module | Triggered Adapter | Owned IDs | Consumed IDs | Cannot conclude | Handoff |
| --- | --- | --- | --- | --- | --- |
| M02 | competitor transfer | none | evidence refs | 竞品功能等于需求/已交付 | A02 证据给 M03/M04 |
| M03 | behavior-to-opportunity; optional survey | OPP | A02 evidence | 单样本代表市场 | A03 机会与证据边给 M04 |
| M04 | graph, four risks, optional sensitivity | OUT/CAN/HYP；仅记录 DEC | OPP/current constraints | 方法分类等于批准 | A04 给 M05/M06/G2 |
| M05 | journey, measurement, optional pre-build findings | MET/EVT | active A04/A05 facts | 定义完成等于已埋点 | A05 给 M06/M07/M09 |
| M06 | hypothesis test | TST | active HYP | 原型完成等于产品验证 | A06 返回 M04 或给 M07 |
| M07 | walking skeleton; optional Roadmap | SLC | CAN/A05/HYP/MET/EVT | 计划等于 G4/排期承诺 | A07 给 G4/M08 |
| M08 | implementation trace | none | active SLC/MET/EVT/DEC | ticket 等于产品批准 | A08 实现证据给 M09 |
| M09 | risk/measurement verification | none | fixed A04/A05/A07/A08 range | 无 finding 等于可发布 | A09 findings 给 M10/G5 |
| M11 | feedback/action register | none | 获准证据和 active IDs | 相关性等于因果 | A11 返回 M03/M04/M05/M12/M13 |
| M12 | experiment decision | independent TST | active HYP/MET/EVT/DEC | 统计结果等于上线决定 | A12 只给 recommended decision |
| M13 | retrospective action | none | Axx/evidence/IDs | 叙事完整等于根因 | A13 候选学习/行动等人工决定 |

M00、M01 和 M10 不增加方法。`prompts/99` 只传递通过派生 active 检查的 ID/权威引用，或传递权威显式关闭；不创建路由、Gate 或授权。

## 7. 条件分支

| Adapter | Trigger | Minimum evidence | Stop/omit rule |
| --- | --- | --- | --- |
| Survey | 已有假设需要更大样本、分群或定量补证据 | research question、人群、假设、决定、样本框和 consent boundary | 样本框/同意不清时仅保留 A03 draft，不发送 |
| Prioritization sensitivity | 至少两个候选竞争同一范围/资源 | 目标贡献、成本、风险、可逆性、依赖和假设区间 | 排序可易反转时标不稳定，留给 G2 |
| Journey backbone | 功能跨多步骤、状态或异常路径 | A04、用户旅程事实、领域状态 | 主路径/状态不清时写 Open questions |
| Measurement contract | Outcome/Hypothesis/acceptance/safety 需要测量 | 目的、获准数据边界、schema/source-of-truth 事实 | 目的、隐私或权威源不清时保持 draft |
| Pre-build findings | 高影响、跨职能、难逆或用户明确要求 | 固定版本 A04/A05/原型证据和适用规范 | blocker 返回 M04/M05；finding 不产生授权 |
| Roadmap | 多 initiative、共享依赖或资源冲突 | 已批准优先级、依赖和容量事实/明示假设 | 依赖/容量不足时只给命名情景，不给日期 |

其他 Adapter 也遵循同一规则：触发为 false 时省略该表，不生成空占位。上游已存在的 ID 则必须消费、传递或权威关闭，不得借“未触发”静默丢失。

## 8. 安全与授权

- G0 只定义数据目的、对象、字段、窗口、保留和访问范围。
- G3 批准数据模型、隐私、保留与架构取舍；G4 批准精确代码/埋点实现及 `ALLOWED_FILES`。
- M11 的生产查询/导出需对象级、未过期 R3；外部 analytics/provider 配置变更另需匹配 R3。任一层不代替另一层。
- M12 真实 launch/stop/extend/traffic/flag/publish 的必要且同时条件为 `MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION`。没有真实 receipt 时写 `Not launched / no production verification`。
- `0 blocker`、统计显著、指标上涨、review finding 或多视角一致都不构成产品、法务、安全、Gate 或外部动作批准。

## 9. 消融式删减检查

每个模块初稿形成后，固定模块目标、产物契约、安全边界、下游输入和验收，再对新增 method、field、table、term 和 check 每次只移除一项。不改变决定质量、证据追踪、安全边界或下游可消费性的候选删除；与现有规则重复者合并；承载必要边界者保留并记录理由。stars、方法知名度、表格更完整或文字更多不是保留理由。

## 10. 使用入口

- 生命周期位置：[`03-AI产品全生命周期映射.md`](03-AI产品全生命周期映射.md)
- 模块职责与交接：[`04-模块化Skills工作流.md`](04-模块化Skills工作流.md)
- 操作手册：[`06-Prompt-Chain使用手册.md`](06-Prompt-Chain使用手册.md)
- 标准 Prompt：[`prompts/`](prompts/)中的 M02–M09、M11–M13
- 人机对话 Prompt：[`prompts_ask/`](prompts_ask/)中的对应模块
- 唯一控制器：[`prompts/99-端到端Prompt-Chain.md`](prompts/99-端到端Prompt-Chain.md)
```

Do not copy source wording or include first-person expert roleplay.

- [ ] **Step 6: Add the one-line README navigation entry**

Between the existing 07 and `report-source.md` entries, add:

```markdown
- [`08-PM-Skill-2.0核心工作流评估与融合.md`](08-PM-Skill-2.0核心工作流评估与融合.md)：PM-Skill 2.0 的价值审计、受限 Adapter、产品决策图和模块投影。
```

- [ ] **Step 7: Normalize only Task 1 files plus the approved design and plan**

Run the authorized helper with exactly these paths:

```zsh
set -euo pipefail
for relative in \
  '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md' \
  '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'; do
  /usr/bin/cmp -s \
    <(/bin/cat "/Users/lute/Project/vibecoding_config/$relative") \
    <(/bin/cat "/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/preimage/$relative") || {
      print -u2 "normalization-only content drift: $relative"
      exit 64
    }
done
print -r -- 'TASK1_NORMALIZATION_ONLY_CONTENT=PASS files=2'
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/report-source.md' \
  '全栈开发Prompt Chain/05-GitHub候选与替代审计.md' \
  '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md' \
  '全栈开发Prompt Chain/README.md' \
  '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md' \
  '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
```

Expected exit `0`, `TASK1_NORMALIZATION_ONLY_CONTENT=PASS files=2`, `TASK1_NORMALIZATION_ONLY_SIX_VALUES=PASS files=2`, `TASK_NORMALIZATION=PASS task=$EVIDENCE_ID files=6`, `TASK_SCOPE=PASS files=32 non_task_unchanged=26`, and `TASK_EVIDENCE=SEALED task=$EVIDENCE_ID scope=32 protected=44 zip=1`.

- [ ] **Step 8: Run the source-registration pass oracle and scoped advisory review**

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task1
print -r -- 'TASK1_SOURCE_AUDIT=PASS'
```

Expected exit `0`, `TASK1_STATIC=PASS`, and `TASK1_SOURCE_AUDIT=PASS`. The verifier checks unique R32/S044–S048/C039–C044 IDs, immutable older rows, full fixed-commit file/tree links, README navigation, ten audit sections, license conflict, no-install and no-E5 boundaries.

Perform the factual-boundary and licensing checklist as scoped advisory input. It creates no standalone PASS receipt and does not satisfy the final independent-review gate. Any finding returns to Step 2–7 under a fresh `EVIDENCE_ID`; only the three Task 9 reports can authorize completion.

---

### Task 2: Add the cross-module workflow contract and controller invariant

**Files:**

- Modify: `全栈开发Prompt Chain/03-AI产品全生命周期映射.md`
- Modify: `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- Modify: `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- Modify: `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`

**Interfaces:**

- Consumes: public audit and approved design.
- Produces: one lifecycle projection, one canonical workflow handoff summary, one usage rule, and either one controller invariant or a recorded ablation decision that leaves the controller cat-identical to Task 0 preimage.
- Must preserve: 36/36 source-Skill mapping, M00–M13 module registry, G0–G6, four scenario chains, R3 fields, existing UI and ablation rules.

- [ ] **Step 1: Run the workflow-contract failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 2 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 2 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 2 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK2' || "$EVIDENCE_ID" == TASK2_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task2 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK2_STATIC=FAIL'* ]]
print -r -- 'TASK2_STATIC_RED=PASS'
```

Expected before edit: nested exit `1`, at least one `FAIL`, and wrapper output `TASK2_STATIC_RED=PASS`.

- [ ] **Step 2: Add the lifecycle projection without touching the 36/36 table**

Before `## 5. 系统级结论`, add `### 4.1 PM-Skill 2.0 受限投影` with this compact mapping:

```text
M02 competitor transfer
M03 behavior-to-opportunity + optional survey
M04 Outcome/Candidate/Hypothesis semantics + existing human/Gate Decision recording + four product risks + optional sensitivity
M05 story backbone + Metric/Event + optional pre-build findings
M06 Hypothesis -> Test
M07 Candidate/Spec -> Slice + instrumentation ticket + optional Roadmap
M08 approved Slice/Metric/Event implementation only
M09 read-only risk/measurement closure
M11 evidence/action register
M12 Hypothesis/Metric/Event -> independent Test and recommended decision
M13 causal hypothesis/action/learning candidate
M00/M01/M10 unchanged; prompts/99 only preserves active references
```

Link to the new 08 audit. Do not add any row to the original 36/36 mapping.

- [ ] **Step 3: Add the single workflow handoff contract and module-local projections**

Immediately before the existing `## 4. M00–M13 模块工作流`, add `### 3.1 产品决策图交接契约`. Define only:

```text
Entity IDs: OUT, OPP, CAN, HYP, TST, SLC, MET, EVT, DEC. Each entity carries stable ID, rev, current meaning, Created_by_Module and Superseded_by; a material semantic/scope change creates a new ID and supersedes the old one.
Ownership: M03=OPP semantics; M04=OUT/CAN/HYP semantics and product-Decision recording only; M05=MET/EVT semantics; M06/M12=independent TST; M07=SLC. Decision authority remains the existing human decision owner or Gate; an Agent can only propose.
Evidence refs: reuse the existing source-reference mechanism; each Evidence_Ref records source, acquisition date, applicability, evidence level and limitation. Do not create a second global evidence registry.
Opportunity evidence cardinality: every decision-stage Opportunity has at least one `Evidence_Ref -[supports]-> Opportunity_ID` edge. Counterevidence uses a separate `Evidence_Ref -[refutes]-> Opportunity_ID` edge and must not be placed in `supports`. Evidence_Ref and Opportunity_ID relations are many-to-many: one Evidence_Ref may support or refute multiple Opportunities, and one Opportunity may have multiple Evidence_Refs.
Cardinality: every decision-stage OPP contributes to at least one OUT; every CAN addresses at least one OPP; every HYP applies to at least one CAN; every TST tests at least one HYP; every SLC realizes at least one approved CAN or A05 Spec; every MET measures at least one allowed target; every event-derived MET derives from at least one EVT; every non-proposed DEC governs at least one entity. All listed relations may have multiple targets or sources where the approved design permits them.
Consumption: `active` is derived at consumption time, never stored as another status. It is true only when Decision Status=`approved`, `Authoritative_decision_ref` still names the current version, expiry has not elapsed, no `invalidated_by` condition is true, and the referenced entity rev is current. Missing, rejected, inconclusive, expired, invalidated or superseded refs stop as blocker. Once expiry elapses, an `invalidated_by` condition becomes true, the authoritative reference is no longer current, or the governed entity revision is superseded, the old Decision is immediately non-consumable. Downstream remains blocked until the same existing human decision owner or Gate creates a successor Decision or supersedes the old record and re-decides. An Agent may not manufacture that authority.
Closure: a known upstream ID can be closed as not applicable only through a Decision with Status=`closed-not-applicable`, Authoritative_decision_ref, Decision_owner, Decision_date, Expiry_or_invalidated_by, Evidence_Refs and applicable Gate/authorization scope; otherwise it is propagated or remains a blocker. A branch that never created an ID is simply omitted and does not invent a closure record.
Handoff: artifact/version, IDs/rev, Facts/Decisions/Assumptions/Open questions, Gate, G0, R3, verification level, not-executed receipt, one next safe action.
```

In each existing module section, add exactly the corresponding projection below. Do not copy the nine-entity schema into each module. Keep M00/M01/M10 text unchanged.

```text
M02: 条件式输出竞品迁移证据，只供 M03/M04 消费，不创建产品实体或批准。
M03: 创建/修订 OPP 及 supports/refutes 证据边；可选 survey-plan 仅输出草案，不发送。
M04: 创建/确认 OUT，以 contributes_to 绑定 OPP，创建 CAN/HYP 及 addresses/applies_to 边；只记录现有决定者/Gate 的 DEC，Agent 默认只提出 proposed。
M05: 条件式输出 journey backbone、MET/EVT 语义及 measures/derived_from 边、pre-build findings；不创建 SLC。
M06: 对 Priority: riskiest 的 HYP 创建独立 TST 和 tests 边，只输出学习证据。
M07: 为已批准 CAN/A05 Spec 创建 SLC 和 realizes 边，只引用 M05 的 MET/EVT 并创建 instrumentation ticket；Roadmap 只在触发时输出。
M08: 只实现可追溯到 active Decision、A05/A07、G3/G4 和精确范围的 SLC/MET/EVT，不新增产品语义。
M09: 在 fixed review range 上只读核对产品风险、测量契约、findings 和 lineage，无证据则记 Unverified scope。
M11: 只在有获准生产证据、用户反馈或 incident 事实时输出证据/行动登记，无生产授权则仅用现有材料。
M12: 消费 active HYP 和 M05-owned MET/EVT，创建独立 TST/tests 边，只输出 recommended decision；真实动作仍需四项授权合取。
M13: 在可复核结果存在时分离事实、因果假设、反证、行动与候选学习，不创建 tracker 或自动写入长期记忆。
```

- [ ] **Step 4: Add the operator-facing handoff rules to the manual**

Immediately after the existing `## 7. 产物交接` section and immediately before the existing `## 8. 四条推荐场景链`, add `### 7.1 产品决策图交接`. Include this example:

```text
Decision graph refs:
- Consumes: OPP-001@rev2, HYP-003@rev1, DEC-004@rev1
- Produces: TST-002@rev1
- Decision active check: PASS | BLOCKED; PASS requires Status=`approved`, Authoritative_decision_ref still current, unexpired, no invalidated_by match, current entity rev, and no supersession. `active` is derived here, not stored.
- Explicitly closed: known ID + `closed-not-applicable` Decision + Authoritative_decision_ref + Decision_owner + Decision_date + Expiry_or_invalidated_by + applicable Gate/authorization scope + Evidence_Refs; or NONE when no optional ID was ever created.
```

Explain that an Adapter is a conditional check inside the current module. If its trigger is false, omit its table. A compact index can point to Axx but cannot replace the complete Handoff. The operator-facing Handoff must preserve source/date/applicability/evidence-level/limitation for each Evidence_Ref and must state `Consumes`, `Produces`, `Explicitly closed`, and unresolved blocker IDs rather than relying on a prose summary.

Add the exact stale-authority instruction: `Downstream remains blocked until the same existing human decision owner or Gate creates a successor Decision or supersedes the old record and re-decides.` State that the Agent cannot synthesize this authority.

For every canonical and dialogue prompt changed in Tasks 3–8, insert exactly the corresponding value from `verify-chain.rb::LINEAGE_LINES` immediately inside the existing `## Handoff` section. Do not paraphrase it, place it elsewhere, add a second `Decision lineage:` line, or use different canonical/dialogue values. The executable verifier extracts only the Handoff section and rejects any missing, duplicate, relocated or altered line.

- [ ] **Step 5: Add exactly one controller discipline item, then test whether it survives ablation**

After current global discipline item 12 and before `模块注册表`, add:

```text
13. 产品决策图兼容：当前 Axx 含产品实体或 Decision 时，下游只消费派生 `active` 检查为真的当前 rev：Decision Status 必须为 `approved`、`Authoritative_decision_ref` 仍指向当前版本、未到 expiry、`invalidated_by` 条件均未命中，且实体未被 supersede。`active` 只在消费时计算，不是持久状态。已存在但不适用的 ID 必须由现有决定者/Gate 以含 `Authoritative_decision_ref`、`Decision_owner`、`Decision_date`、`Expiry_or_invalidated_by`、`Evidence_Refs` 和适用 `Gate_or_authorization_ref` 的 `closed-not-applicable` Decision 关闭；从未创建的可选 ID 不生成空关闭记录。缺失、未批准、过期、被 invalidated/superseded 或所有权冲突时停止，不创建第二路由、Gate 或授权。
```

Do not change the module routes or controller acceptance block.

After the item is added, compare it against the existing Handoff, `Controller acceptance` and R3 contract. If removing it preserves the complete active-reference/explicit-closure requirement without weakening downstream consumption, use `apply_patch` to remove the whole item before normalization and record `remove` in the Task 9 ablation ledger. Otherwise retain exactly one copy and record `retain`; a partial duplicate must be merged into this one item and recorded as `merge`. The verifier accepts only the exact item above or a controller whose cat stream is byte-identical to Task 0 preimage.

- [ ] **Step 6: Normalize exactly the four Task 2 files**

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/03-AI产品全生命周期映射.md' \
  '全栈开发Prompt Chain/04-模块化Skills工作流.md' \
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md' \
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
```

- [ ] **Step 7: Run workflow invariants and review**

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task2
rg -Fq '用户可见 UI 变更' '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
rg -Fq '消融路由' '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
rg -Fq 'Target、Action、Expected effect、Credential scope' '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
print -r -- 'TASK2_WORKFLOW=PASS'
```

Expected exit `0`, `TASK2_STATIC=PASS`, and `TASK2_WORKFLOW=PASS`. The verifier compares module registry/default-route lines with the sealed preimage, requires the exact M00–M13/A00–A13 registry, checks the original 36/36 total and the three new documentation headings, and accepts only the exact controller item or a controller cat-identical to preimage. Perform the no-second-schema/no-new-Gate checklist as scoped advisory input; any finding requires a fresh Task 2 attempt. It is not an independent gate or receipt; Task 9 owns that gate.

---

### Task 3: Integrate discovery and strategy into canonical M02–M04 prompts

**Files:**

- Modify: `全栈开发Prompt Chain/prompts/02-机会与市场调研.md`
- Modify: `全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md`
- Modify: `全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md`

**Interfaces:**

- Consumes: A00/A01 context, A02 evidence, A03 problem evidence, decision graph contract.
- Produces: competitor transfer evidence; M03-owned `Opportunity_ID`; M04-owned `Outcome_ID`/`Candidate_ID`/`Hypothesis_ID`; product `Decision_ID` records whose authority remains an existing human decision owner or Gate; risk/sensitivity records.
- Must preserve: MODE=PLAN, G1/G2 human decisions, source/consent/PII boundaries, no implementation or external action.

- [ ] **Step 1: Run the M02–M04 failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 3 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 3 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 3 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK3' || "$EVIDENCE_ID" == TASK3_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task3 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK3_STATIC=FAIL'* ]]
print -r -- 'TASK3_STATIC_RED=PASS'
```

Expected before edit: nested exit `1`, at least one `FAIL`, and wrapper output `TASK3_STATIC_RED=PASS`.

- [ ] **Step 2: Add competitor transfer to M02**

Immediately after the existing `## Current alternatives` section and before `## Opportunity evidence`, add this A02 Adapter. Its trigger sentence must be exact and must not add a decision-impact gate:

```markdown
## Competitor transfer
仅在用户要求竞品、替代方案或市场比较时生成；决策影响只决定研究深度和下一问题，不是附加触发条件。

| Subject | Observable fact | Target context | Enabling constraints | Counterevidence | Transferable principle | Non-transferable context | Evidence refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

State that unavailable sources are downgraded, A02 provides evidence to M03/M04, and M02 cannot create `Opportunity_ID`, product approval or a claim of tested parity. Add the exact sentence `Evidence_Ref fields: source, acquisition date, applicability, evidence level, limitation.` Extend `## Handoff` with the exact Evidence refs, unresolved transfer limits, M03/M04 consumers, and the exact M02 `LINEAGE_LINES` value; do not imply a product entity was created.

- [ ] **Step 3: Add behavior-to-opportunity and survey-plan modes to M03**

Extend `RESEARCH_MODE` with `survey-plan`. In the method, state that M03 creates `Opportunity_ID` and evidence polarity but does not require a not-yet-created `Outcome_ID`.

Immediately after the existing `## Evidence table` section and before `## Segments and excluded users`, add:

```markdown
## Evidence-to-opportunity map
| Opportunity_ID | Rev | Created_by_Module | Status | Observation | Evidence_Refs + supports/refutes edges | Current alternative | Cost and friction | Affected segment/context | Counterevidence | Evidence quality | Opportunity hypothesis | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Optional survey plan
仅当 `RESEARCH_MODE=survey-plan` 时生成。

| Research question | Question | Response type | Hypothesis ref | Decision affected | Sample frame | Bias review | Consent/distribution boundary | Response-quality check | Preregistered analysis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Add these exact rules: `Every decision-stage Opportunity has at least one \`Evidence_Ref -[supports]-> Opportunity_ID\`.` `Counterevidence uses a separate \`Evidence_Ref -[refutes]-> Opportunity_ID\` and must not be placed in \`supports\`.` `Evidence_Ref and Opportunity_ID relations are many-to-many.` Set `Created_by_Module=M03` and default Status to `proposed`. Non-material clarification increments `Rev`; a material semantic/scope change creates a new ID, preserves the old meaning and sets `Superseded_by`. The survey branch is triggered only when an existing hypothesis needs larger-sample, segment-comparison or quantitative evidence. It drafts only. It does not send, recruit, invent responses or use a universal sample size. Missing sample frame or consent/distribution boundary is a stop condition for the branch and remains in `Assumptions`/`Open questions`. Extend `## Handoff` with produced `Opportunity_ID@rev`, supports/refutes Evidence refs, supersession state, consumers, every unresolved known ID and the exact M03 `LINEAGE_LINES` value.

- [ ] **Step 4: Add the decision graph, product-risk review and optional sensitivity to M04**

Add `A00_PATH` and `A01_PATH` inputs. M04 creates or confirms Outcome, binds Opportunities, then creates separate Candidate and Hypothesis nodes. Immediately after the existing `## Recommended choice` section and before `## MVP scope`, add these A04 sections:

```markdown
## Product decision graph
| Entity ID | Rev | Type | Meaning | Legal edges | Evidence_Refs | Status | Created_by_Module | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |

| Decision_ID | Governs | Status | Authoritative_decision_ref | Decision_owner | Gate_or_authorization_ref | Decision_date | Expiry_or_invalidated_by | Evidence_Refs | Superseded_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Product risk review
| Lens | Evidence | Unknown | Consequence | Cheapest reversible test |
| --- | --- | --- | --- | --- |
| Value | | | | |
| Usability | | | | |
| Feasibility | | | | |
| Viability | | | | |

## Prioritization sensitivity
仅在至少两个候选竞争同一范围或资源时生成。

| Candidate_ID | Outcome contribution | Evidence-backed cost/risk/reversibility | Assumption range | Recommended order | Objection | Rank-reversal condition |
| --- | --- | --- | --- | --- | --- | --- |
```

Use only these M04-local legal edges: `Opportunity_ID -[contributes_to]-> Outcome_ID`, `Candidate_ID -[addresses]-> Opportunity_ID`, `Hypothesis_ID -[applies_to]-> Candidate_ID`, and `Decision_ID -[governs]-> Entity_ID`. Each decision-stage Opportunity binds at least one Outcome; each Candidate addresses at least one Opportunity; each Hypothesis applies to at least one Candidate; each non-proposed Decision governs at least one entity; these relations may be many-to-many. The current largest unknown carries `Priority: riskiest`. For OUT/CAN/HYP, non-material clarification increments `Rev`; a material semantic/scope change creates a successor ID, preserves the old meaning and sets `Superseded_by`.

Add these three lifecycle paragraphs without paraphrase: `Decision authority: every Agent-created Decision defaults to \`proposed\`. A non-proposed Decision may be recorded only when the existing human decision owner or Gate supplies \`Authoritative_decision_ref\`, \`Decision_owner\`, \`Decision_date\`, \`Expiry_or_invalidated_by\`, the applicable \`Gate_or_authorization_ref\`, and \`Evidence_Refs\`.` `Decision lifecycle: legal transitions are \`proposed -> approved | rejected | inconclusive | closed-not-applicable\`. New evidence after \`inconclusive\` creates a new revision or successor and never rewrites the old record to \`approved\`. A material change to \`approved\`, \`rejected\`, or \`closed-not-applicable\` creates a successor and marks the old Decision \`superseded\`. \`superseded\` is terminal and cannot be restored or silently overwritten.` `Decision invalidation: once expiry elapses, an \`invalidated_by\` condition becomes true, the authoritative reference is no longer current, or the governed entity revision is superseded, the old Decision is immediately non-consumable. Downstream remains blocked until the same existing human decision owner or Gate creates a successor Decision or supersedes the old record and re-decides. \`active\` is derived only at consumption and is never stored.` Add the exact sentence `M04 cannot create Metric/Event definitions; the existing Metric tree records measurement intent and desired outcome only.` M04 does not implement, auto-rank or replace G2. Extend `## Handoff` with consumed/produced IDs and revs, current authoritative Decision refs, explicit closures, blockers, M05/M06/G2 consumers and the exact M04 `LINEAGE_LINES` value.

- [ ] **Step 5: Normalize Task 3 and run pass oracles**

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/prompts/02-机会与市场调研.md' \
  '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md' \
  '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md'
```

Run:

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task3
rg -Fq 'G1' '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md'
rg -Fq 'G2' '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md'
rg -Fq 'consent' '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md'
rg -Fq 'PII' '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md'
for relative in \
  '全栈开发Prompt Chain/prompts/02-机会与市场调研.md' \
  '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md' \
  '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md'; do
  rg -Fq 'MODE=PLAN' "$relative"
done
rg -Fq '不发送' '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md'
rg -Fq 'M04 cannot create Metric/Event definitions' '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md'
print -r -- 'TASK3_DISCOVERY_STRATEGY=PASS'
```

Expected exit `0`, `TASK3_STATIC=PASS`, and `TASK3_DISCOVERY_STRATEGY=PASS`.

- [ ] **Step 6: Perform the Spec and ablation scoped advisory check**

Check that M02 does not own Opportunity, M03 does not need Outcome, M04 separates Candidate/Hypothesis, and no table is unconditional. Remove duplicate prose while retaining evidence and Gate boundaries. This checklist creates no PASS receipt; a finding requires a fresh Task 3 attempt, while Task 9 remains the only independent blocking review.

---

### Task 4: Integrate specification, hypothesis testing and walking skeleton into canonical M05–M07 prompts

**Files:**

- Modify: `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`

**Interfaces:**

- Consumes: A04/A05 draft facts for specification only; active Decision refs for downstream consumption; a current Candidate_ID or A05 Spec with an applicable existing approval before M07 may create a Slice; A06 hypothesis evidence.
- Produces: journey backbone, `Metric_ID`/`Event_ID`, review findings, `Test_ID`, `Slice_ID`, instrumentation tickets and optional delivery outline.
- Must preserve: A04 precondition, G3/G4, existing UI and ablation sections, prototype sandbox, tracker-preview and no external write.

- [ ] **Step 1: Run the M05–M07 failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 4 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 4 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 4 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK4' || "$EVIDENCE_ID" == TASK4_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task4 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK4_STATIC=FAIL'* ]]
print -r -- 'TASK4_STATIC_RED=PASS'
```

Expected before edit: nested exit `1`, at least one `FAIL`, and wrapper output `TASK4_STATIC_RED=PASS`.

- [ ] **Step 2: Add M05-owned journey, measurement and pre-build contracts**

M05 is the only semantic owner of Metric/Event. Immediately after the existing `## UI context and visual acceptance` section and before `## Functional requirements`, add the Journey, Measurement and Pre-build blocks below in that order. Add the journey section only when the feature crosses multiple user steps, states or failure paths. Add the measurement section only when an Outcome, Opportunity, Hypothesis, acceptance criterion or safety guardrail requires behavior/system measurement. Add pre-build findings only for a high-impact, cross-functional or hard-to-reverse spec, or when the user explicitly requests pre-build review. If a trigger is false, omit that table rather than emitting an empty shell.

```markdown
## Journey backbone
仅当功能跨多个用户步骤、状态或失败路径时生成。

| Actor/context | Entry | Activity | Key task/state | Completion | Failure/recovery | Proposed first thin slice |
| --- | --- | --- | --- | --- | --- | --- |

## Measurement contract
仅当 Outcome、Opportunity、Hypothesis、acceptance 或 safety guardrail 需要行为/系统测量时生成。

| Entity_ID | Rev | Created_by_Module | Type | Purpose + measures edge | Semantic definition | Trigger + eligibility | Minimal properties | Identity + deduplication | Source of truth | Privacy/consent/retention/access | Quality check | Proposed owner | Status | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Pre-build review findings
仅对高影响、跨职能、高不可逆规格，或用户明确要求的预实现评审生成。

| Lens | Evidence location | Finding | Consequence | Severity | Proposed action | Decision owner | Re-review condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Add the exact sentence `M05 does not create \`Slice_ID\`; its proposed first thin slice remains specification and measurement intent.` Every Metric has at least one `Metric_ID -[measures]-> Outcome_ID | Opportunity_ID | Hypothesis_ID | safety_guardrail` target; a Metric that depends on events also records at least one `Metric_ID -[derived_from]-> Event_ID`, while a non-event Metric names its source of truth. Multiple targets/events are allowed. Each `Minimal properties` entry states name, type, enum/domain and requiredness; missing schema facts remain `Unknown`. M05-created MET/EVT records default to `proposed`; non-material clarification increments `Rev`, while a material semantic/scope change creates a new ID and sets `Superseded_by`. Default-forbidden measurement fields are direct identifiers, persistent device ID, free text, user content, full URL/query string and precise location. Exceptions state G0→G3→G4→M11/R3 separately. If measurement purpose, privacy boundary or source of truth is unresolved, keep the affected contract draft and block downstream instrumentation; if a quality query's executable conditions are unknown, include only a `not executed` query draft. Pre-build review consumes fixed A04/A05/prototype versions and applicable standards, uses only `product | design | engineering | data | security | privacy | legal | operations` lenses and `blocker | major | minor` severity, and routes a blocker back to M04/M05; findings remain recommendations. `0 blocker` does not mean any Gate passed. Extend `## Handoff` with produced MET/EVT IDs/revs, measurement blockers, findings, M06/M07/M09 consumers and the exact M05 `LINEAGE_LINES` value.

- [ ] **Step 3: Bind M06 prototype evidence to a Hypothesis and independent Test**

Immediately after the existing `## Hypothesis and falsifiable prediction` section and before `## Prototype boundary`, add:

```markdown
## Decision graph trace
| Outcome_ID | Opportunity_ID | Candidate_ID | Hypothesis_ID | Test_ID | Test_rev | Created_by_Module | Legal edge | Learning question | Evidence_Refs | Result | Status | Superseded_by |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
```

Only generate it when A04 contains an active relevant graph and a still-decision-changing `Hypothesis_ID`. M06 creates its own `Test_ID`, records at least one `Test_ID -[tests]-> Hypothesis_ID`, tests a Hypothesis marked `Priority: riskiest`, defaults the Test to `proposed`, and produces learning evidence only. A non-material clarification increments `Test_rev`; a material Test change creates a new ID and `Superseded_by`. Missing safe test mode, target-user/fixture boundary, consent or write scope blocks this Adapter. It does not approve a product, create production implementation or relax G0/G4/sandbox/consent. Extend `## Handoff` with consumed Hypothesis/Decision refs, produced Test ID/rev, result/evidence level, unresolved blocker and the M04/M07 consumer.

- [ ] **Step 4: Add M07-owned Slice, measurement ticket and conditional delivery outline**

Immediately before the existing `## Vertical-slice map`, add `## Product slice and measurement trace` followed by `## Conditional delivery outline`:

```markdown
## Product slice and measurement trace
| Slice_ID | Slice_rev | Created_by_Module | Legal realizes edge to Candidate_ID/A05 Spec | Hypothesis_ID/product risks | UI/API/data/observability path | Acceptance | Metric_ID/Event_ID instrumentation ticket | Verification seam | Status | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Conditional delivery outline
仅在多个 initiative、共享依赖或资源冲突时生成。

| Milestone/outcome | Slice_ID | Dependencies | Capacity assumption | Uncertainty/buffer basis | Critical path | Success signal | Change trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Add these exact rules: `M07 may create a Slice only when the referenced Candidate_ID or A05 Spec is current and has an applicable existing approval.` `Otherwise omit the Product slice table, retain the known Candidate_ID or A05 Spec as a blocker, and do not infer approval.` `Every emitted Slice has at least one \`Slice_ID -[realizes]-> Candidate_ID or A05 Spec\` edge to that approved input.` One Candidate may have multiple Slices. A Slice defaults to `proposed`; non-material clarification increments `Slice_rev`, while a material semantic/scope change receives a new ID with `Superseded_by`. Add the exact sentence `Metric/Event semantic/property changes return to M05; M07 only creates an instrumentation ticket.` If dependency or capacity facts are insufficient, the delivery outline may present named scenarios only and must not give a date. The delivery outline is not a date promise, tracker write or G4 authorization. Extend `## Handoff` with consumed approved Candidate/Spec plus Hypothesis/MET/EVT refs, produced Slice ID/rev, instrumentation tickets, blockers, G4/M08 consumers and the exact M07 `LINEAGE_LINES` value.

- [ ] **Step 5: Normalize Task 4 and run pass oracles**

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md' \
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md' \
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'
```

Run:

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task4
rg -Fq 'UI context and visual acceptance' '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md'
for relative in \
  '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md' \
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md' \
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'; do
  rg -Fq 'Ablation evidence' "$relative"
done
for relative in \
  '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md' \
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'; do
  rg -Fq 'G3' "$relative"
done
for relative in \
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md' \
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'; do
  rg -Fq 'G4' "$relative"
done
rg -Fq 'ALLOWED_FILES_OR_SANDBOX' '全栈开发Prompt Chain/prompts/06-原型与UX验证.md'
rg -Fq 'tracker-preview' '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'
rg -Fq '不执行外部写入' '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'
rg -Fq 'M05 does not create `Slice_ID`' '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md'
rg -Fq 'Metric/Event semantic/property changes return to M05; M07 only creates an instrumentation ticket.' '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md'
print -r -- 'TASK4_SPEC_TEST_SLICE=PASS'
```

Expected exit `0`, `TASK4_STATIC=PASS`, and `TASK4_SPEC_TEST_SLICE=PASS`.

- [ ] **Step 6: Perform the safety and ablation scoped advisory check**

Review data minimization, measurement ownership, prototype authorization and Roadmap non-commitment. Remove redundant UI/ablation text instead of duplicating existing blocks. This checklist creates no PASS receipt; a finding requires a fresh Task 4 attempt.

---

### Task 5: Integrate implementation evidence, quality closure, production learning, experiment and retrospective into canonical prompts

**Files:**

- Modify: `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md`
- Modify: `全栈开发Prompt Chain/prompts/12-增长与实验.md`
- Modify: `全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md`

**Interfaces:**

- Consumes: A04/A05/A07 decision graph and measurement contracts, A08 fixed diff, authorized A11 evidence.
- Produces: implementation trace, read-only closure findings, action registers, experiment Test/decision trace and retrospective actions.
- Must preserve: M08 G4/file/dependency bounds, M09 fixed-range read-only review, M11 G0+R3, M12 four-way launch condition, M13 staged adoption and separate local/R3 authorization.

- [ ] **Step 1: Run the canonical back-half failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 5 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 5 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 5 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK5' || "$EVIDENCE_ID" == TASK5_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task5 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK5_STATIC=FAIL'* ]]
print -r -- 'TASK5_STATIC_RED=PASS'
```

Expected before edit: nested exit `1`, at least one `FAIL`, and wrapper output `TASK5_STATIC_RED=PASS`.

- [ ] **Step 2: Add M08 implementation trace without creating product semantics**

Immediately after the existing `## Ticket and acceptance` section and before `## Preflight`, add:

```markdown
## Product trace implemented
仅在 A07 提供对应 ID 时生成。

| Slice_ID | Active Decision/G3/G4 refs | Metric_ID/Event_ID | Implementation location | Tests/verification | Semantic drift or new field |
| --- | --- | --- | --- | --- | --- |
```

Any missing active ref, semantic change or new collection field is a blocker and returns to M05/M07. M08 cannot infer product approval from a ticket. Extend `## Handoff` with consumed Slice/Decision/G3/G4/MET/EVT refs, actual implementation/test evidence, semantic drift, unverified items and the M09 consumer.

- [ ] **Step 3: Add M09 read-only product-risk and measurement closure**

Immediately after the existing `## Ablation evidence review` section and before `## Security review`, add:

```markdown
## Product risk and measurement review
| ID/ref | Expected contract or risk | A07/A08/fixed-diff evidence | Finding | Severity | Closure evidence or Unverified scope |
| --- | --- | --- | --- | --- | --- |
```

Generate this Adapter only when the fixed review range contains an applicable A04 product-risk record, A05 Metric/Event contract or pre-build finding. No evidence means finding or `Unverified scope`. A blocker routes to its owning M04/M05/M07/M08 module and remains a recommendation, not an automatic fix. No finding does not mean product approval, valid production telemetry or release approval. Keep the exact instruction `Do not query production or modify code.` Extend `## Handoff` with the fixed range, consumed refs, findings/unverified scope, blockers and the M10/G5 consumers.

- [ ] **Step 4: Add one shared action-register shape to M11 and M13**

Add this section to both outputs. In M11 place it immediately after the existing `## Recommended actions` section and before `## External mutations not performed`; in M13 place it immediately after `## Candidate learnings` and before `## Proposed evolution target`:

```markdown
## Action register
| Finding_or_Evidence_ID | Observation | Causal hypothesis | Counterevidence/alternative | Proposed action | Proposed owner | Due/trigger | Verification | Destination module | Status | Status evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

M11 generates the table only when authorized production evidence, user feedback or incident facts support at least one finding/action; without production authorization it can use only already supplied material. M13 generates it only when a task, release, experiment or incident has a reviewable result and at least one action candidate. Add the exact line `Status enum: proposed | accepted | in_progress | verified | rejected | superseded; default=proposed.` Any non-proposed status records confirmer, time and `Evidence_Ref`. Recording a status does not create a tracker, notify anyone or prove execution. M11 may consume active IDs but cannot redefine M05 Metric/Event. M13 separates facts from causal hypotheses and never blames an individual. Extend each `## Handoff`: M11 records authorized source/window/quality limits, consumed active IDs, action destinations and unresolved causal hypotheses; M13 records result Evidence refs, action/candidate-learning states, destination modules, withdrawal conditions and pending human decisions.

- [ ] **Step 5: Bind M12 to active hypotheses, measurements and an independent Test**

Immediately after the existing `## Evidence from A04/A11` section and before `## Hypothesis`, add:

```markdown
## Decision graph trace
| Outcome_ID | Opportunity_ID | Hypothesis_ID | Test_ID | Test_rev | Created_by_Module | Legal tests edge | Metric_ID/Event_ID | Active Decision refs | Evidence/result refs | Recommended decision | Test status | Superseded_by |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
```

Generate the trace only when there is a falsifiable active `Hypothesis_ID`, an applicable M05 measurement contract and enough baseline/variance/traffic/guardrail information to design an experiment. M12 creates a new Test ID with at least one `Test_ID -[tests]-> Hypothesis_ID`, defaults it to `proposed`, increments `Test_rev` for non-material clarification, creates a new ID plus `Superseded_by` after a material change, does not redefine Metric/Event, and keeps existing assignment, eligibility, exposure, MDE inputs, guardrails, SRM and pre-registered decision rule. If design inputs are incomplete, keep A12 draft. Add the exact line `Authorization conjunction: MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION.` Preserve the existing receipt rule: without a receipt, write `Not launched / no production verification`. Extend `## Handoff` with consumed active HYP/MET/EVT/DEC refs, produced Test ID/rev, evidence/result, recommended decision, authorization/receipt state, blockers and downstream M04/M11/M13 consumers.

- [ ] **Step 6: Normalize Task 5 and run pass oracles**

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md' \
  '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md' \
  '全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md' \
  '全栈开发Prompt Chain/prompts/12-增长与实验.md' \
  '全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md'
```

Run:

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task5
rg -Fq 'ALLOWED_FILES' '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md'
rg -Fq 'DEPENDENCY_CHANGES' '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md'
rg -Fq 'fixed review range' '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md'
rg -Fq 'No production access' '全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md'
rg -Fq 'Not launched / no production verification' '全栈开发Prompt Chain/prompts/12-增长与实验.md'
rg -Fq 'Not adopted / no persistent change' '全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md'
rg -Fq 'auto-adopt/auto-publish' '全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md'
print -r -- 'TASK5_BACK_HALF=PASS'
```

Expected exit `0`, `TASK5_STATIC=PASS`, and `TASK5_BACK_HALF=PASS`.

- [ ] **Step 7: Perform the safety, causality and ablation scoped advisory check**

Verify that M09 remains read-only, M11 production access remains a conjunction, M12 only recommends, and M13 does not turn action proposals into organizational commitments. Remove repeated authorization prose only if the existing exact condition remains visible. This checklist creates no PASS receipt; a finding requires a fresh Task 5 attempt.

---

### Task 6: Mirror M02–M05 into human-dialogue prompts

**Files:**

- Modify: `全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`

**Interfaces:**

- Consumes: final canonical M02–M05 semantics from Tasks 3–4.
- Produces: dialogue prompts with the same conditional Adapter contracts and A02–A05 structures.
- Must preserve: one question per turn, reason/recommendation/alternative/unknown protocol, completion summary, explicit generation confirmation, PLAN and Gate/R3 boundaries.

- [ ] **Step 1: Run the M02–M05 dialogue failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 6 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 6 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 6 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK6' || "$EVIDENCE_ID" == TASK6_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task6 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK6_STATIC=FAIL'* ]]
print -r -- 'TASK6_STATIC_RED=PASS'
```

Expected: nested exit `1`, at least one `FAIL`, and wrapper output `TASK6_STATIC_RED=PASS`. The nine missing headings are one in M02, two in M03, three in M04 and three in M05.

- [ ] **Step 2: Patch ask M02 at the canonical output anchor**

Immediately after ask M02's existing `## Current alternatives` section and before `## Opportunity evidence`, add:

```markdown
## Competitor transfer
仅在用户要求竞品、替代方案或市场比较时生成；决策影响只决定研究深度和下一问题，不是附加触发条件。

| Subject | Observable fact | Target context | Enabling constraints | Counterevidence | Transferable principle | Non-transferable context | Evidence refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Add this dialogue rule next to the existing one-question protocol: first decide whether the Adapter trigger is true; if false, omit the table. If true, ask only the single missing fact with highest decision impact. A02 supplies evidence to M03/M04 but cannot create `Opportunity_ID`, claim tested parity or approve a product. Add the exact sentence `Evidence_Ref fields: source, acquisition date, applicability, evidence level, limitation.` Mirror the canonical Handoff fields and the exact M02 `LINEAGE_LINES` value.

- [ ] **Step 3: Patch ask M03 with complete Opportunity and survey schemas**

Extend the existing `RESEARCH_MODE` enum with `survey-plan`. Immediately after the existing `## Evidence table` section and before `## Segments and excluded users`, add:

```markdown
## Evidence-to-opportunity map
| Opportunity_ID | Rev | Created_by_Module | Status | Observation | Evidence_Refs + supports/refutes edges | Current alternative | Cost and friction | Affected segment/context | Counterevidence | Evidence quality | Opportunity hypothesis | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Optional survey plan
仅当 `RESEARCH_MODE=survey-plan`，且已有假设需要更大样本、分群比较或定量补证据时生成。

| Research question | Question | Response type | Hypothesis ref | Decision affected | Sample frame | Bias review | Consent/distribution boundary | Response-quality check | Preregistered analysis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

M03 owns Opportunity semantics. Add these exact rules: `Every decision-stage Opportunity has at least one \`Evidence_Ref -[supports]-> Opportunity_ID\`.` `Counterevidence uses a separate \`Evidence_Ref -[refutes]-> Opportunity_ID\` and must not be placed in \`supports\`.` `Evidence_Ref and Opportunity_ID relations are many-to-many.` Every record has `Created_by_Module=M03`, starts `proposed`, increments `Rev` for non-material clarification, and creates a new ID plus `Superseded_by` for material semantic/scope change. The branch does not send, recruit or invent responses. Missing sample frame or consent/distribution boundary blocks only the survey branch and remains in `Open questions`. Mirror the canonical Handoff fields and the exact M03 `LINEAGE_LINES` value.

- [ ] **Step 4: Patch ask M04 with exact graph, Decision and product-risk contracts**

Add `A00_PATH` and `A01_PATH` to the exact startup inputs. Immediately after the existing `## Recommended choice` section and before `## MVP scope`, add the three canonical tables verbatim:

```markdown
## Product decision graph
| Entity ID | Rev | Type | Meaning | Legal edges | Evidence_Refs | Status | Created_by_Module | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |

| Decision_ID | Governs | Status | Authoritative_decision_ref | Decision_owner | Gate_or_authorization_ref | Decision_date | Expiry_or_invalidated_by | Evidence_Refs | Superseded_by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Product risk review
| Lens | Evidence | Unknown | Consequence | Cheapest reversible test |
| --- | --- | --- | --- | --- |
| Value | | | | |
| Usability | | | | |
| Feasibility | | | | |
| Viability | | | | |

## Prioritization sensitivity
仅在至少两个候选竞争同一范围或资源时生成。

| Candidate_ID | Outcome contribution | Evidence-backed cost/risk/reversibility | Assumption range | Recommended order | Objection | Rank-reversal condition |
| --- | --- | --- | --- | --- | --- | --- |
```

Allow only `contributes_to`, `addresses`, `applies_to` and `governs` as M04-local edges. Enforce the canonical minimum cardinalities and permit many-to-many relations. For OUT/CAN/HYP, non-material clarification increments `Rev`; material semantic/scope change creates a successor ID and sets `Superseded_by`. Copy the three exact `Decision authority:`, `Decision lifecycle:` and `Decision invalidation:` paragraphs from canonical M04 without paraphrase, including `\`superseded\` is terminal and cannot be restored or silently overwritten.` and `Downstream remains blocked until the same existing human decision owner or Gate creates a successor Decision or supersedes the old record and re-decides.` Add the exact sentence `M04 cannot create Metric/Event definitions; the existing Metric tree records measurement intent and desired outcome only.` Mirror canonical consumed/produced IDs, authoritative Decisions, explicit closures, blockers, consumers and the exact M04 `LINEAGE_LINES` value in `## Handoff`. The dialogue asks only the highest-impact missing fact and never asks one round per field.

- [ ] **Step 5: Patch ask M05 with exact conditional schemas**

Immediately after the existing `## UI context and visual acceptance` section and before `## Functional requirements`, add the following blocks in Journey, Measurement, Pre-build order, preserving `## Open questions` exactly once:

```markdown
## Journey backbone
仅当功能跨多个用户步骤、状态或失败路径时生成。

| Actor/context | Entry | Activity | Key task/state | Completion | Failure/recovery | Proposed first thin slice |
| --- | --- | --- | --- | --- | --- | --- |

## Measurement contract
仅当 Outcome、Opportunity、Hypothesis、acceptance 或 safety guardrail 需要行为/系统测量时生成。

| Entity_ID | Rev | Created_by_Module | Type | Purpose + measures edge | Semantic definition | Trigger + eligibility | Minimal properties | Identity + deduplication | Source of truth | Privacy/consent/retention/access | Quality check | Proposed owner | Status | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Pre-build review findings
仅对高影响、跨职能、高不可逆规格，或用户明确要求的预实现评审生成。

| Lens | Evidence location | Finding | Consequence | Severity | Proposed action | Decision owner | Re-review condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Add the exact sentence `M05 does not create \`Slice_ID\`; its proposed first thin slice remains specification and measurement intent.` For each Metric record at least one `Metric_ID -[measures]-> Outcome_ID | Opportunity_ID | Hypothesis_ID | safety_guardrail`; when event-derived, also record at least one `Metric_ID -[derived_from]-> Event_ID`; multiple targets/events are allowed. Each `Minimal properties` entry states name, type, enum/domain and requiredness; missing schema facts remain `Unknown`. Set `Created_by_Module=M05`, default `proposed`, increment `Rev` for non-material clarification, and create a successor with `Superseded_by` for a material semantic/scope change. Default-forbidden fields are direct identifiers, persistent device ID, free text, user content, full URL/query string and precise location. Keep G0 purpose/scope, G3 data/privacy/architecture decision, G4 implementation/`ALLOWED_FILES`, M11 production query R3 and external analytics/provider R3 as separate conjunctions. An unresolved executable quality query remains a `not executed` draft. Pre-build review uses fixed A04/A05/prototype versions, applicable standards, the canonical lens enum and `blocker | major | minor` severity; blocker returns to M04/M05. State that `0 blocker` is not a Gate. Mirror MET/EVT IDs/revs, blockers/findings, M06/M07/M09 consumers and the exact M05 `LINEAGE_LINES` value in `## Handoff`. Do not turn each property into a question; ask the one unresolved privacy/semantic fact that can change the affected contract, and block only that requirement.

- [ ] **Step 6: Normalize Task 6 and run the executable green oracle**

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md' \
  '全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md' \
  '全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md' \
  '全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md'
```

Run:

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task6
```

Expected exit `0` and `TASK6_STATIC=PASS`. This checks all nine headings, exact field tokens, eight public sections, one-question/unknown behavior and the four module-specific confirmation lines.

- [ ] **Step 7: Perform the dialogue and safety scoped advisory check**

Check that ask M03's previously anomalous 4096-byte state has a verified preimage and is now consistent; verify no interview/survey is sent and no Product/G2/G3 decision is inferred. This checklist creates no PASS receipt; a finding requires a fresh Task 6 attempt.

---

### Task 7: Mirror M06–M09 into human-dialogue prompts

**Files:**

- Modify: `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`

**Interfaces:**

- Consumes: canonical M06–M09 from Tasks 4–5.
- Produces: dialogue mirrors for Test, Slice, implementation trace and read-only closure.
- Must preserve: G0/consent, G4/sandbox, UI and ablation evidence, tracker preview, M08 file/dependency triple gate, M09 fixed-range read-only review and provider R3.

- [ ] **Step 1: Run the M06–M09 dialogue failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 7 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 7 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 7 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK7' || "$EVIDENCE_ID" == TASK7_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task7 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK7_STATIC=FAIL'* ]]
print -r -- 'TASK7_STATIC_RED=PASS'
```

Expected: nested exit `1`, at least one `FAIL`, and wrapper output `TASK7_STATIC_RED=PASS`.

- [ ] **Step 2: Patch ask M06 at `## Hypothesis and falsifiable prediction`**

Immediately after the existing `## Hypothesis and falsifiable prediction` section and before `## Prototype boundary`, add:

```markdown
## Decision graph trace
| Outcome_ID | Opportunity_ID | Candidate_ID | Hypothesis_ID | Test_ID | Test_rev | Created_by_Module | Legal edge | Learning question | Evidence_Refs | Result | Status | Superseded_by |
| --- | --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
```

Generate only when A04 has an active graph and a still-decision-changing `Priority: riskiest` Hypothesis. Ask M06 creates `Test_ID`, records at least one `Test_ID -[tests]-> Hypothesis_ID`, sets `Created_by_Module=M06` and default Status=`proposed`; non-material clarification increments `Test_rev`, while material Test change creates a new ID plus `Superseded_by`. Missing a safe test mode, target-user/fixture boundary, consent or write scope stops the Adapter. Result is learning evidence only, not approval or production implementation. Mirror consumed Hypothesis/Decision refs, Test ID/rev, result/evidence level, blocker and M04/M07 consumer in `## Handoff`.

- [ ] **Step 3: Patch ask M07 before `## Vertical-slice map`**

Before the existing `## Vertical-slice map`, add:

```markdown
## Product slice and measurement trace
| Slice_ID | Slice_rev | Created_by_Module | Legal realizes edge to Candidate_ID/A05 Spec | Hypothesis_ID/product risks | UI/API/data/observability path | Acceptance | Metric_ID/Event_ID instrumentation ticket | Verification seam | Status | Superseded_by |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Conditional delivery outline
仅在多个 initiative、共享依赖或资源冲突时生成。

| Milestone/outcome | Slice_ID | Dependencies | Capacity assumption | Uncertainty/buffer basis | Critical path | Success signal | Change trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Add these exact rules: `M07 may create a Slice only when the referenced Candidate_ID or A05 Spec is current and has an applicable existing approval.` `Otherwise omit the Product slice table, retain the known Candidate_ID or A05 Spec as a blocker, and do not infer approval.` `Every emitted Slice has at least one \`Slice_ID -[realizes]-> Candidate_ID or A05 Spec\` edge to that approved input.` One Candidate may have multiple Slices; set `Created_by_Module=M07` and default Status to `proposed`; increment `Slice_rev` for non-material clarification and use a successor plus `Superseded_by` for material change. Add the exact sentence `Metric/Event semantic/property changes return to M05; M07 only creates an instrumentation ticket.` With insufficient dependency/capacity facts, output named scenarios without dates. It is neither G4 nor tracker write. Mirror consumed refs, produced Slice ID/rev, instrumentation tickets, blockers, G4/M08 consumers and the exact M07 `LINEAGE_LINES` value in `## Handoff`.

Keep one-question behavior. Do not ask a new round merely to fill an optional Roadmap or graph field.

- [ ] **Step 4: Patch ask M08 after `## Ticket and acceptance`**

Immediately after the existing `## Ticket and acceptance` section and before `## Preflight`, add:

```markdown
## Product trace implemented
仅在 A07 提供对应 ID 时生成。

| Slice_ID | Active Decision/G3/G4 refs | Metric_ID/Event_ID | Implementation location | Tests/verification | Semantic drift or new field |
| --- | --- | --- | --- | --- | --- |
```

Missing active ref, semantic change or a new collection field is a blocker and returns to M05/M07. The dialogue remains default PLAN even though canonical M08 can APPLY after all existing gates; a ticket never implies product approval. Mirror consumed Slice/Decision/G3/G4/MET/EVT refs, implementation/test evidence, drift/unverified items and the M09 consumer in `## Handoff`.

- [ ] **Step 5: Patch ask M09 after `## Ablation evidence review`**

Immediately after the existing `## Ablation evidence review` section and before `## Security review`, add:

```markdown
## Product risk and measurement review
仅当 fixed review range 含适用的 A04 产品风险、A05 Metric/Event 契约或 pre-build finding 时生成。

| ID/ref | Expected contract or risk | A07/A08/fixed-diff evidence | Finding | Severity | Closure evidence or Unverified scope |
| --- | --- | --- | --- | --- | --- |
```

No evidence yields a finding or `Unverified scope`. A blocker returns to its owning M04/M05/M07/M08 module without automatic repair. No finding does not mean product approval, valid production telemetry or release approval. `Do not query production`; do not modify code. Mirror the fixed range, consumed refs, findings/unverified scope, blockers and M10/G5 consumers in `## Handoff`.

- [ ] **Step 6: Normalize Task 7 and run the executable green oracle**

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md' \
  '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md' \
  '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md' \
  '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md'
```

Run:

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task7
rg -Fq 'G4_APPROVAL' '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md'
rg -Fq 'ALLOWED_FILES_OR_SANDBOX' '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md'
rg -Fq 'remove | defer | retain' '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md'
rg -Fq 'tracker-preview' '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md'
rg -Fq 'DEPENDENCY_CHANGES' '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md'
rg -Fq 'Visual verification: not run' '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md'
rg -Fq 'fixed review range' '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md'
rg -Fq -- '--no-share' '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md'
rg -Fq 'R3_ACTION_AUTHORIZATION' '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md'
print -r -- 'TASK7_DIALOGUE_BUILD=PASS pairs=4'
```

Expected exit `0`, `TASK7_STATIC=PASS`, and `TASK7_DIALOGUE_BUILD=PASS pairs=4`.

- [ ] **Step 7: Perform the dialogue, UI, safety and ablation scoped advisory check**

Verify that the added graph text does not duplicate or weaken existing UI/ablation evidence and does not create a new approval path. This checklist creates no PASS receipt; a finding requires a fresh Task 7 attempt.

---

### Task 8: Mirror M11–M13 into human-dialogue prompts

**Files:**

- Modify: `全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/12-增长与实验.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md`

**Interfaces:**

- Consumes: canonical M11–M13 from Task 5.
- Produces: dialogue action registers and experiment decision trace.
- Must preserve: single-question/generation-confirmation protocol, M11 systematic-debugging and G0+R3, M12 pre-registration and four-way launch condition, M13 mock/dry-run and adoption/publish separation.

- [ ] **Step 1: Run the M11–M13 dialogue failure oracle**

```zsh
set -euo pipefail
: "${EVIDENCE_ID:?set Task 8 evidence ID from the task-attempt context}" "${SCOPE_SELECTOR:?set Task 8 selector}" "${PREVIOUS_SCOPE_TSV:?set Task 8 predecessor scope}"
[[ "$EVIDENCE_ID" == 'TASK8' || "$EVIDENCE_ID" == TASK8_R<-> ]]
/bin/zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/guard-workspace.zsh \
  "$EVIDENCE_ID" "$SCOPE_SELECTOR" "$PREVIOUS_SCOPE_TSV"
set +e
output=$(/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task8 2>&1)
verifier_exit=$?
set -e
print -r -- "$output"
test "$verifier_exit" -eq 1
[[ "$output" == *'FAIL '* && "$output" == *'TASK8_STATIC=FAIL'* ]]
print -r -- 'TASK8_STATIC_RED=PASS'
```

Expected: nested exit `1`, at least one `FAIL`, and wrapper output `TASK8_STATIC_RED=PASS`.

- [ ] **Step 2: Patch ask M11 after `## Recommended actions`**

Immediately after the existing `## Recommended actions` section and before `## External mutations not performed`, add:

```markdown
## Action register
仅当获准生产证据、用户反馈或 incident 事实支持至少一项 finding/action 时生成；无生产授权时只能使用已提供材料。

| Finding_or_Evidence_ID | Observation | Causal hypothesis | Counterevidence/alternative | Proposed action | Proposed owner | Due/trigger | Verification | Destination module | Status | Status evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

The Destination module is one of M03/M04/M05/M12/M13. Add the exact line `Status enum: proposed | accepted | in_progress | verified | rejected | superseded; default=proposed.` Any non-proposed status needs confirmer, time and `Evidence_Ref`. The table neither creates tracker items nor proves execution. Mirror authorized source/window/quality limits, consumed active IDs, action destinations and unresolved causal hypotheses in `## Handoff`.

- [ ] **Step 3: Patch ask M13 after `## Candidate learnings`**

Immediately after the existing `## Candidate learnings` section and before `## Proposed evolution target`, add:

```markdown
## Action register
仅当 task、release、experiment 或 incident 存在可复核结果且至少有一项行动候选时生成。

| Finding_or_Evidence_ID | Observation | Causal hypothesis | Counterevidence/alternative | Proposed action | Proposed owner | Due/trigger | Verification | Destination module | Status | Status evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Add the same exact Status-enum line from Step 2. Tie entries to retrospective Evidence and keep action, candidate learning, local adoption and external publish as four separate states. Do not blame individuals or create an organizational commitment. Mirror result Evidence refs, action/candidate-learning states, destination modules, withdrawal conditions and pending human decisions in `## Handoff`.

- [ ] **Step 4: Patch ask M12 after `## Evidence from A04/A11`**

Immediately after the existing `## Evidence from A04/A11` section and before `## Hypothesis`, add:

```markdown
## Decision graph trace
仅当存在可证伪且 active 的 Hypothesis、适用的 M05 measurement contract，且 baseline/variance/traffic/guardrail 输入足以设计实验时生成。

| Outcome_ID | Opportunity_ID | Hypothesis_ID | Test_ID | Test_rev | Created_by_Module | Legal tests edge | Metric_ID/Event_ID | Active Decision refs | Evidence/result refs | Recommended decision | Test status | Superseded_by |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
```

Ask M12 creates a separate `Test_ID`, records at least one `Test_ID -[tests]-> Hypothesis_ID`, sets `Created_by_Module=M12` and default `proposed`, increments `Test_rev` for non-material clarification, and uses a successor plus `Superseded_by` after material change. It consumes active Hypothesis and M05-owned Metric/Event without redefining them. Add the exact line `Authorization conjunction: MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION.` Incomplete design remains draft; no receipt means `Not launched / no production verification`. Mirror consumed HYP/MET/EVT/DEC refs, produced Test ID/rev, result, recommended decision, authorization/receipt state, blockers and M04/M11/M13 consumers in `## Handoff`.

- [ ] **Step 5: Normalize Task 8 and run the executable green oracle**

```zsh
zsh /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/capture-and-normalize.zsh "$EVIDENCE_ID" \
  '全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md' \
  '全栈开发Prompt Chain/prompts_ask/12-增长与实验.md' \
  '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md'
```

Run:

```zsh
set -euo pipefail
/usr/bin/ruby /private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/verify-chain.rb task8
rg -Fq 'No production access' '全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md'
rg -Fq 'Not launched / no production verification' '全栈开发Prompt Chain/prompts_ask/12-增长与实验.md'
rg -Fq 'Not adopted / no persistent change' '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md'
rg -Fq 'mock/dry-run' '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md'
for relative in \
  '全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md' \
  '全栈开发Prompt Chain/prompts_ask/12-增长与实验.md' \
  '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md'; do
  rg -Fq 'R3_ACTION_AUTHORIZATION' "$relative"
done
print -r -- 'TASK8_DIALOGUE_LEARN=PASS pairs=3'
```

Expected exit `0`, `TASK8_STATIC=PASS`, and `TASK8_DIALOGUE_LEARN=PASS pairs=3`.

- [ ] **Step 6: Perform the causality, safety and dialogue scoped advisory check**

Verify that related signals remain hypotheses, experiment output remains a recommendation, and Action status never proves execution. This checklist creates no PASS receipt; a finding requires a fresh Task 8 attempt.

---

### Task 9: Run full integrity, ablation and independent final reviews

**Files:**

- Read: all 32 allowlisted paths, 44 protected files, the ZIP, Task 0 preimage and Tasks 1–8 sealed evidence.
- Create outside workspace only: one generation at `snapshot/task9/run-NNN/`.
- Do not create or edit review/evidence files inside the workspace.

**Interfaces:**

- Consumes: the latest actual Task 8 or rework `scope32-after.tsv`, after its wrapper and green oracle passed.
- Produces: one frozen target/preimage/protected/ZIP evidence set; deterministic changed-line universe; exact ablation ledger; canonical review-input manifest; three independent reports; and one exclusive terminal state.
- Must preserve: the Task 9 input content. Any content fix invalidates the entire generation, returns to the owning Task under a fresh `TASKn_Rk`, and starts the next monotonic run. Evidence-only failure also invalidates the generation; it never edits a published artifact in place.

Task 9 has no mutable status file. A generation moves forward only by creating a new phase artifact. Exactly one `TERMINAL.tsv` is published with `State=COMPLETED` or `State=INVALIDATED`; the two states cannot coexist because they use the same exclusive path. A terminated generation is recursively non-writable and is never resumed. `run-001` is valid only when no run exists; each later ID is exactly the previous number plus one, the prior terminal is `INVALIDATED`, and no prior terminal is `COMPLETED`.

An allocated generation normally has no terminal while its next declared phase is intentionally running. After any phase command exits non-zero, is interrupted, or crashes, no later phase may start until that generation has an `INVALIDATED` terminal. First confirm all Task 9 writers are stopped and preserve the original error output. Known phase handlers below may emit `REWORK_CONTENT` only from a machine-validated owner and Candidate ID. For every otherwise unhandled failure, the recovery block below independently re-samples scope, protected files and the ZIP twice: it emits `REBUILD_EVIDENCE` only when both samples and the frozen input/baselines are byte-identical; every missing, malformed or drifting proof deterministically emits `STOP`. Recovery never deletes, repairs or resumes the failed generation:

```zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}"
[[ "$TASK9_RUN_ID" == run-[0-9][0-9][0-9] ]]
[[ "${TASK9_QUIESCENCE_CONFIRMED:-no}" == yes ]]
workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
manifest="$snapshot_root/four-value-manifest.rb"
plan="$workspace_root/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"
baseline="$snapshot_root/baseline"
[[ -d "$run_root" && ! -L "$run_root" ]]
if [[ -e "$run_root/TERMINAL.tsv" || -L "$run_root/TERMINAL.tsv" ]]; then
  /usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" --finalize-existing "$TASK9_RUN_ID"
  exit 0
fi
[[ -f "$run_root/00-meta/run-meta.tsv" && -f "$run_root/10-input/input-scope.tsv" && -f "$run_root/10-input/input-scope.bin" ]]
[[ -d "$run_root/70-recovery" && ! -L "$run_root/70-recovery" ]]
recovery_root=$(/usr/bin/mktemp -d "$run_root/70-recovery/recovery.XXXXXX")

/usr/bin/ruby - "$snapshot_root" <<'RUBY'
require 'digest'
root = ARGV.fetch(0)
expected = %w[
  capture-and-normalize.zsh four-value-manifest.rb guard-workspace.zsh
  normalize-targets.zsh rollback-target.zsh seal-task9-generation.rb verify-chain.rb
]
lines = File.readlines(File.join(root, 'helper-manifest.tsv'), chomp: true)
raise 'helper manifest header drift' unless lines.shift == "Schema\tName\tBytes\tSHA256\tMode"
rows = lines.map { |line| line.split("\t", -1) }
raise 'helper manifest set/order drift' unless rows.map { |row| row[1] } == expected
rows.each do |schema, name, bytes, hash, mode|
  path = File.join(root, name)
  stat = File.lstat(path)
  body = File.binread(path)
  raise "helper drift: #{name}" unless schema == 'task0-helper-manifest/v1' && stat.file? && !stat.symlink? &&
    (stat.mode & 0o777).to_s(8) == mode && body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == hash
end
RUBY

set +e
/usr/bin/ruby "$manifest" plan-set "$workspace_root" "$plan" scope32 \
  "$recovery_root/scope-a.bin" "$recovery_root/scope-a.tsv" >"$recovery_root/scope-a.out" 2>&1
scope_a_exit=$?
/usr/bin/ruby "$manifest" protected "$workspace_root" "$plan" '全栈开发Prompt Chain' \
  "$recovery_root/protected-a.bin" "$recovery_root/protected-a.tsv" >"$recovery_root/protected-a.out" 2>&1
protected_a_exit=$?
/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" 1 '全栈开发Prompt Chain.zip' \
  "$recovery_root/zip-a.bin" "$recovery_root/zip-a.tsv" >"$recovery_root/zip-a.out" 2>&1
zip_a_exit=$?
/usr/bin/ruby "$manifest" plan-set "$workspace_root" "$plan" scope32 \
  "$recovery_root/scope-b.bin" "$recovery_root/scope-b.tsv" >"$recovery_root/scope-b.out" 2>&1
scope_b_exit=$?
/usr/bin/ruby "$manifest" protected "$workspace_root" "$plan" '全栈开发Prompt Chain' \
  "$recovery_root/protected-b.bin" "$recovery_root/protected-b.tsv" >"$recovery_root/protected-b.out" 2>&1
protected_b_exit=$?
/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" 1 '全栈开发Prompt Chain.zip' \
  "$recovery_root/zip-b.bin" "$recovery_root/zip-b.tsv" >"$recovery_root/zip-b.out" 2>&1
zip_b_exit=$?
set -e

scope_stable=no
protected_stable=no
zip_stable=no
if (( scope_a_exit == 0 && scope_b_exit == 0 )) &&
   /usr/bin/cmp -s "$run_root/10-input/input-scope.bin" "$recovery_root/scope-a.bin" &&
   /usr/bin/cmp -s "$run_root/10-input/input-scope.tsv" "$recovery_root/scope-a.tsv" &&
   /usr/bin/cmp -s "$recovery_root/scope-a.bin" "$recovery_root/scope-b.bin" &&
   /usr/bin/cmp -s "$recovery_root/scope-a.tsv" "$recovery_root/scope-b.tsv"; then
  scope_stable=yes
fi
if (( protected_a_exit == 0 && protected_b_exit == 0 )) &&
   /usr/bin/cmp -s "$baseline/protected-44-before.bin" "$recovery_root/protected-a.bin" &&
   /usr/bin/cmp -s "$baseline/protected-44-before.tsv" "$recovery_root/protected-a.tsv" &&
   /usr/bin/cmp -s "$recovery_root/protected-a.bin" "$recovery_root/protected-b.bin" &&
   /usr/bin/cmp -s "$recovery_root/protected-a.tsv" "$recovery_root/protected-b.tsv"; then
  protected_stable=yes
fi
if (( zip_a_exit == 0 && zip_b_exit == 0 )) &&
   /usr/bin/cmp -s "$baseline/zip-before.bin" "$recovery_root/zip-a.bin" &&
   /usr/bin/cmp -s "$baseline/zip-before.tsv" "$recovery_root/zip-a.tsv" &&
   /usr/bin/cmp -s "$recovery_root/zip-a.bin" "$recovery_root/zip-b.bin" &&
   /usr/bin/cmp -s "$recovery_root/zip-a.tsv" "$recovery_root/zip-b.tsv"; then
  zip_stable=yes
fi

if [[ "$scope_stable" == yes && "$protected_stable" == yes && "$zip_stable" == yes ]]; then
  recovery_action=REBUILD_EVIDENCE
  recovery_reason=UNHANDLED_PHASE_FAILURE
else
  recovery_action=STOP
  recovery_reason=RECOVERY_PROOF_FAILED
fi
RECOVERY_SCOPE="$scope_stable" RECOVERY_PROTECTED="$protected_stable" RECOVERY_ZIP="$zip_stable" \
RECOVERY_FIRST_EXITS="$scope_a_exit,$protected_a_exit,$zip_a_exit" \
RECOVERY_SECOND_EXITS="$scope_b_exit,$protected_b_exit,$zip_b_exit" \
RECOVERY_ACTION="$recovery_action" /usr/bin/ruby - "$recovery_root/recovery-verdict.tsv" "$TASK9_RUN_ID" <<'RUBY'
path, run_id = ARGV
header = %w[Schema Run_ID Quiescence_Confirmed First_Pass_Exits Second_Pass_Exits Scope_Stable Protected_Stable Zip_Stable Required_Action]
values = [
  'task9-recovery-verdict/v1', run_id, 'yes', ENV.fetch('RECOVERY_FIRST_EXITS'), ENV.fetch('RECOVERY_SECOND_EXITS'),
  ENV.fetch('RECOVERY_SCOPE'), ENV.fetch('RECOVERY_PROTECTED'), ENV.fetch('RECOVERY_ZIP'), ENV.fetch('RECOVERY_ACTION')
]
File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
  file.write(header.join("\t") + "\n" + values.join("\t") + "\n")
  file.flush
  file.fsync
end
RUBY
/usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" "$TASK9_RUN_ID" INVALIDATED "$recovery_reason" "$recovery_action" NONE NONE "$recovery_root/recovery-verdict.tsv" NONE NONE NONE NONE
```

The coordinator must not override the recovery verdict merely to keep execution moving. A `STOP` terminal deliberately forbids another generation until a revised, separately reviewed plan defines a safe continuation. If allocation fails before the atomic publish, the staging directory is preserved outside `task9/` and no run ID was allocated; inspect it and rerun only after quiescence. If recovery or sealing itself fails, preserve every artifact and stop for a revised plan rather than fabricating a terminal.

Set both execution inputs explicitly for every Task 9 command:

```text
TASK9_RUN_ID is the next unused monotonic run-NNN ID.
PREVIOUS_SCOPE_TSV is the absolute latest sealed scope32 manifest produced by Task 8 or a Task n rework; for a pure Task 9 evidence rebuild it is the immediately preceding invalidated generation's sealed input-scope TSV.
```

For the first no-rework pass, use `TASK9_RUN_ID=run-001` and set `PREVIOUS_SCOPE_TSV` to the highest contiguous, complete Task 8 attempt (`TASK8`, then `TASK8_R2`, `TASK8_R3`, …). The allocator independently derives that chain head from all 16 sealed guard/wrapper artifacts and requires the supplied path to equal it; it never falls back to an older attempt. It then reruns the full green oracle, so a wrapper-complete but semantically red attempt invalidates the generation. Choosing a later run ID never authorizes content rework. If a generation requests `REWORK_CONTENT`, the rework Task's guard consumes that generation's sealed `10-input/guard-scope.tsv`; after rework, the next Task 9 run consumes the fresh reserved `TASKn_Rk-scope32-after.tsv`. If the generation requests `REBUILD_EVIDENCE`, the next run consumes the preceding generation's always-present sealed `10-input/input-scope.tsv`; content must remain identical.

- [ ] **Step 1: Atomically allocate the run, bind its predecessor, guard the workspace and run the full static oracle**

Run from `/Users/lute/Project/vibecoding_config`. The allocation command validates every earlier terminal and generation seal before it creates the current directory:

```zsh
set -euo pipefail
: "${TASK9_RUN_ID:?set the next monotonic Task 9 run ID}" "${PREVIOUS_SCOPE_TSV:?set the latest sealed scope32 manifest}"
workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_id="$TASK9_RUN_ID"
previous_scope_tsv=${PREVIOUS_SCOPE_TSV:A}
[[ "$run_id" == run-[0-9][0-9][0-9] ]]

/usr/bin/ruby - "$snapshot_root" "$run_id" "$previous_scope_tsv" <<'RUBY'
require 'digest'
require 'fiddle/import'
require 'fileutils'
require 'find'
require 'open3'
require 'tmpdir'

module Task9LibC
  extend Fiddle::Importer
  dlload Fiddle.dlopen(nil)
  extern 'int renamex_np(const char *, const char *, unsigned int)'
end

RENAME_EXCL = 0x00000004

verify_helpers = lambda do |root|
  expected = %w[
    capture-and-normalize.zsh four-value-manifest.rb guard-workspace.zsh
    normalize-targets.zsh rollback-target.zsh seal-task9-generation.rb verify-chain.rb
  ]
  manifest_path = File.join(root, 'helper-manifest.tsv')
  stat = File.lstat(manifest_path)
  raise 'unsafe helper manifest' unless stat.file? && !stat.symlink? && (stat.mode & 0o777) == 0o400
  lines = File.readlines(manifest_path, chomp: true)
  raise 'helper manifest header drift' unless lines.shift == "Schema\tName\tBytes\tSHA256\tMode"
  rows = lines.map { |line| line.split("\t", -1) }
  raise 'helper manifest set/order drift' unless rows.map { |row| row[1] } == expected
  rows.each do |schema, name, bytes, hash, mode|
    path = File.join(root, name)
    helper = File.lstat(path)
    body = File.binread(path)
    raise "helper drift: #{name}" unless schema == 'task0-helper-manifest/v1' && helper.file? && !helper.symlink? &&
      (helper.mode & 0o777).to_s(8) == mode && body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == hash
  end
end

snapshot, run_id, source_tsv = ARGV
verify_helpers.call(snapshot)
raise 'invalid run ID' unless run_id.match?(/\Arun-(\d{3})\z/)
run_number = Integer(Regexp.last_match(1), 10)
raise 'run number must be positive' unless run_number.positive?
task9_root = File.join(snapshot, 'task9')
task9_staging_root = File.join(snapshot, 'task9-staging')

[task9_root, task9_staging_root].each do |root|
  begin
    Dir.mkdir(root, 0o700)
  rescue Errno::EEXIST
    # A concurrent allocator may have created the shared parent.
  end
  raise "invalid allocation parent: #{root}" unless File.directory?(root) && !File.symlink?(root)
end
runs = Dir.children(task9_root).sort
raise "invalid run directory name: #{runs.inspect}" unless runs.all? { |name| name.match?(/\Arun-\d{3}\z/) }
expected_existing = (1...run_number).map { |number| format('run-%03d', number) }
raise "non-monotonic run allocation: existing=#{runs.inspect} expected=#{expected_existing.inspect}" unless runs == expected_existing

prior_terminals = {}
verify_sealed_run = lambda do |prior_id|
  prior_root = File.join(task9_root, prior_id)
  prior_root_stat = File.lstat(prior_root)
  raise "unsafe prior run root: #{prior_id}" unless prior_root_stat.directory? && !prior_root_stat.symlink? && (prior_root_stat.mode & 0o222).zero?
  terminal_path = File.join(prior_root, 'TERMINAL.tsv')
  intent_path = File.join(prior_root, 'terminal-intent.tsv')
  seal_path = File.join(prior_root, 'generation-seal.tsv')
  raise "missing prior terminal: #{prior_id}" unless File.file?(terminal_path) && !File.symlink?(terminal_path)
  raise "missing prior terminal intent: #{prior_id}" unless File.file?(intent_path) && !File.symlink?(intent_path)
  raise "missing prior seal: #{prior_id}" unless File.file?(seal_path) && !File.symlink?(seal_path)
  [terminal_path, intent_path, seal_path].each { |path| raise "writable prior control file: #{path}" unless (File.lstat(path).mode & 0o222).zero? }
  raise "prior terminal intent drift: #{prior_id}" unless File.binread(intent_path) == File.binread(terminal_path)
  terminal_lines = File.readlines(terminal_path, chomp: true)
  header = terminal_lines.shift&.split("\t", -1)
expected_header = %w[Schema Run_ID State Reason_Code Required_Action Owning_Task Candidate_ID Next_Evidence_ID Rework_Reservation_Path Rework_Reservation_SHA256 Artifact_Path Input_Scope_TSV Input_Scope_SHA256 Review_Input_SHA256 Target_Manifest_SHA256 Candidate_Universe_SHA256 Ablation_Ledger_SHA256 Generation_Seal_SHA256]
  raise "terminal header drift: #{prior_id}" unless header == expected_header && terminal_lines.length == 1
  terminal_fields = terminal_lines.first.split("\t", -1)
  raise "terminal field count drift: #{prior_id}" unless terminal_fields.length == header.length
  row = Hash[header.zip(terminal_fields)]
  raise "terminal run drift: #{prior_id}" unless row['Schema'] == 'task9-terminal/v1' && row['Run_ID'] == prior_id
  raise "completed run forbids successor: #{prior_id}" if row['State'] == 'COMPLETED'
  raise "invalid prior state: #{prior_id}" unless row['State'] == 'INVALIDATED'
  if row['Required_Action'] == 'REWORK_CONTENT'
    expected_reservation = File.join(snapshot, 'task9-rework-reservations', "#{prior_id}.tsv")
    raise "prior rework reservation path drift: #{prior_id}" unless row['Rework_Reservation_Path'] == expected_reservation
    raise "unsafe prior rework reservation: #{prior_id}" unless File.file?(expected_reservation) && !File.symlink?(expected_reservation) && (File.lstat(expected_reservation).mode & 0o777) == 0o400
    reservation_bytes = File.binread(expected_reservation)
    raise "prior rework reservation hash drift: #{prior_id}" unless Digest::SHA256.hexdigest(reservation_bytes) == row['Rework_Reservation_SHA256']
    expected_bytes = "Schema\tOwner\tEvidence_ID\tSource_Run\tCandidate_ID\n" +      "task9-rework-reservation/v1\t#{row['Owning_Task']}\t#{row['Next_Evidence_ID']}\t#{prior_id}\t#{row['Candidate_ID']}\n"
    raise "prior rework reservation content drift: #{prior_id}" unless reservation_bytes == expected_bytes
  else
    raise "unexpected prior rework reservation: #{prior_id}" unless row['Next_Evidence_ID'] == 'NONE' && row['Rework_Reservation_Path'] == 'NONE' && row['Rework_Reservation_SHA256'] == 'NONE'
  end
  seal_bytes = File.binread(seal_path)
  raise "prior seal hash drift: #{prior_id}" unless Digest::SHA256.hexdigest(seal_bytes) == row['Generation_Seal_SHA256']
  seal_lines = seal_bytes.lines(chomp: true)
  raise "prior seal header drift: #{prior_id}" unless seal_lines.shift == "Relative_Path\tBytes\tSHA256"
  sealed_relatives = []
  seal_lines.each do |line|
    relative, bytes, sha = line.split("\t", -1)
    raise "prior seal row drift: #{prior_id}" unless line.split("\t", -1).length == 3 && relative && bytes&.match?(/\A\d+\z/) && sha&.match?(/\A[0-9a-f]{64}\z/)
    raise "unsafe prior seal path: #{relative}" if relative.empty? || relative.start_with?('/') || relative.split(File::SEPARATOR).include?('..')
    sealed_relatives << relative
    absolute = File.join(prior_root, relative)
    raise "prior sealed input missing: #{absolute}" unless File.file?(absolute) && !File.symlink?(absolute)
    body = File.binread(absolute)
    raise "prior sealed byte drift: #{absolute}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
  end
  raise "duplicate prior seal path: #{prior_id}" unless sealed_relatives.uniq.length == sealed_relatives.length
  actual_relatives = []
  Find.find(prior_root) do |path|
    next if path == prior_root
    stat = File.lstat(path)
    raise "symlink in prior generation: #{path}" if stat.symlink?
    raise "writable path in prior generation: #{path}" unless (stat.mode & 0o222).zero?
    next if stat.directory?
    raise "special file in prior generation: #{path}" unless stat.file?
    relative = path.delete_prefix(prior_root + File::SEPARATOR)
    next if %w[TERMINAL.tsv terminal-intent.tsv generation-seal.tsv].include?(relative)
    actual_relatives << relative
  end
  raise "prior seal file-set drift: #{prior_id}" unless actual_relatives.sort_by(&:b) == sealed_relatives.sort_by(&:b)
  prior_terminals[prior_id] = row
end
runs.each { |prior_id| verify_sealed_run.call(prior_id) }

source_tsv = File.expand_path(source_tsv)
source_bin = source_tsv.sub(/\.tsv\z/, '.bin')
manifests_prefix = File.join(snapshot, 'manifests') + File::SEPARATOR
verify_task_evidence = lambda do |evidence_id|
  suffixes = %w[
    before-scope before-protected before-zip post-apply-patch normalized
    scope32-after protected-after zip-after
  ]
  suffixes.product(%w[bin tsv]).each do |suffix, extension|
    path = File.join(snapshot, 'manifests', "#{evidence_id}-#{suffix}.#{extension}")
    raise "incomplete task handoff: #{path}" unless File.file?(path) && !File.symlink?(path) && !File.writable?(path)
  end
end
if run_number == 1
  task8_attempts = Dir.children(File.join(snapshot, 'manifests')).map do |name|
    match = name.match(/\A(TASK8(?:_R(\d+))?)-scope32-after\.tsv\z/)
    next unless match
    number = match[2] ? Integer(match[2], 10) : 1
    raise "invalid Task 8 rework ordinal: #{name}" if number < 2 && match[2]
    [number, match[1]]
  end.compact.sort_by(&:first)
  raise 'missing Task 8 handoff' if task8_attempts.empty?
  raise 'Task 8 handoff ordinal gap/duplicate' unless task8_attempts.map(&:first) == (1..task8_attempts.last[0]).to_a
  latest_id = task8_attempts.last[1]
  verify_task_evidence.call(latest_id)
  expected_source = File.join(snapshot, 'manifests', "#{latest_id}-scope32-after.tsv")
  raise 'run-001 must consume the mechanically latest complete Task 8 handoff' unless source_tsv == expected_source
else
  previous_id = format('run-%03d', run_number - 1)
  previous = prior_terminals.fetch(previous_id)
  case previous.fetch('Required_Action')
  when 'REBUILD_EVIDENCE'
    expected_source = File.join(task9_root, previous_id, '10-input', 'input-scope.tsv')
    raise 'evidence rebuild must reuse the preceding sealed input scope' unless source_tsv == expected_source
  when 'REWORK_CONTENT'
    expected_name = "#{previous.fetch('Next_Evidence_ID')}-scope32-after.tsv"
    raise 'content rework must consume the reserved rework scope32-after manifest' unless source_tsv.start_with?(manifests_prefix) && File.basename(source_tsv) == expected_name
    verify_task_evidence.call(previous.fetch('Next_Evidence_ID'))
  else
    raise "prior action forbids successor: #{previous.fetch('Required_Action')}"
  end
end
[source_tsv, source_bin].each do |path|
  raise "invalid source scope member: #{path}" unless File.file?(path) && !File.symlink?(path) && !File.writable?(path)
end

destination_run_root = File.join(task9_root, run_id)
raise 'run destination already exists' if File.exist?(destination_run_root) || File.symlink?(destination_run_root)
run_root = Dir.mktmpdir(".#{run_id}-", task9_staging_root)
raise 'staging directory crossed filesystem' unless File.stat(run_root).dev == File.stat(task9_root).dev
%w[00-meta 10-input 20-final 30-ablation 40-review-input 50-reviews 60-closeout 70-recovery].each do |name|
  Dir.mkdir(File.join(run_root, name), 0o700)
end

copy_exclusive = lambda do |source, destination|
  before = File.lstat(source)
  raise "unsafe source scope member: #{source}" unless before.file? && !before.symlink? && (before.mode & 0o222).zero?
  flags = File::RDONLY
  flags |= File::NOFOLLOW if File.const_defined?(:NOFOLLOW)
  bytes = File.open(source, flags) do |file|
    opened = file.stat
    raise "source scope inode drift: #{source}" unless [before.dev, before.ino] == [opened.dev, opened.ino]
    body = file.read.b
    after = File.lstat(source)
    raise "source scope pathname replaced: #{source}" unless [opened.dev, opened.ino] == [after.dev, after.ino]
    body
  end
  File.open(destination, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
    file.write(bytes)
    file.flush
    file.fsync
  end
  bytes
end
input_tsv = File.join(run_root, '10-input', 'input-scope.tsv')
input_bin = File.join(run_root, '10-input', 'input-scope.bin')
source_tsv_bytes = copy_exclusive.call(source_tsv, input_tsv)
source_bin_bytes = copy_exclusive.call(source_bin, input_bin)
raise 'source/frozen TSV mismatch' unless source_tsv_bytes == File.binread(input_tsv)
raise 'source/frozen BIN mismatch' unless source_bin_bytes == File.binread(input_bin)

cat_sha = lambda do |path|
  stdout, stderr, result = Open3.capture3('/bin/cat', path)
  raise "cat failed: #{path}: #{stderr}" unless result.success?
  Digest::SHA256.hexdigest(stdout.b)
end
workspace = '/Users/lute/Project/vibecoding_config'
plan_path = File.join(workspace, '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md')
design_path = File.join(workspace, '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md')
previous_terminal = run_number == 1 ? 'NONE' : File.join(task9_root, format('run-%03d', run_number - 1), 'TERMINAL.tsv')
previous_terminal_sha = previous_terminal == 'NONE' ? 'NONE' : Digest::SHA256.file(previous_terminal).hexdigest
source_task = run_number == 1 ? File.basename(source_tsv).split('-', 2).first : (source_tsv.start_with?(manifests_prefix) ? File.basename(source_tsv).split('-', 2).first : format('TASK9_RUN_%03d', run_number - 1))
meta_header = %w[Schema Run_ID Guard_ID Previous_Run Previous_Terminal_SHA256 Source_Task_ID Source_Scope_TSV Source_Scope_TSV_SHA256 Source_Scope_BIN_SHA256 Frozen_Input_TSV_SHA256 Frozen_Input_BIN_SHA256 Plan_CAT_SHA256 Design_CAT_SHA256]
meta_values = [
  'task9-run/v1', run_id, "TASK9_RUN_#{format('%03d', run_number)}",
  run_number == 1 ? 'NONE' : format('run-%03d', run_number - 1), previous_terminal_sha,
  source_task, source_tsv, Digest::SHA256.hexdigest(source_tsv_bytes), Digest::SHA256.hexdigest(source_bin_bytes),
  Digest::SHA256.hexdigest(source_tsv_bytes), Digest::SHA256.hexdigest(source_bin_bytes),
  cat_sha.call(plan_path), cat_sha.call(design_path)
]
meta = meta_header.join("\t") + "\n" + meta_values.join("\t") + "\n"
meta_path = File.join(run_root, '00-meta', 'run-meta.tsv')
File.open(meta_path, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
  file.write(meta)
  file.flush
  file.fsync
end
%w[00-meta 10-input 20-final 30-ablation 40-review-input 50-reviews 60-closeout 70-recovery].each do |name|
  File.open(File.join(run_root, name), File::RDONLY) { |directory| directory.fsync }
end
File.open(run_root, File::RDONLY) { |directory| directory.fsync }
File.open(task9_staging_root, File::RDONLY) { |directory| directory.fsync }
rename_result = Task9LibC.renamex_np(run_root, destination_run_root, RENAME_EXCL)
raise SystemCallError.new('renamex_np', Fiddle.last_error) unless rename_result.zero?
File.open(task9_root, File::RDONLY) { |directory| directory.fsync }
puts "TASK9_ALLOCATED=#{run_id} guard_id=#{meta_values[2]} source_scope_sha256=#{meta_values[7]}"
RUBY
```

Now run the unique guard, save its complete output exclusively, and bind its actual scope to this generation. A guard failure must be followed by the `INVALIDATED` seal shown after this command; never reuse the run or guard ID:

```zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}" "${PREVIOUS_SCOPE_TSV:?}"
workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_id="$TASK9_RUN_ID"
[[ "$run_id" == run-[0-9][0-9][0-9] ]]
previous_scope_tsv=${PREVIOUS_SCOPE_TSV:A}
run_number=$((10#${run_id#run-}))
guard_id="TASK9_RUN_$(printf '%03d' "$run_number")"
run_root="$snapshot_root/task9/$run_id"
/usr/bin/ruby - "$run_root" "$run_id" "$guard_id" "$previous_scope_tsv" <<'RUBY'
require 'digest'
run_root, run_id, guard_id, source = ARGV
lines = File.readlines(File.join(run_root, '00-meta', 'run-meta.tsv'), chomp: true)
header = lines.shift&.split("\t", -1)
raise 'run-meta row-count drift' unless lines.length == 1
values = lines.first.split("\t", -1)
raise 'run-meta field-count drift' unless values.length == header.length
meta = Hash[header.zip(values)]
raise 'run-meta identity drift' unless meta['Schema'] == 'task9-run/v1' && meta['Run_ID'] == run_id && meta['Guard_ID'] == guard_id
raise 'run-meta source path drift' unless meta['Source_Scope_TSV'] == source
source_bin = source.sub(/\.tsv\z/, '.bin')
raise 'run-meta source/frozen TSV lineage drift' unless meta['Source_Scope_TSV_SHA256'] == meta['Frozen_Input_TSV_SHA256']
raise 'run-meta source/frozen BIN lineage drift' unless meta['Source_Scope_BIN_SHA256'] == meta['Frozen_Input_BIN_SHA256']
raise 'run-meta source TSV hash drift' unless meta['Source_Scope_TSV_SHA256'] == Digest::SHA256.file(source).hexdigest
raise 'run-meta source BIN hash drift' unless meta['Source_Scope_BIN_SHA256'] == Digest::SHA256.file(source_bin).hexdigest
raise 'frozen input TSV drift' unless meta['Frozen_Input_TSV_SHA256'] == Digest::SHA256.file(File.join(run_root, '10-input', 'input-scope.tsv')).hexdigest
raise 'frozen input BIN drift' unless meta['Frozen_Input_BIN_SHA256'] == Digest::SHA256.file(File.join(run_root, '10-input', 'input-scope.bin')).hexdigest
puts 'TASK9_RUN_META=PASS'
RUBY
set +e
guard_output=$(/bin/zsh "$snapshot_root/guard-workspace.zsh" "$guard_id" scope32 "$previous_scope_tsv" 2>&1)
guard_exit=$?
set -e
GUARD_OUTPUT="$guard_output" /usr/bin/ruby - "$run_root/10-input/guard-output.txt" <<'RUBY'
path = ARGV.fetch(0)
bytes = ENV.fetch('GUARD_OUTPUT').b + "\n"
File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(bytes); file.flush; file.fsync }
RUBY
print -r -- "$guard_output"
if (( guard_exit != 0 )); then
  if (( guard_exit >= 64 && guard_exit <= 70 )); then
    failure_action=REBUILD_EVIDENCE
  else
    failure_action=STOP
  fi
  /usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" "$run_id" INVALIDATED INPUT_GUARD_FAIL "$failure_action" NONE NONE "$run_root/10-input/guard-output.txt" NONE NONE NONE NONE
  exit "$guard_exit"
fi

/usr/bin/ruby - "$snapshot_root" "$run_root" "$guard_id" <<'RUBY'
require 'digest'
snapshot, run_root, guard_id = ARGV
members = {
  File.join(snapshot, 'manifests', "#{guard_id}-before-scope.tsv") => File.join(run_root, '10-input', 'guard-scope.tsv'),
  File.join(snapshot, 'manifests', "#{guard_id}-before-scope.bin") => File.join(run_root, '10-input', 'guard-scope.bin')
}
members.each do |source, destination|
  raise "invalid guard member: #{source}" unless File.file?(source) && !File.symlink?(source) && !File.writable?(source)
  bytes = File.binread(source)
  File.open(destination, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(bytes); file.flush; file.fsync }
end
raise 'guard/source TSV mismatch' unless File.binread(File.join(run_root, '10-input', 'guard-scope.tsv')) == File.binread(File.join(run_root, '10-input', 'input-scope.tsv'))
raise 'guard/source binary mismatch' unless File.binread(File.join(run_root, '10-input', 'guard-scope.bin')) == File.binread(File.join(run_root, '10-input', 'input-scope.bin'))
puts "TASK9_INPUT_FROZEN=PASS guard=#{guard_id} sha256=#{Digest::SHA256.file(File.join(run_root, '10-input', 'guard-scope.tsv')).hexdigest}"
RUBY

set +e
static_output=$(/usr/bin/ruby "$snapshot_root/verify-chain.rb" all 2>&1)
static_exit=$?
set -e
STATIC_OUTPUT="$static_output" /usr/bin/ruby - "$run_root/10-input/static-verifier.txt" <<'RUBY'
path = ARGV.fetch(0)
bytes = ENV.fetch('STATIC_OUTPUT').b + "\n"
File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(bytes); file.flush; file.fsync }
RUBY
print -r -- "$static_output"
if (( static_exit != 0 )) || [[ "$static_output" != 'ALL_STATIC=PASS' ]]; then
  /usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" "$run_id" INVALIDATED STATIC_ORACLE_FAIL STOP NONE NONE "$run_root/10-input/static-verifier.txt" NONE NONE NONE NONE
  exit 81
fi
/usr/bin/ruby - "$snapshot_root/manifests" "$run_root/10-input/manifests-set.tsv" <<'RUBY'
require 'digest'
require 'find'
root, output = ARGV
rows = []
Find.find(root) do |path|
  next if path == root
  stat = File.lstat(path)
  raise "unsafe manifest node: #{path}" if stat.symlink? || !stat.file? || (stat.mode & 0o222) != 0
  bytes = File.binread(path)
  rows << ['task9-manifests-set/v1', path.delete_prefix(root + File::SEPARATOR), bytes.bytesize,
           Digest::SHA256.hexdigest(bytes), (stat.mode & 0o777).to_s(8)]
end
rows.sort_by! { |row| row[1].b }
raise 'empty manifests set' if rows.empty?
body = "Schema\tRelative_Path\tBytes\tSHA256\tMode\n" + rows.map { |row| row.join("\t") + "\n" }.join
File.open(output, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
  file.write(body)
  file.flush
  file.fsync
end
RUBY
/usr/bin/ruby - "$run_root" <<'RUBY'
require 'digest'
run_root = ARGV.fetch(0)
members = %w[
  00-meta/run-meta.tsv 10-input/input-scope.tsv 10-input/input-scope.bin
  10-input/guard-scope.tsv 10-input/guard-scope.bin 10-input/static-verifier.txt
  10-input/manifests-set.tsv
]
rows = members.map do |relative|
  path = File.join(run_root, relative)
  raise "missing input-ready member: #{relative}" unless File.file?(path) && !File.symlink?(path)
  bytes = File.binread(path)
  [relative, bytes.bytesize, Digest::SHA256.hexdigest(bytes)]
end
body = "Schema\tRun_ID\tRelative_Path\tBytes\tSHA256\n" +
  rows.map { |relative, bytes, sha| ['task9-input-ready/v1', File.basename(run_root), relative, bytes, sha].join("\t") + "\n" }.join
path = File.join(run_root, '10-input', 'INPUT_READY.tsv')
File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(body); file.flush; file.fsync }
expected = {
  File.join(run_root, '00-meta') => %w[run-meta.tsv],
  File.join(run_root, '10-input') => %w[
    INPUT_READY.tsv guard-output.txt guard-scope.bin guard-scope.tsv input-scope.bin
    input-scope.tsv manifests-set.tsv static-verifier.txt
  ]
}
expected.each do |root, names|
  raise "input phase file-set drift: #{root}" unless Dir.children(root).sort_by(&:b) == names.sort_by(&:b)
  names.each { |name| File.chmod(0o400, File.join(root, name)) }
  File.chmod(0o500, root)
end
expected.each do |root, names|
  raise "input phase root mode drift: #{root}" unless (File.lstat(root).mode & 0o777) == 0o500
  names.each { |name| raise "input phase file mode drift: #{name}" unless (File.lstat(File.join(root, name)).mode & 0o777) == 0o400 }
end
RUBY
print -r -- "TASK9_INPUT_AND_STATIC=PASS run=$run_id guard=$guard_id"
```

Expected success: `WORKSPACE_GUARD=PASS`, `TASK9_INPUT_FROZEN=PASS`, exact static output `ALL_STATIC=PASS`, and `TASK9_INPUT_AND_STATIC=PASS`. The run now binds the exact global manifest-directory set and freezes `00-meta/` plus `10-input/` to directories `0500` and files `0400`; later Task 9 oracles reject an added, removed or changed global manifest. The fixed verifier covers sources, the ten-section audit, 36/36 mapping, controller registry, all canonical/dialogue schemas, exact Handoff lineage lines, one-question/confirmation rules, UTF-8/fences and forbidden expert roleplay.

- [ ] **Step 2: Freeze targets/protected/ZIP, build the cat-stream diff, and prove the diff did not race**

Generate all evidence under the current run. Every output path is exclusive because `four-value-manifest.rb` uses `File.open(..., 'xb')`:

```zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}"
workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_id="$TASK9_RUN_ID"
[[ "$run_id" == run-[0-9][0-9][0-9] ]]
run_root="$snapshot_root/task9/$run_id"
final_root="$run_root/20-final"
manifest="$snapshot_root/four-value-manifest.rb"
plan="$workspace_root/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"
baseline="$snapshot_root/baseline"
cd "$workspace_root"

/usr/bin/ruby - "$run_root" <<'RUBY'
require 'digest'
run_root = ARGV.fetch(0)
path = File.join(run_root, '10-input', 'INPUT_READY.tsv')
lines = File.readlines(path, chomp: true)
raise 'input-ready header drift' unless lines.shift == "Schema\tRun_ID\tRelative_Path\tBytes\tSHA256"
raise 'input-ready member count drift' unless lines.length == 7
lines.each do |line|
  schema, run_id, relative, bytes, sha = line.split("\t", -1)
  raise 'input-ready row drift' unless schema == 'task9-input-ready/v1' && run_id == File.basename(run_root) && bytes.match?(/\A\d+\z/) && sha.match?(/\A[0-9a-f]{64}\z/)
  body = File.binread(File.join(run_root, relative))
  raise "input-ready hash drift: #{relative}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
end
puts 'TASK9_INPUT_READY=PASS'
RUBY

/usr/bin/ruby "$manifest" plan-set "$workspace_root" "$plan" scope32 \
  "$final_root/targets-32-final.bin" "$final_root/targets-32-final.tsv"
/usr/bin/cmp -s "$run_root/10-input/guard-scope.bin" "$final_root/targets-32-final.bin" || {
  /usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" "$run_id" INVALIDATED PRE_DIFF_CONTENT_DRIFT STOP NONE NONE "$final_root/targets-32-final.tsv" NONE NONE NONE NONE
  exit 82
}
/usr/bin/cmp -s "$run_root/10-input/guard-scope.tsv" "$final_root/targets-32-final.tsv" || {
  /usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" "$run_id" INVALIDATED PRE_DIFF_CONTENT_DRIFT STOP NONE NONE "$final_root/targets-32-final.tsv" NONE NONE NONE NONE
  exit 83
}
/usr/bin/ruby "$manifest" plan-set "$snapshot_root/preimage" "$plan" existing31 \
  "$final_root/preimage-31-final.bin" "$final_root/preimage-31-final.tsv"
/usr/bin/ruby "$manifest" protected "$workspace_root" "$plan" '全栈开发Prompt Chain' \
  "$final_root/protected-44-final.bin" "$final_root/protected-44-final.tsv"
/usr/bin/ruby "$manifest" explicit "$workspace_root" "$plan" 1 '全栈开发Prompt Chain.zip' \
  "$final_root/zip-final.bin" "$final_root/zip-final.tsv"

/usr/bin/ruby - "$workspace_root" "$final_root/targets-32-final.tsv" "$final_root/content" "$final_root/frozen-content-32.tsv" <<'RUBY'
require 'digest'
require 'fileutils'
require 'open3'
workspace, manifest_path, content_root, receipt_path = ARGV
raise 'content root already exists' if File.exist?(content_root) || File.symlink?(content_root)
Dir.mkdir(content_root, 0o700)
rows = File.readlines(manifest_path, chomp: true).map { |line| line.split("\t", -1) }
raise 'target manifest row drift' unless rows.length == 32 && rows.all? { |row| row.length == 6 }
receipt = "Relative_Path\tBytes\tSHA256\n"
rows.each do |relative, _path_bytes, _path_sha, cat_bytes, cat_sha, _mode|
  source = File.join(workspace, relative)
  stdout, stderr, result = Open3.capture3('/bin/cat', source)
  raise "cat failed while freezing #{relative}: #{stderr}" unless result.success?
  bytes = stdout.b
  raise "freeze raced target manifest: #{relative}" unless bytes.bytesize.to_s == cat_bytes && Digest::SHA256.hexdigest(bytes) == cat_sha
  destination = File.join(content_root, relative)
  raise "frozen path escaped root: #{relative}" unless destination.start_with?(content_root + File::SEPARATOR)
  FileUtils.mkdir_p(File.dirname(destination), mode: 0o700)
  File.open(destination, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(bytes); file.flush; file.fsync }
  receipt << [relative, bytes.bytesize, cat_sha].join("\t") + "\n"
end
File.open(receipt_path, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(receipt); file.flush; file.fsync }
directories = Dir.glob(File.join(content_root, '**', '*'), File::FNM_DOTMATCH).select { |path| File.directory?(path) && !%w[. ..].include?(File.basename(path)) }
directories.sort_by { |path| -path.count(File::SEPARATOR) }.each { |path| File.chmod(0o500, path) }
File.chmod(0o500, content_root)
puts "TASK9_FROZEN_CONTENT=PASS files=#{rows.length} sha256=#{Digest::SHA256.hexdigest(receipt)}"
RUBY

for suffix in bin tsv; do
  /usr/bin/cmp -s "$baseline/existing-31-before.$suffix" "$final_root/preimage-31-final.$suffix"
  /usr/bin/cmp -s "$baseline/protected-44-before.$suffix" "$final_root/protected-44-final.$suffix"
  /usr/bin/cmp -s "$baseline/zip-before.$suffix" "$final_root/zip-final.$suffix"
done
/usr/bin/ruby - "$run_root" <<'RUBY'
require 'digest'
run_root = ARGV.fetch(0)
members = %w[
  targets-32-final.bin targets-32-final.tsv preimage-31-final.bin preimage-31-final.tsv
  protected-44-final.bin protected-44-final.tsv zip-final.bin zip-final.tsv frozen-content-32.tsv
]
rows = members.map do |name|
  path = File.join(run_root, '20-final', name)
  bytes = File.binread(path)
  [name, bytes.bytesize, Digest::SHA256.hexdigest(bytes)]
end
body = "Schema\tRun_ID\tName\tBytes\tSHA256\n" +
  rows.map { |name, bytes, sha| ['task9-freeze-ready/v1', File.basename(run_root), name, bytes, sha].join("\t") + "\n" }.join
File.open(File.join(run_root, '20-final', 'FREEZE_READY.tsv'), File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(body); file.flush; file.fsync }
RUBY
```

Create the complete cat-stream diff in one exclusive Ruby write. It deliberately diffs `/bin/cat` output rather than the pathname view:

```zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}"
workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
[[ "$TASK9_RUN_ID" == run-[0-9][0-9][0-9] ]]
/usr/bin/ruby - "$run_root" <<'RUBY'
require 'digest'
run_root = ARGV.fetch(0)
lines = File.readlines(File.join(run_root, '20-final', 'FREEZE_READY.tsv'), chomp: true)
raise 'freeze-ready header drift' unless lines.shift == "Schema\tRun_ID\tName\tBytes\tSHA256"
raise 'freeze-ready count drift' unless lines.length == 9
lines.each do |line|
  schema, receipt_run, name, bytes, sha = line.split("\t", -1)
  raise 'freeze-ready row drift' unless schema == 'task9-freeze-ready/v1' && receipt_run == File.basename(run_root) && bytes.match?(/\A\d+\z/) && sha.match?(/\A[0-9a-f]{64}\z/)
  body = File.binread(File.join(run_root, '20-final', name))
  raise "freeze-ready hash drift: #{name}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
end
puts 'TASK9_FREEZE_READY=PASS'
RUBY
/usr/bin/ruby - "$snapshot_root" "$run_root/20-final/content" "$run_root/20-final/added-content.diff" <<'RUBY'
require 'digest'
require 'open3'
require 'tempfile'

snapshot, frozen_root, output_path = ARGV
plan_path = File.join(frozen_root, '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md')
cat = lambda do |path|
  stdout, stderr, result = Open3.capture3('/bin/cat', path)
  raise "cat failed: #{path}: #{stderr}" unless result.success?
  stdout.b
end
plan = cat.call(plan_path).force_encoding(Encoding::UTF_8)
raise 'invalid plan UTF-8' unless plan.valid_encoding?
scope = plan[/## File Structure and Exact Scope\n(.*?)\n## Frozen Input Gate/m, 1]
raise 'scope missing' unless scope
paths = scope.scan(/^- (?:Modify|Create|Normalize only): `([^`]+)`/).flatten
raise 'scope drift' unless paths.length == 32 && paths.uniq.length == 32
normalization_only = [
  '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md',
  '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
]
diff = +"# cat-stream diff: Task 0 preimage -> Task 9 candidate\n"
(paths - normalization_only).sort_by(&:b).each do |relative|
  current = File.join(frozen_root, relative)
  before = File.join(snapshot, 'preimage', relative)
  before_bytes = File.exist?(before) ? cat.call(before) : ''.b
  current_bytes = cat.call(current)
  Tempfile.create('pm-before') do |left|
    Tempfile.create('pm-current') do |right|
      left.binmode; right.binmode
      left.write(before_bytes); right.write(current_bytes)
      left.flush; right.flush
      stdout, stderr, result = Open3.capture3(
        '/usr/bin/diff', '-u', '-L', "preimage/#{relative}", '-L', "workspace/#{relative}", left.path, right.path
      )
      raise "diff failed: #{relative}: #{stderr}" unless [0, 1].include?(result.exitstatus)
      diff << stdout.b if result.exitstatus == 1
    end
  end
end
raise 'empty diff' unless diff.lines.any? { |line| line.start_with?('+++ workspace/') }
File.open(output_path, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
  file.write(diff)
  file.flush
  file.fsync
end
puts "ABLATION_DIFF=SEALED bytes=#{diff.bytesize} sha256=#{Digest::SHA256.hexdigest(diff)}"
RUBY
```

Immediately re-sample the whole scope after the diff and compare byte-for-byte with the pre-diff frozen manifest:

```zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}"
workspace_root='/Users/lute/Project/vibecoding_config'
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
final_root="$run_root/20-final"
[[ "$TASK9_RUN_ID" == run-[0-9][0-9][0-9] ]]
plan="$workspace_root/全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md"
manifest="$snapshot_root/four-value-manifest.rb"
/usr/bin/ruby "$manifest" plan-set "$workspace_root" "$plan" scope32 \
  "$final_root/targets-32-post-diff.bin" "$final_root/targets-32-post-diff.tsv"
for suffix in bin tsv; do
  /usr/bin/cmp -s "$final_root/targets-32-final.$suffix" "$final_root/targets-32-post-diff.$suffix" || {
    /usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" "$TASK9_RUN_ID" INVALIDATED DIFF_RACE STOP NONE NONE "$final_root/added-content.diff" NONE NONE NONE NONE
    exit 84
  }
done

/usr/bin/ruby - "$final_root/targets-32-final.tsv" "$snapshot_root/baseline/existing-31-before.tsv" "$final_root/inventory.txt" "$final_root/targets-32-final.bin" <<'RUBY'
require 'digest'
final_path, before_path, inventory_path, final_bin = ARGV
load_rows = lambda do |path|
  rows = File.readlines(path, chomp: true).map { |line| line.split("\t", -1) }
  raise "malformed manifest: #{path}" unless rows.all? { |row| row.length == 6 }
  raise "duplicate manifest path: #{path}" unless rows.map(&:first).uniq.length == rows.length
  rows.each_with_object({}) { |row, index| index[row[0]] = row }
end
final = load_rows.call(final_path)
before = load_rows.call(before_path)
new_audit = '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md'
controller = '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
normalization_fixed = [
  '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md',
  '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
]
raise "final count=#{final.length}" unless final.length == 32
raise "before count=#{before.length}" unless before.length == 31
raise 'scope path drift' unless final.keys.sort == (before.keys + [new_audit]).sort
raise 'new audit empty' unless Integer(final.fetch(new_audit)[3], 10).positive?
raise 'dual-read mismatch' unless final.values.all? { |row| row[1] == row[3] && row[2] == row[4] }
raise 'existing mode drift' unless before.all? { |path, row| final.fetch(path)[5] == row[5] }
raise 'normalization-only cat drift' unless normalization_fixed.all? { |path| final.fetch(path)[3, 2] == before.fetch(path)[3, 2] }
content_candidates = before.keys - normalization_fixed
unchanged = content_candidates.select { |path| final.fetch(path)[3, 2] == before.fetch(path)[3, 2] }
raise "unexpected unchanged content: #{unchanged.inspect}" unless unchanged.empty? || unchanged == [controller]
controller_changed = !unchanged.include?(controller)
changed_count = content_candidates.length - unchanged.length
normalization_count = normalization_fixed.length + unchanged.length
branch = controller_changed ? 'retained-or-merged' : 'ablated'
target_sha = Digest::SHA256.file(final_bin).hexdigest
body = "TARGET_INTEGRITY=PASS files=32 content_changed=#{changed_count} normalization_only=#{normalization_count} new=1 controller_adapter=#{branch}\nTARGET_FINAL_MANIFEST_SHA256=#{target_sha}\n"
File.open(inventory_path, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(body); file.flush; file.fsync }
print body
RUBY

/usr/bin/ruby - "$run_root" <<'RUBY'
require 'digest'
run_root = ARGV.fetch(0)
members = %w[
  targets-32-final.bin targets-32-final.tsv targets-32-post-diff.bin targets-32-post-diff.tsv
  preimage-31-final.bin preimage-31-final.tsv protected-44-final.bin protected-44-final.tsv
  zip-final.bin zip-final.tsv frozen-content-32.tsv FREEZE_READY.tsv added-content.diff inventory.txt
]
rows = members.map do |name|
  path = File.join(run_root, '20-final', name)
  raise "missing content-ready member: #{name}" unless File.file?(path) && !File.symlink?(path)
  bytes = File.binread(path)
  [name, bytes.bytesize, Digest::SHA256.hexdigest(bytes)]
end
body = "Schema\tRun_ID\tName\tBytes\tSHA256\n" +
  rows.map { |name, bytes, sha| ['task9-content-ready/v1', File.basename(run_root), name, bytes, sha].join("\t") + "\n" }.join
path = File.join(run_root, '20-final', 'CONTENT_READY.tsv')
File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(body); file.flush; file.fsync }
RUBY

/usr/bin/ruby - "$final_root" <<'RUBY'
require 'digest'
require 'find'
root = ARGV.fetch(0)
root_files = %w[
  targets-32-final.bin targets-32-final.tsv targets-32-post-diff.bin targets-32-post-diff.tsv
  preimage-31-final.bin preimage-31-final.tsv protected-44-final.bin protected-44-final.tsv
  zip-final.bin zip-final.tsv frozen-content-32.tsv FREEZE_READY.tsv added-content.diff inventory.txt
  CONTENT_READY.tsv
].sort_by(&:b)
raise '20-final root set drift' unless Dir.children(root).sort_by(&:b) == (root_files + ['content']).sort_by(&:b)
receipt = File.readlines(File.join(root, 'frozen-content-32.tsv'), chomp: true)
raise 'frozen content receipt header drift' unless receipt.shift == "Relative_Path\tBytes\tSHA256"
expected_content = receipt.map do |line|
  relative, bytes, hash = line.split("\t", -1)
  path = File.join(root, 'content', relative)
  body = File.binread(path)
  raise "frozen content byte drift: #{relative}" unless line.split("\t", -1).length == 3 &&
    body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == hash
  path
end.sort_by(&:b)
actual_content = []
Find.find(File.join(root, 'content')) do |path|
  next if path == File.join(root, 'content')
  stat = File.lstat(path)
  raise "unsafe frozen content node: #{path}" if stat.symlink? || (!stat.directory? && !stat.file?)
  actual_content << path if stat.file?
end
raise 'frozen content exact set drift' unless actual_content.sort_by(&:b) == expected_content
paths = []
Find.find(root) { |path| paths << path }
paths.sort_by { |path| -path.count(File::SEPARATOR) }.each do |path|
  stat = File.lstat(path)
  File.chmod(stat.directory? ? 0o500 : 0o400, path)
end
Find.find(root) do |path|
  stat = File.lstat(path)
  raise "20-final mode drift: #{path}" unless (stat.mode & 0o777) == (stat.directory? ? 0o500 : 0o400)
end
RUBY
print -r -- "TASK9_CONTENT_FROZEN=PASS run=$TASK9_RUN_ID"
```

The only legal inventory branches are `content_changed=29 normalization_only=2 controller_adapter=retained-or-merged` and `content_changed=28 normalization_only=3 controller_adapter=ablated`. Both include `new=1`. The command validates the exact root/content sets and then freezes every `20-final/` file to `0400` and every directory, including the phase root, to `0500`; it performs a fresh mode traversal before PASS. The diff and every later content oracle read only this tree; the post-diff workspace manifest is an endpoint concurrency guard, not the evidence source. No later step may alter workspace content or any `20-final` artifact.

- [ ] **Step 3: Build a deterministic candidate universe and editable draft decisions**

Use `apply_patch` to create `build-ablation-universe.rb` at the fully expanded absolute path `/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce/task9/run-NNN/30-ablation/build-ablation-universe.rb`, replacing `run-NNN` with the current `TASK9_RUN_ID` before the tool call. Never create a workspace-relative `task9/` or `reviews/` path. The complete script is:

```ruby
#!/usr/bin/ruby
require 'base64'
require 'digest'
require 'json'
require 'open3'
require 'set'

SNAPSHOT = '/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
WORKSPACE = '/Users/lute/Project/vibecoding_config'
UNIVERSE_HEADER = %w[
  Candidate_ID Kind Owning_task Role File Anchor_B64 Container_ID Requirement_ref
  First_seen_run Present_in_final Origin Oracle_type Selector_B64 Baseline_Count
].freeze
IDENTITY_FIELDS = %w[
  Kind Owning_task Role File Origin Selector_B64
].freeze
IDENTITY_KEYS = ['Candidate_ID', *IDENTITY_FIELDS].freeze
ORACLE_HEADER = %w[Oracle_ID Candidate_ID Type Artifact_Path Selector_B64 Expected_Count Expected_Present].freeze
HUNK_HEADER = %w[Hunk_ID Candidate_ID].freeze
CROSSWALK_HEADER = %w[Source_Candidate_ID Relation Target_Candidate_ID Rationale].freeze
LEDGER_HEADER = %w[
  Candidate_ID Decision Merge_Target_ID Applied_State Decision_Effect Evidence_Effect
  Safety_Effect Downstream_Effect Verification_Refs Previous_Decision Decision_Change_Reason
].freeze
RECEIPT_KEYS = %w[
  Schema Run_ID Package_Status Universe_Valid Decisions_Valid Applied_Status
  Universe_SHA256 Oracle_SHA256 Hunk_SHA256 Crosswalk_SHA256 Ledger_SHA256
  Target_Manifest_SHA256 Diff_SHA256 Prior_History_SHA256 Pending_Count
  First_Pending_Candidate First_Pending_Owner Failure_Code Details_B64
].freeze
KINDS = %w[method field table term check].freeze

PATH_TASK = {
  '全栈开发Prompt Chain/README.md' => 'TASK1',
  '全栈开发Prompt Chain/report-source.md' => 'TASK1',
  '全栈开发Prompt Chain/05-GitHub候选与替代审计.md' => 'TASK1',
  '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md' => 'TASK1',
  '全栈开发Prompt Chain/03-AI产品全生命周期映射.md' => 'TASK2',
  '全栈开发Prompt Chain/04-模块化Skills工作流.md' => 'TASK2',
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md' => 'TASK2',
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md' => 'TASK2',
  '全栈开发Prompt Chain/prompts/02-机会与市场调研.md' => 'TASK3',
  '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md' => 'TASK3',
  '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md' => 'TASK3',
  '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md' => 'TASK4',
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md' => 'TASK4',
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md' => 'TASK4',
  '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/12-增长与实验.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md' => 'TASK8',
  '全栈开发Prompt Chain/prompts_ask/12-增长与实验.md' => 'TASK8',
  '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md' => 'TASK8'
}.freeze

def role_for(path)
  return 'dialogue' if path.include?('/prompts_ask/')
  return 'controller' if path.end_with?('/prompts/99-端到端Prompt-Chain.md')
  return 'canonical' if path.include?('/prompts/')
  return 'workflow-doc' if path.match?(%r{/(?:03-|04-|06-)})
  'audit'
end

CONTROLLER_PATH = '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
CONTROLLER_LINE = '13. 产品决策图兼容：当前 Axx 含产品实体或 Decision 时，下游只消费派生 `active` 检查为真的当前 rev：Decision Status 必须为 `approved`、`Authoritative_decision_ref` 仍指向当前版本、未到 expiry、`invalidated_by` 条件均未命中，且实体未被 supersede。`active` 只在消费时计算，不是持久状态。已存在但不适用的 ID 必须由现有决定者/Gate 以含 `Authoritative_decision_ref`、`Decision_owner`、`Decision_date`、`Expiry_or_invalidated_by`、`Evidence_Refs` 和适用 `Gate_or_authorization_ref` 的 `closed-not-applicable` Decision 关闭；从未创建的可选 ID 不生成空关闭记录。缺失、未批准、过期、被 invalidated/superseded 或所有权冲突时停止，不创建第二路由、Gate 或授权。'

def cat_bytes(path)
  stdout, stderr, result = Open3.capture3('/bin/cat', path)
  raise "cat failed: #{path}: #{stderr}" unless result.success?
  stdout.b
end

def line_count(root, path, line)
  absolute = File.join(root, path)
  return 0 unless File.file?(absolute) && !File.symlink?(absolute)
  cat_bytes(absolute).lines(chomp: true).count { |candidate| candidate == line }
end

def exclusive_write(path, body, mode = 0o400)
  File.open(path, File::WRONLY | File::CREAT | File::EXCL, mode) do |file|
    file.write(body)
    file.flush
    file.fsync
  end
end

run_root = File.expand_path(ARGV.fetch(0))
run_id = File.basename(run_root)
raise 'run path outside snapshot' unless run_root.start_with?(File.join(SNAPSHOT, 'task9') + File::SEPARATOR)
raise 'invalid run ID' unless run_id.match?(/\Arun-\d{3}\z/)
diff_path = File.join(run_root, '20-final', 'added-content.diff')
out_root = File.join(run_root, '30-ablation')
raise 'invalid diff' unless File.file?(diff_path) && !File.symlink?(diff_path)
content_ready = File.join(run_root, '20-final', 'CONTENT_READY.tsv')
raise 'missing content-ready receipt' unless File.file?(content_ready) && !File.symlink?(content_ready) && !File.writable?(content_ready)
content_root = File.join(run_root, '20-final', 'content')
ready_lines = File.readlines(content_ready, chomp: true)
raise 'content-ready header drift' unless ready_lines.shift == "Schema\tRun_ID\tName\tBytes\tSHA256"
raise 'content-ready member count drift' unless ready_lines.length == 14
ready_lines.each do |line|
  schema, receipt_run, name, bytes, sha = line.split("\t", -1)
  raise 'content-ready row drift' unless schema == 'task9-content-ready/v1' && receipt_run == run_id && bytes.match?(/\A\d+\z/) && sha.match?(/\A[0-9a-f]{64}\z/)
  body = File.binread(File.join(run_root, '20-final', name))
  raise "content-ready hash drift: #{name}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
end

diff_lines = File.binread(diff_path).force_encoding(Encoding::UTF_8).lines(chomp: true)
raise 'invalid diff UTF-8' unless diff_lines.join("\n").valid_encoding?
hunks = []
current_path = nil
current_hunk = nil
diff_lines.each do |line|
  if current_hunk
    if line.start_with?('\\ No newline at end of file')
      current_hunk[:lines] << line
      current_hunk[:positions] << [nil, nil]
      next
    elsif current_hunk[:old_remaining].positive? || current_hunk[:new_remaining].positive?
      old_position = nil
      new_position = nil
      case line[0]
      when ' '
        old_position = current_hunk[:old_line]
        new_position = current_hunk[:new_line]
        current_hunk[:old_remaining] -= 1
        current_hunk[:new_remaining] -= 1
        current_hunk[:old_line] += 1
        current_hunk[:new_line] += 1
      when '-'
        old_position = current_hunk[:old_line]
        current_hunk[:old_remaining] -= 1
        current_hunk[:old_line] += 1
      when '+'
        new_position = current_hunk[:new_line]
        current_hunk[:new_remaining] -= 1
        current_hunk[:new_line] += 1
      else
        raise "invalid hunk body line: #{line.inspect}"
      end
      raise 'negative hunk count' if current_hunk[:old_remaining].negative? || current_hunk[:new_remaining].negative?
      current_hunk[:lines] << line
      current_hunk[:positions] << [old_position, new_position]
      next
    else
      current_hunk = nil
    end
  end
  if (match = line.match(/\A\+\+\+ workspace\/(.+)\z/))
    current_path = match[1]
  elsif (match = line.match(/\A@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@/))
    raise 'hunk without workspace path' unless current_path
    old_start = Integer(match[1], 10)
    old_count = match[2] ? Integer(match[2], 10) : 1
    new_start = Integer(match[3], 10)
    new_count = match[4] ? Integer(match[4], 10) : 1
    current_hunk = { path: current_path, header: line, lines: [], positions: [], old_line: old_start, new_line: new_start, old_remaining: old_count, new_remaining: new_count }
    hunks << current_hunk
  end
end
raise 'truncated final diff hunk' if current_hunk && (current_hunk[:old_remaining].positive? || current_hunk[:new_remaining].positive?)
raise 'no diff hunks' if hunks.empty?

rows = {}
hunk_links = []
add_candidate = lambda do |kind:, task:, role:, path:, anchor:, container:, requirement:, origin:, selector:, baseline_count:, hunk_id:|
  raise "invalid kind: #{kind}" unless KINDS.include?(kind)
  row = {
    'Candidate_ID' => 'PENDING',
    'Kind' => kind,
    'Owning_task' => task,
    'Role' => role,
    'File' => path,
    'Anchor_B64' => Base64.strict_encode64(anchor.b),
    'Container_ID' => container || 'NONE',
    'Requirement_ref' => requirement,
    'First_seen_run' => run_id,
    'Present_in_final' => 'false',
    'Origin' => origin,
    'Oracle_type' => 'exact-line-count',
    'Selector_B64' => Base64.strict_encode64(selector.b),
    'Baseline_Count' => baseline_count.to_s
  }
  identity = IDENTITY_FIELDS.map { |field| row.fetch(field) }.join("\0")
  candidate_id = "CAND-#{Digest::SHA256.hexdigest(identity)[0, 24].upcase}"
  row['Candidate_ID'] = candidate_id
  if rows.key?(candidate_id)
    raise "candidate collision: #{candidate_id}" unless IDENTITY_KEYS.all? { |key| rows[candidate_id][key] == row[key] }
  else
    rows[candidate_id] = row
  end
  hunk_links << [hunk_id, candidate_id] unless hunk_id == 'NONE'
  candidate_id
end

separator = ->(line) { line.match?(/\A\|(?:\s*:?-{3,}:?\s*\|)+\z/) }
normative = /\b(?:must|only|cannot|requires?|forbidden|stop|block|never|unless)\b|不得|必须|只能|禁止|停止|阻断|不可|仅当/i

hunks.each do |hunk|
  path = hunk.fetch(:path)
  task = PATH_TASK.fetch(path) { raise "diff path has no owning task: #{path}" }
  role = role_for(path)
  hunk_bytes = ([hunk.fetch(:header)] + hunk.fetch(:lines)).join("\n") + "\n"
  hunk_id = "HUNK-#{Digest::SHA256.hexdigest(path.b + "\0" + hunk_bytes.b)}"
  nearest_method = { 'added' => nil, 'removed' => nil }
  lines = hunk.fetch(:lines)
  positions = hunk.fetch(:positions)
  before_lines = File.file?(File.join(SNAPSHOT, 'preimage', path)) ? cat_bytes(File.join(SNAPSHOT, 'preimage', path)).lines(chomp: true) : []
  final_lines = cat_bytes(File.join(content_root, path)).lines(chomp: true)
  index = 0
  generated_for_hunk = 0
  while index < lines.length
    raw = lines[index]
    unless raw.start_with?('+', '-')
      index += 1
      next
    end
    origin = raw.start_with?('+') ? 'added' : 'removed'
    text = raw[1..]
    if text.empty?
      index += 1
      next
    end
    baseline_count = line_count(File.join(SNAPSHOT, 'preimage'), path, text)
    requirement = "approved-design + plan:#{task}"
    if text.match?(/\A\#{1,6}\s+\S/)
      nearest_method[origin] = add_candidate.call(kind: 'method', task: task, role: role, path: path, anchor: text, container: nil, requirement: requirement, origin: origin, selector: text, baseline_count: baseline_count, hunk_id: hunk_id)
      generated_for_hunk += 1
    else
      line_number = origin == 'added' ? positions.fetch(index)[1] : positions.fetch(index)[0]
      view_lines = origin == 'added' ? final_lines : before_lines
      table_header = text.start_with?('|') && text.end_with?('|') && line_number && separator.call(view_lines[line_number])
      if table_header
      table_id = add_candidate.call(kind: 'table', task: task, role: role, path: path, anchor: text, container: nearest_method[origin], requirement: requirement, origin: origin, selector: text, baseline_count: baseline_count, hunk_id: hunk_id)
      fields = text.sub(/\A\|/, '').sub(/\|\z/, '').split('|', -1).map(&:strip)
      raise "empty table field: #{path}: #{text}" if fields.empty? || fields.any?(&:empty?)
      fields.each_with_index do |field, field_index|
        selector = JSON.generate([text, field_index, field])
        add_candidate.call(kind: 'field', task: task, role: role, path: path, anchor: field, container: table_id, requirement: requirement, origin: origin, selector: selector, baseline_count: baseline_count, hunk_id: hunk_id)
        generated_for_hunk += 1
      end
      generated_for_hunk += 1
      elsif separator.call(text)
        # A separator is structural evidence owned by its table candidate.
      else
        kind = text.match?(normative) ? 'check' : 'term'
        add_candidate.call(kind: kind, task: task, role: role, path: path, anchor: text, container: nearest_method[origin], requirement: requirement, origin: origin, selector: text, baseline_count: baseline_count, hunk_id: hunk_id)
        generated_for_hunk += 1
      end
    end
    index += 1
  end
  raise "uncovered diff hunk: #{hunk_id}" if generated_for_hunk.zero?
end

controller_path = '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
controller_line = '13. 产品决策图兼容：当前 Axx 含产品实体或 Decision 时，下游只消费派生 `active` 检查为真的当前 rev：Decision Status 必须为 `approved`、`Authoritative_decision_ref` 仍指向当前版本、未到 expiry、`invalidated_by` 条件均未命中，且实体未被 supersede。`active` 只在消费时计算，不是持久状态。已存在但不适用的 ID 必须由现有决定者/Gate 以含 `Authoritative_decision_ref`、`Decision_owner`、`Decision_date`、`Expiry_or_invalidated_by`、`Evidence_Refs` 和适用 `Gate_or_authorization_ref` 的 `closed-not-applicable` Decision 关闭；从未创建的可选 ID 不生成空关闭记录。缺失、未批准、过期、被 invalidated/superseded 或所有权冲突时停止，不创建第二路由、Gate 或授权。'
controller_id = 'CAND-T2-CONTROLLER-ACTIVE-HANDOFF'
controller_row = {
  'Candidate_ID' => controller_id, 'Kind' => 'check', 'Owning_task' => 'TASK2', 'Role' => 'controller',
  'File' => controller_path, 'Anchor_B64' => Base64.strict_encode64(controller_line.b), 'Container_ID' => 'NONE',
  'Requirement_ref' => 'approved-design:controller-ablation', 'First_seen_run' => run_id,
  'Present_in_final' => 'false', 'Origin' => 'controller', 'Oracle_type' => 'exact-line-count',
  'Selector_B64' => Base64.strict_encode64(controller_line.b),
  'Baseline_Count' => line_count(File.join(SNAPSHOT, 'preimage'), controller_path, controller_line).to_s
}
rows[controller_id] = controller_row

run_number = Integer(run_id.delete_prefix('run-'), 10)
prior_decisions = {}
(1...run_number).each do |number|
  prior_root = File.join(SNAPSHOT, 'task9', format('run-%03d', number))
  packages = %w[published pending-history].map { |name| File.join(prior_root, '30-ablation', name) }.select { |path| File.directory?(path) && !File.symlink?(path) }
  next if packages.empty?
  raise "multiple prior packages: #{prior_root}" unless packages.length == 1
  package = packages.first
  phase_lines = File.readlines(File.join(package, 'phase-manifest.tsv'), chomp: true)
  raise "prior phase header drift: #{package}" unless phase_lines.shift == "Relative_Path\tBytes\tSHA256"
  phase_rows = phase_lines.map { |line| line.split("\t", -1) }
  raise "prior phase row drift: #{package}" unless phase_rows.all? { |row| row.length == 3 && row[1].match?(/\A\d+\z/) && row[2].match?(/\A[0-9a-f]{64}\z/) }
  raise "prior phase file-set drift: #{package}" unless Dir.children(package).sort == (phase_rows.map(&:first) + ['phase-manifest.tsv']).sort
  phase_rows.each do |name, bytes, sha|
    body = File.binread(File.join(package, name))
    raise "prior phase member drift: #{name}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
  end
  validation_path = File.join(package, 'ablation-validation.txt')
  pairs = File.readlines(validation_path, chomp: true).map do |line|
    key, value = line.split('=', 2)
    raise "malformed prior receipt: #{validation_path}" unless key && value && !value.empty?
    [key, value]
  end
  raise "prior receipt key/order drift: #{validation_path}" unless pairs.map(&:first) == RECEIPT_KEYS && pairs.map(&:first).uniq.length == pairs.length
  validation = pairs.to_h
  terminal_lines = File.readlines(File.join(prior_root, 'TERMINAL.tsv'), chomp: true)
  terminal_header = terminal_lines.shift&.split("\t", -1)
  expected_terminal_header = %w[Schema Run_ID State Reason_Code Required_Action Owning_Task Candidate_ID Next_Evidence_ID Rework_Reservation_Path Rework_Reservation_SHA256 Artifact_Path Input_Scope_TSV Input_Scope_SHA256 Review_Input_SHA256 Target_Manifest_SHA256 Candidate_Universe_SHA256 Ablation_Ledger_SHA256 Generation_Seal_SHA256]
  raise "prior terminal drift: #{prior_root}" unless terminal_header == expected_terminal_header && terminal_lines.length == 1
  terminal_values = terminal_lines.first.split("\t", -1)
  raise "prior terminal field drift: #{prior_root}" unless terminal_values.length == terminal_header.length
  terminal = Hash[terminal_header.zip(terminal_values)]
  next if terminal['Reason_Code'] == 'ABLATION_REVIEW_BLOCKED'
  next unless validation['Universe_Valid'] == 'PASS'
  universe_path = File.join(package, 'candidate-universe.tsv')
  raise "prior universe receipt hash drift: #{package}" unless validation['Universe_SHA256'] == Digest::SHA256.file(universe_path).hexdigest
  raise "prior universe terminal hash drift: #{package}" unless terminal['Candidate_Universe_SHA256'] == validation['Universe_SHA256']
  next unless File.file?(universe_path) && !File.symlink?(universe_path)
  lines = File.readlines(universe_path, chomp: true)
  header = lines.shift&.split("\t", -1)
  raise "prior universe header drift: #{universe_path}" unless header == UNIVERSE_HEADER
  lines.each do |line|
    fields = line.split("\t", -1)
    raise "prior universe row drift: #{universe_path}" unless fields.length == header.length
    prior = Hash[header.zip(fields)]
    if rows.key?(prior['Candidate_ID'])
      raise "candidate identity changed: #{prior['Candidate_ID']}" unless IDENTITY_KEYS.all? { |key| rows[prior['Candidate_ID']][key] == prior[key] }
      rows[prior['Candidate_ID']]['First_seen_run'] = prior['First_seen_run']
    else
      rows[prior['Candidate_ID']] = prior
    end
  end
  next unless validation['Decisions_Valid'] == 'PASS'
  ledger_path = File.join(package, 'ablation-ledger.tsv')
  raise "prior ledger receipt hash drift: #{package}" unless validation['Ledger_SHA256'] == Digest::SHA256.file(ledger_path).hexdigest
  raise "prior ledger terminal hash drift: #{package}" unless terminal['Ablation_Ledger_SHA256'] == validation['Ledger_SHA256']
  ledger_lines = File.readlines(ledger_path, chomp: true)
  ledger_header = ledger_lines.shift&.split("\t", -1)
  raise "prior ledger header drift: #{ledger_path}" unless ledger_header == LEDGER_HEADER
  ledger_lines.each do |line|
    entry = Hash[ledger_header.zip(line.split("\t", -1))]
    prior_decisions[entry['Candidate_ID']] = entry['Decision']
  end
end

rows.each_value do |row|
  selector = Base64.strict_decode64(row['Selector_B64'])
  current_count = if row['Kind'] == 'field'
    header_line, field_index, field = JSON.parse(selector)
    absolute = File.join(content_root, row['File'])
    headers = cat_bytes(absolute).lines(chomp: true).select { |line| line == header_line }
    headers.count do |line|
      fields = line.sub(/\A\|/, '').sub(/\|\z/, '').split('|', -1).map(&:strip)
      fields.fetch(Integer(field_index)) == field
    end
  else
    line_count(content_root, row['File'], selector)
  end
  baseline_count = Integer(row['Baseline_Count'], 10)
  present = case row['Origin']
            when 'added', 'controller' then current_count > baseline_count
            when 'removed' then current_count >= baseline_count
            else current_count > baseline_count
            end
  row['Present_in_final'] = present.to_s
end

depth = lambda do |candidate_id, seen = Set.new|
  return 0 if candidate_id == 'NONE'
  raise "container cycle: #{candidate_id}" if seen.include?(candidate_id)
  row = rows.fetch(candidate_id)
  1 + depth.call(row['Container_ID'], seen | [candidate_id])
end
ordered = rows.values.sort_by { |row| [-depth.call(row['Candidate_ID']), row['Candidate_ID']] }
raise 'candidate ID collision' unless ordered.map { |row| row['Candidate_ID'] }.uniq.length == ordered.length
raise 'missing candidate kind' unless (KINDS - ordered.map { |row| row['Kind'] }.uniq).empty?

universe = UNIVERSE_HEADER.join("\t") + "\n" + ordered.map { |row| UNIVERSE_HEADER.map { |key| row.fetch(key) }.join("\t") + "\n" }.join
oracles = ORACLE_HEADER.join("\t") + "\n" + ordered.map do |row|
  selector = Base64.strict_decode64(row['Selector_B64'])
  expected_count = if row['Kind'] == 'field'
    header_line, field_index, field = JSON.parse(selector)
    cat_bytes(File.join(content_root, row['File'])).lines(chomp: true).count do |line|
      next false unless line == header_line
      fields = line.sub(/\A\|/, '').sub(/\|\z/, '').split('|', -1).map(&:strip)
      fields.fetch(Integer(field_index)) == field
    end
  else
    line_count(content_root, row['File'], selector)
  end
  ["ORACLE-#{row['Candidate_ID']}", row['Candidate_ID'], row['Oracle_type'], row['File'], row['Selector_B64'], expected_count, row['Present_in_final']].join("\t") + "\n"
end.join
hunk_map = HUNK_HEADER.join("\t") + "\n" + hunk_links.uniq.sort.map { |link| link.join("\t") + "\n" }.join

by_path_kind_anchor = ordered.group_by { |row| [row['File'], row['Kind'], row['Anchor_B64']] }
crosswalk_rows = ordered.select { |row| row['Role'] == 'dialogue' }.map do |row|
  canonical_path = row['File'].sub('/prompts_ask/', '/prompts/')
  candidates = by_path_kind_anchor.fetch([canonical_path, row['Kind'], row['Anchor_B64']], [])
  target = candidates.length == 1 ? candidates.first['Candidate_ID'] : 'UNRESOLVED'
  rationale = candidates.length == 1 ? 'exact canonical kind/anchor match' : 'UNRESOLVED'
  [row['Candidate_ID'], 'mirrors', target, rationale]
end
crosswalk = CROSSWALK_HEADER.join("\t") + "\n" + crosswalk_rows.map { |row| row.join("\t") + "\n" }.join

ledger_rows = ordered.map do |row|
  previous = prior_decisions.fetch(row['Candidate_ID'], 'NONE')
  decision = if row['Present_in_final'] == 'true'
    'retain'
  elsif previous != 'NONE'
    previous
  else
    'remove'
  end
  applied = ((decision == 'retain') == (row['Present_in_final'] == 'true')) ? 'reflected' : 'pending'
  [
    row['Candidate_ID'], decision, 'NONE', applied,
    "#{decision} #{row['Kind']} at #{row['File']}", 'preserve explicit evidence boundary or document its removal',
    'preserve applicable Gate/R3/privacy boundary or document none', 'preserve downstream contract or document none',
    "ORACLE-#{row['Candidate_ID']}", previous, 'NONE'
  ]
end
ledger = LEDGER_HEADER.join("\t") + "\n" + ledger_rows.map { |row| row.join("\t") + "\n" }.join

exclusive_write(File.join(out_root, 'candidate-universe.tsv'), universe)
exclusive_write(File.join(out_root, 'content-oracles.tsv'), oracles)
exclusive_write(File.join(out_root, 'diff-hunk-crosswalk.tsv'), hunk_map)
exclusive_write(File.join(out_root, 'candidate-crosswalk.draft.tsv'), crosswalk, 0o600)
exclusive_write(File.join(out_root, 'ablation-ledger.draft.tsv'), ledger, 0o600)
puts "CANDIDATE_UNIVERSE=SEALED candidates=#{ordered.length} sha256=#{Digest::SHA256.hexdigest(universe)} hunks=#{hunks.length}"
```

Run and syntax-check it:

```zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}"
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
[[ "$TASK9_RUN_ID" == run-[0-9][0-9][0-9] ]]
builder="$run_root/30-ablation/build-ablation-universe.rb"
/usr/bin/ruby -c "$builder"
/bin/chmod a-w "$builder"
/usr/bin/ruby "$builder" "$run_root"
/bin/chmod a-w "$run_root/30-ablation/candidate-universe.tsv" \
  "$run_root/30-ablation/content-oracles.tsv" \
  "$run_root/30-ablation/diff-hunk-crosswalk.tsv"
```

The universe is the exact union of every semantic added/removed diff line, every individual field of each changed Markdown table header, the fixed controller candidate and all candidates from earlier machine-validated `published/` or `pending-history/` packages. An invalid draft is never inherited as authority. Each current diff hunk has at least one crosswalk row. Stable identity is `Kind + Owning_task + Role + File + Origin + Selector_B64`; identity changes create a new ID. The builder preserves the earliest validated `First_seen_run` and orders leaves before containers.

Review the two `.draft.tsv` files row by row. Use `apply_patch` only on their fully expanded absolute snapshot paths. Replace every `UNRESOLVED` dialogue crosswalk with one canonical candidate of the same module and `Kind`; the mapping must express semantic mirroring, not merely a similar word. For every ledger row, decide exactly `retain | remove | merge`; a merge names another Candidate ID. Change the four effect columns from generated starting text wherever they do not state the candidate-specific decision/evidence/safety/downstream effect. If a decision differs from `Previous_Decision`, record a non-`NONE` `Decision_Change_Reason`. Never edit the sealed universe/oracle/hunk files.

- [ ] **Step 4: Validate the complete ablation package, publish it exclusively, and stop on pending work**

Use apply_patch to create validate-ablation.rb at the fully expanded current-run path under 30-ablation/. This is a second implementation, not a call back into the builder. It re-derives the current diff candidates and hunk links, recomputes the content oracles, validates cumulative identity, and publishes the two drafts only after the whole package is structurally valid:

~~~ruby
#!/usr/bin/ruby
require 'base64'
require 'digest'
require 'fiddle/import'
require 'find'
require 'json'
require 'open3'
require 'set'
require 'tempfile'
require 'tmpdir'

SNAPSHOT = '/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
WORKSPACE = '/Users/lute/Project/vibecoding_config'
UNIVERSE_HEADER = %w[
  Candidate_ID Kind Owning_task Role File Anchor_B64 Container_ID Requirement_ref
  First_seen_run Present_in_final Origin Oracle_type Selector_B64 Baseline_Count
].freeze
IDENTITY_FIELDS = %w[
  Kind Owning_task Role File Origin Selector_B64
].freeze
IDENTITY_FIELDS_BYTES = IDENTITY_FIELDS.join("\0").b.freeze
IDENTITY_FIELDS_SHA256 = Digest::SHA256.hexdigest(IDENTITY_FIELDS_BYTES).freeze
IDENTITY_KEYS = ['Candidate_ID', *IDENTITY_FIELDS].freeze
ORACLE_HEADER = %w[Oracle_ID Candidate_ID Type Artifact_Path Selector_B64 Expected_Count Expected_Present].freeze
HUNK_HEADER = %w[Hunk_ID Candidate_ID].freeze
CROSSWALK_HEADER = %w[Source_Candidate_ID Relation Target_Candidate_ID Rationale].freeze
LEDGER_HEADER = %w[
  Candidate_ID Decision Merge_Target_ID Applied_State Decision_Effect Evidence_Effect
  Safety_Effect Downstream_Effect Verification_Refs Previous_Decision Decision_Change_Reason
].freeze
RECEIPT_KEYS = %w[
  Schema Run_ID Package_Status Universe_Valid Decisions_Valid Applied_Status
  Universe_SHA256 Oracle_SHA256 Hunk_SHA256 Crosswalk_SHA256 Ledger_SHA256
  Target_Manifest_SHA256 Diff_SHA256 Prior_History_SHA256 Pending_Count
  First_Pending_Candidate First_Pending_Owner Failure_Code Details_B64
].freeze
PACKAGE_FILES = %w[
  ablation-ledger.tsv ablation-validation.txt candidate-crosswalk.tsv
  candidate-universe.tsv content-oracles.tsv diff-hunk-crosswalk.tsv
  identity-contract.tsv prior-history.tsv
].freeze
TERMINAL_HEADER = %w[
  Schema Run_ID State Reason_Code Required_Action Owning_Task Candidate_ID Next_Evidence_ID
  Rework_Reservation_Path Rework_Reservation_SHA256 Artifact_Path
  Input_Scope_TSV Input_Scope_SHA256 Review_Input_SHA256 Target_Manifest_SHA256
  Candidate_Universe_SHA256 Ablation_Ledger_SHA256 Generation_Seal_SHA256
].freeze
PATH_TASK = {
  '全栈开发Prompt Chain/README.md' => 'TASK1',
  '全栈开发Prompt Chain/report-source.md' => 'TASK1',
  '全栈开发Prompt Chain/05-GitHub候选与替代审计.md' => 'TASK1',
  '全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md' => 'TASK1',
  '全栈开发Prompt Chain/03-AI产品全生命周期映射.md' => 'TASK2',
  '全栈开发Prompt Chain/04-模块化Skills工作流.md' => 'TASK2',
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md' => 'TASK2',
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md' => 'TASK2',
  '全栈开发Prompt Chain/prompts/02-机会与市场调研.md' => 'TASK3',
  '全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md' => 'TASK3',
  '全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md' => 'TASK3',
  '全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md' => 'TASK4',
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md' => 'TASK4',
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md' => 'TASK4',
  '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/12-增长与实验.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md' => 'TASK5',
  '全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md' => 'TASK6',
  '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md' => 'TASK7',
  '全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md' => 'TASK8',
  '全栈开发Prompt Chain/prompts_ask/12-增长与实验.md' => 'TASK8',
  '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md' => 'TASK8'
}.freeze

def role_for(path)
  return 'dialogue' if path.include?('/prompts_ask/')
  return 'controller' if path.end_with?('/prompts/99-端到端Prompt-Chain.md')
  return 'canonical' if path.include?('/prompts/')
  return 'workflow-doc' if path.match?(%r{/(?:03-|04-|06-)})
  'audit'
end

CONTROLLER_PATH = '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
CONTROLLER_LINE = '13. 产品决策图兼容：当前 Axx 含产品实体或 Decision 时，下游只消费派生 `active` 检查为真的当前 rev：Decision Status 必须为 `approved`、`Authoritative_decision_ref` 仍指向当前版本、未到 expiry、`invalidated_by` 条件均未命中，且实体未被 supersede。`active` 只在消费时计算，不是持久状态。已存在但不适用的 ID 必须由现有决定者/Gate 以含 `Authoritative_decision_ref`、`Decision_owner`、`Decision_date`、`Expiry_or_invalidated_by`、`Evidence_Refs` 和适用 `Gate_or_authorization_ref` 的 `closed-not-applicable` Decision 关闭；从未创建的可选 ID 不生成空关闭记录。缺失、未批准、过期、被 invalidated/superseded 或所有权冲突时停止，不创建第二路由、Gate 或授权。'

def cat_bytes(path)
  stdout, stderr, result = Open3.capture3('/bin/cat', path)
  raise "cat failed: #{path}: #{stderr}" unless result.success?
  stdout.b
end

def read_regular(path, required_mode = nil)
  before = File.lstat(path)
  raise "unsafe regular file: #{path}" unless before.file? && !before.symlink? && before.nlink == 1
  raise "file mode drift: #{path}" if required_mode && (before.mode & 0o777) != required_mode
  flags = File::RDONLY
  flags |= File::NOFOLLOW if File.const_defined?(:NOFOLLOW)
  File.open(path, flags) do |file|
    opened = file.stat
    raise "opened inode drift: #{path}" unless [before.dev, before.ino] == [opened.dev, opened.ino]
    bytes = file.read.b
    after = File.lstat(path)
    raise "pathname replaced while reading: #{path}" unless [opened.dev, opened.ino] == [after.dev, after.ino]
    bytes
  end
end

def cat_regular(path, required_mode = nil)
  before = File.lstat(path)
  raise "unsafe cat-stream file: #{path}" unless before.file? && !before.symlink?
  raise "cat-stream mode drift: #{path}" if required_mode && (before.mode & 0o777) != required_mode
  bytes = cat_bytes(path)
  after = File.lstat(path)
  raise "cat-stream pathname replaced: #{path}" unless [before.dev, before.ino] == [after.dev, after.ino]
  bytes
end

def recompute_diff(snapshot, content_root, paths)
  normalization_only = [
    '全栈开发Prompt Chain/docs/superpowers/specs/2026-09-03-pm-skill-core-workflow-integration-design.md',
    '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md'
  ]
  diff = +"# cat-stream diff: Task 0 preimage -> Task 9 candidate\n"
  (paths - normalization_only).sort_by(&:b).each do |relative|
    before_path = File.join(snapshot, 'preimage', relative)
    final_path = File.join(content_root, relative)
    before_bytes = File.exist?(before_path) ? cat_regular(before_path) : ''.b
    final_bytes = cat_regular(final_path, 0o400)
    Tempfile.create('ablation-before') do |before|
      Tempfile.create('ablation-final') do |final|
        before.binmode
        final.binmode
        before.write(before_bytes)
        final.write(final_bytes)
        before.flush
        final.flush
        stdout, stderr, status = Open3.capture3(
          '/usr/bin/diff', '-u', '-L', "preimage/#{relative}", '-L', "workspace/#{relative}",
          before.path, final.path
        )
        raise "diff failed: #{relative}: #{stderr}" unless [0, 1].include?(status.exitstatus)
        diff << stdout.b if status.exitstatus == 1
      end
    end
  end
  diff
end

def parse_tsv(bytes, label, expected_header)
  text = bytes.dup.force_encoding(Encoding::UTF_8)
  raise "invalid UTF-8: #{label}" unless text.valid_encoding?
  lines = text.lines(chomp: true)
  raise "missing final LF: #{label}" unless text.end_with?("\n")
  raise "header drift: #{label}" unless lines.shift&.split("\t", -1) == expected_header
  lines.map.with_index(2) do |line, line_number|
    fields = line.split("\t", -1)
    raise "field count drift: #{label}:#{line_number}" unless fields.length == expected_header.length
    raise "empty field: #{label}:#{line_number}" if fields.any?(&:empty?)
    Hash[expected_header.zip(fields)]
  end
end

def load_tsv(path, expected_header)
  raise "missing TSV: #{path}" unless File.file?(path) && !File.symlink?(path)
  parse_tsv(File.binread(path), path, expected_header)
end

def strict_decode(value)
  bytes = Base64.strict_decode64(value)
  raise 'non-canonical base64' unless Base64.strict_encode64(bytes) == value
  text = bytes.force_encoding(Encoding::UTF_8)
  raise 'invalid decoded UTF-8' unless text.valid_encoding?
  text
end

def exact_line_count(root, relative, line)
  absolute = File.join(root, relative)
  return 0 unless File.file?(absolute) && !File.symlink?(absolute)
  cat_bytes(absolute).lines(chomp: true).count { |candidate| candidate == line }
end

def key_values(path, expected_keys = nil)
  pairs = File.readlines(path, chomp: true).map do |line|
    key, value = line.split('=', 2)
    raise "invalid key-value line: #{path}: #{line}" unless key && value && !value.empty?
    [key, value]
  end
  raise "duplicate receipt key: #{path}" unless pairs.map(&:first).uniq.length == pairs.length
  raise "receipt key/order drift: #{path}" if expected_keys && pairs.map(&:first) != expected_keys
  pairs.to_h
end

def freeze_draft(path)
  flags = File::RDONLY
  flags |= File::NOFOLLOW if File.const_defined?(:NOFOLLOW)
  File.open(path, flags) do |file|
    before = file.stat
    raise "unsafe draft: #{path}" unless before.file? && before.nlink == 1 && (before.mode & 0o777) == 0o600
    bytes = file.read.b
    file.chmod(0o400)
    after = file.stat
    pathname = File.lstat(path)
    raise "draft FD drift: #{path}" unless [before.dev, before.ino] == [after.dev, after.ino]
    raise "draft pathname replaced: #{path}" unless [after.dev, after.ino] == [pathname.dev, pathname.ino]
    raise "draft freeze byte drift: #{path}" unless read_regular(path, 0o400) == bytes
    bytes
  end
end

module DarwinRename
  extend Fiddle::Importer
  dlload Fiddle.dlopen(nil)
  extern 'int renamex_np(const char *, const char *, unsigned int)'
end
RENAME_EXCL = 0x00000004

def publish_package(root, destination_name, files)
  raise 'invalid package destination' unless %w[published pending-history].include?(destination_name)
  raise 'package member set drift' unless files.keys.sort_by(&:b) == PACKAGE_FILES.sort_by(&:b)
  destination = File.join(root, destination_name)
  raise 'package destination exists' if File.exist?(destination) || File.symlink?(destination)
  stage = Dir.mktmpdir('.publish-', root)
  files.each do |name, bytes|
    raise "unsafe package member: #{name}" unless name.match?(/\A[A-Za-z0-9._-]+\z/)
    File.open(File.join(stage, name), File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(bytes); file.flush; file.fsync }
  end
  rows = PACKAGE_FILES.sort_by(&:b).map { |name| [name, files.fetch(name).bytesize, Digest::SHA256.hexdigest(files.fetch(name))] }
  manifest = "Relative_Path\tBytes\tSHA256\n" + rows.map { |row| row.join("\t") + "\n" }.join
  File.open(File.join(stage, 'phase-manifest.tsv'), File::WRONLY | File::CREAT | File::EXCL, 0o400) { |file| file.write(manifest); file.flush; file.fsync }
  expected = (PACKAGE_FILES + ['phase-manifest.tsv']).sort_by(&:b)
  raise 'staged package file-set drift' unless Dir.children(stage).sort_by(&:b) == expected
  File.open(stage, File::RDONLY) { |directory| directory.fsync }
  File.chmod(0o500, stage)
  result = DarwinRename.renamex_np(stage, destination, RENAME_EXCL)
  raise SystemCallError.new("renamex_np #{stage} -> #{destination}", Fiddle.last_error) unless result.zero?
  File.open(root, File::RDONLY) { |directory| directory.fsync }
  raise 'published package file-set drift' unless Dir.children(destination).sort_by(&:b) == expected
  files.each { |name, bytes| raise "published byte drift: #{name}" unless read_regular(File.join(destination, name), 0o400) == bytes }
  raise 'phase manifest drift' unless read_regular(File.join(destination, 'phase-manifest.tsv'), 0o400) == manifest
  Digest::SHA256.hexdigest(manifest)
end

def verify_package(path)
  package_stat = File.lstat(path)
  raise "invalid package directory: #{path}" unless package_stat.directory? && !package_stat.symlink? && (package_stat.mode & 0o777) == 0o500
  manifest_path = File.join(path, 'phase-manifest.tsv')
  lines = read_regular(manifest_path, 0o400).lines(chomp: true)
  raise 'phase manifest header drift' unless lines.shift == "Relative_Path\tBytes\tSHA256"
  rows = lines.map { |line| line.split("\t", -1) }
  raise 'phase manifest row drift' unless rows.all? { |row| row.length == 3 && row[0].match?(/\A[A-Za-z0-9._-]+\z/) && row[1].match?(/\A\d+\z/) && row[2].match?(/\A[0-9a-f]{64}\z/) }
  raise 'duplicate phase manifest row' unless rows.map(&:first).uniq.length == rows.length
  raise 'package schema/order drift' unless rows.map(&:first) == PACKAGE_FILES.sort_by(&:b)
  expected = (PACKAGE_FILES + ['phase-manifest.tsv']).sort_by(&:b)
  raise 'package file-set drift' unless Dir.children(path).sort_by(&:b) == expected
  rows.each do |name, bytes, sha|
    body = read_regular(File.join(path, name), 0o400)
    raise "package member drift: #{name}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
  end
  Digest::SHA256.hexdigest(read_regular(manifest_path, 0o400))
end

def verify_prior_terminal(prior_root, prior_id)
  root_stat = File.lstat(prior_root)
  raise "unsafe prior run root: #{prior_id}" unless root_stat.directory? && !root_stat.symlink? && (root_stat.mode & 0o222).zero?
  terminal_path = File.join(prior_root, 'TERMINAL.tsv')
  intent_path = File.join(prior_root, 'terminal-intent.tsv')
  seal_path = File.join(prior_root, 'generation-seal.tsv')
  terminal_bytes = read_regular(terminal_path, 0o400)
  raise "prior terminal intent drift: #{prior_id}" unless read_regular(intent_path, 0o400) == terminal_bytes
  terminal_lines = terminal_bytes.lines(chomp: true)
  raise "prior terminal header drift: #{prior_id}" unless terminal_lines.shift&.split("\t", -1) == TERMINAL_HEADER
  raise "prior terminal row-count drift: #{prior_id}" unless terminal_lines.length == 1
  terminal_values = terminal_lines.first.split("\t", -1)
  raise "prior terminal field-count drift: #{prior_id}" unless terminal_values.length == TERMINAL_HEADER.length
  terminal = Hash[TERMINAL_HEADER.zip(terminal_values)]
  raise "prior terminal identity drift: #{prior_id}" unless terminal['Schema'] == 'task9-terminal/v1' && terminal['Run_ID'] == prior_id
  raise "prior terminal state drift: #{prior_id}" unless terminal['State'] == 'INVALIDATED'
  if terminal['Required_Action'] == 'REWORK_CONTENT'
    expected_reservation = File.join(SNAPSHOT, 'task9-rework-reservations', "#{prior_id}.tsv")
    raise "prior reservation path drift: #{prior_id}" unless terminal['Rework_Reservation_Path'] == expected_reservation
    reservation_bytes = read_regular(expected_reservation, 0o400)
    raise "prior reservation hash drift: #{prior_id}" unless Digest::SHA256.hexdigest(reservation_bytes) == terminal['Rework_Reservation_SHA256']
    expected_bytes = "Schema\tOwner\tEvidence_ID\tSource_Run\tCandidate_ID\n" +      "task9-rework-reservation/v1\t#{terminal['Owning_Task']}\t#{terminal['Next_Evidence_ID']}\t#{prior_id}\t#{terminal['Candidate_ID']}\n"
    raise "prior reservation content drift: #{prior_id}" unless reservation_bytes == expected_bytes
  else
    raise "unexpected prior reservation: #{prior_id}" unless terminal['Next_Evidence_ID'] == 'NONE' && terminal['Rework_Reservation_Path'] == 'NONE' && terminal['Rework_Reservation_SHA256'] == 'NONE'
  end

  seal_bytes = read_regular(seal_path, 0o400)
  raise "prior generation seal hash drift: #{prior_id}" unless Digest::SHA256.hexdigest(seal_bytes) == terminal['Generation_Seal_SHA256']
  seal_lines = seal_bytes.lines(chomp: true)
  raise "prior generation seal header drift: #{prior_id}" unless seal_lines.shift == "Relative_Path\tBytes\tSHA256"
  rows = seal_lines.map { |line| line.split("\t", -1) }
  raise "prior generation seal row drift: #{prior_id}" unless rows.all? { |row| row.length == 3 && row[0] && !row[0].empty? && !row[0].start_with?('/') && !row[0].split(File::SEPARATOR).include?('..') && row[1].match?(/\A\d+\z/) && row[2].match?(/\A[0-9a-f]{64}\z/) }
  raise "prior generation seal duplicate/order drift: #{prior_id}" unless rows.map(&:first).uniq.length == rows.length && rows.map(&:first) == rows.map(&:first).sort_by(&:b)
  rows.each do |relative, bytes, sha|
    body = read_regular(File.join(prior_root, relative), 0o400)
    raise "prior sealed member drift: #{prior_id}:#{relative}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
  end

  actual = []
  Find.find(prior_root) do |path|
    next if path == prior_root
    stat = File.lstat(path)
    raise "symlink in prior generation: #{path}" if stat.symlink?
    raise "writable prior generation path: #{path}" unless (stat.mode & 0o222).zero?
    next if stat.directory?
    raise "special node in prior generation: #{path}" unless stat.file?
    relative = path.delete_prefix(prior_root + File::SEPARATOR)
    next if %w[TERMINAL.tsv terminal-intent.tsv generation-seal.tsv].include?(relative)
    actual << relative
  end
  raise "prior generation file-set drift: #{prior_id}" unless actual.sort_by(&:b) == rows.map(&:first)
  [terminal, Digest::SHA256.hexdigest(terminal_bytes)]
end

run_root = File.expand_path(ARGV.fetch(0))
mode = ARGV.fetch(1, 'publish')
run_id = File.basename(run_root)
raise 'invalid mode' unless %w[publish check seal-pending].include?(mode)
raise 'invalid run root' unless run_root == File.join(SNAPSHOT, 'task9', run_id) && run_id.match?(/\Arun-\d{3}\z/)
root = File.join(run_root, '30-ablation')
content_root = File.join(run_root, '20-final', 'content')
universe_path = File.join(root, 'candidate-universe.tsv')
oracle_path = File.join(root, 'content-oracles.tsv')
hunk_path = File.join(root, 'diff-hunk-crosswalk.tsv')
if mode == 'publish'
  raise 'package publication already attempted' if %w[published pending-history].any? { |name| File.exist?(File.join(root, name)) || File.symlink?(File.join(root, name)) }
  crosswalk_bytes = freeze_draft(File.join(root, 'candidate-crosswalk.draft.tsv'))
  ledger_bytes = freeze_draft(File.join(root, 'ablation-ledger.draft.tsv'))
  package_root = nil
  package_kind = nil
else
  package_candidates = %w[published pending-history].select { |name| File.exist?(File.join(root, name)) || File.symlink?(File.join(root, name)) }
  raise 'package cardinality drift' unless package_candidates.length == 1
  package_kind = package_candidates.first
  raise 'seal-pending requires pending-history' if mode == 'seal-pending' && package_kind != 'pending-history'
  package_root = File.join(root, package_kind)
  verified_phase_sha = verify_package(package_root)
  universe_path = File.join(package_root, 'candidate-universe.tsv')
  oracle_path = File.join(package_root, 'content-oracles.tsv')
  hunk_path = File.join(package_root, 'diff-hunk-crosswalk.tsv')
  crosswalk_bytes = read_regular(File.join(package_root, 'candidate-crosswalk.tsv'), 0o400)
  ledger_bytes = read_regular(File.join(package_root, 'ablation-ledger.tsv'), 0o400)
end
stability_paths = [
  universe_path, oracle_path, hunk_path,
  File.join(root, 'build-ablation-universe.rb'),
  File.join(root, 'validate-ablation.rb'),
  File.join(run_root, '20-final', 'CONTENT_READY.tsv'),
  File.join(run_root, '20-final', 'targets-32-final.bin'),
  File.join(run_root, '20-final', 'targets-32-final.tsv'),
  File.join(run_root, '20-final', 'frozen-content-32.tsv'),
  File.join(run_root, '20-final', 'added-content.diff')
]
stability_hashes = stability_paths.to_h { |path| [path, Digest::SHA256.file(path).hexdigest] }

content_ready = File.join(run_root, '20-final', 'CONTENT_READY.tsv')
ready_lines = File.readlines(content_ready, chomp: true)
raise 'content-ready header drift' unless ready_lines.shift == "Schema\tRun_ID\tName\tBytes\tSHA256"
raise 'content-ready member count drift' unless ready_lines.length == 14
ready_lines.each do |line|
  schema, receipt_run, name, bytes, sha = line.split("\t", -1)
  raise 'content-ready row drift' unless schema == 'task9-content-ready/v1' && receipt_run == run_id && bytes.match?(/\A\d+\z/) && sha.match?(/\A[0-9a-f]{64}\z/)
  body = File.binread(File.join(run_root, '20-final', name))
  raise "content-ready hash drift: #{name}" unless body.bytesize.to_s == bytes && Digest::SHA256.hexdigest(body) == sha
end

universe = load_tsv(universe_path, UNIVERSE_HEADER)
raise 'empty universe' if universe.empty?
ids = universe.map { |row| row['Candidate_ID'] }
raise 'duplicate candidate ID' unless ids.uniq.length == ids.length
by_id = universe.to_h { |row| [row['Candidate_ID'], row] }
manifest_rows = File.readlines(File.join(run_root, '20-final', 'targets-32-final.tsv'), chomp: true).map { |line| line.split("\t", -1) }
raise 'target manifest drift' unless manifest_rows.length == 32 && manifest_rows.all? { |row| row.length == 6 }
scope_paths = manifest_rows.map(&:first).to_set
frozen_lines = File.readlines(File.join(run_root, '20-final', 'frozen-content-32.tsv'), chomp: true)
raise 'frozen-content header drift' unless frozen_lines.shift == "Relative_Path\tBytes\tSHA256"
frozen_rows = frozen_lines.map { |line| line.split("\t", -1) }
raise 'frozen-content row drift' unless frozen_rows.length == 32 && frozen_rows.all? { |row| row.length == 3 } && frozen_rows.map(&:first).to_set == scope_paths
manifest_by_path = manifest_rows.to_h { |row| [row[0], row] }
frozen_rows.each do |relative, bytes, sha|
  body = read_regular(File.join(content_root, relative), 0o400)
  manifest_row = manifest_by_path.fetch(relative)
  raise "frozen-content hash drift: #{relative}" unless bytes == body.bytesize.to_s && sha == Digest::SHA256.hexdigest(body) && [bytes, sha] == manifest_row[3, 2]
end
actual_frozen_paths = []
Find.find(content_root) do |path|
  stat = File.lstat(path)
  raise "symlink in frozen content: #{path}" if stat.symlink?
  if stat.directory?
    raise "writable frozen directory: #{path}" unless (stat.mode & 0o222).zero?
  elsif stat.file?
    relative = path.delete_prefix(content_root + File::SEPARATOR)
    raise "writable frozen file: #{path}" unless (stat.mode & 0o777) == 0o400
    actual_frozen_paths << relative
  else
    raise "special node in frozen content: #{path}"
  end
end
raise 'frozen content file-set drift' unless actual_frozen_paths.sort_by(&:b) == frozen_rows.map(&:first).sort_by(&:b)
universe.each do |row|
  raise "bad candidate ID: #{row['Candidate_ID']}" unless row['Candidate_ID'].match?(/\ACAND-[A-Z0-9-]+\z/)
  raise "bad kind: #{row['Candidate_ID']}" unless %w[method field table term check].include?(row['Kind'])
  raise "bad role: #{row['Candidate_ID']}" unless %w[canonical dialogue workflow-doc audit controller].include?(row['Role'])
  raise "bad origin: #{row['Candidate_ID']}" unless %w[added removed controller].include?(row['Origin'])
  raise "candidate outside target scope: #{row['File']}" unless scope_paths.include?(row['File'])
  raise "bad owning task: #{row['Candidate_ID']}" unless row['Owning_task'].match?(/\ATASK[1-8]\z/)
  raise "bad first-seen run: #{row['Candidate_ID']}" unless row['First_seen_run'].match?(/\Arun-\d{3}\z/) && row['First_seen_run'] <= run_id
  raise "bad presence: #{row['Candidate_ID']}" unless %w[true false].include?(row['Present_in_final'])
  raise "bad oracle type: #{row['Candidate_ID']}" unless row['Oracle_type'] == 'exact-line-count'
  raise "bad baseline count: #{row['Candidate_ID']}" unless row['Baseline_Count'].match?(/\A\d+\z/)
  anchor = strict_decode(row['Anchor_B64'])
  selector = strict_decode(row['Selector_B64'])
  raise "empty anchor: #{row['Candidate_ID']}" if anchor.empty?
  raise "empty requirement: #{row['Candidate_ID']}" if row['Requirement_ref'] == 'NONE'
  if row['Origin'] == 'controller'
    expected_controller = {
      'Candidate_ID' => 'CAND-T2-CONTROLLER-ACTIVE-HANDOFF', 'Kind' => 'check',
      'Owning_task' => 'TASK2', 'Role' => 'controller', 'File' => CONTROLLER_PATH,
      'Anchor_B64' => Base64.strict_encode64(CONTROLLER_LINE.b), 'Container_ID' => 'NONE',
      'Requirement_ref' => 'approved-design:controller-ablation', 'Origin' => 'controller',
      'Oracle_type' => 'exact-line-count', 'Selector_B64' => Base64.strict_encode64(CONTROLLER_LINE.b)
    }
    expected_controller.each do |key, value|
      raise "controller contract drift: #{key}" unless row[key] == value
    end
  else
    expected_task = PATH_TASK.fetch(row['File']) { raise "candidate path has no owning task: #{row['File']}" }
    raise "candidate owner drift: #{row['Candidate_ID']}" unless row['Owning_task'] == expected_task
    raise "candidate role drift: #{row['Candidate_ID']}" unless row['Role'] == role_for(row['File'])
    raise "candidate requirement drift: #{row['Candidate_ID']}" unless row['Requirement_ref'] == "approved-design + plan:#{expected_task}"
    if row['Kind'] == 'field'
      decoded = JSON.parse(selector)
      raise "field selector shape drift: #{row['Candidate_ID']}" unless decoded.is_a?(Array) && decoded.length == 3 &&
        decoded[0].is_a?(String) && decoded[1].is_a?(Integer) && decoded[1] >= 0 && decoded[2].is_a?(String)
      raise "field anchor drift: #{row['Candidate_ID']}" unless anchor == decoded[2]
    else
      raise "candidate anchor/selector drift: #{row['Candidate_ID']}" unless anchor == selector
    end
  end
  identity = IDENTITY_FIELDS.map { |field| row.fetch(field) }.join("\0")
  expected_id = row['Origin'] == 'controller' ? 'CAND-T2-CONTROLLER-ACTIVE-HANDOFF' : "CAND-#{Digest::SHA256.hexdigest(identity)[0, 24].upcase}"
  raise "candidate identity/hash drift: #{row['Candidate_ID']}" unless row['Candidate_ID'] == expected_id
end

order = ids.each_with_index.to_h
universe.each do |row|
  next if row['Container_ID'] == 'NONE'
  raise "missing container: #{row['Candidate_ID']}" unless by_id.key?(row['Container_ID'])
  raise "leaf not before container: #{row['Candidate_ID']}" unless order.fetch(row['Candidate_ID']) < order.fetch(row['Container_ID'])
end
visit_container = lambda do |candidate_id, active|
  raise "container cycle: #{candidate_id}" if active.include?(candidate_id)
  parent = by_id.fetch(candidate_id)['Container_ID']
  visit_container.call(parent, active | [candidate_id]) unless parent == 'NONE'
end
ids.each { |candidate_id| visit_container.call(candidate_id, Set.new) }

oracles = load_tsv(oracle_path, ORACLE_HEADER)
raise 'oracle candidate set/order drift' unless oracles.map { |row| row['Candidate_ID'] } == ids
oracle_ids = oracles.map { |row| row['Oracle_ID'] }
raise 'duplicate oracle ID' unless oracle_ids.uniq.length == oracle_ids.length
oracles.each do |oracle|
  candidate = by_id.fetch(oracle['Candidate_ID'])
  raise "oracle ID drift: #{candidate['Candidate_ID']}" unless oracle['Oracle_ID'] == "ORACLE-#{candidate['Candidate_ID']}"
  raise "oracle metadata drift: #{candidate['Candidate_ID']}" unless oracle['Type'] == candidate['Oracle_type'] && oracle['Artifact_Path'] == candidate['File'] && oracle['Selector_B64'] == candidate['Selector_B64']
  selector = strict_decode(oracle['Selector_B64'])
  if candidate['Kind'] == 'field'
    header_line, field_index, field = JSON.parse(selector)
    current_count = cat_bytes(File.join(content_root, candidate['File'])).lines(chomp: true).count do |line|
      next false unless line == header_line
      fields = line.sub(/\A\|/, '').sub(/\|\z/, '').split('|', -1).map(&:strip)
      fields.fetch(Integer(field_index)) == field
    end
    baseline_count = exact_line_count(File.join(SNAPSHOT, 'preimage'), candidate['File'], header_line)
  else
    current_count = exact_line_count(content_root, candidate['File'], selector)
    baseline_count = exact_line_count(File.join(SNAPSHOT, 'preimage'), candidate['File'], selector)
  end
  present = candidate['Origin'] == 'removed' ? current_count >= baseline_count : current_count > baseline_count
  raise "baseline count drift: #{candidate['Candidate_ID']}" unless candidate['Baseline_Count'] == baseline_count.to_s
  raise "oracle count drift: #{candidate['Candidate_ID']}" unless oracle['Expected_Count'] == current_count.to_s
  raise "presence drift: #{candidate['Candidate_ID']}" unless oracle['Expected_Present'] == present.to_s && candidate['Present_in_final'] == present.to_s
end

sealed_diff = read_regular(File.join(run_root, '20-final', 'added-content.diff'), 0o400)
rebuilt_diff = recompute_diff(SNAPSHOT, content_root, scope_paths.to_a)
raise 'complete cat-stream diff drift' unless rebuilt_diff == sealed_diff
diff_text = sealed_diff.force_encoding(Encoding::UTF_8)
raise 'invalid diff UTF-8' unless diff_text.valid_encoding?
hunks = []
current_path = nil
current_hunk = nil
diff_text.lines(chomp: true).each do |line|
  if current_hunk
    if line.start_with?('\\ No newline at end of file')
      current_hunk[:lines] << line
      current_hunk[:positions] << [nil, nil]
      next
    elsif current_hunk[:old_remaining].positive? || current_hunk[:new_remaining].positive?
      old_position = nil
      new_position = nil
      case line[0]
      when ' '
        old_position = current_hunk[:old_line]
        new_position = current_hunk[:new_line]
        current_hunk[:old_remaining] -= 1
        current_hunk[:new_remaining] -= 1
        current_hunk[:old_line] += 1
        current_hunk[:new_line] += 1
      when '-'
        old_position = current_hunk[:old_line]
        current_hunk[:old_remaining] -= 1
        current_hunk[:old_line] += 1
      when '+'
        new_position = current_hunk[:new_line]
        current_hunk[:new_remaining] -= 1
        current_hunk[:new_line] += 1
      else
        raise "invalid hunk body line: #{line.inspect}"
      end
      raise 'negative hunk count' if current_hunk[:old_remaining].negative? || current_hunk[:new_remaining].negative?
      current_hunk[:lines] << line
      current_hunk[:positions] << [old_position, new_position]
      next
    else
      current_hunk = nil
    end
  end
  if (match = line.match(/\A\+\+\+ workspace\/(.+)\z/))
    current_path = match[1]
  elsif (match = line.match(/\A@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@/))
    raise 'hunk without path' unless current_path
    old_start = Integer(match[1], 10)
    old_count = match[2] ? Integer(match[2], 10) : 1
    new_start = Integer(match[3], 10)
    new_count = match[4] ? Integer(match[4], 10) : 1
    current_hunk = { path: current_path, header: line, lines: [], positions: [], old_line: old_start, new_line: new_start, old_remaining: old_count, new_remaining: new_count }
    hunks << current_hunk
  end
end
raise 'truncated final diff hunk' if current_hunk && (current_hunk[:old_remaining].positive? || current_hunk[:new_remaining].positive?)
raise 'no diff hunks' if hunks.empty?

find_candidate = lambda do |path, origin, kind, selector|
  matches = universe.select { |row| row['File'] == path && row['Origin'] == origin && row['Kind'] == kind && strict_decode(row['Selector_B64']) == selector }
  raise "candidate derivation mismatch: #{path}:#{origin}:#{kind}:#{selector}" unless matches.length == 1
  matches.first
end
separator = ->(line) { line.match?(/\A\|(?:\s*:?-{3,}:?\s*\|)+\z/) }
normative = /\b(?:must|only|cannot|requires?|forbidden|stop|block|never|unless)\b|不得|必须|只能|禁止|停止|阻断|不可|仅当/i
derived_ids = Set.new
expected_links = Set.new
hunks.each do |hunk|
  hunk_bytes = ([hunk[:header]] + hunk[:lines]).join("\n") + "\n"
  hunk_id = "HUNK-#{Digest::SHA256.hexdigest(hunk[:path].b + "\0" + hunk_bytes.b)}"
  nearest_method = { 'added' => nil, 'removed' => nil }
  positions = hunk.fetch(:positions)
  before_path = File.join(SNAPSHOT, 'preimage', hunk[:path])
  before_lines = File.file?(before_path) ? cat_bytes(before_path).lines(chomp: true) : []
  final_lines = cat_bytes(File.join(content_root, hunk[:path])).lines(chomp: true)
  generated = 0
  index = 0
  while index < hunk[:lines].length
    raw = hunk[:lines][index]
    unless raw.start_with?('+', '-')
      index += 1
      next
    end
    origin = raw.start_with?('+') ? 'added' : 'removed'
    text = raw[1..]
    if text.empty?
      index += 1
      next
    end
    if text.match?(/\A\#{1,6}\s+\S/)
      row = find_candidate.call(hunk[:path], origin, 'method', text)
      raise "method container drift: #{row['Candidate_ID']}" unless row['Container_ID'] == 'NONE'
      nearest_method[origin] = row['Candidate_ID']
      candidates = [row]
    else
      line_number = origin == 'added' ? positions.fetch(index)[1] : positions.fetch(index)[0]
      view_lines = origin == 'added' ? final_lines : before_lines
      table_header = text.start_with?('|') && text.end_with?('|') && line_number && separator.call(view_lines[line_number])
      if table_header
        table = find_candidate.call(hunk[:path], origin, 'table', text)
        raise "table container drift: #{table['Candidate_ID']}" unless table['Container_ID'] == (nearest_method[origin] || 'NONE')
        fields = text.sub(/\A\|/, '').sub(/\|\z/, '').split('|', -1).map(&:strip)
        candidates = [table] + fields.each_with_index.map do |field, field_index|
          child = find_candidate.call(hunk[:path], origin, 'field', JSON.generate([text, field_index, field]))
          raise "field container drift: #{child['Candidate_ID']}" unless child['Container_ID'] == table['Candidate_ID']
          child
        end
      elsif separator.call(text)
        candidates = []
      else
        kind = text.match?(normative) ? 'check' : 'term'
        row = find_candidate.call(hunk[:path], origin, kind, text)
        raise "line container drift: #{row['Candidate_ID']}" unless row['Container_ID'] == (nearest_method[origin] || 'NONE')
        candidates = [row]
      end
    end
    candidates.each do |candidate|
      derived_ids << candidate['Candidate_ID']
      expected_links << [hunk_id, candidate['Candidate_ID']]
      generated += 1
    end
    index += 1
  end
  raise "uncovered hunk: #{hunk_id}" if generated.zero?
end
actual_links = load_tsv(hunk_path, HUNK_HEADER).map { |row| [row['Hunk_ID'], row['Candidate_ID']] }.to_set
raise 'diff-hunk crosswalk drift' unless actual_links == expected_links

run_number = Integer(run_id.delete_prefix('run-'), 10)
prior_ids = Set.new
prior_decisions = {}
prior_history = +"Schema\tRun_ID\tTerminal_SHA256\tPackage_Kind\tPhase_Manifest_SHA256\tUniverse_SHA256\tLedger_SHA256\tUniverse_Authority\tDecision_Authority\n"
(1...run_number).each do |number|
  prior_id = format('run-%03d', number)
  prior_run = File.join(SNAPSHOT, 'task9', prior_id)
  terminal, terminal_sha = verify_prior_terminal(prior_run, prior_id)
  package_candidates = %w[published pending-history].map { |name| File.join(prior_run, '30-ablation', name) }.select { |path| File.exist?(path) || File.symlink?(path) }
  if package_candidates.empty?
    prior_history << ['task9-prior-history/v1', prior_id, terminal_sha, 'NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE'].join("\t") + "\n"
    next
  end
  raise "multiple prior packages: #{prior_run}" unless package_candidates.length == 1
  package = package_candidates.first
  package_kind = File.basename(package)
  phase_sha = verify_package(package)
  prior_validation = File.join(package, 'ablation-validation.txt')
  receipt = key_values(prior_validation, RECEIPT_KEYS)
  expected_status = package_kind == 'published' ? 'PUBLISHED' : 'PENDING_HISTORY'
  expected_applied = package_kind == 'published' ? 'REFLECTED' : 'PENDING'
  raise "prior receipt status drift: #{prior_id}" unless receipt['Schema'] == 'task9-ablation-validation/v1' &&
    receipt['Run_ID'] == prior_id && receipt['Package_Status'] == expected_status &&
    receipt['Universe_Valid'] == 'PASS' && receipt['Decisions_Valid'] == 'PASS' &&
    receipt['Applied_Status'] == expected_applied && receipt['Failure_Code'] == (package_kind == 'published' ? 'NONE' : 'ABLATION_PENDING')
  raise "prior history chain drift: #{prior_id}" unless
    read_regular(File.join(package, 'prior-history.tsv'), 0o400) == prior_history &&
    receipt['Prior_History_SHA256'] == Digest::SHA256.hexdigest(prior_history)
  expected_identity = "Schema\tController_Exception_ID\tIdentity_Fields_SHA256\n" +    "task9-candidate-identity/v1\tCAND-T2-CONTROLLER-ACTIVE-HANDOFF\t#{IDENTITY_FIELDS_SHA256}\n"
  raise "prior identity contract drift: #{prior_id}" unless read_regular(File.join(package, 'identity-contract.tsv'), 0o400) == expected_identity

  prior_universe_path = File.join(package, 'candidate-universe.tsv')
  prior_universe_sha = Digest::SHA256.hexdigest(read_regular(prior_universe_path, 0o400))
  prior_target_sha = Digest::SHA256.hexdigest(read_regular(File.join(prior_run, '20-final', 'targets-32-final.bin'), 0o400))
  raise "prior universe/target receipt drift: #{package}" unless
    receipt['Universe_SHA256'] == prior_universe_sha &&
    receipt['Target_Manifest_SHA256'] == prior_target_sha &&
    terminal['Candidate_Universe_SHA256'] == prior_universe_sha &&
    terminal['Target_Manifest_SHA256'] == prior_target_sha
  prior_universe = load_tsv(prior_universe_path, UNIVERSE_HEADER)
  universe_authority = terminal['Reason_Code'] == 'ABLATION_REVIEW_BLOCKED' ? 'REJECTED' : 'ACCEPTED'
  if universe_authority == 'ACCEPTED'
    prior_universe.each do |prior|
      current = by_id.fetch(prior['Candidate_ID']) { raise "prior candidate disappeared: #{prior['Candidate_ID']}" }
      raise "prior identity changed: #{prior['Candidate_ID']}" unless IDENTITY_KEYS.all? { |key| current[key] == prior[key] }
      raise "first-seen changed: #{prior['Candidate_ID']}" unless current['First_seen_run'] == prior['First_seen_run']
      prior_ids << prior['Candidate_ID']
    end
  end

  prior_ledger_path = File.join(package, 'ablation-ledger.tsv')
  prior_ledger_sha = Digest::SHA256.hexdigest(read_regular(prior_ledger_path, 0o400))
  raise "prior ledger receipt drift: #{package}" unless receipt['Ledger_SHA256'] == prior_ledger_sha && terminal['Ablation_Ledger_SHA256'] == prior_ledger_sha
  prior_ledger = load_tsv(prior_ledger_path, LEDGER_HEADER)
  prior_candidate_ids = prior_universe.map { |row| row['Candidate_ID'] }
  raise "prior ledger domain/order drift: #{prior_id}" unless prior_ledger.map { |row| row['Candidate_ID'] } == prior_candidate_ids
  prior_ledger_by_id = prior_ledger.to_h { |row| [row['Candidate_ID'], row] }
  prior_candidate_by_id = prior_universe.to_h { |row| [row['Candidate_ID'], row] }
  resolve_prior_merge = nil
  resolve_prior_merge = lambda do |candidate_id, active|
    raise "prior merge cycle: #{prior_id}:#{candidate_id}" if active.include?(candidate_id)
    entry = prior_ledger_by_id.fetch(candidate_id)
    case entry['Decision']
    when 'retain'
      candidate_id
    when 'merge'
      target_id = entry['Merge_Target_ID']
      raise "prior merge self-reference: #{candidate_id}" if target_id == candidate_id
      raise "prior merge target missing: #{target_id}" unless prior_ledger_by_id.key?(target_id)
      resolve_prior_merge.call(target_id, active | [candidate_id])
    when 'remove'
      raise "prior merge chain ends at remove: #{candidate_id}"
    else
      raise "invalid prior decision: #{candidate_id}"
    end
  end
  pending_count = 0
  prior_ledger.each do |entry|
    candidate_id = entry['Candidate_ID']
    raise "invalid prior decision: #{candidate_id}" unless %w[retain remove merge].include?(entry['Decision'])
    expected_previous = prior_decisions.fetch(candidate_id, 'NONE')
    raise "prior Previous_Decision drift: #{candidate_id}" unless entry['Previous_Decision'] == expected_previous
    changed = expected_previous != 'NONE' && expected_previous != entry['Decision']
    raise "prior decision-change reason drift: #{candidate_id}" unless changed == (entry['Decision_Change_Reason'] != 'NONE')
    present = prior_candidate_by_id.fetch(candidate_id)['Present_in_final'] == 'true'
    reflected = case entry['Decision']
                when 'retain'
                  entry['Merge_Target_ID'] == 'NONE' && present
                when 'remove'
                  entry['Merge_Target_ID'] == 'NONE' && !present
                when 'merge'
                  final_target = resolve_prior_merge.call(candidate_id, Set.new)
                  !present && prior_candidate_by_id.fetch(final_target)['Present_in_final'] == 'true'
                end
    raise "prior Applied_State drift: #{candidate_id}" unless entry['Applied_State'] == (reflected ? 'reflected' : 'pending')
    pending_count += 1 unless reflected
  end
  raise "prior pending count drift: #{prior_id}" unless receipt['Pending_Count'] == pending_count.to_s
  if package_kind == 'pending-history'
    raise "prior pending terminal drift: #{prior_id}" unless pending_count.positive? &&
      terminal['Reason_Code'] == 'ABLATION_PENDING' && terminal['Required_Action'] == 'REWORK_CONTENT' &&
      terminal['Candidate_ID'] == receipt['First_Pending_Candidate'] && terminal['Owning_Task'] == receipt['First_Pending_Owner']
  else
    raise "prior published package contains pending decisions: #{prior_id}" unless pending_count.zero?
  end
  decision_authority = universe_authority == 'REJECTED' ? 'REJECTED' : 'ACCEPTED'
  prior_ledger.each { |row| prior_decisions[row['Candidate_ID']] = row['Decision'] } if decision_authority == 'ACCEPTED'
  prior_history << ['task9-prior-history/v1', prior_id, terminal_sha, package_kind, phase_sha, prior_universe_sha, prior_ledger_sha, universe_authority, decision_authority].join("\t") + "\n"
end
controller_id = 'CAND-T2-CONTROLLER-ACTIVE-HANDOFF'
raise 'candidate universe union drift' unless by_id.keys.to_set == (derived_ids | prior_ids | [controller_id])

crosswalk = parse_tsv(crosswalk_bytes, 'candidate-crosswalk', CROSSWALK_HEADER)
dialogue_ids = universe.select { |row| row['Role'] == 'dialogue' }.map { |row| row['Candidate_ID'] }
raise 'dialogue crosswalk source-set/order drift' unless crosswalk.map { |row| row['Source_Candidate_ID'] } == dialogue_ids
crosswalk.each do |row|
  source = by_id.fetch(row['Source_Candidate_ID'])
  target = by_id.fetch(row['Target_Candidate_ID']) { raise "unresolved crosswalk target: #{row['Target_Candidate_ID']}" }
  expected_path = source['File'].sub('/prompts_ask/', '/prompts/')
  raise "crosswalk relation drift: #{source['Candidate_ID']}" unless row['Relation'] == 'mirrors'
  raise "crosswalk target drift: #{source['Candidate_ID']}" unless target['Role'] == 'canonical' && target['File'] == expected_path && target['Kind'] == source['Kind']
  raise "empty crosswalk rationale: #{source['Candidate_ID']}" if %w[NONE UNRESOLVED].include?(row['Rationale'])
end

ledger = parse_tsv(ledger_bytes, 'ablation-ledger', LEDGER_HEADER)
raise 'ledger candidate-set/order drift' unless ledger.map { |row| row['Candidate_ID'] } == ids
ledger_by_id = ledger.to_h { |row| [row['Candidate_ID'], row] }
resolve_merge = nil
resolve_merge = lambda do |candidate_id, active|
  raise "merge cycle: #{candidate_id}" if active.include?(candidate_id)
  entry = ledger_by_id.fetch(candidate_id)
  case entry['Decision']
  when 'retain'
    candidate_id
  when 'merge'
    target_id = entry['Merge_Target_ID']
    raise "merge self-reference: #{candidate_id}" if target_id == candidate_id
    raise "missing merge target: #{target_id}" unless ledger_by_id.key?(target_id)
    resolve_merge.call(target_id, active | [candidate_id])
  when 'remove'
    raise "merge chain ends at remove: #{candidate_id}"
  else
    raise "invalid merge decision: #{candidate_id}"
  end
end
pending = []
ledger.each do |entry|
  candidate = by_id.fetch(entry['Candidate_ID'])
  raise "bad decision: #{entry['Candidate_ID']}" unless %w[retain remove merge].include?(entry['Decision'])
  previous = prior_decisions.fetch(entry['Candidate_ID'], 'NONE')
  raise "previous decision drift: #{entry['Candidate_ID']}" unless entry['Previous_Decision'] == previous
  changed = previous != 'NONE' && previous != entry['Decision']
  raise "decision-change reason drift: #{entry['Candidate_ID']}" unless changed == (entry['Decision_Change_Reason'] != 'NONE')
  generic_effects = [
    "#{entry['Decision']} #{candidate['Kind']} at #{candidate['File']}",
    'preserve explicit evidence boundary or document its removal',
    'preserve applicable Gate/R3/privacy boundary or document none',
    'preserve downstream contract or document none'
  ]
  actual_effects = %w[Decision_Effect Evidence_Effect Safety_Effect Downstream_Effect].map { |field| entry[field] }
  raise "generic/empty effect analysis: #{entry['Candidate_ID']}" if actual_effects.any? { |value| value == 'NONE' || generic_effects.include?(value) }
  refs = entry['Verification_Refs'].split(',').map(&:strip)
  raise "verification ref drift: #{entry['Candidate_ID']}" unless refs.include?("ORACLE-#{entry['Candidate_ID']}") && refs.all? { |ref| oracle_ids.include?(ref) }
  present = candidate['Present_in_final'] == 'true'
  reflected = case entry['Decision']
              when 'retain'
                raise "retain merge-target drift: #{entry['Candidate_ID']}" unless entry['Merge_Target_ID'] == 'NONE'
                present
              when 'remove'
                raise "remove merge-target drift: #{entry['Candidate_ID']}" unless entry['Merge_Target_ID'] == 'NONE'
                !present
              when 'merge'
                final_target = resolve_merge.call(entry['Candidate_ID'], Set.new)
                raise "merge source still present: #{entry['Candidate_ID']}" if present
                raise "merge final target absent: #{final_target}" unless by_id.fetch(final_target)['Present_in_final'] == 'true'
                raise "missing final-target oracle: #{entry['Candidate_ID']}" unless refs.include?("ORACLE-#{final_target}")
                true
              end
  expected_state = reflected ? 'reflected' : 'pending'
  raise "applied state drift: #{entry['Candidate_ID']}" unless entry['Applied_State'] == expected_state
  pending << entry if expected_state == 'pending'
end

inventory_line = File.readlines(File.join(run_root, '20-final', 'inventory.txt'), chomp: true).find { |line| line.start_with?('TARGET_INTEGRITY=') }
raise 'missing inventory summary' unless inventory_line
controller = ledger_by_id.fetch(controller_id)
if inventory_line.include?('controller_adapter=ablated')
  raise 'controller branch/ledger drift' unless controller['Decision'] == 'remove' && by_id.fetch(controller_id)['Present_in_final'] == 'false'
else
  raise 'unknown controller branch' unless inventory_line.include?('controller_adapter=retained-or-merged')
  raise 'controller branch/ledger drift' unless %w[retain merge].include?(controller['Decision'])
end

stability_hashes.each do |path, sha|
  label = mode == 'publish' ? 'validation/publication' : 'check-time'
  raise "#{label} drift: #{path}" unless Digest::SHA256.file(path).hexdigest == sha
end

first_pending = pending.first
package_status = pending.empty? ? 'PUBLISHED' : 'PENDING_HISTORY'
applied_status = pending.empty? ? 'REFLECTED' : 'PENDING'
failure_code = pending.empty? ? 'NONE' : 'ABLATION_PENDING'
destination = pending.empty? ? 'published' : 'pending-history'
universe_bytes = read_regular(universe_path, 0o400)
oracle_bytes = read_regular(oracle_path, 0o400)
hunk_bytes = read_regular(hunk_path, 0o400)
identity_contract = "Schema\tController_Exception_ID\tIdentity_Fields_SHA256\n" +  "task9-candidate-identity/v1\tCAND-T2-CONTROLLER-ACTIVE-HANDOFF\t#{IDENTITY_FIELDS_SHA256}\n"
details = JSON.generate(
  'Artifact_Path' => File.join(root, destination, 'phase-manifest.tsv'),
  'Identity_Fields_SHA256' => IDENTITY_FIELDS_SHA256,
  'Candidate_Count' => ids.length.to_s,
  'Diff_Hunk_Count' => hunks.length.to_s
) + "\n"
validation_values = [
  'task9-ablation-validation/v1', run_id, package_status, 'PASS', 'PASS', applied_status,
  Digest::SHA256.hexdigest(universe_bytes), Digest::SHA256.hexdigest(oracle_bytes), Digest::SHA256.hexdigest(hunk_bytes),
  Digest::SHA256.hexdigest(crosswalk_bytes), Digest::SHA256.hexdigest(ledger_bytes),
  Digest::SHA256.hexdigest(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400)),
  Digest::SHA256.hexdigest(read_regular(File.join(run_root, '20-final', 'added-content.diff'), 0o400)),
  Digest::SHA256.hexdigest(prior_history), pending.length.to_s,
  first_pending ? first_pending['Candidate_ID'] : 'NONE',
  first_pending ? by_id.fetch(first_pending['Candidate_ID'])['Owning_task'] : 'NONE',
  failure_code, Base64.strict_encode64(details)
]
validation_bytes = RECEIPT_KEYS.zip(validation_values).map { |key, value| "#{key}=#{value}\n" }.join

if mode == 'publish'
  files = {
    'candidate-universe.tsv' => universe_bytes,
    'content-oracles.tsv' => oracle_bytes,
    'diff-hunk-crosswalk.tsv' => hunk_bytes,
    'candidate-crosswalk.tsv' => crosswalk_bytes,
    'ablation-ledger.tsv' => ledger_bytes,
    'identity-contract.tsv' => identity_contract,
    'prior-history.tsv' => prior_history,
    'ablation-validation.txt' => validation_bytes
  }
  phase_sha = publish_package(root, destination, files)
else
  raise 'checked package kind/state drift' unless package_kind == destination
  raise 'checked identity contract drift' unless read_regular(File.join(package_root, 'identity-contract.tsv'), 0o400) == identity_contract
  raise 'checked prior history drift' unless read_regular(File.join(package_root, 'prior-history.tsv'), 0o400) == prior_history
  raise 'checked validation receipt drift' unless read_regular(File.join(package_root, 'ablation-validation.txt'), 0o400) == validation_bytes
  phase_sha = verified_phase_sha
end

puts "ABLATION_PACKAGE=#{package_status} phase_sha256=#{phase_sha}"
puts "ABLATION_ORACLE=PASS run=#{run_id} pending=#{pending.length}"
if mode == 'seal-pending'
  receipt = key_values(File.join(package_root, 'ablation-validation.txt'), RECEIPT_KEYS)
  raise 'pending seal binding drift' unless package_kind == 'pending-history' &&
    receipt['Package_Status'] == 'PENDING_HISTORY' && receipt['Applied_Status'] == 'PENDING' &&
    Integer(receipt['Pending_Count'], 10).positive?
  $stdout.flush
  exec(
    '/usr/bin/ruby', File.join(SNAPSHOT, 'seal-task9-generation.rb'),
    run_id, 'INVALIDATED', 'ABLATION_PENDING', 'REWORK_CONTENT',
    receipt.fetch('First_Pending_Owner'), receipt.fetch('First_Pending_Candidate'),
    File.join(package_root, 'phase-manifest.tsv'), 'NONE',
    receipt.fetch('Target_Manifest_SHA256'), receipt.fetch('Universe_SHA256'), receipt.fetch('Ledger_SHA256')
  )
end
exit(pending.empty? ? 0 : 3)
~~~

The four effect fields require human, candidate-specific judgment; the validator can reject empty/generated boilerplate but the independent ablation reviewer remains responsible for semantic quality. Run the state machine below. It uses an existing package plus a fresh read-only `check` as the only recovery predicate after an atomic rename; it never republishes or edits a package:

~~~zsh
set -euo pipefail
[[ "$TASK9_RUN_ID" == run-[0-9][0-9][0-9] ]]
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
ablation_root="$run_root/30-ablation"
validator="$ablation_root/validate-ablation.rb"
/usr/bin/ruby -c "$validator"
/bin/chmod 400 "$validator"

package_count=0
for name in published pending-history; do
  [[ -e "$ablation_root/$name" || -L "$ablation_root/$name" ]] && (( package_count += 1 ))
done
attempt_path="$ablation_root/validator-publication-attempt.txt"
if (( package_count == 0 )) && [[ ! -e "$attempt_path" && ! -L "$attempt_path" ]]; then
  set +e
  publish_output=$(/usr/bin/ruby "$validator" "$run_root" publish 2>&1)
  publish_exit=$?
  set -e
  VALIDATOR_OUTPUT="$publish_output" /usr/bin/ruby - "$attempt_path" <<'RUBY'
path = ARGV.fetch(0)
File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
  file.write(ENV.fetch('VALIDATOR_OUTPUT').b + "\n")
  file.flush
  file.fsync
end
RUBY
  print -r -- "$publish_output"
else
  publish_exit=125
fi

set +e
check_output=$(/usr/bin/ruby "$validator" "$run_root" check 2>&1)
check_exit=$?
set -e
VALIDATOR_OUTPUT="$check_output" /usr/bin/ruby - "$ablation_root/validator-output.txt" <<'RUBY'
path = ARGV.fetch(0)
bytes = ENV.fetch('VALIDATOR_OUTPUT').b + "\n"
begin
  File.open(path, File::WRONLY | File::CREAT | File::EXCL, 0o400) do |file|
    file.write(bytes)
    file.flush
    file.fsync
  end
rescue Errno::EEXIST
  stat = File.lstat(path)
  raise 'unsafe validator output' unless stat.file? && !stat.symlink? && (stat.mode & 0o777) == 0o400
  raise 'validator output conflict' unless File.binread(path) == bytes
end
RUBY
print -r -- "$check_output"

case "$check_exit" in
  0)
    [[ -d "$ablation_root/published" && ! -L "$ablation_root/published" ]]
    /usr/bin/ruby - "$ablation_root" <<'RUBY'
require 'find'
root = ARGV.fetch(0)
expected_root = %w[
  ablation-ledger.draft.tsv build-ablation-universe.rb candidate-crosswalk.draft.tsv
  candidate-universe.tsv content-oracles.tsv diff-hunk-crosswalk.tsv published
  validate-ablation.rb validator-output.txt validator-publication-attempt.txt
].sort_by(&:b)
raise 'ablation root file-set drift' unless Dir.children(root).sort_by(&:b) == expected_root
paths = []
Find.find(root) do |path|
  stat = File.lstat(path)
  raise "symlink in ablation phase: #{path}" if stat.symlink?
  raise "special node in ablation phase: #{path}" unless stat.directory? || stat.file?
  paths << path
end
paths.sort_by { |path| -path.count(File::SEPARATOR) }.each do |path|
  stat = File.lstat(path)
  File.chmod(stat.directory? ? 0o500 : 0o400, path)
end
Find.find(root) do |path|
  stat = File.lstat(path)
  raise "ablation post-freeze symlink/special: #{path}" if stat.symlink? || (!stat.directory? && !stat.file?)
  raise "ablation post-freeze mode drift: #{path}" unless (stat.mode & 0o777) == (stat.directory? ? 0o500 : 0o400)
end
RUBY
    set +e
    post_freeze_output=$(/usr/bin/ruby "$validator" "$run_root" check 2>&1)
    post_freeze_exit=$?
    set -e
    [[ $post_freeze_exit -eq 0 && "$post_freeze_output" == "$check_output" ]] || {
      print -u2 'ablation package changed across freeze'
      exit 88
    }
    print -r -- "TASK9_ABLATION=PASS run=$TASK9_RUN_ID"
    ;;
  3)
    [[ -d "$ablation_root/pending-history" && ! -L "$ablation_root/pending-history" ]]
    /usr/bin/ruby "$validator" "$run_root" seal-pending
    exit 86
    ;;
  *)
    package_count=0
    for name in published pending-history; do
      [[ -e "$ablation_root/$name" || -L "$ablation_root/$name" ]] && (( package_count += 1 ))
    done
    if (( package_count > 0 )); then
      failure_reason=ABLATION_PACKAGE_POISONED
      failure_action=STOP
    else
      failure_reason=ABLATION_PACKAGE_INVALID
      failure_action=REBUILD_EVIDENCE
    fi
    /usr/bin/ruby "$snapshot_root/seal-task9-generation.rb" "$TASK9_RUN_ID" INVALIDATED \
      "$failure_reason" "$failure_action" NONE NONE "$ablation_root/validator-output.txt" NONE NONE NONE NONE
    (( publish_exit == 0 )) && publish_exit=87
    exit "$publish_exit"
    ;;
esac
~~~

Expected success is `ABLATION_PACKAGE=PUBLISHED`, `pending=0` and `TASK9_ABLATION=PASS`. The successful branch checks the exact phase-root set, freezes every file to `0400` and directory to `0500`, freshly verifies every node/mode, then reruns `check` and requires byte-identical output before PASS. A valid package with pending decisions is atomically published under `pending-history/`, rechecked from package bytes, bound to real target/universe/ledger hashes by the Ruby `seal-pending` path, and then terminates with `REWORK_CONTENT`. A successful package is atomically published under `published/`; only that directory is completion-eligible. If no package exists after validation failure, the generation terminates with `REBUILD_EVIDENCE`; an existing package that fails the independent check is poisoned and forces `STOP`, so it can never be inherited. Drafts are frozen through their open file descriptors and are never edited after a validation attempt.


- [ ] **Step 5: Freeze one canonical review input and one shared read-only oracle**

Use `apply_patch` to create `review-contract.json` and `task9-review-tools.rb` at the fully expanded current-run path under `40-review-input/`. The contract is fixed to exactly three review roles:

~~~json
{
  "schema": "task9-review-contract/v1",
  "oracle_id": "TASK9_REVIEW_ORACLE_V1",
  "roles": {
    "spec": {
      "oracle_receipt": "spec-oracle.tsv",
      "report": "spec-review.json",
      "scope": [
        "approved-design projection and trigger ownership",
        "entity schemas, legal edges, cardinality and lifecycle",
        "canonical/dialogue parity and handoff completeness"
      ]
    },
    "safety": {
      "oracle_receipt": "safety-oracle.tsv",
      "report": "safety-review.json",
      "scope": [
        "G0/G3/G4/G5/G6 and R3 non-escalation",
        "privacy, production reads, external actions and write scope",
        "Decision authority remains human or existing Gate owned"
      ]
    },
    "ablation": {
      "oracle_receipt": "ablation-oracle.tsv",
      "report": "ablation-review.json",
      "scope": [
        "candidate, hunk, crosswalk and ledger completeness",
        "retain/remove/merge has independent decision or evidence value",
        "duplicate controllers and ceremonial content are removed"
      ]
    }
  }
}
~~~

The complete helper is:

~~~ruby
#!/usr/bin/ruby
require 'base64'
require 'digest'
require 'find'
require 'json'
require 'open3'
require 'set'
require 'tmpdir'

WORKSPACE = '/Users/lute/Project/vibecoding_config'
SNAPSHOT = '/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
ORACLE_ID = 'TASK9_REVIEW_ORACLE_V1'
ROLES = %w[spec safety ablation].freeze
ROLE_FILES = {
  'spec' => ['spec-oracle.tsv', 'spec-review.json'],
  'safety' => ['safety-oracle.tsv', 'safety-review.json'],
  'ablation' => ['ablation-oracle.tsv', 'ablation-review.json']
}.freeze
ROLE_SCOPES = {
  'spec' => [
    'approved-design projection and trigger ownership',
    'entity schemas, legal edges, cardinality and lifecycle',
    'canonical/dialogue parity and handoff completeness'
  ],
  'safety' => [
    'G0/G3/G4/G5/G6 and R3 non-escalation',
    'privacy, production reads, external actions and write scope',
    'Decision authority remains human or existing Gate owned'
  ],
  'ablation' => [
    'candidate, hunk, crosswalk and ledger completeness',
    'retain/remove/merge has independent decision or evidence value',
    'duplicate controllers and ceremonial content are removed'
  ]
}.freeze
INPUT_HEADER = %w[Schema Input_ID Kind Canonical_Path Bytes SHA256].freeze
IDENTITY_HEADER = %w[
  Schema Run_ID Coordinator_ID Review_Input_Path Review_Input_SHA256 Input_Count
  Target_Count Target_Manifest_SHA256 Candidate_Universe_SHA256 Ablation_Ledger_SHA256
].freeze
ORACLE_RECEIPT_HEADER = %w[
  Schema Run_ID Review_Kind Reviewer_ID Reviewer_Instance_ID Oracle_ID Review_Input_Path
  Review_Input_SHA256 Exit_Status Stdout_B64 Stdout_SHA256 Stderr_Bytes
].freeze
REVIEW_INDEX_HEADER = %w[
  Review_Kind Report_Path Report_SHA256 Oracle_Receipt_Path Oracle_Receipt_SHA256
  Reviewer_ID Reviewer_Instance_ID Critical Important Minor Verdict
].freeze
FINDING_KEYS = %w[
  finding_id severity requirement_ref owning_task candidate_id artifact_path line
  required_action summary evidence minimal_fix
].freeze
REVIEW_KEYS = %w[
  schema run_id review_kind reviewer_id reviewer_instance_id review_input_path
  review_input_sha256 oracle_id oracle_receipt_path oracle_receipt_sha256
  verdict counts summary findings
].freeze
CLOSEOUT_HEADER = %w[
  Schema Run_ID Review_Input_Path Review_Input_SHA256 Report_Count Review_Index_SHA256
  Distinct_Reviewer_ID_Count Distinct_Reviewer_Instance_Count Critical_Count
  Important_Count Minor_Count Oracle_ID Oracle_Output_SHA256
  Target_Manifest_SHA256 Protected_Manifest_SHA256 Zip_Manifest_SHA256
  Candidate_Universe_SHA256 Ablation_Ledger_SHA256 Completion_Eligible
].freeze
TOKEN_HEADER = %w[
  Schema Run_ID Review_Input_SHA256 Target_Manifest_SHA256 Candidate_Universe_SHA256
  Ablation_Ledger_SHA256 Report_Count Review_Index_SHA256 Distinct_Reviewer_ID_Count
  Distinct_Reviewer_Instance_Count Critical_Count Important_Count Closeout_SHA256 Eligible
].freeze
READY_HEADER = %w[
  Schema Run_ID Review_Input_SHA256 Closeout_SHA256 Oracle_ID Oracle_Output_SHA256 Eligible
].freeze
ROUTING_HEADER = %w[
  Schema Run_ID Reason_Code Required_Action Owning_Task Candidate_ID Artifact_Path Blocking_Findings_B64
].freeze

def read_regular(path, required_mode = nil)
  before = File.lstat(path)
  raise "unsafe regular file: #{path}" unless before.file? && !before.symlink? && before.nlink == 1
  raise "file mode drift: #{path}" if required_mode && (before.mode & 0o777) != required_mode
  flags = File::RDONLY
  flags |= File::NOFOLLOW if File.const_defined?(:NOFOLLOW)
  File.open(path, flags) do |file|
    opened = file.stat
    raise "opened inode drift: #{path}" unless [before.dev, before.ino] == [opened.dev, opened.ino]
    bytes = file.read.b
    after = File.lstat(path)
    raise "pathname replaced while reading: #{path}" unless [opened.dev, opened.ino] == [after.dev, after.ino]
    bytes
  end
end

def write_exclusive(path, bytes, mode = 0o400)
  File.open(path, File::WRONLY | File::CREAT | File::EXCL, mode) do |file|
    file.write(bytes)
    file.flush
    file.fsync
  end
end

def parse_tsv_bytes(bytes, expected_header, label)
  text = bytes.dup.force_encoding(Encoding::UTF_8)
  raise "invalid UTF-8: #{label}" unless text.valid_encoding? && text.end_with?("\n")
  lines = text.lines(chomp: true)
  raise "header drift: #{label}" unless lines.shift&.split("\t", -1) == expected_header
  lines.map.with_index(2) do |line, line_number|
    fields = line.split("\t", -1)
    raise "field-count drift: #{label}:#{line_number}" unless fields.length == expected_header.length
    Hash[expected_header.zip(fields)]
  end
end

def one_tsv(path, header, mode = 0o400)
  rows = parse_tsv_bytes(read_regular(path, mode), header, path)
  raise "row-count drift: #{path}" unless rows.length == 1
  rows.first
end

def sha(bytes)
  Digest::SHA256.hexdigest(bytes)
end

def safe_identity(value, label)
  raise "invalid #{label}" unless value && value.match?(/\A[A-Za-z0-9._:\/-]+\z/)
  value
end

def verify_helper_manifest
  expected = %w[
    capture-and-normalize.zsh four-value-manifest.rb guard-workspace.zsh
    normalize-targets.zsh rollback-target.zsh seal-task9-generation.rb verify-chain.rb
  ]
  path = File.join(SNAPSHOT, 'helper-manifest.tsv')
  lines = read_regular(path, 0o400).lines(chomp: true)
  raise 'helper manifest header drift' unless lines.shift == "Schema\tName\tBytes\tSHA256\tMode"
  rows = lines.map { |line| line.split("\t", -1) }
  raise 'helper manifest set/order drift' unless rows.map { |row| row[1] } == expected
  rows.each do |schema, name, bytes, hash, mode|
    helper_path = File.join(SNAPSHOT, name)
    body = read_regular(helper_path)
    stat = File.lstat(helper_path)
    raise "helper manifest binding drift: #{name}" unless schema == 'task0-helper-manifest/v1' &&
      (stat.mode & 0o777).to_s(8) == mode && body.bytesize.to_s == bytes && sha(body) == hash
  end
end

def published_root(run_root)
  root = File.join(run_root, '30-ablation')
  published = File.join(root, 'published')
  pending = File.join(root, 'pending-history')
  raise 'published ablation package missing' unless File.directory?(published) && !File.symlink?(published)
  raise 'pending package coexists with published package' if File.exist?(pending) || File.symlink?(pending)
  published
end

def input_identity(run_root)
  path = File.join(run_root, '40-review-input', 'review-input.identity.tsv')
  row = one_tsv(path, IDENTITY_HEADER)
  input_path = File.join(run_root, '40-review-input', 'review-input.tsv')
  package = published_root(run_root)
  raise 'review identity schema/run drift' unless row['Schema'] == 'task9-review-input-identity/v1' && row['Run_ID'] == File.basename(run_root)
  safe_identity(row['Coordinator_ID'], 'coordinator ID')
  raise 'review identity path drift' unless row['Review_Input_Path'] == input_path
  raise 'review identity input hash drift' unless row['Review_Input_SHA256'] == sha(read_regular(input_path, 0o400))
  raise 'review identity input count drift' unless row['Input_Count'] == input_rows(run_root).length.to_s
  raise 'review identity target count drift' unless row['Target_Count'] == '32'
  raise 'review identity target hash drift' unless row['Target_Manifest_SHA256'] == sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400))
  raise 'review identity universe hash drift' unless row['Candidate_Universe_SHA256'] == sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400))
  raise 'review identity ledger hash drift' unless row['Ablation_Ledger_SHA256'] == sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
  row
end

def contract!(run_root)
  path = File.join(run_root, '40-review-input', 'review-contract.json')
  contract = strict_json(read_regular(path, 0o400), path)
  raise 'review contract top-level drift' unless contract.keys.sort == %w[oracle_id roles schema] && contract['schema'] == 'task9-review-contract/v1' && contract['oracle_id'] == ORACLE_ID
  raise 'review contract roles drift' unless contract.fetch('roles').keys == ROLES
  ROLES.each do |role|
    entry = contract.fetch('roles').fetch(role)
    raise "review contract entry keys drift: #{role}" unless entry.is_a?(Hash) && entry.keys.sort == %w[oracle_receipt report scope]
    raise "review contract file drift: #{role}" unless entry['oracle_receipt'] == ROLE_FILES.fetch(role)[0] && entry['report'] == ROLE_FILES.fetch(role)[1]
    raise "review contract scope drift: #{role}" unless entry['scope'] == ROLE_SCOPES.fetch(role)
  end
  contract
end

def collect_regular_tree(root)
  files = []
  Find.find(root) do |path|
    stat = File.lstat(path)
    raise "symlink in evidence tree: #{path}" if stat.symlink?
    if stat.directory?
      next
    elsif stat.file?
      raise "writable evidence file: #{path}" unless (stat.mode & 0o222).zero?
      files << path
    else
      raise "special evidence node: #{path}"
    end
  end
  files
end

def validate_manifests_set(run_root)
  set_path = File.join(run_root, '10-input', 'manifests-set.tsv')
  header = %w[Schema Relative_Path Bytes SHA256 Mode]
  rows = parse_tsv_bytes(read_regular(set_path, 0o400), header, set_path)
  root = File.join(SNAPSHOT, 'manifests')
  actual = collect_regular_tree(root).map do |path|
    bytes = read_regular(path)
    {
      'Schema' => 'task9-manifests-set/v1',
      'Relative_Path' => path.delete_prefix(root + File::SEPARATOR),
      'Bytes' => bytes.bytesize.to_s,
      'SHA256' => sha(bytes),
      'Mode' => (File.lstat(path).mode & 0o777).to_s(8)
    }
  end.sort_by { |row| row['Relative_Path'].b }
  raise 'manifest directory set/content drift' unless rows == actual
end

def expected_input_records(run_root)
  validate_manifests_set(run_root)
  target_manifest = File.join(run_root, '20-final', 'targets-32-final.tsv')
  target_rows = read_regular(target_manifest, 0o400).lines(chomp: true).map { |line| line.split("\t", -1) }
  raise 'target manifest drift while constructing review input' unless target_rows.length == 32 &&
    target_rows.all? { |row| row.length == 6 } && target_rows.map(&:first).uniq.length == 32
  records = target_rows.sort_by { |row| row[0].b }.each_with_index.map do |row, index|
    relative = row[0]
    path = File.realpath(File.join(run_root, '20-final', 'content', relative))
    bytes = read_regular(path, 0o400)
    raise "target/frozen review drift: #{relative}" unless [bytes.bytesize.to_s, sha(bytes)] == row[3, 2]
    ['task9-review-input/v1', format('T%03d:%s', index + 1, relative), 'target', path, bytes.bytesize.to_s, sha(bytes)]
  end
  evidence = []
  %w[
    four-value-manifest.rb guard-workspace.zsh normalize-targets.zsh
    capture-and-normalize.zsh rollback-target.zsh seal-task9-generation.rb verify-chain.rb
    helper-manifest.tsv
  ].each { |name| evidence << File.join(SNAPSHOT, name) }
  evidence.concat(collect_regular_tree(File.join(SNAPSHOT, 'baseline')))
  evidence.concat(collect_regular_tree(File.join(SNAPSHOT, 'manifests')))
  %w[00-meta 10-input].each { |name| evidence.concat(collect_regular_tree(File.join(run_root, name))) }
  final_root = File.join(run_root, '20-final')
  Find.find(final_root) do |path|
    next if path == final_root || path.start_with?(File.join(final_root, 'content') + File::SEPARATOR)
    stat = File.lstat(path)
    raise "unsafe final evidence node: #{path}" if stat.symlink? || (!stat.directory? && !stat.file?)
    evidence << path if stat.file?
  end
  evidence.concat(collect_regular_tree(File.join(run_root, '30-ablation')))
  evidence << File.join(run_root, '40-review-input', 'review-contract.json')
  evidence << File.join(run_root, '40-review-input', 'task9-review-tools.rb')
  evidence = evidence.map { |path| File.realpath(path) }.uniq.sort_by(&:b)
  evidence.each_with_index do |path, index|
    bytes = read_regular(path)
    records << ['task9-review-input/v1', format('E%04d:%s', index + 1, path.delete_prefix(SNAPSHOT + File::SEPARATOR)), 'evidence', path, bytes.bytesize.to_s, sha(bytes)]
  end
  records.sort_by { |row| row[1].b }
end

def input_rows(run_root)
  path = File.join(run_root, '40-review-input', 'review-input.tsv')
  actual = parse_tsv_bytes(read_regular(path, 0o400), INPUT_HEADER, path)
  expected = expected_input_records(run_root).map { |row| Hash[INPUT_HEADER.zip(row)] }
  raise 'review input exact closure drift' unless actual == expected
  actual
end

def build_input(run_root, coordinator_id)
  safe_identity(coordinator_id, 'coordinator ID')
  verify_helper_manifest
  contract!(run_root)
  package = published_root(run_root)
  records = expected_input_records(run_root)
  raise 'review input canonical collision' unless records.map { |row| row[3] }.uniq.length == records.length
  input_bytes = INPUT_HEADER.join("\t") + "\n" + records.map { |row| row.join("\t") + "\n" }.join
  input_path = File.join(run_root, '40-review-input', 'review-input.tsv')
  write_exclusive(input_path, input_bytes)

  identity_values = [
    'task9-review-input-identity/v1', File.basename(run_root), coordinator_id, input_path,
    sha(input_bytes), records.length.to_s, '32',
    sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400)),
    sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400)),
    sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
  ]
  identity_bytes = IDENTITY_HEADER.join("\t") + "\n" + identity_values.join("\t") + "\n"
  write_exclusive(File.join(run_root, '40-review-input', 'review-input.identity.tsv'), identity_bytes)
  review_root = File.join(run_root, '40-review-input')
  expected = %w[review-contract.json review-input.identity.tsv review-input.tsv task9-review-tools.rb].sort_by(&:b)
  raise 'review-input phase file-set drift' unless Dir.children(review_root).sort_by(&:b) == expected
  File.open(review_root, File::RDONLY) { |directory| directory.fsync }
  expected.each { |name| File.chmod(0o400, File.join(review_root, name)) }
  File.chmod(0o500, review_root)
  raise 'review-input phase root mode drift' unless (File.lstat(review_root).mode & 0o777) == 0o500
  expected.each do |name|
    raise "review-input phase file mode drift: #{name}" unless (File.lstat(File.join(review_root, name)).mode & 0o777) == 0o400
  end
  puts "TASK9_REVIEW_INPUT=SEALED run=#{File.basename(run_root)} inputs=#{records.length} sha256=#{sha(input_bytes)}"
end


def command!(*argv)
  stdout, stderr, status = Open3.capture3(*argv)
  raise "command failed: #{argv.inspect}: exit=#{status.exitstatus}: #{stderr}" unless status.success? && stderr.empty?
  stdout.b
end

def common_oracle(run_root)
  verify_helper_manifest
  identity = input_identity(run_root)
  first_rows = input_rows(run_root)
  static_output = command!('/usr/bin/ruby', File.join(SNAPSHOT, 'verify-chain.rb'), 'all')
  raise 'static oracle output drift' unless static_output == "ALL_STATIC=PASS\n"

  package = published_root(run_root)
  phase_sha = sha(read_regular(File.join(package, 'phase-manifest.tsv'), 0o400))
  ablation_output = command!('/usr/bin/ruby', File.join(run_root, '30-ablation', 'validate-ablation.rb'), run_root, 'check')
  expected_ablation = "ABLATION_PACKAGE=PUBLISHED phase_sha256=#{phase_sha}\nABLATION_ORACLE=PASS run=#{File.basename(run_root)} pending=0\n"
  raise 'ablation oracle output drift' unless ablation_output == expected_ablation

  plan = File.join(WORKSPACE, '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md')
  manifest = File.join(SNAPSHOT, 'four-value-manifest.rb')
  Dir.mktmpdir('task9-review-oracle') do |temp|
    calls = [
      ['plan-set', WORKSPACE, plan, 'scope32', File.join(temp, 'targets.bin'), File.join(temp, 'targets.tsv')],
      ['protected', WORKSPACE, plan, '全栈开发Prompt Chain', File.join(temp, 'protected.bin'), File.join(temp, 'protected.tsv')],
      ['explicit', WORKSPACE, plan, '1', '全栈开发Prompt Chain.zip', File.join(temp, 'zip.bin'), File.join(temp, 'zip.tsv')]
    ]
    calls.each { |args| command!('/usr/bin/ruby', manifest, *args) }
    {
      'targets.bin' => 'targets-32-final.bin', 'targets.tsv' => 'targets-32-final.tsv',
      'protected.bin' => 'protected-44-final.bin', 'protected.tsv' => 'protected-44-final.tsv',
      'zip.bin' => 'zip-final.bin', 'zip.tsv' => 'zip-final.tsv'
    }.each do |sample, sealed|
      raise "live/frozen manifest drift: #{sample}" unless
        read_regular(File.join(temp, sample)) == read_regular(File.join(run_root, '20-final', sealed), 0o400)
    end
  end
  second_rows = input_rows(run_root)
  raise 'review input changed during oracle' unless first_rows == second_rows
  output = "TASK9_REVIEW_ORACLE=PASS run=#{File.basename(run_root)} review_input_sha256=#{identity['Review_Input_SHA256']}\n"
  [output, identity]
end

def candidate_index(run_root)
  path = File.join(published_root(run_root), 'candidate-universe.tsv')
  lines = read_regular(path, 0o400).lines(chomp: true)
  header = lines.shift&.split("\t", -1)
  raise 'candidate universe header drift' unless header && header.include?('Candidate_ID') && header.include?('Owning_task')
  rows = lines.map do |line|
    values = line.split("\t", -1)
    raise 'candidate universe field-count drift' unless values.length == header.length
    Hash[header.zip(values)]
  end
  raise 'candidate universe ID collision' unless rows.map { |row| row['Candidate_ID'] }.uniq.length == rows.length
  rows.each_with_object({}) { |row, index| index[row['Candidate_ID']] = row }
end

def validate_findings(findings, role, run_id, instance_id, allowed_paths, candidates)
  raise 'findings must be an array' unless findings.is_a?(Array)
  prefix = "#{run_id}:#{role}:#{instance_id}:F"
  findings.each do |finding|
    raise 'finding must be an object' unless finding.is_a?(Hash) && finding.keys.sort == FINDING_KEYS.sort
    raise "finding ID drift: #{finding['finding_id']}" unless
      finding['finding_id'].is_a?(String) && finding['finding_id'].match?(/\A#{Regexp.escape(prefix)}\d{3}\z/)
    raise 'finding severity drift' unless %w[Critical Important Minor].include?(finding['severity'])
    raise 'finding requirement ref missing' unless finding['requirement_ref'].is_a?(String) && !finding['requirement_ref'].empty?
    raise 'finding owner drift' unless finding['owning_task'] == 'NONE' || finding['owning_task'].match?(/\ATASK[1-8]\z/)
    raise 'finding candidate drift' unless finding['candidate_id'] == 'NONE' || candidates.key?(finding['candidate_id'])
    raise 'finding artifact outside review input' unless allowed_paths.include?(finding['artifact_path'])
    raise 'finding line drift' unless finding['line'].nil? || (finding['line'].is_a?(Integer) && finding['line'].positive?)
    action = finding['required_action']
    raise 'finding action drift' unless %w[REWORK_CONTENT REBUILD_EVIDENCE STOP NONE].include?(action)
    if finding['severity'] == 'Minor'
      raise 'minor finding must not route work' unless action == 'NONE'
      if finding['candidate_id'] == 'NONE'
        raise 'unassociated minor owner drift' unless finding['owning_task'] == 'NONE'
      else
        candidate = candidates.fetch(finding['candidate_id'])
        raise 'associated minor owner mismatch' unless finding['owning_task'] == candidate['Owning_task']
      end
    elsif action == 'REWORK_CONTENT'
      candidate = candidates.fetch(finding['candidate_id']) { raise 'content rework finding lacks candidate' }
      raise 'content rework finding owner mismatch' unless finding['owning_task'] == candidate['Owning_task']
    else
      raise 'blocking finding has no action' if action == 'NONE'
      raise 'non-rework blocking fields drift' unless finding['owning_task'] == 'NONE' && finding['candidate_id'] == 'NONE'
    end
    %w[summary evidence minimal_fix].each do |key|
      raise "finding #{key} missing" unless finding[key].is_a?(String) && !finding[key].empty?
    end
  end
  ids = findings.map { |finding| finding['finding_id'] }
  raise 'duplicate finding ID within report' unless ids.uniq.length == ids.length
end

def derived_counts(findings)
  %w[Critical Important Minor].each_with_object({}) do |severity, result|
    result[severity] = findings.count { |finding| finding['severity'] == severity }
  end
end

def derived_verdict(counts)
  return 'BLOCKED' if counts['Critical'].positive? || counts['Important'].positive?
  return 'PASS_WITH_MINOR' if counts['Minor'].positive?
  'PASS'
end

def publish_review(run_root, role, reviewer_id, instance_id, body)
  raise 'unknown review role' unless ROLES.include?(role)
  safe_identity(reviewer_id, 'reviewer ID')
  safe_identity(instance_id, 'reviewer instance ID')
  contract!(run_root)
  identity = input_identity(run_root)
  raise 'reviewer cannot be coordinator' if reviewer_id == identity['Coordinator_ID']
  parsed = strict_json(body, 'review submission')
  raise 'review body keys drift' unless parsed.is_a?(Hash) && parsed.keys.sort == %w[findings summary]
  raise 'review summary missing' unless parsed['summary'].is_a?(String) && !parsed['summary'].empty?
  rows = input_rows(run_root)
  validate_findings(
    parsed['findings'], role, File.basename(run_root), instance_id,
    rows.map { |row| row['Canonical_Path'] }.to_set, candidate_index(run_root)
  )
  oracle_output, identity_after = common_oracle(run_root)
  raise 'review identity drift during review' unless identity == identity_after

  reviews_root = File.join(run_root, '50-reviews')
  oracle_name, report_name = ROLE_FILES.fetch(role)
  oracle_path = File.join(reviews_root, oracle_name)
  encoded = Base64.strict_encode64(oracle_output.b)
  oracle_values = [
    'task9-review-oracle/v1', File.basename(run_root), role, reviewer_id, instance_id,
    ORACLE_ID, identity['Review_Input_Path'], identity['Review_Input_SHA256'], '0',
    encoded, sha(oracle_output.b), '0'
  ]
  oracle_bytes = ORACLE_RECEIPT_HEADER.join("\t") + "\n" + oracle_values.join("\t") + "\n"
  write_exclusive(oracle_path, oracle_bytes)

  counts = derived_counts(parsed['findings'])
  report = {
    'schema' => 'task9-review-report/v1',
    'run_id' => File.basename(run_root),
    'review_kind' => role,
    'reviewer_id' => reviewer_id,
    'reviewer_instance_id' => instance_id,
    'review_input_path' => identity['Review_Input_Path'],
    'review_input_sha256' => identity['Review_Input_SHA256'],
    'oracle_id' => ORACLE_ID,
    'oracle_receipt_path' => oracle_path,
    'oracle_receipt_sha256' => sha(oracle_bytes),
    'verdict' => derived_verdict(counts),
    'counts' => counts,
    'summary' => parsed['summary'],
    'findings' => parsed['findings']
  }
  write_exclusive(File.join(reviews_root, report_name), JSON.pretty_generate(report) + "\n")
  File.open(reviews_root, File::RDONLY) { |directory| directory.fsync }
  puts "TASK9_REVIEW=PUBLISHED role=#{role} verdict=#{report['verdict']} input_sha256=#{identity['Review_Input_SHA256']}"
end

def validate_review_set(run_root)
  reviews_root = File.join(run_root, '50-reviews')
  expected = ROLE_FILES.values.flatten.sort_by(&:b)
  raise 'review file set drift' unless Dir.children(reviews_root).sort_by(&:b) == expected
  oracle_output, identity = common_oracle(run_root)
  allowed_paths = input_rows(run_root).map { |row| row['Canonical_Path'] }.to_set
  candidates = candidate_index(run_root)
  reports = []
  finding_ids = []
  ROLES.each do |role|
    oracle_name, report_name = ROLE_FILES.fetch(role)
    oracle_path = File.join(reviews_root, oracle_name)
    report_path = File.join(reviews_root, report_name)
    oracle = one_tsv(oracle_path, ORACLE_RECEIPT_HEADER)
    decoded = Base64.strict_decode64(oracle['Stdout_B64'])
    raise "non-canonical oracle base64: #{role}" unless Base64.strict_encode64(decoded) == oracle['Stdout_B64']
    raise "oracle receipt drift: #{role}" unless
      oracle['Schema'] == 'task9-review-oracle/v1' &&
      oracle['Run_ID'] == File.basename(run_root) &&
      oracle['Review_Kind'] == role &&
      oracle['Oracle_ID'] == ORACLE_ID &&
      oracle['Review_Input_Path'] == identity['Review_Input_Path'] &&
      oracle['Review_Input_SHA256'] == identity['Review_Input_SHA256'] &&
      oracle['Exit_Status'] == '0' && oracle['Stderr_Bytes'] == '0' &&
      decoded == oracle_output && oracle['Stdout_SHA256'] == sha(decoded)
    report = strict_json(read_regular(report_path, 0o400), report_path)
    raise "report keys drift: #{role}" unless report.keys.sort == REVIEW_KEYS.sort
    raise "report identity drift: #{role}" unless
      report['schema'] == 'task9-review-report/v1' &&
      report['run_id'] == File.basename(run_root) &&
      report['review_kind'] == role &&
      report['reviewer_id'] == oracle['Reviewer_ID'] &&
      report['reviewer_instance_id'] == oracle['Reviewer_Instance_ID'] &&
      report['review_input_path'] == identity['Review_Input_Path'] &&
      report['review_input_sha256'] == identity['Review_Input_SHA256'] &&
      report['oracle_id'] == ORACLE_ID &&
      report['oracle_receipt_path'] == oracle_path &&
      report['oracle_receipt_sha256'] == sha(read_regular(oracle_path, 0o400))
    validate_findings(
      report['findings'], role, File.basename(run_root), report['reviewer_instance_id'],
      allowed_paths, candidates
    )
    counts = derived_counts(report['findings'])
    raise "report counts/verdict drift: #{role}" unless report['counts'] == counts && report['verdict'] == derived_verdict(counts)
    finding_ids.concat(report['findings'].map { |finding| finding['finding_id'] })
    reports << [role, report_path, oracle_path, report]
  end
  raise 'global finding ID collision' unless finding_ids.uniq.length == finding_ids.length
  reviewer_ids = reports.map { |entry| entry[3]['reviewer_id'] }
  instance_ids = reports.map { |entry| entry[3]['reviewer_instance_id'] }
  raise 'reviewer identity cardinality drift' unless reviewer_ids.uniq.length == 3 && instance_ids.uniq.length == 3
  raise 'coordinator reviewed own work' if reviewer_ids.include?(identity['Coordinator_ID'])
  [reports, oracle_output, identity]
end


def routing_bytes(run_root, reason, action, owner, candidate, artifact, details)
  values = ['task9-failure-routing/v1', File.basename(run_root), reason, action, owner, candidate, artifact, Base64.strict_encode64(details)]
  ROUTING_HEADER.join("\t") + "\n" + values.join("\t") + "\n"
end

def write_routing(run_root, reason, action, owner, candidate, artifact, details)
  path = File.join(run_root, '60-closeout', 'failure-routing.tsv')
  write_exclusive(path, routing_bytes(run_root, reason, action, owner, candidate, artifact, details))
  path
end

def run_manifest!(*args)
  stdout, stderr, status = Open3.capture3('/usr/bin/ruby', File.join(SNAPSHOT, 'four-value-manifest.rb'), *args)
  raise "manifest failed: #{args.inspect}: #{stderr}" unless status.success? && stderr.empty?
  stdout
end

def closeout(run_root)
  closeout_root = File.join(run_root, '60-closeout')
  raise 'closeout directory is not empty' unless Dir.children(closeout_root).empty?
  reports, oracle_output, identity = validate_review_set(run_root)
  blocking = reports.flat_map do |role, _path, _oracle, report|
    report['findings'].map { |finding| [role, finding] }
  end.select { |_role, finding| %w[Critical Important].include?(finding['severity']) }
  unless blocking.empty?
    severity_order = { 'Critical' => 0, 'Important' => 1 }
    role_order = { 'spec' => 0, 'safety' => 1, 'ablation' => 2 }
    ordered_blocking = blocking.sort_by do |entry|
      [severity_order.fetch(entry[1]['severity']), role_order.fetch(entry[0]), entry[1]['finding_id'].b]
    end
    reason_role = if blocking.any? { |entry| entry[0] == 'ablation' }
                    'ablation'
                  elsif blocking.any? { |entry| entry[0] == 'safety' }
                    'safety'
                  else
                    'spec'
                  end
    reason = "#{reason_role.upcase}_REVIEW_BLOCKED"
    actions = blocking.map { |entry| entry[1]['required_action'] }
    rework_pairs = blocking.select { |entry| entry[1]['required_action'] == 'REWORK_CONTENT' }
                           .map { |entry| [entry[1]['owning_task'], entry[1]['candidate_id']] }.uniq
    if actions.include?('STOP')
      action, owner, candidate = ['STOP', 'NONE', 'NONE']
    elsif actions.all? { |value| value == 'REBUILD_EVIDENCE' }
      action, owner, candidate = ['REBUILD_EVIDENCE', 'NONE', 'NONE']
    elsif actions.all? { |value| value == 'REWORK_CONTENT' } && rework_pairs.length == 1
      action, owner, candidate = ['REWORK_CONTENT', rework_pairs.first[0], rework_pairs.first[1]]
    else
      action, owner, candidate = ['STOP', 'NONE', 'NONE']
    end
    details = JSON.generate(
      ordered_blocking.map do |role, finding|
        {
          'role' => role,
          'finding_id' => finding['finding_id'],
          'severity' => finding['severity'],
          'required_action' => finding['required_action']
        }
      end
    ) + "\n"
    first_finding = ordered_blocking.first[1]
    write_routing(run_root, reason, action, owner, candidate, first_finding['artifact_path'], details)
    warn "TASK9_CLOSEOUT=BLOCKED findings=#{ordered_blocking.length} action=#{action}"
    return 4
  end

  package = published_root(run_root)
  review_index_rows = reports.map do |role, report_path, oracle_path, report|
    counts = report['counts']
    [
      role, report_path, sha(read_regular(report_path, 0o400)),
      oracle_path, sha(read_regular(oracle_path, 0o400)),
      report['reviewer_id'], report['reviewer_instance_id'],
      counts['Critical'], counts['Important'], counts['Minor'], report['verdict']
    ]
  end
  review_index = REVIEW_INDEX_HEADER.join("\t") + "\n" + review_index_rows.map { |row| row.join("\t") + "\n" }.join
  write_exclusive(File.join(closeout_root, 'review-index.tsv'), review_index)

  plan = File.join(WORKSPACE, '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-03-pm-skill-core-workflow-integration.md')
  run_manifest!('plan-set', WORKSPACE, plan, 'scope32', File.join(closeout_root, 'targets-32-closeout.bin'), File.join(closeout_root, 'targets-32-closeout.tsv'))
  run_manifest!('protected', WORKSPACE, plan, '全栈开发Prompt Chain', File.join(closeout_root, 'protected-44-closeout.bin'), File.join(closeout_root, 'protected-44-closeout.tsv'))
  run_manifest!('explicit', WORKSPACE, plan, '1', '全栈开发Prompt Chain.zip', File.join(closeout_root, 'zip-closeout.bin'), File.join(closeout_root, 'zip-closeout.tsv'))
  {
    'targets-32-closeout.bin' => 'targets-32-final.bin', 'targets-32-closeout.tsv' => 'targets-32-final.tsv',
    'protected-44-closeout.bin' => 'protected-44-final.bin', 'protected-44-closeout.tsv' => 'protected-44-final.tsv',
    'zip-closeout.bin' => 'zip-final.bin', 'zip-closeout.tsv' => 'zip-final.tsv'
  }.each do |current, sealed|
    raise "closeout manifest drift: #{current}" unless
      read_regular(File.join(closeout_root, current)) == read_regular(File.join(run_root, '20-final', sealed), 0o400)
  end
  %w[
    targets-32-closeout.bin targets-32-closeout.tsv protected-44-closeout.bin
    protected-44-closeout.tsv zip-closeout.bin zip-closeout.tsv
  ].each { |name| File.chmod(0o400, File.join(closeout_root, name)) }

  write_exclusive(File.join(closeout_root, 'closeout-oracle.txt'), oracle_output)
  critical = review_index_rows.inject(0) { |sum, row| sum + row[7] }
  important = review_index_rows.inject(0) { |sum, row| sum + row[8] }
  minor = review_index_rows.inject(0) { |sum, row| sum + row[9] }
  target_sha = sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400))
  universe_sha = sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400))
  ledger_sha = sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
  reviewer_ids = reports.map { |entry| entry[3]['reviewer_id'] }
  instance_ids = reports.map { |entry| entry[3]['reviewer_instance_id'] }
  closeout_values = [
    'task9-closeout/v1', File.basename(run_root), identity['Review_Input_Path'], identity['Review_Input_SHA256'],
    '3', sha(review_index), reviewer_ids.uniq.length.to_s, instance_ids.uniq.length.to_s,
    critical.to_s, important.to_s, minor.to_s, ORACLE_ID, sha(oracle_output),
    target_sha, sha(read_regular(File.join(closeout_root, 'protected-44-closeout.bin'), 0o400)),
    sha(read_regular(File.join(closeout_root, 'zip-closeout.bin'), 0o400)),
    universe_sha, ledger_sha, 'true'
  ]
  closeout_bytes = CLOSEOUT_HEADER.join("\t") + "\n" + closeout_values.join("\t") + "\n"
  closeout_path = File.join(closeout_root, 'closeout.tsv')
  write_exclusive(closeout_path, closeout_bytes)
  token_values = [
    'task9-completion-token/v1', File.basename(run_root), identity['Review_Input_SHA256'],
    target_sha, universe_sha, ledger_sha, '3', sha(review_index), reviewer_ids.uniq.length.to_s,
    instance_ids.uniq.length.to_s, critical.to_s, important.to_s, sha(closeout_bytes), 'true'
  ]
  write_exclusive(
    File.join(closeout_root, 'completion-token.tsv'),
    TOKEN_HEADER.join("\t") + "\n" + token_values.join("\t") + "\n"
  )
  File.open(closeout_root, File::RDONLY) { |directory| directory.fsync }
  Dir.children(File.join(run_root, '50-reviews')).each do |name|
    File.chmod(0o400, File.join(run_root, '50-reviews', name))
  end
  File.chmod(0o500, File.join(run_root, '50-reviews'))
  Dir.children(closeout_root).each { |name| File.chmod(0o400, File.join(closeout_root, name)) }
  raise 'review phase root mode drift' unless (File.lstat(File.join(run_root, '50-reviews')).mode & 0o777) == 0o500
  review_files_sealed = Dir.children(File.join(run_root, '50-reviews')).all? do |name|
    (File.lstat(File.join(run_root, '50-reviews', name)).mode & 0o777) == 0o400
  end
  raise 'review phase file mode drift' unless review_files_sealed
  puts "TASK9_CLOSEOUT=PASS reports=3 critical=#{critical} important=#{important} minor=#{minor}"
  0
end

def seal_failure(run_root)
  routing_path = File.join(run_root, '60-closeout', 'failure-routing.tsv')
  route = one_tsv(routing_path, ROUTING_HEADER)
  raise 'failure route run/schema drift' unless route['Schema'] == 'task9-failure-routing/v1' && route['Run_ID'] == File.basename(run_root)
  details = Base64.strict_decode64(route['Blocking_Findings_B64'])
  raise 'failure route non-canonical base64' unless Base64.strict_encode64(details) == route['Blocking_Findings_B64']
  parsed_details = strict_json(details, routing_path)
  raise 'failure route details shape drift' unless parsed_details.is_a?(Array) || parsed_details.is_a?(Hash)
  raise 'failure route reason drift' unless route['Reason_Code'].match?(/\A[A-Z0-9_]+\z/)
  raise 'failure route action drift' unless %w[REWORK_CONTENT REBUILD_EVIDENCE STOP].include?(route['Required_Action'])
  if route['Required_Action'] == 'REWORK_CONTENT'
    raise 'failure route owner/candidate drift' unless
      route['Owning_Task'].match?(/\ATASK[1-8]\z/) && route['Candidate_ID'].match?(/\ACAND-[A-Z0-9-]+\z/)
    candidate = candidate_index(run_root).fetch(route['Candidate_ID']) { raise 'failure route candidate missing' }
    raise 'failure route owner does not own candidate' unless candidate['Owning_task'] == route['Owning_Task']
  else
    raise 'non-rework failure route drift' unless route['Owning_Task'] == 'NONE' && route['Candidate_ID'] == 'NONE'
  end
  identity = input_identity(run_root)
  package = published_root(run_root)
  exec(
    '/usr/bin/ruby', File.join(SNAPSHOT, 'seal-task9-generation.rb'),
    File.basename(run_root), 'INVALIDATED', route['Reason_Code'], route['Required_Action'],
    route['Owning_Task'], route['Candidate_ID'], routing_path,
    identity['Review_Input_SHA256'],
    sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400)),
    sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400)),
    sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
  )
end

def terminal_ready(run_root)
  closeout_root = File.join(run_root, '60-closeout')
  expected = %w[
    closeout-oracle.txt closeout.tsv completion-token.tsv protected-44-closeout.bin
    protected-44-closeout.tsv review-index.tsv targets-32-closeout.bin
    targets-32-closeout.tsv zip-closeout.bin zip-closeout.tsv
  ].sort_by(&:b)
  raise 'terminal closeout file-set drift' unless Dir.children(closeout_root).sort_by(&:b) == expected
  reports, oracle_output, identity = validate_review_set(run_root)
  package = published_root(run_root)
  review_index_rows = reports.map do |role, report_path, oracle_path, report|
    counts = report['counts']
    [
      role, report_path, sha(read_regular(report_path, 0o400)),
      oracle_path, sha(read_regular(oracle_path, 0o400)),
      report['reviewer_id'], report['reviewer_instance_id'],
      counts['Critical'], counts['Important'], counts['Minor'], report['verdict']
    ]
  end
  review_index_bytes = REVIEW_INDEX_HEADER.join("\t") + "\n" +
    review_index_rows.map { |row| row.join("\t") + "\n" }.join
  raise 'terminal review-index drift' unless
    read_regular(File.join(closeout_root, 'review-index.tsv'), 0o400) == review_index_bytes
  review_index_sha = sha(review_index_bytes)
  closeout_path = File.join(closeout_root, 'closeout.tsv')
  closeout_bytes = read_regular(closeout_path, 0o400)
  closeout = one_tsv(closeout_path, CLOSEOUT_HEADER)
  token = one_tsv(File.join(closeout_root, 'completion-token.tsv'), TOKEN_HEADER)
  reviewer_ids = reports.map { |entry| entry[3]['reviewer_id'] }
  instance_ids = reports.map { |entry| entry[3]['reviewer_instance_id'] }
  minor = reports.inject(0) { |sum, entry| sum + entry[3]['counts']['Minor'] }
  target_sha = sha(read_regular(File.join(run_root, '20-final', 'targets-32-final.bin'), 0o400))
  universe_sha = sha(read_regular(File.join(package, 'candidate-universe.tsv'), 0o400))
  ledger_sha = sha(read_regular(File.join(package, 'ablation-ledger.tsv'), 0o400))
  raise 'terminal closeout eligibility drift' unless
    closeout['Schema'] == 'task9-closeout/v1' && closeout['Run_ID'] == File.basename(run_root) &&
    closeout['Review_Input_Path'] == identity['Review_Input_Path'] &&
    closeout['Review_Input_SHA256'] == identity['Review_Input_SHA256'] &&
    closeout['Report_Count'] == '3' && closeout['Review_Index_SHA256'] == review_index_sha &&
    closeout['Distinct_Reviewer_ID_Count'] == reviewer_ids.uniq.length.to_s &&
    closeout['Distinct_Reviewer_Instance_Count'] == instance_ids.uniq.length.to_s &&
    closeout['Critical_Count'] == '0' && closeout['Important_Count'] == '0' &&
    closeout['Minor_Count'] == minor.to_s && closeout['Oracle_ID'] == ORACLE_ID &&
    closeout['Oracle_Output_SHA256'] == sha(oracle_output) &&
    closeout['Target_Manifest_SHA256'] == target_sha &&
    closeout['Protected_Manifest_SHA256'] == sha(read_regular(File.join(closeout_root, 'protected-44-closeout.bin'), 0o400)) &&
    closeout['Zip_Manifest_SHA256'] == sha(read_regular(File.join(closeout_root, 'zip-closeout.bin'), 0o400)) &&
    closeout['Candidate_Universe_SHA256'] == universe_sha &&
    closeout['Ablation_Ledger_SHA256'] == ledger_sha && closeout['Completion_Eligible'] == 'true'
  raise 'terminal token drift' unless
    token['Schema'] == 'task9-completion-token/v1' && token['Run_ID'] == File.basename(run_root) &&
    token['Review_Input_SHA256'] == identity['Review_Input_SHA256'] &&
    token['Target_Manifest_SHA256'] == target_sha &&
    token['Candidate_Universe_SHA256'] == universe_sha && token['Ablation_Ledger_SHA256'] == ledger_sha &&
    token['Report_Count'] == '3' && token['Review_Index_SHA256'] == review_index_sha &&
    token['Distinct_Reviewer_ID_Count'] == '3' &&
    token['Distinct_Reviewer_Instance_Count'] == '3' && token['Critical_Count'] == '0' &&
    token['Important_Count'] == '0' && token['Closeout_SHA256'] == sha(closeout_bytes) && token['Eligible'] == 'true'
  raise 'closeout oracle receipt drift' unless
    read_regular(File.join(closeout_root, 'closeout-oracle.txt'), 0o400) == oracle_output
  {
    'targets-32-closeout.bin' => 'targets-32-final.bin', 'targets-32-closeout.tsv' => 'targets-32-final.tsv',
    'protected-44-closeout.bin' => 'protected-44-final.bin', 'protected-44-closeout.tsv' => 'protected-44-final.tsv',
    'zip-closeout.bin' => 'zip-final.bin', 'zip-closeout.tsv' => 'zip-final.tsv'
  }.each do |current, sealed|
    raise "terminal manifest drift: #{current}" unless
      read_regular(File.join(closeout_root, current), 0o400) == read_regular(File.join(run_root, '20-final', sealed), 0o400)
  end
  ready_values = [
    'task9-terminal-ready/v1', File.basename(run_root), identity['Review_Input_SHA256'],
    sha(closeout_bytes), ORACLE_ID, sha(oracle_output), 'true'
  ]
  ready_path = File.join(closeout_root, 'terminal-ready.tsv')
  write_exclusive(ready_path, READY_HEADER.join("\t") + "\n" + ready_values.join("\t") + "\n")
  File.open(closeout_root, File::RDONLY) { |directory| directory.fsync }
  File.chmod(0o500, closeout_root)
  puts "TASK9_TERMINAL_READY=PASS run=#{File.basename(run_root)} review_input_sha256=#{identity['Review_Input_SHA256']}"
end

mode = ARGV.shift or abort 'usage: task9-review-tools.rb build-input|publish-review|closeout|seal-failure ...'
run_root = File.expand_path(ARGV.shift || abort('missing run root'))
run_id = File.basename(run_root)
abort 'invalid Task 9 run root' unless run_root == File.join(SNAPSHOT, 'task9', run_id) && run_id.match?(/\Arun-\d{3}\z/)

begin
  case mode
  when 'build-input'
    coordinator_id = ARGV.shift or abort 'missing coordinator ID'
    abort "unexpected arguments: #{ARGV.inspect}" unless ARGV.empty?
    build_input(run_root, coordinator_id)
  when 'publish-review'
    role = ARGV.shift or abort 'missing role'
    reviewer_id = ARGV.shift or abort 'missing reviewer ID'
    instance_id = ARGV.shift or abort 'missing reviewer instance ID'
    abort "unexpected arguments: #{ARGV.inspect}" unless ARGV.empty?
    publish_review(run_root, role, reviewer_id, instance_id, STDIN.read)
  when 'closeout'
    abort "unexpected arguments: #{ARGV.inspect}" unless ARGV.empty?
    exit(closeout(run_root))
  when 'seal-failure'
    abort "unexpected arguments: #{ARGV.inspect}" unless ARGV.empty?
    seal_failure(run_root)
  else
    abort "unknown mode: #{mode}"
  end
rescue StandardError => error
  if mode == 'closeout'
    closeout_root = File.join(run_root, '60-closeout')
    routing_path = File.join(closeout_root, 'failure-routing.tsv')
    unless File.exist?(routing_path) || File.symlink?(routing_path)
      begin
        write_routing(
          run_root, 'CLOSEOUT_VALIDATOR_FAIL', 'STOP', 'NONE', 'NONE',
          File.join(run_root, '40-review-input', 'review-input.tsv'),
          JSON.generate('error_class' => error.class.name, 'message' => error.message) + "\n"
        )
      rescue StandardError
        # Preserve the original exception; the generic recovery protocol handles a routing-write failure.
      end
    end
  end
  warn "#{error.class}: #{error.message}"
  exit 5
end
~~~

Create and freeze the two files, then build the input exactly once:

~~~zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}" "${TASK9_COORDINATOR_ID:?actual coordinator identity}"
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
review_root="$run_root/40-review-input"
[[ "$TASK9_RUN_ID" == run-[0-9][0-9][0-9] ]]
/usr/bin/ruby -c "$review_root/task9-review-tools.rb"
/bin/chmod 400 "$review_root/review-contract.json" "$review_root/task9-review-tools.rb"
/usr/bin/ruby "$review_root/task9-review-tools.rb" build-input "$run_root" "$TASK9_COORDINATOR_ID"
~~~

Expected output: `TASK9_REVIEW_INPUT=SEALED`. The 32 `target` rows point to the immutable `20-final/content/` copies, never to live workspace files. Evidence rows include the fixed helper manifest, baseline, all Task 1–8 manifests, Task 9 input/final evidence and the published ablation package. `review-input.identity.tsv` binds the actual coordinator, input hash, target hash, universe hash and ledger hash.


- [ ] **Step 6: Dispatch three fresh sibling reviewers against the identical frozen input**

The coordinator dispatches `spec`, `safety` and `ablation` simultaneously before any report exists. Each reviewer is a fresh direct child of the coordinator, receives only its exact `ROLE_SCOPES` entry plus the absolute `review-input.tsv` path and hash, and must not read or cite either other review. The three actual `Reviewer_ID` values, the three actual invocation/thread `Reviewer_Instance_ID` values, and the coordinator ID must all differ. These are operational independence requirements; the helper verifies identity cardinality but does not pretend that IDs alone prove cognitive independence.

Each reviewer reads only paths enumerated by the frozen input, runs no mutation or external side effect, and returns exactly this input body to `publish-review`:

~~~json
{
  "summary": "actual review summary",
  "findings": [
    {
      "finding_id": "run-NNN:spec:ACTUAL_INSTANCE_ID:F001",
      "severity": "Critical",
      "requirement_ref": "approved-design section or exact contract reference",
      "owning_task": "TASK1",
      "candidate_id": "CAND-ACTUAL-ID",
      "artifact_path": "/absolute/canonical/path/from/review-input.tsv",
      "line": 1,
      "required_action": "REWORK_CONTENT",
      "summary": "what is wrong",
      "evidence": "direct evidence from the frozen bytes",
      "minimal_fix": "smallest sufficient correction"
    }
  ]
}
~~~

An empty `findings` array is allowed only after the reviewer actually completes its scope. Valid severities are `Critical | Important | Minor`. Every `Critical` or `Important` requires an action. Every `Minor` requires `required_action=NONE`; it may either use `owning_task=NONE,candidate_id=NONE` or associate a real Candidate whose owner is recomputed from the universe, but it never routes work. `REWORK_CONTENT` additionally requires the exact candidate and its machine-derived owning Task. Findings IDs are fixed as `run-NNN:role:actual-instance-id:FNNN`, so they cannot be silently reused across generations or invocations. All submitted and stored JSON is parsed with duplicate-key rejection and `NaN`/`Infinity` disabled before exact-key validation.

For each role, the reviewer publishes through the helper; no reviewer writes a report pathname directly:

~~~zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}" "${REVIEW_ROLE:?spec|safety|ablation}"
: "${REVIEWER_ID:?actual canonical reviewer identity}"
: "${REVIEWER_INSTANCE_ID:?actual invocation identity}"
: "${ACTUAL_REVIEW_JSON:?exact summary/findings JSON}"
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
print -rn -- "$ACTUAL_REVIEW_JSON" |
  /usr/bin/ruby "$run_root/40-review-input/task9-review-tools.rb" publish-review     "$run_root" "$REVIEW_ROLE" "$REVIEWER_ID" "$REVIEWER_INSTANCE_ID"
~~~

Expected for each role: `TASK9_REVIEW=PUBLISHED role=<role>`. Every publication reruns `TASK9_REVIEW_ORACLE_V1` and creates exactly one immutable oracle receipt plus one immutable report. Any failure, duplicate path, invalid schema or interrupted reviewer invalidates this generation; do not replace or supplement a report in place.

- [ ] **Step 7: Validate the exact review set and publish one closeout token**

After all three reviewer processes have stopped, run:

~~~zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}"
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
tool="$run_root/40-review-input/task9-review-tools.rb"
set +e
closeout_output=$(/usr/bin/ruby "$tool" closeout "$run_root" 2>&1)
closeout_exit=$?
set -e
print -r -- "$closeout_output"
if (( closeout_exit != 0 )); then
  if [[ -f "$run_root/60-closeout/failure-routing.tsv" && ! -L "$run_root/60-closeout/failure-routing.tsv" ]]; then
    /usr/bin/ruby "$tool" seal-failure "$run_root"
  fi
  print -u2 'TASK9_CLOSEOUT_FAILED: if no terminal was emitted, stop all writers and use the generic recovery protocol'
  exit "$closeout_exit"
fi
~~~

The closeout helper requires exactly six review files, three roles, three reviewer IDs, three invocation IDs, the same review-input hash, valid per-review oracle receipts, and a fresh shared-oracle pass. It deterministically selects the first blocker by `Critical > Important`, then `spec > safety > ablation`, then byte-sorted finding ID. A role-specific blocker terminates with `SPEC_REVIEW_BLOCKED`, `SAFETY_REVIEW_BLOCKED` or `ABLATION_REVIEW_BLOCKED`; only the last invalidates both prior candidate-universe and decision authority for inheritance. A malformed review set or closeout helper exception routes fail-closed and never produces a completion token.

Expected pass: `TASK9_CLOSEOUT=PASS reports=3 critical=0 important=0`. Minor findings may remain and are counted. The pass creates immutable `review-index.tsv`, fresh target/protected/ZIP closeout manifests, `closeout-oracle.txt`, `closeout.tsv` and `completion-token.tsv`. No `Critical` or `Important` can coexist with `Eligible=true`.

- [ ] **Step 8: Atomically create terminal readiness and publish the exclusive completed terminal**

Compute the four claimed hashes and immediately `exec` the sole sealer. The claims are inputs for equality checking, not authority: the sealer independently rebuilds the review closure, creates `terminal-ready.tsv`, seals `60-closeout/`, rechecks all eligibility, and publishes the terminal in that same process:

~~~zsh
set -euo pipefail
: "${TASK9_RUN_ID:?}"
snapshot_root='/private/tmp/vibecoding-pm-skill-integration-20260903-71c6d4ce'
run_root="$snapshot_root/task9/$TASK9_RUN_ID"
/usr/bin/ruby - "$snapshot_root" "$run_root" <<'RUBY'
require 'digest'
snapshot, run_root = ARGV
run_id = File.basename(run_root)
paths = {
  review: File.join(run_root, '40-review-input', 'review-input.tsv'),
  target: File.join(run_root, '20-final', 'targets-32-final.bin'),
  universe: File.join(run_root, '30-ablation', 'published', 'candidate-universe.tsv'),
  ledger: File.join(run_root, '30-ablation', 'published', 'ablation-ledger.tsv')
}
hashes = paths.map { |_name, path| Digest::SHA256.file(path).hexdigest }
exec(
  '/usr/bin/ruby', File.join(snapshot, 'seal-task9-generation.rb'),
  run_id, 'COMPLETED', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE', *hashes
)
RUBY
~~~

Expected output ends with:

~~~text
TASK9_TERMINAL=COMPLETED run=run-NNN sha256=<64hex> seal_sha256=<64hex>
~~~

The sealer rejects a missing or extra review/evidence row, duplicate JSON key, blocker, review-index mismatch, manifest-set drift, closeout/token mismatch, pending package, or any of the four caller hashes that differs from actual bytes. It creates and fsyncs `terminal-ready.tsv`, freezes the closeout directory, reruns the full eligibility check, publishes `terminal-intent.tsv`, `generation-seal.tsv` and `TERMINAL.tsv`, then performs a fresh complete path/hash/mode traversal. If a process dies after terminal publication, only `--finalize-existing run-NNN` may continue; it accepts no caller-supplied state. If it dies earlier, the pre-created `70-recovery/` channel remains available even when another phase directory is already `0500`.

Failure and retry rules are immutable:

- `REWORK_CONTENT` returns to its exact `Owning_Task` under the O_EXCL-reserved next `TASKn_Rk`. That task consumes the invalidated run's sealed `guard-scope.tsv`; the next Task 9 generation consumes its new sealed `scope32-after.tsv`.
- `REBUILD_EVIDENCE` changes no workspace file. The next monotonic generation consumes the preceding run's sealed `input-scope.tsv`, but only after the recovery proof or a fixed phase handler established unchanged content.
- `STOP` forbids another generation until a revised and independently reviewed plan resolves the unknown condition.
- Every retry uses the next `run-NNN` and rebuilds input, ablation, three reviews and closeout. No report, receipt, package or completion token is copied forward.
- A `COMPLETED` terminal forbids every successor.

## Execution handoff

The plan is ready for either execution style:

1. **Subagent-Driven（推荐）**：one fresh implementer per Task plus the declared independent reviewers; the coordinator enforces manifests, scopes and handoffs.
2. **Inline Execution**：the coordinator executes the same Tasks serially in this task, using the identical guards and receipts.

Either choice starts with **Task 0 only**. Task 0 builds and validates the snapshot and then stops at Step 6 to request the separate normalization authorization. Selecting an execution style is not permission to normalize files, implement Tasks 1–9, access production, or perform any external side effect.

<!-- TASK9_REWRITE_ANCHOR -->
