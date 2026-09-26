---
id: "data.data_validation"
type: "data"
data_kind: "validation"
status: "pending"
authority: "non-canonical"
title: "Dataset validation procedure"
created: "2026-09-25"
updated: "2026-09-26"
related_entities: ["data.integrity", "data.hash_registry", "data.dataset_manifest", "data.dataset_registry", "test.fixture_registry", "test.source_validation", "test.baseline_policy", "algorithm.raw"]
source_reference: []
---

# Dataset validation procedure

For an exact input, verify path and SHA-256 before calculating. Parse the original bytes and check the five-key schema, finite OHLC, positive integer epochs, ordering, duplicates, first/last range and nominal-grid alignment. Compare production sidecar `dataSha256`, byte count and candle count when present. Record any longer-than-nominal intervals as gap candidates; distinguish missing market data from market closures only with independent coverage evidence. Never fill a gap to make a fixture pass.

Then bind a case to the same dataset hash and run settings. Verify lower and main candle chronology, both directional dependencies when the pipeline requires them, final visibility, public serialization and the case's explicit expected assertion. A byte-identical RAW alone does not imply byte-identical output if source, settings, scope or accepted rules differ. `test.baseline_policy` defines the additional evidence needed for a full zero-difference comparison.

The 2026-09-26 inventory confirmation found seven retained physical RAW arrays, five retained physical sidecars, and three reproducible logical windows. It did **not** execute full trading-pipeline regressions or establish provider-session completeness. The FARAZ filename/end-time discrepancy is open, and the Phase 5 Pending cases remain Pending. The Vault index builder checks pinned RAW paths, byte sizes, SHA values, exact window reconstruction, and fixture hash relationships when rebuilding derived indexes.
