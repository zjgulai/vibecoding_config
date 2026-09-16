# M13：复盘与 Skill 自进化

## 用途

把失败、用户纠正、测试回退、重复故障和实验学习转成待审候选；用固定 benchmark 和人工 gate 演进 Prompt/Skill，而不是自动修改长期规则。

推荐 Skill：`memory-governance`、`writing-for-agents` Audit、上游 `retro`、SkillOpt/`skillopt-sleep`、PostHog `improving-mcp-tools` 的 gated loop 方法。

## 输入变量

```text
{{A00_PATH}}
{{A08_PATH}}
{{A09_PATH}}
{{A11_PATH}}
{{A12_PATH}}
{{EVOLUTION_TARGET}} = prompt | skill | project-rule | eval | process
{{BENCHMARK_OR_TASKS}}
{{MODE}} = PLAN | APPLY；默认 PLAN
{{G6_ADOPTION_DECISION}} = NONE | Stage | Reject | Needs evidence | Approved design
{{LOCAL_CHANGE_AUTHORIZATION}} = NONE 或绑定 target files/exact diff 的 G3/G4 本地变更授权
{{R3_ACTION_AUTHORIZATION}} = NONE 或外部发布的对象级授权
```

## 可复制 Prompt

```text
你正在执行 M13「复盘与 Skill 自进化」。默认只生成候选和评估计划，不自动采用。

输入：
- A00_PATH: {{A00_PATH}}
- A08_PATH: {{A08_PATH}}
- A09_PATH: {{A09_PATH}}
- A11_PATH: {{A11_PATH}}
- A12_PATH: {{A12_PATH}}
- EVOLUTION_TARGET: {{EVOLUTION_TARGET}}
- BENCHMARK_OR_TASKS: {{BENCHMARK_OR_TASKS}}
- MODE: {{MODE}}
- G6_ADOPTION_DECISION: {{G6_ADOPTION_DECISION}}
- LOCAL_CHANGE_AUTHORIZATION: {{LOCAL_CHANGE_AUTHORIZATION}}
- R3_ACTION_AUTHORIZATION: {{R3_ACTION_AUTHORIZATION}}

原则：
1. 普通成功不自动触发长期记忆。优先复盘：测试失败、用户纠正、返工、重复故障、安全发现、错误触发、显著成本/延迟或实验反证。
2. 区分 incident facts、contributing factors、decision quality、process gap、tool gap 和 outcome。避免事后诸葛亮；问“当时可获得的证据能否支持该决定”。
3. 候选经验必须有可复现 evidence、窄 scope、反例、冲突/风险和 expiry signal。秘密、PII、原始会话和一次性路径不得进入 Memory。
4. 选择正确载体：跨项目稳定规则 -> user kernel candidate；项目事实 -> project profile/local docs；多步骤判断 -> Skill；路径/技术栈约束 -> local module；确定性阻断 -> hook/CI；测试可捕获的行为 -> test/eval。
5. 若 memory-governance 或 writing-for-agents Audit 已安装且用户显式选择，加载它们。它们只提出 retain/rewrite/move/delete/needs-evidence，不自动晋升。
6. “同类工作重复三次”只是一条发现信号，不是自动 Skill 化或采纳阈值。还必须证明任务边界稳定、输入/输出可描述、存在可复现 failure/trap，且相对普通 Prompt 有待验证的决策价值；证据不足时保留为 candidate/needs-evidence。
7. Skill/Prompt evolution 使用固定循环：harvest sanitized cases -> mine recurring task -> split replay/holdout -> run baseline -> propose bounded single-variable edit -> replay -> held-out gate -> stage -> human adopt。
8. Skill 候选必须交付一个可独立审计的 bundle：`adapter + trap fixture + answer/oracle + smoke A/B`。adapter 描述触发/输入/输出/权限/停止边界；trap fixture 暴露最容易误判的决策点；answer/oracle 定义可判定的期望；smoke A/B 固定任务、模型、配置与评分，并保留 raw result。缺任一项不得晋升正式 Skill。
9. 不在同一候选中同时修改 benchmark 和被测 Prompt/Skill。保留 no-regression cases、null result、negative result 和失败 journal，不删除失败样本来制造提升。仅使用合成 fixture、少量任务或少量重复运行时，结论只能称 `smoke`，不得称 benchmark、稳定提升或普适增益。
10. 限制 edit budget、sessions/tasks、并行 proposal 和轮次。连续两次同类失败先 park；非收敛时停止，不无限自改。
11. SkillOpt 或其他真实 backend 可能发送脱敏会话到 provider并消费预算；必须先审查数据边界和费用。默认用 mock/dry-run 和 reviewed tasks file。
12. 所有候选先 stage。G6 只决定采纳设计是否可进入变更提案，不授权写入。实际修改 Prompt、Skill、AGENTS/CLAUDE、project rule 或长期 Memory 必须同时满足 MODE=APPLY，以及与 target files、exact diff、风险等级、备份/回滚、验证和失效条件绑定的 `LOCAL_CHANGE_AUTHORIZATION`；R2 目标须经过 G3/G4。任一项缺失时只输出候选 diff 并停止。
13. 若还要向 registry、远端仓库、plugin catalog 或其他外部系统 publish/adopt，必须另有 `R3_ACTION_AUTHORIZATION`，逐项包含 Target、Action、Expected effect、Credential scope（不含值）、Cost、Rollback、Verification、Idempotency/duplicate guard、Expiry。auto-adopt/auto-publish 默认禁止。
14. 经授权采纳后仍只称在固定任务/模型/权限下通过，不推广为普遍提升。记录版本、评测、写入 receipt 和过期条件。

每次配置失败先分类为事实、候选规则、工具缺口、项目事实缺口或评测缺口。只有同类问题具备可复验证据、窄适用范围且 holdout 不退化时，才可提出单变量候选；否则保留为证据缺口或 park，不写成永久规则。

输出 `A13-retrospective.md`：

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

## Candidate classification
事实 | 候选规则 | 工具缺口 | 项目事实缺口 | 评测缺口；每项写依据、下一补证据动作或 park 原因。

## Proposed evolution target
## Skill candidate bundle
- Adapter: trigger、inputs/outputs、decision points、authority、stop conditions。
- Trap fixture: 最容易误判的情境与输入。
- Answer/oracle: 可判定的期望与失败条件。
- Smoke A/B: 固定任务、模型、配置、评分、原始结果和运行次数；合成/少量运行必须标为 `smoke`。
## Baseline and held-out evaluation plan
## Bounded proposed edit
以 diff/明确变更描述呈现，不直接应用。

## Evaluation result
Not run | Baseline | Candidate | Gate result；写模型、配置、权限、cases 和限制。

## Adoption decision
G6 design decision：Stage | Reject | Needs evidence | Approved design。`Approved design` 不等于已写入。

## Change proposal and authorization
列 target files、exact diff、risk level、backup/rollback、verification、expiry；未获本地变更授权写 `Not authorized`。若含外部发布，另列 R3 对象级授权。

## Execution receipt
未写入时写 `Not adopted / no persistent change`；实际写入时记录 changed targets、验证层级和回滚入口，不记录秘密。

## Rollback and monitoring
## Handoff
回到 M02/M03/M04/M08/M12，或不行动。

完成标准：学习有证据和边界；“重复三次”未被当作晋升阈值；Skill 候选 bundle 完整；benchmark 与被测对象没有共同漂移；G6 design 与实际写入授权分离；候选未自动晋升；null/negative/失败记录被保留；任何提升表述限定于实际评测范围，合成或少量运行只称 smoke。
```
