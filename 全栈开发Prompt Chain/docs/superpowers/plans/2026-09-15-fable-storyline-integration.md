# 故事线驱动与编译式交付融合 Implementation Plan

**Goal:** 将受控 Feishu 故事线、Fable compiler 的多目标工程方法和 fable-method 的证据闭环投影到现有 AI 全栈开发链；不新建状态机、Gate、artifact 或默认权限。

**Canonical design:** 完整取舍见 `全栈开发Prompt Chain/09-故事线驱动与编译式交付模式.md`。`04-模块化Skills工作流.md` 维护 M00–M13、A00–A13 与 G0–G6 的规范映射；`08-AI-Native-SDLC控制面规范.md` 维护 Control Contract、状态、责任、证据、回退与 R3 授权语义。本轮只投影二者，不建立第二套控制面。

**Execution boundary:** P0 只修改仓库内 Markdown、JSON、既有 Skill 与 Prompt；P1 才考虑本地 synthetic eval。不安装上游脚本，不改 shared core、生成 adapter 或用户主目录配置，不调用真实模型或生产系统，不 commit、不 push。任何新增依赖、外部写入、用户级持久化或 R3 动作另行决定。

**Current status:** P0 的来源、模型配置说明、Prompt、既有 Skill 投影和本地结构/测试验证已完成；shared core 经审计无需修改，00/99 无需承载本轮细节。Task 5 的 EVAL-02 synthetic trap suite 已完成 4 个独立 pair / 8 个 deterministic stub run，并由 targeted test 7/7 与 manifest structure/tree contract 复验。真实 Agent、跨模型、真实项目切片、真实 adapter/browser/database/network 与生产验证均未执行。

## Source baseline

- Feishu：access-controlled AI meeting summary revision 6；主文已读，原始 transcript 无权限；公开仓库不记录租户 URL。
- Fable compiler：固定 `5d62380cb30dc1080c6943445a256e27db6246f8`。
- fable-method：固定 `88b5cf36b10ee3679e08ee0f0181b9774d481508`；MIT、社区萃取、非 Anthropic 官方。
- 所有能力收益均为待验证假设；静态文档与结构检查不能升级为真实 Agent 或生产证据。

## Task 1: 建立方案与来源追溯

**Files:**

- Create: `全栈开发Prompt Chain/09-故事线驱动与编译式交付模式.md`
- Create: `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-15-fable-storyline-integration.md`
- Modify: `Constraint/coding-agent-system/report-source.md`
- Modify: `Constraint/coding-agent-system/docs/research/source-ledger.md`
- Modify: `Constraint/coding-agent-system/sources/research-methods.lock.json`
- Modify: `Constraint/coding-agent-system/sources/rule-traceability.json`
- Modify: `Constraint/coding-agent-system/sources/NOTICE.md`
- Modify: `全栈开发Prompt Chain/report-source.md`
- Modify: `全栈开发Prompt Chain/README.md`

- [x] 登记三源身份、固定版本、许可证或访问边界、采用用途和不可支持的主张。
- [x] Feishu 只记录来源类型、revision、读取日期与证据边界；公开仓库不记录 access-controlled URL、文档 ID、完整内容摘要或原始 transcript 内容。
- [x] 为每条新增规则绑定来源、目标文件、现有 eval ID、失效条件与 `contract-only` 状态。
- [x] 为方案文档建立 README 导航，不复制控制面规范。

**Acceptance:** JSON 可解析；来源 ID 唯一；所有事实能回到固定公开来源或受控快照描述；不出现 Anthropic 官方背书、已验证收益或 transcript 已读等错误主张。

**Rollback:** 删除新增来源/规则记录与导航；不影响 M00–M13 状态和运行文件。

## Task 2: 审计 shared core 并收敛模型配置说明

**Files:**

- Audit only: `Constraint/coding-agent-system/templates/shared/user-core.md`
- Audit only: `Constraint/coding-agent-system/templates/shared/project-core.md`
- Modify: `Constraint/coding-agent-system/docs/model-configuration.md`

- [x] 审计 canonical user/project core；确认现有通用完成定义、证据分层、最小实现和验证规则已覆盖稳定内核要求，本轮不修改 shared core。
- [x] 在 model configuration 中把固定模型角色改为可更新能力卡和「任务形态 → 风险/工具 → 验证 → 模型」路由。
- [x] 将 task shape、canonical/shared/target、native verification 等详细方法留在 Skills 与 Prompts，避免常驻上下文重复。
- [x] 因 shared core 没有本轮变更，不运行 `render-templates --apply`，也不手改任何生成 adapter。

**Acceptance:** scoped Fable 集成没有向 shared core 或生成 adapter 增加专属语义；模型品牌只作为校准对象，不作为永久职责。工作区中其他任务已存在的 shared core 变更不属于本轮结论或回滚范围。

