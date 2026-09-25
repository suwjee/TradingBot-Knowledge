---
id: "source.s_zone_detector"
type: "source"
status: "active"
authority: "executable"
title: "s zone detector"
source_path: "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"
sha256: "7714025b3f43087b09844df6feeef4eef0ec72eeb841115293df4c126fd202ee"
implements: ["algorithm.s", "algorithm.s.type1", "algorithm.s.type2", "algorithm.s.type3", "algorithm.s.type4", "algorithm.order.a", "algorithm.order", "algorithm.orderaudit"]
affects: ["behavior.s", "behavior.s.red", "behavior.s.blue"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1"]
related_entities: ["test.source_validation"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1"]
---

# s zone detector
## Identity and snapshot
Production: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py
Mirror: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py
SHA-256: 7714025b3f43087b09844df6feeef4eef0ec72eeb841115293df4c126fd202ee
Declared versions: [('S_ZONE_VERSION', '4.20.0')]

## Responsibility
Owns A-to-S handoff, immutable first stopped-A Order, Simple/Advanced/Type-3/Type-4 candidate routes, exact decision race and shared accepted Order-stop reconciliation.

## Classes and owned concepts
SZone (L26), SZoneDetector (L64)

## Important symbols
- SZoneDetector._first_order_after: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L274
- SZoneDetector._first_type3: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L482
- SZoneDetector._first_type4: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L543
- SZoneDetector._decision: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L964
- SZoneDetector.detect: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1319
- SZoneDetector.reconcile_shared_order_stops: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1422

## Inputs and outputs
Trend/opposite Reactions, opposite Resets, Blue, A, chronology -> SZone candidates, eligible A, initial stopped-A audit.

## State, direction, chronology, and invariants
Stores A ownership windows, sorted opposite Order matches, Reset/Blue event indexes and caches. Same-event candidate+Order stop invalidates; accepted-live use never changes creation cause.

## Upstream dependencies and downstream consumers
Upstream: reaction_engine; blue_line_detector; a_zone_detector; core_utils; direction_policy.

Downstream: e_zone_detector, lifecycle_engine, trading_pipeline.

## Relationships
Algorithms: algorithm.s algorithm.s.type1 algorithm.s.type2 algorithm.s.type3 algorithm.s.type4 algorithm.order.a.
Behaviors: behavior.s behavior.s.red behavior.s.blue.
