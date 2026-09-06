# Task 2 实施报告：UI 规则 SOP、行为评测与来源追踪

## 结论

**DONE**。当前目录不是 Git 仓库；未创建 commit。仅修改了 Task 2 允许的六个目标文件，并新增本报告。

## 实施内容与需求映射

| 要求 | 实际改动 | 结果 |
| --- | --- | --- |
| 1 | `EVAL-05` 新增四类明确失败 oracle：次要控件压过主操作、陌生图标只靠 tooltip、视觉收敛损害可访问性/命中区、无 viewport/状态/同屏证据即声明完成。 | 保留 `contract-only`，明确未运行真实 browser fixture 或 real-agent。 |
| 2 | SOP 阶段 9 增加界面类型、主/次/风险操作、输入方式、同屏基准、静止态/图标/icon-only 检查、实际渲染比较和调整后回归。 | CLI 无浏览器、截图或视觉回归工具时记录未验证范围，不依赖 Codex Desktop 面板。 |
| 3 | 账本新增 `LOC-030` 后续会话来源。 | 明确为 2026-09-02 用户确认经验，不计入原始 29 个内容文件。 |
| 4 | 决策矩阵新增 `TIP-077`，并将来源覆盖更新为 `LOC-001` 至 `LOC-030`。 | 记录条件采用并改写、例外、tooltip 边界、视觉尺寸与命中区分离及落点。 |
| 5 | 原始材料审计新增「后续来源」。 | 明确原始逐文件审计计数仍为 29。 |
| 6 | `rule-traceability.json` 更新 `verified_on`、来源计数并新增 `RUL-022`。 | destination 与 artifacts 使用相同的 14 个实际路径；全部 status 为 `implemented`；仅关联 `EVAL-05`，状态含 `eval-contract-only; real-agent-not-run`。 |
| 7–8 | 更新适用 Markdown 的 `updated` 元数据，保持既有结构和中文写作风格。 | 未复制完整视觉模块，新增表述均限制为阶段动作、失败条件或追踪元数据。 |

## 审查修复

Task 2 独立审查为 Approved with one Minor。按审查意见，仅修正 `docs/research/local-material-audit.md`「规则落点摘要」中“76 条可执行建议”的过时范围，改为“原始 76 条可执行建议及后续 `TIP-077`”。原始 29 个本地内容文件的审计边界未改变；未编辑其他交付目标。

## 最终规则审查修复

按最终规则审查意见，`EVAL-05` 补充一条紧凑失败 oracle：歧义、低频或高后果动作缺少可见文字标签，或危险动作缺少适当的 undo、review 或 confirm 保护。既有四条失败 oracle 和 `contract-only` 边界均保持不变；未编辑 SOP、账本、追踪 JSON 或 Prompt。

## 验证命令与原始结果摘要

```text
$ cd Constraint/coding-agent-system && python3 -m json.tool sources/rule-traceability.json >/dev/null
exit 0; no stdout

$ cd Constraint/coding-agent-system && python3 tools/agent_system.py validate .
VALID

$ cd Constraint/coding-agent-system && python3 -m unittest discover -s tools/tests -p 'test_*.py'
.............................................................
----------------------------------------------------------------------
Ran 117 tests in 55.204s

OK

$ TRACEABILITY_CHECK
TRACEABILITY_CHECK=PASS

$ MARKDOWN_FENCE_CHECK
MARKDOWN_FENCE_CHECK=PASS

$ UTF8_CHECK
UTF8_CHECK=PASS
```

追踪检查确认：`RUL-022` 仅定义一次；`LOC-030` 与 `TIP-077` 各仅有一行定义；destination/artifact 路径集合完全相等、均从 `Constraint/coding-agent-system/` 解析存在，且全为 `implemented`。`local_source_count` 为 30，而审计文档仍明确原始计数为 29。

## 六个目标文件 after 哈希与大小（两种文件视图）

