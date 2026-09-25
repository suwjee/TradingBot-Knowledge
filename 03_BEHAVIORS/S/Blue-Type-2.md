---
id: "behavior.s.blue.type2"
type: "behavior"
status: "canonical"
authority: "normative"
title: "S Blue Type-2"
calculated_by: ["algorithm.s.type2"]
implemented_by: ["source.s_zone_detector"]
depends_on: ["behavior.s.blue"]
source_refs: ["engine/pipeline/s_zone_detector.py#L418", "engine/bridge/trading_pipeline.py#L1145"]
related_entities: ["test.behavior_invariants"]
source_reference: ["engine/pipeline/s_zone_detector.py#L418", "engine/bridge/trading_pipeline.py#L1145"]
---

# S Blue Type-2

Public formation Type-2 is the advanced S Blue route (formation_type=advanced). Its candidate is tied to a completed nested same-direction Reaction inside the opposite Order before that Order confirms. The nested confirmation owns the earliest eligible decision start. It remains one S behavior and shares S's parent, stop, and lifecycle contract. Exact nested geometry belongs to algorithm.s.type2.
