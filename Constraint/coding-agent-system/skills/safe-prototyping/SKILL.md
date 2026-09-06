---
name: "safe-prototyping"
description: "用隔离、一次性的原型回答一个逻辑、状态或 UI 设计问题；不用于直接生产化、真实数据试验或完整功能实现。"
metadata:
  source: "Method adapted from mattpocock/skills prototype (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Safe Prototyping

原型只回答一个决策问题。最小化 artifact、隔离副作用，并把学习带回正式设计，而不是把试验代码直接生产化。

## Choose the path

- **Fast path:** 纸面示例、静态 mock、REPL 或单文件实验足以回答问题时，使用最便宜的可逆形式；无需创建持久 artifact。
- **Full path:** 必须通过交互感受状态或比较 UI 结构时，选择 logic 或 UI 分支并建立明确隔离的 throwaway artifact。

## Workflow

1. 写下一句可判定的问题和停止条件，例如“这个状态模型能否表示取消后恢复？”而不是“探索一下设计”。一次原型只回答一个问题。
2. 选择形状：
   - **Logic/state:** 使用纯函数、reducer 或 state machine，配最薄的可运行外壳；暴露每次操作后的相关状态。
   - **UI:** 在最接近真实上下文的已有页面中比较 2–3 个结构明显不同的只读 variants；若无法嵌入，才建明显标记的本地 prototype surface。
3. 在开始前明确 artifact 位置、隔离方式、可允许的输入/输出和清理方案。优先仓库既有工具；不为原型安装依赖。
4. 使用 fixture、内存状态、stub 或 scratch 数据。真实 credentials、生产服务、外部 mutations、收费调用、真实消息和不可逆数据动作一律停下请求逐项授权。
5. 只实现回答问题所需的路径。跳过与结论无关的抽象、全面错误处理、迁移和 polish；但不得绕过安全控制或把 prototype 暴露到 production。
6. 与用户一起运行或展示关键场景，记录观察、结论、仍不确定项和原问题是否已回答。
7. 将确认的决定重新按 production 标准实现并验证；不要直接提升原型代码。列出待清理 artifact，删除或移动 material 文件前获得用户确认。

## Completion criterion

问题得到可观察证据支持的回答，结论与未知项已记录，正式代码不依赖 prototype，且所有临时 artifact 的保留或清理状态明确。

## Authorization boundary

原型请求不授权安装依赖、访问生产/真实数据、外部写入、创建 issue、commit、push、发布或部署。危险或外部副作用必须在动作发生前获得明确授权。
