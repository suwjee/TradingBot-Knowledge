---
id: "behavior.e.red"
type: "behavior"
status: "pending"
authority: "non-canonical"
title: "E Red"
calculated_by: ["algorithm.e", "algorithm.reconciliation"]
implemented_by: ["source.e_zone_detector", "source.lifecycle_engine"]
depends_on: ["behavior.e", "core.e_numbering"]
source_refs: []
related_entities: ["test.behavior_invariants"]
source_reference: []
---

# E Red

E Red is a reconciled Red-family E, with family inherited from an active accepted parent or won through Red-priority reconciliation. It outranks S Red, E Blue, S Blue, and A, and remains below StopAll. It can advance recursive numbering after a stopped Red E. An accepted Red E clears pending Blue-repeat reversal evidence, but does not itself reset the independent E-driven StopAll owner counters unless a gate forms.
