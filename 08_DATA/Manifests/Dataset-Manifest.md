---
id: "data.dataset_manifest"
type: "data"
data_kind: "manifest"
status: "pending"
authority: "non-canonical"
title: "Observed RAW inventory manifest"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.dataset_registry", "data.hash_registry", "data.integrity", "data.data_validation", "source.trading_pipeline"]
source_reference: []
---

# Observed RAW inventory manifest

Snapshot date: 2026-09-25. Ten distinct byte streams were inspected; seven are registered as retained physical RAWs and three are exact windows reproducible from their parent files. The three superseded smaller files and sidecars are still on disk pending deletion. Five retained files have matching local metadata sidecars. Each JSON array was checked for five-key rows, increasing positive integer epochs, OHLC bounds and nominal timestamp alignment. The captured byte hashes are in the dataset and window notes; this inventory does not depend on a production directory.

| Dataset | Rows | First epoch | Last epoch | Gaps > nominal | Max gap (s) | Sidecar |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| [data.dataset_062df750](../Datasets/Dataset-062df750.md) | 57,963 | 1788839600 | 1789159495 | 2,753 | 3,665 | matched |
| [data.dataset_9e2e159a](../Datasets/Dataset-9e2e159a.md) | 36,821 | 1789082610 | 1789457625 | 1,310 | 177,365 | matched |
| [data.dataset_7e12ea5f](../Datasets/Dataset-7e12ea5f.md) | 30,935 | 1790018400 | 1790196980 | 2,128 | 3,670 | matched |
| [data.window_0291455b](../Datasets/Window-0291455b.md) | 161,376 | 1788449740 | 1788824908 | 12,132 | 176,481 | window in f531a06d |
| [data.dataset_f531a06d](../Datasets/Dataset-f531a06d.md) | 621,326 | 1788449740 | 1789501784 | 28,387 | 176,481 | absent |
| [data.dataset_ea82be1a](../Datasets/Dataset-ea82be1a.md) | 354,698 | 1787617410 | 1790173875 | 991 | 176,485 | matched |
| [data.dataset_f5bc29e3](../Datasets/Dataset-f5bc29e3.md) | 309,906 | 1787617410 | 1789765170 | 821 | 176,485 | absent |
| [data.window_18632e27](../Datasets/Window-18632e27.md) | 183,741 | 1788448440 | 1789765175 | 535 | 176,485 | window in ea82be1a |
| [data.window_d33c7e2c](../Datasets/Window-d33c7e2c.md) | 14,140 | 1789585500 | 1789659935 | 9 | 3,655 | window in ea82be1a |
| [data.dataset_b47246b4](../Datasets/Dataset-b47246b4.md) | 25,877 | 1790062200 | 1790195740 | 85 | 3,655 | matched |

The `data.window_*` rows are historical observed intervals, not separate files or sidecars. A gap is an adjacent timestamp delta greater than the nominal 1s/5s step; closures and provider coverage were not independently classified. The FARAZ 1s filename says `TO 1789388126`, while its actual last row is `1789501784`; the corresponding dataset remains draft. This manifest is an inspection record, not a trading-output PASS report.
