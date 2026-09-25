---
id: "market.candle"
type: "market"
status: "active"
authority: "empirical"
title: "Candle"
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L27", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L91"]
related_entities: ["data.candle_model", "source.reaction_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L27", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L91"]
---

# Candle

A retained `Candle` stores index, displayed wall time, exact timestamp, Decimal OHLC, and tag. The retained color helper returns GREEN if close >= open, so exact Doji is GREEN in both directions. One-second and main-timeframe bucket aggregation belongs to the absent bridge source and remains pending in `data.candle_model`.
