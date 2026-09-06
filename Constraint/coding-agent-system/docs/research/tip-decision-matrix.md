---
title: Coding Agent Tips 原子决策矩阵
doc_type: knowledge
module: coding-agent-system
topic: atomic-tip-decisions
status: stable
created: 2026-08-30
updated: 2026-09-02
owner: self
source: human+ai
---

# Coding Agent Tips 原子决策矩阵

## 目的与判定口径

本矩阵回答两个问题：每条经验是否采用，以及为什么。它把本地 29 个内容文件和 `ref_links.txt` 的 7 个唯一外链拆成独立决策单元；另有用户会话来源 `LOC-030`、`LOC-031`，不改变原始文件审计计数。精确来源行见[本地逐文件账本](local-tip-ledger.md)，外链正文与证据等级见[外链正文账本](ref-links-ledger.md)。

决策值含义：

- **常驻采用**：几乎每个任务都需要，且不能稳定地从仓库推断，进入用户级短核心。
- **路由采用**：有价值但只在特定任务触发，进入项目路由、局部规则或 Skill。
- **条件采用**：只有仓库证据或基础设施存在时启用，不能写成通用默认。
- **改写采用**：保留方法，删除平台臆测、硬阈值、仪式或越权动作后独立重写。
- **排除**：收益缺少证据，或会制造冲突、上下文噪声、安全风险和维护负担。

`静态可达` 只表示相应文件已进入生成/路由契约；`contract-only` 只表示存在评测规格。二者都不等于真实 Codex 或 DSH Desktop 行为已经验证。

## 1. 常驻行为与认识论纪律

