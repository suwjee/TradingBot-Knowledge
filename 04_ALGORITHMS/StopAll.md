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
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L375", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L375"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.lifecycle"]
name: "StopAll"
aliases: ["Stop All"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# StopAll sequence gates and hard cycle boundary

## Bullish

### 12.1 Exact S/E dominance priority

The complete dominance priority for S/E behavior is `S Blue < E Blue < S Red < E Red`. `A` is not a member of this ranking and cannot become its highest behavior, increment its count, or arm its StopAll rule. StopAll is a hard lifecycle boundary, not a competing S/E behavior. Separate A/S/E/StopAll visibility and Order_B ownership rules retain their own scopes.

This priority and exact-identity rule are identical in Bullish and Bearish. Only the strict price stop is directional: Bullish uses `Low < owner price` and Bearish uses `High > owner price`; equality is not a stop.

### 12.2 Highest existing behavior and armed owner

The first accepted S/E occurrence immediately becomes the highest existing exact behavior with count `1`. It is not armed. A repeated occurrence increments only the same exact identity: `S Blue`, `S Red`, or an E identity with the same family and number such as `E1 Blue` or `E1 Red`. Different E numbers and colors never combine. The current exact owner is armed for StopAll at count `>= 2`; its latest accepted occurrence supplies the strict stop level and search start. A third or later exact occurrence remains armed while it still owns the highest state.

An accepted unrelated higher-priority behavior replaces the owner at its source time and starts at count `1`. A direct E child first resolves the strict stop of its exact armed parent, even when its retrospectively chosen source candle begins at or before that stop. An accepted independent E sourced from a different S parent may also donate the currently armed owner stop when the first strict crossing belongs to that very E source candle and its directional source extreme strictly penetrates the owner price. A larger number within the same E family advances the E owner; a smaller number does not. Lower-priority accepted objects may remain valid calculation/output objects, but cannot count, remain armed, or trigger StopAll behind the current owner. There is one active exact owner and no independent Blue repetition ledger.

### 12.3 Chronological strict stop and E donor

The armed owner's stop is the first strict 5-second crossing at or after its latest occurrence's decision event. A stop must precede replacement by an unrelated higher-priority behavior to belong to the former owner; an E directly caused by that stop is resolved as a donor before it replaces its parent. A completed earlier stop is frozen as pending historical evidence if no eligible donor exists at that transition; later replacement cannot cancel it. This pending completed gate is not a second occurrence counter and cannot re-arm a displaced behavior.

At an incoming E, a completed owner stop strictly before the E source time creates `StopAll1` through `sequence-group-stop`; the incoming E supplies physical geometry and Order provenance regardless of family. Two causal exceptions also admit an owner stop at/after retrospective E source time **and no later than E's decision**: (1) exact direct child of the armed owner, whose `parentStopEventTime` equals its first strict stop and whose parent type/source identity/price exactly match the owner's latest occurrence; or (2) an independently accepted E at a new physical source whose directional source extreme strictly penetrates the armed owner's price, and the owner's **first** strict stop belongs to that exact 30s (or configured) E source candle `[sourceTime, sourceTime + timeframe)`. The second route does not depend on E ancestry or require the parent S to postdate the dominant E: independent E parents can predate the owner. An unrelated E cannot consume a stop in a *later* main candle merely because its E decision is later. No earlier displaced owner is revived and no parallel Blue counter is introduced. Bridge includes only otherwise-omitted accepted independent S-root E identities as extra StopAll donor candidates, preserving the preexisting E candidate and Order provenance at every already-admitted physical source. An existing active StopAll that strictly stops at or before the incoming E decision continues to create the next numbered StopAll through `stopall-stop` under its separate historical contract. Its gate precedes the S/E owner gate.

**Superseded by V5.4.33:** the V5.4.32 sentence limiting *all* retrospective E donor exceptions to exact direct children alone. That direct-child rule remains active; the same-source-candle independent-E route is the additional narrowly bounded general exception.

### 12.4 S Red donor and legacy gate name

**ACTIVE (5.4.31 direct accepted-S Red rule):** When the currently dominant exact S/E behavior is Blue, its count is `>= 2`, and its latest accepted occurrence was confirmed **strictly before** the decision event of an accepted `S Red`, the **first eligible S Red itself** immediately produces `StopAll1`. No strict Blue price stop is required. Either Order Mode A or Mode B is valid. Formation must be checked at the incoming S **decision event**, not merely its retrospective source candle. The new `gateEventTime` is exactly the S decision event, and `stoppedBehaviorKey` preserves `S blue` or the precise `E(n) blue` owner and its count. The S is the donor; the StopAll resets the current dominant owner and pending stop state. This direct accepted-S Red gate has precedence inside S handling over the older completed-stop-only path. A previously displaced lower-priority Blue cannot trigger it.

**HISTORICAL LEGACY ROUTE (still executable as fallback):** When the direct gate is not eligible, an accepted S Red of Mode B may still consume an already-completed strict stop of an earlier armed Blue owner using the existing pending-stop rule. This fallback gate event is the earlier physical stop; Mode A does not consume that fallback. The two routes reuse the legacy serialized name `opposite-s-group-stop` but differ in gate chronology. Neither fallback nor other StopAll/E donor paths is removed.



**HISTORICAL / SUPERSEDED (`5.4.22` and earlier):** accepted Blue occurrences were counted in a parallel ledger independent of dominant-owner transitions. That ledger could promote a lower-priority Blue group after a higher-priority Red owner had formed, or promote without a strict stop. It is not an active rule.

### 12.5 Hard StopAll boundary

Materializing StopAll resets the active exact owner, its count/armed state, and any pending completed stop. Historical S/E and StopAll objects remain available as calculation and output evidence. E receives the accepted StopAll source map through the existing atomic sequence-reset publication; its dependent candidate/carried context caches refresh while immutable physical stop/cross caches and historical accepted causes remain retained. A later lifecycle cannot inherit an earlier count or resurrect a displaced owner.

## Bearish

### 12.1 Exact S/E dominance priority

The complete dominance priority for S/E behavior is `S Blue < E Blue < S Red < E Red`. `A` is not a member of this ranking and cannot become its highest behavior, increment its count, or arm its StopAll rule. StopAll is a hard lifecycle boundary, not a competing S/E behavior. Separate A/S/E/StopAll visibility and Order_B ownership rules retain their own scopes.

This priority and exact-identity rule are identical in Bullish and Bearish. Only the strict price stop is directional: Bullish uses `Low < owner price` and Bearish uses `High > owner price`; equality is not a stop.

### 12.2 Highest existing behavior and armed owner

The first accepted S/E occurrence immediately becomes the highest existing exact behavior with count `1`. It is not armed. A repeated occurrence increments only the same exact identity: `S Blue`, `S Red`, or an E identity with the same family and number such as `E1 Blue` or `E1 Red`. Different E numbers and colors never combine. The current exact owner is armed for StopAll at count `>= 2`; its latest accepted occurrence supplies the strict stop level and search start. A third or later exact occurrence remains armed while it still owns the highest state.

An accepted unrelated higher-priority behavior replaces the owner at its source time and starts at count `1`. A direct E child first resolves the strict stop of its exact armed parent, even when its retrospectively chosen source candle begins at or before that stop. An accepted independent E sourced from a different S parent may also donate the currently armed owner stop when the first strict crossing belongs to that very E source candle and its directional source extreme strictly penetrates the owner price. A larger number within the same E family advances the E owner; a smaller number does not. Lower-priority accepted objects may remain valid calculation/output objects, but cannot count, remain armed, or trigger StopAll behind the current owner. There is one active exact owner and no independent Blue repetition ledger.

### 12.3 Chronological strict stop and E donor

The armed owner's stop is the first strict 5-second crossing at or after its latest occurrence's decision event. A stop must precede replacement by an unrelated higher-priority behavior to belong to the former owner; an E directly caused by that stop is resolved as a donor before it replaces its parent. A completed earlier stop is frozen as pending historical evidence if no eligible donor exists at that transition; later replacement cannot cancel it. This pending completed gate is not a second occurrence counter and cannot re-arm a displaced behavior.

At an incoming E, a completed owner stop strictly before the E source time creates `StopAll1` through `sequence-group-stop`; the incoming E supplies physical geometry and Order provenance regardless of family. Two causal exceptions also admit an owner stop at/after retrospective E source time **and no later than E's decision**: (1) exact direct child of the armed owner, whose `parentStopEventTime` equals its first strict stop and whose parent type/source identity/price exactly match the owner's latest occurrence; or (2) an independently accepted E at a new physical source whose directional source extreme strictly penetrates the armed owner's price, and the owner's **first** strict stop belongs to that exact 30s (or configured) E source candle `[sourceTime, sourceTime + timeframe)`. The second route does not depend on E ancestry or require the parent S to postdate the dominant E: independent E parents can predate the owner. An unrelated E cannot consume a stop in a *later* main candle merely because its E decision is later. No earlier displaced owner is revived and no parallel Blue counter is introduced. Bridge includes only otherwise-omitted accepted independent S-root E identities as extra StopAll donor candidates, preserving the preexisting E candidate and Order provenance at every already-admitted physical source. An existing active StopAll that strictly stops at or before the incoming E decision continues to create the next numbered StopAll through `stopall-stop` under its separate historical contract. Its gate precedes the S/E owner gate.

**Superseded by V5.4.33:** the V5.4.32 sentence limiting *all* retrospective E donor exceptions to exact direct children alone. That direct-child rule remains active; the same-source-candle independent-E route is the additional narrowly bounded general exception.

### 12.4 S Red donor and legacy gate name

**ACTIVE (5.4.31 direct accepted-S Red rule):** When the currently dominant exact S/E behavior is Blue, its count is `>= 2`, and its latest accepted occurrence was confirmed **strictly before** the decision event of an accepted `S Red`, the **first eligible S Red itself** immediately produces `StopAll1`. No strict Blue price stop is required. Either Order Mode A or Mode B is valid. Formation must be checked at the incoming S **decision event**, not merely its retrospective source candle. The new `gateEventTime` is exactly the S decision event, and `stoppedBehaviorKey` preserves `S blue` or the precise `E(n) blue` owner and its count. The S is the donor; the StopAll resets the current dominant owner and pending stop state. This direct accepted-S Red gate has precedence inside S handling over the older completed-stop-only path. A previously displaced lower-priority Blue cannot trigger it.

**HISTORICAL LEGACY ROUTE (still executable as fallback):** When the direct gate is not eligible, an accepted S Red of Mode B may still consume an already-completed strict stop of an earlier armed Blue owner using the existing pending-stop rule. This fallback gate event is the earlier physical stop; Mode A does not consume that fallback. The two routes reuse the legacy serialized name `opposite-s-group-stop` but differ in gate chronology. Neither fallback nor other StopAll/E donor paths is removed.



**HISTORICAL / SUPERSEDED (`5.4.22` and earlier):** accepted Blue occurrences were counted in a parallel ledger independent of dominant-owner transitions. That ledger could promote a lower-priority Blue group after a higher-priority Red owner had formed, or promote without a strict stop. It is not an active rule.

### 12.5 Hard StopAll boundary

Materializing StopAll resets the active exact owner, its count/armed state, and any pending completed stop. Historical S/E and StopAll objects remain available as calculation and output evidence. E receives the accepted StopAll source map through the existing atomic sequence-reset publication; its dependent candidate/carried context caches refresh while immutable physical stop/cross caches and historical accepted causes remain retained. A later lifecycle cannot inherit an earlier count or resurrect a displaced owner.

## Review scope

These are current accepted Reference statements compared with the captured executable owners. They do not establish independent RAW correctness. The current source-scope exclusion applies to additional features present incidentally in exact snapshots.

## Executable owner

_DominantBehavior and advance_dominant_behavior own one exact S/E owner. StopAllDetector.detect walks S sources before each E source, then processes remaining S. Direct S Red handling compares decision events; E donor handling retains exact source-bucket/direct-parent evidence. Accepted independent S-root E donors are supplemented before final StopAll reconciliation without replacing an existing E physical source or its Order provenance. Each reconciliation call publishes one hard-boundary map; feedback and final visibility share explicit lifecycle enablement.
