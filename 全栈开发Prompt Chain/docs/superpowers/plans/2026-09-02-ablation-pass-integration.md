# Codex 消融式删减检查融合 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将已批准的「消融式删减检查」落入 Codex 用户规则、前端视觉模块、项目生命周期、M06–M09 Prompt Chain、来源追溯和现有 contract-only 评测文档，使设计与实现首次满足验收后能够删除本轮无依据复杂度，同时保护必要质量边界。

**Architecture:** Codex 用户模板只保存常驻触发和最小协议；`frontend-visual-quality.md` 保存 UI 专项投影；`project-lifecycle.md` 与使用手册保存完整执行协议；M06/M07/M08 分别执行原型、架构和实现消融，M09 只读审证。追溯复用 `LOC-031 → TIP-078 → RUL-004 → EVAL-02 + EVAL-06`，不新增重复规则或第 12 个评测。

**Tech Stack:** Markdown、JSON、Python 3 标准库、Ruby、现有 `tools/agent_system.py` 与现有单元测试；不新增依赖，不调用真实模型、浏览器、外部 provider 或生产系统。

**Approved design:** `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-02-ablation-pass-integration-design.md`

## Global Constraints

- 首选术语是「消融式删减检查」。用户说「进行消融实验」时应触发该检查，但不得把静态文档集成写成已经完成严格模型消融实验。
- 只处理本轮新增设计或当前 diff，不清理历史无关抽象。
- 先取得可信 baseline/green，再冻结验收、不变量、风险和证据层级；每次只移除一个候选，使用同一组验收和回归复验。
- `remove | defer | retain` 必须有证据。代码行数、文件数、抽象层数或单次 green 不能单独证明方案更优。
- 不得删除由正确性、安全、权限、数据完整性、兼容性、并发/失败语义、可访问性、可观测性、性能、migration、恢复、回滚或已批准 UX 支撑的 seam。
- 消融不得扩大 G3/G4、`ALLOWED_FILES`、`DEPENDENCY_CHANGES`、R3、本地写入、外部动作或生产权限，不得删测试或降低 acceptance 制造 green。
- M06/M07 做设计消融；M08 在首次可信 green 后做实现消融；M09 只读核对证据，不自动修复。M04 现有 MVP/non-goals/no-build 已承担产品范围消融；M05 不借消融静默删需求。
- 只有用户级常驻触发面向 Codex，并且只写入 Codex user adapter；不修改 shared core 或 Claude Code、DeepSeek Harness/DSH Desktop、Cursor 的用户/项目配置。frontend module、SOP 与 Prompt Chain 是平台中立的方法资产，其他 Agent 只有在项目显式路由/加载时才可能消费；其中不得携带模型效果结论或冒充其他平台的常驻配置。
- 不修改真实 `~/.codex/AGENTS.md`、生产环境、外部 tracker、部署环境、zip 压缩包或已审计的旧输入材料。
- 当前目录不是 Git repository；不 commit，以固定输入哈希、逐文件检查、现有 validator/test 和三路独立审查替代 Git 证据。
- 所有人工内容编辑使用 `apply_patch`。若基线不匹配、发现用户并发改动或目标锚点不再唯一，立即停止并重新读取，不套用旧行号或旧 patch。
- 计划文件保持只读，checkbox 进度记录在任务状态中；实施开始时在 workspace 外创建固定、私有的 preimage snapshot，只复制 20 个目标文件正文，198 个受保护文件只保存 hash manifest，本计划另存动态 hash/size 而不复制正文；成功交付后只删除精确验证过的临时文件/空目录，失败时保留并报告位置。

## Exact Scope

仅允许修改以下 20 个交付文件：

1. `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`
2. `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`
3. `Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
4. `Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md`
5. `Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md`
6. `Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
7. `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
8. `Constraint/coding-agent-system/docs/research/local-material-audit.md`
9. `Constraint/coding-agent-system/sources/rule-traceability.json`
10. `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
11. `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
12. `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
13. `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
14. `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
15. `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
16. `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
17. `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
18. `全栈开发Prompt Chain/04-模块化Skills工作流.md`
19. `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
20. `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`

明确不修改：Codex 项目级 `templates/project/codex/AGENTS.md`、shared user/project core、Claude/DSH/Cursor 配置、`Constraint/Codex_AGENTS.md`、M00–M05 与 M10–M13 的普通/对话 Prompt、`templates/modules/typescript-nextjs.md`、评测 ID/schema/fixture manifest、两个 zip，以及前一轮 UI 视觉任务的历史规格和报告。这里的「配置未修改」不等于平台中立 module/SOP/Prompt Chain 对其他 Agent 不可见。

## Frozen Input Gate

### 20 个目标文件基线

实施前必须按 logical-readable 内容重跑哈希，结果与下表逐项一致；聚合值必须为 `c58402c59f4f9d0fadda96a07c07c17304d1743707bea57d5870f241c1c7068e`。

| SHA-256 | bytes | 路径 |
| --- | ---: | --- |
| `9ca8aa6698a17252cfcb4c8ff4d16fed5cf3d7041f8ec3aa08c922dd4e69bada` | 16229 | `Constraint/coding-agent-system/docs/research/local-material-audit.md` |
| `4331ad34d605fa315657574ea090140ddb4be9b8d2339323bb52f835739b0d09` | 18051 | `Constraint/coding-agent-system/docs/research/local-tip-ledger.md` |
| `7654502503284a7babb5d6108a387dadb9d870c91860dc6cef75cd72d1fb9396` | 24670 | `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md` |
| `d1b72b3c14593ccf489c2c3c9b09f0d4750e1ec9708bf3fc3357db9a32a6d32e` | 39277 | `Constraint/coding-agent-system/docs/sop/project-lifecycle.md` |
| `f30b146bff6f30905c398aca84411533913860cfd6d1de2f589a830253bd12d8` | 1243 | `Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md` |
| `d94e1b839a62969ee360c69aeec6cffed6d25ba120596b1822698f6660d2a777` | 1534 | `Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md` |
| `43811539e42fb0934e91ead0a45ab73d717f8677a015192ef3ee7e5d19d675f5` | 24036 | `Constraint/coding-agent-system/sources/rule-traceability.json` |
| `11920c5151f699bb4f7dfb647a77ea5b1a524c5e46abe8a486f1fa0dc355fdad` | 4231 | `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md` |
| `4c479667ab4197510e75a31f30b839e8081e26b43fbd069ce830cf034eb1eff1` | 5417 | `Constraint/coding-agent-system/templates/user/codex/AGENTS.md` |
| `73cea31abe38d2651e8ff048233c58b0d328ec2595a339b17bc6dfd8c71be22c` | 27476 | `全栈开发Prompt Chain/04-模块化Skills工作流.md` |
| `b9d03c70893902253b281c0231d49dda6576005164ccd116367f2a94729b3547` | 8834 | `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md` |
| `492560544495d04932ccbc73e3d22850f55e29b70fe60f052f6496473f914d73` | 4395 | `全栈开发Prompt Chain/prompts/06-原型与UX验证.md` |
| `7a55bc6f18e0a43464882b6b9f659cfd9cd78a4cd60dd540b412b7cab4a98bf4` | 4254 | `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md` |
| `dc278f16f93a96bdc3ce3d29dde4934ce0b2045513fc10afdc0d79ca458f4785` | 5196 | `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md` |
| `4a15a3688ad96079ce0d64ba61e058d38f6a576a370bcffd0354d0470f224151` | 4878 | `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md` |
| `2d4f44df5b26bc825b7137f9a1d81dfc7ea46ca2cb4e8f94608ce87c9031f38f` | 6770 | `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md` |
| `400a9e41b5398e27dace92ae07275e2b701af2beaaca7e99ede36047334afb7c` | 5329 | `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md` |
| `1d52e5076b62947d76915d479387bdc4c8cca4061ba3d96384970c3c67eeae48` | 5318 | `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md` |
| `bd56bfe6a2753ddebbff2fb64fa97dcf7990ff886ccbe62d7485cd0fdbc5feeb` | 6616 | `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md` |
| `2932debd09320393ca2299798dbdd8be32aefbb0360a3346fca17984af6c51f9` | 6103 | `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md` |

### 非目标保护基线

从 workspace root 运行计划附录 A 的 `protected_manifest` 检查。排除上述 20 个目标、`.DS_Store` 与本计划自身后，预期为：

```text
PROTECTED_FILES=198
PROTECTED_MANIFEST_SHA256=cd4fb937437161aa9946fc71f09c3109d53a8711b0d50b0f68f1cd4616b5e35b
```

任何差异都只说明受保护范围发生了变化。先识别是否为用户并发修改；不得还原或覆盖用户改动，也不得在未重新建立基线时继续。

---

### Task 1: 建立 Codex 常驻触发与 UI 专项消融门

**Files:**

- Modify: `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`
- Modify: `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`

**Interfaces:**

- Consumes: 已批准协议、现有 Codex adapter、现有 frontend visual quality module。
- Produces: Codex 用户层的紧凑触发和 UI 的同 viewport、同状态删减检查，供 SOP 与 Prompt 投影引用。
- Must preserve: `<!-- BEGIN SHARED CORE -->` 至 `<!-- END SHARED CORE -->` 字节不变；不得修改项目级 Codex adapter 或 shared core。

- [ ] **Step 1: 重跑 Frozen Input Gate**

运行附录 A 的目标清单与保护清单检查。预期分别输出 `TARGET_BASELINE=PASS files=20` 和上述 198 文件保护聚合值。任一项不符则停止。随后运行附录 A 的 `preimage_snapshot`，在 `/private/tmp/vibecoding-ablation-pass-20260902-c58402c5` 保存 20 个目标文件的 preimage、目标逐文件 manifest、198 个受保护文件的 hash manifest 和本计划的动态 hash/size；不复制受保护文件或计划正文。该路径已存在时不得覆盖或清空，应停止并确认来源。预期 `PREIMAGE_SNAPSHOT=PASS targets=20 protected=198 plan=1`。

