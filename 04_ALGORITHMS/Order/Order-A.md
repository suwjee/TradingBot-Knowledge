---
id: "algorithm.order.a"
type: "algorithm"
status: "active"
authority: "executable"
title: "Order_A canonical accepted parent-stop creation"
version: "current"
related_entities: ["algorithm.order", "algorithm.orderaudit"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1313", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1758", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1892", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.order_audit_engine", "source.reaction_engine", "source.s_zone_detector", "source.e_zone_detector", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L203", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L203"]
mirror_links: ["mirror.contract"]
name: "Order_A"
aliases: ["Order A", "Parent-stop Order"]
---

# Order_A canonical accepted parent-stop creation

## Bullish

#### 9.1 Creation gate

Order_A is the physical `parent-stop` route opened by an accepted strict behavior stop. A bounded/direct geometry candidate may create Order_A **only** when its `(FirstIndex, BreakIndex)` exists in the canonical opposite-direction (Bearish) Reaction stream. Geometry absent from that canonical registry remains internal evidence and cannot enter OrderAudit as Order_A or receive a synthetic reaction number.

After a stopped A, the first canonical opposite Order is immutable for that A. For S/E parent stops, direct bounded geometry may be evaluated, but canonical membership remains mandatory. One exact parent-stop cause may own at most one physical Order_A; when multiple candidates compete, earliest canonical confirmation, then FirstIndex, then BreakIndex owns the cause.

#### 9.2 Canonical stop

Order stop provenance comes from `MarketChronology.canonical_order_stop`. For Mode A it uses the canonical leg-head/floor context required by that opposite Reaction; for Mode B it uses the previous healthy opposite Reaction's outer edge under the established chronology. The Order's exact strict stop uses the **opposite direction** predicate; for this Bullish calculation that is `High > OrderStop`. Equality does not stop an Order.

#### 9.3 Parent validity and retention

An S explicitly identified in invalid_s_root_identities is calculation evidence, not an accepted S parent, and cannot create or retain a `parent-stop` Order_A cause. Once a valid canonical Order_A enters the identity-keyed ledger, later E/lifecycle reconciliation may change who uses it but cannot delete that physical identity/provenance. A shared Order_B identity may add reset-leg provenance without erasing valid parent-stop provenance.

## Bearish

#### 9.1 Creation gate

Order_A is the physical `parent-stop` route opened by an accepted strict behavior stop. A bounded/direct geometry candidate may create Order_A **only** when its `(FirstIndex, BreakIndex)` exists in the canonical opposite-direction (Bullish) Reaction stream. Geometry absent from that canonical registry remains internal evidence and cannot enter OrderAudit as Order_A or receive a synthetic reaction number.

After a stopped A, the first canonical opposite Order is immutable for that A. For S/E parent stops, direct bounded geometry may be evaluated, but canonical membership remains mandatory. One exact parent-stop cause may own at most one physical Order_A; when multiple candidates compete, earliest canonical confirmation, then FirstIndex, then BreakIndex owns the cause.

#### 9.2 Canonical stop

Order stop provenance comes from `MarketChronology.canonical_order_stop`. For Mode A it uses the canonical leg-head/floor context required by that opposite Reaction; for Mode B it uses the previous healthy opposite Reaction's outer edge under the established chronology. The Order's exact strict stop uses the **opposite direction** predicate; for this Bearish calculation that is `Low < OrderStop`. Equality does not stop an Order.

#### 9.3 Parent validity and retention

An S explicitly identified in invalid_s_root_identities is calculation evidence, not an accepted S parent, and cannot create or retain a `parent-stop` Order_A cause. Once a valid canonical Order_A enters the identity-keyed ledger, later E/lifecycle reconciliation may change who uses it but cannot delete that physical identity/provenance. A shared Order_B identity may add reset-leg provenance without erasing valid parent-stop provenance.

## Source-level contract

Mode-A physical Bearish Order stop scans maximum High from anchor or First-1 through Break inclusive and extends backward over contiguous GREEN; physical Bullish mirrors minimum Low and RED. Strict improvement keeps earliest source. Mode B uses preceding healthy canonical BoxTop Bearish/BoxBottom Bullish; number <=1 raises.

S first physical Order confirms strictly after A stop and First index >= stop-main index. Bounded direct/trend-leg geometry must map to canonical identity,Reaction and number. Exact parent cause has one physical owner by confirmation,First,Break. Explicit invalid S has no parent-stop rights; accepted historical nonpublic provenance remains. accepted_audit_entry selects first accepted A cause for E without deleting complete cause list.

Publishing sequence_resets atomically copies its map, refreshes sorted reset times and clears dependent candidate/carried context caches once. Immutable physical stop/cross caches and historical accepted Order_A causes remain retained. The reset lookup window is (start,end]. Explicit invalid S identities are rejected at parent registration and reconstructed parent-stop cause retention; valid historical S and shared Order_B reset-leg provenance remain eligible.


## Continuous gate and bounded geometry selectors

The overlapping direct-geometry helper selects the earliest confirming main candle. If multiple healthy candidates confirm in that main, current Source chooses the smallest First index. It does not compare their exact lower confirmation times for this tie. This geometry selection remains separate from downstream exact physical Order/cause ranking and canonical membership gates.

Continuous Order gate geometry uses canonical context confirmed no later than the gate, with exact same-main confirmation eligibility. Without canonical history it chooses healthy bounded geometry and tags no-history. With an owner, strict outer-boundary restart races strict gate-boundary continuation from the exact gate; restart owns a true lower-position tie. Restart begins geometry after the decision main; continuation begins after the gate main. Existing anchor is preserved, with prior-Reset reconstruction only when absent. The separate bounded structural wrapper has a main-index/end cache and ignores its gate_event argument; it is not the continuous exact-gate selector. All returned geometry still requires canonical physical membership before Order_A acceptance.
