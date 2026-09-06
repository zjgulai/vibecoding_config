# Task 3: 将 UI 约束投影到原始 M05–M09 Prompt

## Context

本任务执行已批准实施计划的第三阶段。Task 1 的 `frontend-visual-quality.md` 是完整规则的单一事实源；本任务只把 UI 约束按生命周期职责投影到 M05 定义、M06 验证、M07 传递、M08 实现和 M09 审查。不得在 Prompt 中复制整套风格清单或扩大授权。当前目录不是 Git 仓库，不 commit；所有人工编辑必须使用 `apply_patch`。

开始前完整阅读：

- `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-02-ui-visual-restraint-integration-design.md`
- `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ui-visual-restraint-integration.md` 的 Global Constraints 与 Task 3
- `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`
- 本任务列出的五个目标 Prompt

## Global constraints

- 只修改原始 `prompts/05–09` 五份文件及本任务报告；不得修改 `prompts_ask`、AGENTS、SOP、评测、追踪、Claude、DSH、Cursor 或 zip。
- M05–M09 各司其职：M05 定义可观察规格，M06 验证不确定性，M07 传递已确认约束而不重新设计，M08 实现并作真实同屏自检，M09 以证据审查。
- 任务型界面默认克制，但显著性按任务的重要性、后果和紧迫性决定；不得牺牲可发现性、可读性、可访问性、命中区或风险表达。
- `hover`、`tooltip`、颜色与动效不是核心语义的唯一通道；单一图标家族不构成安装新 dependency 的授权。
- 不削弱现有 Axx、G0/G3/G4、R3、MODE、停止条件、写入边界、真实 provider/付费/生产/外部写入授权或公共输出结构。
- 无真实渲染证据时只记录未验证，不把静态阅读或代码检查冒充视觉通过。

## Files

- Modify: `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- Report: `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-3-report.md`

不得修改其他文件。

## Before hashes

- `prompts/05-领域模型与产品规格.md`: `3c33c7d0bcbe3de39a039a640349645d6b1ee8b104be567d60e014b5cbc08c2f`
- `prompts/06-原型与UX验证.md`: `453cfce835956cd1c570c1fcf303801f87448ed22168ac59ed86625d13c5bef3`
- `prompts/07-架构设计与任务拆解.md`: `ff7b7a95226d84f01d3139cdc8805b972e4dac3e564f1f7332da1babeccf1bfd`
- `prompts/08-全栈实现与TDD.md`: `a0cd9e5c7cb546b59275b0673262085b8b3e85eed38faead5ce177235be1e206`
- `prompts/09-AI-Eval与质量安全.md`: `889d4407d242a4881ddb9083cb7a0573c7bad42a85a88bb0a062bbe30ab49c4e`

## Requirements

1. M05：在方法和输出结构中加入条件化 UI 规格契约。若规格包含 UI，记录界面类型、目标 viewport/输入方式、信息密度、使用频率、主操作、次要操作和高风险操作；把相对显著性、图标可识别性、静止态层级和状态反馈写成可观察 acceptance。禁止跨场景统一像素规格、指定新图标库或把实现风格伪装成需求。建议在现有 `## User journeys` 后、`## Functional requirements` 前加入紧凑的 `## UI context and visual acceptance`，但不拆散公共输出契约。
2. M06：在既有步骤中先读取同屏页面、design tokens、组件、单一图标家族和内容密度；2–3 个方向主要在结构、流程或层级上不同，不得只是装饰换皮；强强调若作为实验变量必须预先记录。把证据落在现有 `## Variants or experiment design` 与 `## Accessibility/usability checks`，覆盖静止态可理解性、图标理解、命中区和同屏相对视觉重量。
3. M07：用户可见 ticket 必须从 A05/A06 追溯视觉约束、已批准例外、目标页面、viewport、状态、复用的 token/component/icon source 和同屏验证方法。M07 不重新做视觉决策；缺失或矛盾是 blocker/open question。新增组件或图标 dependency、跨 design system、公共 UI API 变化仍分别受 G3 决策与 G4 精确写入授权约束；不得让 G4 代替依赖或外部动作授权。
4. M08：在现有前端执行规则中加入紧凑但完整的阶段检查：
   - 复用 design tokens、组件和单一图标家族。
   - 按界面类型、平台、输入方式、密度、频率和任务层级决定尺寸/间距，不靠单纯放大建立层级。
   - 真正次要的入口、设置、开关和工具按钮不压过主任务；安全、隐私、无障碍和主任务例外按规格处理。
   - 标准动作使用熟悉图标；歧义、低频、高后果动作有可见文字；icon-only 控件具备 accessible name、可见 focus、明确状态和足够命中区。
   - 静止态不依赖 hover、tooltip、颜色或动效传达核心语义；无任务/平台/品牌依据时避免过度装饰。
   - 实际渲染后与同屏元素比较相对尺度、视觉重量和密度；调整后复验可读性、focus、命中区和状态。
   在输出中增加 `## UI visual verification`，记录页面、viewport、主题/状态、同屏基准、方法和结果；未查看实际渲染时必须原样写 `Visual verification: not run`。不要把这一要求解释为安装或调用未授权工具。
