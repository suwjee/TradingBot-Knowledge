---
id: "market.events"
type: "market"
status: "canonical"
authority: "normative"
title: "Market events"
source_refs: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L209", "engine/pipeline/reaction_engine.py#L39"]
---

# Market events

Reaction confirmation, Reset, Blue formation, A trigger/stop, S source/decision, physical Order confirmation/stop, E parent stop/decision, and StopAll gates may have distinct exact event times inside the same main candle. Preserve each event's physical source and containing main index. Native Reaction mode and S/E family are independent labels.
