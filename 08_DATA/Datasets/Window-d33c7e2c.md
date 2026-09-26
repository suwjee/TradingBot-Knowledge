---
id: "data.window_d33c7e2c"
type: "data"
data_kind: "window"
status: "active"
authority: "empirical"
title: "Verified RAW window d33c7e2c"
created: "2026-09-25"
updated: "2026-09-26"
symbol: "XAUUSD"
broker: "FOREXCOM"
market: "unknown"
source: "import"
instrument: "unknown"
timeframe: "5s"
resolution: "5s"
start_time: "2026-09-16 22:35:00 Asia/Tehran (+03:30)"
end_time: "2026-09-17 19:15:35 Asia/Tehran (+03:30)"
timezone: "Asia/Tehran"
direction_support: ["Bullish", "Bearish"]
consumed_by_algorithms: ["algorithm.raw"]
produces_behaviors: []
used_by_fixtures: []
validated_by: ["test.fixture_registry", "test.baseline_policy"]
chronology_model: "core.chronology"
regression_role: "available-unanchored"
hash_reference: "data.hash_registry"
raw_path: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json"
raw_sha256: "d33c7e2c46440f7a4495bac7d80b38101a635491f0f95b8ea353caa8fdb7d96d"
row_count: 14140
first_epoch: 1789585500
last_epoch: 1789659935
integrity_status: "verified"
related_entities: ["algorithm.raw", "core.chronology", "data.candle_model", "data.data_validation", "data.dataset_ea82be1a", "data.dataset_manifest", "data.hash_registry", "data.raw_model", "source.trading_pipeline", "test.baseline_policy", "test.fixture_registry", "test.regression_policy"]
source_reference: []
retained_raw_sha256: "ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9"
parent_dataset: "data.dataset_ea82be1a"
original_raw_bytes: 1156527
---

# Verified RAW window d33c7e2c

The 14140-candle historical RAW is represented in the active registry by the exact inclusive window from epoch `1789585500` through `1789659935` in `08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json`. No smaller physical file is retained. The slice, serialized as compact JSON, has SHA-256 `d33c7e2c46440f7a4495bac7d80b38101a635491f0f95b8ea353caa8fdb7d96d` and reproduces the former smaller RAW byte for byte. The retained parent has SHA-256 `ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9`. A consumer must apply this window before calculating a fixture that previously used the smaller file; using the whole parent changes chronology and physical indexes.
