---
id: "system.phase_4_5_audit"
type: "system"
status: "active"
authority: "empirical"
title: "Phase 4.5 independent forensic audit"
source_refs: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md", "engine/bridge/trading_pipeline.py#L1903"]
related_entities: ["system.manifest"]
source_reference: ["engine/bridge/trading_pipeline.py#L1903"]
---

# Phase 4.5 independent forensic audit

Audit performed: 2026-09-25, approximately 03:16–03:35 UTC (06:46–07:05 Asia/Tehran). This is empirical audit evidence, not a trading-rule specification or a Knowledge Core release declaration.

## Baseline before repair

- Vault Git branch: `main`; HEAD: `96124f6feb3c54dc2dc709d7d8ad347490b5e543`; working tree clean.
- Vault inventory excluding `.git`: 132 files; 75 populated Markdown notes/entities; 27 zero-byte placeholders; 320 typed relations; 6 JSON schemas; 6 index files; 12 mirrored Python files. No untracked or modified files.
- Full pre-change SHA-256 inventory of Vault files, all nine production modules, and both references: `00_SYSTEM/PHASE_4_5_BASELINE.json`. This was written before any existing Vault note was edited.
- Production Git HEAD at audit: `822c5ce1c1e7f464d2e08085fd6d991ee1d5d8ed`. The production working tree was already dirty; its Git HEAD alone is not source identity. An untracked Graphify `last_query_stamp` predated this phase and was not touched.

## Scope and source identity

Audited all 75 populated Vault notes: 7 system, 10 core, 8 market, 15 Behavior, 22 Algorithm, and 13 Source notes. Reviewed 320 original and 264 repaired relation edges, six schemas, index builder, six indexes, 12 mirrors, 27 placeholders, five Obsidian files, and Git tracking. The four `05_MIRROR` files and later-phase files remain zero-byte placeholders.

Re-read current implementation responsibilities and critical rule paths in `reaction_engine.py`, `blue_line_detector.py`, `a_zone_detector.py`, `s_zone_detector.py`, `e_zone_detector.py`, `lifecycle_engine.py`, `trading_pipeline.py`, `direction_policy.py`, and `core_utils.py`; reviewed both synchronized directional references and the chart range-input boundary. Source module notes' 60 named symbol anchors and declared versions were checked against AST/current source. Critical frontmatter anchors were checked for claim relevance; every source reference path and line was also checked mechanically.

| Production module | Declared version | SHA-256 (first 16 hex) |
| --- | --- | --- |
| reaction_engine.py | 9.8.0 | `bea0d5a5e95ee15a` |
| blue_line_detector.py | 2.3.0 | `6fa01d94bc98060b` |
| a_zone_detector.py | 1.6.4 | `d7c33dd619ad7e45` |
| s_zone_detector.py | 4.20.0 | `7714025b3f43087b` |
| e_zone_detector.py | 6.14.2 | `6becc792a17e40f5` |
| lifecycle_engine.py / StopAll | 1.15.6 | `330e26ffc04c24de` |
| trading_pipeline.py | 1.5.1 | `a14b00ef08e3e972` |
| direction_policy.py | 1.0.0 | `a27ac63c2f06631` |
| core_utils.py | 1.0.0 | `3dae390ae77b7296` |

Reference identity: Bullish V5.4.11 HPZR6 SHA-256 `fe9de3f6aaad68aec5f4de53437cb5d0d7398b9d35050d2c825cd0755c762ea0`; Bearish V5.4.11 HPZR6 SHA-256 `7537cb0a8c007e66b24967ab272af53a1e952414ce143c1d38d396951c49adc3`. Both references' nine declared module hashes match the nine current production module bytes. Full hashes and paths are in `_INDEX/source-hashes.json` and the pre-change baseline.

## Verified defects and repairs

