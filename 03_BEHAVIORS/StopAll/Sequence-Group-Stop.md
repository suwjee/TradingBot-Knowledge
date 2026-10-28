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
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# StopAll sequence-group-stop gate

One exact dominant S color or E(family,number) arms at its second accepted occurrence. Its first strict stop starts at the latest occurrence decision. A completed stop before an E source can create fresh StopAll1; an at/after-source stop additionally needs the exact direct-child parent proof or strict same-source-candle independent-E donor proof in algorithm.stopall.sequence_group. A later unrelated main candle cannot use that exception.

Incoming accepted E supplies geometry and physical Order provenance. A completed stop may remain frozen pending evidence after replacement; it is not a second repetition counter. StopAll creation resets owner/count/pending state. Strict Low/High geometry mirrors; identity, family and gate chronology remain invariant.
