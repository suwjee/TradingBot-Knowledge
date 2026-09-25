---
id: "case.fixture_4_1"
type: "case"
status: "active"
authority: "empirical"
title: "4.1 2026-09-09 — same-Break Bullish confirmation/reset"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bullish"
timeframe: "30s"
dataset: "08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json"
dataset_sha256: "062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6"
timestamp: "2026-09-09 19:09:45"
behavior: "unknown"
behavior_detail: "same-Break confirmation and Reset boundary"
algorithm: "algorithm.reset"
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
expected_output: "19:09:30 remains Reset boundary after exact confirmation 19:09:45; later 19:09:50 event cannot create next normal FirstRed there."
validation_target: "Same main-candle Break/Reset chronology"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.reset", "source.reaction_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1546"]
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 192
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 4.1 2026-09-09 — same-Break Bullish confirmation/reset

## Validation claim

19:09:30 remains Reset boundary after exact confirmation 19:09:45; later 19:09:50 event cannot create next normal FirstRed there.

**Purpose:** Same main-candle Break/Reset chronology. **Status:** Active; **authority:** Canonical.

## Evidence boundary

The supplied scenario and retained local source support this bounded assertion; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 192 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 4.1 2026-09-09 — same-Break Bullish confirmation/reset
- Bullish Reaction Break main candle: `19:09:30`
- Exact confirmation: `19:09:45`
- Later lower event in same main candle: `19:09:50`
- Expected: `19:09:30` remains Reset boundary
- It cannot simultaneously become next normal Bullish FirstRed
- Status: **Active Reaction/Reset chronology fixture**
