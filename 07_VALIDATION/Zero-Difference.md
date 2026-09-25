---
id: "test.zero_difference"
type: "test"
status: "canonical"
authority: "normative"
title: "Zero-difference refactor rule"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.regression_policy","test.output_validation","core.precision","core.chronology","algorithm.serialization","mirror.invariants"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1080","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1080","engine/pipeline/core_utils.py#L11","engine/bridge/trading_pipeline.py#L2942"]
---

# Zero-difference refactor rule

A performance or structural refactor may reduce runtime, allocations or code complexity only when the stable public result and its prerequisite exact stage semantics remain unchanged on the approved test corpus. Preserve behavior identities and sequence, all event times, lifecycle and StopAll state, physical Order identity/provenance, exact lower chronology, Decimal comparisons, equality ties, visibility and serialized key/value/order/null semantics. Both references §§3A, 17–19; core_utils.py line 11; trading_pipeline.py lines 239–493.

Record a baseline source hash, candidate source hash, identical RAW hash/settings, both-direction results and a field-level or normalized ordered-JSON comparison. The top-level timings envelope is runtime telemetry: require its contract/presence while measuring its numeric values separately. A speedup without output comparison is not zero-difference proof.

Any intentional algorithm change uses the approved-change process in Regression-Policy.md; it is not a zero-difference refactor. An interrupted baseline, missing RAW or unmatched reference hash yields INCOMPLETE.
