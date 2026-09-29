---
id: "algorithm.orderaudit"
type: "algorithm"
status: "active"
authority: "executable"
title: "First-class physical OrderAudit ledger"
version: "current"
related_entities: ["algorithm.order", "algorithm.order.a", "algorithm.order.b", "algorithm.serialization"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1578", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
implemented_by: ["source.order_audit_engine", "source.trading_pipeline", "source.e_zone_detector", "source.s_zone_detector", "source.lifecycle_engine", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L259", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L259"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.reaction"]
name: "OrderAudit"
aliases: ["Order Audit"]
---

# First-class physical OrderAudit ledger

## Bullish

### 11. Order / OrderAudit architecture

1. The identity-keyed Order ledger is canonical; parent labels are provenance, not identity.
2. Creation causes are exactly `parent-stop` (Order_A) and `reset-leg` (Order_B). `carried-live` and `accepted-live` are consumption/use routes.
3. One exact parent-stop event has one physical Order_A owner. Cause deduplication ranks by confirmation, FirstIndex, BreakIndex.
4. `prepare_order_audit` merges S-stage and E-stage accepted ledgers, retains identities outside the presentation range when required by a visible behavior, deduplicates causes, and computes a strict stop only when it was not already authoritative.
5. `accepted_audit_entry` filters an A-owned identity to accepted A provenance without discarding the complete physical cause set used for presentation.
6. OrderAudit must not fabricate parentage: invalid/suppressed parents lose creation rights; valid historical parent-stop provenance survives later consumer reconciliation.
7. The active physical Order routes are Order_A and Order_B.

## Bearish

### 11. Order / OrderAudit architecture

1. The identity-keyed Order ledger is canonical; parent labels are provenance, not identity.
2. Creation causes are exactly `parent-stop` (Order_A) and `reset-leg` (Order_B). `carried-live` and `accepted-live` are consumption/use routes.
3. One exact parent-stop event has one physical Order_A owner. Cause deduplication ranks by confirmation, FirstIndex, BreakIndex.
4. `prepare_order_audit` merges S-stage and E-stage accepted ledgers, retains identities outside the presentation range when required by a visible behavior, deduplicates causes, and computes a strict stop only when it was not already authoritative.
5. `accepted_audit_entry` filters an A-owned identity to accepted A provenance without discarding the complete physical cause set used for presentation.
6. OrderAudit must not fabricate parentage: invalid/suppressed parents lose creation rights; valid historical parent-stop provenance survives later consumer reconciliation.
7. The active physical Order routes are Order_A and Order_B.

## Source-level contract

order_audit_engine.py owns physical discovery,canonical stop,identity registration,cause merging/reuse,accepted rebuild and preparation. S mixin records stopped-A first Order; E mixin maintains accepted S/E/StopAll/reset-leg ledger. Entry retains canonical Reaction/number,confirmation,stop level/source,authoritative optional stop_cross and creation causes.

Live means accepted physical Order not stopped before consuming gate; acceptance means valid creating provenance entered calculation. Rebuild rejects explicit invalid S parent-stop causes but preserves valid historical parent-stop identity. Reset cause separately records stop owner and geometric anchor.

prepare_order_audit merges accepted S/E by physical identity, retains required out-of-range Order, merges distinct causes and computes stop only if stop_cross key absent. Authoritative null remains null. Parent cause key is parentType,parentFamily,eventTime,parentSourceTime,owner rank confirmation,First,Break.

Public OrderAudit includes original physical mode/number/First/Break/boxes/stop sources,nullable hit fields and causes. parent-stop contains kind,parentType,parentFamily,eventTime,parentSourceTime. reset-leg contains post behavior,anchor,reset Reaction identity/confirmation,Reset index/level/time,boundary/source,strict break and final physical identity/confirmation. Current identity/cause joins never substitute row position.

Publishing sequence_resets atomically copies its map, refreshes sorted reset times and clears dependent candidate/carried context caches once. Immutable physical stop/cross caches and historical accepted Order_A causes remain retained. The reset lookup window is (start,end]. Explicit invalid S identities are rejected at parent registration and reconstructed parent-stop cause retention; valid historical S and shared Order_B reset-leg provenance remain eligible.


## Preparation entry ownership and exact null semantics

Preparation visits accepted S-stage A entries before E-stage entries. For a physical identity already inserted, later entries merge distinct creating causes only; they do not replace the first entry's canonical Reaction/stop metadata or prepared crossing. A present stop_cross key is authoritative even when None; only a missing key triggers physical-cross lookup. Then exact parent-stop cause owners are chosen by confirmation, FirstIndex, BreakIndex, while independent reset-leg causes remain. Output preparation order is subsequently projected to serializer FirstTime/BreakTime ordering.
