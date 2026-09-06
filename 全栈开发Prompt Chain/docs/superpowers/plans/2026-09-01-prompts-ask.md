# `prompts_ask` Human-AI Dialogue Prompts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 `prompts_ask/01–13`，把 13 个模块 Prompt 转换为可逐轮提问、确认并生成原 `Axx` 产物的人机对话版本。

**Architecture:** 所有文件共享一套对话状态机和八段公共产物契约；每份文件只替换模块目标、输入、核心问题树、Gate 和专用产物章节。原 `prompts/` 是事实与安全边界来源，不直接修改。

**Tech Stack:** Markdown、静态 shell/Ruby 校验；不新增依赖。

## Global Constraints

- 目标文件仅为 `prompts_ask/01–13`；排除 `00` 与 `99`。
- 每轮只问一个问题，并提供推荐答案、理由、选项影响和「不知道」路径。
- 最终产物名称必须与原模块的 `A01–A13` 完全一致。
- 每份最终产物必须显式包含八段公共契约。
- 默认 `PLAN`；G5/G6 不构成真实动作授权；R3 动作必须单独授权。
- 不修改 `prompts/`，不安装依赖，不执行外部副作用。
- 当前目录不是 Git 仓库。跳过 worktree、commit 和 Git diff，以文件隔离、内容哈希和独立审查替代。

---

### Task 1: 初始化、研究与产品决策对话 Prompt

**Files:**

- Create: `全栈开发Prompt Chain/prompts_ask/01-项目初始化与治理.md`
- Create: `全栈开发Prompt Chain/prompts_ask/02-机会与市场调研.md`
- Create: `全栈开发Prompt Chain/prompts_ask/03-用户研究与问题定义.md`
- Create: `全栈开发Prompt Chain/prompts_ask/04-产品策略与范围决策.md`

**Interfaces:**

- Consumes: 对应的 `prompts/01–04` 和统一设计文档。
- Produces: 对话式 M01–M04，以及 `A01–A04` 的输出契约。

- [x] 为每个模块写用途、启动方式和可复制对话 Prompt。
- [x] 写入逐轮状态、单问题、推荐答案和确认规则。
- [x] 保留 G0–G2、project-profile、调研来源与产品取舍边界。
- [x] 运行文件级标题、变量、Axx 和公共八段检查。

### Task 2: 规格、原型、架构与实现对话 Prompt

**Files:**

- Create: `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md`
- Create: `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md`
- Create: `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md`
- Create: `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md`

**Interfaces:**

- Consumes: `A04–A07` 与对应的 `prompts/05–08`。
- Produces: 对话式 M05–M08，以及 `A05–A08` 的输出契约。

- [x] 保留领域模型、验收、原型问题、架构 DAG 和垂直切片语义。
- [x] M06 明确 G4 与 sandbox 范围；M08 明确 G4、允许文件和依赖边界。
- [x] Debug 路径先复现和证伪，不使用猜测性补丁。
- [x] 运行文件级标题、变量、Axx 和公共八段检查。

### Task 3: 质量、发布、反馈、实验与演进对话 Prompt

**Files:**

- Create: `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md`
- Create: `全栈开发Prompt Chain/prompts_ask/10-发布与上线.md`
- Create: `全栈开发Prompt Chain/prompts_ask/11-可观测性与反馈闭环.md`
- Create: `全栈开发Prompt Chain/prompts_ask/12-增长与实验.md`
- Create: `全栈开发Prompt Chain/prompts_ask/13-复盘与Skill自进化.md`

**Interfaces:**

- Consumes: `A05–A12` 与对应的 `prompts/09–13`。
- Produces: 对话式 M09–M13，以及 `A09–A13` 的输出契约。

- [x] 保留 Spec/Standards、AI Eval、安全、发布 readiness、生产读取、实验和演进边界。
- [x] M10–M12 分离 G5/G6 与 `R3_ACTION_AUTHORIZATION`。
- [x] M13 分离 G6 design、本地 G3/G4 变更授权和外部 R3 发布授权。
- [x] 运行文件级标题、变量、Axx 和公共八段检查。

### Task 4: 全目录一致性与安全审查

**Files:**

- Review: `全栈开发Prompt Chain/prompts_ask/*.md`
- Compare: `全栈开发Prompt Chain/prompts/01–13`

**Interfaces:**

- Consumes: Tasks 1–3 的 13 个文件。
- Produces: 13/13 覆盖、安全门一致性、链接与 Markdown 完整性证据。

- [x] 检查文件数、文件名和 Mxx/Axx 映射。
- [x] 检查每份文件的单问题协议、公共八段、停止条件和完成标准。
- [x] 搜索旧授权字段、跨 Gate 执行、自动外部动作和未定义占位符。
- [x] 独立审查全部文件，修复 Critical/Important 问题。
- [x] 比较 native size 与可读字节数，并记录最终内容哈希。
