# Exploring design alternatives

Use design-it-twice when the interface is consequential and at least two credible shapes exist. It is a comparison technique, not a mandate to create branches or delegate work.

For each candidate, state:

- the caller-visible interface and where its seam sits;
- responsibilities hidden in the implementation and any genuine adapters;
- leverage for callers, locality for changes and tests, and likely failure modes;
- migration, compatibility and operational costs.

Reject candidates that merely rename the current structure, add seams with no real variation, or move complexity to every caller. Choose only after the decision owner confirms a trade-off when the choice changes architecture or compatibility.
