---
id: "algorithm.reset"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Reset"
implemented_by: ["source.reaction_engine"]
depends_on: ["algorithm.reaction", "market.exact_chronology"]
source_refs: ["engine/pipeline/reaction_engine.py#L247", "engine/pipeline/reaction_engine.py#L267", "engine/pipeline/reaction_engine.py#L1070"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/reaction_engine.py#L247", "engine/pipeline/reaction_engine.py#L267", "engine/pipeline/reaction_engine.py#L1070"]
---

# Reset

A confirmed Reaction's opposite boundary is strictly broken by Bullish Low < BoxBottom or Bearish High > BoxTop. Before a waiting candidate confirms, compare first exact Reset and confirmation lower events in the same main candle; Reset wins when earlier or tied under the detector's Reset-first order.

After confirmation, inspect only the remainder of that same Break main candle, strictly after the confirmation event. Freeze the confirmation-side opposite edge (analysis.extreme in both current directions). A later strict crossing creates Reset with index=Break, secondTime=exact lower event, brokenLevel=frozen edge, fromFirstIndex=confirmed First. That Break cannot also seed the next Mode-B First. If secondTime is absent, main display time supplies Reset chronology. Reset reopens Mode A in the same requested direction.