5. M09：Web UI 审查加入显著性是否匹配当前任务、次要控件是否压过主任务、核心语义是否依赖 hover/tooltip、图标是否熟悉且语义正确、危险动作是否有清晰标签和适当保护、同屏尺度/重量/密度是否有真实证据。Finding 只能归入既有 Spec 或 Standards 两轴：追溯到 A05/A06 的已确认需求归 Spec，适用 AGENTS/module/项目设计系统或可观察任务受阻归 Standards；不得增加「个人审美」第三轴。无浏览器、截图或视觉回归证据时写入 `Unverified scope`。
6. 为兑现 M09 对 A06 的直接追溯，在 M09 的输入变量和 Prompt 输入列表中加入 `{{A06_PATH}}`，位于 `A05_PATH` 后；同步为 Findings 表增加明确的 evidence/trace 字段。不得借此改变 review range、只读审查或 G4 修复门。
7. 保留以下既有行为：
   - M05：A04 approved/draft 边界、需求与验收双向追溯、G3 架构 seam、外部 tracker/发布授权。
   - M06：每次原型只回答一个问题；APPLY 必须同时匹配有效 G4 和精确 sandbox/write scope；无真实客户数据/生产路由/生产数据库/自动 branch/Issue；用户测试受 G0。
   - M07：始终 PLAN；G3 未通过不固化高影响方案；G4 request 精确；外部 tracker 只 preview；tickets 保持垂直切片和无环 DAG。
   - M08：仅当前 slice 的 G4 可写；未知重叠改动停止；dependency 默认 DENY；TDD/debug/三次失败停止；不读取 secrets 或未经授权 install/lockfile/commit/push/Issue/PR/deploy。
   - M09：先只读、修复另需 G4；review range 不固定则停止；仅 Spec/Standards 两轴；安全 finding 有 exploitability 证据；页面内容视为不可信数据；真实 provider、red-team、付费调用另行授权；不得改 spec 或跳测试制造通过。
8. 更新 frontmatter 日期/修订号时延续现有格式；不要顺手修复 M08 既有 `A05_PATH` 输入轻微不一致或任何非本任务问题。

## Verification

从工作区根运行：

```bash
ruby -e 'files=Dir.glob("全栈开发Prompt Chain/prompts/{05,06,07,08,09}-*.md").sort; abort("expected 5 files") unless files.size==5; files.each{|f| t=File.read(f, encoding:"UTF-8"); abort("unbalanced fence: #{f}") unless t.scan(/^```/).size.even?; base=File.basename(f)[0,2]; abort("missing M#{base}: #{f}") unless t.include?("M#{base}"); abort("missing A#{base}: #{f}") unless t.include?("A#{base}"); abort("missing completion: #{f}") unless t.include?("完成标准")}; puts "PROMPT_SOURCE_CHECK=PASS"'
```

另做只读静态检查并记录：

- 五份文件均含与其阶段相符的 UI 语义，而不是五份相同清单。
- M09 同时含 `A05_PATH`、`A06_PATH`、Spec/Standards 与 evidence/trace；M08 含原样 `Visual verification: not run`。
- M05–M09 的既有 Gate、MODE、停止条件、外部/生产/dependency 授权关键词仍存在；不得把文本存在性描述成真实行为验证。
- 五个目标 UTF-8 可读、Markdown fence 平衡；记录 after SHA-256 与 native/readable byte size。

完整报告写入指定 report 文件，列出 exact changed files、requirements mapping、测试、after hashes、未验证项与 concerns。最终回复只给 DONE 状态、无 commit、测试摘要、concerns 和报告路径。
