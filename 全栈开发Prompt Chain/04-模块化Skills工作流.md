# 模块化 Skills 工作流

## 1. 执行契约

本工作流把 M00–M13 作为可恢复的状态机。模块之间通过 A00–A13 传递事实、决策和证据，不通过隐含对话状态传递授权。

`[08-AI-Native-SDLC控制面规范.md](08-AI-Native-SDLC控制面规范.md)` 是控制面语义的单一真相源：它规定每个非琐碎 artifact 的 Control Contract、状态、人类责任、证据和回退含义。本文件只把该规范应用到模块流程，不建立第二套 artifact 或审批门。

默认按「单一责任链」推进：一个主责任 Agent/人类整合者负责当前 Axx 的完整性、衔接和回退。只有输入、文件、状态和验收真正独立的只读研究、测试、审计或隔离切片可以并行；每条结果都必须回写到同一个 Axx，不得让共享接口、数据迁移、权限、核心架构或生产动作并行写入。

每次运行先确定：

| 变量 | 默认值 | 作用 |
|---|---|---|
| PROJECT_ROOT | 未知时停止仓库写入 | 约束读取、修改和验证范围。 |
| PRODUCT_OR_TASK | 无法从上下文确定时询问 | 定义本轮唯一目标。 |
| MODE | PLAN | PLAN 只做读取、分析和获准的文档产出；APPLY 才允许获批的本地可逆修改。 |
| EXTERNAL_EFFECTS | DENY | 任何外部或破坏性动作默认禁止。 |
| DATA_BOUNDARY | 不读 secret、PII、.env 和生产数据 | 约束日志、反馈、trace、session replay 和研究材料。 |
| TIME_OR_BUDGET | 未知 | 不伪造预算；提出有依据的最小范围。 |
| KNOWN_ARTIFACTS | 空 | 使用前核验存在性、状态、新鲜度和 superseding 关系。 |
| HUMAN_RESPONSIBILITY | 由风险和任务决定 | `Delegate`、`Review` 或 `Own`；R3 默认为 `Own`。 |

已安装 Skill 的使用规则：

1. 使用 exact identifier，并遵守其 user-invoked/model-invoked 语义。
2. Skill 未安装时按本文件的步骤执行，不声称已调用。
3. 同职责采用一主一辅；不同时加载多个重叠的大型规则包。
4. 原仓高副作用步骤必须由本工作流的门和边界覆盖；冲突时以更严格规则为准。
5. 目标系统 15 个 Skill 目前只有 static-baseline/contract 证据；不能把文档存在写成行为有效。

## 2. G0–G6 审批门

| Gate | 必须回答的决定 | 未通过时的安全状态 |
|---|---|---|
| G0 数据与任务边界 | 项目、目标、数据、隐私、成本、允许读取和允许动作是什么？ | 只读公开资料与不含敏感数据的本地事实。 |
| G1 问题证据 | 目标用户、痛点、现有替代、频率/严重性和反证是否足够？ | 继续 M02/M03，不承诺解决方案。 |
| G2 产品承诺 | 范围、成功指标、非目标、优先级和责任人是否明确？ | A04 保持 draft，不进入正式规格。 |
| G3 架构与风险 | 数据模型、权限、安全、依赖、兼容、迁移和回滚是否可接受？ | 只做 prototype、ADR 备选和 dry-run，不实施高影响改动。 |
| G4 实现授权 | 当前 slice、目标文件、依赖、测试和允许的本地写入是否明确？ | 保持 plan，不改代码、配置、依赖或 tracker。 |
| G5 上线与生产 readiness | 目标环境、发布对象、凭据入口、回滚、观测、窗口和责任人是否就绪？ | 只做 readiness、plan、preview 或 dry-run。 |
| G6 实验/晋升 design | 实验设计、流量、停止规则、隐私、Memory/Skill 候选的试用和人工晋升是否批准？ | 只生成实验计划或规则候选，不 launch、publish、adopt。 |

Gate 记录在相应 artifact 的 Decisions 中，并带批准对象、范围、日期和失效条件。仓库、分支、环境、数据集、接收方、成本或副作用变化后，原批准失效。

