---
id: "test.test_policy"
type: "test"
status: "pending"
authority: "non-canonical"
title: "TradingBot test policy"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.validation_contract", "test.fixture_model", "test.regression_policy", "test.mirror_validation", "test.output_validation", "test.test_model", "test.unit_test_policy", "test.integration_test_policy", "test.regression_test_execution", "source.trading_pipeline"]
source_reference: []
---

# TradingBot test policy

Select a targeted check for the changed owner, then run the complete safe validation path for both directions and the affected RAW datasets. A result is PASS only after a fresh run with exit status, exact inputs, source/reference hashes, expected assertion and observed output recorded. Missing input, timeout or interruption is INCOMPLETE, never PASS. These are execution requirements, not a claim that Phase 5 ran the full pipeline.

Use exact lower-timeframe events for ties and strict crossings. Assert equality is not a crossing; Doji remains GREEN. Preserve Decimal semantics and full physical indexes. Run dependent A/S/E logic with both Reaction streams even when one output direction is requested. Both references §§3A, 5, 18; direction_policy.py lines 32–46; trading_pipeline.py lines 2300–2350.

For a new or edited fixture: validate RAW identity and analysis timeframe, reproduce the scenario under the complete input, inspect stage result and final visibility, match the exact current reference/source rule, and capture stable serialized output. Compare the opposite direction through Mirror-Validation.md without demanding that two naturally different market outputs be byte equal.

Never use an old historical expectation as a current pass criterion. A Pending fixture can direct investigation but cannot certify a release. No fixture-specific branch may be added to production code.
