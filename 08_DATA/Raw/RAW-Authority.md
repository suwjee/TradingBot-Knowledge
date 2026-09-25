---
id: "data.raw_authority"
type: "data"
data_kind: "raw_authority"
status: "pending"
authority: "non-canonical"
title: "Physical RAW authority and scope"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.raw_model", "data.lineage", "data.hash_policy", "core.chronology", "algorithm.raw", "test.baseline_policy", "source.trading_pipeline"]
source_reference: []
---

# Physical RAW authority and scope

The exact input bytes sent to `--data` own calculation chronology. On a direct full-file invocation, `prepare_market_context` reads and normalizes the complete RAW, and `--from-time`/`--to-time` are presentation boundaries applied after calculation. Earlier or later rows may resolve an open Reaction, Blue or behavior. Physical indexes are based on that full received input.

The chart middleware can instead send an in-memory selected-range stream for a partial request. The bridge then calculates over that stream as its complete input, without history outside it. Record input scope and hash of the actual supplied bytes before comparing outputs; a partial stream is not the same dataset calculation as the full file merely because it originated from the same RAW path.

Do not edit source RAW to reconcile a case, fill an interval, rename a row or change price precision. A view, normalized candle array or sidecar is not the original. The dataset's SHA-256 pins physical bytes; algorithm rules and final behavior authority remain in their separate layers.
