---
id: "source.ownership_map"
type: "source"
status: "active"
authority: "executable"
title: "Current ownership map"
version: "current"
related_entities: ["source.reference_registry", "source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/__init__.py", "06_SOURCE/Code/engine/bridge/__init__.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/__init__.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Current ownership map

| Owned calculation/state | Current owner |
| --- | --- |
| Package marker | 06_SOURCE/Code/engine/__init__.py |
| Package marker | 06_SOURCE/Code/engine/bridge/__init__.py |
| CLI input normalization, dynamic module loading, cross-stage coordination, OrderAudit preparation and JSON serialization | 06_SOURCE/Code/engine/bridge/trading_pipeline.py |
| Pipeline sibling-import compatibility wrapper | 06_SOURCE/Code/engine/pipeline/__init__.py |
| A formation, paired Blue provenance and inherited stops | 06_SOURCE/Code/engine/pipeline/a_zone_detector.py |
| Scale and Reset Blue construction and public/calculation-valid Blue ownership | 06_SOURCE/Code/engine/pipeline/blue_line_detector.py |
| Behavior-neutral Decimal normalization and physical Reaction/Order identity | 06_SOURCE/Code/engine/pipeline/core_utils.py |
| Shared direction-sensitive geometry, strict comparisons, extrema and confirmation | 06_SOURCE/Code/engine/pipeline/direction_policy.py |
| E parent-stop cycles, recursive families and reconciled Order-backed continuation | 06_SOURCE/Code/engine/pipeline/e_zone_detector.py |
| Lifecycle ownership, StopAll gates, retained calculation lineage and final visibility | 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py |
| Physical Order_A and Order_B discovery, reset-leg anchors, immutable identity/provenance and accepted/live ledgers | 06_SOURCE/Code/engine/pipeline/order_audit_engine.py |
| Reaction, Reset, reflected direction geometry, exact lower-timeframe chronology and internal Reaction classification | 06_SOURCE/Code/engine/pipeline/reaction_engine.py |
| S candidate races, source geometry, color decisions and shared accepted-Order stop reconciliation | 06_SOURCE/Code/engine/pipeline/s_zone_detector.py |

## Project integration and scope

Chart owns browser interaction, presentation and user workspace/drawings; source.chart_workspace maps those contracts. Vite orchestration/cache/progress belongs to source.local_server. RAW persistence/identity/transfer belongs to source.raw_resources. FARAZ session/acquisition belongs to source.faraz. Current release mechanics belong to workflow.project_release. source_scope explicitly limits added-feature audit/standalone Source coverage.
