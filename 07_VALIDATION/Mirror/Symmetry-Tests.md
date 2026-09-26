---
id: "test.symmetry_tests"
type: "test"
status: "canonical"
authority: "normative"
title: "Constructed mirror symmetry checks"
related_entities: ["test.mirror_policy", "test.mirror_validation", "test.direction_tests", "test.mirror_regression", "mirror.contract", "mirror.invariants", "mirror.exceptions", "source.reaction_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560", "06_SOURCE/Code/engine/pipeline/direction_policy.py#L21"]
---

# Constructed mirror symmetry checks

**Definition and purpose.** A controlled reflected-price input tests a specified directional transformation while keeping candle order, epoch time, physical indexes and non-price identity fixed. It is a constructed test, not a claim that two naturally observed directions must match.

**Related algorithm and source.** The Reaction engine has explicit reflected candle/candidate coordinates (`reaction_engine.py#L560-L703`); `direction_policy.py#L21-L70` supplies strict directional extrema/crossing. Reflect OHLC consistently around a documented reference level and transform expected prices back before comparing only fields covered by the asserted mirror rule. Preserve Decimal precision and Doji semantics.

**Invariant checks.** Compare retained Reaction chronology, directional crossings and physical indexes under the stated transformation. The retained source uses `analysis.extreme` for the post-confirmation Reset when available in both directions and the directional structural box boundary when it is absent. Keep a focused regression for both branches. Downstream Order/E/StopAll ownership, lifecycle priority and public serialization now have captured source, but B/C-dependent conclusions require a corrected accepted contract and fresh mirror runs. The mixed-cause Internal-Reaction final visibility rule remains unresolved.

**Validation relation.** Pin original and transformed RAW hashes, transformation formula, both source/reference identities and output diffs. `test.direction_tests` checks each side individually before claiming a mirrored relationship.
