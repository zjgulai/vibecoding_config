# Architecture review report

Keep the report in the response unless the user separately authorizes a repository artifact.

```markdown
## Scope and evidence
- Scope: <paths, subsystem or pain point>
- Evidence inspected: <code, tests, incidents, metrics or decisions>
- Limits: <what was not inspected>

## Candidates
### <candidate title>
- Current friction: <observable symptom>
- Evidence: <specific code/test/operational evidence>
- Proposed direction: <change in module/interface/seam responsibility>
- Expected leverage and locality: <why callers and maintainers benefit>
- Failure modes / trade-offs: <what could worsen or break>
- Recommendation strength: Strong | Worth exploring | Speculative

## Recommendation
<ordered next investigation or explicitly no recommendation>
```

Use `Strong` only with direct, repeated evidence and a bounded remedy. Use `Worth exploring` for a credible direction with an unresolved assumption. Use `Speculative` when the observation is weak, indirect or based on a narrow sample.
