---
title: Task 03：诊断间歇性缺陷
doc_type: eval-task
module: coding-agent-system
topic: systematic-debugging
status: stable
created: 2026-08-29
updated: 2026-08-29
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 03：诊断间歇性缺陷

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-03` / `contract-v1`。当前 `readiness` 是 `contract-only`，仓库未交付 representative fixture，不能据此形成 baseline。

团队后续需要固定一个具有可控时钟和并发测试工具的服务。测试报告指出订单状态偶尔从 `paid` 回退为 `pending`，但没有稳定复现步骤；setup、reset、oracle、artifact 与 initial digest 必须满足 manifest contract。

## Prompt

“这个状态回退问题在线上偶发。请找出根因并修复。”

## 验收重点

- 在改代码前建立能提高复现率的反馈信号。
- 明确区分观测事实、假设和已证伪假设。
- 假设能预测新的观察结果，而不是事后解释。
- 修复后重跑原始复现路径和回归测试。
- 清除临时 instrumentation，不输出敏感日志。
