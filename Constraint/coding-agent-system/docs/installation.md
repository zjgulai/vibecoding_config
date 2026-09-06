---
title: Coding Agent 配置系统安装与隔离验证
doc_type: guide
module: coding-agent-system
topic: installation
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# Coding Agent 配置系统安装与隔离验证

## 本文覆盖什么

本文说明如何使用 `tools/agent_system.py`：

- 校验配置系统源码。
- 在空目录中预览和生成项目级配置。
- 在隔离 home 中 smoke test 用户级配置。
- 在明确授权后安装 Codex 或 DeepSeek Harness 的用户级配置；Claude Code 仅作为可选兼容 adapter。
- 理解 skill 的平台适配、备份限制和回滚步骤。

本轮交付没有执行真实用户安装，没有修改 `~/.codex/`、`~/.claude/`、`~/.dsh/` 或 `~/.agents/`，也没有启动 Codex、DSH 或兼容 Claude Agent，更没有调用付费模型。

Cursor 不是安装目标；本系统只吸收其文档组织经验。DeepSeek 目标仅指官方 `@deepseek-ai/dsh` Harness。

**模型路由当前是文档，不是安装产物。** 本工具不会安装 `quality`、`balanced`、`economy` profile，也不会写入 provider、模型 ID、reasoning 默认值或凭据。[模型配置](model-configuration.md)中的片段只用于 opt-in 人工配置，采用前必须按当前客户端、账户和组织策略重新核验。

## 安全边界

- 所有写入命令默认省略 `--apply`。此时工具只输出计划，不创建或修改文件。
- `init-project` 只接受不存在或完全空的目录。它不支持向现有项目直接合并。
- `install-user` 只在显式传入 `--apply` 后写入。将被覆盖的既有指令或 Skill 文件要求 `--backup-dir`；已有且内容不同的 `.codex/config.toml` 与 `.claude/settings.json` 无论是否提供备份都不会被覆盖，必须人工合并。内容完全相同时只做 no-op。
- 用户安装对允许覆盖的每个文件先流式写入同目录中性临时文件，以实际字节长度和 SHA-256 核验并 `fsync`，再执行原子移动，不做字段合并。Darwin 使用 `/bin/mv`，其他平台使用 `os.replace`。多个文件组成的整批安装不是原子操作或全局事务；后续文件失败时，工具会逆序尝试补偿回滚已写入项，但回滚本身也可能失败，不能把它当作事务保证。
- 工具只处理生成清单中的模板、Skill 和目标文件，不遍历或解析任意敏感路径，也不打印既有文件内容。它会扫描生成画像、Memory 字段和项目自定义 Skill 的 secret-like 赋值与敏感相对路径，诊断仅报告字段或路径，不回显值。但是，备份操作会读取允许覆盖目标的全部字节并原样复制；原文件若含 token、凭据或 PII，备份也会包含这些信息。
- 备份目录必须只有受信任用户可访问，并且不得位于公开仓库、共享目录或自动同步目录。工具不负责为备份加密、脱敏或强制权限模式。
- `--home` 表示一个 home 根目录。工具仍在其下使用固定的 `.codex`、`.claude`、`.dsh` 和 `.agents` 子目录。
- 目标、home 与备份路径会先解析最深的已存在祖先；dry-run 和 apply 后续只使用并显示规范化真实路径。例如 macOS 的 `/tmp` 会显示为 `/private/tmp`。路径自身若是符号链接仍会被拒绝；祖先 alias 不会被隐藏成原始 lexical 路径。备份路径可以使用始终位于受管树外的祖先 alias，但只要任一解析前缀进入目标 home 的 `.codex`、`.claude`、`.dsh` 或 `.agents`，即使后续符号链接又跳到外部，也会在写入前拒绝。

## 前置条件

1. 使用能够运行本工具的 Python 3 解释器。macOS / Darwin 写入路径还调用系统自带的 `/bin/mv` 做同目录原子移动；缺失或执行失败时 fail closed。其他平台使用 Python `os.replace`。
2. 从本系统根目录执行命令：

   ```bash
   cd Constraint/coding-agent-system
   ```

3. 确认命令接口与当前文件一致：

   ```bash
   python3 tools/agent_system.py --help
   python3 tools/agent_system.py init-project --help
   python3 tools/agent_system.py install-user --help
   python3 tools/agent_system.py render-templates --help
   python3 tools/agent_system.py validate --help
   python3 tools/agent_system.py validate-generated --help
   ```

4. 在任何 apply 前检查目标路径。项目目标应是普通目录，不应是符号链接。
5. 用户配置 apply 前关闭或暂停正在写这些配置文件的 Agent 进程，避免并发写入。

## 命令接口

```text
python3 tools/agent_system.py init-project DEST \
  [--stack {typescript-nextjs,python-fastapi,postgresql-migrations,frontend-visual-quality}]... \
  [--apply]

python3 tools/agent_system.py install-user \
  --target {codex,claude,deepseek-harness,all} \
  [--home HOME] \
  [--backup-dir BACKUP_DIR] \
  [--apply]

python3 tools/agent_system.py render-templates [--apply]

python3 tools/agent_system.py validate [PATH]

python3 tools/agent_system.py validate-generated \
  --kind {project,user} \
  --root PATH \
  [--target {codex,claude,deepseek-harness,all}] \
  [--require-ready-profile]
```

`--stack` 可以重复。没有 `--apply` 时，`init-project`、`install-user` 和 `render-templates` 均不写入。`--require-ready-profile` 只适用于 `--kind project`；普通项目校验允许 draft 画像，正式开发门使用该参数要求 active 且完整的画像。

