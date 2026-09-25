---
id: "test.stage_profiling"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Stage profiling and timing interpretation"
related_entities: ["test.runtime_benchmark", "test.memory_benchmark", "test.optimization_rules", "core.pipeline", "source.trading_pipeline", "test.output_validation"]
source_reference: []
---

# Stage profiling and timing interpretation

**Definition and purpose.** Attribute measured bridge time to actual executed calls before selecting an optimization target. A label describes a measured call, not a guaranteed once-only conceptual stage.

**Related algorithm and source.** `timed()` adds repeated durations under the same label (`trading_pipeline.py#L55-L63`). `calculate_full_direction_state()` can run E initially and again after S validity, accepted Order context or shared stop reconciliation (`#L1903-L2299`). `prepare_pipeline_state()` prepares both Reaction streams for dependent modules (`#L2300-L2452`). Final visibility and serialization are separate phases. A profiler must respect the actual call order and direction; do not impose the linear diagram in the prompt as runtime instrumentation.

**Procedure.** Capture stage labels and bridge total on the same RAW/settings/source identity as a baseline. Retain per-call traces when available; if only aggregate labels exist, say so. Attribute external loading, parsing, serialization and process startup separately. Identify the slow stage from repeated comparable runs, then trace its owned source before proposing a change.

**Validation relation.** Compare stable output through `test.output_validation` and `test.zero_difference` after any optimization. A timing shift without semantic parity is not a successful optimization.
