---
id: "algorithm.s.type3"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "S Type-3 Reset-leg"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s.blue.type3"]
depends_on: ["algorithm.s", "algorithm.reset"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L457", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L482", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1090", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1355"]
related_entities: ["test.source_validation", "test.behavior_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L457", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L482", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1090", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1355"]
---

# S Type-3 Reset-leg

## Calculation logic

For one stopped A, set the no-Order deadline to the first newly eligible opposite Order confirmation, or to the received-range end when there is no such Order. Consider an opposite Reset whose exact event is strictly after the A-stop event and strictly before that deadline. Its owner must have confirmed no later than the A stop and must not already have reset on or before that stop.

Resolve the owner by the Reset's `from_first_idx`. The candidate leg is the inclusive interval from that owner's Break main index through the main index containing the Reset event. Bullish selects the minimum Low; Bearish selects the maximum High; the shared candidate helper assigns an equal extreme to the last candle. Starting at the exact Reset event and ending before the deadline, find the first strict lower-timeframe crossing (`Low < boundary` for Bullish, `High > boundary` for Bearish).

Require a same-direction trend Reaction confirmation strictly after the A-stop event and no later than that crossing. Among eligible Reset legs, the detector retains the earliest crossing event. The resulting zone is Blue/public Type-3, records the Reset reaction number/time and source/decision provenance, and sets every forming-Order field to `None`.

Type-3 and Type-4 are independent order-free routes evaluated to the same deadline. Earlier exact decision chronology wins; a true equal decision event keeps established Type-3 precedence. Bullish HPZR6 §9.2 and Bearish HPZR6 §9.2 state the same route with the corresponding Low/High directional source; neither supplies an additional Order rule.

## Contract interface

- **Purpose:** Evaluate the pre-Order Reset-led S candidate route.
- **Inputs:** Stopped A, pre-existing opposite Reaction Reset, interval extreme and Order deadline.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Type-3 Blue S or competing Red S decision evidence.
- **Source ownership:** source.s_zone_detector.
- **Validation relationship:** test.behavior_invariants; test.source_validation checks the line anchors and owner.
