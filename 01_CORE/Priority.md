---
id: "core.priority"
type: "core"
status: "active"
authority: "executable"
title: "Shared lifecycle priority and chronology"
version: "current"
related_entities: ["algorithm.lifecycle", "algorithm.reconciliation", "algorithm.stopall"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Lifecycle priority and chronology

StopAll repetition owns only S/E: S Blue < E Blue < S Red < E Red. One exact S color or E(family,number) starts at count1 and arms at count>=2. Exact repeats increment; higher priority or a larger same-family E number replaces at count1. Lower-priority accepted output cannot count behind the owner. A does not participate in this S/E counter.

Cross-stage visibility and Order_B ownership separately use module_priority: StopAll5, E Red4, S Red3, E Blue2, S Blue1, A0. Latest stopped main boundary precedes same-boundary rank/source ties where the owning function requires it. Same-source E Red beats Blue; within one family larger number wins and remaining equality preserves earlier provenance. These scopes must not be flattened into one universal ranking.

Hard StopAll clears exact owner/count/armed state and pending completed stop. Its existing historical numbering gate remains separate from S/E occurrence identity.
