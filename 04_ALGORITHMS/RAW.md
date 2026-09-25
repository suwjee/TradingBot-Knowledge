---
id: "algorithm.raw"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "RAW normalization and candle construction"
implemented_by: ["source.trading_pipeline", "source.reaction_engine"]
produces: ["market.candle", "market.exact_chronology"]
depends_on: []
relates_to: ["source.integration_boundary"]
source_refs: ["engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L1732", "engine/pipeline/core_utils.py#L11"]
related_entities: ["test.source_validation"]
source_reference: ["engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L1732", "engine/pipeline/core_utils.py#L11"]
---

# RAW normalization and candle construction

Input is the full JSON that the bridge receives, each row with epoch-second time and OHLC. The bridge strips UTF-8 BOM, parses with orjson, and rejects empty input. as_decimal preserves Decimal and otherwise uses Decimal(str(value)). Same-second rows collapse to one lower candle: first Open, max High, min Low, last Close. For timeframe T, bucket time is original time if T=1 and floor(time/T)*T otherwise. Main bucket OHLC uses the same first/max/min/last rule.

build_candle_objects converts epoch to Asia/Tehran wall time, stores naive datetimes and color GREEN iff close >= open. One shared lower index supports strict first-event/range-extreme queries. Requested from/to determine presentation indexes after full received-input normalization; no source index renumbering occurs. If upstream sends a prefiltered stream, that stream is the complete engine input and lacks earlier/later RAW chronology.