| Tip ID | 原子经验 | 来源 | 决策 | 原因 | 落点与验证状态 |
| --- | --- | --- | --- | --- | --- |
| TIP-001 | 根据请求语义区分只读、诊断和实施，不要求所有写入再说一次固定口令。 | LOC-001、003、012、017、019 | 改写采用 | 固定“执行”口令会阻塞明确的 build/change 请求；高风险转折仍须确认。 | `templates/shared/user-core.md`；静态可达，行为未实测。 |
| TIP-002 | 启动时读取适用指令、就近规则、工程规范和长期开发记录。 | LOC-001、003、006 | 常驻采用 | 这是避免遗漏项目事实的低成本入口；不存在的文件必须跳过。 | 用户 core；静态可达。 |
| TIP-003 | 写前先搜索实现、调用点、数据流、配置、依赖和测试。 | LOC-001、002、005、012、REF-006 | 常驻采用 | 可直接减少平行实现、错误 API 和无谓新文件。 | 用户 core；单元测试不证明 Agent 会遵守。 |
| TIP-004 | 区分 Fact、Inference、Decision、Assumption、Open question。 | LOC-001、002、011、REF-003、005 | 改写采用 | 保留证据分层；排除给每句话机械打标签。 | 用户 core、project profile、Memory；静态可达。 |
| TIP-005 | 设计意图、dry-run、fixture、本地 smoke 和真实副作用不得混为一谈。 | LOC-001、011、REF-005 | 常驻采用 | 直接约束虚假完成声明，且不会依赖特定技术栈。 | 用户 core、验证报告；静态检查通过后仍需实测。 |
| TIP-006 | 不基于截断输出、未运行命令或不可用环境宣称完成。 | LOC-001、011 | 常驻采用 | 防止证据链断裂。 | 用户 core；行为未实测。 |
| TIP-007 | 写入前检查版本控制或等价工作区状态；保留来源不明的既有变更。 | LOC-001、010 | 常驻采用 | 多 Agent 与脏工作区下是必要的所有权边界；无 Git 时明确记录限制。 | 用户 core；EVAL-06 为 contract-only。 |
| TIP-008 | 删除、批量覆盖、生产写入、外部发送、付费调用、权限扩大与发布部署需要精确授权。 | LOC-001、010、REF-004 | 常驻采用 | 这些动作不可由普通“实现功能”请求隐含授权。 | 用户 core；自然语言不是强制安全边界。 |
| TIP-009 | 不读取、打印或提交 secrets、token、私钥、凭据与 PII。 | LOC-001、010 | 常驻采用 | 无条件安全不变量；平台 permissions / sandbox 应做确定性补强。 | 用户 core、controls 文档；未做真实权限 smoke。 |
| TIP-010 | 最小、可追溯、可审阅的修改；不顺手清理和全局格式化。 | LOC-001、002、008、010、012、019、021、023、024、REF-001、006 | 常驻采用 | 多个独立来源一致，且可由 diff 和验收行为检查。 | 用户 core；EVAL-02/06 为 contract-only。 |
| TIP-011 | 单次用例不提前建立 Manager、Factory、Registry 等抽象。 | LOC-001、021、023、024、REF-001 | 改写采用 | 保留“需求证据先于抽象”，不把类型名称本身列为禁用词。 | 用户 core；需代表性实现评测。 |
| TIP-012 | 只清理由本次改动造成的 unused / orphan，不清理历史无关问题。 | LOC-001、021、023、024、REF-001 | 常驻采用 | 同时满足完整性与窄 scope。 | 用户 core；EVAL-02/06 为 contract-only。 |
| TIP-013 | 不手改生成物；修改源头并按项目既有流程再生成。 | LOC-001、002 | 常驻采用 | 可防止生成漂移；前提是先确认文件确为生成物。 | 用户 core；静态可达。 |
| TIP-014 | 不手改 lockfile；依赖变更通过项目包管理器产生。 | LOC-001、002、005、008 | 常驻采用 | lockfile 的直接编辑容易制造不可复现状态；不等于默认允许新增依赖。 | 用户 core；静态可达。 |
| TIP-015 | 外部依赖、框架语义、权限和部署行为优先查当前官方资料与仓库既有做法。 | LOC-001、002、REF-002、004、005 | 常驻采用 | 可降低 API/版本幻觉；简单且仓库已有明确先例的改动无需仪式化检索。 | 用户 core、technical-research Skill。 |
| TIP-016 | 非琐碎任务先定义可观察成功条件；完成声明附新鲜验证证据。 | LOC-001、003、021、023、024、REF-001、005 | 常驻采用 | 目标驱动验证比“写了代码”更接近产品完成。 | 用户 core、TDD/评测；真实 Agent 未跑。 |
| TIP-017 | Debug 先复现；根因假说必须预测尚未观察的证据。 | LOC-001、003、005、021、023、REF-001 | 常驻采用 + Skill 深化 | 能区分可证伪根因与事后附会。 | 用户 core、`systematic-debugging`；contract-only。 |
| TIP-018 | 同一路径连续三次仍失败或 patch 相互干扰时，停止叠加补丁并审查系统边界。 | LOC-001、003、014 | 改写采用 | 阈值用于触发重新建模，不用于宣告任务失败或机械终止。 | 用户 core、debug Skill。 |
| TIP-019 | 错误不可静默吞掉；关键失败需可追踪。 | LOC-001、002、005、011、REF-006 | 常驻采用 | 可观测失败优于“看似稳定”的兜底。 | 用户 core；具体日志策略由项目决定。 |
| TIP-020 | 验证按风险扩展：先窄后宽，UI、migration、外部调用使用对应证据。 | LOC-001、005、008、009、021、023、024 | 常驻采用 | 避免小改过度验证和高风险改动验证不足。 | 用户 core、workflow；未跑代表性 fixture。 |
| TIP-021 | 以用户语言汇报，保留路径、API、错误和专有名词原文。 | LOC-001、003、019 | 常驻采用 | 提高可读性，不改变工程语义。 | 用户 core。 |
| TIP-022 | 技术判断不因用户施压而改口；有新证据时公开修正。 | LOC-001、011、REF-005 | 改写采用 | 采用抗谄媚和证据优先；排除“连续同意三次就强制反驳”。 | 用户 core；EVAL-10 为 contract-only。 |
| TIP-023 | 冲突按 authority、scope、evidence、recency 解析，不平均矛盾规则。 | LOC-011、014、REF-005、006 | 常驻采用 | 可处理本地材料中互相冲突的 RIPER 门禁。 | 用户 core；EVAL-10 为 contract-only。 |
| TIP-024 | 对非琐碎设计显式报告目标、约束、不变量、系统边界、失败模式和二阶影响。 | LOC-003、014、REF-007 | 改写采用 | 把第一性原理和系统思维转成可检查产物；不要求展示隐藏推理链。 | 用户 core / architecture Skills；行为未实测。 |

