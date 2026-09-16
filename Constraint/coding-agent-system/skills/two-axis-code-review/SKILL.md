---
name: "two-axis-code-review"
description: "按 Standards 与 Spec 两个独立轴线审查代码变更；适用于 branch、PR、工作区 diff 或指定比较范围的证据化 review。"
metadata:
  source: "Method adapted from mattpocock/skills code-review (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Two-Axis Code Review

分别回答两个问题，避免“代码写得漂亮”掩盖“做错了东西”，或反过来：

- **Standards:** 变更是否符合仓库规则、接口惯例、安全边界和可维护性要求？
- **Spec:** 变更是否完整、准确地实现了已确认需求，且没有越界行为？

## Choose the path

- **Fast path:** 小 diff 可在一次阅读中完成，但 findings 仍按两个轴线分栏。
- **Full path:** 大 diff、跨模块或高风险变更分别建立两个审查上下文；有授权且环境支持时可并行评估，最终不跨轴线重排结论。

## Workflow

1. 固定 review scope：用户指定的 ref/diff 优先；否则使用当前工作区变更并明确范围。对 Git ref 先验证可解析，确认 diff 非空。不要擅自 fetch、切分支或改工作区。
2. 定位 spec 来源：用户给定材料、相关本地 spec/issue 内容或明确的验收条件。找不到时标记 `Spec unavailable`，不猜需求。
3. 定位 standards 来源：就近 `AGENTS.md`、贡献指南、工程规范、相关 ADR、公共接口和现有测试惯例。工具已经确定性检查的格式问题不重复人工报告。
4. 独立完成两轴审查：
   - Standards 轴报告有证据的正确性、安全性、兼容性、测试或维护风险；启发式 smell 标为判断，不冒充硬性规则。
   - Spec 轴逐项检查遗漏、部分实现、错误实现和 scope creep；每条 finding 引用对应要求，若没有来源则说明推断依据。
5. 对完成报告中的关键主张建立 `claim → observation → verdict` 表。报告、配置、绿色 CI 摘要或实现者自述都不是独立证据；在只读范围内重跑命名验证或检查实际 diff/运行状态，结论只能是 `Verified`、`Verified with caveats`、`Refuted` 或 `Unverified`。
6. 每条 finding 给出 severity、文件/行、触发条件、影响和最小修正方向。先 findings，后简短总结；没有 finding 时明确写 `No findings` 并列出未验证范围。若同一批准契约有多个目标实现，分别检查 reference contract 与 target-native 结果，不为单个 target 降低共同验收。

## Completion criterion

所有 changed behavior 都在两个轴线上被审视；findings 可定位、可复现并能追溯到代码与规则/需求证据。关键完成主张有独立 observation 和 verdict；两轴分别汇总，不用一个总分掩盖任何一轴。

## Authorization boundary

Review 是只读任务，不授权修改代码、创建 issue、安装依赖、commit、push、发布或执行危险/外部操作。用户另行要求修复时再进入实现流程。
