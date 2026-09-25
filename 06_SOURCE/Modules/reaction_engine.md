---
id: "source.reaction_engine"
type: "source"
status: "active"
authority: "executable"
title: "reaction engine"
source_path: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
sha256: "bea0d5a5e95ee15ad54d024f6c01b8c777ba2abcc3c8e671118f1ae2df28f2a6"
implements: ["algorithm.reaction", "algorithm.reset", "algorithm.internal_reaction", "algorithm.order", "algorithm.raw"]
affects: ["behavior.a", "behavior.s", "behavior.e"]
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1"]
related_entities: ["test.source_validation"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1"]
---

# reaction engine
## Identity and snapshot
Production: 06_SOURCE/Code/engine/pipeline/reaction_engine.py
Mirror: 06_SOURCE/Code/engine/pipeline/reaction_engine.py
SHA-256: bea0d5a5e95ee15ad54d024f6c01b8c777ba2abcc3c8e671118f1ae2df28f2a6
Declared versions: [('REACTION_ENGINE_VERSION', '9.8.0')]

## Responsibility
Owns Candle/Candidate/ResetEvent, Bullish detector, reflected Bearish detector, UnifiedReactionDetector, lower index, MarketChronology, public frozen Reaction geometry, and internal classification.

## Classes and owned concepts
Candle (L27), Candidate (L39), ResetEvent (L67), IntrabarAnalysis (L76), DetectionResult (L83), DetectorBase (L101), BullishDetector (L174), _ReflectedCandles (L608), BearishDetector (L646), LowerTimeframeIndex (L809), ReflectedLowerTimeframeIndex (L947), MarketChronology (L971), UnifiedReactionDetector (L1376)

## Important symbols
- BullishDetector.detect: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L282
- BearishDetector.detect: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L695
- UnifiedReactionDetector.detect: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L2104
- published_reaction_candidate: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L706
- build_behavior_reaction_views: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1202
- MarketChronology.reaction_confirmation: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1089
- MarketChronology.canonical_order_stop: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1137
- UnifiedReactionDetector.first_order_reaction_after_gate: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1758

## Inputs and outputs
Main/lower candles and direction -> both directional Reaction/Reset streams and exact chronology queries.

## State, direction, chronology, and invariants
Candidate Mode A/B and frozen boundaries; lower first-cross/range indexes; confirmation/Reset caches. Exact invalidation-before-confirmation ties and same-Break Reset are decisive.

## Upstream dependencies and downstream consumers
Upstream: trading_pipeline raw construction; core_utils; direction_policy.

Downstream: blue_line_detector, a_zone_detector, s_zone_detector, e_zone_detector, lifecycle_engine, trading_pipeline serialization.

## Relationships
Algorithms: algorithm.reaction algorithm.reset algorithm.internal_reaction algorithm.order.
Behaviors: behavior.a behavior.s behavior.e.