- [ ] **Step 2: 先运行 Task 1 失败 oracle**

```bash
cd /Users/lute/Project/vibecoding_config
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path

if not __debug__:
    raise SystemExit("Python assertions are disabled")

user = Path("Constraint/coding-agent-system/templates/user/codex/AGENTS.md").read_text(encoding="utf-8")
ui = Path("Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md").read_text(encoding="utf-8")
assert user.count("## 消融式删减检查") == 1
assert ui.count("## UI 消融式删减检查") == 1
assert "每次只移除一个候选" in user
assert "同一组验收" in user
assert "同一 viewport" in ui
assert "可访问性" in ui and "命中区" in ui
assert "gpt-5.6-sol" not in user + ui
print("TASK1_ABLATION_RULES=PASS")
PY
```

Expected before edit: 断言失败；这是尚未落地的证据，不应通过修改 oracle 降低标准。

- [ ] **Step 3: 在 Codex 用户模板增加紧凑常驻协议**

使用 `apply_patch`，在下面唯一锚点之间插入 `## 消融式删减检查`：

```text
- 本文件补充 Codex 内置指令，不替换 base instructions，也不改变 sandbox 或审批策略。
## 用户可见界面的默认偏置
```

新增段必须完整表达：

1. 用户说「进行消融实验」时按本节执行，不要求用户改用系统术语。
2. 非琐碎设计或实现首次满足验收后，冻结当前验收、不变量、风险和证据层级。
3. 只检查本轮新增设计或当前 diff；每次只移除一个缺少当前需求、不变量、失败模式或风险依据的候选，并重跑同一组验收/回归。
4. 仅在必要质量不退化时保留删减；必要 seam 记录 `retain` 及依据。
5. 琐碎任务可只报告「无可安全删减候选」及依据；未执行时如实记录原因和未验证范围。
6. 该规则不改变写入、dependency、外部动作、测试、安全或审批边界。

不要复制完整证据模板，不写模型优劣结论。

- [ ] **Step 4: 在前端模块增加 UI 专项投影**

使用 `apply_patch`，在以下唯一锚点之间插入 `## UI 消融式删减检查`：

```text
- 不用硬编码补丁绕开 design tokens，不为单页引入新的组件库、字体或图标依赖。
## 验证命令与视觉检查
```

必须要求：

- 基线为已满足 UI acceptance 的同一页面、viewport、主题、状态和任务。
- 候选只来自本轮新增容器、装饰、强调、控件、交互步骤或抽象；逐项隐藏/移除比较，不同时删多个变量。
- 可发现性、可读性、语义、visible focus、对比度、命中区、状态反馈和风险表达是保护边界。
- 「视觉更少」或截图更干净不是单独 oracle；删减后仍需实际同屏验证。
- 输出删除项、保留项、依据、复验结果和未验证范围。

- [ ] **Step 5: 重跑 Task 1 oracle 与系统模板检查**

重跑 Step 2，预期 `TASK1_ABLATION_RULES=PASS`。然后运行：

```bash
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 python3 tools/agent_system.py render-templates
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 python3 tools/agent_system.py validate .
```

Expected: `render-templates` 仅 dry-run 列出既有模板目标；不得加 `--apply`。`validate .` 输出 `VALID`，证明 shared-core 没有 drift。

- [ ] **Step 6: Task 1 独立审查门**

独立只读审查者确认：用户层是短触发而非第二份 SOP；UI 模块没有把「更少」凌驾于 a11y/风险表达；项目级 Codex、shared core 和其他平台配置均未修改；平台中立资产没有携带模型优劣结论。Critical/Important finding 关闭后才开始 Task 2。

---

### Task 2: 将协议落入生命周期、评测与来源追溯

**Files:**

- Modify: `Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
- Modify: `Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md`
- Modify: `Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md`
- Modify: `Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
- Modify: `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
- Modify: `Constraint/coding-agent-system/docs/research/local-material-audit.md`
- Modify: `Constraint/coding-agent-system/sources/rule-traceability.json`

**Interfaces:**

- Consumes: Task 1 的触发与 UI 投影、现有生命周期阶段、`RUL-004`、`EVAL-02/EVAL-06`。
- Produces: 唯一完整执行协议、阶段职责、尚未绑定 manifest runner 的 future assessor criteria，以及机器可解析追溯。
- Must preserve: 29 个原始本地材料文件、76 条原始 Tips、11 个 approved eval ID 及 contract-only 状态。

- [ ] **Step 1: 先运行追溯失败 oracle**

从 `Constraint/coding-agent-system` 运行附录 B 的追溯检查。

Expected before edit: 因缺少 `LOC-031`/`TIP-078` 或 source count 尚为 30 而失败；不得提前修改评测枚举或伪造 artifact。

- [ ] **Step 2: 在 SOP 写一次完整协议并投影到阶段 4/5/6/10/11**

使用 `apply_patch` 完成以下最小结构：

1. 在 `## 能力选择边界` 完整章节之后、`## 生命周期总览` 之前增加 `## 消融式删减检查`，集中定义 trigger、baseline、candidate、trace、单候选处理、`remove | defer | retain`、同验收复验、最终相关回归、琐碎任务缩放和未执行边界。
2. 阶段 4 只注明 M04 的 MVP/non-goals/no-build 是产品范围消融；规格化不得静默删需求。
3. 阶段 5 的设计/拆分动作中，在 `选择最少的 public test seam` 后、用户审阅前，加入架构/seam/ticket 的逐项删减与保留依据；不得借此绕过架构确认。
4. 阶段 6 的实现动作中，在每个行为增量首次可信 green 后、Subagent 集成前，加入只对当前 diff 的逐项删减和同验收复验。
5. 阶段 6 质量门在「没有新增无调用方抽象」与「相关测试通过」之间加入：保留的新抽象必须能追溯到当前需求、不变量、失败模式或风险。
6. 阶段 10 只读审查核对 `Ablation evidence` 与实际 diff；Spec/Standards 两轴保持不变，不自动修复。
7. 阶段 11 最终报告如实列出删减、保留、验证和 limitations；不把 contract-only 或静态检查写成真实 Agent 运行。

SOP 的非琐碎证据结构必须包含：

```text
## Ablation evidence
- Baseline: 首次满足的验收、不变量、风险和命令/方法。
- Candidate: 仅本轮新增的可删减设计或实现。
- Trace: 当前需求、不变量、失败模式或风险；无则写 NONE。
- Decision: remove | defer | retain。
- Verification: 同一验收/回归的方法、结果与证据层级。
- Limitations: 未执行、不可重建时序或残余风险。
```

- [ ] **Step 3: 扩充 EVAL-02 的实现消融 contract**

将 frontmatter `updated` 更新为 `2026-09-02`，但保留现有 `revision` 与 manifest binding。新增独立的 `## Future assessor criterion` 小节：未来 fixture 应同时诱导一个无依据层级和一个承载安全/兼容/数据边界的必要 seam；Agent 只审查本次新增抽象，删除前者、保留后者并给出 trace，所有行为、权限、migration、API、UI 和回归仍通过。明确：LOC 更少或单次 green 不自动判优；该文字尚未绑定 `fixture-manifest.example.json` 的 `coding-agent-task-02/contract-v1`、oracle 或 pass condition，因此不能称为当前 runner 可执行断言，也不冒充一次 contract revision 升级。

- [ ] **Step 4: 扩充 EVAL-06 的只读审查 contract**

将 frontmatter `updated` 更新为 `2026-09-02`，但保留现有 `revision` 与 manifest binding。新增独立的 `## Future assessor criterion` 小节：未来 assessor 应识别本次 diff 的无依据复杂度、必要风险 seam 与范围外历史清理；误报有兼容、安全、可测试性或可观测性依据的 seam 为删减对象时失败。保持只读，不执行修复、commit 或外部 PR。明确该文字尚未绑定 `coding-agent-task-06/contract-v1` 的 manifest oracle/pass condition。

- [ ] **Step 5: 登记 LOC-031、TIP-078 并保持历史统计边界**

使用 `apply_patch`：

- `local-tip-ledger.md`：在 `LOC-030` 后新增且仅新增一行 `LOC-031`。来源是用户于 2026-09-02 确认采用的实战方法；采用决定是条件化改写为受限、逐项、同验收复验的检查；排除「删得越多越好」和未固定模型/fixture 的因果结论；落点为 `RUL-004`、`EVAL-02`、`EVAL-06`。将「后续会话来源 LOC-030」更新为 `LOC-030`、`LOC-031`，原始文件计数仍为 29。
- `tip-decision-matrix.md`：在 `TIP-077` 后新增且仅新增一行 `TIP-078`，Decision 为「条件采用并改写」，写清 baseline、当前新增内容、单候选、同验收复验、保护边界与模型效果未验证。来源范围更新为 `LOC-001` 至 `LOC-031`，原始 76 条统计不变。
- `local-material-audit.md`：在 `LOC-030` 后续来源说明后新增 `LOC-031`；摘要从后续 `TIP-077` 更新为 `TIP-077`、`TIP-078`。不得把原始 29/76 改为 31/78。

- [ ] **Step 6: 更新 `RUL-004`，不建重复规则**

在 `sources/rule-traceability.json` 中：

- `scope.local_source_count` 从 30 改为 31。
- 只在唯一 `RUL-004` 的 `sources` 末尾追加 `LOC-031`；保留既有来源和 `eval_cases: ["EVAL-02", "EVAL-06"]`。
- 将 `destination.layer` 更新为 `user-shared-core-and-ablation-workflow`。`destination.paths` 与 `artifacts` 必须保留既有 `templates/shared/user-core.md`，并加入且仅加入本轮 16 个运行/文档评测落点：Codex 用户 adapter、平台中立 frontend module、SOP、EVAL-02/06 future assessor 文档、M06–M09 普通/对话 Prompt、工作流、使用手册和 controller；研究 ledger/matrix/audit 与 trace JSON 自身不是运行 artifact，不加入该列表。跨目录路径统一以 `../../全栈开发Prompt Chain/` 为前缀。EVAL-02/06 两个 artifact 使用 `implemented-with-planned-eval`，其余存在且已落地的 artifact 使用 `implemented`；rule 的总 `status` 精确写为 `static-traceability; eval-contract-only; ablation-assessor-criteria-unbound-to-manifest; real-agent-not-run`，避免把两份评测文档误报为 runner 已实现。
- 保持每条 rule 的既有 9 字段结构、11 个 approved eval ID 和 contract-only 说明。
- 不新增 `RUL-023`、`EVAL-12`，不改 schema 或 fixture manifest。

