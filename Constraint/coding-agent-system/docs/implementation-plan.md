---
title: 多 Coding Agent 开发系统实施计划
doc_type: plan
module: coding-agent-system
topic: implementation
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# 多 Coding Agent 开发系统实施计划

> **执行约定：** 使用 subagent-driven development 完成互不重叠的任务，并在集成后执行独立审查。当前目录不是 Git 仓库，因此不创建 worktree 或 commit；用户已明确要求本轮不修改真实用户配置。

**目标：** 在 `Constraint/coding-agent-system/` 中交付可审查、可初始化、可安装、可验证的 Codex 与 DeepSeek Harness 基础配置系统；既有 Claude Code adapter 仅保留作兼容性回归。

**架构：** 共同规则和 skill 正文是单一事实源；平台差异由模板和生成器处理。确定性工具使用 Python 标准库实现，第三方方法只经固定来源和本地重写进入系统。

**技术栈：** Markdown、TOML、JSON、YAML、Python 3 标准库、`unittest`。

## 全局约束

- 不修改 `Constraint/` 中既有文件。
- 不遍历、解析或输出 `.env`、token、密钥或其他凭据。用户安装备份既有目标时会原样读取并复制目标字节；备份可能含敏感信息，必须放在受保护的新目录中。
- 不修改真实的 `~/.codex/`、`~/.claude/`、`~/.dsh/`。
- 不 commit、push、merge、发布或部署。
- 不新增第三方运行依赖。
- 项目级产物必须跨 macOS、Linux、Windows。
- 每个 material claim 必须有来源或明确标记为推断、建议或未验证项。
- 完成声明必须附本轮新鲜验证证据。

---

### Task 1：研究报告与证据账本

**文件：**

- 创建：`report-source.md`
- 创建：`docs/research/deep-research-report.md`
- 创建：`docs/research/source-ledger.md`
- 创建：`docs/research/local-material-audit.md`
- 创建：`sources/third-party-skills.lock.json`
- 创建：`sources/NOTICE.md`

**产出：** 官方机制对照、现有材料缺陷、共享可行性、第三方 skill 分级、限制与建议；账本记录标题、发布者、日期、URL、访问说明和置信度。

**验证：**

- `rg -n 'turn[0-9]+(search|view|fetch)' Constraint/coding-agent-system` 无内部引用 ID。
- `python3 -m json.tool sources/third-party-skills.lock.json` 成功。
- 报告中的关键平台结论均能映射到账本条目。

### Task 2：共享核心与三平台模板

**文件：**

- 创建：`templates/shared/user-core.md`
- 创建：`templates/shared/project-core.md`
- 创建：`templates/user/codex/AGENTS.md`
- 创建：`templates/user/codex/config.toml`
- 创建：`templates/user/claude/CLAUDE.md`
- 创建：`templates/user/claude/settings.json`
- 创建：`templates/user/deepseek-harness/AGENTS.md`
- 创建：`templates/user/deepseek-harness/README.md`
- 创建：`templates/project/AGENTS.md`
- 创建：`templates/project/.claude/CLAUDE.md`
- 创建：`templates/project/.codex/config.toml`
- 创建：`templates/project/.claude/settings.json`
- 创建：`templates/project/.agents/README.md`

**接口：** 模板中的共享块使用 `<!-- BEGIN SHARED CORE -->` 和 `<!-- END SHARED CORE -->` 标记。`templates/shared/*` 是 canonical core；渲染器确定性生成用户级和项目级平台快照，校验器比较重渲染结果并检测漂移。项目 `.codex/config.toml` 不设置会覆盖个人或组织安全基线的审批、sandbox 或模型键。

DeepSeek Harness 模板只描述默认 spine 已启用 `agent-instructions`、skill registry、tool consumer 与 skill filesystem plugins 时的行为。`.claude/CLAUDE.md` 只避免初始根候选冲突；Harness 触达 `.claude/` 后仍可能动态发现该文件，并把 Claude `@` import 当作普通文本。

**验证：** JSON 和 TOML 可解析；共享块一致；不存在真实主目录路径、凭据或替换内置 Codex base prompt 的设置。

### Task 3：首批八个核心 Skills

**文件：**

- 创建：`skills/<skill-name>/SKILL.md`
- 创建：`skills/<skill-name>/agents/openai.yaml`
- 按需创建：`skills/<skill-name>/references/*.md`

