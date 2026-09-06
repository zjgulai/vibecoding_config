# Task 5: 全量验证、双视图归一化与最终证据

## Context

Tasks 1–4 已完成并通过独立审查；22 个交付文件的语义内容现已冻结。本任务先验证 logical-readable 内容，再依已修正计划安全归一化 pathname/logical 双视图，最后重跑全套检查并形成可复核 manifest。本目录不是 Git 仓库，不 commit。除计划明确的内容保持不变的机械归一化外，不得改动交付语义。

开始前完整阅读：

- `全栈开发Prompt Chain/docs/superpowers/specs/2026-09-02-ui-visual-restraint-integration-design.md`
- `全栈开发Prompt Chain/docs/superpowers/plans/2026-09-02-ui-visual-restraint-integration.md` 的 Global Constraints 与已修正 Task 5 全节
- `progress.md`、`task-1-report.md`、`task-2-report.md`、`task-3-report.md`、`task-4-report.md`
- 22 个交付文件的 logical-readable UTF-8 内容

## Authorization and exact scope

- 允许执行 Task 5 Steps 1–5 的只读校验、`/tmp/codex-ui-rule.*` 隔离项目初始化，以及计划内 22 个静态 allowlist 文件的内容保持不变归一化。
- 归一化只能把每个文件当前 `/bin/cat` logical-readable 字节原样写入同目录临时文件，经 hard-link backup、fsync、原子 `/bin/mv` 和四重校验后替换；logical size 或 SHA-256 不得变化。
- 允许删除归一化产生且已逐路径校验的唯一临时 hard-link backup；不得使用递归删除、glob 删除或宽目录目标。隔离 `/tmp` 项目不删除。
- 不允许语义性编辑 22 个文件。若任一验证或后续审查发现需改内容，停止并报告，由父任务另行给出精确修复范围。
- 允许创建：`全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-5-report.md`。
- 不修改真实 `~/.codex/AGENTS.md`，不修改 31 个保护文件、其他平台、zip 或计划/brief。

## Frozen logical-readable manifest

以下 SHA-256 与 bytes 由 `/bin/cat` logical-readable stream 于 Task 4 通过 scoped review 后采集。Step 5 前后必须逐项一致；任一不一致即 BLOCKED，不得用归一化覆盖。

```text
76c7371a0b413ed4c6c9b8fd93a73678ad5c2e959bb06186f0c203c86af830b8 bytes=5299 Constraint/coding-agent-system/templates/user/codex/AGENTS.md
d38153c221dc2018239f355bbe9c73af88a5fd84e42bafe641ff6cbccf340d25 bytes=4042 Constraint/coding-agent-system/templates/project/codex/AGENTS.md
11920c5151f699bb4f7dfb647a77ea5b1a524c5e46abe8a486f1fa0dc355fdad bytes=4231 Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md
0c57930d6861f9488fccf05ab80af8ffae18eb348d02aaf63678f628c0d59bd1 bytes=1828 Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md
d1b72b3c14593ccf489c2c3c9b09f0d4750e1ec9708bf3fc3357db9a32a6d32e bytes=39277 Constraint/coding-agent-system/docs/sop/project-lifecycle.md
4331ad34d605fa315657574ea090140ddb4be9b8d2339323bb52f835739b0d09 bytes=18051 Constraint/coding-agent-system/docs/research/local-tip-ledger.md
7654502503284a7babb5d6108a387dadb9d870c91860dc6cef75cd72d1fb9396 bytes=24670 Constraint/coding-agent-system/docs/research/tip-decision-matrix.md
9ca8aa6698a17252cfcb4c8ff4d16fed5cf3d7041f8ec3aa08c922dd4e69bada bytes=16229 Constraint/coding-agent-system/docs/research/local-material-audit.md
43811539e42fb0934e91ead0a45ab73d717f8677a015192ef3ee7e5d19d675f5 bytes=24036 Constraint/coding-agent-system/sources/rule-traceability.json
fc51f093b5e9eae7e4e834e13e64cd537c0f3713bf6cab36c6c094c86f2e5ba0 bytes=27468 全栈开发Prompt Chain/04-模块化Skills工作流.md
b9d03c70893902253b281c0231d49dda6576005164ccd116367f2a94729b3547 bytes=8834 全栈开发Prompt Chain/06-Prompt-Chain使用手册.md
2d4f44df5b26bc825b7137f9a1d81dfc7ea46ca2cb4e8f94608ce87c9031f38f bytes=6770 全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md
813932012a7c74d455cd7931a2c380e9320edaa45a7c89be1052e831e474f505 bytes=4151 全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md
492560544495d04932ccbc73e3d22850f55e29b70fe60f052f6496473f914d73 bytes=4395 全栈开发Prompt Chain/prompts/06-原型与UX验证.md
7a55bc6f18e0a43464882b6b9f659cfd9cd78a4cd60dd540b412b7cab4a98bf4 bytes=4254 全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md
dc278f16f93a96bdc3ce3d29dde4934ce0b2045513fc10afdc0d79ca458f4785 bytes=5196 全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md
4a15a3688ad96079ce0d64ba61e058d38f6a576a370bcffd0354d0470f224151 bytes=4878 全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md
7204fc389a3adefe9cfa5044d0bbe82c0c43de218e9be16d0cdb0a0aaade60d0 bytes=5658 全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md
400a9e41b5398e27dace92ae07275e2b701af2beaaca7e99ede36047334afb7c bytes=5329 全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md
1d52e5076b62947d76915d479387bdc4c8cca4061ba3d96384970c3c67eeae48 bytes=5318 全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md
bd56bfe6a2753ddebbff2fb64fa97dcf7990ff886ccbe62d7485cd0fdbc5feeb bytes=6616 全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md
2932debd09320393ca2299798dbdd8be32aefbb0360a3346fca17984af6c51f9 bytes=6103 全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md
```

