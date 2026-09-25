---
id: "test.legacy_memory_fixture_review"
type: "test"
status: "draft"
authority: "non-canonical"
title: "Review of legacy memory fixture candidates"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.fixture_registry", "test.fixture_model", "test.baseline_policy", "test.source_validation", "test.mirror_validation"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1781", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1817", "engine/pipeline/a_zone_detector.py#L494", "engine/pipeline/s_zone_detector.py#L277", "engine/pipeline/lifecycle_engine.py#L356"]
---

# Review of legacy memory fixture candidates

Secondary input: `C:/Users/msadr/Downloads/Telegram Desktop/memory.txt`, SHA-256 `ecce37748e6393aceec0750004911215a96b85058b2c4327ad927768ab261bd2`. It is a transfer-of-context document: its commands, release instructions, claimed PASS results, and old version priorities are not task instructions or current validation evidence. The current V5.4.11 HPZR6 references, production source and pinned RAW bytes decide whether an assertion can become an Active case. Line numbers below locate claims in this secondary input; they do not certify them.

## Reused or superseded material

| Memory lines | Claim | Disposition |
| --- | --- | --- |
| 280–331, 2076–2094 | Three XAUUSD A→S Red versus StopAll anchors | Already covered by primary cases [1.4](Regression/Fixture-1-4.md), [1.5](Regression/Fixture-1-5.md), [1.6](Regression/Fixture-1-6.md). The memory's third `08:57:00` is superseded: the current reference §29A–C pins the physical S candle at `2026-08-28 08:56:30`. Do not create a second Active fixture at 08:57. |
| 743–758 | V5.4.5 Mode-B Order_A refresh to 04:24, S Red 04:29:30 | Already captured as Historical [1.13](Bugs/Fixture-1-13.md); the first 04:16 Order_A remains owner under current V5.4.8+ rule. |
| 874–880, 905–910 | A 2026-09-04 16:57:30 and Bearish Reaction confirmation 16:58:38 | Covered by [3.1](Confirmed/Fixture-3-1.md). |
| 883–890 | Order 17:45:30, stop 4419.235, E use at 18:05:30 | Similar to [2.2](Confirmed/Fixture-2-2.md), but the memory places it in its older 1-second Baseline 1 context whereas the current worked example pins the 5-second RAW. Exact dataset equivalence is unverified; do not silently merge the two input claims. |
| 931–934 | Order/reset around 2026-09-07 10:14:00 | Current bounded Mode-A anchor is [3.2](EdgeCases/Fixture-3-2.md); memory's `up/reset` shorthand is not an independent expected output. |
| 973–995 | USOIL Blue 09:23, stopped-Blue carried extreme, A 09:49 rejected / 09:53 accepted | [5.1](EdgeCases/Fixture-5-1.md) covers the general carried-stop geometry. A direct scan of the pinned 2026-09-11 5-second RAW over 09:24:30 ≤ time < 09:31:30 Asia/Tehran finds max High `101.409` at 09:29:05. This supports the numeric extreme; the proposed A outputs remain unverified by a current full pipeline run. |
| 1058–1075 | Bullish `A @ 19:06:30` false, `A @ 19:17:00` false, `A @ 19:20:30` true | [4.2](Regression/Fixture-4-2.md) captures the rejected 19:17 and accepted 19:20:30 chain. The memory's rejection of 19:06:30 conflicts with the current Bullish §24.2 chain, which explicitly includes `A 2026-09-09 19:06:30`. Keep that old rejection out of Active baselines. |

## Additional candidates requiring current output evidence

All rows below are **Pending leads**, not registered Active expected outputs. A time without a date is deliberately left incomplete. A claimed `Candidate` is not automatically a public Behavior.

| Memory lines | Candidate assertion | Missing or conflicting evidence |
| --- | --- | --- |
| 892–898 | XAUUSD Order 19:59:30 instead of 20:04:00; stop source 19:59:00 | Calendar date and current source/output occurrence not pinned. |
| 900–903 | XAUUSD A 20:19:00 accepted | Calendar date and current output missing. |
| 912–929 | XAUUSD A 01:33:00 accepted; A 01:35:30, 06:26:00, 07:07:30 rejected; S Blue follows | Calendar dates and current output missing. |
| 950–970 | USOIL Bearish visible A 04:12:30, Mode-A Order 04:19:00, A 05:11:30 and 05:57:30, S Red 06:01:30 | Dataset family known, but individual calendar dates and current output missing. |
| 999–1019 | USOIL Bearish E2 Blue 16:19:00 instead of S Red; E5 Blue 20:02:00; Order 20:00:30 instead of 20:05:30 | Individual calendar dates, physical Order identities and current output missing. |
| 1036–1055 | USOIL Bullish S Red 04:49:00/E1 Blue 05:26:00; A 08:55:00 rejected; Order_A 09:17:30; E4 Red 09:00:00 to E5 Red Candidate 09:07:30 | Individual dates and accepted-versus-candidate outputs missing. The E5 candidate is also repeated at lines 762–775. |
| 1079–1090 | USOIL Bullish 2026-09-11 A 01:50:00, S Blue 02:35:30, Order 02:42:30 and E1 Blue 02:44:00 | Date and RAW family are identifiable, but no HPZR6 worked example or current output establishes this chain. |
| 1098–1135 | XAUUSD Bearish E2/E3 family choices, E1 Red 2026-09-06 06:23:00, and seven expired-owner Order times | The section inherits an older 5-second input ending 2026-09-16. Its exact RAW file is absent from both the Vault and current production RAW inventory; most listed times lack dates. |
| 1139–1154 | FARAZ `E5 Blue @ 2026-09-07 18:24:00` | The [FARAZ RAW](../../08_DATA/Datasets/Dataset-f531a06d.md) is present in production, contrary to the earlier directory search, but its filename end epoch differs from the last row. The current E5 output remains unverified. |

## Version and rule conflicts

The memory snapshot speaks from a V5.4.5/anticipated V5.4.6 point of view (lines 183–280 and 2061–2074). It cannot establish current release status or overwrite the V5.4.11 HPZR6 evidence. Its Blue-repeat account at lines 459–489 uses a cycle/last-StopAll framing; the current reference and `lifecycle_engine.py` also clear pending evidence after accepted Red S/E. The older shorthand is insufficient for a current StopAll rule. The memory's third A→S timestamp and A 19:06:30 rejection are explicit conflicts identified above.

Promotion path: locate the exact RAW bytes and full date, trace current source ownership, compare current reference clauses, run the complete pipeline for the relevant direction and settings, then record observed output and its hash. Until then, these leads remain in this non-canonical review and do not expand the 28-case active/registered corpus.