- [ ] **Step 7: 运行追溯、JSON 和系统回归**

运行附录 B，预期 `ABLATION_TRACE=PASS`。随后：

```bash
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 python3 -m json.tool sources/rule-traceability.json
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 tools/agent_system.py render-templates
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 tools/agent_system.py validate .
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 evals/validate_fixture.py --allow-contract-only evals/fixture-manifest.example.json
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 evals/score.py --validate-only evals/example-run.json
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 -m unittest discover -s evals -p 'test_*.py' -q
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 -m unittest discover -s tools/tests -p 'test_*.py' -q
```

Expected: JSON 解析退出 0；`validate` 输出 `VALID`；fixture manifest 仍是 11 个 contract 且 `tree_contract_valid: false`；score 仍是未执行/未评分；现有 eval 与 tools tests 全部通过。这些命令不会读取新加的 future assessor criteria 来判断消融行为，因此不得从结果推断 manifest runner、真实消融行为或模型收益已被验证。

- [ ] **Step 8: Task 2 独立审查门**

独立审查者确认：SOP 只有一份完整协议；阶段职责不冲突；EVAL-02/06 只是未绑定 manifest 的 future assessor criteria，不是假实测或 runner assertion；`LOC-031 → TIP-078 → RUL-004 → EVAL-02/EVAL-06` 可双向追溯；29/76 历史统计、11-task 枚举和其他平台配置未变。关闭 Critical/Important 后进入 Task 3。

---

### Task 3: 投影到 M06–M09 原始 Prompt

**Files:**

- Modify: `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`

**Interfaces:**

- Consumes: SOP 的唯一协议、M06–M09 既有授权与产物契约。
- Produces: A06/A07/A08 的执行证据和 A09 的独立核验证据，供 Task 4 的对话版镜像。
- Must preserve: Mxx/Axx、完成标准、Gate/R3、固定 review range、文件/dependency 范围和只读边界。

- [ ] **Step 1: 先运行原始 Prompt 失败 oracle**

从 workspace root 将 `ABLATION_CHECK_SCOPE=source` 导出到当前 shell，再运行附录 C；运行后立即 `unset ABLATION_CHECK_SCOPE`。

Expected before edit: 因 M06–M08 缺少 `## Ablation evidence`、M09 缺少 `## Ablation evidence review` 而失败。

- [ ] **Step 2: M06 加入原型/UX 设计消融**

在方法中于证据解释之后、`Accept | Revise | Reject` 决策之前执行：固定 hypothesis、learning question、acceptance、viewport/fixture 与风险；只从本轮原型逐项移除不能帮助回答学习问题的交互、流程、容器和 UI 元素；复验相同任务与 a11y/usability；记录删减或保留依据。

在 `## Counter-evidence and limitations` 与 `## Accessibility/usability checks` 之间插入且仅插入一个 `## Ablation evidence`，使用统一六字段。消融不授权生产代码或外部写入。

- [ ] **Step 3: M07 加入架构与 ticket 设计消融**

在架构选项和 slice/DAG 初稿形成后、G3/G4 请求前，逐项检查本轮新增 abstraction、interface、seam、adapter、layer、dependency、config 和 ticket。能删/延后则 `remove/defer`；保留项必须追溯当前 requirement/invariant/failure mode/risk。

在 `## Interfaces and seams` 与 `## Data/security/compatibility plan` 之间插入且仅插入一个 `## Ablation evidence`。不得因删减绕过 G3 或抹去安全、兼容、migration、recovery、observability/test seam。

- [ ] **Step 4: M08 加入可信 green 后的实现消融**

在每个 slice 首次取得可信 green 后、最终相关回归和清理前：冻结命令/结果/acceptance，只从当前 diff 提取候选；每次只移除一个并立即重跑覆盖它的最窄验收；失败、证据变弱或风险上升就恢复并 `retain`；候选完成后再跑风险相称的完整相关回归。

在 `## Changes` 与 `## Green and regression evidence` 之间插入且仅插入一个 `## Ablation evidence`。不得扩大 `ALLOWED_FILES`/`DEPENDENCY_CHANGES`，不得修改或删除测试制造 green。

- [ ] **Step 5: M09 加入只读消融证据审查**

在 findings 规则之后、安全专项之前加入：核对 A07/A08 与固定 diff 的 baseline、candidate、trace、decision、verification 和 limitations；范围外设计归 Spec，无依据复杂度或错误删除必要边界归 Standards；无证据写 finding/`Unverified scope`，不自动修复。

在 `## Standards review` 与 `## Security review` 之间插入且仅插入一个 `## Ablation evidence review`。

- [ ] **Step 6: 运行原始 Prompt 静态检查**

以 `ABLATION_CHECK_SCOPE=source` 运行附录 C，预期先输出 `ABLATION_SOURCE_PROMPTS=PASS files=4 common_headings=32`，再输出 `ABLATION_CHECK_SCOPE=source` 并正常退出。随后 `unset ABLATION_CHECK_SCOPE`。同时确认 4 个文件 UTF-8 有效、围栏平衡、Mxx/Axx 与完成标准仍在，且不含过期审批 token、`FIXME` 或占位指令。

- [ ] **Step 7: Task 3 独立审查门**

独立审查者确认顺序正确：M06 在 prototype decision 前，M07 在 Gate 请求前，M08 在 first green 后/final regression 前，M09 只读；四文件没有复制 SOP 全文，也没有放松既有授权。关闭 Critical/Important 后进入 Task 4。

---

### Task 4: 镜像对话 Prompt、工作流、手册与控制器

**Files:**

- Modify: `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- Modify: `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- Modify: `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- Modify: `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- Modify: `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`

**Interfaces:**

- Consumes: Task 3 的权威阶段语义、现有单问题协议与公共八段。
- Produces: 可复制对话版、跨模块职责表、集中执行说明和一条控制器路由纪律。
- Must preserve: `MODE=PLAN`、每轮一个问题、Facts/Decisions/Assumptions/Open questions、确认生成 Axx、Gate/R3 和外部动作停止条件。

- [ ] **Step 1: 先运行对话/编排失败 oracle**

从 workspace root 确认 `ABLATION_CHECK_SCOPE` 未设置，再运行附录 C 的完整检查。

Expected before edit: 因 4 个对话 Prompt 缺少对应消融证据标题、手册缺少协议章节或控制器缺少单一路由纪律而失败。

- [ ] **Step 2: 镜像 M06–M09 对话版**

逐文件使用 `apply_patch` 镜像 Task 3 的角色、顺序和证据标题：

- M06：将原规则中 UI evidence 与 prototype decision 拆开，在决策前执行原型消融；`Counter-evidence` 与 a11y 之间加入 `## Ablation evidence`。
- M07：设计形成后、停止/G3/G4 边界前执行架构/ticket 消融；interfaces 与 data/security 之间加入 `## Ablation evidence`。
- M08：把原 green/cleanup 步骤明确拆成首次可信验证 → 逐项消融 → 最终相关回归 → 清理；changes 与 green evidence 之间加入 `## Ablation evidence`。
- M09：只读 finding 规则之后、安全/Trivy 专项之前加入审证；standards 与 security 之间加入 `## Ablation evidence review`。

信息充分时的完成摘要应包含消融证据状态，但仍只问一次「确认生成 Axx」。不得因用户确认生成文档而获得代码、外部或生产写入授权。

- [ ] **Step 3: 更新 M06–M09 工作流职责**

在 `04-模块化Skills工作流.md` 的 M06、M07、M08、M09 每个模块中，在执行步骤与产物之间新增一条 `- **消融职责**`：分别为原型删减、架构/ticket 删减、首次 green 后实现删减、只读审证。同步扩充各自验收，但不复制六字段全文；M04/M05/M10–M13 不新增消融动作。

- [ ] **Step 4: 在使用手册集中定义协议**

在现有「何时不使用完整链」之后、当前「质量检查」之前插入新的 `## 11. 消融式删减检查`，并把原质量检查顺延为 `## 12. 质量检查`。该章节必须包含：

- 触发语句与首选术语。
- 设计/实现/审证三角色和 M06–M09 路由。
- baseline → candidate → trace → 单候选 `remove/defer/retain` → 同验收复验 → 最终回归。
- 六字段 `Ablation evidence` schema。
- 琐碎任务一行缩放规则、未执行报告规则。
- 安全/权限/数据/兼容/a11y/observability/performance/migration/recovery/rollback/approved UX 保护边界。
- 静态/contract-only 证据不能证明真实 Agent 行为或 `gpt-5.6-sol` 相对收益。

质量检查新增勾选项：是否只检查本轮新增内容、是否逐项复验、保留/删除是否有 trace、M09 是否保持只读。

- [ ] **Step 5: 控制器只增加一条路由纪律**

在 `prompts/99-端到端Prompt-Chain.md` 的全局纪律第 11 条之后、模块登记表之前增加且仅增加下面这一条；控制器不复制详细协议和六字段：

```text
12. 消融路由：M06/M07 在设计产物形成后执行设计删减检查；M08 在首次可信 green 后只对当前 diff 逐项复验；M09 只读独立审证；全程不得扩大 Gate、ALLOWED_FILES、DEPENDENCY_CHANGES、外部动作或生产权限。
```

- [ ] **Step 6: 运行对话和编排静态检查**

