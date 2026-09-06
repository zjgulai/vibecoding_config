# Task 4 Report — `prompts_ask` 全目录一致性与安全审查

## Spec verdict

`NEEDS CHANGES`

- 把握：高。已逐份读取 `prompts/01–13` 与 `prompts_ask/01–13`，并对目录、结构、Gate、占位符、Markdown、文件字节和内容哈希做了新鲜检查。
- Critical：0。
- Important：2。
- Minor：3。
- 安全 Gate 未发现会直接放行未授权外部动作的路径；不通过主要由文件完整性异常和 M03 的条件式 Skill 加载契约不完整造成。

## 范围与边界

已读取：

- `docs/superpowers/sdd/2026-09-01-prompts-ask/task-4-brief.md`
- `docs/superpowers/specs/2026-09-01-prompts-ask-design.md`
- `docs/superpowers/plans/2026-09-01-prompts-ask.md` 的 Global Constraints
- `docs/superpowers/sdd/2026-09-01-prompts-ask/progress.md`
- `prompts/01–13`
- `prompts_ask/01–13`

本轮未修改 `prompts/` 或 `prompts_ask/`，未安装依赖，未执行 Git、网络、provider、tracker、部署、生产读写或其他外部动作。当前目录不是 Git 仓库，与 plan/ledger 记录一致。

## Findings

### Important

#### I-01 — 13/13 交付文件的 native size 与实际可读字节数不一致

事实：`/usr/bin/stat -f %z` 对每份 `prompts_ask/*.md` 的报告值都比 `/bin/cat file | /usr/bin/wc -c` 和 Ruby `File.binread(...).bytesize` 大 4096 字节。对照的原始 `prompts/01–13` 全部 delta=0，因此不是这些 Markdown 内容本身必然产生的差异。

影响：普通流式读取可取得完整文本，但依赖 native `st_size` 进行预分配、完整性校验或严格读取的工具可能将文件判为截断/异常。实测 `/usr/bin/iconv -f UTF-8 -t UTF-8` 对 01、03、04、05、11 返回非零且报 `iconv: iconv(): Inappropriate ioctl for device`；Ruby 对全部 13 份的可读内容均判定为有效 UTF-8。

修复建议：在最终交付前以相同可读字节重写/规范化全部 13 份文件，保持下表内容 SHA-256 不变，然后重跑 `native == cat bytes == File.binread bytesize`、UTF-8 和 Markdown 检查。

#### I-02 — M03 的条件式 Skill 加载缺少安装门与 fallback

事实：`prompts_ask/03-用户研究与问题定义.md:14` 对 `product-discovery` 只要求“用户已显式选择”，未要求“已安装”；对 `grill-with-docs` 写为“可使用”，同样没有安装检查。该文件也没有“未安装则按本 Prompt fallback，不得声称已加载”的规则。其他含条件 Skill 的对话版已普遍保留这个门。

影响：直接复制主 Prompt 时，Agent 可被要求加载不存在的 Skill，且没有规定失败后的等价对话 fallback。这不会自动造成外部副作用，但违反本件要求的条件式 Skill 加载和可直接复制契约。

修复建议：两个 Skill 均改为“用户显式选择/适用，且已安装时才加载”，并增加未安装 fallback 和禁止虚假加载声明。

### Minor

#### M-01 — M11 主 Prompt 内未显式写 `MODE=PLAN`

`prompts_ask/11-可观测性与反馈闭环.md:9` 的围栏外“启动方式”列出 `MODE=PLAN`，但可复制主 Prompt 的首句（第 14 行）没有明说默认 PLAN。主 Prompt 已强制生产默认不可访问，并以 G0+R3 守门，所以实际安全语义未放宽；但它是 13 份中唯一一份不能在主 Prompt 内命中“默认 MODE=PLAN”的文件。建议在首句补齐。

#### M-02 — ledger deferred：M10 `每步先验 precondition` 用词不准确

`prompts_ask/10-发布与上线.md:27` 的“先验”容易理解为 a priori，不如原 Prompt 的“每一步先验证 precondition”明确。Gate 上下文仍完整，因此不升级为 Important；但发布属高风险流程，建议最终交付前改为“每步先核验 precondition”。

#### M-03 — ledger deferred：M13 未显式保留全部可选上游方法名

原 M13 的推荐名称还包含上游 `retro`、`skillopt-sleep` 和 PostHog `improving-mcp-tools`；对话版保留了 `memory-governance`、`writing-for-agents` Audit、SkillOpt/backend/provider 评测边界和完整 gated loop，但未列出前述全部可选名称。核心方法和授权语义未丢失，因此保持 Minor。为做到与原 Prompt 的完整可追溯，建议最终交付前以“用户明确选择+已安装+只读/候选建议”方式补回；如决定不补，至少应在交付记录说明是有意使用内置 loop 替代命名依赖。

