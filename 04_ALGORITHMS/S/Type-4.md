---
id: "algorithm.s.type4"
type: "algorithm"
status: "active"
authority: "executable"
title: "S Type-4 public-Blue-qualified aligned continuation"
version: "current"
related_entities: ["algorithm.blue", "algorithm.s", "algorithm.s.type3"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.s_zone_detector", "source.blue_line_detector", "source.reaction_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L138", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L138"]
mirror_links: ["mirror.contract"]
---

# S Type-4 public-Blue-qualified aligned continuation

## Bullish

#### 7.3 Order-free Type-4 S Blue

Type-4 is the same-direction Reaction continuation available after A stop only while no opposite Order has formed. For every aligned Bullish Reaction confirmed before the Order deadline, candidate geometry spans the A-stop main candle through that Reaction Break main candle, inclusive, selects the minimum Low and assigns equality to the **last** candidate candle. Search begins at the maximum of A-stop event, aligned Reaction confirmation and candidate formation event. That lower-timeframe start is inclusive. The next aligned Reaction confirmation and Order deadline are exclusive upper bounds. The first strict Bullish cross creates S Blue only when a public calculation-valid Blue formed from the candidate source through that cross. If a candidate crosses without qualifying Blue, no S is created from it; the next aligned Reaction rebuilds a fresh candidate from the same A-stop origin.

Type-3 and Type-4 are independent. Earlier exact decision event wins; Type-3 owns only a true exact-event tie.

## Bearish

#### 7.3 Order-free Type-4 S Blue

Type-4 is the same-direction Reaction continuation available after A stop only while no opposite Order has formed. For every aligned Bearish Reaction confirmed before the Order deadline, candidate geometry spans the A-stop main candle through that Reaction Break main candle, inclusive, selects the maximum High and assigns equality to the **last** candidate candle. Search begins at the maximum of A-stop event, aligned Reaction confirmation and candidate formation event. That lower-timeframe start is inclusive. The next aligned Reaction confirmation and Order deadline are exclusive upper bounds. The first strict Bearish cross creates S Blue only when a public calculation-valid Blue formed from the candidate source through that cross. If a candidate crosses without qualifying Blue, no S is created from it; the next aligned Reaction rebuilds a fresh candidate from the same A-stop origin.

Type-3 and Type-4 are independent. Earlier exact decision event wins; Type-3 owns only a true exact-event tie.

## Source-level contract

Aligned confirmation is > A stop and < first opposite Order confirmation. Complete A-stop..aligned Break extrema assign equality to last main source. Crossing search begins max(A stop,aligned confirmation,candidate event), ends before min(next aligned confirmation,Order deadline).

Public calculation-valid Blue formation lies [candidate source main time,cross event]. Cross without qualifying Blue emits nothing; next aligned Reaction rebuilds same A-stop origin. Native Blue/type4 has physical Order and opposite Reset null; aligned calculation Reaction is not inserted as opposite Reset provenance.
