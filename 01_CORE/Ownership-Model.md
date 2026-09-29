---
id: "core.ownership"
type: "core"
status: "active"
authority: "executable"
title: "Calculation, acceptance and public ownership"
version: "current"
related_entities: ["algorithm.lifecycle", "algorithm.orderaudit", "algorithm.visibility", "core.identity"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49"]
name: "Ownership"
aliases: ["Behavior ownership"]
---

# Calculation, acceptance and public ownership

## Owning layers

Reaction owns structural First/Break/box/Reset and exact chronology. Geometry-only helpers bypass lifecycle acceptance for bounded evidence,not canonical Orders. Internal marking protects calculation evidence without deleting identity. Blue owns source/line/validity/internal flags; A owns pair trigger/exact confirming source; S owns A-stop route/decision; E owns accepted parent continuation and reconciled family/number.

Physical OrderAudit owns creating causes/immutable identity. parent-stop/reset-leg create; carried-live/accepted-live reuse. A consumer can use another accepted owner's physical identity while retaining original cause. Historical accepted parentage survives visibility; invalid parentage never gains creation rights.

Latest stopped chronology selects current closed transition before same-boundary priority StopAll>E Red>S Red>E Blue>S Blue>A. Strict beyond-boundary source can become consumed leg head. Nonpublic accepted evidence may continue stopped larger E; explicit stage-invalid S cannot manufacture accepted parent provenance.

Final visibility resolves occupancy/referenced lineage; serialization projects it. A missing public label,drawing offset or chart position does not prove absent calculation evidence.
