---
id: "test.source_validation"
type: "test"
status: "canonical"
authority: "normative"
title: "Fixture to source validation"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.fixture_model", "test.fixture_registry", "mirror.source_map", "algorithm.reaction", "algorithm.order", "source.reaction_engine", "source.s_zone_detector", "source.e_zone_detector", "source.lifecycle_engine", "source.trading_pipeline"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L277"]
---

# Fixture to source validation

For each case, trace Fixture → public Behavior when one exists → Algorithm → physical Source module → real function. Reaction, Reset, Blue and Order cases may have behavior=unknown because they are not Behaviors. Keep the algorithm/source edge even then. The Vault builder checks case relation targets, retained source module existence and named top-level/class method symbols. A complete bridge trace remains pending because its source is absent from this Vault.


An optional source_function must be a function or Class.method present in the cited module. Use unknown rather than a guessed symbol. The supplied prompt's conditional Reaction Mode-B refresh is **not** an active rule: retained `s_zone_detector.py` lines 277–321 keep the first stopped-A Order_A even before S decision. Reaction Mode-B names a Reaction mode, not another physical Order creation route. Preserve older refresh results only as Historical fixtures.