## 2. 项目上下文、文件与技术栈

| Tip ID | 原子经验 | 来源 | 决策 | 原因 | 落点与验证状态 |
| --- | --- | --- | --- | --- | --- |
| TIP-025 | 项目根指令应是路由器，不重复用户级宪法。 | LOC-004、006、022、026、027、REF-002、004、005 | 路由采用 | 减少常驻上下文与多副本漂移。 | `templates/shared/project-core.md`；渲染校验。 |
| TIP-026 | 只有文件存在且与当前任务相关时才读取 project profile、局部规则、controls、Memory 和开发记录。 | LOC-004、006、007、REF-002、005 | 路由采用 | 让可直接复制的根文件不依赖缺失配套，也避免无关加载。 | project core；隔离生成 smoke 已记录于 [`verification-report.md`](../verification-report.md)；真实 Agent 未跑。 |
| TIP-027 | 生成的技术栈模块必须由根 `AGENTS.md` 明确列出路径和触发条件。 | LOC-005、007、008、009、REF-002、004 | 路由采用 | Codex/DSH 不会自动读取任意 `.agents/rules/*.md`；仅复制文件不可达。 | 初始化器 managed routing block；单元测试覆盖。 |
| TIP-028 | 项目画像记录业务/安全不变量、权威入口、联动关系、禁区、DoD、权威资料和局部风险。 | LOC-004、REF-002、003、005 | 路由采用 | 这些是代码通常无法完整推断、却能改变 Agent 决策的隐性知识。 | `.agents/project-profile.md`；结构校验。 |
| TIP-029 | 画像 readiness 按当前任务相关域和风险判断；不相关域可写有来源的 `Not applicable`。 | REF-005；本轮缺陷复盘 | 改写采用 | 强制所有项目填写所有域会诱导伪造事实并阻塞小项目。 | profile 模板和 validator；单元测试覆盖。 |
| TIP-030 | 局部规则放在风险模块附近，并由根路由说明触发范围。 | LOC-004、006、007、REF-002、004、005 | 条件采用 | 就近规则能提高相关性；不同平台的自动发现机制不可混用。 | `.agents/rules/` 与根路由；静态可达。 |
| TIP-031 | 新经验先进入带来源、scope、状态、过期信号的候选池，经人工审核后才晋升。 | LOC-001、002、REF-002、003 | 条件采用 | 防止网页 prompt injection、错误观察和一次性任务污染长期规则。 | Memory 模板/Skill；无自动晋升。 |
| TIP-032 | 需要每次可靠执行或阻断的规则进入 permission、sandbox、hook、script 或 CI。 | LOC-006、007、009、013、REF-002、004、005、006 | 条件采用 | 自然语言与 Skill 不是强制执行层。 | controls 示例默认关闭；未接入真实 hook/CI。 |
| TIP-033 | 根目录极简、草稿/临时/归档分层、语义化命名。 | LOC-002、003、004、007、010 | 条件采用 | 对文档密集型混合仓库有价值，但不能强加给已有结构不同的代码库。 | `file-document-governance` 模块；仅显式选择时生成。 |
| TIP-034 | Markdown frontmatter 只在项目已采用该规范时要求。 | LOC-002、003、007 | 条件采用 | 通用强制会污染既有文档和第三方文件。 | file/document 模块，不进入常驻核心。 |
| TIP-035 | 新建文件前先判断能否更新既有文件；一次性产物不进入正式区。 | LOC-002、003、005、007、008、010 | 条件采用 | 方法普适，但具体目录由仓库事实决定。 | 用户 core + file/document 模块。 |
| TIP-036 | Python 类型、测试、包管理和框架规则必须由 `pyproject.toml`、依赖或现有代码确认。 | LOC-002、005、018 | 条件采用 | Python 3.12、FastAPI、uv、mypy 等不是所有项目的通用事实。 | `python-fastapi` 模块；不在用户 core。 |
| TIP-037 | 性能优化先测量瓶颈，再选择 profiler 和改动。 | LOC-002、005、009 | 改写采用 | 保留 evidence-first；不把 `cProfile` 写成所有 Python 场景的固定工具。 | Python 模块、technical-research/debug Skill。 |
| TIP-038 | TypeScript strict、React、Next.js、Tailwind、状态库和包管理器由仓库版本与既有约定决定。 | LOC-002、008 | 条件采用 | 固定 React 19 / Next.js 15 会快速过时并误导非 React 项目。 | `typescript-nextjs` 模块。 |
| TIP-039 | 前端验证同时覆盖功能状态、响应式、键盘、可访问性和实际视觉结果。 | LOC-008、REF-005 | 改写采用 | 这组检查面向用户可见行为，不依赖固定框架。 | frontend visual module、workflow、EVAL-05 contract。 |
| TIP-040 | 数据库变更说明 forward、rollback/repair、兼容窗口、锁/数据影响和验证。 | LOC-002、009 | 改写采用 | “必须可回滚”对所有 migration 并不现实，repair path 与兼容策略更精确。 | PostgreSQL module、EVAL-04 contract。 |
| TIP-041 | `EXPLAIN ANALYZE` 只在隔离、只读或可恢复环境对已审查语句使用。 | LOC-002、009 | 改写采用 | PostgreSQL 会实际执行语句；把它写成无条件只读检查有数据风险。 | PostgreSQL module。 |
| TIP-042 | Dataverse 查询先发现知识源、理解 schema、主表与关联方向。 | LOC-015 | 条件采用 | 方法合理，但列出的私有工具名不能假定存在。 | 仅项目能发现对应工具时建立 private Skill；默认不生成。 |
| TIP-043 | `common.lute_logger`、`lute_file`、`mysql_instance` 等私有 wrapper 只在仓库中真实存在时使用。 | LOC-018 | 条件采用 | 写入通用配置会生成不存在的 import。 | private adapter 候选；默认排除。 |

