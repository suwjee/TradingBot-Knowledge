---
id: "behavior.stopall.stopall_stop"
type: "behavior"
status: "active"
authority: "executable"
title: "StopAll stopall-stop gate"
version: "current"
related_entities: ["algorithm.stopall.stopall_stop", "behavior.stopall"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.e_zone_detector", "source.s_zone_detector"]
---

# StopAll stopall-stop gate

Active StopAll first strict stops <= incoming E decision qualify. Incoming E donates geometry/Order,new number=max(stopped active number)+1,gate event=earliest qualifying stop,count=number of qualified active identities. Historical objects remain while stopped active ownership leaves. This gate is checked before repeated-sequence gate.

Gate name is invariant across Bullish/Bearish;strict directional stop geometry reflects and price equality never stops.
