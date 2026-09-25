---
id: "test.precision_invariants"
type: "test"
status: "canonical"
authority: "normative"
title: "Precision and strictness checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.invariant_validation","core.precision","market.crossing","market.candle","source.core_utils","source.direction_policy","source.blue_line_detector"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145","engine/pipeline/core_utils.py#L11","engine/pipeline/direction_policy.py#L32","engine/pipeline/blue_line_detector.py#L19"]
---

# Precision and strictness checks

Normalize non-Decimal prices with Decimal(str(value)); preserve already-Decimal values. No binary-float decision may replace a strict price comparison. For Bullish trend stop use Low < level, Bearish High > level; Reaction confirmation uses Bullish High > BoxTop and Bearish Low < BoxBottom. Equality never confirms, stops, resets or breaks. Both references §§3.2, 3A, 4, 15; core_utils.py lines 11–13; direction_policy.py lines 32–46.

Check 0.618 Fibonacci and Blue line values under Decimal arithmetic, and verify output prices are strings. Market Doji (close == open) is GREEN in either direction; reflected detector-internal color roles do not change market classification. blue_line_detector.py lines 19 and 75–81; reaction_engine.py lines 91–93 and 560–577; trading_pipeline.py lines 239–493.

Use equality and near-boundary fixtures to expose a changed comparison operator; do not invent an expected crossing when a supplied fixture lacks the exact RAW event.

