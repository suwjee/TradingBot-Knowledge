---
id: "system.authority"
type: "system"
status: "canonical"
authority: "normative"
title: "Authority and status model"
---

# Authority and status model

Authority values separate evidence layers: `normative` = accepted algorithm/reference contract; `executable` = current source behavior; `empirical` = RAW, test, or runtime observation; `historical` = prior version; `non-canonical` = known incomplete or unresolved component. `status` tracks lifecycle independently: canonical, active, draft, proposed, pending-fix, deprecated, superseded, archived.

A canonical normative rule needs support from the two synchronized V5.4.11 HPZR6 directional references and current source. Both references are external, hash-pinned dependencies listed in `_INDEX/source-hashes.json`; they are not stored in this Vault. A Vault-only reader must obtain the exact production reference files before treating a cited rule as independently verified. Current source is executable evidence, not an automatic normative replacement.

If references and source disagree, cite both with path, line, version, and hash, mark the rule unresolved, and seek a domain decision. Neither a newer timestamp nor current executable behavior silently wins. Empirical evidence can demonstrate a mismatch but cannot automatically rewrite a normative rule. Historical cases cannot override current canonical knowledge. Pending-fix/non-canonical OrderAudit may describe what current code emits but must never supply accepted S/E/StopAll rules. Empty placeholders carry no authority.

A source snapshot proves file identity, not semantic correctness. A generated index is a cache of Markdown frontmatter, never an authority layer. Do not hand-edit generated indexes or `_GENERATED` content to change a rule.
