---
id: "system.retrieval"
type: "system"
status: "active"
authority: "normative"
title: "Current retrieval and Plugin bootstrap"
version: "current"
related_entities: ["core.invariants", "core.pipeline", "source.reference_registry", "source.source_manifest", "system.authority", "version.current", "workflow.operating"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Current retrieval and Plugin bootstrap

Retrieve system.authority, version.current, source.source_manifest, source.reference_registry, core.invariants, core.pipeline and workflow.operating before semantic reasoning. Resolve Concept → Algorithm → Source → Mirror → Current Version. Inspect the current validation report and stable IDs before selecting evidence.

The Plugin reads canonical Markdown through its validated local entity index. Local Algorithm References are the default first-class evidence source. Both local bytes/hash and declared version/direction must agree with Registry and Source Manifest. An external Engine checkout is optional cross-verification; configuring it requires exact agreement and never permits a bad local file to fall back silently.

Trusted JSON rejects nested duplicate keys and non-JSON numeric constants. Full frontmatter and schema-owned metadata must equal the index; relations must equal canonical typed arrays. Generated navigation cannot alter a rule. Current Source defines executable behavior and synchronized canonical References specify it. Material disagreement requires evidence and resolution.

RAW and Fixture stores are EMPTY_BY_DESIGN. Data-dependent tools return explicit ENTITY_NOT_FOUND for absent IDs. No expected market outcome or regression evidence is supplied by knowledge retrieval.
