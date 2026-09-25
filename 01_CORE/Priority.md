---
id: "core.priority"
type: "core"
status: "pending"
authority: "non-canonical"
title: "Priority"
source_refs: []
related_entities: ["algorithm.lifecycle", "test.lifecycle_invariants"]
source_reference: []
---

# Priority

The direction-invariant sequence table is S Blue=1, E Blue=2, S Red=3, E Red=4. StopAll outranks these; A is below them. Priority resolves competing accepted owners at the relevant transition, but an old high-priority behavior does not own later chronology forever. For E candidates at one physical source, ownership priority precedes decision time and parent-stop time. Red E wins over Blue E at the same source, then higher number wins within one family.

The complete rank, from highest to lowest, is **StopAll > E Red > S Red > E Blue > S Blue > A**. Apply it only after the chronology and eligibility checks for the same competing transition; `test.lifecycle_invariants` protects the rank and its ownership boundary.
