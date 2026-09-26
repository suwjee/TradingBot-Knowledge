---
id: "source.lifecycle_engine"
type: "source"
status: "active"
authority: "executable"
title: "Lifecycle and StopAll: mixed source evidence"
source_path: "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"
sha256: "330e26ffc04c24dea952e9a1e8e39da1a434936d0f80ef2233bd279fc32e8af1"
implementation_validity: "mixed"
affected_by_known_invalid_order_route: true
implements: ["algorithm.lifecycle", "algorithm.reconciliation", "algorithm.stopall", "algorithm.visibility"]
source_refs: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L33", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L403", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L946", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L1658"]
related_entities: ["test.source_validation"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L33"]
---

# Lifecycle engine

The exact snapshot contains `StopAllDetector.detect` (line 403), dominant-stop A selection (line 946), E/S participation (lines 1314–1363), reconciliation (line 1532), and final visibility (line 1708). These responsibilities are not globally invalidated by B/C defects. `forbidden_internal_order_b` (line 1658) and dependent filtering use the current defective B route; conclusions that require that route remain quarantined. Audit-specific functions remain source evidence only and do not define an active Vault algorithm.
