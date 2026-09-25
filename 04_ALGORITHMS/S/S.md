---
id: "algorithm.s"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "S calculation and decision"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s", "behavior.s.red", "behavior.s.blue"]
depends_on: ["algorithm.a", "algorithm.order", "algorithm.reaction"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1319", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L964", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1422"]
related_entities: ["test.source_validation", "test.behavior_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1319", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L964", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1422"]
---

# S calculation and decision

## Calculation logic

An eligible A's first strict trend-side price stop opens S at exact aStopEventTime. The earliest canonical opposite Reaction with First main index >= A-stop main index and confirmation > exact A stop is the immutable stopped-A Order_A owner, ranked (confirmationTime,FirstIndex,BreakIndex). S also tests independent Type-3/4 order-free routes before that Order deadline.

Order-backed routes choose pre-Order Simple, post-Order Simple, or nested Advanced candidate. The decision scan starts at Order confirmation and processes exact lower events: simultaneous candidate and Order-stop strict crossings invalidate; earlier Order stop gives Red; earlier qualified candidate crossing gives Blue. A candidate requires aligned Reset Blue already formed or ordinary trend Reaction confirmation after active behavior start and no later than decision. An unqualified pre-Order provisional cross falls back to post-Order evaluation. Main-candle fallback preserves branch order if lower data unavailable.

A later calculation-accepted physical Order may recolor an open S Red when order confirmation < stop event and S.sourceTime <= stop event < current decision; rank (stopEvent,confirmation,FirstIndex,BreakIndex). Freeze source/time/price; update family, decision, and Order provenance only. Shared use does not transfer creation cause.

## Contract interface

- **Purpose:** Select Red or Blue S after an eligible A stop.
- **Inputs:** A strict stop, physical Orders, directional candidate sources and exact lower race.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Accepted or rejected S with color, subtype, source and Order provenance.
- **Source ownership:** source.s_zone_detector.
- **Validation relationship:** test.behavior_invariants; test.source_validation checks the line anchors and owner.
