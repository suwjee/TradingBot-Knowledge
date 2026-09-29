---
id: "core.pipeline"
type: "core"
status: "active"
authority: "executable"
title: "Current full calculation pipeline"
version: "current"
related_entities: ["algorithm.orderaudit", "algorithm.raw", "algorithm.reaction", "algorithm.reconciliation", "algorithm.serialization", "algorithm.visibility"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/core_utils.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L37", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L37"]
name: "Pipeline"
aliases: ["Trading pipeline"]
---

# Current full calculation pipeline

## Stage contract

RAW normalization -> required Reaction/Reset directions -> cross-direction internal ownership -> Blue -> A -> initial S -> E discovery/reconciliation -> S/A lifecycle and accepted Order context -> final E -> shared accepted-Order S decision reconciliation and E rebuild when changed -> consumed-S native E continuation -> accepted OrderAudit rebuild -> converged Order_B feedback -> one-pass hard StopAll -> independent accepted-S root restoration/audit synchronization -> final visibility -> OrderAudit preparation -> serialization.

Behavior enablement can require both Reaction directions even for one output direction. Full E context is reused when E loaded and S enabled. Reaction,Blue,A,initial S are Order_B-independent and shared across feedback passes. Dependent accepted state recalculates while exact reset-leg causes change; repeat changed identity or eighth-pass failure raises. Final causes must match converged identity.

Complete supplied input calculates before presentation indexes against epoch-aligned main buckets. Both directions share MarketChronology and lower indexes. Clipping a view does not restart a detector at from-time.

## Owning modules

Reaction/Reset/internal: reaction_engine.py. Blue: blue_line_detector.py. A: a_zone_detector.py. S: s_zone_detector.py. E: e_zone_detector.py. Physical Orders/provenance: order_audit_engine.py. Lifecycle/StopAll/visibility: lifecycle_engine.py. Decimal/identity: core_utils.py. Price direction: direction_policy.py. Input/orchestration/public projection: trading_pipeline.py.

Selected-range HTTP requests supply only inclusive chart-candle buckets through an in-memory stream. Such a calculation starts with empty state at its supplied start; the bridge cannot use omitted rows. Presentation bounds within a complete supplied input are a separate operation.
