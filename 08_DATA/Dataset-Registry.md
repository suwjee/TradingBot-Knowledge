---
id: "data.registry_root"
type: "data"
data_kind: "registry"
status: "pending"
authority: "non-canonical"
title: "Data registry entry point"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.dataset_registry", "data.dataset_manifest", "data.hash_registry", "data.data_validation", "test.fixture_registry", "algorithm.raw"]
source_reference: []
---

# Data registry entry point

The current registry has **seven retained physical RAW files** and **three exact, hash-verified windows** within larger files. The three superseded smaller files and their sidecars still occupy the Vault directory pending deletion; no active dataset or fixture points to them. Six retained files support the 22 retained fixture cases; one currently has no registered case. These counts describe the selected inventory, not the mutable production directory.

[Datasets/Dataset-Registry.md](Datasets/Dataset-Registry.md) lists physical datasets and retained windows. [Hashes/Hash-Registry.md](Hashes/Hash-Registry.md) distinguishes full-file SHA-256 from window SHA-256; [Manifests/Dataset-Manifest.md](Manifests/Dataset-Manifest.md) records observed ranges. The [Fixture Registry](../07_VALIDATION/Fixtures/Fixture-Registry.md) is the evidence consumer. A dataset's physical presence does not imply a completed Bullish/Bearish run or a current accepted behavior.

The FARAZ XAUUSD 1-second file is present in production RAW. Its filename's stated terminal epoch differs from its final row, so its dataset entity remains draft until that metadata conflict is resolved. Other absent historical filenames mentioned in legacy memory are not silently mapped to a similarly named file.
