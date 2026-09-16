---
title: 模型能力卡校准协议
doc_type: workflow
module: coding-agent-system
topic: model-capability-card-calibration
status: stable
created: 2026-09-16
updated: 2026-09-16
owner: self
source: human+ai
---

# 模型能力卡校准协议

## 1. 当前结论

本目录只建立一层 fail-closed 的校准证据协议，不改写 `evals/` 既有
EVAL v3 runner、receipt、score 或 compare 语义。

当前仓库已经保留一次 receipt-bound 的真实 Codex connectivity smoke，但它只形成
`smoke-only` 证据，不是模型质量评测：

- Codex 已有独立 `test-double` 路径，可在纯本地跑通 EVAL-10、receipt、oracle、输出
  guard 与 summary；它只生成 `calibration-test-double-observation-v1`，不能生成或冒充
  `smoke-observation-v2`；
- `smoke-observation-v2` 只接受 receipt-bound 的真实 Codex 证据图，并要求可重验的
  batch、manifest、fixture、prompt、adapter、control、安全策略、安装快照、授权 grant、
  一次性消费记录、provider invocation sidecar、receipt、artifact 和 summary；
- Codex 与 Claude Code 的通用 `platform-invocations.json` 仍是 `execute=false` 的零请求计划；
- DeepSeek Harness / DSH Desktop 因本机没有 PATH 上可复现、可固定版本的公开
  `dsh` CLI 而保持 `blocked`；Desktop 应用内 bundle 不得冒充公开调用接口；
- `codex-eval10-real-smoke-2026-09-16-once-01` 在匹配风险边界的一次性 grant 下完成：
  harness retries 为 0，oracle 与 output guard 为 `pass`，一次性消费 marker 已写入；
  provider wire request 数、实际 endpoint、usage、成本、publisher/provider/model identity 与
  `resolved_model` 仍为 `unknown/null`；
- Codex 卡为 `smoke-only`，Claude Code 与 DeepSeek Harness 卡仍为 `unobserved`；不存在
  质量比较、winner、ranking、默认路由、production-ready 或 promotion 结论。

## 2. 文件与验证边界

| 文件 | 职责 |
|---|---|
| `calibration-batch.schema.json` | 声明 batch、执行配置、固定控制、授权、预算、停止条件与调用计划的结构契约 |
| `capability-card.schema.json` | 声明 capability card 的证据状态，以及 provider、derived、billed、unknown 的边界 |
| `smoke-observation.schema.json` | 声明 connectivity smoke 的专用观察格式；不含任何质量分数或 `0` 分占位 |
| `smoke-summary.schema.json` | 声明无 winner、ranking、promotion、quality score 的机械 summary |
| `installation-identity.schema.json` | 声明 Codex npm/native 目录形状与本地 digest 身份；真实证据还必须打开 retained snapshot 重验，但它不认证 package publisher 或 provider/model 身份 |
| `authorization-grant.schema.json` | 声明一次性、exact allow/deny、未知 wire request 与无可验证账单上限的授权边界 |
| `codex-eval10-authorized-smoke-2026-09-16.json` | 已消费的一次性真实 smoke batch；只允许一个 Codex EVAL-10 connectivity invocation |
| `codex-eval10-authorization-grant-2026-09-16.json` | 与用户授权、batch digest 和本机 installation identity 绑定的一次性 grant；不是可重放授权 |
| `platform-invocations.json` | 当前机器上 Codex、Claude 与 DSH 的零请求计划；不是可直接执行的脚本 |
| `validate_calibration.py` | runtime fail-closed validator；补充 JSON Schema 难以表达的一对一引用、唯一变量和参数位置约束 |
| `test_calibration_contract.py` | validator 的正例、反例与 dry-run 安全回归测试 |
| `test_capability_card_evidence.py` | evidence-root、digest 与 summary/receipt/observation 交叉绑定回归测试 |

