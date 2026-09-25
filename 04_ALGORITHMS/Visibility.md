---
id: "algorithm.visibility"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Final visibility and lineage"
implemented_by: ["source.lifecycle_engine", "source.trading_pipeline"]
depends_on: ["algorithm.lifecycle", "algorithm.stopall", "algorithm.internal_reaction"]
source_refs: ["engine/pipeline/lifecycle_engine.py#L1612", "engine/pipeline/lifecycle_engine.py#L1708", "engine/bridge/trading_pipeline.py#L2549"]
---

# Final visibility and lineage

After full reconciliation, build visible A against accepted S, detect StopAll once from reconciled E and StopAll-eligible S, then restore independent accepted S-owned E1 roots without rewriting StopAll history. StopAll source index suppresses E at the same source; final E/StopAll source suppresses A and S there. Restore calculation-eligible S referenced by final E and A referenced by final S for lineage, subject to same-source occupancy and calculation-invalid identity exclusions.

Remove S descendants of stage-invalid A. A provenance crossing a dominant current-module strict-stop boundary is hidden unless rebuilt wholly after it. Internal Reaction status alone does not hide all behavior: public Blue requires calculation_valid and not behavior_internal; forbidden internal physical Orders are only native Mode-B internal identities whose surviving causes are Reset-leg-only. A valid independent parent-stop or blue-leg cause prevents that narrow exclusion.

Eligible historical E rescues are appended after lifecycle, StopAll, Internal, and audit ownership is fixed; they must not feed back into calculation, family/number, S/A visibility, or Order provenance. Only at the end clip to presentation main indexes.
