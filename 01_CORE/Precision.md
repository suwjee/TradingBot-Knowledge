---
id: "core.precision"
type: "core"
status: "active"
authority: "empirical"
title: "Precision and strictness"
source_refs: ["06_SOURCE/Code/engine/pipeline/core_utils.py#L11", "06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L19"]
related_entities: ["source.core_utils", "test.precision_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py#L11", "06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L19"]
---

# Precision and strictness

The retained helpers normalize price values with Decimal(str(value)). Their directional strict crosses use Bullish Low < level and Bearish High > level. Reaction confirmation uses Bullish High > BoxTop and Bearish Low < BoxBottom. Equality does not satisfy those strict comparisons or the retained Reaction Reset crossing. The retained Blue detector computes its 0.618 Fibonacci level with Decimal. Broader stage rules and public serialization are present in captured source but remain pending/non-canonical because no approved full-output baseline exists and B/C-dependent outcomes need a rewrite.
