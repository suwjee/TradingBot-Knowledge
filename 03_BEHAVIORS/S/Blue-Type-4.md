---
id: "behavior.s.blue.type4"
type: "behavior"
status: "canonical"
authority: "normative"
title: "S Blue Type-4"
calculated_by: ["algorithm.s.type4"]
implemented_by: ["source.s_zone_detector", "source.trading_pipeline"]
depends_on: ["behavior.s.blue", "algorithm.blue"]
source_refs: ["engine/pipeline/s_zone_detector.py#L543", "engine/pipeline/s_zone_detector.py#L613"]
---

# S Blue Type-4

Public formation Type-4 is an order-free aligned-Reaction S Blue route. After A strictly stops, the latest same-direction Reaction rebuilds its candidate. A strict directional cross becomes S Blue only with calculation-valid, non-Internal Blue evidence formed no later than the crossing. The route ends when the first eligible opposite Order confirms. An unqualified cross emits no Type-4; a later aligned Reaction can rebuild the candidate. Exact event and interval rules live in algorithm.s.type4.
