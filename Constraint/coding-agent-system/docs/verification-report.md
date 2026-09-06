---
title: Coding Agent 配置系统验证报告
doc_type: verification
module: coding-agent-system
topic: staged-verification
status: stable
created: 2026-08-29
updated: 2026-08-30
owner: self
source: human+ai
---

# Coding Agent 配置系统验证报告

本报告记录方案 B 在 2026-08-30 的最终本地证据。直接配置目标只有 Codex 与 DSH Desktop / 官方 DeepSeek Harness；Claude Code adapter 仅作兼容回归，Cursor 仅作为经验来源。以下结果证明当前源码、模板、生成器和隔离目录满足列出的本地契约，不证明真实 Agent 已加载配置或 coding 质量已经提高。

## 当前结论

| 结论 | 状态 | 证据边界 |
| --- | --- | --- |
| 四份 Codex / DSH 用户级与项目级 `AGENTS.md` 可从 canonical core 确定性渲染。 | 通过（静态与渲染） | `render-templates` dry-run 列出 6 个受管快照；`validate .` 返回 `VALID`；四份直接文件的 shared block 与 canonical core 一致。 |
| 29 份本地材料和 `ref_links.txt` 的 7 个唯一 URL 已逐项处理。 | 通过（来源覆盖） | `LOC-001`–`LOC-029`、`REF-001`–`REF-007` 与 TIP-001–TIP-076 连续且唯一；76 条决策中 50 条进入常驻、改写或路由采用，10 条条件采用，16 条排除、延期或排除原表述。 |
| 空项目和两个直接目标的用户目录可在隔离路径生成并校验。 | 通过（隔离本地 smoke） | 五个模块全部可从根 `AGENTS.md` 到达；15 个 canonical Skills、7 个 DSH explicit-only overlay 齐全；project、Codex user、DSH user 均返回 `VALID-GENERATED`。 |
| 生成写入没有已知的 4096-byte backing-view 偏差。 | 通过（Darwin 延迟 smoke） | 117 个仓库实质文件为 0 mismatch；fresh 隔离生成的 170 个文件在 25 秒后仍为 0 mismatch。 |
| 平台设置、画像、Memory 与项目 Skill 的新增安全门按本地契约 fail closed。 | 通过（单元与隔离 smoke） | 不同平台设置要求人工合并；动态内容做 secret-like 扫描；active profile preamble、敏感 Skill 路径、custom explicit-only 与 self-loop symlink 反例均被拒绝。 |
| 目标 Agent 已加载配置且产出质量提升。 | 未验证 | 未运行真实 Codex 或 DSH discovery / invocation / representative coding task；11 个评测仍为 `contract-only`。 |

## 最终验证矩阵

| 检查 | 当前结果 | 能证明什么 |
| --- | --- | --- |
| `python3 -m unittest discover -s tools/tests -p 'test_*.py' -q` | 117/117 通过 | renderer、initializer、用户安装、备份/回滚、profile、Memory、controls、Skill adapter、symlink、secret-like 内容与 Darwin 延迟 writer 回归满足当前本地契约。 |
| `python3 -m unittest discover -s evals -p 'test_*.py' -q` | 60/60 通过 | 11-task manifest、receipt-v2、assessment、rubric-v3、score-v5 与 hard gate 的实现契约；不是 Agent 行为结果。 |
| `python3 tools/agent_system.py validate .` | `VALID` | 声明文件、canonical 快照、Skills、JSON/TOML 和 traceability 满足静态校验。 |
| `python3 tools/agent_system.py render-templates` | `DRY-RUN`，6 个映射 | canonical core 可以无写入地列出全部受管快照；结合上一行 `validate` 才能证明当前无漂移。 |
| 全部 Skills 运行 `quick_validate.py` | 15/15 通过 | 15 个 Skills 的静态格式有效；其中 7 个 explicit-only 的 Codex metadata 与 DSH overlay 数量一致。 |
| 三个 JSON 来源/规则锁文件解析 | 3/3 通过 | `research-methods.lock.json`、`rule-traceability.json` 与 `third-party-skills.lock.json` 是有效 JSON。 |
| 本地 Markdown 链接扫描 | 113 个本地链接，0 broken | 当前仓库内相对文档链接可解析；不代表外部页面永久可用。 |
| 来源与 tip 覆盖 | 29 LOC、7 REF、76 TIP | 所有本地实质输入和去重外链都有去留决定；TIP ID 001–076 连续且唯一。 |
| 隔离项目初始化 | `APPLIED` → `VALID-GENERATED` | 五个模块可达；15 个 canonical Skills 和 7 个 DSH overlay 生成；draft 画像的普通校验通过。 |
| 隔离 Codex / DSH 用户安装 | 两次 `APPLIED`，两次 `VALID-GENERATED` | 两个直接目标可分别在空模拟 home 生成；没有触碰真实用户目录。 |
| ready profile gate | draft + `--require-ready-profile` 返回非零 | 未完成画像不能伪装成正式 ready；受控 `Not applicable` 和完整 active profile 由单元及独立 focused repro 覆盖。 |
| 已有不同 Codex 设置 | exit `2`；config 与 AGENTS 哈希不变；无 backup | `.codex/config.toml` 即使给出备份目录也不会被自动覆盖，且失败前无部分写入。Claude 对应设置由同组单元反例覆盖。 |
| 全树 native / streamed size | 仓库 117/117、fresh 生成 170/170 一致 | 当前 Darwin 环境不存在已知的延迟 4096-byte 假尾部；生成、安装、备份和回滚统一使用受校验的中性临时写入路径。 |

