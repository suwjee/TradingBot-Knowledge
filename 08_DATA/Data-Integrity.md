---
id: "data.integrity"
type: "data"
data_kind: "integrity"
status: "pending"
authority: "non-canonical"
title: "Data integrity checks and observed limits"
created: "2026-09-25"
updated: "2026-09-26"
related_entities: ["data.raw_schema", "data.hash_registry", "data.dataset_manifest", "data.data_validation", "test.chronology_invariants", "source.trading_pipeline"]
source_reference: []
source_refs: ["06_SOURCE/Code/apps/chart/server/raw-resource-store.js#L13"]
---

# Data integrity checks and observed limits

Check that the file exists, bytes match its SHA-256, JSON is a nonempty array, each row has exactly the five known keys, `time` is a positive integer epoch second, OHLC are finite numeric values and `low <= open,close <= high`. Check strictly increasing timestamps for chart-store compatible RAW. The production chart store enforces these constraints on write (`raw-resource-store.js#L13-L22`); the bridge itself collapses same-second rows but should not be treated as a general unsorted-data repairer.

At the 2026-09-26 inventory confirmation, the seven retained physical byte streams contained no duplicate adjacent timestamps, reverse timestamp steps, off-grid timestamp or OHLC violations. The three registered logical windows reconstruct their pinned former byte streams from retained parents. All recorded inputs have gaps longer than their nominal 1s/5s step; without provider-session coverage, a gap is a candidate for investigation, not a proven missing candle. The exact count and maximum gap for each physical dataset/window are in [Manifests/Dataset-Manifest.md](Manifests/Dataset-Manifest.md).

For the five retained physical sidecars, observed `dataSha256`, `candleCount` and byte count agree with their RAW. The FARAZ 1s file and the 309,906-row XAUUSD snapshot have no sidecar. The FARAZ filename claims terminal epoch `1789388126`, whereas the final row is `1789501784`, so filename metadata is pending. A matching hash proves identity/integrity of present bytes, not completeness of the external market feed or correctness of every strategy output.
