---
id: "mirror.algorithm_matrix"
type: "mirror"
status: "active"
authority: "executable"
title: "Current algorithm mirror coverage"
version: "current"
related_entities: ["core.pipeline", "mirror.source_map", "mirror.validation_rules"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/core_utils.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Current algorithm mirror coverage

| Owner | Directional dimension | Invariant dimension |
| --- | --- | --- |
| Reaction/Reset | reflected geometry,explicit Unified price sides | identity,chronology,mode/Reset priority |
| Blue/A | Fibonacci/render,strict strikes/stops/extrema | spacing,formation/expiry,Blue provenance |
| S/E | candidate/parent/Order stops,source extrema | subtype,family/number,accepted lineage/race |
| OrderAudit | canonical opposite stop,LL/HH | cause creation/use,identity,dedup,retention |
| Lifecycle/StopAll | strict stop/boundary comparator | priority,exact group keys,hard prefix |

RAW normalization/serialization preserve normalized inputs and finalized fields instead of mirrored trading selection. DirectionPolicy owns price primitives;core_utils owns Decimal/identity.

A future changed rule must cover every dependent owner/field. This matrix describes current Source documentation scope,not executed parity or independent market proof.

## Coverage boundary

This mirror description covers the existing upstream owners only. The manifest source_scope records the explicitly excluded added feature. Complete raw Reference bytes remain exact evidence; incidental extension content does not create a mirror approval or semantic audit result.
