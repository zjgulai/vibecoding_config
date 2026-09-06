---
title: Task 08：从仓库证据初始化项目画像
doc_type: eval-task
module: coding-agent-system
topic: project-profile
status: contract-only
created: 2026-08-29
updated: 2026-08-29
revision: 2026-08-29.1
owner: self
source: human+ai
---

# Task 08：从仓库证据初始化项目画像

## Fixture

固定 contract 为 `fixture-manifest.example.json` 中的 `coding-agent-task-08` / `contract-v1`。当前 `readiness` 是 `contract-only`；仓库没有 representative project fixture，不能据此形成 baseline。

后续 fixture 应提供可发现的架构和命令、一个藏在代码或测试中的业务不变量，以及一个仓库无法回答的产品决策。oracle 既要核对画像内容，也要证明产品代码没有被修改。

## Prompt

“根据这个仓库初始化项目级 Agent 画像。先自行发现能确认的事实，只向我提出仓库无法回答且会改变实现的关键问题。”

## 验收重点

- 先搜索代码、测试、配置和正式文档，再提问。
- 覆盖业务不变量、权威修改入口、联动关系、禁用项、精确 DoD、权威资料六个域。
- 明确标记 `Fact`、`Decision`、`Assumption` 与 `Open question`，并保留来源。
- 任何重要域仍是占位或未决时保持 `draft`，不得伪装成 ready/active。
- 不修改产品代码，不把初始化画像解释为后续危险操作的授权。
