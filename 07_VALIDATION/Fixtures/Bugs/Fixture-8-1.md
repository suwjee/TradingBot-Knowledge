---
id: "case.fixture_8_1"
type: "case"
status: "archived"
authority: "historical"
title: "8.1 `2026-09-04 02:36:00` Bullish StopAll"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Bug"
fixture_status: "Historical"
fixture_authority: "Historical"
direction: "Bullish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-09-04 02:36:00"
behavior: "StopAll"
behavior_detail: "superseded Bullish StopAll claim"
algorithm: "algorithm.stopall"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Historical Bullish StopAll at 02:36:00 is not current; Bearish StopAll1 at same timestamp remains active."
validation_target: "Direction-specific historical expectation quarantine"
validation_rule: "test.mirror_validation"
related_entities: ["test.fixture_registry", "test.mirror_validation", "algorithm.stopall", "source.lifecycle_engine", "behavior.stopall"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 276
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 8.1 `2026-09-04 02:36:00` Bullish StopAll

## Validation claim

Historical Bullish StopAll at 02:36:00 is not current; Bearish StopAll1 at same timestamp remains active.

**Purpose:** Direction-specific historical expectation quarantine. **Status:** Historical; **authority:** Historical.

## Evidence boundary

The old assertion is superseded. Its current replacement is described above; this historical value must never serve as an active expected output. The Vault-local curated fixture section starts at line 276 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 8.1 `2026-09-04 02:36:00` Bullish StopAll
- Historical 5.4.4 example
- **Not current expected**
- Bearish StopAll1 at same timestamp remains current retained anchor
