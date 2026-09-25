---
id: "case.fixture_2_2"
type: "case"
status: "active"
authority: "empirical"
title: "2.2 2026-09-04 — shared accepted-Order / parent-neutral use"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"
dataset_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
timestamp: "2026-09-04 17:55:45"
behavior: "E"
behavior_detail: "E uses accepted-live shared Order"
algorithm: "algorithm.e"
source_module: "engine/pipeline/e_zone_detector.py"
source_function: "EZoneDetector._post_stop_accepted_orders_for_parent"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "accepted-live Order use"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Physical Order retains original A parent-stop creation cause; E use provenance is accepted-live."
validation_target: "Separate creation cause from use provenance and parent-neutral reuse"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.e", "source.e_zone_detector", "behavior.e"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1813", "engine/pipeline/e_zone_detector.py#L1901"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 198
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 2.2 2026-09-04 — shared accepted-Order / parent-neutral use

## Validation claim

Physical Order retains original A parent-stop creation cause; E use provenance is accepted-live.

**Purpose:** Separate creation cause from use provenance and parent-neutral reuse. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 2.2, line 198, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 2.2 2026-09-04 — shared accepted-Order / parent-neutral use
- Physical Bullish Order First: `17:45:30`
- Canonical stop source:
  - `Low @ 17:41:30 = 4419.235`
- Exact Order confirmation: `17:55:45`
- Exact strict Order stop: `18:24:40`
- Different S Red parent stop: `17:13:05`
- Bearish E source:
  - `High @ 18:05:30 = 4442.395`
- Creation cause remains original A `parent-stop`
- E use provenance: `accepted-live`
- Status: **Active shared accepted-Order fixture**
