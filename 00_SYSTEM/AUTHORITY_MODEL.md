---
id: "system.authority"
type: "system"
status: "canonical"
authority: "normative"
title: "Authority and status model"
related_entities: ["market.leg", "algorithm.orderaudit"]
source_reference: []
---

# Authority and status model

Authority values separate evidence layers: `normative` = accepted algorithm/reference contract; `executable` = current source behavior; `empirical` = RAW, test, or runtime observation; `historical` = prior version; `non-canonical` = known incomplete or unresolved component. `status` tracks lifecycle independently: canonical, active, draft, proposed, pending-fix, deprecated, superseded, archived.

For `type: mirror` notes, `authority: canonical` identifies the curated direction-transformation contract grounded in the synchronized references and current source, with `status: active`. This is a knowledge-layer authority label, not a transfer of implementation ownership from source. Mirror notes use `source_reference` for verified production line anchors and `related_entities` for indexed `relates_to` edges.

For `type: test`, `status: canonical` and `authority: normative` define a validation contract, not a recorded successful run. For `type: case`, fixture authority is separate from the note authority: Active maps to `status: active`, `authority: empirical`, `fixture_authority: Canonical`; Pending maps to `draft`, `non-canonical`, `Pending`; Historical maps to `archived`, `historical`, `Historical`. Canonical fixture authority accepts a specific assertion as regression evidence only. A complete zero-difference baseline still requires saved inputs, source identity, outputs and a fresh comparison. See `07_VALIDATION/Fixture-Model.md` and `07_VALIDATION/Fixtures/Fixture-Registry.md`.

For `type: data`, canonical/normative notes define the data knowledge contract. A dataset note is active/empirical only for verified present bytes and stated metadata; it does not assert that the trading pipeline passed. A dataset with a known metadata conflict is draft/non-canonical until resolved. Dataset SHA-256 identifies physical input, not output correctness. See `08_DATA/Data-Policy.md` and `08_DATA/Datasets/Dataset-Registry.md`.

A canonical normative rule needs support from the two synchronized V5.4.11 HPZR6 directional references and current source. Both references are external, hash-pinned dependencies listed in `_INDEX/source-hashes.json`; they are not stored in this Vault. A Vault-only reader must obtain the exact production reference files before treating a cited rule as independently verified. Current source is executable evidence, not an automatic normative replacement.

If references and source disagree, cite both with path, line, version, and hash, mark the rule unresolved, and seek a domain decision. Neither a newer timestamp nor current executable behavior silently wins. Empirical evidence can demonstrate a mismatch but cannot automatically rewrite a normative rule. Historical cases cannot override current canonical knowledge. Pending-fix/non-canonical OrderAudit may describe what current code emits but must never supply accepted S/E/StopAll rules. Draft/non-canonical `market.leg` records the absent general Leg contract and cannot supply one. Empty placeholders carry no authority.

A source snapshot proves file identity, not semantic correctness. A generated index is a cache of Markdown frontmatter, never an authority layer. Do not hand-edit generated indexes or `_GENERATED` content to change a rule.
