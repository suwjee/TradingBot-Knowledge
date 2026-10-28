---
id: "algorithm.reset"
type: "algorithm"
status: "active"
authority: "executable"
title: "Reset events and same-direction restart"
version: "current"
related_entities: ["algorithm.blue", "algorithm.order.b", "algorithm.reaction"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.reaction_engine", "source.order_audit_engine", "source.blue_line_detector", "source.s_zone_detector"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L174", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L174"]
mirror_links: ["mirror.contract"]
name: "Reset"
aliases: ["Reaction Reset"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Reset events and same-direction restart

## Bullish

#### 4.6 Reset

A confirmed Bullish Reaction resets only on the first strict `Low < confirmed BoxBottom` event. Equality is not Reset. When Reset and confirmation/break activity share a main candle, selected lower-TF ordering decides which event owns the state transition. Reset reopens **same-direction** Reaction ownership; opposite-direction patterns do not gate that search. A Reset event with an exact lower-TF second exposes that exact second; otherwise the owning main-candle start is the fallback representation.

#### 4.7 Post-Reset structural owner vs geometry-only evidence

After Reset, `_first_direct_same_direction_after_reset` scans eligible First candidates in chronological First-index order within the configured end index. It returns a candidate only if confirmation wins before strict loss of its frozen owning boundary. If invalidation wins first, candidates with First indexes at or before that invalidation main index are blocked. A candidate unfinished at the bounded end is skipped, so a later eligible candidate that completes healthily may be returned. The standalone initial Mode-A WAITING state retains its selected unfinished structural owner. The returned healthy result joins the canonical same-direction Reaction stream. `_first_geometry_after_reset` separately returns complete geometry without lifecycle acceptance; generic geometry alone cannot create Order_A; accepted stopped-A Order_A separately admits complete independent confirmed physical geometry as specified by algorithm.order.a.

## Bearish

#### 4.6 Reset

A confirmed Bearish Reaction resets only on the first strict `High > confirmed BoxTop` event. Equality is not Reset. When Reset and confirmation/break activity share a main candle, selected lower-TF ordering decides which event owns the state transition. Reset reopens **same-direction** Reaction ownership; opposite-direction patterns do not gate that search. A Reset event with an exact lower-TF second exposes that exact second; otherwise the owning main-candle start is the fallback representation.

#### 4.7 Post-Reset structural owner vs geometry-only evidence

After Reset, `_first_direct_same_direction_after_reset` scans eligible First candidates in chronological First-index order within the configured end index. It returns a candidate only if confirmation wins before strict loss of its frozen owning boundary. If invalidation wins first, candidates with First indexes at or before that invalidation main index are blocked. A candidate unfinished at the bounded end is skipped, so a later eligible candidate that completes healthily may be returned. The standalone initial Mode-A WAITING state retains its selected unfinished structural owner. The returned healthy result joins the canonical same-direction Reaction stream. `_first_geometry_after_reset` separately returns complete geometry without lifecycle acceptance; generic geometry alone cannot create Order_A; accepted stopped-A Order_A separately admits complete independent confirmed physical geometry as specified by algorithm.order.a.

## Source-level contract

Reset/confirmation same lower-position tie checks strict Reset first. Post-confirmation Reset excludes the decisive timestamp using one-microsecond later boundary. MarketChronology.reset_time uses second_time then main display_time fallback. Order_B separately demands proven first strict lower Reset crossing; unproven main fallback cannot create a reset leg.

Reset reopens same-direction Mode-A search after Reset main candle. Aligned Reset feeds Reset Blue and Order_B; opposite Reset feeds S Type-3. Reset is distinct from hard StopAll boundary.
