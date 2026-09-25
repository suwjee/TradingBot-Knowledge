---
id: "core.e_numbering"
type: "core"
status: "canonical"
authority: "normative"
title: "E numbering"
calculated_by: ["algorithm.reconciliation"]
implemented_by: ["source.e_zone_detector"]
depends_on: ["behavior.e"]
source_refs: ["engine/pipeline/e_zone_detector.py#L2463", "engine/pipeline/e_zone_detector.py#L2267"]
related_entities: ["algorithm.reconciliation", "test.identity_invariants"]
source_reference: ["engine/pipeline/e_zone_detector.py#L2463", "engine/pipeline/e_zone_detector.py#L2267"]
---

# E numbering

E1 opens from an accepted stopped S. A stopped accepted E can open E(n+1). The reconciler maintains active accepted E state by chronology and family. When a winner stops accepted same-family E owners, the next number is max(stopped numbers)+1; without stopped same-family owner it begins at 1, subject to Red priority and inherited active-parent family. A StopAll hard sequence boundary resets active E continuation; lineage may report parentType=StopAll for a child at that source.

Numbers are state on one E algorithm, not distinct E1/E2/E3 algorithms. Same-source conflict chooses Red over Blue, then higher number within family, then first accepted object. Read algorithm.reconciliation for exact precedence.
