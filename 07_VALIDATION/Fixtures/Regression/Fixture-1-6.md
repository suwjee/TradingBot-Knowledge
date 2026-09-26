---
id: "case.fixture_1_6"
type: "case"
status: "draft"
authority: "non-canonical"
title: "1.6 2026-08-28 — A→S / native Mode-B eligibility anchor #3"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-28 08:56:30"
behavior: "S"
behavior_detail: "S Red"
algorithm: "algorithm.stopall"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "A @ 2026-08-28 08:31:30"
next_behavior: "unknown"
stopall_boundary: false
expected_output: "S Red @ 2026-08-28 08:56:30; no StopAll1; 08:57:00 is superseded."
validation_target: "Exact RAW chronology and native Mode-B eligibility"
validation_rule: "test.chronology_invariants"
related_entities: ["test.fixture_registry", "test.chronology_invariants", "algorithm.stopall", "source.lifecycle_engine", "behavior.s"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 41
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 1.6 2026-08-28 — A→S / native Mode-B eligibility anchor #3

## Pending validation claim (not an approved baseline)

S Red @ 2026-08-28 08:56:30; no StopAll1; 08:57:00 is superseded.

**Purpose:** Exact RAW chronology and native Mode-B eligibility. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied scenario records this candidate assertion; its expected output is not approved as a regression baseline; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 41 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.6 2026-08-28 — A→S / native Mode-B eligibility anchor #3
- A: `08:31:30`
- Correct S candle: `08:56:30`
- Earlier `08:57:00` result was corrected by exact RAW chronology.
- Expected: **S Red, not StopAll1**
- Supplied scenario label: **Active regression anchor** (historical wording; current Vault status: Pending)