### 2.1 永不自动执行的动作

本 Chain、任何 Skill、MCP、Hook 或 Subagent 都不得自动执行以下动作：

- commit、push、merge、rebase continue、tag 或 release；
- 创建、评论、改标签、认领、关闭 Issue/PR；
- 读取、回显、生成或写入 secret、token、cookie、密码、私钥或 .env 内容；
- deploy、项目链接、云资源创建、migration/cutover；
- 生产配置、feature flag、流量、数据、事故状态或服务的写操作。

G5/G6 的通用“通过”只证明 readiness/design 已达到人工决策条件，不是执行授权。真实外部动作必须单列 `R3_ACTION_AUTHORIZATION`，包含 Target、Action、Expected effect、Credential scope（不含值）、Cost、Rollback、Verification、Idempotency/duplicate guard、Expiry；它只授权清单内、当次且未过期的动作。缺少该记录时，真实动作必须另行取得授权。Secret 值由人通过平台安全入口输入，Agent 只处理名称和引用。

## 3. 通用产物与恢复规则

每个 Axx 至少包含规范定义的 `Control Contract`、Metadata、Facts、Decisions、Assumptions、Open questions、Risks and reversibility、Acceptance evidence 和 Handoff。Evidence level 只能写实际达到的 static、dry-run、fixture、local-smoke、external-read 或 real-side-effect。未知授权、预算、平台能力或验证范围必须明确写 `Unknown`、`Not authorized` 或 `Not run`，不得由下游补全。

消费上游 artifact 前检查：

1. 文件存在，Status 是可消费状态。
2. 输入版本、日期和目标仍与当前工作区一致。
3. 没有更新的 artifact 或代码事实使其 superseded。
4. Facts、Decisions、Assumptions 和 Open questions 没有混写。
5. 所需 Gate 的对象与当前动作一致。

任一条件失败时，回到产出该 artifact 的模块修订；不要在下游静默补假设。

| 模块 | UI 跨模块契约 |
|---|---|
| M05 | 定义可观察的 UI 约束与验收。 |
| M06 | 验证高价值 UI 不确定性及其证据。 |
| M07 | 传递 A05/A06 约束和例外，不重新设计。 |
| M08 | 按约束实现，并在目标状态同屏复核。 |
| M09 | 独立审查并要求可追溯证据。 |

### 3.1 条件叠加层：故事追踪与编译式交付

该叠加层沿用 A00–A13、G0–G6 与 Control Contract，不建立第二套流程；完整契约见 [09-故事线驱动与编译式交付模式.md](09-故事线驱动与编译式交付模式.md)。

- 产品决定依赖可观察的用户转变时，在 M03–M05 追踪故事假说、反证和 `SH -> FR/RISK -> AC`；故事本身不是证据。
- M06 按最大不确定性选择 capability spike 或 UI prototype；前者用 TUI/CLI + fixture 验证 Agent 与工具能否闭环，不能替代 UX 证据。
- 两个以上真实目标共享同一语义，或已有跨目标漂移时，才在 M07–M09 叠加 shared transform、跨目标契约与目标矩阵。单目标只有存在不能由简单配置表达的平台/协议/provider 差异时才使用窄 adapter，且必须先有 native validator；它不自动触发 shared transform 或目标矩阵。
- M11 若观察与预期转变冲突，保留冲突并回 M03 或 M05。
- M13 只把稳定重复模式整理为 adapter + trap + oracle + smoke 候选包，不自动晋升 Skill。

## 4. M00–M13 模块工作流

### M00 全局上下文与流程控制