| Severity before repair | Finding | Evidence and repair |
| --- | --- | --- |
| MAJOR | Reaction and Reset public key inventories were swapped. | `trading_pipeline.py` L254–280 and both reference serialization sections prove the correct sets. `04_ALGORITHMS/Serialization.md` now has exact Reaction/Reset keys; independent key-set comparison also matched Blue, A, S, E, StopAll, and four Bridge projections. |
| MAJOR | Internal Reaction depended on final Visibility, and E construction depended on its own later reconciliation. | Source classifies Internal Reaction before final filtering; E discovery precedes reconciliation. Removed those `depends_on` edges; retained E↔reconciliation navigation as `relates_to`. All dependency cycles are now absent. |
| MAJOR | `implemented_by`/`implements` conflated detector ownership, bridge orchestration, shared primitives, and Source maps. | Pruned false owners; added `orchestrates` for bridge pass coordination and `supports` for shared utilities. Physical module `implements` is now the inverse of actual Algorithm `implemented_by`. Behavior `calculated_by` and Algorithm `produces` were aligned; lifecycle filtering no longer claims to form A/S/E. |
| MAJOR | Canonical Serialization had `depends_on: algorithm.orderaudit`. | Removed the authoritative edge into pending-fix knowledge. Current OrderAudit serialization is still described as executable/non-canonical evidence. |
| MODERATE | Source-path documentation said `path` while all nine module notes used `source_path`. | Normalized documentation/schema/builder on `source_path`; aggregate Source maps are exempt from physical-module requirements. |
| MODERATE | Schemas accepted unknown fields and the builder did not validate them. | The note schema now rejects unknown/ill-typed metadata, enforces identity/status/authority and module hash fields, and pins OrderAudit quarantine. Specialized schemas plus the builder enforce class relationships, inverse implementation, path normalization, external hashes, and exact mirror/reference inventories. Seven intentionally invalid in-memory examples were rejected. |
| MODERATE | External reference and chart evidence access were implicit. | Chose external canonical-reference model: exact production paths and hashes remain in `_INDEX/source-hashes.json`; retrieval requires access and hash verification. Chart files are explicit external source paths with SHA-256 pinned in `source.integration_boundary`. No uncontrolled second reference copy was created. |
| MODERATE | Integration note labeled a code-path consequence as observed runtime behavior. | Separated normative complete-RAW contract, bridge complete-received-input behavior, chart prefiltering, inferred consequence, and lack of paired runtime comparison. Divergence remains open. |
| MODERATE | Several source anchors pointed to unrelated or blank lines. | Repaired priority table L23→L25, StopAll Type-1 L503→L514, Type-2 L476→L487, S public mapping L1142→L1145, chart integration anchors, and other nearby anchors. Source-map named symbols were checked against AST. |
| MODERATE | `.obsidian/workspace.json` was tracked shared UI state. | Added `.gitignore`; removed only this path from the Git index with `git rm --cached`. Its local file still exists and is ignored. The four shared Obsidian configuration files remain tracked. No commit was made. |
| MINOR | Future type and empty-directory policies were implicit; important human entry links were plain text. | Documented versioned future type addition, zero-byte tracked placeholders/no blanket `.gitkeep`, generated-file ownership, and four verified navigation links in the manifest. |

The suspected physical-module `source_path` mismatch was **not reproduced**: all nine notes already used `source_path`; the error was in system prose/schema strictness. Mirror mismatch, reference hash mismatch, and OrderAudit metadata promotion were **not reproduced**.

## Semantic audit result

Behavior taxonomy remains A/S/E/StopAll only; Reaction, Reset, Blue, Order, OrderAudit, Visibility, Reconciliation, and Serialization remain Algorithms/evidence. A is one Behavior. S Red has no public subtype; Blue Type-1/2/3/4 map simple/advanced/type3/type4. E numbers are recursive state, not separate algorithms. StopAll has exactly the three current public gate mappings. The Order_A/B/C cause labels remain distinct from native Reaction Mode A/B, and physical identity remains `(FirstIndex,BreakIndex)`.

Static comparison with both directional references and owning Source supported the documented Decimal conversion, GREEN Doji classification, directional strict inequalities, lower-timeframe first-event chronology, A/S/E ownership, exact-key Blue repetition, StopAll priority, repeated E reconciliation passes, and final presentation clipping. No new trading rule was added. This audit did not run a strategy regression or paired chart full/partial calculation; semantic confidence is bounded by static source/reference inspection.

OrderAudit remains exactly `pending-fix` and `non-canonical`; no normative graph edge points into it. The dedicated general Leg files remain empty. The chart prefiltering/full-RAW divergence remains open and is not declared correct or incorrect. `05_MIRROR` and later-phase placeholders remain deferred. Nineteen system/core/market context notes have no graph edges by design; they remain addressable by stable ID, and retrieval policy requires global authority-policy bootstrap instead of decorative edges.

## Validation and index evidence

- YAML and JSON Schema parsed all 75 original populated notes with 75 unique IDs before adding this report. Nine module notes' 60 named symbols and versions matched current AST/source. No populated future-phase file was found.
- Independent byte comparison confirmed 12/12 mirrors equal their production files, with identical SHA-256 and sizes; 2/2 reference hashes and both references' 9/9 declared module hashes matched.
- Every repaired relation target resolves; no `depends_on` cycle, no authoritative edge into OrderAudit, and no missing Algorithm implementation inverse remained after repair. Behavior `calculated_by` ↔ Algorithm `produces` pairs were checked.
- Serializer key-set comparison against AST/text found no missing or extra fields for Reaction, Reset, Blue, A, S, E, StopAll, or the four Bridge behavior projections.
- Six JSON schemas and `_SCHEMA/build_indexes.py` were changed. Five frontmatter-derived indexes were regenerated: `entities.json`, `relations.json`, `files.json`, `source-map.json`, `knowledge-graph.json`. `_INDEX/source-hashes.json` stayed byte-identical because no source mirror/reference changed.
- Final builder output: 76 entities (including this empirical audit report), 264 relations, 12 verified mirrors, 2 verified reference hashes. Two consecutive rebuilds produced byte-identical hashes for all six index files. Generated indexes are never manually edited.

