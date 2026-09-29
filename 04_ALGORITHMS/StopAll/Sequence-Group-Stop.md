---
id: "algorithm.stopall.sequence_group"
type: "algorithm"
status: "active"
authority: "executable"
title: "StopAll sequence-group-stop gate"
version: "current"
related_entities: ["algorithm.e", "algorithm.stopall"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.e_zone_detector", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269"]
mirror_links: ["mirror.contract"]
---

# StopAll sequence-group-stop gate

## Bullish

#### 12.2 Dominant S/E sequence state

Accepted S/E objects remain valid output even when lower priority prevents them from replacing current dominant sequence ownership. Repeated exact dominant S color or exact E `(family, number)` increments its occurrence count. A higher-priority incoming behavior replaces lower dominant state. For E within equal family priority, a larger same-family number advances the dominant E group; Red E dominates Blue E.

#### 12.3 E-driven StopAll

If an existing active StopAll is strictly stopped before/equal to an incoming E decision, the incoming E constructs the next numbered StopAll and the stopped active StopAll leaves current active ownership. Separately, when the current dominant S or exact E group has at least two accepted occurrences and its owning behavior strictly stops at or before the incoming E decision, that E becomes `StopAll1` through the `sequence-group-stop` gate. The incoming E supplies the physical Order/provenance; its family need not equal the stopped group.

## Bearish

#### 12.2 Dominant S/E sequence state

Accepted S/E objects remain valid output even when lower priority prevents them from replacing current dominant sequence ownership. Repeated exact dominant S color or exact E `(family, number)` increments its occurrence count. A higher-priority incoming behavior replaces lower dominant state. For E within equal family priority, a larger same-family number advances the dominant E group; Red E dominates Blue E.

#### 12.3 E-driven StopAll

If an existing active StopAll is strictly stopped before/equal to an incoming E decision, the incoming E constructs the next numbered StopAll and the stopped active StopAll leaves current active ownership. Separately, when the current dominant S or exact E group has at least two accepted occurrences and its owning behavior strictly stops at or before the incoming E decision, that E becomes `StopAll1` through the `sequence-group-stop` gate. The incoming E supplies the physical Order/provenance; its family need not equal the stopped group.

## Source-level contract

Dominant exact S color or E(family,number) needs >=2 dominant accepted occurrences. Latest prior exact-group member strictly stops from decision; stop <= incoming E decision qualifies. Incoming E creates fresh StopAll1 and supplies physical geometry/Order regardless of family match. Creation clears dominant keys/counts and Blue-repeat evidence; lower-priority accepted output cannot split active dominant group.
