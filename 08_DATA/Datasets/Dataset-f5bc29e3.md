---
id: "data.dataset_f5bc29e3"
type: "data"
data_kind: "dataset"
status: "active"
authority: "empirical"
title: "XAUUSD 5s RAW 2026-08-25 / f5bc29e3"
created: "2026-09-25"
updated: "2026-09-25"
name: "RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
symbol: "XAUUSD"
broker: "FOREXCOM"
market: "unknown"
source: "unknown"
instrument: "unknown"
timeframe: "5s"
resolution: "5s"
start_time: "2026-08-25 03:53:30 Asia/Tehran (+03:30)"
end_time: "2026-09-19 00:29:30 Asia/Tehran (+03:30)"
timezone: "Asia/Tehran"
direction_support: ["Bullish", "Bearish"]
consumed_by_algorithms: ["algorithm.raw"]
produces_behaviors: ["behavior.a", "behavior.s", "behavior.e", "behavior.stopall"]
used_by_fixtures: ["case.fixture_1_1", "case.fixture_1_10", "case.fixture_1_11", "case.fixture_1_12", "case.fixture_1_13", "case.fixture_1_4", "case.fixture_1_5", "case.fixture_1_6", "case.fixture_1_7", "case.fixture_1_8", "case.fixture_1_9", "case.fixture_8_1"]
validated_by: ["test.fixture_registry", "test.baseline_policy"]
chronology_model: "core.chronology"
regression_role: "fixture-backed"
hash_reference: "data.hash_registry"
raw_path: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
raw_locations: ["08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"]
raw_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
raw_bytes: 25331244
row_count: 309906
first_epoch: 1787617410
last_epoch: 1789765170
integrity_status: "verified"
related_entities: ["data.raw_model", "data.candle_model", "data.hash_registry", "data.dataset_manifest", "data.data_validation", "core.chronology", "algorithm.raw", "source.trading_pipeline", "test.fixture_registry", "test.baseline_policy", "test.regression_policy", "behavior.a", "behavior.s", "behavior.e", "behavior.stopall", "case.fixture_1_1", "case.fixture_1_10", "case.fixture_1_11", "case.fixture_1_12", "case.fixture_1_13", "case.fixture_1_4", "case.fixture_1_5", "case.fixture_1_6", "case.fixture_1_7", "case.fixture_1_8", "case.fixture_1_9", "case.fixture_8_1"]
source_reference: []
---

# XAUUSD 5s RAW 2026-08-25 / f5bc29e3

This entity identifies exact RAW bytes, not an algorithm or a directional dataset. The broker/symbol and nominal input interval are supported by the filename and, where present, a matching production sidecar. `market` and `instrument` remain unknown because the physical file does not establish the trading venue or contract type. `direction_support` means the pipeline can interpret the same input in either direction; it is not a completed two-direction run.

## Physical identity and observed integrity

- SHA-256: `f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974`; 25331244 bytes; 309906 rows.
- First row: `2026-08-25 03:53:30 Asia/Tehran (+03:30)` (epoch `1787617410`); last row: `2026-09-19 00:29:30 Asia/Tehran (+03:30)` (epoch `1789765170`).
- Input interval: nominal 5s from filename and observed minimum step; 821 adjacent intervals exceed that step; maximum observed interval 176485s.
- Paths with byte-identical content:
- `08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json`

No production sidecar is present for this exact byte stream. The present bytes, row schema, positive increasing epochs, OHLC bounds and nominal-grid alignment passed this snapshot inspection. Longer intervals are gap candidates, not independently proven missing market records.

## Usage and authority boundary

Fixture dependencies: `case.fixture_1_1` `case.fixture_1_10` `case.fixture_1_11` `case.fixture_1_12` `case.fixture_1_13` `case.fixture_1_4` `case.fixture_1_5` `case.fixture_1_6` `case.fixture_1_7` `case.fixture_1_8` `case.fixture_1_9` `case.fixture_8_1`

Positive behavior subset evidenced by current fixtures: `behavior.a` `behavior.s` `behavior.e` `behavior.stopall` This is not a complete output inventory. The direct calculation consumer is `algorithm.raw`; downstream behavior is owned by the source and algorithm layers. No full-payload baseline or new pipeline run was produced merely by registering this dataset.
