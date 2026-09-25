---
id: "case.fixture_1_2"
type: "case"
status: "active"
authority: "empirical"
title: "1.2 2026-08-25 — Order_C / Mode-B Reset owner"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-25 14:58:30"
behavior: "StopAll"
behavior_detail: "Mode-B Reset Order_C; downstream StopAll2"
algorithm: "algorithm.order.c"
source_module: "engine/pipeline/e_zone_detector.py"
source_function: "EZoneDetector._build_order_c_formations"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "Mode-B Reset owner"
previous_behavior: "unknown"
next_behavior: "StopAll2 @ 2026-08-25 15:20:30"
stopall_boundary: "unknown"
expected_output: "Order_C First 2026-08-25 15:16:30; exact confirmation 15:17:05; StopAll 15:10:30 absent; 15:20:30 is StopAll2."
validation_target: "Frozen-leg strict crossing and correct blue-leg owner"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.order.c", "source.e_zone_detector", "behavior.stopall"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L15476", "engine/pipeline/e_zone_detector.py#L727"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 23
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 1.2 2026-08-25 — Order_C / Mode-B Reset owner

## Validation claim

Order_C First 2026-08-25 15:16:30; exact confirmation 15:17:05; StopAll 15:10:30 absent; 15:20:30 is StopAll2.

**Purpose:** Frozen-leg strict crossing and correct blue-leg owner. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 1.2, line 23, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.2 2026-08-25 — Order_C / Mode-B Reset owner
- Direction: Bearish
- Previous Bearish Reaction:
  - First: `14:27:00`
  - Breakout: `14:28:30`
- Leg Start Reaction:
  - First: `14:50:00`
  - Breakout: `14:52:00`
- Reset owner:
  - First: `14:56:30`
  - Reset main candle: `14:58:30`
- Frozen leg High: `4645.225`
- Frozen High source:
  - Main: `14:49:30`
  - RAW 5s: `14:49:35`
- Exact strict `High > 4645.225`: `15:10:40`
- Bullish First `15:10:00`: too early / invalid as Order_C
- Correct physical Order_C:
  - First: `15:16:30`
  - Exact confirmation: `15:17:05`
- Incorrect historical `StopAll 15:10:30`: must be absent
- Later `StopAll 15:20:30`: current numbering = `StopAll2`
- Status: **Active V5.4.11 anchor**