**Rollback:** 只需回退 model configuration 的本轮增量；shared core 与生成 adapter 无本轮回滚项。

## Task 3: 投影到现有 M00–M13

**Files:**

- Modify: `全栈开发Prompt Chain/03-AI产品全生命周期映射.md`
- Modify: `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- Modify: `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- Modify: `全栈开发Prompt Chain/08-AI-Native-SDLC控制面规范.md`
- Modify: `Constraint/coding-agent-system/docs/workflow.md`
- Modify: `全栈开发Prompt Chain/prompts/03-用户研究与问题定义.md`
- Modify: `全栈开发Prompt Chain/prompts/04-产品策略与范围决策.md`
- Modify: `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/prompts/11-可观测性与反馈闭环.md`
- Modify: `全栈开发Prompt Chain/prompts/13-复盘与Skill自进化.md`
- Modify: matching `prompts_ask/03–09,11,13-*.md`

- [x] M03/M04 将故事线限定为可证伪假设，并把叙事证据用于范围决策而不是替代范围决策；M05 明确前置最小规格与 canonical behavior，不采用「完成后才写 PRD」。
- [x] M06 按最大不确定性选择 capability spike 或 UX prototype。
- [x] M07 仅在条件满足时设计 shared transform、target adapter、native validator 与 conformance matrix。
- [x] M08 处理用户最新意图、A05 和既有测试的冲突；先最窄验证，再目标原生与相关矩阵；完成后消融。
- [x] M09 使用 `claim → expected evidence → observed evidence → verdict → gap`，由独立上下文审证。
- [x] M11 为产品故事或目标观测冲突定义回退入口。
- [x] M13 使用 `adapter + trap + oracle + smoke` 候选包；重复三次仅触发审查，不自动晋升。
- [x] formal/ask 对应版本同步触发、停止、证据和授权语义；00/99 保持通用入口，不加入本轮 Fable 细节。

**Acceptance:** 所有新增字段都落入既有 Axx；不出现新 Gate、artifact 或并行控制面；formal/ask 版本在触发、停止、证据和授权语义上相同。

**Rollback:** 按模块逆序移除投影；canonical 控制面与原有 artifact 链保持可用。

## Task 4: 强化既有 Skill，而非整包安装上游

**Files:**

- Modify: `Constraint/coding-agent-system/skills/safe-prototyping/SKILL.md`
- Modify: `Constraint/coding-agent-system/skills/codebase-design/SKILL.md`
- Create: `Constraint/coding-agent-system/skills/codebase-design/references/spec-to-target-pipeline.md`
- Modify: `Constraint/coding-agent-system/skills/implementation-orchestration/SKILL.md`
- Modify: `Constraint/coding-agent-system/skills/two-axis-code-review/SKILL.md`
- Modify: `Constraint/coding-agent-system/docs/skills-governance.md`

- [x] safe-prototyping 增加 capability spike / UX prototype 分流和证据边界。
- [x] codebase-design 以按需 reference 承载 canonical/shared/target、相邻 adapter 与 native validator 方法，不新增笼统 Fable Skill。
- [x] implementation-orchestration 增加 canonical/shared/target 分类、相邻 adapter 检查、native validator 与消融停止条件。
- [x] two-axis-code-review 增加 claim-to-observation 独立判定，不让静态符合替代运行观察。
- [x] Skill 晋升要求 recurrence、稳定 I/O、权限边界、trap、oracle、smoke/held-out、owner、expiry 与人工决定。
- [x] 未运行 fable-method 的 install 脚本，也未复制它的状态或 artifact contract。

**Acceptance:** 现有 Skill 触发互斥或可解释；Skill 不授予文件、网络、凭据或外部动作权限；没有自动安装/晋升路径。

**Rollback:** 回退对应 Skill 文本；候选证据与来源账本仍保留。

## Task 5: 建立可证伪的本地评测

**Files:**

- Modify: `Constraint/coding-agent-system/evals/README.md`
- Modify: existing relevant tasks under `Constraint/coding-agent-system/evals/tasks/`
- Modify: existing synthetic fixture/config only where required
- Modify: eval unit tests only where required

- [x] 设计并实现规格/测试冲突、相邻 adapter 回归、无收益 Skill、越权外部动作四类 synthetic trap。
- [x] 4 个 baseline/candidate pair 固定同 task/case/control，每对只改变 `treatment.enabled`；未改变模型、权限、工具或环境声明。
- [x] 保存 raw stdout/stderr、observation、verdict、receipt、record、`failure: null`/失败理由和未验证项；case 不含 expected label/winner，deterministic oracle 不是模型 judge 或人工审查；summary/CLI 以 `deterministic-local-stub`、`no-model`、`real_agent_execution: false` 自描述执行身份。
- [x] 运行纯本地 synthetic trap suite；结果固定为 `quality_comparison: not-applicable`、`inference: not_computed`，真实模型、跨模型和生产验证保持未运行。
- [x] 唯一 EVAL-02 ready fixture 与最小 synthetic 样本已稳定；真实模型评测决定仍未作出，也未获授权。

