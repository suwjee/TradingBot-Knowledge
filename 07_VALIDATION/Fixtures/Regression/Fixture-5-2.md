---
id: "case.fixture_5_2"
type: "case"
status: "active"
authority: "empirical"
title: "5.2 2026-09-11 — stage ownership"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"
dataset_sha256: "9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c"
timestamp: "2026-09-11 18:01:30"
behavior: "A"
behavior_detail: "rejected fallback A after accepted S Blue"
algorithm: "algorithm.lifecycle"
source_module: "engine/pipeline/lifecycle_engine.py"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "S Blue @ 2026-09-11 17:43:00"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "A @ 2026-09-11 18:01:30 absent; accepted S Blue @ 17:43:00 retained."
validation_target: "Accepted S Blue must not be consumed by rejected fallback A"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.lifecycle", "source.lifecycle_engine", "behavior.a"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1817", "engine/pipeline/lifecycle_engine.py#L946"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 300
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 5.2 2026-09-11 — stage ownership

## Validation claim

A @ 2026-09-11 18:01:30 absent; accepted S Blue @ 17:43:00 retained.

**Purpose:** Accepted S Blue must not be consumed by rejected fallback A. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 5.2, line 300, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 5.2 2026-09-11 — stage ownership
- Accepted S Blue: `17:43:00`
- Would-be fallback A: `18:01:30`
- Expected: A `18:01:30` rejected / absent
- Accepted S Blue must not be consumed by rejected A
- Status: **Active stage-order regression**
