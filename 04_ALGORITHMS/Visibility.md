---
id: "algorithm.visibility"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Final visibility and lineage"
implemented_by: ["source.lifecycle_engine", "source.trading_pipeline"]
depends_on: ["algorithm.lifecycle", "algorithm.stopall", "algorithm.internal_reaction"]
source_refs: ["engine/pipeline/lifecycle_engine.py#L1612", "engine/pipeline/lifecycle_engine.py#L1708", "engine/bridge/trading_pipeline.py#L2549"]
related_entities: ["test.source_validation", "mirror.exceptions", "test.mirror_validation"]
source_reference: ["engine/pipeline/lifecycle_engine.py#L1612", "engine/pipeline/lifecycle_engine.py#L1708", "engine/bridge/trading_pipeline.py#L2549"]
---

# Final visibility and lineage

After full reconciliation, build visible A against accepted S, detect StopAll once from reconciled E and StopAll-eligible S, then restore independent accepted S-owned E1 roots without rewriting StopAll history. StopAll source index suppresses E at the same source; final E/StopAll source suppresses A and S there. Restore calculation-eligible S referenced by final E and A referenced by final S for lineage, subject to same-source occupancy and calculation-invalid identity exclusions.

Remove S descendants of stage-invalid A. A provenance crossing a dominant current-module strict-stop boundary is hidden unless rebuilt wholly after it. Internal Reaction status alone does not hide all behavior: public Blue requires calculation_valid and not behavior_internal. The accepted physical-Order ledger excludes an internal native Mode-B identity only when all surviving causes are reset-leg (`lifecycle_engine.py#L777-L800`). The separate final E/StopAll output filter currently excludes an internal native Mode-B owner when any reset-leg cause or reset-leg timestamp is present (`lifecycle_engine.py#L1658-L1708`); both references §14 specify reset-leg-only. Its mixed-cause result is unresolved and must not be treated as a settled canonical visibility rule; see `mirror.exceptions` and `test.mirror_validation`.

Eligible historical E rescues are appended after lifecycle, StopAll, Internal, and audit ownership is fixed; they must not feed back into calculation, family/number, S/A visibility, or Order provenance. Only at the end clip to presentation main indexes.
