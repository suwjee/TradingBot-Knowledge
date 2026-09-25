---
id: "case.fixture_3_1"
type: "case"
status: "active"
authority: "empirical"
title: "3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json"
dataset_sha256: "f531a06d89e518964d4579f6b126ffdcd2b4f31fe2b6e4828ef71fd122809da3"
timestamp: "2026-09-04 16:58:38"
behavior: "A"
behavior_detail: "A source at 16:57:30 frozen by exact 1s confirmation"
algorithm: "algorithm.a"
source_module: "06_SOURCE/Code/engine/pipeline/a_zone_detector.py"
source_function: "AZoneDetector._a_source"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "A source remains 2026-09-04 16:57:30; moving A to 16:58:30 is wrong."
validation_target: "Exact lower-timeframe Reaction confirmation fixes A source"
validation_rule: "test.chronology_invariants"
related_entities: ["algorithm.a", "behavior.a", "data.window_0291455b", "source.a_zone_detector", "test.chronology_invariants", "test.fixture_registry"]
source_reference: ["06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L547"]
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 168
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
dataset_window_first_epoch: 1788449740
dataset_window_last_epoch: 1788824908
dataset_window_row_count: 161376
dataset_window_sha256: "0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776"
---

# 3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership

## Validation claim

A source remains 2026-09-04 16:57:30; moving A to 16:58:30 is wrong.

**Purpose:** Exact lower-timeframe Reaction confirmation fixes A source. **Status:** Active; **authority:** Canonical.

## Evidence boundary

The supplied scenario and retained local source support this bounded assertion; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 168 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership
- Direction: Bearish
- A source: `16:57:30`
- Bearish Reaction FirstGreen: `16:58:00`
- BoxBottom source: `16:57:30`
- BoxTop source: `16:58:00`
- Exact 1s breakdown confirmation: `16:58:38`
- Expected: A source freezes at exact confirmation
- Wrong candidate: moving A to `16:58:30`
- Status: **Active exact chronology fixture**

## Reproduction RAW window

Use `08_DATA/Raw/XAUUSD/RAW FARAZ_FOREXCOM_XAUUSD 1S FROM 1788449740 TO 1789388126.json` and select the inclusive source-row interval `1788449740`–`1788824908`. The resulting 161376 rows reproduce SHA-256 `0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776` for the former small RAW. Do not calculate from the entire parent for this case.
