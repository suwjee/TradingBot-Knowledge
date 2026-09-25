---
id: "source.dependencies"
type: "source"
status: "active"
authority: "executable"
title: "Source dependency map"
source_refs: ["engine/bridge/trading_pipeline.py#L1698", "engine/bridge/trading_pipeline.py#L1903"]
relates_to: ["core.pipeline"]
---

# Source dependency map

Runtime loading: trading_pipeline.py adds engine/pipeline to sys.path, then dynamically loads reaction_engine and other detectors. Flat imports of core_utils and direction_policy in detector modules are supported through that bridge bootstrap; importing pipeline files directly as a package is not the production contract.

Data edges verified in source:
- bridge.prepare_market_context -> build_candle_buckets / build_candle_objects -> reaction_engine.LowerTimeframeIndex and MarketChronology.
- bridge.prepare_pipeline_state -> both direction UnifiedReactionDetector streams -> reaction_engine.build_behavior_reaction_views.
- bridge.calculate_full_direction_state -> blue_line_detector.detect_blue_lines -> a_zone_detector.detect_a_zones -> s_zone_detector.SZoneDetector.detect -> e_zone_detector.EZoneDetector.detect.
- S consumes A/Blue and opposite Reaction/Reset. E consumes accepted S, both Reaction/Reset streams, trend Blue, initial stopped-A Order ledger and lifecycle priority resolver.
- lifecycle_engine resolves A/S/E eligibility, StopAll, internal visibility, lineage, and audit preparation. Bridge serializes after these decisions.
- direction_policy and core_utils supply shared primitives to detectors; they own no cross-stage state.

The E detector may run more than once after S and Order context changes. StopAll is detected once on the reconciled input, so there is no E/StopAll fixed-point cycle. Graphify edges, when queried, remain navigational hints until confirmed in the current source.
