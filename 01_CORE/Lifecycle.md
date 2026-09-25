---
id: "core.lifecycle"
type: "core"
status: "canonical"
authority: "normative"
title: "Lifecycle ownership"
source_refs: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L589", "engine/pipeline/lifecycle_engine.py#L946"]
---

# Lifecycle ownership

A -> S -> E -> StopAll is the fixed stage order. A fallback rejected under accepted S cannot consume that S or feed descendants into E. Dominant stopped owner selection uses the most recent relevant stop main index before priority and number tie breaking. A starts a new cycle only when its trigger is strictly after a prior A stop; at/before overlaps.

S/E candidates can remain calculation evidence even when hidden from public display, subject to stage-invalid rules. Same physical source occupied by final E or StopAll suppresses lower-stage labels; calculation-eligible historical parents may be restored solely to keep lineage. StopAll resets active owner and Blue-repeat counters.
