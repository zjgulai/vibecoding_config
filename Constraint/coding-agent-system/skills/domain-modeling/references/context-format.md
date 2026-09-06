# Context record format

Use this only when an authorized context/glossary record is needed. Follow an existing repository format when one exists; otherwise keep the record scoped to one bounded area.

```markdown
# <Context name>

## Scope
What part of the business this language covers, and what it excludes.

## Shared language
| Term | Meaning | Invariants / boundaries | Example or counterexample |
| --- | --- | --- | --- |
| <term> | <agreed definition> | <what must or must not hold> | <concrete scenario> |

## Open questions
- <unresolved ambiguity and owner/next evidence>
```

Keep implementation classes, table names, transport details and unconfirmed hypotheses out of the glossary unless they are part of the domain language itself.
