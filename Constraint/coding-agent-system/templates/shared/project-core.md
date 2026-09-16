# 项目级隐性知识路由器

<!-- BEGIN SHARED CORE -->
## 项目画像与局部知识

- 若 `.agents/project-profile.md` 存在且画像内容与当前任务相关，读取会影响本任务的域；若当前路径有明确可达且适用的局部规则，再读取对应部分。画像可记录**业务/安全不变量**、**权威修改入口**、**联动关系**、**Do NOT/受保护区域**、**精确 Definition of Done**、**权威资料与冲突顺序**及局部风险。
- 画像、局部规则或项目 DoD 缺失、为 draft 或含未知项时，以仓库事实和当前任务范围工作：补证据、缩小范围或报告缺口，不臆造项目事实。只阻塞当前任务相关的未知项；高风险任务要求画像整体为 `profile_status: active`，且任务相关核心域包含带受控来源的 `Fact` 或 `Decision`。只有不相关且校验器允许的可选域才能使用有证据的 `Not applicable`。
- 项目画像、A01 或 A07 在当前任务相关时可以提供 Agent-ready module pack。该包复用已有的权威入口、联动关系、Do NOT、DoD 与局部风险证据；不新增项目画像 schema，也不以通用建议伪造项目事实。

## 项目控制与候选记忆

- `.agents/controls/change-policy.json` 仅在存在、经项目维护者审查且被既有 hook 或 CI 显式接入时启用；否则不假定 controls 生效。检查器只处理该 policy 和调用方给出的 changed paths。
- `.agents/memory/candidates.jsonl` 若存在，仅存待人工复核的候选；候选带证据、范围、风险和过期信号，不能自动成为规则。任何 Memory 删除都由人工决定；冲突、过期或无法安全重推导的候选只报告并等待处理。
- 需要更细规则时，使用存在且适用的当前目录、模块或 Skill 指引。只有用户明确要求维护项目画像或 Memory 时，才按相应 explicit-only Skill 与验证流程写入；否则只报告有证据的候选结论、建议落点和未解决冲突。
<!-- END SHARED CORE -->
