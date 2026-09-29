---
id: "algorithm.s.type3"
type: "algorithm"
status: "active"
authority: "executable"
title: "S Type-3 opposite-Reset continuation"
version: "current"
related_entities: ["algorithm.reset", "algorithm.s", "algorithm.s.type4"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.s_zone_detector", "source.reaction_engine", "source.order_audit_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L138", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L138"]
mirror_links: ["mirror.contract"]
---

# S Type-3 opposite-Reset continuation

## Bullish

#### 7.2 Order-free Type-3 S Blue

Type-3 is an opposite-Reset-leg route available after A stop and before the first Order deadline. The opposite Reaction owning the Reset must have confirmed by the A-stop event and must not already have Reset before that A stop. Candidate geometry spans the **complete opposite Reaction Break main candle through the Reset main candle**, inclusive, and selects the minimum Low with **last-candle ownership on equality**. After Reset, the first strict Bullish cross of that candidate wins only if at least one ordinary same-direction Reaction confirms after A stop and no later than the cross. Earliest valid Type-3 decision wins.

## Bearish

#### 7.2 Order-free Type-3 S Blue

Type-3 is an opposite-Reset-leg route available after A stop and before the first Order deadline. The opposite Reaction owning the Reset must have confirmed by the A-stop event and must not already have Reset before that A stop. Candidate geometry spans the **complete opposite Reaction Break main candle through the Reset main candle**, inclusive, and selects the maximum High with **last-candle ownership on equality**. After Reset, the first strict Bearish cross of that candidate wins only if at least one ordinary same-direction Reaction confirms after A stop and no later than the cross. Earliest valid Type-3 decision wins.

## Source-level contract

Opposite Reset is strictly after A stop and before first immutable opposite Order confirmation. Opposite owner confirms <= A stop and first Reset > A stop. Candidate complete Break..Reset uses last-on-equality. Crossing window includes Reset event and excludes Order deadline; ordinary aligned confirmation must be > A stop and <= cross.

Native Blue/type3 has all physical Order fields null and exact opposite reset owner/time explicit. Earliest exact decision wins; true tie vs Type-4 belongs to Type-3. Later accepted-Order reconciliation may recolor subtype while retaining frozen source/price.
