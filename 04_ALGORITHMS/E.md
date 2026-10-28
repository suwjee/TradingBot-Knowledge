---
id: "algorithm.e"
type: "algorithm"
status: "active"
authority: "executable"
title: "E physical-Order race and recursive accepted lifecycle"
version: "current"
related_entities: ["algorithm.order", "algorithm.reconciliation", "algorithm.s", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L376", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L856", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L991", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1244", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1369", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1392", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1453", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L500", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L880", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.e_zone_detector", "source.order_audit_engine", "source.lifecycle_engine", "source.reaction_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L271", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L271"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.s", "algorithm.order", "algorithm.orderaudit"]
name: "E"
aliases: ["E Zone", "EZone"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# E physical-Order race and recursive accepted lifecycle

## Bullish

### 8.1 Parent stop and E-space opening

Every E cycle starts only after the first strict Bullish stop of an accepted S/E parent. For an E parent, a stop search begins at its decision event, so E cannot stop before the Order-stop event that confirmed it. Sequence/StopAll boundaries may later reinterpret parent type, but do not invent a different price event.

### 8.2 Physical Order choices

At each parent stop, E considers physical Orders from these routes: direct parent-stop Order_A, an S-carried unconsumed Order, a gate-owned initial A Order, carried-live accepted identity, post-stop accepted-live identity, and accepted Order_B reset-leg identities. `parent-stop` and `reset-leg` are creation causes; `carried-live` / `accepted-live` are use routes only. A candidate must possess an exact strict Order stop. Winner is earliest stop event; for an exact same stop event the larger Order First index wins (`-FirstIndex` tie key). Sequence reset boundaries may invalidate an Order crossing that would span a hard reset.

E performs this comparison over one complete eligible candidate set spanning all direct, inherited, carried and post-stop accepted routes. No route may reduce to a single candidate before the global `(exact stop event, -FirstIndex)` adjudication. This E-consumption tie rule does not change physical Order creation ordering.

### 8.3 E source and decision

`decision_event = max(parent_stop_event, order_stop_event)`. The E source is the minimum Low across the **complete main candle containing the parent stop through the complete main candle containing the Order stop**, inclusive. Lower-TF chronology decides whether stops occurred; it does not truncate either E boundary candle's OHLC. Strict-better replacement retains the earliest equal source.

### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

## Bearish

### 8.1 Parent stop and E-space opening

Every E cycle starts only after the first strict Bearish stop of an accepted S/E parent. For an E parent, a stop search begins at its decision event, so E cannot stop before the Order-stop event that confirmed it. Sequence/StopAll boundaries may later reinterpret parent type, but do not invent a different price event.

### 8.2 Physical Order choices

At each parent stop, E considers physical Orders from these routes: direct parent-stop Order_A, an S-carried unconsumed Order, a gate-owned initial A Order, carried-live accepted identity, post-stop accepted-live identity, and accepted Order_B reset-leg identities. `parent-stop` and `reset-leg` are creation causes; `carried-live` / `accepted-live` are use routes only. A candidate must possess an exact strict Order stop. Winner is earliest stop event; for an exact same stop event the larger Order First index wins (`-FirstIndex` tie key). Sequence reset boundaries may invalidate an Order crossing that would span a hard reset.

E performs this comparison over one complete eligible candidate set spanning all direct, inherited, carried and post-stop accepted routes. No route may reduce to a single candidate before the global `(exact stop event, -FirstIndex)` adjudication. This E-consumption tie rule does not change physical Order creation ordering.

### 8.3 E source and decision

`decision_event = max(parent_stop_event, order_stop_event)`. The E source is the maximum High across the **complete main candle containing the parent stop through the complete main candle containing the Order stop**, inclusive. Lower-TF chronology decides whether stops occurred; it does not truncate either E boundary candle's OHLC. Strict-better replacement retains the earliest equal source.

### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

## Review scope

These are current accepted Reference statements compared with the captured executable owners. They do not establish independent RAW correctness. The current source-scope exclusion applies to additional features present incidentally in exact snapshots.

## Executable selection and provenance

EZoneDetector._zone considers every eligible candidate from direct/reset-leg, inherited unconsumed S, carried-live, and post-stop accepted-live routes. Global selection minimizes (exact Order stop, -FirstIndex). Route-local sorting does not discard tied candidates before this race; exact remaining ties preserve route concatenation order. The S continuous deadline derives from the minimum inherited stop when no carried candidate exists.

Carried accepted E-ledger use requires a creation event strictly between parent decision and stop, confirmation at/before parent stop and physical stop at/after it. Post-stop accepted-live requires confirmation strictly after parent stop and physical stop after both; hard resets veto crossing spans. Initial accepted A-ledger reuse uses inclusive FirstTime bounds. These are use routes, never new creation causes.

An explicit invalid S cannot create a parent-stop cause. Its E continuation/restored root requires independently valid accepted Order provenance; a stopped-A accepted identity can supply that independent cause. Exact simultaneous invalid-A/E stop can admit a canonical E-parent Order whose First belongs to the stop main candle and whose confirmation is strictly after the exact stop; the exception is keyed by (exactStop, FirstTime), applies only to that E parent, and never globally unblocks inherited A/S vetoes.

Main extrema use a run-scoped sparse table preserving earliest equality. Publishing sequence_resets clears candidate, carried, post-stop and direct parent-stop caches. Ledger rebuild/restore maintains both physical rows and chronological confirmation-index tuples.