| 文件 | pathname view：`/usr/bin/stat -f %z` bytes | pathname view：`sha256sum FILE` | logical-readable stream：`/bin/cat \| wc -c` bytes | logical-readable stream：`/bin/cat \| shasum -a 256` | logical UTF-8 characters | 编码 / Markdown fences |
| --- | ---: | --- | ---: | --- | ---: | --- |
| `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md` | 6070 | `96c2487f2ec0c8a0309bb7c0b5203e83088b81eceff2fc6a66b0d078205539ab` | 1974 | `69152f64b6139ee4435b7a2835bd537b8d5019a6b32e5e8767044cdd1bb01b92` | 1122 | UTF-8 / 0（平衡） |
| `Constraint/coding-agent-system/docs/sop/project-lifecycle.md` | 43373 | `51da8bef52af5c33a9a1328ecf093cf42480cadcea82f634370081f16066f98f` | 39277 | `d1b72b3c14593ccf489c2c3c9b09f0d4750e1ec9708bf3fc3357db9a32a6d32e` | 18479 | UTF-8 / 0（平衡） |
| `Constraint/coding-agent-system/docs/research/local-tip-ledger.md` | 22147 | `20d31194269bb7c7df86a7d9222fb8f568d3e67ec50fd12814594bbaad535f68` | 18051 | `4331ad34d605fa315657574ea090140ddb4be9b8d2339323bb52f835739b0d09` | 11795 | UTF-8 / 0（平衡） |
| `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md` | 28766 | `e34a444ba9dd6fcf8a57e28ecbb8e952bce57ed9294d91643e9934956f523c62` | 24670 | `7654502503284a7babb5d6108a387dadb9d870c91860dc6cef75cd72d1fb9396` | 13460 | UTF-8 / 0（平衡） |
| `Constraint/coding-agent-system/docs/research/local-material-audit.md` | 20325 | `e68aa43169c5f7f7307061f8093bdd9c91ef7161fb8c1ca8d5020f98456b2730` | 16229 | `9ca8aa6698a17252cfcb4c8ff4d16fed5cf3d7041f8ec3aa08c922dd4e69bada` | 9119 | UTF-8 / 0（平衡） |
| `Constraint/coding-agent-system/sources/rule-traceability.json` | 24036 | `43811539e42fb0934e91ead0a45ab73d717f8677a015192ef3ee7e5d19d675f5` | 24036 | `43811539e42fb0934e91ead0a45ab73d717f8677a015192ef3ee7e5d19d675f5` | 23612 | UTF-8 / n/a |

五个 Markdown 文件在 pathname 与 logical-readable stream 两种视图中返回不同的大小和 SHA-256；JSON 两种视图一致。logical-readable stream 的 UTF-8 字节和哈希由 Ruby/Python 解码后的内容再次交叉核对。**本报告不推断该差异的原因。**Task 5 应在内容冻结后统一选择记录视图，并重新计算最终 logical manifest。

## 文件清单

- 修改：`Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md`
- 修改：`Constraint/coding-agent-system/docs/sop/project-lifecycle.md`
- 修改：`Constraint/coding-agent-system/docs/research/local-tip-ledger.md`
- 修改：`Constraint/coding-agent-system/docs/research/tip-decision-matrix.md`
- 修改：`Constraint/coding-agent-system/docs/research/local-material-audit.md`
- 修改：`Constraint/coding-agent-system/sources/rule-traceability.json`
- 新增：`全栈开发Prompt Chain/docs/superpowers/sdd/2026-09-02-ui-visual-restraint-integration/task-2-report.md`

## 未验证项与 Concerns

- 未运行真实 browser fixture、截图/视觉回归或 real-agent evaluation；`EVAL-05` 仍仅为 `contract-only`。
- RUL-022 对 M05–M09 普通版与对话版记录的是已存在的实际路径及计划完成态的静态追踪；本 Task 未修改这些 Prompt，不能据此声称其 UI 行为已经运行或通过。
- 未创建 commit：工作区不是 Git repository，且任务明确要求不提交。
- 收尾哈希读取曾显示 pathname 与 logical-readable stream 两种视图不同；父 Agent 确认没有其他获授权 Agent 写入 Task 2 目标文件。已暂停交付目标写入，仅在授权后更正本报告；不推断两种视图差异的原因。
