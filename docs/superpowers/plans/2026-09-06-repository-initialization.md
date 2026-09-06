# Repository Initialization and Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax.

**Goal:** 将当前 vibecoding_config 资料库初始化为可维护的 Git 仓库，保留既有文档路径，补齐根 README，并将初始快照推送到 zjgulai/vibecoding_config。

**Architecture:** 保持 Constraint/ 和 全栈开发Prompt Chain/ 两个既有内容根不变；根目录只增加入口、忽略规则、归档目录和治理文档。Git 历史以已提交的设计规格为起点，随后提交仓库卫生、归档快照、根 README 与所有既有受管内容，最后配置远端并推送 main。

**Tech Stack:** Git、GitHub、Markdown、现有 Python 标准库 unittest 校验工具。

## Global Constraints

- 不重命名、移动、重写或删除 Constraint/ 和 全栈开发Prompt Chain/ 下既有文件。
- 将 全栈开发Prompt Chain.zip 移至 archive/ 并纳入 Git。
- Git 忽略 .DS_Store、Python cache/virtualenv、node_modules/、构建输出、日志和 .env/.env.*；不得忽略 .env.example。
- 不读取、不输出、不提交 token、SSH key、credential 或 .env 内容。
- 不创建 tag、GitHub Release、PR、Issue、Action、MCP、Hook、部署或生产变更。
- 推送前必须验证现有工具校验、单元测试、关键链接、暂存范围和 Git 对象；推送后必须验证 origin/main 与本地 HEAD 一致。
- 遇到认证失败、远端非空冲突、受保护分支或网络失败时，保留本地提交并停止；不得 force push、删除远端内容或改写历史。

---

### Task 1: 建立根目录卫生规则并归档快照

**Files:**
- Create: .gitignore
- Create: archive/
- Move: 全栈开发Prompt Chain.zip → archive/全栈开发Prompt Chain.zip

**Interfaces:**
- Consumes: 根目录现有 .DS_Store、各子目录 .DS_Store、现有 ZIP 快照。
- Produces: 适用于本仓库的忽略策略；被 Git 追踪的 archive/全栈开发Prompt Chain.zip；未更名的两个内容根。

- [x] **Step 1: 创建最小 .gitignore**

写入以下规则：

~~~gitignore
# OS and editor metadata
.DS_Store
.idea/
.vscode/
*.swp
*.swo

# Python caches and virtual environments
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/

# JavaScript dependencies and build output
node_modules/
coverage/
dist/
build/

# Local logs and secrets
*.log
.env
.env.*
!.env.example
~~~

- [x] **Step 2: 移动 ZIP 而不改动其内容**

运行：

~~~bash
mkdir -p archive
git mv '全栈开发Prompt Chain.zip' 'archive/全栈开发Prompt Chain.zip'
~~~

预期：根目录不存在原 ZIP；archive/全栈开发Prompt Chain.zip 存在；Constraint/ 与 全栈开发Prompt Chain/ 仍位于原路径。

- [x] **Step 3: 验证忽略规则与归档范围**

运行：

~~~bash
git check-ignore -v .DS_Store Constraint/.DS_Store '全栈开发Prompt Chain/.DS_Store'
if git check-ignore -q 'archive/全栈开发Prompt Chain.zip'; then
  printf '%s\n' 'archive ZIP must not be ignored'
  exit 1
fi
test -f 'archive/全栈开发Prompt Chain.zip'
test -d Constraint
test -d '全栈开发Prompt Chain'
~~~

预期：.DS_Store 显示由 .gitignore 忽略；ZIP 不被忽略；两个内容根存在。

- [x] **Step 4: 提交受管内容、卫生规则与归档快照**

运行：

~~~bash
git add .gitignore archive/ Constraint/ '全栈开发Prompt Chain/' docs/superpowers/plans/
git commit -m 'chore: initialize repository content and archive snapshot'
~~~

预期：提交包含受管资料、.gitignore 和 ZIP，不包含 .DS_Store、.env 或缓存文件。

### Task 2: 编写根 README 作为仓库入口

**Files:**
- Create: README.md
- Read: Constraint/coding-agent-system/README.md
- Read: 全栈开发Prompt Chain/README.md
- Read: Constraint/coding-agent-system/docs/sop/project-lifecycle.md
- Read: 全栈开发Prompt Chain/06-Prompt-Chain使用手册.md

**Interfaces:**
- Consumes: 两个内容根的既有入口、平台边界、验证边界和归档快照。
- Produces: 中文根 README，提供仓库定位、内容地图、四种使用入口、平台范围、验证边界、版本约定和归档链接。

- [x] **Step 1: 写入 README 内容**

README 必须包含以下章节：

~~~markdown
# VibeCoding Config

## 仓库定位
## 内容地图
## 从哪里开始
## 直接支持的平台与边界
## 验证与安全边界
## 版本管理与贡献约定
## 归档快照
~~~

内容地图必须列出：

