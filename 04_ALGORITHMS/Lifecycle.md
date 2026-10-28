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
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L375", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L375"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.a", "algorithm.s", "algorithm.e"]
name: "Lifecycle"
aliases: ["Behavior lifecycle"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Accepted lifecycle and cross-stage ownership

## Bullish

### 12.1 Exact S/E dominance priority

The complete dominance priority for S/E behavior is `S Blue < E Blue < S Red < E Red`. `A` is not a member of this ranking and cannot become its highest behavior, increment its count, or arm its StopAll rule. StopAll is a hard lifecycle boundary, not a competing S/E behavior. Separate A/S/E/StopAll visibility and Order_B ownership rules retain their own scopes.

This priority and exact-identity rule are identical in Bullish and Bearish. Only the strict price stop is directional: Bullish uses `Low < owner price` and Bearish uses `High > owner price`; equality is not a stop.

### 12.2 Highest existing behavior and armed owner

The first accepted S/E occurrence immediately becomes the highest existing exact behavior with count `1`. It is not armed. A repeated occurrence increments only the same exact identity: `S Blue`, `S Red`, or an E identity with the same family and number such as `E1 Blue` or `E1 Red`. Different E numbers and colors never combine. The current exact owner is armed for StopAll at count `>= 2`; its latest accepted occurrence supplies the strict stop level and search start. A third or later exact occurrence remains armed while it still owns the highest state.

An accepted unrelated higher-priority behavior replaces the owner at its source time and starts at count `1`. A direct E child first resolves the strict stop of its exact armed parent, even when its retrospectively chosen source candle begins at or before that stop. An accepted independent E sourced from a different S parent may also donate the currently armed owner stop when the first strict crossing belongs to that very E source candle and its directional source extreme strictly penetrates the owner price. A larger number within the same E family advances the E owner; a smaller number does not. Lower-priority accepted objects may remain valid calculation/output objects, but cannot count, remain armed, or trigger StopAll behind the current owner. There is one active exact owner and no independent Blue repetition ledger.

### 12.5 Hard StopAll boundary

Materializing StopAll resets the active exact owner, its count/armed state, and any pending completed stop. Historical S/E and StopAll objects remain available as calculation and output evidence. E receives the accepted StopAll source map through the existing atomic sequence-reset publication; its dependent candidate/carried context caches refresh while immutable physical stop/cross caches and historical accepted causes remain retained. A later lifecycle cannot inherit an earlier count or resurrect a displaced owner.

### 12.6 Cross-stage A/S/E visibility ownership

A, S and E calculations continue to retain internal historical evidence. Public ownership is resolved from exact strict stops, source chronology and shared priority. A source that strictly extends beyond the newest stopped owner can be consumed as the closed owner's next leg head instead of re-entering as equal/smaller behavior; equality stays with the earlier owner. S under a stopped larger owner obeys analogous chronology-first ownership; a higher-priority Red S may supersede a stopped Blue S, while equal/lower candidates remain owned by the prior lifecycle. Final E/StopAll source occupancy removes duplicate A/S labels on the same physical source, while referenced historical parents are retained for lineage closure.

## Bearish

### 12.1 Exact S/E dominance priority

The complete dominance priority for S/E behavior is `S Blue < E Blue < S Red < E Red`. `A` is not a member of this ranking and cannot become its highest behavior, increment its count, or arm its StopAll rule. StopAll is a hard lifecycle boundary, not a competing S/E behavior. Separate A/S/E/StopAll visibility and Order_B ownership rules retain their own scopes.

This priority and exact-identity rule are identical in Bullish and Bearish. Only the strict price stop is directional: Bullish uses `Low < owner price` and Bearish uses `High > owner price`; equality is not a stop.

### 12.2 Highest existing behavior and armed owner

The first accepted S/E occurrence immediately becomes the highest existing exact behavior with count `1`. It is not armed. A repeated occurrence increments only the same exact identity: `S Blue`, `S Red`, or an E identity with the same family and number such as `E1 Blue` or `E1 Red`. Different E numbers and colors never combine. The current exact owner is armed for StopAll at count `>= 2`; its latest accepted occurrence supplies the strict stop level and search start. A third or later exact occurrence remains armed while it still owns the highest state.

An accepted unrelated higher-priority behavior replaces the owner at its source time and starts at count `1`. A direct E child first resolves the strict stop of its exact armed parent, even when its retrospectively chosen source candle begins at or before that stop. An accepted independent E sourced from a different S parent may also donate the currently armed owner stop when the first strict crossing belongs to that very E source candle and its directional source extreme strictly penetrates the owner price. A larger number within the same E family advances the E owner; a smaller number does not. Lower-priority accepted objects may remain valid calculation/output objects, but cannot count, remain armed, or trigger StopAll behind the current owner. There is one active exact owner and no independent Blue repetition ledger.

### 12.5 Hard StopAll boundary

Materializing StopAll resets the active exact owner, its count/armed state, and any pending completed stop. Historical S/E and StopAll objects remain available as calculation and output evidence. E receives the accepted StopAll source map through the existing atomic sequence-reset publication; its dependent candidate/carried context caches refresh while immutable physical stop/cross caches and historical accepted causes remain retained. A later lifecycle cannot inherit an earlier count or resurrect a displaced owner.

### 12.6 Cross-stage A/S/E visibility ownership

A, S and E calculations continue to retain internal historical evidence. Public ownership is resolved from exact strict stops, source chronology and shared priority. A source that strictly extends beyond the newest stopped owner can be consumed as the closed owner's next leg head instead of re-entering as equal/smaller behavior; equality stays with the earlier owner. S under a stopped larger owner obeys analogous chronology-first ownership; a higher-priority Red S may supersede a stopped Blue S, while equal/lower candidates remain owned by the prior lifecycle. Final E/StopAll source occupancy removes duplicate A/S labels on the same physical source, while referenced historical parents are retained for lineage closure.

## Review scope

These are current accepted Reference statements compared with the captured executable owners. They do not establish independent RAW correctness. The current source-scope exclusion applies to additional features present incidentally in exact snapshots.

## Owner scopes

The StopAll repetition hierarchy contains only S/E. module_priority separately ranks cross-stage visibility and Order_B ownership as StopAll 5, E Red 4, S Red 3, E Blue 2, S Blue 1, A 0. Latest stopped main boundary precedes same-boundary priority/number/source ties in split_a_zones_by_dominant_stops. Consumed-S continuation and A provenance filtering have their own gates in algorithm.reconciliation and algorithm.visibility.
