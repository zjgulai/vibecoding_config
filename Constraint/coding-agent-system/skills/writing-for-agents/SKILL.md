---
name: "writing-for-agents"
description: "创建、精简或审计 coding agent 的 instructions、rules 与 skills；适用于判断规则是否值得进入上下文、应放在哪一层，以及如何消除重复或冲突。"
metadata:
  source: "Method adapted from mattpocock/skills writing-for-agents (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Writing for Agents

让文档稳定改变 agent 的决策，而不是堆积模型本来就会做的建议。

## Choose the mode

- **Create:** 用户要求新建、重写或精简 agent instruction、rule、pointer 或 skill。
- **Audit:** 用户要求审计现有材料的价值、层级、证据、重复或冲突。审计不隐含改写授权。

## Admission gate

每条候选规则都回答三个问题；任一答案不明确时，不直接纳入常驻上下文。

1. **Behavior:** 它会在什么真实场景改变 agent 的选择、停止条件或完成判定？如果只是复述通用能力或口号，删除。
2. **Layer:** 它的最窄有效范围和唯一权威位置在哪里？如果当前文件不是正确层级，移动而非复制。
3. **Evidence:** 权威来源、适用条件和失效信号是否足以支撑这项约束？会实质限制工作的规则若证据不足，标为 `needs-evidence`。

## Destination map

- 跨项目稳定、几乎每次任务都需要的行为放用户级 core。
- 项目长期不变量、权威入口、联动关系与完成定义放项目画像或项目级指针。
- 只对特定目录、技术栈或风险生效的规则放就近规则或条件 module。
- 有独立触发边界、可复用的多步判断流程放 skill；单条提醒不值得新建 skill。
- 必须确定执行的格式、权限或联动限制放 validator、hook、script、permissions 或 CI，不用自然语言假装自动化。
- 面向人的背景知识留在普通文档，由短 pointer 按需引导；不要全文复制进常驻指令。

只有同时满足以下条件才新建 skill：存在可区分的目标请求与近邻非目标请求；流程包含模型本来不会稳定完成的决策边界；该流程会在多个任务中复用。否则优先短规则、项目画像、确定性控制或普通文档。

## Create mode

1. 定义目标行为、目标请求与一个容易误触发的近邻请求。
2. 对每条拟写规则执行 Admission gate，并选择 Destination map 中最窄的层级。
3. 打磨 context pointer：先说明能力，再说明何时加载；不要用穷举同义词扩大触发范围。
4. 主文件只保留每条路径都需要的内容；分支细节按触发时机放 reference。一个含义只保留一个 source of truth。
5. 保留完整判据、证据档位、固定术语与真正的顺序依赖；精简不能删掉会改变判定的边界。多平台变体使用“通用规则 + 已验证的 platform delta”，不因适配而缩水通用判据，也不臆造平台路径或能力。
6. 写出可观察的完成条件，并检查是否夹带安装、写配置、外部调用或其他未获授权的动作。
7. 用两个行为场景检查结果：目标场景应加载正确材料并得到预期决策；近邻场景应不加载或明确退出。结构校验通过不等于行为已验证。

## Audit mode

先确定审计范围和当前权威链，再逐条运行 Admission gate。每条规则只能给出一个主判定：

- `retain`：能改变行为，层级正确，证据足够，且无未解决冲突。
- `rewrite`：意图有效但表述含糊、过宽、不可检查或夹带隐藏授权；保留在当前层并重写。
- `move`：内容有效但层级错误；指出唯一目标层，不在两处并存。
- `delete`：重复、陈旧、无行为影响，或已由更权威机制覆盖。
- `needs-evidence`：可能值得保留，但来源、适用范围或失效条件不足以支持约束。

审计结果至少包含：规则定位、主判定、行为影响、证据、当前与建议层级、冲突/重复对象、建议动作。不要用篇幅、语气或个人偏好替代行为证据。

## Conflict handling

先遵循目标平台明示的 instruction precedence；同一权威层内再比较适用范围、项目 source of truth、证据与时效。更窄规则只覆盖其真实适用范围。无法据此消解的实质冲突必须显式列出并请求决定，不得平均矛盾、静默选择或复制两套说法。

## Completion criterion

目标 agent 能在目标场景触达唯一、足量的材料并识别 done；近邻场景不会被宽泛 pointer 误触发。Audit 的每条候选都有唯一判定和可追溯理由，未把结构检查冒充行为效果。

## Authorization boundary

编写或审计 agent 文档不授权安装、发布、修改真实用户配置、创建 issue、安装依赖、commit、push 或执行危险/外部操作；这些动作需要当前任务的明确授权。
