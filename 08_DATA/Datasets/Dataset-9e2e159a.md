---
id: "data.dataset_9e2e159a"
type: "data"
data_kind: "dataset"
status: "active"
authority: "empirical"
title: "USOIL 5s RAW 2026-09-11 / 9e2e159a"
created: "2026-09-25"
updated: "2026-09-25"
name: "RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"
symbol: "USOIL"
broker: "FXCM"
market: "unknown"
source: "import"
instrument: "unknown"
timeframe: "5s"
resolution: "5s"
start_time: "2026-09-11 02:53:30 Asia/Tehran (+03:30)"
end_time: "2026-09-15 11:03:45 Asia/Tehran (+03:30)"
timezone: "Asia/Tehran"
direction_support: ["Bullish", "Bearish"]
consumed_by_algorithms: ["algorithm.raw"]
produces_behaviors: ["behavior.s"]
used_by_fixtures: ["case.fixture_5_1", "case.fixture_5_2"]
validated_by: ["test.fixture_registry", "test.baseline_policy"]
chronology_model: "core.chronology"
regression_role: "fixture-backed"
hash_reference: "data.hash_registry"
raw_path: "08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"
raw_locations: ["08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"]
raw_sha256: "9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c"
raw_bytes: 2941746
row_count: 36821
first_epoch: 1789082610
last_epoch: 1789457625
integrity_status: "verified"
related_entities: ["data.raw_model", "data.candle_model", "data.hash_registry", "data.dataset_manifest", "data.data_validation", "core.chronology", "algorithm.raw", "source.trading_pipeline", "test.fixture_registry", "test.baseline_policy", "test.regression_policy", "behavior.s", "case.fixture_5_1", "case.fixture_5_2"]
source_reference: []
---

# USOIL 5s RAW 2026-09-11 / 9e2e159a

This entity identifies exact RAW bytes, not an algorithm or a directional dataset. The broker/symbol and nominal input interval are supported by the filename and, where present, a matching production sidecar. `market` and `instrument` remain unknown because the physical file does not establish the trading venue or contract type. `direction_support` means the pipeline can interpret the same input in either direction; it is not a completed two-direction run.

## Physical identity and observed integrity

- SHA-256: `9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c`; 2941746 bytes; 36821 rows.
- First row: `2026-09-11 02:53:30 Asia/Tehran (+03:30)` (epoch `1789082610`); last row: `2026-09-15 11:03:45 Asia/Tehran (+03:30)` (epoch `1789457625`).
- Input interval: nominal 5s from filename and observed minimum step; 1310 adjacent intervals exceed that step; maximum observed interval 177365s.
- Paths with byte-identical content:
- `08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json`

Production sidecar source label is `import`; its data SHA-256, byte count and candle count match the RAW. This label is not proof of upstream market/provider provenance. The present bytes, row schema, positive increasing epochs, OHLC bounds and nominal-grid alignment passed this snapshot inspection. Longer intervals are gap candidates, not independently proven missing market records.

## Usage and authority boundary

Fixture dependencies: `case.fixture_5_1` `case.fixture_5_2`

Positive behavior subset evidenced by current fixtures: `behavior.s` This is not a complete output inventory. The direct calculation consumer is `algorithm.raw`; downstream behavior is owned by the source and algorithm layers. No full-payload baseline or new pipeline run was produced merely by registering this dataset.
