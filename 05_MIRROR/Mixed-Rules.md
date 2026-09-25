---
id: "mirror.mixed_rules"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Mixed mirror rules"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["algorithm.stopall", "algorithm.order", "algorithm.e", "algorithm.internal_reaction", "algorithm.visibility", "source.reaction_engine", "source.e_zone_detector", "source.lifecycle_engine", "source.core_utils"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1202"]
---

# Mixed mirror rules

> Scope: This mirror description is provisional. Full directional references and mixed source modules are absent from this Vault; verify each rule against retained local source before use.

Each row is a higher-level composition of separately classified atomic rules. “Invariant” never means that its directional price input is identical.

| Composite | Directional atom | Invariant atom | Evidence |
|---|---|---|---|
| StopAll | Strict stop of candidate/active StopAll: Bullish Low < level, Bearish High > level. | One `StopAll > E Red > S Red > E Blue > S Blue > A` priority, Type-1/2/3 gate identities, accepted Red/Blue keys, hard reset and new cycle. | Both references §13; `lifecycle_engine.py#L25-L35`, `#L115-L127`, `#L331-L455` |
| E | Parent/Order price relation and strict stop side mirror. | E Red/Blue family, recursive continuation, number progression, same-source reconciliation and accepted ownership. | Both references §10.1–10.8; `e_zone_detector.py#L329-L357`, `#L1901-L2463` |
| Internal Reaction | The underlying Reaction geometry and its containment prices are direction-aware. | Physical First/confirmation chronology, internal classification meaning and calculation evidence are shared. The mixed-cause public E/StopAll prohibition is **unresolved** below. | Both references §6.14, §14; `reaction_engine.py#L1202-L1376`; `lifecycle_engine.py#L777-L800`, `#L1658-L1708` |
