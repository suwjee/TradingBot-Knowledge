---
id: "market.direction"
type: "market"
status: "canonical"
authority: "normative"
title: "Direction"
source_refs: ["engine/pipeline/direction_policy.py#L21", "engine/pipeline/reaction_engine.py#L560"]
---

# Direction

Bullish trend extreme is Low/min with strict Low < level; Reaction First is RED in GREEN context and confirms on High > BoxTop. Bearish trend extreme is High/max with strict High > level; First is GREEN in RED context and confirms on Low < BoxBottom. Bearish detector uses reflected Bullish candles/candidates. Direction-invariant lifecycle, family labels, Doji, numbering, and serialization are not reflected.