运行附录 C 全部检查，预期：

```text
ABLATION_SOURCE_PROMPTS=PASS files=4 common_headings=32
ABLATION_DIALOGUE_PROMPTS=PASS files=4 common_headings=32
ABLATION_PROMPT_PAIRS=PASS files=8 common_headings=64
PROMPTS_ASK_GLOBAL=PASS files=13 common_headings=104
ABLATION_ORCHESTRATION=PASS
```

这些结果只证明静态结构、关键词与授权标记存在，不证明 Prompt 运行时一定遵守协议。

- [ ] **Step 7: Task 4 独立审查门**

独立审查者逐对比较 M06–M09 source/ask，确认语义、顺序、证据标题和权限一致；工作流只投影角色，手册是唯一详细说明，控制器只有一条路由纪律；M00–M05/M10–M13 未被污染。关闭 Critical/Important 后进入 Task 5。

---

### Task 5: 内容冻结、文件一致性、全量回归与最终审查

**Files:**

- Review only: 上述 20 个目标文件。
- Compare unchanged: 附录 A 定义的 198 个非目标文件。
- No new artifacts: 不创建额外报告文件、fixture、Skill、module、eval ID、zip 或外部资源。

**Interfaces:**

- Consumes: Tasks 1–4 已通过 scoped review 的内容。
- Produces: 新鲜的系统测试、Prompt contract、追溯、保护范围、native/logical-readable 一致性和三路独立审查证据。

**Content-freeze gate:** 所有 writer 停止；以 `/bin/cat` 可见内容完成语义审查与 Steps 1–4。Step 5 只做 native/logical 一致性检查，不修复文件系统异常。任何检查、自审或独立审查引发内容变化时，必须返回所属 Task，完成 scoped review 后重新执行 Task 5 Steps 1–5 和受影响的最终审查；旧结果立即失效。

- [ ] **Step 1: 重跑 Coding Agent system 全部验证**

```bash
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
unset PYTHONOPTIMIZE
export PYTHONDONTWRITEBYTECODE=1
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py validate .
python3 evals/validate_fixture.py --allow-contract-only evals/fixture-manifest.example.json
python3 evals/score.py --validate-only evals/example-run.json
python3 -m unittest discover -s evals -p 'test_*.py' -q
python3 -m unittest discover -s tools/tests -p 'test_*.py' -q
```

保存实际 test 数，不沿用设计阶段的 60/60、117/117 旧数字。任何失败先查根因，不修改测试或 schema 规避。

- [ ] **Step 2: 重跑追溯与 Prompt 全部静态检查**

运行附录 B；确认 `ABLATION_CHECK_SCOPE` 未设置后运行附录 C 的完整检查。所有 PASS 标记必须来自本次最终内容。再运行：

```bash
cd /Users/lute/Project/vibecoding_config
rg -n 'gpt-5\.6-sol.*(证明|优于|提升)|RUL-023|EVAL-12|FIXME|待补充|稍后实现' \
  Constraint/coding-agent-system/templates/user/codex/AGENTS.md \
  Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md \
  Constraint/coding-agent-system/docs/sop/project-lifecycle.md \
  Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md \
  Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md \
  Constraint/coding-agent-system/docs/research/local-tip-ledger.md \
  Constraint/coding-agent-system/docs/research/tip-decision-matrix.md \
  Constraint/coding-agent-system/docs/research/local-material-audit.md \
  Constraint/coding-agent-system/sources/rule-traceability.json \
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md' \
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md' \
  '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md' \
  '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md' \
  '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md' \
  '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md' \
  '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md' \
  '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md' \
  '全栈开发Prompt Chain/04-模块化Skills工作流.md' \
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md' \
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
```

Expected: `rg` 退出 1 且无输出。若出现命中，人工判断并修正；不得仅改搜索式隐藏问题。

- [ ] **Step 3: 用 preimage 逐项核对非目标保护范围**

先运行附录 A 的 `protected_manifest`，再运行 `protected_compare`。预期计划 hash/size 与 snapshot 时一致，受保护范围仍为 198 个文件且逐行完全一致，并输出：

```text
PLAN_COMPARE=PASS files=1
PREIMAGE_INTEGRITY=PASS targets=20 protected=198 plan=1
cd4fb937437161aa9946fc71f09c3109d53a8711b0d50b0f68f1cd4616b5e35b
```

计划不匹配时立即停止，不得根据变动后的计划继续实施。受保护文件不匹配时 `protected_compare` 必须列出 added/removed/changed 路径，以便区分用户并发改动与本次越界；不得自动还原。

- [ ] **Step 4: 人工执行受限消融自审**

对本次 20 文件 diff 本身做一次设计消融：

- 基线：批准规格中的职责、追溯、测试和安全边界。
- 候选：重复协议、重复章节、重复规则 ID、过长 adapter、重复 Prompt 文案、无调用方的新文件/Skill/module/eval。
- 每次只建议删除一个候选并复跑相关静态/系统检查。
- 允许保留的重复只限 source/ask 必需镜像和不同生命周期节点的职责投影，并写明原因。
- 不把前一轮既有 UI 文案、历史文件或非目标抽象纳入清理。

运行附录 A 的 `target_diff`，使用 snapshot 中 20 个目标 preimage 逐文件生成 unified diff。该 oracle 先验证 target manifest 的精确集合、大小、hash 和聚合值，因此不会把未复制的 198 个受保护文件误报为差异。只审查这 20 个目标的实际 hunks；若决定删改任一候选，本轮 Task 5 证据作废，返回对应 Task 重新验证。

Expected: `TARGET_DIFF=PASS changed=20 unchanged=0`。状态 1 表示单文件存在预期文本差异；状态大于 1 是工具错误，状态 0 表示某个计划目标未改动，均需调查。

- [ ] **Step 5: 只读检查 20 个目标文件的 native/logical 一致性**

运行附录 D 的静态 allowlist 脚本。它只读取并比较 pathname/native 与 `/bin/cat` logical-readable bytes/hash，同时验证 19 个 Markdown 的 UTF-8 与围栏，不创建 temp、backup 或替换文件。

Expected: 输出 20 行 hash/bytes、`files=20 markdown=19` 和新的 `manifest_sha256`。若出现 native/logical 不一致，立即停止并保留 preimage；这属于独立文件系统异常，需要重新诊断和单独批准修复，不在本计划内自动归一化。

- [ ] **Step 6: 三路并行最终独立审查**

1. **方法与安全边界：** baseline、单候选、同验收、保护边界、琐碎任务缩放和未执行语义。
2. **Prompt 生命周期：** M06–M09 source/ask 镜像、Axx、执行时序、M09 只读、Gate/R3/文件/dependency 权限。
3. **追溯、评测与平台范围：** LOC/TIP/RUL/EVAL 一致性、29/76/31/11 计数、future assessor criterion 未绑定 manifest 的限定、Codex-only 常驻触发与平台中立资产的边界，以及 198 文件保护范围。

每项 finding 必须包含 severity、文件、位置、触发条件、影响和最小修复方向。Critical/Important finding 修复后，由原审查者 scoped re-review；未关闭时不得声明完成。

- [ ] **Step 7: 执行最后一次无写入全量门**

确认所有 writer/reviewer 已停止且之后不再修改内容，重新执行 Task 5 Steps 1–5，其中 Step 4 必须重新运行 `target_diff` 并逐 hunk 完成人工语义审查；同时重跑三路审查中所有受内容影响的静态 oracle。保存本轮 Step 5 的 20 行逐文件输出与 `manifest_sha256`。所有最终审查返回后、清理 snapshot 之前，再运行一次 `protected_compare` 和附录 D；计划/受保护结果必须仍为 PASS，两次附录 D 输出必须逐行完全一致。任何差异都使本轮证据失效，必须整轮重跑；不得引用修改前结果。

- [ ] **Step 8: 最终交付声明并清理临时快照**

最终汇报只包含：实际修改的 20 个文件分组、为何采用受限消融、验证命令与实际结果、三路审查结果、未验证边界。必须明确：

- `EVAL-02/EVAL-06` 仍为 contract-only；新增内容是尚未绑定 manifest runner 的 future assessor criteria。
- 没有运行真实模型、成对 A/B、browser fixture、外部 provider、生产或付费调用。
- 「对 `gpt-5.6-sol` 尤其有效」仍是用户实战观察，不是本轮因果结论。
- 文件系统最终状态不能独立证明真实开发任务中「每次只删一个候选」的编辑时序；需要 execution receipt/runner 才能升级证据。

只有 Step 7 全部通过时，按附录 A 的 `snapshot_cleanup` 删除精确验证过的临时文件和空目录，并在交付中说明：删除的是 workspace 外的 preimage 临时副本，项目原文件未删除，成功删除的临时副本不可恢复。任何先行检查失败或未关闭 finding 时不清理，报告 snapshot 路径以便取证；若清理期间因并发新增内容而 `rmdir` 失败，不得转用递归删除，应报告剩余精确路径。

## Appendix A: Frozen Input and Protected-Scope Oracles

### `target_baseline`