**接口：** Task 3 首批八个目录名与 `name` 完全一致；方案 B 后当前总数为 15。所有 Skill 使用共同安全边界，并允许 `SKILL.md` 相对引用的 `references/`、`scripts/` 与 `assets/` 随完整 Skill 树生成。规范化 `SKILL.md` 中的 `metadata.invocation: explicit-only` 只是本项目渲染器识别的内部 marker，不是 Codex 官方调用字段。Codex 的实际调用策略由 `agents/openai.yaml` 的 `policy.allow_implicit_invocation: false` 表达；初始化器据内部 marker 为 Claude Code 与 DeepSeek Harness 生成带顶层 `disable-model-invocation: true` 的平台副本。当前 explicit-only 集合为 7 个。

**验证：** 对每个目录运行官方 `quick_validate.py`；校验引用存在；搜索自动 commit、真实 issue 写入和危险 Git 命令，确认不存在隐式授权。

### Task 4：技术栈模块

**文件：**

- 创建：`templates/modules/typescript-nextjs.md`
- 创建：`templates/modules/python-fastapi.md`
- 创建：`templates/modules/postgresql-migrations.md`
- 创建：`templates/modules/frontend-visual-quality.md`
- 创建：`templates/modules/file-document-governance.md`

**接口：** 每个模块说明触发路径、需要先从仓库发现的事实、最小质量门槛和验证命令选择原则；不硬编码版本、包管理器或项目不存在的命令。初始化器选择模块后，必须在根 `AGENTS.md` 的受管路由块中写入路径和触发条件，不能只复制不可达文件。

**验证：** 每个模块可独立阅读；无相互矛盾的默认技术选型；无未经核实的项目路径。

### Task 5：初始化、安装与校验 CLI

**文件：**

- 创建测试：`tools/tests/test_agent_system.py`
- 创建实现：`tools/agent_system.py`

**命令接口：**

```text
python3 tools/agent_system.py init-project DEST [--stack NAME ...] [--apply]
python3 tools/agent_system.py install-user --target {codex,claude,deepseek-harness,all} [--apply]
python3 tools/agent_system.py render-templates [--apply]
python3 tools/agent_system.py validate [PATH]
python3 tools/agent_system.py validate-generated --kind {project,user} --root PATH [--target TARGET] [--require-ready-profile]
```

**生成与用户安装接口：** 项目初始化写入 `.agents/generated-manifest.json` 绑定所选 stack modules 和 managed Skills，并在根 `AGENTS.md` 生成可达的受管模块路由；`validate-generated` 严格保护生成器拥有的产物，同时允许不覆盖 managed 名称的合规项目 Skill 与 supporting resources。项目自定义 Skill 不得使用内部 `metadata.invocation: explicit-only`；需要跨平台显式调用适配时应进入 canonical managed registry。普通项目校验允许 draft 画像；active 画像必须保持 canonical preamble 并通过七域、来源和 secret-like 内容校验，`--require-ready-profile` 还要求状态为 active，其七域可使用有受控来源且说明边界的 `Not applicable`。`--target` 选择平台入口，不承诺 Skill 根隔离。target 包含 `codex` 或 `deepseek-harness` 时，共享 `.agents/skills/` 与七个 `.dsh/skills/` explicit-only overlay 必须始终同步；同机多平台建议使用 `--target all`。目标、home 与备份路径先规范化最深已存在祖先，输出和写入使用同一真实路径；路径自身是 symlink 时拒绝。已有且不同的 `.codex/config.toml` 与 `.claude/settings.json` 不会被备份选项覆盖，必须人工合并；相同内容 no-op。安装器不自动跟随 `CODEX_HOME`、`CLAUDE_CONFIG_DIR`、`DSH_HOME` 或 `DSH_AGENTS_HOME`；自定义根采用隔离生成、人工审查和人工迁移。

**单文件写入契约：** 所有生成、用户安装、备份和回滚文件先通过同目录中性临时名做 chunked stream 写入，以实际长度与 SHA-256 核验并 `fsync`。Darwin 调用系统 `/bin/mv` 原子移动，其他平台使用 `os.replace`；移动失败时清理临时文件并 fail closed，不把内容写进错误信息。

**测试顺序：**

