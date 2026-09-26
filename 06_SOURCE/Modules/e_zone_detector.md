---
id: "source.e_zone_detector"
type: "source"
status: "active"
authority: "executable"
title: "E zone detector: mixed source evidence"
source_path: "06_SOURCE/Code/engine/pipeline/e_zone_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/e_zone_detector.py"
sha256: "6becc792a17e40f572673bf65bc9818c9a957244de811be2823402d41c36e628"
implementation_validity: "mixed"
affected_by_known_invalid_order_route: true
implements: ["algorithm.e", "algorithm.reconciliation", "algorithm.order.a", "algorithm.order.b", "algorithm.order.c"]
source_refs: ["06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L118", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L499", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L727", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L2040"]
related_entities: ["test.source_validation"]
source_reference: ["06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L118"]
---

# E zone detector

This byte-exact source snapshot is executable evidence, not proof that every route is correct. `EZoneDetector` starts at line 118. The current independent Order_B construction is in `_build_order_b_formations` (line 499); Order_C is in `_build_order_c_formations` (line 727). Both routes are known invalid by project decision and require a rewrite. Their current geometry and downstream choices may be inspected only as defective implementation evidence.

Order_A evidence occurs in `_trend_leg_direct_order` (line 1009) and `_direct_parent_stop_order` (line 1058). The broader E assembly, strict stops, candidate reconciliation and recursive continuation occur in `_zone` (line 2040), `continuation_chain_from_s` (line 2185), `_reconcile_candidate_chains` (line 2463), and `detect` (line 3118). These mixed paths must be assessed per route; an E result that uses a B/C cause is not an approved regression baseline. The audit functions in this exact source are not an active Vault knowledge concept.
