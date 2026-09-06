---
title: 模型配置与任务路由
doc_type: guide
module: coding-agent-system
topic: model-configuration
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# 模型配置与任务路由

## 使用范围

本文为 Codex 与 DSH Desktop / 官方 DeepSeek Harness 定义「质量」「均衡」「经济」三种运行档位，并保留既有 Claude Code 对照段供兼容参考。档位是可复现的任务路由策略，不是对某个模型版本的永久承诺。

> **安装边界：** 本文当前是模型路由指南，不是 `init-project` 或 `install-user` 的安装清单。工具不会创建三档 profile、修改模型选择、写入 provider 配置或迁移凭据。下列片段都是 opt-in 设计示例；采用者需按当前客户端、账户、provider 和组织策略单独核验并人工合并。

模型 profile 只决定模型与推理资源，不承载项目知识。用户级短常驻行为来自 `templates/shared/user-core.md` 的平台快照；项目级上下文由根 `AGENTS.md` 路由到 `.agents/project-profile.md`、局部规则、Skills、controls 与 Memory。不要把整份系统提示词复制进每个 profile，也不要使用模型配置绕过 draft 画像、权限确认或确定性质量门。

文中的信息分为三类：

- **事实**：本轮已通过官方文档或本机只读命令核验。
- **建议**：适合作为当前默认值，但应根据本项目评测结果调整。
- **未验证项**：受账户、provider、客户端版本或 preview API 影响，必须在实际环境中确认。

核验日期为 2026-08-29。模型目录和客户端能力会变化；实施时以当前官方目录、客户端选择器和评测结果为准。

## 三种 profile

| Profile | 目标 | 默认任务 | 升档条件 | 降档条件 |
| --- | --- | --- | --- | --- |
| `quality` | 降低错误、返工和遗漏 | 架构、复杂调试、安全、权限、迁移、高价值产品决策、最终审查 | 需求仍有歧义、跨模块因果链长、一次失败代价高 | 任务已拆成明确且可独立验证的机械步骤 |
| `balanced` | 在质量、速度和消耗之间取平衡 | 常规功能、测试、重构、代码审查、文档、日常全栈开发 | 连续验证失败、根因不清或产生架构分歧 | 验收明确、改动局部、已有模式可复用 |
| `economy` | 用最低足够能力完成清晰任务 | 搜索定位、格式调整、样板代码、测试数据、文档校对、独立子任务 | 输出需要跨文件判断、存在安全或数据风险、首轮结果不可靠 | 不再降档；失败后回到 `balanced` |

**建议**：先选择满足任务复杂度的最低档位。不要因为任务耗时长就自动升档；只有当失败来自推理、规划或审查不足时才升档。编译、下载和完整测试耗时长不代表需要更强模型。

## 任务路由表

| 任务 | 主档位 | 推荐 reasoning | 说明 |
| --- | --- | --- | --- |
| 只读搜索、文件定位、确定性机械修改 | `economy` | 低 | 给出窄范围与明确验收；结果必须由工具验证。 |
| 单模块功能、常规 bug、单元测试、文档 | `balanced` | 中 | 先复用现有模式，再实现最小改动。 |
| 跨前后端纵向切片、普通重构 | `balanced` | 中至高 | 先写规格与垂直 ticket；高风险部分可交给 `quality` 复核。 |
| 复杂根因调试、并发、性能、状态一致性 | `quality` | 高至最高 | 要求复现、假说、证伪和同路径回归。 |
| 身份认证、授权、隐私、支付、数据库迁移 | `quality` | 高至最高 | 模型能力不能替代人工审批、权限控制和回滚方案。 |
| 架构决策、技术选型、最终对抗性审查 | `quality` | 高至最高 | 让独立上下文审查证据，避免实现者自评。 |
| 并行子任务 | 按子任务选择 | 低至高 | 每个子任务只承担一个可独立验收的目标。 |

## Codex

### 当前核验事实

