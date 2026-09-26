---
id: "source.reference_registry"
type: "source"
status: "active"
authority: "empirical"
title: "Directional reference registry"
related_entities: ["algorithm.order.a", "algorithm.order.b", "algorithm.order.c"]
source_reference: []
---

# Directional reference registry

`06_SOURCE/References/registry.json` pins the exact HPZR6 Bullish and Bearish reference names, versions, repository-relative paths, bytes and SHA-256 digests. The full files are deliberately outside this standalone Vault because they include current defective B/C descriptions and an inactive audit section. The plugin can optionally read them from `TRADINGBOT_ENGINE_ROOT`, after byte length and hash verification. Vault-only retrieval needs no production checkout.

The project accepts the immutable first stopped-A Order_A owner described at line 29 in each reference and implemented in the captured S source. The B/C sections describe known-invalid current logic, even where source and reference agree. The audit section is not active knowledge. Registry hashes pin the observed untracked reference files; they are not identified solely by the source Git commit.
