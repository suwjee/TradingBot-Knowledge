---
id: "algorithm.blue"
type: "algorithm"
status: "active"
authority: "executable"
title: "Scale and Reset Blue calculation"
version: "current"
related_entities: ["algorithm.a", "algorithm.reaction", "algorithm.reset", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L299", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L84", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.blue_line_detector", "source.reaction_engine", "source.direction_policy"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L96", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L96"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.reaction", "algorithm.reset"]
name: "Blue"
aliases: ["Blue Line", "BlueLine"]
reference_agreement: "conflict"
reference_conflicts: ["REF-BLUE-ENDPOINT"]
---

# Scale and Reset Blue calculation

## Bullish

#### 5.1 Inputs and reference level

Blue consumes canonical Bullish Reactions and Bullish Resets. For each Reaction, the scale reference is the Mode-A boundary when present; otherwise it is the previous Reaction opposite edge. The 0.618 level is `BoxTop − 0.618 × (BoxTop − reference)`.

#### 5.2 Scale strikes

Within Reaction First..Break inclusive, a new strike requires a strictly lower `Low` than the previous confirmed strike (or than the Fibonacci level for the first strike). Pending strikes confirm on a `GREEN` main candle. Pending intrabar confirmation scans lower rows from pending source time through the Break main-candle close, exclusive. A strict Bullish Low penetration (Bearish High penetration) is added before testing that row's strict Reaction crossing. The helper returns at the first crossing with a nonempty eligible set, selecting the earliest most-directional eligible extreme. A crossing while the eligible set is empty does not end the scan. The decisive row is included. This conditional scan is the executable contract; the Reference's unconditional first-confirmation endpoint is disputed in source.reference_consistency.

A Scale Blue is emitted when strike count increases and spacing ownership permits it (first Blue, or at least one healthy Reaction since the previous Blue). Its source is the decisive strike; line price is `Low + (High − Low) / 3` and its drawing interval is one timeframe before/after the source time.

#### 5.3 Reset Blue and double-stop calculation validity

A Reset Blue is sourced by the Reset main candle, with source extreme `Low`, broken level from Reset, and line price `Low + (High − Low) / 5`. If the prior Blue first strict-stops on that same Reset candle and the Reset source extends strictly farther in the Bullish direction than the prior Blue source extreme, the new Reset Blue is marked `calculation_valid=False`. That invalid line remains calculation evidence for the A double-stop route but is excluded from public Blue output.

#### 5.4 Internal/public Blue

A Blue becomes behavior-internal when its owning Reaction is internal, or when both the source extreme and rendered line price lie strictly inside the same protected healthy Reaction. Drawing offset alone does not create internal ownership. Public Blue is exactly `calculation_valid and not behavior_internal`.

## Bearish

#### 5.1 Inputs and reference level

Blue consumes canonical Bearish Reactions and Bearish Resets. For each Reaction, the scale reference is the Mode-A boundary when present; otherwise it is the previous Reaction opposite edge. The 0.618 level is `BoxBottom + 0.618 × (reference − BoxBottom)`.

#### 5.2 Scale strikes

Within Reaction First..Break inclusive, a new strike requires a strictly higher `High` than the previous confirmed strike (or than the Fibonacci level for the first strike). Pending strikes confirm on a `RED` main candle. Pending intrabar confirmation scans lower rows from pending source time through the Break main-candle close, exclusive. A strict Bullish Low penetration (Bearish High penetration) is added before testing that row's strict Reaction crossing. The helper returns at the first crossing with a nonempty eligible set, selecting the earliest most-directional eligible extreme. A crossing while the eligible set is empty does not end the scan. The decisive row is included. This conditional scan is the executable contract; the Reference's unconditional first-confirmation endpoint is disputed in source.reference_consistency.

A Scale Blue is emitted when strike count increases and spacing ownership permits it (first Blue, or at least one healthy Reaction since the previous Blue). Its source is the decisive strike; line price is `High − (High − Low) / 3` and its drawing interval is one timeframe before/after the source time.

#### 5.3 Reset Blue and double-stop calculation validity

A Reset Blue is sourced by the Reset main candle, with source extreme `High`, broken level from Reset, and line price `High − (High − Low) / 5`. If the prior Blue first strict-stops on that same Reset candle and the Reset source extends strictly farther in the Bearish direction than the prior Blue source extreme, the new Reset Blue is marked `calculation_valid=False`. That invalid line remains calculation evidence for the A double-stop route but is excluded from public Blue output.

#### 5.4 Internal/public Blue

A Blue becomes behavior-internal when its owning Reaction is internal, or when both the source extreme and rendered line price lie strictly inside the same protected healthy Reaction. Drawing offset alone does not create internal ownership. Public Blue is exactly `calculation_valid and not behavior_internal`.

## Source-level contract

Mode A resets prior strike-count baseline and requires anchor_value or leg_boundary_value; Mode B uses previous aligned opposite edge. Scale emission requires an existing previous count and strict count increase. Mode-A baseline alone does not emit Scale Blue. Pending extrema replace only on strict improvement; equal eligible lower extremes keep earliest row.

Pending main strikes confirm GREEN Bullish/RED Bearish. Remaining pending intrabar strikes use the conditional crossing-and-eligible-set window described above, including the decisive row. Source_extreme can be lower-TF while rendered line_price uses source main High/Low. Scale/Reset share spacing state; first Blue bypasses spacing, later Blue needs one completed aligned Reaction since prior Blue. calculation_valid and behavior_internal are distinct. Invalid Reset Blue remains input for special A; public requires valid and not internal.


## Retained emissions and shared spacing

Shared spacing is driven by canonical calculation chronology. Emitting any retained Scale or Reset Blue resets the spacing counter, including a Reset marked calculation-invalid or a line later marked behavior-internal. Those flags affect later ownership/projection; they do not undo emission history or renumber canonical Reaction counts.
