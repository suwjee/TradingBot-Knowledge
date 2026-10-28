---
id: "algorithm.reconciliation"
type: "algorithm"
status: "active"
authority: "executable"
title: "Accepted E, S and physical Order reconciliation"
version: "current"
related_entities: ["algorithm.e", "algorithm.orderaudit", "algorithm.s", "algorithm.stopall"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L2149", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L2226", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L2591", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L984", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L1006", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L929", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
implemented_by: ["source.e_zone_detector", "source.s_zone_detector", "source.order_audit_engine", "source.lifecycle_engine", "source.trading_pipeline"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L287", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L287"]
mirror_links: ["mirror.contract"]
name: "Reconciliation"
aliases: ["Accepted-state reconciliation"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Accepted E, S and physical Order reconciliation

## Bullish

#### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

#### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

#### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets the single exact dominant owner, its count and pending completed stop. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

## Bearish

#### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

#### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

#### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets the single exact dominant owner, its count and pending completed stop. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

## Source-level contract

Bridge calculates initial S/E,filters S eligibility,resolves A-cycle invalidity/accepted Order context,then final E. Changed earlier shared Order-stop S decision rebuilds E. Consumed S continuation replaces only later descendants; accepted ledger rebuild follows.

Same-source E chooses Red,then greater same-family number,then earlier accepted object/provenance. Stopped E leaves active but remains history. Independent accepted-S E1 restoration occurs after hard StopAll with audit synchronization retaining canonical history Orders. Same-source E prevents competing provisional S root.

Order_B feedback compares the complete exact reset-leg identity after each dependent calculation pass, with at most eight passes. Every lifecycle-enabled feedback pass invokes a fresh StopAll reconciliation over that pass's accepted S/E state for accepted reset-leg discovery; final visibility invokes reconciliation again after convergence. Each **reconciliation call** makes one source-order StopAll pass and publishes its sequence-reset map without rebuilding that call's E prefix from future reset state. Reaction, Blue, A and initial S remain shared across feedback passes. Repeated changed cause identity, exhaustion of eight passes or a final cause identity differing from the converged detector identity raises an error.


## Consumed S Close gates and selected owner

Consumed-S continuation is evaluated separately from public S visibility. A candidate already accepted under `(a_source_time, source_time)` is excluded. Its owning E must have formed strictly before the candidate's parent A source, must have strictly stopped before that A source, and must have higher lifecycle priority than the S. The price gate compares the S source main-candle **Close** with the owning E stop main-candle **Close**, not the S extreme or E behavior price: Bullish requires `sourceClose < stopClose`; Bearish requires `sourceClose > stopClose`; equality does not qualify.

The latest accepted E source strictly before A source marks current lineage. That E can qualify directly. An older E can qualify only when `(priority, number)` is strictly larger than the latest source's rank, its exact stop is strictly later than the latest source's decision, and, when the latest source also qualifies, its stop main index is no earlier. Among the remaining owners, choose greatest `(stopMainIndex, priority, number, sourceTime, sourceIndex)`. For each owner retain the earliest suppressed S by `(sourceTime, sourceIndex)`.

The bridge excludes S descendants rejected specifically by S-stage A ownership before this continuation selection. It resolves the chosen owner against current E physical source identity, obtains the native continuation chain, replaces only descendants later than that earlier chain, then rebuilds the accepted OrderAudit ledger from the actual final E list and supplemental consumed S evidence. Public-label suppression and explicit calculation invalidity therefore remain different states.

## Current lifecycle and ledger corrections

The StopAll owner/count/direct-S/causal-E rules are maintained in algorithm.stopall. The old independent Blue repetition ledger is superseded. Lifecycle enablement is explicit and identical in feedback/final visibility. Before final hard boundaries, the bridge supplements only absent accepted independent S-root E physical sources; an existing source keeps its prior candidate and Order provenance. Final root visibility restoration and audit synchronization remain afterward. Invalid S continuation/restoration requires an independent accepted physical creating cause. Ledger restoration includes its chronological confirmation-index tuple.
