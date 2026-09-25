---
id: "market.raw"
type: "market"
status: "canonical"
authority: "normative"
title: "RAW input"
relates_to: ["source.integration_boundary"]
source_refs: ["engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L1732"]
---

# RAW input

Each input row carries time, open, high, low, close. The bridge reads the entire supplied JSON; a UTF-8 BOM is removed before orjson parsing. Duplicate exact timestamps collapse with first Open, maximum High, minimum Low, last Close. Missing input raises ValueError. A chart server may supply a prefiltered JSON stream, so preserve the distinction between engine input and the original resource.
