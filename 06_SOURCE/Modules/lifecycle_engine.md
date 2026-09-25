---
id: "source.lifecycle_engine"
type: "source"
status: "active"
authority: "executable"
title: "lifecycle engine"
source_path: "engine/pipeline/lifecycle_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"
sha256: "330e26ffc04c24dea952e9a1e8e39da1a434936d0f80ef2233bd279fc32e8af1"
implements: ["algorithm.lifecycle", "algorithm.stopall", "algorithm.visibility", "algorithm.reconciliation", "algorithm.orderaudit"]
affects: ["behavior.a", "behavior.s", "behavior.e", "behavior.stopall"]
source_refs: ["engine/pipeline/lifecycle_engine.py#L1"]
---

# lifecycle engine
## Identity and snapshot
Production: engine/pipeline/lifecycle_engine.py
Mirror: 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py
SHA-256: 330e26ffc04c24dea952e9a1e8e39da1a434936d0f80ef2233bd279fc32e8af1
Declared versions: [('STOP_ALL_VERSION', '1.15.6')]

## Responsibility
Owns shared priority, StopAll gate state machine, cross-stage A/S/E eligibility, consumed S, internal Order filters, final visibility and audit preparation.

## Classes and owned concepts
StopAll (L39), StopAllDetector (L93)

## Important symbols
- sequence_priority: engine/pipeline/lifecycle_engine.py#L33
- StopAllDetector.detect: engine/pipeline/lifecycle_engine.py#L403
- split_a_zones_by_dominant_stops: engine/pipeline/lifecycle_engine.py#L946
- consumed_s_evidence_after_larger_stop: engine/pipeline/lifecycle_engine.py#L1172
- s_zones_for_module_engines: engine/pipeline/lifecycle_engine.py#L1314
- visible_s_zones_after_module_resets: engine/pipeline/lifecycle_engine.py#L1363
- filter_internal_behavior_outputs: engine/pipeline/lifecycle_engine.py#L1678
- finalize_behavior_visibility: engine/pipeline/lifecycle_engine.py#L1708
- prepare_order_audit: engine/pipeline/lifecycle_engine.py#L621

## Inputs and outputs
A/S/E candidates, Reactions, chronology and accepted Orders -> StopAll and final public A/S/E/OrderAudit preparation.

## State, direction, chronology, and invariants
StopAllDetector keeps dominant S/E group keys/counts, active StopAll and independent pending exact Blue-repeat counters. Accepted S stage lock prevents a rejected A fallback consuming S.

## Upstream dependencies and downstream consumers
Upstream: A/S/E detector outputs; reaction_engine chronology; core_utils; direction_policy.

Downstream: trading_pipeline final visibility and serialization.

## Relationships
Algorithms: algorithm.lifecycle algorithm.stopall algorithm.visibility algorithm.reconciliation.
Behaviors: behavior.a behavior.s behavior.e behavior.stopall.