- **入口**：任何新请求、跨会话恢复、目标变化或阶段切换。
- **推荐组合**：project-profile 为 Core；ask-matt 路由和 handoff 脱敏方法为 Supplement。
- **只读步骤**：读取用户最新指令、AGENTS/CLAUDE、就近项目规范、现有 Axx、工作区状态和允许的数据源；识别请求属于 idea、existing feature、bug/incident、post-launch iteration 或轻量任务。
- **审批门**：先完成 G0；G0 未确定时不读取 secret、PII、.env、生产数据或外部私有状态。
- **执行步骤**：选择 MODE、风险等级 R0–R3、人类责任级别、当前模块、权威 artifact、允许文件和唯一下一安全动作；建立或刷新 A00 的 Control Contract。仅在用户要求文档产出时写 A00。
- **产物**：A00-context-pack.md。
- **验收**：目标、项目根、模式、数据边界、外部副作用、人类责任、已批准 Gate、权威输入、冲突、开放风险、当前证据层级和 next action 全部明确。
- **停止/回退**：目标或根目录无法确定、输入互相冲突、数据边界不明时停止；恢复时重新核对文件，不盲信旧摘要。
- **下一模块**：新产品到 M01；existing feature 到 M03/M04；bug/incident 到 M11 或 M08；post-launch 到 M11；明确小改可到 G4/M08；只读问答可结束。

### M01 项目初始化与治理

- **入口**：新项目、治理文件缺失，或平台、权限、tracker、测试、Skill 配置发生变化。
- **推荐组合**：project-profile、writing-for-agents；setup-matt-pocock-skills 和 hook 方法只作 Adapter。
- **只读步骤**：读取项目说明、技术栈、目录、Git 状态、现有 hooks、CI、测试命令、tracker/domain 约定、已安装 Skill 清单与许可证；不读取 .env 内容。
- **审批门**：G0 覆盖项目与数据；修改依赖、hooks、全局配置或 agent 指引前通过 G3/G4。
- **执行步骤**：先起草 charter、风险表、平台调用方式、文档布局和验证命令；获批后只修改列明的本地文件。当前任务需要局部理解时，可在 A01 中提供按需的 **Agent-ready module pack**：目标模块、真实入口/调用方、允许文件、现有命令与 mock、接口/不变量、依赖服务、失败/恢复、验证和 owner。每项必须来自仓库事实或受控决定；它不创建新的项目画像 schema。默认不创建 tracker labels、不安装包、不改全局设置。
- **产物**：A01-project-charter.md。
- **验收**：facts/decisions/not-applicable 有受控来源；角色、数据、权限、技术栈、验证、Skill 版本和退出方式可追溯。
- **停止/回退**：发现用户未提交改动与目标文件重叠、依赖许可证不明或全局影响未批准时停止；回退只撤销本轮可识别修改。
- **下一模块**：idea 到 M02；已有明确机会证据可到 M03；纯工程维护可在 G4 后到 M08。

### M02 机会与市场调研

- **入口**：产品 idea、市场/替代方案不明，或 G1 证据不足。
- **推荐组合**：technical-research 为 Core；research 的一手来源原则为 Supplement；新增 opportunity-research。
- **只读步骤**：读取 A00/A01、既有产品资料和日期化一手来源；分别调查目标人群、现有替代、约束、购买/采用行为、竞争与反证。
- **审批门**：G0 明确网络、成本和数据源；本模块只为 G1 提供证据，不自行通过 G1。
- **执行步骤**：建立 claim→source ledger，标出事实、推断、不确定项、来源日期、矛盾和样本偏差；达到停止条件后形成机会判断。
- **产物**：A02-opportunity-brief.md。
- **验收**：每个关键 claim 有可访问来源；替代方案和反对证据存在；没有用 stars、搜索排名或名人背书替代质量/需求证据。
- **停止/回退**：来源不足、关键页面不可核验或结论只靠二手转述时降级置信度并停止承诺；需要用户证据时转 M03。
- **下一模块**：M03；若证据否定机会，则记录 no-go 并到 M13。

### M03 用户研究与问题定义

