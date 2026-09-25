---
id: "data.raw_model"
type: "data"
data_kind: "raw_model"
status: "canonical"
authority: "normative"
title: "Physical RAW input model"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.raw_format", "data.raw_schema", "data.raw_authority", "algorithm.raw", "source.trading_pipeline", "data.candle_model"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/bridge/trading_pipeline.py#L120"]
---

# Physical RAW input model

RAW is the original JSON candle input received by the calculation bridge. Its byte stream preserves row order, epoch timestamps and the written JSON price tokens. Every inspected RAW array contains records with exactly `time`, `open`, `high`, `low`, `close`; sidecar `.meta.json` files are separate metadata, not candle rows. The bridge strips a leading UTF-8 BOM if present, parses JSON, normalizes OHLC and builds lower/main candle views. It must not mutate the physical file to do that.

Byte preservation and calculation precision are related but distinct. The physical hash identifies the exact original JSON, including textual number representation. Current bridge parsing uses `orjson`, then `as_decimal`/`Decimal(str(value))` for logic; that path preserves its parsed numeric value under Decimal comparisons but cannot be claimed to retain lexical trailing zeros from a JSON number. No data note may promise more precision than the source path actually provides.

See [RAW-Format.md](Raw/RAW-Format.md), [RAW-Schema.md](Raw/RAW-Schema.md), [RAW-Authority.md](Raw/RAW-Authority.md) and `algorithm.raw` for the distinct storage, validation and normalization boundaries.
