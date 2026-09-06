@../AGENTS.md

## Claude Code 项目说明

- `AGENTS.md` 是本项目的共同契约；本文件只承载 Claude Code 差异，避免维护重复正文。
- 将本文件放在 `.claude/` 只避免 DeepSeek Harness 的初始根候选冲突。默认 `agent-instructions` plugin 在 Harness 成功访问该目录后仍可能动态发现本文件，并把首行 `@../AGENTS.md` 当作普通文本；不要在这里复制根契约或添加与 Harness 冲突的规则。
- `CLAUDE.md` 内容属于模型上下文，不是安全边界。强制限制应放在 permissions、sandbox、hooks、CI 或组织策略中。
