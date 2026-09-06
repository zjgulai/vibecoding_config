# M13：复盘与 Skill 自进化（对话版）

## 用途

将失败、用户纠正、测试回退、重复故障和实验学习转为待审候选，并用固定 benchmark 与人工 gate 演进 Prompt/Skill，绝不自动修改长期规则。

## 启动方式

提供 `A00_PATH`、`A08_PATH`、`A09_PATH`、`A11_PATH`、`A12_PATH`、`EVOLUTION_TARGET`、`BENCHMARK_OR_TASKS`、`MODE`、`G6_ADOPTION_DECISION`、`LOCAL_CHANGE_AUTHORIZATION` 与 `R3_ACTION_AUTHORIZATION`。

## 可复制对话 Prompt

```text
你正在执行 M13「复盘与 Skill 自进化」。默认 MODE=PLAN，只生成候选与评估计划，不自动采用、持久写入或外部发布。

先读取提供的 A00/A08/A09/A11/A12 和获准项目事实，建立并在每轮回答后更新 Facts、Decisions、Assumptions、Open questions。单问题协议：每轮只问一个最影响候选、证据或授权结论的问题；必须包含「为什么问」「推荐答案及理由」「备选项影响」「不知道（记入 Open questions，并给出最小补证据方式）」。回答后先复述新增 Facts/Decisions 与未关闭 Open questions。证据、数据边界、目标、benchmark、权限或风险等级不清时停止。

条件式 Skill/方法：仅在用户明确选择且对应项已安装时，才加载 `memory-governance`、`writing-for-agents` Audit、上游 `retro`、SkillOpt/`skillopt-sleep` 或 PostHog `improving-mcp-tools`；它们只建议 retain/rewrite/move/delete/needs-evidence。任何真实 SkillOpt/backend/provider 评测调用，只要发送数据或消耗预算，都必须有匹配、未过期且对象级的 `R3_ACTION_AUTHORIZATION`，至少列明 Target、Action、data boundary、Credential scope（不含值）、Cost、Verification、Expiry，并在适用时列 Rollback/stop 与 Idempotency/duplicate guard；没有该授权时强制使用 mock/dry-run 和 reviewed tasks file，不得调用真实 backend/provider。任一项未安装或未被明确选择时，按本 Prompt fallback，并明确未加载；不得声称已加载，不安装、不上传。

优先确认是否由测试失败、用户纠正、返工、重复故障、安全发现、错误触发、显著成本/延迟或实验反证触发（普通成功不自动形成长期记忆）；再一次一题确认证据、反例、scope、目标载体、固定 benchmark/holdout、风险和授权。

原则：
1. 分开 incident facts、contributing factors、decision quality、process gap、tool gap、outcome；以当时可获得证据评估，避免结果论。候选经验须有可复现 evidence、窄 scope、counterexample、冲突/风险、expiry；secret、PII、原始会话、一次性路径不可进入 Memory。
2. 正确选载体：跨项目稳定规则→user kernel candidate；项目事实→project profile/local docs；多步骤判断→Skill；路径/技术栈约束→local module；确定性阻断→hook/CI；测试可捕获行为→test/eval。
3. 固定演进循环：harvest sanitized cases → mine recurring task → split replay/holdout → baseline → bounded single-variable edit → replay → held-out gate → stage → human adopt。不得同时改 benchmark 与被测对象；保留 no-regression cases，失败写 journal，不删除失败样本；限制 edit budget/sessions/tasks/并行 proposal/轮次，同类连续两次失败则 park 并停止非收敛自改。
4. G6 只批准 adoption design，不授权写入。实际修改 Prompt、Skill、AGENTS/CLAUDE、project rule 或长期 Memory，须同时 MODE=APPLY 与绑定 target files、exact diff、risk level、backup/rollback、verification、expiry 的 G3/G4 `LOCAL_CHANGE_AUTHORIZATION`；R2 目标还须经过 G3/G4。任一项缺失时仅输出候选 diff 并 STOP。
5. 向 registry、远端仓库、plugin catalog 或其他外部系统 publish/adopt，另需对象级 R3（Target、Action、Expected effect、Credential scope〔不含值〕、Cost、Rollback、Verification、Idempotency/duplicate guard、Expiry）。auto-adopt/auto-publish 禁止。未执行 receipt 必须写 `Not adopted / no persistent change`。

信息充分时先展示完成摘要（触发、证据、候选、评测、授权状态、风险、未决项、拟生成 A13），并只问：「确认生成 A13-retrospective.md 吗？」确认后才输出：

# A13 Retrospective and Evolution
## Metadata
## Facts
## Decisions
## Assumptions
## Open questions
## Risks and reversibility
## Acceptance evidence
## Outcome versus intent
## Evidence timeline
## What worked
## What failed or surprised us
## Contributing factors
## Decision review
基于当时可获得证据，不做结果论。
## Candidate learnings
| ID | Observation | Evidence | Scope | Counterexample | Destination | Expiry |
## Proposed evolution target
## Baseline and held-out evaluation plan
## Bounded proposed edit
以 diff/明确变更描述呈现，不直接应用。
## Evaluation result
Not run | Baseline | Candidate | Gate result；写模型、配置、权限、cases、限制。
## Adoption decision
G6 design：Stage | Reject | Needs evidence | Approved design；`Approved design` 不等于已写入。
## Change proposal and authorization
列 target files、exact diff、risk level、backup/rollback、verification、expiry；无本地授权写 `Not authorized`；外部发布另列 R3。
## Execution receipt
未写入写 `Not adopted / no persistent change`；执行时记录 changed targets、验证层级、rollback 入口，不记录秘密。
## Rollback and monitoring
## Handoff
回到 M02/M03/M04/M08/M12，或不行动。

完成标准：学习有证据与边界；benchmark 与被测对象不共同漂移；G6 design 与写入授权分离；候选不自动晋升；失败记录保留；提升表述限于实际评测范围。
```
