---
id: "test.source_validation"
type: "test"
status: "canonical"
authority: "normative"
title: "Fixture to source validation"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.fixture_model","test.fixture_registry","mirror.source_map","algorithm.reaction","algorithm.order","source.reaction_engine","source.s_zone_detector","source.e_zone_detector","source.lifecycle_engine","source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L95","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L95","engine/bridge/trading_pipeline.py#L1903","engine/pipeline/s_zone_detector.py#L277"]
---

# Fixture to source validation

For each case, trace Fixture → public Behavior when one exists → Algorithm → physical Source module → real function. Reaction, Reset, Blue and Order cases may have behavior=unknown because they are not Behaviors. Keep the algorithm/source edge even then. The Vault builder checks case relation targets, source module existence and named top-level/class method symbols. Both references §§0.1, 20; trading_pipeline.py lines 1903–2300.

Owner map: Reaction/Reset and physical Reaction geometry → reaction_engine.py; Blue → blue_line_detector.py; A → a_zone_detector.py; S and immutable first Order_A → s_zone_detector.py; E, Order_B/C and number reconciliation → e_zone_detector.py; StopAll, priority, final visibility and physical Order audit preparation → lifecycle_engine.py; Decimal/identity → core_utils.py; pipeline scope and public serialization → bridge/trading_pipeline.py. direction_policy.py owns shared directional primitives. See `05_MIRROR/Source-Mirror.md` and the individual `06_SOURCE/Modules/` notes.

An optional source_function must be a function or Class.method present in the cited module. Use unknown rather than a guessed symbol. The supplied prompt's conditional Mode-B refresh is **not** an active rule: current s_zone_detector.py lines 277–321 and both references V5.4.8+ retain the first stopped-A Order_A even before S decision. Preserve older refresh results only as Historical fixtures.
