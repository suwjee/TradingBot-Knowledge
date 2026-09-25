---
id: "case.fixture_3_2"
type: "case"
status: "active"
authority: "empirical"
title: "3.2 2026-09-07 — bounded Mode-A anchor"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "EdgeCase"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 1S FROM 2026-09-03 19-05-40 TO 2026-09-08 03-18-28.json"
dataset_sha256: "0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776"
timestamp: "2026-09-07 10:14:00"
behavior: "unknown"
behavior_detail: "current-leg Mode-A anchor"
algorithm: "algorithm.order.a"
source_module: "engine/pipeline/reaction_engine.py"
source_function: "UnifiedReactionDetector.first_order_reaction_after_gate"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Current-leg Mode-A anchor at 10:14:00 with stop source 10:13:30; older Reset provenance does not overwrite it."
validation_target: "Bounded Mode-A ownership and old Reset exclusion"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.order.a", "source.reaction_engine"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1781", "engine/pipeline/reaction_engine.py#L1758"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 248
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 3.2 2026-09-07 — bounded Mode-A anchor

## Validation claim

Current-leg Mode-A anchor at 10:14:00 with stop source 10:13:30; older Reset provenance does not overwrite it.

**Purpose:** Bounded Mode-A ownership and old Reset exclusion. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 3.2, line 248, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 3.2 2026-09-07 — bounded Mode-A anchor
- Direction: Bearish
- Reference Order: `10:14:00`
- Stop source: `10:13:30`
- Expected: resolved current-leg Mode-A anchor remains authoritative
- An older Reset must not overwrite it merely because historical Reset provenance exists
- Status: **Active geometry/anchor fixture**

---
