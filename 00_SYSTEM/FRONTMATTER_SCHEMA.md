---
id: "system.frontmatter"
type: "system"
status: "canonical"
authority: "normative"
title: "Frontmatter schema"
related_entities: []
source_reference: []
---

# Frontmatter schema

Every populated note has `id`, `type`, `status`, `authority`, `title`, `related_entities`, and `source_reference`. Frontmatter uses JSON scalar/array syntax within YAML-compatible `key: value` lines; duplicate keys and unknown fields are errors. Stable IDs, not file paths, are machine identity. Source references use Vault-root-relative `06_SOURCE/Code/...#Lnumber` anchors; line numbers must be paired with a symbol or claim in prose because they can move. A Vault-governance `system` note without a directly implementing engine rule may use `source_reference: []`; non-system notes require at least one anchored reference. An empty `related_entities` list is valid when no loose relation is justified; typed relations remain in their own fields.

`status: pending` is reserved here for required general knowledge whose rule is not established, such as the general Leg model; it requires `authority: non-canonical`. It differs from `pending-fix`, which marks the known incomplete OrderAudit contract. Fixture `fixture_status: Pending` continues to map to Vault `status: draft` under the separate case schema. Case notes include scalar `first_index` and `break_index` only when their physical `order_identity` pair is evidenced; otherwise both use `unknown`.

Canonical relation arrays contain entity IDs. `calculated_by` links a behavior to calculation algorithms; `implemented_by` links an entity to modules that actually own its implementation. `implements` is the inverse for algorithm implementation. `depends_on` denotes a real input/computation dependency, not a loose association. `produces`, `parent_of`, `child_of`, `relates_to`, and `affects` carry their literal meanings. `orchestrates` marks bridge coordination without ownership; `supports` marks shared primitive support. Do not use an authoritative dependency edge into pending-fix knowledge.

Physical Source module notes use `source_path` and `mirror` for the Vault-local captured source path, and `sha256` for its byte hash. Aggregate Source maps have no `source_path`; `path` is not a valid field. Chart evidence files are listed in `external_source_paths` with byte hashes in `external_source_hashes`; those fields retain their historical names but their values point only inside the Vault. The JSON schemas in `_SCHEMA` validate the structural contract; `_SCHEMA/build_indexes.py` checks cross-note relations and hashes. Generated indexes are derived from frontmatter and must not be hand-edited.

Data notes use `type: data` with `data_kind` to distinguish policy, registry, RAW model and physical dataset records. A dataset record includes the exact `raw_path`, all equal-hash `raw_locations`, `raw_sha256`, size, row count, epoch bounds, metadata fields and fixture/validation IDs. The builder verifies approved RAW roots, byte hashes, sizes and fixture hash relationships. The full dataset field contract is in `_SCHEMA/data.schema.json`; an `active` empirical dataset is not a successful trading-output test.
