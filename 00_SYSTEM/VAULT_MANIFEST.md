---
id: "system.manifest"
type: "system"
status: "canonical"
authority: "normative"
title: "Vault manifest"
source_refs: []
related_entities: ["system.authority", "core.pipeline", "data.dataset_registry"]
source_reference: []
---

# Vault manifest

This Vault records a scoped TradingBot knowledge snapshot for AI retrieval. Canonical and pending notes have stable IDs. `_INDEX` is derived; `06_SOURCE/Code` holds byte-exact snapshots of all nine main Engine modules, including mixed E, lifecycle and bridge source. `Order_A` is the accepted route. Current `Order_B` and `Order_C` logic is registered as known-invalid diagnostic evidence and excluded from normative reasoning and regression baselines. The full HPZR6 references are registered by hash in `06_SOURCE/References/registry.json` and are optional external evidence; their B/C sections do not define accepted future rules.

Phase 1 covers system controls and the minimum core/market model. Phase 2 covers A, S, E, StopAll. Phase 3 covers the calculation path. Phase 4 maps source modules and captures hashes. Phase 4.8 adds the Mirror layer; Phase 5 adds fixture and validation knowledge; Phase 6 identifies byte-pinned RAW datasets and exact retained windows in `08_DATA`. Plugin runtime code and its documentation live outside this Vault. Empty future directories have no authority. Zero-byte tracked placeholders preserve the selected future folder structure in Git; truly empty directories appear only when populated. No blanket .gitkeep policy is used.

Read [Authority Model](AUTHORITY_MODEL.md) before resolving any rule and [Pipeline](../01_CORE/Pipeline.md) before tracing a stage. The [Source Map](../06_SOURCE/Source-Map.md) identifies retained and pending source owners; [Data Registry](../08_DATA/Dataset-Registry.md) locates physical inputs; [Integration Boundary](../06_SOURCE/Integration-Boundary.md) records the unresolved chart input scope. Resolve IDs through `_INDEX/entities.json`, then open the owning Markdown note. An index never overrides its note.

All operational paths in this Vault are relative to its own root. The retained source came from a dirty working tree; do not infer its identity from a Git commit alone. A later source refresh requires new hashes and review of affected claims. The Vault reader needs no access to the production checkout.

Current open issue: the chart server may send a selected-range stream to the bridge, while full-RAW chronology was assumed by earlier rule descriptions. The retained Vault does not resolve that integration contract. Until the affected source is republished and reviewed, related calculation claims remain pending.
