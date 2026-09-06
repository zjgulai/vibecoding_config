---
name: "systematic-debugging"
description: "通过可复现信号、可证伪假设和最小实验诊断复杂缺陷、flaky failure 或性能回退；不用于已经明确根因的机械修正。"
metadata:
  source: "Method adapted from mattpocock/skills diagnosing-bugs (MIT), consulted via vinvcn/mattpocock-skills-zh-CN at 9fb0161ac2be0c45c59cbea0878eb77d92cc24b5."
---

# Systematic Debugging

先建立能捕获用户实际症状的 feedback loop，再用证据缩小因果空间。

## Choose the path

- **Fast path:** 症状稳定、代码路径短且根因由直接证据支持时，执行“复现 → 单一可证伪假设 → 最小修正（若已授权）→ 原路径复验”。
- **Full path:** 复现困难、根因不明、跨模块、flaky 或性能问题使用完整流程。

## Full workflow

1. 定义 exact symptom、预期行为与一个 pass/fail command。优先测试、fixture CLI、HTTP 调用或浏览器脚本；让信号尽量快、确定且可无人值守。
2. 至少运行一次并确认它捕获的是用户报告的同一故障。缩减输入、数据、配置和调用链；每次删减后重跑，只保留 load-bearing 条件。
3. 提出若干按证据排序的假设。每个假设必须写出预测：若原因是 X，改变或观察 Y 应产生什么结果。
4. 一次只检验一个变量。优先 debugger/REPL 和边界处的定向 instrumentation；性能问题先建立基线 measurement。临时日志使用唯一标记，便于收尾删除。
5. 证据确认根因后，若用户已授权修复，在正确 public seam 写 regression test，观察其失败，再应用最小修正。
6. 重跑最小复现、原始未缩减场景和相关回归测试；删除临时 instrumentation 与 throwaway artifacts。

如果无法建立 red-capable loop，停止推测，列出已尝试的方法与缺少的证据。请求经脱敏的 artifact、可复现环境访问或临时 production instrumentation 授权；不要自行扩大权限。

## Evidence discipline

- 输出前脱敏 secrets、credentials、auth headers 和 PII；不足以诊断时明确说明，不读取密钥文件补全上下文。
- 失败率低的 flaky bug 先提高复现率；“偶尔看起来好了”不算修复。
- 诊断请求不自动包含修复授权。结论区分已复现事实、证据支持的根因与仍未排除的假设。

## Completion criterion

根因由实验预测支持；修复任务还需原始症状消失、回归测试通过且临时诊断改动清理完毕。无法验证时只报告诊断进展，不声明完成。

## Authorization boundary

本流程不授权 production 探针、真实数据变更、依赖安装、commit、push、发布或其他危险/外部操作；逐项获得明确授权后才能执行。
