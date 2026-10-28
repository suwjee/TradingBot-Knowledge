---
id: "algorithm.order.a"
type: "algorithm"
status: "active"
authority: "executable"
title: "Order_A canonical accepted parent-stop creation"
version: "current"
related_entities: ["algorithm.order", "algorithm.orderaudit"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1316", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1768", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1917", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.order_audit_engine", "source.reaction_engine", "source.s_zone_detector", "source.e_zone_detector", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L299", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L299"]
mirror_links: ["mirror.contract"]
name: "Order_A"
aliases: ["Order A", "Parent-stop Order"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Order_A canonical accepted parent-stop creation

## Bullish

### 9.1 Creation gate

Order_A is the physical `parent-stop` route opened by an accepted strict behavior stop. Ordinarily a bounded/direct Order candidate must match a canonical opposite-direction (Bearish) Reaction identity `(FirstIndex, BreakIndex)`. **Approved 5.4.30 exception:** after an accepted A stop, independently confirmed complete physical opposite Order geometry may enter S OrderAudit even when it is absent from the public opposite Reaction stream. It receives `reactionNumber=0`, not a synthetic canonical Reaction, and retains its real physical First/Break identity and exact confirmation. An incomplete, unconfirmed, or otherwise invalid geometry cannot enter the accepted audit.

After a stopped A, the first eligible physically confirmed opposite Order is immutable for that A. For S/E parent stops, direct bounded geometry may be evaluated subject to the existing canonical acceptance contract. One exact parent-stop cause may own at most one physical Order_A; when multiple candidates compete, earliest canonical confirmation, then FirstIndex, then BreakIndex owns the cause.

For an A parent, “accepted” means the A survives S ownership and current invalid-A lifecycle filtering into the finalized A behavior set. A provisional/detected A that is S-owned, consumed, filtered or invalid cannot open an A-owned Order_A and cannot be retained as an A `parent-stop` cause in the final OrderAudit. Other independently valid creation causes on the same physical Order identity remain valid.

A shared accepted physical Order stop that changes S Blue to S Red must preserve its opposite `order_direction`, identity, First/Break, confirmation, and exact stop provenance.

### 9.2 Canonical stop

Order stop provenance comes from `MarketChronology.canonical_order_stop`. For Mode A it uses the canonical leg-head/floor context required by that opposite Reaction; for Mode B it uses the previous healthy opposite Reaction's outer edge under the established chronology. The Order's exact strict stop uses the **opposite direction** predicate; for this Bullish calculation that is `High > OrderStop`. Equality does not stop an Order.

### 9.3 Parent validity and retention

An S explicitly identified in invalid_s_root_identities is calculation evidence, not an accepted S parent, and cannot create or retain a `parent-stop` Order_A cause. An E derived from that S may be accepted only when its chosen physical Order has a valid creating cause independent of the invalid S. This applies to ordinary chain reconciliation, consumed-S continuation, and independent-root restoration; provisional geometry alone cannot publish an E or StopAll. Once a valid canonical Order_A enters the identity-keyed ledger, later E/lifecycle reconciliation may change who uses it but cannot delete that physical identity/provenance. A shared Order_B identity may add reset-leg provenance without erasing valid parent-stop provenance.

The same acceptance rule applies during every OrderAudit rebuild/reconciliation pass: nonaccepted A causes are removed before a physical identity is retained on A provenance. This prevents a provisional A cause from being reintroduced after downstream E reconciliation while preserving independent valid S/E or reset-leg provenance for the same physical Order.

## Bearish

### 9.1 Creation gate

Order_A is the physical `parent-stop` route opened by an accepted strict behavior stop. Ordinarily a bounded/direct Order candidate must match a canonical opposite-direction (Bullish) Reaction identity `(FirstIndex, BreakIndex)`. **Approved 5.4.30 exception:** after an accepted A stop, independently confirmed complete physical opposite Order geometry may enter S OrderAudit even when it is absent from the public opposite Reaction stream. It receives `reactionNumber=0`, not a synthetic canonical Reaction, and retains its real physical First/Break identity and exact confirmation. An incomplete, unconfirmed, or otherwise invalid geometry cannot enter the accepted audit.

After a stopped A, the first eligible physically confirmed opposite Order is immutable for that A. For S/E parent stops, direct bounded geometry may be evaluated subject to the existing canonical acceptance contract. One exact parent-stop cause may own at most one physical Order_A; when multiple candidates compete, earliest canonical confirmation, then FirstIndex, then BreakIndex owns the cause.

For an A parent, “accepted” means the A survives S ownership and current invalid-A lifecycle filtering into the finalized A behavior set. A provisional/detected A that is S-owned, consumed, filtered or invalid cannot open an A-owned Order_A and cannot be retained as an A `parent-stop` cause in the final OrderAudit. Other independently valid creation causes on the same physical Order identity remain valid.

A shared accepted physical Order stop that changes S Blue to S Red must preserve its opposite `order_direction`, identity, First/Break, confirmation, and exact stop provenance.

### 9.2 Canonical stop

Order stop provenance comes from `MarketChronology.canonical_order_stop`. For Mode A it uses the canonical leg-head/floor context required by that opposite Reaction; for Mode B it uses the previous healthy opposite Reaction's outer edge under the established chronology. The Order's exact strict stop uses the **opposite direction** predicate; for this Bearish calculation that is `Low < OrderStop`. Equality does not stop an Order.

### 9.3 Parent validity and retention

An S explicitly identified in invalid_s_root_identities is calculation evidence, not an accepted S parent, and cannot create or retain a `parent-stop` Order_A cause. An E derived from that S may be accepted only when its chosen physical Order has a valid creating cause independent of the invalid S. This applies to ordinary chain reconciliation, consumed-S continuation, and independent-root restoration; provisional geometry alone cannot publish an E or StopAll. Once a valid canonical Order_A enters the identity-keyed ledger, later E/lifecycle reconciliation may change who uses it but cannot delete that physical identity/provenance. A shared Order_B identity may add reset-leg provenance without erasing valid parent-stop provenance.

The same acceptance rule applies during every OrderAudit rebuild/reconciliation pass: nonaccepted A causes are removed before a physical identity is retained on A provenance. This prevents a provisional A cause from being reintroduced after downstream E reconciliation while preserving independent valid S/E or reset-leg provenance for the same physical Order.

## Review scope

These are current accepted Reference statements compared with the captured executable owners. They do not establish independent RAW correctness. The current source-scope exclusion applies to additional features present incidentally in exact snapshots.

## Executable accepted-A gate

S detects physical A-stop candidates independently, then accepted_audit_entry/accepted_audit_entries remove A causes outside the calculation-eligible A set. The bridge reapplies this filter after S ownership, lifecycle invalidity and before final preparation. Every independent valid cause on the same physical identity survives. A complete post-stop independent geometry can receive reactionNumber=0 only for the accepted stopped-A Order_A route; this exception does not authorize geometry-only Order_B.
