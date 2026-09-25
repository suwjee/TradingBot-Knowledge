---
id: "behavior.a"
type: "behavior"
status: "canonical"
authority: "normative"
title: "A"
calculated_by: ["algorithm.a"]
implemented_by: ["source.a_zone_detector", "source.lifecycle_engine"]
depends_on: ["algorithm.blue", "algorithm.reaction"]
source_refs: ["engine/pipeline/a_zone_detector.py#L38", "engine/pipeline/lifecycle_engine.py#L946", "engine/bridge/trading_pipeline.py#L1040"]
related_entities: ["test.behavior_invariants"]
source_reference: ["engine/pipeline/a_zone_detector.py#L38", "engine/pipeline/lifecycle_engine.py#L946", "engine/bridge/trading_pipeline.py#L1040"]
---

# A

A is one public behavior. An ordinary adjacent-Blue route and a special double-stop route may create it, but these are calculation routes, not separate A behaviors. A carries Blue pair, validating Reaction, trigger, source, and price provenance. A is the smallest lifecycle owner.

A may become S parent only after its first strict directional stop: Bullish Low < A.price; Bearish High > A.price. The exact lower event and main candle are distinct. A can be hidden at an S/E/StopAll source or invalidated by a dominant stopped owner. A fallback rejected under accepted S cannot consume that S or produce valid S descendants. A historical A referenced by final S may remain visible unless a higher-stage source occupies the same candle.

Calculation details: algorithm.a and algorithm.lifecycle.
