---
id: "market.model"
type: "market"
status: "canonical"
authority: "normative"
title: "Market model"
source_refs: ["engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L1732"]
---

# Market model

The engine constructs exact-second lower candles and selected-timeframe main candles from the same received RAW rows. Candle indexes belong to the complete engine input. Reaction/Reset geometry and opposite Order evidence are computed from these candles. The general standalone Leg definition remains unestablished; dedicated Leg files are intentionally empty.
