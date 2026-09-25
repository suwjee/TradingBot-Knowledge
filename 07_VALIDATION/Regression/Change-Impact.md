---
id: "test.change_impact"
type: "test"
status: "canonical"
authority: "normative"
title: "Regression change impact"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.regression_policy","test.regression_model","test.source_validation","core.pipeline","algorithm.reaction","algorithm.blue","algorithm.a","algorithm.s","algorithm.e","algorithm.stopall","algorithm.serialization"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L129","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L129","engine/bridge/trading_pipeline.py#L1903","engine/bridge/trading_pipeline.py#L2549"]
---

# Regression change impact

Trace the changed source rule through the actual pipeline: RAW/Reaction/Reset → Blue → A → S/Order → E → StopAll/lifecycle → visibility → serialization. Shared direction policy, chronology and core identity can affect both directions; a change to an early stage may legitimately alter every downstream collection. Both references §§2, 15A; trading_pipeline.py lines 1903–2300 and 2549–2942.

Before testing, name the owner function, input boundary, current reference clause, directional or invariant category, and expected affected fields. After testing, compare every stage and both directions. For approved changes, separate directly intended differences from causal downstream differences and verify that unrelated stages remain equal. For example, V5.4.11 Order_C changed eligible physical Orders and downstream S/E/StopAll while Reaction/Reset/Blue/A remained stable; both references §29H and e_zone_detector.py lines 674–830.

A historical fixture is evidence of a past change, not permission to restore it. A Bug result does not become a new rule without current reference/source agreement. Record source-reference conflicts as unresolved and keep them out of acceptance gates.

