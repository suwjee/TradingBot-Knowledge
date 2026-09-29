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
reference_agreement: "ambiguous"
reference_conflicts: ["REF-S-MODE-B"]
name: "StopAll reversal behavior"
---

# StopAll opposite-s-group-stop gate

Accepted Blue keys are S and each exact E number;count>=2 qualifies and different E numbers never combine. Incoming accepted S Red with final order_mode=B creates fresh StopAll1. Latest qualified occurrence chooses metadata. Accepted Red S,Red E or any hard StopAll clears earlier Blue evidence,even when a final Mode-A Red cannot promote.

Gate name is invariant across Bullish/Bearish;strict directional stop geometry reflects and price equality never stops.


The stronger Reference phrase 'native Mode-B formation Order' has unresolved scope after shared accepted-Order recoloring. See source.reference_consistency; no original subtype/formation guard is added to the executable predicate.
