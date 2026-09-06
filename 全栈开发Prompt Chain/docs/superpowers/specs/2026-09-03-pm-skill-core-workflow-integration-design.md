# PM-Skill 2.0 核心工作流受限融合设计

## 目标

将空格.space 分享的产品经理工作流中有独立增量的方法，改写为受限的产品方法 Adapter，并融入现有全栈开发 Prompt Chain。

本次融合保留 M00–M13、G0–G6、R3 和 A00–A13 为唯一流程、决策、授权与产物体系。不安装 `pm-skills`，不引入 `pm-master`，不新增 M14、新 Gate、自动外部动作或第二套状态机。

融合后的主要增量是一张可追踪的产品决策图。生命周期仍按 M00–M13 顺序推进，但产品实体之间不是一条一对一单链：

```text
Evidence_Ref -[supports]-> Opportunity_ID
Evidence_Ref -[refutes]-> Opportunity_ID
Opportunity_ID -[contributes_to]-> Outcome_ID
Candidate_ID -[addresses]-> Opportunity_ID
Hypothesis_ID -[applies_to]-> Candidate_ID
Test_ID -[tests]-> Hypothesis_ID
Slice_ID -[realizes]-> Candidate_ID 或 A05 Spec
Metric_ID -[measures]-> Outcome_ID / Opportunity_ID / Hypothesis_ID / safety_guardrail
Metric_ID -[derived_from]-> Event_ID
Decision_ID -[governs]-> Entity_ID
```

这张图允许一对多和多对多关系，附着在现有 Axx 产物中，不替代 `Facts`、`Decisions`、`Assumptions`、`Open questions`、`Risks and reversibility`、`Acceptance evidence` 或 `Handoff`。

## 已批准边界

- 采用「分层 Adapter」方案，只吸收方法，不复制或安装原仓库 Skill。
- 不增加新的生命周期模块、Gate、控制器、Agent 人格或并行顾问委员会。
- `prompts/99-端到端Prompt-Chain.md` 仍是唯一总控；任何产品方法只能在当前 Mxx 内受限调用。
- 普通 Prompt 是模块语义源。受影响的 `prompts_ask/` 文件必须同步表达相同事实、边界、产物字段和停止条件。
- 不默认联网、搜索、联系用户、发送问卷、读取生产数据、创建 tracker、启动实验、调整流量或部署。
- 外部动作继续要求对象级、未过期的 `R3_ACTION_AUTHORIZATION`；G5/G6 不能替代动作授权。
- 缺少字段事实时使用 `Unknown`；未经验证的解释写入公共 `Assumptions`；会改变决定且尚未回答的问题写入公共 `Open questions`。不使用默认分数制造精确结论。
- 每个新增方法块都必须经过消融式删减检查。没有独立决策、安全或交接价值的内容应删除。

## 事实边界与来源

本次评估使用以下公开材料：

