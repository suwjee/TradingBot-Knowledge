---
id: "behavior.stopall.type2"
type: "behavior"
status: "pending"
authority: "non-canonical"
title: "StopAll Type-2"
calculated_by: ["algorithm.stopall"]
implemented_by: ["source.lifecycle_engine"]
depends_on: ["behavior.stopall"]
source_gate_type: "stopall-stop"
source_refs: []
related_entities: ["test.lifecycle_invariants"]
source_reference: []
---

# StopAll Type-2

Public Type-2 maps exactly to gate_type=stopall-stop. Before an E decision, an active StopAll's own strict stop is checked; if its first stop is no later than that decision, the arriving E creates the next StopAll. Its number is one above the highest strictly stopped active StopAll number. Gate metadata names StopAll rather than an S/E repeat group. The new StopAll resets the current owner-cycle counters.
