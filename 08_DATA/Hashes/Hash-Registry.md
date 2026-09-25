---
id: "data.hash_registry"
type: "data"
data_kind: "hash_registry"
status: "canonical"
authority: "normative"
title: "RAW SHA-256 registry"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.hash_policy", "data.dataset_registry", "data.dataset_manifest", "test.baseline_policy"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/bridge/trading_pipeline.py#L1732"]
---

# RAW SHA-256 registry

These hashes cover physical RAW JSON bytes. They exclude the optional `.meta.json` sidecar. A changed byte or serialized number spelling changes the dataset identity. Recalculate from the file before using a fixture or regression baseline.

| Dataset | SHA-256 | Bytes | Locations |
| --- | --- | ---: | ---: |
| [data.dataset_062df750](../Datasets/Dataset-062df750.md) | `062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6` | 4,495,847 | 2 |
| [data.dataset_9e2e159a](../Datasets/Dataset-9e2e159a.md) | `9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c` | 2,941,746 | 2 |
| [data.dataset_7e12ea5f](../Datasets/Dataset-7e12ea5f.md) | `7e12ea5f56754b2cc408753c34d7a7482de1e8eb0d9773bba577208d16903e17` | 2,368,419 | 1 |
| [data.dataset_0291455b](../Datasets/Dataset-0291455b.md) | `0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776` | 13,189,547 | 2 |
| [data.dataset_f531a06d](../Datasets/Dataset-f531a06d.md) | `f531a06d89e518964d4579f6b126ffdcd2b4f31fe2b6e4828ef71fd122809da3` | 50,789,635 | 1 |
| [data.dataset_ea82be1a](../Datasets/Dataset-ea82be1a.md) | `ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9` | 28,991,710 | 1 |
| [data.dataset_f5bc29e3](../Datasets/Dataset-f5bc29e3.md) | `f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974` | 25,331,244 | 1 |
| [data.dataset_18632e27](../Datasets/Dataset-18632e27.md) | `18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0` | 15,018,536 | 2 |
| [data.dataset_d33c7e2c](../Datasets/Dataset-d33c7e2c.md) | `d33c7e2c46440f7a4495bac7d80b38101a635491f0f95b8ea353caa8fdb7d96d` | 1,156,527 | 1 |
| [data.dataset_b47246b4](../Datasets/Dataset-b47246b4.md) | `b47246b45bb66db9ddfb75b6a431e5b6a7fced5fd521e358e5d5c438f91641dc` | 2,114,937 | 1 |

The production RAW store's `dataSha256` matched the eight present sidecars in this snapshot. The Vault-only long XAUUSD snapshot and production FARAZ 1s file have no matching production sidecar. Hash equality establishes byte identity, not feed completeness, source-code identity or approved behavior.
