---
id: "mirror.directional_rules"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Directional rule components"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["algorithm.reaction", "algorithm.reset", "algorithm.blue", "algorithm.a", "algorithm.s", "algorithm.e", "algorithm.stopall", "source.direction_policy", "source.reaction_engine", "source.blue_line_detector", "source.a_zone_detector", "source.s_zone_detector", "source.e_zone_detector", "source.lifecycle_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L75", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L97", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L223"]
---

# Directional rule components

> Scope: This mirror description is provisional. Full directional references and mixed source modules are absent from this Vault; verify each rule against retained local source before use.

This page lists the transforming part of each **Mixed** algorithm. The invariant part is cited to prevent the whole algorithm from being mislabeled Directional. The exact low/high mapping is in `Direction-Mapping.md`.

| Algorithm | Directional component | Invariant component | Grounding |
|---|---|---|---|
| Reaction | First/context roles RED/GREEN ↔ GREEN/RED; Bullish High > BoxTop confirmation and Low-based invalidation/refinement; Bearish Low < BoxBottom confirmation and High-based invalidation/refinement. | Candidate/Break identity, Mode A/B state-machine meaning, exact-event race and physical ownership. | Both references §6.2–6.9; `reaction_engine.py#L174-L560`, `#L560-L703` |
| Reset | Strict break of the previous opposite boundary: Bullish Low < BoxBottom; Bearish High > BoxTop. Same-Break frozen edge is directionally selected from `analysis.extreme`. | Reset identity, event time, Break owner and exclusion of that Break as a new Mode-B First after same-Break Reset. | Both references §6.6–6.8; `reaction_engine.py#L247-L267`, `#L1562-L1581` |
| Blue | Fibonacci, strike extreme and confirming color, scale/reset line price and strict Blue stop mirror by direction. | Scale/Reset Blue kinds, strike-count state, source chronology and lifecycle position. | Both references §7, §15; `blue_line_detector.py#L75-L81`, `#L139-L204`, `#L217-L282` |
| A | Candidate extreme, inherited Blue stop price, strict trigger and source price use trend-side Low/min or High/max. | One A identity, ordinary/special formation routes, parent/trigger time ownership and A stage. | Both references §8; `a_zone_detector.py#L97-L166`, `#L219-L311` |
| S | A stop, candidate trend extreme, candidate/Order strict race and resulting price geometry mirror. | One S identity, Red/Blue family and Blue Type-1..4 identities, immutable first Order_A ownership. | Both references §9; `s_zone_detector.py#L223-L270`, `#L315-L331`, `#L482-L595` |
| StopAll | Its strict price stop is Bullish Low < level versus Bearish High > level. | Gate types, priority, exact Blue-group keys, number/counter reset and hard cycle boundary. | Both references §13; `lifecycle_engine.py#L115-L127`, `#L331-L455` |

The detector modules may implement the mapped geometry explicitly. `direction_policy.py` supplies shared primitives but does not own Blue formulas, S/E candidate state, or StopAll lifecycle. Treat the source-owned branches as current implementation facts, and verify both directions before changing them. `direction_policy.py#L1-L10`; `blue_line_detector.py#L75-L81`; `lifecycle_engine.py#L1-L5`.