**Acceptance:** Task 5 已实施：targeted test 7/7、manifest `structure_valid: true` / `tree_contract_valid: true`、4 pair / 8 run 及四态 verdict 已由实现者和独立审查者复验。`agent: codex` 是 invocation-declared synthetic label，实际为 `model: no-model` 的 deterministic local stub，不是 Codex/Claude/DeepSeek 真实运行；mutation fail-closed 只证明 oracle 拒绝四类内部矛盾样本。证据不支持真实 Agent、模型质量、Skill 收益、跨模型优势、真实 adapter 兼容性、授权安全、browser/database/network/production 行为、用户价值或因果收益。Task 6 的 post-Task-5 全 eval/tools suite 与仓库级 validator 已由主线程完成，结果见下节。

**Rollback:** 按 Task 5 scoped diff 回退新增 synthetic case/config 与 runner/test/manifest 增量，并同步回退本节状态；不改 approved eval ID 集合，不删除历史 run record，也不覆盖共享工作区的其他未提交改动。

## Task 6: 验证、审计与交接

- [x] `python3 tools/agent_system.py render-templates`：退出 0，`DRY-RUN`；未执行 `--apply`。
- [x] `python3 tools/agent_system.py validate .`：Task 5 合入后退出 0，`VALID`；首次集成运行发现 synthetic artifact status 误用了 rule-level 边界串，修正为受控枚举 `implemented-with-planned-eval` 后复验通过，未放宽 validator。
- [x] `python3 -m unittest discover -s tools/tests -v`：Task 5 合入后 118 tests，`OK`。
- [x] `python3 -m unittest discover -s evals -p 'test_*.py' -v`：Task 5 合入后 75 tests，`OK`。
- [x] `python3 -m unittest test_synthetic_fixture -v`：7 tests，`OK`；`validate_fixture.py fixture-manifest.synthetic.json` 报告 `structure_valid: true`、`tree_contract_valid: true`。
- [x] trap/default CLI 使用不同 `TemporaryDirectory` 运行并执行语义 gate：4 pair / 8 run verdict 符合契约，receipt/record/control/identity/path 均绑定，no-benefit 保留 null，输出不含 winner、ranking、score delta、promotion recommendation 或 causal claim；临时输出退出时清理。
- [x] `python3 -m json.tool sources/research-methods.lock.json >/dev/null`：退出 0。
- [x] `python3 -m json.tool sources/rule-traceability.json >/dev/null`：退出 0；27 个 Rule ID 唯一。
- [x] 4 个增强 Skill 分别通过 `skill-creator/scripts/quick_validate.py`。
- [x] `git diff --check`：tracked diff 退出 0；另对本轮 33 个 scoped untracked 文件逐项做 UTF-8 与 `git diff --no-index --check` 检查，whitespace diagnostics 为 0；fixture 内无 `__pycache__`、`.pyc` 或落盘 run output。
- [x] P0 审查 scoped diff、formal/ask 语义配对、未验证声明和 access-controlled 信息泄露；P0 三轮独立只读审计最终均为 `No findings`，不作为 P1 终审替代证据。
- [x] P1 最终技术/证据审计均完成：分别发现“P0/P1 审计状态混用”和“Task 5B/5C review record 未落盘”两个 Important 记录问题；修正后原审查者复核关闭，最终均为 `Approved`，无开放 Critical / Important / Minor finding。
- [x] P1 交接材料已完成，包含实际改动、原始验证结果、已修复的集成失败、未运行项和下一安全动作；未 commit、未 push。

验证证据仅支持仓库结构、规则追踪、模板一致性、本地 deterministic harness、artifact 链路、固定 oracle 拒错与本地测试通过。它不支持真实 Agent 能力提升、模型质量、Skill 收益、跨模型优势、真实项目收益、真实授权安全、用户价值或生产安全结论。

**Final acceptance:** 静态校验、测试、三源追溯、本地 synthetic evidence gate、P1 最终审计与交接材料均已完成，本计划的 P0/P1 范围关闭。现有控制面未分叉；无 secret/PII/受控 URL；所有真实 Agent、模型质量、用户价值和生产结论仍明确为未验证；模型能力卡校准与 P2 不在本次完成范围。

**Global rollback:** P0 变更仍是仓库内可逆 Markdown、JSON 与 Skill 文本；Task 5 已增加可逆的本地 synthetic fixture/config/runner/test/manifest 增量。需要回退时按各 Task scoped diff 逐文件处理；不得删除历史 run record，不得用 `git reset --hard` 或覆盖他人已有未提交改动。
