---
id: "data.timeframe_registry"
type: "data"
data_kind: "timeframe_registry"
status: "pending"
authority: "non-canonical"
title: "Input resolution and analysis timeframe registry"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.dataset_registry", "data.candle_model", "core.chronology", "algorithm.raw", "test.chronology_invariants", "source.trading_pipeline"]
source_reference: []
---

# Input resolution and analysis timeframe registry

The inspected RAW filenames and observed minimum timestamp step identify **1-second** and **5-second** input resolutions. The registered Phase 5 examples use **30-second main candles** with either input. A 1-second filename does not mean a 1-second main calculation; `--timeframe` selects the main bucket size in seconds. The bridge accepts an integer `T >= 1`; do not claim that every such value has been regression-tested.

Exact lower-timeframe chronology controls confirmation, breakout/breakdown, strict stop, A source/trigger, S/E decision and StopAll ordering whenever several events share a main candle. The lower view is built from the input rows after same-second normalization; no finer events can be inferred between recorded seconds. Each inspected file has some intervals longer than its nominal step. Those intervals are gap candidates, not proof of lost market records without a provider calendar and acquisition coverage evidence.

The engine interprets epoch seconds through `Asia/Tehran` for internal wall time. Keep raw epoch values, event seconds, main bucket seconds and display timezone distinct in fixture and regression metadata. See `core.chronology` and [Data-Integrity.md](Data-Integrity.md).
