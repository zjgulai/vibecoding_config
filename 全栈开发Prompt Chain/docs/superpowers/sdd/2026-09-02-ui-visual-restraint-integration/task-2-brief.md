# Task 2: 建立 UI 规则的 SOP、行为评测与来源追踪

## Context

本任务执行已批准实施计划的第二阶段。Task 1 已建立 Codex 用户/项目入口与 `frontend-visual-quality.md` 单一事实源，并以 `Approved with documented exception` 通过独立审查；本任务只投影可失败的 EVAL contract、生命周期步骤及来源追踪，不重新定义视觉规则。当前目录不是 Git 仓库，不 commit；所有人工编辑必须使用 `apply_patch`。

开始前完整阅读：

- `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-02-ui-visual-restraint-integration-design.md`
- `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ui-visual-restraint-integration.md` 的 Global Constraints 与 Task 2
- `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`
- 本任务列出的六个目标文件

## Global constraints

- 只面向 Codex CLI，不修改任何 AGENTS、Claude、DSH、Cursor、Prompt 或 zip 文件。
- `templates/modules/frontend-visual-quality.md` 仍是完整 UI 操作规则的单一事实源；本任务文件只承载阶段动作、失败条件和追踪元数据。
- 视觉克制不得牺牲可发现性、可读性、可访问性、命中区或风险表达；`hover`、`tooltip`、颜色与动效不是核心语义的唯一通道。
- EVAL-05 保持 `contract-only`，不得暗示真实 browser fixture、real-agent run 或视觉通过。
- 原始本地材料审计仍是 29 个内容文件；会话新增来源 LOC-030 只增加追踪来源总数，不篡改历史文件计数。
- JSON 只使用现有 schema/词汇；路径必须能相对 `Constraint/coding-agent-system/` 解析到实际文件。Prompt 文件当前尚未由 Tasks 3–4 更新，但其既有路径确实存在；不得将规则行为写成已经运行过。

## Files