1. 先写 dry-run 不产生文件的失败测试。
2. 先写空目录生成预期树的失败测试。
3. 先写非空目标拒绝覆盖的失败测试。
4. 先写用户配置已存在时要求备份的失败测试。
5. 先写 skill 和共享块校验的失败测试。
6. 先写 canonical core 重渲染、漂移检测与 apply 前 fail-closed 的失败测试。
7. 先写生成项目与用户 home 的 `validate-generated` 失败测试，并验证 dry-run/apply 输出包含显示路径到绝对目标的映射。
8. 逐项实现最小代码并保持全部测试通过。

**验证命令：**

```bash
python3 -m unittest discover -s Constraint/coding-agent-system/tools/tests -v
python3 Constraint/coding-agent-system/tools/agent_system.py validate Constraint/coding-agent-system
```

### Task 6：SOP、模型配置与工作流

**文件：**

- 创建：`docs/sop/project-lifecycle.md`
- 创建：`docs/model-configuration.md`
- 创建：`docs/workflow.md`
- 创建：`docs/skills-governance.md`
- 创建：`docs/installation.md`

**产出：** 从空目录、需求发现、初始化、开发、测试、视觉检查、审查、交付到规则进化的分阶段流程；说明 Codex、Claude Code、DeepSeek Harness 的模型和 reasoning 路由，不硬编码快速变化的默认值。模型 profile 先作为 opt-in 文档设计，不进入自动安装产物。

**验证：** 每个操作步骤包含前置条件、动作、预期结果、停止条件或恢复方式；外部副作用均有显式授权点。

### Task 7：评测套件

**文件：**

- 创建：`evals/README.md`
- 创建：`evals/tasks/*.md`
- 创建：`evals/rubrics/coding-agent-rubric.md`
- 创建：`evals/run-record.schema.json`
- 创建：`evals/execution-receipt.schema.json`
- 创建：`evals/assessment.schema.json`
- 创建：`evals/assessment.py`
- 创建：`evals/eval_protocol.py`
- 创建：`evals/receipt.py`
- 创建：`evals/run_lifecycle.py`
- 创建：`evals/score.py`
- 创建测试：`evals/test_*.py`

**接口：** 任务覆盖规格理解、功能实现、复杂调试、数据库迁移、前端视觉质量和代码审查。Auto Research 评测协议/控制面严格记录质量、验证证据、范围纪律、返工次数、耗时和 token，并要求固定 lifecycle、最小子进程环境、pre-run fixture tree digest、post-run 完整 artifact digest、评分时重跑 artifact contract、execution receipt、control snapshot、逐维 assessor assessment、artifact bundle、成对比较、停止条件与缺失数据保持 `null`。自报 score/counter/control 不作为观测事实；未绑定 assessment 不产生质量分或晋升资格。其方法只选择性吸收 `karpathy/autoresearch@228791f` 的固定范围、固定度量、实验记录和保留/丢弃循环，不复用训练代码或 `program.md` 文本。本轮没有运行真实 Agent、付费模型或代表性 fixture。

**验证：** 先写协议、receipt、lifecycle 与评分失败测试，再实现最小控制面；schema 可解析。示例 manifest 和记录只做 `contract-only` / `--validate-only` 结构演示，默认评分必须拒绝未绑定真实执行证据的示例记录。

### Task 8：集成入口与最终审查

**文件：**

- 创建：`README.md`
- 创建：`docs/verification-report.md`

**验证：**

```bash
python3 -m unittest discover -s Constraint/coding-agent-system/tools/tests -p 'test_*.py' -v
python3 -m unittest discover -s Constraint/coding-agent-system/evals -p 'test_*.py' -v
python3 Constraint/coding-agent-system/tools/agent_system.py render-templates
python3 Constraint/coding-agent-system/tools/agent_system.py validate Constraint/coding-agent-system
rg -n '(TODO|TBD|PLACEHOLDER|<REPLACE_ME>|api[_-]?key\s*=|token\s*=)' \
  Constraint/coding-agent-system/README.md \
  Constraint/coding-agent-system/report-source.md \
  Constraint/coding-agent-system/docs \
  Constraint/coding-agent-system/templates \
  Constraint/coding-agent-system/skills \
  Constraint/coding-agent-system/sources \
  -g '!implementation-plan.md'
find Constraint/coding-agent-system -type l -print
```

独立审查必须覆盖：需求完整性、平台事实、第三方许可证、安全边界、初始化器行为、引用可达性、重复与冲突。所有重要发现修复并重新验证后，才写入 `docs/verification-report.md`。

---

### Task 9：Codex 与 DSH Desktop 项目级直接配置

