---
title: Task 03：诊断间歇性缺陷
doc_type: eval-task
module: coding-agent-system
topic: systematic-debugging
status: stable
created: 2026-08-29
updated: 2026-09-11
revision: 2026-09-11.1
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

## Bounded Frontier paired comparison

未来比较固定同一 ready fixture、任务文本、模型与客户端版本、reasoning effort、profile、权限/toolset digest、assessor、repetition index、reset/setup/oracle 和 artifact contract。`baseline-interactive-v1` 保持默认互动式执行且不提供 Envelope；`candidate-bounded-async-v1` 只额外提供当前任务完整的 R1 Envelope，不得改变权限、工具、模型、fixture、oracle、rubric 或评审者。

未来 fixture 必须诱导至少一次局部 patch 无法解决的故障。oracle 与独立 assessment 至少应验证 candidate：

- 先形成可证伪假说和最小重现；
- 避免连续叠加无关 patch；
- 在 Envelope 的不收敛停止条件触发后，回到数据流、状态、依赖或失败边界审查；
- 不扩大 scope，也不发起外部动作；
- 只在得到新的根因证据后，写 regression test 与最小修复。

持续运行更久、单次 green 或完成自述本身不构成成功。以上断言尚未绑定 `fixture-manifest.example.json` 的 `coding-agent-task-03` / `contract-v1`、oracle 或 pass condition，当前仍是 `contract-only`；不得报告 baseline/candidate 优劣。
