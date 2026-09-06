# Codex UI 视觉克制经验分层融合 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将用户确认的 UI 视觉克制经验分层写入 Codex 用户/项目指引、前端视觉条件模块、M05–M09 Prompt Chain、工作流与评测，并保持可追溯、可验证且不影响其他平台。

**Architecture:** Codex 用户级 `AGENTS.md` 只保存条件触发与最小默认偏置，Codex 项目级 `AGENTS.md` 只路由详细规则，`frontend-visual-quality.md` 是完整操作清单的单一事实源。M05–M09 只投影各生命周期阶段需要的约束与证据；原始 Prompt 先更新，对话版再做语义镜像，评测与追踪文件负责证明规则可达且有失败条件。

**Tech Stack:** Markdown、JSON、Python 3 标准库、现有 `tools/agent_system.py`、Ruby 静态检查；不新增依赖。

## Global Constraints

- 只面向 Codex CLI；不得修改 Claude Code、DSH Desktop / DeepSeek Harness 或 Cursor 配置。
- 不修改真实 `~/.codex/AGENTS.md`；本次只更新仓库内可配置模板。
- `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md` 是完整 UI 操作规则的单一事实源；其他文件只保留触发、路由、阶段投影或验收。
- 视觉显著性与任务的重要性、后果和紧迫性匹配；任务型产品界面默认克制，但不得牺牲可发现性、可读性、可访问性、交互命中区或风险表达。
- `hover`、`tooltip`、颜色和动效只能补充，不能成为核心语义的唯一通道。
- 不隐式新增组件库、图标库、字体或其他 dependency。
- Prompt Chain 的原始版与 `prompts_ask` 对话版必须同步；不得削弱既有 Gate、R3 授权、停止条件、Axx 契约或单问题协议。
- 当前目录不是 Git 仓库；不执行 commit，以变更前后哈希、现有 validator、单元测试和独立审查替代 Git 证据。
- 所有人工文件编辑使用 `apply_patch`；不得手改生成器受管块或自动生成快照。

---

### Task 1: 建立 Codex UI 规则入口与单一事实源

**Files:**

- Modify: `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`，在 `## Codex 适配说明` 之后增加 Codex 用户级条件偏置。
- Modify: `Constraint/coding-agent-system/templates/project/codex/AGENTS.md`，在 `## Codex 项目适配` 之后增加项目 UI 规则路由。
- Modify: `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`，扩充发现、规则和视觉验证闭环。

**Interfaces:**

- Consumes: 已批准设计规格中的核心不变量，以及现有 `frontend-visual-quality` 触发范围和验证结构。
- Produces: 用户级最小基线、项目级可达路由和完整视觉规则，供 Task 2 的评测/SOP 与 Tasks 3–4 的 Prompt 投影引用。

- [ ] **Step 1: 保存非目标平台与共享 core 的变更前哈希**

Run from `/Users/lute/Project/vibecoding_config`:

```bash
find \
  Constraint/coding-agent-system/templates/shared \
  Constraint/coding-agent-system/templates/user/claude \
  Constraint/coding-agent-system/templates/user/deepseek-harness \
  Constraint/coding-agent-system/templates/project/.claude \
  Constraint/coding-agent-system/templates/project/deepseek-harness \
  Constraint/cursor_rules \
  -type f -print0 | sort -z | xargs -0 shasum -a 256
shasum -a 256 \
  Constraint/coding-agent-system/templates/project/AGENTS.md \
  Constraint/Codex_AGENTS.md \
  Constraint/coding-agent-system/templates.zip \
  '全栈开发Prompt Chain.zip'
```

Expected: 每个明确不修改文件各有一行 SHA-256；保存完整输出到任务报告，最终 Task 5 使用相同命令逐行比对。

- [x] **Step 2: 在 Codex 用户模板加入紧凑条件偏置**

使用 `apply_patch` 在共享块之外新增 `## 用户可见界面的默认偏置`，必须包含以下完整语义：

- 仅当任务改变页面、组件、样式、交互、响应式布局或可访问性时生效。
- 项目存在可达的 `.agents/rules/frontend-visual-quality.md` 时先读取；不存在时不得声称已加载。
- 任务型产品界面默认克制，显著性与任务的重要性、后果和紧迫性匹配。
- 优先复用项目既有设计语言；实现后检查真实渲染和同屏关系；工具不可用时标记视觉未验证。
- 该短章节不复制完整图标、状态和验收清单。

- [x] **Step 3: 在 Codex 项目模板加入条件路由**

使用 `apply_patch` 新增一条明确路由：UI 任务且 `.agents/rules/frontend-visual-quality.md` 存在时必须读取；不存在时沿用用户级基线和项目既有规范，报告模块缺口，不能臆造文件或规则。不得修改 `templates/project/AGENTS.md` 的 `BEGIN/END MANAGED MODULE ROUTES` 块。

- [x] **Step 4: 扩充前端视觉条件模块的事实发现**

在 `## 先发现项目事实` 中加入：

- 判断任务型产品、营销/品牌、专家高密度工具或安全关键流程。
- 识别主操作、次要操作、高风险操作、目标 viewport、输入方式、信息密度和使用频率。
- 记录可比较的同屏主操作、正文、表单和相邻控件。
- 图标来源优先级为项目现有图标家族，其次是项目已可用的系统或行业通用符号；不得为单页新增依赖。

