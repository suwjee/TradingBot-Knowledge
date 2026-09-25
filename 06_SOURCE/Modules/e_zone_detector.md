---
id: "source.e_zone_detector"
type: "source"
status: "active"
authority: "executable"
title: "e zone detector"
source_path: "engine/pipeline/e_zone_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/e_zone_detector.py"
sha256: "6becc792a17e40f572673bf65bc9818c9a957244de811be2823402d41c36e628"
implements: ["algorithm.order", "algorithm.order.a", "algorithm.order.b", "algorithm.order.c", "algorithm.e", "algorithm.reconciliation", "algorithm.orderaudit"]
affects: ["behavior.e", "behavior.e.red", "behavior.e.blue"]
source_refs: ["engine/pipeline/e_zone_detector.py#L1"]
---

# e zone detector
## Identity and snapshot
Production: engine/pipeline/e_zone_detector.py
Mirror: 06_SOURCE/Code/engine/pipeline/e_zone_detector.py
SHA-256: 6becc792a17e40f572673bf65bc9818c9a957244de811be2823402d41c36e628
Declared versions: [('E_ZONE_VERSION', '6.14.2')]

## Responsibility
Owns physical Order_A/B/C discovery and use, recursive E chains, accepted cause ledger, family/number reconciliation and continuation.

## Classes and owned concepts
EZone (L27), OrderBFormation (L75), OrderCFormation (L99), EZoneDetector (L118)

## Important symbols
- EZoneDetector._build_order_b_formations: engine/pipeline/e_zone_detector.py#L499
- EZoneDetector._build_order_c_formations: engine/pipeline/e_zone_detector.py#L727
- EZoneDetector._direct_parent_stop_order: engine/pipeline/e_zone_detector.py#L1058
- EZoneDetector._post_stop_accepted_orders_for_parent: engine/pipeline/e_zone_detector.py#L1901
- EZoneDetector._zone: engine/pipeline/e_zone_detector.py#L2040
- EZoneDetector._reconcile_candidate_chains: engine/pipeline/e_zone_detector.py#L2463
- EZoneDetector.resolve_same_source_conflicts: engine/pipeline/e_zone_detector.py#L2267
- EZoneDetector.detect: engine/pipeline/e_zone_detector.py#L3118

## Inputs and outputs
Accepted S, both Reaction/Reset streams, Blue, chronology, stopped-A ledger, lifecycle priority -> EZone, OrderBFormation/OrderCFormation, accepted physical Order ledger.

## State, direction, chronology, and invariants
Caches physical identity, B/C formations, confirmation and strict stop lookups. Creation causes stay separate from accepted/carried use. Historical rescues cannot feed calculation. Same-source E conflict is reconciled.

## Upstream dependencies and downstream consumers
Upstream: reaction_engine; s_zone_detector; blue_line_detector; lifecycle_engine sequence_priority; core_utils; direction_policy.

Downstream: lifecycle_engine, trading_pipeline.

## Relationships
Algorithms: algorithm.order algorithm.order.a algorithm.order.b algorithm.order.c algorithm.e algorithm.reconciliation.
Behaviors: behavior.e behavior.e.red behavior.e.blue.
