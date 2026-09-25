---
id: "market.model"
type: "market"
status: "canonical"
authority: "normative"
title: "Market model"
source_refs: ["engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L1732"]
related_entities: ["data.raw_model", "core.pipeline", "market.leg"]
source_reference: ["engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L1732"]
---

# Market model

The engine constructs exact-second lower buckets and selected-timeframe main candles from the same received RAW rows. Candle indexes belong to the complete engine input. Reaction/Reset geometry and opposite Order evidence are computed from these candles. The lower buckets contain only timestamps present in the input; a nominal 5-second RAW does not become a complete 1-second feed. The general standalone Leg definition remains unestablished; see draft `market.leg`. Its Recognition and Calculation files remain empty.
