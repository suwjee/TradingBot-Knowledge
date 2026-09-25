---
id: "test.change_impact"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Regression change impact"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.regression_policy", "test.regression_model", "test.source_validation", "core.pipeline", "algorithm.reaction", "algorithm.blue", "algorithm.a", "algorithm.s", "algorithm.e", "algorithm.stopall", "algorithm.serialization"]
source_reference: []
---

# Regression change impact

Trace the changed source rule through the actual pipeline: RAW/Reaction/Reset → Blue → A → S/Order → E → StopAll/lifecycle → visibility → serialization. Shared direction policy, chronology and core identity can affect both directions; a change to an early stage may legitimately alter every downstream collection. Both references §§2, 15A; trading_pipeline.py lines 1903–2300 and 2549–2942.


A historical fixture is evidence of a past change, not permission to restore it. A Bug result does not become a new rule without current reference/source agreement. Record source-reference conflicts as unresolved and keep them out of acceptance gates.
