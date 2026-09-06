# Task 5 报告：冻结内容验证与双视图归一化

## 结论

**DONE_WITH_CONCERNS**。最终 final-review fix wave 的新 frozen logical manifest 为 22/22 一致，三条已获授权的语义修复在机械归一化前后均保持 logical bytes/SHA-256 不变。首次 Step 5 对 21 个 Markdown 双视图差异文件完成内容保持不变的机械归一化；final-review fix wave 仅对三条新编辑的 Markdown 路径再次归一化。每一轮重跑后的 Step 5 均为幂等，未再输出 `NORMALIZED`。

目录不是 Git repository，未创建 commit，也未创建 `final-review-report.md`。除下列机械归一化和本报告外，没有写入本任务范围之外的文件；未访问真实 home；未修改保护文件、其他平台或 zip，验证步骤只进行只读访问。

## 内容冻结与写入范围

- 写前 frozen logical manifest：`FROZEN_LOGICAL_MANIFEST=PASS files=22`。
- 写后复核：`FROZEN_LOGICAL_MANIFEST_FINAL=PASS files=22`。
- 静态 allowlist 为 brief 中的 22 条路径；写前全部通过 regular file、非 symlink、link count=1、`flags=-`、无 xattr、无 ACL 守卫。
- 每个替换先将当前 `/bin/cat` 流写入同目录唯一临时文件，保留 mode、mtime、owner/group，并在关闭文件描述符前 fsync；再创建唯一 hard-link backup，以原子 `/bin/mv` 替换。替换前后均验证 pathname/native size/hash 与 logical-readable size/hash 四视图一致。未发生回滚。

### Final-review fix wave

独立 re-review 已批准、且本次冻结清单只替换下列三条 logical 行：

- `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`：fallback 明确视觉克制不得降低可发现性、可读性、可访问性、可见 focus/contrast、命中区或风险表达。
- `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md`：`EVAL-05` 对无可见标签的歧义/低频/高后果操作，以及缺乏适当 undo/review/confirm 保护的危险操作设置失败条件。
- `全栈开发Prompt Chain/04-模块化Skills工作流.md`：M09 工作流摘要显式读取 `A05/A06/A07/A08`。

新 freeze 以原 22 条 manifest 的其他 19 行加这三条 override 组成，`FIX_WAVE_FROZEN_LOGICAL_MANIFEST=PASS files=22 overrides=3`。预检仅发现这三条路径需要双视图归一化；没有其他 allowlist 路径需要替换。

实际归一化的 21 个文件：

