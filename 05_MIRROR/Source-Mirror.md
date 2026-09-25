---
id: "mirror.source_map"
type: "mirror"
status: "active"
authority: "canonical"
title: "Mirror source ownership"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["source.direction_policy", "source.reaction_engine", "source.blue_line_detector", "source.a_zone_detector", "source.s_zone_detector", "source.e_zone_detector", "source.lifecycle_engine", "source.core_utils", "source.trading_pipeline", "algorithm.reaction", "algorithm.blue", "algorithm.a", "algorithm.s", "algorithm.e", "algorithm.lifecycle", "algorithm.serialization"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L95", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L95", "engine/pipeline/direction_policy.py#L1", "engine/pipeline/reaction_engine.py#L560", "engine/pipeline/blue_line_detector.py#L75", "engine/pipeline/a_zone_detector.py#L70", "engine/pipeline/s_zone_detector.py#L223", "engine/pipeline/e_zone_detector.py#L141", "engine/pipeline/lifecycle_engine.py#L25", "engine/pipeline/core_utils.py#L11", "engine/bridge/trading_pipeline.py#L2300"]
---

# Mirror source ownership

`direction_policy.py` owns the *shared price-direction primitives*: trend/opposite extreme, first/context tags, strict/better-extreme/confirmation predicates, and opposite direction. It explicitly excludes chronology, lifecycle, numbering, visibility and trading state. Detectors consume its policy where shown below, while also implementing their own direction-aware formulas and control branches. A rule's actual owner is the module/function containing that rule. `direction_policy.py#L1-L10`, `#L21-L70`.

| Mirror rule → source file → function/component | Ownership boundary |
|---|---|
| Extreme, strict crossing, confirmation and First/context tags → `pipeline/direction_policy.py` → `DirectionPolicy`, `policy_for` | Shared primitive mapping; no detector state. `#L21-L70` |
| Bearish Reaction coordinate reflection and candidate/Reset conversion → `pipeline/reaction_engine.py` → `mirror_candle`, `mirror_candidate`, `mirror_analysis`, `BearishDetector` | Runs the Bullish state machine in reflected coordinates; preserves physical indexes/times. `#L560-L703` |
| Unified Reaction direct/Normal search and same-Break Reset → `pipeline/reaction_engine.py` → `UnifiedReactionDetector` | Directional branches and exact-event ownership belong here, including `analysis.extreme` for both directions. `#L1376-L1581` |
| Blue Fibonacci, strikes, scale/reset line and stop → `pipeline/blue_line_detector.py` → `fibonacci_level`, `count_scale_strikes`, Blue builders | Uses `policy_for` but owns explicit directional formulas and price roles. `#L75-L81`, `#L139-L299` |
| A candidate extreme and strict trigger → `pipeline/a_zone_detector.py` → `AZoneDetector` | Uses policy extreme/cross; owns Blue pairing, triggers and A source. `#L70-L166`, `#L219-L311` |
| S trend extreme, Type-3/4 and Order/candidate race → `pipeline/s_zone_detector.py` → `SZoneDetector` | Uses policy primitives; owns S-specific branch geometry and A/Order handoff. `#L223-L270`, `#L315-L331`, `#L482-L638` |
| E/Order_B/C directional range and E formation → `pipeline/e_zone_detector.py` → `EZoneDetector` | Uses policy and explicit direction branches; owns cause formation, source/decision and number reconciliation. `#L141-L151`, `#L329-L550`, `#L727-L830`, `#L2267-L2463` |
| StopAll strict stop versus invariant gates/priority/visibility → `pipeline/lifecycle_engine.py` → `StopAllDetector`, `sequence_priority`, visibility functions | Owns one priority table and cycle state; strict price lookup branches by direction. `#L25-L35`, `#L115-L127`, `#L331-L609`, `#L1708` |
| Decimal and physical Order identity → `pipeline/core_utils.py` → `as_decimal`, `order_identity` | Shared invariant primitive, not directional policy. `#L11-L29` |
| Both-direction orchestration and common output schema → `bridge/trading_pipeline.py` → `prepare_market_context`, `prepare_pipeline_state`, `calculate_full_direction_state`, `finalize_direction_visibility`, serializers | Runs source-owned detectors and emits common keys; does not create a second browser-side mirror authority. `#L1732`, `#L1903`, `#L2300`, `#L2549`, `#L2776` |

The architectural requirement to avoid **independently drifting** Bullish/Bearish rule sets is supported by both references §15 and the reflected Reaction implementation. It is not a claim that every detector delegates every price comparison to `DirectionPolicy`: current Blue, S, E and StopAll code contains explicit directional branches. Any refactor must preserve their exact rules and evidence before centralizing them.
