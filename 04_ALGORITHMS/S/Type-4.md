---
id: "algorithm.s.type4"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "S Type-4 Blue-qualified aligned Reaction"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s.blue.type4"]
depends_on: ["algorithm.s", "algorithm.blue", "algorithm.reaction"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L543", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L613"]
related_entities: ["test.source_validation", "test.behavior_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L543", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L613"]
---

# S Type-4 Blue-qualified aligned Reaction

## Calculation logic

From exact A stop until first eligible opposite Order confirmation, each later same-direction Reaction confirmation rebuilds the candidate from the closed A-stop main candle through latest Reaction Break main candle. Bullish selects minimum Low, Bearish maximum High; candidate helper gives last-candle equal-extreme ownership. After that confirmation, first strict candidate crossing must precede next aligned confirmation and Order deadline.

At least one calculation-valid, non-Internal trend Blue must exist from candidate-source main candle through crossing, formed no later than the crossing exact event. A Blue on crossing main candle qualifies only if its formation event is <= crossing. An unqualified cross emits no S; another aligned Reaction can rebuild. Successful route is Blue/public Type-4, with no new Order.

## Contract interface

- **Purpose:** Evaluate the later same-direction Reaction S candidate route.
- **Inputs:** Exact A stop, later Reaction confirmations, closed range extrema and Order deadline.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Type-4 Blue S or competing Red S decision evidence.
- **Source ownership:** source.s_zone_detector.
- **Validation relationship:** test.behavior_invariants; test.source_validation checks the line anchors and owner.
