---
id: "algorithm.order.c"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Order_C Blue-leg cause"
implemented_by: ["source.e_zone_detector", "source.blue_line_detector", "source.reaction_engine"]
depends_on: ["algorithm.order", "algorithm.blue", "algorithm.reset"]
source_refs: ["engine/pipeline/e_zone_detector.py#L648", "engine/pipeline/e_zone_detector.py#L674", "engine/pipeline/e_zone_detector.py#L727"]
---

# Order_C Blue-leg cause

For each exact same-direction Reset, find its owning Reaction. If owner native Mode A, it is the Leg Start; if Mode B, use latest earlier native Mode A. Require a Reaction immediately preceding that selected Leg Start. Freeze the closed main-candle range from preceding Reaction Break through Leg Start Break inclusive. Bullish LegLow=min Low; Bearish LegHigh=max High; first equal-extreme main candle owns the level. This is a specific Order_C leg interval, not a standalone general Leg definition.

After exact Reset, require earliest calculation-valid non-Internal same-direction Blue with Reaction ordinal >= Reset owner's ordinal. Use Blue formation event: Scale at exact Reaction confirmation, Reset Blue at exact Reset. Wait until strictly after Blue formation and after completion of frozen Leg Start Break main candle. Then find first exact lower event crossing Bullish Low < LegLow or Bearish High > LegHigh. The first canonical opposite Reaction with First in crossing main candle or later and exact confirmation strictly after crossing becomes physical Order_C; reject a hard sequence reset between initial Reset and confirmation.

Store independent blue-leg cause with resetTime, nullable legacy nextBreakoutTime, frozen level/source, Blue source/formation time, strict break event, and both interval Break times. On duplicate physical identity, latest (resetTime,strictBreakTime) origin wins. It does not itself force E or StopAll.
