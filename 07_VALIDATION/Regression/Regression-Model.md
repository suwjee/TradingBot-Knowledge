---
id: "test.regression_model"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Regression evidence model"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.regression_policy", "test.baseline_policy", "test.change_impact", "test.fixture_model", "algorithm.serialization", "source.trading_pipeline"]
source_reference: []
---

# Regression evidence model

A regression record binds a fixture id to dataset SHA, source/reference version and hashes, input flags, baseline output, candidate output, a stable-field comparison, and a result: PASS, FAIL or INCOMPLETE. Compare Bullish and Bearish independently. A result belongs to those exact bytes and settings; it cannot be promoted to untested datasets. Both references §§17–19; trading_pipeline.py lines 2776–2995.

Fixture classification is orthogonal to run outcome. Regression means an active expectation must survive an unapproved refactor; Historical preserves an older version's result without treating it as current. EdgeCase covers an exact boundary and can still join a regression corpus. A pending fixture directs investigation but is not a trusted baseline. See Fixture-Model.md.

Record changes at stage granularity (Reaction, Reset, Blue, A, S, E, StopAll, Order identity, final visibility, serialization). A count match is insufficient if timestamps, cause ownership or ordering differ. Time telemetry is measured separately from deterministic payload values.
