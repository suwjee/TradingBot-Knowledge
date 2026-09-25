---
id: "test.unit_test_policy"
type: "test"
status: "canonical"
authority: "normative"
title: "Engine unit test policy"
related_entities: ["test.test_model", "test.fixture_model", "test.invariant_validation", "test.precision_invariants", "test.chronology_invariants", "test.integration_test_policy", "source.direction_policy"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py#L11", "06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
---

# Engine unit test policy

**Definition and purpose.** A unit check isolates one source-owned rule with controlled inputs and a stated expected value. This policy does not claim a repository-local Python unit suite currently exists.

**Related algorithm and source.** For numerical rules test `core_utils.py` Decimal conversion and `direction_policy.py` strict operators; for reflected Reaction test the source-owned transformation in `reaction_engine.py`. Include equality, just-below and just-above cases, exact event order, null/unknown provenance and both directions where the rule has directional form. An isolated detector check must not substitute for downstream S/E/StopAll ownership validation.

**Execution boundary.** Use the actual supported loader or an explicit test harness: flat package imports are not a supported production smoke path in the current migration state. Pin the exact source commit/hash and reference clause. Avoid fixture-specific production branches or manually edited expected payloads.

**Validation relation.** Run a relevant integration check after an isolated rule changes, then protected regression. Record PASS/FAIL/INCOMPLETE through `test.test_model`; do not promote a Pending fixture because one narrow unit check passes.
