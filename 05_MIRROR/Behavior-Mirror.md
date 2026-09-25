---
id: "mirror.behavior"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Behavior mirror model"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["behavior.a", "behavior.s", "behavior.s.red", "behavior.s.blue", "behavior.s.blue.type1", "behavior.s.blue.type2", "behavior.s.blue.type3", "behavior.s.blue.type4", "behavior.e", "behavior.stopall", "core.e_numbering", "source.a_zone_detector", "source.s_zone_detector", "source.e_zone_detector", "source.lifecycle_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L219", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L482"]
---

# Behavior mirror model

> Scope: This mirror description is provisional. Full directional references and mixed source modules are absent from this Vault; verify each rule against retained local source before use.

The taxonomy is shared across directions. Direction changes formation geometry and strict stops, not behavior identity. Both references §0.1 and §22.4–22.7; `trading_pipeline.py#L1040-L1307`.

## A

One A behavior may arise through ordinary adjacent-Blue or special double-stop paths. Its candidate extreme and trigger mirror Low/min/< ↔ High/max/>; its A identity, Blue provenance, trigger event, and stage ownership do not. Both references §8; `a_zone_detector.py#L219-L311`, `#L568`.

## S

```text
S
├── Red
└── Blue
    ├── Type-1 (simple)
    ├── Type-2 (advanced)
    ├── Type-3 (Reset-leg)
    └── Type-4 (aligned-Reaction)
```

Those four public Blue formation types are canonical across directions. S candidate prices and strict crossing side mirror, while Red/Blue family, type number, A-parent identity and first Order_A ownership do not. Do not create Bullish S Type-1 or Bearish S Type-1 entities. Both references §9 and §22.5; `s_zone_detector.py#L315-L331`, `#L482-L638`; `trading_pipeline.py#L1130`.

## E

E has Red/Blue families and a **number** in the accepted lifecycle. E1/E2/E3 are instances or states of E, never separate algorithms. Parent/Order price geometry mirrors; same-family number progression, winner selection and ownership remain invariant. Both references §10.6–10.8; `e_zone_detector.py#L2267-L2463`.

## StopAll

StopAll is Mixed: strict price triggers mirror; gate type, priority, number, pending Blue-repeat keys, counter reset and hard cycle boundary remain shared. Type-1 `sequence-group-stop`, Type-2 `stopall-stop`, and Type-3 `opposite-s-group-stop` are common gate identities, not Bullish/Bearish variants. Both references §13 and §22.7; `lifecycle_engine.py#L115-L127`, `#L331-L455`, `#L487-L609`; `trading_pipeline.py#L1285`.
