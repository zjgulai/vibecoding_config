# Task 3 Report — 原始 M05–M09 UI 视觉约束投影

## Status

DONE

未创建 commit；工作区不是 Git 仓库。

## Exact changed files

- `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-3-report.md`

未修改 `prompts_ask`、AGENTS、Task 2 文件、workflows/manual/controller、其他平台或 zip。

## Requirements mapping

| Requirement | Implemented projection |
| --- | --- |
| M05 | 新增条件化 `UI context and visual acceptance`：记录界面上下文与操作层级，并将相对显著性、图标可识别性、静止态层级和状态反馈作为可观察 acceptance；明确不写跨场景像素、新图标库或实现风格。 |
| M06 | UI 原型先读取同屏页面、tokens、组件、单一图标家族和密度；2–3 个方向按结构/流程/层级区分，强强调预先记录为实验变量；输出记录静止态、图标、命中区与同屏重量证据。 |
| M07 | 用户可见 ticket 从 A05/A06 传递视觉约束、例外、页面/viewport/状态、复用来源及同屏验证方法；缺失或冲突为 blocker/open question，不重新设计；G3/G4 与 dependency/外部授权边界保留。 |
| M08 | 前端执行规则覆盖 token/component/icon source 复用、上下文化尺寸/间距、次要控件、图标与 icon-only 可访问性、静止态语义、真实同屏复验；明确此检查不授权安装或调用未经授权工具，只可使用适用授权范围内项目已有或当前环境可用的工具；A08 新增 `UI visual verification`，未渲染、工具不可用或未经授权时原样记录 `Visual verification: not run`。 |
| M09 | 在输入变量与 Prompt 输入中于 `A05_PATH` 后加入 `A06_PATH`；Web UI 审查增加任务显著性、次要控件、hover/tooltip、图标、危险动作和同屏证据；finding 保持 Spec/Standards 两轴，增加 `Evidence/trace`，无视觉证据时写入 `Unverified scope`。 |

## Review fix

Task 3 独立审查发现 0 Critical、1 Important：M08 的真实渲染检查未明确工具授权边界。已在 M08 执行规则补充：不得以该检查安装或调用未经授权的浏览器、截图、网络、外部或其他工具；仅可在适用授权范围内使用项目已有或当前环境可用工具；工具不可用或未经授权时原样记录 `Visual verification: not run`。

## Verification

- `PROMPT_SOURCE_CHECK=PASS`：五个目标文件均存在 Mxx/Axx/完成标准，UTF-8 可读，Markdown fence 平衡。
- `TASK3_SEMANTIC_CHECK=PASS`：五份文件分别含其生命周期职责所需的 UI 语义；M08 含原样 `Visual verification: not run`；M09 同时含 `A05_PATH`、`A06_PATH`、Spec/Standards 与 `Evidence/trace`。
- `TASK3_PRESERVATION_CHECK=PASS`：既有 Gate、MODE、停止条件、G3/G4 与授权相关关键词仍存在。此为静态文本保留检查，不是对运行时行为的证明。
- `TASK3_TOOL_AUTHORIZATION_CHECK=PASS`：M08 明确实际渲染检查不构成未经授权工具的安装或调用授权，仅允许适用授权范围内项目已有或当前环境可用工具；不可用或未经授权时要求原样记录 `Visual verification: not run`。

未运行浏览器、截图或视觉回归：本任务只修改 Prompt 源文件，因此没有真实 UI 渲染证据。

## Before hashes

| File | SHA-256 |
| --- | --- |
| `prompts/05-领域模型与产品规格.md` | `3c33c7d0bcbe3de39a039a640349645d6b1ee8b104be567d60e014b5cbc08c2f` |
| `prompts/06-原型与UX验证.md` | `453cfce835956cd1c570c1fcf303801f87448ed22168ac59ed86625d13c5bef3` |
| `prompts/07-架构设计与任务拆解.md` | `ff7b7a95226d84f01d3139cdc8805b972e4dac3e564f1f7332da1babeccf1bfd` |
| `prompts/08-全栈实现与TDD.md` | `a0cd9e5c7cb546b59275b0673262085b8b3e85eed38faead5ce177235be1e206` |
| `prompts/09-AI-Eval与质量安全.md` | `889d4407d242a4881ddb9083cb7a0573c7bad42a85a88bb0a062bbe30ab49c4e` |

## After hashes and sizes

`shasum -a 256` computes the content hash. On this workspace, `stat -f '%z'` reports a native size that differs from the readable UTF-8 stream size returned by `File.read(..., encoding: "UTF-8").bytesize`; both are recorded explicitly. The logical-readable SHA-256 is computed from that UTF-8 stream and matches the content SHA-256 for every file.

| File | SHA-256 / logical-readable SHA-256 | Native bytes (`stat`) | Logical-readable UTF-8 bytes |
| --- | --- | ---: | ---: |
| `prompts/05-领域模型与产品规格.md` | `813932012a7c74d455cd7931a2c380e9320edaa45a7c89be1052e831e474f505` | 8247 | 4151 |
| `prompts/06-原型与UX验证.md` | `492560544495d04932ccbc73e3d22850f55e29b70fe60f052f6496473f914d73` | 8491 | 4395 |
| `prompts/07-架构设计与任务拆解.md` | `7a55bc6f18e0a43464882b6b9f659cfd9cd78a4cd60dd540b412b7cab4a98bf4` | 8350 | 4254 |
| `prompts/08-全栈实现与TDD.md` | `dc278f16f93a96bdc3ce3d29dde4934ce0b2045513fc10afdc0d79ca458f4785` | 9292 | 5196 |
| `prompts/09-AI-Eval与质量安全.md` | `4a15a3688ad96079ce0d64ba61e058d38f6a576a370bcffd0354d0470f224151` | 8974 | 4878 |

## Unverified scope and concerns

- 未执行真实页面渲染、浏览器、截图或视觉回归；没有把静态检查描述为视觉通过。
- 原生大小与逻辑可读大小的差异已按路径记录；内容 SHA-256 与 logical-readable SHA-256 一致。未转换文件编码或修改无关内容。
