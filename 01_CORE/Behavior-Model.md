---
id: "core.behavior_model"
type: "core"
status: "pending"
authority: "non-canonical"
title: "Behavior model"
source_refs: []
related_entities: ["algorithm.a", "algorithm.s", "algorithm.e", "algorithm.stopall", "test.behavior_invariants"]
source_reference: []
---

# Behavior model

A is the smallest behavior, formed from Blue pair or special double-stop route. S begins after A strict stop and may be Red (Order stop) or Blue (candidate cross). E recursively follows a stopped S or E with an accepted physical Order; family/number are reconciled after discovery. StopAll is the hard boundary created by one of three exact gate strings. These are public semantic roles; detector routes are documented under 04_ALGORITHMS.

A **Behavior** is the public semantic object and lifecycle role emitted by the pipeline. An **Algorithm** is the rule that calculates candidates, ownership, stops and output fields. One Behavior can have several calculation routes: for example, S Blue Type-1..4 share S's behavior family but use distinct routes. Reaction, Reset, Blue, and Order support calculation or evidence and do not become additional Behaviors. Exact source may serialize audit material, but it has no Behavior, Algorithm, fixture-authority, or retrieval-concept role in this Vault. `test.behavior_invariants` validates this taxonomy against the serialized collections.