Schema 和 runtime validator 是互补约束。任何消费者不得只看 schema 通过就执行；真实
运行还必须通过 runtime validator、显式外发授权边界检查和 receipt/oracle 完整性检查；
实际 endpoint 与 provider wire request 数仍保持 `unknown`。

## 3. 实验单位：Execution Configuration

能力证据归属于完整执行栈，而不是只归属于模型名：

```text
platform + harness + client_version + requested_model + resolved_model
+ model_resolution_status + reasoning + profile + permissions_digest
+ toolset_digest + adapter_revision
```

模型身份必须拆开记录：

- `requested_model` 是传给客户端的请求值；
- `resolved_model` 只容纳 provider 实际返回/确认的模型 ID，未观察到就必须为 `null`；
- `model_resolution_status=client-catalog-alias` 表示客户端目录确认了请求 alias，但 provider
  实际 ID 未被观察。该状态允许 `receipt-bound`，但不得把 alias 回填到 `resolved_model`；
- `declared-unbound` 与 `blocked` 的两类模型字段都必须为 `null`，状态为
  `not-observed`。

`binding_state` 的含义：

- `declared-unbound`：只声明调用形状；模型或控制 digest 未绑定；不能运行。
- `control-bound`：配置已绑定，但还没有真实 receipt；不能生成观察型能力卡。
- `receipt-bound`：真实运行 receipt 与配置完全绑定；当前只允许进入 `smoke-only`。
  `provisionally-calibrated` 还要求 batch 逐 cell 预注册 run 与 task shape，v1 batch
  尚未表达这一契约，因此 validator 暂时 fail closed。
- `blocked`：调用接口或必要控制不可用；必须有 blocker，未解决字段保持 `null`。

模型 alias 未解析、权限/toolset digest 不完整或版本发生漂移时，必须停止；不得静默回退
或把旧证据迁移到新配置。

## 4. Batch contract

每个 batch 必须预先冻结：

1. fixture manifest、任务、初始状态、prompt 与 oracle 的绑定；
2. 唯一 treatment：`none` 或一个明确的 `single-variable`；
3. 工作区、prompt 来源、工具、浏览器、MCP、外部副作用、git writes、重试、证据产物等
   固定控制；
4. CLI invocation 数、provider request 的已知/未知状态、任务数、重复次数与整个
   lifecycle wall clock；built-in Codex 路径没有可验证 billed-cost cap，故金额必须为
   `null`、来源为 `unknown`，一次 CLI invocation 也不得被表述为一次 provider wire request；
5. 授权状态、平台、动作、引用和有效期；
6. 每个 execution configuration 恰好一条 invocation；
7. 所有 stop condition 均为 `stop-no-retry`，失败 cell 不得从结果中删除。

`dry-run-only` 额外强制：零请求、零 runtime、无 data egress、无执行、无平台授权。
所有授权状态都要求 `authorized_actions` 与 `forbidden_actions` 不相交；
`authorized-once / authorized-batch` 必须显式授权 `model-request`，非执行状态必须显式
禁止它。Codex real smoke 还会在消费一次性授权前要求 exact 五项 allow
（model request、Codex client transport、synthetic prompt egress、本地证据写入、一次性
消费 registry 写入）与 exact 九项 deny（retry、web、browser、MCP、agent tool、credential
content inspection、用户配置写、Git 写、外部副作用），不能只凭 authorization state 放行。
grant 必须绑定 batch digest 和安装身份，且有效期必须覆盖剩余完整 lifecycle；adapter 会在
模型子进程前再次检查 grant digest 与剩余 client timeout。消费 registry 以 batch digest
作为唯一键，同一 authorized-once batch 不能通过更换 nonce、grant ID 或安装重复消费。
任何真实 smoke 或 batch 都必须写入一个新的、已绑定且经明确授权的 batch 文件；不得就地
把本目录的 dry-run 计划改成可执行状态后直接运行。

