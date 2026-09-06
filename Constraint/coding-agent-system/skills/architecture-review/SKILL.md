---
name: "architecture-review"
description: "显式审查指定热点或受限范围的架构摩擦与改进候选；仅用于用户要求架构 review，不代替实现或自动扫描整个代码库。"
metadata:
  invocation: "explicit-only"
  source: "Method independently adapted from mattpocock/skills improve-codebase-architecture (MIT) at 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76."
---

# Architecture Review

先把 review 限定到用户指定的模块、痛点或变更热点；若没有范围，提出一个小的候选范围并说明依据，再开始。不要默认扫描整个代码库、推断 Git 历史、或把普通重构建议包装成架构问题。

## Review workflow

1. 读取范围内的接口、调用者、测试、相关领域语言和既有设计决定。把已观察到的事实与设计判断分开。
2. 按 `codebase-design` 的 module、interface、seam、adapter、leverage 和 locality 词汇，找出有限数量的可行动候选；现有 ADR 只在有真实摩擦证据时才建议重新评估。
3. 对每个候选说明当前症状、证据、可能改动、预期收益、失败模式和推荐强度。使用 [references/report-format.md](references/report-format.md) 的报告结构；没有足够证据时明确为 speculative。
4. 给出推荐次序和仍需验证的问题，然后等待用户选择是否探索或实施。不得在 review 中自动改代码、创建仓库文件、提交或发布。

## Completion criterion

输出的候选可追溯到受限范围内的证据，推荐强度反映证据质量，并且失败模式与未知项可见；没有可靠候选时如实报告这一结果。

## Authorization boundary

本 skill 是只读 review。它不授权修改代码、生成仓库文件、创建 issue、安装依赖、commit、push、发布或调用外部写入；后续行动须由用户明确授权。
