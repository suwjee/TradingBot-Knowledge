---
id: "case.fixture_6_1"
type: "case"
status: "draft"
authority: "non-canonical"
title: "6.1 2026-09-22 — stopped dominant E must advance +1"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Regression"
fixture_status: "Pending"
fixture_authority: "Pending"
direction: "Bearish"
timeframe: "30s"
dataset: "08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-22 11-00-00 TO 2026-09-24 00-05-40.json"
dataset_sha256: "b47246b45bb66db9ddfb75b6a431e5b6a7fced5fd521e358e5d5c438f91641dc"
timestamp: "2026-09-22 21:46:00"
behavior: "E"
behavior_detail: "claimed E5 Red after stopped dominant E4"
algorithm: "algorithm.e"
source_module: "unknown"
source_function: "unknown"
reaction_identity: "unknown"
order_identity: "unknown"
first_index: "unknown"
break_index: "unknown"
lifecycle_state: "unknown"
previous_behavior: "E4 Red @ 2026-09-22 16:02:00"
next_behavior: "claimed E6 @ 2026-09-22 23:07:30"
stopall_boundary: "unknown"
expected_output: "Unverified supplied claim: E5 Red @ 2026-09-22 21:46:00 and E6 @ 23:07:30; no independent current output."
validation_target: "Dominant E continuation increments family number after stop"
validation_rule: "test.behavior_invariants"
related_entities: ["test.fixture_registry", "test.behavior_invariants", "algorithm.e", "source.e_zone_detector", "behavior.e"]
source_reference: []
source_fixture: "07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 231
source_fixture_sha256: "0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5"
---

# 6.1 2026-09-22 — stopped dominant E must advance +1

## Validation claim

Unverified supplied claim: E5 Red @ 2026-09-22 21:46:00 and E6 @ 23:07:30; no independent current output.

**Purpose:** Dominant E continuation increments family number after stop. **Status:** Pending; **authority:** Pending.

## Evidence boundary

The supplied event is retained as a candidate. The general rule and specific occurrence require fresh source review and a verified run. The Vault-local curated fixture section starts at line 231 in the SHA-256-pinned source document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` lists retained local implementation anchors when available; `source_function` names the verified owner when present; `unknown` records an unresolved owner. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 6.1 2026-09-22 — stopped dominant E must advance +1
- Direction: Bearish
- E4 Red: `16:02:00`
- E2 stop exact RAW event: `21:22:25`
- E4 stop exact RAW event: `21:22:35`
- S: `21:42:00`
- Correct later E: `E5 Red @ 21:46:00`
- Next: `E6 @ 23:07:30`
- Fixture purpose:
  - after valid dominant En stops
  - a valid continuation must advance to `E(n+1)`
  - it must not repeat E4 or break numbering
- Supplied source status claim: **Active conversation regression anchor**; current Vault status: Pending.

---