若已授权计划在实际客户端调用前的 preflight 失败，使用
`authorization.state=blocked-after-preflight`：全部 invocation 必须进入 `blocked`、
`execute=false`、CLI invocation 为 `0`，并保留 blocker。它是终态证据，不是可以静默
重试或继续调用 provider 的授权状态。
仅在授权未消费时才会写 `preflight-report.json`。一旦 batch-keyed marker 已成功
消费，任何后续异常都必须改写 `execution-failure-report.json`，显式记录 phase、
`authorization_consumed`、`model_execution_may_have_started` 与 sidecar 中可观察的子进程状态；
不得把消费后失败回写为“调用前停止”。

## 5. 平台调用计划

### 5.1 Codex CLI

调用计划固定只读 sandbox、`never` approval、显式工作目录、模型与 reasoning。Codex 的
global options 必须放在 `exec` 之前，exec-local options 必须放在 `exec` 之后：

```text
codex --ask-for-approval never --sandbox read-only
      --model <requested-model>
      --config model_reasoning_effort="<reasoning-effort>"
      --config project_doc_max_bytes=0
      --config web_search="disabled"
      --disable <each frozen non-provider feature>
      --strict-config
      exec --ephemeral --ignore-user-config --ignore-rules
      --skip-git-repo-check --cd <isolated-read-only-fixture-root>
      --color never --json
      --output-last-message <artifact-root>/decision-log.md -
```

完整禁用列表以 `platform-invocations.json` 与 adapter 常量为准，并由 runtime validator
逐 token 比对；不得用省略号形式直接执行。`--sandbox read-only` 限制文件写入，不等价于
网络 deny。当前 harness 只能诚实声明 `codex-client-network-endpoints-unverified`，不能证明
网络只到 provider；built-in provider 内部 wire retry 与实际 request 数也无法可靠归零或
计数，必须保持 `unknown/null`。认证文件只会复制到临时 `0600` auth-only `CODEX_HOME`，
不使用 symlink；复制前后复核源文件 identity/digest，父进程的 `HOME`、评测目录和其他
配置不得继承给 Codex 子进程。

真实路径只接受 PATH 解析到、且符合 `@openai/codex` 预期 npm metadata 形状的
package，并核对 package、entrypoint、当前 OS/CPU native package 与唯一 native binary 的
本地 digest。这些检查不是签名或 provenance 证明；`codex-package-publisher-authenticity`
与 `provider-and-model-identity-authentication` 始终列入未验证范围。最小安装文件会被
复制到 evidence root 的 `installation-artifacts/package/`，后续的唯一 model-bearing
invocation 直接执行这个 digest-bound native snapshot；回溯 validator 会重新打开
snapshot，而不是相信 identity JSON 自报。

当前真实路径 **仅支持 macOS**：运行前必须自检 `/usr/bin/sandbox-exec` 的
`deny process-fork` 策略，adapter 在独立外层 lifecycle process group 内执行，model-bearing
client 必须加入同一外层组而不得再建可逃离的 nested session，且由 runner
持有并回收 `0700` 临时 session root 及其 `0600` auth copy。通用 lifecycle runner 的
POSIX process-group timeout 只是当前组内的失败回收，不能阻止一个恶意子进程
`setsid`逃逸，因而不单独构成真实运行的 containment 证明。其他平台在提供并
验证等价边界前 fail closed。

### 5.2 Claude Code

调用计划使用 non-interactive `--print`、`--bare`、无 session persistence、无 Chrome、
`dontAsk`、只读工具白名单、显式预算/模型/effort，并从 stdin 读取 fixture：

```text
claude --print --bare --output-format json --input-format text
       --no-session-persistence --no-chrome --permission-mode dontAsk
       --tools Read,Glob,Grep --max-budget-usd <authorized-max-usd>
       --model <requested-model> --effort <reasoning-effort>
```

这些 CLI flags 也不构成完整网络隔离；真实运行必须由外部边界补足。

### 5.3 DeepSeek Harness / DSH Desktop

当前状态为 `blocked`：本机仅验证到 Desktop 应用与其 bundle 元数据，没有 PATH 上可供
校准使用的公开、版本固定 `dsh` CLI。协议明确保持：

