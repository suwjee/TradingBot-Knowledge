---
id: "mirror.contract"
type: "mirror"
status: "active"
authority: "canonical"
title: "Mirror contract"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["market.direction", "core.behavior_model", "core.lifecycle", "algorithm.reaction", "source.direction_policy", "source.reaction_engine", "source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L11", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L11", "engine/pipeline/direction_policy.py#L21", "engine/pipeline/reaction_engine.py#L560", "engine/bridge/trading_pipeline.py#L2300"]
---

# Mirror contract

## Definition and authority

Mirror is the deterministic directional transformation of the **one canonical algorithm model** into Bullish or Bearish execution. A directional price, extreme, comparison, confirmation side, or detector-internal color role changes only where the synchronized references and current source specify it. Behavior identity, state-machine meaning, physical chronology and provenance, lifecycle ownership and priority, numbering model, and public serialization key structure remain invariant. This is canonical *knowledge*; executable ownership stays with the cited engine modules. Bullish reference §15 (`engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L641`); Bearish reference §15 (`engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L641`); `direction_policy.py#L1`.

```text
Canonical algorithm and behavior contracts
                  ↓
Direction policy and source-owned directional geometry
                  ↓
Bullish or Bearish execution
                  ↓
Shared lifecycle, visibility, and serialization contracts
```

The bridge prepares both directional Reaction streams for dependent stages, runs the same stage order, and serializes the chosen direction through the same payload shape. This is execution of one contract under two directional inputs, not two independent behavior taxonomies. `trading_pipeline.py#L2300`, `#L2776`; both references §15A.

## Mirror is not

- A duplicated Bullish and Bearish algorithm, behavior folder, E numbering system, or lifecycle engine.
- A blanket sign inversion of every output field: physical indexes, event times, causes, nullable fields, order identity, and serialization keys retain their own contracts.
- Permission to infer missing directional rules. Unproven transformations remain unresolved until verified in the pinned references and source.

`reaction_engine.py#L560` mirrors coordinates while preserving candidate provenance; `lifecycle_engine.py#L25` owns one priority table; `trading_pipeline.py#L239` and `#L2776` own the shared output structure.

## Category rule

Classify each *atomic rule* once: **Directional** if its predicate/price role changes; **Invariant** if it does not; **Mixed** only for a higher-level rule composed of both. The algorithm matrix is a summary of atomic classifications, not an additional rule category. See `Direction-Mapping.md`, `Invariant-Rules.md`, and `Mixed-Rules.md`.

## Evidence boundary

The two V5.4.11 HPZR6 references and nine current engine modules are hash-pinned by `_INDEX/source-hashes.json`. A reference–source disagreement must be recorded as unresolved, with both anchors; neither side silently wins. Current OrderAudit output alone cannot establish a Mirror trading rule. No market-specific or example-specific branch becomes a Mirror rule. Both references §0.2 and §11; `trading_pipeline.py#L1537`.
