---
id: "behavior.s"
type: "behavior"
status: "active"
authority: "executable"
title: "S accepted behavior taxonomy"
version: "current"
related_entities: ["algorithm.s", "behavior.s.blue", "behavior.s.red", "core.behavior_model"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.s_zone_detector", "source.lifecycle_engine", "source.e_zone_detector", "source.order_audit_engine"]
---

# S accepted behavior taxonomy

S opens from accepted A's first strict stop. Native formation_type=simple,advanced,type3,type4. Native Simple/Advanced are physical-Order-backed and Red/Blue;native Type-3/Type-4 are order-free Blue. Exact route selection,later shared accepted-Order recoloring and final ownership are separate.

S retains A source/price/stop,candidate source/price and exact decision. Native optional Order/Reset fields remain null when absent. Shared reconciliation can decide Red using accepted physical identity while preserving original subtype/source and creating cause. Stopped accepted S can open E;explicit invalid S has no accepted parent-stop Order_A rights.
