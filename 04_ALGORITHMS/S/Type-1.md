---
id: "algorithm.s.type1"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "S Type-1 Simple"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s.blue.type1", "behavior.s.red"]
depends_on: ["algorithm.s", "algorithm.order.a"]
source_refs: ["engine/pipeline/s_zone_detector.py#L820", "engine/pipeline/s_zone_detector.py#L1148", "engine/bridge/trading_pipeline.py#L1145"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/s_zone_detector.py#L820", "engine/pipeline/s_zone_detector.py#L1148", "engine/bridge/trading_pipeline.py#L1145"]
---

# S Type-1 Simple

Simple is an order-backed S candidate route. A pre-Order source uses the directional extreme from exact A-stop remainder through Order First inclusive. Post-Order Simple uses Order Break through first subsequent aligned Reaction Break inclusive, with last candle owning equal extrema. An exact candidate formation earlier than Order First main timestamp can reclassify a provisional after route to before; equality stays after. Source helper tie policies must be preserved by branch. A qualified strict candidate crossing before Order stop produces Blue/public Type-1; an Order stop first produces Red with no public numbered formation. Simultaneous strict crossings invalidate the candidate.