## Deferred minors 的最终判断

- M10 “每步先验”：应在最终交付前修复。改动极小，但可消除高风险发布步骤的语义歧义。
- M13 可选上游名称：建议在最终交付前修复，但不应单独阻断交付；核心 loop 与 Gate 已保留。

## 验收矩阵

| 项目 | 结果 | 证据摘要 |
| --- | --- | --- |
| 目录数量/文件名 | PASS | `prompts_ask/` 恰好 13 份 Markdown；与 `prompts/01–13` 文件名集合完全相同；无 00/99。 |
| Mxx/Axx 映射 | PASS | 每份恰好命中 1 个对应 Mxx 主标题和 1 个对应 Axx 产物主标题。 |
| 单主 Prompt | PASS | 每份恰好 1 个 `## 可复制对话 Prompt`；没有第二个竞争性主 Prompt。 |
| 单问题协议 | PASS | 13/13 均显式要求每轮只问一个，并包含原因、推荐答案/理由、备选影响和“不知道”路径。 |
| 四类状态 | PASS | 13/13 均建立并要求每轮更新 Facts/Decisions/Assumptions/Open questions；回答后先复述新增状态与未决项。 |
| 生成前确认 | PASS | 13/13 均只有 1 个明确的 `确认生成 Axx-...md 吗？`。 |
| 八段公共契约 | PASS | 13/13 均显式含 Metadata/Facts/Decisions/Assumptions/Open questions/Risks and reversibility/Acceptance evidence/Handoff。 |
| 模块专用章节 | PASS | 原 Axx 的所有 `##` 产物章节在对应对话版中均保留；未发现章节级别遗漏。 |
| 停止条件/完成标准 | PASS | 13/13 均有明确停止语义；13/13 均恰好含 1 个“完成标准”。 |
| 条件式 Skill | FAIL | M03 见 I-02；其他关键条件 Skill/Adapter 规则均有安装/适用范围与 fallback。 |
| Gate/外部动作 | PASS with minor | 要求指定的 M06/M08/M09/M10/M11/M12/M13 Gate 全部保留；M11 主 Prompt 未显式写 PLAN，但生产默认不可访问和 G0+R3 未放宽。 |
| Markdown fence | PASS | 所有文件 fence 数为偶数；01–04/09–13 各 2 个，05–08 各 4 个（输入块+主 Prompt）。 |
| 未定义 `{{VARIABLE}}` | PASS | 只有 05–08 使用 `{{...}}`，均在同文件 `## 输入变量` 中定义；其他文件用启动字段名而非未绑定占位符。 |
| 旧授权字段 | PASS | 未命中 `APPROVAL_TOKEN`/`AUTH_TOKEN`/`ACTION_APPROVAL`/`AUTHORIZED_ACTIONS`/`EXECUTION_AUTHORIZATION`/`DEPLOY_APPROVAL`/`PRODUCTION_APPROVAL`；现有授权字段为 G4/R3/LOCAL_CHANGE_AUTHORIZATION 等当前契约。 |
| TODO/TBD/FIXME | PASS | 0 命中。 |
| 本地相对 Markdown 链接 | PASS | 0 个 Markdown link，因此无失效本地相对链接。 |
| Native/readable size | FAIL | 13/13 的 native size 均比可读字节数大 4096，见 I-01 和哈希表。 |

## Gate 审计

- 全局：13 份的文件级启动信息都是 PLAN；M11 主 Prompt 内显式性问题见 M-01。
- M06：默认 PLAN；APPLY 之前必须精确匹配 `G4_APPROVAL` 与 `ALLOWED_FILES_OR_SANDBOX`；生产/外部动作另要 R3。PASS。
- M08：默认 PLAN；只有 `G4_APPROVAL` + `ALLOWED_FILES` + `DEPENDENCY_CHANGES` 全部匹配才能明确切到 APPLY；依赖/lockfile 变更和外部动作有独立门。PASS。
- M09：真实 provider、付费 eval、red-team endpoint 要求匹配、未过期、对象级 R3；否则只能 fixture/mock/dry-run。PASS。
- M10：G5 明确只是 readiness；真实执行同时要求 MODE=APPLY + G5 GO/CONDITIONAL + 匹配 R3；无执行时回执固定为 `Not deployed / no production verification`。PASS（用词 minor 见 M-02）。
- M11：生产读取同时要求 G0 数据边界和未过期、对象级 R3；G5 明确不可替代；写工具和 mutation 保持关闭。PASS with minor。
- M12：真实 flag/experiment/rollout/campaign/流量变更同时要求 MODE=APPLY + G5 GO/CONDITIONAL + G6 Approved + 匹配 R3；否则只保留 draft，回执为 `Not launched / no production verification`。PASS。
- M13：G6 只是 adoption design；本地持久写入要求 MODE=APPLY + 绑定 exact diff/目标文件的 G3/G4 `LOCAL_CHANGE_AUTHORIZATION`；真实 backend/provider 评测或外部 publish/adopt 要求匹配 R3；否则回执 `Not adopted / no persistent change`。PASS。

