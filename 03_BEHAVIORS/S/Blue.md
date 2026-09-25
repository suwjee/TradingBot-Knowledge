---
id: "behavior.s.blue"
type: "behavior"
status: "canonical"
authority: "normative"
title: "S Blue"
calculated_by: ["algorithm.s"]
implemented_by: ["source.s_zone_detector"]
depends_on: ["behavior.s"]
parent_of: ["behavior.s.blue.type1", "behavior.s.blue.type2", "behavior.s.blue.type3", "behavior.s.blue.type4"]
source_refs: ["engine/bridge/trading_pipeline.py#L1130", "engine/pipeline/lifecycle_engine.py#L331"]
related_entities: ["test.behavior_invariants"]
source_reference: ["engine/bridge/trading_pipeline.py#L1130", "engine/pipeline/lifecycle_engine.py#L331"]
---

# S Blue

S Blue is the candidate-cross family of S. It is lower priority than E Blue, S Red, E Red, and StopAll. Its public formation field maps simple -> Type-1, advanced -> Type-2, type3 -> Type-3, and type4 -> Type-4. All accepted S Blue occurrences count as one exact group for the StopAll Type-3 reversal gate, regardless of formation subtype. The shared source, decision, parent A, stop, and lifecycle rules live in behavior.s.

Type-3 and Type-4 have no new forming Order. Simple/Advanced can be Order-backed. The variant notes state only their distinct semantic role; algorithm.s.typeN owns exact calculation.
