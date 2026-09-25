---
id: "algorithm.s.type2"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "S Type-2 Advanced"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s.blue.type2", "behavior.s.red"]
depends_on: ["algorithm.s", "algorithm.reaction"]
source_refs: ["engine/pipeline/s_zone_detector.py#L418", "engine/pipeline/s_zone_detector.py#L1148"]
---

# S Type-2 Advanced

Advanced is selected when a complete nested same-direction Reaction is wholly inside the opposite Order before that Order confirms. The nested Reaction must already be valid when ownership is classified as after. Candidate source is the Order's opposite semantic box edge: Bullish BoxBottom source, Bearish BoxTop source. It cannot decide before nested trend confirmation. The shared exact S decision race applies; qualified candidate cross gives Blue/public Type-2, Order stop first gives Red, same-event dual crossing invalidates.