- [空格.space 的 X 帖子](https://x.com/kongge_space/status/2094622724924838322)。2026-09-03 访问时，公开 oEmbed 请求成功，信息显示帖子发布于 2026-09-01，并指向一篇 X Article；该 Article 在匿名访问下未返回可审读正文。
- [SpaceZephyr/pm-skills 固定提交](https://github.com/SpaceZephyr/pm-skills/tree/4c486c7a532de8890e88036533e0a48d578087ed)。本设计以提交 `4c486c7a532de8890e88036533e0a48d578087ed` 为可复核快照，不跟随仓库后续变化。
- [固定版本 README](https://github.com/SpaceZephyr/pm-skills/blob/4c486c7a532de8890e88036533e0a48d578087ed/README.md) 与 [固定版本 pm-master](https://github.com/SpaceZephyr/pm-skills/blob/4c486c7a532de8890e88036533e0a48d578087ed/pm-master/SKILL.md)。

X Article 正文无法在匿名访问条件下完整取得。因此，本设计不声称逐字还原文章内容；可复现的方法评估以固定仓库快照为主，X 帖子只作为来源入口。

仓库 README 声称采用 MIT License，但固定快照根目录未发现 `LICENSE` 文件。为避免授权含义不清，本项目只吸收抽象方法、重新组织字段并注明来源，不复制原仓库提示词、模板或大段表述。

## 价值审计

| 原工作流部分 | 独立价值 | 与现有 Chain 的关系 | 决定 |
| --- | --- | --- | --- |
| `pm-master` 自动路由与预制链 | 降低 Skill 选择成本 | 现有 M00 与 `prompts/99` 已有更强的逐模块、Gate、授权和恢复协议 | 不采用 |
| 最多十行的 Skill Handoff | 降低阅读成本 | 会丢失现有 Axx 的事实、决定、假设、风险、授权和验证状态 | 不采用；只增加结构化索引 |
| Mom Test 式过去行为取证 | 抑制礼貌性回答和愿望陈述 | M03 已有证据纪律，但替代方案、变通成本和机会映射仍可增强 | 条件采用并改写 |
| Torres 式 Outcome–Opportunity–Solution–Test | 保持研究、方案与测试之间的因果可追踪性 | 现有模块分别覆盖，但缺少稳定的跨模块 ID 谱系 | 采用核心关系；不采用固定频率和固定方案数 |
| 俞军式用户价值与切换成本 | 强制与当前替代方案比较 | 现有 M04 有 no-build，但可补充切换成本和行为摩擦 | 定性采用；拒绝无数据效用公式 |
| Story Mapping | 以用户旅程确定第一个端到端切片 | M05/M07 已有旅程和垂直切片，可增加明确的旅程骨架 | 条件采用；不另建 Story Map 产物 |
| Build Trap 式 Outcome 导向 | 避免用交付数量替代产品结果 | M04 指标树与 M11 学习流程已覆盖 | 只用于强化谱系，不增加独立流程 |
| Cagan 四类产品风险 | 提供紧凑的产品风险扫描 | 不能覆盖安全、隐私、合规、无障碍和运维风险 | 作为可选产品视角采用 |
| PRD 模板 | 提高规格完整性 | M05 已有更严格的事实、决策和开放问题边界 | 只吸收缺项显式化；不复制模板 |
| 多角色评审板 | 暴露跨职能分歧 | 人格扮演和模拟共识容易产生伪权威 | 改写为无人格的 review findings |
| 优先级引擎 | 比较多个候选并解释取舍 | 默认桶值和自动排序会制造伪精确 | 只采用敏感性和排序反转分析 |
| 问卷设计 | 补充规模化研究工具 | 现有 M03 缺少问卷专用的假设与偏差契约 | 作为可选分支采用 |
| 埋点规格 | 连接产品假设、实现和生产学习 | 现有 Chain 缺少统一的事件语义、身份和质量契约 | 高价值采用，但默认数据最小化 |
| 实验设计 | 连接假设、指标与决策 | M12 已覆盖分流、暴露、MDE 输入、护栏、SRM 和停止规则 | 只补充谱系引用，不降级现有标准 |
| 复盘行动项 | 将发现转成可验证后续动作 | M13 有学习候选，但缺少通用行动登记字段 | 条件采用；禁止自动承诺负责人或日期 |
| Roadmap | 表达多 initiative 的顺序和依赖 | 单一 slice 不需要；多 initiative 时有价值 | 作为 M07 可选分支采用 |

## 总体架构

### 外层控制契约

现有 M00 与 `prompts/99` 继续决定当前模块、所需输入、Gate、模式和下一安全动作。产品方法 Adapter 不能执行以下行为：

1. 根据「很急」或「需求明确」跨过当前模块、Gate 或确认。
2. 自动调用后续模块。
3. 把 review finding、评分、实验结论或多视角一致意见写成批准决定。
4. 把方法建议解释为本地写入、外部访问或生产动作授权。

M00 不需要修改。`prompts/99` 控制器最多增加一条兼容规则：若当前 Axx 含产品决策图，下游模块必须引用或显式关闭对应 ID。该规则不增加路由、状态、Gate 或权限。

### 方法 Adapter

Adapter 是当前模块内部的一组条件检查，不是独立 Agent、Skill 或工作流。每个 Adapter 必须声明：

- 触发条件。
- 所需输入和证据等级。
- 对当前 Axx 增加的最小字段。
- 不能得出的结论。
- 停止条件和下一模块接口。

同一任务不满足触发条件时，不生成空表格或占位报告。

### Adapter 契约表

| Adapter / 模块 | 触发条件 | 输入与最低证据 | 对 Axx 的最小增量 | 不能得出的结论 | 停止条件与下游 |
| --- | --- | --- | --- | --- | --- |
| Competitor transfer / M02 | 用户要求竞品、替代方案或市场比较 | 可定位的一手产品资料、实际行为或明确标为二手的资料；记录日期与适用市场 | 事实、目标情境、成立条件、反证、可迁移原则、不可迁移约束 | 竞品功能等于用户需求；公开承诺等于已交付能力 | 来源不可验证则降级；A02 交给 M03/M04，不产生产品批准 |
| Behavior-to-opportunity / M03 | 需要理解问题、行为、替代方案或机会 | 经同意取得的访谈/观察、获准数据或可引用现有研究；至少记录来源和样本限制 | `Opportunity_ID`、`Evidence_Refs`、过去行为、当前替代、摩擦、反例、适用分群 | 单个样本代表市场；愿望陈述证明需求；无承诺即失败 | 证据不足时写入 `Assumptions`；A03 交给 M04 |
| Survey plan / M03 | 已有假设且需要规模化、分群或定量补证据 | Research question、目标人群、已有假设、数据和同意边界 | 问题—假设—决定映射、样本框、偏差、发放边界、回答质量、预注册分析草案 | 固定样本量有效；问卷计划等于已发送或已有结果 | 缺少样本框/同意边界时停止；仍输出 A03 draft，不发送问卷 |
| Decision graph and product risks / M04 | A03 存在可评估机会，或用户提供了可验证问题证据 | A03、A00/A01 中仍有效的目标与约束、当前替代方案 | `Outcome_ID`、`Candidate_ID`、`Hypothesis_ID`、`Priority: riskiest`、四产品风险、最便宜可逆测试 | 框架分类证明方案正确；四产品风险覆盖安全/合规风险 | Outcome 或关键决定权不清时停在 G2 前；A04 交给 M05/M06 |
| Prioritization sensitivity / M04 | 至少两个竞争候选且顺序会影响范围或资源 | 候选、目标贡献、成本/风险/可逆性证据；未知项保留区间 | 输入来源、假设区间、排序建议、反对理由、排序反转条件 | 无数据分数是事实；自动置顶、取消、排期或写 backlog | 关键输入变化即可反转时标记不稳定；交给 G2 人工决定 |
| Story backbone / M05 | 功能跨多个用户步骤、状态或异常路径 | 已批准或明确允许 draft 的 A04、用户旅程事实、领域状态 | 入口、活动、关键任务、完成状态、异常路径、首个产品 thin slice | 完整旅程图等于规格批准；工作坊形式是必需 | 主路径或状态不清时写入 `Open questions`；A05 交给 M06/M07 |
| Measurement contract / M05 | Outcome/Hypothesis/验收需要行为或系统测量 | A04/A05、获准数据范围、现有 schema/analytics 事实 | `Metric_ID`、`Event_ID`、语义、触发、属性、身份去重、隐私、质量和版本 | 定义完成等于已埋点、已有数据或可读生产数据 | 目的、隐私或 source of truth 不清时保持 draft；M07 只创建 ticket |
| Pre-build findings / M05 | 规格高影响、跨职能、不可逆或用户明确要求预评审 | 固定版本的 A04/A05/原型证据和适用规范 | lens、证据位置、finding、后果、severity、建议动作、复评条件 | 模拟角色意见是专家批准；`0 blocker` 等于 Gate 通过 | blocker 返回 M04/M05；否则 findings 随 A05 交给 M07/M09 |
| Hypothesis test / M06 | M04 存在仍会推翻方案的 `Hypothesis_ID` | A04、目标用户/fixture、学习问题、同意和写入边界 | `Test_ID`、被测 `Hypothesis_ID` 引用、最小原型/研究、通过/失败/不确定判据、证据 | 原型完成度证明价值；未执行测试等于已验证 | 无安全测试方式或关键样本边界不清时停止；A06 交给 M07 或返回 M04 |
| Walking skeleton / M07 | 已批准的产品 slice 需要转为架构和 ticket | A05、A06、G3 决定、项目代码与约束事实 | `Slice_ID`、UI/API/data/observability 路径、依赖、验收、instrumentation ticket | 只完成一个技术层等于端到端；计划等于 G4 写入授权 | 高影响 seam 未决定时停止；A07 交给 G4/M08 |
| Roadmap outline / M07 | 同时存在多个 initiative、共享依赖或资源冲突 | 已批准优先级、依赖、容量事实或明确假设 | milestone、slice、依赖、容量假设、关键路径、成功信号、改向触发 | 粗略轮廓是工期承诺；自动写 tracker | 依赖/容量无最小事实时只给情景，不给日期承诺；A07 交给人工排期 |
| Implementation trace / M08 | G4 已批准某个 `Slice_ID` 和精确写入范围 | A05/A07、匹配 G3/G4、`ALLOWED_FILES`、测试和代码事实 | `Slice_ID` 引用、changed files、`Metric_ID`/`Event_ID` 实现位置、测试和未验证项 | 实现可以新增产品决定、采集字段或外部动作权限 | 任一授权/范围不匹配即停止；A08 交给 M09 |
| Risk and measurement verification / M09 | 存在固定 review range 和 A05/A07/A08 | 固定 diff、适用规范、测试/构建/视觉或只读证据 | 产品风险 closure、measurement finding、证据位置、severity、Unverified scope | finding 是批准；无 finding 证明可发布；审查自动修复 | blocker 返回对应模块；A09 交给 G5/M10，不修改文件 |
| Feedback and action register / M11 | 已有获准生产证据、用户反馈或 incident 事实 | G0 数据范围、匹配 R3、查询/来源、窗口和质量限制 | Evidence、Observation、Causal hypothesis、Counterevidence、建议行动、验证和目标模块 | 相关性证明因果；建议已创建 tracker 或已执行 | 无生产授权则只用已有材料；A11 返回 M03/M04/M05/M12/M13 |
| Experiment decision / M12 | 已有可证伪 `Hypothesis_ID`、测量契约与实验适用性 | A04/A11、`Metric_ID`/`Event_ID`、baseline/variance/traffic、护栏和现有 Gate | `Test_ID`、被测 `Hypothesis_ID` 引用、assignment、eligibility、exposure、分析计划、限制、recommended decision | 统计结果自动代表用户价值、长期留存或上线决定 | 设计不完整停在 draft；真实动作缺任一条件则 `Not launched` |
| Retrospective action / M13 | 任务、发布、实验或 incident 产生可复核结果 | Axx、时间线、预期与实际、验证证据和限制 | 事实、因果假设、反证、行动登记、候选学习和撤回条件 | 叙事完整证明根因；行动已有负责人；候选已进入长期记忆 | 证据不足则保持 causal hypothesis；A13 指向目标模块并等待人工决定 |

### 产物与交接

产品决策图作为 A03–A13 的可选公共子节存在。每个模块只更新本模块有权产生的字段：

- M03 创建或修订 `Opportunity_ID` 和 `Evidence_Refs`，不要求引用尚未形成的 `Outcome_ID`。
- M04 创建或确认 `Outcome_ID`，将一个或多个 `Opportunity_ID` 绑定到该结果；随后分别创建 `Candidate_ID` 和 `Hypothesis_ID`，并将当前最大未知假设标记为 `Priority: riskiest`。
- M05/M06/M07 创建产品规格、测试或首个切片引用。
- M05 是 `Metric_ID` 和 `Event_ID` 语义的唯一所有者。M07 只能引用定义并创建 instrumentation ticket；发现语义需要改变时返回 M05。M08 只实现已批准定义。
- M09 记录独立验证结果，不替产品负责人决定。
- M11/M12 记录观测或实验结果及建议决定。
- M13 记录学习候选、反证和后续动作。

完整 Handoff 继续包含：

```text
- Artifact: 权威产物路径、版本或 hash。
- Facts / Decisions / Assumptions / Open questions。
- Decision lineage: 当前有效 ID、引用和未关闭项。
- Gate state: 状态、证据和失效条件。
- G0 data scope: 已批准的数据、来源、时间窗和用途。
- R3 state: 动作、对象、范围、授权和过期状态。
- Verification level: dry-run、fixture、本地 smoke、只读或已授权真实动作。
- Not executed: 未执行事项及原因。
- Next safe action: 唯一下一安全动作。
```

不得用固定行数摘要替代完整 Handoff。可增加便于阅读的索引，但索引必须指向权威 Axx。

## 公共数据结构

### 产品决策图

产品决策图由九类实体和显式边组成。推荐的项目内 ID 格式如下；项目已有等价 ID 规范时可以复用，但必须保持类型可区分、项目内唯一和内容修订后仍可追踪。

| 实体 | 推荐 ID | 语义所有者 | 最小约束 |
| --- | --- | --- | --- |
| Outcome | `OUT-001` | M04 | 希望改变的用户或业务结果；可以确认 A00/A01 已有结果，但不能用功能交付数量代替结果 |
| Opportunity | `OPP-001` | M03 | 基于证据形成的机会假设；必须引用一个或多个 `Evidence_Ref` |
| Candidate | `CAN-001` | M04 | 针对一个或多个机会的候选方案；允许并存多个候选，并与 no-build/current-alternative 比较 |
| Hypothesis | `HYP-001` | M04 | 候选成立所依赖的可证伪机制或前提；`Priority: riskiest` 表示当前最大未知假设，不另建无 ID 的 assumption 节点 |
| Test | `TST-001` | M06 或 M12 | 验证一个或多个 `Hypothesis_ID` 的最小原型、研究或实验；M06 与 M12 不复用同一个 ID 表示不同测试 |
| Slice | `SLC-001` | M07 | 实现一个或多个已批准 Candidate/Spec 的端到端切片；不能与 Test 混为同一实体 |
| Metric | `MET-001` | M05 | 测量 Outcome、Opportunity、Hypothesis 或安全护栏的语义定义 |
| Event | `EVT-001` | M05 | 为 Metric 或诊断提供输入的行为/系统事件；不能与 Metric 混为同一实体 |
| Decision | `DEC-001` | 现有决定者或 Gate | 记录针对一个或多个实体的产品、设计或 Gate 决定；Agent 只能提出 `proposed` |

Evidence 使用项目已有来源引用方式。每个 `Evidence_Ref` 至少包含来源、取得日期、适用范围、证据等级和限制，不要求建立新的全局 Evidence 注册中心。

合法边与基数为：

| 边 | 基数与约束 |
| --- | --- |
| `Evidence_Ref -[supports]-> Opportunity_ID` | 进入决策的 Opportunity 至少有一条 `supports` 边；同一 Evidence 可以支持多个 Opportunity |
| `Evidence_Ref -[refutes]-> Opportunity_ID` | 反例使用 `refutes`，不能塞进 `supports`；同一 Evidence 可以反驳多个 Opportunity |
| `Opportunity_ID -[contributes_to]-> Outcome_ID` | M03 阶段可以暂未绑定；M04 完成后，每个进入决策的 Opportunity 至少绑定一个 Outcome，且允许多对多 |
| `Candidate_ID -[addresses]-> Opportunity_ID` | 每个 Candidate 至少对应一个 Opportunity；一个 Opportunity 可以有多个 Candidate |
| `Hypothesis_ID -[applies_to]-> Candidate_ID` | 每个 Hypothesis 至少对应一个 Candidate；跨候选假设可以显式引用多个 Candidate |
| `Test_ID -[tests]-> Hypothesis_ID` | 每个 Test 至少测试一个 Hypothesis；一个 Hypothesis 可以有多个 Test |
| `Slice_ID -[realizes]-> Candidate_ID 或 A05 Spec` | 每个 Slice 至少引用一个已批准 Candidate 或 A05 Spec；一个 Candidate 可以拆成多个 Slice |
| `Metric_ID -[measures]-> Outcome_ID / Opportunity_ID / Hypothesis_ID / safety_guardrail` | 每个 Metric 至少引用一个 Outcome、Opportunity、Hypothesis 或明确安全护栏 |
| `Metric_ID -[derived_from]-> Event_ID` | 需要事件数据的 Metric 至少引用一个 Event；不依赖事件的数据源应明确写出 source of truth |
| `Decision_ID -[governs]-> Entity_ID` | 每个非 `proposed` Decision 至少引用一个实体、权威决定证据和决定者 |

每个实体包含稳定 ID、`rev`、当前语义、创建模块和 `superseded_by`。非实质修订沿用 ID 并递增 `rev`；目标、语义或适用范围发生实质变化时创建新 ID，并将旧实体标记为 `superseded`。不得覆盖旧语义后继续使用旧引用。

Decision 使用以下字段：

```text
- Decision_ID
- Governs: 一个或多个实体 ID
- Status: proposed | approved | rejected | inconclusive | closed-not-applicable | superseded
- Authoritative_decision_ref: Axx 章节、版本或 hash
- Decision_owner
- Gate_or_authorization_ref
- Decision_date
- Expiry_or_invalidated_by
- Evidence_Refs
- Superseded_by
```

合法状态迁移为：

- 新记录默认为 `proposed`。
- `proposed` 可以变为 `approved`、`rejected`、`inconclusive` 或 `closed-not-applicable`。
- `inconclusive` 获得新证据后创建新修订或后继 Decision；旧记录保留，不直接改写成已批准。
- `approved`、`rejected` 或 `closed-not-applicable` 发生实质变化时只能变为 `superseded`，并引用后继 `Decision_ID`。
- `superseded` 是终止状态；不得恢复或静默覆盖。

`approved` 只表示 `Decision_ID` 指定范围内的产品、设计或 Gate 决定。它不表示 G3/G4/G5/G6 自动通过，也不构成本地写入或外部动作授权。没有 `Authoritative_decision_ref`、`Decision_owner`、适用 Gate/授权引用、日期和失效条件时，状态保持 `proposed` 或 blocker。

消费任一 Decision 前必须计算派生有效性 `active`：只有状态为 `approved`、权威引用仍指向当前版本、尚未到达 expiry，且 `invalidated_by` 条件均未发生时才为 active。达到失效时间或命中任一失效条件后，旧 Decision 立即不可消费；下游保持 blocker，并由原决定者创建后继 Decision，或将旧记录标记为 `superseded` 后重新决策。`active` 是消费检查，不是新的 Gate 或可持久化批准状态。

M08 只能消费能追溯到 A05/A07 且匹配 G3/G4 的 `Slice_ID`；缺少权威决定引用、精确 `ALLOWED_FILES` 或其他必要写入范围时保持 draft 或 blocker。

### 证据—机会映射

M03 的最小结构为：

| 字段 | 要求 |
| --- | --- |
| Observation | 观察到的过去行为或可验证事实，不写愿望性回答 |
| Current alternative | 当前使用的替代方案、变通方法或 no-action 状态 |
| Cost and friction | 时间、金钱、认知、流程、组织或切换摩擦；未知时不量化 |
| Affected segment/context | 证据适用的人群、任务和环境 |
| Counterevidence | 反例、不受影响群体和相反解释 |
| Evidence quality | 来源、日期、样本限制、同意和偏差 |
| Opportunity hypothesis | 从证据推导的机会假设，明确标记为推断 |

「过去购买」「明确承诺」或固定频率只能增强证据，不能作为所有场景的硬 Gate。低频、B2B、合规、公共服务和受限用户场景允许使用其他可验证行为证据。

### 产品风险登记

M04 使用以下四项作为产品视角：

- Value：目标用户是否会选择或持续使用。
- Usability：目标用户能否理解并完成任务。
- Feasibility：当前技术、时间和组织约束下能否实现。
- Viability：商业、运营、渠道和组织约束下能否持续。

每项只记录 `Evidence`、`Unknown`、`Consequence` 和 `Cheapest reversible test`。不生成无依据的风险分数。

四项产品风险不能替代以下现有审查：安全、隐私、合规、数据完整性、无障碍、可靠性、可运维性、兼容性和 AI 安全。

### 测量契约

M05 定义语义，M07 形成 ticket，M08 实现，M09 验证，M11/M12 消费。最小字段为：

| 字段 | 要求 |
| --- | --- |
| `Metric_ID` | 指标的稳定 ID 与版本 |
| `Event_ID` | 事件的稳定 ID 与版本；不需要事件的 Metric 可以不创建 Event |
| Purpose | 对应的 Outcome、机会、假设或安全监控用途 |
| Semantic definition | 指标公式或事件含义、包含项和排除项 |
| Trigger and eligibility | 触发时点、行为主体和适用条件 |
| Properties | 最小属性集合、类型、枚举和是否必填 |
| Identity and deduplication | 身份边界、去重键和重复事件处理 |
| Source of truth | 权威来源与允许的时间窗 |
| Privacy classification | 数据分类、同意依据、保留期和访问范围 |
| Quality check | 完整性、有效性、及时性或一致性检查；可执行条件不明时只写查询草案 |
| Owner and version | 建议责任角色、版本和变更记录；未经确认不生成组织承诺 |

默认禁止直接标识符、持久设备 ID、自由文本、用户内容、完整 URL/查询串和精确位置。确需收集时，按现有权限层分别处理：G0 只限定数据目的、对象、字段、时间窗、保留期、访问范围和读取边界；涉及数据模型、隐私、保留或架构取舍时取得 G3；实现代码或埋点时取得 G4，并精确匹配 `ALLOWED_FILES`；生产查询或导出时取得 M11 对象级、未过期的 R3；修改外部 analytics/provider 或采集配置时取得与动作精确匹配、未过期的 R3。任何一层都不能代替其他层。

### Review findings

M05 可在高影响、跨职能或高不可逆规格形成后触发一次预实现评审。M09 可复核对应风险是否关闭。

```text
- Lens: product | design | engineering | data | security | privacy | legal | operations
- Evidence location: 文件、章节、需求或测试位置。
- Finding: 基于材料能够观察到的问题。
- Consequence: 不处理时的具体影响。
- Severity: blocker | major | minor。
- Proposed action: 建议动作，不是批准或自动任务。
- Decision owner: 待确认的决定角色。
- Re-review condition: 关闭 finding 所需的新证据。
```

`0 blocker` 只表示「在已提供材料中未发现 blocker」。它不表示 G3/G4/G5/G6 通过、法律或安全批准、测试完成或可以部署。

### 行动登记

M11/M13 使用同一最小结构：

```text
- Finding_or_Evidence_ID
- Observation
- Causal hypothesis
- Counterevidence / alternative explanation
- Proposed action
- Proposed owner
- Due date or trigger: 未确认时写 pending confirmation
- Verification method
- Destination module
- Status: proposed | accepted | in_progress | verified | rejected | superseded
```

`proposed` 是默认状态。其他状态必须记录确认者、确认时间和 `Evidence_Ref`。状态记录本身不创建 tracker、不发送通知，也不证明对应动作已经执行。

不得把相关性自动写成因果关系，不得归咎个人。负责人、日期、SLA、tracker、模板更新和长期记忆写入均需现有流程中的明确决定或授权。

## 可选分支

### 问卷分支

仅在需要覆盖更大样本、比较分群或验证已形成假设时触发。每个问题必须映射到：

- 待验证假设。
- 预期影响的决定。
- 回答类型和分析方法。
- 诱导、顺序、社会期许和幸存者偏差。
- 样本框、招募方式、同意、隐私和回答质量。

不发送问卷，不虚构回答，不用固定样本量表替代流量、方差、分群和决策风险分析。

### 优先级敏感性分支

仅在 M04 存在多个竞争候选时触发：

1. 列出已知输入、未知输入和假设区间。
2. 分别比较用户价值、目标贡献、风险降低、成本、可逆性和依赖。
3. 识别哪些输入变化会导致排序反转。
4. 输出建议顺序、反对理由和需要补充的证据。

不自动置顶、取消、排期或写入 backlog。安全、合规、事故和外部承诺进入现有人工风险流程，不作为评分捷径。

### Roadmap 分支

仅在 M07 同时包含多个 initiative、共享依赖或资源冲突时触发。输出：

- Milestone 或可验收结果。
- 对应的 thin slice。
- 依赖和关键路径。
- 容量与可用性假设。
- 不确定性与缓冲依据。
- 成功信号。
- 改向、延期或停止的触发条件。

该分支是带假设的交付轮廓，不是工期承诺，也不产生 G4。

## 模块融合

| 模块 | 新增或强化内容 | 下游接口 |
| --- | --- | --- |
| M02 机会与市场调研 | 竞品可迁移分析：事实、目标情境、成立条件、反证、可迁移原则、不可迁移约束 | A02 为 M03/M04 提供证据，不直接产生产品决定 |
| M03 用户研究与问题定义 | 过去行为、替代方案、变通与切换成本、反例、受影响分群；创建 `Opportunity_ID`；可选问卷分支 | A03 输出证据—机会映射 |
| M04 产品策略与范围决策 | 创建或确认 Outcome，将机会绑定到 Outcome，分离 Candidate 与 Hypothesis，比较 no-build/current-alternative，选择最大未知假设，并执行四产品风险和优先级敏感性检查 | A04 输出待验证 `Hypothesis_ID` 和最便宜可逆测试 |
| M05 领域模型与产品规格 | 旅程骨架、异常路径、首个端到端产品切片、测量契约、可选预实现 review findings | A05 形成可观察规格，不把开放问题补成默认需求 |
| M06 原型与 UX 验证 | 原型必须引用标记为 `Priority: riskiest` 的 `Hypothesis_ID` 和具体学习问题 | A06 输出 Accept/Revise/Reject 证据，不以视觉完成度代替学习 |
| M07 架构设计与任务拆解 | walking skeleton、端到端 thin slice、测量 ticket、产品风险追踪；可选 Roadmap | A07 将已批准产品契约转成可执行 ticket 和依赖图 |
| M08 全栈实现与 TDD | 实现并引用已批准的 `Slice_ID`、`Metric_ID` 和 `Event_ID`；不得新增采集字段 | A08 保存实现和验证证据，不产生新产品批准 |
| M09 AI Eval 与质量安全 | 只读核对产品风险、测量语义、review findings 和谱系闭合 | A09 输出 findings 与未验证范围，不自动修复或批准 |
| M11 可观测性与反馈闭环 | 将获准生产观察写入证据和行动登记，必要时返回 M03/M04 | A11 输出事实与建议，不自动读取生产系统 |
| M12 增长与实验 | 复用假设、指标与事件 ID；保留现有实验设计、安全和授权标准 | A12 只给 recommended decision；真实 launch/stop/extend/traffic/flag/publish 仅在 `MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION` 时发生 |
| M13 复盘与 Skill 自进化 | 分离事实、因果假设、反证和行动；候选经验仍需人工晋升 | A13 指向后续模块，不自动创建任务或长期记忆 |
| `prompts/99` 控制器 | 只保证产品决策图随完整 Handoff 传递；若字段不适用则显式关闭 | 不增加路由器、Gate、状态或权限 |

M00、M01 和 M10 不增加产品方法。M08 仅增加接口追踪，不引入新的方法块。若 `prompts/99` 现有 Handoff 已完整覆盖产品决策图传递，消融检查可以删除控制器的新增文字。

## 对话版同步规则

受影响的 `prompts_ask/` 继续遵守每轮一个高信息价值问题的协议。同步时必须满足：

- 普通版中的事实边界、可选分支、停止条件和禁止动作，在对话版中不能弱化。
- 不为填满产品方法表格连续追问低价值问题。
- 能从已获准读取的 Axx 或项目事实得到的信息先读取，不重复询问。
- 用户选择「不知道」时写入 `Open questions`，并说明最小补证据方式。
- 只有信息充分且用户确认生成时，才输出对应 Axx。
- 产品方法名称可以出现在解释中，最终决定仍由证据和现有 Gate 支持。

## 证据与认识论规则

- 框架给出的分类和建议属于 `Inference`，不能标记为 `Fact`。
- 用户访谈、问卷、埋点或实验记录必须保留来源、日期、适用范围和限制。
- 一位受访者、一个竞品、一条日志或一次实验不能自动代表目标市场或全部用户。
- 多个模拟分析视角的一致意见不是独立实证共识。
- 相关性、时间先后和叙事完整性不能单独证明因果关系。
- review、dry-run、fixture、本地 smoke、只读生产检查和已授权真实动作必须分层表述。
- 未执行真实动作时，使用 `Not executed`、`Not launched`、`Production unchanged` 或等价明确状态。

## 安全与权限规则

### 外部研究

- 只有当前 G0 允许的公开来源才可访问。
- 记录 URL、访问日期、来源类型、直接证据和不确定性。
- Sub-agent 只能读取获准的事实池和文件范围，不自动获得浏览、写入、联系用户或外部动作权限。

### 数据与埋点

- 数据最小化是默认值。新增事件或属性必须追溯到 Outcome、假设、安全监控或明确验收。
- SQL 和分析代码在未获真实读取授权时只能作为 `not executed` 草案。
- 真实生产读取继续由 M11 的 G0 数据范围和对象级 R3 控制。

### 实验与发布

- 显著性、提升方向或护栏状态只产生建议决定。
- 真实实验启动、停止、延长、流量修改、feature flag 修改和发布，仅在 `MODE=APPLY + G5=GO/CONDITIONAL + G6=Approved + matching, unexpired R3_ACTION_AUTHORIZATION` 时发生。R3 必须与当前 target、action、effect、credential scope、cost、rollback、verification、idempotency 和 expiry 精确匹配。
- 任一条件不满足或没有真实动作 receipt 时，必须记录 `Not launched / no production verification`，不得写成已上线、已停止或已验证生产行为。

### 人格与权威

- 不以第一人称扮演 Marty Cagan、Teresa Torres、俞军或其他真实专家。
- 可以使用「基于公开框架的产品价值视角」等无人格表述。
- 法务、安全、数据或产品视角只能提出 finding 和升级建议，不能冒充专业批准。

## 消融式删减检查

每个模块初稿形成后，执行一次受限消融：

1. 固定模块目标、产物契约、安全边界、下游输入和当前验收。
2. 从本次新增内容中提取方法、字段、表格、术语和检查项。
3. 每次只移除一个候选。
4. 使用同一组验收检查决策质量、证据追踪、安全边界和下游可消费性。
5. 没有独立价值的候选删除；与现有规则重复的候选合并；承载必要边界的候选保留并记录依据。

以下项目不能作为单独保留理由：方法知名、仓库 star 较多、表格更完整、文字更多或结构更像专业流程。

以下项目不能作为单独删除理由：字段较多、文档较长或界面显得复杂。若字段承载授权、隐私、失败语义、证据等级或必要交接，则必须保留。

## 文件范围

设计批准后的实施计划可以修改以下范围：

### 研究与说明

- 新增 `全栈开发Prompt Chain/08-PM-Skill-2.0核心工作流评估与融合.md`。
- 更新 `全栈开发Prompt Chain/report-source.md`。
- 更新 `全栈开发Prompt Chain/05-GitHub候选与替代审计.md`。
- 更新 `全栈开发Prompt Chain/03-AI产品全生命周期映射.md`。
- 更新 `全栈开发Prompt Chain/04-模块化Skills工作流.md`。
- 更新 `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`。
- 仅在需要增加入口时更新 `全栈开发Prompt Chain/README.md`。

### 普通 Prompt

- 更新 M02–M09 中实际需要的模块，以及 M11–M13。
- M08 只允许增加已批准切片和测量 ID 的实现追踪。
- M09 只允许增加只读验证职责。
- M10 不修改。
- `prompts/99` 只允许增加产品决策图传递兼容规则；消融后若无独立价值则不修改。

### 对话 Prompt

- 同步修改普通版最终实际变更的 M02–M09、M11–M13 对话版。
- 不创建 M00 或 `prompts/99` 的对话版。
- M10 不修改。

最终实施计划必须给出精确文件清单。不得使用范围表达式作为实际写入授权。

## 明确不在范围内

- 不安装或 vendoring `SpaceZephyr/pm-skills`。
- 不修改 Codex、Claude Code、DeepSeek Harness/DSH Desktop 或 Cursor 的用户级和项目级配置。
- 不复制专家人格、原始提示词、HTML 模板、评分表或 PRD 模板。
- 不新增依赖、Skill、Hook、MCP、Agent、数据库、脚本运行时或外部服务。
- 不修改现有 Gate、R3、部署、生产读取、实验启动或长期记忆规则。
- 不执行用户访谈、问卷发送、客户联系、生产查询、tracker 写入、实验或部署。
- 不修改 `全栈开发Prompt Chain.zip` 或其他压缩包。
- 不清理现有 workspace 外快照，除非单独确认其来源和恢复价值。

## 实施前置条件

当前 workspace 不是 Git repository，无法使用 commit 或 Git diff 作为恢复与审查证据。实施必须使用逐文件 hash、精确 preimage、目标清单、受保护文件清单和独立只读审查。

此前审计发现部分候选 Markdown 文件存在两种读取结果。直接 pathname 读取报告的大小比 `/bin/cat` 可读流多 4096 bytes；该差异尚未解释或规范化。本次新增的设计文档也出现同类差异，因此正式 Chain 文件不能在诊断完成前继续写入。

为避免读取视图的含义因工具不同而变化，后续计划固定使用以下定义：

- `pathname_size`：`/usr/bin/stat -f %z "$path"` 的十进制结果。
- `pathname_sha256`：`/sbin/sha256sum "$path"` 输出的首列。
- `cat_size`：`/bin/cat "$path" | /usr/bin/wc -c` 去除外围空白后的十进制结果。
- `cat_sha256`：`/bin/cat "$path" | /sbin/sha256sum` 输出的首列。

四个值都必须记录，不能将 pathname hash 与 cat hash 混称为同一字节流。文件只有在 `pathname_size == cat_size` 且 `pathname_sha256 == cat_sha256` 时才视为两种读取一致。

Manifest 使用相对于 `/Users/lute/Project/vibecoding_config` 的 UTF-8 POSIX 路径，不带 `./`。只接受 regular file；遇到 symlink 或其他文件类型立即停止。路径按 `LC_ALL=C` 字节序排序，每条记录序列化为：

```text
relative_path NUL pathname_size NUL pathname_sha256 NUL cat_size NUL cat_sha256 LF
```

完整 manifest 的 SHA-256 是上述二进制记录串经 `/sbin/sha256sum` 计算的结果。目标 manifest、受保护 manifest、压缩包 hash 和实施计划 hash 分开保存，不用一个聚合值掩盖单文件差异。

正式修改异常文件前必须单独完成以下安全门：

1. 在实施计划中列出精确目标文件，不使用范围表达式代替 allowlist。
2. 使用上述四值协议生成目标和受保护 manifest，确认一致文件与异常文件。
3. 在 workspace 外创建不可覆盖的逐文件 preimage。备份方法必须先在隔离目录证明可以恢复 pathname 和 cat 两种读取结果；只能恢复 cat 流的方法不足以证明异常文件可完整回滚。
4. 保留现有 `/private/tmp/vibecoding-ablation-pass-20260902-c58402c5`，不得覆盖或删除。
5. 向用户提交精确的规范化对象、字节来源、方法、失败停止条件、回滚方式和复验命令。
6. 取得单独授权后才规范化或修改异常文件。若无法构造同时保留两种读取结果的 preimage，则保持阻塞，不执行规范化。

未取得该授权时，可以保存本设计文档和后续实施计划，但不能修改存在差异的正式 Chain 文件。本设计文档自身也必须在最终规范化范围中单独列出，不能把当前可读内容误报为字节一致。

## 验证设计

### 结构检查

- 产品决策图只定义一次，模块文件只投影本模块字段。
- 每个普通 Prompt 和对应对话 Prompt 的边界、字段、停止条件与禁止动作一致。
- 不新增 M14、新 Gate、第二个控制器或新的公共产物编号。
- M00、M01 和 M10 保持不变。

### 内容检查

- 每个新增字段都能追溯到已确认价值缺口。
- 不出现专家第一人称扮演、固定 RICE/ICE 分数、通用样本量、自动上线或自动排期指令。
- `0 blocker`、统计结果和 review finding 不被写成批准或真实动作。
- 测量契约包含目的、最小化、隐私、保留、访问、身份去重和质量检查边界。
- M12 保留当前 assignment、eligibility、exposure、MDE 输入、guardrails、SRM 和 R3 约束。

### 来源检查

- `report-source.md` 是来源状态的单一事实源。
- 所有 `pm-skills` 仓库引用固定到提交 `4c486c7a532de8890e88036533e0a48d578087ed`；X 引用保留 URL、访问日期和无法完整验证正文的状态。
- 文档明确区分 X 帖子、无法完整取得的 X Article 和可审计仓库快照。
- 不把 README 的 License 声明写成已经由根目录 License 文件验证。

### 文件与恢复检查

- 修改前后保存目标文件和受保护文件 manifest。
- 压缩包 hash 保持不变。
- 不覆盖用户并发改动或未知修改。
- 修改后的 `pathname_*` 与 `cat_*` 读取必须一致；若验证工具仍报告差异，立即停止，不声明完成。

### 独立审查

至少执行三类只读审查：

1. Spec review：检查方法价值是否正确投影到对应模块。
2. Safety review：检查 Gate、R3、隐私、生产与外部动作边界是否保持。
3. Ablation review：删除重复、仪式化或不改变决策的新增内容。

Critical 或 Important finding 未关闭时，不进入正式写入或完成声明。

## 验收标准

设计实施后必须同时满足：

1. 现有 Chain 仍只有 M00–M13、G0–G6、R3 和 A00–A13。
2. M03–M13 需要产品判断的模块可以通过稳定 ID 追踪证据、机会、假设、测试、测量和决定。
3. 问卷、优先级、review、测量和 Roadmap 只在满足触发条件时出现。
4. 产品四风险没有覆盖或弱化安全、隐私、合规、无障碍、可靠性和 AI 安全。
5. 普通 Prompt 与对话 Prompt 的事实边界和安全语义一致。
6. 外部研究、生产读取、实验、tracker、发布和长期记忆权限没有扩大。
7. 没有原文复制、真人人格扮演、伪精确评分或自动批准语义。
8. 新增内容经过消融式删减检查，保留项均有决策、证据、安全或交接依据。
9. 所有修改文件通过 Markdown、引用、目标范围、hash 以及 `pathname_*`/`cat_*` 读取一致性检查。
10. 最终报告区分静态文档检查、实际命令验证和未执行的真实外部行为。

## 后续步骤

1. 用户复核本设计文档。
2. 设计确认后，使用 `writing-plans` 生成精确、可审查的实施计划。
3. 计划中先完成目标文件清单和字节差异审计。
4. 对异常文件的规范化取得单独授权。
5. 按任务分阶段修改、同步对话版、执行消融并独立审查。
6. 全部验证通过后，再报告正式 Chain 已完成融合。
