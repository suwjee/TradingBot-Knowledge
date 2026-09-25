---
id: "data.policy"
type: "data"
data_kind: "policy"
status: "pending"
authority: "non-canonical"
title: "Data knowledge and authority policy"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.dataset_registry", "data.raw_authority", "data.hash_policy", "data.data_validation", "algorithm.raw", "test.fixture_model", "core.chronology"]
source_reference: []
---

# Data knowledge and authority policy

This layer identifies byte-pinned RAW inputs and their provenance, range, shape, integrity observations, and fixture dependencies. It does not decide A/S/E/StopAll rules. `algorithm.raw` owns normalization; the rest of `04_ALGORITHMS` owns calculation; `03_BEHAVIORS` owns public behavior meaning; `07_VALIDATION` owns expected-output decisions. A physical RAW file can be interpreted in Bullish and Bearish runs without duplicating the dataset.

A dataset entity identifies one exact SHA-256 byte stream. Two paths with the same hash are locations of one entity; a changed hash is a different version even if a filename has the same stem. `active`/`empirical` means the file's present bytes and stated integrity checks were observed, not that a trading output passed. `draft`/`non-canonical` records unresolved data metadata, including the FARAZ filename/end-time mismatch. Unknown upstream provenance, market and instrument type remain `unknown` rather than being inferred from a broker token.

Do not rewrite, round, sort, fill gaps in, or relabel the pinned RAW during analysis. Derived candles and presentation windows are separate views. The bridge calculates over the complete input it receives; an upstream prefiltered stream has a different physical scope. The filename and sidecar are useful metadata, while content and verified hash determine actual identity. See [Dataset-Registry.md](Dataset-Registry.md), [RAW-Authority.md](Raw/RAW-Authority.md) and [Data-Validation.md](Data-Validation.md).
