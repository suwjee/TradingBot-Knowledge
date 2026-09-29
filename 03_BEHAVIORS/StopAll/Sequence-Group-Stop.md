---
id: "behavior.stopall.sequence_group"
type: "behavior"
status: "active"
authority: "executable"
title: "StopAll sequence-group-stop gate"
version: "current"
related_entities: ["algorithm.stopall.sequence_group", "behavior.stopall"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.e_zone_detector", "source.s_zone_detector"]
name: "StopAll sequence group behavior"
---

# StopAll sequence-group-stop gate

Exact dominant S color or E(family,number) has >=2 accepted dominant occurrences;latest prior exact member first strictly stops <= incoming E decision. Incoming E creates fresh StopAll1 and donates physical geometry/Order regardless of family match. Creation resets dominant/Blue-repeat state.

Gate name is invariant across Bullish/Bearish;strict directional stop geometry reflects and price equality never stops.
