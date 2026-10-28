---
id: "behavior.stopall.blue_reversal"
type: "behavior"
status: "active"
authority: "executable"
title: "StopAll opposite-s-group-stop gate"
version: "current"
related_entities: ["algorithm.stopall.blue_reversal", "behavior.stopall", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.e_zone_detector", "source.s_zone_detector"]
reference_agreement: "match"
reference_conflicts: []
name: "StopAll reversal behavior"
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# StopAll accepted S Red donor

The current exact dominant Blue S/E owner must be armed with count >=2 and its latest decision strictly before the incoming accepted S Red decision. The first qualifying S Red directly donates StopAll1 in either Order Mode A or B; no prior strict Blue price stop is required. gateEventTime is the S decision. The legacy opposite-s-group-stop name also covers the separate Mode-B fallback using an already completed frozen Blue owner stop.

There is one active exact owner and no independent Blue-repeat ledger. Displaced lower-priority Blue cannot re-arm. Hard StopAll resets owner/count/pending stop. See algorithm.stopall.blue_reversal and source.reference_consistency for scope and evidence.
