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
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L395", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L395"]
mirror_links: ["mirror.contract"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# StopAll opposite-s-group-stop gate

## Bullish

### 12.2 Highest existing behavior and armed owner

The first accepted S/E occurrence immediately becomes the highest existing exact behavior with count `1`. It is not armed. A repeated occurrence increments only the same exact identity: `S Blue`, `S Red`, or an E identity with the same family and number such as `E1 Blue` or `E1 Red`. Different E numbers and colors never combine. The current exact owner is armed for StopAll at count `>= 2`; its latest accepted occurrence supplies the strict stop level and search start. A third or later exact occurrence remains armed while it still owns the highest state.

An accepted unrelated higher-priority behavior replaces the owner at its source time and starts at count `1`. A direct E child first resolves the strict stop of its exact armed parent, even when its retrospectively chosen source candle begins at or before that stop. An accepted independent E sourced from a different S parent may also donate the currently armed owner stop when the first strict crossing belongs to that very E source candle and its directional source extreme strictly penetrates the owner price. A larger number within the same E family advances the E owner; a smaller number does not. Lower-priority accepted objects may remain valid calculation/output objects, but cannot count, remain armed, or trigger StopAll behind the current owner. There is one active exact owner and no independent Blue repetition ledger.

### 12.4 S Red donor and legacy gate name

**ACTIVE (5.4.31 direct accepted-S Red rule):** When the currently dominant exact S/E behavior is Blue, its count is `>= 2`, and its latest accepted occurrence was confirmed **strictly before** the decision event of an accepted `S Red`, the **first eligible S Red itself** immediately produces `StopAll1`. No strict Blue price stop is required. Either Order Mode A or Mode B is valid. Formation must be checked at the incoming S **decision event**, not merely its retrospective source candle. The new `gateEventTime` is exactly the S decision event, and `stoppedBehaviorKey` preserves `S blue` or the precise `E(n) blue` owner and its count. The S is the donor; the StopAll resets the current dominant owner and pending stop state. This direct accepted-S Red gate has precedence inside S handling over the older completed-stop-only path. A previously displaced lower-priority Blue cannot trigger it.

**HISTORICAL LEGACY ROUTE (still executable as fallback):** When the direct gate is not eligible, an accepted S Red of Mode B may still consume an already-completed strict stop of an earlier armed Blue owner using the existing pending-stop rule. This fallback gate event is the earlier physical stop; Mode A does not consume that fallback. The two routes reuse the legacy serialized name `opposite-s-group-stop` but differ in gate chronology. Neither fallback nor other StopAll/E donor paths is removed.



**HISTORICAL / SUPERSEDED (`5.4.22` and earlier):** accepted Blue occurrences were counted in a parallel ledger independent of dominant-owner transitions. That ledger could promote a lower-priority Blue group after a higher-priority Red owner had formed, or promote without a strict stop. It is not an active rule.

### 12.5 Hard StopAll boundary

Materializing StopAll resets the active exact owner, its count/armed state, and any pending completed stop. Historical S/E and StopAll objects remain available as calculation and output evidence. E receives the accepted StopAll source map through the existing atomic sequence-reset publication; its dependent candidate/carried context caches refresh while immutable physical stop/cross caches and historical accepted causes remain retained. A later lifecycle cannot inherit an earlier count or resurrect a displaced owner.

## Bearish

### 12.2 Highest existing behavior and armed owner

The first accepted S/E occurrence immediately becomes the highest existing exact behavior with count `1`. It is not armed. A repeated occurrence increments only the same exact identity: `S Blue`, `S Red`, or an E identity with the same family and number such as `E1 Blue` or `E1 Red`. Different E numbers and colors never combine. The current exact owner is armed for StopAll at count `>= 2`; its latest accepted occurrence supplies the strict stop level and search start. A third or later exact occurrence remains armed while it still owns the highest state.

An accepted unrelated higher-priority behavior replaces the owner at its source time and starts at count `1`. A direct E child first resolves the strict stop of its exact armed parent, even when its retrospectively chosen source candle begins at or before that stop. An accepted independent E sourced from a different S parent may also donate the currently armed owner stop when the first strict crossing belongs to that very E source candle and its directional source extreme strictly penetrates the owner price. A larger number within the same E family advances the E owner; a smaller number does not. Lower-priority accepted objects may remain valid calculation/output objects, but cannot count, remain armed, or trigger StopAll behind the current owner. There is one active exact owner and no independent Blue repetition ledger.

### 12.4 S Red donor and legacy gate name

**ACTIVE (5.4.31 direct accepted-S Red rule):** When the currently dominant exact S/E behavior is Blue, its count is `>= 2`, and its latest accepted occurrence was confirmed **strictly before** the decision event of an accepted `S Red`, the **first eligible S Red itself** immediately produces `StopAll1`. No strict Blue price stop is required. Either Order Mode A or Mode B is valid. Formation must be checked at the incoming S **decision event**, not merely its retrospective source candle. The new `gateEventTime` is exactly the S decision event, and `stoppedBehaviorKey` preserves `S blue` or the precise `E(n) blue` owner and its count. The S is the donor; the StopAll resets the current dominant owner and pending stop state. This direct accepted-S Red gate has precedence inside S handling over the older completed-stop-only path. A previously displaced lower-priority Blue cannot trigger it.

**HISTORICAL LEGACY ROUTE (still executable as fallback):** When the direct gate is not eligible, an accepted S Red of Mode B may still consume an already-completed strict stop of an earlier armed Blue owner using the existing pending-stop rule. This fallback gate event is the earlier physical stop; Mode A does not consume that fallback. The two routes reuse the legacy serialized name `opposite-s-group-stop` but differ in gate chronology. Neither fallback nor other StopAll/E donor paths is removed.



**HISTORICAL / SUPERSEDED (`5.4.22` and earlier):** accepted Blue occurrences were counted in a parallel ledger independent of dominant-owner transitions. That ledger could promote a lower-priority Blue group after a higher-priority Red owner had formed, or promote without a strict stop. It is not an active rule.

### 12.5 Hard StopAll boundary

Materializing StopAll resets the active exact owner, its count/armed state, and any pending completed stop. Historical S/E and StopAll objects remain available as calculation and output evidence. E receives the accepted StopAll source map through the existing atomic sequence-reset publication; its dependent candidate/carried context caches refresh while immutable physical stop/cross caches and historical accepted causes remain retained. A later lifecycle cannot inherit an earlier count or resurrect a displaced owner.

## Review scope

These are current accepted Reference statements compared with the captured executable owners. They do not establish independent RAW correctness. The current source-scope exclusion applies to additional features present incidentally in exact snapshots.