## Required known-issue checklist

| Check | Status | Evidence / limit |
| --- | --- | --- |
| Reaction/Reset serialization mapping | FIXED | Exact Source and reference keys match. |
| Internal-Reaction ↔ Visibility dependency cycle | FIXED | Removed reverse dependency; no cycle remains. |
| implemented_by / implements semantics | FIXED | Detector ownership and inverse checked. |
| Source path vs source_path metadata consistency | FIXED | `source_path` is canonical. |
| Schema strictness and useful validation | FIXED | Unknown fields rejected; seven negative cases rejected. |
| Future entity-type readiness | FIXED | Versioned schema extension policy. |
| Algorithm reference availability policy | FIXED | External hash-pinned model explicit. |
| Integration-Boundary authority wording | FIXED | Normative, executable, inferred layers separated. |
| External chart-source dependency representation | FIXED | Two external paths and hashes pinned. |
| Source line-reference accuracy | FIXED | Critical stale anchors corrected; all paths/bounds and 60 symbols checked. |
| OrderAudit pending-fix metadata | PASS | Pending-fix/non-canonical retained and schema-pinned. |
| OrderAudit canonical leakage | FIXED | Authoritative Serialization dependency removed; prose quarantined. |
| Leg deferred-state preservation | PASS | Three dedicated files remain empty. |
| Stable ID uniqueness | PASS | All populated IDs unique and unchanged. |
| Relation target integrity | PASS | All targets resolve. |
| Relation semantic integrity | FIXED | False owners, cycles, and inverse gaps repaired. |
| Index reproducibility | PASS | Two byte-identical rebuilds required at final gate. |
| Source hash integrity | PASS | Nine core module hashes and manifest match. |
| Source mirror byte equality | PASS | 12/12 equal. |
| Reference hash integrity | PASS | 2/2 reference files match; embedded module hashes 9/9 each. |
| Obsidian workspace Git hygiene | FIXED | Local file retained; Git cached removal staged. |
| Empty-directory Git policy | FIXED | Tracked zero-byte placeholders; no blanket `.gitkeep`. |
| Duplicate canonical rules | PASS | Concise summaries retain single Algorithm rule owners; no full competing copies found. |
| Note granularity | PASS | 15 Behaviors, 22 Algorithms, 13 Source notes; no split/merge needed. |
| Retrieval policy usability | FIXED | S Type-4, E2, StopAll, strictness, serialization, Order_C, noncanonical tasks traced. |
| Authority model consistency | FIXED | Conflicts surfaced; lower layers cannot rewrite normative rules. |
| Editing policy completeness | FIXED | Stable IDs, schemas, hashes, relations, quarantine, read-only source covered. |
| Knowledge model accuracy | FIXED | Current entity types, generated evidence, future versioning covered. |
| ID convention consistency | PASS | No ID rename; public type mappings checked. |
| Mirror correctness | PASS | Static directional/invariant rules checked against both references and policy/source; empirical mirror phase deferred. |
| Decimal correctness | PASS | `Decimal(str(value))` and strict decisions checked. |
| Strict inequality correctness | PASS | `<`/`>` paths and equality exclusion checked. |
| Candle color correctness | PASS | GREEN iff close >= open, including Doji. |
| Pipeline order correctness | PASS | Bridge and both references aligned in audited pass order. |
| Reconciliation-pass correctness | PASS | Repeated E passes and single final StopAll verified statically. |
| Visibility-stage correctness | PASS | Calculation eligibility precedes final public filtering. |
| Presentation-range vs calculation-range semantics | PASS | Contract vs received-input divergence explicitly separated. |

## Open items, severity, and gate

| Open item | Severity | Boundary |
| --- | --- | --- |
| Corrected normative OrderAudit contract unavailable | MAJOR, quarantined | No use as accepted trading logic until user supplies/approves correction. |
| General standalone Leg definition absent | MODERATE, deferred | No rule inferred from specific Order/Reaction leg uses. |
| Chart partial-range integration versus complete physical RAW contract | MODERATE, unresolved | Code-path inference documented; paired runtime investigation remains future work. |
| Mirror/validation/data/cases/decision/version/workflow/plugin phases | INFORMATIONAL, deferred | Placeholder files remain empty; no Plugin/MCP runtime built. |
| External reference dependency | INFORMATIONAL, controlled | Future Vault-only reader must obtain hash-matching production references. |

