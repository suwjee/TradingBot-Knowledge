---
id: "system.editing"
type: "system"
status: "canonical"
authority: "normative"
title: "AI editing policy"
related_entities: []
source_reference: []
---

# AI editing policy

Before changing a trading note, retrieve its owning canonical note, dependency algorithms, both current directional references, and the current source symbols. Verify the claim against exact chronology, strictness, Decimal semantics, tie order, nullable fields, parent/source provenance, direction mapping, and public serialization. Never infer a trading rule from a title, folder, generated index, or observed case alone.

Edit the single owning note; keep secondary summaries short and linked by ID. Preserve stable IDs and update relation metadata atomically. Use `implemented_by` only for actual implementation ownership, `orchestrates` for bridge stage coordination, and `supports` for shared primitives. Preserve the distinction between normative, executable, empirical, historical, and non-canonical evidence. Document a reference/source conflict instead of guessing. Do not promote pending-fix OrderAudit, an incomplete Leg model, or presentation-only historical rescues into canonical calculation.

Production source is read-only for Vault work. Mirror refresh requires explicit source identity and byte/hash verification; never hand-edit mirrored Python. After any Vault metadata or rule edit, run `_SCHEMA/build_indexes.py`, validate all schemas and relation targets, verify source/reference hashes, and check deterministic index regeneration. Generated `_INDEX` and `_GENERATED` files are machine-owned and must not be hand-edited. Review Git diff before committing; keep local Obsidian workspace state out of shared knowledge.
