---
id: "case.fixture_2_5"
type: "case"
status: "archived"
authority: "historical"
title: "2.5 2026-09-17 — S reversal historical example"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Bug"
fixture_status: "Historical"
fixture_authority: "Historical"
direction: "Bullish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json"
dataset_sha256: "ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9"
timestamp: "2026-09-17 16:15:00"
behavior: "S"
behavior_detail: "historical S Red→StopAll reversal claim"
algorithm: "algorithm.stopall"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Historical StopAll claim superseded; current output is ordinary S Red with native Mode-A Order."
validation_target: "Prevent superseded StopAll expectation from entering current baseline"
validation_rule: "test.lifecycle_invariants"
related_entities: ["algorithm.stopall", "behavior.s", "data.window_18632e27", "source.lifecycle_engine", "test.fixture_registry", "test.lifecycle_invariants"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 158
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
dataset_window_first_epoch: 1788448440
dataset_window_last_epoch: 1789765175
dataset_window_row_count: 183741
dataset_window_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
---

# 2.5 2026-09-17 — S reversal historical example

## Validation claim

Historical StopAll claim superseded; current output is ordinary S Red with native Mode-A Order.

**Purpose:** Prevent superseded StopAll expectation from entering current baseline. **Status:** Historical; **authority:** Historical.

## Evidence boundary

The old assertion is superseded. Its current replacement is described above; this historical value must never serve as an active expected output. The Vault-local curated fixture section starts at line 158 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 2.5 2026-09-17 — S reversal historical example
- S Red: `16:15:00`
- Previously described as StopAll
- Current expected: ordinary `S Red` with native Mode-A Order
- Status: **Historical / Superseded StopAll expectation**

---

## Reproduction RAW window

Use `08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json` and select the inclusive source-row interval `1788448440`–`1789765175`. The resulting 183741 rows reproduce SHA-256 `18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0` for the former small RAW. Do not calculate from the entire parent for this case.
