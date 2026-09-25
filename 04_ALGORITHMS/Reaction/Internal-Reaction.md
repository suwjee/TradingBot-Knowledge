---
id: "algorithm.internal_reaction"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Internal Reaction"
implemented_by: ["source.reaction_engine"]
depends_on: ["algorithm.reaction"]
source_refs: ["engine/pipeline/reaction_engine.py#L1202", "engine/pipeline/lifecycle_engine.py#L1658"]
related_entities: ["test.source_validation", "mirror.exceptions"]
source_reference: ["engine/pipeline/reaction_engine.py#L1202", "engine/pipeline/lifecycle_engine.py#L1658"]
---

# Internal Reaction

After both directional streams exist, classify a Reaction internal only when its First is strictly after an opposite Reaction First; its confirmation is no later than the opposite confirmation; its published box lies inside the opposite published box; and every lower event from inner First through confirmation remains inside that outer box.

Internal status does not erase calculation geometry. Blue may be marked internal for public display. Order_B raw opposite geometry may use internal evidence. In the accepted physical-Order ledger, an internal native Mode-B Order is rejected only when all surviving creation causes are reset-leg; an independent parent-stop/blue-leg cause protects that ledger identity (`lifecycle_engine.py#L777-L800`). Final E/StopAll output visibility uses a different predicate that conflicts with the references for mixed causes (`lifecycle_engine.py#L1658-L1708`); see `mirror.exceptions`. Do not infer its accepted behavior from the ledger rule.
