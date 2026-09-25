---
id: "algorithm.order.a"
type: "algorithm"
status: "active"
authority: "empirical"
title: "Order_A parent-stop cause"
implemented_by: ["source.s_zone_detector"]
depends_on: ["algorithm.order", "algorithm.a"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L274"]
related_entities: ["test.source_validation", "test.identity_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L274"]
---

# Order_A parent-stop cause

The retained S-stage source selects the first canonical opposite Reaction after an eligible A strict stop, ordered by exact confirmation and physical indexes. This first physical Order_A owner remains fixed while S is undecided. Other routes await a new source-grounded review.
