# prompts_ask 终审返修报告

## 结论

终审列出的 3 项 Important 与 4 项 Minor 已在指定范围内修复；未修改原稿 `prompts/` 或其他交付文件。

## 文件与修改

| 文件 | 级别 | 修复 |
| --- | --- | --- |
| `prompts_ask/03-用户研究与问题定义.md` | Important | 首轮改为展示 Outcome、User、Why now、Success、Constraints、Out of scope 六字段暂定摘要；仅提问最高影响的一项差异/缺口，其余登记为 Open questions，后续仍每轮一题。 |
| `prompts_ask/05-领域模型与产品规格.md` | Minor | 恢复 Spec 只描述可观察产品行为、状态与验收结果，不写逐文件施工清单或将实现路径伪装成需求的边界。 |
| `prompts_ask/09-AI-Eval与质量安全.md` | Minor | 明确 Trivy 与任何静态扫描必须固定工具/规则版本，且仅为确定性第二信号，不上传源码或凭据。 |
| `prompts_ask/11-可观测性与反馈闭环.md` | Important | 恢复 correlation ID、业务 event、error context、AI prompt/model version、cost/latency、redaction、SLO 的 observability-gap 检查；每项缺口必须限制可执行的查询、假说验证、归因或 SLO 判断。 |
| `prompts_ask/11-可观测性与反馈闭环.md` | Minor | incident diagnosis 在稳定影响面与 rollback 决定后，若 `systematic-debugging` 实际可用即直接加载并运行，无需用户选择；仅不可用时才采用等价 fallback，且保留无修复先于根因调查的门禁。 |
| `prompts_ask/12-增长与实验.md` | Important | 要求在查看或解释结果前预注册 Ship / Iterate / Stop / Inconclusive 规则，并明确统计变化不自动等于用户价值或长期留存。 |
| `docs/superpowers/sdd/2026-09-01-prompts-ask/progress.md` | Minor | 清除 M10/M13 已修问题仍标为 deferred 的过期记录，追加本轮终审返修完成状态。 |

## 自检

- 已按原稿核对 M05、M09、M11、M12 的遗漏约束，并按设计稿核对统一对话协议。
- 上述 5 份对话 Prompt 均保留 Facts、Decisions、Assumptions、Open questions；每轮只问一个问题；信息充分后先请求确认，确认后才输出对应 Axx。
- 各文件的 `Metadata`、`Facts`、`Decisions`、`Assumptions`、`Open questions`、`Risks and reversibility`、`Acceptance evidence`、`Handoff` 八段均存在。
- G/R 授权语义未放宽：M11 生产读取仍要求 G0 边界和未过期对象级 R3，M12 launch 仍同时要求 MODE=APPLY、G5、G6 与 R3，M09 修复仍要求 G4 与明确文件范围；未引入 fail-open 路径。
- 已知 native stat 写后可能多出 4096 字节；本轮未执行 `rm`、`mv` 或任何归一化操作。
