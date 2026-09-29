---
id: "market.raw"
type: "market"
status: "active"
authority: "executable"
title: "Supplied RAW normalization"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
---

# Supplied RAW normalization

The bridge accepts the complete JSON it receives, normalizes numeric prices through Decimal semantics, collapses duplicate exact seconds according to its current normalization path and builds selected-timeframe candles and exact lower-timeframe indexes. Validate original input chronology and scope before interpreting an output. No physical RAW bytes or symbol-specific data registry are stored in this Vault.
