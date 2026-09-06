# Task 4 Report — 对话 Prompt、工作流与控制器 UI 追溯

## Status

DONE_WITH_CONCERNS

未创建 commit；工作区不是 Git 仓库。

## Exact changed files

- `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`
- `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-4-report.md`

未修改原始 `prompts/05–09`、AGENTS、Task 2 文件、其他平台、zip 或其他文件。

## Requirements mapping

| Requirement | Implemented projection |
| --- | --- |
| M05 | 在优先澄清和规格规则中加入 UI 界面类型、viewport/输入方式、密度、频率及主/次/高风险操作；新增同名 `UI context and visual acceptance`，以可观察 acceptance 表达层级、图标和状态，不写统一像素、新图标库或实现风格。 |
| M06 | UI 事实读取覆盖同屏页面、tokens、组件、图标家族和密度；方向按结构/流程/层级区分，强强调须预登记；Variants 与 Accessibility/usability sections 记录静止态、图标、命中区和同屏重量证据。G4+sandbox、G0 用户测试边界未改。 |
| M07 | 只从 A05/A06 传递视觉约束与例外；用户可见 ticket 记录页面、viewport、状态、token/component/icon source 和同屏验证方法。缺失/冲突为 open question/blocker，不重新设计；G3 决定新增组件/图标 dependency、跨 design system 与公共 UI API 变化，G4 只精确授权本地写入且不能替代独立 dependency 或外部动作授权；PLAN、R3 和 tracker-preview 边界保留。 |
| M08 | 实现规则镜像权威 M08 的 token/component/icon reuse、上下文尺寸、次要控件、图标/可访问性、静止态与实际同屏复核；新增 `UI visual verification`，无渲染/工具不可用/未经授权时原样写 `Visual verification: not run`。G4、ALLOWED_FILES、DEPENDENCY_CHANGES 与 R3 边界保留。 |
| M09 | 启动方式与事实读取增加 `A06_PATH`；UI finding 归入 Spec/Standards 两轴并要求真实同屏证据、危险动作和 `Unverified scope`；Findings 表增加 `Evidence/trace`。固定 review range、只读审查、修复另需 G4，以及真实 provider/付费/red-team endpoint 的对象级未过期 R3 未改。 |
| 工作流 | 在通用产物规则后、M00–M13 工作流前加入五行表：M05 定义、M06 验证、M07 传递、M08 实现并同屏复核、M09 独立证据审查。 |
| 使用手册 | 质量检查新增「上下文决定 UI 层级」和「viewport/主题/状态真实同屏证据」两项；只允许 Codex CLI 使用项目已有或当前环境可用的本地视觉工具，不可用时记录原样标记，且不依赖 Desktop 面板。 |
| 控制器 | 全局纪律新增 UI 追溯不变量：适用 A05/A06 约束传到 M07/M08，M08/M09 记录真实同屏渲染证据；无证据只标未验证。未复制风格清单或扩大授权。 |

## Verification

- `PROMPTS_ASK_CHECK=PASS`：13 份对话 Prompt、104/104 公共标题、围栏、单问题协议和确认生成门均完整。
- `PROMPTS_ASK_COMMON_HEADINGS=104/104`：八个公共标题均恰好出现一次。
- `TASK4_SEMANTIC_CHECK=PASS` 和 `TASK4_DETAILED_SEMANTIC_CHECK=PASS`：M05–M09 的阶段特定语义存在；M08 含原样 `Visual verification: not run`，M09 含 `A06_PATH` 与 `Evidence/trace`。
- `SOURCE_DIALOGUE_STAGE_SEMANTICS_CHECK=PASS`：按阶段特定断言核验 Task 3 原始版与对话版的 UI 语义。该检查不将不同阶段的措辞强制为同一字面量。
- `TARGET_FENCE_CHECK=PASS`、`UTF8_TARGETS_CHECK=PASS`：八个目标文件 UTF-8 可读、Markdown fence 平衡。
- stale-token 检查未返回 `G5_APPROVAL`、`G6_APPROVAL`、`G5_PRODUCTION_READ_APPROVAL`、`TODO` 或 `FIXME`。
- `rg -n "Visual verification: not run|同屏|视觉约束"` 显示使用手册中的 CLI 限制与控制器中的追溯不变量。

## Review fix

Task 4 审查发现 0 Critical、1 Important：M07 仅写「进入 G3/G4」，未明确两者各自的授权职责。已将 M07 对话版收紧为：G3 决定新增组件/图标 dependency、跨 design system 与公共 UI API 变化；G4 只精确授权本地写入，不能替代独立 dependency 或外部动作授权。M07 的 PLAN-only、单问题、确认生成和 R3 边界未改。

上述均为静态文本验证。未运行浏览器、截图、视觉回归或真实 Agent 行为；没有把静态检查描述为视觉通过。

