---
id: "algorithm.e"
type: "algorithm"
status: "active"
authority: "executable"
title: "E physical-Order race and recursive accepted lifecycle"
version: "current"
related_entities: ["algorithm.order", "algorithm.reconciliation", "algorithm.s", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L308", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L749", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L880", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1053", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1179", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1202", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1263", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L476", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L816", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.e_zone_detector", "source.order_audit_engine", "source.lifecycle_engine", "source.reaction_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L177", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L177"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.s", "algorithm.order", "algorithm.orderaudit"]
name: "E"
aliases: ["E Zone", "EZone"]
reference_agreement: "ambiguous"
reference_conflicts: ["REF-E-TIE-SCOPE"]
---

# E physical-Order race and recursive accepted lifecycle

## Bullish

#### 8.1 Parent stop and E-space opening

Every E cycle starts only after the first strict Bullish stop of an accepted S/E parent. For an E parent, a stop search begins at its decision event, so E cannot stop before the Order-stop event that confirmed it. Sequence/StopAll boundaries may later reinterpret parent type, but do not invent a different price event.

#### 8.2 Physical Order choices

At each parent stop, E considers physical Orders from these routes: direct parent-stop Order_A, an S-carried unconsumed Order, carried-live accepted identity, post-stop accepted-live identity, and accepted Order_B reset-leg identities. `parent-stop` and `reset-leg` are creation causes; `carried-live` / `accepted-live` are use routes only. A candidate must possess an exact strict Order stop. Each route first selects its own representative; E's final race uses earliest stop and then larger FirstIndex. A gate-owned initial A Order is a separate nested-candidate exclusion context, not an appended race choice. Sequence reset boundaries may invalidate an Order crossing that would span a hard reset.

#### 8.3 E source and decision

`decision_event = max(parent_stop_event, order_stop_event)`. The E source is the minimum Low across the **complete main candle containing the parent stop through the complete main candle containing the Order stop**, inclusive. Lower-TF chronology decides whether stops occurred; it does not truncate either E boundary candle's OHLC. Strict-better replacement retains the earliest equal source.

#### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

#### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

#### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

## Bearish

#### 8.1 Parent stop and E-space opening

Every E cycle starts only after the first strict Bearish stop of an accepted S/E parent. For an E parent, a stop search begins at its decision event, so E cannot stop before the Order-stop event that confirmed it. Sequence/StopAll boundaries may later reinterpret parent type, but do not invent a different price event.

#### 8.2 Physical Order choices

At each parent stop, E considers physical Orders from these routes: direct parent-stop Order_A, an S-carried unconsumed Order, carried-live accepted identity, post-stop accepted-live identity, and accepted Order_B reset-leg identities. `parent-stop` and `reset-leg` are creation causes; `carried-live` / `accepted-live` are use routes only. A candidate must possess an exact strict Order stop. Each route first selects its own representative; E's final race uses earliest stop and then larger FirstIndex. A gate-owned initial A Order is a separate nested-candidate exclusion context, not an appended race choice. Sequence reset boundaries may invalidate an Order crossing that would span a hard reset.

#### 8.3 E source and decision

`decision_event = max(parent_stop_event, order_stop_event)`. The E source is the maximum High across the **complete main candle containing the parent stop through the complete main candle containing the Order stop**, inclusive. Lower-TF chronology decides whether stops occurred; it does not truncate either E boundary candle's OHLC. Strict-better replacement retains the earliest equal source.

#### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

#### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

#### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

## Source-level contract

Parent strict stop searches from parent.decision_event_time inclusive. Carried Orders must stop >= parent stop; post-stop accepted-live requires confirmation > parent stop and stop > both parent stop and confirmation. Final route representatives race by exact Order stop then larger FirstIndex; route-local ranks differ. E decision=max(parent stop,Order stop), source full containing parent-stop..decision main candles, earliest equal extreme.

Every stopped S discovers provisional E1 and recursive children; repeated physical source terminates chain. Chronological acceptance resolves active lineage, same-source behavioral priority and family/number. Stopped accepted Red inheritance can advance Red even for provisional Blue input.

