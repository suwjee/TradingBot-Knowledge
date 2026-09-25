---
id: "data.raw_schema"
type: "data"
data_kind: "raw_schema"
status: "canonical"
authority: "normative"
title: "RAW row schema and validation boundary"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.raw_format", "data.integrity", "data.candle_model", "algorithm.raw", "source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L149", "engine/bridge/trading_pipeline.py#L143", "engine/bridge/trading_pipeline.py#L1737"]
source_refs: ["apps/chart/server/raw-resource-store.js#L13"]
---

# RAW row schema and validation boundary

The source-confirmed storage shape is `[{"time": epoch_second, "open": number, "high": number, "low": number, "close": number}, ...]`. The chart RAW store requires exactly these keys, a nonempty array, safe positive integer `time`, finite OHLC, `high >= open,close,low`, `low <= open,close,high`, and strictly increasing times. Its `Number(...)` coercion means the store accepts values that convert to finite numbers before it serializes them; the ten inspected persisted files actually use JSON numeric tokens. Do not generalize observed row types into a claim that all external inputs were originally numeric.

The Python bridge accesses the same keys and casts time with `int`, then normalizes prices through `as_decimal`. It does not independently enforce the chart store's full strict schema at that point. The data layer records both contracts, uses the stronger storage checks for integrity reporting, and never silently repairs invalid rows. Same-second aggregation is a calculation transform, not permission to alter the stored input.

No row contains a timezone field. `time` is an epoch second, and Tehran localization is performed by the bridge. File-level broker/symbol/timeframe are metadata inferred only from the observed path/name or validated sidecar, never from each row.
