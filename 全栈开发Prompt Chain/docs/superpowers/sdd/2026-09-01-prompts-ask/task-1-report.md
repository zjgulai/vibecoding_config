# Task 1 Report

## Result

DONE

## Created files

- `全栈开发Prompt Chain/prompts_ask/01-项目初始化与治理.md`
- `全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md`
- `全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md`
- `全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md`

## Checks

- 文件名：`prompts_ask/` 中恰好为以上 4 个 Task 1 Markdown 文件。
- 模块和产物标识：M01–M04 与 A01–A04 均存在且编号匹配。
- 公共契约：每份均包含 `Metadata`、`Facts`、`Decisions`、`Assumptions`、`Open questions`、`Risks and reversibility`、`Acceptance evidence`、`Handoff` 八段。
- 格式：每份均有一对可复制 Prompt 代码围栏。
- 协议：每份均含“每轮只问一个”、推荐答案与“不知道”处理。

## Concerns

无。检查为静态文件级检查；未执行外部动作、Git 操作或运行时测试。

## Review fix

已修复两项审查发现：

- M01 恢复条件式 `project-profile` 加载规则，并补充创建 Agent 指令时可加载 `writing-for-agents`；两者未安装时均明确使用 Prompt 回退且不得声称已加载。
- M02 恢复技术或标准事实会改变结论时的条件式 `technical-research` 加载规则；未安装时明确使用 Prompt 回退且不得声称已加载。

验证命令与输出：

```text
rg -n "project-profile|writing-for-agents|technical-research|未安装|不得声称已加载" \
  全栈开发Prompt\ Chain/prompts_ask/01-项目初始化与治理.md \
  全栈开发Prompt\ Chain/prompts_ask/02-机会与市场调研.md

M01: project-profile、writing-for-agents、未安装回退和禁止虚假加载声明均命中。
M02: technical-research、未安装回退和禁止虚假加载声明均命中。
```

实际复跑结果：

```text
file names: PASS (01-项目初始化与治理.md 02-机会与市场调研.md 03-用户研究与问题定义.md 04-产品策略与范围决策.md)
M01/A01 + eight headings + fenced prompt + single-question protocol: PASS
M02/A02 + eight headings + fenced prompt + single-question protocol: PASS
M03/A03 + eight headings + fenced prompt + single-question protocol: PASS
M04/A04 + eight headings + fenced prompt + single-question protocol: PASS
22: M01 命中 project-profile、writing-for-agents 和未安装回退声明。
16: M02 命中 technical-research 和未安装回退声明。
```