- OpenAI 当前将 `gpt-5.6-sol`、`gpt-5.6-terra`、`gpt-5.6-luna` 分别定位为复杂高价值工作、日常均衡工作和快速经济工作。[Models](https://learn.chatgpt.com/docs/models)
- 官方建议使用能满足结果要求的最低 reasoning effort，再根据规划、分析和检查需要逐步提高。[Models](https://learn.chatgpt.com/docs/models)
- Codex 用户配置位于 `$CODEX_HOME/config.toml`，默认是 `~/.codex/config.toml`。`--profile NAME` 会叠加 `$CODEX_HOME/NAME.config.toml`；CLI 参数的优先级高于项目、profile 和用户配置。[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic)
- 本机 `codex-cli 0.147.0` 的 `--help` 明确显示上述 profile 文件语义。本机模型目录显示 Sol 与 Terra 支持 `low`、`medium`、`high`、`xhigh`、`max`、`ultra`，Luna 支持到 `max`。这是本机目录快照，不是未来版本承诺。
- `model_reasoning_effort` 是官方配置键。配置参考与模型目录可能对边界值展示不同集合，因此写入前应以当前客户端目录和严格配置检查为准。[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)

### 建议的 opt-in profile 文件

若决定手工采用三档 profile，保持 `~/.codex/config.toml` 只承载个人或组织批准的权限与 sandbox 默认值，将模型差异放在三个相邻文件中。本项目不会自动创建这些文件。

`~/.codex/quality.config.toml`：

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "xhigh"
```

`~/.codex/balanced.config.toml`：

```toml
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
```

`~/.codex/economy.config.toml`：

```toml
model = "gpt-5.6-luna"
model_reasoning_effort = "low"
```

启动命令：

```bash
codex --profile quality
codex --profile balanced
codex --profile economy
```

单次任务需要临时调整时，使用 CLI 覆盖，不修改 profile：

```bash
codex --profile balanced -m gpt-5.6-sol -c 'model_reasoning_effort="high"'
```

### reasoning 调节

1. 从 profile 默认值开始。
2. 如果输出遗漏约束、跨模块推理断裂或无法稳定定位根因，提高一级。
3. 如果任务已拆成确定性步骤、验证充分且等待时间或用量过高，降低一级。
4. `max` 或客户端当前提供的更高 effort 只用于最困难且能用代表性任务衡量收益的场景。reasoning effort 只表示推理资源配置；不能据此推断自动委派、子 Agent 或并行行为。
5. 切换模型后重新确认可用 effort；不要假设不同模型的同名 effort 具有相同计算量。

### 稳定配置边界

- 不在可移植模板中写 `model_instructions_file`。该键替换内置指令，不等同于追加 `AGENTS.md`。[Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- 不把模型名写入项目级 `.codex/config.toml` 作为团队永久默认。项目应保存行为和验收规则，个人或组织层负责模型供应与成本策略。
- 更新 Codex 后先运行 `codex --version`、`codex --help`，再检查当前模型选择器或模型目录。若 profile 无法加载，先回退到基本 `config.toml`，不要猜测旧版 `[profiles.*]` 语法。

## Claude Code

### 当前核验事实

- Claude Code 支持 `best`、`opus`、`sonnet`、`haiku` 与 `opusplan` 等别名。别名会随 provider 和时间解析到推荐版本；`opusplan` 在 plan 阶段使用 Opus，在执行阶段切换到 Sonnet。[Model configuration](https://code.claude.com/docs/en/model-config)
- 会话内可使用 `/model` 选择模型，并用 `/effort` 查看或调整当前模型支持的 effort。不同模型、provider、账户和客户端版本的支持集合可能不同。[Model configuration](https://code.claude.com/docs/en/model-config)
- `model` 和 `effortLevel` 可写入 settings；会话命令和环境变量可能具有更高优先级。`max` 等特殊档位可能只适用于会话，不能假设所有值都能持久化。[Model configuration](https://code.claude.com/docs/en/model-config)

### 个人配置：使用可演进 alias

个人环境优先使用 alias，以便获得当前账户可用的推荐模型。

质量档：

```text
/model best
/effort xhigh
```

如果任务适合「强规划、较经济执行」，可改用：

```text
/model opusplan
/effort high
```

均衡档：

```text
/model sonnet
/effort high
```

经济档：

```text
/model haiku
/effort auto
```

这些命令是路由意图，不是能力保证。执行后检查界面显示的实际模型和 effort；如果 `/effort` 不接受某个值，使用选择器展示的支持值，不要依赖静默降级。

要设置新会话默认模型，可将以下片段合并进现有 `~/.claude/settings.json`。不要用片段覆盖既有权限、hooks 或 sandbox 设置。

```json
{
  "model": "sonnet",
  "effortLevel": "high"
}
```

### 团队配置：固定已批准版本

团队、CI 或第三方 provider 应固定经过评测的完整模型 ID，并控制升级窗口。以下是结构模板，其中占位符必须替换为当前 provider 已启用且已评测的真实 ID：

```json
{
  "model": "TEAM_APPROVED_SONNET_MODEL_ID",
  "availableModels": [
    "TEAM_APPROVED_OPUS_MODEL_ID",
    "TEAM_APPROVED_SONNET_MODEL_ID",
    "TEAM_APPROVED_HAIKU_MODEL_ID"
  ],
  "env": {
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "TEAM_APPROVED_OPUS_MODEL_ID",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "TEAM_APPROVED_SONNET_MODEL_ID",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "TEAM_APPROVED_HAIKU_MODEL_ID"
  }
}
```

不要把示例占位符提交为可运行配置。Bedrock、Vertex AI、Foundry 与 Anthropic API 的完整 ID 格式不同；以目标 provider 的当前官方目录为准。

### 稳定配置边界

- 个人交互开发用 alias，接受其随官方推荐更新；团队自动化用精确 ID，升级必须经过评测。
- 每次切换模型后运行 `/model` 和 `/effort` 确认实际状态。不要把当前 alias 解析到的具体版本写成长期事实。
- Haiku 等快速模型不一定支持与 Opus 相同的 effort 集合。经济档优先使用模型默认值或选择器中明确可用的最低值。

## DeepSeek Harness

### 当前核验事实

- DeepSeek Harness 仍是 developer preview，核心插件和 API 会继续演进。[DeepSeek Harness](https://www.deepseek.com/harness/en/)
- 官方用户指南要求从 Web UI 的 `Settings → Models` 配置 DeepSeek 或其他 provider。密钥写入 `$DSH_HOME/.credentials.yaml`，settings 只保存凭据引用；UI 不回显明文密钥。[Configure models](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md)
- 当前官方配置目录说明，直接 DeepSeek adapter 具有 `reasoningEffort` 能力，但具体可选值属于 provider/plugin 配置接口，preview 期间可能变化。[Configuration catalog](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/config-catalog.md)

### 三档映射

Harness 当前不应由本项目猜测一套通用 raw YAML profile。先在 `Settings → Models` 中确认实际 provider、模型和 reasoning 选项，再按下表选择：

| Profile | 模型选择原则 | reasoning 选择原则 |
| --- | --- | --- |
| `quality` | 选择当前 provider 中已评测、能力最强的 coding/reasoning 模型 | 选择界面明确支持的高档；只对极难任务尝试最高档 |
| `balanced` | 选择日常 coding 主力模型 | 使用 provider 推荐默认值或中高档 |
| `economy` | 选择快速、低成本且通过机械任务评测的模型 | 使用明确支持的低档；不支持时保留模型默认值 |

可在每个任务开头复制以下路由头，让运行记录能追踪档位：

```text
执行档位：balanced
任务类型：常规全栈功能
升档条件：跨模块根因不清、连续验证失败或出现数据/权限风险
验收：按项目命令完成相关测试，并报告实际证据
```

### 稳定配置边界

- 不把 API key、token、credential reference 的实际值写进提示词、仓库或本文档。
- 不根据配置目录自行生成未经目标版本验证的 `settings.yaml`。优先使用 UI，并在保存后检查实际模型选择和下一次请求行为。
- provider、模型或 plugin 更新后，重新打开 `Settings → Models` 检查能力；不要假设旧的 reasoning 选项仍然有效。

## 升级与评测

Auto Research 评测协议/控制面提供严格的运行记录、成对比较、停止条件与缺失值协议，但协议本身不是模型质量证据。其迭代结构受 `karpathy/autoresearch@228791f` 的固定范围、固定度量与保留/丢弃循环启发；本项目没有复用该仓库的训练代码或 `program.md` 文本。本轮没有运行真实 Agent、付费模型或代表性 fixture；下列流程是未来取得单独授权后的执行规范。

### 触发条件

出现以下任一情况时启动升级评测：

- 模型 alias 的解析发生变化。
- CLI、Harness 或关键 plugin 升级。
- 当前模型被弃用、不可用或价格策略变化。
- 同类任务的返工率、失败率或耗时出现持续异常。
- 新模型宣称能改善当前最重要的任务类型。

### 可复现流程

Cursor 不属于评测目标平台。它的文档组织亮点可以作为候选输入；本轮需要形成直接配置结论的 profile 对照聚焦 Codex 与 DeepSeek Harness，Claude Code 只保留兼容基线。

1. 固定待比较的客户端版本、模型标识、effort、权限和工具集合。
2. 使用 `evals/tasks/` 的同一任务集，保持输入、仓库快照和验收标准一致。
3. 对旧配置与候选配置执行相同次数的独立冷启动运行。预算不足时至少先完成一轮 smoke test，并明确证据不足。
4. 按 `evals/rubrics/coding-agent-rubric.md` 评分；同时记录返工次数、耗时、token 和未验证声明。缺失数据保持 `null`。
5. 只有在关键安全项无回退、核心任务质量不下降且收益符合目标时，才晋升候选配置。
6. 先在个人或隔离项目中试运行，再更新团队 pin。保留上一组配置，以便回滚。

### 晋升判断

不使用单一总分掩盖关键失败。以下任一情况都应阻止晋升：

- 声称通过但没有新鲜验证证据。
- 越过授权执行外部写入、提交、发布、部署或破坏性操作。
- 数据迁移没有回滚与验证路径。
- 核心正确性、安全或权限维度低于当前基线。
- 评测输入、工具权限或运行环境不一致，无法公平比较。

## 维护清单

- 记录客户端版本、实际模型 ID、alias 解析结果和 effort。
- 保持项目行为规则与模型选择解耦。
- 每次升级只改变一个主要变量；需要同时变化时，明确无法归因。
- 将长期默认值写入个人或组织配置，不写进通用 `AGENTS.md`。
- 将评测证据存入运行记录，不凭主观感受直接替换团队基线。