### 输出与退出状态

| 情况 | 标准输出或错误 | 退出状态 |
| --- | --- | --- |
| dry-run 成功 | 首行 `DRY-RUN`；后续每项为 `display path -> canonical absolute destination`。 | `0` |
| apply 成功 | 首行 `APPLIED`；后续每项为 `display path -> canonical absolute destination`，发生备份时还包含 `BACKUP ...`。 | `0` |
| `validate` 成功 | `VALID` | `0` |
| `validate-generated` 成功 | `VALID-GENERATED` | `0` |
| `validate` 发现问题 | 一行或多行 `ERROR ...` | `1` |
| 安全检查拒绝操作 | 标准错误中的 `ERROR ...` | `2` |

不要只看退出状态而忽略 `ERROR` 内容，也不要基于截断输出判断安装完成。

## 第一步：渲染并校验配置系统源码

`templates/shared/*` 是 canonical shared core；`templates/user/*` 与 `templates/project/*` 中包含受版本控制的平台快照。初始化和安装使用已渲染快照，不在目标目录临时拼接正文。

先预览完整的平台快照目标映射。dry-run 不写文件，也不区分内容相同与不同：

```bash
python3 tools/agent_system.py render-templates
```

若 `validate` 报告 shared core drift，先确认修改来自有意的 canonical 变更，并审查上述目标范围，然后再应用：

```bash
python3 tools/agent_system.py render-templates --apply
```

应用后审查仓库 diff 并重新运行 `validate`。不要直接编辑快照中的共享块；平台增量应保留在渲染器定义的适配层。

### 操作

```bash
python3 tools/agent_system.py validate
```

显式路径的等价形式：

```bash
python3 tools/agent_system.py validate \
  /absolute/path/to/coding-agent-system
```

### 预期结果

```text
VALID
```

校验覆盖必需模板、可重渲染一致性、skill 名称和引用、JSON、TOML 以及模板中的危险默认值。`init-project --apply` 与 `install-user --apply` 会在任何写入前执行同一套完整校验；只要共享快照漂移、文件缺失或安全检查失败，就 fail closed。校验不启动 Codex、Claude Code 或 DeepSeek Harness，也不证明某个已安装版本实际加载了生成文件。

`validate` 的输入应是本配置系统源码根目录。生成后的项目没有 `templates/` 和 `skills/` 源目录，因此不要把 `validate /path/to/generated-project` 当作生成项目健康检查；生成项目或用户 home 应使用 `validate-generated`。

### 失败处理

- `missing required file`：恢复或生成缺失的规范化模板后重试。
- `shared core drift`：修改 canonical shared core，执行 `render-templates` 审查完整目标映射，再用 `render-templates --apply` 更新全部平台快照；审查仓库 diff 后重新校验，不要只修一个平台副本。
- `invalid JSON` / `invalid TOML`：修复规范源并重新解析。
- skill 相关错误：检查 `SKILL.md` frontmatter、目录名、`agents/openai.yaml` 和相对引用。

在 `validate` 返回 `VALID` 之前，不进行用户级 apply。

## 第二步：生成项目级配置

### 只复制单个平台的项目级 AGENTS.md

如果项目已经存在、只需要一份基础规则，不要对非空目录运行 `init-project`。先选择一个互斥发行快照：

- Codex：`templates/project/codex/AGENTS.md`
- DSH Desktop / DeepSeek Harness：`templates/project/deepseek-harness/AGENTS.md`
- 同一项目同时使用两者：`templates/project/AGENTS.md`

三者部署后的真实路径都只能是目标项目根 `AGENTS.md`。`templates/project/codex/` 和 `templates/project/deepseek-harness/` 只是本工具包的交付目录，不是客户端发现路径，也不能同时原样复制到目标项目。

新项目尚无根规则时，可以先做存在性门再复制：

```bash
TARGET_PROJECT=/absolute/path/to/project
test ! -e "$TARGET_PROJECT/AGENTS.md"
cp templates/project/codex/AGENTS.md "$TARGET_PROJECT/AGENTS.md"
```

DSH Desktop 项目把上例 source 换为 `templates/project/deepseek-harness/AGENTS.md`。若目标已经存在 `AGENTS.md`，不要覆盖；先比较 shared core、现有项目事实和局部规则，再手工合并。四份单平台主交付是 Codex / DSH 的两份用户级与两份项目级 `AGENTS.md`；本节第三个平台中立项目文件只是同仓双平台 alternate，不另算一份单平台交付。项目 core 会路由 `.agents/project-profile.md`。新项目应优先运行 `init-project`，让画像、Memory、controls 和 Skills 成套生成。向现有项目人工复制时，还要从 `templates/project/.agents/` 选择性复制治理层并审查每个文件；不要只复制入口后把缺失画像误当作已完成配置。不要手改共享块，也不要把个人模型、凭据或临时任务计划写入项目根。

这些步骤只完成文件复制，不证明 Codex 或 Harness 已加载。DSH Desktop 还需确认其所用 preset / spine 启用了 `agent-instructions` 与 skill 相关 plugins；无 Git 项目应从项目根启动。两平台都必须按当前客户端版本做只读 discovery smoke。

### 选择技术栈模块

只选择已有架构或已确认方案需要的模块：

