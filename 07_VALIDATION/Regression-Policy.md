---
id: "test.regression_policy"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Regression comparison policy"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.validation_contract", "test.zero_difference", "test.regression_model", "test.baseline_policy", "algorithm.serialization", "core.chronology", "source.trading_pipeline"]
source_reference: []
---

# Regression comparison policy

A regression compares a trusted, versioned previous result to a new result on the **same complete physical RAW bytes**, analysis timeframe, direction, enablement flags and bridge-output mode. Save dataset/source/reference hashes and command settings beside the baseline. The comparison covers the ordered behavior sequence, physical and exact event timestamps, lifecycle state and transitions, Order identity/causes, stage collections, visibility and stable serialization. Both references §§16–19; trading_pipeline.py lines 239–493 and 2776–2995.

For a pure refactor, old stable output equals new stable output. The response contains measured timings; preserve their field structure but do not compare elapsed numeric values as deterministic algorithm output. For an approved algorithm change, record the approval, exact rule/version boundary, expected changed fields and causally affected downstream outputs; compare all unaffected fields and both directions. Do not hide an E/StopAll change behind unchanged Reaction counts.


Compare missing/extra objects, ordering, nulls, source/decision time, physical indexes, parent/cause identity, family and E number. A failed or incomplete run cannot replace the trusted baseline. See Regression/Baseline-Policy.md and Regression/Change-Impact.md.
