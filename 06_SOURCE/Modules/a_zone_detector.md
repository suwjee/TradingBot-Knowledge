---
id: "source.a_zone_detector"
type: "source"
status: "active"
authority: "executable"
title: "a zone detector"
source_path: "engine/pipeline/a_zone_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/a_zone_detector.py"
sha256: "d7c33dd619ad7e4590027667a2c4e984c83be7b82fbfafeb5d7f944ddd521097"
implements: ["algorithm.a"]
affects: ["behavior.a"]
source_refs: ["engine/pipeline/a_zone_detector.py#L1"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/a_zone_detector.py#L1"]
---

# a zone detector
## Identity and snapshot
Production: engine/pipeline/a_zone_detector.py
Mirror: 06_SOURCE/Code/engine/pipeline/a_zone_detector.py
SHA-256: d7c33dd619ad7e4590027667a2c4e984c83be7b82fbfafeb5d7f944ddd521097
Declared versions: [('A_ZONE_VERSION', '1.6.4')]

## Responsibility
Owns ordinary adjacent-Blue and special double-stop A formation, inherited stop, exact trigger/source and pair cycle.

## Classes and owned concepts
BlueState (L25), AZone (L38), AZoneDetector (L67)

## Important symbols
- AZoneDetector._build_blue_states: engine/pipeline/a_zone_detector.py#L219
- AZoneDetector._pair_trigger: engine/pipeline/a_zone_detector.py#L311
- AZoneDetector._inherited_stop: engine/pipeline/a_zone_detector.py#L494
- AZoneDetector._detect_ordinary_a: engine/pipeline/a_zone_detector.py#L568
- AZoneDetector._double_stop_a_candidates: engine/pipeline/a_zone_detector.py#L248
- AZoneDetector.detect: engine/pipeline/a_zone_detector.py#L753

## Inputs and outputs
Reaction, Blue and chronology -> AZone candidates with Blue ordinals, trigger event, source, price.

## State, direction, chronology, and invariants
BlueState pairs and cycle consumption are local. Open Scale Blue cannot borrow hypothetical inherited stop. Source ends at exact validating confirmation; Bearish/Bullish inherited windows mirror price, not time.

## Upstream dependencies and downstream consumers
Upstream: reaction_engine; blue_line_detector; core_utils; direction_policy.

Downstream: s_zone_detector, lifecycle_engine, trading_pipeline.

## Relationships
Algorithms: algorithm.a.
Behaviors: behavior.a.
