---
id: "algorithm.orderaudit"
type: "algorithm"
status: "active"
authority: "executable"
title: "First-class physical OrderAudit ledger"
version: "current"
related_entities: ["algorithm.order", "algorithm.order.a", "algorithm.order.b", "algorithm.serialization"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1928", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L1948"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
implemented_by: ["source.order_audit_engine", "source.trading_pipeline", "source.e_zone_detector", "source.s_zone_detector", "source.lifecycle_engine", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L363", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L363"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.reaction"]
name: "OrderAudit"
aliases: ["Order Audit"]
last_modified_at: "2026-10-28T18:07:57+03:30"
---
# First-class physical OrderAudit ledger

## Bullish

## 11. Order / OrderAudit architecture

1. The identity-keyed Order ledger is canonical; parent labels are provenance, not identity.
2. Creation causes are exactly `parent-stop` (Order_A) and `reset-leg` (Order_B). `carried-live` and `accepted-live` are consumption/use routes.
3. One exact parent-stop event has one physical Order_A owner. Cause deduplication ranks by confirmation, FirstIndex, BreakIndex.
4. `prepare_order_audit` merges S-stage and E-stage accepted ledgers, retains identities outside the presentation range when required by a visible behavior, deduplicates causes, and computes a strict stop only when it was not already authoritative.
5. `accepted_audit_entry` filters an A-owned identity to accepted A provenance without discarding the complete physical cause set used for presentation.
6. OrderAudit must not fabricate parentage: invalid/suppressed parents lose creation rights; valid historical parent-stop provenance survives later consumer reconciliation.
7. The active physical Order routes are Order_A and Order_B.

## Bearish

## 11. Order / OrderAudit architecture

1. The identity-keyed Order ledger is canonical; parent labels are provenance, not identity.
2. Creation causes are exactly `parent-stop` (Order_A) and `reset-leg` (Order_B). `carried-live` and `accepted-live` are consumption/use routes.
3. One exact parent-stop event has one physical Order_A owner. Cause deduplication ranks by confirmation, FirstIndex, BreakIndex.
4. `prepare_order_audit` merges S-stage and E-stage accepted ledgers, retains identities outside the presentation range when required by a visible behavior, deduplicates causes, and computes a strict stop only when it was not already authoritative.
5. `accepted_audit_entry` filters an A-owned identity to accepted A provenance without discarding the complete physical cause set used for presentation.
6. OrderAudit must not fabricate parentage: invalid/suppressed parents lose creation rights; valid historical parent-stop provenance survives later consumer reconciliation.
7. The active physical Order routes are Order_A and Order_B.

## Review scope

These are current accepted Reference statements compared with the captured executable owners. They do not establish independent RAW correctness. The current source-scope exclusion applies to additional features present incidentally in exact snapshots.

## Ledger and index integrity

Physical First/Break keys and independent creation causes survive consumer changes. prepare_order_audit collects only accepted A parent-stop causes from both S and E ledgers, merges physical identities, preserves required out-of-range identities and chooses one owner per exact parent-stop cause by confirmation/First/Break. accepted_audit_entry filters its a_causes list as well as selected A fields. ensure_accepted_order_audit restores each retained ledger row together with its chronological confirmation-index tuple. Cause changes invalidate carried-use caches; new identity indexes alter post-stop query keys. This is structural and Source evidence, not a fresh market replay.
