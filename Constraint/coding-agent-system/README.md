---
title: 多 Coding Agent 全栈开发配置系统
doc_type: index
module: coding-agent-system
topic: overview
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# 多 Coding Agent 全栈开发配置系统

这套配置把用户级短常驻内核与项目级隐性知识路由器分开维护，再渲染平台快照。本轮可直接配置的主交付入口是 Codex 与 DSH Desktop / DeepSeek Harness；仓库保留既有 Claude Code adapter 供兼容性回归。能力层包含 15 个 Skills，其中 7 个只能显式调用；项目初始化器生成风险敏感的项目画像、Memory 候选队列、默认关闭的确定性 controls、可达的按需技术栈/文件治理模块，系统另提供 11 个评测契约。默认写入型命令只输出计划；不会修改真实用户配置、连接 MCP、调用付费模型或执行 Git/部署操作。

**模型配置当前主要是文档，不是安装产物。** `init-project` 与 `install-user` 不会安装 `quality`、`balanced`、`economy` profile，也不会写入 provider、模型 ID 或凭据。需要采用[模型配置](docs/model-configuration.md)中的示例时，必须按当前客户端和账户单独核验，并作为 opt-in 变更人工合并。

Cursor 不是目标平台，本项目不生成 Cursor rules。现有 Cursor 材料只用于吸收可迁移的亮点，例如作用域拆分、证据要求、最小 diff 和验证纪律。

## 四份可直接配置的 AGENTS.md

| 用途 | 交付文件 | 安装位置 |
| --- | --- | --- |
| Codex 用户级 | [`templates/user/codex/AGENTS.md`](templates/user/codex/AGENTS.md) | 默认 `~/.codex/AGENTS.md`；建议先用 `install-user` 在隔离 home 预览。 |
| DSH Desktop / DeepSeek Harness 用户级 | [`templates/user/deepseek-harness/AGENTS.md`](templates/user/deepseek-harness/AGENTS.md) | 默认 `$DSH_HOME/AGENTS.md`，`DSH_HOME` 默认 `~/.dsh`。 |
| Codex 项目级 | [`templates/project/codex/AGENTS.md`](templates/project/codex/AGENTS.md) | 复制为目标项目根 `AGENTS.md`。 |
| DSH Desktop / DeepSeek Harness 项目级 | [`templates/project/deepseek-harness/AGENTS.md`](templates/project/deepseek-harness/AGENTS.md) | 复制为目标项目根 `AGENTS.md`。 |

两份项目级文件是互斥发行快照，因为两个平台的真实项目入口都叫根 `AGENTS.md`。同一项目同时使用 Codex 与 DSH Desktop 时，不拼接两份文件，改用平台中立 alternate [`templates/project/AGENTS.md`](templates/project/AGENTS.md)；它不计入上表四份单平台主交付入口。外围差异由 `.codex/`、`.agents/skills/` 与 `.dsh/skills/` 承载。用户 core 只保存跨项目稳定行为；项目 core 只负责路由 `.agents/project-profile.md`、局部规则、controls 和 Memory，不复制用户级宪法。所有共享块由 canonical core 渲染，不要直接编辑共享块。

## 最快开始

以下命令从本目录执行。

先验证工具包结构：

```bash
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py validate .
python3 -m unittest discover -s tools/tests -v
```

`render-templates` 默认输出完整的渲染目标映射，不写文件，也不区分内容相同与不同；是否存在快照漂移由 `validate` 判断。修改 canonical shared core 后，先审查 dry-run 的目标范围，再执行 `render-templates --apply`、审查仓库 diff 并重新 `validate`；不要手改渲染快照的共享块。

预览一个 TypeScript / Next.js 与前端视觉质量项目。默认 dry-run 不创建文件：

```bash
python3 tools/agent_system.py init-project ../agent-project-sandbox \
  --stack typescript-nextjs \
  --stack frontend-visual-quality
```

确认计划后，在新的空目录中生成：

```bash
python3 tools/agent_system.py init-project ../agent-project-sandbox \
  --stack typescript-nextjs \
  --stack frontend-visual-quality \
  --apply

python3 tools/agent_system.py validate-generated \
  --kind project \
  --root ../agent-project-sandbox
```