- Modify: `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md`
- Modify: `Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
- Modify: `Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
- Modify: `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
- Modify: `Constraint/coding-agent-system/docs/research/local-material-audit.md`
- Modify: `Constraint/coding-agent-system/sources/rule-traceability.json`
- Report: `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-2-report.md`

不得修改其他文件。

## Before hashes

- `evals/tasks/05-frontend-visual-quality.md`: `7266de94fb1eb1bd2c217c394d297ec746a998d99337ae91ccd2c0f53bbd4a27`
- `docs/sop/project-lifecycle.md`: `f8bd8ba419482492336c23bb987c97b41ee7cb5cd94089551b87e7e92e9aef64`
- `docs/research/local-tip-ledger.md`: `700b778d77a30a53e372d5a2485396ef6f08a262ea5cd40a4c8554432ff94ac8`
- `docs/research/tip-decision-matrix.md`: `6672fb9ed556bf3a7e87b1723aa44419a38b3a3ba7b80c4778016efdfd25af26`
- `docs/research/local-material-audit.md`: `656c26a92a20de579f387c9eb4eca4de5383aa4a04c244685c4c271da5bb1177`
- `sources/rule-traceability.json`: `70abcafe62bd6d6c318f12c480a172c6cc6392b96ab492c439b9b017082dabf4`

## Requirements

1. 扩充 EVAL-05 的「验收重点」，至少使以下行为可明确判失败：
   - 次要设置、开关或工具按钮无依据地比当前主操作更显著。
   - 标准动作使用陌生图标，核心含义只依赖 tooltip。
   - 所谓视觉收敛降低文字可读性、focus、对比度或交互命中区。
   - 没有目标 viewport、关键状态与同屏比较证据，却声明视觉完成。
   保留 fixture 的 `contract-only` 事实，不写成已运行或已通过。
2. 扩充 SOP 阶段 9 的前端专项：先确认界面类型、主/次/风险操作、输入方式和同屏基准；验证静止态层级、通用图标语义、icon-only accessible name 与命中区；实际渲染后比较相对尺度、视觉重量和密度；调整后复验可读性、focus 与命中区。CLI 没有浏览器、截图或视觉回归工具时记录未验证范围，不依赖 Codex Desktop 右侧面板。
3. 在 `local-tip-ledger.md` 登记 `LOC-030`：来源为用户于 2026-09-02 明确提供并确认采用的 UI 设计经验；采用方式是 Codex 用户模板最小偏置、前端视觉模块完整规则、生命周期 Prompt 与 EVAL-05 的分层改写；条件化品牌/营销、安全、无障碍、主任务例外，tooltip 不承担核心语义，视觉图形尺寸与交互命中区分离；排除跨场景绝对禁止和「只有用户要求才可强调」。不得把它伪装成原始 29 个本地文件之一。
4. 在 `tip-decision-matrix.md` 新增 `TIP-077`：原子经验为「任务型界面默认克制，视觉显著性按任务重要性、后果和紧迫性决定；复用熟悉图标并以真实同屏证据验收」；决策为「条件采用并改写」；落点明确 Codex 用户偏置、frontend module、M05–M09 与 EVAL-05。把来源覆盖范围从 `LOC-001` 至 `LOC-029` 更新为 `LOC-001` 至 `LOC-030`，不得改写原始文件审计计数。
5. 在 `local-material-audit.md` 增加「后续来源」说明：LOC-030 是 2026-09-02 用户会话新增经验，不属于原始 29 个本地内容文件的逐文件审计；原始计数仍为 29。
6. 更新 `rule-traceability.json`：
   - `verified_on` 为 `2026-09-02`，`scope.local_source_count` 为 `30`。
   - 新增 `RUL-022`，`sources` 只含 `LOC-030`，decision 与 TIP-077 一致。
   - destination/artifacts 至少精确列出：`templates/user/codex/AGENTS.md`、`templates/project/codex/AGENTS.md`、`templates/modules/frontend-visual-quality.md`、`evals/tasks/05-frontend-visual-quality.md`，以及相对系统根解析的 `../../全栈开发Prompt Chain/prompts/{05,06,07,08,09}-*.md` 与 `../../全栈开发Prompt Chain/prompts_ask/{05,06,07,08,09}-*.md` 十个实际文件。请使用实际文件名逐项列出，不使用 glob。
   - artifacts 与 destination 使用同一组实际文件，artifact status 均为现有受支持值 `implemented`；不得使用模糊中间状态。
   - `eval_cases` 只含 `EVAL-05`，rule status 明确包含 `eval-contract-only; real-agent-not-run`。
   - `expiry_signal` 覆盖品牌/设计系统变更、平台可访问性要求变化、行为评测出现过度弱化或误判。
7. 更新适用 Markdown 的 `updated`/`revision` 元数据时延续文件既有格式；不为追求日期而重写无关 frontmatter。
8. 保持六个文件现有结构和语言风格，避免复制完整视觉模块；每个新增表述都可追溯到本任务要求。

## Verification

从 `Constraint/coding-agent-system` 运行并保存原始摘要：

```bash
python3 -m json.tool sources/rule-traceability.json >/dev/null
python3 tools/agent_system.py validate .
python3 -m unittest discover -s tools/tests -p 'test_*.py'
```

另做以下只读检查并记录结果：

- JSON 中 `RUL-022` 的 destination 与 artifact path 集合完全相等，所有路径从系统根解析后存在。
- `LOC-030`、`TIP-077`、`RUL-022` 各只定义一次，语义一致。
- 原始审计文档仍明确 29 个本地内容文件；source count 为 30 的原因只来自后续会话来源。
- 六个目标文件 UTF-8 可读、Markdown fence 平衡；记录 after SHA-256 及 native/readable byte size。

完整报告写入指定 report 文件，列出 exact changed files、requirements mapping、测试、after hashes、未验证项与 concerns。最终回复只给 DONE 状态、无 commit、测试摘要、concerns 和报告路径。
