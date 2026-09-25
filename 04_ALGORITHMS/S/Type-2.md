---
id: "algorithm.s.type2"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "S Type-2 Advanced"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s.blue.type2", "behavior.s.red"]
depends_on: ["algorithm.s", "algorithm.reaction"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L418", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1148"]
related_entities: ["test.source_validation", "test.behavior_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L418", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1148"]
---

# S Type-2 Advanced

## Calculation logic

Advanced is selected when a complete nested same-direction Reaction is wholly inside the opposite Order before that Order confirms. The nested Reaction must already be valid when ownership is classified as after. Candidate source is the Order's opposite semantic box edge: Bullish BoxBottom source, Bearish BoxTop source. It cannot decide before nested trend confirmation. The shared exact S decision race applies; qualified candidate cross gives Blue/public Type-2, Order stop first gives Red, same-event dual crossing invalidates.

## Contract interface

- **Purpose:** Evaluate the Advanced nested-Reaction S candidate route.
- **Inputs:** Eligible opposite Order, complete nested Reaction and box-edge source.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Type-2 Blue S or competing Red S decision evidence.
- **Source ownership:** source.s_zone_detector.
- **Validation relationship:** test.behavior_invariants; test.source_validation checks the line anchors and owner.
