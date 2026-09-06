---
title: Coding Agent 系统研究来源索引
doc_type: knowledge
module: coding-agent-system
topic: research-sources
status: stable
created: 2026-08-29
updated: 2026-09-06
owner: self
source: human+ai
---

# Coding Agent 系统研究来源索引

本文件是 Task 1 的规范化来源入口。结论、来源元数据与 claim 映射分别位于：

- 面向使用者的结论：[深度研究报告](docs/research/deep-research-report.md)。
- 每项 material claim 的逐项映射：[claim-to-source ledger](docs/research/source-ledger.md)。
- 输入材料的可用性与风险：[本地材料审计](docs/research/local-material-audit.md)。
- 29 个本地内容文件的逐项行号、去留与规则映射：[本地 Tips 逐文件账本](docs/research/local-tip-ledger.md)。
- `ref_links.txt` 中 7 个唯一 URL 的正文摘要、证据等级与官方复核：[外链正文账本](docs/research/ref-links-ledger.md)。
- 逐条说明采用、条件采用、改写与排除原因的 76 项原子决定：[Tips 原子决策矩阵](docs/research/tip-decision-matrix.md)。
- 规则到来源、目标层、产物、评测和过期信号的机器可解析映射：[`rule-traceability.json`](sources/rule-traceability.json)。
- 第三方 skill 的版本、许可证和处理决定：[Skill 锁文件](sources/third-party-skills.lock.json)。
- 外部研究方法的版本、许可证边界和 adapt/exclude 决定：[研究方法锁文件](sources/research-methods.lock.json) 与 [NOTICE](sources/NOTICE.md)。

## 规范化来源

