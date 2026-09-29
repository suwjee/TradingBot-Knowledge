---
id: "algorithm.visibility"
type: "algorithm"
status: "active"
authority: "executable"
title: "Final behavior visibility, range and lineage"
version: "current"
related_entities: ["algorithm.lifecycle", "algorithm.orderaudit", "algorithm.serialization"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L1155", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L1357", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
implemented_by: ["source.lifecycle_engine", "source.trading_pipeline", "source.order_audit_engine", "source.blue_line_detector", "source.reaction_engine"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L269"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.lifecycle", "algorithm.stopall"]
name: "Visibility"
aliases: ["Final visibility"]
---

# Final behavior visibility, range and lineage

## Bullish

#### 12.6 Cross-stage A/S/E visibility ownership

A, S and E calculations continue to retain internal historical evidence. Public ownership is resolved from exact strict stops, source chronology and shared priority. A source that strictly extends beyond the newest stopped owner can be consumed as the closed owner's next leg head instead of re-entering as equal/smaller behavior; equality stays with the earlier owner. S under a stopped larger owner obeys analogous chronology-first ownership; a higher-priority Red S may supersede a stopped Blue S, while equal/lower candidates remain owned by the prior lifecycle. Final E/StopAll source occupancy removes duplicate A/S labels on the same physical source, while referenced historical parents are retained for lineage closure.

#### 13.1 Projection rule

Legacy serialization contains no trading recalculation. Decimal prices are stringified; native local datetimes are converted through the existing Tehran-local epoch contract. Stable source ordering is preserved. Presentation range filtering is applied after full calculation, and OrderAudit may retain a pre-range physical identity when an in-range public behavior references it. `calculationValid` is emitted as `true` for public A/S because invalid calculation objects have already been removed by the calculation/visibility owner.

## Bearish

#### 12.6 Cross-stage A/S/E visibility ownership

A, S and E calculations continue to retain internal historical evidence. Public ownership is resolved from exact strict stops, source chronology and shared priority. A source that strictly extends beyond the newest stopped owner can be consumed as the closed owner's next leg head instead of re-entering as equal/smaller behavior; equality stays with the earlier owner. S under a stopped larger owner obeys analogous chronology-first ownership; a higher-priority Red S may supersede a stopped Blue S, while equal/lower candidates remain owned by the prior lifecycle. Final E/StopAll source occupancy removes duplicate A/S labels on the same physical source, while referenced historical parents are retained for lineage closure.

#### 13.1 Projection rule

Legacy serialization contains no trading recalculation. Decimal prices are stringified; native local datetimes are converted through the existing Tehran-local epoch contract. Stable source ordering is preserved. Presentation range filtering is applied after full calculation, and OrderAudit may retain a pre-range physical identity when an in-range public behavior references it. `calculationValid` is emitted as `true` for public A/S because invalid calculation objects have already been removed by the calculation/visibility owner.

## Source-level contract

StopAll source removes E label; final E/StopAll source removes A/S. Explicit invalid identities stay excluded after lineage restoration. Referenced historical S parents of E and A parents of S are restored before occupancy.

A provenance rebuilt after a stop checks Blue1,Blue2,continuation source,Reaction First >= boundary; it does not create new A by comparing old module price. S uses exact candidate event and chronologically consumed stopped owner.

Complete supplied input is calculated before presentation clipping. Reaction uses First index,Reset event main index,Blue/A/S/E/StopAll source index. Required out-of-range physical Order remains in audit with accepted full-calculation A causes. Public Blue requires valid/noninternal; current accepted A/S/E/StopAll internal filter passes through. Optional projection may resolve historical parents without new independent rows.


## Closed S transition and separate A provenance

S closed-transition visibility uses its exact candidate formation event when a candidate-event finder is supplied; later S decision/stop time does not replace that event. A newer accepted E or StopAll source starts current external lineage, so older-source owners are removed from the comparison set. Among owners strictly earlier than S source and stopped at or before its candidate event, the newest external E/StopAll source supplies an additional Close-based gate: a lower-priority S is suppressed when its source main-candle Close is strictly beyond that external owner's stop main-candle Close (`<` Bullish, `>` Bearish).

The general stopped-owner comparison then chooses greatest `(exactStopEvent, priority, number, sourceTime, sourceIndex)`. A higher-priority Red S may survive a stopped Blue S. Otherwise a S price that is equal to or does not extend strictly beyond the chosen owner's price remains visible; a strict extension consumes stopped owners of equal/lower priority and suppresses this S label. An active larger owner does not globally disable independent A/S discovery.

A provenance filtering is a separate operation from A cycle acceptance. It chooses the dominant already-stopped S/E owner by `(priority, number, sourceTime, sourceIndex)`, then requires the earliest of Blue-1 source, Blue-2 source, continuation source and Reaction First to be at or after that owner's exact stop. Equality is admitted. This provenance check must not be described as the latest-stop-main selection used by `split_a_zones_by_dominant_stops`.