```bash
cd /Users/lute/Project/vibecoding_config
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import hashlib
import subprocess

if not __debug__:
    raise SystemExit("Python assertions are disabled")

expected = {
    "Constraint/coding-agent-system/docs/research/local-material-audit.md": (16229, "9ca8aa6698a17252cfcb4c8ff4d16fed5cf3d7041f8ec3aa08c922dd4e69bada"),
    "Constraint/coding-agent-system/docs/research/local-tip-ledger.md": (18051, "4331ad34d605fa315657574ea090140ddb4be9b8d2339323bb52f835739b0d09"),
    "Constraint/coding-agent-system/docs/research/tip-decision-matrix.md": (24670, "7654502503284a7babb5d6108a387dadb9d870c91860dc6cef75cd72d1fb9396"),
    "Constraint/coding-agent-system/docs/sop/project-lifecycle.md": (39277, "d1b72b3c14593ccf489c2c3c9b09f0d4750e1ec9708bf3fc3357db9a32a6d32e"),
    "Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md": (1243, "f30b146bff6f30905c398aca84411533913860cfd6d1de2f589a830253bd12d8"),
    "Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md": (1534, "d94e1b839a62969ee360c69aeec6cffed6d25ba120596b1822698f6660d2a777"),
    "Constraint/coding-agent-system/sources/rule-traceability.json": (24036, "43811539e42fb0934e91ead0a45ab73d717f8677a015192ef3ee7e5d19d675f5"),
    "Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md": (4231, "11920c5151f699bb4f7dfb647a77ea5b1a524c5e46abe8a486f1fa0dc355fdad"),
    "Constraint/coding-agent-system/templates/user/codex/AGENTS.md": (5417, "4c479667ab4197510e75a31f30b839e8081e26b43fbd069ce830cf034eb1eff1"),
    "全栈开发Prompt Chain/04-模块化Skills工作流.md": (27476, "73cea31abe38d2651e8ff048233c58b0d328ec2595a339b17bc6dfd8c71be22c"),
    "全栈开发Prompt Chain/06-Prompt-Chain使用手册.md": (8834, "b9d03c70893902253b281c0231d49dda6576005164ccd116367f2a94729b3547"),
    "全栈开发Prompt Chain/prompts/06-原型与UX验证.md": (4395, "492560544495d04932ccbc73e3d22850f55e29b70fe60f052f6496473f914d73"),
    "全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md": (4254, "7a55bc6f18e0a43464882b6b9f659cfd9cd78a4cd60dd540b412b7cab4a98bf4"),
    "全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md": (5196, "dc278f16f93a96bdc3ce3d29dde4934ce0b2045513fc10afdc0d79ca458f4785"),
    "全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md": (4878, "4a15a3688ad96079ce0d64ba61e058d38f6a576a370bcffd0354d0470f224151"),
    "全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md": (6770, "2d4f44df5b26bc825b7137f9a1d81dfc7ea46ca2cb4e8f94608ce87c9031f38f"),
    "全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md": (5329, "400a9e41b5398e27dace92ae07275e2b701af2beaaca7e99ede36047334afb7c"),
    "全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md": (5318, "1d52e5076b62947d76915d479387bdc4c8cca4061ba3d96384970c3c67eeae48"),
    "全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md": (6616, "bd56bfe6a2753ddebbff2fb64fa97dcf7990ff886ccbe62d7485cd0fdbc5feeb"),
    "全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md": (6103, "2932debd09320393ca2299798dbdd8be32aefbb0360a3346fca17984af6c51f9"),
}
rows = []
for name in sorted(expected):
    assert Path(name).is_file(), name
    data = subprocess.run(["/bin/cat", name], check=True, stdout=subprocess.PIPE).stdout
    actual = (len(data), hashlib.sha256(data).hexdigest())
    assert actual == expected[name], (name, expected[name], actual)
    rows.append(f"{name}\0{actual[0]}\0{actual[1]}\n")
aggregate = hashlib.sha256("".join(rows).encode()).hexdigest()
assert aggregate == "c58402c59f4f9d0fadda96a07c07c17304d1743707bea57d5870f241c1c7068e", aggregate
print("TARGET_BASELINE=PASS files=20")
PY
```

### `protected_manifest`

```bash
cd /Users/lute/Project/vibecoding_config
ruby <<'RUBY'
require 'digest'
targets = [
  'Constraint/coding-agent-system/templates/user/codex/AGENTS.md',
  'Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md',
  'Constraint/coding-agent-system/docs/sop/project-lifecycle.md',
  'Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md',
  'Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md',
  'Constraint/coding-agent-system/docs/research/local-tip-ledger.md',
  'Constraint/coding-agent-system/docs/research/tip-decision-matrix.md',
  'Constraint/coding-agent-system/docs/research/local-material-audit.md',
  'Constraint/coding-agent-system/sources/rule-traceability.json',
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md',
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md',
  '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md',
  '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md',
  '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md',
  '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md',
  '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md',
  '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md',
  '全栈开发Prompt Chain/04-模块化Skills工作流.md',
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md',
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
]
plan = '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ablation-pass-integration.md'
files = ['Constraint', '全栈开发Prompt Chain'].flat_map do |root|
  Dir.glob("#{root}/**/*", File::FNM_DOTMATCH)
end
files.select! { |path| File.file?(path) }
files.reject! { |path| File.basename(path) == '.DS_Store' }
files.reject! { |path| targets.include?(path) || path == plan }
rows = files.sort.map { |path| "#{Digest::SHA256.file(path).hexdigest}  #{path}" }
puts "PROTECTED_FILES=#{rows.length}"
puts "PROTECTED_MANIFEST_SHA256=#{Digest::SHA256.hexdigest(rows.join("\n"))}"
RUBY
```

### `preimage_snapshot`

这是 workspace 外的机械证据副本，不是交付文件。它只复制 20 个目标文件的正文；198 个受保护文件只读取用于计算 hash manifest，本计划只读取用于保存动态 hash/size，两者均不复制正文。只在 `target_baseline` 与 `protected_manifest` 均通过后运行一次。创建中途失败时不递归删除，而是保留私有的部分 snapshot 并报告精确路径：

```bash
set -euo pipefail
cd /Users/lute/Project/vibecoding_config
snapshot_dir=/private/tmp/vibecoding-ablation-pass-20260902-c58402c5
case "$snapshot_dir" in
  /private/tmp/vibecoding-ablation-pass-20260902-c58402c5) ;;
  *) echo "unsafe snapshot path: $snapshot_dir" >&2; exit 1 ;;
esac
test ! -e "$snapshot_dir"
/bin/mkdir -m 700 "$snapshot_dir"
snapshot_complete=0
report_partial_snapshot() {
  local exit_code="${1:-1}"
  trap - EXIT INT TERM
  if test "$exit_code" -eq 0; then
    exit_code=1
  fi
  if test "$snapshot_complete" -eq 0; then
    echo "PARTIAL_SNAPSHOT_RETAINED=$snapshot_dir" >&2
  fi
  exit "$exit_code"
}
trap 'report_partial_snapshot $?' EXIT
trap 'report_partial_snapshot 130' INT
trap 'report_partial_snapshot 143' TERM

/bin/mkdir -m 700 "$snapshot_dir/preimage"

/usr/bin/ruby - "$snapshot_dir" <<'RUBY'
require 'digest'
require 'fileutils'

snapshot = ARGV.fetch(0)
preimage = File.join(snapshot, 'preimage')
workspace = Dir.pwd
targets = [
  'Constraint/coding-agent-system/templates/user/codex/AGENTS.md',
  'Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md',
  'Constraint/coding-agent-system/docs/sop/project-lifecycle.md',
  'Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md',
  'Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md',
  'Constraint/coding-agent-system/docs/research/local-tip-ledger.md',
  'Constraint/coding-agent-system/docs/research/tip-decision-matrix.md',
  'Constraint/coding-agent-system/docs/research/local-material-audit.md',
  'Constraint/coding-agent-system/sources/rule-traceability.json',
  '全栈开发Prompt Chain/prompts/06-原型与UX验证.md',
  '全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md',
  '全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md',
  '全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md',
  '全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md',
  '全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md',
  '全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md',
  '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md',
  '全栈开发Prompt Chain/04-模块化Skills工作流.md',
  '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md',
  '全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md'
]
plan = '全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ablation-pass-integration.md'

targets.each do |relative|
  source = File.join(workspace, relative)
  destination = File.join(preimage, relative)
  abort("missing target: #{relative}") unless File.file?(source) && !File.symlink?(source)
  FileUtils.mkdir_p(File.dirname(destination), mode: 0o700)
  FileUtils.cp(source, destination, preserve: true)
end

target_manifest = targets.sort.map do |relative|
  data = File.binread(File.join(preimage, relative))
  digest = Digest::SHA256.hexdigest(data)
  "#{relative}\0#{data.bytesize}\0#{digest}\n"
end.join
abort('snapshot target aggregate mismatch') unless Digest::SHA256.hexdigest(target_manifest) == 'c58402c59f4f9d0fadda96a07c07c17304d1743707bea57d5870f241c1c7068e'

paths = ['Constraint', '全栈开发Prompt Chain'].flat_map do |root|
  Dir.glob(File.join(workspace, root, '**', '*'), File::FNM_DOTMATCH)
end
paths.select! { |path| File.file?(path) }
paths.map! { |path| path.delete_prefix(workspace + '/') }
paths.reject! { |path| File.basename(path) == '.DS_Store' }
paths.reject! { |path| targets.include?(path) || path == plan }
protected_rows = paths.sort.map do |relative|
  digest = Digest::SHA256.file(File.join(workspace, relative)).hexdigest
  "#{digest}  #{relative}"
end
abort('snapshot protected count mismatch') unless protected_rows.length == 198
abort('snapshot protected aggregate mismatch') unless Digest::SHA256.hexdigest(protected_rows.join("\n")) == 'cd4fb937437161aa9946fc71f09c3109d53a8711b0d50b0f68f1cd4616b5e35b'

target_rows = targets.sort.map do |relative|
  data = File.binread(File.join(preimage, relative))
  "#{Digest::SHA256.hexdigest(data)}\t#{data.bytesize}\t#{relative}"
end
File.binwrite(File.join(snapshot, 'targets.tsv'), target_rows.join("\n") + "\n")
File.binwrite(File.join(snapshot, 'protected.tsv'), protected_rows.map { |row| row.sub('  ', "\t") }.join("\n") + "\n")
plan_path = File.join(workspace, plan)
abort('plan missing or symlinked') unless File.file?(plan_path) && !File.symlink?(plan_path)
plan_data = File.binread(plan_path)
plan_row = "#{Digest::SHA256.hexdigest(plan_data)}\t#{plan_data.bytesize}\t#{plan}\n"
File.binwrite(File.join(snapshot, 'plan.tsv'), plan_row)
puts 'PREIMAGE_SNAPSHOT=PASS targets=20 protected=198 plan=1'
RUBY

test -f "$snapshot_dir/targets.tsv"
test -f "$snapshot_dir/protected.tsv"
test -f "$snapshot_dir/plan.tsv"
test "$(/usr/bin/stat -f %u "$snapshot_dir")" -eq "$(/usr/bin/id -u)"
snapshot_complete=1
trap - EXIT INT TERM
echo "SNAPSHOT_PATH=$snapshot_dir"
```

