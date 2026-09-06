---
profile_status: draft
---

# 项目画像

本文件是项目隐性知识路由器。填写前保持 `profile_status: draft`；只有当前任务相关的六个通用领域与一个局部风险领域均有项目证据或可追溯的 `Not applicable` 结论时，才可按项目流程改为 `active`。不相关领域不阻塞普通任务；高风险任务须要求其相关领域为 active。

每个标题域使用以下两行一组的条目；一个域可以有多组。条目类型是 `Fact`、`Decision` 或 `Not applicable`，每条都必须紧跟一个 `Source`：

```markdown
- Fact: 这里写会改变 Agent 决策的已验证项目事实
  Source: path:README.md
- Decision: 这里写维护者已经确认的项目决定
  Source: user-confirmation:2026-08-29:profile-review
- Not applicable: 这里写该领域为何不适用于当前项目或任务
  Source: path:README.md
```

`Source` 只允许 `path:<项目相对路径>`、`command:<可复现命令>`、`url:<http(s) URL>` 或 `user-confirmation:<YYYY-MM-DD>:<确认上下文>`。`Not applicable` 必须说明适用边界，不能用 `N/A`、“待定”“未确认”“无”等低信息值替代证据。不要新增、重命名或重复 H2。active 域中不得出现 fenced block、HTML comment、HTML 隐藏元素或零宽/双向控制字符；校验器会拒绝整个域，不会先删除隐藏内容再接受剩余条目。

## 业务与安全不变量

尚未确认

## 权威修改入口

尚未确认

## 联动关系

尚未确认

## Do NOT 与受保护区域

尚未确认

## 精确 Definition of Done

尚未确认

## 权威资料与冲突顺序

尚未确认

## 局部风险

尚未确认
