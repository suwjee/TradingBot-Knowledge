---
id: "behavior.s.red"
type: "behavior"
status: "active"
authority: "executable"
title: "S Red physical Order-stop decision"
version: "current"
related_entities: ["algorithm.s", "algorithm.stopall.blue_reversal", "core.priority"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.s_zone_detector", "source.order_audit_engine", "source.lifecycle_engine"]
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# S Red physical Order-stop decision

S Red is native family selected when exact strict opposite Order stop wins before qualified candidate cross. Same lower-position tie yields no native decision. Native Red recomputes complete Order Break..Red decision directional source except accepted authoritative pre-Order geometry.

Shared accepted-Order stop may recolor any native S subtype while frozen source/price/subtype persist. Its window includes source main-time equality and excludes current decision equality. Physical confirmation must be strictly earlier than stop. Original accepted creation cause remains parent-neutral.

Red outranks Blue S/Blue E through lifecycle gates. An accepted S Red may directly donate StopAll1 after a currently dominant armed Blue owner in either Order mode. A separate completed-stop fallback remains Mode-B-only; see algorithm.stopall.blue_reversal.
