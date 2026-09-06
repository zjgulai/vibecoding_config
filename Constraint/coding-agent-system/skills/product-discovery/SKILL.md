---
name: "product-discovery"
description: "通过依赖感知的产品访谈澄清问题、用户、约束与验收边界；仅在用户明确要求需求发现或方案压力测试时使用。"
metadata:
  invocation: "explicit-only"
  source: "Method adapted from mattpocock/skills grilling and grill-with-docs (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Product Discovery

把模糊想法收敛为可验证的产品决策；不在访谈结束前进入实现。

## Choose the path

- **Fast path:** 对低风险、边界清楚的小需求，复述目标、列出一个关键假设与验收条件；只询问会改变结果的缺失决策。
- **Full path:** 当目标、用户、流程、权限、数据或取舍互相依赖时，维护一棵 decision tree，按依赖顺序逐轮访谈。

## Full discovery

1. 先从对话、仓库和现有文档获取事实。不要把可自行查明的事实问给用户。
2. 区分 `Fact`、`Decision`、`Assumption` 和 `Open question`。把每个待决策项挂到它的前置决策下。
3. 每轮只询问当前 frontier：前置项已经确定、现在可以回答的问题。问题应编号，给出 2–3 个真实选项、影响和推荐答案。
4. 根据回答重算 frontier。新答案若推翻旧假设，显式修正记录，不悄悄保留冲突结论。
5. 收敛时总结：问题与用户、期望结果、核心流程、成功信号、约束、非目标、风险、尚未解决项和验收场景。
6. 请用户确认这份共同理解；未经确认，不把推断包装成决定。

## Completion criterion

完成时，所有会改变架构、数据、权限、UX 或兼容性的分支都已由用户决定或明确列为未决项，并且验收场景足以区分“做对了”和“只是做出来了”。

## Authorization boundary

本 skill 只产生发现结论。它不授权写代码、写 issue、安装依赖、commit、push、发布或执行任何外部/危险操作；这些动作需要用户在相应任务中明确授权。
