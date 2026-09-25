---
id: "market.crossing"
type: "market"
status: "active"
authority: "empirical"
title: "Strict crossing"
source_refs: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L211", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1066"]
related_entities: ["mirror.direction_mapping", "test.precision_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L211", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1066"]
---

# Strict crossing

The retained Reaction, direction-policy, A, and S crossing routines use strict < or > comparisons; equality does not satisfy those crossings. Their lower-timeframe scans choose the first qualifying event inside each routine's bounds. Reaction invalidation can win a same-second tie with confirmation; the retained S routine invalidates its candidate when the candidate and Order stop cross at the same lower event. Other stages and their bounds remain pending.
