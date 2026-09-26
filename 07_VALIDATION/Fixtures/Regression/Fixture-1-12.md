---
id: "case.fixture_1_12"
type: "case"
status: "draft"
authority: "non-canonical"
title: "1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-09-04 02:36:00"
behavior: "StopAll"
behavior_detail: "StopAll1; opposite-s-group-stop"
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
stopall_boundary: true
expected_output: "Bearish StopAll1 @ 2026-09-04 02:36:00; old Bullish version is historical."
validation_target: "Repeated-Blue reversal gate with incoming native Mode-B S Red"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.stopall", "source.lifecycle_engine", "behavior.stopall"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 106
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll

## Pending validation claim (not an approved baseline)

Bearish StopAll1 @ 2026-09-04 02:36:00; old Bullish version is historical.

**Purpose:** Repeated-Blue reversal gate with incoming native Mode-B S Red. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied scenario records this candidate assertion; its expected output is not approved as a regression baseline; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 106 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll
- Current valid direction: Bearish
- Expected: `StopAll1`
- Gate: `opposite-s-group-stop`
- Incoming S Red has native Mode-B formation Order
- Historical Bullish version of the same timestamp is not current expected
- Supplied scenario label: **Active Bearish anchor / Bullish version superseded** (historical wording; current Vault status: Pending)
