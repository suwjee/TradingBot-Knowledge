---
id: "market.timeframe"
type: "market"
status: "active"
authority: "executable"
title: "Analysis timeframe and supplied input scope"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
---

# Analysis timeframe and supplied input scope

The bridge normalizes its supplied rows before constructing analysis candles in timeframe buckets. Chart timeframe and analysis timeframe are distinct request parameters. Main physical indexes and exact lower-timeframe event positions must survive output projection. Requested visibility bounds do not alter a complete supplied bridge input, but a server-selected stream cannot supply omitted history.
