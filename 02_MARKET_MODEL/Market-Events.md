---
id: "market.events"
type: "market"
status: "pending"
authority: "non-canonical"
title: "Market events"
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L39"]
related_entities: ["algorithm.reaction", "algorithm.reset"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L39"]
---

# Market events

The retained Reaction, Blue, A, S, E, lifecycle, and bridge sources record distinct exact events that may share one main candle. Preserve their physical source and containing main index. E parent/decision and StopAll gate chronology are now source-visible; this full-stage inventory remains pending/non-canonical because B/C-dependent semantics and fresh paired runtime validation are unresolved. Native Reaction mode is a separate label from S/E family.
