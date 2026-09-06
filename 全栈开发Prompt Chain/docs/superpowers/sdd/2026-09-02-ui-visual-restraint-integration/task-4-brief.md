# Task 4: 同步对话 Prompt、跨模块工作流与控制器

## Context

本任务执行已批准实施计划的第四阶段。以 Task 3 最终通过审查的原始 M05–M09 为权威阶段语义，将其对话化镜像到 `prompts_ask`，并在模块工作流、CLI 使用手册和端到端控制器中增加紧凑的跨模块追溯契约。Task 3 未完成审查前不得实施；实施时必须重新完整读取最终原始 M05–M09，不得依据旧预检快照。当前目录不是 Git 仓库，不 commit；所有人工编辑必须使用 `apply_patch`。

开始前完整阅读：

- `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-02-ui-visual-restraint-integration-design.md`
- `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ui-visual-restraint-integration.md` 的 Global Constraints 与 Task 4
- Task 3 最终 `task-3-report.md` 及 `prompts/05–09` 五份权威 Prompt
- 本任务列出的八个目标文件

## Global constraints

- 只修改五份 `prompts_ask/05–09`、模块化工作流、使用手册、端到端控制器及本任务报告；不得修改原始 M05–M09、AGENTS、SOP、评测、追踪、其他平台或 zip。
- 对话版必须保留自身更严格的 PLAN、单问题、生成确认和授权语义，不能用原始版整文件覆盖。
- 五阶段职责保持为 M05 定义、M06 验证、M07 传递、M08 实现、M09 审查；完整风格规则仍只存在于 `frontend-visual-quality.md`。
- 不扩大 G0/G3/G4/R3、MODE、ALLOWED_FILES、DEPENDENCY_CHANGES、浏览器、网络、付费、真实 provider、生产或外部动作授权。
- CLI 工具不可用时记录 `Visual verification: not run`；不得依赖 Codex Desktop 右侧浏览器面板。
- 不新增 dependency；单一图标家族不构成安装图标库的授权。

## Files

- Modify: `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- Modify: `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- Modify: `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`
- Report: `全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-4-report.md`

不得修改其他文件。

## Before hashes

- `prompts_ask/05-领域模型与产品规格.md`: `e1ba23c03ba28f3044152cb51a64f5ae90a299e6c0f04240a269688708b661e5`
- `prompts_ask/06-原型与UX验证.md`: `958fa92667198199a3475149a292c637bff40cb034e133c69ed07931ff4553db`
- `prompts_ask/07-架构设计与任务拆解.md`: `88f75b758b143b25f631a073d3a1805afc142c92b976bbbca8347c587a7d14b9`
- `prompts_ask/08-全栈实现与TDD.md`: `59e2a0d42480eb38861f6de26f0902095e1aa30be1d975298187f5835563ed0f`
- `prompts_ask/09-AI-Eval与质量安全.md`: `6b746b201cd58fb9567201c037f32c0baa4a5c1c86dfec8996ac9bafeb4a143b`
- `04-模块化Skills工作流.md`: `f1c0ee0922d5753b47a216012b7a95234c825f3303bc733d6f7247d30bcb4a03`
- `06-Prompt-Chain使用手册.md`: `d574a50a89658199d3807cefbb12a46b50ffd03cc9d49b97c0b39d198bfbab79`
- `prompts/99-端到端Prompt-Chain.md`: `84ef0cbe3c82bb862f902d058b82cf52b49925eb3766f3648fd44f62c90a324f`

这些哈希必须在实施前重算；若任一不一致，暂停并报告，不覆盖未知变化。

## Requirements

1. 对话化镜像 Task 3 最终 M05–M09 的阶段语义，但逐文件保留：
   - `Facts`、`Decisions`、`Assumptions`、`Open questions` 的持续更新。
   - 每轮只问一个会改变当前阶段结论的问题；每题包含原因、推荐答案、备选影响和「不知道」。
   - 能从 Axx、代码、同屏页面或设计系统查明的视觉事实先查，不向用户重复询问。
   - 信息充分后先给完成摘要，只问一次是否「确认生成」对应 A05–A09；确认前不输出最终 artifact、不执行写入或外部动作。
   - 八个公共标题各恰好出现一次：Metadata、Facts、Decisions、Assumptions、Open questions、Risks and reversibility、Acceptance evidence、Handoff。
