---
id: "test.fixture_registry"
type: "test"
status: "canonical"
authority: "normative"
title: "Fixture registry"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.fixture_model","test.validation_contract","test.regression_policy","test.source_validation","test.mirror_validation"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L78","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L78","engine/bridge/trading_pipeline.py#L2776"]
---

# Fixture registry

The supplied fixture document is `C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md`, SHA-256 `f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2`. This registry inventories its unique scenarios; each case note preserves its source section and line, exact RAW identity, accepted or pending assertion, validation target, and evidence boundary. The fixture document's final status paragraph names HPZR5, while the required current synchronized references are V5.4.11 HPZR6. That version mismatch is treated as provenance; current assertions were checked against HPZR6/source before being marked Active.

## Unique scenarios

| Source section | Case note | Kind | Status | Direction | Primary timestamp |
| --- | --- | --- | --- | --- | --- |
| 1.1 | [1.1 2026-08-25 — Order_A ownership / immutable first Order](Confirmed/Fixture-1-1.md) | Confirmed | Active | Bearish | 2026-08-25 09:32:30 |
| 1.2 | [1.2 2026-08-25 — Order_C / Mode-B Reset owner](Confirmed/Fixture-1-2.md) | Confirmed | Active | Bearish | 2026-08-25 14:58:30 |
| 1.3 | [1.3 2026-08-26 — native Mode-A Order_C owner](Confirmed/Fixture-1-3.md) | Confirmed | Active | Bearish | 2026-08-26 10:08:00 |
| 1.4 | [1.4 2026-08-26 — A→S / native Mode-B eligibility anchor #1](Regression/Fixture-1-4.md) | Regression | Active | Bearish | 2026-08-26 11:04:00 |
| 1.5 | [1.5 2026-08-26 — A→S / native Mode-B eligibility anchor #2](Regression/Fixture-1-5.md) | Regression | Active | Bearish | 2026-08-26 23:00:00 |
| 1.6 | [1.6 2026-08-28 — A→S / native Mode-B eligibility anchor #3](Regression/Fixture-1-6.md) | Regression | Active | Bearish | 2026-08-28 08:56:30 |
| 1.7 | [1.7 V5.4.2 lifecycle chain — Bearish](Regression/Fixture-1-7.md) | Regression | Pending | Bearish | unknown |
| 1.8 | [1.8 V5.4.3 dominant Red E / cycle ownership](Regression/Fixture-1-8.md) | Regression | Active | Bearish | 2026-08-27 03:55:00 |
| 1.9 | [1.9 Canonical Bullish Order geometry inside Bearish regression](Confirmed/Fixture-1-9.md) | Confirmed | Active | Bearish | 2026-08-27 08:37:10 |
| 1.10 | [1.10 2026-08-28 — exact-key StopAll](Regression/Fixture-1-10.md) | Regression | Active | Bearish | 2026-08-28 03:41:00 |
| 1.11 | [1.11 2026-08-28 — S Blue Type-4](EdgeCases/Fixture-1-11.md) | EdgeCase | Active | Bearish | 2026-08-28 06:34:15 |
| 1.12 | [1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll](Regression/Fixture-1-12.md) | Regression | Active | Bearish | 2026-09-04 02:36:00 |
| 1.13 | [1.13 2026-09-09 — historical Mode-B refresh chain](Bugs/Fixture-1-13.md) | Bug | Historical | Bearish | 2026-09-09 04:29:30 |
| 2.1 | [2.1 2026-09-04 — canonical Order_B](Confirmed/Fixture-2-1.md) | Confirmed | Active | Bearish | 2026-09-04 09:45:55 |
| 2.2 | [2.2 2026-09-04 — shared accepted-Order / parent-neutral use](Confirmed/Fixture-2-2.md) | Confirmed | Active | Bearish | 2026-09-04 17:55:45 |
| 2.3 | [2.3 2026-09-17 — Exact-source E continuation](Regression/Fixture-2-3.md) | Regression | Active | Bullish | 2026-09-17 08:54:00 |
| 2.4 | [2.4 2026-09-17 — downstream StopAll consequence](Regression/Fixture-2-4.md) | Regression | Active | Bullish | 2026-09-17 18:30:30 |
| 2.5 | [2.5 2026-09-17 — S reversal historical example](Bugs/Fixture-2-5.md) | Bug | Historical | Bullish | 2026-09-17 16:15:00 |
| 3.1 | [3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership](Confirmed/Fixture-3-1.md) | Confirmed | Active | Bearish | 2026-09-04 16:58:38 |
| 3.2 | [3.2 2026-09-07 — bounded Mode-A anchor](EdgeCases/Fixture-3-2.md) | EdgeCase | Active | Bearish | 2026-09-07 10:14:00 |
| 4.1 | [4.1 2026-09-09 — same-Break Bullish confirmation/reset](Confirmed/Fixture-4-1.md) | Confirmed | Active | Bullish | 2026-09-09 19:09:45 |
| 4.2 | [4.2 2026-09-09 — Bullish Blue→A→S→Order chain](Regression/Fixture-4-2.md) | Regression | Active | Bullish | 2026-09-09 19:17:00 |
| 4.3 | [4.3 2026-09-10 — stage ownership / invalid fallback](Regression/Fixture-4-3.md) | Regression | Active | Bullish | 2026-09-10 13:56:00 |
| 5.1 | [5.1 2026-09-11 — Bearish chained Blue carried-stop](EdgeCases/Fixture-5-1.md) | EdgeCase | Pending | Bearish | 2026-09-11 09:23:00 |
| 5.2 | [5.2 2026-09-11 — stage ownership](Regression/Fixture-5-2.md) | Regression | Active | Bearish | 2026-09-11 18:01:30 |
| 5.3 | [5.3 USOIL Bearish Order_A / Order_C chain remembered from prior chat](EdgeCases/Fixture-5-3.md) | EdgeCase | Pending | Bearish | unknown |
| 6.1 | [6.1 2026-09-22 — stopped dominant E must advance +1](Regression/Fixture-6-1.md) | Regression | Pending | Bearish | 2026-09-22 21:46:00 |
| 8.1 | [8.1 `2026-09-04 02:36:00` Bullish StopAll](Bugs/Fixture-8-1.md) | Bug | Historical | Bullish | 2026-09-04 02:36:00 |

**Total:** 28 unique case notes: 8 Confirmed, 13 Regression, 4 EdgeCase and 3 Bug; 21 Active, 4 Pending and 3 Historical. `Active` means the selected assertion is grounded by current reference/source inspection; it does not mean a fresh full-output regression run or payload hash was produced.

## Dataset pins

| Dataset path | SHA-256 |
| --- | --- |
| `D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json` | `062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6` |
| `D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/USOIL/RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json` | `9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c` |
| `D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 1S FROM 2026-09-03 19-05-40 TO 2026-09-08 03-18-28.json` | `0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776` |
| `D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json` | `f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974` |
| `D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json` | `18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0` |
| `D:/My-Projects/TradingBot/data/raw/FOREXCOM/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-22 11-00-00 TO 2026-09-24 00-05-40.json` | `b47246b45bb66db9ddfb75b6a431e5b6a7fced5fd521e358e5d5c438f91641dc` |

The sixth dataset (2026-09-22 XAUUSD) is pinned from the production RAW directory; it was not copied into the Vault. The 1-second XAUUSD dataset is lower-timeframe input; the related examples use 30-second main candles.

## Deduplication and historical mapping

- Supplied section 7 repeats the three 2026-08-26/28 S Red cases in 1.4, 1.5 and 1.6. Its three headings map to those three case notes.
- Supplied section 8.2 repeats the historical chain in 1.13; 8.3 repeats 2.5. Section 8.4 is the old output excluded by active negative case 2.4. Sections 8.5–8.7 are three facets of active case 1.2.
- Section 8.1 is distinct: the superseded **Bullish** StopAll at 2026-09-04 02:36:00 has its own Bug case; active 1.12 is the **Bearish** StopAll1 at the same time.
- Historical Bug notes keep the old claim as provenance and explicitly identify the current replacement. They are excluded from active expected-output baselines.

## Open evidence and readiness

- 1.7 lacks a complete calendar date for its lifecycle chain; 5.3 lacks the calendar date for the remembered USOIL Order_A/Order_C chain. Those rows cannot be exact replay cases yet.
- 5.1 gives a geometry method but no complete numeric expected output; 6.1 gives a conversation-derived E5/E6 expectation without an independently verified current output. Both remain Pending.
- Full serialized output baselines, settings, engine source fingerprint for a specific run, and approved payload hashes are not supplied. The Active cases support targeted assertion design, while complete zero-difference regression is not ready.
- Reference §14 versus current lifecycle final filter disagree about a mixed-cause internal Mode-B E/StopAll visibility gate. That unresolved conflict remains excluded from accepted assertions; see `05_MIRROR/Mirror-Exceptions.md` and `Mirror-Validation.md`.
- Current `s_zone_detector.py` retains the first stopped-A Order_A owner. The historical V5.4.5 Mode-B refresh in 1.13 does not establish a current pre-decision refresh rule.

Use `Fixture-Model.md`, `Test-Policy.md`, `Regression-Policy.md`, and `Baseline-Policy.md` to promote a Pending case or attach a run baseline. No case note authorizes production code to branch on its symbol, date, price, RAW filename or expected output.

## Supplemental legacy memory review

The later supplied `memory.txt` contains older fixture leads, duplicate cases and superseded assertions. [Legacy-Memory-Review.md](Legacy-Memory-Review.md) maps them to this registry and records the additional candidates that lack current HPZR6 output evidence. Its instructions and historical release claims are not part of this Phase 5 request. The registered corpus remains 28 unique cases until individual leads pass the fixture promotion path.
