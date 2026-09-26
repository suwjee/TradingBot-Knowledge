---
id: "case.fixture_2_3"
type: "case"
status: "draft"
authority: "non-canonical"
title: "2.3 2026-09-17 — Exact-source E continuation"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bullish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json"
dataset_sha256: "ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9"
timestamp: "2026-09-17 08:54:00"
behavior: "E"
behavior_detail: "E3 Blue continuation; no competing E1 Red"
algorithm: "algorithm.e"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "E2 Blue @ 2026-09-17 08:00:00"
next_behavior: "E3 Blue @ 2026-09-17 08:54:00"
stopall_boundary: "unknown"
expected_output: "E1 Blue 07:50:00 → E2 Blue 08:00:00 → E3 Blue 08:54:00; E1 Red 08:54:00 absent."
validation_target: "Same-source E continuation and cross-family conflict ownership"
validation_rule: "test.behavior_invariants"
related_entities: ["algorithm.e", "behavior.e", "data.window_18632e27", "source.e_zone_detector", "test.behavior_invariants", "test.fixture_registry"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 142
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
dataset_window_first_epoch: 1788448440
dataset_window_last_epoch: 1789765175
dataset_window_row_count: 183741
dataset_window_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
---

# 2.3 2026-09-17 — Exact-source E continuation

## Pending validation claim (not an approved baseline)

E1 Blue 07:50:00 → E2 Blue 08:00:00 → E3 Blue 08:54:00; E1 Red 08:54:00 absent.

**Purpose:** Same-source E continuation and cross-family conflict ownership. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied scenario records this candidate assertion; its expected output is not approved as a regression baseline; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 142 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 2.3 2026-09-17 — Exact-source E continuation
- Direction: Bullish chain
- E1 Blue: `07:50:00`
- E2 Blue: `08:00:00`
- E3 Blue: `08:54:00`
- Calculation-invalid S Red at `08:00:00` may remain evidence/Order provenance
- It must not open competing cross-family E1
- Incorrect E1 Red `08:54:00`: must not exist
- Supplied scenario label: **Active same-source ownership fixture** (historical wording; current Vault status: Pending)

## Reproduction RAW window

Use `08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-23 18-01-15.json` and select the inclusive source-row interval `1788448440`–`1789765175`. The resulting 183741 rows reproduce SHA-256 `18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0` for the former small RAW. Do not calculate from the entire parent for this case.
