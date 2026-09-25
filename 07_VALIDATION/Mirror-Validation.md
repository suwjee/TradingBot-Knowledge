---
id: "test.mirror_validation"
type: "test"
status: "canonical"
authority: "normative"
title: "Mirror validation"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["mirror.contract","mirror.direction_mapping","mirror.invariants","mirror.exceptions","test.invariant_validation","source.direction_policy","source.reaction_engine"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L641","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L641","engine/pipeline/direction_policy.py#L21","engine/pipeline/reaction_engine.py#L560"]
---

# Mirror validation

Validate Bullish fixtures and Bearish fixtures independently on identical physical RAW/settings, then check the directional mapping: trend Low/min/< ↔ High/max/>, opposite Reaction confirmation High > BoxTop ↔ Low < BoxBottom, First/context roles, Blue line geometry and Order direction. Equality never crosses. Market Doji remains GREEN. The invariant layer keeps behavior taxonomy, priority, chronology, numbering, physical identity and output schema. Both references §15 and §23; direction_policy.py lines 21–70; reaction_engine.py lines 560–703.

Do not expect naturally observed Bullish and Bearish payloads to be identical. For a constructed reflected-price case, transform OHLC and preserve physical time/index to check the corresponding geometry, then verify lifecycle invariants separately. Full pipeline dependent stages require both Reaction streams. trading_pipeline.py lines 2300–2350.

The existing Mirror-Exceptions.md records one unresolved mixed-cause Internal-Reaction E/StopAll visibility discrepancy: references §14 say reset-leg-only while lifecycle_engine.py lines 1658–1678 filter if any reset-leg cause/time is present. Do not turn either interpretation into a current pass criterion for a mixed-cause case until the conflict is resolved.

