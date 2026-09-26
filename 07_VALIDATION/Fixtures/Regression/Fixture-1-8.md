---
id: "case.fixture_1_8"
type: "case"
status: "draft"
authority: "non-canonical"
title: "1.8 V5.4.3 dominant Red E / cycle ownership"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-27 03:55:00"
behavior: "S"
behavior_detail: "S Red after dominant Red E history"
algorithm: "algorithm.lifecycle"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "E1 Red @ 2026-08-27 03:34:30"
next_behavior: "unknown"
stopall_boundary: true
expected_output: "S Red @ 2026-08-27 03:55:00 accepted, not StopAll; A @ 04:41:30 absent."
validation_target: "Dominant Red E cycle ownership across StopAll boundary"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.lifecycle", "source.lifecycle_engine", "behavior.s"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 63
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 1.8 V5.4.3 dominant Red E / cycle ownership

## Pending validation claim (not an approved baseline)

S Red @ 2026-08-27 03:55:00 accepted, not StopAll; A @ 04:41:30 absent.

**Purpose:** Dominant Red E cycle ownership across StopAll boundary. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied scenario records this candidate assertion; its expected output is not approved as a regression baseline; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 63 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.8 V5.4.3 dominant Red E / cycle ownership
- StopAll boundary: `2026-08-26 02:21:30`
- E1 Red repeats:
  - `2026-08-26 06:13:30`
  - `2026-08-26 09:00:30`
  - `2026-08-27 03:34:30`
- S Red: `2026-08-27 03:55:00`
- Expected: accepted S Red, **not StopAll**
- A `2026-08-27 04:41:30`: expected absent / cycle-invalid
- Supplied scenario label: **Active regression anchor** (historical wording; current Vault status: Pending)