## 3. Skill 与工程工作流

| Tip ID | 原子经验 | 来源 | 决策 | 原因 | 落点与验证状态 |
| --- | --- | --- | --- | --- | --- |
| TIP-044 | Skill 的 description 写清能力、触发和不适用边界，正文保留完整判据。 | LOC-006、026、REF-004、Matt skills | 改写采用 | 兼顾可发现性与执行闭环，避免为了短而丢失关键量表。 | 全部 Skills；静态 `quick_validate`。 |
| TIP-045 | 一个 canonical Skill 源，经平台 adapter 生成调用字段；不手工维护等价正文副本。 | LOC-022、026、027、REF-004、005 | 改写采用 | 直接解决本地重复正文和多平台漂移。 | `skills/` + renderer；快照测试。 |
| TIP-046 | Skill 可带 `references/`、`scripts/`、`assets/` 和 Codex `agents/openai.yaml`；只按需加载。 | LOC-006、REF-004；Codex 官方资料 | 路由采用 | 这是 progressive disclosure 的正式能力，不应被封闭白名单误拒。 | 生成器整树复制/校验；单元测试覆盖。 |
| TIP-047 | 项目可新增合规 Skill 与支持文件，生成器只锁定自己拥有的 managed artifacts；自定义 Skill 不得私用内部 explicit-only marker。 | REF-004、005；本轮缺陷复盘 | 改写采用 | 完全封闭 allowlist 会阻止能力层演进；放宽不能覆盖 managed 文件和安全校验。显式调用还需要 DSH/Claude overlay，只能由 canonical registry 统一生成。 | `validate-generated` 所有权边界、敏感路径与 explicit-only 拒绝测试。 |
| TIP-048 | 模糊产品目标用依赖感知访谈收敛 actors、流程、失败、边界和验收。 | REF-005、Matt `grilling` / `grill-with-docs` | 改写采用 | 保留高价值提问法；不对普通模糊任务静默启动长访谈。 | `product-discovery`，explicit-only。 |
| TIP-049 | 技术调研优先一方资料，形成 claim→source→confidence→expiry，而非链接堆积。 | LOC-020、REF-002 至 007、Matt `research` | 改写采用 | 可审计、可更新，也能阻止第三方帖子升级成平台事实。 | `technical-research` + research ledgers。 |
| TIP-050 | 规格必须包含 scope、行为、数据/权限、失败语义、非目标和验收。 | LOC-016、REF-005、Matt `to-spec` | 改写采用 | 让实现与验证都能追溯；不自动发布到 issue tracker。 | `specification`，explicit-only。 |
| TIP-051 | 以可独立演示和验证的垂直 slice 拆票，显式记录阻塞边。 | LOC-016、Matt `to-tickets` | 改写采用 | 比 frontend/backend 横切更接近可交付增量；不推导外部写入。 | `vertical-ticketing`，explicit-only。 |
| TIP-052 | 新行为先观察正确失败，再做最小实现并保持 green。 | LOC-005、021、023、REF-001、Matt `tdd` | 改写采用 | 保留 red-green 反馈；对文档/生成配置等非生产代码不机械套用。 | `tdd` Skill；行为未实测。 |
| TIP-053 | 调试一次只检验一个可证伪假说，修复后同路径回归。 | LOC-001、003、005、Matt `diagnosing-bugs` | 改写采用 | 避免连续猜测 patch。 | `systematic-debugging`；EVAL-03 contract。 |
| TIP-054 | Code review 分开检查 Spec compliance 与 engineering standards。 | LOC-001、016、Matt `code-review` | 改写采用 | 防止“代码整洁”掩盖“做错需求”，反之亦然。 | `two-axis-code-review`；contract-only。 |
| TIP-055 | 原型必须由一个待回答问题驱动，隔离、可丢弃，并明确结论与清理状态。 | LOC-014、016、Matt `prototype` | 改写采用 | 保留学习价值；排除强制建分支或 commit。 | `safe-prototyping`。 |
| TIP-056 | 领域建模先提取术语、actor、规则、不变量、事件和歧义，再选择代码结构。 | REF-005、Matt `domain-modeling` | 改写采用 | 防止框架结构替代业务理解；只产出证据化模型，不臆造业务事实。 | `domain-modeling`。 |
| TIP-057 | 代码库设计先定位变化轴、稳定边界、数据/控制流和失败边界，再决定模块。 | LOC-001、014、Matt `codebase-design` | 改写采用 | 将系统思维转成可审查设计，而非固定架构模式。 | `codebase-design`。 |
| TIP-058 | 架构审查使用证据化风险、反例、替代方案和迁移/回滚要求。 | LOC-001、011、014、REF-007、Matt `improve-codebase-architecture` | 改写采用，explicit-only | 它可能改变长期边界，必须由用户明确选择，不能因关键词自动触发大审查。 | `architecture-review`；无真实项目评测。 |
| TIP-059 | 实施编排只拆分边界清晰、无重叠写集、可独立验收的子任务，主 Agent 复核集成。 | LOC-001、016、REF-004、Matt `implement` | 改写采用，explicit-only | 保留并行收益；禁止借编排扩大授权、自动 commit 或让子 Agent 相互覆盖。 | `implementation-orchestration`；无真实多 Agent 评测。 |
| TIP-060 | 项目画像和 Memory 治理是显式管理动作，不靠相似关键词自动改长期知识。 | REF-003、005 | 路由采用，explicit-only | 长期事实的写入、晋升和删除需要人类决定。 | `project-profile`、`memory-governance`。 |
| TIP-077 | 任务型界面默认克制，视觉显著性按任务重要性、后果和紧迫性决定；复用熟悉图标并以真实同屏证据验收。 | LOC-030 | 条件采用并改写 | 保留任务型界面的默认偏置和证据闭环；营销/品牌、安全、无障碍和当前主任务按职责例外，tooltip 不承担核心语义，视觉尺寸不缩小命中区；排除跨场景绝对禁止和“只有用户要求才可强调”。 | Codex 用户偏置、`frontend-visual-quality` module、M05–M09、`EVAL-05`；静态可达 / `EVAL-05` contract-only。 |
| TIP-078 | 在首次可信 baseline 后，只对当前新增设计或 diff 的单一候选作消融式删减检查。 | LOC-031 | 条件采用并改写 | 每次只处理一个候选，并用同一验收和相关回归复验；保护正确性、安全、权限、数据完整性、兼容性、可测试性、可观测性、migration、恢复、回滚与已批准 UX seam；模型效果未固定模型 / fixture 验证。 | `RUL-004`、SOP、`EVAL-02`、`EVAL-06`；静态追溯，两个 eval 均为 contract-only。 |

