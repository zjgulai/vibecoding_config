# Task 5 review package

- Review mode: independent read-only verification after content freeze and normalization; no Git repository, diff or commit range exists.
- Authority: `task-5-brief.md` and the corrected Task 5 plan.
- Implementation claims and final 22-file manifest: `task-5-report.md`.
- Mechanical scope: 21 Markdown allowlist files normalized with logical content unchanged; `rule-traceability.json` was already four-view-consistent and not replaced.

## Review requirements

1. Independently verify all 22 current files against the frozen logical manifest in `task-5-brief.md` and the final per-file manifest in `task-5-report.md`; recompute aggregate using the documented `path + NUL + bytes + NUL + SHA-256 + newline` algorithm.
2. For every allowlisted file, require `/usr/bin/stat` size = `/bin/cat` bytes and `/sbin/sha256sum FILE` = `/bin/cat | shasum -a 256`; require 22 unique regular non-symlink paths and 21 Markdown files.
3. Verify all 21 Markdown files are valid UTF-8 with balanced fences, and no `.normalize.*` or `.pre-normalize-*` residue exists in their exact parent directories.
4. Independently rerun `validate .`, the 117-test suite (report actual number), the corrected final Prompt contract, the protected 31-file comparison, and one isolated `frontend-visual-quality` generated-project route/cmp check. Use fail-fast guarded temp paths and do not delete the `/tmp` fixture recursively.
5. Confirm the report does not overstate: protected evidence covers only the named 31 current-vs-Task1 paths; four historical before hashes remain unavailable; no real browser, screenshot, visual regression or real-agent run occurred; EVAL-05 remains contract-only.
6. Confirm no semantic edits are indicated by frozen before/after logical hashes. Historical details of temp creation/deletion can only be assessed from the report and current residue, not reconstructed; label that evidence boundary accurately.

Return `Spec Compliance`, `Independent Evidence`, `Issues` grouped Critical/Important/Minor, and `Assessment: Approved` or `Needs fixes`. Include exact file:line evidence for report problems and exact command results for validation. Do not edit any file.
