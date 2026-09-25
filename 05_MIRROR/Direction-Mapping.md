---
id: "mirror.direction_mapping"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Verified direction mapping"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["market.direction", "market.crossing", "market.candle", "algorithm.reaction", "algorithm.blue", "algorithm.order", "source.direction_policy", "source.reaction_engine", "source.blue_line_detector", "source.a_zone_detector", "source.e_zone_detector"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L75", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L311"]
---

# Verified direction mapping

> Scope: This mirror description is provisional. Full directional references and mixed source modules are absent from this Vault; verify each rule against retained local source before use.

`direction_policy.py#L21-L70` supplies the shared primitive map; both synchronized references §15 list the same directional pairs. The mapped `value` must already be the appropriate price side. Do not substitute the stop predicate for the separate Reaction confirmation predicate.

| Atomic concept | Bullish | Bearish | Source |
|---|---|---|---|
| Trend extreme / strict stop input | Low | High | `direction_policy.py#L23`, `#L59-L69` |
| Opposite extreme | High | Low | `direction_policy.py#L24`, `#L59-L69` |
| Better trend extreme | smaller; minimum | larger; maximum | `direction_policy.py#L35-L39` |
| Directional strict crossing | `Low < level` | `High > level` | `direction_policy.py#L32-L33` |
| Reaction confirmation | `High > BoxTop` | `Low < BoxBottom` | `direction_policy.py#L41-L46`; `reaction_engine.py#L197`, `#L688` |
| Reaction confirmation box edge | Top | Bottom | `reaction_engine.py#L560-L598`; both references §6.2 |
| First Reaction tag | RED | GREEN | `direction_policy.py#L25`, `#L59-L69` |
| Reaction context tag | GREEN | RED | `direction_policy.py#L26`, `#L59-L69` |
| Opposite Order direction | Bearish | Bullish | `direction_policy.py#L28-L30`; `e_zone_detector.py#L151` |
| Mode-B Order inherited stop edge | prior healthy BoxTop | prior healthy BoxBottom | `reaction_engine.py#L1185-L1195`; both references §6.12 |
| Mode-A opposite Order outer stop | Bearish Order: maximum High | Bullish Order: minimum Low | `reaction_engine.py#L1137-L1195`; both references §6.12 |
| Blue Fibonacci level | `Top − 0.618 × (Top − reference)` | `Bottom + 0.618 × (reference − Bottom)` | `blue_line_detector.py#L75-L81` |
| Scale Blue line price | `Low + (High − Low)/3` | `High − (High − Low)/3` | `blue_line_detector.py#L217-L238` |
| Reset Blue line price | `Low + (High − Low)/5` | `High − (High − Low)/5` | `blue_line_detector.py#L246-L263` |
| Chained stopped-Blue source extreme | minimum Low over the fixed next-Break main candle | maximum High over the same time window | Both references §15; `a_zone_detector.py#L311-L390` |

All displayed crossings are strict: equality does **not** cross. Source: `direction_policy.py#L32-L46`, `blue_line_detector.py#L114-L116`, both references §15.

`Bottom ↔ Top` is a **role mapping**, not a command to swap all serialized `boxBottom`/`boxTop` field names. The Bearish adapter maps `box_top` to negated Bullish `box_bottom` and swaps their physical source indices/times; the public schema keeps both field names. `reaction_engine.py#L560-L598`; `trading_pipeline.py#L267-L282`.

The market candle color classifier is invariant: `open <= close` is GREEN, including a Doji. Only the detector-internal reflected role swaps GREEN/RED. `reaction_engine.py#L91-L93`, `#L560-L577`; both references §3.6.
