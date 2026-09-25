---
id: "test.mirror_policy"
type: "test"
status: "canonical"
authority: "normative"
title: "Mirror validation routing policy"
related_entities: ["test.mirror_validation", "test.direction_tests", "test.symmetry_tests", "test.mirror_regression", "mirror.contract", "mirror.exceptions", "test.zero_difference"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
---

# Mirror validation routing policy

**Definition and purpose.** This policy routes a directional claim to the relevant check under `Mirror/`; it does not duplicate detector calculations. `test.mirror_validation` owns the shared procedure and `mirror.contract` owns the direction-transformation knowledge.

**Related algorithm and source.** Direction tests compare the strict Bullish and Bearish rules at their own physical events. Constructed symmetry tests reflect OHLC while preserving time and index. Mirror regression checks both complete payloads and stable invariants. Current direction policy and reflected Reaction coordinates are in `direction_policy.py#L21-L70` and `reaction_engine.py#L560-L703`.

**Validation relation.** A passing claim needs exact input hashes, settings, two directional outputs, an asserted transformation, and recorded differences. The unresolved mixed-cause final visibility claim is documented in `mirror.exceptions` and remains outside accepted pass criteria until its source and reference are retained. An unrun test is not PASS.
