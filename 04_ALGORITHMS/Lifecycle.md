---
id: "algorithm.lifecycle"
type: "algorithm"
status: "active"
authority: "executable"
title: "Accepted lifecycle and cross-stage ownership"
version: "current"
related_entities: ["algorithm.visibility", "core.ownership", "core.priority"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.trading_pipeline", "source.e_zone_detector", "source.s_zone_detector", "source.order_audit_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.a", "algorithm.s", "algorithm.e"]
name: "Lifecycle"
aliases: ["Behavior lifecycle"]
---

# Accepted lifecycle and cross-stage ownership

## Bullish

#### 12.1 Shared priority and directional invariance

Lifecycle family semantics are direction-invariant. The cross-stage priority is exactly:

`StopAll > E Red > S Red > E Blue > S Blue > A`

Within a stage/family, accepted number/source chronology supplies deterministic ties. Directional price movement enters only through the strict Bullish stop predicate.

#### 12.2 Dominant S/E sequence state

Accepted S/E objects remain valid output even when lower priority prevents them from replacing current dominant sequence ownership. Repeated exact dominant S color or exact E `(family, number)` increments its occurrence count. A higher-priority incoming behavior replaces lower dominant state. For E within equal family priority, a larger same-family number advances the dominant E group; Red E dominates Blue E.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets active sequence keys/counts, dominant owners and pending Blue-repeat evidence. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

#### 12.6 Cross-stage A/S/E visibility ownership

A, S and E calculations continue to retain internal historical evidence. Public ownership is resolved from exact strict stops, source chronology and shared priority. A source that strictly extends beyond the newest stopped owner can be consumed as the closed owner's next leg head instead of re-entering as equal/smaller behavior; equality stays with the earlier owner. S under a stopped larger owner obeys analogous chronology-first ownership; a higher-priority Red S may supersede a stopped Blue S, while equal/lower candidates remain owned by the prior lifecycle. Final E/StopAll source occupancy removes duplicate A/S labels on the same physical source, while referenced historical parents are retained for lineage closure.

## Bearish

#### 12.1 Shared priority and directional invariance

Lifecycle family semantics are direction-invariant. The cross-stage priority is exactly:

`StopAll > E Red > S Red > E Blue > S Blue > A`

Within a stage/family, accepted number/source chronology supplies deterministic ties. Directional price movement enters only through the strict Bearish stop predicate.

#### 12.2 Dominant S/E sequence state

Accepted S/E objects remain valid output even when lower priority prevents them from replacing current dominant sequence ownership. Repeated exact dominant S color or exact E `(family, number)` increments its occurrence count. A higher-priority incoming behavior replaces lower dominant state. For E within equal family priority, a larger same-family number advances the dominant E group; Red E dominates Blue E.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets active sequence keys/counts, dominant owners and pending Blue-repeat evidence. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

#### 12.6 Cross-stage A/S/E visibility ownership

A, S and E calculations continue to retain internal historical evidence. Public ownership is resolved from exact strict stops, source chronology and shared priority. A source that strictly extends beyond the newest stopped owner can be consumed as the closed owner's next leg head instead of re-entering as equal/smaller behavior; equality stays with the earlier owner. S under a stopped larger owner obeys analogous chronology-first ownership; a higher-priority Red S may supersede a stopped Blue S, while equal/lower candidates remain owned by the prior lifecycle. Final E/StopAll source occupancy removes duplicate A/S labels on the same physical source, while referenced historical parents are retained for lineage closure.

## Source-level contract

module_priority is StopAll5,E Red4,S Red3,E Blue2,S Blue1,A0. Latest stopped main boundary precedes same-boundary priority/number/source tie. New A trigger > prior A stop is independent; trigger <= old stop overlaps transition.

Strictly extending A may be consumed leg head; equality preserves valid boundary ownership. Earlier more-extreme aligned interior head can preserve an interior A. Rejected A under S cannot consume that S by rejection; descendants are tracked stage-invalid.

Larger active owner does not globally disable half-leg A/S discovery. S exact candidate event owns closed-transition comparison before later stops rewrite it. Historical accepted parents survive for lineage; chart labels do not establish accepted Order_B lifecycle anchors.


## Detailed continuation and visibility owners

Consumed-S continuation compares main-candle Close values and selects the owner under the exact gates in algorithm.reconciliation. Closed S visibility and A provenance apply distinct owner ranks in algorithm.visibility. These functions do not share one universal dominance/stop-time rule. Native S-stage A handoff windows are detailed in algorithm.s and end at the decided native window, rather than the complete later public S lifetime.
