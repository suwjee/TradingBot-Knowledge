---
id: "case.fixture_5_3"
type: "case"
status: "draft"
authority: "non-canonical"
title: "5.3 USOIL Bearish Order_A / Order_C chain remembered from prior chat"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "EdgeCase"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"
dataset_sha256: "9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c"
timestamp: "unknown"
behavior: "S"
behavior_detail: "remembered S Red and separate Order_A/Order_C routes"
algorithm: "algorithm.order"
source_module: "engine/pipeline/s_zone_detector.py"
source_function: "SZoneDetector._first_order_after"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Unverified: S Red 13:55:00, Order_A 14:35:00 and separate Order_C 17:19:00; calendar date unknown."
validation_target: "Separate Order creation causes without automatic Order_A refresh"
validation_rule: "test.identity_invariants"
related_entities: ["test.fixture_registry", "test.identity_invariants", "algorithm.order", "source.s_zone_detector", "behavior.s"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1833", "engine/pipeline/s_zone_detector.py#L277"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 307
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 5.3 USOIL Bearish Order_A / Order_C chain remembered from prior chat

## Validation claim

Unverified: S Red 13:55:00, Order_A 14:35:00 and separate Order_C 17:19:00; calendar date unknown.

**Purpose:** Separate Order creation causes without automatic Order_A refresh. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied event is retained as a candidate. The cited reference/source establish the general rule, but the specific occurrence or expected output remains unverified. The fixture source is section 5.3, line 307, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 5.3 USOIL Bearish Order_A / Order_C chain remembered from prior chat
- S Red: `13:55:00`
- S stop: `14:34:30`
- Reaction / Order_A candidate: `14:35:00`
- Later Reset: `17:17:30`
- Later Reaction / separately proven Order_C: `17:19:00`
- Fixture purpose:
  - Order_A `14:35`
  - Order_C `17:19`
  - are separate creation causes/routes
  - later Order must not automatically refresh earlier Order_A
- Exact calendar date was not safely recoverable from context, so it is intentionally not guessed.
- Status: **Remembered regression case; date not re-verified**

---
