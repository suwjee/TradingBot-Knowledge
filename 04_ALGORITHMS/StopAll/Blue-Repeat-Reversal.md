---
id: "algorithm.stopall.blue_reversal"
type: "algorithm"
status: "active"
authority: "executable"
title: "StopAll opposite-s-group-stop gate"
version: "current"
related_entities: ["algorithm.s", "algorithm.stopall", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.lifecycle_engine", "source.s_zone_detector", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269"]
mirror_links: ["mirror.contract"]
reference_agreement: "ambiguous"
reference_conflicts: ["REF-S-MODE-B"]
---

# StopAll opposite-s-group-stop gate

## Bullish

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

Exact accepted Blue keys are (S,None) and (E,number),each count>=2; different E numbers never add. Incoming accepted S Red must have final order_mode=B. Latest qualified source/time/index owns metadata,then E-over-S and E number tie. Result fresh StopAll1 copies incoming S donor geometry/Order and selected Blue group metadata.

Every accepted Red S clears old Blue even when Mode A cannot promote; accepted Red E/hard StopAll clear too. Older-cycle Blue cannot arm later reversal.


The stronger Reference phrase 'native Mode-B formation Order' has unresolved scope after shared accepted-Order recoloring. See source.reference_consistency; no original subtype/formation guard is added to the executable predicate.
