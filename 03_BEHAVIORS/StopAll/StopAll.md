---
id: "behavior.stopall"
type: "behavior"
status: "canonical"
authority: "normative"
title: "StopAll"
calculated_by: ["algorithm.stopall"]
implemented_by: ["source.lifecycle_engine"]
depends_on: ["behavior.e", "behavior.s"]
parent_of: ["behavior.stopall.type1", "behavior.stopall.type2", "behavior.stopall.type3"]
source_refs: ["engine/pipeline/lifecycle_engine.py#L39", "engine/bridge/trading_pipeline.py#L1285"]
related_entities: ["test.lifecycle_invariants"]
source_reference: ["engine/pipeline/lifecycle_engine.py#L39", "engine/bridge/trading_pipeline.py#L1285"]
---

# StopAll

StopAll is the highest behavior and a hard lifecycle boundary. The detector has three gate_type mechanisms; the bridge exposes them as Type-1 sequence-group-stop, Type-2 stopall-stop, and Type-3 opposite-s-group-stop. A StopAll has source/decision, gate event, stopped-group metadata, donor provenance, optional Order, own strict stop, and number. Gate metadata and constructor donor are distinct.

Type-1 and Type-3 begin StopAll1; Type-2 advances to one above the highest active StopAll it strictly stops. A formed StopAll clears active S/E owner keys and pending Blue-repeat counters. Its own stop is the first strict trend-direction crossing after its decision. Final same-source occupancy suppresses lower behaviors. Direction mirrors price crossing, not gate semantics.
