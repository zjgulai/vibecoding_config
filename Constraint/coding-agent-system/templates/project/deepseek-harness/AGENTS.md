# DSH Desktop / DeepSeek Harness 项目级 AGENTS.md

> 将本文件复制为目标项目根目录的 `AGENTS.md`；不要把 `deepseek-harness/` 目录本身复制进目标项目。若同一项目同时使用 Codex 与 DSH Desktop，优先采用 `templates/project/AGENTS.md` 的平台中立版本。

<!-- BEGIN SHARED CORE -->
## 项目画像与局部知识

- 若 `.agents/project-profile.md` 存在且画像内容与当前任务相关，读取会影响本任务的域；若当前路径有明确可达且适用的局部规则，再读取对应部分。画像可记录**业务/安全不变量**、**权威修改入口**、**联动关系**、**Do NOT/受保护区域**、**精确 Definition of Done**、**权威资料与冲突顺序**及局部风险。
- 画像、局部规则或项目 DoD 缺失、为 draft 或含未知项时，以仓库事实和当前任务范围工作：补证据、缩小范围或报告缺口，不臆造项目事实。只阻塞当前任务相关的未知项；高风险任务要求画像整体为 `profile_status: active`，且任务相关核心域包含带受控来源的 `Fact` 或 `Decision`。只有不相关且校验器允许的可选域才能使用有证据的 `Not applicable`。

## 项目控制与候选记忆

- `.agents/controls/change-policy.json` 仅在存在、经项目维护者审查且被既有 hook 或 CI 显式接入时启用；否则不假定 controls 生效。检查器只处理该 policy 和调用方给出的 changed paths。
- `.agents/memory/candidates.jsonl` 若存在，仅存待人工复核的候选；候选带证据、范围、风险和过期信号，不能自动成为规则。任何 Memory 删除都由人工决定；冲突、过期或无法安全重推导的候选只报告并等待处理。
- 需要更细规则时，使用存在且适用的当前目录、模块或 Skill 指引。只有用户明确要求维护项目画像或 Memory 时，才按相应 explicit-only Skill 与验证流程写入；否则只报告有证据的候选结论、建议落点和未解决冲突。
<!-- END SHARED CORE -->

## DSH Desktop / DeepSeek Harness 项目适配

- 以下规则以 DSH Desktop 使用官方 DeepSeek Harness，且当前 preset / spine 已启用 `agent-instructions`、skill registry、tool consumer 与 skill filesystem plugins 为前提。自定义 bundle 可以禁用或替换这些能力，必须做版本级 smoke test。
- 把本文件放在项目根并命名为 `AGENTS.md`。同目录内所有内容不同的 base candidates 会加载并去重，local overlays 后加载；不要维护内容重复或冲突的根候选。
- 默认项目根标记为 `.git`。Harness 首次请求加载项目根到当前 cwd 的适用链；成功的第一方 `read`、`write` 或 `edit` 触达更深目录后，后续请求可能动态加入新规则，shell `cd` 不会触发。局部规则应短小、自包含且不重复根契约。
- 指令受 `maxBytes` 预算约束；预算不足时优先保留更具体文件。根文件只放稳定规则，长流程进入 skill，语言和框架约束放在明确路由的项目文件或就近目录。
- 默认 skill 项目根取最近的 `.git` 祖先；找不到 Git 根时回退到启动 cwd。无 Git 项目必须从真正的项目根启动，否则根 `AGENTS.md` 与 `.agents/skills/` 可能不在预期发现范围。
- 共享 skills 放在 `.agents/skills/`；需要 DSH 专属调用控制的同名适配可放 `.dsh/skills/`。同名优先级和调用字段必须按当前 Harness 版本核验，不能把文件存在当成已加载。
- Harness 不解释 `.claude/rules` 或 Claude Code 的 `@path` import。若工具访问 `.claude/` 后动态发现 `.claude/CLAUDE.md`，其中内容会作为普通文本；该文件不得追加与根契约冲突或重复的 DSH 指令。最终 symlink 可跨越 trust boundary，不要把可读路径当作信任或授权证明。
- DeepSeek Harness 仍处于 developer preview。本项目文件不写入未经核实的 provider、model、权限或项目 settings；升级 DSH Desktop / Harness 后重新验证发现链、预算和 skill 调用行为。

## 项目定制原则

- 用户明确要求维护项目知识时，才把当前仓库有证据的业务不变量、真实架构入口、联动关系、测试命令、生成流程和受保护区域写入 `.agents/project-profile.md`；只对某目录生效的约束放就近规则，不在本平台后缀复制第二份项目事实。其他任务只报告候选与建议落点。
- 共享块之外只保留已核实的 Harness 平台差异。只有在明确的画像或规则维护请求中才更新权威条目、处理过期内容；不得自动删除 Memory 或正式规则，也不要把临时任务计划、个人偏好、模型名称或快速失效的外部状态写进根规则。
