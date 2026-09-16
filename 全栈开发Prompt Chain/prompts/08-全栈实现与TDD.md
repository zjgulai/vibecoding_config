# M08：全栈实现与 TDD

## 用途

在 G4 通过后，一次实现一个垂直 slice，保留最小 diff 和新鲜验证。也包含已知/未知根因的 Debug 路由。

推荐 Skill：`implementation-orchestration`、`tdd`、`systematic-debugging`、目标仓库 `implement` 的批次思路。必须移除自动 commit。

## 输入变量

```text
{{PROJECT_ROOT}}
{{A07_PATH}}
{{CURRENT_TICKET_ID}}
{{G4_APPROVAL}}
{{MODE}} = PLAN
{{ALLOWED_FILES}}
{{DEPENDENCY_CHANGES}} = DENY 或精确授权
{{AUTONOMY_MODE}} = interactive | bounded_async；默认 interactive
{{AUTONOMY_ENVELOPE}} = NONE 或当前任务的完整 Envelope
```

## 可复制 Prompt

```text
你正在执行 M08「全栈实现与 TDD」，默认 MODE=PLAN、只读。只有 `MODE=APPLY`，且当前 slice 的 `G4_APPROVAL`、`ALLOWED_FILES` 与 `DEPENDENCY_CHANGES` 三者均精确、未过期并彼此匹配时，才能写文件；否则只输出实施计划或预览。

输入：
- PROJECT_ROOT: {{PROJECT_ROOT}}
- A07_PATH: {{A07_PATH}}
- CURRENT_TICKET_ID: {{CURRENT_TICKET_ID}}
- G4_APPROVAL: {{G4_APPROVAL}}
- MODE: {{MODE}}
- ALLOWED_FILES: {{ALLOWED_FILES}}
- DEPENDENCY_CHANGES: {{DEPENDENCY_CHANGES}}
- AUTONOMY_MODE: {{AUTONOMY_MODE}}
- AUTONOMY_ENVELOPE: {{AUTONOMY_ENVELOPE}}

启动检查：
1. 读取指令、A07 中当前 ticket、相关代码/测试/规范源；检查工作区状态。发现与允许文件重叠的未知改动时停止。
2. 验证前置 ticket 完成证据、接口名称、acceptance 和最窄验证命令。只有 `MODE=APPLY` 且 G4、允许文件与依赖变更范围精确匹配时才进入写入；任一项缺失、过期、不明确、不匹配，或 ticket 依赖未满足时保持 PLAN，不写文件。
3. implementation-orchestration 只在用户显式选择且有已确认 tickets 时加载。目标仓库 implement 的“自动 commit”不适用。
4. 建立 intent authority：用户当前明确要求 > approved spec > tests > current behavior。低层证据与高层意图冲突时停止并列明冲突，不擅自重写 spec，也不得修改或删除测试来迎合实现；无法判断用户新指令是否覆盖既有批准时请求确认。

有界连续执行：若 `AUTONOMY_MODE=bounded_async`，先核对完整 `AUTONOMY_ENVELOPE` 的 Objective/DoD、R1、`ALLOWED_FILES`、tool/data scope、最窄验证、stop conditions、enforcement evidence 与 handoff。仅在全部一致时循环「最窄反馈 → 最小修改 → 重跑同一检查 → 记录证据」。遇到新依赖、架构/API/schema/auth/迁移、范围外文件、外部动作、敏感数据、连续不收敛或验证证据变弱时停止；不得自行降级风险或扩大范围。

执行规则：
5. 先搜索现有实现、调用点、工具函数和测试；优先复用。若 A07 启用了 shared transform，先检查共享语义源与所有受影响目标；若当前 slice 涉及任一 target adapter，先确认 A07 已命名该目标的 native validator，再检查适用的 sibling/platform branches。单目标 adapter 不因此启用 shared transform 或目标矩阵。只改当前 slice 所需内容，不预做后续 ticket、不全局格式化。
6. 新行为/已知修复：加载 tdd。在 public seam 写一个能因目标行为缺失而失败的测试；运行确认是正确 red；写最小实现；运行 green；只在 green 上做必要重构并复验。
7. 根因不明、flaky、性能或跨模块故障：先加载 systematic-debugging。定义 exact symptom/pass-fail command，缩减复现，提出可证伪预测，一次改变一个变量；根因有证据后再写 regression test 和 fix。
8. 连续三次验证失败、patch 相互干扰或范围膨胀时停止局部修补，重新审查 data/state/dependency/failure boundary。
9. 前端同时覆盖 loading/empty/error/disabled/success、responsive、keyboard/focus、accessibility 和实际页面检查：复用 design tokens、组件和单一图标家族；按界面类型、平台、输入方式、密度、频率和任务层级决定尺寸/间距，不靠单纯放大建立层级。真正次要的入口、设置、开关和工具按钮不得压过主任务；安全、隐私、无障碍和主任务例外按规格处理。标准动作使用熟悉图标；歧义、低频或高后果动作有可见文字；icon-only 控件具备 accessible name、可见 focus、明确状态和足够命中区。静止态不得依赖 hover、tooltip、颜色或动效传达核心语义；没有任务、平台或品牌依据时避免过度装饰。实际渲染后与同屏元素比较相对尺度、视觉重量和密度；调整后复验可读性、focus、命中区和状态。此要求不授权安装或调用未经授权的浏览器、截图、网络、外部或其他工具；仅可在适用授权范围内使用项目已有或当前环境可用的工具。工具不可用或未经授权时，必须原样记录 `Visual verification: not run`。
10. 后端同时检查 validation、authn/authz、error semantics、idempotency、transaction/concurrency、timeout/retry、logging redaction 和 compatibility。
11. 数据库改动必须有 forward、rollback/repair、compatibility window 和隔离验证；未经授权不连接真实数据库。
12. AI 功能实现必须保留 deterministic seam、provider boundary、prompt/model/config 版本、fallback、cost/latency observation 和 eval fixtures。
13. 不安装依赖、不改 lockfile、不读取 secrets、不 commit/push/Issue/PR/deploy，除非这些精确动作另行授权。若生成物或 lockfile 已获精确授权，只通过项目权威 generator/package-manager 流程改变源头并重新生成，禁止手改；运行验证前后检查工作区，任何验证命令造成未预期改写都视为失败并停止，不能把它隐去后宣称验证通过。
14. 验证按 `quick fixture -> affected native suite -> risk/full gate` 逐级执行：先以最小 fixture 获得快速反馈；每个被修改的 adapter 必须运行其预先定义的 native validator。启用 shared transform 时，再运行所有受影响目标各自的 native suite 与风险相称的目标矩阵；单目标 adapter 只需要目标原生证据，不自动产生矩阵。共享语义源、兼容/安全边界或高影响改动必须进入风险相称的完整 gate。只运行项目中存在且来源明确的命令；工具输出截断时重新获取，不声称通过。
15. 修改 shared transform 或 target adapter 时执行 semantic twin sweep：shared transform 搜索所有目标、sibling adapter、runtime helper 和测试中的同义实现；单目标 adapter 搜索该平台分支、runtime helper、配置边界和测试中的同义实现，不因此声称存在跨目标一致性。记录受影响 twin 与处置；范围外 twin 不擅自修改，列为 blocker/handoff。
16. 每个 slice 首次取得可信 green 后、最终相关回归和清理前，冻结命令、结果与 acceptance，只从当前 diff 提取候选；每次只移除一个并立即重跑覆盖它的最窄验收。失败、证据变弱或风险上升就恢复并 retain；候选完成后再跑风险相称的完整相关回归。消融不得删除已被 approved contract、兼容性、安全边界、迁移/recovery 或目标适配要求证明必要的 target adapter/seam。不得扩大 ALLOWED_FILES 或 DEPENDENCY_CHANGES，也不得修改或删除测试制造 green。
17. 删除临时 instrumentation、debug code、测试数据和孤儿产物。

按 `A08-implementation-report.md` 的以下 schema 输出内容；只有该报告路径也包含在精确 `ALLOWED_FILES` 中时才可落盘：

# A08 Implementation Report
## Metadata
## Facts
## Decisions
## Assumptions
## Open questions
## Risks and reversibility
## Acceptance evidence
## Ticket and acceptance
## Preflight
- Worktree status
- Existing patterns reused
- Allowed write set
- Intent authority conflicts

## Autonomy execution receipt
- Mode: interactive | bounded_async | Not used
- Scope and commands/results: 实际范围与原始证据
- Stop trigger and human intervention: 未触发时写 `Not triggered`
- Enforcement evidence: Not available | Declared only | 实际验证证据
- Unverified scope: 未验证范围

## Red/diagnostic evidence
命令、关键结果、证据层级；未运行写 not run。

## Changes
逐文件说明行为原因，不写流水账。

## Ablation evidence
- Baseline: 首次可信 green 的命令、结果、acceptance、不变量、风险和证据层级。
- Candidate: 仅当前 diff 中逐项检查的可删减实现。
- Trace: 当前 requirement、invariant、failure mode 或 risk；无则写 NONE。
- Decision: remove | defer | retain。
- Verification: 覆盖候选的最窄验收、最终相关回归的方法、结果和证据层级。
- Limitations: 未执行项、不可重建时序或残余风险。

## Green and regression evidence
| Check | Command | Result | Evidence level |

## Verification ladder and semantic twins
记录 quick fixture、每个被修改 adapter 的 native validator、shared transform 受影响目标的 native suite/目标矩阵、risk/full gate，以及 semantic twin sweep 的检索范围、命中、处置与范围外 handoff。单目标 adapter 明确写 `Shared transform/target matrix: Not applicable`；没有 adapter 或 twin 风险时写 `Not applicable`。

## UI visual verification
记录页面、viewport、主题/状态、同屏基准、方法和结果。未查看实际渲染时必须原样写：`Visual verification: not run`。

## Frontend/backend/data/AI special checks
## Scope review
## Unresolved risks
## External actions not performed
## Handoff
给出固定 review range、A05/A07、changed files 和未验证项。

完成标准：写入只发生在 MODE=APPLY 且 G4/ALLOWED_FILES/DEPENDENCY_CHANGES 精确匹配时；当前 slice 的验收有新鲜证据；intent authority 冲突已停止或解决；每个 adapter 有 native 证据，shared transform 才运行目标矩阵；semantic twins 已检查；diff 最小；用户变更未被覆盖；没有自动 commit 或范围外副作用。
```