未发现“G5/G6 自动升级为动作授权”、“对话确认自动等于 R3”或“无授权自动执行外部动作”的路径。

## Native/readable size 与内容 SHA-256

下表 `readable` 由 `cat | wc -c` 与 Ruby `File.binread.bytesize` 交叉验证，两者相等；SHA-256 针对可读内容。

| File | Native | Readable | Delta | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| 01-项目初始化与治理.md | 9547 | 5451 | 4096 | `ae0279940765a46f6e8f227dd55fecb1af37bc3c9a82001c157e4a2c86b251ef` |
| 02-机会与市场调研.md | 8177 | 4081 | 4096 | `bcc3d37a66a14ab399470fa364a461f07c465b6369324ff4d3641a37ad869731` |
| 03-用户研究与问题定义.md | 7840 | 3744 | 4096 | `2d5ddfb3ed1744432ae5eebfb25c0b70894d8b48b0df92d84f59775f2e287416` |
| 04-产品策略与范围决策.md | 7777 | 3681 | 4096 | `7c6e862bd9e7ffe6aef3479e559e8551cf96c6b08eb5bd515b6b1a1f389a770d` |
| 05-领域模型与产品规格.md | 8884 | 4788 | 4096 | `40b9b7f99d862fb9639a424ef0eede40a46a9c9aa73730d183090669b28a21a7` |
| 06-原型与UX验证.md | 8818 | 4722 | 4096 | `958fa92667198199a3475149a292c637bff40cb034e133c69ed07931ff4553db` |
| 07-架构设计与任务拆解.md | 8745 | 4649 | 4096 | `88f75b758b143b25f631a073d3a1805afc142c92b976bbbca8347c587a7d14b9` |
| 08-全栈实现与TDD.md | 9474 | 5378 | 4096 | `59e2a0d42480eb38861f6de26f0902095e1aa30be1d975298187f5835563ed0f` |
| 09-AI-Eval与质量安全.md | 9469 | 5373 | 4096 | `0cada695977fd8513fe5d7ff576afae0fb1ddc2945b4954a7dfb3977fcc523f0` |
| 10-发布与上线.md | 8931 | 4835 | 4096 | `f6fe18db0d100977647a5443bd6d097cef87732498e783e698b6cd1ea31c510b` |
| 11-可观测性与反馈闭环.md | 8589 | 4493 | 4096 | `497613dff6a093ae71ca211222f44395960526caa9cd20a48e332701715bd0cd` |
| 12-增长与实验.md | 9032 | 4936 | 4096 | `7b8282b3d537ff48d38487f21597a87f9d273c8bffc176d6a3c9599bd97cfdf2` |
| 13-复盘与Skill自进化.md | 9701 | 5605 | 4096 | `d469aef6332bf5e80933b92429f7d39d7b20e9bcceb0c3bd08fd659de10c5771` |

## 机器检查摘要

```text
Markdown files: 13
Filename diff vs prompts/01–13: empty
Mxx mappings: 13/13 PASS
Axx mappings: 13/13 PASS
Single dialogue-prompt headings: 13/13 PASS
Common contract headings: 104/104 PASS
Completion-standard markers: 13/13 PASS
Generation-confirmation markers: 13/13 PASS
Balanced fences: 13/13 PASS
TODO/TBD/FIXME: 0
Undefined {{VARIABLE}}: 0
Legacy authorization-field suspects: 0
Local relative Markdown links: 0
Requested gate checks: 11/11 PASS
Native/readable equality: 0/13 PASS
Original prompts native/readable equality: 13/13 PASS
```

## 交付前处理顺序

1. 先修复 I-01，确保 13/13 的 native/readable size 相等，且可读内容 SHA-256 不变。
2. 修复 I-02，为 M03 补全“已安装+未安装 fallback+不得虚报加载”。
3. 同批修复 M10 用词和 M11 主 Prompt 内的显式 PLAN；建议补回 M13 的可选上游名称或记录有意替代决策。
4. 修复后重跑全部目录级检查并重新计算 13 份内容哈希；只有 Important=0 时才建议将 verdict 改为 `PASS`。