- **入口**：A02 的机会、现有反馈、issue、支持记录，或待确认的问题陈述。
- **推荐组合**：product-discovery 为 Core；grilling、grill-with-docs、to-questionnaire 和 domain-modeling 为 Supplement。
- **只读步骤**：读取已有研究、反馈、行为数据定义、相关代码与领域词汇；去重来源并区分直接用户证据、代理证据和团队假设。
- **审批门**：G0 规定 PII、录音、日志、反馈和外部联系范围；对外发送问卷或联系用户不属于默认权限。完成证据评估后请求 G1。
- **执行步骤**：在会话内逐项澄清 decision；需要外部专家时只生成本地 questionnaire 草稿；综合用户、场景、痛点、替代、频率、严重性、反例和未知项。
- **产物**：A03-problem-evidence.md。
- **验收**：问题从用户视角表达；证据与假设分开；样本、时间、来源、反例和缺口可见；G1 的批准或拒绝被记录。
- **停止/回退**：样本不足、用户与购买者混淆、PII 不能安全处理或相互矛盾的证据未解释时停止；回 M02 或继续研究。
- **下一模块**：G1 通过后到 M04；未通过留在 M02/M03。

### M04 产品策略与范围决策

- **入口**：G1 通过的 A03，或新鲜且已批准的等价问题证据。
- **推荐组合**：product-discovery、specification；wayfinder 的 destination/fog/frontier 作 Supplement。
- **只读步骤**：读取 A02/A03、项目约束、能力边界、已有路线图和指标定义；检查问题是否已有实现或既往拒绝。
- **审批门**：G2 决定目标结果、优先级、范围、非目标、成功指标和责任人。
- **执行步骤**：提出至少一个可行方案和 no-build/低成本替代；比较直接与第二序效应；把未决问题留在本地 decision map，不写真实 Issue。
- **产物**：A04-product-strategy.md。
- **验收**：目标用户、价值主张、成功/护栏指标、范围、非目标、取舍、停止条件和下一决策明确；指标基线未知时明确写未知。
- **停止/回退**：多个方案会实质改变产品、权限、UX 或成本而用户未选择时停止；证据被推翻时回 M03。
- **下一模块**：G2 通过后到 M05；大型未知可用本地 wayfinder 子循环。

### M05 领域模型与产品规格

- **入口**：已通过 G2 的 A04。
- **推荐组合**：domain-modeling、specification 为 Core；to-spec 模板为 Adapter。
- **只读步骤**：读取 A01–A04、CONTEXT/ADR、代码接口、schema、API、相关 tests 和项目 vocabulary；确认已有能力与约束。
- **审批门**：G2 必须有效；涉及 schema、auth、公开 API、数据迁移或核心 UX 的决策先标为 G3 待审，不在规格中假定获批。
- **执行步骤**：定义领域对象、状态、invariant、错误、用户故事、验收、测试 seam、非目标和 traceability；只写本地规格。
- **产物**：A05-product-spec.md。
- **验收**：每个需求能追到问题证据，每项验收能追到需求；术语一致；错误、权限、数据和 out-of-scope 明确；不存在自动 tracker 发布。
- **停止/回退**：领域术语冲突、关键状态未定义或高影响决策缺 owner 时停止；产品范围变化回 M04。
- **下一模块**：存在高不确定交互或逻辑时到 M06；否则到 M07。

### M06 原型与 UX 验证

- **入口**：A05 中有需要用可运行 artifact 回答的一个明确问题。
- **推荐组合**：safe-prototyping 为 Core；prototype 方法和 browser-e2e/axe/Lighthouse 为 Supplement/Adapter。
- **只读步骤**：读取目标问题、现有 router、component system、design tokens、可访问性约束和相邻代码；选择 fixture，不读取生产数据。
- **审批门**：隔离目录或 route 的本地 R1 写入通过 G4；触碰真实 route、依赖、schema 或共享组件前通过 G3/G4。
- **执行步骤**：一次只验证一个问题；创建最小 logic artifact 或 2–3 个 UI 方案；运行可行的本地 browser、keyboard、可访问性和性能 smoke；把决策而非完整 demo 折回规格。
- **消融职责**：在原型决策前，只从本轮原型逐项删减不能回答学习问题的交互、流程、容器和 UI 元素，并以相同任务及 accessibility/usability 复验；记录 remove/defer/retain 与依据，不授权生产或外部写入。
- **产物**：A06-prototype-evidence.md，以及获批范围内的隔离 prototype。
- **验收**：问题、方案、fixture、观察、限制、选择和逐项删减证据可追溯；prototype 明确标为非生产；没有自动 branch、commit、Issue 或外部发布。
- **停止/回退**：原型开始承载生产逻辑、需要真实凭据/数据、或验证问题发生漂移时停止；删除或隔离本轮 artifact，回 M05 修订。
- **下一模块**：结论改变规格时回 M05；稳定后到 M07。

