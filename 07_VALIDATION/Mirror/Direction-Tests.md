---
id: "test.direction_tests"
type: "test"
status: "canonical"
authority: "normative"
title: "Directional rule checks"
related_entities: ["test.mirror_policy", "test.mirror_validation", "test.symmetry_tests", "mirror.direction_mapping", "mirror.directional_rules", "test.precision_invariants", "source.direction_policy"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
---

# Directional rule checks

**Definition and purpose.** Check each direction against its own accepted rule and exact physical event. Natural Bullish and Bearish outputs on the same market data are not expected to be identical.

**Related algorithm and source.** Bullish trend invalidation uses Low/minimum with strict Low < level; Bearish uses High/maximum with strict High > level. Reaction confirmation uses Bullish High > BoxTop and Bearish Low < BoxBottom. Equality is no crossing. Inspect `direction_policy.py#L21-L70` and the reflected Reaction path in `reaction_engine.py#L560-L703`; retain the market Doji classification separately from internal reflection roles.

**Cases and evidence.** Include equality, just-crossed, same-main-candle lower-event order, missing candidate and accepted candidate for each rule under test. Record RAW hash, full timestamp, main/lower index, source/reference anchors, flags and observed fields. Check downstream A/S/E/StopAll only when the stage depends on the directional event.

**Validation relation.** Use `test.symmetry_tests` only for constructed reflection; use `test.mirror_regression` to protect complete directional outputs. Do not generalize a single inverse formula across source-confirmed exceptions in `mirror.exceptions`.
