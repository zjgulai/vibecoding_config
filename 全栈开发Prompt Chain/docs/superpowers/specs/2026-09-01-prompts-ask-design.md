# `prompts_ask` 人机对话版设计

## 目标

将 `prompts/01–13` 转换为 13 份适合自然对话的 Prompt。每份 Prompt 通过逐轮提问收集信息，在证据充分后生成与原模块一致的 `A01–A13` 产物。

## 范围

- 创建 `prompts_ask/01–13`，文件名与 `prompts/01–13` 一致。
- 不创建 `00` 和 `99` 的对话版。
- 不修改原 `prompts/`。
- 不安装 Skill、MCP 或依赖，不执行 Git、tracker、部署或生产动作。

## 统一对话协议

每份 Prompt 必须执行以下协议：

1. 先读取用户提供的上游产物和获准读取的项目事实。
2. 建立四类状态：`Facts`、`Decisions`、`Assumptions`、`Open questions`。
3. 每轮只问一个会显著改变当前模块结论的问题。
4. 每个问题包含提问原因、推荐答案、备选项影响和「不知道」选项。
5. 用户回答后，先复述新增决定和仍未解决的问题，再进入下一轮。
6. 证据不足时继续提问；出现安全、权限或关键歧义时停止，不替用户作决定。
7. 信息充分后先给出完成摘要。用户确认生成时，输出原模块规定的 `Axx` 文件结构。

## 公共产物契约

最终 `A01–A13` 均显式包含以下八段：

- `Metadata`
- `Facts`
- `Decisions`
- `Assumptions`
- `Open questions`
- `Risks and reversibility`
- `Acceptance evidence`
- `Handoff`

各文件还必须保留原模块的专用章节、完成标准、停止条件和安全边界。

## 权限模型

- 对话默认是 `PLAN` 和只读模式。
- 本地产品代码或配置写入必须有匹配的 G3/G4 决定和明确文件范围。
- commit、push、Issue/PR、消息、付费调用、secret、部署、生产读写或实验启动必须有独立、未过期的 `R3_ACTION_AUTHORIZATION`。
- G5/G6 只表示 readiness/design 决定，不能替代动作授权。

## 验收

- `prompts_ask/` 恰好包含 13 个 Markdown 文件。
- 文件编号和名称与 `prompts/01–13` 一致。
- 每份文件只有一个明确的模块目标、一个逐轮对话 Prompt 和一个对应 `Axx` 产物。
- 每份文件都包含统一对话协议、八段公共契约、模块专用问题、停止条件和完成标准。
- M06、M08、M10、M11、M12、M13 保留原 Prompt 的授权边界。

