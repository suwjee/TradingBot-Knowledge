---
id: "algorithm.s"
type: "algorithm"
status: "active"
authority: "executable"
title: "S opening, candidates and decisions"
version: "current"
related_entities: ["algorithm.a", "algorithm.orderaudit", "algorithm.s.type1", "algorithm.s.type2", "algorithm.s.type3", "algorithm.s.type4"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1228", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L640"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.s_zone_detector", "source.order_audit_engine", "source.lifecycle_engine", "source.trading_pipeline", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L228", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L228"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.a", "algorithm.order", "algorithm.reaction", "algorithm.blue"]
name: "S"
aliases: ["S Zone", "SZone"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# S opening, candidates and decisions

## Bullish

#### 7.1 General A→S gate

Only A candidates outside an already-owned S continuation are eligible. S begins at A's first strict Bullish stop. If the next A confirmation is already reached at/before that handoff, the stale A does not open S. The detector audits the stopped A's first physical Order_A independently before choosing the S route.

A decided S normally owns subsequent A continuation. A newly built Reset-Blue/Reset-Blue pair may preempt that ownership only when both Blue sources are born after the S handoff, Blue-1 stops before Blue-2 forms, the A source is Blue-2's stop candle, and the pair is actually Reset/Reset. A trigger that begins strictly after the exact S ownership handoff is independently eligible.

#### 7.2 Order-free Type-3 S Blue

Type-3 is an opposite-Reset-leg route available after A stop and before the first Order deadline. The opposite Reaction owning the Reset must have confirmed by the A-stop event and must not already have Reset before that A stop. Candidate geometry spans the **complete opposite Reaction Break main candle through the Reset main candle**, inclusive, and selects the minimum Low with **last-candle ownership on equality**. After Reset, the first strict Bullish cross of that candidate wins only if at least one ordinary same-direction Reaction confirms after A stop and no later than the cross. Earliest valid Type-3 decision wins.

#### 7.3 Order-free Type-4 S Blue

Type-4 is the same-direction Reaction continuation available after A stop only while no opposite Order has formed. For every aligned Bullish Reaction confirmed before the Order deadline, candidate geometry spans the A-stop main candle through that Reaction Break main candle, inclusive, selects the minimum Low and assigns equality to the **last** candidate candle. Search begins at the maximum of A-stop event, aligned Reaction confirmation and candidate formation event. That lower-timeframe start is inclusive. The next aligned Reaction confirmation and Order deadline are exclusive upper bounds. The first strict Bullish cross creates S Blue only when a public calculation-valid Blue formed from the candidate source through that cross. If a candidate crosses without qualifying Blue, no S is created from it; the next aligned Reaction rebuilds a fresh candidate from the same A-stop origin.

Type-3 and Type-4 are independent. Earlier exact decision event wins; Type-3 owns only a true exact-event tie.

#### 7.4 Order-backed Simple and Advanced routes

The first physical opposite Order_A owned by the stopped A is immutable for that A; later native Reactions do not refresh it merely because they are newer. Candidate timing first applies established price geometry. Exact event chronology may reclassify an apparent after-Order Simple candidate as pre-Order only when its candidate event is strictly before Order First; equality belongs to after-Order. A valid nested same-direction Reaction wholly contained in the physical opposite Order, with aligned confirmation at or before Order confirmation, owns the **Advanced** path and cannot be stolen by the pre-Order Simple chronology optimization.

For pre-Order Simple, candidate geometry spans A-stop through Order First with the A-stop candle restricted to lower-TF prices at/after the exact A-stop event. For post-Order Simple, the first aligned Reaction after Order confirmation is used and candidate geometry spans Order Break through aligned Reaction Break inclusive with last-on-equality ownership. Advanced uses the directionally relevant opposite Order box source after a nested aligned Reaction confirms.

#### 7.5 S decision race

After Order confirmation, two strict lower-TF events compete:

- physical Order stop: `High > OrderStop` → **S Red**;
- S candidate strict Bullish cross → **S Blue** only after an aligned Reset Blue formation or an ordinary aligned Reaction completion qualifies the candidate.

An exact same lower-TF position for both crossings produces no decision. Otherwise the earlier event wins. The legacy pre-Order Simple fallback may initially observe an unqualified candidate cross; if later qualification exists by that exact event it becomes Blue, otherwise the fallback path is rebuilt through normal ownership rather than inventing a family.

When a Red decision wins, Red source geometry is recalculated from Order Break through the Red decision main candle unless the accepted pre-Order source is itself authoritative.

#### 7.6 Shared accepted-Order stop reconciliation

After E/OrderAudit accepts physical Orders, an open S may be converted to Red by **any** accepted physical Order whose strict stop occurs at or after the frozen S source main-candle start and strictly before S's current decision; the Order confirmation must be strictly earlier than its stop. Parent identity is irrelevant to use; physical identity is authoritative. Candidates are deduplicated by `(FirstIndex, BreakIndex)`, ordered by `(stopCrossEvent, confirmation, FirstIndex, BreakIndex)`, and provenance remains attached to the Order that created it.

## Bearish

#### 7.1 General A→S gate

Only A candidates outside an already-owned S continuation are eligible. S begins at A's first strict Bearish stop. If the next A confirmation is already reached at/before that handoff, the stale A does not open S. The detector audits the stopped A's first physical Order_A independently before choosing the S route.

A decided S normally owns subsequent A continuation. A newly built Reset-Blue/Reset-Blue pair may preempt that ownership only when both Blue sources are born after the S handoff, Blue-1 stops before Blue-2 forms, the A source is Blue-2's stop candle, and the pair is actually Reset/Reset. A trigger that begins strictly after the exact S ownership handoff is independently eligible.

#### 7.2 Order-free Type-3 S Blue

Type-3 is an opposite-Reset-leg route available after A stop and before the first Order deadline. The opposite Reaction owning the Reset must have confirmed by the A-stop event and must not already have Reset before that A stop. Candidate geometry spans the **complete opposite Reaction Break main candle through the Reset main candle**, inclusive, and selects the maximum High with **last-candle ownership on equality**. After Reset, the first strict Bearish cross of that candidate wins only if at least one ordinary same-direction Reaction confirms after A stop and no later than the cross. Earliest valid Type-3 decision wins.

#### 7.3 Order-free Type-4 S Blue

Type-4 is the same-direction Reaction continuation available after A stop only while no opposite Order has formed. For every aligned Bearish Reaction confirmed before the Order deadline, candidate geometry spans the A-stop main candle through that Reaction Break main candle, inclusive, selects the maximum High and assigns equality to the **last** candidate candle. Search begins at the maximum of A-stop event, aligned Reaction confirmation and candidate formation event. That lower-timeframe start is inclusive. The next aligned Reaction confirmation and Order deadline are exclusive upper bounds. The first strict Bearish cross creates S Blue only when a public calculation-valid Blue formed from the candidate source through that cross. If a candidate crosses without qualifying Blue, no S is created from it; the next aligned Reaction rebuilds a fresh candidate from the same A-stop origin.

Type-3 and Type-4 are independent. Earlier exact decision event wins; Type-3 owns only a true exact-event tie.

#### 7.4 Order-backed Simple and Advanced routes

The first physical opposite Order_A owned by the stopped A is immutable for that A; later native Reactions do not refresh it merely because they are newer. Candidate timing first applies established price geometry. Exact event chronology may reclassify an apparent after-Order Simple candidate as pre-Order only when its candidate event is strictly before Order First; equality belongs to after-Order. A valid nested same-direction Reaction wholly contained in the physical opposite Order, with aligned confirmation at or before Order confirmation, owns the **Advanced** path and cannot be stolen by the pre-Order Simple chronology optimization.

For pre-Order Simple, candidate geometry spans A-stop through Order First with the A-stop candle restricted to lower-TF prices at/after the exact A-stop event. For post-Order Simple, the first aligned Reaction after Order confirmation is used and candidate geometry spans Order Break through aligned Reaction Break inclusive with last-on-equality ownership. Advanced uses the directionally relevant opposite Order box source after a nested aligned Reaction confirms.

#### 7.5 S decision race

After Order confirmation, two strict lower-TF events compete:

- physical Order stop: `Low < OrderStop` → **S Red**;
- S candidate strict Bearish cross → **S Blue** only after an aligned Reset Blue formation or an ordinary aligned Reaction completion qualifies the candidate.

An exact same lower-TF position for both crossings produces no decision. Otherwise the earlier event wins. The legacy pre-Order Simple fallback may initially observe an unqualified candidate cross; if later qualification exists by that exact event it becomes Blue, otherwise the fallback path is rebuilt through normal ownership rather than inventing a family.

When a Red decision wins, Red source geometry is recalculated from Order Break through the Red decision main candle unless the accepted pre-Order source is itself authoritative.

#### 7.6 Shared accepted-Order stop reconciliation

After E/OrderAudit accepts physical Orders, an open S may be converted to Red by **any** accepted physical Order whose strict stop occurs at or after the frozen S source main-candle start and strictly before S's current decision; the Order confirmation must be strictly earlier than its stop. Parent identity is irrelevant to use; physical identity is authoritative. Candidates are deduplicated by `(FirstIndex, BreakIndex)`, ordered by `(stopCrossEvent, confirmation, FirstIndex, BreakIndex)`, and provenance remains attached to the Order that created it.

## Source-level contract

Native formation_type is simple,advanced,type3,type4. Native Type-3/Type-4 are order-free Blue; Simple/Advanced may Red/Blue. Immutable first A-owned canonical opposite Order is independently audited even when order-free route wins. No-Order deadline is its exact confirmation or full range end. Type-3/Type-4 race first, Type-3 on exact tie; Order-backed route only if both fail.

Shared reconciliation includes source_time equality under current synchronized Source/Reference contract. It requires physical confirmation < stop and stop < current decision; physical winner key is stop,confirmation,First,Break. Recoloring keeps frozen source/price/formation_type, replaces decisive Order geometry/provenance fields, clears opposite Reset fields, and preserves existing order_direction field. A source main timestamp is separate from exact candidate formation event; neither is a strict price crossing.

Accepted,stage-invalid,consumed/historical and public S are distinct lifecycle states. Native construction nullability is preserved by current field projection rather than inferred from subtype.


## Native A handoff window

S-stage A ownership uses a native window beginning at the exact parent A-stop event. While that handoff has no resolved S decision its end is open. Once S decides, the window ends at `max(aStopEvent, sDecisionEvent + one microsecond)`; the upper boundary is exclusive, so the decision timestamp itself is included. This is the S detector's A eligibility window, not the later full lifecycle lifetime of S.

Compare A's exact source event with that window. An A whose trigger begins strictly after the handoff is independently eligible. In a decided window, a fresh Reset/Reset Blue pair can also remain eligible when Blue-1 source is strictly after handoff, Blue-1 stop is strictly before Blue-2 source, and A source main time equals Blue-2 stop main time. Later lifecycle owners still decide calculation acceptance and public visibility. Every stopped A is audited independently before these S-selection filters run.

## Current stopped-A physical admission and direction

The first Order_A search after an accepted A stop is independent of continuous public opposite-Reaction ownership. Complete confirmed physical geometry absent from that stream may be accepted with reactionNumber=0, preserving real First/Break and exact confirmation; see algorithm.order.a. A-owned causes from provisional or lifecycle-invalid A are filtered before downstream use/final audit. Shared accepted-Order recoloring sets order_direction to the physical opposite direction as well as identity/stop fields.