新项目画像默认是 `profile_status: draft`。普通 `validate-generated` 允许 draft，便于逐步调查；draft 不会阻塞边界清晰的普通任务。进入高风险或正式 readiness gate 前，应根据仓库证据填写六个通用领域与一个局部风险领域；不适用的领域使用带受控 `Source` 的 `Not applicable`，不能伪造事实或只写 `N/A`。完成后改为 `profile_status: active`，再运行：

```bash
python3 tools/agent_system.py validate-generated \
  --kind project \
  --root ../agent-project-sandbox \
  --require-ready-profile
```

`.agents/memory/candidates.jsonl` 只保存待人工审核的候选，不能自动晋升为正式规则。`.agents/controls/change-policy.example.json` 只是示例；controls 默认关闭。只有项目维护者创建唯一实际文件 `.agents/controls/change-policy.json` 并显式接入现有 hook 或 CI 后，检查器才生效。

在隔离的模拟主目录中预览并安装一个直接目标；DSH 验证时把 `codex` 替换为 `deepseek-harness` 并使用另一个空 sandbox：

```bash
python3 tools/agent_system.py install-user \
  --target codex \
  --home ../codex-home-sandbox

python3 tools/agent_system.py install-user \
  --target codex \
  --home ../codex-home-sandbox \
  --apply

python3 tools/agent_system.py validate-generated \
  --kind user \
  --root ../codex-home-sandbox \
  --target codex
```

`init-project` 只接受不存在或为空的目标目录，并生成 `.agents/generated-manifest.json` 绑定所选 stack modules，供 `validate-generated` 检测缺失模块。`install-user --apply` 遇到将被覆盖的既有指令或 Skill 文件时，必须同时提供尚不存在的全新 `--backup-dir`；备份根不得是符号链接，也不得位于或经路径解析过程进入 `.codex`、`.claude`、`.dsh` 或 `.agents` 管理树。已有且内容不同的 `.codex/config.toml` 或 `.claude/settings.json` 属于受保护平台设置：安装器即使收到 `--backup-dir` 也不会覆盖，必须人工合并；内容完全相同时只做 no-op。安装到真实主目录前，先阅读[安装与隔离验证](docs/installation.md)并审查 dry-run 映射。

`install-user --target` 选择要安装的平台入口，不表示 Skill 根完全隔离。只要目标包含 `codex` 或 `deepseek-harness`，安装器都会同步共享 `.agents/skills/` 与七个 `.dsh/skills/` 显式调用安全 overlay；dry-run 会列出这组耦合路径。`--target all` 还会安装 Claude compatibility adapter，只在明确需要三套兼容入口时使用；它不是 Codex + DSH 的默认主路径。

## 支持范围

| 平台 | 用户级入口 | 项目级入口 | 本系统策略 |
| --- | --- | --- | --- |
| Codex | `~/.codex/AGENTS.md`、`~/.codex/config.toml` | 根 `AGENTS.md`、注释型 `.codex/config.toml`、`.agents/skills/` | 行为规则在 `AGENTS.md`；审批与 sandbox 基线留在用户或组织层，不替换内置 base instructions。 |
| Claude Code（兼容） | `~/.claude/CLAUDE.md`、`~/.claude/settings.json` | `.claude/CLAUDE.md` 导入 `@../AGENTS.md`，并使用 `.claude/skills/` | 保留用于兼容性回归，不是本轮直接交付目标。Claude 入口不放在项目根，避免初始根候选冲突。 |
| DeepSeek Harness | `~/.dsh/AGENTS.md` | 根 `AGENTS.md`、`.agents/skills/`，显式 skill 使用 `.dsh/skills/` 适配 | 行为以默认 spine 已启用 `agent-instructions` 与 skill filesystem plugins 为前提；不猜测 provider、model 或项目 settings。 |
| Cursor | 不支持 | 不生成 | 只吸收文档亮点，不作为目标平台。 |

