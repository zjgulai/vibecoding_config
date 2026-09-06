# M08：全栈实现与 TDD（对话版）

## 用途

在 G4 通过后，一次实现一个垂直 slice，并保留最小 diff 与新鲜验证；包含已知/未知根因的 Debug 路由。

## 输入变量

```text
{{PROJECT_ROOT}}
{{A07_PATH}}
{{CURRENT_TICKET_ID}}
{{G4_APPROVAL}}
{{MODE}} = PLAN
{{ALLOWED_FILES}}
{{DEPENDENCY_CHANGES}} = DENY 或精确授权
```

## 可复制对话 Prompt

```text
你正在执行 M08「全栈实现与 TDD」，默认 MODE=PLAN、只读。只有当前 slice 的 G4_APPROVAL、ALLOWED_FILES 和 DEPENDENCY_CHANGES 均精确匹配并已核验后，才可明确切换为 MODE=APPLY 并改代码。

先读取项目指令、A07 当前 ticket、相关代码/测试/规范源，并检查工作区状态。建立并在每轮回答后更新 Facts、Decisions、Assumptions、Open questions：Facts 有来源；Decisions 已确认；Assumptions 未证实；Open questions 只保留会改变当前 slice、架构、数据、权限、安全、兼容性或验收的未决项。发现与 ALLOWED_FILES 重叠的未知改动即停止。

仅在用户显式选择且已有确认 tickets 时加载 `implementation-orchestration`；新行为或已知修复时若 `tdd` 已安装则加载；根因不明、flaky、性能或跨模块故障时若 `systematic-debugging` 已安装则加载。未安装时按照本 Prompt 执行，明确没有加载；目标仓库的自动 commit 不适用。

单问题协议：每轮只问一个当前信息价值最高的问题。问题必须含「为什么问」「推荐答案及理由」「备选项影响」「不知道（记为 Open question，并说明最小补证据方式）」。用户回答后，先复述新增 Decisions、更新 Facts/Assumptions 和仍未关闭的 Open questions，再继续；可由代码或 A07 查明的事实先查。

启动门：核验当前 ticket、前置 ticket 完成证据、接口名称、acceptance、最窄验证命令、G4_APPROVAL、ALLOWED_FILES 与 DEPENDENCY_CHANGES。仅当三项授权均精确匹配且其余前置条件满足时，才明确切换为 APPLY；G4 缺失/过期/不匹配、ticket 不明确、依赖未满足、允许文件缺失/不匹配，或所需依赖/lockfile 变更不是精确授权时，保持 PLAN，只给计划并停止。

执行规则：
1. 先搜索现有实现、调用点、工具函数和测试，优先复用；只改当前 slice 所需内容，不预做后续 ticket、不全局格式化。
2. 新行为/已知修复：在 public seam 写会因目标行为缺失而失败的测试；先运行确认正确 red，再写最小实现，运行 green；仅在 green 后做必要重构并复验。
3. Debug 必须先稳定复现并证伪：定义 exact symptom 与 pass/fail command，缩减复现，提出可证伪预测，一次只改变一个变量。根因有证据后才写 regression test 和 fix；不得猜测性 patch。
4. 连续三次验证失败、patch 相互干扰或范围膨胀时停止局部修补，重新审查 data/state/dependency/failure boundary。
5. 前端先复用 design tokens、组件和单一图标家族；按界面类型、平台、输入方式、密度、频率和任务层级决定尺寸/间距，不靠单纯放大建立层级。真正次要的入口、设置、开关和工具按钮不压过主任务；安全、隐私、无障碍和主任务例外按规格处理。标准动作使用熟悉图标；歧义、低频和高后果动作有可见文字；icon-only 控件有 accessible name、focus、状态和足够命中区。静止态层级不依赖 hover、tooltip、颜色或动效；没有任务、平台或品牌依据时避免过度装饰。前端检查 loading/empty/error/disabled/success、responsive、keyboard/focus、accessibility 与实际页面；后端检查 validation、authn/authz、error、idempotency、transaction/concurrency、timeout/retry、日志脱敏和 compatibility。
6. 数据库变更须有 forward、rollback/repair、compatibility window 与隔离验证，未经授权不连真实数据库。AI 须有 deterministic seam、provider boundary、prompt/model/config 版本、fallback、成本/延迟观察与 eval fixtures。
7. 实际渲染后在目标 viewport/状态与同屏元素比较相对尺度、重量和密度；调整后复验可读性、focus、命中区与状态。不得以该检查安装或调用未经授权的浏览器、截图、网络、外部或其他工具；仅可在适用授权范围内使用项目已有或当前环境可用工具。未查看渲染、工具不可用或未经授权时原样记录 `Visual verification: not run`。
8. 每个行为增量先跑最窄验证；首次取得可信 green 后，冻结命令、结果与 acceptance，只从当前 diff 提取候选。每次只移除一个候选并立即重跑覆盖它的最窄验收；失败、证据变弱或风险上升就恢复并 retain。候选完成后再运行共享接口/配置变化所需的最终相关 regression、lint、typecheck、build，最后清理临时 instrumentation、debug code、测试数据和孤儿产物。不得扩大 ALLOWED_FILES 或 DEPENDENCY_CHANGES，也不得修改或删除测试制造 green；工具输出截断时重新获取，未运行写 not run。

安全与停止边界：不得安装依赖、改 lockfile、读取 secrets、commit/push、建 Issue/PR、deploy，除非该精确动作另有未过期 R3_ACTION_AUTHORIZATION；`DEPENDENCY_CHANGES=DENY` 一律禁止依赖与 lockfile 变更。G5/G6 不能替代动作授权。发现用户改动重叠、权限/安全问题、关键验收歧义或范围外需求时停止，不替用户决定。

信息充分且执行/验证证据已收集后，先展示完成摘要（ticket、写入范围、变更、red/diagnostic、green/回归证据、消融证据状态、风险、Open questions、拟生成 A08），并只问：“确认生成 A08-implementation-report.md 吗？”确认后才输出下列结构；不要执行 commit、外部动作或范围外写入。

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
记录页面、目标 viewport、主题、状态、同屏比较基准和结果；未查看渲染、工具不可用或未经授权时原样写 `Visual verification: not run`。
## Frontend/backend/data/AI special checks
## Scope review
## Unresolved risks
## External actions not performed
## Handoff
给出固定 review range、A05/A07、changed files 和未验证项。

完成标准：当前 slice 验收有新鲜证据；diff 最小；用户变更未被覆盖；无自动 commit 或范围外副作用；Debug 在稳定复现与证伪后才修复。
```
