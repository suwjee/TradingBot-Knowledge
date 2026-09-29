---
id: "mirror.contract"
type: "mirror"
status: "active"
authority: "executable"
title: "Current directional mirror contract"
version: "current"
related_entities: ["mirror.direction_mapping", "mirror.exceptions", "mirror.invariants", "mirror.validation_rules"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
---

# Current directional mirror contract

## Current implementation

BearishDetector executes the Bullish reference state machine through exact reflected Candle/Analysis/Candidate coordinates. UnifiedReactionDetector maintains explicit directional normal/post-Reset branches over original candles. DirectionPolicy supplies price-side primitives,not chronology,lifecycle,numbering or visibility. Both current references cover these same production owners.

## Price transform

High/Low,max/min,strict comparators and explicit inclusive price comparators map by owner. Bullish FirstRed after GREEN maps to Bearish FirstGreen after RED. Bullish confirmation High>BoxTop maps to Bearish Low<BoxBottom. Behavior stop Low<level maps High>level; physical opposite Order uses its own direction predicate. Fibonacci/Blue rendered formulas reflect geometrically.

## Invariants

Time,chronology windows,physical identity,provenance,Red/Blue behavior family,priority,accepted numbering,nullability/public keys/stable ordering retain semantics. Market Doji remains GREEN. Internal reflected role tag swapping cannot recolor original market candles.

## Boundary scope

Current Source and canonical References specify Blue decisive confirmation-row eligibility and shared S source-main-time equality in both directions. These inclusive time gates do not relax strict price crossing. Documentation/static Source coverage does not prove independent real-data correctness or supply stored fixture evidence.
