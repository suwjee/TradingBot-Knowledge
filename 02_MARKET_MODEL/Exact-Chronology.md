---
id: "market.exact_chronology"
type: "market"
status: "active"
authority: "empirical"
title: "Exact lower-timeframe chronology"
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L971"]
related_entities: ["core.chronology", "test.chronology_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L971"]
---

# Exact lower-timeframe chronology

The retained `MarketChronology` maps exact lower timestamps to main indexes, offers half-open lower windows, first strict crossings, Reaction confirmation, Reset event time, and physical opposite-Reaction Order stop provenance. A Reset secondTime is used when present. The first event is chosen by physical chronology; a main candle containing both candidate and stop is insufficient evidence of which won. Downstream lifecycle use is captured in source, while any B/C-dependent conclusion remains pending/non-canonical.
