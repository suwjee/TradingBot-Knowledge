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
dataset: "08_DATA/Raw/XAUUSD/RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json"
dataset_sha256: "f531a06d89e518964d4579f6b126ffdcd2b4f31fe2b6e4828ef71fd122809da3"
timestamp: "2026-09-07 10:14:00"
behavior: "unknown"
behavior_detail: "current-leg Mode-A anchor"
algorithm: "algorithm.order.a"
source_module: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
source_function: "UnifiedReactionDetector.first_order_reaction_after_gate"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Current-leg Mode-A anchor at 10:14:00 with stop source 10:13:30; older Reset provenance does not overwrite it."
validation_target: "Bounded Mode-A ownership and old Reset exclusion"
validation_rule: "test.identity_invariants"
related_entities: ["algorithm.order.a", "data.window_0291455b", "source.reaction_engine", "test.fixture_registry", "test.identity_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1758"]
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 179
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
dataset_window_first_epoch: 1788449740
dataset_window_last_epoch: 1788824908
dataset_window_row_count: 161376
dataset_window_sha256: "0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776"
---

# 3.2 2026-09-07 — bounded Mode-A anchor

## Validation claim

Current-leg Mode-A anchor at 10:14:00 with stop source 10:13:30; older Reset provenance does not overwrite it.

**Purpose:** Bounded Mode-A ownership and old Reset exclusion. **Status:** Active; **authority:** Canonical.

## Evidence boundary

The supplied scenario and retained local source support this bounded assertion; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 179 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 3.2 2026-09-07 — bounded Mode-A anchor
- Direction: Bearish
- Reference Order: `10:14:00`
- Stop source: `10:13:30`
- Expected: resolved current-leg Mode-A anchor remains authoritative
- An older Reset must not overwrite it merely because historical Reset provenance exists
- Status: **Active geometry/anchor fixture**

---

## Reproduction RAW window

Use `08_DATA/Raw/XAUUSD/RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json` and select the inclusive source-row interval `1788449740`–`1788824908`. The resulting 161376 rows reproduce SHA-256 `0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776` for the former small RAW. Do not calculate from the entire parent for this case.