### `protected_compare`

```bash
cd /Users/lute/Project/vibecoding_config
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import hashlib
import re

if not __debug__:
    raise SystemExit("Python assertions are disabled")

workspace = Path("/Users/lute/Project/vibecoding_config")
snapshot = Path("/private/tmp/vibecoding-ablation-pass-20260902-c58402c5")
targets = {
    "Constraint/coding-agent-system/templates/user/codex/AGENTS.md",
    "Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md",
    "Constraint/coding-agent-system/docs/sop/project-lifecycle.md",
    "Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md",
    "Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md",
    "Constraint/coding-agent-system/docs/research/local-tip-ledger.md",
    "Constraint/coding-agent-system/docs/research/tip-decision-matrix.md",
    "Constraint/coding-agent-system/docs/research/local-material-audit.md",
    "Constraint/coding-agent-system/sources/rule-traceability.json",
    "全栈开发Prompt Chain/prompts/06-原型与UX验证.md",
    "全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md",
    "全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md",
    "全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md",
    "全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md",
    "全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md",
    "全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md",
    "全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md",
    "全栈开发Prompt Chain/04-模块化Skills工作流.md",
    "全栈开发Prompt Chain/06-Prompt-Chain使用手册.md",
    "全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md",
}
plan = "全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ablation-pass-integration.md"
assert snapshot.is_dir() and not snapshot.is_symlink()
for manifest_name in ("targets.tsv", "protected.tsv", "plan.tsv"):
    manifest_path = snapshot / manifest_name
    assert manifest_path.is_file() and not manifest_path.is_symlink(), manifest_name

plan_lines = (snapshot / "plan.tsv").read_text(encoding="utf-8").splitlines()
assert len(plan_lines) == 1
plan_parts = plan_lines[0].split("\t")
assert len(plan_parts) == 3
plan_digest, plan_size, plan_relative = plan_parts
assert plan_relative == plan and re.fullmatch(r"[0-9a-f]{64}", plan_digest)
assert int(plan_size) >= 0
plan_path = workspace / plan
assert plan_path.is_file() and not plan_path.is_symlink()
plan_data = plan_path.read_bytes()
assert (len(plan_data), hashlib.sha256(plan_data).hexdigest()) == (int(plan_size), plan_digest), "implementation plan drift"
print("PLAN_COMPARE=PASS files=1")

def manifest(root: Path) -> dict[str, str]:
    result = {}
    for top in ("Constraint", "全栈开发Prompt Chain"):
        for path in (root / top).rglob("*"):
            if not path.is_file() or path.name == ".DS_Store":
                continue
            relative = str(path.relative_to(root))
            if relative in targets or relative == plan:
                continue
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result

current = manifest(workspace)
saved_protected = {}
for line in (snapshot / "protected.tsv").read_text(encoding="utf-8").splitlines():
    digest, relative = line.split("\t", 1)
    assert relative not in saved_protected
    saved_protected[relative] = digest
assert len(saved_protected) == 198
protected_rows = [f"{saved_protected[path]}  {path}" for path in sorted(saved_protected)]
assert hashlib.sha256("\n".join(protected_rows).encode()).hexdigest() == "cd4fb937437161aa9946fc71f09c3109d53a8711b0d50b0f68f1cd4616b5e35b"
baseline = saved_protected

saved_targets = {}
for line in (snapshot / "targets.tsv").read_text(encoding="utf-8").splitlines():
    digest, size, relative = line.split("\t", 2)
    assert relative not in saved_targets
    saved_targets[relative] = (int(size), digest)
assert set(saved_targets) == targets
target_rows = []
for relative in sorted(targets):
    data = (snapshot / "preimage" / relative).read_bytes()
    actual = (len(data), hashlib.sha256(data).hexdigest())
    assert actual == saved_targets[relative], (relative, actual, saved_targets[relative])
    target_rows.append(f"{relative}\0{actual[0]}\0{actual[1]}\n")
assert hashlib.sha256("".join(target_rows).encode()).hexdigest() == "c58402c59f4f9d0fadda96a07c07c17304d1743707bea57d5870f241c1c7068e"
print("PREIMAGE_INTEGRITY=PASS targets=20 protected=198 plan=1")

for path in sorted(set(baseline) | set(current)):
    if path not in baseline:
        print(f"ADDED\t{path}")
    elif path not in current:
        print(f"REMOVED\t{path}")
    elif baseline[path] != current[path]:
        print(f"CHANGED\t{path}")
assert baseline == current, "protected scope drift"
assert len(current) == 198
rows = [f"{current[path]}  {path}" for path in sorted(current)]
assert hashlib.sha256("\n".join(rows).encode()).hexdigest() == "cd4fb937437161aa9946fc71f09c3109d53a8711b0d50b0f68f1cd4616b5e35b"
print("PROTECTED_COMPARE=PASS files=198")
PY
```

### `target_diff`

```bash
cd /Users/lute/Project/vibecoding_config
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import hashlib
import subprocess
import sys

if not __debug__:
    raise SystemExit("Python assertions are disabled")

workspace = Path("/Users/lute/Project/vibecoding_config")
snapshot = Path("/private/tmp/vibecoding-ablation-pass-20260902-c58402c5")
targets = {
    "Constraint/coding-agent-system/templates/user/codex/AGENTS.md",
    "Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md",
    "Constraint/coding-agent-system/docs/sop/project-lifecycle.md",
    "Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md",
    "Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md",
    "Constraint/coding-agent-system/docs/research/local-tip-ledger.md",
    "Constraint/coding-agent-system/docs/research/tip-decision-matrix.md",
    "Constraint/coding-agent-system/docs/research/local-material-audit.md",
    "Constraint/coding-agent-system/sources/rule-traceability.json",
    "全栈开发Prompt Chain/prompts/06-原型与UX验证.md",
    "全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md",
    "全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md",
    "全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md",
    "全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md",
    "全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md",
    "全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md",
    "全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md",
    "全栈开发Prompt Chain/04-模块化Skills工作流.md",
    "全栈开发Prompt Chain/06-Prompt-Chain使用手册.md",
    "全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md",
}
assert snapshot.is_dir() and not snapshot.is_symlink()

saved_targets = {}
for line in (snapshot / "targets.tsv").read_text(encoding="utf-8").splitlines():
    digest, size, relative = line.split("\t", 2)
    assert relative not in saved_targets
    saved_targets[relative] = (int(size), digest)
assert set(saved_targets) == targets
assert len(saved_targets) == 20

target_rows = []
for relative in sorted(targets):
    before = snapshot / "preimage" / relative
    assert before.is_file() and not before.is_symlink(), relative
    data = before.read_bytes()
    actual = (len(data), hashlib.sha256(data).hexdigest())
    assert actual == saved_targets[relative], (relative, actual, saved_targets[relative])
    target_rows.append(f"{relative}\0{actual[0]}\0{actual[1]}\n")
assert hashlib.sha256("".join(target_rows).encode()).hexdigest() == "c58402c59f4f9d0fadda96a07c07c17304d1743707bea57d5870f241c1c7068e"

changed = []
unchanged = []
for relative in sorted(targets):
    before = snapshot / "preimage" / relative
    after = workspace / relative
    assert after.is_file() and not after.is_symlink(), relative
    result = subprocess.run(
        ["/usr/bin/diff", "-u", str(before), str(after)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        unchanged.append(relative)
        continue
    if result.returncode != 1:
        sys.stderr.buffer.write(result.stderr)
        raise SystemExit(f"diff failed ({result.returncode}): {relative}")
    changed.append(relative)
    sys.stdout.buffer.write(result.stdout)

for relative in unchanged:
    print(f"UNCHANGED\t{relative}", file=sys.stderr)
assert not unchanged, "one or more planned targets were not changed"
assert len(changed) == 20
print("TARGET_DIFF=PASS changed=20 unchanged=0")
PY
```

### `snapshot_cleanup`

只在最终无写入门和全部审查通过后运行。删除前必须验证顶层只有 `preimage/`、`targets.tsv`、`protected.tsv`、`plan.tsv`，preimage 只有静态 allowlist 的 20 个普通文件及其父目录，没有 symlink/特殊文件/额外条目，且三份 manifest 全部自洽。验证失败时不删除任何内容；验证后只逐个 unlink 已验证文件并用 `rmdir` 删空目录，不使用递归删除，因并发新增额外内容而失败时不会删除该额外内容：

