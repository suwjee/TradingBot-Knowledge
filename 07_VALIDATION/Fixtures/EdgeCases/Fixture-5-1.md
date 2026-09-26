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
dataset: "08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json"
dataset_sha256: "9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c"
timestamp: "2026-09-11 09:23:00"
behavior: "unknown"
behavior_detail: "stopped Bearish Blue carried-stop geometry"
algorithm: "algorithm.a"
source_module: "06_SOURCE/Code/engine/pipeline/a_zone_detector.py"
source_function: "AZoneDetector._inherited_stop"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Supplied geometry rule only; exact computed High/stop and current serialized occurrence unverified."
validation_target: "Stopped Blue carried-stop range ending at next Bearish Reaction Breakout"
validation_rule: "test.mirror_validation"
related_entities: ["test.fixture_registry", "test.mirror_validation", "algorithm.a", "source.a_zone_detector", "algorithm.blue"]
source_reference: ["06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L494"]
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 214
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 5.1 2026-09-11 — Bearish chained Blue carried-stop

## Pending validation claim (not an approved baseline)

Supplied geometry rule only; exact computed High/stop and current serialized occurrence unverified.

**Purpose:** Stopped Blue carried-stop range ending at next Bearish Reaction Breakout. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied event is retained as a candidate. The general rule and specific occurrence require fresh source review and a verified run. The Vault-local curated fixture section starts at line 214 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 5.1 2026-09-11 — Bearish chained Blue carried-stop
- Blue reference: `09:23:00`
- For a stopped Bearish Blue:
  - locate first valid Bearish Reaction after stop
  - compute maximum High from Blue stop main candle through complete next Bearish Reaction Breakout main candle inclusive
- Supplied source status claim: **Active mirror geometry anchor**; current Vault status: Pending.

## Supplemental RAW check

The older `memory.txt` (SHA-256 `ecce37748e6393aceec0750004911215a96b85058b2c4327ad927768ab261bd2`, lines 973–995) reports max High `101.409` near the 09:23 Blue route and claims A 09:49 rejected / A 09:53 accepted. Directly scanning the pinned USOIL 5-second RAW over `2026-09-11 09:24:30 ≤ time < 2026-09-11 09:31:30` in Asia/Tehran gives max High `101.409` at exact `2026-09-11 09:29:05`. This verifies the numeric extreme for that bounded window. It does not establish the current full-pipeline A outputs, so this case remains Pending.
