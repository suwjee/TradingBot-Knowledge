---
id: "case.fixture_1_8"
type: "case"
status: "active"
authority: "empirical"
title: "1.8 V5.4.3 dominant Red E / cycle ownership"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-27 03:55:00"
behavior: "S"
behavior_detail: "S Red after dominant Red E history"
algorithm: "algorithm.lifecycle"
source_module: "engine/pipeline/lifecycle_engine.py"
source_function: "StopAllDetector.detect"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "E1 Red @ 2026-08-27 03:34:30"
next_behavior: "unknown"
stopall_boundary: true
expected_output: "S Red @ 2026-08-27 03:55:00 accepted, not StopAll; A @ 04:41:30 absent."
validation_target: "Dominant Red E cycle ownership across StopAll boundary"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.lifecycle", "source.lifecycle_engine", "behavior.s"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1825", "engine/pipeline/lifecycle_engine.py#L403"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 97
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 1.8 V5.4.3 dominant Red E / cycle ownership

## Validation claim

S Red @ 2026-08-27 03:55:00 accepted, not StopAll; A @ 04:41:30 absent.

**Purpose:** Dominant Red E cycle ownership across StopAll boundary. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 1.8, line 97, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.8 V5.4.3 dominant Red E / cycle ownership
- StopAll boundary: `2026-08-26 02:21:30`
- E1 Red repeats:
  - `2026-08-26 06:13:30`
  - `2026-08-26 09:00:30`
  - `2026-08-27 03:34:30`
- S Red: `2026-08-27 03:55:00`
- Expected: accepted S Red, **not StopAll**
- A `2026-08-27 04:41:30`: expected absent / cycle-invalid
- Status: **Active regression anchor**