2. M05 对话版：在优先澄清、规格规则和输出结构中镜像界面类型、viewport/输入方式、密度、频率、主/次/高风险操作与可观察 visual acceptance；禁止统一像素、新图标库和实现风格冒充需求；增加与原始版同名且阶段匹配的 `## UI context and visual acceptance`。
3. M06 对话版：事实读取覆盖同屏页面、tokens、组件、图标家族与内容密度；方向以结构/流程/层级区分，强强调作为实验变量时预登记；现有 Variants 与 Accessibility/usability sections 承载静止态、图标理解、命中区和同屏相对重量证据。保留 G4+sandbox 双重门与 G0 用户测试边界。
4. M07 对话版：明确消费 A05/A06 视觉约束与例外，用户可见 ticket 记录页面、viewport、状态、token/component/icon source、同屏验证方法；只传递不重新设计，缺失/冲突即 open question/blocker。保留始终 PLAN、G3/G4/R3 和 tracker preview 边界。
5. M08 对话版：镜像最终原始 M08 的阶段实现/同屏自检，不重复完整模块；输出增加 `## UI visual verification`，无实际渲染时原样写 `Visual verification: not run`。保留对话版默认 PLAN，以及 G4、ALLOWED_FILES、DEPENDENCY_CHANGES 三者精确匹配的 APPLY 边界和 R3 外部动作限制。
6. M09 对话版：在输入变量、启动方式、事实读取中加入 `A06_PATH`；镜像 Spec/Standards 视觉 finding 归轴、真实同屏证据、危险动作与 `Unverified scope`；Findings 表增加 `Evidence/trace`。保留固定 review range、先只读、修复另需 G4，以及真实 provider/付费/red-team endpoint 的对象级未过期 R3。
7. `04-模块化Skills工作流.md`：在通用产物规则之后、M00–M13 模块工作流之前增加紧凑五行表格，说明 M05 定义、M06 验证、M07 传递、M08 实现并同屏复核、M09 独立证据审查。只写跨模块契约，不复制视觉清单。
8. `06-Prompt-Chain使用手册.md`：在质量检查中增加两项：UI 层级是否由界面类型、输入方式、信息密度、频率和任务优先级决定，而不是统一规格/装饰放大；用户可见改动是否有目标 viewport、主题和状态下的真实同屏证据。明确 Codex CLI 只使用项目已有或当前环境可用的本地浏览器、截图/视觉回归工具；不可用则写 `Visual verification: not run`，不依赖 Desktop 面板。
9. `prompts/99-端到端Prompt-Chain.md`：在全局纪律增加一条 UI 追溯不变量：适用 A05/A06 视觉约束必须传递到 M07/M08，M08/M09 记录真实同屏渲染证据；无证据只能标记未验证，不得声明视觉完成。不要在 Controller acceptance 重复，也不要复制圆角/阴影/图标清单。
10. 更新 frontmatter 日期/修订号时延续既有格式；不顺手修复非本任务问题。

## Verification

从工作区根运行：

```bash
ruby -e 'common=%w[Metadata Facts Decisions Assumptions]; common += ["Open questions","Risks and reversibility","Acceptance evidence","Handoff"]; files=Dir.glob("全栈开发Prompt Chain/prompts_ask/*.md").sort; abort("expected 13") unless files.size==13; files.each{|f| t=File.read(f,encoding:"UTF-8"); abort("bad fence #{f}") unless t.scan(/^```/).size.even?; common.each{|h| abort("missing or duplicate #{h}: #{f}") unless t.scan(/^## #{Regexp.escape(h)}$/).size==1}; abort("missing single-question protocol: #{f}") unless t.include?("每轮只问一个"); abort("missing confirmation: #{f}") unless t.include?("确认生成")}; puts "PROMPTS_ASK_CHECK=PASS"'
rg -n "Visual verification: not run|同屏|视觉约束" \
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md' \
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
```

另做静态语义检查并记录：

- M05–M09 普通/对话版逐阶段语义匹配，但对话版专属安全门保留。
- M09 对话版含 `A06_PATH` 与 `Evidence/trace`；M08 对话版含原样 `Visual verification: not run`。
- 13 份对话 Prompt 的公共标题共 104/104，围栏平衡，单问题与确认门完整。
- 不存在 `G5_APPROVAL`、`G6_APPROVAL`、`G5_PRODUCTION_READ_APPROVAL`、`TODO` 或 `FIXME` stale token。
- 八个目标 UTF-8 可读；记录 after logical-readable SHA-256 及 pathname/logical size/hash 差异，不推断文件系统原因。

完整报告写入指定 report 文件，列出 exact changed files、requirements mapping、验证、after hashes、未验证项与 concerns。最终回复只给 DONE 状态、无 commit、测试摘要、concerns 和报告路径。
