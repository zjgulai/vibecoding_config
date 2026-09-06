---
name: "domain-modeling"
description: "澄清并检验代码库的共享业务语言、概念边界与关键决策记录；适用于术语冲突、领域关系或 ADR 是否必要的设计讨论。"
metadata:
  source: "Method independently adapted from mattpocock/skills domain-modeling (MIT) at 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76."
---

# Domain Modeling

建立可被人和代码共同使用的 shared language；它描述业务概念和边界，不把实现细节伪装成领域事实。

## Work with the language

1. 从用户用语、已有 glossary/context、规格、测试和实际代码找出术语。术语含义冲突、过载或缺少边界时明确指出，而不是自行合并。
2. 用具体情景检验术语：谁触发什么事件、哪些状态或关系允许/不允许、边界情况如何解释。情景与代码证据相矛盾时，分别报告“当前代码行为”和“待确认的模型”，请相关方裁决。
3. 将已确认术语、定义、反例和不变量保持在适当的 context 记录中；需要新增或更新格式时，读取 [references/context-format.md](references/context-format.md)。仅在用户已授权的文件和范围内写入；否则在回复中提供候选文本。

## ADR discipline

只在一个决定同时满足以下条件时建议 ADR：改变代价显著、没有背景会令人困惑、且确有替代方案与真实权衡。满足后，按 [references/adr-format.md](references/adr-format.md) 组织内容；仍仅在授权范围内创建或修改文件。

不把一次命名、显而易见的实现选择或尚未决策的问题升级为 ADR。

## Completion criterion

关键术语可通过情景和相关代码证据解释，已确认语言与未决分歧分开呈现；若记录决定，读者能看到它为何值得记录及其取舍。

## Authorization boundary

本 skill 不授权创建 `CONTEXT`/ADR 文件、改代码、安装依赖、提交、推送或写入外部系统。任何持久化记录均需用户或项目规则明确覆盖该目标范围。
