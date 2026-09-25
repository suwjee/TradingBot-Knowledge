---
id: "case.fixture_1_12"
type: "case"
status: "active"
authority: "empirical"
title: "1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-09-04 02:36:00"
behavior: "StopAll"
behavior_detail: "StopAll1; opposite-s-group-stop"
algorithm: "algorithm.stopall"
source_module: "engine/pipeline/lifecycle_engine.py"
source_function: "StopAllDetector._opposite_s_stopall_gate"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: true
expected_output: "Bearish StopAll1 @ 2026-09-04 02:36:00; old Bullish version is historical."
validation_target: "Repeated-Blue reversal gate with incoming native Mode-B S Red"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.stopall", "source.lifecycle_engine", "behavior.stopall"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1829", "engine/pipeline/lifecycle_engine.py#L356"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 140
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll

## Validation claim

Bearish StopAll1 @ 2026-09-04 02:36:00; old Bullish version is historical.

**Purpose:** Repeated-Blue reversal gate with incoming native Mode-B S Red. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 1.12, line 140, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll
- Current valid direction: Bearish
- Expected: `StopAll1`
- Gate: `opposite-s-group-stop`
- Incoming S Red has native Mode-B formation Order
- Historical Bullish version of the same timestamp is not current expected
- Status: **Active Bearish anchor / Bullish version superseded**
