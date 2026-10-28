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
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# TradingBot Knowledge Vault

This Vault describes the current reviewed TradingBot project. Start with [Authority Model](00_SYSTEM/AUTHORITY_MODEL.md), [Retrieval Policy](00_SYSTEM/RETRIEVAL_POLICY.md), [Current Version](11_VERSIONS/Current.md), [Source Manifest](06_SOURCE/Source-Manifest.md), [Reference Registry](06_SOURCE/Reference-Registry.md) and [Operating Workflow](12_WORKFLOWS/Operating-Workflow.md).

Canonical/normative knowledge and accepted References define intended semantics under project AGENTS authority. Active/executable notes describe current reviewed Source. [Source/Reference Consistency](06_SOURCE/Source-Reference-Consistency.md) preserves the remaining ambiguity instead of reconciling it silently. Hashes, versions and generated navigation are evidence rather than trading authority.

The source_scope declaration in _INDEX/source-hashes.json records the explicit user exclusion of new primary-structure concepts and the standalone added detector. Existing owner snapshots remain exact; complete accepted Reference bytes retain incidental extension content unchanged. Embedded excluded payloads are integrity-pinned but not semantically audited. The standalone Code tree is intentionally a scoped snapshot, not a complete runnable Engine package.

| Responsibility | Current navigation |
| --- | --- |
| Knowledge schema, authority and retrieval | 00_SYSTEM/ |
| Core invariants and market model | 01_CORE/ and 02_MARKET_MODEL/ |
| Existing behavior and algorithm owners | 03_BEHAVIORS/ and 04_ALGORITHMS/ |
| Upstream directional mirror scopes | 05_MIRROR/ |
| Exact Source, References and maps | 06_SOURCE/ |
| Server dispatch/cache/progress | [Local Server](06_SOURCE/Local-Server.md) |
| RAW identity/transfer and external acquisition | [RAW Resources](06_SOURCE/RAW-Resources.md), [FARAZ](06_SOURCE/FARAZ-Integration.md) |
| Chart workspace and review | [Chart Workspace](06_SOURCE/Chart-Workspace.md) |
| Validation and future supplied data | 07_VALIDATION/ and 08_DATA/ |
| Decisions, versions and procedures | 10_DECISIONS/, 11_VERSIONS/, 12_WORKFLOWS/ |
| Maintained release tooling | [Project Release](12_WORKFLOWS/Project-Release.md) |

RAW datasets, windows and regression fixtures remain EMPTY_BY_DESIGN. No market-data correctness result is supplied by knowledge retrieval. [Current Validation](_GENERATED/Current-Validation.md) records fresh completed gates separately from NOT RUN and intentionally excluded scopes. This maintenance leaves live production Source and accepted References read-only; publication is not authorized by a knowledge update.

Generate derived navigation with a Python environment containing jsonschema:

```text
python -B _SCHEMA/build_indexes.py
python -B _SCHEMA/build_indexes.py --check
python -B -m unittest discover -s _SCHEMA/tests -v
```

Resolve concept -> algorithm -> Source -> mirror -> current evidence identity. Generated maps cannot change a rule. Future Source ownership is rediscovered dynamically rather than frozen by this capture inventory.
