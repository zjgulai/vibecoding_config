# Task 3 review package

- Review mode: read-only full-file review; no Git repository, diff or commit range exists.
- Authority: `task-3-brief.md` plus the approved design and Task 3 plan.
- Implementation claims: `task-3-report.md`; independently inspect the five current Prompt files.
- Exact scope: only `prompts/05–09` plus the implementation report.

| Exact target | Before logical SHA-256 | Current logical SHA-256 |
| --- | --- | --- |
| `全栈开发Prompt Chain/prompts/05-领域模型与产品规格.md` | `3c33c7d0bcbe3de39a039a640349645d6b1ee8b104be567d60e014b5cbc08c2f` | `813932012a7c74d455cd7931a2c380e9320edaa45a7c89be1052e831e474f505` |
| `全栈开发Prompt Chain/prompts/06-原型与UX验证.md` | `453cfce835956cd1c570c1fcf303801f87448ed22168ac59ed86625d13c5bef3` | `492560544495d04932ccbc73e3d22850f55e29b70fe60f052f6496473f914d73` |
| `全栈开发Prompt Chain/prompts/07-架构设计与任务拆解.md` | `ff7b7a95226d84f01d3139cdc8805b972e4dac3e564f1f7332da1babeccf1bfd` | `7a55bc6f18e0a43464882b6b9f659cfd9cd78a4cd60dd540b412b7cab4a98bf4` |
| `全栈开发Prompt Chain/prompts/08-全栈实现与TDD.md` | `a0cd9e5c7cb546b59275b0673262085b8b3e85eed38faead5ce177235be1e206` | `4c2e59b88289d325682b1b806e8496b8f60204649b05bd653755d18dca63cd7c` |
| `全栈开发Prompt Chain/prompts/09-AI-Eval与质量安全.md` | `889d4407d242a4881ddb9083cb7a0573c7bad42a85a88bb0a062bbe30ab49c4e` | `4a15a3688ad96079ce0d64ba61e058d38f6a576a370bcffd0354d0470f224151` |

Hashes above use the logical-readable UTF-8 stream. The implementation report separately records pathname/logical size differences; Task 5 owns post-freeze normalization.

## Review instructions

Read each exact target completely, plus the brief and report. Return both spec compliance and task quality. Verify:

1. Lifecycle separation: M05 defines observable UI context/acceptance; M06 tests uncertainty and differentiates variants structurally; M07 only transmits approved A05/A06 constraints; M08 implements and records same-screen render evidence; M09 independently reviews with evidence.
2. M05 does not dictate cross-context pixels, a new icon library or implementation taste; M07 does not make new design decisions.
3. M08 contains the exact fallback `Visual verification: not run`, retains text/focus/contrast/hit-area protections, and does not turn browser/tool availability into authorization.
4. M09 includes `A06_PATH`, `Evidence/trace`, only Spec/Standards axes, and `Unverified scope` when real visual evidence is absent.
5. Existing Axx output structure, G0/G3/G4, MODE, review range, dependency, production/external/provider/payment, R3 inheritance and stop conditions remain fail-closed. Text existence alone is not enough; assess semantic interactions.
6. The same full UI checklist was not copied into every stage; each projection is proportional.
7. No non-target edits or unsupported real-browser/behavior claims appear in the report.

Run the source static check if useful. Return `Spec Compliance`, `Strengths`, `Issues` grouped Critical/Important/Minor, and `Assessment: Approved` or `Needs fixes`, with exact file:line evidence. Do not edit files.
