---
id: "test.memory_benchmark"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Memory benchmark contract"
related_entities: ["test.runtime_benchmark", "test.stage_profiling", "test.optimization_rules", "test.zero_difference", "source.trading_pipeline", "data.dataset_registry"]
source_reference: []
---

# Memory benchmark contract

**Definition and purpose.** Compare peak process memory under identical input and runtime conditions. The current bridge reads and parses complete supplied RAW bytes in `prepare_market_context()` (`trading_pipeline.py#L1732-L1764`); a data-size or input-scope change therefore invalidates a direct memory comparison.

**Related source and algorithm.** The bridge has stage timing telemetry but no built-in peak-memory field or resident-set baseline. A memory result must come from a named external process monitor or an explicitly instrumented, isolated run. State whether the metric is peak RSS, Python allocation peak, or another measure; these are not interchangeable. Do not write a measured number into canonical knowledge unless a run artifact exists.

**Measurement record.** Record process boundary, sampling tool/version, peak definition, RAW hash, settings, source hash, Python version, host, start/end time and repetitions. Account for cold-start imports separately from steady calculation. Keep the full result set and mark missing/failed samples INCOMPLETE.

**Validation relation.** A lower peak is useful only alongside `test.zero_difference` output parity and `test.runtime_benchmark` for the same input. The benchmark policy does not authorize changing Decimal, chronology, or lifecycle ownership to save memory.
