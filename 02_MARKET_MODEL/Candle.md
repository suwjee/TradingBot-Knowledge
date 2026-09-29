---
id: "market.candle"
type: "market"
status: "active"
authority: "executable"
title: "Current candle and Doji contract"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
---

# Current candle and Doji contract

Candle.index and native timestamp identify the physical source. Market color is GREEN when close >= open and RED when close < open. A Doji is GREEN. Decimal open/high/low/close are authoritative. Reflected computational coordinates transform price/color roles internally; the physical market Doji classification remains unchanged.
