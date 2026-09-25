---
id: "data.hash_policy"
type: "data"
data_kind: "hash_policy"
status: "canonical"
authority: "normative"
title: "RAW hash and version policy"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.hash_registry", "data.dataset_manifest", "test.baseline_policy", "test.fixture_registry", "source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L141", "engine/bridge/trading_pipeline.py#L1732"]
source_refs: ["apps/chart/server/raw-resource-store.js#L92"]
---

# RAW hash and version policy

Compute SHA-256 over the entire unchanged RAW file byte stream. Record the hash, size, full path, observed first/last epoch and row count together; a filename alone is insufficient. Identical hashes across Vault/production paths are two locations of one dataset entity. Any byte change creates a new content version and requires reassessing affected fixture and output baselines. Sidecar hashes, when present, are separate metadata evidence and never replace the RAW hash.

The chart RAW store writes `dataSha256` over its serialized JSON bytes in `.meta.json`. For the inspected production files with sidecars, that value matched the direct file hash. The Python bridge parses input bytes but does not by itself make a dataset hash into a complete regression baseline: source fingerprint, scope, timeframe, direction, options, reference version and stable output must also be pinned. See `test.baseline_policy` and [Hashes/Hash-Registry.md](Hashes/Hash-Registry.md).

Do not overwrite an old hash record merely because a longer RAW file shares its beginning or broker/symbol. The 309,906-row XAUUSD Vault snapshot and the 354,698-row production extension are distinct byte streams and separate dataset entities.
