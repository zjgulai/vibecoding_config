---
title: vibecoding_config 仓库初始化与文档治理设计
status: implemented
created: 2026-09-06
updated: 2026-09-06
owner: lute
scope: repository-initialization
---

# vibecoding_config 仓库初始化与文档治理设计

## 1. 目标

将当前本地资料整理为一个可公开访问、可追溯、可持续维护的 GitHub 仓库，并将首个本地提交推送至：

`https://github.com/zjgulai/vibecoding_config`

本轮交付应做到：

- 保留现有研究、模板、Skills、工具、评测与 Prompt Chain 的内容和相对路径；
- 提供根 `README.md`，使首次访问者能理解仓库目标、两套内容的关系、主要入口、使用边界与验证方法；
- 将现有 `全栈开发Prompt Chain.zip` 移入 `archive/` 并纳入 Git；
- 排除系统垃圾文件、缓存、虚拟环境、依赖目录和本地敏感配置；
- 建立 `main` 分支、本地首个提交和名为 `origin` 的指定 GitHub 远端；
- 在推送前完成内容、链接、暂存范围、现有配置工具和 Git 对象检查。

## 2. 已确认决策

| 决策 | 结果 | 原因 |
|---|---|---|
| 目录策略 | 保路径、补入口 | 两个内容根内部已有大量相对链接；首次发布不应以美化目录为代价引入断链风险。 |
| 内容根 | 保持 `Constraint/` 与 `全栈开发Prompt Chain/` | 前者承载原始材料与可配置系统，后者承载完整全栈 Prompt Chain；两者互相引用。 |
| 压缩快照 | 移至 `archive/全栈开发Prompt Chain.zip` 并提交 | 用户明确要求远端保留该 136 KB 快照。 |
| 直接支持的平台 | Codex、DSH Desktop / DeepSeek Harness | Claude Code 保留兼容资料；Cursor 仅吸收规则设计亮点。 |
| 版本管理 | Git `main` + 初始快照提交 | 本轮不创建 tag、GitHub Release、Issue、PR 或自动化。 |
| 远端 | `origin` 指向用户指定 GitHub 空仓库 | 推送前仍须只读核验远端状态与当前认证。 |

## 3. 目标结构

```text
vibecoding_config/
├── README.md
├── .gitignore
├── archive/
│   └── 全栈开发Prompt Chain.zip
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-09-06-repository-initialization-design.md
├── Constraint/
└── 全栈开发Prompt Chain/
```

`Constraint/` 与 `全栈开发Prompt Chain/` 下现有文件不更名、不移动、不做内容重写。根 `docs/` 仅保存本次及后续仓库治理设计，不与两套既有内容的内部 `docs/` 目录合并。

## 4. 根 README 设计

根 `README.md` 使用中文，包含：

1. 仓库定位：面向 AI 全栈开发的配置、研究、Skill 治理和 Prompt Chain 资料库；
2. 内容地图：`Constraint/coding-agent-system` 与 `全栈开发Prompt Chain` 的职责、入口文件和适用人群；
3. 快速开始：从研究、直接配置、项目初始化、完整 Prompt Chain 四种意图进入相应文档；
4. 平台边界：Codex、DSH Desktop / DeepSeek Harness 为直接目标，Claude Code 为兼容资料，Cursor 仅作经验来源；
5. 验证与安全：说明静态契约、工具测试、真实平台 smoke 与对照评测的区别；
6. 版本与贡献约定：以 Git 历史记录可追溯变更，重大配置/研究结论应同步更新来源账本与验证证据；
7. 归档入口：链接到版本化 ZIP 快照，并说明 Markdown 正文是权威可维护版本。

README 只建立导航和使用边界，不复制两套子项目的长篇技术说明或宣称未运行的效果。

## 5. 忽略与归档规则

`.gitignore` 至少排除：

- macOS 的 `.DS_Store`；
- Python 字节码、`__pycache__/`、`.pytest_cache/` 与虚拟环境；
- `node_modules/`、常见构建/coverage 输出；
- `.env`、`.env.*`，但允许提交明确命名的示例文件；
- 编辑器临时目录和日志。

`archive/` 不被整体忽略，确保用户要求的 ZIP 快照被版本化。

## 6. 执行与验证顺序

1. 创建根 `README.md` 与 `.gitignore`；
2. 创建 `archive/` 并以 Git 移动 ZIP；
3. 初始化 `main` 分支，核验 Git 作者身份，不读取或输出任何凭据；
4. 运行 `Constraint/coding-agent-system` 现有渲染/结构校验与单元测试；
5. 校验根 README 链接、现有关键相对链接、忽略规则及暂存文件清单；
6. 创建首个本地提交；
7. 只读检查远端仓库状态，配置 `origin` 并推送 `main`；
8. 推送后以 `git ls-remote`、本地 HEAD 与 `git status` 核验远端分支、提交哈希与干净工作区。

如果 GitHub 认证、远端非空冲突、保护分支或网络失败阻止推送，保留本地提交并报告准确错误；不得用 force push、删除远端内容或改写历史绕过。

## 7. 非目标与风险边界

- 不重构、翻译、合并或删除现有研究和 Prompt 文档；
- 不修改用户级 Agent 配置、凭据、平台权限、MCP、Hooks 或生产系统；
- 不创建 GitHub Release、tag、PR、Issue、Actions 或外部自动化；
- 不将静态文档、工具校验或测试通过表述为 Codex、Claude Code 或 DSH 的真实运行效果；
- 不输出 GitHub token、SSH key、Git credential 或 `.env` 内容。

## 8. 验收标准

| 验收项 | 证据 |
|---|---|
| 两个既有内容根保持原路径 | Git diff / 文件检查未显示其中既有路径迁移或删除。 |
| 根 README 可作为入口 | README 的本地相对链接目标均存在，且覆盖两套内容、使用路径、边界与版本说明。 |
| ZIP 已归档并被追踪 | `archive/全栈开发Prompt Chain.zip` 出现在暂存区和提交树。 |
| 垃圾/敏感本地文件未进入提交 | `.gitignore` 规则与 `git status --ignored`、暂存文件清单一致；`.DS_Store` 与 `.env` 不在提交树。 |
| 配置系统未因仓库化受损 | 既有结构校验与单元测试通过，或准确记录环境性失败。 |
| 远端首个快照可复核 | `origin/main` 的 commit hash 与本地 `HEAD` 一致，工作区干净。 |

## 9. 实施结果（2026-09-06）

- 已在当前目录创建 Git main 分支，并保留 Constraint/ 与 全栈开发Prompt Chain/ 的既有路径；
- 已创建根 README.md、根 .gitignore、archive/，并将 全栈开发Prompt Chain.zip 移至归档目录后纳入版本控制；
- 首个历史包含设计规格、受管内容与归档快照、仓库 README 三个提交：e66d115、980db56、4b27150；
- 已运行模板渲染与结构校验，结果为 VALID；已独立运行 117 个单元测试，结果为 OK；
- 根 README 的 8 个核心章节和 17 个本地入口已逐项检查，归档 ZIP 完整性检查通过；
- 已将 main 推送至 https://github.com/zjgulai/vibecoding_config.git，推送后远端分支与本地 HEAD 的哈希一致；
- git diff --check 会报告导入材料中原有的尾随空白和 EOF 空行。为遵守本规格的内容保留约束，本轮未格式化或重写这些既有文件；
- 本次验证只证明仓库结构、工具与 Git 发布状态；不证明 Codex、Claude Code 或 DSH 的真实运行效果。