用户级模板面向 macOS。项目生成物不写死主目录、包管理器或平台命令，适合团队提交并在 macOS、Linux 与 Windows 项目中继续定制。实际平台发现与 sandbox 行为仍应在目标环境按安装版本做 smoke test。

## 体系架构

```text
templates/shared/*                 skills/*
用户短常驻内核 / 项目画像路由器      十五个规范化能力源
          |                           |
          +------------+--------------+
                       v
              tools/agent_system.py
                 生成与安全校验
                       |
          +------------+-------------+
          v            v             v
        Codex   Claude compatibility   DeepSeek Harness
          |            |             |
          +------------+-------------+
                       v
          permissions / hooks / CI / MCP
                       |
                       v
              测试、评测与交付证据
```

常驻规则只保存每个任务都需要的稳定边界。多步骤方法进入 skill；框架和路径约束进入按需 stack module；必须确定性执行或阻止的行为进入 permissions、hook 或 CI；只有实时外部能力才使用白名单 MCP。详细判定见 [Skills 与能力层治理](docs/skills-governance.md)。

## 产物地图

| 路径 | 用途 |
| --- | --- |
| [`templates/shared/`](templates/shared/) | 用户级短常驻内核与项目级画像路由器的 canonical 单一事实源。 |
| [`templates/user/`](templates/user/) | Codex、Claude Code、DeepSeek Harness 的用户级平台模板。 |
| [`templates/project/`](templates/project/) | 从 canonical core 渲染的平台中立项目 bundle，以及 Codex / DSH Desktop 两份互斥、可直接复制的项目级快照。 |
| [`templates/modules/`](templates/modules/) | TypeScript / Next.js、Python / FastAPI、PostgreSQL migration、前端视觉质量和文件/文档治理模块。 |
| [`skills/`](skills/) | 15 个独立重写、可路由的产品研发 Skills，其中 7 个 explicit-only。 |
| [`tools/agent_system.py`](tools/agent_system.py) | `render-templates`、`init-project`、`install-user`、`validate` 与 `validate-generated` CLI。 |
| [`tools/tests/`](tools/tests/) | 初始化、覆盖保护、备份、共享块和 skill 适配测试。 |
| [`evals/`](evals/README.md) | 11 个行为契约、receipt-v2 control snapshot、逐维 assessment、`coding-agent-rubric-v3`、`score-v5` 与本地评分器。当前任务都未配 ready fixture。 |
| [`docs/research/`](docs/research/deep-research-report.md) | 官方机制对照、本地材料审计和 claim-to-source ledger。 |
| [`sources/`](sources/NOTICE.md) | 第三方 skill 与外部研究方法的固定 commit、选择决定和许可证边界。 |

## 关键安全边界

- dry-run 是 `init-project` 与 `install-user` 的默认行为；只有显式 `--apply` 才写文件。
- 项目初始化拒绝非空目标目录；用户安装只对允许覆盖的既有文件启用显式备份门。已有且不同的 Codex / Claude 平台设置文件必须人工合并，不能用备份选项绕过。单文件先流式写入同目录中性临时文件，核对实际长度与 SHA-256 并 `fsync` 后再原子移动；Darwin 使用系统 `/bin/mv`，避免当前环境对最终 `.md` 名直接写入造成的延迟 4096-byte 视图偏差。整个用户安装仍不是原子操作或全局事务；中途失败会尝试补偿回滚，回滚结果仍须核验。
- 配置工具不会遍历或解析声明清单之外的 JSON/TOML，也拒绝模板/Skill、生成画像、Memory 候选和项目自定义 Skill 中的敏感路径、secret-like 赋值、敏感映射键与非 UTF-8 指令文本；诊断只报告字段或路径，不回显命中的值。它不主动把秘密写入模板。备份允许覆盖的既有目标时会按字节复制完整文件，目标若含 token、凭据或 PII，备份也会包含这些内容。评测 runner 使用最小子进程环境，但会原样保存外部命令的 stdout/stderr；外部命令自行读取或输出的秘密可能进入 artifact bundle，因此评测必须使用隔离环境和合成凭据，并在共享前审查日志。备份与评测目录都不得同步或提交到公开仓库。
- 自然语言指令和 skill 不是权限边界。强制限制使用平台 permissions、sandbox、hook、CI 或组织策略，并在目标平台实测。
- 默认不 commit、push、merge、发布、部署、写生产数据、对外发送或运行付费调用；对应任务必须单独明确授权。
- MCP 默认关闭。启用前需要白名单、最小权限、凭据注入方式和失败恢复评审。
- 第三方 skills 固定来源版本后逐项重写；禁止整包安装和浮动分支自动更新。
- DeepSeek Harness 仍处于开发者预览阶段。模板与适配行为需要随已安装版本重新核验。

