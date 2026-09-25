---
id: "data.candle_model"
type: "data"
data_kind: "candle_model"
status: "canonical"
authority: "normative"
title: "RAW and normalized candle identities"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.raw_schema", "data.timeframe_registry", "market.candle", "core.chronology", "algorithm.raw", "source.trading_pipeline", "source.reaction_engine"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L149", "engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L181", "engine/pipeline/reaction_engine.py#L27"]
---

# RAW and normalized candle identities

One physical RAW row has an epoch-second `time` and OHLC numeric values. Physical identity is its position in the hashed input plus its timestamp; do not replace it with a chart label. The maintained engine `Candle` has full-input `index`, Tehran-local `timestamp`, `display_time`, `tag`, and Decimal `open/high/low/close` (`reaction_engine.py#L27-L36`). These are derived calculation objects, not extra RAW fields.

`build_candle_buckets` preserves first Open, maximum High, minimum Low and last Close when rows share a second or belong to one selected main bucket. For timeframe `T`, the bucket epoch is `time` when `T=1`, otherwise `floor(time/T)*T`. `build_candle_objects` assigns indexes from the resulting full input sequence, converts epochs to Asia/Tehran wall time and classifies Doji as GREEN. Both directions read the same physical candles; price-direction decisions belong to algorithms.

The five Vault RAWs and five additional distinct production RAWs inspected for this phase have strictly increasing timestamps and no duplicate exact seconds. This observed property is not a universal parser guarantee: the bridge has a same-second collapse path, while the chart RAW store rejects non-increasing timestamps when it writes data.
