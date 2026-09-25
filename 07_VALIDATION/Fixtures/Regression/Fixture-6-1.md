---
id: "case.fixture_6_1"
type: "case"
status: "draft"
authority: "non-canonical"
title: "6.1 2026-09-22 — stopped dominant E must advance +1"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot/data/raw/FOREXCOM/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-22 11-00-00 TO 2026-09-24 00-05-40.json"
dataset_sha256: "b47246b45bb66db9ddfb75b6a431e5b6a7fced5fd521e358e5d5c438f91641dc"
timestamp: "2026-09-22 21:46:00"
behavior: "E"
behavior_detail: "claimed E5 Red after stopped dominant E4"
algorithm: "algorithm.e"
source_module: "engine/pipeline/e_zone_detector.py"
source_function: "EZoneDetector._reconcile_candidate_chains"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "E4 Red @ 2026-09-22 16:02:00"
next_behavior: "claimed E6 @ 2026-09-22 23:07:30"
stopall_boundary: "unknown"
expected_output: "Unverified supplied claim: E5 Red @ 2026-09-22 21:46:00 and E6 @ 23:07:30; no independent current output."
validation_target: "Dominant E continuation increments family number after stop"
validation_rule: "test.behavior_invariants"
related_entities: ["test.fixture_registry", "test.behavior_invariants", "algorithm.e", "source.e_zone_detector", "behavior.e"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1829", "engine/pipeline/e_zone_detector.py#L2463"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 326
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 6.1 2026-09-22 — stopped dominant E must advance +1

## Validation claim

Unverified supplied claim: E5 Red @ 2026-09-22 21:46:00 and E6 @ 23:07:30; no independent current output.

**Purpose:** Dominant E continuation increments family number after stop. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied event is retained as a candidate. The cited reference/source establish the general rule, but the specific occurrence or expected output remains unverified. The fixture source is section 6.1, line 326, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 6.1 2026-09-22 — stopped dominant E must advance +1
- Direction: Bearish
- E4 Red: `16:02:00`
- E2 stop exact RAW event: `21:22:25`
- E4 stop exact RAW event: `21:22:35`
- S: `21:42:00`
- Correct later E: `E5 Red @ 21:46:00`
- Next: `E6 @ 23:07:30`
- Fixture purpose:
  - after valid dominant En stops
  - a valid continuation must advance to `E(n+1)`
  - it must not repeat E4 or break numbering
- Status: **Active conversation regression anchor**

---