### M07 架构与垂直切片

- **入口**：新鲜 A05 和可选 A06。
- **推荐组合**：codebase-design、architecture-review、vertical-ticketing 为 Core；to-tickets、setup-ts-deep-modules 方法作 Supplement。
- **只读步骤**：读取架构、依赖、CONTEXT/ADR、tests、CI、当前 diff 和 Git 状态；定位现有 seam、复用点、blast radius 与回滚路径。
- **审批门**：G3 批准数据、权限、安全、兼容、依赖和架构取舍；G4 批准下一 implementation slice、文件和验证范围。
- **执行步骤**：形成 architecture options、选定方案、ADR 草案和 tracer-bullet tickets；wide refactor 用 expand–migrate–contract；默认本地 ticket 文件，不创建 tracker Issue。每个进入 M08 的 ticket 必须投影 A05/A07 的持久行为契约、反馈可达性和当前 parallel frontier；缺少真实入口、接口/不变量、允许范围、失败/恢复、验证或整合 owner 时，标记缺口而不是用通用建议填补。
- **消融职责**：在 G3/G4 前逐项审查本轮新增的 abstraction、interface、seam、adapter、layer、dependency、config 和 ticket；仅在同一需求/不变量/失败模式/风险 trace 不成立时 remove/defer，保留必要 seam。
- **产物**：A07-architecture-and-tickets.md。
- **验收**：接口、invariant、failure boundary、security、migration、rollback、observability 和架构/ticket 删减依据齐全；每个 ticket 可独立 demo/verify，blocking graph 无循环。
- **停止/回退**：无法保持每个 slice 可验证、依赖许可不明、迁移无回滚或 G3 未通过时停止；回 M05/M06 或保留备选。
- **下一模块**：G3/G4 通过后按 frontier 到 M08。

### M08 实现、TDD 与调试

- **入口**：G4 明确批准的一个 A07 ticket，或具有等价验收的小型改动/缺陷。
- **推荐组合**：implementation-orchestration、tdd、systematic-debugging 为 Core；原仓 implement/diagnosing-bugs 只取方法。
- **只读步骤**：读取指令、ticket、spec、架构、相关实现/tests、Git 状态和用户改动；先定位现有实现、工具函数和 test seam。
- **审批门**：G4 绑定当前 slice、目标文件、dependency、命令和本地副作用；commit、push、merge/rebase 和 Issue 不包含在 G4。
- **执行步骤**：功能按一个 test→最小实现循环；bug 先建立 red-capable、deterministic、fast、agent-runnable feedback loop，再最小复现、可证伪假设、单变量 probe、fix 和 regression test。仅当当前任务有完整 Autonomy Envelope 且属于 R0/R1 时，才可在明确范围内连续执行「最窄反馈 → 最小修改 → 重跑同一检查 → 记录证据」；遇到新依赖、架构/API/schema/auth/迁移、范围外文件、外部动作、敏感数据、连续不收敛或证据变弱时停止并交接。
- **消融职责**：每个 slice 首次可信 green 后，只对当前 diff 逐项删减候选并立即复验最窄验收；失败、证据变弱或风险上升即 retain，随后运行最终相关回归，不扩大 G4 文件或 dependency 范围。
- **产物**：A08-implementation-report.md，以及获批的代码/tests 修改。
- **验收**：验收项逐条对应新鲜命令输出；可行时有 red→green、首次可信 green 后逐项删减及最终相关回归证据；无 debug 残留、无无关重构、无自动 commit。
- **停止/回退**：无稳定复现、不存在可测试 seam、第三次验证仍失败、范围扩张或碰到未授权用户改动时停止；保留失败证据，回 M07 或请求数据/环境。
- **下一模块**：M09；incident 修复也必须进入 M09。

### M09 AI Eval、质量与安全

