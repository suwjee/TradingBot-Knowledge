---
id: "case.fixture_1_1"
type: "case"
status: "active"
authority: "empirical"
title: "1.1 2026-08-25 — Order_A ownership / immutable first Order"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Confirmed"
fixture_status: "Active"
fixture_authority: "Canonical"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json"
dataset_sha256: "f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974"
timestamp: "2026-08-25 09:32:30"
behavior: "A"
behavior_detail: "stopped A; first Order_A ownership"
algorithm: "algorithm.order.a"
source_module: "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"
source_function: "SZoneDetector._first_order_after"
reaction_identity: "unknown"
order_identity: [689, 693]
first_index: 689
break_index: 693
lifecycle_state: "A stopped"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "First eligible Order_A keeps parent-stop ownership; later native Mode-B Orders do not refresh it."
validation_target: "Order_A parent-stop ownership and physical identity"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.order.a", "source.s_zone_detector", "behavior.a"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L277"]
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 21
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 1.1 2026-08-25 — Order_A ownership / immutable first Order

## Validation claim

First eligible Order_A keeps parent-stop ownership; later native Mode-B Orders do not refresh it.

**Purpose:** Order_A parent-stop ownership and physical identity. **Status:** Active; **authority:** Canonical.

## Evidence boundary

The supplied scenario and retained local source support this bounded assertion; no fresh engine run or complete serialized output hash is claimed. The Vault-local curated fixture section starts at line 21 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 1.1 2026-08-25 — Order_A ownership / immutable first Order
- Direction: Bearish
- A: `09:32:30`
- بعد از Stop شدن A، اولین Order معتبر مالک `parent-stop` می‌ماند.
- Physical identity قبلی: `(FirstIndex, BreakIndex) = (689,693)`
- Mode-Bهای بعدی حق ندارند Order_A را refresh کنند.
- Status: **Active current anchor**
