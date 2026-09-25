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
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-09-04 02:36:00"
behavior: "StopAll"
behavior_detail: "superseded Bullish StopAll claim"
algorithm: "algorithm.stopall"
source_module: "engine/pipeline/lifecycle_engine.py"
source_function: "StopAllDetector._opposite_s_stopall_gate"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Historical Bullish StopAll at 02:36:00 is not current; Bearish StopAll1 at same timestamp remains active."
validation_target: "Direction-specific historical expectation quarantine"
validation_rule: "test.mirror_validation"
related_entities: ["test.fixture_registry", "test.mirror_validation", "algorithm.stopall", "source.lifecycle_engine", "behavior.stopall"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1820", "engine/pipeline/lifecycle_engine.py#L356"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 371
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 8.1 `2026-09-04 02:36:00` Bullish StopAll

## Validation claim

Historical Bullish StopAll at 02:36:00 is not current; Bearish StopAll1 at same timestamp remains active.

**Purpose:** Direction-specific historical expectation quarantine. **Status:** Historical; **authority:** Historical.

## Evidence boundary

The old assertion is superseded. Its current replacement is described above; this historical value must never serve as an active expected output. The fixture source is section 8.1, line 371, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 8.1 `2026-09-04 02:36:00` Bullish StopAll
- Historical 5.4.4 example
- **Not current expected**
- Bearish StopAll1 at same timestamp remains current retained anchor