## Before content identity

以 `File.read(path, encoding: "UTF-8")` 的 logical-readable UTF-8 view 计算 SHA-256。八个目标的逻辑哈希均与简报的 before hashes 一致。

已记录的双视图例外仅影响写前 `prompts_ask/05` 和 `prompts_ask/09` 的 pathname view：

| File | Pathname view (bytes / SHA-256) | Logical-readable view (bytes / SHA-256) |
| --- | --- | --- |
| `prompts_ask/05-领域模型与产品规格.md` | 9016 / `e5d10bfc60629028856a7793ad98c8c6c8ed52407c4b319388a5ac1cc332706e` | 4920 / `e1ba23c03ba28f3044152cb51a64f5ae90a299e6c0f04240a269688708b661e5` |
| `prompts_ask/09-AI-Eval与质量安全.md` | 9579 / `4801855ad70cb2d81df69cd3c9ef5a247f0d097146c06b026718f928cbdd24b8` | 5483 / `6b746b201cd58fb9567201c037f32c0baa4a5c1c86dfec8996ac9bafeb4a143b` |

其余六个目标的 write-before logical hashes 与简报完全一致。按已确认授权，未在本任务中归一化该文件系统表现。

## After pathname and logical-readable evidence

Pathname view 使用 `/usr/bin/stat -f '%z'` 和 `/sbin/sha256sum`；logical-readable view 使用 Ruby `File.read(..., encoding: "UTF-8")`、`bytesize` 与 SHA-256。每个路径的两个 view 均显式记录，不推断其差异原因。

| File | Pathname bytes / SHA-256 | Logical-readable UTF-8 bytes / SHA-256 |
| --- | --- | --- |
| `prompts_ask/05-领域模型与产品规格.md` | 9754 / `a19db33f0040427cadab106e46c260521b943b5295b583a9cb898974141d378b` | 5658 / `7204fc389a3adefe9cfa5044d0bbe82c0c43de218e9be16d0cdb0a0aaade60d0` |
| `prompts_ask/06-原型与UX验证.md` | 9425 / `4fce2801551980c0373da3f02cee236fcd0fc92eaac11343f4b84db9726c29d5` | 5329 / `400a9e41b5398e27dace92ae07275e2b701af2beaaca7e99ede36047334afb7c` |
| `prompts_ask/07-架构设计与任务拆解.md` | 9414 / `47f70d0032782936190572b701c0a91190b54f94185ad17c391a010a3ea5bcd0` | 5318 / `1d52e5076b62947d76915d479387bdc4c8cca4061ba3d96384970c3c67eeae48` |
| `prompts_ask/08-全栈实现与TDD.md` | 10712 / `c91fca8a392cbfd96c5d654f77d75593adfea8474546cdfafd59c72374f258d4` | 6616 / `bd56bfe6a2753ddebbff2fb64fa97dcf7990ff886ccbe62d7485cd0fdbc5feeb` |
| `prompts_ask/09-AI-Eval与质量安全.md` | 10199 / `3fb1eb76c588a91d64de268ccf514a9d2b005922bbbf19f77f300ff20aeb5b59` | 6103 / `2932debd09320393ca2299798dbdd8be32aefbb0360a3346fca17984af6c51f9` |
| `04-模块化Skills工作流.md` | 31564 / `fe1d54965af66127d8f3a45f2bc381a54a3d05d4067d8b85d7f74a6294bbee0b` | 27468 / `fc51f093b5e9eae7e4e834e13e64cd537c0f3713bf6cab36c6c094c86f2e5ba0` |
| `06-Prompt-Chain使用手册.md` | 12930 / `c5fd0a5b1976d4f214d19e006be3a74bddcb51289bb9a9bd715a9d3ccc31cb4d` | 8834 / `b9d03c70893902253b281c0231d49dda6576005164ccd116367f2a94729b3547` |
| `prompts/99-端到端Prompt-Chain.md` | 10866 / `cd9b6d307ecd7eaca4e9e70da12e52818139ffdc871f34916846d0ade59a0a42` | 6770 / `2d4f44df5b26bc825b7137f9a1d81dfc7ea46ca2cb4e8f94608ce87c9031f38f` |

## Concerns and unverified scope

- 未执行真实 UI 渲染、浏览器、截图、视觉回归或真实 Agent 行为；`Visual verification: not run` 仍是适用时必须如实写出的运行时边界。
- Task 5 原计划中的一个过宽字面量 regex 会在 Task 3 权威原始 M05 上失败：该文件使用 `相对显著性` 和 `UI context and visual acceptance`，但不含 `同屏`、`视觉显著性` 或 `视觉约束`。该计划检查将由主任务改为阶段特定断言；本任务未修改原始 M05，且这不是 Task 4 失败。
