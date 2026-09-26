---
id: "core.chronology"
type: "core"
status: "pending"
authority: "non-canonical"
title: "Time and chronology"
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L971"]
related_entities: ["market.exact_chronology", "test.chronology_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L971"]
---

# Time and chronology

Raw time is epoch seconds. Main buckets use floor(time/T)*T except T=1. Internal datetimes represent Asia/Tehran wall time without timezone; serialization interprets them as Tehran. Lower windows are half-open [start,end) unless a rule explicitly includes an endpoint. An exact lower event maps to the greatest main timestamp <= event.

Store both main-candle and lower-event chronology. Reaction confirmation and Reset may occur in one main candle; first strict lower event wins under each routine's tie order. Presentation clipping occurs after full engine calculation over its received input and never renumbers main indexes.

The retained `reaction_engine.py` proves the lower-window and event-mapping subset. Bucket construction, bridge serialization, and presentation clipping are present in the captured bridge source; the complete Vault-local chronology contract remains pending/non-canonical until end-to-end runtime evidence is refreshed.
