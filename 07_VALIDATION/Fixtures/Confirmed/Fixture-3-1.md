---
id: "case.fixture_3_1"
type: "case"
status: "active"
authority: "empirical"
title: "3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 1S FROM 2026-09-03 19-05-40 TO 2026-09-08 03-18-28.json"
dataset_sha256: "0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776"
timestamp: "2026-09-04 16:58:38"
behavior: "A"
behavior_detail: "A source at 16:57:30 frozen by exact 1s confirmation"
algorithm: "algorithm.a"
source_module: "engine/pipeline/a_zone_detector.py"
source_function: "AZoneDetector._a_source"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "A source remains 2026-09-04 16:57:30; moving A to 16:58:30 is wrong."
validation_target: "Exact lower-timeframe Reaction confirmation fixes A source"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.a", "source.a_zone_detector", "behavior.a"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1777", "engine/pipeline/a_zone_detector.py#L547"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 237
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership

## Validation claim

A source remains 2026-09-04 16:57:30; moving A to 16:58:30 is wrong.

**Purpose:** Exact lower-timeframe Reaction confirmation fixes A source. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 3.1, line 237, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership
- Direction: Bearish
- A source: `16:57:30`
- Bearish Reaction FirstGreen: `16:58:00`
- BoxBottom source: `16:57:30`
- BoxTop source: `16:58:00`
- Exact 1s breakdown confirmation: `16:58:38`
- Expected: A source freezes at exact confirmation
- Wrong candidate: moving A to `16:58:30`
- Status: **Active exact chronology fixture**
