---
id: "test.behavior_invariants"
type: "test"
status: "canonical"
authority: "normative"
title: "Behavior invariant checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.invariant_validation","core.behavior_model","behavior.a","behavior.s","behavior.e","behavior.stopall","core.e_numbering","source.e_zone_detector"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L78","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L78","engine/pipeline/e_zone_detector.py#L2267","engine/bridge/trading_pipeline.py#L1040"]
---

# Behavior invariant checks

Only A, S, E and StopAll are Behaviors. Reaction, Reset, Blue and Order are calculation/evidence objects. S has Red and Blue families; Blue Type-1..4 are canonical formation identities shared across directions. E1/E2/E3 are numbered accepted instances of E, not separate algorithms or behavior kinds. Both references §§0.1, 10.7, 22; e_zone_detector.py lines 2267–2463; trading_pipeline.py lines 1040–1307.

Assert one source/parent identity per accepted behavior occurrence, preserved family labels, E number progression from stopped eligible owners, and StopAll gate type/number. A negative fixture asserting that an object is absent must check its absence from the correct final collection and not merely from a chart label. Source fixtures 1.10, 1.11, 2.3 and 6.1 target these boundaries; 6.1 remains Pending until its output is independently verified.

No direction-specific A/S/E/StopAll entity may be introduced; Mirror applies to price geometry, not taxonomy.

