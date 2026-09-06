---
name: "project-profile"
description: "初始化或审计项目的长期隐性知识画像；仅在用户明确要求梳理项目不变量、权威入口、联动关系或画像就绪度时使用，不代替需求发现、规格编写或实现。"
metadata:
  invocation: "explicit-only"
---

# Project Profile

从仓库证据生成或审计 `.agents/project-profile.md`，让后续 agent 知道项目特有的不变量和正确入口，而不是把通用工程建议写成项目事实。

## Operating modes

- **Initialize:** 仓库尚无可信画像时，发现事实并提出一份画像草案。
- **Audit:** 画像已存在时，检查每项是否仍有证据、是否冲突、是否遗漏会改变实现的项目知识。

开始时先读取适用的 instruction chain、README、架构与工程文档、构建/依赖配置、CI、生成声明、相关代码和测试。能从仓库查明的事实不问用户；不读取或复述 secrets。只有仓库材料无法决定、且答案会实质改变画像时才询问用户。

## Evidence model

调查记录中的所有结论标为以下一种，并附仓库路径、配置项、测试或已确认决定作为来源：

- `Fact`：当前仓库可直接验证。
- `Decision`：由权威项目记录或用户明确确认。
- `Not applicable`：有来源地说明某领域为何不适用于当前项目或任务，并写清适用边界；不能只写 `N/A` 或“无”。
- `Assumption`：暂用于推进但尚未验证，不能作为不变量。
- `Open question`：缺失且会改变后续行为的决定。

发现冲突时保留双方来源，按项目明示的权威顺序判断；没有足够依据时列为 Open question，不静默拼接。

写入 `active` 画像时只保留已证实的 `Fact`、已确认的 `Decision` 与有边界证据的 `Not applicable`。每个规定 H2 只能出现一次，不新增自定义 H2；每个域使用一组或多组固定条目：

```markdown
- Fact: README 声明配置必须从生成源修改
  Source: path:README.md
- Decision: 维护者确认发布前必须运行完整 smoke
  Source: user-confirmation:2026-08-29:release-review
- Not applicable: 本仓库不持久化业务数据，因此当前项目没有 database migration 域
  Source: path:README.md
```

`Source` 只允许四种受控形式：`path:<项目相对路径>`、`command:<可复现命令>`、`url:<http(s) URL>`、`user-confirmation:<YYYY-MM-DD>:<确认上下文>`。不要把绝对路径、父目录路径、无日期的“用户说过”、不可复现描述或简单文本伪装成来源。

## Six domains

画像必须路由这六类项目知识，并单列路径级局部风险：

1. 业务与安全不变量。
2. 权威修改入口，包括生成源而非生成结果。
3. 必须同步变更的联动关系。
4. Do NOT 与受保护区域。
5. 精确、可运行或可观察的 Definition of Done。
6. 权威资料与冲突顺序。

只写会改变 agent 决策的项目事实；版本、命令、路径或约定必须能从当前仓库验证。不要复制整份 README、通用 coding 守则或短期任务流水。

## Readiness gate

默认先给 dry-run：按域列出证据、冲突、缺口、拟议画像或 diff，以及 `draft` / `active` 判定。缺少任何会改变架构、数据、权限、安全、兼容性或验收的材料事实时，必须保持 `profile_status: draft`；不得用占位符、猜测或形式完整来伪造 ready。

只有七域都包含至少一条结构化 `Fact` / `Decision` / `Not applicable`、每条都有受控 `Source`，且无未决重大冲突时，才建议 `active`。核心域不得用 `Not applicable` 豁免；非核心域只有在理由明确描述范围、未承认该领域仍与当前任务相关时才可关闭。`x`、`N/A`、“待定”“未确认”“无”等低信息值不算结论；fenced block、HTML comment、HTML 隐藏元素、零宽字符或双向控制字符属于隐藏非结构化内容，active 域必须整体拒绝，不能清洗后继续。没有额外局部风险时也要用有范围和来源的 `Not applicable` 说明，而不是留空。仓库变化使来源失效时，画像退回 draft 直到复核。

只有当前用户请求明确要求创建或更新本地画像时才写 `.agents/project-profile.md`；否则只给 dry-run。即使获准写画像，也不因此获得修改代码、需求、spec、规则、CI 或外部系统的授权。

## Completion criterion

七域都有结构化、可追溯的 Fact / Decision / 合规 Not applicable；Assumption 与 Open question 未进入 active 画像；规定 H2 无缺失、重复或未知项；就绪状态与材料缺口一致。另一 agent 能据此找到正确入口和完成检查，但不会把未知项误当项目事实。
