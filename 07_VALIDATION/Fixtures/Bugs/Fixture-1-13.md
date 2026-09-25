---
id: "case.fixture_1_13"
type: "case"
status: "archived"
authority: "historical"
title: "1.13 2026-09-09 — historical Mode-B refresh chain"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Bug"
fixture_status: "Historical"
fixture_authority: "Historical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-09-09 04:29:30"
behavior: "S"
behavior_detail: "superseded S Red from old Mode-B refresh chain"
algorithm: "algorithm.order.a"
source_module: "engine/pipeline/s_zone_detector.py"
source_function: "SZoneDetector._first_order_after"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "A @ 2026-09-09 03:33:30"
next_behavior: "current S Blue @ 2026-09-09 04:45:00"
stopall_boundary: "unknown"
expected_output: "Historical S Red 04:29:30 is not current; current first Order_A is 04:16:00 and full RAW emits S Blue 04:45:00."
validation_target: "Prevent historical Mode-B refresh output from becoming current baseline"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.order.a", "source.s_zone_detector", "behavior.s"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1833", "engine/pipeline/s_zone_detector.py#L277"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 148
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 1.13 2026-09-09 — historical Mode-B refresh chain

## Validation claim

Historical S Red 04:29:30 is not current; current first Order_A is 04:16:00 and full RAW emits S Blue 04:45:00.

**Purpose:** Prevent historical Mode-B refresh output from becoming current baseline. **Status:** Historical; **authority:** Historical.

## Evidence boundary

The old assertion is superseded. Its current replacement is described above; this historical value must never serve as an active expected output. The fixture source is section 1.13, line 148, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.13 2026-09-09 — historical Mode-B refresh chain
- A: `03:33:30`
- Consecutive opposite native Mode-B Order Firsts:
  - `04:16:00`
  - `04:17:30`
  - `04:20:30`
  - `04:24:00`
- Historical final Order stop source: `04:21:00`
- Under old V5.4.5:
  - final owner = `04:24:00`
  - S Red = `04:29:30`
  - S Blue `04:45:00` removed
  - E1 Red = `05:15:30`
  - StopAll = `06:23:00`
- Under current V5.4.8+:
  - Order_A remains First `04:16:00`
  - `04:24:00` cannot inherit its parent-stop
  - `S Red 04:29:30` is not current expected
  - current full-RAW emits `S Blue 04:45:00`
- Status: **Historical / Superseded, retained as regression provenance**

---
