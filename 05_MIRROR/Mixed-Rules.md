---
id: "mirror.mixed_rules"
type: "mirror"
status: "active"
authority: "canonical"
title: "Mixed mirror rules"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["algorithm.stopall", "algorithm.order", "algorithm.e", "algorithm.internal_reaction", "algorithm.visibility", "source.reaction_engine", "source.e_zone_detector", "source.lifecycle_engine", "source.core_utils"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L311", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L311", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L638", "engine/pipeline/lifecycle_engine.py#L115", "engine/pipeline/lifecycle_engine.py#L1658", "engine/pipeline/lifecycle_engine.py#L1687", "engine/pipeline/e_zone_detector.py#L393", "engine/pipeline/reaction_engine.py#L1202"]
---

# Mixed mirror rules

Each row is a higher-level composition of separately classified atomic rules. “Invariant” never means that its directional price input is identical.

| Composite | Directional atom | Invariant atom | Evidence |
|---|---|---|---|
| StopAll | Strict stop of candidate/active StopAll: Bullish Low < level, Bearish High > level. | One `StopAll > E Red > S Red > E Blue > S Blue > A` priority, Type-1/2/3 gate identities, accepted Red/Blue keys, hard reset and new cycle. | Both references §13; `lifecycle_engine.py#L25-L35`, `#L115-L127`, `#L331-L455` |
| Order | Opposite Reaction direction, Mode-A outer extreme and Mode-B inherited edge; Order_B/C frozen range and exact crossing mirror. | Physical `(FirstIndex,BreakIndex)` identity, first parent-stop owner, independent creation causes, cause merging and use-route distinction. | Both references §6.12, §10.2–10.3C, §11; `core_utils.py#L19-L29`; `reaction_engine.py#L1137-L1195`; `e_zone_detector.py#L393-L830`; `lifecycle_engine.py#L728-L800` |
| E | Parent/Order price relation and strict stop side mirror. | E Red/Blue family, recursive continuation, number progression, same-source reconciliation and accepted ownership. | Both references §10.1–10.8; `e_zone_detector.py#L329-L357`, `#L1901-L2463` |
| Internal Reaction | The underlying Reaction geometry and its containment prices are direction-aware. | Physical First/confirmation chronology, internal classification meaning and calculation evidence are shared. The mixed-cause public E/StopAll prohibition is **unresolved** below. | Both references §6.14, §14; `reaction_engine.py#L1202-L1376`; `lifecycle_engine.py#L777-L800`, `#L1658-L1708` |

Internal does **not** mean “discard all downstream A/S/E/StopAll.” The source retains internal Reaction evidence for calculation. The accepted physical-Order ledger excludes an internal native Mode-B identity only when all accepted causes are reset-leg (`lifecycle_engine.py#L777-L800`). **Unresolved conflict:** both references §14 say the final E/StopAll filter is also reset-leg-only, but `forbidden_internal_order_b` returns true when *any* reset-leg cause or reset-leg timestamp is present on an internal native Mode-B owner (`lifecycle_engine.py#L1658-L1678`). Whether an additional parent-stop/blue-leg cause protects the final E/StopAll output therefore cannot be stated as a settled Mirror rule.
