---
id: "behavior.s"
type: "behavior"
status: "canonical"
authority: "normative"
title: "S"
calculated_by: ["algorithm.s"]
implemented_by: ["source.s_zone_detector", "source.lifecycle_engine"]
depends_on: ["behavior.a", "algorithm.order"]
parent_of: ["behavior.s.red", "behavior.s.blue"]
source_refs: ["engine/pipeline/s_zone_detector.py#L26", "engine/bridge/trading_pipeline.py#L1130"]
---

# S

S is the behavior opened by an eligible A strict stop. It owns an A parent and carries an A-stop event, source/decision event, price, family color, and optional physical Order provenance. A first opposite Order_A after A stop is immutable for the stopped-A route. S may also form through order-free Type-3 or Type-4 Blue routes.

The S family is Red when an accepted opposite Order strict stop wins; Blue when a qualified directional candidate strict cross wins. A same lower event crossing both candidate and Order stop invalidates the candidate. Later accepted physical Order stops may recolor an open S Red without moving its source or fabricating Order creation provenance. Lifecycle can consume S as non-public evidence for E continuation; stage-invalid A descendants cannot return.

Public Blue formation values Type-1..4 correspond to simple, advanced, type3, type4. Red S has no public numbered formation.
