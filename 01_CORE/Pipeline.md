---
id: "core.pipeline"
type: "core"
status: "pending"
authority: "non-canonical"
title: "Calculation pipeline"
relates_to: ["source.integration_boundary"]
source_refs: []
related_entities: ["source.trading_pipeline", "test.validation_contract"]
source_reference: []
---

# Calculation pipeline

1. Bridge parses its entire received JSON, collapses exact-second duplicate rows, builds main timeframe buckets and a shared lower-timeframe index. It computes visible index bounds separately.
2. When behavior modules run, both Bullish and Bearish Reaction/Reset streams are calculated and cross-direction Internal Reactions classified.
3. Per requested direction, Blue -> A -> S -> provisional E run. Lifecycle filters S and may rebuild E. A stop/cycle ownership invalidates some A/S; accepted stopped-A Order context rebuilds E. Shared accepted Order stops may recolor S Red and trigger another E rebuild. Suppressed S may continue a stopped larger E.
4. Final visibility detects StopAll once from reconciled E/S, restores eligible independent E roots, resolves A/S/E lineage and same-source occupancy, filters public Blue/internal Orders, prepares OrderAudit, clips presentation, then serializes.

The repeated E passes are dependency reconciliation, not duplicate output stages. StopAll is not in a global E/StopAll fixed point.

For retrieval, the conceptual dependency chain is **RAW → Reaction/Reset → Blue → A → S → E → reconciliation → lifecycle/StopAll → visibility → OrderAudit → serialization**. Reset is part of the Reaction stream rather than an independent bridge pass. The bridge performs lifecycle-related checks before final E as well as during final visibility; StopAll is detected within final visibility. OrderAudit evidence is prepared after ownership resolution. This chain is a navigation map, while steps 1–4 above record actual execution and repeated passes. See `test.integration_test_policy` for the full-input boundary.
