---
title: Coding Agent 系统方案 B 优化计划
doc_type: plan
module: coding-agent-system
topic: evidence-driven-configuration-repair
status: stable
created: 2026-08-30
updated: 2026-08-30
owner: self
source: human+ai
---

# 方案 B 优化计划

## 目标

修复上一版交付物中「规则已记录但运行时不可达」「直接配置依赖缺失配套文件」「项目画像门槛过重」「生成器阻止项目扩展」和「证据状态高于实际验证强度」的问题，同时保留共享语义核心、薄平台适配器和最小权限边界。

## 全局约束

- 目标平台仅包括 Codex 与 DSH Desktop / DeepSeek Harness。Cursor 只作为经验来源。
- 不要求输出隐藏 Chain-of-Thought，不采用固定质量倍数、token 配额或通用行数硬限制。
- 不把具体技术栈、私有 wrapper、Hook 或 MCP 配置写入通用核心。
- 不读取或输出秘密；不修改真实用户配置；所有安装验证在隔离临时目录完成。
- 当前工作区不是 Git 仓库，因此不创建 commit，也不以 Git diff 作为完成证据。
- 新增或改变 Python 行为时先写失败测试并观察预期失败。

## 任务

1. [x] 修复用户级与项目级常驻核心，并更新 Codex、DSH 平台适配说明。
2. [x] 为生成项目建立可达的技术栈模块路由；让项目级直接文件在缺少配套文件时仍可使用。
3. [x] 将项目画像 readiness 改为按相关领域和风险判断，并支持有证据的 `not-applicable`。
4. [x] 将生成器所有权与项目扩展分开，允许合规的项目 Skill 和 Skill supporting resources。
5. [x] 补齐 `technical-research`、`domain-modeling`、`codebase-design`、`architecture-review` 与 `implementation-orchestration`。
6. [x] 建立原子级 tips 决策矩阵，并修正来源、规则、平台 claims 与验证状态。
7. [x] 同步 README、SOP、workflow、Skill 治理、模型配置和验证报告。
8. [x] 执行全量测试、Skill 校验、隔离项目/用户生成、静态安全检查和独立审查。

## 完成标准

- 生成项目的每个已选模块都能从根 `AGENTS.md` 到达，并带准确触发条件。
- 两份项目级平台模板可单独复制；缺少 `.agents/` 配套文件时不会要求读取不存在路径。
- 与任务无关的 profile 领域不会阻塞普通实现；高风险任务仍有严格证据门。
- 项目可以新增合规 Skill；官方支持的 `references/`、`scripts/`、`assets/` 不再被封闭白名单误拒。
- 所有采纳、改写采纳、条件采纳、排除和延期项都有来源、理由、实际产物、可达性和验证状态。
- 测试和校验报告明确区分静态检查、隔离 smoke、真实平台 discovery 与真实 Agent 行为。

## 完成证据

- 输入覆盖：29 份本地实质材料、7 个去重外链、76 条连续唯一原子 tip；50 条进入常驻/改写/路由采用，10 条条件采用，16 条排除、延期或排除原表述。
- 交付结构：四份 Codex / DSH 直接 `AGENTS.md`、5 个条件模块、15 个 `static-baseline` Skills，其中 7 个 explicit-only。
- 新鲜回归：tools 117/117、evals 60/60、Skills 15/15，`validate .` 为 `VALID`。
- 隔离 smoke：project、Codex user、DSH user 均为 `VALID-GENERATED`；170 个生成文件延迟 25 秒复测为 0 native/stream mismatch。
- 安全门：不同平台设置人工合并且失败前无部分写入；profile preamble、动态 secret-like 内容、项目 Skill 敏感路径/custom explicit-only/self-loop symlink 均 fail closed。
- 独立审查：生成器安全 focused repro 与四份直接 AGENTS 内容复审均为 PASS；真实 Codex / DSH 行为仍未运行，11 个 eval 仍为 `contract-only`。
