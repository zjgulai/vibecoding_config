---
title: Task 02：实现一条全栈垂直切片
doc_type: eval-task
module: coding-agent-system
topic: full-stack-feature
status: stable
created: 2026-08-29
updated: 2026-09-02
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 02：实现一条全栈垂直切片

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-02` / `contract-v1`。当前 `readiness` 是 `contract-only`，仓库未交付真实 Next.js/PostgreSQL/browser fixture，不能据此形成 baseline。

团队后续需要固定一个带现有测试的 Next.js API 与 PostgreSQL fixture，需求涉及一个新字段、API 返回值和页面展示；setup、reset、oracle、artifact 与 initial digest 必须满足 manifest contract。

## Prompt

“在客户详情中增加内部风险备注。备注只能由管理员编辑，普通成员只能查看。完成实现并验证。”

## 验收重点

- 先发现仓库的权限、迁移、测试和 UI 模式。
- 以一条可演示的垂直切片推进，而不是分别批量修改数据库、API 和 UI。
- 权限在服务端强制执行，不只隐藏按钮。
- 迁移有回滚或向前恢复说明。
- 执行相关测试、类型检查和页面运行验证。

## Future assessor criterion

未来 fixture 应同时诱导一个没有当前需求、不变量、失败模式或风险依据的新增层级，以及一个承载安全、兼容性或数据边界的必要 seam。Agent 只审查本次新增抽象，执行消融式删减检查：删除前者、保留后者并给出 trace，且所有行为、权限、migration、API、UI 和回归仍通过。LOC 更少或单次 green 不自动判优。

本节尚未绑定 `fixture-manifest.example.json` 的 `coding-agent-task-02` / `contract-v1`、oracle 或 pass condition，因此不是当前 runner 可执行断言，也不构成一次 contract revision 升级；当前仍是 `contract-only`。
