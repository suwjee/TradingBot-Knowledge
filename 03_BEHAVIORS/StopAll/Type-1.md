---
id: "behavior.stopall.type1"
type: "behavior"
status: "pending"
authority: "non-canonical"
title: "StopAll Type-1"
calculated_by: ["algorithm.stopall"]
implemented_by: ["source.lifecycle_engine"]
depends_on: ["behavior.stopall"]
source_gate_type: "sequence-group-stop"
source_refs: []
related_entities: ["test.lifecycle_invariants"]
source_reference: []
---

# StopAll Type-1

Public Type-1 maps exactly to gate_type=sequence-group-stop. An E arrives after a dominant same-key E group has at least two occurrences, or, with no E key, a same-color S group has at least two. The latest matching prior group owner must strictly stop by the arriving E's decision. The arriving E donates the new StopAll1; stopped-group metadata records the gate owner. This is distinct from the cycle-wide Blue repetition used by Type-3.
