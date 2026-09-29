---
id: "system.frontmatter"
type: "system"
status: "active"
authority: "normative"
title: "Frontmatter and evidence schema"
version: "current"
related_entities: ["system.ids", "system.knowledge_model"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Frontmatter and evidence schema

Each knowledge Markdown note begins with an opening --- line, one unique lowercase key per line whose value is valid JSON, and a closing --- line. This deliberately bounded format supports unambiguous scalars, arrays and objects without requiring a YAML loader. Required fields are id, type, status, authority, title and source_reference.

The stable ID prefix matches the entity type. Source references are normalized Vault-relative paths with optional one-based #L anchors. source_path, mirror and sha256 pin an exact module. Relations are typed arrays of existing stable IDs; implemented_by identifies an actual executable owner, depends_on identifies a dependency and related_entities supplies navigation only.

Algorithm and behavior notes name current source owners. algorithm_reference links the precise current raw reference sections; mirror_links links current mirror knowledge. version is per note or Source module; Reference version is independent. Generated output is validated against the Markdown metadata and exact local evidence.

Schemas support system, core, market, behavior, algorithm, source, mirror, test, case, data, decision, version and workflow records. Empty Data and Fixture stores are valid. Future records must supply provenance; schema validity alone does not establish a correct expected trading output.


## Names, narrative status and derived note identity

Optional name and aliases are navigation metadata. Case-folded names/aliases cannot shadow another stable ID. reference_agreement records match/conflict/ambiguous/not-applicable; reference_conflicts lists review record keys and does not change executable authority. Every generated entity row carries content_sha256 and content_bytes for the complete Markdown bytes. These three derived row fields (including file) are excluded from frontmatter equality only; every authored metadata field remains compared. The current contract requires note identity pins, so deleting them cannot bypass body currentness. Regeneration follows any authorized Markdown change.