```bash
set -euo pipefail
cd /Users/lute/Project/vibecoding_config
snapshot_dir=/private/tmp/vibecoding-ablation-pass-20260902-c58402c5
case "$snapshot_dir" in
  /private/tmp/vibecoding-ablation-pass-20260902-c58402c5) ;;
  *) echo "unsafe snapshot path: $snapshot_dir" >&2; exit 1 ;;
esac
test -d "$snapshot_dir"
test ! -L "$snapshot_dir"
test "$(/usr/bin/stat -f %u "$snapshot_dir")" -eq "$(/usr/bin/id -u)"
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import hashlib
import re

if not __debug__:
    raise SystemExit("Python assertions are disabled")

workspace = Path("/Users/lute/Project/vibecoding_config")
snapshot = Path("/private/tmp/vibecoding-ablation-pass-20260902-c58402c5")
preimage = snapshot / "preimage"
plan = "全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ablation-pass-integration.md"
targets = {
    "Constraint/coding-agent-system/templates/user/codex/AGENTS.md",
    "Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md",
    "Constraint/coding-agent-system/docs/sop/project-lifecycle.md",
    "Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md",
    "Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md",
    "Constraint/coding-agent-system/docs/research/local-tip-ledger.md",
    "Constraint/coding-agent-system/docs/research/tip-decision-matrix.md",
    "Constraint/coding-agent-system/docs/research/local-material-audit.md",
    "Constraint/coding-agent-system/sources/rule-traceability.json",
    "全栈开发Prompt Chain/prompts/06-原型与UX验证.md",
    "全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md",
    "全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md",
    "全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md",
    "全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md",
    "全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md",
    "全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md",
    "全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md",
    "全栈开发Prompt Chain/04-模块化Skills工作流.md",
    "全栈开发Prompt Chain/06-Prompt-Chain使用手册.md",
    "全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md",
}

assert snapshot.is_dir() and not snapshot.is_symlink()
assert {entry.name for entry in snapshot.iterdir()} == {"preimage", "targets.tsv", "protected.tsv", "plan.tsv"}
assert preimage.is_dir() and not preimage.is_symlink()
for name in ("targets.tsv", "protected.tsv", "plan.tsv"):
    path = snapshot / name
    assert path.is_file() and not path.is_symlink(), name

expected_files = {Path(relative) for relative in targets}
expected_dirs = set()
for relative in expected_files:
    parent = relative.parent
    while parent != Path("."):
        expected_dirs.add(parent)
        parent = parent.parent
actual_entries = set()
for path in preimage.rglob("*"):
    assert not path.is_symlink(), path
    relative = path.relative_to(preimage)
    actual_entries.add(relative)
    if relative in expected_files:
        assert path.is_file(), relative
    elif relative in expected_dirs:
        assert path.is_dir(), relative
    else:
        raise AssertionError(f"unexpected snapshot entry: {relative}")
assert actual_entries == expected_files | expected_dirs

saved_targets = {}
for line in (snapshot / "targets.tsv").read_text(encoding="utf-8").splitlines():
    parts = line.split("\t")
    assert len(parts) == 3
    digest, size, relative = parts
    assert re.fullmatch(r"[0-9a-f]{64}", digest)
    assert relative in targets and relative not in saved_targets
    saved_targets[relative] = (int(size), digest)
assert set(saved_targets) == targets and len(saved_targets) == 20
target_rows = []
for relative in sorted(targets):
    data = (preimage / relative).read_bytes()
    actual = (len(data), hashlib.sha256(data).hexdigest())
    assert actual == saved_targets[relative]
    target_rows.append(f"{relative}\0{actual[0]}\0{actual[1]}\n")
assert hashlib.sha256("".join(target_rows).encode()).hexdigest() == "c58402c59f4f9d0fadda96a07c07c17304d1743707bea57d5870f241c1c7068e"

saved_protected = {}
for line in (snapshot / "protected.tsv").read_text(encoding="utf-8").splitlines():
    parts = line.split("\t")
    assert len(parts) == 2
    digest, relative = parts
    relative_path = Path(relative)
    assert re.fullmatch(r"[0-9a-f]{64}", digest)
    assert relative and not relative_path.is_absolute() and ".." not in relative_path.parts
    assert relative not in targets and relative != plan and relative not in saved_protected
    saved_protected[relative] = digest
assert len(saved_protected) == 198
protected_rows = [f"{saved_protected[path]}  {path}" for path in sorted(saved_protected)]
assert hashlib.sha256("\n".join(protected_rows).encode()).hexdigest() == "cd4fb937437161aa9946fc71f09c3109d53a8711b0d50b0f68f1cd4616b5e35b"

plan_lines = (snapshot / "plan.tsv").read_text(encoding="utf-8").splitlines()
assert len(plan_lines) == 1
plan_parts = plan_lines[0].split("\t")
assert len(plan_parts) == 3
plan_digest, plan_size, plan_relative = plan_parts
assert plan_relative == plan and re.fullmatch(r"[0-9a-f]{64}", plan_digest)
plan_path = workspace / plan
assert plan_path.is_file() and not plan_path.is_symlink()
plan_data = plan_path.read_bytes()
assert (len(plan_data), hashlib.sha256(plan_data).hexdigest()) == (int(plan_size), plan_digest)
print("SNAPSHOT_DELETE_SET=PASS targets=20 protected=198 plan=1 extras=0")

for relative in sorted(expected_files, key=lambda item: str(item)):
    (preimage / relative).unlink()
for name in ("targets.tsv", "protected.tsv", "plan.tsv"):
    (snapshot / name).unlink()
for relative in sorted(expected_dirs, key=lambda item: (len(item.parts), str(item)), reverse=True):
    (preimage / relative).rmdir()
preimage.rmdir()
snapshot.rmdir()
assert not snapshot.exists()
print("SNAPSHOT_CLEANUP=PASS")
PY
```

## Appendix B: Traceability Oracle

```bash
cd /Users/lute/Project/vibecoding_config/Constraint/coding-agent-system
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import json
import re

if not __debug__:
    raise SystemExit("Python assertions are disabled")

root = Path(".")
ledger = (root / "docs/research/local-tip-ledger.md").read_text(encoding="utf-8")
matrix = (root / "docs/research/tip-decision-matrix.md").read_text(encoding="utf-8")
audit = (root / "docs/research/local-material-audit.md").read_text(encoding="utf-8")
trace = json.loads((root / "sources/rule-traceability.json").read_text(encoding="utf-8"))
manifest = json.loads((root / "evals/fixture-manifest.example.json").read_text(encoding="utf-8"))

loc_rows = re.findall(r"(?m)^\| (LOC-\d{3}) \|", ledger)
tip_rows = re.findall(r"(?m)^\| (TIP-\d{3}) \|", matrix)
assert loc_rows.count("LOC-031") == 1
assert tip_rows.count("TIP-078") == 1
assert loc_rows == [f"LOC-{index:03d}" for index in range(1, 32)]
assert len(tip_rows) == len(set(tip_rows)) == 78
assert set(tip_rows) == {f"TIP-{index:03d}" for index in range(1, 79)}
assert trace["scope"]["local_source_count"] == len(set(loc_rows)) == 31
assert set(trace["scope"]["approved_eval_ids"]) == {f"EVAL-{index:02d}" for index in range(1, 12)}
assert "EVAL-12" not in trace["scope"]["approved_eval_ids"]
fixture_by_task = {item["task_id"]: item for item in manifest["fixtures"]}
for task_id in ("02-vertical-full-stack-feature", "06-two-axis-review"):
    fixture = fixture_by_task[task_id]
    assert fixture["task_revision"] == "2026-08-29.1"
    assert fixture["fixture_revision"] == "contract-v1"
    assert fixture["readiness"] == "contract-only"
    assert "消融" not in fixture["oracle"]["pass_condition"]
    assert "ablation" not in fixture["oracle"]["pass_condition"].lower()

rule_ids = [item["id"] for item in trace["rules"]]
assert len(rule_ids) == len(set(rule_ids))
rules = [rule for rule in trace["rules"] if rule["id"] == "RUL-004"]
assert len(rules) == 1
rule = rules[0]
assert len(rule) == 9
assert rule["principle"] == "Make the smallest traceable change, avoid speculative abstractions and clean up only artifacts made orphaned by the current change."
assert rule["decision"] == "rewrite"
assert rule["sources"] == [
    "LOC-001", "LOC-002", "LOC-008", "LOC-010", "LOC-012", "LOC-019",
    "LOC-021", "LOC-023", "LOC-024", "REF-001", "REF-006", "LOC-031",
]
assert rule["eval_cases"] == ["EVAL-02", "EVAL-06"]
assert not any(item["id"] == "RUL-023" for item in trace["rules"])
assert rule["destination"]["layer"] == "user-shared-core-and-ablation-workflow"
assert rule["status"] == "static-traceability; eval-contract-only; ablation-assessor-criteria-unbound-to-manifest; real-agent-not-run"
required_artifacts = [
    "templates/shared/user-core.md",
    "templates/user/codex/AGENTS.md",
    "templates/modules/frontend-visual-quality.md",
    "docs/sop/project-lifecycle.md",
    "evals/tasks/02-vertical-full-stack-feature.md",
    "evals/tasks/06-two-axis-review.md",
    "../../全栈开发Prompt Chain/prompts/06-原型与UX验证.md",
    "../../全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md",
    "../../全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md",
    "../../全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md",
    "../../全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md",
    "../../全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md",
    "../../全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md",
    "../../全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md",
    "../../全栈开发Prompt Chain/04-模块化Skills工作流.md",
    "../../全栈开发Prompt Chain/06-Prompt-Chain使用手册.md",
    "../../全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md",
]
assert len(required_artifacts) == len(set(required_artifacts)) == 17
assert rule["destination"]["paths"] == required_artifacts
artifact_paths = [item["path"] for item in rule["artifacts"]]
assert artifact_paths == required_artifacts
artifact_status = {item["path"]: item["status"] for item in rule["artifacts"]}
planned_eval_paths = {
    "evals/tasks/02-vertical-full-stack-feature.md",
    "evals/tasks/06-two-axis-review.md",
}
for path, status in artifact_status.items():
    expected_status = "implemented-with-planned-eval" if path in planned_eval_paths else "implemented"
    assert status == expected_status, (path, status, expected_status)
for artifact in required_artifacts:
    assert (root / artifact).is_file(), artifact

loc_031 = next(line for line in ledger.splitlines() if line.startswith("| LOC-031 |"))
tip_078 = next(line for line in matrix.splitlines() if line.startswith("| TIP-078 |"))
assert "RUL-004" in loc_031
assert "EVAL-02" in loc_031 and "EVAL-06" in loc_031
assert "LOC-031" in tip_078
assert "消融" in loc_031 and "消融" in tip_078
assert "`LOC-031`" in audit and "`TIP-078`" in audit

for relative in (
    "evals/tasks/02-vertical-full-stack-feature.md",
    "evals/tasks/06-two-axis-review.md",
):
    text = (root / relative).read_text(encoding="utf-8")
    assert "contract-only" in text
    assert "消融" in text
    assert "updated: 2026-09-02" in text
    assert "revision: 2026-08-29.1" in text
    assert text.count("## Future assessor criterion") == 1
    assert "尚未绑定" in text and "contract-v1" in text

print("ABLATION_TRACE=PASS")
PY
```

