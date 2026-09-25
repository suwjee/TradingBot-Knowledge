---
id: "data.dataset_registry"
type: "data"
data_kind: "registry"
status: "canonical"
authority: "normative"
title: "Inventory of byte-distinct RAW datasets"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.registry_root", "data.dataset_template", "data.hash_registry", "data.dataset_manifest", "test.fixture_registry", "algorithm.raw"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/bridge/trading_pipeline.py#L1732"]
---

# Inventory of byte-distinct RAW datasets

One row is one SHA-256-identified byte stream. A Vault path and an equal-hash production path are two locations of the same dataset. `1s`/`5s` describes observed RAW resolution; registered examples use a 30s main timeframe. A `draft` row has an unresolved metadata conflict, not a failed OHLC scan.

| Dataset | Symbol / nominal RAW | Rows | Actual Tehran range | Fixtures | Status | Locations |
| --- | --- | ---: | --- | ---: | --- | ---: |
| [data.dataset_062df750](Dataset-062df750.md) | USOIL / 5s | 57,963 | 2026-09-08 07:23:20 Asia/Tehran (+03:30) → 2026-09-12 00:14:55 Asia/Tehran (+03:30) | 3 | active | 2 |
| [data.dataset_9e2e159a](Dataset-9e2e159a.md) | USOIL / 5s | 36,821 | 2026-09-11 02:53:30 Asia/Tehran (+03:30) → 2026-09-15 11:03:45 Asia/Tehran (+03:30) | 3 | active | 2 |
| [data.dataset_7e12ea5f](Dataset-7e12ea5f.md) | USOIL / 5s | 30,935 | 2026-09-21 22:50:00 Asia/Tehran (+03:30) → 2026-09-24 00:26:20 Asia/Tehran (+03:30) | 0 | active | 1 |
| [data.dataset_0291455b](Dataset-0291455b.md) | XAUUSD / 1s | 161,376 | 2026-09-03 19:05:40 Asia/Tehran (+03:30) → 2026-09-08 03:18:28 Asia/Tehran (+03:30) | 2 | active | 2 |
| [data.dataset_f531a06d](Dataset-f531a06d.md) | XAUUSD / 1s | 621,326 | 2026-09-03 19:05:40 Asia/Tehran (+03:30) → 2026-09-15 23:19:44 Asia/Tehran (+03:30) | 0 | draft | 1 |
| [data.dataset_ea82be1a](Dataset-ea82be1a.md) | XAUUSD / 5s | 354,698 | 2026-08-25 03:53:30 Asia/Tehran (+03:30) → 2026-09-23 18:01:15 Asia/Tehran (+03:30) | 0 | active | 1 |
| [data.dataset_f5bc29e3](Dataset-f5bc29e3.md) | XAUUSD / 5s | 309,906 | 2026-08-25 03:53:30 Asia/Tehran (+03:30) → 2026-09-19 00:29:30 Asia/Tehran (+03:30) | 14 | active | 1 |
| [data.dataset_18632e27](Dataset-18632e27.md) | XAUUSD / 5s | 183,741 | 2026-09-03 18:44:00 Asia/Tehran (+03:30) → 2026-09-19 00:29:35 Asia/Tehran (+03:30) | 5 | active | 2 |
| [data.dataset_d33c7e2c](Dataset-d33c7e2c.md) | XAUUSD / 5s | 14,140 | 2026-09-16 22:35:00 Asia/Tehran (+03:30) → 2026-09-17 19:15:35 Asia/Tehran (+03:30) | 0 | active | 1 |
| [data.dataset_b47246b4](Dataset-b47246b4.md) | XAUUSD / 5s | 25,877 | 2026-09-22 11:00:00 Asia/Tehran (+03:30) → 2026-09-24 00:05:40 Asia/Tehran (+03:30) | 1 | active | 1 |

Six datasets are fixture-backed and four are available without a registered case. The FARAZ 1s file is present and has a filename/end-time mismatch; its note is `draft`. For exact paths, hashes, gap observations and sidecar checks, open each dataset note and the [manifest](../Manifests/Dataset-Manifest.md). Do not infer identical output from overlapping or extended time ranges.
