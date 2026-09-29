---
id: "behavior.s.blue.type2"
type: "behavior"
status: "active"
authority: "executable"
title: "S Blue Type-2 Advanced"
version: "current"
related_entities: ["algorithm.s.type2", "behavior.s.blue"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.s_zone_detector", "source.order_audit_engine", "source.reaction_engine"]
---

# S Blue Type-2 Advanced

Native Advanced Blue requires a completed aligned Reaction wholly inside canonical opposite Order before its confirmation. Bullish candidate is Order bottom-source candle Low;Bearish top-source candle High. Candidate qualification starts at nested confirmation. Strict candidate cross beats physical Order stop;same-position tie yields no decision. Valid nested ownership cannot be stolen by Simple pre-Order timing optimization.

Native formation_type=advanced. Later shared accepted-Order reconciliation can recolor the subtype without changing frozen source/price;it does not create a new Order route.
