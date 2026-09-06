# Task 2 review package

- Review mode: read-only full-file review; the workspace is not a Git repository, so no diff or commit range exists.
- Authority: `task-2-brief.md` and the approved design/plan.
- Implementation claims: `task-2-report.md`; treat commands and test results as claims unless independently rerun.
- Content identity below uses the logical-readable stream (`/bin/cat FILE | shasum -a 256`), because that is the UTF-8 content reviewed by Python, Ruby and the repository validator. The report separately records a pathname-view discrepancy for five Markdown files; do not treat that discrepancy as a semantic content change.

| Exact target | Before logical SHA-256 | Current logical SHA-256 |
| --- | --- | --- |
| `Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md` | `7266de94fb1eb1bd2c217c394d297ec746a998d99337ae91ccd2c0f53bbd4a27` | `0c57930d6861f9488fccf05ab80af8ffae18eb348d02aaf63678f628c0d59bd1` |
| `Constraint/coding-agent-system/docs/sop/project-lifecycle.md` | `f8bd8ba419482492336c23bb987c97b41ee7cb5cd94089551b87e7e92e9aef64` | `d1b72b3c14593ccf489c2c3c9b09f0d4750e1ec9708bf3fc3357db9a32a6d32e` |
| `Constraint/coding-agent-system/docs/research/local-tip-ledger.md` | `700b778d77a30a53e372d5a2485396ef6f08a262ea5cd40a4c8554432ff94ac8` | `4331ad34d605fa315657574ea090140ddb4be9b8d2339323bb52f835739b0d09` |
| `Constraint/coding-agent-system/docs/research/tip-decision-matrix.md` | `6672fb9ed556bf3a7e87b1723aa44419a38b3a3ba7b80c4778016efdfd25af26` | `7654502503284a7babb5d6108a387dadb9d870c91860dc6cef75cd72d1fb9396` |
| `Constraint/coding-agent-system/docs/research/local-material-audit.md` | `656c26a92a20de579f387c9eb4eca4de5383aa4a04c244685c4c271da5bb1177` | `ef23b5c612aab449ee0e4f7792cb036378cd22ffa19379a60315a886c2bbe573` |
| `Constraint/coding-agent-system/sources/rule-traceability.json` | `70abcafe62bd6d6c318f12c480a172c6cc6392b96ab492c439b9b017082dabf4` | `43811539e42fb0934e91ead0a45ab73d717f8677a015192ef3ee7e5d19d675f5` |

## Review instructions

Read all six exact targets completely, plus the task brief and implementation report. Review both spec compliance and task quality. In particular verify:

1. EVAL-05 supplies four observable failure oracles while remaining `contract-only`.
2. SOP stage 9 is executable from Codex CLI and does not depend on Codex Desktop.
3. `LOC-030`, `TIP-077` and `RUL-022` describe the same conditional adoption; the original 29-file audit remains historically intact.
4. RUL-022 has exactly the required 14 real paths; destination and artifact sets match; artifacts use `implemented`; status does not claim a real-agent run.
5. Full visual rules were not redundantly copied into governance files, and exceptions/accessibility boundaries were not weakened.
6. The report describes evidence and the two-view filesystem anomaly honestly. Do not require semantic edits merely to eliminate the pathname/logical discrepancy; Task 5 owns post-freeze normalization and final manifest.

Return `Spec Compliance`, `Strengths`, `Issues` grouped Critical/Important/Minor, and `Assessment: Approved` or `Needs fixes`, with file:line evidence. Do not edit files.
