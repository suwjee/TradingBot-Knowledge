---
id: "mirror.direction_mapping"
type: "mirror"
status: "active"
authority: "executable"
title: "Current directional price and candle-role map"
version: "current"
related_entities: ["mirror.contract", "mirror.invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
---

# Current directional price and candle-role map

| Rule | Bullish | Bearish |
| --- | --- | --- |
| First/context | RED/GREEN | GREEN/RED |
| Reaction confirmation | High>BoxTop | Low<BoxBottom |
| Behavior extreme/stop | minimum Low / Low<level | maximum High / High>level |
| Opposite physical Order stop | High>OrderStop | Low<OrderStop |
| Frozen Order_B boundary/break | LL minimum Low / Low<LL | HH maximum High / High>HH |

Scale Fibonacci is top-0.618*(top-reference) or bottom+0.618*(reference-bottom). Scale rendered line is low+(high-low)/3 or high-(high-low)/3; Reset divisor is5. A/S/E use mirrored extrema with same interval and tie owner.

mirror_candle maps open/close to exact negatives,high=-original low,low=-original high,swaps internal role tag,preserves index/timestamp/display_time. Candidate top/bottom price-source pairs swap/sign,anchor/boundary negate; mode/gate state persists. Original market Doji remains GREEN.
