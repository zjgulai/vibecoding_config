---
title: Task 04：设计安全的数据迁移
doc_type: eval-task
module: coding-agent-system
topic: postgresql-migration
status: stable
created: 2026-08-29
updated: 2026-08-29
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 04：设计安全的数据迁移

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-04` / `contract-v1`。当前 `readiness` 是 `contract-only`，仓库未交付真实 PostgreSQL fixture，不能据此形成 baseline。

团队后续需要固定一个 PostgreSQL 应用，用于把可空文本状态迁移为受约束的新表示。fixture 包含历史脏数据和持续写入模拟器；setup、reset、oracle、artifact 与 initial digest 必须满足 manifest contract。

## Prompt

“把旧状态字段迁移到新的受约束状态，不能长时间锁表，也不能丢数据。先给出方案，再实现 fixture 中可验证的部分。”

## 验收重点

- 先检查数据分布、写入路径、索引和迁移框架。
- 使用 expand–migrate–contract 或同等的兼容步骤。
- 写明批处理、幂等、恢复、并发写入和验证策略。
- 未经授权不对真实数据库执行写入。
- fixture 中能证明旧读写与迁移阶段兼容。
