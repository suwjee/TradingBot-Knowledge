---
id: "case.fixture_1_11"
type: "case"
status: "active"
authority: "empirical"
title: "1.11 2026-08-28 — S Blue Type-4"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "EdgeCase"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-28 06:34:15"
behavior: "S"
behavior_detail: "S Blue Type-4"
algorithm: "algorithm.s.type4"
source_module: "engine/pipeline/s_zone_detector.py"
source_function: "SZoneDetector._first_type4"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "A stopped @ 2026-08-28 06:22:00"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "S Blue Type-4 following strict crossing @ 2026-08-28 06:34:15."
validation_target: "Type-4 source and exact lower-timeframe strict crossing"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.s.type4", "source.s_zone_detector", "behavior.s"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1825", "engine/pipeline/s_zone_detector.py#L543"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 127
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 1.11 2026-08-28 — S Blue Type-4

## Validation claim

S Blue Type-4 following strict crossing @ 2026-08-28 06:34:15.

**Purpose:** Type-4 source and exact lower-timeframe strict crossing. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 1.11, line 127, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.11 2026-08-28 — S Blue Type-4
- A: `06:22:00`, then Stop
- Bearish Reaction:
  - First: `06:31:30`
  - Breakout: `06:32:00`
- Type-4 candidate:
  - Main source: `06:30:30`
  - Price: `4587.505`
- Blue: `06:34:00`
- Exact strict crossing: `06:34:15`
- Expected: `S Blue Type-4`
- Status: **Active Type-4 fixture**
