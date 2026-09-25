---
id: "source.direction_policy"
type: "source"
status: "active"
authority: "executable"
title: "direction policy"
source_path: "engine/pipeline/direction_policy.py"
mirror: "06_SOURCE/Code/engine/pipeline/direction_policy.py"
sha256: "a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea"
implements: ["algorithm.reaction", "algorithm.blue", "algorithm.a", "algorithm.s", "algorithm.e"]
affects: []
source_refs: ["engine/pipeline/direction_policy.py#L1"]
---

# direction policy
## Identity and snapshot
Production: engine/pipeline/direction_policy.py
Mirror: 06_SOURCE/Code/engine/pipeline/direction_policy.py
SHA-256: a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea
Declared versions: [('DIRECTION_POLICY_VERSION', '1.0.0')]

## Responsibility
Owns behavior-neutral directional primitives only, not chronology, family, lifecycle or numbering.

## Classes and owned concepts
DirectionPolicy (L21)

## Important symbols
- DirectionPolicy.strict_cross: engine/pipeline/direction_policy.py#L32
- DirectionPolicy.better_extreme: engine/pipeline/direction_policy.py#L35
- DirectionPolicy.choose_extreme: engine/pipeline/direction_policy.py#L38
- DirectionPolicy.confirmation_cross: engine/pipeline/direction_policy.py#L41
- policy_for: engine/pipeline/direction_policy.py#L49

## Inputs and outputs
Direction and Decimal values -> opposite direction, strict cross, better extreme, confirmation predicate.

## State, direction, chronology, and invariants
Frozen policy: Bullish Low/min/<, First RED/GREEN context, High>BoxTop; Bearish High/max/>, First GREEN/RED context, Low<BoxBottom. Family and priority do not mirror.

## Upstream dependencies and downstream consumers
Upstream: none.

Downstream: reaction_engine, blue_line_detector, a_zone_detector, s_zone_detector, e_zone_detector, lifecycle_engine.

## Relationships
Algorithms: algorithm.reaction algorithm.blue algorithm.a algorithm.s algorithm.e.
Behaviors: No direct behavior ownership.
