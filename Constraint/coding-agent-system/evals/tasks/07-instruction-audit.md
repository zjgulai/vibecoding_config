---
title: Task 07：审计并分层一组 Agent 指令
doc_type: eval-task
module: coding-agent-system
topic: instruction-audit
status: contract-only
created: 2026-08-29
updated: 2026-08-29
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 07：审计并分层一组 Agent 指令

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-07` / `contract-v1`。当前 `readiness` 是 `contract-only`；仓库没有交付 representative 指令包和 oracle，不能据此判断任一 Agent 会正确审计规则。

后续 fixture 应包含：重复的常驻规则、一个确有价值的局部规则、一个多步骤工作流、一个无证据的量化收益声明，以及一个被误写为共享 prose 的平台专属 control。每条输入都要有稳定 ID，oracle 必须逐项核对 disposition 与目标层。

## Prompt

“审计这组用户级和项目级 coding-agent 指令。不要直接覆盖源文件；给出每条规则的处置、依据和建议落点，并标出仍需证据的主张。”

## 验收重点

- 先判断规则是否改变可观察行为、是否应常驻、是否有充分证据。
- 每条输入只能明确归为 `retain`、`rewrite`、`move`、`delete` 或 `needs-evidence`。
- 区分用户核心、项目画像、局部规则、Skill、文档和确定性 control。
- 不把平台专属 Hook 伪装成跨平台共享格式，不复制相互冲突的规则。
- 不因完成静态审计就宣称真实 Agent 质量或效率已提高。
