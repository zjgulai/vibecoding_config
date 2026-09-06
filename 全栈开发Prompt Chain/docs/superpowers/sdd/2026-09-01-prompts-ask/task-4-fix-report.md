# Task 4 Fix Report — `prompts_ask` 内容修复波

## 结论

`DONE`。已修复 Task 4 审计指出的 M03、M10、M11、M13 内容问题；未执行文件大小归一化。

## 实际改动

- `prompts_ask/03-用户研究与问题定义.md`
  - `product-discovery` 改为仅在“用户明确选择 + 已安装”时加载。
  - 保留 `grill-with-docs` 的“有仓库且需同步领域词汇”边界，并同样要求“用户明确选择 + 已安装”。
  - 未安装或未明确选择时使用当前 Prompt 的研究与问题定义 fallback，明确不得声称已加载或安装 Skill。
- `prompts_ask/10-发布与上线.md`
  - 将“每步先验 precondition”改为“每步先核验 precondition”。
- `prompts_ask/11-可观测性与反馈闭环.md`
  - 在可复制主 Prompt 首句显式加入默认 `MODE=PLAN`；G0 与对象级 R3 的生产只读边界未改动。
- `prompts_ask/13-复盘与Skill自进化.md`
  - 在条件式加载规则中补回上游 `retro`、SkillOpt/`skillopt-sleep`、PostHog `improving-mcp-tools`。
  - 每项均要求“用户明确选择 + 已安装”；未安装或未选择时使用 Prompt fallback、明确未加载且不得虚报调用。
  - 真实 SkillOpt/backend/provider 评测的对象级、未过期 `R3_ACTION_AUTHORIZATION` 要求保持不变。

## 聚焦检查

基于本地 Ruby 只读检查：

| 项目 | 结果 |
| --- | --- |
| 四份文件均只有一个 `## 可复制对话 Prompt` | PASS (4/4) |
| 八段公共契约 | PASS (每份 8/8) |
| 单问题协议 | PASS (4/4) |
| Markdown 围栏 | PASS (每份 2 个，偶数) |
| 未定义 `{{VARIABLE}}` | PASS (4/4 均无) |
| M03 安装门、fallback 与禁止虚报 | PASS |
| M10 precondition 用词 | PASS |
| M11 主 Prompt 默认 PLAN，G0+R3 边界 | PASS |
| M13 上游名称、安装门、fallback、provider R3 | PASS |

## 未处理项

- 未做文件大小归一化；按任务边界留给 controller 在内容冻结后处理。
- 未执行 Git、网络、provider、部署或生产动作。
