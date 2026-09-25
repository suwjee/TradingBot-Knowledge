---
id: "algorithm.order"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Physical Order and provenance"
implemented_by: ["source.reaction_engine", "source.s_zone_detector"]
depends_on: ["algorithm.reaction", "market.exact_chronology"]
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1137", "06_SOURCE/Code/engine/pipeline/core_utils.py#L19"]
related_entities: ["test.source_validation", "test.identity_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1137", "06_SOURCE/Code/engine/pipeline/core_utils.py#L19"]
---

# Physical Order identity

A physical Order is a canonical opposite Reaction with identity `(FirstIndex,BreakIndex)`. The retained Order creation route in this Vault is `Order_A` after an eligible parent stop. Native Reaction modes A and B are separate state-machine labels. Additional creation routes are outside the current Vault authority.
