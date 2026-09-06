---
name: "implementation-orchestration"
description: "显式把已确认的规格或 tickets 编排为可验证的小批次实现；不用于需求尚未确定时的自动执行或外部工作流写入。"
metadata:
  invocation: "explicit-only"
  source: "Method independently adapted from mattpocock/skills implement (MIT) at 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76."
---

# Implementation Orchestration

将已确认的 spec 或 tickets 转换为可观察、可暂停的小批次工作。它编排实现，不替代需求澄清、架构决定或用户对写入权限的授权。

## Orchestrate the work

1. 核对输入是否已确认：目标、验收条件、非目标、依赖和变更范围。关键产品、权限、数据或架构决定未定时，暂停并指向 `product-discovery`、`specification` 或用户确认，而不是猜测实现。
2. 按用户可观察的行为与现有 seam 切成小批次；每批都列出目标、受影响区域、验证命令和完成信号。避免按纯技术层或文件数量切分。
3. 在每个适用 seam 调用 `tdd` 建立或执行 red-green 反馈；出现根因不明、flaky 或跨模块失败时调用 `systematic-debugging`；完成可审查批次后可调用 `two-axis-code-review`。这些调用受各自触发条件和权限边界约束。
4. 每批结束报告实际变更、验证结果、未验证项和与计划的偏离。偏离范围、验收、架构、数据或权限时停止继续扩展，解释原因并请求决定。
5. 在最后一批后汇总已完成、未完成、风险与验证证据。不要把尚未运行的检查称作通过。

## Completion criterion

每个已执行批次都可追溯到确认输入，并有相称的验证或明确阻塞；计划偏离已被报告和处理，没有隐藏的范围扩张。

## Authorization boundary

显式调用本 skill 不自动授权 commit、push、创建/更新 issue tracker、发布、部署、安装依赖或任何外部写入。它也不把组织计划视为代码修改授权；每个执行动作仍须落在用户已授权范围内。
