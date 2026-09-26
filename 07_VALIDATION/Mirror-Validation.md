---
id: "test.mirror_validation"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Mirror validation"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["mirror.contract", "mirror.direction_mapping", "mirror.invariants", "mirror.exceptions", "test.invariant_validation", "test.mirror_policy", "test.direction_tests", "test.symmetry_tests", "test.mirror_regression", "source.direction_policy", "source.reaction_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
---

# Mirror validation

Validate Bullish fixtures and Bearish fixtures independently on identical physical RAW/settings, then check the directional mapping: trend Low/min/< ↔ High/max/>, opposite Reaction confirmation High > BoxTop ↔ Low < BoxBottom, First/context roles, Blue line geometry and Order direction. Equality never crosses. Market Doji remains GREEN. The retained direction policy and Reaction source support these local predicates. Full lifecycle, numbering, and output-schema symmetry are pending source capture and review.

Do not expect naturally observed Bullish and Bearish payloads to be identical. For a constructed reflected-price case, transform OHLC and preserve physical time/index to check the corresponding geometry, then verify lifecycle invariants separately. The bridge is now captured, but full accepted pipeline validation still requires fresh paired runs and a B/C rewrite for affected outcomes.
