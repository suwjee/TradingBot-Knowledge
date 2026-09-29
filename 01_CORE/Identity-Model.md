---
id: "core.identity"
type: "core"
status: "active"
authority: "executable"
title: "Physical identity and provenance model"
version: "current"
related_entities: ["algorithm.orderaudit", "algorithm.reconciliation", "core.determinism"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49"]
name: "Identity"
aliases: ["Physical identity"]
---

# Physical identity and provenance model

## Reaction and physical Order

core_utils.order_identity normalizes FirstIndex/BreakIndex to integer tuple; reaction_identity reads Reaction-like fields. Direction-owned physical Order ledger keys that pair. Canonical reaction number stays original full-stream ordinal; internal marking does not renumber. Parent type/family/number,creation stop and consumer remain separate provenance.

## Behaviors and causes

E same-source reconciliation keys source_index/source_time. A/S invalid identity ledgers use that same physical pair in owner-defined tuple order. module_identity adds class,family/color,optional number,source_time/source_index to distinguish lifecycle owners. Exact parent-stop cause key is parentType,parentFamily,eventTime,parentSourceTime; one physical Order owns it.

## Reset-leg convergence

Order_B cause identity includes post-stop type/source/event,anchor type/source/extreme,aligned reset Reaction First/Break,Reset index/level/time,frozen boundary/source,strict break and physical opposite First/Break. Complete identity equality drives feedback convergence. Multiple reset causes may share one Order; cause identity is not duplicate physical identity.

Physical identity and source joins remain invariant across mirror/projection. Row position,chart label,parent name or visible ordinal cannot substitute physical identity.
