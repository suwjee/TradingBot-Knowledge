---
id: "market.crossing"
type: "market"
status: "canonical"
authority: "normative"
title: "Strict crossing"
source_refs: ["engine/pipeline/direction_policy.py#L32", "engine/pipeline/reaction_engine.py#L211", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L429"]
related_entities: ["mirror.direction_mapping", "test.precision_invariants"]
source_reference: ["engine/pipeline/direction_policy.py#L32", "engine/pipeline/reaction_engine.py#L211", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L429"]
---

# Strict crossing

A crossing is strictly < or > as required by direction and stage; equality fails. The first exact lower event in the permitted window owns stop/decision chronology. Invalidation may win a same-finest-event tie with confirmation; S candidate and Order-stop crossing at the same lower event invalidates the S candidate. The scan's start/end boundaries are algorithm-specific; consult the owning note.