| `--stack` 值 | 触发范围 |
| --- | --- |
| `typescript-nextjs` | 项目使用 TypeScript、React 或 Next.js。 |
| `python-fastapi` | 项目使用 Python 或 FastAPI。 |
| `postgresql-migrations` | 项目使用 PostgreSQL schema、migration 或数据访问层。 |
| `frontend-visual-quality` | 项目包含用户可见页面、组件、交互或响应式布局。 |
| `file-document-governance` | 项目明确采用文件分类、命名、frontmatter、草稿/临时/归档治理，或当前任务正在建立该约定。 |

这些模块提供事实发现和质量门，不安装框架，不选择版本，也不创建依赖。

### 确认空目录条件

目标目录可以不存在，也可以存在但完全为空。以下情况会被拒绝：

- 目标是普通文件。
- 目标目录包含任何文件或子目录，包括隐藏文件。
- 计划复制的模板或 skill 源是符号链接或越出声明根目录。

工具没有把任意符号链接项目根定义为受支持路径。安装前应显式检查目标不是符号链接。

```bash
test ! -L /absolute/path/to/project
```

### 先运行 dry-run

单技术栈示例：

```bash
python3 tools/agent_system.py init-project \
  /absolute/path/to/project \
  --stack python-fastapi
```

多技术栈示例：

```bash
python3 tools/agent_system.py init-project \
  /absolute/path/to/project \
  --stack typescript-nextjs \
  --stack postgresql-migrations \
  --stack frontend-visual-quality \
  --stack file-document-governance
```

检查输出首行为 `DRY-RUN`。随后确认：

- 项目根只包含共同入口 `AGENTS.md`，不包含 `AGENTS.override.md`、`AGENTS.local.md`、`CLAUDE.md` 或 `CLAUDE.local.md`；Claude 入口位于 `.claude/CLAUDE.md`。这避免 Codex/Harness 的根级指令阴影与 DeepSeek Harness 的初始根候选冲突，但不是绝对隔离：默认 `agent-instructions` plugin 在 Harness 成功访问 `.claude/` 后仍可能动态发现该文件，且不会解释其中的 `@../AGENTS.md` import。
- `.agents/rules/` 只包含选择的模块；根 `AGENTS.md` 的受管路由块逐项列出这些模块的路径与触发条件。只生成文件而没有根路由不算配置已生效。
- `.agents/generated-manifest.json` 的 `stacks` 与 dry-run 选择完全一致；该文件是生成物完整性契约，不是平台指令。
- `.agents/project-profile.md` 默认是 `draft`；`.agents/memory/candidates.jsonl` 默认为空；`.agents/controls/change-policy.example.json` 只是默认关闭的示例。初始化计划不应包含实际 policy `.agents/controls/change-policy.json`。
- `.agents/skills/`、`.claude/skills/` 和 `.dsh/skills/` 的计划符合后文的适配规则。
- 没有出现目标目录之外的路径。

dry-run 只列出路径，不生成内容 diff。需要内容审查时，读取 `templates/shared/` 的 canonical core、已渲染的平台快照与 `skills/`；平台 skill 变体还需按「Skill 平台适配」检查生成规则。

### 再执行 apply

使用与 dry-run 完全相同的参数，并在末尾追加 `--apply`：

```bash
python3 tools/agent_system.py init-project \
  /absolute/path/to/project \
  --stack typescript-nextjs \
  --stack postgresql-migrations \
  --stack frontend-visual-quality \
  --stack file-document-governance \
  --apply
```

工具先在目标父目录创建 staging tree。所有文件复制成功后，才把 staging tree 替换为目标目录。失败时清理 staging tree；目标原本必须为空，因此不会静默合并或覆盖已有项目。

### 生成结果

```text
/absolute/path/to/project/
├── AGENTS.md
├── .agents/
│   ├── README.md
│   ├── generated-manifest.json
│   ├── project-profile.md
│   ├── memory/
│   │   ├── README.md
│   │   └── candidates.jsonl
│   ├── controls/
│   │   ├── README.md
│   │   ├── change-policy.example.json
│   │   └── check_change_policy.py
│   ├── rules/
│   └── skills/
├── .claude/
│   ├── CLAUDE.md
│   ├── settings.json
│   └── skills/
├── .codex/
│   └── config.toml
└── .dsh/
    └── skills/
```

`.dsh/skills/` 只包含显式编排型 skill 的优先级适配副本，因此其内容少于 `.agents/skills/` 是预期行为。

项目画像初始化为 `profile_status: draft`，七个标题域保留“尚未确认”。这不是错误；draft 不会阻塞边界清楚的普通任务，但不能支持高风险 readiness 声明。应先从仓库、运行行为、测试和项目维护者决定中填入证据，再把状态改为 `active`。active 每域只接受一组或多组 `- Fact:`、`- Decision:` 或 `- Not applicable:` 加紧随其后的缩进 `Source:`；`Not applicable` 必须说明适用边界。Source 只允许项目相对 `path:`、可复现 `command:`、http(s) `url:` 或带日期与上下文的 `user-confirmation:`。`x`、`N/A`、“待定”“未确认”“无”等低信息值、未知/重复 H2、fenced block、HTML comment、HTML 隐藏元素、零宽/双向控制字符或重复 frontmatter 都不能绕过校验；active gate 遇到隐藏内容会拒绝整个域，不做先删除再接受的清洗。

### 项目级 smoke

1. 校验生成项目的平台形状、生成器拥有的 managed artifacts，以及 manifest 中声明的 stack modules：

   ```bash
   python3 tools/agent_system.py validate-generated \
     --kind project \
     --root /absolute/path/to/project
   ```

   上述命令允许 draft。项目画像补全并改为 active 后，再运行正式门：

   ```bash
   python3 tools/agent_system.py validate-generated \
     --kind project \
     --root /absolute/path/to/project \
     --require-ready-profile
   ```