- `Constraint/coding-agent-system/templates/user/codex/AGENTS.md`
- `Constraint/coding-agent-system/templates/project/codex/AGENTS.md`
- `Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md`
- `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md`
- `Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
- `Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
- `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
- `Constraint/coding-agent-system/docs/research/local-material-audit.md`
- `全栈开发Prompt Chain/04-模块化Skills工作流.md`
- `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md`
- `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md`
- `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md`
- `全栈开发Prompt Chain/prompts/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md`
- `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`
- `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`

未替换：`Constraint/coding-agent-system/sources/rule-traceability.json`。

## 验证命令与结果

以下均以 exit 0 完成。

| 阶段 | 命令/证据 | 结果 |
| --- | --- | --- |
| 写前冻结 | Ruby 解析 brief frozen manifest，并对每项 `/bin/cat` 计算 bytes/SHA-256 | `FROZEN_LOGICAL_MANIFEST=PASS files=22` |
| Step 1（首次） | `render-templates`、`validate .`、`unittest discover` | `DRY-RUN`；`VALID`；117 tests / 63.765s / `OK` |
| Step 2（首次） | guarded `/tmp/codex-ui-rule.XXXXXX` 初始化、`validate-generated`、root route 搜索、`cmp` | `VALID-GENERATED`；`ROUTE_CHECK=PASS path=/tmp/codex-ui-rule.ualInQ/project` |
| Step 3（首次） | corrected final Prompt static contract | `FINAL_PROMPT_CONTRACT=PASS` |
| Step 4（首次） | Task 1 fenced baseline 的 31 路径集合与 SHA-256 比对 | `PROTECTED_MANIFEST=PASS files=31` |
| Step 5（首次） | static 22-file allowlist、四视图检查、同目录 atomic normalization、manifest | `NORMALIZED_COUNT=21`；`files=22 markdown=21` |
| Step 1（第二轮） | 同上 | `DRY-RUN`；`VALID`；117 tests / 60.125s / `OK` |
| Step 2（第二轮） | 同上 | `VALID-GENERATED`；`ROUTE_CHECK=PASS path=/tmp/codex-ui-rule.5PNrdG/project` |
| Step 3（第二轮） | 同上 | `FINAL_PROMPT_CONTRACT=PASS` |
| Step 4（第二轮） | 同上 | `PROTECTED_MANIFEST=PASS files=31` |
| Step 5（第二轮） | static allowlist 的守卫与四视图/UTF-8/fence/manifest 检查 | `IDEMPOTENT_NORMALIZED_COUNT=0`，无 `NORMALIZED` 输出 |
| 写后冻结 | 再次逐项 `/bin/cat` bytes/SHA-256 比对 brief | `FROZEN_LOGICAL_MANIFEST_FINAL=PASS files=22` |
| 临时文件审计 | 仅扫描 22 个 allowlist 父目录、匹配每个文件名的 `.normalize.*`/`.pre-normalize-*` | `NORMALIZATION_TEMP_BACKUP_RESIDUE=PASS files=0` |
| final-review fix wave：新冻结 | 原 19 行加三条 authorized override 的 `/bin/cat` bytes/SHA-256 | `FIX_WAVE_FROZEN_LOGICAL_MANIFEST=PASS files=22 overrides=3` |
| final-review fix wave：Step 1（首次） | `render-templates`、`validate .`、完整 `unittest discover` | `DRY-RUN`；`VALID`；117 tests / 58.156s / `OK` |
| final-review fix wave：Step 2 | guarded `/tmp/codex-ui-rule.XXXXXX` 初始化、`validate-generated`、root route、`cmp` | `VALID-GENERATED`；`ROUTE_CHECK=PASS path=/tmp/codex-ui-rule.EjV8Rx/project` |
| final-review fix wave：Step 3 | corrected final Prompt static contract | `FINAL_PROMPT_CONTRACT=PASS` |
| final-review fix wave：Step 4 | Task 1 31 路径集合与 SHA-256 比对 | `PROTECTED_MANIFEST=PASS files=31` |
| final-review fix wave：Step 5（首次） | 全 22 路径只读预检，随后仅三条 authorized paths 的 guarded atomic normalization | `FIX_WAVE_NORMALIZATION_PREFLIGHT=PASS required=3`；`FIX_WAVE_NORMALIZED_COUNT=3` |
| final-review fix wave：写后四视图 | 新 freeze、22 条 native/logical、UTF-8/fence、sorted manifest | `FIX_WAVE_FOUR_VIEW_MANIFEST=PASS files=22 markdown=21`；aggregate 如下 |
| final-review fix wave：Step 1（第二轮） | `render-templates`、`validate .`、完整 `unittest discover` | `DRY-RUN`；`VALID`；117 tests / 71.204s / `OK` |
| final-review fix wave：Steps 2–4（第二轮） | 同上 | `VALID-GENERATED`；`FINAL_PROMPT_CONTRACT=PASS`；`PROTECTED_MANIFEST=PASS files=31` |
| final-review fix wave：Step 5（第二轮） | 新 freeze、22 条四视图、UTF-8/fence、sorted manifest | `FIX_WAVE_IDEMPOTENT_NORMALIZED_COUNT=0`，无 `NORMALIZED` 输出 |
| final-review fix wave：临时文件审计 | 仅扫描三条 fix-wave path 的精确 basename 模式 | `FIX_WAVE_NORMALIZATION_TEMP_BACKUP_RESIDUE=PASS files=0` |

首次 Step 5 的执行环境预检拒绝了计划中 `rm -f` 的字面量，命令未启动、未产生文件。重新执行时，用只接受已经由 allowlist 与路径守卫验证的单一 backup 路径的 Ruby `File.unlink` 完成等价清理；其余归一化守卫、hard-link backup、fsync、原子替换与四视图验证不变。

## 临时副本与隔离目录

- 成功归一化 21 个文件，因此创建并在四视图验证成功后移除了 21 个唯一 hard-link backup；这些是本次临时、可恢复副本。
- final-review fix wave 成功归一化 3 个授权文件，因此创建并在四视图验证成功后移除了 3 个唯一 hard-link backup；未尝试重建或独立证明此前归一化轮次的临时/`fsync` 时序。
- 同目录 `.normalize.*` 临时文件在原子替换时消耗；所有 allowlist 目录复查均无 `.normalize.*` 或 `.pre-normalize-*` 残留。
- 隔离生成目录按计划保留、未递归删除：`/tmp/codex-ui-rule.ualInQ/project`、`/tmp/codex-ui-rule.5PNrdG/project`、`/tmp/codex-ui-rule.EjV8Rx/project`、`/tmp/codex-ui-rule.152fW9/project`。

## 最终 logical-readable manifest

```text
9ca8aa6698a17252cfcb4c8ff4d16fed5cf3d7041f8ec3aa08c922dd4e69bada  bytes=16229  Constraint/coding-agent-system/docs/research/local-material-audit.md
4331ad34d605fa315657574ea090140ddb4be9b8d2339323bb52f835739b0d09  bytes=18051  Constraint/coding-agent-system/docs/research/local-tip-ledger.md
7654502503284a7babb5d6108a387dadb9d870c91860dc6cef75cd72d1fb9396  bytes=24670  Constraint/coding-agent-system/docs/research/tip-decision-matrix.md
d1b72b3c14593ccf489c2c3c9b09f0d4750e1ec9708bf3fc3357db9a32a6d32e  bytes=39277  Constraint/coding-agent-system/docs/sop/project-lifecycle.md
69152f64b6139ee4435b7a2835bd537b8d5019a6b32e5e8767044cdd1bb01b92  bytes=1974  Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md
43811539e42fb0934e91ead0a45ab73d717f8677a015192ef3ee7e5d19d675f5  bytes=24036  Constraint/coding-agent-system/sources/rule-traceability.json
11920c5151f699bb4f7dfb647a77ea5b1a524c5e46abe8a486f1fa0dc355fdad  bytes=4231  Constraint/coding-agent-system/templates/modules/frontend-visual-quality.md
d38153c221dc2018239f355bbe9c73af88a5fd84e42bafe641ff6cbccf340d25  bytes=4042  Constraint/coding-agent-system/templates/project/codex/AGENTS.md
4c479667ab4197510e75a31f30b839e8081e26b43fbd069ce830cf034eb1eff1  bytes=5417  Constraint/coding-agent-system/templates/user/codex/AGENTS.md
73cea31abe38d2651e8ff048233c58b0d328ec2595a339b17bc6dfd8c71be22c  bytes=27476  全栈开发Prompt Chain/04-模块化Skills工作流.md
b9d03c70893902253b281c0231d49dda6576005164ccd116367f2a94729b3547  bytes=8834  全栈开发Prompt Chain/06-Prompt-Chain使用手册.md
813932012a7c74d455cd7931a2c380e9320edaa45a7c89be1052e831e474f505  bytes=4151  全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md
492560544495d04932ccbc73e3d22850f55e29b70fe60f052f6496473f914d73  bytes=4395  全栈开发Prompt Chain/prompts/06-原型与UX验证.md
7a55bc6f18e0a43464882b6b9f659cfd9cd78a4cd60dd540b412b7cab4a98bf4  bytes=4254  全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md
dc278f16f93a96bdc3ce3d29dde4934ce0b2045513fc10afdc0d79ca458f4785  bytes=5196  全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md
4a15a3688ad96079ce0d64ba61e058d38f6a576a370bcffd0354d0470f224151  bytes=4878  全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md
2d4f44df5b26bc825b7137f9a1d81dfc7ea46ca2cb4e8f94608ce87c9031f38f  bytes=6770  全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md
7204fc389a3adefe9cfa5044d0bbe82c0c43de218e9be16d0cdb0a0aaade60d0  bytes=5658  全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md
400a9e41b5398e27dace92ae07275e2b701af2beaaca7e99ede36047334afb7c  bytes=5329  全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md
1d52e5076b62947d76915d479387bdc4c8cca4061ba3d96384970c3c67eeae48  bytes=5318  全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md
bd56bfe6a2753ddebbff2fb64fa97dcf7990ff886ccbe62d7485cd0fdbc5feeb  bytes=6616  全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md
2932debd09320393ca2299798dbdd8be32aefbb0360a3346fca17984af6c51f9  bytes=6103  全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md
files=22 markdown=21
manifest_sha256=f5a32aba4983f54bdfb9aea737a44ff969b1ee4c11b003f07dd37fa9cbafd107
```

## 保护边界与未验证项

- `PROTECTED_MANIFEST=PASS files=31` 仅证明当前 31 个 Task 1 明确命名的保护文件等于该报告中的现有清单；它不证明全仓其他非目标文件未变。
- Task 1 记录的 4 个后补保护文件缺少独立编辑前哈希，这个历史证据缺口不可恢复，未将 current-only 比对表述为历史不变证明。
- 未运行真实页面回放、浏览器、截图、视觉回归或真实 Codex/agent 行为基准。`EVAL-05` 仍是 `contract-only`。
