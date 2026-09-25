---
id: "market.candle"
type: "market"
status: "canonical"
authority: "normative"
title: "Candle"
source_refs: ["engine/pipeline/reaction_engine.py#L27", "engine/pipeline/reaction_engine.py#L91"]
related_entities: ["data.candle_model", "source.reaction_engine"]
source_reference: ["engine/pipeline/reaction_engine.py#L27", "engine/pipeline/reaction_engine.py#L91"]
---

# Candle

A Candle stores index, displayed wall time, exact timestamp, Decimal OHLC, and tag. GREEN if close >= open, RED otherwise. Exact Doji is GREEN in both directions. The same aggregation rule applies to one-second and main timeframe buckets, with first/last ownership for Open/Close.
