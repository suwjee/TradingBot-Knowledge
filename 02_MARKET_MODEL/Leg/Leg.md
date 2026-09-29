---
id: "market.leg"
type: "market"
status: "active"
authority: "executable"
title: "Current Reaction leg state"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
---

# Current Reaction leg state

A Reaction leg is the detector structural ownership interval. Mode A establishes the first candidate of a leg from context and First color with an outer boundary; strict invalidation releases that candidate before later confirmation when chronology proves it first. Mode B follows an accepted Reaction. A reset leg used for Order_B is a distinct current OrderAudit structure, not a generic conversion of every Reaction Reset into an Order.
