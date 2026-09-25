---
id: "test.precision_invariants"
type: "test"
status: "canonical"
authority: "normative"
title: "Precision and strictness checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.invariant_validation", "core.precision", "market.crossing", "market.candle", "source.core_utils", "source.direction_policy", "source.blue_line_detector"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py#L11", "06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L19"]
---

# Precision and strictness checks

Normalize non-Decimal prices with Decimal(str(value)); preserve already-Decimal values. No binary-float decision may replace a strict price comparison. For the retained directional trend stop use Bullish Low < level and Bearish High > level; Reaction confirmation uses Bullish High > BoxTop and Bearish Low < BoxBottom. Equality does not satisfy these strict comparisons or the retained Reaction Reset crossing. Check any other stage's equality behavior against its own source when that source becomes available. These local comparisons are grounded in retained `core_utils.py`, `direction_policy.py`, and `reaction_engine.py`.

Check 0.618 Fibonacci and Blue line values under Decimal arithmetic. Market Doji (close == open) is GREEN in either direction; reflected detector-internal color roles do not change market classification. These local calculations are grounded in retained `blue_line_detector.py` and `reaction_engine.py`. Public output string formatting remains pending until the bridge serializer is retained and reviewed.

Use equality and near-boundary fixtures to expose a changed comparison operator; do not invent an expected crossing when a supplied fixture lacks the exact RAW event.
