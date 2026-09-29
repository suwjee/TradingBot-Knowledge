---
id: "data.raw_model"
type: "data"
status: "active"
authority: "executable"
title: "Generic future RAW schema"
version: "current"
related_entities: ["data.policy", "market.raw"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
data_kind: "raw_model"
---

# Generic future RAW schema

The production boundary consumes a JSON array of candle rows with native time and OHLC fields. Verify actual current parser requirements in the local bridge and raw-resource-store snapshots before registering supplied data. Preserve numeric lexical precision for Decimal decisions and record metadata separately. Main timeframe geometry and lower-timeframe chronology derive from the supplied input scope. No populated market-data schema example, hash or filename is stored here.