- **入口**：A08 的 release candidate，或任何 AI、auth、数据、依赖、用户可见行为变更。
- **推荐组合**：two-axis-code-review 为 Core；architecture-review、ai-evaluation、security-change-review、browser-e2e、performance-accessibility 为补充。
- **只读步骤**：固定 review base；读取 diff、commit list、A05/A06/A07/A08、standards、威胁面、依赖、模型/提示/数据集版本和既有测试。
- **审批门**：新增本地测试或 fixture 仍受 G4；外部扫描服务、真实账号 browser test 或生产数据必须回到 G0/G5。
- **执行步骤**：分别做 Standards 与 Spec review；再按风险选择 AI Eval、安全、依赖/secret scan、E2E、性能和可访问性检查。优先离线数据和本地 server。作者验证与独立审证必须在上下文、证据方法、审查者或 CI 中至少有一项实质分离；否则记录为 `Not independent`，不能作为 R2/R3 放行依据。
- **消融职责**：只读核对 A07/A08 与固定 diff 的 baseline、candidate、trace、decision、verification 和 limitations；无证据记 finding/Unverified scope，不自动修复。
- **产物**：A09-quality-evidence.md。
- **验收**：每个轴独立给 finding；消融证据与实际 diff 一致或明确为 finding/Unverified scope；高风险 finding 已关闭或明确阻塞；命令、数据集、版本、阈值、失败样例和未测范围可复现；不把静态 scan 写成安全证明。
- **停止/回退**：review base 不可解析、diff 为空但目标要求变更、测试环境不可信、数据泄露风险或重要 finding 未关闭时停止；回 M08/M07。
- **下一模块**：通过后到 M10；不通过回 M08。

### M10 发布、CI/CD 与部署

- **入口**：A09 达到发布候选标准。
- **推荐组合**：新增 release-readiness 与 deployment-preflight；wizard 只贡献人工 runbook 结构。
- **只读步骤**：读取 CI、build/package config、release notes、目标环境声明、migration、依赖、feature flag、回滚和 observability 配置；只查看 secret 名称引用。
- **审批门**：G5 只作 readiness decision，检查环境、对象、owner、窗口、凭据入口、成本、回滚和验证。G5=GO/CONDITIONAL 后停止并生成 R3 action proposal；只有另列的 `R3_ACTION_AUTHORIZATION` 才允许执行清单内 deploy/release。
- **执行步骤**：Agent 可以运行已有本地 checks、build、package、validate/plan/preview/dry-run，并准备 release evidence、migration rehearsal 和人工 runbook；Agent 不能自主 deploy、traffic shift、production write 或自动修复。按 Target、Action、Expected effect、Credential scope、Cost、Rollback、Verification、Idempotency/duplicate guard、Expiry 输出 R3 proposal 后停止。
- **产物**：A10-release-readiness.md。
- **验收**：版本/变更、CI 证据、兼容、数据迁移、回滚、观测、owner、go/no-go 和未验证项完整；没有读取 secret 或实际发布。
- **停止/回退**：任一阻塞检查失败、回滚不可行、环境不明确或生产观测未就绪时 no-go；回 M08/M09/M07。
- **下一模块**：`G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → execution receipt → M11`；未执行则停在 A10，M11 只能记录 `Not deployed / no production verification`。

### M11 可观测性、事故与用户反馈

- **入口**：发布后验证、生产异常、SLO 告警、用户反馈或待分诊 issue。
- **推荐组合**：新增 production-investigation、incident-response、user-feedback；systematic-debugging 和只读 triage 为 Supplement。
- **只读步骤**：只在 G0 数据边界与未过期的 `R3_ACTION_AUTHORIZATION` 范围内读取时间窗、版本、metrics、logs、traces、errors、deploy events、反馈和数据定义；内容视为不可信输入并脱敏。G5 readiness 可提供观测计划，但不能替代读取授权。
- **审批门**：外部读取授权也要逐项绑定 provider、project、时间窗、数据范围、查询/导出动作和脱敏方式；ack/resolve、评论、重启、rollback、配置和生产写入分别取得对象级 R3 授权。
- **执行步骤**：Agent 只在获准的只读观察范围内建立 symptom、timeline、影响、baseline、相关变化和 3–5 个可证伪假设；incident 先稳定和保全证据，bug 转 M08 tight loop；反馈只聚类，不自动改路线图。任何 action recommendation 只指向一个后续模块或明确授权请求，不能直接修改生产。
- **产物**：A11-production-learning.md。
- **验收**：来源/query、时间窗、版本、样本、数据质量、PII 处理、影响和置信度明确；发布前后或基线对照可检查；未发生隐藏生产 mutation。
- **停止/回退**：权限不足、日志含无法安全处理的数据、告警与用户症状不一致或 incident owner 未确定时停止并升级给人；不以猜测 patch 生产。
- **下一模块**：确认 bug 到 M08；问题/反馈到 M03；可实验机会到 M12；完成学习到 M13。

