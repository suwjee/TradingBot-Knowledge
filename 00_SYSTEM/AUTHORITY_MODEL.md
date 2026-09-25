---
id: "system.authority"
type: "system"
status: "canonical"
authority: "normative"
title: "Authority and status model"
---

# Authority and status model

Authority values: normative = accepted calculation rule supported by current synchronized references and source; executable = present code behavior; empirical = observed output, test, or RAW evidence; historical = old version; non-canonical = known incomplete or unresolved component. Status values: canonical, active, draft, proposed, pending-fix, deprecated, superseded, archived.

Authority and status are separate. A source note is active/executable. A synchronized algorithm note is canonical/normative. OrderAudit is pending-fix/non-canonical even though code exists. A source snapshot proves implementation identity, not correctness.

If a reference and source disagree, retain both statements, cite exact lines and hashes, and mark the affected rule unresolved. Do not silently promote the newer file or current executable code to normative. Legacy empty notes have no rule authority. Historical prose is never used to fill a canonical gap.
