---
id: "algorithm.lifecycle"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Lifecycle eligibility and stage ownership"
implemented_by: ["source.lifecycle_engine"]
depends_on: ["algorithm.a", "algorithm.s", "algorithm.e"]
source_refs: []
affects: ["behavior.a", "behavior.s", "behavior.e"]
related_entities: ["test.source_validation", "test.lifecycle_invariants"]
source_reference: []
---

# Lifecycle eligibility and stage ownership

## Calculation logic

Fixed stage order is A -> S -> E -> StopAll. Compare a later A to the most recent relevant stopped owner main index first; priority, number, and source break same-transition ties. If A price does not strictly extend beyond dominant stopped-owner price in trend direction, keep it. Otherwise apply the existing interior-leg provenance exception or reject. A -> A overlap is invalid when new triggerEventTime <= prior A strict stop; strictly later trigger may reopen.

When an A fallback is rejected under accepted S ownership, do not consume S. Mark that A stage-invalid and remove its S descendants from accepted S, E roots, StopAll participation, and suppressed-continuation evidence. Cycle validation must inspect every S-eligible A, including A temporarily hidden by provisional S. Other calculation-invalid A/S may remain geometry/audit/lineage evidence only where explicit rules allow.

S participation after larger stops uses exact owner stop and priority; an older high-priority object cannot own all later legs. Consumed lower-priority S can continue a stopped larger E when exact source/close and owner-selection rules qualify. The dominant stopped E owner is chosen by latest eligible stop-main index, then priority/number/source while respecting newer accepted E transitions.

## Contract interface

- **Purpose:** Choose accepted sequence ownership and lifecycle boundaries.
- **Inputs:** A/S/E candidates, exact stop chronology, priority and source identities.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Accepted, stopped, hidden or restored lineage and final owner state.
- **Source ownership:** source.lifecycle_engine.
- **Validation relationship:** test.lifecycle_invariants; test.source_validation checks the line anchors and owner.
