---
id: "case.fixture_5_2"
type: "case"
status: "draft"
authority: "non-canonical"
title: "5.2 2026-09-11 — stage ownership"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"
dataset_sha256: "9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c"
timestamp: "2026-09-11 18:01:30"
behavior: "A"
behavior_detail: "rejected fallback A after accepted S Blue"
algorithm: "algorithm.lifecycle"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "S Blue @ 2026-09-11 17:43:00"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "A @ 2026-09-11 18:01:30 absent; accepted S Blue @ 17:43:00 retained."
validation_target: "Accepted S Blue must not be consumed by rejected fallback A"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.lifecycle", "source.lifecycle_engine", "behavior.a"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 221
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 5.2 2026-09-11 — stage ownership

## Pending validation claim (not an approved baseline)

A @ 2026-09-11 18:01:30 absent; accepted S Blue @ 17:43:00 retained.

**Purpose:** Accepted S Blue must not be consumed by rejected fallback A. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied scenario records this candidate assertion; its expected output is not approved as a regression baseline; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 221 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 5.2 2026-09-11 — stage ownership
- Accepted S Blue: `17:43:00`
- Would-be fallback A: `18:01:30`
- Expected: A `18:01:30` rejected / absent
- Accepted S Blue must not be consumed by rejected A
- Supplied scenario label: **Active stage-order regression** (historical wording; current Vault status: Pending)
