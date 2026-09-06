# Task 5 final-review fix wave

## Authorized content changes already completed

The final rules/accessibility and prompt-lifecycle reviews authorized and independently re-approved exactly three semantic fixes:

1. `templates/user/codex/AGENTS.md`: the compact fallback now states that visual restraint must not reduce discoverability, readability, accessibility, visible focus/contrast, hit area or risk expression.
2. `evals/tasks/05-frontend-visual-quality.md`: EVAL-05 now fails ambiguous/low-frequency/high-consequence actions without visible labels, or dangerous actions without suitable undo/review/confirm protection.
3. `全栈开发Prompt Chain/04-模块化Skills工作流.md`: the M09 workflow summary now explicitly reads `A05/A06/A07/A08`, preserving the evidence chain from product specification and prototype validation through implementation and review.

No other deliverable semantic change is authorized. The scoped rules/accessibility and prompt-lifecycle re-reviews both returned PASS.

## New content freeze

The original 22-file frozen logical manifest in `task-5-brief.md` remains authoritative except for these three rows:

```text
4c479667ab4197510e75a31f30b839e8081e26b43fbd069ce830cf034eb1eff1 bytes=5417 Constraint/coding-agent-system/templates/user/codex/AGENTS.md
69152f64b6139ee4435b7a2835bd537b8d5019a6b32e5e8767044cdd1bb01b92 bytes=1974 Constraint/coding-agent-system/evals/tasks/05-frontend-visual-quality.md
73cea31abe38d2651e8ff048233c58b0d328ec2595a339b17bc6dfd8c71be22c bytes=27476 全栈开发Prompt Chain/04-模块化Skills工作流.md
```

All other 19 rows must match `task-5-brief.md` exactly. With the same sorted manifest algorithm, the expected new aggregate is:

```text
f5a32aba4983f54bdfb9aea737a44ff969b1ee4c11b003f07dd37fa9cbafd107
```

## Required rerun

1. Before writing, verify the new 22-file logical manifest: the 19 unchanged rows plus the three rows above. Any mismatch is BLOCKED.
2. Rerun corrected Task 5 Steps 1–4 in full. All must pass.
3. Run the same static-allowlist Step 5 normalization. It may normalize only the three edited Markdown paths above; if any other file requires normalization, stop and report before replacing it.
4. Confirm all three logical hashes remain unchanged, all 22 files become four-view-consistent, then rerun Steps 1–5 again. The second Step 5 must be idempotent with zero normalization.
5. Update `task-5-report.md` using `apply_patch` for report text and evidence:
   - add the final-review fix wave and new 22-file manifest/aggregate;
   - replace the inaccurate sentence “未访问……保护文件、其他平台或 zip” with “未访问真实 home；未修改保护文件、其他平台或 zip，验证步骤只进行只读访问”；
   - retain the 31-file current-only and four-historical-hash limitations;
   - retain prior normalization history, then record this wave’s exact normalized paths, backups and zero residue;
   - do not claim the historical temp/fsync sequence was independently reconstructed.
6. Rerun the full unittest suite rather than a targeted subset; report the actual count and time.
7. Do not create `final-review-report.md`, edit other deliverables, modify protected files, delete `/tmp` fixtures recursively, or use broad/glob deletion.

Return exact normalization count/paths, all rerun outcomes, new aggregate, report path and remaining unverified boundaries.
