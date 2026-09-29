---
id: "algorithm.s.type1"
type: "algorithm"
status: "active"
authority: "executable"
title: "S Type-1 Simple physical-Order route"
version: "current"
related_entities: ["algorithm.order.a", "algorithm.s"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.s_zone_detector", "source.order_audit_engine", "source.reaction_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L138", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L138"]
mirror_links: ["mirror.contract"]
---

# S Type-1 Simple physical-Order route

## Bullish

#### 7.4 Order-backed Simple and Advanced routes

The first physical opposite Order_A owned by the stopped A is immutable for that A; later native Reactions do not refresh it merely because they are newer. Candidate timing first applies established price geometry. Exact event chronology may reclassify an apparent after-Order Simple candidate as pre-Order only when its candidate event is strictly before Order First; equality belongs to after-Order. A valid nested same-direction Reaction wholly contained in the physical opposite Order, with aligned confirmation at or before Order confirmation, owns the **Advanced** path and cannot be stolen by the pre-Order Simple chronology optimization.

For pre-Order Simple, candidate geometry spans A-stop through Order First with the A-stop candle restricted to lower-TF prices at/after the exact A-stop event. For post-Order Simple, the first aligned Reaction after Order confirmation is used and candidate geometry spans Order Break through aligned Reaction Break inclusive with last-on-equality ownership. Advanced uses the directionally relevant opposite Order box source after a nested aligned Reaction confirms.

#### 7.5 S decision race

After Order confirmation, two strict lower-TF events compete:

- physical Order stop: `High > OrderStop` → **S Red**;
- S candidate strict Bullish cross → **S Blue** only after an aligned Reset Blue formation or an ordinary aligned Reaction completion qualifies the candidate.

An exact same lower-TF position for both crossings produces no decision. Otherwise the earlier event wins. The legacy pre-Order Simple fallback may initially observe an unqualified candidate cross; if later qualification exists by that exact event it becomes Blue, otherwise the fallback path is rebuilt through normal ownership rather than inventing a family.

When a Red decision wins, Red source geometry is recalculated from Order Break through the Red decision main candle unless the accepted pre-Order source is itself authoritative.

## Bearish

#### 7.4 Order-backed Simple and Advanced routes

The first physical opposite Order_A owned by the stopped A is immutable for that A; later native Reactions do not refresh it merely because they are newer. Candidate timing first applies established price geometry. Exact event chronology may reclassify an apparent after-Order Simple candidate as pre-Order only when its candidate event is strictly before Order First; equality belongs to after-Order. A valid nested same-direction Reaction wholly contained in the physical opposite Order, with aligned confirmation at or before Order confirmation, owns the **Advanced** path and cannot be stolen by the pre-Order Simple chronology optimization.

For pre-Order Simple, candidate geometry spans A-stop through Order First with the A-stop candle restricted to lower-TF prices at/after the exact A-stop event. For post-Order Simple, the first aligned Reaction after Order confirmation is used and candidate geometry spans Order Break through aligned Reaction Break inclusive with last-on-equality ownership. Advanced uses the directionally relevant opposite Order box source after a nested aligned Reaction confirms.

#### 7.5 S decision race

After Order confirmation, two strict lower-TF events compete:

- physical Order stop: `Low < OrderStop` → **S Red**;
- S candidate strict Bearish cross → **S Blue** only after an aligned Reset Blue formation or an ordinary aligned Reaction completion qualifies the candidate.

An exact same lower-TF position for both crossings produces no decision. Otherwise the earlier event wins. The legacy pre-Order Simple fallback may initially observe an unqualified candidate cross; if later qualification exists by that exact event it becomes Blue, otherwise the fallback path is rebuilt through normal ownership rather than inventing a family.

When a Red decision wins, Red source geometry is recalculated from Order Break through the Red decision main candle unless the accepted pre-Order source is itself authoritative.

## Source-level contract

Serialized native subtype is simple. Initial Bullish timing is after if Order BoxBottom <= A-stop main Low, otherwise before; Bearish uses Order BoxTop >= A-stop main High. Valid nesting preserves Advanced. Without nesting, after may become before only if exact candidate event < Order First; equality remains after.

Pre-Order source includes A-stop..Order First but stop main is restricted to lower rows >= exact A stop, with earliest equal source. Post-Order uses first aligned confirmation strictly after Order confirmation and complete Order Break..aligned Break, last equal source. Native race begins at Order confirmation; same lower-position crossings yield no decision. Temporary unqualified pre-Order cross falls back to normal route, never publishes fallback as a family.

Native Red retains authoritative accepted pre-Order source; otherwise complete Order Break..Red decision directional extreme owns source.
