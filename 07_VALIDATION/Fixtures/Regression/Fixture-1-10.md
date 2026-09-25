---
id: "case.fixture_1_10"
type: "case"
status: "draft"
authority: "non-canonical"
title: "1.10 2026-08-28 — exact-key StopAll"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-28 03:41:00"
behavior: "S"
behavior_detail: "S Red; E3 Blue exact-key history"
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
stopall_boundary: false
expected_output: "S Red @ 2026-08-28 03:41:00, not StopAll; E1/E2/E3 are distinct Blue keys."
validation_target: "Blue repetition requires identical key, not family sequence length"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.stopall", "source.lifecycle_engine", "behavior.s"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 86
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 1.10 2026-08-28 — exact-key StopAll

## Validation claim

S Red @ 2026-08-28 03:41:00, not StopAll; E1/E2/E3 are distinct Blue keys.

**Purpose:** Blue repetition requires identical key, not family sequence length. **Status:** Active; **authority:** Canonical.

## Evidence boundary

The supplied scenario and retained local source support this bounded assertion; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 86 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.10 2026-08-28 — exact-key StopAll
- E3 Blue: only one occurrence
- S Red: `03:41:00`
- Expected: **not StopAll**
- E1→E2→E3 must not count as three occurrences of one Blue group.
- Status: **Active**
