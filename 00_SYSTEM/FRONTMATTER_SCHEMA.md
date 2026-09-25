---
id: "system.frontmatter"
type: "system"
status: "canonical"
authority: "normative"
title: "Frontmatter schema"
---

# Frontmatter schema

Every populated note has `id`, `type`, `status`, `authority`, and `title`. Frontmatter uses JSON scalar/array syntax within YAML-compatible `key: value` lines; duplicate keys and unknown fields are errors. Stable IDs, not file paths, are machine identity. Source references use production-repository-relative `path#Lnumber` anchors; line numbers must be paired with a symbol or claim in prose because they can move.

Canonical relation arrays contain entity IDs. `calculated_by` links a behavior to calculation algorithms; `implemented_by` links an entity to modules that actually own its implementation. `implements` is the inverse for algorithm implementation. `depends_on` denotes a real input/computation dependency, not a loose association. `produces`, `parent_of`, `child_of`, `relates_to`, and `affects` carry their literal meanings. `orchestrates` marks bridge coordination without ownership; `supports` marks shared primitive support. Do not use an authoritative dependency edge into pending-fix knowledge.

Physical Source module notes use `source_path` for the production path, `mirror` for the Vault snapshot path, and `sha256` for their common byte hash. Aggregate Source maps have no `source_path`; `path` is not a valid field. External chart files are listed in `external_source_paths` with byte hashes in `external_source_hashes`; they remain production-repository-only evidence. The JSON schemas in `_SCHEMA` validate the structural contract; `_SCHEMA/build_indexes.py` checks cross-note relations and hashes. Generated indexes are derived from frontmatter and must not be hand-edited.
