# 项目 Agent 资源

先阅读 `project-profile.md`；它仍为 `draft` 或含“尚未确认”时，只能作为待核对线索。`memory/` 仅保存待人工审核的候选；`controls/` 默认未启用，必须由项目明确接入 hook 或 CI。

项目初始化器把明确选择的模块复制到 `.agents/rules/`。不要默认复制全部模块；常驻无关规则会增加冲突与上下文成本。模块中的命令名称只是检查类别，实际命令必须来自仓库依赖、脚本、CI 或工程文档。

可选模块：

- `typescript-nextjs.md`
- `python-fastapi.md`
- `postgresql-migrations.md`
- `frontend-visual-quality.md`
- `file-document-governance.md`
