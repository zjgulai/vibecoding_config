# UI 视觉克制规则融合最终审查报告

## 结论

**PASS_WITH_DOCUMENTED_LIMITATIONS**。用户经验已作为 Codex-only 的条件性 UI 工作契约，融入用户级模板、项目级路由、单一视觉质量模块、EVAL/SOP/来源追溯以及 M05–M09 普通版和对话版 Prompt Chain。三路最终语义审查与一路独立机械证据复核均通过，没有未关闭的 Critical、Important 或 Minor finding。

本次只更新配置素材，没有写入真实 `~/.codex/AGENTS.md`；没有修改 shared core、Claude、DeepSeek Harness、Cursor、平台中立根模板、旧 `Constraint/Codex_AGENTS.md` 或 zip。

## 实际改动

- Codex 配置层：更新用户级 `AGENTS.md` 模板和项目级 `AGENTS.md` 路由，新建 `frontend-visual-quality.md` 作为完整规则的单一事实源。
- 评测与治理层：新建 `EVAL-05`，补全项目生命周期 SOP，并将本地经验记录为 `LOC-030 → TIP-077 → RUL-022 → artifacts → EVAL-05` 可追溯链。
- Prompt Chain 层：在 M05 定义可观察验收、M06 验证 UI 假设、M07 传递约束、M08 实现与同屏复核、M09 独立审查；同步普通版、人与 AI 对话版、模块工作流、使用手册和端到端控制器。
- 最终审查后关闭三个小缺口：用户级 fallback 补齐可访问性守门；`EVAL-05` 补齐显示标签和危险动作保护 oracle；M09 工作流摘要显式读取 `A05/A06/A07/A08`。

## 采用、条件化与排除

| 处理 | 内容 | 原因 |
| --- | --- | --- |
| 采用 | 视觉显著性与任务重要性、后果和紧迫性匹配；常见动作优先既有图标家族、系统符号或行业通用隐喻；实现后检查真实渲染与同屏重量。 | 这些规则可观察、可验收，并能直接防止辅助控件抢占主任务。 |
| 条件化 | 任务型产品默认克制；营销/品牌、关键警告和不可逆动作可根据规格、任务或风险加强表达。`hover`/`tooltip`/动效只能补充，不能承担唯一核心语义。 | 保留原经验的默认偏置，同时避免对营销、安全和品牌场景产生错误的绝对约束。 |
| 条件化 | 真实视觉检查只使用项目已有或当前环境明确可用且已授权的工具；不可用或未授权时必须记录 `Visual verification: not run`。 | 视觉验收要求不应隐式扩大 browser、screenshot、network、dependency 或外部工具权限。 |
| 排除 | 统一写死尺寸、间距、圆角或其他像素值；对大尺寸、重色块、阴影、渐变作无例外禁令。 | 它们与 viewport、信息密度、平台惯例、design tokens、品牌和风险场景相冲突。 |
| 排除 | 为单页新增图标/组件依赖，以及将完整视觉清单复制到每个 Prompt。 | 前者扩大依赖与变更范围；后者会制造多个事实源和后续漂移。 |

## 验证证据

- Coding Agent system：`render-templates` dry-run 通过，`validate .` 返回 `VALID`；独立复核重跑 117 项单元测试，90.151s，`OK`。
- 生成路由：隔离目录的 `init-project` / `validate-generated` / root route / module `cmp` 通过。
- Prompt：`FINAL_PROMPT_CONTRACT=PASS`；13 份对话 Prompt 保留 104/104 公共标题、单问题协议和确认生成门。
- 内容与文件系统：`FIX_WAVE_MANIFEST=PASS files=22 overrides=3`；`FOUR_VIEW_ALL=PASS files=22`；`UTF8_FENCES=PASS markdown=21`；`NORMALIZATION_RESIDUE=PASS files=0`。
- 保护边界：`PROTECTED_MANIFEST=PASS files=31`，只证明这 31 个明确命名的文件与 Task 1 后补基线当前一致。
- 机械归一化：初始轮对 21 个 Markdown 执行内容保持的原子替换；最终修复轮仅对 3 个已授权文件执行同样操作，随后重跑得到 `FIX_WAVE_IDEMPOTENT_NORMALIZED_COUNT=0`。共 24 个临时 hard-link backup 在各自成功验证后移除，无 `.normalize.*` 或 `.pre-normalize-*` 残留。历史临时/调用时序无法由最终文件系统独立重建，本报告不将其表述为当前状态证明。
- 独立审查：规则/可访问性、Prompt 生命周期、平台/授权边界以及 Task 5 机械证据复核均为 `PASS`，最终 0 Critical / 0 Important / 0 Minor。

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

## 保留边界

- Task 1 的 4 个后补保护文件没有独立编辑前哈希；这个历史证据缺口不可恢复，当前 31 文件比对不能被表述为全部历史未变。
- 未运行真实页面回放、浏览器、截图、视觉回归或真实 Codex/agent 行为基准；`EVAL-05` 仍是 `contract-only`。
- 归一化的 24 个临时 hard-link backup 已移除，不可恢复；它们只是同次内容保持替换的短期回滚点。四个隔离 `/tmp/codex-ui-rule.*` fixture 依计划保留，未进行递归删除。
- 目录不是 Git repository，因此没有 branch、diff 或 commit 证据；本次未创建 commit。
