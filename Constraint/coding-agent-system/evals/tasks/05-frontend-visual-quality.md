---
title: Task 05：实现并视觉检查用户界面
doc_type: eval-task
module: coding-agent-system
topic: frontend-visual-quality
status: stable
created: 2026-08-29
updated: 2026-09-02
revision: 2026-09-02.1
owner: self
source: human+ai
---

# Task 05：实现并视觉检查用户界面

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-05` / `contract-v1`。当前 `readiness` 是 `contract-only`，仓库未交付真实 browser fixture，不能据此形成 baseline。

团队后续需要固定一个已有 design tokens、组件库和 Playwright 的响应式 Web 应用。它提供目标流程和内容，不提供像素级稿件；setup、reset、oracle、artifact 与 initial digest 必须满足 manifest contract。

## Prompt

“为首次创建项目的用户设计 onboarding 页面。它需要解释三个步骤、支持跳过，并在移动端可用。”

## 验收重点

- 复用现有 design system，不引入无关视觉体系。
- 信息层级、状态、键盘操作、对比度和移动端布局可用。
- 不用装饰性组件掩盖不清晰的信息架构。
- 使用浏览器检查关键 viewport、console、network 和交互。
- 截图或可观察证据与完成声明一致。
- **判失败：** 次要设置、开关或工具按钮没有任务、后果或风险依据，却比当前主操作更显著。
- **判失败：** 标准动作使用陌生图标，且核心含义只依赖 tooltip。
- **判失败：** 所谓视觉收敛降低文字可读性、可见 focus、对比度或交互命中区。
- **判失败：** 没有目标 viewport、关键状态和同屏比较证据，却声明视觉完成。
- **判失败：** 歧义、低频或高后果动作缺少可见文字标签，或危险动作缺少适当的 undo、review 或 confirm 保护。

以上是 `contract-only` fixture 的验收 oracle，不表示真实 browser fixture、视觉基线或 real-agent run 已交付、运行或通过。
