# Task 3 Report

## 状态

已完成。

## 创建文件

- `prompts_ask/09-AI-Eval与质量安全.md`
- `prompts_ask/10-发布与上线.md`
- `prompts_ask/11-可观测性与反馈闭环.md`
- `prompts_ask/12-增长与实验.md`
- `prompts_ask/13-复盘与Skill自进化.md`

## 检查摘要

- M09–M13 均含单问题协议、状态更新、生成确认、八段公共标题和模块专用章节。
- M09 分离审查与修复授权。
- M10 在没有匹配 R3 时于 G5 readiness 后停止，未执行时记录 `Not deployed / no production verification`。
- M11 的生产读取同时要求 G0 数据边界和对象级 R3；G5 不足以替代。
- M12 启动需要 MODE=APPLY、G5、G6 与匹配 R3；否则记录 `Not launched / no production verification`。
- M13 将 G6 限定为设计决定；本地持久写入要求 G3/G4 `LOCAL_CHANGE_AUTHORIZATION`，外部发布另要求 R3；未执行时记录 `Not adopted / no persistent change`。

## 注意事项

- 工作区不是 Git 仓库，因此无法提供 Git 状态或 commit 验证；未执行 commit。

## Review 修复记录

### 精确改动

- `prompts_ask/09-AI-Eval与质量安全.md`：新增 `R3_ACTION_AUTHORIZATION` 输入；真实 provider、付费评测和 red-team endpoint 明确要求匹配、未过期的对象级 R3，并要求 data boundary、Credential scope、Cost、Verification、Expiry 及适用的 Rollback/stop、Idempotency/duplicate guard。无授权时仅允许 fixture/mock/dry-run，禁止外部 endpoint。
- `prompts_ask/13-复盘与Skill自进化.md`：真实 SkillOpt/backend/provider 评测只要发送数据或消耗预算即要求同等对象级 R3；无授权时强制 mock/dry-run，原有外部 publish/adopt R3 规则保留。

### 焦点检查

命令：

```sh
set -e
rg -n 'R3_ACTION_AUTHORIZATION|真实 provider 调用|付费评测|red-team endpoint|data boundary|fixture/mock/dry-run|外部 endpoint' '全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md'
rg -n 'R3_ACTION_AUTHORIZATION|真实 SkillOpt/backend/provider 评测调用|发送数据|消耗预算|data boundary|mock/dry-run|真实 backend/provider' '全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md'
printf 'Focused R3 gate checks: PASS\n'
```

输出：

```text
9:提供 `PROJECT_ROOT`、`A05_PATH`、`A07_PATH`、`A08_PATH`、`REVIEW_RANGE`、`APP_URL_OR_START_COMMAND`、`AI_EVAL_SCOPE`、`R3_ACTION_AUTHORIZATION` 和 `MODE=PLAN`。
28:4. AI Eval 从 A05 acceptance/风险设计 3–10 个最小代表 fixture，先 deterministic assertion，再固定 grader；记录 model/prompt/config/provider、seed/temperature 或不可控项，覆盖正常、边界、拒答、注入、泄露、tool misuse、成本/延迟。Promptfoo 固定版本、默认 `--no-share`。任何真实 provider 调用、付费评测或 red-team endpoint 访问都须有匹配、未过期且对象级的 `R3_ACTION_AUTHORIZATION`，至少列明 Target、Action、data boundary、Credential scope（不含值）、Cost、Verification、Expiry，并在适用时列 Rollback/stop 与 Idempotency/duplicate guard；没有该授权时仅可用 fixture/mock/dry-run，且不得调用外部 endpoint。不得同时改 benchmark 与被测实现后宣称提升。
9:提供 `A00_PATH`、`A08_PATH`、`A09_PATH`、`A11_PATH`、`A12_PATH`、`EVOLUTION_TARGET`、`BENCHMARK_OR_TASKS`、`MODE`、`G6_ADOPTION_DECISION`、`LOCAL_CHANGE_AUTHORIZATION` 与 `R3_ACTION_AUTHORIZATION`。
18:条件式 Skill：仅用户明确选择且已安装时加载 `memory-governance`、`writing-for-agents` Audit；它们只建议 retain/rewrite/move/delete/needs-evidence。任何真实 SkillOpt/backend/provider 评测调用，只要发送数据或消耗预算，都必须有匹配、未过期且对象级的 `R3_ACTION_AUTHORIZATION`，至少列明 Target、Action、data boundary、Credential scope（不含值）、Cost、Verification、Expiry，并在适用时列 Rollback/stop 与 Idempotency/duplicate guard；没有该授权时强制使用 mock/dry-run 和 reviewed tasks file，不得调用真实 backend/provider。未安装时按本 Prompt fallback，不安装、不上传。
Focused R3 gate checks: PASS
```
