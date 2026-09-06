---
name: "codebase-design"
description: "用 deep module、interface 与 seam 的设计语言评估或重塑模块边界；适用于接口形状、适配器、可测试性和局部性取舍。"
metadata:
  source: "Method independently adapted from mattpocock/skills codebase-design (MIT) at 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76."
---

# Codebase Design

用一致词汇讨论可维护的模块边界：

- **module**：向调用者提供一个 interface 的代码单元。
- **interface**：调用者必须了解的完整契约，包括输入、结果、不变量、失败模式、顺序和性能约束。
- **seam**：可以在不改调用方的前提下改变行为的位置。
- **adapter**：在某个 seam 上满足 interface 的具体实现。
- **deep module**：以小而易学的 interface 隐藏较多行为，给调用者带来 **leverage**，并把知识、修改和验证集中为 **locality**。

## Design work

1. 从调用路径、约束和真实变化点开始，描述当前 interface 的成本及其给调用者的 leverage/locality；不要仅按文件大小判断深浅。
2. 选择 seam 时区分稳定的调用契约和内部实现。测试优先通过调用者会跨越的 interface 验证行为，而不是为测试暴露内部结构。
3. 仅当已有真实变化、独立替换需求或明确的隔离价值时引入 adapter/seam。一个单实现的假想替换点不是足以增加抽象的理由。
4. 若一个依赖簇反复向调用者泄漏知识，按 [references/deepening.md](references/deepening.md) 检查能否把行为收进更 deep 的 module。
5. 有关键但尚未定型的 interface 取舍时，可选择 design-it-twice：比较两个或更多明显不同的设计，再按 leverage、locality、失败模式与迁移成本选择。它是可选探索，不强制并行分支或多 agent；见 [references/design-alternatives.md](references/design-alternatives.md)。

## Completion criterion

推荐清楚说明 interface、seam 和实现责任的边界，并用真实调用、变化或测试需求证明其 leverage/locality；不以虚构的可替换性证明抽象。

## Authorization boundary

设计分析不自动授权重构、写代码、创建分支、安装依赖、commit、push 或部署。实施需要相应任务的明确授权。