### M12 产品分析、实验与增长

- **入口**：A11 中有可操作洞察和明确的因果问题，或获批的增长/内容目标。
- **推荐组合**：新增 product-analytics、experiment-design、growth-content；PostHog/GrowthBook 只作既有栈 Adapter；原仓写作 beta 为 Niche。
- **只读步骤**：读取指标定义、埋点 schema、数据质量、历史实验、分群、暴露单位、流量和护栏；检查幸存者偏差、重复曝光和 novelty effect。
- **审批门**：G6 只决定实验 design：假设、流量、受众、隐私、时长、停止规则和 owner。真实 feature flag 或生产实验写入还必须有 G5 readiness=GO/CONDITIONAL 与单列的 `R3_ACTION_AUTHORIZATION`。
- **执行步骤**：先做离线分析和实验预注册；定义 primary/guardrail metrics、assignment unit、样本依据、decision rule 和异常处理；G6=Approved 后停止，只有 G5 readiness 与 R3 对象级授权均存在时才可 launch。
- **产物**：A12-experiment-decision.md。
- **验收**：假设可证伪；指标与事件有唯一含义；暴露、样本、数据质量、护栏、停止和 keep/iterate/stop 决策完整；不把相关性写成因果。
- **停止/回退**：埋点不可信、样本依据不存在、护栏已恶化、实验会伤害用户或无法安全回滚时停止；回 M11/M04。
- **下一模块**：生产实验走 `G6 → STOP → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → execution receipt → M11`；未 launch 时停在 A12。结论改变产品时到 M04/M05/M07；否则到 M13。

### M13 复盘、Memory 与 Skill 演进

- **入口**：链完成、暂停、失败三次、incident 结束、实验决策完成，或相同模式重复出现。
- **推荐组合**：memory-governance、writing-for-agents 为 Core；新增 retrospective、skill-evolution；AutoResearch keep/discard 方法为 Supplement。
- **只读步骤**：读取 A00–A12、代码 diff、测试、事故时间线、用户纠正、实验和真实运行证据；区分一次性事件与可泛化模式。
- **审批门**：G6 只决定 reject、more-evidence、trial 或 approved-design，不授权写入。长期 Memory、Skill、AGENTS/CLAUDE 或全局规则的实际晋升还需绑定 target files、exact diff、备份/回滚、验证和失效条件的 G3/G4 本地变更授权；外部发布另需 `R3_ACTION_AUTHORIZATION`。
- **执行步骤**：形成事实化复盘；为候选规则记录触发、证据、适用范围、反例、预期行为、trial、eval、过期信号和撤回方式；默认只写候选，不修改长期主数据。
- **产物**：A13-retrospective.md，以及可选但未晋升的候选提案。
- **验收**：事实、推断、不确定项分开；成功与失败都有可追溯证据；候选能被独立试用、评测和撤回；没有自动规则写入或 Git 动作。
- **停止/回退**：只有一次偶然成功、没有反例、证据来自截断输出或会扩大权限时拒绝晋升；需要更多证据则回相应模块设计 trial。
- **下一模块**：G6 通过后先停止在 change proposal；经匹配的本地/外部动作授权和 receipt 后，从 M00 开新一轮。产品机会回 M02/M03，工程改进回 M07/M08。

## 5. 四条组合链

### 5.1 Idea to MVP

