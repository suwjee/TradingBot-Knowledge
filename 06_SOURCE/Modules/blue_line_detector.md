---
id: "source.blue_line_detector"
type: "source"
status: "active"
authority: "executable"
title: "blue line detector"
source_path: "06_SOURCE/Code/engine/pipeline/blue_line_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/blue_line_detector.py"
sha256: "6fa01d94bc98060b62bc7e68db0ec24a0b0159727d44043affee7130a9c11448"
implements: ["algorithm.blue"]
affects: ["behavior.a", "behavior.s.blue.type4"]
source_refs: ["06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L1"]
related_entities: ["test.source_validation"]
source_reference: ["06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L1"]
---

# blue line detector
## Identity and snapshot
Production: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py
Mirror: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py
SHA-256: 6fa01d94bc98060b62bc7e68db0ec24a0b0159727d44043affee7130a9c11448
Declared versions: [('BLUE_LINE_VERSION', '2.3.0')]

## Responsibility
Owns Fibonacci 0.618, pending/confirmed Scale strikes, Reset Blue, spacing, calculation validity, and internal/public Blue filtering.

## Classes and owned concepts
ScaleStrike (L23), BlueLine (L30)

## Important symbols
- fibonacci_level: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L75
- count_scale_strikes: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L139
- _intrabar_pending_confirmation: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L84
- detect_blue_lines: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L299
- public_blue_lines: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L407
- mark_internal_blue_lines: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L416

## Inputs and outputs
Reaction/Reset and chronology -> BlueLine records with sourceExtreme, linePrice, validity and internal flags.

## State, direction, chronology, and invariants
Pending strike and prior count/Blue spacing are local state. Break-pending strike uses exact lower chronology. Invalid double-stop Reset Blue stays structural A evidence.

## Upstream dependencies and downstream consumers
Upstream: reaction_engine; direction_policy.


## Relationships
Algorithms: algorithm.blue.
Behaviors: behavior.a behavior.s.blue.type4.
