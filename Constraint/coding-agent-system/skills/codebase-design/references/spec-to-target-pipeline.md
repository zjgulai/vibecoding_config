# Spec-to-target delivery pipeline

当同一项已批准行为必须落到多个客户端、协议、模型 provider、数据表示或部署目标，且直接分别实现会产生可观测漂移时，使用本参考。它借鉴多目标编译器的职责分层，但不要求引入编译器、代码生成器或新的项目状态机。

## 启用门槛

至少满足一项，且收益大于新增维护成本：

- 两个以上目标消费同一语义，并需要保持可测试的一致性；
- 已出现同一规则在多个目标中重复翻译、修复或漂移；
- 有稳定 reference contract、目标原生 validator 和明确 owner；
- 目标差异是真实运行时差异，而非尚未证实的未来扩展。

否则继续使用普通垂直 slice，并把该模式标为 `Not needed`。

## 设计映射

```text
story/evidence
→ canonical product contract
→ shared transforms
→ target adapters
→ target-native materialization
→ reference + native verification
```

1. **Canonical product contract** 只表达已批准的用户行为、领域不变量、失败语义、权限和兼容要求，不包含某个目标的施工细节。
2. **Shared transforms** 只承载所有目标共同的确定性规则；每一步写清输入、输出、错误和来源 trace。
3. **Target adapter** 只处理目标运行时、框架、协议或 provider 的真实差异。修改共享契约前列出受影响目标；新增 adapter 前先检查现有目标的同类实现，但不因表面相似强行合并语义差异。
4. **Materialization** 通过项目已有的生成或实现入口完成。生成物只从规范源更新，不手改；验证命令不得顺便改写 lockfile。
5. **Verification** 先用最小 fixture/quick check，再运行受影响目标的 native tests；共享、高风险或发布变更才扩大到相关矩阵和完整门禁。reference contract 已成立时，不得为迁就单一目标而削弱它。

## 必须记录

- 规范源及版本；共享不变量和 failure semantics；
- 目标清单、maturity（Stable / Beta / Experimental）、owner 与最近验证日期；
- adapter 的输入、输出、真实差异和禁止重新解释的语义；
- 影响半径，以及 golden、differential、round-trip、schema compatibility 或其他实际 oracle；
- 目标原生验证命令、未验证目标和回滚路径。

## 消融检查

在 reference contract 不变的前提下，逐项尝试删除本次新增 transform、adapter、layer 或配置。没有当前 requirement、invariant、failure mode 或 risk trace 的项应删除或延期；已由契约证明必要的兼容层、安全边界、目标 adapter 和 validator 不得为缩短代码而删除。

## 停止条件

- 规格、目标语义或 authority 尚未确认；
- 只有一个目标，且没有可测漂移；
- 缺少目标原生 validator 或 reference oracle；
- 引入中间契约会让调用者学习更多规则，却没有减少重复和漂移；
- 文档、测试与可执行 manifest 冲突。此时 fail fast，报告冲突，不自行选择对当前实现最有利的解释。
