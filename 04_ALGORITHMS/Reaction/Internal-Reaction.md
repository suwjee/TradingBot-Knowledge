---
id: "algorithm.internal_reaction"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Internal Reaction"
implemented_by: ["source.reaction_engine", "source.lifecycle_engine", "source.trading_pipeline"]
depends_on: ["algorithm.reaction", "algorithm.visibility"]
source_refs: ["engine/pipeline/reaction_engine.py#L1202", "engine/pipeline/lifecycle_engine.py#L1658"]
---

# Internal Reaction

After both directional streams exist, classify a Reaction internal only when its First is strictly after an opposite Reaction First; its confirmation is no later than the opposite confirmation; its published box lies inside the opposite published box; and every lower event from inner First through confirmation remains inside that outer box.

Internal status does not erase calculation geometry. Blue may be marked internal for public display. Order_B raw opposite geometry may use internal evidence. The later public Order filter is narrow: a native Mode-B internal physical Order is excluded only if every surviving creation cause is Reset-leg; an independent parent-stop/blue-leg cause survives.
