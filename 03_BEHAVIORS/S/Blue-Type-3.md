---
id: "behavior.s.blue.type3"
type: "behavior"
status: "canonical"
authority: "normative"
title: "S Blue Type-3"
calculated_by: ["algorithm.s.type3"]
implemented_by: ["source.s_zone_detector"]
depends_on: ["behavior.s.blue", "algorithm.reset"]
source_refs: ["engine/pipeline/s_zone_detector.py#L457", "engine/pipeline/s_zone_detector.py#L1090"]
---

# S Blue Type-3

Public formation Type-3 is the order-free Reset-leg S Blue route. It may decide after A stops and before any newly eligible opposite Order confirms. It carries opposite Reset provenance and requires a same-direction Reaction confirmation; it does not carry new Order geometry. It is still subordinate to the global S/E/StopAll lifecycle hierarchy. Exact closed Break-to-Reset source ownership belongs to algorithm.s.type3.
