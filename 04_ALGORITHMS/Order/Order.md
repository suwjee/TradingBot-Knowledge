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

A physical Order is a canonical opposite Reaction with identity `(FirstIndex,BreakIndex)`. The accepted creation route is `Order_A` after an eligible parent stop; direct Order_A evidence is also present in E source. Native Reaction modes A and B are separate state-machine labels. `Order_B` and `Order_C` have diagnostic notes, but both current implementations are known invalid and cannot supply normative reasoning or regression baselines. The physical identity is shared across independently proven causes; current code behavior does not establish the future B/C contract.

| Cause | Current knowledge status | Use |
| --- | --- | --- |
| Order_A | accepted canonical | reasoning and validation of evidenced A-owned routes |
| Order_B | pending-fix, known-invalid | diagnostic source/reference evidence only |
| Order_C | pending-fix, known-invalid | diagnostic source/reference evidence only |
