---
id: "case.fixture_1_3"
type: "case"
status: "active"
authority: "empirical"
title: "1.3 2026-08-26 — native Mode-A Order_C owner"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-26 10:08:00"
behavior: "unknown"
behavior_detail: "native Mode-A Order_C owner"
algorithm: "algorithm.order.c"
source_module: "engine/pipeline/e_zone_detector.py"
source_function: "EZoneDetector._build_order_c_formations"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "native Mode-A Reset owner"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Eligible opposite Order First 2026-08-26 10:10:30; confirmation 10:11:30; earlier First 10:10:00 is ineligible."
validation_target: "Closed-range High strict crossing and shared physical Order roles"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.order.c", "source.e_zone_detector"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L15480", "engine/pipeline/e_zone_detector.py#L727"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 47
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 1.3 2026-08-26 — native Mode-A Order_C owner

## Validation claim

Eligible opposite Order First 2026-08-26 10:10:30; confirmation 10:11:30; earlier First 10:10:00 is ineligible.

**Purpose:** Closed-range High strict crossing and shared physical Order roles. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 1.3, line 47, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.3 2026-08-26 — native Mode-A Order_C owner
- Direction: Bearish
- Bearish owner First: `10:06:00`
- Owner Breakout: `10:07:00`
- Reset candle: `10:08:00`
- Previous Bearish Breakout: `09:58:30`
- Closed-range High: `4631.275`
- Exact RAW strict crossing: `10:10:45`
- Bullish First `10:10:00`, confirmation `10:10:35`: too early
- Correct eligible Bullish First: `10:10:30`
- Confirmation: `10:11:30`
- Same physical Order identity may contain both:
  - `parent-stop / Order_A`
  - `blue-leg / Order_C`
- Status: **Active current anchor**
