---
id: "algorithm.s.type3"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "S Type-3 Reset-leg"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s.blue.type3"]
depends_on: ["algorithm.s", "algorithm.reset"]
source_refs: ["engine/pipeline/s_zone_detector.py#L457", "engine/pipeline/s_zone_detector.py#L482", "engine/pipeline/s_zone_detector.py#L1090"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/s_zone_detector.py#L457", "engine/pipeline/s_zone_detector.py#L482", "engine/pipeline/s_zone_detector.py#L1090"]
---

# S Type-3 Reset-leg

Before the first newly eligible opposite Order confirms (or calculation end if absent), a pre-existing opposite Reaction may Reset after A stop. Select directional source extreme over its owner Break through Reset main inclusive, last candle on equality. Find first strict candidate crossing before the deadline. At least one same-direction Reaction must confirm after A stop and no later than the crossing. The result is always Blue/public Type-3, with Reset provenance and no new Order geometry. A true exact-event tie with Type-4 uses detector Type-3 precedence.
