---
id: "algorithm.order"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Physical Order and provenance"
implemented_by: ["source.reaction_engine", "source.e_zone_detector", "source.s_zone_detector"]
depends_on: ["algorithm.reaction", "market.exact_chronology"]
source_refs: ["engine/pipeline/reaction_engine.py#L1137", "engine/pipeline/e_zone_detector.py#L1229", "engine/pipeline/core_utils.py#L19"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/reaction_engine.py#L1137", "engine/pipeline/e_zone_detector.py#L1229", "engine/pipeline/core_utils.py#L19"]
---

# Physical Order and provenance

A physical Order is an opposite-direction canonical Reaction with identity (FirstIndex,BreakIndex); one identity may have several independently proven creation causes. The trend direction's Order is Bearish for Bullish calculations and Bullish for Bearish. Native Reaction Mode A/B is not Order_A/B/C. A physical Order's confirmation uses exact opposite Reaction chronology. Its strict Order stop is obtained once through MarketChronology.canonical_order_stop: Mode A computes the true leg outer boundary from anchor/context through Break inclusive (Bearish maximum High, Bullish minimum Low); Mode B inherits the previous healthy opposite Reaction's BoxTop (Bearish) or BoxBottom (Bullish). A Mode B Order without previous healthy Reaction is invalid.

Creation causes are parent-stop (Order_A), reset-leg (Order_B), blue-leg (Order_C). Carried-live and accepted-live are use routes, never replacement creation causes. Direct, carried, parent-neutral accepted-live, Reset-leg, and Blue-leg physical Orders compete by exact strict stop event where their parent lifecycle permits. One exact parent-stop cause can belong to only one physical Order. Do not manufacture a cause because a behavior reused an already accepted Order.
