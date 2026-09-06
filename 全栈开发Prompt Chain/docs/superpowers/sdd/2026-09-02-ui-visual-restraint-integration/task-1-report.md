# Task 1 实施报告：Codex UI 规则入口与单一事实源

## 实施前基线

执行时间：2026-09-02（Asia/Shanghai）。当前目录不是 Git 仓库；未创建 commit。

### 明确不修改文件的 SHA-256

写入三个允许目标文件前已建立本报告。收尾审查发现初始哈希清单漏列 4 个由 Step 1 的 `find` 覆盖的文件；以下为按该精确命令补足后的完整 31 行清单。漏列文件从未是写入目标，收尾 SHA-256 与下列值一致；但完整清单是在允许文件编辑后补足，时序缺口见「Concerns」。

```text
a1659447de74f8fb1ef61c99093f652d69ad3acabbcaacb408037cfc3a674ce6  Constraint/coding-agent-system/templates/project/.claude/CLAUDE.md
43e9464c455ab1ff15abd70cb2744da0b16254a43c9cbbf3862e3f0a6ac15f2d  Constraint/coding-agent-system/templates/project/.claude/settings.json
fe35ca1aa647f2a4f29faf2b626fb1d139ea954632858f8e3caddbe674b1c969  Constraint/coding-agent-system/templates/project/deepseek-harness/AGENTS.md
5208be266eb5b3f93a6ba30929c67e10da5de2f2d3580704f9f6588064eaf30d  Constraint/coding-agent-system/templates/shared/project-core.md
41cc6733f3b91efc6c60347526fe3495879a1ee087cf242cd24de7f583cf5140  Constraint/coding-agent-system/templates/shared/user-core.md
604f14e5b38383ff765e39834d4e4630418f78157e8ce1add718d76366d4b16d  Constraint/coding-agent-system/templates/user/claude/CLAUDE.md
43e9464c455ab1ff15abd70cb2744da0b16254a43c9cbbf3862e3f0a6ac15f2d  Constraint/coding-agent-system/templates/user/claude/settings.json
d8e36cc3557c520aaf5a09b8e9ea2df50f7ff67b78eb6590ad3abecbfc9f469e  Constraint/coding-agent-system/templates/user/deepseek-harness/AGENTS.md
81a0dcf31e8efeab63820e1aca936ca38ae25383e604c0b142f894ee873776ec  Constraint/coding-agent-system/templates/user/deepseek-harness/README.md
d65165279105ca6773180500688df4bdc69a2c7b771752f0a46ef120b7fd8ec3  Constraint/cursor_rules/.DS_Store
c65a33408f5b09d731b86d1bda8c004971cfa146f164ac71dcc4ba9796b93d58  Constraint/cursor_rules/00-core.mdc
3acd44025f41ae2786c39ec9d49da3dee84a4444f862b1515a30d03844b1261a  Constraint/cursor_rules/10-structure.mdc
32499ffda096fd09835b4ec102a9851b52b93c20fbc0458dab73e984519730f6  Constraint/cursor_rules/20-python.mdc
a5f2547230e8705cf6aa86200792a4c095f635530b270a0bcaff31c13bb59694  Constraint/cursor_rules/24-skill-authoring.mdc
8678b10006df2f1adb5836ba1a2d02cfd92a58d434c4cbf0317792d6cab7b943  Constraint/cursor_rules/30-docs.mdc
854cfb72b6b17a08f2a33021b6d5f49fe6f4ac328ca8edbd815199ebc2e7db7a  Constraint/cursor_rules/40-frontend.mdc
10617bfdc33fd5b6dd20e33d5b51ee19d5d7abde1cc22b9254bc2ee82548dd71  Constraint/cursor_rules/50-database.mdc
13de898fcab6237a001fd18b5564cc6bed0521d8edba1bae0f173dd08e11e088  Constraint/cursor_rules/90-safety.mdc
5d9a85c07f69c8da83e19f44c35f9353751c03c729d7275a74e7a78c0a55c0e9  Constraint/cursor_rules/anti-sycophancy.mdc
26947f45c7347f24a2fb9be4fd277fbbecfe196c25439f72eebbab56a2a7c147  Constraint/cursor_rules/code-change-minimalism.mdc
d0ab529450451898b77cfe035dfc2fb6e1d6b6633d81072c8991254bd88a0420  Constraint/cursor_rules/code-line-count-tagging.mdc
f67bcd374f88f5d27fa8569494d436a0e54c9593548d02b390df9aa3b7c16a71  Constraint/cursor_rules/common_rules.mdc
fe470b29b2d40000f6f1b6b61c8043f60bf3d6e0f043a92422f3b3ba8d62f99f  Constraint/cursor_rules/dataverse-query-protocol.mdc
19bd48bc7b37e409204752351beee16dee0850061019a62dae57a837f73c247e  Constraint/cursor_rules/implementation-workflow.mdc
92464da2f53638223b04ddc15e36484edb8266a825b80afc6a6a995f3611d628  Constraint/cursor_rules/mode-gating.mdc
7fc08654cb6c093fd8d32f71ac51ac6c923f61450e031073561cb41140432cf2  Constraint/cursor_rules/python.mdc
cfa228ad9244f971cb4f03211bc52de016392d5a053b1f568040cdfad322f727  Constraint/cursor_rules/zh-collaboration.md
2c85bb1afb3a6fb83c50af2c3b99f6dadd0638a2e3d4f85e9bb755604d290365  Constraint/coding-agent-system/templates/project/AGENTS.md
fa3074d194e62d36e5c46e6af78636b2f898cbd932d2b37c90046684348d0dde  Constraint/Codex_AGENTS.md
5e5e1999567f8dddcdae21b145a7ac3e414943d616eb3586b6e6671f1b0f2779  Constraint/coding-agent-system/templates.zip
af45e076a34778c10aab388d191a563df11694036fb25857ca629605732c5142  全栈开发Prompt Chain.zip
```