~~~markdown
| 内容 | 入口 | 适合何时使用 |
|---|---|---|
| Coding Agent 配置系统 | [Constraint/coding-agent-system/README.md](Constraint/coding-agent-system/README.md) | 配置 Codex 或 DSH Desktop / DeepSeek Harness、初始化项目、治理 Skills、运行结构校验。 |
| AI 产品全生命周期 Prompt Chain | [全栈开发Prompt Chain/README.md](全栈开发Prompt%20Chain/README.md) | 按 M00–M13、A00–A13、G0–G6 组织需求、实现、验证、发布和复盘。 |
~~~

README 把 Claude Code 表述为兼容资料，把 Cursor 表述为规则设计参考；不得承诺真实平台已加载、测试或优于其他工作流。

- [x] **Step 2: 验证 README 的必需入口与本地链接**

运行：

~~~bash
rg -n '^# |^## ' README.md
test -e 'Constraint/coding-agent-system/README.md'
test -e 'Constraint/coding-agent-system/docs/sop/project-lifecycle.md'
test -e '全栈开发Prompt Chain/README.md'
test -e '全栈开发Prompt Chain/06-Prompt-Chain使用手册.md'
test -e 'archive/全栈开发Prompt Chain.zip'
~~~

预期：README 包含七个既定章节；所有本地入口均存在。

- [x] **Step 3: 提交根 README**

运行：

~~~bash
git add README.md
git commit -m 'docs: add repository overview and navigation'
~~~

预期：提交只包含根 README。

### Task 3: 运行既有校验并审计首个快照

**Files:**
- Read: Constraint/coding-agent-system/tools/agent_system.py
- Read: Constraint/coding-agent-system/tools/tests/
- Read: .gitignore
- Read: README.md

**Interfaces:**
- Consumes: 当前 main 提交树、既有配置工具、README 与忽略规则。
- Produces: 可复核的本地验证结果；如有失败，记录准确的失败原因且不伪称通过。

- [x] **Step 1: 运行配置系统静态校验**

运行：

~~~bash
cd Constraint/coding-agent-system
python3 tools/agent_system.py render-templates
python3 tools/agent_system.py validate .
~~~

预期：两条命令退出码为 0；render-templates 只输出渲染映射，不改写快照。

- [x] **Step 2: 运行配置系统单元测试**

运行：

~~~bash
cd Constraint/coding-agent-system
python3 -m unittest discover -s tools/tests -v
~~~

预期：测试进程退出码为 0，且没有失败或错误。

- [x] **Step 3: 审计 Git 内容与对象完整性**

从仓库根运行：

~~~bash
git diff --check HEAD~2..HEAD
git ls-files | rg '(^|/)\\.DS_Store$|(^|/)\\.env($|\\.)|(^|/)__pycache__/' && exit 1 || true
git ls-files --error-unmatch 'archive/全栈开发Prompt Chain.zip'
git fsck --no-reflogs
git status --short
~~~

预期：git diff --check 无输出；敏感或缓存路径匹配命令无输出；ZIP 被追踪；git fsck 无错误；工作区干净。

### Task 4: 连接并推送指定 GitHub 远端

**Files:**
- Modify: .git/config（由 Git 命令管理）

**Interfaces:**
- Consumes: 本地 main、用户指定 URL https://github.com/zjgulai/vibecoding_config.git、已通过 Task 3 的本地提交树。
- Produces: origin/main 指向与本地 HEAD 相同的首个可复核提交。

- [x] **Step 1: 只读确认远端状态**

运行：

~~~bash
git ls-remote --heads https://github.com/zjgulai/vibecoding_config.git
~~~

预期：空仓库不返回分支行；若返回 main 或其他分支，停止并比较提交历史，不覆盖远端。

- [x] **Step 2: 配置远端并推送 main**

运行：

~~~bash
git remote add origin https://github.com/zjgulai/vibecoding_config.git
git push -u origin main
~~~

预期：GitHub 接受首个 main 分支；不使用 --force、--mirror 或删除参数。

- [x] **Step 3: 交叉核验远端提交和干净状态**

运行：

~~~bash
local_head=$(git rev-parse HEAD)
remote_head=$(git ls-remote --heads origin main | awk '{print $1}')
test "$local_head" = "$remote_head"
git status --short
git remote -v
~~~

预期：本地与远端哈希一致；git status --short 无输出；origin 的 fetch/push URL 都是用户指定仓库。

## Plan Self-Review

| 规格要求 | 覆盖任务 |
|---|---|
| 保留两个内容根的路径和内容 | Task 1 的约束、移动后目录验证与暂存范围。 |
| ZIP 归档且远端可得 | Task 1 的 Git 移动与追踪验证；Task 4 推送。 |
| 根 README 完整导航 | Task 2 的章节、内容地图和本地链接检查。 |
| 忽略垃圾、缓存和本地敏感文件 | Task 1 的 .gitignore 与 git check-ignore；Task 3 的提交树审计。 |
| Git 初始化、提交与 main 推送 | 已完成的设计提交；Task 1/2 内容提交；Task 4 远端配置、推送和 hash 比对。 |
| 现有配置系统不被破坏 | Task 3 的 render、validate 和 unit test。 |
| 不越权创建发布、tag、PR、Issue 或外部自动化 | 全局约束与 Task 4 的非 force、仅 push main。 |

计划无未定义接口、未完成标记或新增依赖；没有新增应用代码、运行时 API 或外部依赖。