- [x] **Step 5: 写入完整的视觉显著性、尺寸与图标规则**

在 `## 最小质量门槛` 前新增 `## 视觉显著性、尺寸与图标`，逐条写明：

1. 任务型界面默认克制；营销、品牌、关键警告和不可逆动作可按职责使用更强表达，但必须有规格、任务或风险依据。
2. 尺寸和间距先复用 design tokens、组件规格和平台惯例，再结合 viewport、输入方式、密度、频率和层级选择；不能靠单纯放大建立层级。
3. 当前主任务中的辅助入口、设置、开关和工具按钮默认次级但可发现；其本身为主任务或涉及安全、隐私、无障碍和关键状态时按实际优先级处理。
4. 常见动作复用成熟图标隐喻和单一图标家族；歧义、低频或高后果动作配可见文字。
5. Icon-only 控件具备正确语义、accessible name、可见 focus、明确状态和足够命中区；装饰图标不进入 accessibility tree。
6. 静止态通过位置、分组、排版、间距、对比、分隔和状态建立层级；颜色、hover、tooltip 和动效不能成为唯一线索。
7. 没有任务、平台或品牌依据时，避免夸张尺寸、重色块、过度圆角、厚边框、强阴影和装饰性渐变。

- [x] **Step 6: 扩充实际视觉检查与回归条件**

在 `## 验证命令与视觉检查` 中要求记录页面、viewport、主题、状态、比较基准和结果，并检查：

- 同屏相对尺度、填充、对比、字重、边框、阴影、elevation 和信息密度。
- 不触发 hover、tooltip 或动画时，主任务与关键状态仍可理解。
- 次要控件未无依据地压过主操作；危险动作有清晰标签、区分和适当的 undo/review/confirm。
- 视觉调整没有降低文字可读性、命中区、focus 或状态语义。
- 没有启动实际页面并检查渲染时，不声明视觉质量通过。

- [x] **Step 7: 运行模板和系统基线校验**

Run:

```bash
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py validate .
```

Expected: `render-templates` 只列出既有 shared snapshot 目标；`validate .` 输出 `VALID`。不得运行 `render-templates --apply`，因为 shared core 未变化。

- [x] **Step 8: 独立审查 Task 1**

审查者逐项确认：完整规则只有模块一处；用户和项目 AGENTS 只保存偏置/路由；没有传播到其他平台；没有把「克制」写成缩小命中区或覆盖安全/品牌职责。Critical 或 Important finding 未关闭时不得开始 Task 2。

> **2026-09-02 审计例外：** Step 1 的完整编辑前基线漏采 4 个非目标文件，且不存在独立时间戳记录，故该步骤保持未勾选并标记为不可追溯。当前三个目标文件的身份、31 个保护文件的当前哈希、模板 dry-run 与系统校验均已复验；独立审查结论为 `Approved with documented exception`。该例外不等同于补齐编辑前证据。

---

### Task 2: 建立 UI 规则的 SOP、行为评测与来源追踪

**Files:**

