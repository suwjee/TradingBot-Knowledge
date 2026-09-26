---
id: "test.fixture_registry"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Fixture registry"
created: "2026-09-25"
updated: "2026-09-26"
related_entities: ["test.fixture_model", "test.validation_contract", "test.regression_policy", "test.source_validation", "test.mirror_validation", "test.test_model", "test.regression_test_execution"]
source_reference: []
---

# Fixture registry

The curated Vault-local fixture source is `07_VALIDATION/Fixtures/Sources/TradingBot_Fixtures_Regression_Anchors.md`, SHA-256 `0f49b80a0caa687b8f5e8fc5cb7d16dc934393528db5e0a7694d6ef744f440e5`. It contains only the retained case sections. Each case note pins its heading, RAW file, and any exact input window. All nine main Engine modules are now captured; Pending cases remain Pending because no newly approved full-payload regression baseline or route-specific review was established. No retained fixture explicitly claims Order_B or Order_C as its algorithm.

The fixture source's literal `5.4.11-HPZR5` label is preserved historical fixture evidence, not the current reference registry state. The current Bullish and Bearish HPZR6 documents are the hash-registered external references. Changing that pinned fixture source would require a deliberate review of all 22 fixture hashes, so this repair leaves every fixture SHA and review marker unchanged.

## Retained scenarios

| Section | Case | Kind | Status | Direction | Primary time |
| --- | --- | --- | --- | --- | --- |
| 1.1 | [1.1 2026-08-25 — Order_A ownership / immutable first Order](Confirmed/Fixture-1-1.md) | Confirmed | Active | Bearish | 2026-08-25 09:32:30 |
| 1.4 | [1.4 2026-08-26 — A→S / native Mode-B eligibility anchor #1](Regression/Fixture-1-4.md) | Regression | Pending | Bearish | 2026-08-26 11:04:00 |
| 1.5 | [1.5 2026-08-26 — A→S / native Mode-B eligibility anchor #2](Regression/Fixture-1-5.md) | Regression | Pending | Bearish | 2026-08-26 23:00:00 |
| 1.6 | [1.6 2026-08-28 — A→S / native Mode-B eligibility anchor #3](Regression/Fixture-1-6.md) | Regression | Pending | Bearish | 2026-08-28 08:56:30 |
| 1.7 | [1.7 V5.4.2 lifecycle chain — Bearish](Regression/Fixture-1-7.md) | Regression | Pending | Bearish | unknown |
| 1.8 | [1.8 V5.4.3 dominant Red E / cycle ownership](Regression/Fixture-1-8.md) | Regression | Pending | Bearish | 2026-08-27 03:55:00 |
| 1.9 | [1.9 Canonical Bullish Order geometry inside Bearish regression](Confirmed/Fixture-1-9.md) | Confirmed | Active | Bearish | 2026-08-27 08:37:10 |
| 1.10 | [1.10 2026-08-28 — exact-key StopAll](Regression/Fixture-1-10.md) | Regression | Pending | Bearish | 2026-08-28 03:41:00 |
| 1.11 | [1.11 2026-08-28 — S Blue Type-4](EdgeCases/Fixture-1-11.md) | EdgeCase | Active | Bearish | 2026-08-28 06:34:15 |
| 1.12 | [1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll](Regression/Fixture-1-12.md) | Regression | Pending | Bearish | 2026-09-04 02:36:00 |
| 1.13 | [1.13 2026-09-09 — historical Mode-B refresh chain](Bugs/Fixture-1-13.md) | Bug | Historical | Bearish | 2026-09-09 04:29:30 |
| 2.3 | [2.3 2026-09-17 — Exact-source E continuation](Regression/Fixture-2-3.md) | Regression | Pending | Bullish | 2026-09-17 08:54:00 |
| 2.4 | [2.4 2026-09-17 — downstream StopAll consequence](Regression/Fixture-2-4.md) | Regression | Pending | Bullish | 2026-09-17 18:30:30 |
| 2.5 | [2.5 2026-09-17 — S reversal historical example](Bugs/Fixture-2-5.md) | Bug | Historical | Bullish | 2026-09-17 16:15:00 |
| 3.1 | [3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership](Confirmed/Fixture-3-1.md) | Confirmed | Active | Bearish | 2026-09-04 16:58:38 |
| 3.2 | [3.2 2026-09-07 — bounded Mode-A anchor](EdgeCases/Fixture-3-2.md) | EdgeCase | Active | Bearish | 2026-09-07 10:14:00 |
| 4.1 | [4.1 2026-09-09 — same-Break Bullish confirmation/reset](Confirmed/Fixture-4-1.md) | Confirmed | Active | Bullish | 2026-09-09 19:09:45 |
| 4.3 | [4.3 2026-09-10 — stage ownership / invalid fallback](Regression/Fixture-4-3.md) | Regression | Pending | Bullish | 2026-09-10 13:56:00 |
| 5.1 | [5.1 2026-09-11 — Bearish chained Blue carried-stop](EdgeCases/Fixture-5-1.md) | EdgeCase | Pending | Bearish | 2026-09-11 09:23:00 |
| 5.2 | [5.2 2026-09-11 — stage ownership](Regression/Fixture-5-2.md) | Regression | Pending | Bearish | 2026-09-11 18:01:30 |
| 6.1 | [6.1 2026-09-22 — stopped dominant E must advance +1](Regression/Fixture-6-1.md) | Regression | Pending | Bearish | 2026-09-22 21:46:00 |
| 8.1 | [8.1 `2026-09-04 02:36:00` Bullish StopAll](Bugs/Fixture-8-1.md) | Bug | Historical | Bullish | 2026-09-04 02:36:00 |

**Total:** 22 cases: 3 Bug, 4 Confirmed, 3 EdgeCase, 12 Regression; 6 Active, 3 Historical, 13 Pending.

## Input identity

Six physical RAW files support these cases. The retained parent path and full-file SHA are in each case frontmatter. When `dataset_window_*` fields are present, select those inclusive source epochs and verify the original window SHA before calculation. The three superseded smaller RAWs are not registered inputs.

## Evidence boundary

The mixed source modules are present and byte-pinned. HPZR6 references are hash-registered optional external evidence. Pending cases cannot be promoted from historical notes or current computed output alone. Exact source authority, settings, both directional results, and approved expected values are required for a new regression baseline. A future fixture that depends on current Order_B/C must carry `valid_for_regression_baseline: false` and stay non-canonical.
