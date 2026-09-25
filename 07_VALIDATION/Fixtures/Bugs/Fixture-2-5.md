---
id: "case.fixture_2_5"
type: "case"
status: "archived"
authority: "historical"
title: "2.5 2026-09-17 — S reversal historical example"
created: "2026-09-25"
updated: "2026-09-25"
fixture_kind: "Bug"
fixture_status: "Historical"
fixture_authority: "Historical"
direction: "Bullish"
timeframe: "30s"
dataset: "D:/My-Projects/TradingBot-Knowledge/08_DATA/Raw/XAUUSD/RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json"
dataset_sha256: "18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0"
timestamp: "2026-09-17 16:15:00"
behavior: "S"
behavior_detail: "historical S Red→StopAll reversal claim"
algorithm: "algorithm.stopall"
source_module: "engine/pipeline/lifecycle_engine.py"
source_function: "StopAllDetector._opposite_s_stopall_gate"
reaction_identity: "unknown"
order_identity: "unknown"
lifecycle_state: "unknown"
previous_behavior: "unknown"
next_behavior: "unknown"
stopall_boundary: "unknown"
expected_output: "Historical StopAll claim superseded; current output is ordinary S Red with native Mode-A Order."
validation_target: "Prevent superseded StopAll expectation from entering current baseline"
validation_rule: "test.lifecycle_invariants"
related_entities: ["test.fixture_registry", "test.lifecycle_invariants", "algorithm.stopall", "source.lifecycle_engine", "behavior.s"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1793", "engine/pipeline/lifecycle_engine.py#L356"]
source_fixture: "C:/Users/msadr/Desktop/TradingBot_Fixtures_Regression_Anchors.md"
source_fixture_line: 227
source_fixture_sha256: "f0234c1342ce57ccf0abd556860c1f3c4535c0b80e94dadc918f3b9bf86c13f2"
---

# 2.5 2026-09-17 — S reversal historical example

## Validation claim

Historical StopAll claim superseded; current output is ordinary S Red with native Mode-A Order.

**Purpose:** Prevent superseded StopAll expectation from entering current baseline. **Status:** Historical; **authority:** Historical.

## Evidence boundary

The old assertion is superseded. Its current replacement is described above; this historical value must never serve as an active expected output. The fixture source is section 2.5, line 227, in the SHA-256-pinned supplied document. The dataset SHA-256 identifies the exact RAW bytes. `source_reference` pins a synchronized reference passage and an implementation location; `source_function: unknown` means a single owning function was not verified. Unknown metadata is deliberately not inferred.

## Supplied scenario

### 2.5 2026-09-17 — S reversal historical example
- S Red: `16:15:00`
- Previously described as StopAll
- Current expected: ordinary `S Red` with native Mode-A Order
- Status: **Historical / Superseded StopAll expectation**

---
