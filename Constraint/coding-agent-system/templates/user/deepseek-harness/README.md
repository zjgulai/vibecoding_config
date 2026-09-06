# DeepSeek Harness 用户模板

将同目录的 `AGENTS.md` 安装为 `$DSH_HOME/AGENTS.md`。未设置 `DSH_HOME` 时，默认目标是 `~/.dsh/AGENTS.md`。

DeepSeek Harness 是开发者预览项目，配置接口仍可能变化。以下发现行为以默认 spine 已启用 `agent-instructions`、skill registry、tool consumer 与 skill filesystem plugins 为前提；自定义 preset 可以禁用或替换这些 plugins。本系统只交付这些官方 plugins 已确认支持的用户指令与 skill 文件，不创建或猜测项目级 settings 文件，也不写入 provider、model、凭据或 profile 配置。

项目继续只使用根目录 `AGENTS.md`。官方加载器也会把项目根 `CLAUDE.md` 当作初始候选，因此本系统把 Claude 专属入口放在 `.claude/CLAUDE.md`，只避免初始根候选冲突。Harness 成功访问 `.claude/` 后仍可能动态发现该文件；`@path` import 不是 `agent-instructions` 的通用语义，`@../AGENTS.md` 会作为普通文本进入上下文。项目共享内容由根 `AGENTS.md` 直接承载；不要在 `.claude/CLAUDE.md` 复制根契约或追加与 Harness 冲突的规则，并按当前版本实测。

安装器只生成默认 `<home>/.agents/skills` 布局，不读取 `DSH_AGENTS_HOME`。若当前环境自定义了 `DSH_AGENTS_HOME`，先在隔离 home 生成并审查，再按已安装 Harness 版本核实发现路径，最后人工复制 canonical skills。只要 `install-user` target 包含 Codex 或 DeepSeek Harness，安装器都会同步 shared skills 和七个 `.dsh/skills` explicit-only overlay；同机使用多平台时建议选择 `--target all`。无 Git 项目应从项目根启动；从嵌套 cwd 启动可能无法发现根 `AGENTS.md` 或 `.agents/skills`。

参考：

- <https://github.com/deepseek-ai/deepseek-harness>
- <https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/context/agent-instructions/README.md>
- <https://github.com/deepseek-ai/deepseek-harness/blob/cd5ef8148158c3a752a658978873241fdf8e2bbc/packages/skill/skill-filesystem/README.md>