**目标：** 在不复制维护共同规则的前提下，交付可分别复制到项目根的 Codex 与 DSH Desktop / DeepSeek Harness 完整 `AGENTS.md`，并把 `Constraint/` 现有 tips 的采用、下沉和排除决策形成可审计证据。

**文件：**

- 修改：`docs/research/local-material-audit.md`
- 修改：`templates/shared/user-core.md`
- 修改：`templates/shared/project-core.md`
- 创建：`templates/project/codex/AGENTS.md`
- 创建：`templates/project/deepseek-harness/AGENTS.md`
- 修改：`templates/project/AGENTS.md`
- 修改：`templates/user/codex/AGENTS.md`
- 修改：`templates/user/deepseek-harness/AGENTS.md`
- 修改：`tools/agent_system.py`
- 修改：`tools/tests/test_agent_system.py`
- 修改：`README.md`
- 修改：`docs/design.md`
- 修改：`docs/installation.md`
- 修改：`docs/verification-report.md`

**接口与边界：**

- `templates/shared/project-core.md` 继续作为项目级共享块的唯一规范源；Task 10 后该共享块只承担项目画像与局部知识路由，不复制用户级通用行为。
- `templates/project/AGENTS.md` 继续作为 `init-project` 生成的多平台项目根入口。
- `templates/project/codex/AGENTS.md` 与 `templates/project/deepseek-harness/AGENTS.md` 是供单平台项目直接复制的完整快照；两者只允许在共享块之外保存平台差异。
- `init-project` 只复制既有多平台项目 bundle，不把两个参考快照目录复制进生成项目。
- 不把 Cursor 设为目标平台；Cursor tips 只按「共同核心 / skill / stack module / hook 或 CI / 排除」分类吸收。
- 不新增模型、provider、sandbox、审批或权限配置，不修改真实用户目录。

- [x] **Step 1：新增失败测试**

  测试必须覆盖：两个项目平台快照属于渲染目标；任一快照共享块漂移会被 `validate` 检出；`init-project` 不复制 `codex/` 或 `deepseek-harness/` 参考目录；平台适配正文在渲染后保持不变。

- [x] **Step 2：运行目标测试并确认失败**

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
    tools.tests.test_agent_system.AgentSystemTests.test_render_templates_updates_project_platform_snapshots \
    tools.tests.test_agent_system.AgentSystemTests.test_validate_detects_project_platform_core_drift \
    tools.tests.test_agent_system.AgentSystemTests.test_init_project_excludes_reference_project_snapshots -v
  ```

  预期：在新增常量、模板和渲染映射前至少一项失败。

- [x] **Step 3：实现模板与确定性渲染**

  扩展声明文件、project bundle allowlist、共享适配映射和 drift 校验；渲染只替换 `<!-- BEGIN SHARED CORE -->` 与 `<!-- END SHARED CORE -->` 之间的内容。

- [x] **Step 4：深度萃取并重写共同核心**

  用户级正文吸收请求类型、认知诚实、风险分级、根因调试、验证证据和长任务协作；项目级正文吸收工作区预检、最小可追溯 diff、生成物与 lockfile、官方资料门、migration、测试、文件治理、项目记录和能力分层。硬编码栈、固定目录、RIPER 门禁、隐藏推理输出、未验证平台能力和手工统计规则不得进入共享块。

- [x] **Step 5：运行渲染并验证目标测试通过**

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 tools/agent_system.py render-templates --apply
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
    tools.tests.test_agent_system.AgentSystemTests.test_render_templates_updates_project_platform_snapshots \
    tools.tests.test_agent_system.AgentSystemTests.test_validate_detects_project_platform_core_drift \
    tools.tests.test_agent_system.AgentSystemTests.test_init_project_excludes_reference_project_snapshots -v
  ```

- [x] **Step 6：更新研究、安装和入口文档**

  本地审计加入逐文件 tips 矩阵、规则去向、冲突与排除理由；README、设计和安装文档说明四份可直接配置文件、项目快照的复制位置和多平台共用方式。

