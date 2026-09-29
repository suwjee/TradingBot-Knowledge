---
id: "algorithm.a"
type: "algorithm"
status: "active"
authority: "executable"
title: "A Blue-pair triggers and confirming source"
version: "current"
related_entities: ["algorithm.blue", "algorithm.reaction", "algorithm.s"]
source_reference: ["06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L114", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L156", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L219", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L329", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L401", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L424", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L443", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L494", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L568", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L650", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L68", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L689", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L753", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.a_zone_detector", "source.blue_line_detector", "source.reaction_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L116", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L116"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.blue"]
name: "A"
aliases: ["A Zone", "AZone"]
---

# A Blue-pair triggers and confirming source

## Bullish

#### 6.1 Blue state and strict stops

A builds an immutable `BlueState` ledger from all Blue calculation state. Blue formation is exact: Scale Blue forms at its Reaction confirmation; Reset Blue uses the first strict lower-TF crossing of its broken level when available. Each Blue stop is the first strict Bullish crossing of its `source_extreme`; equality does not stop a Blue.

#### 6.2 Ordinary adjacent-Blue route

Ordinary A evaluates adjacent calculation-valid Blue states. A pair may trigger through the established direct or inherited-stop route. When the first Blue stopped before the second formed, continuation geometry is frozen over the owning interval; inherited-stop ownership uses the complete stop-candle through the aligned Reaction Break candle. Directional source selection is the minimum Low and strict comparisons preserve chronology. Exact equal-event ties use deterministic ordering; the second/current Blue may be reused for the next adjacent pair only when the current A's first strict stop and the next Blue formation satisfy the source lifecycle gate.

#### 6.3 Double-stop route

A Reset Blue marked calculation-invalid by the Blue double-stop rule can create the special A route with the previous valid Blue only when the previous Blue's first strict stop belongs to the invalid Reset Blue source candle. The route then requires the first qualifying same-direction canonical Reaction after the trigger chronology. A special route cannot duplicate a Reaction already owned by ordinary A, and earlier ordinary A lifecycle may suppress the special route when its first stop already completed before the special Reaction.

#### 6.4 Reaction confirmation and A source freeze

After a valid Blue-pair trigger, the first qualifying canonical Bullish Reaction confirms A. The A source/price is the minimum Low from the trigger main-candle open through the exact lower-TF Reaction confirmation, inclusive. Prices later in the same Break candle are outside A ownership and cannot move the source retroactively. Ties retain the earliest source unless the owning helper explicitly states otherwise.

#### 6.5 A stop and lifecycle handoff

A itself stops on the first strict Bullish crossing after its confirming Reaction. A historical stop before a route's `not_before` boundary belongs to the previous cycle; a later recross of the same level cannot be reinterpreted as the new cycle's first stop. The stop event opens S space.

## Bearish

#### 6.1 Blue state and strict stops

A builds an immutable `BlueState` ledger from all Blue calculation state. Blue formation is exact: Scale Blue forms at its Reaction confirmation; Reset Blue uses the first strict lower-TF crossing of its broken level when available. Each Blue stop is the first strict Bearish crossing of its `source_extreme`; equality does not stop a Blue.

#### 6.2 Ordinary adjacent-Blue route

Ordinary A evaluates adjacent calculation-valid Blue states. A pair may trigger through the established direct or inherited-stop route. When the first Blue stopped before the second formed, continuation geometry is frozen over the owning interval; inherited-stop ownership uses the complete stop-candle through the aligned Reaction Break candle. Directional source selection is the maximum High and strict comparisons preserve chronology. Exact equal-event ties use deterministic ordering; the second/current Blue may be reused for the next adjacent pair only when the current A's first strict stop and the next Blue formation satisfy the source lifecycle gate.

#### 6.3 Double-stop route

A Reset Blue marked calculation-invalid by the Blue double-stop rule can create the special A route with the previous valid Blue only when the previous Blue's first strict stop belongs to the invalid Reset Blue source candle. The route then requires the first qualifying same-direction canonical Reaction after the trigger chronology. A special route cannot duplicate a Reaction already owned by ordinary A, and earlier ordinary A lifecycle may suppress the special route when its first stop already completed before the special Reaction.

#### 6.4 Reaction confirmation and A source freeze

After a valid Blue-pair trigger, the first qualifying canonical Bearish Reaction confirms A. The A source/price is the maximum High from the trigger main-candle open through the exact lower-TF Reaction confirmation, inclusive. Prices later in the same Break candle are outside A ownership and cannot move the source retroactively. Ties retain the earliest source unless the owning helper explicitly states otherwise.

#### 6.5 A stop and lifecycle handoff

A itself stops on the first strict Bearish crossing after its confirming Reaction. A historical stop before a route's `not_before` boundary belongs to the previous cycle; a later recross of the same level cannot be reinterpreted as the new cycle's first stop. The stop event opens S space.

## Source-level contract

Ordinary BlueState ledger includes only calculation-valid lines while retaining original Blue ordinals. Scale forms at exact aligned confirmation and stop scan begins there. Reset forms at first strict broken-level crossing in source main, with open fallback, while its stop scan starts after that source main candle. Stop level is source_extreme, not line_price.

Adjacent pair expires at third Blue formation if present. Previous Blue must stop by expiry. Inherited-stop route has priority: use first qualifying aligned Reaction after owning boundary and before current formation, freeze its directional extreme, then cross from current formation. A live Scale Blue cannot borrow an inherited stop; stopped noninternal pair includes complete stop candle through aligned Break.

Without inheritance, previous stop before current formation freezes extreme from exact previous stop to just before current formation main. Crossing during current formation can trigger immediately; otherwise current must stop by expiry then strictly recross continuation level from its stop. Previous stop at/after current formation requires both stops, ordered by exact event plus mirrored stop-level tie. Same-event stops trigger directly; distinct stop events require crossing first stop-event extreme from later stop.

First aligned Reaction confirmation >= trigger and First >= both effective stop main times validates A. A source freezes trigger main open through exact confirmation inclusive. Ordinary A owns its Reaction before special double-stop; accepted special Blue pairs consume shared ordinals against later ordinary candidates. Current Blue can be reused only when A first strictly stops and next Blue forms >= that stop. Source,continuation,trigger and confirming Reaction provenance are separate.


## Expiry equality by owning operation

Stop guards reject an event strictly after third-Blue formation expiry and therefore retain equality. Lower-row crossing windows are expiry-exclusive. A same-event two-stop direct trigger can equal that formation expiry. Do not flatten the direct-stop and searched-crossing endpoints into one universal exclusive bound. Source lines 329-331, 401-403, 424-426 and 443-454 own these distinct checks.


## Exact lower fallback and inherited windows

A lower-window crossing fallback is allowed only when no lower rows exist in that interval. Existing lower rows without a strict crossing are decisive absence of crossing. A directional source range includes its exact end; empty lower source range alone falls back to complete containing mains. Chained inherited stop requires both Blues noninternal and previous exact stop before current formation, and spans prior stop main-open through complete aligned Break main. Unchained Reset inheritance spans prior formation event through aligned Break main-open inclusive. The qualifying aligned Reaction has First strictly after the window start and Break main strictly before current formation. A live nonchained Scale does not inherit.


## Canonical Blue ledger and A cycle ordering

A retains original sorted Blue ordinals while ordinary adjacent pairs use only calculation-valid states, including internal valid Blues. Third-state expiry is based on that valid ledger. Confirmation-main cycle ownership consumes Blue formations at or before the confirming Break; a triggered pair without qualifying canonical Reaction terminates ordinary search. Current Blue reuse requires an actual first strict A stop and next Blue formation at/after that stop. Special ownership removes ordinary candidates only on shared physical pair with strictly later trigger; equal trigger remains. Final output order is `(A source_time,trigger_event_time)`. Route and exact effective-stop fields are conditional provenance/presentation data; they do not substitute source/main/exact calculation gates.
