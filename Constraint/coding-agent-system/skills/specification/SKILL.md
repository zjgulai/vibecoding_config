---
name: "specification"
description: "把已经讨论清楚的需求与仓库事实整理成可实现、可验收的规格；仅在用户明确要求产出或更新 spec 时使用，不代替需求访谈。"
metadata:
  invocation: "explicit-only"
  source: "Method adapted from mattpocock/skills to-spec (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Specification

把已解决的上下文固化为实现合同。优先综合现有信息；只有缺口会实质改变规格时才停下来询问。

## Choose the path

- **Fast path:** 小而明确的变更可用一页以内的轻量规格：问题、期望行为、验收条件、非目标。
- **Full path:** 跨模块、用户可见、数据/权限相关或存在多方取舍时，使用完整结构并核对仓库事实。

## Workflow

1. 读取用户指定材料和与改动直接相关的代码、规则、术语与测试先例。记录事实来源；不要写入会快速过时的猜测性文件路径或代码片段。
2. 将内容分为已确认决策、仓库事实、建议和未决项。未决项不能伪装成实现要求。
3. 选择最少且最高层的可观察测试 seam。沿用已有 public boundary；新增 seam 属于设计决策，需要说明理由。
4. 起草与复杂度相称的规格：
   - Problem / intended outcome
   - Actors and user-visible flows
   - Functional requirements and acceptance scenarios
   - Implementation decisions and affected interfaces
   - Data, permission, compatibility and failure behavior（适用时）
   - Testing decisions and prior art
   - Out of scope
   - Open questions / assumptions
5. 做双向检查：每个需求至少有一个验收方式；每个验收项都能追溯到需求或明确风险。
6. 输出草稿供用户审阅。只有用户要求写入本地文件时才写文件；只有再次明确授权后才写入真实 issue tracker。

## Completion criterion

另一个 agent 无需猜测产品行为即可实现；所有关键边界可验收，事实、决定和未决项彼此可区分。

## Authorization boundary

生成规格不授权创建/修改 issue、安装依赖、commit、push、发布或执行危险/外部操作。保留草稿状态，直到用户明确批准相应写入。
