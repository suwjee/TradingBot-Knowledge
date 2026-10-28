---
id: "core.lifecycle"
type: "core"
status: "active"
authority: "executable"
title: "Accepted lifecycle model"
version: "current"
related_entities: ["algorithm.lifecycle", "algorithm.stopall", "core.ownership", "core.priority"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Accepted lifecycle model

Canonical aligned confirmation validates A's source. First strict A stop opens S; next-A confirmation already reached makes older handoff stale. Accepted S/E strict stops from decision open E cycles; accepted parent/family priority reconciles recursive numbers.

Lower half-leg A/S discovery may continue inside larger active owner. Closed-owner leg head can consume a strict beyond-boundary candidate. A prior cycle first stop cannot be recreated by later recross. Historical accepted owners remain lineage/evidence independent of public label.

StopAll freezes accepted hard prefix and clears the single exact owner/count and pending completed stop. Future state cannot delete/move prefix. Independent accepted-S E1 roots can restore after hard boundary without changing dominant StopAll sequence.

Valid physical Order parent provenance persists across consumers; explicit invalid S has no accepted parent-stop creation rights. Order_B uses accepted stopped-main owner and latest accepted geometric source before reset aligned First,with next accepted A trigger expiry.

Publishing sequence_resets atomically copies its map, refreshes sorted reset times and clears dependent candidate/carried context caches once. Immutable physical stop/cross caches and historical accepted Order_A causes remain retained. The reset lookup window is (start,end]. Explicit invalid S identities are rejected at parent registration and reconstructed parent-stop cause retention; valid historical S and shared Order_B reset-leg provenance remain eligible.