## 关键修复与独立审查

- 项目根现在为所有已选技术栈和文件治理模块生成明确路径与触发条件，不再出现“模块已复制但 Agent 不可达”。
- 项目画像按任务风险工作：高风险任务要求文件级 `profile_status: active` 与相关核心域的受控来源；不相关可选域可使用有边界的 `Not applicable`。active preamble 不能被额外自由文本劫持。
- 项目自定义 Skill 可保留 `references/`、`scripts/` 与 `assets/`，但不能覆盖 managed Skill、使用敏感相对路径、注入 symlink 或私用没有跨平台 overlay 的内部 explicit-only marker。
- 已有且不同的 `.codex/config.toml` / `.claude/settings.json` 必须人工合并；Codex 用户模板为 comments-only，不设置 model、approval 或 sandbox。
- 动态 profile、Memory 和项目 Skill 会做 secret-like 检查；错误只报告字段或路径，不回显命中的值。
- 单文件通过同目录 `.agent-write-*` 流式写入，核对实际长度与 SHA-256、`fsync` 后移动；Darwin 使用参数数组调用 `/bin/mv`，其他平台使用 `os.replace`。移动失败会清理临时文件并 fail closed。
- 两轮独立只读审查分别发现并促成修复：证据状态漂移、直接目标口径、来源过程不可复现、配置覆盖、profile/Memory 授权、错误 profile gate、custom Skill 逃逸与 backing-view race。修复后的生成器安全 focused repro 和四份直接 AGENTS 内容复审均为 PASS。

## 已交付配置层

- 用户级：短常驻授权、证据、安全、最小改动、根因调试、验证层级、Skill 与 Memory 路由。
- 项目级：按任务相关性读取项目画像和局部知识；长期知识写入必须由用户明确要求，并经 explicit-only Skill 与验证流程处理。
- 能力层：15 个 `static-baseline` Skills，其中 7 个 explicit-only；没有任何 Skill 被标记为 `behavior-validated`。
- 模块层：TypeScript/Next.js、Python/FastAPI、PostgreSQL migration、前端视觉质量、文件与文档治理，共 5 个条件模块。
- 控制与评测：默认关闭的 change-policy 示例和 11 个 contract-only 评测；自然语言规则不替代 permissions、sandbox、hook 或 CI。

## 仍未验证与操作边界

1. 当前机器能发现 Codex 可执行文件，但本轮没有启动真实 Codex；未发现 `dsh` 可执行文件，因此没有真实 DSH Desktop / Harness discovery、Skill invocation 或版本兼容 smoke。
2. 11 个评测没有 representative ready fixture、稳定 oracle 或真实 Agent 结果；在此之前不得宣称质量提升、模型优劣或 Skill behavior validation。
3. 本轮只在 `mktemp` 隔离目录产生写入，没有修改真实 `~/.codex`、`~/.claude`、`~/.dsh` 或 `~/.agents`，没有连接 MCP、调用付费模型、部署、生产写入或外部发送。
4. 当前工作区不是 Git 仓库；未创建 commit，也不能用 Git diff 作为改动证据。
5. Darwin 的 `/bin/mv` 分支已在当前 macOS 环境实测；非 Darwin 路径由单元契约覆盖，仍需在目标 OS 做隔离 smoke。
