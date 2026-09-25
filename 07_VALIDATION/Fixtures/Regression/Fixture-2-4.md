---
id: "case.fixture_2_4"
type: "case"
status: "active"
authority: "empirical"
title: "2.4 2026-09-17 — downstream StopAll consequence"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bullish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"
dataset_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
timestamp: "2026-09-17 18:30:30"
behavior: "StopAll"
behavior_detail: "negative downstream StopAll assertion"
algorithm: "algorithm.stopall"
source_module: "engine/pipeline/lifecycle_engine.py"
source_function: "StopAllDetector.detect"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "StopAll @ 2026-09-17 18:30:30 absent because invalid Red E root is absent."
validation_target: "Downstream lifecycle consequence of rejected Red E root"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.stopall", "source.lifecycle_engine", "behavior.stopall"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1789", "engine/pipeline/lifecycle_engine.py#L403"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 221
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 2.4 2026-09-17 — downstream StopAll consequence

## Validation claim

StopAll @ 2026-09-17 18:30:30 absent because invalid Red E root is absent.

**Purpose:** Downstream lifecycle consequence of rejected Red E root. **Status:** Active; **authority:** Canonical.

## Evidence boundary

Current assertion supported by the synchronized reference and the named source owner; no fresh engine run or complete serialized output hash is claimed. The fixture source is section 2.4, line 221, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 2.4 2026-09-17 — downstream StopAll consequence
- Historical incorrect StopAll: `18:30:30`
- Expected current: **absent**
- Reason: invalid Red E root no longer exists
- Status: **Active negative regression fixture**
