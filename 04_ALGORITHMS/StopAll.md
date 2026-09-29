---
id: "algorithm.stopall"
type: "algorithm"
status: "active"
authority: "executable"
title: "StopAll sequence gates and hard cycle boundary"
version: "current"
related_entities: ["algorithm.stopall.blue_reversal", "algorithm.stopall.sequence_group", "algorithm.stopall.stopall_stop", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.e_zone_detector", "source.trading_pipeline", "source.order_audit_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.lifecycle"]
name: "StopAll"
aliases: ["Stop All"]
reference_agreement: "ambiguous"
reference_conflicts: ["REF-S-MODE-B"]
---

# StopAll sequence gates and hard cycle boundary

## Bullish

#### 12.1 Shared priority and directional invariance

Lifecycle family semantics are direction-invariant. The cross-stage priority is exactly:

`StopAll > E Red > S Red > E Blue > S Blue > A`

Within a stage/family, accepted number/source chronology supplies deterministic ties. Directional price movement enters only through the strict Bullish stop predicate.

#### 12.2 Dominant S/E sequence state

Accepted S/E objects remain valid output even when lower priority prevents them from replacing current dominant sequence ownership. Repeated exact dominant S color or exact E `(family, number)` increments its occurrence count. A higher-priority incoming behavior replaces lower dominant state. For E within equal family priority, a larger same-family number advances the dominant E group; Red E dominates Blue E.

#### 12.3 E-driven StopAll

If an existing active StopAll is strictly stopped before/equal to an incoming E decision, the incoming E constructs the next numbered StopAll and the stopped active StopAll leaves current active ownership. Separately, when the current dominant S or exact E group has at least two accepted occurrences and its owning behavior strictly stops at or before the incoming E decision, that E becomes `StopAll1` through the `sequence-group-stop` gate. The incoming E supplies the physical Order/provenance; its family need not equal the stopped group.

#### 12.4 Exact Blue-repeat reversal gate

Blue-repeat evidence is **accepted-occurrence counting**, independent of dominant-owner transitions:

- all S Blue occurrences share exact key `S` regardless of S subtype;
- every numbered E Blue has its own key: `E1`, `E2`, `E3`, ...;
- different E numbers never add together;
- a key qualifies only at count `>= 2`;
- the incoming reversal must be an accepted **S Red whose final accepted `order_mode` is `B`**;
- among qualified keys, the latest accepted qualifying occurrence owns deterministic metadata;
- any accepted Red S, accepted Red E, or hard StopAll boundary clears prior Blue-repeat evidence, so stale Blue evidence cannot be consumed later.

A qualifying S Red is promoted to fresh `StopAll1` through `opposite-s-group-stop`. S/Red/Blue labels are not direction-mirrored.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets active sequence keys/counts, dominant owners and pending Blue-repeat evidence. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

## Bearish

#### 12.1 Shared priority and directional invariance

Lifecycle family semantics are direction-invariant. The cross-stage priority is exactly:

`StopAll > E Red > S Red > E Blue > S Blue > A`

Within a stage/family, accepted number/source chronology supplies deterministic ties. Directional price movement enters only through the strict Bearish stop predicate.

#### 12.2 Dominant S/E sequence state

Accepted S/E objects remain valid output even when lower priority prevents them from replacing current dominant sequence ownership. Repeated exact dominant S color or exact E `(family, number)` increments its occurrence count. A higher-priority incoming behavior replaces lower dominant state. For E within equal family priority, a larger same-family number advances the dominant E group; Red E dominates Blue E.

#### 12.3 E-driven StopAll

If an existing active StopAll is strictly stopped before/equal to an incoming E decision, the incoming E constructs the next numbered StopAll and the stopped active StopAll leaves current active ownership. Separately, when the current dominant S or exact E group has at least two accepted occurrences and its owning behavior strictly stops at or before the incoming E decision, that E becomes `StopAll1` through the `sequence-group-stop` gate. The incoming E supplies the physical Order/provenance; its family need not equal the stopped group.

#### 12.4 Exact Blue-repeat reversal gate

Blue-repeat evidence is **accepted-occurrence counting**, independent of dominant-owner transitions:

- all S Blue occurrences share exact key `S` regardless of S subtype;
- every numbered E Blue has its own key: `E1`, `E2`, `E3`, ...;
- different E numbers never add together;
- a key qualifies only at count `>= 2`;
- the incoming reversal must be an accepted **S Red whose final accepted `order_mode` is `B`**;
- among qualified keys, the latest accepted qualifying occurrence owns deterministic metadata;
- any accepted Red S, accepted Red E, or hard StopAll boundary clears prior Blue-repeat evidence, so stale Blue evidence cannot be consumed later.

A qualifying S Red is promoted to fresh `StopAll1` through `opposite-s-group-stop`. S/Red/Blue labels are not direction-mirrored.

#### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets active sequence keys/counts, dominant owners and pending Blue-repeat evidence. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

## Source-level contract

Current gate_type values are sequence-group-stop,stopall-stop,opposite-s-group-stop. number is lifecycle occurrence,not a numeric subtype. Source-order walk tests active StopAll stops then repeated dominant sequence for incoming E; independent Blue accepted counts can reverse after last E.

E constructor donates geometry/Order from incoming E; reversal uses incoming accepted S Red with final order_mode=B. stopped_behavior_* is gate owner; donor_* is immutable exact constructor provenance and cannot affect trading selection. First strict StopAll stop scans decision inclusive or stays null. One-pass reconcile publishes sequence_resets[source_time]=number without future prefix rebuild.

Publishing sequence_resets atomically copies its map, refreshes sorted reset times and clears dependent candidate/carried context caches once. Immutable physical stop/cross caches and historical accepted Order_A causes remain retained. The reset lookup window is (start,end]. Explicit invalid S identities are rejected at parent registration and reconstructed parent-stop cause retention; valid historical S and shared Order_B reset-leg provenance remain eligible.


The stronger Reference phrase 'native Mode-B formation Order' has unresolved scope after shared accepted-Order recoloring. See source.reference_consistency; no original subtype/formation guard is added to the executable predicate.
