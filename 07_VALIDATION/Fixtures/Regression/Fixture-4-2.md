---
id: "case.fixture_4_2"
type: "case"
status: "active"
authority: "empirical"
title: "4.2 2026-09-09 — Bullish Blue→A→S→Order chain"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bullish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json"
dataset_sha256: "062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6"
timestamp: "2026-09-09 19:17:00"
behavior: "A"
behavior_detail: "rejected A candidate in Blue→A→S→Order chain"
algorithm: "algorithm.a"
source_module: "engine/pipeline/a_zone_detector.py"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "S Red @ 2026-09-09 19:09:30"
next_behavior: "A @ 2026-09-09 19:20:30"
stopall_boundary: "unknown"
expected_output: "A @ 19:17:00 rejected; later A @ 19:20:30 retained; S Blue @ 19:47:00."
validation_target: "Exact Reset and chained-Blue ownership"
validation_rule: "test.behavior_invariants"
related_entities: ["test.fixture_registry", "test.behavior_invariants", "algorithm.a", "source.a_zone_detector", "behavior.a"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1781", "engine/pipeline/a_zone_detector.py#L568"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 269
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 4.2 2026-09-09 — Bullish Blue→A→S→Order chain

## Validation claim

A @ 19:17:00 rejected; later A @ 19:20:30 retained; S Blue @ 19:47:00.

**Purpose:** Exact Reset and chained-Blue ownership. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 4.2, line 269, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 4.2 2026-09-09 — Bullish Blue→A→S→Order chain
- A: `19:06:30`
- S Red: `19:09:30`
- Order: `19:14:30`
- Rejected A candidate: `19:17:00`
- Correct later A: `19:20:30`
- S Blue: `19:47:00`
- Expected: A `19:17:00` rejected
- Status: **Active chained-Blue / exact-reset fixture**
