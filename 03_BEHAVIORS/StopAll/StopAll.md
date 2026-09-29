---
id: "behavior.stopall"
type: "behavior"
status: "active"
authority: "executable"
title: "StopAll hard-cycle behavior"
version: "current"
related_entities: ["algorithm.stopall", "behavior.stopall.blue_reversal", "behavior.stopall.sequence_group", "behavior.stopall.stopall_stop"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.e_zone_detector", "source.s_zone_detector"]
---

# StopAll hard-cycle behavior

StopAll is highest-priority accepted numbered behavior and hard chronological prefix boundary. Current gates are sequence-group-stop,stopall-stop,opposite-s-group-stop. number is lifecycle occurrence,not subtype.

Exact donor source/decision/physical Order provenance differs from stopped-group metadata. First strict directional stop at/after decision can open numbered continuation. Creation clears dominant sequence and pending Blue-repeat state while retaining historical output;future state cannot move/remove decided prefix.