**Integrity Gate: PASS WITH NON-BLOCKING OPEN ITEMS.** No known blocker or material semantic defect remains in the audited Phases 1–4 after these repairs. The unresolved items are visibly isolated from canonical calculation. This is a Knowledge Core v1 candidate, not a release declaration.

## Files changed

The following is the post-repair Git working-tree inventory. `D` on `.obsidian/workspace.json` is a cached/tracked deletion only; the local file remains present.

```text
D  .obsidian/workspace.json
 M 00_SYSTEM/AUTHORITY_MODEL.md
 M 00_SYSTEM/EDITING_POLICY.md
 M 00_SYSTEM/FRONTMATTER_SCHEMA.md
 M 00_SYSTEM/ID_CONVENTIONS.md
 M 00_SYSTEM/KNOWLEDGE_MODEL.md
 M 00_SYSTEM/RETRIEVAL_POLICY.md
 M 00_SYSTEM/VAULT_MANIFEST.md
 M 01_CORE/Core-Invariants.md
 M 01_CORE/Precision.md
 M 01_CORE/Priority.md
 M 03_BEHAVIORS/A.md
 M 03_BEHAVIORS/E/Blue.md
 M 03_BEHAVIORS/E/E.md
 M 03_BEHAVIORS/E/Numbering.md
 M 03_BEHAVIORS/E/Red.md
 M 03_BEHAVIORS/S/Blue-Type-1.md
 M 03_BEHAVIORS/S/Blue-Type-2.md
 M 03_BEHAVIORS/S/Blue-Type-3.md
 M 03_BEHAVIORS/S/Blue-Type-4.md
 M 03_BEHAVIORS/S/Blue.md
 M 03_BEHAVIORS/S/Red.md
 M 03_BEHAVIORS/S/S.md
 M 03_BEHAVIORS/StopAll/StopAll.md
 M 03_BEHAVIORS/StopAll/Type-1.md
 M 03_BEHAVIORS/StopAll/Type-2.md
 M 03_BEHAVIORS/StopAll/Type-3.md
 M 04_ALGORITHMS/A.md
 M 04_ALGORITHMS/Blue.md
 M 04_ALGORITHMS/E.md
 M 04_ALGORITHMS/Lifecycle.md
 M 04_ALGORITHMS/Order/Order-A.md
 M 04_ALGORITHMS/Order/Order-B.md
 M 04_ALGORITHMS/Order/Order-C.md
 M 04_ALGORITHMS/RAW.md
 M 04_ALGORITHMS/Reaction/Internal-Reaction.md
 M 04_ALGORITHMS/Reaction/Reaction.md
 M 04_ALGORITHMS/Reconciliation.md
 M 04_ALGORITHMS/S/S.md
 M 04_ALGORITHMS/S/Type-1.md
 M 04_ALGORITHMS/S/Type-2.md
 M 04_ALGORITHMS/S/Type-3.md
 M 04_ALGORITHMS/S/Type-4.md
 M 04_ALGORITHMS/Serialization.md
 M 04_ALGORITHMS/StopAll.md
 M 06_SOURCE/Dependency-Map.md
 M 06_SOURCE/Integration-Boundary.md
 M 06_SOURCE/Modules/core_utils.md
 M 06_SOURCE/Modules/direction_policy.md
 M 06_SOURCE/Modules/e_zone_detector.md
 M 06_SOURCE/Modules/lifecycle_engine.md
 M 06_SOURCE/Modules/reaction_engine.md
 M 06_SOURCE/Modules/s_zone_detector.md
 M 06_SOURCE/Modules/trading_pipeline.md
 M 06_SOURCE/Source-Map.md
 M 06_SOURCE/State-Map.md
 M _INDEX/entities.json
 M _INDEX/files.json
 M _INDEX/knowledge-graph.json
 M _INDEX/relations.json
 M _INDEX/source-map.json
 M _SCHEMA/algorithm.schema.json
 M _SCHEMA/behavior.schema.json
 M _SCHEMA/build_indexes.py
 M _SCHEMA/case.schema.json
 M _SCHEMA/note.schema.json
 M _SCHEMA/source.schema.json
 M _SCHEMA/test.schema.json
?? .gitignore
?? 00_SYSTEM/PHASE_4_5_AUDIT.md
?? 00_SYSTEM/PHASE_4_5_BASELINE.json
```

Production mutation during Phase 4.5: NONE detected. The final SHA-256 comparison found 0 changes among the nine baseline core modules and two baseline algorithm references (11/11), and the targeted production Git status matched the initial snapshot. The prior Graphify stamp is pre-existing, not a Phase 4.5 mutation.
