---
id: "test.zero_difference"
type: "test"
status: "canonical"
authority: "normative"
title: "Zero-difference refactor rule"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.regression_policy", "test.output_validation", "core.precision", "core.chronology", "algorithm.serialization", "mirror.invariants", "test.runtime_benchmark", "test.memory_benchmark", "test.optimization_rules"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py#L11"]
---

# Zero-difference refactor rule

A performance or structural refactor may reduce runtime, allocations or code complexity only when the stable public result and its prerequisite exact stage semantics remain unchanged on the approved test corpus. Preserve behavior identities and sequence, all event times, lifecycle and StopAll state, physical Order identity/provenance, exact lower chronology, Decimal comparisons, equality ties, visibility and serialized key/value/order/null semantics. This is a validation policy; the public serializer is captured but no full approved output baseline exists, and current B/C-dependent output cannot supply one.

Record a baseline source hash, candidate source hash, identical RAW hash/settings, both-direction results and a field-level or normalized ordered-JSON comparison. The top-level timings envelope is runtime telemetry: require its contract/presence while measuring its numeric values separately. A speedup without output comparison is not zero-difference proof.

Any intentional algorithm change uses the approved-change process in Regression-Policy.md; it is not a zero-difference refactor. An interrupted baseline, missing RAW or unmatched reference hash yields INCOMPLETE.