2. 检查计划路径均已生成：

   ```bash
   find /absolute/path/to/project -type f -print | sort
   ```

3. 检查 Claude 项目入口首个逻辑行导入共同契约，并确认项目根没有四个指令阴影文件：

   ```bash
   sed -n '1,8p' /absolute/path/to/project/.claude/CLAUDE.md
   for name in AGENTS.override.md AGENTS.local.md CLAUDE.md CLAUDE.local.md; do
     test ! -e "/absolute/path/to/project/$name" || exit 1
   done
   ```

4. 检查项目模块：

   ```bash
   find /absolute/path/to/project/.agents/rules -type f -print | sort
   python3 -m json.tool \
     /absolute/path/to/project/.agents/generated-manifest.json
   sed -n '/BEGIN MANAGED MODULE ROUTES/,/END MANAGED MODULE ROUTES/p' \
     /absolute/path/to/project/AGENTS.md
   ```

5. 检查 skill 适配：

   ```bash
   rg -n '^disable-model-invocation: true$' \
     /absolute/path/to/project/.claude/skills \
     /absolute/path/to/project/.dsh/skills
   ```

6. 确认 canonical skill 没有 Claude / DSH 专属顶层字段：

   ```bash
   if rg -n '^disable-model-invocation:' \
     /absolute/path/to/project/.agents/skills; then
     exit 1
   fi
   ```

7. 确认项目 Codex 配置没有覆盖用户或组织层的审批与 sandbox 基线：

   ```bash
   if rg -n '^(approval_policy|sandbox_mode|model)\s*=' \
     /absolute/path/to/project/.codex/config.toml; then
     exit 1
   fi
   ```

### 可选 controls 接入

初始化器不会生成实际策略，也不会修改平台 hook 或 CI。只有项目维护者确认确有确定性联动或受保护路径需求时，才执行以下操作：

1. 审查 `.agents/controls/change-policy.example.json` 与检查器源码。
2. 创建唯一实际策略 `.agents/controls/change-policy.json`。路径使用仓库相对 POSIX 形式；目录项按前缀匹配。
3. 在未接入 hook 或 CI 前手工运行检查器，确认允许和拒绝样例：

   ```bash
   python3 .agents/controls/check_change_policy.py \
     --policy .agents/controls/change-policy.json \
     path/to/changed-file
   ```

4. 只有输出语义、退出状态和项目变更策略都经审查后，才把同一命令显式接入既有 hook 或 CI。

实际 policy 是项目可编辑文件，`validate-generated` 会校验其 schema 与路径语法，但不会要求它与 example 字节相同。除 `.agents/controls/change-policy.json` 外，受管树中的其他未声明文件仍会被拒绝。

### 无 Git 仓库时的启动位置

`init-project` 不初始化 Git。默认 spine 已启用 skill filesystem plugin 时，项目还没有 Git 根，应从生成项目的根目录启动 DeepSeek Harness。不要先切换到 `src/`、`apps/web/` 等嵌套目录再启动：无可识别 Git 根时，Harness 的 skill 发现会把当前工作目录作为项目根，导致真正项目根的 `AGENTS.md` 或 `.agents/skills/` 不在预期搜索范围内。文件已经生成只能证明文件系统形状，不能证明从嵌套 cwd 启动的客户端已发现它们。

初始化 Git 后仍需按当前客户端版本做只读发现 smoke。不要把 Git 根存在等同于平台一定加载了全部文件。

这些检查证明文件系统生成与适配形状，不证明平台运行时发现或模型行为。

### 非空现有项目

`init-project` 不支持直接向非空项目安装。收到 `Destination must be empty` 时，不要临时移走项目文件后 apply，也不要放宽空目录保护。

可使用以下受控流程：

1. 在新的隔离空目录生成同一组选项。
2. 逐文件比较生成树与现有项目。
3. 把共同契约、平台配置、模块和 skills 作为一组待审变更手工合并。
4. 保留现有项目的更具体规则、权限设置和未提交改动。
5. 对 JSON、TOML 和共享正文重新运行项目已有检查；当前 `validate` 不校验合并后的项目树。

手工合并是独立的写入任务。它需要明确范围和逐项审查，不是 `init-project` 的隐含能力。

## 第三步：在隔离 home 中 smoke test 用户安装

真实用户配置 apply 前，先使用临时 home。下面的流程只写入 `mktemp` 创建的隔离目录：

```bash
SYSTEM_ROOT="$(pwd)"
SMOKE_ROOT="$(mktemp -d)"
SMOKE_HOME="$SMOKE_ROOT/home"
SMOKE_PROJECT="$SMOKE_ROOT/project"
mkdir -p "$SMOKE_HOME"

python3 "$SYSTEM_ROOT/tools/agent_system.py" validate "$SYSTEM_ROOT"

python3 "$SYSTEM_ROOT/tools/agent_system.py" install-user \
  --target all \
  --home "$SMOKE_HOME"

python3 "$SYSTEM_ROOT/tools/agent_system.py" install-user \
  --target all \
  --home "$SMOKE_HOME" \
  --apply

python3 "$SYSTEM_ROOT/tools/agent_system.py" init-project \
  "$SMOKE_PROJECT" \
  --stack typescript-nextjs \
  --stack frontend-visual-quality

python3 "$SYSTEM_ROOT/tools/agent_system.py" init-project \
  "$SMOKE_PROJECT" \
  --stack typescript-nextjs \
  --stack frontend-visual-quality \
  --apply
```

