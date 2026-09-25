---
id: "system.knowledge_model"
type: "system"
status: "canonical"
authority: "normative"
title: "Knowledge model"
---

# Knowledge model

Current populated entity kinds are `system`, `core`, `market`, `behavior`, `algorithm`, and `source`; `mirror`, `test`, and `case` are reserved in the schema for later phases. A Behavior states public semantic role and lifecycle (A, S, E, StopAll only). An Algorithm states calculation rules. A Source module note maps current executable symbols and state. Source maps describe relationships but are not physical implementation owners. Reaction, Reset, Blue, physical Order, and OrderAudit are calculation/evidence structures, not Behaviors.

Stable ID is the primary key; a file path is a locator. Relations describe calculation, implementation ownership, dependency, output, parentage, orchestration, support, or loose association, and must not be substituted for one another. Source references use repository-relative paths and one-based line anchors. The byte-exact Python snapshot and reference hashes are recorded in `_INDEX/source-hashes.json`; both reference documents remain external to the Vault.

Authority and status are independent. Only `canonical`/`normative` notes assert accepted trading rules. `active`/`executable` describes current code; `pending-fix`/`non-canonical` OrderAudit is quarantined. Empirical validation and case entities are future evidence, not automatic rule authority. `_INDEX` is a deterministic cache of Markdown frontmatter; `_GENERATED` is machine-owned. Both must be regenerated, never hand-edited as knowledge.

Future data, decision, version, workflow, plugin, and policy entity types will be added through a versioned schema/ID-convention update when those phases begin. Their folders and empty placeholders do not currently imply populated entities or a frozen type vocabulary.
