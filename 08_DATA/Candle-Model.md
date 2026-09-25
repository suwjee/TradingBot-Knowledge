---
id: "data.candle_model"
type: "data"
data_kind: "candle_model"
status: "pending"
authority: "non-canonical"
title: "RAW and normalized candle identities"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.raw_schema", "data.timeframe_registry", "market.candle", "core.chronology", "algorithm.raw", "source.trading_pipeline", "source.reaction_engine"]
source_refs: ["06_SOURCE/Code/apps/chart/server/raw-resource-store.js#L19"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L27"]
---

# RAW and normalized candle identities

One physical RAW row has an epoch-second `time` and OHLC numeric values. Physical identity is its position in the hashed input plus its timestamp; do not replace it with a chart label. The maintained engine `Candle` has full-input `index`, Tehran-local `timestamp`, `display_time`, `tag`, and Decimal `open/high/low/close` (`reaction_engine.py#L27-L36`). These are derived calculation objects, not extra RAW fields.

`build_candle_buckets` preserves first Open, maximum High, minimum Low and last Close when rows share a second or belong to one selected main bucket. For timeframe `T`, the bucket epoch is `time` when `T=1`, otherwise `floor(time/T)*T`. `build_candle_objects` assigns indexes from the resulting full input sequence, converts epochs to Asia/Tehran wall time and classifies Doji as GREEN. Both directions read the same physical candles; price-direction decisions belong to algorithms.

The ten distinct RAW streams now stored under `08_DATA/Raw` had strictly increasing timestamps and no duplicate exact seconds at inspection. This observed property is not a universal parser guarantee. The bridge's bucket construction and duplicate-second handling are not retained in this Vault; the chart RAW store's retained source covers its write validation only.
