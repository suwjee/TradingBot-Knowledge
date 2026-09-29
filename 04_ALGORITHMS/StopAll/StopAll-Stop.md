---
id: "algorithm.stopall.stopall_stop"
type: "algorithm"
status: "active"
authority: "executable"
title: "StopAll stopall-stop continuation gate"
version: "current"
related_entities: ["algorithm.e", "algorithm.stopall"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.e_zone_detector", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269"]
mirror_links: ["mirror.contract"]
---

# StopAll stopall-stop continuation gate

## Bullish

#### 12.3 E-driven StopAll

If an existing active StopAll is strictly stopped before/equal to an incoming E decision, the incoming E constructs the next numbered StopAll and the stopped active StopAll leaves current active ownership. Separately, when the current dominant S or exact E group has at least two accepted occurrences and its owning behavior strictly stops at or before the incoming E decision, that E becomes `StopAll1` through the `sequence-group-stop` gate. The incoming E supplies the physical Order/provenance; its family need not equal the stopped group.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets active sequence keys/counts, dominant owners and pending Blue-repeat evidence. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

## Bearish

#### 12.3 E-driven StopAll

If an existing active StopAll is strictly stopped before/equal to an incoming E decision, the incoming E constructs the next numbered StopAll and the stopped active StopAll leaves current active ownership. Separately, when the current dominant S or exact E group has at least two accepted occurrences and its owning behavior strictly stops at or before the incoming E decision, that E becomes `StopAll1` through the `sequence-group-stop` gate. The incoming E supplies the physical Order/provenance; its family need not equal the stopped group.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets active sequence keys/counts, dominant owners and pending Blue-repeat evidence. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

## Source-level contract

Active StopAll stops <= incoming E decision qualify. New number=max(stopped active number)+1; gate event=min(qualifying stops); stopped count=qualifying active count. Incoming E donates geometry/Order. Stopped active identities leave current ownership,history remains. This gate precedes sequence-group-stop and clears sequence/Blue-repeat state.
