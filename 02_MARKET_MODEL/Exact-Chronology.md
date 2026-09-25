---
id: "market.exact_chronology"
type: "market"
status: "canonical"
authority: "normative"
title: "Exact lower-timeframe chronology"
source_refs: ["engine/pipeline/reaction_engine.py#L971", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L209"]
related_entities: ["core.chronology", "test.chronology_invariants"]
source_reference: ["engine/pipeline/reaction_engine.py#L971", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L209"]
---

# Exact lower-timeframe chronology

MarketChronology maps exact lower timestamps to main indexes, offers half-open lower windows, first strict crossings, Reaction confirmation, Reset event time, and canonical physical Order stop. A Reset secondTime is authoritative when present. The first event is chosen by physical chronology; a main candle containing both candidate and stop is insufficient evidence of which won.
