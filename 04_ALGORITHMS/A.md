---
id: "algorithm.a"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "A calculation"
implemented_by: ["source.a_zone_detector", "source.blue_line_detector"]
produces: ["behavior.a"]
depends_on: ["algorithm.blue", "algorithm.reaction", "market.exact_chronology"]
source_refs: ["engine/pipeline/a_zone_detector.py#L219", "engine/pipeline/a_zone_detector.py#L311", "engine/pipeline/a_zone_detector.py#L568"]
---

# A calculation

Ordinary A pairs adjacent calculation-valid Blue states in sorted (reactionNumber,sourceTime,kind) order; a third formation may expire an unresolved pair. Scale Blue forms at exact owning Reaction confirmation; Reset Blue at exact Reset event, but its stop scan begins next main boundary. Blue stop is first strict trend-side crossing of sourceExtreme. Blue-1 must stop before the pair triggers. An open Scale Blue at Blue-2 formation cannot borrow hypothetical inherited stop; an eligible previously stopped Scale or Reset structural chain may use the first aligned Reaction in the allowed window.

For a chained Bullish stopped Blue, inherited minimum Low includes the complete next Reaction Break main candle; Bearish mirrors maximum High with the same endpoint. When both Blue stops overlap, order exact events; equal-time stop-level tie is higher level first Bullish and lower first Bearish. The first validating Reaction confirms at/after trigger; its First is at/after max(Blue stop times). A source is the directional extreme from trigger main open through exact validating confirmation inclusive, never the later Break remainder.

After acceptance, the validating Break closes the Blue pair cycle. Adjacent Blue-2 reuse requires that A itself strictly stops and next Blue forms at/after that stop. Special A pairs invalid Reset Blue with most recent valid Blue when the former's main candle strictly crosses the latter's sourceExtreme; ordinary A ownership and prior A stops can invalidate duplicates. Both routes produce one A behavior.
