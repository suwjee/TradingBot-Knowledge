---
id: "test.mirror_regression"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Bullish and Bearish mirror regression"
related_entities: ["test.mirror_policy", "test.mirror_validation", "test.direction_tests", "test.symmetry_tests", "test.regression_policy", "test.zero_difference", "mirror.exceptions", "test.output_validation"]
source_reference: []
---

# Bullish and Bearish mirror regression

**Definition and purpose.** Protect both directional calculations against a source change. The baseline for each direction is its own trusted output on the same pinned physical input and settings, not the other direction's naturally observed output.

**Related algorithm and source.** The bridge prepares both Reaction streams for dependent stages (`trading_pipeline.py#L2300-L2452`) and serializes each requested direction later (`#L2776-L2994`). Compare Reaction/Reset, Blue, A, S, E, StopAll, visibility, Order provenance and stable public fields, preserving physical indexes and exact times. Use `test.symmetry_tests` only for a separately constructed reflected input.

**Execution and status.** Pin RAW hash, source/reference hashes, direction, timeframes, flags, scope and baseline artifact. Run both directions, capture exit codes, compare ordered stable payloads and list all differences. Numeric timings are measured separately. If one direction is missing, a baseline is stale, or a required dataset is absent, report INCOMPLETE rather than PASS.

**Validation relation.** `test.regression_policy` governs approved changes and `test.zero_difference` governs refactors. Keep the unresolved mixed-cause visibility claim documented in `mirror.exceptions` out of accepted pass assertions until source/reference ownership is resolved. This note does not claim a fresh run.
