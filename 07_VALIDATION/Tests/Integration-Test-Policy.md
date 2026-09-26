---
id: "test.integration_test_policy"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Full pipeline integration test policy"
related_entities: ["test.test_model", "test.unit_test_policy", "test.regression_test_execution", "test.mirror_validation", "test.output_validation", "core.pipeline", "source.integration_boundary", "data.dataset_registry"]
source_reference: []
---

# Full pipeline integration test policy

**Definition and purpose.** An integration check validates public outcomes and provenance across dependent stages on one exact input. It includes Reaction/Reset, Blue, A, S, E, Order reconciliation, StopAll, visibility and serialization where enabled. Audit output may be inspected as raw executable output, but has no active Vault validation authority.

**Related algorithm and source.** `prepare_market_context()` receives the complete supplied input (`trading_pipeline.py#L1732`); `prepare_pipeline_state()` builds the dependent Reaction streams (`#L2300`); final visibility and serialization run later (`#L2549`, `#L2776`). The engine's actual E rebuilds and StopAll ownership are not a single-pass copy of the conceptual stage list. Test both directions and retain full physical indexes/timestamps.

**Scope rule.** A chart partial-range request passes a filtered input to the same bridge. It starts with the chronology of that supplied range; it is not equivalent to a full-RAW calculation clipped for display. Record which path and RAW scope were used. Do not compare their outputs as if the inputs were identical.

**Validation relation.** Pin RAW hash, timeframe, flags, source/reference hashes and full stable output. Assert upstream causes and downstream visibility together; a count-only comparison is insufficient. `test.mirror_validation` and `test.output_validation` cover directional and serialization contracts. No fresh integration run is claimed by this policy.