- [x] **Step 7：完整回归与新鲜验证**

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/tests -p 'test_*.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_*.py' -v
  PYTHONDONTWRITEBYTECODE=1 python3 tools/agent_system.py render-templates
  PYTHONDONTWRITEBYTECODE=1 python3 tools/agent_system.py validate .
  ```

  另需比较三个项目快照的共享块、检查两份平台适配正文均存在，并在隔离空目录运行一次 `init-project --apply` 与 `validate-generated`。当前目录不是 Git 仓库，因此本 Task 不创建 commit。

---

### Task 10：专家经验可追踪重构与项目画像初始化器

**触发原因：** Task 9 只把本地 tips 归类为共同核心、模块或能力层，没有逐篇读取 `ref_links.txt` 的外链正文，也没有把“项目隐性知识、Memory 治理、规则生命周期、确定性控制和 Agent 行为评测”落实为可执行产物。用户已于 2026-08-29 确认采用“分层 Coding Agent Operating System + 项目初始化器”。

**架构决定：**

- 用户级配置采用短常驻跨项目行为内核；直接目标 Codex 与 DSH 只保留平台发现和预算差异，Claude adapter 仅作兼容性回归。
- 项目级配置是项目隐性知识路由器，不再重复整套用户级开发宪法。
- `AGENTS.md` 负责稳定上下文；多步骤方法进入 Skill；确定性底线进入 control / hook / CI 模板；历史知识进入带来源和过期治理的 Memory 候选层。
- 项目初始化器生成可审查的画像草稿；未填写业务不变量、权威入口、联动关系、禁用项、Definition of Done 与权威资料时，不得宣称是完整项目配置。
- Cursor 继续只作为方法来源，不新增 Cursor 目标产物。
- 机器可校验的追踪账本使用 JSON 而不是 YAML，以保持 Python 标准库可解析、拒绝引入 YAML 运行依赖。

**计划产物：**

- 研究与追踪：`docs/research/local-tip-ledger.md`、`docs/research/ref-links-ledger.md`、`sources/rule-traceability.json`。
- 项目画像与 Memory：`templates/project/.agents/project-profile.md`、`templates/project/.agents/memory/README.md`、`templates/project/.agents/memory/candidates.jsonl`。
- 确定性控制：`templates/project/.agents/controls/README.md` 以及不默认启用的检查模板。
- 能力层：扩展 `writing-for-agents` 的 Create/Audit 模式，并新增有独立触发边界的 `project-profile` 与 `memory-governance`；不为 instruction audit 再造重复 Skill。
- 行为评测：新增 instruction / project-profile / Memory / conflict / local-rule 任务和 rubric 维度；结构测试与真实 Agent 运行证据保持分层。

- [x] **Step 1：修复来源证据链**

  逐项登记 29 个本地内容文件和 7 个唯一外链；每个采用、改写或排除决定映射到规则 ID、目标层、实际产物和评测任务。纠正旧审计的文件计数与 `source seed` 过度声明。

- [x] **Step 2：重构 canonical user/project core**

  用户级只保留稳定身份、请求语义、Karpathy 决策内核、认知纪律、授权边界、冲突和能力路由；项目级改为项目画像入口、业务不变量、权威修改入口、联动关系、禁用项、精确 DoD、权威资料与局部规则路由。

- [x] **Step 3：扩展初始化、渲染与校验**

  `init-project` 在空目录生成项目画像、Memory 候选层和 control 说明；dry-run / apply 继续 fail closed。校验器验证追踪账本、项目画像字段、Memory schema、声明文件和 canonical 漂移，不读取 secrets。

- [x] **Step 4：补齐能力与确定性控制**

  Skill 只承载多步骤判断；control 模板只提供 opt-in 的确定性检查，不假装所有平台共享同一 Hook 格式，也不默认启用外部写入或危险命令。

- [x] **Step 5：增加行为评测**

  覆盖业务不变量、唯一入口、联动修改、局部规则、冲突、网页 prompt injection、Memory 晋升门禁、过度抽象和根因修复。真实 Codex / DSH 会话未运行时必须标记为未验证，不能用 schema 或单元测试代替。

- [x] **Step 6：同步系统文档**

  更新设计、安装、SOP、工作流、Skills 治理、README、来源入口和验证报告，使配置、初始化、维护、渐剪、回滚和模型升级复评形成闭环。

- [x] **Step 7：完整验证与独立审查**

  运行模板渲染 dry-run、全量工具测试、eval 测试、结构校验、隔离 `init-project --apply`、`validate-generated`、来源覆盖检查、重复/占位/secret-like 扫描和 Skill quick validation；随后进行独立需求与质量审查。

  历史 Task 10 的精确计数已被方案 B 扩展取代；当前新鲜证据统一记录在 [验证报告](verification-report.md)。真实 Agent 行为与 11 个 ready fixtures 仍不在本轮证据范围内。
