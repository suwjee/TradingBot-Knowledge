---
id: "data.registry_root"
type: "data"
data_kind: "registry"
status: "canonical"
authority: "normative"
title: "Data registry entry point"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.dataset_registry", "data.dataset_manifest", "data.hash_registry", "data.data_validation", "test.fixture_registry", "algorithm.raw"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/bridge/trading_pipeline.py#L1732"]
---

# Data registry entry point

The current local inventory contains **10 distinct RAW byte streams**: five files in this Vault and nine production RAW files, with four byte-identical copies across the two roots. Six streams are used by the 28 registered Phase 5 cases; four currently have no registered case. These counts describe the inspected files on 2026-09-25, not a promise that the production directory cannot change.

[Datasets/Dataset-Registry.md](Datasets/Dataset-Registry.md) lists the ten dataset entities and links each to its metadata note. [Hashes/Hash-Registry.md](Hashes/Hash-Registry.md) pins SHA-256 identity; [Manifests/Dataset-Manifest.md](Manifests/Dataset-Manifest.md) records byte, row, range and sidecar observations. The [Fixture Registry](../07_VALIDATION/Fixtures/Fixture-Registry.md) is the evidence consumer. A dataset's physical presence does not imply a completed Bullish/Bearish run or a current accepted behavior.

The FARAZ XAUUSD 1-second file is present in production RAW. Its filename's stated terminal epoch differs from its final row, so its dataset entity remains draft until that metadata conflict is resolved. Other absent historical filenames mentioned in legacy memory are not silently mapped to a similarly named file.
