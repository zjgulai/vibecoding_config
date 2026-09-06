# Task 4 review package

- Review mode: read-only full-file review; no Git repository, diff or commit range exists.
- Authority: `task-4-brief.md`, the approved design/Task 4 plan, and the final Task 3 original M05–M09 semantics.
- Implementation claims: `task-4-report.md`; independently inspect all eight targets.
- Exact scope: `prompts_ask/05–09`, modular workflow, CLI usage manual, end-to-end controller, plus the report.

| Exact target | Before logical SHA-256 | Current logical SHA-256 |
| --- | --- | --- |
| `全栈开发Prompt Chain/prompts_ask/05-领域模型与产品规格.md` | `e1ba23c03ba28f3044152cb51a64f5ae90a299e6c0f04240a269688708b661e5` | `7204fc389a3adefe9cfa5044d0bbe82c0c43de218e9be16d0cdb0a0aaade60d0` |
| `全栈开发Prompt Chain/prompts_ask/06-原型与UX验证.md` | `958fa92667198199a3475149a292c637bff40cb034e133c69ed07931ff4553db` | `400a9e41b5398e27dace92ae07275e2b701af2beaaca7e99ede36047334afb7c` |
| `全栈开发Prompt Chain/prompts_ask/07-架构设计与任务拆解.md` | `88f75b758b143b25f631a073d3a1805afc142c92b976bbbca8347c587a7d14b9` | `0ad9778726882ba6daa37858741bf40215f06c22894f0451486e5f1eb221696e` |
| `全栈开发Prompt Chain/prompts_ask/08-全栈实现与TDD.md` | `59e2a0d42480eb38861f6de26f0902095e1aa30be1d975298187f5835563ed0f` | `bd56bfe6a2753ddebbff2fb64fa97dcf7990ff886ccbe62d7485cd0fdbc5feeb` |
| `全栈开发Prompt Chain/prompts_ask/09-AI-Eval与质量安全.md` | `6b746b201cd58fb9567201c037f32c0baa4a5c1c86dfec8996ac9bafeb4a143b` | `2932debd09320393ca2299798dbdd8be32aefbb0360a3346fca17984af6c51f9` |
| `全栈开发Prompt Chain/04-模块化Skills工作流.md` | `f1c0ee0922d5753b47a216012b7a95234c825f3303bc733d6f7247d30bcb4a03` | `fc51f093b5e9eae7e4e834e13e64cd537c0f3713bf6cab36c6c094c86f2e5ba0` |
| `全栈开发Prompt Chain/06-Prompt-Chain使用手册.md` | `d574a50a89658199d3807cefbb12a46b50ffd03cc9d49b97c0b39d198bfbab79` | `b9d03c70893902253b281c0231d49dda6576005164ccd116367f2a94729b3547` |
| `全栈开发Prompt Chain/prompts/99-端到端Prompt-Chain.md` | `84ef0cbe3c82bb862f902d058b82cf52b49925eb3766f3648fd44f62c90a324f` | `2d4f44df5b26bc825b7137f9a1d81dfc7ea46ca2cb4e8f94608ce87c9031f38f` |

Hashes use the logical-readable UTF-8 stream. The report separately records the known pathname/logical view discrepancy; Task 5 owns post-freeze normalization.

## Review instructions

Read the five final original M05–M09 files, their five dialogue counterparts, the three cross-module targets, task brief and report. Verify:

1. Source/dialogue lifecycle semantics match by stage while dialogue-only PLAN, one-question, generation-confirmation and public eight-section contracts remain intact.
2. All 13 `prompts_ask` still have exactly 104/104 public headings, balanced fences, one-question protocol and confirmation gate; no duplicate H2s were introduced.
3. M09 dialogue adds `A06_PATH` and `Evidence/trace`; M08 dialogue has exact `Visual verification: not run` and explicitly does not authorize unapproved tools.
4. G0/G3/G4/R3, MODE, ALLOWED_FILES, DEPENDENCY_CHANGES, fixed review range, real provider/payment/production/external actions remain fail-closed. M08 dialogue must remain default PLAN even though source M08 is APPLY-oriented.
5. Workflow table is a compact M05–M09 transfer contract, manual is CLI-only and not Desktop-dependent, controller contains only the UI trace/evidence invariant without a duplicated style checklist.
6. Full visual rules remain centralized in `frontend-visual-quality.md`; M05–M09 are proportional projections, not repeated full lists.
7. Report claims match current content and do not claim actual browser/real-agent behavior.

Independently run the common-heading/static checks if useful. Return `Spec Compliance`, `Strengths`, `Issues` grouped Critical/Important/Minor, and `Assessment: Approved` or `Needs fixes`, with file:line evidence. Do not edit files.
