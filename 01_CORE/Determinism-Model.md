---
id: "core.determinism"
type: "core"
status: "active"
authority: "executable"
title: "Deterministic event, source and ledger selection"
version: "current"
related_entities: ["core.identity", "core.invariants", "mirror.validation_rules", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/core_utils.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
reference_agreement: "match"
reference_conflicts: []
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Deterministic event, source and ledger selection

## Numeric and temporal state

Decimal inputs and immutable original market color precede calculations. Shared timestamps/indexes apply explicit strict comparator/window. Time never reflects. Index/cache optimization must preserve first event,tie ownership and underlying physical identity.

## Rule-specific ties

Reaction/A/E and Order_B normally replace only strict-better extrema,earliest equal source. S Type-3/Type-4/after-Order Simple choose last equal main source. Mode-A invalidation/Reset wins same lower-position confirmation ties. S candidate/Order stop same-position tie makes no native decision. Blue includes the exact confirmation row and never consumes later rows; shared S reconciliation includes source main-time equality. Order_B admits First in the strict-break calculation candle, while confirmation must be strictly after the exact crossing.

## Acceptance ties

Parent-stop physical owner ranks confirmation/First/Break. E globally races every eligible route candidate by exact stop then larger FirstIndex; route-local sorts do not reduce the candidate set before adjudication. Same-source E Red beats Blue,then larger same-family number,then prior accepted object. Latest stopped lifecycle boundary precedes priority/number/source ties. Order_B exact immutable cause identity must stabilize within eight passes or raise.

## Projection evidence

Stable ordering/nulls/cause joins come from accepted state. Runtime timings are not deterministic trading values. No actual repeated runtime/market output equality is claimed by this note; synthetic boundary probes,mirror parity and independent target real-data evidence are separate scopes.

Publishing sequence_resets atomically copies its map, refreshes sorted reset times and clears dependent candidate/carried context caches once. Immutable physical stop/cross caches and historical accepted Order_A causes remain retained. The reset lookup window is (start,end]. Explicit invalid S identities are rejected at parent registration and reconstructed parent-stop cause retention; valid historical S and shared Order_B reset-leg provenance remain eligible.
