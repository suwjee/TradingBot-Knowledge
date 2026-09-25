---
id: "behavior.e"
type: "behavior"
status: "pending"
authority: "non-canonical"
title: "E"
calculated_by: ["algorithm.e", "algorithm.reconciliation"]
implemented_by: ["source.e_zone_detector", "source.lifecycle_engine"]
depends_on: ["behavior.s", "algorithm.order"]
parent_of: ["behavior.e.red", "behavior.e.blue"]
source_refs: []
related_entities: ["test.behavior_invariants"]
source_reference: []
---

# E

E is the larger behavior built recursively from stopped accepted S or E. Each E has family Red/Blue, number, parent identity, source, decision, price, and accepted physical Order provenance. An E child may continue a stopped parent, while lifecycle reconciliation can preserve independent S-owned E1 roots. A consumed non-public S may supply continuation evidence for a stopped larger E without becoming public S.

Family and number are reconciled from active accepted ownership, not inferred solely from discovery order. One physical source (sourceIndex,sourceTime) has at most one accepted E: Red outranks Blue, then higher number within family, with first accepted provenance retained on exact ties. StopAll and final visibility can suppress E at a common source.
