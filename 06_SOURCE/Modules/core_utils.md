---
id: "source.core_utils"
type: "source"
status: "active"
authority: "executable"
title: "core utils"
source_path: "engine/pipeline/core_utils.py"
mirror: "06_SOURCE/Code/engine/pipeline/core_utils.py"
sha256: "3dae390ae77b72965f5799f7c132c4eba203775d5e72761fd7dd60c90f8578de"
affects: []
source_refs: ["engine/pipeline/core_utils.py#L1"]
supports: ["algorithm.raw", "algorithm.order"]
---

# core utils
## Identity and snapshot
Production: engine/pipeline/core_utils.py
Mirror: 06_SOURCE/Code/engine/pipeline/core_utils.py
SHA-256: 3dae390ae77b72965f5799f7c132c4eba203775d5e72761fd7dd60c90f8578de
Declared versions: [('CORE_UTILS_VERSION', '1.0.0')]

## Responsibility
Owns shared Decimal normalization and physical Order/Reaction identity.

## Classes and owned concepts
No classes.

## Important symbols
- as_decimal: engine/pipeline/core_utils.py#L11
- order_identity: engine/pipeline/core_utils.py#L19
- reaction_identity: engine/pipeline/core_utils.py#L24

## Inputs and outputs
Numeric values or Reaction-like object -> Decimal or (FirstIndex,BreakIndex).

## State, direction, chronology, and invariants
Preserve existing Decimal; otherwise Decimal(str(value)). Identity is physical indexes, independent of timestamp, native mode, cause or direction.

## Upstream dependencies and downstream consumers
Upstream: none.

Downstream: reaction_engine, a_zone_detector, s_zone_detector, e_zone_detector, lifecycle_engine, trading_pipeline.

## Relationships
Supports algorithm.raw Decimal normalization and algorithm.order physical identity; it does not own RAW ingestion or Order formation.
Behaviors: No direct behavior ownership.
