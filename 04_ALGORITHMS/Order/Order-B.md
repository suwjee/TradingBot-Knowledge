---
id: "algorithm.order.b"
type: "algorithm"
status: "active"
authority: "executable"
title: "Order_B accepted HH/LL reset-leg creation"
version: "current"
related_entities: ["algorithm.order", "algorithm.orderaudit", "algorithm.reset"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L101", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.order_audit_engine", "source.trading_pipeline", "source.reaction_engine", "source.e_zone_detector", "source.lifecycle_engine"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L219", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L219"]
mirror_links: ["mirror.contract"]
name: "Order_B"
aliases: ["Order B", "Reset-leg Order"]
---

# Order_B accepted HH/LL reset-leg creation

## Bullish

#### 10.1 Eligibility and post-stop owner

Order_B is eligible only after an accepted lifecycle stop (`A`, `S`, `E`, or `StopAll`) selected by the accepted lifecycle owner of the stopped main candle. The stop opens eligibility; it is **not** the geometric LL anchor.

#### 10.2 Geometric behavior anchor

For each reset Bullish Reaction, choose the latest accepted behavior source that exists strictly before the Reaction FirstRed candle, independent of current dominance. Valid anchor families are A/S/E/StopAll. When several lifecycle projections share exactly one source candle, lifecycle priority and number resolve only that exact-source tie.

#### 10.3 LL construction and extension

Use the closed main-candle range from anchor behavior source through reset Reaction FirstRed, inclusive:

`LL = minimum Low(anchor candle .. reset Reaction FirstRed)`

Only a strict better Low replaces the current source, so equal extremes retain the earliest source. The LL source must be strictly before the reset Reaction FirstRed. It must also extend beyond the anchor itself: the LL must be strictly below the anchor behavior `Low`; equality invalidates the setup.

#### 10.4 Reset and strict break

The reset Reaction must first produce its canonical Reset. Search **strictly after** that exact Reset event for the first lower-TF `Low < LL`. Equality is not a break. This exact lower-TF timestamp is `strict_break_time`.

#### 10.5 Accepted-A expiry

Let the next accepted A formation after the reset Reaction First be `A_next`. If `A_next <= strict_break_time`, the pending reset leg expires. A is upstream of Order_B feedback, so this hard expiry prevents a stale S/E/StopAll setup from firing inside a newer A lifecycle.

#### 10.6 Physical canonical opposite Reaction

After the strict break, choose the first canonical Bearish Reaction satisfying both:

`strict_break_time <= FirstTime`

`strict_break_time < ConfirmationTime`

Thus **FirstTime equality is valid**, while the price break and confirmation remain strict. Canonical-Reaction membership is mandatory; geometry-only evidence cannot become Order_B.

#### 10.7 Provenance and identity

Order_B records post-stop behavior, geometric anchor type/source/extreme, reset Reaction identity/confirmation, Reset index/broken level/time, frozen LL boundary/source, exact strict break, and final physical opposite Reaction identity/confirmation. Physical Order identity remains `(FirstIndex, BreakIndex)`. Multiple reset-leg causes may merge into one identity; they do not create duplicate physical Orders.

## Bearish

#### 10.1 Eligibility and post-stop owner

Order_B is eligible only after an accepted lifecycle stop (`A`, `S`, `E`, or `StopAll`) selected by the accepted lifecycle owner of the stopped main candle. The stop opens eligibility; it is **not** the geometric HH anchor.

#### 10.2 Geometric behavior anchor

For each reset Bearish Reaction, choose the latest accepted behavior source that exists strictly before the Reaction FirstGreen candle, independent of current dominance. Valid anchor families are A/S/E/StopAll. When several lifecycle projections share exactly one source candle, lifecycle priority and number resolve only that exact-source tie.

#### 10.3 HH construction and extension

Use the closed main-candle range from anchor behavior source through reset Reaction FirstGreen, inclusive:

`HH = maximum High(anchor candle .. reset Reaction FirstGreen)`

Only a strict better High replaces the current source, so equal extremes retain the earliest source. The HH source must be strictly before the reset Reaction FirstGreen. It must also extend beyond the anchor itself: the HH must be strictly above the anchor behavior `High`; equality invalidates the setup.

#### 10.4 Reset and strict break

The reset Reaction must first produce its canonical Reset. Search **strictly after** that exact Reset event for the first lower-TF `High > HH`. Equality is not a break. This exact lower-TF timestamp is `strict_break_time`.

#### 10.5 Accepted-A expiry

Let the next accepted A formation after the reset Reaction First be `A_next`. If `A_next <= strict_break_time`, the pending reset leg expires. A is upstream of Order_B feedback, so this hard expiry prevents a stale S/E/StopAll setup from firing inside a newer A lifecycle.

#### 10.6 Physical canonical opposite Reaction

After the strict break, choose the first canonical Bullish Reaction satisfying both:

`strict_break_time <= FirstTime`

`strict_break_time < ConfirmationTime`

Thus **FirstTime equality is valid**, while the price break and confirmation remain strict. Canonical-Reaction membership is mandatory; geometry-only evidence cannot become Order_B.

#### 10.7 Provenance and identity

Order_B records post-stop behavior, geometric anchor type/source/extreme, reset Reaction identity/confirmation, Reset index/broken level/time, frozen HH boundary/source, exact strict break, and final physical opposite Reaction identity/confirmation. Physical Order identity remains `(FirstIndex, BreakIndex)`. Multiple reset-leg causes may merge into one identity; they do not create duplicate physical Orders.

## Source-level contract

Eligible post-stop event is strictly before reset aligned First main time. Stop ownership chooses accepted active lifecycle owner per stopped main using priority/number/source/event. Geometric anchor is independently latest accepted source strictly before First; exact same-source projections collapse by priority/number/type, but later lower-priority source can still become anchor.

Aligned Reaction confirmation < its Reset. LL/HH strictly extends anchor main extreme and source < aligned First. Boundary cross starts bisect_right(exact Reset), excluding Reset-time equality. Canonical opposite choices sort confirmation then First/Break. FirstTime==strict break is valid; confirmation==strict break is invalid.

Next accepted A expiry uses trigger_event_time strictly after aligned First; trigger <= strict break expires. Source time or later confirmation is not substituted. Exact full cause identity drives at most eight feedback passes. Blue/A/initial S reuse while dependent accepted state recalculates; repeated changed cause identity/eighth-pass failure raises. Final visibility requires same discovered and converged cause identity.


## Reset-event fallback proof

If the aligned Reset carries an exact second_time, the chronology Reset representation supplies the event. Otherwise Order_B independently resolves the Reset main candle to the first strict direction-specific crossing of broken_level within that complete main interval using selected lower rows. If no strict crossing is proven, the reset-leg setup is skipped. An eligible owning aligned Reaction must confirm strictly before the resolved Reset event.
