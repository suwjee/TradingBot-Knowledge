---
id: "market.timeframe"
type: "market"
status: "canonical"
authority: "normative"
title: "Timeframe"
source_refs: ["engine/bridge/trading_pipeline.py#L120", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L159"]
---

# Timeframe

For T seconds, main bucket timestamp is time for T=1 and floor(time/T)*T otherwise. The one-second candle stream supplies exact event chronology. Main-candle source indexes and closed extrema ranges cannot be reconstructed by clipping or renumbering a presentation window.
