---
id: "system.knowledge_model"
type: "system"
status: "canonical"
authority: "normative"
title: "Knowledge model"
---

# Knowledge model

Entity kinds: system, core, market, behavior, algorithm, source, mirror. A behavior states meaning and lifecycle role; an algorithm states calculation rules; a source note maps executable symbols and state. Reactions, Resets, Blue Lines, Orders, and OrderAudit are calculation/evidence structures, not behaviors. Stable ID is the primary key; path is a locator.

Relations are typed: calculated_by, implemented_by, depends_on, produces, implements, parent_of, child_of, relates_to. Source references use repository-relative paths plus one-based line anchors. Exact source snapshot identity is recorded in _INDEX/source-hashes.json. Do not treat an inferred edge as a proved call.

The query chain is behavior -> algorithm -> source, adding lifecycle, chronology, direction, and validation evidence as needed. Only a canonical normative note may assert an accepted trading rule. Executable evidence describes what current code does; a mismatch must remain visible as a conflict.
