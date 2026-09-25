---
id: "algorithm.reaction"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Reaction"
implemented_by: ["source.reaction_engine"]
produces: ["algorithm.reset", "algorithm.internal_reaction"]
depends_on: ["algorithm.raw", "market.direction", "market.exact_chronology"]
source_refs: ["engine/pipeline/reaction_engine.py#L174", "engine/pipeline/reaction_engine.py#L646", "engine/pipeline/reaction_engine.py#L1376"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/reaction_engine.py#L174", "engine/pipeline/reaction_engine.py#L646", "engine/pipeline/reaction_engine.py#L1376"]
---

# Reaction

Bullish First is RED after GREEN context; Bearish First is GREEN after RED context, executed through reflected Bullish coordinates. Native Mode A is first/Reset recovery; Mode B is continued Normal search. Bullish confirms only on High > BoxTop; Bearish on Low < BoxBottom. A frozen owner floor/ceiling strictly invalidates Mode A before confirmation; when both events occur in one main candle, lower-timeframe first event decides and an exact tie invalidates first.

Candidate stores First, box edges and their physical sources, mode, optional anchor/leg boundary, Break, exact intrabar start, and internal/public metadata. On confirmation, outer edge remains the discovered threshold; opposite edge is min Low (Bullish) or max High (Bearish) First..Break inclusive, refined through exact confirmation if Break owns it. Published geometry freezes Break-sourced opposite edge at confirmation, excluding later same-candle prices. A confirmation candle may seed the next Mode-B First only when no post-confirmation same-Break Reset exists.

Normal Mode B carries the running trend-side outer extreme. Reset reopens same-direction Mode A without an opposite pattern gate. Direct/anchor candidates compete by earliest valid exact confirmation. Both directional streams are required for S/E opposite-Order geometry.
