---
id: "case.fixture_5_1"
type: "case"
status: "draft"
authority: "non-canonical"
title: "5.1 2026-09-11 — Bearish chained Blue carried-stop"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "EdgeCase"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"
dataset_sha256: "9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c"
timestamp: "2026-09-11 09:23:00"
behavior: "unknown"
behavior_detail: "stopped Bearish Blue carried-stop geometry"
algorithm: "algorithm.a"
source_module: "engine/pipeline/a_zone_detector.py"
source_function: "AZoneDetector._inherited_stop"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Supplied geometry rule only; exact computed High/stop and current serialized occurrence unverified."
validation_target: "Stopped Blue carried-stop range ending at next Bearish Reaction Breakout"
validation_rule: "test.mirror_validation"
related_entities: ["test.fixture_registry", "test.mirror_validation", "algorithm.a", "source.a_zone_detector", "algorithm.blue"]
source_reference: ["engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1785", "engine/pipeline/a_zone_detector.py#L494"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 293
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 5.1 2026-09-11 — Bearish chained Blue carried-stop

## Validation claim

Supplied geometry rule only; exact computed High/stop and current serialized occurrence unverified.

**Purpose:** Stopped Blue carried-stop range ending at next Bearish Reaction Breakout. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied event is retained as a candidate. The cited reference/source establish the general rule, but the specific occurrence or expected output remains unverified. The fixture source is section 5.1, line 293, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 5.1 2026-09-11 — Bearish chained Blue carried-stop
- Blue reference: `09:23:00`
- For a stopped Bearish Blue:
  - locate first valid Bearish Reaction after stop
  - compute maximum High from Blue stop main candle through complete next Bearish Reaction Breakout main candle inclusive
- Status: **Active mirror geometry anchor**

## Supplemental RAW check

The older `memory.txt` (SHA-256 `ecce37748e6393aceec0750004911215a96b85058b2c4327ad927768ab261bd2`, lines 973–995) reports max High `101.409` near the 09:23 Blue route and claims A 09:49 rejected / A 09:53 accepted. Directly scanning the pinned USOIL 5-second RAW over `2026-09-11 09:24:30 ≤ time < 2026-09-11 09:31:30` in Asia/Tehran gives max High `101.409` at exact `2026-09-11 09:29:05`. This verifies the numeric extreme for that bounded window. It does not establish the current full-pipeline A outputs, so this case remains Pending.
