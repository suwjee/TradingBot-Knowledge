---
id: "case.fixture_2_3"
type: "case"
status: "active"
authority: "empirical"
title: "2.3 2026-09-17 — Exact-source E continuation"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bullish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"
dataset_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
timestamp: "2026-09-17 08:54:00"
behavior: "E"
behavior_detail: "E3 Blue continuation; no competing E1 Red"
algorithm: "algorithm.e"
source_module: "engine/pipeline/e_zone_detector.py"
source_function: "EZoneDetector._reconcile_candidate_chains"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "E2 Blue @ 2026-09-17 08:00:00"
next_behavior: "E3 Blue @ 2026-09-17 08:54:00"
stopall_boundary: "unknown"
expected_output: "E1 Blue 07:50:00 → E2 Blue 08:00:00 → E3 Blue 08:54:00; E1 Red 08:54:00 absent."
validation_target: "Same-source E continuation and cross-family conflict ownership"
validation_rule: "test.behavior_invariants"
related_entities: ["test.fixture_registry", "test.behavior_invariants", "algorithm.e", "source.e_zone_detector", "behavior.e"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1785", "engine/pipeline/e_zone_detector.py#L2463"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 211
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 2.3 2026-09-17 — Exact-source E continuation

## Validation claim

E1 Blue 07:50:00 → E2 Blue 08:00:00 → E3 Blue 08:54:00; E1 Red 08:54:00 absent.

**Purpose:** Same-source E continuation and cross-family conflict ownership. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 2.3, line 211, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 2.3 2026-09-17 — Exact-source E continuation
- Direction: Bullish chain
- E1 Blue: `07:50:00`
- E2 Blue: `08:00:00`
- E3 Blue: `08:54:00`
- Calculation-invalid S Red at `08:00:00` may remain evidence/Order provenance
- It must not open competing cross-family E1
- Incorrect E1 Red `08:54:00`: must not exist
- Status: **Active same-source ownership fixture**
