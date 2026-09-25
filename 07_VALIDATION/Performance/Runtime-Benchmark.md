---
id: "test.runtime_benchmark"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Runtime benchmark contract"
related_entities: ["test.stage_profiling", "test.memory_benchmark", "test.optimization_rules", "test.zero_difference", "test.regression_policy", "source.trading_pipeline", "data.dataset_registry"]
source_reference: []
---

# Runtime benchmark contract

**Definition and purpose.** Measure elapsed time for an exact TradingBot input so a proposed optimization can be compared on the same work. A timing result is performance evidence, not a trading-rule or correctness result.

**Related algorithm and source.** The bridge accumulates labelled stage durations with `perf_counter` in `timed()` (`trading_pipeline.py#L55-L63`) and emits `timings.stagesMs` plus `bridgeTotalMs` (`#L2986-L2990`). Repeated passes of E and other stages are separate measured calls; a report must keep their labels and may sum them only when it says so. The telemetry is not a complete wall-clock measurement of the chart HTTP request.

**Measurement record.** Pin RAW SHA-256, input scope, timeframe, direction, enabled stages, source/reference hashes, command, Python and host environment, warm-up policy and repeated-run count. Record each run and a stated summary statistic; compare like with like. A changed input or settings is a different benchmark. Do not treat one noisy run as an established speedup.

**Validation relation.** `test.zero_difference` must compare stable outputs for both directions before an optimization is accepted. Numeric elapsed values are excluded from byte-equal payload comparison, while timing field presence and shape remain checked. See `test.stage_profiling` and `test.optimization_rules`.
