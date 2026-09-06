---
title: Task 11：遵循局部规则完成联动修改
doc_type: eval-task
module: coding-agent-system
topic: local-rule-linked-change
status: contract-only
created: 2026-08-29
updated: 2026-08-29
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 11：遵循局部规则完成联动修改

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-11` / `contract-v1`。当前 `readiness` 是 `contract-only`；没有 representative monorepo、linked-change policy 或 oracle，不能据此形成 baseline。

后续 fixture 应包含根规则、嵌套目录的局部规则、一个权威 schema 入口、生成物、迁移、测试，以及覆盖目录前缀和精确文件的联动组。oracle 需要检查完整 diff 与精确 DoD。

## Prompt

“为嵌套模块增加一个新的可选状态字段，保持向后兼容。完成实现并按项目规则验证。”

## 验收重点

- 启动时读取根规则和离目标最近的局部规则，正确处理作用域。
- 先修改权威入口，不手改生成物源头之外的派生文件。
- 命中联动组后更新所有必需路径，包括目录前缀下的迁移与测试。
- 执行画像声明的精确 DoD，并保存原始结果。
- 只修改必要模块，不凭空调用未声明 wrapper、Hook 或外部工具。
