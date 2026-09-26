---
id: "system.knowledge_model"
type: "system"
status: "canonical"
authority: "normative"
title: "Knowledge model"
related_entities: []
source_reference: []
---

# Knowledge model

Current populated entity kinds are `system`, `core`, `market`, `behavior`, `algorithm`, `source`, `mirror`, `test`, `case`, and `data`. A Behavior states public semantic role and lifecycle (A, S, E, StopAll only). An Algorithm states calculation rules. A Source module note maps current executable symbols and state. Mirror notes describe verified direction transformations; test notes define validation contracts; case notes pin individual fixtures; data notes pin physical RAW identity and data policies. Source maps describe relationships but are not physical implementation owners. Reaction, Reset, Blue and physical Order are algorithm/evidence structures, not Behaviors. Current audit output remains in exact source evidence but has no active knowledge entity.

Stable ID is the primary key; a file path is a locator. Relations describe calculation, implementation ownership, dependency, output, parentage, orchestration, support, or loose association, and must not be substituted for one another. Source references use Vault-relative paths and one-based line anchors. All nine main byte-exact Engine files are pinned in `_INDEX/source-hashes.json`; the comprehensive HPZR6 references are registered as optional external evidence.

The retrieval route for a public claim is **Behavior → calculating Algorithm → implementing Source → Validation**. A Behavior note says what A/S/E/StopAll means; the Algorithm note states how it is calculated; the Source note identifies the current executable owner; the Validation note states how the claim is checked. The reverse route is useful for impact analysis. A link along this route is evidence navigation, not proof that a run passed. Data and Fixture entities supply pinned inputs and scenario assertions to Validation without becoming algorithm owners.

Authority and status are independent. `canonical`/`normative` system, core, algorithm and validation notes assert accepted contracts, while `active`/`canonical` mirror notes describe the curated transformation contract. `active`/`executable` describes current code; `pending-fix`/`non-canonical` Order_B/C are quarantined. Audit output is physically present in exact source snapshots but has no indexed algorithm concept. Active case notes use `authority: empirical` and `fixture_authority: Canonical` to identify accepted fixture assertions, not trading-rule authority. Pending and Historical cases cannot supply current expected outputs. `_INDEX` is a deterministic cache of Markdown frontmatter; `_GENERATED` is machine-owned. Both must be regenerated, never hand-edited as knowledge.

Future decision, version, workflow, plugin, and policy entity types will be added through a versioned schema/ID-convention update when those phases begin. Their folders and empty placeholders do not currently imply populated entities or a frozen type vocabulary. `data.dataset_<hash8>` identifies one exact RAW byte stream; `data` records do not grant algorithm or Behavior authority.
