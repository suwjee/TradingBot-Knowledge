---
id: "test.optimization_rules"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Performance optimization acceptance rules"
related_entities: ["test.runtime_benchmark", "test.memory_benchmark", "test.stage_profiling", "test.zero_difference", "test.regression_policy", "test.mirror_validation", "core.precision", "core.chronology"]
source_reference: []
---

# Performance optimization acceptance rules

**Definition and purpose.** An optimization is a source change justified by reproducible runtime or memory evidence while preserving the approved calculation contract. This document defines an acceptance gate; it reports no optimization as completed.

**Related algorithm and source.** Changes may affect Reaction through final serialization, including repeated E reconciliation, shared Order ownership, lifecycle and visibility. The bridge's `timings` envelope is telemetry (`trading_pipeline.py#L2942-L2990`), not a trading outcome. Decimal comparisons, strict equality, exact lower chronology, physical Order identity, nulls, ordering, both directions and output schema remain protected by `test.zero_difference` and `test.mirror_validation`.

**Before/after comparison.** Keep identical RAW bytes, scope, flags, timeframes, environment and baseline/candidate source hashes. Record repeated runtime and peak-memory samples, profiling evidence, and complete stable-output comparisons. Treat a source or input mismatch as INCOMPLETE. State the expected speed/memory benefit and observed variance; never hide a semantic difference inside an average.

**Validation relation.** For a pure refactor, stable serialized results must match on the protected corpus. An intentionally changed rule follows `test.regression_policy` with explicit approval and affected-field expectations; it cannot be labelled zero difference.
