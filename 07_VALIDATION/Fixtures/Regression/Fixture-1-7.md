---
id: "case.fixture_1_7"
type: "case"
status: "draft"
authority: "non-canonical"
title: "1.7 V5.4.2 lifecycle chain — Bearish"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "unknown"
behavior: "S"
behavior_detail: "S Red in fresh post-StopAll cycle"
algorithm: "algorithm.lifecycle"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "fresh cycle after StopAll"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: true
expected_output: "Unverified supplied claim: S Red at 17:43:00 remains S; full date and current serialized output unknown."
validation_target: "Old StopAll state must not leak into a fresh cycle"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.lifecycle", "source.lifecycle_engine", "behavior.s"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 48
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 1.7 V5.4.2 lifecycle chain — Bearish

## Pending validation claim (not an approved baseline)

Unverified supplied claim: S Red at 17:43:00 remains S; full date and current serialized output unknown.

**Purpose:** Old StopAll state must not leak into a fresh cycle. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied event is retained as a candidate. The general rule and specific occurrence require fresh source review and a verified run. The Vault-local curated fixture section starts at line 48 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.7 V5.4.2 lifecycle chain — Bearish
- Invalid A that must not exist: `11:07:00`
- Correct A: `11:15:30`
- S Red: `11:54:30`
- Second S Red: `12:47:00`
- StopAll1: `13:20:30`
- StopAll2: `15:20:30`
- Fresh cycle:
  - E1 Blue: `16:21:30`
  - A: `17:36:30`, then stops
  - S Red: `17:43:00`
  - E1 Red: `17:56:30`
- Expected: `S Red 17:43:00` must not immediately become StopAll from pre-StopAll state.
- Supplied source status claim: **Active lifecycle/StopAll boundary regression**; current Vault status: Pending.