```text
executable = null
argv = null
expected_cli_invocations = 0
expected_provider_requests = 0 | null
```

只有公开 CLI 安装、版本固定、headless profile、权限/toolset digest、网络边界和 receipt
接口全部可验证后，才可新建计划；禁止直接调用应用内部 `app.asar` 路径。

## 6. Capability card 证据状态

| 状态 | 最低证据 | 允许表达 | 禁止表达 |
|---|---|---|---|
| `unobserved` | 无真实运行 | 未观察、阻塞原因 | usage、成本、能力或质量结论 |
| `smoke-only` | receipt-bound 的单次真实 smoke | 启动/完成/失败等观察事实 | calibrated、winner、默认路由 |
| `provisionally-calibrated` | **协议保留、当前 HOLD**；需未来 batch schema 逐 cell 预注册至少 2 runs / 2 task shapes | 当前不允许生成 | 以自报计数代替预注册 cell、泛化为模型品牌排名或生产保证 |
| `expired` | claim-free tombstone 与失效原因 | 仅表示旧证据已经失效 | 携带旧 task shape、outcome、usage/cost、参与当前路由或 promotion |

所有卡片的 `decision` 固定为 `routing=undecided`，其余决策字段为 `null`。路由决策属于更
高层、经人工审核的控制面，不由一张能力卡自我声明。
`state_reason` 也不是逃逸通道；它不再接受自由叙事，而是必须由
`evidence_state + outcome_summary` exact 派生的受控 reason code。`blockers`、
`execution_configuration.blocker` 和 `expired_reason` 也只接受明确 allowlist code，
因此不能通过换同义句绕过结构化 decision。

`batch_binding` 必须记录 `planned / retained / observed` 的 runs 与 task shapes；单次 smoke
还要求 `planned_runs` 等于 batch 中预注册的 CLI invocation 数。v1 batch 没有逐 cell 的
task-shape 计划，故即使三组自报计数相等也不能进入 `provisionally-calibrated`。
`outcome_summary` 分开记录 `completed / failed / stopped` 与 stop reason 计数；
`unobserved` 卡片的 outcome 必须为 `null`。

每个真实 smoke 使用 `smoke-observation-v2`，只记录 connectivity scope、完整 execution
configuration、结构化 outcome、summary/receipt 引用及 usage/cost 证据层。该对象故意没有
`scores`、`quality_score`、`penalty` 或 `final_score`，因此不能用 `0` 分伪装为未评分。
summary 同样使用 exact 字段集，不能注入 winner、ranking、promotion 或质量分。

观察型卡片不能只通过 JSON 结构校验。必须提供 `--evidence-root`，validator 会真实打开：

1. capability card 引用的 observation；
2. observation 引用的 summary 与完整 lifecycle receipt；
3. observation 的 manifest、fixture tree、prompt、canonical adapter、configuration tree、
   exact control policy、retained installation snapshot 与 artifact tree；
4. observation 与 capability card 共同引用的 batch、authorization grant 与 batch-keyed
   consumption marker；
5. artifact tree 内的 `codex-provider-invocation-v2` sidecar、output guard 与 oracle。

