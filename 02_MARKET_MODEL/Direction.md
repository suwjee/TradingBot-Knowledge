---
id: "market.direction"
type: "market"
status: "active"
authority: "empirical"
title: "Direction"
source_refs: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
related_entities: ["mirror.direction_mapping", "source.direction_policy"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
---

# Direction

The retained direction policy gives Bullish Low/min and strict Low < level; Reaction First is RED in GREEN context and confirms on High > BoxTop. Bearish uses High/max and strict High > level; First is GREEN in RED context and confirms on Low < BoxBottom. The retained Bearish detector uses reflected Bullish candles/candidates. Lifecycle, family labels, numbering, and serialization are traceable in captured source but remain pending/non-canonical until fresh paired validation and the B/C rewrite resolve affected outcomes; Doji classification is retained in the Reaction source.
