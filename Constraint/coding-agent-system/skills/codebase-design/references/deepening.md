# Deepening a module

Use this when callers repeatedly coordinate lower-level details that belong to one responsibility.

1. List the knowledge each caller must carry: ordering, retries, data conversion, error translation, policy, configuration or lifecycle.
2. Identify which knowledge is invariant across callers and can become implementation responsibility behind a smaller interface.
3. Check that the proposed module owns a coherent behavior, rather than becoming a pass-through wrapper or a catch-all service.
4. Compare before/after: callers should learn fewer rules, and a change or bug should become verifiable in fewer places.
5. Preserve seams that correspond to genuine variation. Keep private test seams internal unless callers have a real need for the same contract.

The deletion check is useful evidence: if removing the proposed module would duplicate meaningful coordination across callers, it may add depth; if it only removes a forwarding layer, do not keep it.