| ID | 来源 | 发布者 | 访问日期 | 用途 |
| --- | --- | --- | --- | --- |
| RSP-001 | [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md/) | OpenAI | 2026-08-30 | Codex 指令发现、优先级与大小限制。 |
| RSP-002 | [How Claude remembers your project](https://code.claude.com/docs/en/memory) | Anthropic | 2026-08-29 | Claude Code 的 `CLAUDE.md`、`AGENTS.md` 导入、规则与自动记忆边界。 |
| RSP-003 | [Configure permissions](https://code.claude.com/docs/en/permissions) | Anthropic | 2026-08-29 | Claude Code `permissions.allow` / `ask` / `deny` 规则、工具匹配与求值顺序。 |
| RSP-004 | [dsh-agent-instructions @ cd5ef81](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/context/agent-instructions/README.md) | DeepSeek | 2026-08-29 | 固定审计 commit 下的工作区指令候选、项目根、预算、优先级与动态刷新。 |
| RSP-005 | [DeepSeek Harness skills @ cd5ef81](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/docs/subsystems/skills.md)；[skill-filesystem @ cd5ef81](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/skill/skill-filesystem/README.md) | DeepSeek | 2026-08-29 | 固定审计 commit 下的 skill 根、`DSH_AGENTS_HOME`、优先级、调用字段，以及无 Git 时的 cwd 回退。 |
| RSP-006 | `Constraint/Codex_AGENTS.md`、`Constraint/CLAUDE.md`、`Constraint/cursor_rules/`、`Constraint/andrej-karpathy-skills-main/`、`Constraint/ref_links.txt` | 本仓库输入材料 | 2026-08-29 | 29 个本地内容文件（2 个根指令 + 17 个 Cursor rules + 1 个 URL 清单 + 9 个本地 Karpathy 包文件）的规则、重复、冲突、格式缺陷和无证据机制主张审计；本地 Karpathy 包只作方法线索，不作可复制代码来源。 |
| RSP-007 | [mattpocock/skills @ 6654f6b](https://github.com/mattpocock/skills/tree/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76) | Matt Pocock | 2026-08-29 | 第三方 skill 方法候选与 MIT 许可证。 |
| RSP-008 | [vinvcn/mattpocock-skills-zh-CN @ 9fb0161](https://github.com/vinvcn/mattpocock-skills-zh-CN/tree/9fb0161ac2be0c45c59cbea0878eb77d92cc24b5) | vinvcn | 2026-08-29 | 中文版本对照、译文审计与 MIT 许可证。 |
| RSP-009 | [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model) | OpenAI | 2026-08-29 | Codex 可用模型家族、reasoning effort、精简提示词与评测建议。 |
| RSP-010 | [Model configuration](https://code.claude.com/docs/en/model-config) | Anthropic | 2026-08-29 | Claude Code 模型 alias、选择优先级、effort 与 pin 策略。 |
| RSP-011 | [Configure models](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md) | DeepSeek | 2026-08-29 | Harness 模型、provider、凭据存储与默认模型选择。 |
| RSP-012 | [Plugin Config Catalog](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/config-catalog.md) | DeepSeek | 2026-08-29 | Harness 生成式配置参考与 `settings.yaml` 所属机制。 |
| RSP-013 | [Hooks reference](https://code.claude.com/docs/en/hooks) | Anthropic | 2026-08-29 | Claude Code hooks 的作用域、事件、matcher 与执行类型。 |
| RSP-014 | [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) | Anthropic | 2026-08-29 | Claude Code MCP 的外部工具连接与配置边界。 |
| RSP-015 | [DeepSeek Harness MCP client @ cd5ef81](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/mcp/mcp-client/README.md) | DeepSeek | 2026-08-30 | Harness MCP client 如何把外部 server tools 注册为模型工具；当前不支持 resources 或 prompts。 |
| RSP-016 | [DeepSeek Harness developer preview](https://www.deepseek.com/harness/en/) | DeepSeek | 2026-08-29 | Harness 的预览状态、插件架构与官方启动入口。 |
| RSP-017 | `tools/tests/test_agent_system.py`、`evals/test_*.py` 与本轮测试输出 | 本项目 | 2026-08-30 | 初始化、可达模块路由、风险敏感 profile readiness、完整 Skill 子树、项目 Skill 扩展、Memory、controls、备份、symlink 防护、11-task 评测契约及平台 Skill 适配的本地证据。 |
| RSP-018 | [Build skills](https://developers.openai.com/codex/skills/)；[`agents/openai.yaml` 字段参考 @ 6478a75](https://github.com/openai/codex/blob/6478a751fde8884b2fdc76486fe23175a8e795d4/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md)；[Skill parser @ 6478a75](https://github.com/openai/codex/blob/6478a751fde8884b2fdc76486fe23175a8e795d4/codex-rs/skills/src/parser.rs) | OpenAI | 2026-08-30 | Skill 的渐进披露目录、supporting resources、`agents/openai.yaml` 的 `interface`、`dependencies`、`policy.allow_implicit_invocation`，以及未知 Skill frontmatter 的静态解析边界。 |
| RSP-019 | [Extend Claude with skills](https://code.claude.com/docs/en/skills) | Anthropic | 2026-08-29 | Claude Skill 的 `disable-model-invocation`、`allowed-tools` 与 permission 关系。 |
| RSP-020 | [Claude Code settings](https://code.claude.com/docs/en/settings) | Anthropic | 2026-08-29 | 用户/共享项目 settings 路径、`$schema`、`permissions.deny` 示例、hooks 所属配置与优先级。 |
| RSP-021 | [Codex Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) | OpenAI | 2026-08-29 | 用户 `config.toml`、受信任项目 `.codex/config.toml` override 层及项目模板的安全分层。 |
| RSP-022 | [Codex Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) | OpenAI | 2026-08-29 | `model_reasoning_effort`、`model_instructions_file` 等配置键的当前字段语义。 |
| RSP-023 | [Codex best practices](https://learn.chatgpt.com/guides/best-practices) | OpenAI | 2026-08-29 | 明确目标、项目上下文、验证反馈与工作流建议。 |
| RSP-024 | [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) | Anthropic | 2026-08-29 | 先探索、再计划、再实现，保持 `CLAUDE.md` 精简，并提供可执行验证信号。 |
| RSP-025 | [Explore the `.claude` directory](https://code.claude.com/docs/en/claude-directory)；[Environment variables](https://code.claude.com/docs/en/env-vars)；[Checkpointing](https://code.claude.com/docs/en/checkpointing) | Anthropic | 2026-08-29 | `CLAUDE_CONFIG_DIR` 的影响范围与 macOS Keychain 边界；`file-history` checkpoint、`/rewind` 及恢复限制。 |
| RSP-026 | [`karpathy/autoresearch` README @ 228791f](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/README.md)；[`program.md` @ 228791f](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md) | Andrej Karpathy | 2026-08-29 | 固定可变范围、固定预算与度量、实验记录和保留/丢弃循环的方法灵感。固定 commit 无独立许可证文件，GitHub license 元数据为空；不支持复制代码或长文本。 |
| RSP-027 | [本地 Tips 逐文件账本](docs/research/local-tip-ledger.md) | 本项目 | 2026-08-29 | 29 个实际本地内容文件的来源行、独特经验、采用/改写/排除、规则 ID、目标层、产物、评测和可靠性。 |
| RSP-028 | [外链正文账本](docs/research/ref-links-ledger.md) | 本项目；外链作者 | 2026-08-29 | `ref_links.txt` 的 7 个唯一 canonical URL、释义摘要、证据等级、采用/改写/排除和平台第一方复核。X 作者页面曾在登录浏览器中核对，但未保存可复现 receipt；不把浏览器过程、转录或缓存当作平台事实或效果证据。 |
| RSP-029 | [`rule-traceability.json`](sources/rule-traceability.json) | 本项目 | 2026-08-29 | 规则级 source→decision→destination→artifact→eval→expiry 映射。artifact 的 `implemented` 只表示文件已创建并纳入静态契约；eval 的 `contract-only` 不表示真实 Agent 行为已验证。 |
| RSP-030 | [Harness Codex hook bridge @ cd5ef81](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/hooks/hooks-codex/README.md)；[Claude Code hook bridge @ cd5ef81](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/hooks/hooks-claude-code/README.md) | DeepSeek | 2026-08-30 | Harness hook bridge 的受支持 command-hook 子集、失败行为与 native plugin 边界。 |
| RSP-031 | [Harness MCP client @ cd5ef81](https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/mcp/mcp-client/README.md) | DeepSeek | 2026-08-30 | MCP 默认 opt-in、tools-only、resources/prompts 不支持、schema token 成本与重连边界。 |
| RSP-032 | [Tips 原子决策矩阵](docs/research/tip-decision-matrix.md) | 本项目 | 2026-08-30 | 29 个本地内容文件、7 个唯一外链和 Matt Skills 方法候选的原子级 decision→reason→runtime layer→verification 映射。 |
| RSP-033 | [Shao Meng：产物链与人工门](https://x.com/shao__meng/status/2095034431614677320)（[公开镜像](https://api.fxtwitter.com/status/2095034431614677320)）；[代码、知识与认知债](https://x.com/shao__meng/status/2094027833505144919)（[公开镜像](https://api.fxtwitter.com/status/2094027833505144919)）；[AI Native SDLC](https://x.com/shao__meng/status/2093990789584236857)（[公开镜像](https://api.fxtwitter.com/status/2093990789584236857)） | Shao Meng | 2026-09-06 | 本轮通过公开镜像读取三条短帖正文；原始 X 页面与链接长文未作为正文证据。仅支持作者提出的工作流框架，不支持平台事实或效果结论。 |
| RSP-034 | [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)；[What is agentic engineering?](https://simonwillison.net/2025/Jun/6/what-is-agentic-engineering/)；[Code is cheap](https://simonwillison.net/2025/Mar/11/cheaper-than-human-thinking/)；[Hoard things you know how to do](https://simonwillison.net/2025/Mar/11/hoard-things-you-know-how-to-do/)；[Better code](https://simonwillison.net/2025/Mar/15/better-code/)；[Anti-patterns](https://simonwillison.net/2025/Jun/7/agentic-engineering-anti-patterns/) | Simon Willison | 2026-09-06 | Agentic engineering 的作者方法论：工具/执行/验证循环、人类目标与验证责任、已验证样例的复用和代码便宜不等于质量成本消失。 |
| RSP-035 | [Claude Code features overview](https://code.claude.com/docs/en/features-overview)；[Hooks reference](https://code.claude.com/docs/en/hooks)；[Configure permissions](https://code.claude.com/docs/en/permissions) | Anthropic | 2026-09-06 | 项目上下文、hooks 与 permissions 的当前机制边界；仅支持官方页面明确写出的机制，不支持跨平台等价或真实运行效果。 |

## 使用规则

- RSP-001 至 RSP-005、RSP-009 至 RSP-016、RSP-018 至 RSP-025、RSP-030 与 RSP-031 是平台行为与字段级结论的第一方证据；它们只支持文中明确写出的机制，不支持真实客户端运行结果。
- RSP-006 是待迁移材料，不是平台事实的证据。RSP-027 至 RSP-029、RSP-032 只记录审计、取舍与追踪，也不能替代平台第一方证据；涉及产品行为时，必须回到相应官方来源。
- RSP-033 是动态社交短帖的作者框架，且本轮只有公开镜像的短帖正文可复核；不得把它升级为平台事实、外链长文内容或效果证据。RSP-034 支持作者的方法论，RSP-035 支持 Anthropic 页面明确写出的 Claude Code 机制；两者均不替代本项目真实任务验证。
- RSP-007 与 RSP-008 仅支持 skill 方法来源、许可证和处理决定；本项目不整包安装，也不把其 README 或 `SKILL.md` 当作规范正文复制。
- RSP-026 只支持 Auto Research 的方法灵感与来源边界。本项目没有运行或复制该仓库；README 的 `MIT` 标签没有独立许可证文本佐证，不作为代码或长文本复用许可。
- RSP-004、RSP-005、RSP-018 与 RSP-026 已固定到本轮只读审计 commit；这保证证据可复核，不表示已安装客户端与该 commit 一致。RSP-009 至 RSP-016、RSP-019 至 RSP-025 属于动态平台资料；正式升级前必须重新读取当前版本。
- RSP-017 只证明本项目生成器、校验器和评测控制面在本地与隔离临时目录中的行为，不证明 Codex 或 DSH 已加载生成配置或在代表性任务上更优；Claude 产物仅作兼容性回归。
- 页面未显示发布日期时，ledger 记录为「页面未标示」；访问日期不是发布日期。
