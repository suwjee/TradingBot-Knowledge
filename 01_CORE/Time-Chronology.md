---
id: "core.chronology"
type: "core"
status: "canonical"
authority: "normative"
title: "Time and chronology"
source_refs: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L209", "engine/pipeline/reaction_engine.py#L971"]
related_entities: ["market.exact_chronology", "test.chronology_invariants"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L209", "engine/pipeline/reaction_engine.py#L971"]
---

# Time and chronology

Raw time is epoch seconds. Main buckets use floor(time/T)*T except T=1. Internal datetimes represent Asia/Tehran wall time without timezone; serialization interprets them as Tehran. Lower windows are half-open [start,end) unless a rule explicitly includes an endpoint. An exact lower event maps to the greatest main timestamp <= event.

Store both main-candle and lower-event chronology. Reaction confirmation and Reset may occur in one main candle; first strict lower event wins under each routine's tie order. Presentation clipping occurs after full engine calculation over its received input and never renumbers main indexes.
