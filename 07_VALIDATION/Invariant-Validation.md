---
id: "test.invariant_validation"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Invariant validation"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.lifecycle_invariants", "test.behavior_invariants", "test.chronology_invariants", "test.precision_invariants", "test.identity_invariants", "core.invariants", "mirror.invariants", "test.unit_test_policy", "test.integration_test_policy"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py#L11"]
---

# Invariant validation

Validate the five invariant groups separately, then across the integrated pipeline: lifecycle priority/stage boundary; Behavior and E-number identity; exact lower chronology; Decimal and strict equality; physical Order/Reaction identity and immutable provenance. The complete integrated assertion is pending because lifecycle and bridge source and comprehensive references are absent. Retained `core_utils.py` supports only its local Decimal and identity rules.

The child notes under Invariants/ give assertions, source owners and fixture links. A later directional price change may alter which object exists, but it cannot alter these invariant contracts. Any source-reference disagreement remains unresolved rather than being converted into an assertion.
