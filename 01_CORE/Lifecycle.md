---
id: "core.lifecycle"
type: "core"
status: "pending"
authority: "non-canonical"
title: "Lifecycle ownership"
source_refs: []
related_entities: ["algorithm.lifecycle", "test.lifecycle_invariants"]
source_reference: []
---

# Lifecycle ownership

A -> S -> E -> StopAll is the fixed stage order. A fallback rejected under accepted S cannot consume that S or feed descendants into E. Dominant stopped owner selection uses the most recent relevant stop main index before priority and number tie breaking. A starts a new cycle only when its trigger is strictly after a prior A stop; at/before overlaps.

S/E candidates can remain calculation evidence even when hidden from public display, subject to stage-invalid rules. Same physical source occupied by final E or StopAll suppresses lower-stage labels; calculation-eligible historical parents may be restored solely to keep lineage. StopAll resets active owner and Blue-repeat counters.

For validation, distinguish **candidate → accepted owner → stopped owner → historical lineage or suppressed output**. A strict A stop can open S; an accepted S stop can open E1; a stopped eligible E can open its successor. A later accepted owner may hide an earlier public label while preserving its physical parent/cause history. A StopAll boundary clears the active sequence and pending Blue-repeat evidence; a new eligible post-boundary owner begins the next sequence. `test.lifecycle_invariants` checks these transitions and `algorithm.lifecycle` owns the detailed tie and priority rules.
