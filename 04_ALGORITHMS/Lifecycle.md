---
id: "algorithm.lifecycle"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Lifecycle eligibility and stage ownership"
implemented_by: ["source.lifecycle_engine", "source.trading_pipeline"]
produces: ["behavior.a", "behavior.s", "behavior.e"]
depends_on: ["algorithm.a", "algorithm.s", "algorithm.e"]
source_refs: ["engine/pipeline/lifecycle_engine.py#L946", "engine/pipeline/lifecycle_engine.py#L1172", "engine/bridge/trading_pipeline.py#L1903"]
---

# Lifecycle eligibility and stage ownership

Fixed stage order is A -> S -> E -> StopAll. Compare a later A to the most recent relevant stopped owner main index first; priority, number, and source break same-transition ties. If A price does not strictly extend beyond dominant stopped-owner price in trend direction, keep it. Otherwise apply the existing interior-leg provenance exception or reject. A -> A overlap is invalid when new triggerEventTime <= prior A strict stop; strictly later trigger may reopen.

When an A fallback is rejected under accepted S ownership, do not consume S. Mark that A stage-invalid and remove its S descendants from accepted S, E roots, StopAll participation, and suppressed-continuation evidence. Cycle validation must inspect every S-eligible A, including A temporarily hidden by provisional S. Other calculation-invalid A/S may remain geometry/audit/lineage evidence only where explicit rules allow.

S participation after larger stops uses exact owner stop and priority; an older high-priority object cannot own all later legs. Consumed lower-priority S can continue a stopped larger E when exact source/close and owner-selection rules qualify. The dominant stopped E owner is chosen by latest eligible stop-main index, then priority/number/source while respecting newer accepted E transitions.
