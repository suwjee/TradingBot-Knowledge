---
id: "test.fixture_model"
type: "test"
status: "canonical"
authority: "normative"
title: "Fixture entity model"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.validation_contract", "test.fixture_registry", "core.behavior_model", "algorithm.order", "source.core_utils", "mirror.invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py#L19"]
---

# Fixture entity model

A Fixture is one source-located scenario with one primary validation target. Its stable Vault id has type case. The frontmatter field fixture_kind is Confirmed, Regression, EdgeCase or Bug; type remains case because type is the Vault entity kind. S Red, S Blue Type-1..4, and numbered E instances stay details of the same Behavior entity. Reaction, Reset, Blue and Order are calculation structures: when a case tests only one of them, behavior is unknown rather than a fabricated Behavior link. Physical Order identity is implemented in the retained `core_utils.py` source.

Every case records id, type, status, authority, fixture_kind, fixture_status, fixture_authority, direction, timeframe, dataset and SHA-256, timestamp, behavior and behavior_detail, algorithm, source_module, source_function, reaction_identity, order_identity, first_index, break_index, lifecycle_state, previous_behavior, next_behavior, stopall_boundary, expected_output, validation_target, validation_rule, related_entities, source_reference, and the supplied fixture document path/line/hash. Unknown means unavailable evidence; it is not zero, false, an empty identity, or an inferred event. Physical Order identity is the pair (FirstIndex, BreakIndex). The two scalar index fields repeat this pair only when the physical Order is proved; otherwise both are `unknown`. They are never derived from a similarly named Reaction or a filename.

Fixture status is Active, Pending or Historical. Active requires a bounded assertion supported by retained local source and fixture evidence; it does not establish a complete calculated output. Pending retains supplied claims awaiting exact date, output or ownership proof; Historical preserves a superseded expectation and never acts as the current baseline. Fixture authority Canonical means accepted *fixture evidence*, not a normative trading rule. The Vault's separate authority field remains empirical for Active, non-canonical for Pending, historical for Historical. The Vault status maps to active, draft, archived respectively.

Each case relates to one validation rule and, when known, its Behavior, Algorithm and Source module. The case body cites the Vault-local curated fixture section and retained source anchors where available; the supplied document alone does not prove an engine result. A case can be classified while Pending. No current baseline is manufactured from a historical Bug.

Fixture-Registry.md is the inventory and deduplication map. Additional expected payload fields, complete source/candidate output hashes, and run results may be added later without changing the case identity.
