---
id: "system.retrieval"
type: "system"
status: "canonical"
authority: "normative"
title: "Retrieval policy"
related_entities: []
source_reference: []
---

# Retrieval policy

For every retrieval session, first load `system.authority` and this policy by ID; load `system.frontmatter` when editing metadata. Resolve IDs through `_INDEX/entities.json`, open the owning Markdown, then follow only relations relevant to the question. Check status, authority, and `_INDEX/sync-status.json` before using a claim. Verify source symbols and lines against the hash-pinned files in `06_SOURCE/Code`. All nine main Engine modules are retained; comprehensive HPZR6 references are hash-registered optional external evidence. Order_B/C current semantics are known invalid, so affected claims remain pending even if source and references agree. A Vault snapshot does not prove that a later production checkout has the same bytes.

Follow **Behavior → Algorithm → Source → Validation** for a public-rule answer, and include Data/Fixture only when the question needs concrete input or expected output. For performance questions, load `test.runtime_benchmark`, `test.memory_benchmark`, `test.stage_profiling` and `test.optimization_rules` according to the requested metric. For test execution, load `test.test_model` and the unit, integration or regression policy. For directional proof, load `test.mirror_policy` and the appropriate direction, constructed-symmetry or mirror-regression note. Policy notes specify a method; a PASS needs a separate run artifact.


Use `implemented_by` for actual rule owners. `orchestrates` identifies pass coordination; `supports` identifies a shared primitive. For a dataset or fixture question, start at `data.dataset_registry` and the hash-pinned dataset note, then follow its case IDs to `test.fixture_registry`; check dataset status and input scope before interpreting an expected output. For chart result questions, inspect `source.integration_boundary` and the request input scope before applying the full-physical-RAW normative contract. Its chart evidence is stored in `06_SOURCE/Code/apps/chart`. If a needed relation or reference is absent, report that gap. If a source/reference or RAW hash changed, mark the affected answer stale until re-audited. Tests/cases and data evidence supplement retrieval but cannot silently change a normative trading rule.
