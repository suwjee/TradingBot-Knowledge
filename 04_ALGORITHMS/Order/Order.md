---
id: "algorithm.order"
type: "algorithm"
status: "active"
authority: "executable"
title: "Physical Orders, causes and consumption"
version: "current"
related_entities: ["algorithm.order.a", "algorithm.order.b", "algorithm.orderaudit"]
source_reference: ["06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/core_utils.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.order_audit_engine", "source.reaction_engine", "source.e_zone_detector", "source.s_zone_detector", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L259", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L259"]
mirror_links: ["mirror.contract"]
name: "Order"
aliases: ["Physical Order", "Orders"]
---

# Physical Orders, causes and consumption

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

Order is canonical opposite-direction Reaction plus First/Break identity,physical box sources,confirmation and canonical stop/source/hit. Parent label/family is provenance; multiple valid parent-stop/reset-leg causes share identity. Current creation routes are parent-stop and reset-leg; carried-live/accepted-live only consume.

One stopped A owns immutable first physical Order. E or shared S may use another accepted creator's identity under its own exact gates without changing original cause. Noncanonical geometry cannot become physical Order_A/Order_B; equality does not satisfy physical strict price stop.
