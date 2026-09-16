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
2. 在改变行为前对齐当前行为、目标行为与 authority。发生冲突时按「用户当前明确要求 → 已批准规格 → 仍有效的测试 → 当前实现」判断；不得把失败测试自动视为错误规格，也不得修改测试迁就实现。冲突会改变需求、兼容或风险时停止并报告。
3. 按用户可观察的行为与现有 seam 切成小批次；每批都列出目标、受影响区域、验证命令和完成信号。避免按纯技术层或文件数量切分。
4. 在每个适用 seam 调用 `tdd` 建立或执行 red-green 反馈；出现根因不明、flaky 或跨模块失败时调用 `systematic-debugging`；完成可审查批次后可调用 `two-axis-code-review`。这些调用受各自触发条件和权限边界约束。
5. 每批先运行能捕获目标行为的最小 fixture/quick check，再按影响半径升级到受影响模块、目标原生 integration、相关矩阵和发布前门禁。共享契约改变时，搜索同根因的调用点、复制实现与其他 adapter；记录命中与排除依据，不用字符串命中代替语义判断。
6. 修改规范源而非生成物；使用项目的权威生成流程。普通验证不得隐式改写 lockfile、生成物或 release 记录；若工具造成非目标变更，停止并恢复到进入该步骤前的可核验状态。
7. 每批结束报告实际变更、验证结果、未验证项和与计划的偏离。偏离范围、验收、架构、数据或权限时停止继续扩展，解释原因并请求决定。
8. 在最后一批后汇总已完成、未完成、风险与验证证据。不要把尚未运行的检查称作通过。

## Bounded asynchronous batch

仅当用户明确要求连续或后台批次，且当前任务已有完整 `Autonomy Envelope` 时，才可以使用 `bounded_async`。它只适用于 R0/R1 的本地工作，不创建后台会话、不默认派生 subagent，也不改变 R2/R3 的审证或对象级授权边界。

1. 先核对目标/DoD、风险和人类责任、write/tool/data scope、最窄反馈、停止条件、enforcement evidence 与 handoff 是否和当前任务一致。
2. 只在一致时运行「最窄反馈 → 最小修改 → 重跑同一检查 → 保存原始证据」循环；每批仍遵守既有文件范围和依赖限制。
3. 遇到范围或权限变化、新依赖、架构/API/schema/auth/迁移、敏感数据、外部动作、连续不收敛或证据变弱时停止。交接实际范围、命令/结果、停止触发、人工介入和未验证项；不得自行降级风险或扩大范围。

## Completion criterion

每个已执行批次都可追溯到确认输入，并有相称的验证或明确阻塞；计划偏离已被报告和处理，没有隐藏的范围扩张。

## Authorization boundary

显式调用本 skill 不自动授权 commit、push、创建/更新 issue tracker、发布、部署、安装依赖或任何外部写入。它也不把组织计划视为代码修改授权；每个执行动作仍须落在用户已授权范围内。
