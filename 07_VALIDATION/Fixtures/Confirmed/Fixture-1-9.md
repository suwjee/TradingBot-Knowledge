---
id: "case.fixture_1_9"
type: "case"
status: "active"
authority: "empirical"
title: "1.9 Canonical Bullish Order geometry inside Bearish regression"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-27 08:37:10"
behavior: "unknown"
behavior_detail: "Bullish physical Order geometry inside Bearish calculation"
algorithm: "algorithm.order"
source_module: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
source_function: "UnifiedReactionDetector._candidate_from_confirmation_remainder"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "BoxTop 4620.825, BoxBottom 4619.565; lower event 08:37:10; later 08:37:50 low cannot rewrite BoxBottom."
validation_target: "Exact confirmation freezes physical Order geometry"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.order", "source.reaction_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1546"]
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 74
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 1.9 Canonical Bullish Order geometry inside Bearish regression

## Validation claim

BoxTop 4620.825, BoxBottom 4619.565; lower event 08:37:10; later 08:37:50 low cannot rewrite BoxBottom.

**Purpose:** Exact confirmation freezes physical Order geometry. **Status:** Active; **authority:** Canonical.

## Evidence boundary

The supplied scenario and retained local source support this bounded assertion; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 74 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.9 Canonical Bullish Order geometry inside Bearish regression
- Date: `2026-08-27`
- Order First: `08:36:30`
- BoxTop: `4620.825`
- BoxTop source main: `08:36:00`
- BoxBottom: `4619.565`
- BoxBottom source main: `08:37:00`
- Exact lower event: `08:37:10`
- Breakout main: `08:37:30`
- Later low `08:37:50`: post-confirmation and must not rewrite BoxBottom
- Status: **Active exact-confirmation geometry fixture**
