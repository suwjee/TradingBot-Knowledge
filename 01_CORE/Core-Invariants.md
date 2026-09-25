---
id: "core.invariants"
type: "core"
status: "pending"
authority: "non-canonical"
title: "Core invariants"
source_refs: []
related_entities: ["test.invariant_validation"]
source_reference: []
---

# Core invariants

All price decisions use Decimal(str(value)) unless already Decimal. GREEN iff close >= open, so every Doji is GREEN. Strict crossing excludes equality. Lower-timeframe first-event chronology decides same-main-candle ordering; main candle extrema still own explicitly closed source ranges.

Both direction Reaction streams feed opposite-Order geometry. Internal Reaction is often calculation-visible although public output may hide it. The full received engine input determines calculation state; from/to are bridge presentation bounds. Stage ownership is A -> S -> E -> StopAll. Priority is StopAll > E Red > S Red > E Blue > S Blue > A. A StopAll is a hard lifecycle boundary. Creation cause and use provenance for Orders remain distinct.
