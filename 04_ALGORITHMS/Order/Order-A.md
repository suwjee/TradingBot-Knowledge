---
id: "algorithm.order.a"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Order_A parent-stop cause"
implemented_by: ["source.s_zone_detector", "source.e_zone_detector"]
implementation_validity: "accepted"
valid_for_reasoning: true
valid_for_validation: true
valid_for_regression_baseline: true
relates_to: ["algorithm.order", "algorithm.a"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L274", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L1009", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L1058"]
related_entities: ["test.source_validation", "test.identity_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L274", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L1009"]
---

# Order_A parent-stop cause

## Accepted parent-stop route

After an eligible A strictly stops, the S detector selects the first canonical opposite Reaction confirmed strictly after that exact stop, with First in or after the stop main candle (`SZoneDetector._first_order_after`, lines 274–282 and `_order_matches_after`, lines 285–309). Its physical identity is `(FirstIndex, BreakIndex)`. This first A-owned Order_A is immutable while S is undecided; a later native Mode-B Reaction does not refresh it. Native Reaction Mode B is distinct from the defective independent Order_B creation route. The accepted HPZR6 parent-stop correction is recorded for both directions in `06_SOURCE/Reference-Registry.md`.

## Direct E ownership and validation

The E detector also constructs direct Order_A evidence at `_trend_leg_direct_order` (line 1009) and selects a direct parent-stop Order at `_direct_parent_stop_order` (line 1058). Do not assume every E result is accepted: an E result using the currently defective B/C causes remains quarantined. Validate the Order_A identity, strict stop gate, first confirmation and immutable parent-stop provenance independently in both directions on pinned RAW. No timestamp or fixture-specific production branch is permitted.
