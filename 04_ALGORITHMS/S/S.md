---
id: "algorithm.s"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "S calculation and decision"
implemented_by: ["source.s_zone_detector"]
produces: ["behavior.s", "behavior.s.red", "behavior.s.blue"]
depends_on: ["algorithm.a", "algorithm.order", "algorithm.reaction"]
source_refs: ["engine/pipeline/s_zone_detector.py#L1319", "engine/pipeline/s_zone_detector.py#L964", "engine/pipeline/s_zone_detector.py#L1422"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/s_zone_detector.py#L1319", "engine/pipeline/s_zone_detector.py#L964", "engine/pipeline/s_zone_detector.py#L1422"]
---

# S calculation and decision

An eligible A's first strict trend-side price stop opens S at exact aStopEventTime. The earliest canonical opposite Reaction with First main index >= A-stop main index and confirmation > exact A stop is the immutable stopped-A Order_A owner, ranked (confirmationTime,FirstIndex,BreakIndex). S also tests independent Type-3/4 order-free routes before that Order deadline.

Order-backed routes choose pre-Order Simple, post-Order Simple, or nested Advanced candidate. The decision scan starts at Order confirmation and processes exact lower events: simultaneous candidate and Order-stop strict crossings invalidate; earlier Order stop gives Red; earlier qualified candidate crossing gives Blue. A candidate requires aligned Reset Blue already formed or ordinary trend Reaction confirmation after active behavior start and no later than decision. An unqualified pre-Order provisional cross falls back to post-Order evaluation. Main-candle fallback preserves branch order if lower data unavailable.

A later calculation-accepted physical Order may recolor an open S Red when order confirmation < stop event and S.sourceTime <= stop event < current decision; rank (stopEvent,confirmation,FirstIndex,BreakIndex). Freeze source/time/price; update family, decision, and Order provenance only. Shared use does not transfer creation cause.
