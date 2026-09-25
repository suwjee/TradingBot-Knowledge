---
id: "algorithm.visibility"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Final visibility and lineage"
implemented_by: ["source.lifecycle_engine", "source.trading_pipeline"]
depends_on: ["algorithm.lifecycle", "algorithm.stopall", "algorithm.internal_reaction"]
source_refs: []
related_entities: ["test.source_validation", "mirror.exceptions", "test.mirror_validation", "test.output_validation"]
source_reference: []
---

# Final visibility and lineage

## Calculation logic

After full reconciliation, build visible A against accepted S, detect StopAll once from reconciled E and StopAll-eligible S, then restore independent accepted S-owned E1 roots without rewriting StopAll history. StopAll source index suppresses E at the same source; final E/StopAll source suppresses A and S there. Restore calculation-eligible S referenced by final E and A referenced by final S for lineage, subject to same-source occupancy and calculation-invalid identity exclusions.


Eligible historical E rescues are appended after lifecycle, StopAll, Internal, and audit ownership is fixed; they must not feed back into calculation, family/number, S/A visibility, or Order provenance. Only at the end clip to presentation main indexes.

## Contract interface

- **Purpose:** Choose public labels while retaining eligible calculation lineage.
- **Inputs:** Reconciled A/S/E, StopAll occupancy, source identity and requested display bounds.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Final visible collections and OrderAudit preparation context.
- **Source ownership:** source.lifecycle_engine, source.trading_pipeline.
- **Validation relationship:** test.output_validation; test.source_validation checks the line anchors and owner.
