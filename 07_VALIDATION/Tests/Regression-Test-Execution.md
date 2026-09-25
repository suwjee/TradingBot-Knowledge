---
id: "test.regression_test_execution"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Regression test execution protocol"
related_entities: ["test.test_model", "test.regression_policy", "test.baseline_policy", "test.zero_difference", "test.integration_test_policy", "test.mirror_regression", "data.hash_policy"]
source_reference: []
---

# Regression test execution protocol

**Definition and purpose.** Execute a protected comparison against an approved prior result, without rewriting the baseline to make a candidate pass. `test.baseline_policy` defines what qualifies as a trusted baseline; this note defines the run sequence.

**Related algorithm and source.** The comparison covers ordered stage collections and bridge serialization (`trading_pipeline.py#L2776-L2994`), physical indexes, exact times, family/number, parent/cause, lifecycle/StopAll and nulls. Numeric timing measurements are excluded from semantic equality, but their envelope contract remains checked.

**Run sequence.** (1) Verify RAW bytes and baseline source/reference hashes. (2) Reproduce the baseline command, settings, scope and both directions. (3) Capture candidate outputs and exit statuses without modifying either payload. (4) Compare all stable fields, missing/extra objects and order. (5) Record precise diffs and causal downstream impact. (6) Report PASS, FAIL or INCOMPLETE with links to run artifacts.

**Validation relation.** A pure refactor requires `test.zero_difference`; an approved rule change follows `test.regression_policy` for specified changed fields and verifies unaffected fields. Pending/Historical fixture assertions cannot become current baselines by repeated execution. This policy records no run as completed.
