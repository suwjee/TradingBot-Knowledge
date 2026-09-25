---
id: "case.fixture_2_1"
type: "case"
status: "active"
authority: "empirical"
title: "2.1 2026-09-04 — canonical Order_B"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"
dataset_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
timestamp: "2026-09-04 09:45:55"
behavior: "unknown"
behavior_detail: "physical Bullish Order_B in Bearish calculation"
algorithm: "algorithm.order.b"
source_module: "engine/pipeline/e_zone_detector.py"
source_function: "EZoneDetector._build_order_b_formations"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Order_B First 2026-09-04 09:45:00, Break 09:45:30, exact confirmation 09:45:55."
validation_target: "Bounded evidence range, strict floor break, and Order_B identity"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.order.b", "source.e_zone_detector"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1799", "engine/pipeline/e_zone_detector.py#L499"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 176
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 2.1 2026-09-04 — canonical Order_B

## Validation claim

Order_B First 2026-09-04 09:45:00, Break 09:45:30, exact confirmation 09:45:55.

**Purpose:** Bounded evidence range, strict floor break, and Order_B identity. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 2.1, line 176, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 2.1 2026-09-04 — canonical Order_B
- Direction: Bearish calculation
- Physical Order direction: Bullish
- Bearish Reaction First: `09:24:00`
- Breakout main: `09:24:30`
- Reset main: `09:25:30`
- Breakout→Reset minimum Low: `4467.370`
- Floor source main: `09:25:00`
- Exact strict floor break: `09:42:10`
- Crossing main candle: `09:42:00`
- Evidence interval: `09:25:00 .. 09:42:00`
- Raw Bullish evidence:
  - First: `09:27:00`
  - Break: `09:28:00`
- Maximum High in evidence range: `4473.530`
- Ceiling source: `09:31:30`
- Physical Order_B:
  - Bullish First: `09:45:00`
  - Break: `09:45:30`
  - Exact confirmation: `09:45:55`
- Status: **Active canonical Order_B fixture**
