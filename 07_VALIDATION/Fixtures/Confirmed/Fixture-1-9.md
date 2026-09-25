---
id: "case.fixture_1_9"
type: "case"
status: "active"
authority: "empirical"
title: "1.9 Canonical Bullish Order geometry inside Bearish regression"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-27 08:37:10"
behavior: "unknown"
behavior_detail: "Bullish physical Order geometry inside Bearish calculation"
algorithm: "algorithm.order"
source_module: "engine/pipeline/reaction_engine.py"
source_function: "UnifiedReactionDetector._candidate_from_confirmation_remainder"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "BoxTop 4620.825, BoxBottom 4619.565; lower event 08:37:10; later 08:37:50 low cannot rewrite BoxBottom."
validation_target: "Exact confirmation freezes physical Order geometry"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.order", "source.reaction_engine"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1825", "engine/pipeline/reaction_engine.py#L1546"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 108
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 1.9 Canonical Bullish Order geometry inside Bearish regression

## Validation claim

BoxTop 4620.825, BoxBottom 4619.565; lower event 08:37:10; later 08:37:50 low cannot rewrite BoxBottom.

**Purpose:** Exact confirmation freezes physical Order geometry. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 1.9, line 108, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.9 Canonical Bullish Order geometry inside Bearish regression
- Date: `2026-08-27`
- Order First: `08:36:30`
- BoxTop: `4620.825`
- BoxTop source main: `08:36:00`
- BoxBottom: `4619.565`
- BoxBottom source main: `08:37:00`
- Exact lower event: `08:37:10`
- Breakout main: `08:37:30`
- Later low `08:37:50`: post-confirmation and must not rewrite BoxBottom
- Status: **Active exact-confirmation geometry fixture**
