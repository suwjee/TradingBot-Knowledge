---
id: "behavior.s.blue.type1"
type: "behavior"
status: "canonical"
authority: "normative"
title: "S Blue Type-1"
calculated_by: ["algorithm.s.type1"]
implemented_by: ["source.s_zone_detector"]
depends_on: ["behavior.s.blue"]
source_refs: ["engine/pipeline/s_zone_detector.py#L1148", "engine/bridge/trading_pipeline.py#L1145"]
---

# S Blue Type-1

Public formation Type-1 is the simple S Blue route (source formation_type=simple). It uses an ordinary directional candidate associated with the stopped A and opposite Order handoff. Pre-Order and post-Order ownership windows can select distinct candidate geometry. A qualifying strict candidate cross before the Order strict stop decides Blue; the exact geometry and tie behavior are in algorithm.s.type1.