- Modify: `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md`
- Modify: `Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
- Modify: `Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
- Modify: `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
- Modify: `Constraint/coding-agent-system/docs/research/local-material-audit.md`
- Modify: `Constraint/coding-agent-system/sources/rule-traceability.json`

**Interfaces:**

- Consumes: Task 1 的核心不变量、完整规则和现有 `EVAL-05` contract。
- Produces: 可失败的行为 oracle、生命周期执行步骤及 `LOC-030 → Tip decision → aggregated rule → artifacts → EVAL-05` 追踪链。

- [x] **Step 1: 扩充 EVAL-05 的失败 oracle**

使用 `apply_patch` 在验收重点中加入四项：

- 次要设置、开关或工具按钮无依据地比当前主操作更显著时失败。
- 标准动作使用陌生图标且核心含义只靠 tooltip 时失败。
- 视觉收敛同时损害文字、focus、对比度或交互命中区时失败。
- 没有目标 viewport、关键状态和同屏比较证据却声明视觉完成时失败。

保留 `contract-only` 与未交付真实 browser fixture 的现状，不将新规则写成已通过行为基准。

- [x] **Step 2: 更新项目生命周期前端视觉专项**

在阶段 9 中增加：

- 前置确认界面类型、主次/风险操作、输入方式和同屏基准。
- 静止态层级、通用图标语义、icon-only accessible name 与命中区检查。
- 实际渲染后比较相对尺度、视觉重量和密度；调整后复验可读性、focus 和命中区。
- CLI 没有可用浏览器、截图或视觉回归工具时，记录未验证范围，不要求 Codex Desktop 右侧面板。

- [x] **Step 3: 将当前用户经验登记为 LOC-030**

在 `local-tip-ledger.md` 新增一行：

- 来源：用户于 2026-09-02 明确提供并确认采用的 UI 设计经验。
- 采用：分层改写；Codex 用户模板保存最小偏置，完整操作规则进入前端视觉模块，生命周期 Prompt 和 EVAL-05 承载阶段行为与证据。
- 条件化：营销/品牌、安全、无障碍和主任务例外；tooltip 非核心语义；视觉尺寸与命中区分离。
- 排除：原文跨场景绝对禁止和「只有用户要求才可强调」。

- [x] **Step 4: 在 Tip 决策矩阵增加原子决策**

新增 `TIP-077`，原子经验为「任务型界面默认克制，视觉显著性按任务重要性、后果和紧迫性决定；复用熟悉图标并以真实同屏证据验收」。决策写为「条件采用并改写」，落点写明 Codex 用户偏置、frontend module、M05–M09 和 EVAL-05。把来源覆盖范围从 `LOC-001` 至 `LOC-029` 更新为 `LOC-001` 至 `LOC-030`。

- [x] **Step 5: 保留原始 29 文件审计的历史边界**

在 `local-material-audit.md` 增加「后续来源」说明：`LOC-030` 是 2026-09-02 用户会话新增经验，不属于该文档原始 29 个本地内容文件的逐文件审计；不得把原始计数改写为 30 个文件。

- [x] **Step 6: 更新机器可解析规则追踪**

使用 `apply_patch` 修改 `rule-traceability.json`：

- `verified_on` 更新为 `2026-09-02`。
- `scope.local_source_count` 从 `29` 更新为 `30`。
- 新增 `RUL-022`，原则对应 TIP-077，`sources` 为 `["LOC-030"]`。
- `destination.paths` 明确列出 `templates/user/codex/AGENTS.md`、`templates/project/codex/AGENTS.md`、`templates/modules/frontend-visual-quality.md`、`evals/tasks/05-frontend-visual-quality.md`，以及以 `../../全栈开发Prompt Chain/` 为基准的 M05–M09 普通版和对话版路径。
- `artifacts` 使用同一组实际文件路径；这些文件在本计划完成时均使用状态 `implemented`，不得使用未定义或笼统的中间状态。
- `eval_cases` 为 `["EVAL-05"]`，状态仍明确 `eval-contract-only; real-agent-not-run`。
- `expiry_signal` 覆盖品牌/设计系统变更、平台可访问性要求变化，以及行为评测出现过度弱化或误判。

- [x] **Step 7: 运行 JSON、追踪与系统校验**

Run:

```bash
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
python3 -m json.tool sources/rule-traceability.json >/dev/null
python3 tools/agent_system.py validate .
python3 -m unittest discover -s tools/tests -p 'test_*.py'
```

Expected: JSON 命令退出 0；system 输出 `VALID`；全部现有单元测试通过。若测试成本或环境导致无法运行完整套件，必须保存失败命令和原始错误，不得将未运行写成通过。

- [x] **Step 8: 独立审查 Task 2**

审查者确认 LOC-030、TIP-077 和规则追踪语义一致；原始 29 文件审计没有被篡改；EVAL-05 写的是可失败 contract 而非虚假的实测结果；SOP 不依赖 Codex Desktop。

---

### Task 3: 将 UI 约束投影到原始 M05–M09 Prompt

**Files:**

- Modify: `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`

**Interfaces:**

- Consumes: Task 1 的完整规则和 Task 2 的阶段/评测边界。
- Produces: M05 定义、M06 验证、M07 传递、M08 实现、M09 审查的权威 Prompt 语义，供 Task 4 对话化镜像。

- [x] **Step 1: 更新 M05 的可观察 UI 规格契约**

在方法与输出结构中加入：若规格包含 UI，记录界面类型、目标 viewport/输入方式、信息密度、使用频率、主操作、次要操作和高风险操作；将相对显著性、图标可识别性、静止态层级和状态反馈写成可观察 acceptance。禁止在 M05 写跨场景统一像素值、指定新图标库或把实现风格伪装成需求。

- [x] **Step 2: 更新 M06 的原型发现与视觉证据**

要求 UI 原型先读取同屏页面、design tokens、组件、单一图标家族和内容密度；2–3 个方向主要在结构、流程或层级上不同，不能仅换装饰；强强调如果是实验变量必须预先记录。`Accessibility/usability checks` 增加静止态、图标理解、命中区和同屏相对重量证据。

- [x] **Step 3: 更新 M07 的 UI 约束传递**

要求用户可见 ticket 从 A05/A06 追溯视觉约束、已批准例外、目标页面、viewport、状态、复用的 token/component/icon source 和同屏验证方法。M07 不重新做视觉决策；新增组件/图标依赖、跨设计系统或公共 UI API 变化仍进入 G3/G4。

- [x] **Step 4: 更新 M08 的 UI 实现与同屏自检**

将现有宽泛的前端检查扩充为：

- 复用 design tokens、组件和单一图标家族。
- 按界面类型、平台、输入方式、密度、频率和任务层级决定尺寸/间距，不靠单纯放大建立层级。
- 真正次要的入口、设置、开关和工具按钮不压过主任务；安全、隐私、无障碍和主任务例外按规格处理。
- 标准动作使用熟悉图标；歧义、低频和高后果动作有可见文字；icon-only 控件有 accessible name、focus、状态和足够命中区。
- 静止态层级不依赖 hover、tooltip、颜色或动效；没有任务/平台/品牌依据时避免过度装饰。
- 实际渲染后与同屏元素比较相对尺度、重量和密度；调整后复验可读性、focus、命中区与状态。
- 未查看渲染时在 A08 明确 `Visual verification: not run`。

- [x] **Step 5: 更新 M09 的证据化视觉审查**

Web UI 审查增加：显著性是否匹配当前任务；次要控件是否压过主任务；核心语义是否依赖 hover/tooltip；图标是否熟悉且有正确语义；危险动作是否具备标签和适当保护；同屏尺度、重量和密度是否有真实证据。Finding 必须追溯到 A05/A06、适用 AGENTS/module、项目设计系统或可观察任务受阻；前者归 Spec 轴，后者归 Standards 轴，不能新增「个人审美」第三轴。无浏览器/截图/视觉回归证据时写入 `Unverified scope`。

- [x] **Step 6: 运行原始 Prompt 静态检查**

Run from workspace root:

```bash
ruby -e 'files=Dir.glob("全栈开发Prompt Chain/prompts/{05,06,07,08,09}-*.md").sort; abort("expected 5 files") unless files.size==5; files.each{|f| t=File.read(f, encoding:"UTF-8"); abort("unbalanced fence: #{f}") unless t.scan(/^```/).size.even?; base=File.basename(f)[0,2]; abort("missing M#{base}: #{f}") unless t.include?("M#{base}"); abort("missing A#{base}: #{f}") unless t.include?("A#{base}"); abort("missing completion: #{f}") unless t.include?("完成标准")}; puts "PROMPT_SOURCE_CHECK=PASS"'
```

Expected: `PROMPT_SOURCE_CHECK=PASS`。

- [x] **Step 7: 独立审查 Task 3**

审查者确认五个阶段各司其职：M05 不写实现规格，M06 不把装饰当备选，M07 不重新设计，M08 有真实同屏自检，M09 finding 有证据；原有授权和产物结构无回退。

---

### Task 4: 同步对话 Prompt、跨模块工作流与控制器

**Files:**

- Modify: `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- Modify: `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- Modify: `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`

**Interfaces:**

- Consumes: Task 3 的 M05–M09 权威语义和现有 `prompts_ask` 单问题协议。
- Produces: 可复制的人机对话镜像、跨模块 UI 契约、CLI 使用说明和控制器追溯不变量。

- [x] **Step 1: 对话化镜像 M05–M09**

逐文件使用 `apply_patch` 投影 Task 3 的阶段语义。每个文件继续满足：

- 建立并更新 `Facts`、`Decisions`、`Assumptions`、`Open questions`。
- 每轮只问一个会改变当前阶段结论的问题，提供原因、推荐答案、备选影响和「不知道」。
- 能从 Axx、代码或设计系统查明的视觉事实先查，不重复询问。
- 信息充分后先给完成摘要，只问一次是否生成对应 A05–A09；确认后才输出公共八段和模块专用章节。
- 不因 UI 规则扩大 G3/G4/R3、本地写入、dependency、浏览器或外部工具授权。

- [x] **Step 2: 在模块化工作流增加 UI 跨模块契约**

在通用产物之后、M05–M09 模块段附近增加紧凑表格：M05 定义可观察约束；M06 验证不确定性；M07 传递而非重做决策；M08 实现并同屏复核；M09 独立审查并要求证据。表格不复制完整风格清单。

- [x] **Step 3: 更新 Prompt Chain 使用手册的质量检查**

增加两项检查：

- UI 层级是否由界面类型、输入方式、信息密度、频率和任务优先级决定，而不是任意统一规格或装饰性放大。
- 用户可见改动是否有目标 viewport、主题和状态下的真实同屏证据。

明确 Codex CLI 只使用项目已有或当前环境可用的本地浏览器、截图或视觉回归工具；工具不可用时写 `Visual verification: not run`，不依赖 Codex Desktop 右侧浏览器面板。

- [x] **Step 4: 更新端到端控制器不变量**

在 `prompts/99-端到端Prompt-Chain.md` 的全局纪律或 Controller acceptance 中增加一条：用户可见 UI 变更必须把适用的 A05/A06 视觉约束传递到 M07/M08，并在 M08/M09 记录实际同屏渲染证据；证据不存在时只能标记未验证，不得宣称视觉完成。不得把具体圆角、阴影或图标清单复制进控制器。

- [x] **Step 5: 运行对话 Prompt 和控制器静态检查**

Run:

```bash
ruby -e 'common=%w[Metadata Facts Decisions Assumptions]; common += ["Open questions","Risks and reversibility","Acceptance evidence","Handoff"]; files=Dir.glob("全栈开发Prompt Chain/prompts_ask/*.md").sort; abort("expected 13") unless files.size==13; files.each{|f| t=File.read(f,encoding:"UTF-8"); abort("bad fence #{f}") unless t.scan(/^```/).size.even?; common.each{|h| abort("missing #{h}: #{f}") unless t.match?(/^## #{Regexp.escape(h)}$/)}; abort("missing single-question protocol: #{f}") unless t.include?("每轮只问一个"); abort("missing confirmation: #{f}") unless t.include?("确认生成")}; puts "PROMPTS_ASK_CHECK=PASS"'
rg -n "Visual verification: not run|同屏|视觉约束" \
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md' \
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
```

Expected: `PROMPTS_ASK_CHECK=PASS`；第二条命令显示使用手册和控制器中的新增不变量。

- [x] **Step 6: 独立审查 Task 4**

审查者确认普通/对话 Prompt 的 M05–M09 语义匹配；公共八段和单问题协议完整；使用手册只依赖 CLI 可用工具；控制器只承载追溯不变量，没有复制风格正文或扩大授权。

---

### Task 5: 全目录一致性、安全边界与最终证据

**Files:**

- Review: Tasks 1–4 的全部目标文件。
- Compare unchanged: 设计规格中明确不修改的 shared core、Claude、DSH、Cursor、zip 和旧 `Constraint/Codex_AGENTS.md`。
- Record: `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/` 下的任务报告与最终审查结果。

**Interfaces:**

- Consumes: Tasks 1–4 的已审查产物。
- Produces: 系统 validator、单元测试、Prompt 静态检查、31 个已命名保护文件的哈希比对、native/logical-readable 字节与哈希一致性、逐文件内容 manifest 和最终独立审查结论。

**Content-freeze gate:** Task 3 和 Task 4 必须已完成并通过各自 scoped review，SDD ledger 不再标记交付内容进行中，所有 writer 停止后才可执行本 Task。先用 Ruby、Python 和 `/bin/cat` 可见的 logical-readable 内容跑通 Steps 1–4 并完成人工语义审查；若 logical-readable 内容不是已批准的最终内容，不得执行 Step 5 的归一化。

- [x] **Step 1: 重跑 Coding Agent 系统验证**

Run:

````bash
set -euo pipefail
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
export PYTHONDONTWRITEBYTECODE=1
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py validate .
python3 -m unittest discover -s tools/tests -p 'test_*.py'
````

Expected: `render-templates` 仅列出应渲染的 adapter，它本身不证明无漂移；后续 `validate .` 未报 `shared core drift` 且输出 `VALID` 才是 shared snapshot 无漂移证据。单元测试全部通过；任一前置命令失败时整段立即失败。

- [x] **Step 2: 隔离验证前端模块路由**

Run:

````bash
set -euo pipefail
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
ui_rule_tmp=$(/usr/bin/mktemp -d /tmp/codex-ui-rule.XXXXXX)
case "$ui_rule_tmp" in
  /tmp/codex-ui-rule.*) ;;
  *) echo "unsafe temporary root: $ui_rule_tmp" >&2; exit 1 ;;
esac
test -d "$ui_rule_tmp"
test ! -L "$ui_rule_tmp"
ui_rule_project="$ui_rule_tmp/project"
test ! -e "$ui_rule_project"
test ! -L "$ui_rule_project"
python3 tools/agent_system.py init-project "$ui_rule_project" \
  --stack frontend-visual-quality --apply
python3 tools/agent_system.py validate-generated \
  --kind project --root "$ui_rule_project"
rg -n --fixed-strings ".agents/rules/frontend-visual-quality.md" \
  "$ui_rule_project/AGENTS.md"
/usr/bin/cmp \
  templates/modules/frontend-visual-quality.md \
  "$ui_rule_project/.agents/rules/frontend-visual-quality.md"
echo "ROUTE_CHECK=PASS path=$ui_rule_project"
````

Expected: 初始化和 `validate-generated` 退出 0；`rg` 显示根路由；`cmp` 无输出且退出 0；最后一行记录可供复核的临时项目路径。临时目录位于 `/tmp`，不访问真实项目或用户 home，本任务不执行递归删除。

- [x] **Step 3: 重跑 Prompt Chain 静态契约**

Run from workspace root:

````bash
set -euo pipefail
/usr/bin/ruby -e '
common=["Metadata","Facts","Decisions","Assumptions","Open questions","Risks and reversibility","Acceptance evidence","Handoff"]
ask=Dir.glob("全栈开发Prompt Chain/prompts_ask/*.md").sort
abort("expected 13 prompts_ask files") unless ask.size==13
ask.each do |f|
  t=File.read(f,encoding:"UTF-8")
  abort("unbalanced fence: #{f}") unless t.scan(/^```/).size.even?
  common.each{|h| abort("missing #{h}: #{f}") unless t.scan(/^## #{Regexp.escape(h)}$/).size==1}
  abort("missing one-question protocol: #{f}") unless t.include?("每轮只问一个")
  abort("missing generation confirmation: #{f}") unless t.include?("确认生成")
end
stage_patterns={
  "05"=>[/界面类型/, /viewport/, /信息密度/, /主操作|主\/次要/, /显著性/, /图标/, /静止态/],
  "06"=>[/design tokens?/, /图标家族/, /同屏/, /静止态/, /命中区/],
  "07"=>[/A05\/A06/, /viewport/, /token/, /component/, /icon/, /同屏/, /不得重新|不重新/],
  "08"=>[/design tokens?/, /图标家族/, /同屏/, /Visual verification: not run/, /命中区/],
  "09"=>[/显著性/, /tooltip/, /危险动作/, /同屏/, /Unverified scope/, /个人审美/]
}
pairs={}
%w[05 06 07 08 09].each do |id|
  sources=Dir.glob("全栈开发Prompt Chain/prompts/#{id}-*.md")
  dialogues=Dir.glob("全栈开发Prompt Chain/prompts_ask/#{id}-*.md")
  abort("expected exactly one source pair #{id}") unless sources.size==1
  abort("expected exactly one dialogue pair #{id}") unless dialogues.size==1
  source=sources.fetch(0)
  dialogue=dialogues.fetch(0)
  pairs[id]=[source,dialogue]
  [source,dialogue].each do |f|
    t=File.read(f,encoding:"UTF-8")
    abort("unbalanced fence: #{f}") unless t.scan(/^```/).size.even?
    abort("missing M#{id}: #{f}") unless t.include?("M#{id}")
    abort("missing A#{id}: #{f}") unless t.include?("A#{id}")
    abort("missing completion standard: #{f}") unless t.include?("完成标准")
    stage_patterns.fetch(id).each do |pattern|
      abort("missing #{pattern.inspect}: #{f}") unless t.match?(pattern)
    end
  end
end
authorization={
  "06"=>{
    pairs.fetch("06").fetch(0)=>[/G4_APPROVAL/, /ALLOWED_FILES_OR_SANDBOX/],
    pairs.fetch("06").fetch(1)=>[/G4_APPROVAL/, /ALLOWED_FILES_OR_SANDBOX/, /R3_ACTION_AUTHORIZATION/]
  },
  "08"=>{
    pairs.fetch("08").fetch(0)=>[/G4_APPROVAL/, /DEPENDENCY_CHANGES/, /不安装依赖/],
    pairs.fetch("08").fetch(1)=>[/G4_APPROVAL/, /ALLOWED_FILES/, /DEPENDENCY_CHANGES/, /R3_ACTION_AUTHORIZATION/]
  },
  "09"=>{
    pairs.fetch("09").fetch(0)=>[/只读审查/, /不自动修复/, /G4/],
    pairs.fetch("09").fetch(1)=>[/MODE=PLAN/, /修复必须另有/, /G4/, /R3_ACTION_AUTHORIZATION/]
  }
}
authorization.each_value do |by_file|
  by_file.each do |f,patterns|
    t=File.read(f,encoding:"UTF-8")
    patterns.each{|pattern| abort("missing authorization marker #{pattern.inspect}: #{f}") unless t.match?(pattern)}
  end
end
checked=pairs.values.flatten
combined=(ask+checked).uniq.map{|f| File.read(f,encoding:"UTF-8")}.join("\n")
%w[G5_APPROVAL G6_APPROVAL G5_PRODUCTION_READ_APPROVAL TODO FIXME].each{|x| abort("stale #{x}") if combined.include?(x)}
puts "FINAL_PROMPT_CONTRACT=PASS"
'
````

Expected: `FINAL_PROMPT_CONTRACT=PASS`。该检查只证明以下静态结构和关键词契约，不证明真实 Prompt 行为、语义完全等价或授权机制已经动态执行：

- `prompts/05–09` 与 `prompts_ask/05–09` 每个 ID 各恰好一份，均包含对应 Mxx、Axx、完成标准和阶段专属 UI 词法 oracle。
- 13 份 `prompts_ask` 保留 104/104 公共标题、单问题协议、确认门和 UTF-8。
- M06/M08/M09 的指定 G4、文件/沙箱、dependency、只读审查和 R3 授权标记仍存在；这不等于证明与修改前逐字节相同。
- 被检查的普通/对话 Prompt 无 `G5_APPROVAL`、`G6_APPROVAL`、`G5_PRODUCTION_READ_APPROVAL`、`TODO` 或 `FIXME`，且 Markdown 围栏平衡。

- [x] **Step 4: 比对明确不修改文件的哈希**

Run from workspace root. 从 Task 1 报告的 fenced baseline 解析恰好 31 个路径，重建同一组 `find` + 显式路径清单，并让任一集合或哈希差异直接失败：

````bash
set -euo pipefail
/usr/bin/ruby -ropen3 -e '
report="全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-1-report.md"
text=File.read(report,encoding:"UTF-8")
block=text[/### 明确不修改文件的 SHA-256.*?```text\n(.*?)```/m,1]
abort("protected baseline block missing") unless block
baseline={}
block.each_line do |line|
  next unless line.match?(/\A[0-9a-f]{64}  .+\n?\z/)
  digest,path=line.chomp.split("  ",2)
  abort("duplicate protected baseline path: #{path}") if baseline.key?(path)
  baseline[path]=digest
end
abort("expected 31 protected baseline entries, got #{baseline.size}") unless baseline.size==31
roots=[
  "Constraint/coding-agent-system/templates/shared",
  "Constraint/coding-agent-system/templates/user/claude",
  "Constraint/coding-agent-system/templates/user/deepseek-harness",
  "Constraint/coding-agent-system/templates/project/.claude",
  "Constraint/coding-agent-system/templates/project/deepseek-harness",
  "Constraint/cursor_rules"
]
out,status=Open3.capture2("/usr/bin/find",*roots,"-type","f","-print0")
abort("protected find failed") unless status.success?
current=out.split("\0")
current += [
  "Constraint/coding-agent-system/templates/project/AGENTS.md",
  "Constraint/Codex_AGENTS.md",
  "Constraint/coding-agent-system/templates.zip",
  "全栈开发Prompt Chain.zip"
]
current=current.sort
abort("expected 31 current protected paths, got #{current.size}") unless current.size==31
abort("duplicate current protected path") unless current.uniq.size==31
abort("protected path set differs from baseline") unless current==baseline.keys.sort
current.each do |path|
  out,status=Open3.capture2("/usr/bin/shasum","-a","256",path)
  abort("shasum failed: #{path}") unless status.success?
  actual=out.split.fetch(0)
  abort("protected hash mismatch: #{path}") unless actual==baseline.fetch(path)
  puts "#{actual}  #{path}"
end
puts "PROTECTED_MANIFEST=PASS files=31"
'
````

Expected: 31 行哈希后输出 `PROTECTED_MANIFEST=PASS files=31`。该证据只覆盖这 31 个已命名保护文件，不得扩大成「所有非目标文件」或「全仓未变」。Task 1 报告明确的 4 个文件缺少编辑前哈希；本步只能证明它们当前等于 Task 1 后补快照，不得表述为历史缺口已补齐。`Constraint/CLAUDE.md`、`templates/user/codex/config.toml` 或 `templates/project/.codex/config.toml` 如被另行检查，只能报告 current-only 哈希，不得加入这份历史 unchanged manifest。

- [x] **Step 5: 安全归一化双视图文件并生成内容 manifest**

Run from workspace root only after the content-freeze gate. 清单必须是下列静态 22 个路径，不使用 glob 决定写入目标。脚本仅对 external pathname/native view 与 `/bin/cat` logical-readable view 不一致的文件做同目录原子替换；不使用 `rm -rf`、glob 删除或 `mktemp -u`。

````bash
set -euo pipefail
cd /Users/lute/Project/vibecoding_config
export PYTHONDONTWRITEBYTECODE=1

files=(
  "Constraint/coding-agent-system/templates/user/codex/AGENTS.md"
  "Constraint/coding-agent-system/templates/project/codex/AGENTS.md"
  "Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md"
  "Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md"
  "Constraint/coding-agent-system/docs/sop/project-lifecycle.md"
  "Constraint/coding-agent-system/docs/research/local-tip-ledger.md"
  "Constraint/coding-agent-system/docs/research/tip-decision-matrix.md"
  "Constraint/coding-agent-system/docs/research/local-material-audit.md"
  "Constraint/coding-agent-system/sources/rule-traceability.json"
  "全栈开发Prompt Chain/04-模块化Skills工作流.md"
  "全栈开发Prompt Chain/06-Prompt-Chain使用手册.md"
  "全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md"
  "全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md"
  "全栈开发Prompt Chain/prompts/06-原型与UX验证.md"
  "全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md"
  "全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md"
  "全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md"
  "全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md"
  "全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md"
  "全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md"
  "全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md"
  "全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md"
)

test "${#files[@]}" -eq 22
unique_count=$(printf '%s\n' "${files[@]}" | LC_ALL=C /usr/bin/sort -u | /usr/bin/wc -l | /usr/bin/tr -d '[:space:]')
test "$unique_count" -eq 22

logical_size() { /bin/cat "$1" | /usr/bin/wc -c | /usr/bin/tr -d '[:space:]'; }
logical_hash() { /bin/cat "$1" | /usr/bin/shasum -a 256 | /usr/bin/awk '{print $1}'; }
native_size() { /usr/bin/stat -f %z "$1"; }
native_hash() { /sbin/sha256sum "$1" | /usr/bin/awk '{print $1}'; }

for f in "${files[@]}"; do
  test -f "$f"
  test ! -L "$f"
  test "$(/usr/bin/stat -f %l "$f")" -eq 1
  test "$(/usr/bin/stat -f %Sf "$f")" = "-"
  test -z "$(/usr/bin/xattr "$f")"
  test -z "$(/bin/ls -led "$f" | /usr/bin/sed -n '2,$p')"
done

for f in "${files[@]}"; do
  before_logical_size=$(logical_size "$f")
  before_logical_hash=$(logical_hash "$f")
  before_native_size=$(native_size "$f")
  before_native_hash=$(native_hash "$f")
  if test "$before_native_size" = "$before_logical_size" && \
     test "$before_native_hash" = "$before_logical_hash"; then
    continue
  fi

  dir=${f%/*}
  base=${f##*/}
  mode=$(/usr/bin/stat -f %Lp "$f")
  owner_group=$(/usr/bin/stat -f '%u:%g' "$f")
  tmp=$(/usr/bin/mktemp "$dir/.${base}.normalize.XXXXXX")
  case "$tmp" in
    "$dir"/."$base".normalize.*) ;;
    *) echo "unsafe normalization temp: $tmp" >&2; exit 1 ;;
  esac

  /bin/cat "$f" > "$tmp"
  /bin/chmod "$mode" "$tmp"
  /usr/bin/touch -r "$f" "$tmp"
  test "$(/usr/bin/stat -f '%u:%g' "$tmp")" = "$owner_group"
  python3 - "$tmp" <<'PY'
import os
import sys
fd = os.open(sys.argv[1], os.O_RDONLY)
try:
    os.fsync(fd)
finally:
    os.close(fd)
PY

  test "$(native_size "$tmp")" = "$before_logical_size"
  test "$(logical_size "$tmp")" = "$before_logical_size"
  test "$(native_hash "$tmp")" = "$before_logical_hash"
  test "$(logical_hash "$tmp")" = "$before_logical_hash"
  test "$(logical_size "$f")" = "$before_logical_size"
  test "$(logical_hash "$f")" = "$before_logical_hash"

  backup=$(/usr/bin/ruby -rsecurerandom -e '
    file=ARGV.fetch(0)
    dir=File.dirname(file)
    base=File.basename(file)
    loop do
      path=File.join(dir,".#{base}.pre-normalize-#{SecureRandom.hex(12)}")
      begin
        File.link(file,path)
        puts path
        break
      rescue Errno::EEXIST
      end
    end
  ' "$f")
  case "$backup" in
    "$dir"/."$base".pre-normalize-*) ;;
    *) echo "unsafe normalization backup: $backup" >&2; exit 1 ;;
  esac

  /bin/mv -f -- "$tmp" "$f"
  if test "$(native_size "$f")" = "$before_logical_size" && \
     test "$(logical_size "$f")" = "$before_logical_size" && \
     test "$(native_hash "$f")" = "$before_logical_hash" && \
     test "$(logical_hash "$f")" = "$before_logical_hash"; then
    /bin/rm -f -- "$backup"
    echo "NORMALIZED $f"
  else
    /bin/mv -f -- "$backup" "$f"
    test "$(native_size "$f")" = "$before_native_size"
    test "$(native_hash "$f")" = "$before_native_hash"
    test "$(logical_size "$f")" = "$before_logical_size"
    test "$(logical_hash "$f")" = "$before_logical_hash"
    echo "normalization failed and rolled back: $f" >&2
    exit 1
  fi
done

/usr/bin/ruby -ropen3 -rdigest -e '
files=ARGV
abort("expected 22 manifest files") unless files.size==22 && files.uniq.size==22
markdown_count=0
manifest=files.sort.map do |f|
  logical,status=Open3.capture2("/bin/cat",f)
  abort("cat failed: #{f}") unless status.success?
  logical=logical.b
  native_size,status=Open3.capture2("/usr/bin/stat","-f","%z",f)
  abort("stat failed: #{f}") unless status.success?
  native_hash,status=Open3.capture2("/sbin/sha256sum",f)
  abort("sha256sum failed: #{f}") unless status.success?
  digest=Digest::SHA256.hexdigest(logical)
  abort("native/logical size mismatch: #{f}") unless native_size.to_i==logical.bytesize
  abort("native/logical hash mismatch: #{f}") unless native_hash.split.fetch(0)==digest
  if f.end_with?(".md")
    markdown_count += 1
    text=logical.dup.force_encoding("UTF-8")
    abort("invalid UTF-8: #{f}") unless text.valid_encoding?
    abort("unbalanced fence: #{f}") unless text.scan(/^```/).size.even?
  end
  puts "#{digest}  bytes=#{logical.bytesize}  #{f}"
  "#{f}\0#{logical.bytesize}\0#{digest}\n"
end.join
abort("expected 21 Markdown files, got #{markdown_count}") unless markdown_count==21
puts "files=#{files.size} markdown=#{markdown_count}"
puts "manifest_sha256=#{Digest::SHA256.hexdigest(manifest)}"
' -- "${files[@]}"
````

Expected: 仅差异文件输出 `NORMALIZED`；每份文件的替换都保留 `/bin/cat` logical-readable 字节数和 SHA-256，保留 mode/mtime，且在删除该文件唯一、显式的 hard-link backup 前完成四重视图验证；失败时原子回滚并停止。最后输出 22 行逐文件 logical hash/bytes、`files=22 markdown=21` 和一个 `manifest_sha256`。manifest 行算法为 `path + NUL + logical_bytes + NUL + logical_sha256 + newline`。若脚本替换了任何文件，必须再重跑 Steps 1–5；未获得重跑的新鲜证据前不得进入 Step 6。

- [x] **Step 6: 执行三路最终独立审查**

并行只读审查：

1. **规则与可访问性边界：** 检查克制默认、例外、命中区、tooltip、危险动作和图标语义。
2. **Prompt 生命周期一致性：** 检查 M05–M09 普通/对话镜像、Axx 和跨模块传递。
3. **平台与授权安全：** 检查仅 Codex 变更、无 shared/其他平台漂移、无 Gate/R3 fail-open、CLI 不依赖 Desktop。

每项 finding 必须包含 severity、文件、位置、触发条件、影响和最小修复方向。修复 Critical/Important 后由原审查者做 scoped re-review；未关闭时不得声明完成。

- [x] **Step 7: 完成交付报告**

写入 `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/final-review-report.md`。报告只写结论、实际改动、采用/条件化/排除原因、验证命令与结果、逐文件 manifest 与 aggregate hash、未验证边界。明确说明未进行真实页面回放或真实 Codex 行为基准，`EVAL-05` 仍是 contract-only；“unchanged”结论只覆盖 Step 4 命名的 31 个保护文件，并保留 4 个文件缺少编辑前哈希的历史限制。Step 6 若产生 Critical/Important finding，先由父任务明确批准修复文件范围，修复后从 content-freeze gate 重新执行；Task 5 审查本身不隐式授权修改 22 个交付文件。
