---
id: "mirror.invariants"
type: "mirror"
status: "active"
authority: "canonical"
title: "Mirror invariants"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["core.behavior_model", "core.priority", "core.lifecycle", "core.chronology", "core.precision", "core.e_numbering", "algorithm.order", "algorithm.serialization", "source.core_utils", "source.lifecycle_engine", "source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L581", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L581", "engine/pipeline/lifecycle_engine.py#L25", "engine/pipeline/core_utils.py#L11", "engine/bridge/trading_pipeline.py#L239"]
---

# Mirror invariants

These atomic rules do not change when direction changes. The surrounding algorithm can still be **Mixed** when its price predicate is directional.

| Invariant | Exact contract | Evidence |
|---|---|---|
| Behavior identity | A, S, E, StopAll are shared behavior identities; `Bullish A`, `Bearish S`, etc. are not new entities. S Red/Blue and Blue Type-1..4 are family/formation identities shared across directions. | Both references §0.1, §23.2; `trading_pipeline.py#L1040-L1307` |
| E numbering | E1/E2/E3 are numbered states/instances of one E algorithm, not separate algorithms. Same-family stopped-owner and reconciliation rules govern the next number. | Both references §10.7; `e_zone_detector.py#L2267-L2463` |
| Priority | `StopAll > E Red > S Red > E Blue > S Blue > A` (`5 > 4 > 3 > 2 > 1 > smallest`). Red/Blue **family labels** never swap with market direction. | Both references §12 and §13; `lifecycle_engine.py#L25-L35` |
| Stage cycle | Accepted stage progression is `A → S → E → StopAll`; after a hard StopAll boundary, a new cycle may begin at A. StopAll clears active owner and pending repeat state. | Both references §12, §13, §15A; `lifecycle_engine.py#L403-L455` |
| Chronology | The exact lower-timeframe event order determines confirmation, breakout, strict stops and A/S/E/StopAll decisions; main-candle OHLC alone cannot reorder those events. Physical source and event indexes/times stay attached to their objects. | Both references §5, §12, §15A; `trading_pipeline.py#L1732-L1903` |
| Precision | Calculation-side prices use `Decimal`; `as_decimal` keeps an existing Decimal or uses `Decimal(str(value))`. No float conversion is permitted as a substitute for calculation comparisons. | Both references §3.2; `core_utils.py#L11-L13`; `trading_pipeline.py#L120-L134` |
| Physical Order identity | `(FirstIndex, BreakIndex)` identifies one physical opposite Reaction/Order; multiple independently proven causes may belong to it. Identity is independent of direction and native Reaction mode. | Both references §6.12, §11; `core_utils.py#L19-L29`; `lifecycle_engine.py#L728-L776` |
| Ownership and provenance | Parent-stop, reset-leg and blue-leg are distinct creation causes; accepted-live/carried-live are use routes. Priority, lineage and cause identity do not change by directional reflection. | Both references §10.2, §11; `lifecycle_engine.py#L728-L800` |
| Serialization structure | The same JSON keys, collection shape, nullable slots and version fields apply in both directions; only direction-dependent **values** change. Decimal prices serialize as strings. This structural rule does not claim that every emitted OrderAudit value is a validated trading rule. | Both references §16; `trading_pipeline.py#L239-L493`, `#L2776-L2950` |
| Doji market color | `open == close` remains GREEN in either market direction; internal reflected tags are an adapter, not a market-color reclassification. | Both references §3.6; `reaction_engine.py#L91-L93`, `#L560-L577` |

StopAll priority outranks the other behaviors, while its *formation* remains Mixed because strict price stops use `Low <` or `High >`. Stage order must be applied before priority resolves eligible ownership; priority alone does not justify skipping A/S/E state transitions. Both references §12; `lifecycle_engine.py#L25-L35`, `#L946-L1177`.
