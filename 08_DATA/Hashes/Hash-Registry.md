---
id: "data.hash_registry"
type: "data"
data_kind: "hash_registry"
status: "pending"
authority: "non-canonical"
title: "RAW SHA-256 registry"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.hash_policy", "data.dataset_registry", "data.dataset_manifest", "test.baseline_policy"]
source_reference: []
---

# RAW SHA-256 registry

`data.dataset_*` hashes cover retained physical RAW JSON bytes. `data.window_*` hashes cover the exact compact JSON serialization of the inclusive candle slice in their retained parent RAW; they reproduce the former smaller file byte for byte. The hashes exclude optional `.meta.json` sidecars. Recalculate the file and any selected window before using a fixture or regression baseline.

| Dataset or window | SHA-256 | Bytes | Copies or parent |
| --- | --- | ---: | ---: |
| [data.dataset_062df750](../Datasets/Dataset-062df750.md) | `062df750514715ecc57ff6e5c16c4c36fc4d8ed3020620654a505b3eeffc9ea6` | 4,495,847 | 2 |
| [data.dataset_9e2e159a](../Datasets/Dataset-9e2e159a.md) | `9e2e159ae32976db8a88a9642414bceb46b0fdba0935a32caee7969036f10c2c` | 2,941,746 | 2 |
| [data.dataset_7e12ea5f](../Datasets/Dataset-7e12ea5f.md) | `7e12ea5f56754b2cc408753c34d7a7482de1e8eb0d9773bba577208d16903e17` | 2,368,419 | 1 |
| [data.window_0291455b](../Datasets/Window-0291455b.md) | `0291455b94b2a536b75b6129f3a90b71cd2eadb40a6a685f8a4e01dc2e744776` | 13,189,547 | parent f531a06d |
| [data.dataset_f531a06d](../Datasets/Dataset-f531a06d.md) | `f531a06d89e518964d4579f6b126ffdcd2b4f31fe2b6e4828ef71fd122809da3` | 50,789,635 | 1 |
| [data.dataset_ea82be1a](../Datasets/Dataset-ea82be1a.md) | `ea82be1aa715f266dab711b6f65139780402afa0529d6fcedde7cc579fdad7f9` | 28,991,710 | 1 |
| [data.dataset_f5bc29e3](../Datasets/Dataset-f5bc29e3.md) | `f5bc29e3ccb08b1cfb322c0ad2c86c0585949c8e0918b63b2e7837b795446974` | 25,331,244 | 1 |
| [data.window_18632e27](../Datasets/Window-18632e27.md) | `18632e270173105be865ea00608290bb70de2c8129e3622c6dcab1e7f1225ee0` | 15,018,536 | parent ea82be1a |
| [data.window_d33c7e2c](../Datasets/Window-d33c7e2c.md) | `d33c7e2c46440f7a4495bac7d80b38101a635491f0f95b8ea353caa8fdb7d96d` | 1,156,527 | parent ea82be1a |
| [data.dataset_b47246b4](../Datasets/Dataset-b47246b4.md) | `b47246b45bb66db9ddfb75b6a431e5b6a7fced5fd521e358e5d5c438f91641dc` | 2,114,937 | 1 |

The three window rows are historical SHA-256 identities, not separate physical locations; their parent paths and exact epochs are in their notes. The retained physical sidecars match their RAWs. Hash equality establishes byte identity, not feed completeness, source-code identity or approved behavior.
