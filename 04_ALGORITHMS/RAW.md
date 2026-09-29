---
id: "algorithm.raw"
type: "algorithm"
status: "active"
authority: "executable"
title: "RAW normalization and selected candle construction"
version: "current"
related_entities: ["algorithm.reaction", "core.chronology", "core.pipeline", "core.precision"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/core_utils.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
implemented_by: ["source.trading_pipeline", "source.reaction_engine", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L37", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L37"]
mirror_links: ["mirror.contract"]
---

# RAW normalization and selected candle construction

## Input normalization

Bridge parses complete supplied JSON row array after optional UTF-8 BOM removal. Rows use time/open/high/low/close; time becomes integer epoch,prices pass as_decimal. Cache keys include type and value to preserve string-normalized representation. Supplied chronology is consumed directly; build_candle_buckets does not sort,fill gaps or silently repair invalid OHLC.

Consecutive equal timestamps aggregate lower bucket with first open,max High,min Low,last close. Main time is timestamp when timeframe1,otherwise timestamp//timeframe*timeframe; same OHLC aggregation applies. Lower rows preserve finest supplied timestamps rather than inventing one-second candles.

## Candle and event model

Candle index is zero-based in complete supplied input. Epoch becomes Asia/Tehran local naive datetime; display is YYYY-MM-DD HH:MM:SS. GREEN iff close>=open,RED otherwise; Doji remains GREEN in both directions. OHLC stays Decimal. MarketChronology shares main/lower timestamp arrays and strict crossing/range-extreme index.

Requested from/to selects inclusive epoch-aligned presentation main buckets after input preparation. Empty rows or selected range raises. MarketContext outputs seconds,candles,lower_index,chronology,start_index,end_index. All stages share physical normalized input; serialization maps finalized state. This generic contract includes no stored market dataset or expected candle result.
