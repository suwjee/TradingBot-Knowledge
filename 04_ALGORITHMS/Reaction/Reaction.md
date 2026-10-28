---
id: "algorithm.reaction"
type: "algorithm"
status: "active"
authority: "executable"
title: "Reaction geometry and structural ownership"
version: "current"
related_entities: ["algorithm.internal_reaction", "algorithm.reset", "core.identity", "source.reference_consistency"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1436", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1564", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1592", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1658", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1991", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L2133", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L2316", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L2357", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L2395"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-sensitive geometry"
implemented_by: ["source.reaction_engine", "source.direction_policy", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L148", "06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L148"]
mirror_links: ["mirror.contract"]
name: "Reaction"
aliases: ["Reaction detection"]
reference_agreement: "ambiguous"
reference_conflicts: ["REF-REACTION-SUCCESSOR"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Reaction geometry and structural ownership

## Bullish

#### 4.1 Data and color contract

`Candle` carries `index`, native `timestamp`, display time, immutable market `tag`, and Decimal OHLC. `Candidate` carries First/box sources, Mode A/B, optional anchor and leg boundary, Break, intrabar start, cross-direction gate metadata, public box/number metadata and internal/public ownership flags. `ResetEvent` records main index/time, optional exact lower-TF second, broken level, and the owning Reaction First index.

#### 4.2 Canonical directional geometry

For Bullish, the canonical First candle role is **FirstRed** (`RED`) following the opposite context color `GREEN`. Confirmation is the first strict breakout satisfying `High > BoxTop`. The confirmation edge is `BoxTop`. The opposite box edge `BoxBottom` may evolve only through chronology available up to the exact confirmation event.

The source does not maintain an independent hand-written Bearish state machine: Bearish geometry executes the Bullish reference state machine through exact Decimal sign/High-Low/color-role reflection. Therefore the initial leg, Mode-A invalidation, breakout/breakdown priority, Reset priority, post-confirmation handling, and lower-timeframe tie rules share one mechanical geometry contract. The reflected color role is internal coordinate machinery only; market Doji remains GREEN.

#### 4.3 Mode A / leg-start ownership

Mode A is the first Reaction of a leg. The detector establishes the contiguous context run, builds the directional First candidate, preserves any qualifying adjacent anchor, and freezes the outer leg boundary. Before confirmation, strict outer-boundary invalidation owns the candidate ahead of confirmation when lower-TF chronology proves it first. In the standalone initial Mode-A WAITING state, an invalidated owner releases search and nested geometry cannot confirm while its selected structural owner remains unresolved. The bounded Unified post-Reset search has the separate completion-selection contract in Section 4.7.

#### 4.4 Mode B / normal ownership

After a confirmed Reaction, normal search uses the running directional context and the required First color. A correctly colored confirmation main candle can seed the next Mode-B First in initial, post-Reset and normal branches that call the shared successor helper. The strictly later remainder first checks for Reset against analysis.extreme. If reuse survives, current Source sets whole_confirmation_candle=True: both successor edges use all lower rows of the complete confirmation main candle, and intrabar_start is the main open. The successor boundary is not limited to post-event prices. Published geometry of the just-confirmed Reaction has its separate confirmation-bounded refinement.

#### 4.5 Exact confirmation and published box

If the Break main candle owns the full-main-candle opposite extreme, only lower-TF prices at or before the first strict confirmation may define the published opposite edge. Later prices in that same main candle cannot retroactively alter Reaction/Order geometry. If lower-TF chronology cannot prove a refinement, detector geometry is retained rather than guessed. Equal eligible extremes retain the earliest main-candle owner.

#### 4.7 Post-Reset structural owner vs geometry-only evidence

After Reset, `_first_direct_same_direction_after_reset` scans eligible First candidates in chronological First-index order within the configured end index. It returns a candidate only if confirmation wins before strict loss of its frozen owning boundary. If invalidation wins first, candidates with First indexes at or before that invalidation main index are blocked. A candidate unfinished at the bounded end is skipped, so a later eligible candidate that completes healthily may be returned. The standalone initial Mode-A WAITING state retains its selected unfinished structural owner. The returned healthy result joins the canonical same-direction Reaction stream. `_first_geometry_after_reset` separately returns complete geometry without lifecycle acceptance; Order_B still requires canonical membership; accepted stopped-A Order_A has its separate complete-geometry admission rule.

## Bearish

#### 4.1 Data and color contract

`Candle` carries `index`, native `timestamp`, display time, immutable market `tag`, and Decimal OHLC. `Candidate` carries First/box sources, Mode A/B, optional anchor and leg boundary, Break, intrabar start, cross-direction gate metadata, public box/number metadata and internal/public ownership flags. `ResetEvent` records main index/time, optional exact lower-TF second, broken level, and the owning Reaction First index.

#### 4.2 Canonical directional geometry

For Bearish, the canonical First candle role is **FirstGreen** (`GREEN`) following the opposite context color `RED`. Confirmation is the first strict breakdown satisfying `Low < BoxBottom`. The confirmation edge is `BoxBottom`. The opposite box edge `BoxTop` may evolve only through chronology available up to the exact confirmation event.

The source does not maintain an independent hand-written Bearish state machine: Bearish geometry executes the Bullish reference state machine through exact Decimal sign/High-Low/color-role reflection. Therefore the initial leg, Mode-A invalidation, breakout/breakdown priority, Reset priority, post-confirmation handling, and lower-timeframe tie rules share one mechanical geometry contract. The reflected color role is internal coordinate machinery only; market Doji remains GREEN.

#### 4.3 Mode A / leg-start ownership

Mode A is the first Reaction of a leg. The detector establishes the contiguous context run, builds the directional First candidate, preserves any qualifying adjacent anchor, and freezes the outer leg boundary. Before confirmation, strict outer-boundary invalidation owns the candidate ahead of confirmation when lower-TF chronology proves it first. In the standalone initial Mode-A WAITING state, an invalidated owner releases search and nested geometry cannot confirm while its selected structural owner remains unresolved. The bounded Unified post-Reset search has the separate completion-selection contract in Section 4.7.

#### 4.4 Mode B / normal ownership

After a confirmed Reaction, normal search uses the running directional context and the required First color. A correctly colored confirmation main candle can seed the next Mode-B First in initial, post-Reset and normal branches that call the shared successor helper. The strictly later remainder first checks for Reset against analysis.extreme. If reuse survives, current Source sets whole_confirmation_candle=True: both successor edges use all lower rows of the complete confirmation main candle, and intrabar_start is the main open. The successor boundary is not limited to post-event prices. Published geometry of the just-confirmed Reaction has its separate confirmation-bounded refinement.

#### 4.5 Exact confirmation and published box

If the Break main candle owns the full-main-candle opposite extreme, only lower-TF prices at or before the first strict confirmation may define the published opposite edge. Later prices in that same main candle cannot retroactively alter Reaction/Order geometry. If lower-TF chronology cannot prove a refinement, detector geometry is retained rather than guessed. Equal eligible extremes retain the earliest main-candle owner.

#### 4.7 Post-Reset structural owner vs geometry-only evidence

After Reset, `_first_direct_same_direction_after_reset` scans eligible First candidates in chronological First-index order within the configured end index. It returns a candidate only if confirmation wins before strict loss of its frozen owning boundary. If invalidation wins first, candidates with First indexes at or before that invalidation main index are blocked. A candidate unfinished at the bounded end is skipped, so a later eligible candidate that completes healthily may be returned. The standalone initial Mode-A WAITING state retains its selected unfinished structural owner. The returned healthy result joins the canonical same-direction Reaction stream. `_first_geometry_after_reset` separately returns complete geometry without lifecycle acceptance; Order_B still requires canonical membership; accepted stopped-A Order_A has its separate complete-geometry admission rule.

## Source-level contract

Mode-A Bullish FirstRed follows a contiguous GREEN run. Its opening BoxTop is maximum High of that run and FirstRed; equality keeps the context source. Frozen leg floor and adjacent anchor are separate from evolving BoxBottom. Bearish uses FirstGreen after RED, minimum Low for BoxBottom and frozen ceiling. Strict leg invalidation wins a true same lower-position tie against confirmation.

Normal Mode B uses running Bullish High/Bearish Low for confirmation edge. Opposite geometry begins after that edge source through First and evolves while waiting. The successor helper uses full confirmation-candle geometry after its post-event Reset reuse check; Unified initial confirmation also calls that helper when no same-Break Reset is recorded. Current Unified initial, post-Reset and normal branches use analysis.extreme in both directions; stored BoxBottom/BoxTop is fallback only without exact analysis.

Canonical First/Break identity and original stream number survive Reset/internal marking. Published clone preserves confirmation edge and exact-confirmation opposite geometry. Geometry-only continuation does not become canonical. Independently complete stopped-A Order_A may retain physical identity with reactionNumber=0 under the current exception. Inputs are Decimal Candle sequences and MarketChronology; outputs are DetectionResult.reactions plus separate resets.


## Unified initial branch and successor provenance

Initial confirmation now calls _candidate_from_confirmation_remainder when same-Break Reset does not win. The helper first checks strictly later rows for Reset against analysis.extreme; surviving correctly colored Break candles seed Mode B from the complete confirmation candle, with intrabar_start at main open. Current Reference section4.4 separately says post-event chronology controls eligible boundary prices; its scope remains ambiguous against complete-candle successor geometry. Preserve this distinction rather than inventing a post-event-only Source rule.

The gate-geometry cache is run-scoped and bounded. Cached Candidates are cloned on return so caller mutation does not alter retained geometry. The bounded post-Reset completion scanner skips unfinished candidates; its stronger owner-blocking docstring remains a comment qualification rather than an executed branch guarantee.
