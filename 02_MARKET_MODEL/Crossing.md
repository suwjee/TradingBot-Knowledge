---
id: "market.crossing"
type: "market"
status: "active"
authority: "executable"
title: "Strict price crossing and equality"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
name: "Strict Crossing"
aliases: ["Strict crossing and equality"]
---

# Strict price crossing and equality

Strict price crossing excludes equality. Reaction confirmation is High > BoxTop for Bullish and Low < BoxBottom for Bearish. Behavior-space strict stops use Low < level for Bullish and High > level for Bearish. Strictness of a time window is independently owned by its component; do not infer time exclusion merely from a strict price comparator.
