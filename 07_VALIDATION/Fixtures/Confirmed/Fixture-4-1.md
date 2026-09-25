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
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json"
dataset_sha256: "062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6"
timestamp: "2026-09-09 19:09:45"
behavior: "unknown"
behavior_detail: "same-Break confirmation and Reset boundary"
algorithm: "algorithm.reset"
source_module: "engine/pipeline/reaction_engine.py"
source_function: "UnifiedReactionDetector._candidate_from_confirmation_remainder"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "19:09:30 remains Reset boundary after exact confirmation 19:09:45; later 19:09:50 event cannot create next normal FirstRed there."
validation_target: "Same main-candle Break/Reset chronology"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.reset", "source.reaction_engine"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1777", "engine/pipeline/reaction_engine.py#L1546"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 261
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 4.1 2026-09-09 — same-Break Bullish confirmation/reset

## Validation claim

19:09:30 remains Reset boundary after exact confirmation 19:09:45; later 19:09:50 event cannot create next normal FirstRed there.

**Purpose:** Same main-candle Break/Reset chronology. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 4.1, line 261, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 4.1 2026-09-09 — same-Break Bullish confirmation/reset
- Bullish Reaction Break main candle: `19:09:30`
- Exact confirmation: `19:09:45`
- Later lower event in same main candle: `19:09:50`
- Expected: `19:09:30` remains Reset boundary
- It cannot simultaneously become next normal Bullish FirstRed
- Status: **Active Reaction/Reset chronology fixture**
