---
id: "data.dataset_f531a06d"
type: "data"
data_kind: "dataset"
status: "draft"
authority: "non-canonical"
title: "XAUUSD 1s RAW 2026-09-03 / f531a06d"
created: "2026-09-25"
updated: "2026-09-25"
name: "RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json"
symbol: "XAUUSD"
broker: "FOREXCOM"
market: "unknown"
source: "unknown"
instrument: "unknown"
timeframe: "1s"
resolution: "1s"
start_time: "2026-09-03 19:05:40 Asia/Tehran (+03:30)"
end_time: "2026-09-15 23:19:44 Asia/Tehran (+03:30)"
timezone: "Asia/Tehran"
direction_support: ["Bullish", "Bearish"]
consumed_by_algorithms: ["algorithm.raw"]
produces_behaviors: []
used_by_fixtures: []
validated_by: ["test.fixture_registry", "test.baseline_policy"]
chronology_model: "core.chronology"
regression_role: "available-unanchored"
hash_reference: "data.hash_registry"
raw_path: "D:/My-Projects/TradingBot/data/raw/FOREXCOM/XAUUSD/RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json"
raw_locations: ["D:/My-Projects/TradingBot/data/raw/FOREXCOM/XAUUSD/RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json"]
raw_sha256: "f531a06d89e518964d4579f6b126ffdcd2b4f31fe2b6e4828ef71fd122809da3"
raw_bytes: 50789635
row_count: 621326
first_epoch: 1788449740
last_epoch: 1789501784
integrity_status: "pending_metadata_conflict"
related_entities: ["data.raw_model", "data.candle_model", "data.hash_registry", "data.dataset_manifest", "data.data_validation", "core.chronology", "algorithm.raw", "source.trading_pipeline", "test.fixture_registry", "test.baseline_policy", "test.regression_policy"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/bridge/trading_pipeline.py#L1732"]
---

# XAUUSD 1s RAW 2026-09-03 / f531a06d

This entity identifies exact RAW bytes, not an algorithm or a directional dataset. The broker/symbol and nominal input interval are supported by the filename and, where present, a matching production sidecar. `market` and `instrument` remain unknown because the physical file does not establish the trading venue or contract type. `direction_support` means the pipeline can interpret the same input in either direction; it is not a completed two-direction run.

## Physical identity and observed integrity

- SHA-256: `f531a06d89e518964d4579f6b126ffdcd2b4f31fe2b6e4828ef71fd122809da3`; 50789635 bytes; 621326 rows.
- First row: `2026-09-03 19:05:40 Asia/Tehran (+03:30)` (epoch `1788449740`); last row: `2026-09-15 23:19:44 Asia/Tehran (+03:30)` (epoch `1789501784`).
- Input interval: nominal 1s from filename and observed minimum step; 28387 adjacent intervals exceed that step; maximum observed interval 176481s.
- Paths with byte-identical content:
- `D:/My-Projects/TradingBot/data/raw/FOREXCOM/XAUUSD/RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json`

No production sidecar is present for this exact byte stream. The filename terminal epoch is 1789388126, while the last actual row is 1789501784; the file exists but this metadata discrepancy remains unresolved. No current output claim is promoted from the legacy FARAZ memory.

## Usage and authority boundary

Fixture dependencies: No registered Phase 5 fixture uses this hash.

Positive behavior subset evidenced by current fixtures: No positive behavior outcome is asserted from current registered fixtures. This is not a complete output inventory. The direct calculation consumer is `algorithm.raw`; downstream behavior is owned by the source and algorithm layers. No full-payload baseline or new pipeline run was produced merely by registering this dataset.
