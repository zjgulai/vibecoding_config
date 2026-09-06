# Task 2 Report — prompts_ask 05–08

## Status

完成。仅新增 Task 2 的四份 `prompts_ask` 模块文件及本报告；未修改原始 `prompts/`，未执行 Git、依赖安装、外部动作或生产操作。

## Created files

- `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`

## Check summary

- 四个文件名与 Task 2 brief 一致，分别包含对应的 `M05`–`M08` 和 `A05`–`A08`。
- 每份均含 `Metadata`、`Facts`、`Decisions`、`Assumptions`、`Open questions`、`Risks and reversibility`、`Acceptance evidence`、`Handoff` 八段公共契约。
- 每份均含单问题协议及“为什么问 / 推荐答案 / 备选项影响 / 不知道”；回答后更新四类状态；信息充分后先请求生成确认。
- M05 保留领域语言、验收矩阵、test seams 与 G3 边界；M06 保留单一决策问题、可证伪假说、G4 与 `ALLOWED_FILES_OR_SANDBOX` 匹配写入门；M07 保留架构选项、Mermaid 无环 DAG 与垂直切片；M08 保留 G4、`ALLOWED_FILES`、`DEPENDENCY_CHANGES` 三重门，并要求 Debug 先稳定复现和证伪。
- 静态检查已运行：文件存在、M/A 编号、八段标题、四个代码围栏、单问题字段、M06/M08 高风险字段和 M08 Debug 要求均通过。

## Concerns

- 当前工作目录不是 Git 仓库，无法提供 Git 状态或 diff 证据；本任务未要求 commit。
- `prompts_ask/` 的完整 13 文件验收依赖其他并行任务；本报告只验证 Task 2 负责的 05–08。

## Review fixes

Changed lines:

- `prompts_ask/08-全栈实现与TDD.md`：`{{MODE}}` 默认值改为 `PLAN`；启动说明和启动门改为只有匹配的 G4、`ALLOWED_FILES`、`DEPENDENCY_CHANGES` 均已核验后才可明确切换至 `APPLY`。
- `prompts_ask/06-原型与UX验证.md`：新增实验结束后清理或隔离原型产物的规则；保留产物必须记录 Owner 和到期日期/条件；`Prototype disposition` 新增 Owner 字段。

Focused check command and output:

```text
set -e
rg -q '^\{\{MODE\}\} = PLAN$' prompts_ask/08-全栈实现与TDD.md
rg -q '明确切换为 MODE=APPLY' prompts_ask/08-全栈实现与TDD.md
rg -q 'G4_APPROVAL、ALLOWED_FILES 与 DEPENDENCY_CHANGES' prompts_ask/08-全栈实现与TDD.md
rg -q '清理或隔离原型产物' prompts_ask/06-原型与UX验证.md
rg -q '明确 Owner 和到期日期/条件' prompts_ask/06-原型与UX验证.md
rg -q 'Owner：<name/role>' prompts_ask/06-原型与UX验证.md

Output:
M08 PLAN default and explicit APPLY gate: ok
M06 cleanup, Owner, and expiry disposition: ok
14:{{MODE}} = PLAN
22:...默认 MODE=PLAN、只读。只有当前 slice 的 G4_APPROVAL、ALLOWED_FILES 和 DEPENDENCY_CHANGES 均精确匹配并已核验后，才可明确切换为 MODE=APPLY 并改代码。
40:6. 实验结束后清理或隔离原型产物；任何保留产物必须记录明确 Owner 和到期日期/条件。
70:Deleted | Isolated | Retained until <date/reason>；Owner：<name/role>。
```
