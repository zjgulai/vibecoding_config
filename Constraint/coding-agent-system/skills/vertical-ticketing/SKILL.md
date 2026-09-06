---
name: "vertical-ticketing"
description: "把已确认的 spec 或计划拆成可独立验证的垂直 tickets 与显式依赖图；仅在用户明确要求拆票时使用。"
metadata:
  invocation: "explicit-only"
  source: "Method adapted from mattpocock/skills to-tickets (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Vertical Ticketing

把工作拆成能独立交付价值、保持可验证状态的 tracer-bullet slices，而不是按技术层横切。

## Choose the path

- **Fast path:** 单一行为且可在一个上下文完成时，产出一个 ticket，不制造依赖图。
- **Full path:** 多行为、跨层或可并行工作时，产出垂直 slices 与无环 blocking edges。

## Workflow

1. 完整读取用户指定的 spec、计划或对话结论；必要时检查相关代码和既有术语。缺少关键产品决定时返回规格阶段，不用切票掩盖歧义。
2. 每个 slice 贯穿实现该行为所需的层（例如数据、服务、界面、验证），并满足：可独立演示/验证、能在一个 fresh context 中完成、完成后仓库保持可用。
3. 只添加真正阻止开始的 `Blocked by` 边；偏好较小 frontier，而不是人为线性化所有工作。检查依赖图无环。
4. 对无法保持 green 的 wide mechanical refactor 使用 expand–migrate–contract：先兼容扩展，分批迁移，确认无残留后再收缩。不要伪装成独立业务 slices。
5. 每个 ticket 包含：Title、What it delivers、Blocked by、Acceptance criteria、Out of scope/notes（仅在必要时）。验收条件描述可观察行为，不写逐文件施工清单。
6. 先展示编号草稿，请用户确认粒度与依赖。用户批准后，才按其要求写本地文件；写真实 tracker 需要针对该次写入的明确授权。

## Completion criterion

每个 ticket 都能单独验收，依赖边真实且无环；所有规格要求恰好被覆盖，没有遗漏、重复 ownership 或暗含的“大爆炸”集成步骤。

## Authorization boundary

拆票不授权创建/修改真实 issue、安装依赖、commit、push、发布或执行危险/外部操作。默认只输出草稿。
