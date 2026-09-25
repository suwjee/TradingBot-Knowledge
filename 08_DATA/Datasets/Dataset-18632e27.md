---
id: "data.dataset_18632e27"
type: "data"
data_kind: "dataset"
status: "active"
authority: "empirical"
title: "XAUUSD 5s RAW 2026-09-03 / 18632e27"
created: "2026-09-25"
updated: "2026-09-25"
name: "RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"
symbol: "XAUUSD"
broker: "FOREXCOM"
market: "unknown"
source: "import"
instrument: "unknown"
timeframe: "5s"
resolution: "5s"
start_time: "2026-09-03 18:44:00 Asia/Tehran (+03:30)"
end_time: "2026-09-19 00:29:35 Asia/Tehran (+03:30)"
timezone: "Asia/Tehran"
direction_support: ["Bullish", "Bearish"]
consumed_by_algorithms: ["algorithm.raw"]
produces_behaviors: ["behavior.e"]
used_by_fixtures: ["case.fixture_2_1", "case.fixture_2_2", "case.fixture_2_3", "case.fixture_2_4", "case.fixture_2_5"]
validated_by: ["test.fixture_registry", "test.baseline_policy"]
chronology_model: "core.chronology"
regression_role: "fixture-backed"
hash_reference: "data.hash_registry"
raw_path: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"
raw_locations: ["D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json", "D:/My-Projects/TradingBot/data/raw/FOREXCOM/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"]
raw_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
raw_bytes: 15018536
row_count: 183741
first_epoch: 1788448440
last_epoch: 1789765175
integrity_status: "verified"
related_entities: ["data.raw_model", "data.candle_model", "data.hash_registry", "data.dataset_manifest", "data.data_validation", "core.chronology", "algorithm.raw", "source.trading_pipeline", "test.fixture_registry", "test.baseline_policy", "test.regression_policy", "behavior.e", "case.fixture_2_1", "case.fixture_2_2", "case.fixture_2_3", "case.fixture_2_4", "case.fixture_2_5"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/bridge/trading_pipeline.py#L1732"]
---

# XAUUSD 5s RAW 2026-09-03 / 18632e27

This entity identifies exact RAW bytes, not an algorithm or a directional dataset. The broker/symbol and nominal input interval are supported by the filename and, where present, a matching production sidecar. `market` and `instrument` remain unknown because the physical file does not establish the trading venue or contract type. `direction_support` means the pipeline can interpret the same input in either direction; it is not a completed two-direction run.

## Physical identity and observed integrity

- SHA-256: `18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0`; 15018536 bytes; 183741 rows.
- First row: `2026-09-03 18:44:00 Asia/Tehran (+03:30)` (epoch `1788448440`); last row: `2026-09-19 00:29:35 Asia/Tehran (+03:30)` (epoch `1789765175`).
- Input interval: nominal 5s from filename and observed minimum step; 535 adjacent intervals exceed that step; maximum observed interval 176485s.
- Paths with byte-identical content:
- `D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json`
- `D:/My-Projects/TradingBot/data/raw/FOREXCOM/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json`

Production sidecar source label is `import`; its data SHA-256, byte count and candle count match the RAW. This label is not proof of upstream market/provider provenance. The present bytes, row schema, positive increasing epochs, OHLC bounds and nominal-grid alignment passed this snapshot inspection. Longer intervals are gap candidates, not independently proven missing market records.

## Usage and authority boundary

Fixture dependencies: `case.fixture_2_1` `case.fixture_2_2` `case.fixture_2_3` `case.fixture_2_4` `case.fixture_2_5`

Positive behavior subset evidenced by current fixtures: `behavior.e` This is not a complete output inventory. The direct calculation consumer is `algorithm.raw`; downstream behavior is owned by the source and algorithm layers. No full-payload baseline or new pipeline run was produced merely by registering this dataset.