## 验证层级

| 层级 | 能证明什么 | 不能证明什么 |
| --- | --- | --- |
| 渲染与结构校验 | canonical core 可确定性渲染平台快照；快照无漂移，且必需文件、skill frontmatter、相对引用、JSON/TOML 和已知危险默认值符合本工具包约束。 | 目标 Agent 已实际加载配置。 |
| 单元测试 | dry-run、空目录生成、覆盖保护、备份、两个直接目标与 Claude 兼容 adapter 的 Skill 转换按实现工作。 | 平台升级后的真实运行兼容性。 |
| 生成物校验与隔离 smoke | `validate-generated` 检查生成项目或模拟 home 的受管文件白名单；项目 manifest 绑定所选 stack modules；隔离目录不触碰真实配置。 | 真实 sandbox、hook、MCP 或模型行为。 |
| 目标平台 smoke | 指定版本能发现规则与 skill，permissions 和 sandbox 的实际行为符合预期。 | 其他版本、其他仓库或所有任务上的普遍效果。 |
| 对照评测 | 在固定 fixture、任务、模型与权限下比较质量、返工、耗时和 token。 | 未测试模型或生产环境的绝对质量保证。 |

Auto Research 评测协议/控制面提供严格的运行记录、成对比较、停止条件和缺失值协议；其迭代方法受 `karpathy/autoresearch@228791f` 的固定范围、固定度量与保留/丢弃循环启发，但没有复用该仓库的训练代码或 `program.md` 文本。这只定义如何比较，不等于已经得到模型质量结论。本轮没有运行真实 Agent、付费模型对照或代表性 fixture。工具包不把文档推断、schema 通过或本地示例评分当作真实平台运行结果。集成完成后的实际检查与未验证项记录在[验证报告](docs/verification-report.md)。

## 文档导航

- [系统设计](docs/design.md)：已确认的架构与非目标。
- [深度研究报告](docs/research/deep-research-report.md)：Codex / DSH 官方机制、Claude 兼容差异、现有材料审计和第三方 skill 取舍。
- [本地 Tips 深度萃取审计](docs/research/local-material-audit.md)：29 个本地内容文件的逐项采用、下沉、冲突与排除矩阵。
- [Tips 原子决策矩阵](docs/research/tip-decision-matrix.md)：76 条独立经验的采用、条件采用、改写与排除原因，以及实际落点和验证状态。
- [安装与隔离验证](docs/installation.md)：用户级和项目级生成、备份及恢复。
- [项目生命周期 SOP](docs/sop/project-lifecycle.md)：从空目录、需求、开发、测试、审查到交付。
- [模型配置](docs/model-configuration.md)：质量、均衡和经济 profile 的任务路由。
- [工作流与可移植行为契约](docs/workflow.md)：全栈开发阶段、授权点与验证证据。
- [Skills 与能力层治理](docs/skills-governance.md)：15 个 Skill、7 个显式调用边界、平台适配、第三方来源、项目画像和 Memory 治理。
- [评测套件](evals/README.md)：共同任务、评分、运行记录和停止条件。
- [实施计划](docs/implementation-plan.md)：交付任务、文件接口和集成检查。
- [验证报告](docs/verification-report.md)：最终检查证据、限制和未运行项。

如果只需要研究结论，从[深度研究报告](docs/research/deep-research-report.md)开始；如果准备在空目录建立项目，从[安装与隔离验证](docs/installation.md)和[项目生命周期 SOP](docs/sop/project-lifecycle.md)开始。
