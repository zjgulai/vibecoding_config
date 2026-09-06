---
name: "tdd"
description: "用小步 red-green-refactor 循环实现行为或修复缺陷；适用于用户要求 TDD，或改动需要以自动化反馈约束实现时。"
metadata:
  source: "Method adapted from mattpocock/skills tdd (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Test-Driven Development

用测试推动一个可观察行为从 red 到 green，再在 green 上整理设计。

## Choose the path

- **Fast path:** 极小、边界明确的行为使用一个测试和一次最小实现；仍要亲眼看到测试先因目标行为失败，再因实现通过。
- **Full path:** 多个行为或高风险路径逐个 vertical slice 循环，上一轮的学习决定下一轮测试。

## Workflow

1. 找到调用者能观察到的 public seam 和仓库中的测试先例。优先现有 seam；若 seam 会改变架构或需求含义，先让用户确认。
2. 写一个只描述当前行为的测试。期望值来自规格、已知样例或独立 oracle，不能复算实现逻辑。
3. 运行最窄命令，确认测试以预期原因失败。测试意外通过、编译失败或因环境失败都不算 red；先修正反馈信号。
4. 只写让这个测试通过的最小生产代码，不提前实现后续案例。
5. 重跑目标测试并执行与改动风险相称的相关测试，确认 green。
6. 在 green 上重构，保持行为不变；每次结构调整后重跑测试。
7. 对下一个行为重复。一次只推进一个可验证 slice。

## Test quality

- 通过 public interface 验证调用者关心的行为；避免 private method、内部调用次数和结构快照。
- 只在系统边界 mock，例如外部 API、时间、随机性或隔离所需的文件系统；优先真实的内部协作者和测试数据库。
- 一个测试表达一个逻辑结果。重构不改变行为时，测试应继续通过。

## Completion criterion

每个新增行为都有已观察到的 red→green 证据，目标测试和相关回归测试通过，重构后仍 green；未运行或因环境阻塞的检查明确列出。

## Authorization boundary

TDD 循环不授权安装依赖、修改外部服务或数据、commit、push、发布或执行危险操作。需要这些动作时停在当前可验证状态并请求明确授权。