所有路径必须为 evidence root 内无 symlink 的安全相对路径，文件/tree digest 必须与当前
内容一致。validator 会调用完整 receipt 与 artifact binding 校验，并要求 batch ID/digest
同时出现在 receipt-bound configuration tree 的 `control.json` 中，并重新计算 permission/
toolset policy digest；summary、receipt、observation、batch 的 task、configuration、fixture/
oracle revision、完整 adapter argv 与 outcome 也必须相互一致。伪路径、synthetic client、
三字段伪 receipt、同配置但不同 batch、伪 digest 或跨文件不一致均 fail closed。SHA-256 只证明当前
本地 bundle 的一致性，不认证创建者，也不能抵抗可同时重写全部文件的攻击者。
当前 v2 real contract 还 exact 要求 retained installation platform 为 `darwin`，以匹配
macOS-only containment revision；Linux/Windows package 即使重算全部 digest，也不能搭配自报的
macOS sidecar 通过。control reference 也必须 exact 指向 configuration root 下的
`control.json`，不接受同目录改名替代。
真实 sidecar 还必须把 grant 消费、invocation 开始/结束与 grant expiry 绑定为
`consumed_at <= started_at <= finished_at <= expires_at`，并绑定声明、digest-bound 且经本地
self-test 的 macOS containment template/profile digest 与 wrapper/child outcome。若 output guard 失败，validator 会打开
quarantine，验证 exact 文件/目录集、逐文件 digest、无 symlink 和 owner-only 权限；不接受
空树或自报 digest 代替原件。
该 receipt 的 `lifecycle_duration_seconds` 保留包括超时回收开销在内的实际 elapsed，
不截断为声明的 deadline；`lifecycle_timed_out` 与 timeout 字段用于区分 deadline 触发后
终止与清理开销造成的 elapsed overrun。

## 7. Usage 与成本的认识论边界

四个 measurement 必须分别记录，不能相互回填：

- `provider_usage=provider-receipt`：只接受 provider/客户端 receipt 直接提供的 token
  字段，并绑定安全相对路径；
- `derived_usage=derived-estimate`：必须声明推导方法，永远不是 provider receipt；
- `billed_cost=provider-billed`：只接受收费一手证据；
- `derived_cost=derived-estimate`：必须声明计算方法，不能冒充 billed；
- `unknown`：所有相关值必须为 `null`，不能用 `0`、估算值或另一证据层回填。

原始 provider body 可能包含 prompt、response、账户或敏感信息，不应默认进入仓库。
能力卡只引用经过审查、规范化、digest 绑定的证据。

## 8. 授权、预算与停止条件

真实模型调用至少需要同时满足：

- fixture 完整绑定，输入仅为本地 synthetic fixture；
- exact model、reasoning、profile、client、permissions 与 toolset 已固定；
- `authorization.state` 与 execution mode 匹配，structured grant 存在、未消费且有效期
  覆盖整个剩余 lifecycle；
- 只允许一次 model-bearing CLI invocation；本地 package metadata/digest 检查和
  containment self-test 不得启动模型客户端，harness retry 为零；provider wire request 数、实际 endpoint
  与 billed cost cap 无法验证时必须显式为 `unknown/null`，不能伪造上限；
- manifest/fixture/prompt/oracle、本地 package-shape/digest installation snapshot、canonical adapter、exact
  permissions/toolset 与完整 adapter argv 全部 digest-bound；
- macOS `sandbox-exec deny process-fork` 自检、client 加入 adapter 外层 lifecycle process group、
  deadline 时立即硬终止该组、runner-owned 临时凭据目录
  回收与 receipt v4 的 lifecycle deadline 全部通过；其他平台当前 fail closed；
- stdout/stderr、summary、
  observation、output guard、provider sidecar 与 oracle 全部保留；connectivity smoke 不生成
  quality `record.json`；
- 触发任一 stop condition 后立即停止且不自动重试。

凭证、`.env`、账户内容、PII 和 fixture 外仓库内容永远不属于允许 data egress。

## 9. 本地验证命令

以下命令只解析本地文件，不执行模型请求：

```bash
cd Constraint/coding-agent-system/evals/calibration
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_calibration_contract.py test_capability_card_evidence.py
python3 validate_calibration.py --batch platform-invocations.json
python3 validate_calibration.py --smoke-observation <observation.json> \
  --evidence-root <evidence-root>
python3 validate_calibration.py --capability-card <card.json> \
  --evidence-root <evidence-root>
python3 -m json.tool calibration-batch.schema.json >/dev/null
python3 -m json.tool capability-card.schema.json >/dev/null
python3 -m json.tool smoke-observation.schema.json >/dev/null
```

若要验证 CLI 参数归属，只能在外部 `deny network`、`deny file-write` 的 sandbox 中追加
`--help` 做 parse-only 检查；不得提供 prompt、stdin 或任何会触发模型请求的参数组合。
