---
id: "test.baseline_policy"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Trusted baseline policy"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.regression_policy", "test.zero_difference", "test.fixture_registry", "test.regression_model", "algorithm.serialization", "source.trading_pipeline"]
source_reference: []
---

# Trusted baseline policy

Promote a baseline only after recording a complete successful run, its raw dataset SHA, full-input scope, timeframe, direction, enablement and bridge-output flags, source/reference hashes, exact output artifact SHA, and current rule version. Keep the original artifact immutable. The accepted reference and current source must agree for the asserted rule. Both references §§0.2, 19, 29G–29H; trading_pipeline.py lines 1732 and 2942.
