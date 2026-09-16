# EVAL-02 synthetic harness fixture

This fixture is a deterministic, standard-library-only local vertical slice. It
exists to exercise reset/setup/oracle ordering, receipt binding, configuration
root propagation, artifact contracts, and comparison plumbing. It is not a
Codex, Claude Code, DeepSeek Harness, browser, database, or model-quality
evaluation.

`baseline/workspace/` is the immutable reset source. `workspace/` begins as an
identical mirror and is the only fixture subtree the deterministic local stub
may alter. The stub may alter exactly four files: `risk_note.py`,
`risk_note_api.py`, `risk_note_migration.py`, and `risk_note_render.py`.

The fixture-control interface is fixed:

```text
./fixture-control reset
./fixture-control setup
./fixture-control oracle --artifacts <absolute-artifact-root>
```

`setup` checks that reset reconstructed an identical regular workspace.
`oracle` rejects undeclared workspace changes, runs only local `unittest`
tests, checks the deterministic stub receipt and candidate envelope, and
rejects `.env`, `credentials/**`, and `production-write.log` artifacts.

Run it from a temporary staged copy. The source fixture's digest is part of the
manifest contract and must not be treated as a mutable execution workspace.
