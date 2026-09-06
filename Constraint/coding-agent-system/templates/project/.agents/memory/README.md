# Memory candidates

`candidates.jsonl` 默认为空。每个候选必须是一行 JSON，且仅含：`id`、`observation`、`evidence`、`scope`、`destination`、`conflicts_and_risks`、`expiry_signal`、`status`。

八个字段都必须是非空字符串，`status` 固定为 `candidate`。候选需要人工复核，不能自动成为常驻规则；没有来源、已经过期、与项目事实冲突或无法安全删除和重新推导的候选不得保留。
