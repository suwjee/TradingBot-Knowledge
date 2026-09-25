---
id: "behavior.e.blue"
type: "behavior"
status: "canonical"
authority: "normative"
title: "E Blue"
calculated_by: ["algorithm.e", "algorithm.reconciliation"]
implemented_by: ["source.e_zone_detector", "source.lifecycle_engine"]
depends_on: ["behavior.e", "core.e_numbering"]
source_refs: ["engine/pipeline/e_zone_detector.py#L2463", "engine/pipeline/lifecycle_engine.py#L331"]
related_entities: ["test.behavior_invariants"]
source_reference: ["engine/pipeline/e_zone_detector.py#L2463", "engine/pipeline/lifecycle_engine.py#L331"]
---

# E Blue

E Blue is a reconciled Blue-family E. It outranks S Blue and A, while Red S/E and StopAll outrank it. Each numbered E Blue group is distinct for pending StopAll Type-3 repetition: two accepted E1 Blue count together, but E1 Blue plus E2 Blue do not. Blue family may be inherited from a stopped accepted Blue parent; reconciliation can replace a later descendant branch with an earlier valid continuation without deleting unrelated E lineages.