## 4. 明确排除或延期的经验

| Tip ID | 原子经验 | 来源 | 决策 | 不采用原因 | 替代方案 |
| --- | --- | --- | --- | --- | --- |
| TIP-061 | 常驻 RIPER-5/6 状态机、每次响应 mode header 和自动模式切换。 | LOC-014、016、017 | 排除 | 与请求语义冲突，增加上下文和交互税，并与多处门禁自相矛盾。 | 低风险 fast path；复杂任务使用计划与风险 gate。 |
| TIP-062 | 每个计划步骤都等待人工确认。 | LOC-014、016 | 排除 | 对可逆、明确任务造成不必要阻塞。 | 只在架构/数据/权限/外部副作用等实质转折确认。 |
| TIP-063 | 强制展示完整 Chain-of-Thought、固定 3–5 条推理路径或思维树。 | LOC-014、REF-007 | 排除 | 不是可验证质量控制，还会诱导冗长和泄露隐藏推理要求。 | 输出假设、证据、候选方案、取舍和决策摘要。 |
| TIP-064 | “10 倍质量”、固定响应延迟、固定 token 预算。 | LOC-014、REF-006、007 | 排除 | 没有代表性实验和跨模型稳定证据。 | 在固定 fixture、模型和权限下做成对评测。 |
| TIP-065 | 模型手工计算并标记每个代码块的 AI 修改行数。 | LOC-013 | 排除 | 不可靠、污染源码且没有当前产品需求。 | 真有合规要求时用 diff/AST 的确定性工具。 |
| TIP-066 | 所有任务都先澄清用户“真正动机”。 | LOC-002、003、010 | 改写后排除常驻门禁 | 明确、低风险任务不应被访谈阻塞。 | 只澄清会改变架构、数据、权限、UX、兼容性或安全的缺口。 |
| TIP-067 | 所有仓库统一 Python/FastAPI/PostgreSQL/React/Next/Tailwind/Zustand/uv/pnpm。 | LOC-002、005、008、009 | 排除通用默认 | 技术栈是项目事实，不是用户级偏好；版本也会过时。 | 有仓库证据时选择对应模块。 |
| TIP-068 | 复杂查询无条件运行 `EXPLAIN ANALYZE`。 | LOC-002、009 | 排除原表述 | 它会执行语句，可能锁表或写数据。 | 隔离、只读或可恢复环境中的受控使用。 |
| TIP-069 | 每次编辑前自动创建 50 份历史快照，或假设 `/restore`、私有备份工具存在。 | LOC-001、002、010 | 排除通用默认 | 平台行为、保留数量与恢复命令缺少跨平台证据，并可能复制秘密。 | 使用项目现有 VCS/备份；破坏性操作前建立经确认的可回滚路径。 |
| TIP-070 | 自动把成功/失败经验写入长期 Memory，或由 Agent自行删除/晋升正式规则。 | LOC-001、REF-002、003 | 排除 | 会积累错误、PII、prompt injection 与过期规则。 | 来源化候选池 + 人工审核、晋升、失效和删除。 |
| TIP-071 | 复制 X 帖中的 Hook JSON、目录或平台命令并当作官方机制。 | REF-002 至 006 | 排除 | 作者经验只能证明作者主张，动态平台字段需当前一方资料和 runtime smoke。 | 官方文档固定证据 + 隔离实测。 |
| TIP-072 | 把 Cursor `.mdc`、`alwaysApply`、globs 和 `.claude/rules` 语义直接移植给 Codex/DSH。 | LOC-003 至 019、REF-004 | 排除 | 两个目标平台的发现、预算、局部加载与调用字段不同。 | 共享语义核心 + Codex/DSH 薄 adapter + 显式根路由。 |
| TIP-073 | 整包安装第三方高-star Skills 或把 star 数当质量证明。 | REF-001、Matt 上游、中文镜像 | 排除 | 流行度不证明适配性、安全性和行为收益；脚本可能带外部副作用。 | 固定 commit、许可证审计、逐项 adapt/exclude、独立重写和评测。 |
| TIP-074 | 默认安装 setup、wizard、tracker triage、pre-commit、Git guardrail 等生态绑定 Skill。 | Matt 上游 | 排除或延期 | 涉及安装、Git、外部 tracker、凭据或 Hook，超出通用基础配置授权。 | 项目确有需求时单独评审、显式安装并做回滚 smoke。 |
| TIP-075 | 强制“用户连续三次被同意后必须提出反方”。 | LOC-011 | 排除 | 人为制造异议，不提高事实准确性。 | 只在证据、假设或风险真实冲突时提出反例。 |
| TIP-076 | 固定根目录清单、四态文件生命周期与所有 Markdown frontmatter 对所有项目永久生效。 | LOC-002、003、004、007、010 | 排除通用默认 | 会与既有仓库结构、生成器和第三方文件冲突。 | `file-document-governance` 条件模块。 |

