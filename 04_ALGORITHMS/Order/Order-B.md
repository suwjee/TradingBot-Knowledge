---
id: "algorithm.order.b"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Order_B Reset-leg cause"
implemented_by: ["source.e_zone_detector"]
depends_on: ["algorithm.order", "algorithm.reset", "algorithm.reaction"]
source_refs: ["engine/pipeline/e_zone_detector.py#L390", "engine/pipeline/e_zone_detector.py#L499", "engine/pipeline/e_zone_detector.py#L1143"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/e_zone_detector.py#L390", "engine/pipeline/e_zone_detector.py#L499", "engine/pipeline/e_zone_detector.py#L1143"]
---

# Order_B Reset-leg cause

Order_B begins at a same-direction Reaction Reset. Resolve its owner via from_first_idx. On the closed owner Break main candle .. Reset main candle interval, Bullish selects maximum High as trigger ceiling; Bearish minimum Low as trigger floor. Equal extrema keep the first main candle. From exact Reset time, find first strict Bullish High > ceiling or Bearish Low < floor. Equality fails.

The evidence interval is closed from trigger-extreme source main candle through strict-break main candle. Require bounded raw opposite Reaction geometry wholly in that interval; geometry alone suffices, independent of normal Reset validity, public/Internal classification, or lifecycle. Over the same closed interval retain the opposite edge (Bullish minimum Low, Bearish maximum High), with source. The first canonical opposite Reaction whose First is in strict-break main candle or later and exact confirmation is strictly after the lower gate becomes physical Order_B; native mode may be A/B.

Persist reset-leg cause with exact resetTime and strict boundaryBreakTime. If several valid Reset origins reach the same identity, latest (resetTime,strictBreakEventTime) wins, preserving independent parent-stop/blue-leg causes. The later narrow public internal-Order filter does not alter geometry proof.
