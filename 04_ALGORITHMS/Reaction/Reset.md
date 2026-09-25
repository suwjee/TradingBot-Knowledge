---
id: "algorithm.reset"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Reset"
implemented_by: ["source.reaction_engine"]
depends_on: ["algorithm.reaction", "market.exact_chronology"]
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L247", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L267", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1070"]
related_entities: ["test.source_validation", "test.chronology_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L247", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L267", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1070"]
---

# Reset

## Calculation logic

A confirmed Reaction's opposite boundary is strictly broken by Bullish Low < BoxBottom or Bearish High > BoxTop. Before a waiting candidate confirms, compare first exact Reset and confirmation lower events in the same main candle; Reset wins when earlier or tied under the detector's Reset-first order.

After confirmation, inspect only the remainder of that same Break main candle, strictly after the confirmation event. Freeze the confirmation-side opposite edge (analysis.extreme in both current directions). A later strict crossing creates Reset with index=Break, secondTime=exact lower event, brokenLevel=frozen edge, fromFirstIndex=confirmed First. That Break cannot also seed the next Mode-B First. If secondTime is absent, main display time supplies Reset chronology. Reset reopens Mode A in the same requested direction.

## Contract interface

- **Purpose:** Find exact strict Reset events within Reaction ownership.
- **Inputs:** Confirmed Reaction boundary, waiting candidate and ordered lower events.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Reset event with owner, source and exact time.
- **Source ownership:** source.reaction_engine.
- **Validation relationship:** test.chronology_invariants; test.source_validation checks the line anchors and owner.
