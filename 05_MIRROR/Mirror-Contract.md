---
id: "mirror.contract"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Mirror contract"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["market.direction", "core.behavior_model", "core.lifecycle", "algorithm.reaction", "source.direction_policy", "source.reaction_engine", "source.trading_pipeline"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
---

# Mirror contract

> Scope: All nine main Engine modules are captured, but full HPZR6 references are optional external evidence. Current Order_B/C mirror behavior is diagnostic only until those routes are rewritten and accepted.

## Definition and authority


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

All nine main Engine modules are hash-pinned by `_INDEX/source-hashes.json`; comprehensive directional references are registered as optional external evidence. Current B/C symmetry can be inspected in source but cannot define the accepted future B/C Mirror contract. Audit output cannot establish a Mirror trading rule. No market-specific or example-specific branch becomes a Mirror rule.