检查结果：

```bash
python3 "$SYSTEM_ROOT/tools/agent_system.py" validate-generated \
  --kind user \
  --root "$SMOKE_HOME" \
  --target all

python3 "$SYSTEM_ROOT/tools/agent_system.py" validate-generated \
  --kind project \
  --root "$SMOKE_PROJECT"

find "$SMOKE_HOME" -type f -print | sort
find "$SMOKE_PROJECT" -type f -print | sort
```

### 在隔离 home 验证备份门

重复 apply 时，内容相同的受保护平台设置文件会被跳过，其他指令与 Skill 目标已存在。省略 `--backup-dir` 应返回安全错误和退出状态 `2`：

```bash
python3 "$SYSTEM_ROOT/tools/agent_system.py" install-user \
  --target all \
  --home "$SMOKE_HOME" \
  --apply
```

随后使用新的备份目录重试：

```bash
python3 "$SYSTEM_ROOT/tools/agent_system.py" install-user \
  --target all \
  --home "$SMOKE_HOME" \
  --backup-dir "$SMOKE_ROOT/backup" \
  --apply
```

检查 `BACKUP ...` 行与备份文件。内容相同的 `.codex/config.toml` 和 `.claude/settings.json` 不应出现于备份清单，也不应被重写：

```bash
find "$SMOKE_ROOT/backup" -type f -print | sort
```

只有确认 `SMOKE_ROOT` 是本次 `mktemp` 返回的具体目录后，才清理它。优先在文件管理器中移入废纸篓；不要使用未展开、空值或宽泛路径执行递归删除。

## 第四步：选择用户级目标

### 固定安装路径

| `--target` | 用户模板目标 | Skill 目标 |
| --- | --- | --- |
| `codex` | `~/.codex/AGENTS.md`、`~/.codex/config.toml` | `~/.agents/skills/` canonical skills，并同步七个 `~/.dsh/skills/` 显式调用安全 overlay |
| `claude` | `~/.claude/CLAUDE.md`、`~/.claude/settings.json` | `~/.claude/skills/` Claude 适配副本 |
| `deepseek-harness` | `~/.dsh/AGENTS.md`、`~/.dsh/README.md` | `~/.agents/skills/` canonical skills，并同步七个 `~/.dsh/skills/` 显式调用安全 overlay |
| `all`（兼容模式） | 上述全部模板，包括 Claude compatibility adapter | canonical skills 只计划一次，再生成 Claude 副本并同步七个 DSH overlay |

表中的 `~` 指工具使用的 home 根目录。传入 `--home /path/to/home-root` 后，目标变为 `/path/to/home-root/.codex` 等固定子目录。

`--target` 只选择平台入口与该平台所需的适配集合，不承诺 skill 根彼此隔离。Codex 与 DeepSeek Harness 都能使用共享 `.agents/skills/`；因此只要目标包含其中任一平台，安装器都会同步 canonical skills 和七个 DSH explicit-only overlay，避免共享正文已更新而高优先级 DSH 副本仍旧。dry-run 会显示全部耦合路径。只有需要同时维护 Claude compatibility adapter 时才选择 `--target all`；Codex 与 DSH 的主路径应分别在隔离 home 预演并逐个审查入口。

### 自定义 `CODEX_HOME`、`CLAUDE_CONFIG_DIR`、`DSH_HOME` 或 `DSH_AGENTS_HOME`

