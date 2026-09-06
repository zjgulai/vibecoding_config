# Codex 项目级 AGENTS.md

> 将本文件复制为目标项目根目录的 `AGENTS.md`；不要把 `codex/` 目录本身复制进目标项目。若同一项目同时使用 Codex 与 DSH Desktop，优先采用 `templates/project/AGENTS.md` 的平台中立版本。

<!-- BEGIN SHARED CORE -->
## 项目画像与局部知识

- 若 `.agents/project-profile.md` 存在且画像内容与当前任务相关，读取会影响本任务的域；若当前路径有明确可达且适用的局部规则，再读取对应部分。画像可记录**业务/安全不变量**、**权威修改入口**、**联动关系**、**Do NOT/受保护区域**、**精确 Definition of Done**、**权威资料与冲突顺序**及局部风险。
- 画像、局部规则或项目 DoD 缺失、为 draft 或含未知项时，以仓库事实和当前任务范围工作：补证据、缩小范围或报告缺口，不臆造项目事实。只阻塞当前任务相关的未知项；高风险任务要求画像整体为 `profile_status: active`，且任务相关核心域包含带受控来源的 `Fact` 或 `Decision`。只有不相关且校验器允许的可选域才能使用有证据的 `Not applicable`。

## 项目控制与候选记忆

- `.agents/controls/change-policy.json` 仅在存在、经项目维护者审查且被既有 hook 或 CI 显式接入时启用；否则不假定 controls 生效。检查器只处理该 policy 和调用方给出的 changed paths。
- `.agents/memory/candidates.jsonl` 若存在，仅存待人工复核的候选；候选带证据、范围、风险和过期信号，不能自动成为规则。任何 Memory 删除都由人工决定；冲突、过期或无法安全重推导的候选只报告并等待处理。
- 需要更细规则时，使用存在且适用的当前目录、模块或 Skill 指引。只有用户明确要求维护项目画像或 Memory 时，才按相应 explicit-only Skill 与验证流程写入；否则只报告有证据的候选结论、建议落点和未解决冲突。
<!-- END SHARED CORE -->

## Codex 项目适配

- 每次运行仅构造一条指令链：项目从 root 到 cwd，每目录依次在 override、`AGENTS.md`、fallback 中取一份，近目录内容后置。全局 override 与全局 `AGENTS.md` 同样二选一；不要依赖同目录的重复文件叠加。
- 项目指令链受 `project_doc_max_bytes` 预算限制，当前官方默认值为 32 KiB。根文件保持稳定、紧凑；长方法放按需 Skill，技术栈规则可放在相关子目录或由根 `AGENTS.md` 明确路由。
- `.agents/rules/` 不会自动生效；只有根指针或显式读取才可用。Skill 采用渐进披露：先依据元数据发现，任务相关时才读取正文和 supporting resources。
- 项目 `.codex/config.toml` 只在受信任项目中加载。不要在共享项目配置中写个人模型、provider、凭据，也不要降低用户或组织层的 approval 与 sandbox 基线。
- 本文件补充 Codex 内置 base instructions，不替换它，也不保证 permissions、sandbox、hook 或工具行为；这些能力必须按当前客户端版本单独配置和验证。

## 用户可见界面规则路由

- UI 任务且 `.agents/rules/frontend-visual-quality.md` 存在时必须读取该模块；不存在时沿用用户级基线和项目既有规范，报告模块缺口，不臆造文件或规则。

## 项目定制原则

- 用户明确要求维护项目知识时，才把当前仓库有证据的业务不变量、真实架构入口、联动关系、测试命令、生成流程和受保护区域写入 `.agents/project-profile.md`；只对某目录生效的约束放就近规则，不在本平台后缀复制第二份项目事实。其他任务只报告候选与建议落点。
- 共享块之外只保留已核实的 Codex 平台差异。只有在明确的画像或规则维护请求中才更新权威条目、处理过期内容；不得自动删除 Memory 或正式规则，也不要把临时任务计划、个人偏好、模型名称或快速失效的外部状态写进根规则。