Consumed nonpublic S continuation inherits stopped larger E family,next number and rebuilds children natively. Replacement must decide earlier than existing child; equal decision retains accepted branch. Independent accepted-S roots cannot restore a source already occupied by accepted E. All accepted branch replacement/root restoration synchronizes canonical OrderAudit before serialization.

Publishing sequence_resets atomically copies its map, refreshes sorted reset times and clears dependent candidate/carried context caches once. Immutable physical stop/cross caches and historical accepted Order_A causes remain retained. The reset lookup window is (start,end]. Explicit invalid S identities are rejected at parent registration and reconstructed parent-stop cause retention; valid historical S and shared Order_B reset-leg provenance remain eligible.


## Route-local representatives and final tie scope

E selects one representative from each eligible use route before the final race. The direct/reset-leg candidate route sorts by exact physical stop event and then ascending physical FirstTime; `_first_order` returns its first stopped candidate. Carried accepted Orders sort by stop event and descending FirstIndex. Post-stop accepted Orders sort by stop event, confirmation time, then descending FirstIndex. Blue-S inherited unconsumed Order is a singleton. `_zone` races those representatives by stop event and descending FirstIndex; exact remaining ties retain route-list order. The larger-FirstIndex rule therefore applies to the final representative race, not unconditionally to every underlying candidate before route-local selection.


## Inherited and carried live Order gates

An inherited unconsumed S Order is eligible only for Blue S with physical Order confirmation and stop fields, and its exact physical stop must occur at or after the S parent stop. In accepted E-ledger carried reuse, at least one original creation event must lie strictly between the parent's decision event and strict stop; confirmation must be at or before parent stop and the physical Order stop at or after it. A parent-stop Order uses its earliest creating stop as its creation event; each Order_B cause uses physical Order confirmation. Initial accepted A-ledger reuse instead uses an inclusive FirstTime interval from parent decision through parent stop, with the same confirmation<=stop and physical crossing>=stop gates. These are use routes and preserve the creator's physical identity and provenance.


## Direct and gate-owned arbitration

Direct parent-stop selection considers canonical independent opposite Reactions whose First main time is at or after the parent-stop main-candle start, while blocked First times apply at that exact gate candle. Bounded direct geometry restarts when the previously active opposite Reaction resets after search start and at or before candidate confirmation; geometry can return a physical Order only after canonical First/Break membership replaces it with the canonical object/number/confirmation. A fresh trend-leg alternative additionally requires trend First after parent stop, a noninternal trend, an explicit continue gate, and opposite First strictly after trend confirmation. Bounded geometry is preferred when a continuous deadline exists, the returned canonical geometry carries restart, and that deadline is range_end or is strictly before its confirmation. Otherwise bounded geometry wins only when the independent candidate has no strict stop and the bounded candidate's FirstTime precedes the independent FirstTime, or there is no independent candidate. Otherwise the independent candidate is used. A gate-owned initial A Order has FirstTime equal to the parent-stop main start, confirmation>=parent stop, and physical stop>=parent stop. The lookup is an acceptance exclusion rather than a separate item appended to the final E race: its confirmation strictly before a parent-stop zone's Order FirstTime blocks that nested direct candidate. Equality does not satisfy this exclusion.


## Chronological accepted-parent gates

Chronological reconciliation admits an S-root candidate only when its physical S parent exists. After a sequence reset, parent S source must be strictly after the sequence start and its A source may not precede that start. In a prior accepted E context, S may establish a root when rebuilt S source is later than prior E source and A source is at or after that E source, or under the explicit still-unconsumed Red-S versus nested Blue-E condition. E-parent lineage must remain active or be the hard boundary gate. A new candidate stops an active owner only with strictly later decision and strictly beyond directional price; price or decision equality leaves the owner active. Native active E continuation protects ownership against lower-priority S-root alternatives. Same-source choice uses parent behavioral priority before exact decision and parent-stop chronology; final family/number derives from stopped accepted active family, never a blanket color inverse.
