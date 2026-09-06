# Task 1: 建立 Codex UI 规则入口与单一事实源

## Context

本任务是已批准的方案 B 第一阶段。只建立 Codex 用户/项目入口和完整 UI 条件模块；评测、SOP、Prompt 与追踪由后续任务完成。当前目录不是 Git 仓库，不 commit；所有人工编辑必须使用 `apply_patch`。

## Global constraints

- 只面向 Codex CLI，不修改 shared core、Claude、DSH、Cursor、旧 `Constraint/Codex_AGENTS.md` 或任何 zip。
- 不修改真实 `~/.codex/AGENTS.md`。
- `templates/modules/frontend-visual-quality.md` 是完整 UI 操作清单的单一事实源；两个 AGENTS 只保留触发、偏置或路由。
- 视觉显著性与任务的重要性、后果和紧迫性匹配；任务型界面默认克制，但不得牺牲可发现性、可读性、可访问性、命中区或风险表达。
- `hover`、`tooltip`、颜色和动效不能成为核心语义的唯一通道。
- 不隐式新增组件、图标、字体或其他依赖。

## Files

- Modify: `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`
- Modify: `Constraint/coding-agent-system/templates/project/codex/AGENTS.md`
- Modify: `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`
- Report: `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-1-report.md`

## Before hashes

- `templates/user/codex/AGENTS.md`: `62af0b665069728706ecb57af99b3b3078432b4569dc6ff184978278099e1c6b`
- `templates/project/codex/AGENTS.md`: `8dd4f69c7c1ba2ada6e8049b054557245ba045a3898dc5d908f0f6ed9d5ab6c2`
- `templates/modules/frontend-visual-quality.md`: `44704ede0170a04835d0915e2f239ec427ed332a320b0ad5166df91c50594313`

## Requirements

0. 在编辑前，按实施计划 Task 1 Step 1 对 shared core、Claude、DSH、Cursor、平台中立项目入口、旧 `Constraint/Codex_AGENTS.md` 和两个 zip 计算完整 SHA-256 基线，并写入报告；这些文件不得修改，Task 5 将用相同清单逐行比对。
1. 在 Codex 用户模板共享块之外新增紧凑的「用户可见界面默认偏置」：只在 UI 任务触发；项目视觉模块存在时先读，不存在时不虚报；任务型界面默认克制且显著性匹配任务；复用项目设计语言；完成真实渲染/同屏检查，工具不可用则标记未验证。不得复制完整清单。
2. 在 Codex 项目模板新增条件路由：UI 任务且 `.agents/rules/frontend-visual-quality.md` 存在时必须读取；不存在时沿用用户级基线与项目规范，报告模块缺口，不臆造文件。不要修改平台中立项目模板或受管路由块。
3. 在视觉模块的事实发现阶段增加：界面类型（任务型、营销/品牌、专家高密度、安全关键）、主/次/高风险操作、输入方式、信息密度、使用频率、同屏基准、图标来源。
4. 新增完整「视觉显著性、尺寸与图标」规则：
   - 任务型界面默认克制；营销、品牌、关键警告和不可逆动作可因职责加强表达，但要有规格、任务或风险依据。
   - 尺寸/间距优先复用 design tokens、组件规格和平台惯例，再结合 viewport、输入方式、密度、频率、层级；不靠单纯放大建立层级。
   - 当前主任务中的辅助入口、设置、开关、工具按钮默认次级但可发现；若其本身是主任务或涉及安全、隐私、无障碍、关键状态，则按实际优先级处理。
   - 常见动作复用项目现有组件/图标家族、系统符号或行业通用隐喻；不混用家族，不为单页新增依赖；歧义、低频、高后果动作配可见文字。
   - Icon-only 控件有正确语义、accessible name、可见 focus、明确状态和足够命中区；装饰图标不进入 accessibility tree。
   - 静止态优先通过位置、分组、排版、间距、对比、分隔和状态建立层级；颜色、hover、tooltip、动效只作补充。
   - 没有任务、平台或品牌依据时避免夸张尺寸、重色块、过度圆角、厚边框、强阴影和装饰性渐变。
5. 扩充验证：记录页面、viewport、主题、状态、同屏比较基准与结果；检查相对尺度/填充/对比/字重/边框/阴影/elevation/密度，静止态可理解，次要控件不压过主操作，危险动作有标签及适当 undo/review/confirm。调整后复验可读性、命中区、focus、状态；没有实际页面检查不得宣称视觉通过。
6. 保留现有响应式、状态、键盘、reduced motion、design token 和禁止单页新增依赖等规则，消除重复而不丢条件。

## Verification

从 `Constraint/coding-agent-system` 运行：

```bash
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py validate .
```

预期：`render-templates` 只列既有 shared snapshot 目标；`validate .` 输出 `VALID`。不得运行 `render-templates --apply`。

同时记录三个目标文件的 after SHA-256、native/readable byte size、UTF-8 与 Markdown fence 检查。完整报告必须写入指定 report 文件；最终回复只给 DONE 状态、无 commit、测试摘要、concerns 和报告路径。
