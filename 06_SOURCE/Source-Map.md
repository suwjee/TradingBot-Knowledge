---
id: "source.map"
type: "source"
status: "active"
authority: "executable"
title: "Source map"
source_refs: ["engine/bridge/trading_pipeline.py#L1698", "engine/bridge/trading_pipeline.py#L1903"]
relates_to: ["core.pipeline"]
---

# Source map

The current bridge dynamically loads engine/pipeline modules; module notes and the byte-exact mirror resolve every source ID. Line anchors below are one-based current production lines. The 2026-09-23 Graphify snapshot is supplemental and predates some current module edits; important edges here were checked against current source.

| Algorithm ID | Module / symbol | State or output | Related behavior |
| --- | --- | --- | --- |
| algorithm.raw | trading_pipeline.build_candle_buckets L120; prepare_market_context L1732 | lower/main candles, MarketContext | all |
| algorithm.reaction | reaction_engine.UnifiedReactionDetector.detect L2104; BullishDetector.detect L282; BearishDetector.detect L695 | Candidate, DetectionResult | all downstream |
| algorithm.reset | reaction_engine.BullishDetector.post_breakout_reset L267; MarketChronology.reset_time L1070 | ResetEvent | downstream A/S/E |
| algorithm.internal_reaction | reaction_engine.build_behavior_reaction_views L1202 | behavior_internal identity | public visibility |
| algorithm.blue | blue_line_detector.detect_blue_lines L299 | BlueLine | A, S Type-4, Order_C |
| algorithm.a | a_zone_detector.AZoneDetector.detect L753 | AZone, BlueState | A |
| algorithm.s | s_zone_detector.SZoneDetector.detect L1319; SZoneDetector._decision L964 | SZone, order_audit | S |
| algorithm.s.type1 / type2 | s_zone_detector.SZoneDetector._build_order_backed_zone L1148 | simple / advanced | S Blue Type-1/2; Red |
| algorithm.s.type3 | s_zone_detector.SZoneDetector._first_type3 L482; SZoneDetector._build_type3_zone L1090 | order-free Reset leg | S Blue Type-3 |
| algorithm.s.type4 | s_zone_detector.SZoneDetector._first_type4 L543; SZoneDetector._build_type4_zone L613 | order-free Blue qualified | S Blue Type-4 |
| algorithm.order | reaction_engine.MarketChronology.canonical_order_stop L1137; core_utils.order_identity L19 | physical (FirstIndex,BreakIndex) | S/E/StopAll |
| algorithm.order.a | s_zone_detector.SZoneDetector._first_order_after L274; e_zone_detector.EZoneDetector._direct_parent_stop_order L1058 | parent-stop creation cause | S/E |
| algorithm.order.b | e_zone_detector.EZoneDetector._build_order_b_formations L499 | reset-leg cause | E |
| algorithm.order.c | e_zone_detector.EZoneDetector._build_order_c_formations L727 | blue-leg cause | E |
| algorithm.e | e_zone_detector.EZoneDetector._zone L2040; EZoneDetector.detect L3118 | EZone, physical Order ledger | E |
| algorithm.reconciliation | e_zone_detector.EZoneDetector._reconcile_candidate_chains L2463; lifecycle_engine.split_a_zones_by_dominant_stops L946 | accepted E and invalid A/S identities | A/S/E |
| algorithm.lifecycle | lifecycle_engine.s_zones_for_module_engines L1314; consumed_s_evidence_after_larger_stop L1172 | calculation-eligible state | A/S/E |
| algorithm.stopall | lifecycle_engine.StopAllDetector.detect L403 | StopAll gate_type | StopAll |
| algorithm.visibility | lifecycle_engine.finalize_behavior_visibility L1708; bridge.finalize_direction_visibility L2549 | public lineage/occupancy | A/S/E/StopAll |
| algorithm.serialization | bridge.serialize_direction_payload L2776; build_bridge_output L1364 | versioned JSON and bridge behavior view | all |
| algorithm.orderaudit | S/E ledgers, lifecycle_engine.prepare_order_audit L621, bridge.serialize_order_audit L1537 | pending-fix executable output | none canonical |

This map documents source ownership; it is not itself an implementation module. The bridge orchestrates Blue -> A -> S -> E and then lifecycle passes within calculate_full_direction_state L1903. prepare_pipeline_state L2300 constructs both Reaction directions for dependent stages. finalize_direction_visibility L2549 detects StopAll and clips only after full calculation. See Dependency-Map and State-Map.

