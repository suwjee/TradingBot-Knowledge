---
id: "data.raw_format"
type: "data"
data_kind: "raw_format"
status: "canonical"
authority: "normative"
title: "Observed RAW JSON format"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.raw_schema", "data.raw_model", "data.candle_model", "algorithm.raw", "source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L149", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L149", "engine/bridge/trading_pipeline.py#L143", "engine/bridge/trading_pipeline.py#L1737"]
---

# Observed RAW JSON format

Each inspected RAW file is one JSON array of candle objects. The confirmed row keys are exactly `time`, `open`, `high`, `low`, `close`; `time` is an integer Unix epoch second, while OHLC are JSON numbers (some parse as integers, others as decimals). No volume, symbol, timeframe, direction, indicator, source ID or lifecycle field occurs inside those ten RAW row shapes. Filename and optional `.meta.json` sidecar carry separate identity metadata and are not extra candle fields.

The bridge reads complete file bytes, removes a leading UTF-8 BOM if present, parses with `orjson` and accesses the five keys. The chart RAW store's write validator requires a nonempty array, those exact keys, safe positive integer times, finite prices, valid OHLC and strictly increasing row times. The bridge can aggregate duplicate seconds if such an external input reaches it, so storage acceptance and engine normalization are distinct boundaries.

The inspected files are minified or serialized JSON variants; whitespace and numeric spelling are part of the byte hash. Do not reformat a RAW file merely to compare it. See [RAW-Schema.md](RAW-Schema.md) for acceptance checks and [../Hash-Policy.md](../Hash-Policy.md) for identity.
