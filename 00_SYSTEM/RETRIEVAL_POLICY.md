---
id: "system.retrieval"
type: "system"
status: "canonical"
authority: "normative"
title: "Retrieval policy"
---

# Retrieval policy

Resolve an ID via _INDEX/entities.json, open its Markdown, and follow typed relations. Confirm source symbol and line in the current module or hashed mirror. Check _INDEX/source-hashes.json before using a snapshot as current.

Behavior question: behavior -> calculated_by algorithm -> dependency algorithms -> lifecycle/visibility -> implemented_by source -> mirror and validation evidence. Algorithm question: algorithm -> exact dependencies and outputs -> source -> both direction rules -> relevant tests/cases. Source debugging: module -> owned symbols/state -> algorithms -> related behaviors -> upstream/downstream consumers.

Reject pending-fix/non-canonical notes as normative context. If source hash changed, mark the answer stale until source and references are rechecked. If a needed relation is absent, report it instead of inventing one.