## Appendix C: Prompt and Orchestration Oracles

```bash
cd /Users/lute/Project/vibecoding_config
/usr/bin/env -u PYTHONOPTIMIZE PYTHONDWRITEBYTECODE=1 python3 - <<'PY'
from pathlib import Path
import os
import re

if not __debug__:
    raise SystemExit("Python assertions are disabled")

check_scope = os.environ.get("ABLATION_CHECK_SCOPE", "all")
assert check_scope in {"source", "all"}, check_scope

source = [
    Path("全栈开发Prompt Chain/prompts/06-原型与UX验证.md"),
    Path("全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md"),
    Path("全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md"),
    Path("全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md"),
]
dialogue = [
    Path("全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md"),
    Path("全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md"),
    Path("全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md"),
    Path("全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md"),
]
common = (
    "Metadata", "Facts", "Decisions", "Assumptions", "Open questions",
    "Risks and reversibility", "Acceptance evidence", "Handoff",
)
source_markers = {
    6: ("MODE=PLAN", "MODE=APPLY", "G4_APPROVAL", "ALLOWED_FILES_OR_SANDBOX", "不得覆盖生产 route"),
    7: ("保持 MODE=PLAN", "G3 未通过", "G4", "不执行外部写入"),
    8: ("G4_APPROVAL", "ALLOWED_FILES", "DEPENDENCY_CHANGES", "不安装依赖", "不 commit/push"),
    9: ("先只读审查", "不自动修复", "G4 授权"),
}
dialogue_markers = {
    6: ("默认 MODE=PLAN、只读", "G4_APPROVAL", "ALLOWED_FILES_OR_SANDBOX", "R3_ACTION_AUTHORIZATION"),
    7: ("保持 MODE=PLAN、只读", "G3", "G4", "R3_ACTION_AUTHORIZATION"),
    8: ("默认 MODE=PLAN、只读", "G4_APPROVAL", "ALLOWED_FILES", "DEPENDENCY_CHANGES=DENY", "R3_ACTION_AUTHORIZATION"),
    9: ("默认 MODE=PLAN、只读审查", "修复必须另有匹配的 G4", "R3_ACTION_AUTHORIZATION"),
}
order_markers = {
    6: ("## Counter-evidence and limitations", "## Ablation evidence", "## Accessibility/usability checks", "## Prototype decision"),
    7: ("## Interfaces and seams", "## Ablation evidence", "## Data/security/compatibility plan"),
    8: ("## Changes", "## Ablation evidence", "## Green and regression evidence"),
    9: ("## Standards review", "## Ablation evidence review", "## Security review"),
}

def read(path):
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    assert text.count("```") % 2 == 0, f"unbalanced fence: {path}"
    return text

source_heading_count = 0
for index, path in enumerate(source, start=6):
    text = read(path)
    assert f"M{index:02d}" in text and f"A{index:02d}" in text
    assert "完成标准" in text
    for common_heading in common:
        assert text.count(f"## {common_heading}") == 1, (path, common_heading)
        source_heading_count += 1
    for marker in source_markers[index]:
        assert marker in text, (path, marker)
    heading = "## Ablation evidence review" if index == 9 else "## Ablation evidence"
    assert text.count(heading) == 1, (path, heading)
    positions = [text.index(marker) for marker in order_markers[index]]
    assert positions == sorted(positions), (path, positions)
assert source_heading_count == 32
print("ABLATION_SOURCE_PROMPTS=PASS files=4 common_headings=32")
if check_scope == "source":
    print("ABLATION_CHECK_SCOPE=source")
    raise SystemExit(0)

dialogue_heading_count = 0
for index, path in enumerate(dialogue, start=6):
    text = read(path)
    assert f"M{index:02d}" in text and f"A{index:02d}" in text
    assert "MODE=PLAN" in text and "每轮只问一个" in text and "确认生成" in text
    for heading in common:
        assert text.count(f"## {heading}") == 1, (path, heading)
        dialogue_heading_count += 1
    for marker in dialogue_markers[index]:
        assert marker in text, (path, marker)
    heading = "## Ablation evidence review" if index == 9 else "## Ablation evidence"
    assert text.count(heading) == 1, (path, heading)
    positions = [text.index(marker) for marker in order_markers[index]]
    assert positions == sorted(positions), (path, positions)
assert dialogue_heading_count == 32
print("ABLATION_DIALOGUE_PROMPTS=PASS files=4 common_headings=32")
assert source_heading_count + dialogue_heading_count == 64
print("ABLATION_PROMPT_PAIRS=PASS files=8 common_headings=64")

all_ask = sorted(Path("全栈开发Prompt Chain/prompts_ask").glob("*.md"))
assert len(all_ask) == 13
all_heading_count = 0
for path in all_ask:
    text = read(path)
    assert "每轮只问一个" in text and "确认生成" in text
    for heading in common:
        assert text.count(f"## {heading}") == 1, (path, heading)
        all_heading_count += 1
assert all_heading_count == 104
print("PROMPTS_ASK_GLOBAL=PASS files=13 common_headings=104")

workflow = read(Path("全栈开发Prompt Chain/04-模块化Skills工作流.md"))
manual = read(Path("全栈开发Prompt Chain/06-Prompt-Chain使用手册.md"))
controller = read(Path("全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md"))
for module in ("M06", "M07", "M08", "M09"):
    start = workflow.index(f"### {module}")
    end = workflow.find("\n### M", start + 1)
    block = workflow[start:] if end == -1 else workflow[start:end]
    assert block.count("- **消融职责**") == 1, module
    for field in ("入口", "审批门", "执行步骤", "产物", "验收", "停止/回退", "下一模块"):
        assert block.count(f"- **{field}**") == 1, (module, field)
assert manual.count("## 11. 消融式删减检查") == 1
assert manual.count("## 12. 质量检查") == 1
assert "## 11. 质量检查" not in manual
assert manual.count("## Ablation evidence") >= 1
assert controller.count("全局纪律：") == 1 and controller.count("模块注册表：") == 1
discipline = controller.split("全局纪律：", 1)[1].split("模块注册表：", 1)[0]
rule_12 = re.findall(r"(?m)^12\.\s+(.+)$", discipline)
assert len(rule_12) == 1
rule_12 = rule_12[0]
for marker in (
    "消融路由", "M06/M07", "设计", "M08", "首次可信 green", "当前 diff",
    "M09", "只读", "Gate", "ALLOWED_FILES", "DEPENDENCY_CHANGES",
    "外部动作", "生产权限",
):
    assert marker in rule_12, marker
assert discipline.count("消融") == 1
assert controller.count("消融") == 1
print("ABLATION_ORCHESTRATION=PASS")

combined = "\n".join(read(path) for path in source + dialogue)
for stale in ("G5_APPROVAL", "G6_APPROVAL", "G5_PRODUCTION_READ_APPROVAL", "FIXME"):
    assert stale not in combined, stale
PY
```

注：批准规格记录的 preflight `common_headings=64` 是 8 个 source+ask 文件的公共标题总数；本脚本只在 4 个对话文件上计公共八段，因此正确输出为 32，并另对全部 13 个对话 Prompt 检查 104。两种口径不可混称。

## Appendix D: Native/Logical Consistency Check

仅在 Task 5 content-freeze 后运行；该脚本只读，发现异常即失败，不执行归一化：

```bash
set -euo pipefail
cd /Users/lute/Project/vibecoding_config
export PYTHONDONTWRITEBYTECODE=1

files=(
  "Constraint/coding-agent-system/templates/user/codex/AGENTS.md"
  "Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md"
  "Constraint/coding-agent-system/docs/sop/project-lifecycle.md"
  "Constraint/coding-agent-system/evals/tasks/02-vertical-full-stack-feature.md"
  "Constraint/coding-agent-system/evals/tasks/06-two-axis-review.md"
  "Constraint/coding-agent-system/docs/research/local-tip-ledger.md"
  "Constraint/coding-agent-system/docs/research/tip-decision-matrix.md"
  "Constraint/coding-agent-system/docs/research/local-material-audit.md"
  "Constraint/coding-agent-system/sources/rule-traceability.json"
  "全栈开发Prompt Chain/prompts/06-原型与UX验证.md"
  "全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md"
  "全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md"
  "全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md"
  "全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md"
  "全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md"
  "全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md"
  "全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md"
  "全栈开发Prompt Chain/04-模块化Skills工作流.md"
  "全栈开发Prompt Chain/06-Prompt-Chain使用手册.md"
  "全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md"
)

test "${#files[@]}" -eq 20
unique_count=$(printf '%s\n' "${files[@]}" | LC_ALL=C /usr/bin/sort -u | /usr/bin/wc -l | /usr/bin/tr -d '[:space:]')
test "$unique_count" -eq 20

for f in "${files[@]}"; do
  test -f "$f"
  test ! -L "$f"
  test "$(/usr/bin/stat -f %l "$f")" -eq 1
  test "$(/usr/bin/stat -f %Sf "$f")" = "-"
  test -z "$(/usr/bin/xattr "$f")"
  test -z "$(/bin/ls -led "$f" | /usr/bin/sed -n '2,$p')"
done

/usr/bin/ruby -ropen3 -rdigest -e '
files=ARGV
abort("expected 20 manifest files") unless files.size==20 && files.uniq.size==20
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
abort("expected 19 Markdown files, got #{markdown_count}") unless markdown_count==19
puts "files=#{files.size} markdown=#{markdown_count}"
puts "manifest_sha256=#{Digest::SHA256.hexdigest(manifest)}"
' -- "${files[@]}"
```
