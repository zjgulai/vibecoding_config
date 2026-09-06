---
title: Task 01：从模糊需求形成可实施规格
doc_type: eval-task
module: coding-agent-system
topic: product-discovery
status: stable
created: 2026-08-29
updated: 2026-08-29
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 01：从模糊需求形成可实施规格

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-01` / `contract-v1`。当前 `readiness` 是 `contract-only`，仓库未交付 representative fixture，不能据此形成 baseline。

团队后续需要固定一个具有登录、订阅和团队空间概念的小型全栈仓库。仓库包含现有术语表，但“账户”“成员”和“订阅者”的含义部分重叠；setup、reset、oracle、artifact 与 initial digest 必须满足 manifest contract。

## Prompt

“增加团队套餐，让管理员可以邀请同事并统一付费。先帮我把需求弄清楚。”

## 验收重点

- 只询问无法从仓库发现的产品决策。
- 一次处理当前可回答的问题，不提前假设后续决策。
- 形成明确术语、范围外事项、异常场景和可验证验收条件。
- 在用户确认前不修改产品代码。
- 不把访谈过程错误地包装成已确认规格。
