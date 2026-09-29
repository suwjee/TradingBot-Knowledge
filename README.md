---
id: "system.readme"
type: "system"
status: "active"
authority: "normative"
title: "Current-only TradingBot Knowledge Vault"
version: "current"
related_entities: ["source.reference_consistency", "system.authority", "system.manifest", "system.retrieval"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# TradingBot Knowledge Vault

This Vault represents CURRENT TradingBot only. Legacy implementation knowledge has been intentionally removed. RAW/Data and Regression Fixtures are intentionally empty.

Current Production Source and synchronized current directional References are the evidence roots. Source describes executable behavior. Both References embed exact current Source; narrative agreement has four separately recorded scope discrepancies in source.reference_consistency. Start with [Authority Model](00_SYSTEM/AUTHORITY_MODEL.md), [Current Version](11_VERSIONS/Current.md), [Source Manifest](06_SOURCE/Source-Manifest.md), [Reference Registry](06_SOURCE/Reference-Registry.md), [Core Invariants](01_CORE/Core-Invariants.md), [Pipeline](01_CORE/Pipeline.md) and [Operating Workflow](12_WORKFLOWS/Operating-Workflow.md).

00_SYSTEM governs authority, schema and retrieval. 01_CORE and 02_MARKET_MODEL explain current invariants and market chronology. 03_BEHAVIORS and 04_ALGORITHMS describe actual current behavior and calculation rules. 05_MIRROR explains geometric transforms and invariant state. 06_SOURCE contains exact local Source/Reference evidence and maps. 10_DECISIONS, 11_VERSIONS and 12_WORKFLOWS describe current architecture, versions and operating methods.

07_VALIDATION/Fixtures and 08_DATA/Raw contain no market cases or physical data. Their generic policy/schema notes explain how explicitly supplied future evidence can be added. No regression fixture evidence or RAW evidence is currently stored. Indexes and schemas support these empty stores without fabricating evidence.

Generate all derived navigation with Python 3 and the installed jsonschema dependency:

```text
python -B _SCHEMA/build_indexes.py
python -B _SCHEMA/build_indexes.py --check
python -B -m unittest discover -s _SCHEMA/tests -v
```

Resolve Concept -> Algorithm -> Source -> Mirror -> Current Version. Exact Reference bytes are available locally under 06_SOURCE/Code/engine/algorithms and registered by local_path/hash. Generated indexes and graph maps are caches of current Markdown and Source structure, not trading authority. Current boundaries come from the reviewed Source owners and their qualified algorithm notes. Reference narrative discrepancies are disclosed; no compensating Engine override is active.

See [Current Validation](_GENERATED/Current-Validation.md) for actual current gate results and Plugin readiness. This Phase-1 audit keeps Production Engine and both References read-only. Only Vault/Plugin changes are authorized. RAW, trading fixtures and market regression are NOT_REQUIRED_THIS_PHASE.
