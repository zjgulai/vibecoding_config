# Optional deterministic controls

本目录的 controls 默认未启用。先审查 `change-policy.example.json`，再由项目维护者创建并维护唯一的实际 policy：`.agents/controls/change-policy.json`；只有显式接入既有 hook 或 CI 后才生效。本工具不会创建平台 Hook、自动修改 policy 或扫描 Git 历史。

`check_change_policy.py` 只接收 policy 和显式 changed paths，输出确定性 JSON。它不猜测 Git base、不扫描 secrets，也不写入文件。
