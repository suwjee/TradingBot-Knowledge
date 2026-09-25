---
id: "data.dataset_ea82be1a"
type: "data"
data_kind: "dataset"
status: "active"
authority: "empirical"
title: "XAUUSD 5s RAW 2026-08-25 / ea82be1a"
created: "2026-09-25"
updated: "2026-09-25"
name: "RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json"
symbol: "XAUUSD"
broker: "FOREXCOM"
market: "unknown"
source: "import"
instrument: "unknown"
timeframe: "5s"
resolution: "5s"
start_time: "2026-08-25 03:53:30 Asia/Tehran (+03:30)"
end_time: "2026-09-23 18:01:15 Asia/Tehran (+03:30)"
timezone: "Asia/Tehran"
direction_support: ["Bullish", "Bearish"]
consumed_by_algorithms: ["algorithm.raw"]
produces_behaviors: ["behavior.e"]
used_by_fixtures: ["case.fixture_2_3", "case.fixture_2_4", "case.fixture_2_5"]
validated_by: ["test.fixture_registry", "test.baseline_policy"]
chronology_model: "core.chronology"
regression_role: "available-unanchored"
hash_reference: "data.hash_registry"
raw_path: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json"
raw_locations: ["08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json"]
raw_sha256: "ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9"
raw_bytes: 28991710
row_count: 354698
first_epoch: 1787617410
last_epoch: 1790173875
integrity_status: "verified"
related_entities: ["algorithm.raw", "behavior.e", "case.fixture_2_3", "case.fixture_2_4", "case.fixture_2_5", "core.chronology", "data.candle_model", "data.data_validation", "data.dataset_manifest", "data.hash_registry", "data.raw_model", "source.trading_pipeline", "test.baseline_policy", "test.fixture_registry", "test.regression_policy"]
source_reference: []
---

# XAUUSD 5s RAW 2026-08-25 / ea82be1a

This retained physical RAW contains the exact verified windows [18632e27](Window-18632e27.md) and [d33c7e2c](Window-d33c7e2c.md). Three retained fixtures use only the former window. Their input range and original window hash are recorded in each fixture; the entire parent is a different calculation input.

This entity identifies exact RAW bytes, not an algorithm or a directional dataset. The broker/symbol and nominal input interval are supported by the filename and, where present, a matching production sidecar. `market` and `instrument` remain unknown because the physical file does not establish the trading venue or contract type. `direction_support` means the pipeline can interpret the same input in either direction; it is not a completed two-direction run.

## Physical identity and observed integrity

- SHA-256: `ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9`; 28991710 bytes; 354698 rows.
- First row: `2026-08-25 03:53:30 Asia/Tehran (+03:30)` (epoch `1787617410`); last row: `2026-09-23 18:01:15 Asia/Tehran (+03:30)` (epoch `1790173875`).
- Input interval: nominal 5s from filename and observed minimum step; 991 adjacent intervals exceed that step; maximum observed interval 176485s.
- Paths with byte-identical content:
- `08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json`

Production sidecar source label is `import`; its data SHA-256, byte count and candle count match the RAW. This label is not proof of upstream market/provider provenance. The present bytes, row schema, positive increasing epochs, OHLC bounds and nominal-grid alignment passed this snapshot inspection. Longer intervals are gap candidates, not independently proven missing market records.

## Usage and authority boundary

Fixture dependencies: `case.fixture_2_3` `case.fixture_2_4` `case.fixture_2_5`

Positive behavior subset evidenced by current fixtures: No positive behavior outcome is asserted from current registered fixtures. This is not a complete output inventory. The direct calculation consumer is `algorithm.raw`; downstream behavior is owned by the source and algorithm layers. No full-payload baseline or new pipeline run was produced merely by registering this dataset.
