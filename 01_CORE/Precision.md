---
id: "core.precision"
type: "core"
status: "canonical"
authority: "normative"
title: "Precision and strictness"
source_refs: ["engine/pipeline/core_utils.py#L11", "engine/pipeline/direction_policy.py#L32", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L199"]
related_entities: ["source.core_utils", "test.precision_invariants"]
source_reference: ["engine/pipeline/core_utils.py#L11", "engine/pipeline/direction_policy.py#L32", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L199"]
---

# Precision and strictness

Price values normalize to Decimal(str(value)); no binary-float strict comparisons. Strict Bullish directional crosses use Low < level, Bearish High > level. Reaction confirmation uses High > BoxTop for Bullish and Low < BoxBottom for Bearish. Equality never stops, confirms, resets, or breaks. The 0.618 Fibonacci level is Decimal-based. Public Decimal prices serialize as strings.
