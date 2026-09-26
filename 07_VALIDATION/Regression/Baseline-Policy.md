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

Promote a baseline only after recording a complete successful run, its raw dataset SHA, full-input scope, timeframe, direction, enablement and bridge-output flags, source/reference hashes, exact output artifact SHA, and current rule version. Keep the original artifact immutable. The project owner must explicitly accept the asserted rule; source/reference agreement alone does not approve it. Current Order_B/Order_C implementation and all outputs dependent on those routes are known-invalid diagnostic evidence and cannot become an approved regression baseline. Both references §§0.2, 19, 29G–29H; trading_pipeline.py lines 1732 and 2942.
