---
id: "algorithm.order.b"
type: "algorithm"
status: "pending-fix"
authority: "non-canonical"
title: "Order_B current implementation, quarantined"
implementation_validity: "known-invalid"
valid_for_reasoning: false
valid_for_validation: false
valid_for_regression_baseline: false
rewrite_required: true
implemented_by: ["source.e_zone_detector"]
depends_on: ["algorithm.order", "algorithm.reset"]
source_refs: ["06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L390", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L499", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L620"]
related_entities: ["test.source_validation", "source.lifecycle_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L499"]
---

# Order_B

## وضعیت فعلی

Known-invalid by explicit project decision. This note records the current implementation for diagnosis only. It is not the future Order_B specification and cannot authorize trading conclusions or expected regression outputs.

## Current Implementation Evidence

`EZoneDetector._order_b_reset_leg` (line 390), `_order_b_strict_break` (line 418), `_order_b_geometry_evidence` (line 458), `_first_order_b_reaction_after_break` (line 482), and `_build_order_b_formations` (line 499) construct the current Reset-leg route. `_order_b_orders` (line 620) exposes matches. `lifecycle_engine.forbidden_internal_order_b` (line 1658) gates a dependent visibility path. These line anchors describe current code, including its defects; they are not a validated algorithm contract.

## Reference Evidence

The Bullish and Bearish HPZR6 files registered in `06_SOURCE/Reference-Registry.md` describe an Order_B route. Both references are evidence of the current documented implementation. Their B sections are known-invalid for future normative use even when they match source.

## Known Validity State

`pending-fix` / `non-canonical` / `known-invalid`. No implementation patch or corrected replacement rule is approved. A physical Reaction's native Mode B does not itself mean independent Order_B provenance.

## Dependencies

Current source reads Reset-leg geometry, strict price chronology, opposite Reaction and physical Order identity. The accepted future dependency graph must be established by a rewrite; this list is diagnostic.

## Impact Surface

Current E cause selection, lifecycle internal filtering, bridge orchestration, visibility, serialization and related fixtures may depend on this route. Other E and lifecycle paths remain independently reviewable.

## Validation Policy

Use source/ref comparisons only to detect drift and to diagnose the defective path. Exclude B-dependent observed output from approved regression baselines; require a new accepted specification and independent Bullish/Bearish tests before promotion.

## Rewrite Requirements

Define formation geometry, strict temporal gates, parent and physical identity, stop/selection semantics, interaction with Order_A/C, mirror behavior, and lifecycle effects from the revised project decision. Then update source, references, fixtures and this note together.
