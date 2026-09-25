---
id: "case.fixture_4_3"
type: "case"
status: "draft"
authority: "non-canonical"
title: "4.3 2026-09-10 — stage ownership / invalid fallback"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bullish"
timeframe: "30s"
dataset: "08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json"
dataset_sha256: "062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6"
timestamp: "2026-09-10 13:56:00"
behavior: "E"
behavior_detail: "E1 Blue→E2 Blue; rejected S Red fallback"
algorithm: "algorithm.lifecycle"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "E2 Blue @ 2026-09-10 14:26:30"
stopall_boundary: "unknown"
expected_output: "S Red @ 13:51:00 rejected; E1 Blue @ 13:56:00 continues to E2 Blue @ 14:26:30."
validation_target: "Accepted later-stage ownership blocks rejected A/S fallback"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.lifecycle", "source.lifecycle_engine", "behavior.e"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 200
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 4.3 2026-09-10 — stage ownership / invalid fallback

## Validation claim

S Red @ 13:51:00 rejected; E1 Blue @ 13:56:00 continues to E2 Blue @ 14:26:30.

**Purpose:** Accepted later-stage ownership blocks rejected A/S fallback. **Status:** Active; **authority:** Canonical.

## Evidence boundary

The supplied scenario and retained local source support this bounded assertion; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 200 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 4.3 2026-09-10 — stage ownership / invalid fallback
- Direction: Bullish
- Competing S Red: `13:51:00` → expected rejected
- E1 Blue: `13:56:00`
- E2 Blue: `14:26:30`
- Expected continuation: `E1 Blue → E2 Blue`
- Rejected A/S fallback cannot reopen accepted later-stage ownership
- Status: **Active A→S→E ownership regression**

---