M00 → M01 → M02 → M03 → G1 → M04 → G2 → M05 → M06 → M07 → G3/G4 → M08 → M09 → M10 → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → execution receipt → M11 → M13

- M06 只有在界面、逻辑或技术可行性存在实质不确定时执行。
- 资源有限可以缩小样本、功能和 prototype，但不能省略 G2、G3、G5。
- G5 后 Chain 先停止；未发生真实发布时，M11 只能记录“未发布”，不能声称生产验证。

### 5.2 Existing feature

M00 → M03（复用现有反馈）→ M04 → M05 → M07 → G3/G4 → M08 → M09 → M10 → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → execution receipt → M11 → M13

- 新鲜、已批准的 A03–A07 可以复用，但必须记录版本和复用依据。
- 已存在行为先做 redundancy search；不因用户请求而重复实现。
- 若 feature 改变商业目标或目标用户，补走 M02/G1。

### 5.3 Bug or incident

M00 → M11（只读现象与影响）→ M08（tight loop 与修复）→ M09（regression/security review）→ M10（readiness）→ G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → execution receipt → M11（验证）→ M13

- 生产事故先由人类 incident lead 决定稳定、回滚或切流；Agent 不自动操作。
- 没有 red-capable loop、脱敏证据或获准环境时停在 M11/M08，不猜测 patch。
- 无正确 test seam 时回 M07，不能用浅层测试制造信心。

### 5.4 Post-launch iteration

M00 → M11 → M03 → M12 → G6 → STOP → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → execution receipt → M11 分析 → M04/M05 更新 → M07 → G3/G4 → M08 → M09 → M10 → G5 → STOP → R3 proposal → R3_ACTION_AUTHORIZATION → execution receipt → M11 → M13

- G6 只批准实验设计；任何生产 flag、流量或消息还需 G5 readiness 与对象级 `R3_ACTION_AUTHORIZATION`。
- 实验结论必须记录样本、暴露、数据质量、primary/guardrail 指标和停止规则。
- 指标上涨只表示观察结果；因果结论取决于设计、执行和数据质量。

## 6. 停止与恢复

| 情况 | 停止动作 | 恢复入口 |
|---|---|---|
| 上游 artifact 缺失、过期或冲突 | 标为 blocked，列出缺失事实，不在下游补假设 | 回产出该 artifact 的模块 |
| 第三次验证仍失败 | 停止叠加 patch，保存复现、假设和命令证据 | M07 架构审查或 M13 复盘 |
| 外部 mutation 结果不确定 | 不重试，不用新参数重复；先只读查询真实状态和幂等键 | G5/G6 动作级重新审批 |
| 发现 secret/PII | 停止输出和传播，保留脱敏 signal，缩小数据范围 | G0 |
| 生产事故扩大 | 停止非稳定性工作，把决策交给 incident lead | M11 |
| 用户目标或环境改变 | 原 Gate 失效，保留旧 artifact 为 superseded | M00 |
| 运行/实验事实否定问题、规格、架构或实现假设 | 记录触发证据与失效 artifact；选择最小正确回退点 | M03/M04、M05、M07 或 M08 |
| Memory/Skill 候选证据不足 | 返回 more-evidence 或 reject，不写主数据 | M13 trial 或相关证据模块 |

跨会话恢复只需提供 Goal、Current module、Approved gates、Authoritative artifacts、Latest evidence、Open risks 和 Next safe action；Agent 必须再与当前文件和只读状态核对。

## 7. 工作流自检

- M00–M13 均有入口、只读步骤、审批门、执行步骤、产物、验收、停止/回退和下一模块。
- A00–A13 一一对应，不以聊天摘要替代持久 artifact。
- 每个非琐碎 artifact 的 Control Contract 均能说明状态、人类责任、授权、权威输入、证据、未验证范围和唯一下一安全动作。
- G0–G6 的未通过状态和失效条件明确。
- 四条场景链均在真实外部动作前停止并要求对象级授权。
- commit、push、Issue/PR、secret、deploy、production write 没有任何自动路径。
- Skill、MCP、Hook、Subagent 和自然语言调用均不能扩大权限。
