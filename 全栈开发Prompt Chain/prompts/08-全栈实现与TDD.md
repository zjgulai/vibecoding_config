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
{{MODE}} = APPLY
{{ALLOWED_FILES}}
{{DEPENDENCY_CHANGES}} = DENY 或精确授权
```

## 可复制 Prompt

```text
你正在执行 M08「全栈实现与 TDD」。只有 G4 对当前 slice 明确通过时才能改代码。

输入：
- PROJECT_ROOT: {{PROJECT_ROOT}}
- A07_PATH: {{A07_PATH}}
- CURRENT_TICKET_ID: {{CURRENT_TICKET_ID}}
- G4_APPROVAL: {{G4_APPROVAL}}
- MODE: {{MODE}}
- ALLOWED_FILES: {{ALLOWED_FILES}}
- DEPENDENCY_CHANGES: {{DEPENDENCY_CHANGES}}

启动检查：
1. 读取指令、A07 中当前 ticket、相关代码/测试/规范源；检查工作区状态。发现与允许文件重叠的未知改动时停止。
2. 验证前置 ticket 完成证据、接口名称、acceptance 和最窄验证命令。G4 缺失、ticket 不明确或依赖未满足时保持 PLAN。
3. implementation-orchestration 只在用户显式选择且有已确认 tickets 时加载。目标仓库 implement 的“自动 commit”不适用。

执行规则：
4. 先搜索现有实现、调用点、工具函数和测试；优先复用。只改当前 slice 所需内容，不预做后续 ticket、不全局格式化。
5. 新行为/已知修复：加载 tdd。在 public seam 写一个能因目标行为缺失而失败的测试；运行确认是正确 red；写最小实现；运行 green；只在 green 上做必要重构并复验。
6. 根因不明、flaky、性能或跨模块故障：先加载 systematic-debugging。定义 exact symptom/pass-fail command，缩减复现，提出可证伪预测，一次改变一个变量；根因有证据后再写 regression test 和 fix。
7. 连续三次验证失败、patch 相互干扰或范围膨胀时停止局部修补，重新审查 data/state/dependency/failure boundary。
8. 前端同时覆盖 loading/empty/error/disabled/success、responsive、keyboard/focus、accessibility 和实际页面检查：复用 design tokens、组件和单一图标家族；按界面类型、平台、输入方式、密度、频率和任务层级决定尺寸/间距，不靠单纯放大建立层级。真正次要的入口、设置、开关和工具按钮不得压过主任务；安全、隐私、无障碍和主任务例外按规格处理。标准动作使用熟悉图标；歧义、低频或高后果动作有可见文字；icon-only 控件具备 accessible name、可见 focus、明确状态和足够命中区。静止态不得依赖 hover、tooltip、颜色或动效传达核心语义；没有任务、平台或品牌依据时避免过度装饰。实际渲染后与同屏元素比较相对尺度、视觉重量和密度；调整后复验可读性、focus、命中区和状态。此要求不授权安装或调用未经授权的浏览器、截图、网络、外部或其他工具；仅可在适用授权范围内使用项目已有或当前环境可用的工具。工具不可用或未经授权时，必须原样记录 `Visual verification: not run`。
9. 后端同时检查 validation、authn/authz、error semantics、idempotency、transaction/concurrency、timeout/retry、logging redaction 和 compatibility。
10. 数据库改动必须有 forward、rollback/repair、compatibility window 和隔离验证；未经授权不连接真实数据库。
11. AI 功能实现必须保留 deterministic seam、provider boundary、prompt/model/config 版本、fallback、cost/latency observation 和 eval fixtures。
12. 不安装依赖、不改 lockfile、不读取 secrets、不 commit/push/Issue/PR/deploy，除非这些精确动作另行授权。
13. 每个行为增量先运行最窄验证；工具输出截断时重新获取，不声称通过。
14. 每个 slice 首次取得可信 green 后、最终相关回归和清理前，冻结命令、结果与 acceptance，只从当前 diff 提取候选；每次只移除一个并立即重跑覆盖它的最窄验收。失败、证据变弱或风险上升就恢复并 retain；候选完成后再跑风险相称的完整相关回归，包含共享接口/配置改变所需的相关 regression、lint、typecheck、build。不得扩大 ALLOWED_FILES 或 DEPENDENCY_CHANGES，也不得修改或删除测试制造 green。
15. 删除临时 instrumentation、debug code、测试数据和孤儿产物。

输出 `A08-implementation-report.md`：

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

## UI visual verification
记录页面、viewport、主题/状态、同屏基准、方法和结果。未查看实际渲染时必须原样写：`Visual verification: not run`。

## Frontend/backend/data/AI special checks
## Scope review
## Unresolved risks
## External actions not performed
## Handoff
给出固定 review range、A05/A07、changed files 和未验证项。

完成标准：当前 slice 的验收有新鲜证据；diff 最小；用户变更未被覆盖；没有自动 commit 或范围外副作用。
```
