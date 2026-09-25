---
id: "algorithm.s.type1"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "S Type-1 Simple"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s.blue.type1", "behavior.s.red"]
depends_on: ["algorithm.s", "algorithm.order.a"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L820", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1148"]
related_entities: ["test.source_validation", "test.behavior_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L820", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1148"]
---

# S Type-1 Simple

## Calculation logic

Simple is an order-backed S candidate route. A pre-Order source uses the directional extreme from exact A-stop remainder through Order First inclusive. Post-Order Simple uses Order Break through first subsequent aligned Reaction Break inclusive, with last candle owning equal extrema. An exact candidate formation earlier than Order First main timestamp can reclassify a provisional after route to before; equality stays after. Source helper tie policies must be preserved by branch. A qualified strict candidate crossing before Order stop produces Blue/public Type-1; an Order stop first produces Red with no public numbered formation. Simultaneous strict crossings invalidate the candidate.

## Contract interface

- **Purpose:** Evaluate the Simple order-backed S candidate route.
- **Inputs:** A stop, Order First/Break, aligned Reaction range and exact candidate crossing.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Type-1 Blue S or competing Red S decision evidence.
- **Source ownership:** source.s_zone_detector.
- **Validation relationship:** test.behavior_invariants; test.source_validation checks the line anchors and owner.
