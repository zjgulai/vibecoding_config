---
title: Task 06：按规格与工程标准审查变更
doc_type: eval-task
module: coding-agent-system
topic: two-axis-review
status: stable
created: 2026-08-29
updated: 2026-09-02
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 06：按规格与工程标准审查变更

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-06` / `contract-v1`。当前 `readiness` 是 `contract-only`，仓库未交付 representative fixture，不能据此形成 baseline。

团队后续需要固定一个包含明确 issue/spec、项目规范和候选 diff 的仓库。diff 同时包含一个需求遗漏、一个范围外功能和一个低影响代码异味；setup、reset、oracle、artifact 与 initial digest 必须满足 manifest contract。由于 fixture digest 明确排除 `.git`，fixture root 还必须包含一个普通控制文件记录期望 review-base commit/ref；固定在 digest 中的 `fixture-control` 必须在 reset、setup 和 oracle 中把实际 Git HEAD/base 与该文件核对，并把解析后的 base 写入 `review-base.txt`。仅有相同工作树不能证明 review base 相同。

## Prompt

“审查当前分支相对基线的改动，只报告可执行问题，不修改代码。”

## 验收重点

- 固定并验证 review base。
- 分开检查 Spec compliance 与 Engineering standards。
- 每个 finding 指向具体文件、范围和证据。
- 区分阻塞问题、判断性建议和非问题。
- 不执行修复、commit 或外部 PR 操作。

## Future assessor criterion

未来 assessor 应从本次 diff 中识别无依据复杂度、必要风险 seam 与范围外历史清理，并核对消融式删减检查；若把有兼容性、安全、可测试性或可观测性依据的 seam 误报为删减对象，则评测失败。审查保持只读，不执行修复、commit 或外部 PR。

本节尚未绑定 `coding-agent-task-06` / `contract-v1` 的 manifest oracle 或 pass condition，因此不是当前 runner 可执行断言；当前仍是 `contract-only`。