## 实施与验证

### 实施内容

- 在 `templates/user/codex/AGENTS.md` 的共享块外新增「用户可见界面的默认偏置」：条件触发、存在时读取项目模块、任务型界面克制、显著性与任务匹配、复用设计语言，以及真实渲染/同屏检查与未验证标记。
- 在 `templates/project/codex/AGENTS.md` 新增「用户可见界面规则路由」：存在项目视觉模块时强制读取，缺失时沿用用户级基线与项目规范并报告缺口；未修改平台中立入口或受管路由块。
- 扩充 `templates/modules/frontend-visual-quality.md`：事实发现、视觉显著性/尺寸/图标规则和视觉检查回归条件均集中于此唯一完整清单。

### 验证命令与原始结果摘要

```text
$ cd Constraint/coding-agent-system && python3 tools/agent_system.py render-templates
DRY-RUN
templates/project/AGENTS.md -> .../templates/project/AGENTS.md
templates/project/codex/AGENTS.md -> .../templates/project/codex/AGENTS.md
templates/project/deepseek-harness/AGENTS.md -> .../templates/project/deepseek-harness/AGENTS.md
templates/user/claude/CLAUDE.md -> .../templates/user/claude/CLAUDE.md
templates/user/codex/AGENTS.md -> .../templates/user/codex/AGENTS.md
templates/user/deepseek-harness/AGENTS.md -> .../templates/user/deepseek-harness/AGENTS.md

$ cd Constraint/coding-agent-system && python3 tools/agent_system.py validate .
VALID
```

未运行 `render-templates --apply`。收尾还执行了：完整不修改清单 SHA-256 比对（原始结果：`unchanged baseline: 31/31 SHA-256 entries match`）、三份目标文件 SHA-256 与 `stat`/`wc`、`file -I` UTF-8 检查，以及 Ruby UTF-8 与 Markdown fence 平衡检查。目标文件均为 UTF-8、围栏数为 0（平衡）。

### 目标文件 after SHA-256 与大小

| 文件 | SHA-256 | native bytes (`stat`) | readable characters (`wc -m`) | 编码 / fences |
| --- | --- | ---: | ---: | --- |
| `Constraint/coding-agent-system/templates/user/codex/AGENTS.md` | `76c7371a0b413ed4c6c9b8fd93a73678ad5c2e959bb06186f0c203c86af830b8` | 9395 | 2275 | UTF-8 / 0 |
| `Constraint/coding-agent-system/templates/project/codex/AGENTS.md` | `d38153c221dc2018239f355bbe9c73af88a5fd84e42bafe641ff6cbccf340d25` | 8138 | 1934 | UTF-8 / 0 |
| `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md` | `11920c5151f699bb4f7dfb647a77ea5b1a524c5e46abe8a486f1fa0dc355fdad` | 8327 | 1725 | UTF-8 / 0 |

### 文件清单

- 修改：`Constraint/coding-agent-system/templates/user/codex/AGENTS.md`
- 修改：`Constraint/coding-agent-system/templates/project/codex/AGENTS.md`
- 修改：`Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`
- 新增：本报告。
- 未修改：上述 31 个共享 core、Claude、DSH、Cursor、平台中立入口、旧 Codex 文件和 zip 文件；收尾 SHA-256 与报告基线一致。

### 自审

- 完整图标、状态和视觉验收规则仅位于 `frontend-visual-quality.md`；两个 Codex `AGENTS.md` 仅保存条件偏置或路由。
- 规则明确保留响应式、状态、键盘、reduced-motion、design token 与禁止单页新增依赖要求。
- 克制默认值不覆盖安全、隐私、无障碍、关键状态、营销/品牌、关键警告或不可逆动作；并且未把 hover、tooltip、颜色或动效作为唯一语义通道。
- 本任务只修改规则模板，没有页面实现，因此未声明实际页面视觉质量已通过。

### Concerns

- Requirement 0 对以下四项的「编辑前」SHA-256 基线**不能证明已满足**：`templates/project/.claude/settings.json`、`templates/user/claude/settings.json`、`templates/user/deepseek-harness/README.md` 和 `cursor_rules/.DS_Store`。初始报告漏列它们，完整 Step 1 清单在目标文件编辑后补足；对工作区的独立报告、审计、manifest 和 checksum 检索未找到带时间的编辑前记录。四者从未是写入目标，且收尾 SHA-256 已记录，但这不能替代缺失的编辑前证据。

## 最终规则审查修正

- 经最终规则审查，用户级「克制」默认值补充了保护语：不得降低可发现性、可读性、可访问性、可见 focus 或对比、交互命中区或风险表达。只修改 `templates/user/codex/AGENTS.md` 的紧凑偏置，未复制模块完整清单。
- 当前用户文件的逻辑路径 SHA-256（`shasum -a 256 FILE`）为 `4c479667ab4197510e75a31f30b839e8081e26b43fbd069ce830cf034eb1eff1`；其 pathname 可读流 SHA-256（`/bin/cat FILE | shasum -a 256`）相同。
- 当前双视图仍存在：`/usr/bin/stat -f %z FILE` 为 9513 native bytes，而 `/bin/cat FILE | /usr/bin/wc -c` 为 5417 readable bytes。两者均原样记录；本次未进行任何 normalizing，Task 5 负责最终 normalizing。
- 修正后 `python3 tools/agent_system.py render-templates` 仍为 dry-run 既有目标，`python3 tools/agent_system.py validate .` 输出 `VALID`；用户文件 UTF-8 有效、Markdown fences 为 0。