## 5. 来源覆盖与可追溯性

- 本地来源覆盖：`LOC-001` 至 `LOC-031` 全部至少出现在本矩阵、[逐文件账本](local-tip-ledger.md)或纯 provenance 决策中。`LOC-025`、`LOC-028`、`LOC-029` 不含新增行为规则，只用于翻译/打包/许可证线索，因此不被伪装成行为 Tip；`LOC-030`、`LOC-031` 是后续用户会话来源，不计入原始 29 个本地内容文件。
- 外链覆盖：`REF-001` 至 `REF-007` 全部进入上述决策；作者经验不支撑平台事实或质量倍率。
- 第三方 Skill 覆盖：逐候选决定和固定 commit 在 [`third-party-skills.lock.json`](../../sources/third-party-skills.lock.json)；当前 Skills 是独立重写，不是整包复制。
- 规则追踪：聚合后的可执行原则仍以 [`rule-traceability.json`](../../sources/rule-traceability.json) 为机器可解析索引。本矩阵保留比聚合规则更细的采用/排除理由。

## 6. 复审触发

出现以下任一情况时，相关决策失效并需复审：Codex 或 DSH 的发现/Skill schema 改变；项目技术栈或安全边界改变；代表性行为评测显示规则引发过度停顿、漏读上下文或范围扩张；来源内容被修订；候选规则无法提供来源、适用范围或过期信号。