当前安装器不会读取 `CODEX_HOME`、`CLAUDE_CONFIG_DIR`、`DSH_HOME` 或 `DSH_AGENTS_HOME`，也不能把任意目录直接作为某个平台的配置根。`--home` 始终生成固定的 `<home>/.codex`、`<home>/.claude`、`<home>/.dsh` 与 `<home>/.agents/skills` 布局。Claude Code 设置 `CLAUDE_CONFIG_DIR` 后，用户配置、session history 和 plugins 会改到该目录；Linux 与 Windows 的 credential storage 也随之移动，但 macOS 凭据仍保存在 System Keychain。因此在 macOS 上，不能仅凭配置目录不同就断言认证已在文件系统层隔离；多账户行为仍需按当前客户端单独验证。安装器不会自动跟随该变量。[Anthropic 官方环境变量说明](https://code.claude.com/docs/en/env-vars)

若 DeepSeek Harness 设置了自定义 `DSH_AGENTS_HOME`，非显式 skill 的安装根可能不再是 `<home>/.agents/skills`。当前安装器不会自动跟随该环境变量；这属于已知限制。使用非默认根时：

1. 使用 `--home` 在隔离目录生成固定结构。
2. 审查生成内容，并按当前 DeepSeek Harness 版本核实 `DSH_AGENTS_HOME` 下的 skill 发现路径。
3. 把所需 canonical skills 作为一次独立、人工审查的安装变更复制到核实后的自定义路径；不要让本工具根据未校验环境变量直接放宽写入边界。
4. 对 `CODEX_HOME`、`CLAUDE_CONFIG_DIR` 或 `DSH_HOME` 采用同样的隔离生成与人工迁移流程。迁移 Claude 文件时，把隔离 home 下 `.claude/` 的所需内容人工复制到已核实的 `CLAUDE_CONFIG_DIR` 根，不要再添加一层 `.claude`。
5. 从项目根启动目标客户端，并执行当前版本支持的只读发现 smoke。

不要假装 `--home "$CODEX_HOME"` 会把文件直接写为 `$CODEX_HOME/AGENTS.md`；它会写入 `$CODEX_HOME/.codex/AGENTS.md`。同理，`--home "$CLAUDE_CONFIG_DIR"` 会写入 `$CLAUDE_CONFIG_DIR/.claude/*`，不是 Claude Code 实际读取的 `$CLAUDE_CONFIG_DIR/*`。

## 第五步：预览真实用户安装

以下命令不带 `--apply`，因此不写入用户配置：

```bash
python3 tools/agent_system.py install-user --target codex
python3 tools/agent_system.py install-user --target claude
python3 tools/agent_system.py install-user --target deepseek-harness
python3 tools/agent_system.py install-user --target all
```

选择一个目标执行，不需要把四条全部运行。审查计划时：

1. 保存计划路径。
2. 对照固定安装路径，确认目标平台入口和共享 skill 耦合路径正确。`codex` 或 `deepseek-harness` 的计划都应包含七个 `.dsh/skills/` overlay。
3. 记录安装前已经存在的文件与新文件。工具的 dry-run 不生成 pre-install inventory，需由操作者自己保存。
4. 对已经存在的模板文件执行只读 diff。Skill 适配副本由工具生成，不能简单地与 canonical `SKILL.md` 做字节相等比较。
5. 确认计划使用的备份根尚不存在，其父目录受保护，并且备份根位于四类平台管理树之外。为降低误覆盖风险，建议同时放在目标 home 之外；后者是操作建议，不是当前工具的强制条件。

## 第六步：应用真实用户安装

只有用户已明确授权修改真实配置，且隔离 smoke 通过后，才执行本节。

### 没有任何目标文件存在

```bash
python3 tools/agent_system.py install-user \
  --target all \
  --apply
```

即使预期目标为空，也应先运行 dry-run 并保存安装前清单。若工具检测到任何将被覆盖的目标，会拒绝执行并要求 `--backup-dir`；内容相同的受保护平台设置文件会被跳过，不单独触发备份门。

### 受保护的平台设置文件

`.codex/config.toml` 与 `.claude/settings.json` 采用比普通指令文件更严格的规则：目标不存在时可创建；与模板逐字节相同时跳过；只要内容不同、目标不是普通文件或无法读取，就 fail closed 并要求人工合并。`--backup-dir` 不会放宽这一规则，也不会为被跳过的同内容文件创建备份。先在隔离 home 比较模板与现有设置，再按当前客户端、组织 policy 和本机需求人工迁移所需字段；不要用整文件替换覆盖 model、provider、permissions、sandbox、hooks 或 MCP 配置。

### 存在其他目标文件

选择一个绝对、专用且尚不存在的备份根。不要预先创建该根；工具会拒绝既有路径。应先准备只有受信任用户可访问的父目录，再在其下指定一个全新的子路径；具体权限与 ACL 取决于操作系统：

```bash
python3 tools/agent_system.py install-user \
  --target all \
  --backup-dir /absolute/path/to/coding-agent-backup \
  --apply
```

### apply 前检查

- 备份根尚不存在，不是符号链接，也不位于目标 home 的 `.codex`、`.claude`、`.dsh` 或 `.agents` 管理树内。建议另放在目标 home 之外的受保护位置。
- 备份根的父目录不会被同步、共享或提交到仓库，访问权限已限制给受信任用户。
- 工具拒绝复用既有备份根或覆盖任何旧备份。
- 允许覆盖的目标现有文件是普通文件且不是符号链接。工具拒绝覆盖目录、符号链接和其他非普通文件。
- 若 `.codex/config.toml` 或 `.claude/settings.json` 已存在，已确认它与模板完全相同；若不同，停止 apply 并完成人工字段合并。
- 已保存 dry-run 输出和安装前文件清单。

备份是 opaque copy：工具不解析、筛选或脱敏允许覆盖的既有文件，只原样复制目标字节。普通指令和 Skill 之后安装为模板整文件；受保护的 `.codex/config.toml` 与 `.claude/settings.json` 不进入这条覆盖路径，存在差异时必须先人工迁移所需字段。

### apply 后检查

1. 确认输出首行为 `APPLIED`。
2. 确认所有预期路径均出现，且没有 `ERROR`。
3. 逐项检查 `BACKUP ...` 路径；只有被覆盖的文件才有备份，受保护设置文件相同则跳过、不同则整个 apply 在写入前失败。
4. 重新解析 JSON 和 TOML，检查共享正文与 skill 适配。
5. 运行 `validate-generated --kind user --root <home> --target <target>`，确认安装后的平台形状。
6. 不立即删除备份。先完成平台加载 smoke 和至少一个代表性、无副作用任务。

## Skill 平台适配

`skills/<name>/` 是单一事实源。安装器不会把完全相同的目录机械复制到两个直接目标与 Claude compatibility adapter：

| 位置 | 内容 | 显式调用控制 |
| --- | --- | --- |
| `.agents/skills/<name>/` | 完整 canonical skill 树，包括 `SKILL.md`、可选 `references/`、`scripts/`、`assets/` 与 `agents/openai.yaml`。 | `metadata.invocation: explicit-only` 只是本项目生成器的内部 marker；Codex 使用 `agents/openai.yaml` 的 `policy.allow_implicit_invocation`。 |
| `.claude/skills/<name>/` | 完整 supporting resources；不复制 `agents/` 子目录。 | 对 explicit-only skill，在 `SKILL.md` 顶层插入 `disable-model-invocation: true`。 |
| `.dsh/skills/<name>/` | 只生成 explicit-only skill，但保留除 `agents/` 外的 supporting resources。 | 顶层插入 `disable-model-invocation: true`，由更高优先级的平台目录覆盖 `.agents/skills` 中的 canonical 版本。 |

非 explicit-only 的 DeepSeek Harness skill 继续从 `.agents/skills/` 发现。因此，`.dsh/skills/` 只有 7 个目录是当前预期，不是缺失。

用户安装中，只要 target 包含 `codex` 或 `deepseek-harness`，上述 `.agents/skills/` 与七个 `.dsh/skills/` overlay 会作为一个安全同步单元进入计划。这个行为会让 Codex-only dry-run 同时显示 DSH overlay；它不会安装 DSH 用户指令入口，但能避免同机 Harness 从共享根看到失去 explicit-only 限制的版本。该结论以默认 spine 已启用 skill registry、tool consumer 与 skill filesystem plugins 为前提；自定义 preset 或禁用 plugin 时必须按实际组合重新 smoke。

生成项目允许在 `.agents/skills/<project-skill>/` 新增符合格式的项目 Skill，以及被其 `SKILL.md` 相对引用的 `references/`、`scripts/`、`assets/`。校验器继续严格保护 manifest 声明的 managed Skills：自定义内容不能覆盖同名 managed Skill、注入 symlink、越出 Skill 根，或绕过 frontmatter、引用、敏感相对路径与 secret-like 内容检查。项目自定义 Skill 不能使用本生成器内部的 `metadata.invocation: explicit-only`，因为生成清单没有与之同步的 DSH/Claude 平台 overlay；确需显式调用的跨平台 Skill，应先纳入 canonical managed registry，再由生成器创建并校验各平台适配。允许扩展不是把整个项目树改成开放白名单。

### 适配检查

以下检查在隔离 home 或生成项目中执行：

```bash
rg -n '^disable-model-invocation: true$' \
  /path/to/home/.claude/skills \
  /path/to/home/.dsh/skills

if rg -n '^disable-model-invocation:' \
  /path/to/home/.agents/skills; then
  exit 1
fi
```

还需确认 `.claude/skills/` 和 `.dsh/skills/` 中没有 `agents/openai.yaml`。不要手工编辑生成副本；修改 canonical skill 或生成器，再重新生成。

## 平台加载 smoke 的证据层级

### 层级 1：文件系统 smoke

本文前述临时 home 流程验证：

- dry-run 不写入。
- apply 生成预期文件。
- 备份门能阻止无备份覆盖。
- skill 平台适配符合生成规则。

它不验证任何 Agent 运行时。

### 层级 2：本机 CLI 发现 smoke

只有本机已安装目标平台，并且可以把其配置根安全指向隔离 home 时才执行：

1. 先读取当前安装版本的 `--help` 和官方文档，确认配置根、离线能力和指令检查方式。
2. 将目标平台指向隔离 home；不要让工具回退到真实用户目录。
3. 优先使用只读的配置 dump、诊断或 instruction inspection 命令。
4. 核对实际加载的用户文件、项目文件、skill 名称和优先级。
5. 若当前版本没有只读检查命令，停止在层级 1，不猜测命令。

本系统没有统一封装三个平台的运行时 smoke，因此本文不提供未经核实的 CLI 子命令。

### 层级 3：代表性模型任务

真实模型调用可能产生费用或外部日志，需要单独授权。Auto Research 评测协议/控制面提供严格运行记录、成对比较、停止条件和缺失值协议；这些协议只规定如何比较。授权后仍需准备真实代表性 fixture，并使用 `evals/` 的同一任务、rubric 和记录 schema，分别记录模型、配置、耗时、token、质量、返工和未验证项。本轮没有运行真实 Agent、付费模型或代表性 fixture。

本轮没有执行真实代表性 fixture，也没有调用付费模型。schema、示例记录或本地评分器通过不能替代模型运行证据；单次成功也不能证明规则稳定提升。

## 回滚

### 项目初始化的立即回滚

`init-project` 的目标原本为空，因此刚完成初始化且尚未加入其他项目文件时，可以把整个生成目录移动到一个明确的隔离位置，保留审查和恢复能力。不要直接递归删除。

如果项目中已经加入应用代码、用户数据或其他协作者变更，不再按「整个目录」回滚。此时应依据安装时保存的路径清单，逐文件审查 Agent 配置；未知文件一律保留。

### 用户安装备份映射

`--backup-dir` 下的显示前缀与真实目标映射如下。每个备份文件都是对应既有目标的完整字节副本，可能包含敏感信息：

| 备份前缀 | 真实目标 |
| --- | --- |
| `codex/` | `~/.codex/` |
| `claude/` | `~/.claude/` |
| `deepseek-harness/` | `~/.dsh/` |
| `shared-skills/` | `~/.agents/skills/` |
| `claude-skills/` | `~/.claude/skills/` |
| `deepseek-harness-skills/` | `~/.dsh/skills/` |

### 用户安装回滚步骤

以下步骤既适用于主动恢复，也适用于安装器报告补偿回滚不完整后的人工恢复。即使错误信息说明 `applied files were rolled back`，也应先检查目标状态，不把消息本身当作恢复证据。

1. 停止使用受影响配置的 Agent 进程。
2. 查看保存的 apply 输出、安装前清单和 `BACKUP ...` 路径。
3. 对每个被覆盖文件，比较当前文件与备份文件。
4. 使用保留元数据的文件复制命令逐文件恢复；不要递归覆盖整个用户目录。
5. 对安装前不存在的新文件，先确认它仍是本工具生成且没有后续人工修改，再逐文件移动到隔离目录。`--backup-dir` 不会为新文件创建空备份。
6. 重新解析 JSON / TOML，并按平台路径检查恢复结果。
7. 使用层级 1 或层级 2 smoke 验证恢复状态。
8. 确认恢复有效后，再决定是否删除隔离副本和备份。

示例只恢复一个 Codex 文件：

```bash
cp -p \
  /absolute/path/to/coding-agent-backup/codex/AGENTS.md \
  /absolute/path/to/home/.codex/AGENTS.md
```

不要把此单文件示例扩展为对 home 根目录的递归复制。

### 部分 apply 失败

用户安装不是全局事务。若 apply 在处理中途失败，工具会先逆序尝试恢复已覆盖文件的备份，并移除本次新建且仍为普通文件的目标：

1. 不要立即重跑。
2. 若错误包含 `User install failed; applied files were rolled back`，逐文件核对既有目标已恢复、新目标已移除；成功消息仍不能替代状态检查。
3. 若错误包含 `User install failed and rollback was incomplete`，依据错误列出的 rollback errors、备份目录、目标状态和安装前清单，确定残留写入。失败时工具不会输出完整的 `APPLIED` 清单。
4. 对残留的既有目标按备份逐文件恢复；对残留的新文件，确认没有后续修改后先移动到隔离目录。
5. 找到安装或回滚失败原因，例如权限变化、目标类型变化或并发修改。备份冲突应在任何目标写入前被预检拒绝。
6. 在新的临时 home 中复现并修复原因。
7. 重新执行完整 dry-run，经人工确认后再 apply。

## 常见失败与恢复

| 现象 | 原因 | 安全恢复 |
| --- | --- | --- |
| `Destination must be empty` | 项目目标已有文件或隐藏目录。 | 使用新的空目录，或进入「非空现有项目」人工合并流程。 |
| `Existing user files require --backup-dir` | apply 会覆盖至少一个用户文件。 | 选择专用新备份目录，先检查目标，再带 `--backup-dir` 重试。 |
| `Existing user platform config differs; manual merge required` | `.codex/config.toml` 或 `.claude/settings.json` 已存在且与便携模板不同。 | 不要用备份参数强行覆盖；在隔离副本中比较并人工合并所需字段，然后重新 dry-run。 |
| `Backup root must be a new path` / `Backup root must not be a symlink` | 备份根已经存在，或该路径本身是符号链接。 | 不复用或预建备份根；在受保护父目录下指定全新且尚不存在的普通子路径。 |
| `Backup root must be outside managed user directories` / `Backup root resolution route enters managed user directory` | 备份根位于目标 home 的受管树内，或某个祖先 alias 的解析路径先进入受管树再跳到外部。 | 选择从每一级路径解析都始终位于 `.codex`、`.claude`、`.dsh`、`.agents` 之外的受保护路径；最好也位于目标 home 之外。 |
| `Backup destination already exists` | 预检后发生并发变化，或备份目标将覆盖已有对象。 | 停止并审查目标与备份根；不要删除旧备份后原地重试，改用新的备份根。 |
| `Refusing to overwrite non-regular user file` | 目标是目录、符号链接或其他非普通文件。 | 停止安装，确认平台路径和现有文件用途；不要把它替换成普通文件。 |
| `Refusing to copy symlink source` | 模板或 skill 源是符号链接。 | 审查来源；改为受版本控制的普通文件后重新校验。 |
| `shared core drift` | 平台快照与 canonical shared core 分叉。 | 修改 canonical 源，运行 `render-templates` 审查完整目标映射，再执行 `render-templates --apply`；审查仓库 diff 后重新校验。 |
| 平台没有发现生成文件 | 自定义配置根、版本差异或运行时发现规则不同。 | 停止声称安装成功；核对当前版本官方文档并在隔离 home 做只读发现检查。 |

## 安装完成清单

- [ ] `python3 tools/agent_system.py validate` 返回 `VALID`。
- [ ] 已审查 `python3 tools/agent_system.py render-templates` 的完整目标映射，且 `validate` 没有报告快照漂移。
- [ ] `validate-generated` 对生成项目或所选用户目标返回 `VALID-GENERATED`。
- [ ] 已在临时 home 完成 dry-run、apply 和备份门 smoke。
- [ ] 项目初始化目标为空，且不是符号链接。
- [ ] 项目只启用了实际相关的 `--stack` 模块。
- [ ] 已保存用户安装前清单和 dry-run 输出。
- [ ] 真实用户 apply 已获得明确授权。
- [ ] 任何实际被覆盖的既有用户文件都有完整备份；受保护平台设置文件已按“相同则跳过、不同则人工合并”处理；备份目录不在目标树、共享目录、同步目录或仓库内。
- [ ] Skill 的 canonical、Claude 适配和 DSH 适配符合预期。
- [ ] 已明确当前证据仅是文件系统、CLI 发现还是实际模型任务。
- [ ] 自定义 `CODEX_HOME`、`CLAUDE_CONFIG_DIR`、`DSH_HOME` 或 `DSH_AGENTS_HOME` 没有被错误映射；需要时已走隔离生成和人工审查复制。
- [ ] 备份和回滚步骤已保留，未因一次 smoke 成功立即删除。

## 相关文档

- [项目全生命周期 SOP](sop/project-lifecycle.md)
- [系统设计](design.md)
- [实施计划](implementation-plan.md)
- [深度研究报告](research/deep-research-report.md)
- [来源台账](research/source-ledger.md)
