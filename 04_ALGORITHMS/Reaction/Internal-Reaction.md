---
id: "algorithm.internal_reaction"
type: "algorithm"
status: "active"
authority: "executable"
title: "Cross-direction internal Reaction ownership"
version: "current"
related_entities: ["algorithm.blue", "algorithm.reaction", "algorithm.visibility"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.reaction_engine", "source.blue_line_detector", "source.lifecycle_engine", "source.trading_pipeline"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L182", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L182"]
mirror_links: ["mirror.contract"]
name: "Internal Reaction"
aliases: ["InternalReaction"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Cross-direction internal Reaction ownership

## Bullish

#### 4.8 Internal Reaction ownership

Cross-direction internal protection is determined after both directions exist. A candidate is internal only when its temporal/box structure is contained by a healthy opposite Reaction and the complete lower-timeframe physical path through its confirmation remains inside the protecting box. Internal identity affects behavior/public ownership; it does not delete historical calculation evidence or renumber the canonical Reaction stream.

## Bearish

#### 4.8 Internal Reaction ownership

Cross-direction internal protection is determined after both directions exist. A candidate is internal only when its temporal/box structure is contained by a healthy opposite Reaction and the complete lower-timeframe physical path through its confirmation remains inside the protecting box. Internal identity affects behavior/public ownership; it does not delete historical calculation evidence or renumber the canonical Reaction stream.

## Source-level contract

Inner First > outer First; inner confirmation <= outer confirmation; inner published top <= outer top and bottom >= outer bottom. Nonempty complete physical lower path through inner confirmation inclusive requires min Low >= outer bottom and max High <= outer top. Containment permits box-edge equality.

build_behavior_reaction_views attaches internal identity, original public ordinal and published box/time metadata without deleting canonical streams. Blue point protection is strict interior with First < source_time <= confirmation and both source_extreme/line_price inside. Current filter_internal_behavior_outputs returns accepted A/S/E/StopAll unchanged; it does not discard all internal physical Orders.
