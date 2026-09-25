---
id: "data.dataset_062df750"
type: "data"
data_kind: "dataset"
status: "active"
authority: "empirical"
title: "USOIL 5s RAW 2026-09-08 / 062df750"
created: "2026-09-25"
updated: "2026-09-25"
name: "RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json"
symbol: "USOIL"
broker: "FXCM"
market: "unknown"
source: "import"
instrument: "unknown"
timeframe: "5s"
resolution: "5s"
start_time: "2026-09-08 07:23:20 Asia/Tehran (+03:30)"
end_time: "2026-09-12 00:14:55 Asia/Tehran (+03:30)"
timezone: "Asia/Tehran"
direction_support: ["Bullish", "Bearish"]
consumed_by_algorithms: ["algorithm.raw"]
produces_behaviors: ["behavior.a", "behavior.s", "behavior.e"]
used_by_fixtures: ["case.fixture_4_1", "case.fixture_4_3"]
validated_by: ["test.fixture_registry", "test.baseline_policy"]
chronology_model: "core.chronology"
regression_role: "fixture-backed"
hash_reference: "data.hash_registry"
raw_path: "08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json"
raw_locations: ["08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json"]
raw_sha256: "062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6"
raw_bytes: 4495847
row_count: 57963
first_epoch: 1788839600
last_epoch: 1789159495
integrity_status: "verified"
related_entities: ["data.raw_model", "data.candle_model", "data.hash_registry", "data.dataset_manifest", "data.data_validation", "core.chronology", "algorithm.raw", "source.trading_pipeline", "test.fixture_registry", "test.baseline_policy", "test.regression_policy", "behavior.a", "behavior.s", "behavior.e", "case.fixture_4_1", "case.fixture_4_3"]
source_reference: []
---

# USOIL 5s RAW 2026-09-08 / 062df750

This entity identifies exact RAW bytes, not an algorithm or a directional dataset. The broker/symbol and nominal input interval are supported by the filename and, where present, a matching production sidecar. `market` and `instrument` remain unknown because the physical file does not establish the trading venue or contract type. `direction_support` means the pipeline can interpret the same input in either direction; it is not a completed two-direction run.

## Physical identity and observed integrity

- SHA-256: `062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6`; 4495847 bytes; 57963 rows.
- First row: `2026-09-08 07:23:20 Asia/Tehran (+03:30)` (epoch `1788839600`); last row: `2026-09-12 00:14:55 Asia/Tehran (+03:30)` (epoch `1789159495`).
- Input interval: nominal 5s from filename and observed minimum step; 2753 adjacent intervals exceed that step; maximum observed interval 3665s.
- Paths with byte-identical content:
- `08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json`

Production sidecar source label is `import`; its data SHA-256, byte count and candle count match the RAW. This label is not proof of upstream market/provider provenance. The present bytes, row schema, positive increasing epochs, OHLC bounds and nominal-grid alignment passed this snapshot inspection. Longer intervals are gap candidates, not independently proven missing market records.

## Usage and authority boundary

Fixture dependencies: `case.fixture_4_1` `case.fixture_4_3`

Positive behavior subset evidenced by current fixtures: `behavior.a` `behavior.s` `behavior.e` This is not a complete output inventory. The direct calculation consumer is `algorithm.raw`; downstream behavior is owned by the source and algorithm layers. No full-payload baseline or new pipeline run was produced merely by registering this dataset.