## Requirements

1. 在任何归一化前逐项复核 frozen manifest，执行 Task 5 Steps 1–4 的原文命令并保存完整摘要：
   - `render-templates` 仅说明渲染目标；`validate . = VALID` 才是 shared drift 检查证据。
   - 117 项或当前实际数量的全部单元测试通过；不得假定数量。
   - 隔离项目位于经守卫的 `/tmp/codex-ui-rule.*`，`VALID-GENERATED`、根路由与 `cmp` 均通过；保留输出路径，不递归删除。
   - `FINAL_PROMPT_CONTRACT=PASS`。
   - `PROTECTED_MANIFEST=PASS files=31`，并明确它只证明当前等于 Task 1 清单；四个后补文件的编辑前缺口仍不可恢复。
2. 只有 Requirements 1 全部通过、logical content 与 frozen manifest 逐项相同且所有 writer 停止时，才执行计划 Task 5 Step 5 的原文安全归一化脚本。
3. 归一化必须使用计划中的静态 22 文件 allowlist，逐项验证 regular/non-symlink/link count/flags/xattr/ACL。不得临时扩大路径或跳过守卫。
4. 对每个双视图差异文件，保留其 logical bytes/hash，保留 mode/mtime，验证同目录 temp 的 native/logical size/hash 后才建唯一 hard-link backup 和原子替换；失败按计划用明确 backup 回滚并停止。
5. 归一化完成后必须确认：
   - frozen logical manifest 22/22 完全不变。
   - 每个文件 pathname/native 与 logical-readable size/hash 四重一致。
   - 21 个 Markdown 均为有效 UTF-8 且 fences 平衡。
   - 输出 22 行逐文件 `hash + bytes + path` 与 aggregate `manifest_sha256`。
6. 若任何文件被归一化，重新执行 Tasks 5 Steps 1–5；第二轮不得再次输出 `NORMALIZED`，并保存新的完整新鲜证据。
7. 检查所有归一化 temp/backup 路径：成功路径无遗留 `.normalize.*` 或 `.pre-normalize-*`；只能对本次精确记录路径做清理，禁止 glob/递归删除。报告实际移除的临时 hard-link backup 数量；这些只是本次可恢复临时副本。
8. 创建 `task-5-report.md`，包含：结论、精确机械写入文件、logical 内容不变证据、每条命令/退出状态、单元测试数、隔离路径、31 文件边界、逐文件最终 manifest、aggregate hash、临时备份清理、未验证范围和 concerns。不得先创建最终 `final-review-report.md`；三路独立审查后由父任务汇总。
9. 明确未运行真实页面回放、截图/视觉回归或真实 Codex 行为基准；`EVAL-05` 仍是 `contract-only`。

## Return format

返回 `DONE`、`DONE_WITH_CONCERNS` 或 `BLOCKED`，列出实际被归一化的精确文件、所有验证结论、aggregate manifest、临时备份处理和报告绝对路径。若发生任何逻辑哈希变化或无法可靠回滚，返回 BLOCKED，禁止继续。
