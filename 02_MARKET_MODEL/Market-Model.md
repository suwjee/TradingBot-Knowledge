---
id: "market.model"
type: "market"
status: "active"
authority: "executable"
title: "Current market model"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
---

# Current market model

Current input is an ordered collection of Decimal OHLC candles. Main candles and selected lower-timeframe chronology serve different purposes: main candles carry geometry and physical source ownership, while lower-timeframe positions prove strict event ordering. Direction chooses price geometry without changing native time, physical indexes, identity or provenance.
