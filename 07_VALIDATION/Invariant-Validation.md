---
id: "test.invariant_validation"
type: "test"
status: "canonical"
authority: "normative"
title: "Invariant validation"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.lifecycle_invariants","test.behavior_invariants","test.chronology_invariants","test.precision_invariants","test.identity_invariants","core.invariants","mirror.invariants"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L169","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L169","engine/pipeline/lifecycle_engine.py#L25","engine/pipeline/core_utils.py#L11"]
---

# Invariant validation

Validate the five invariant groups separately, then across the integrated pipeline: lifecycle priority/stage boundary; Behavior and E-number identity; exact lower chronology; Decimal and strict equality; physical Order/Reaction identity and immutable provenance. These do not swap under Bullish/Bearish direction. Both references §3A and §23.2; lifecycle_engine.py lines 25–35; core_utils.py lines 11–29.

The child notes under Invariants/ give assertions, source owners and fixture links. A later directional price change may alter which object exists, but it cannot alter these invariant contracts. Any source-reference disagreement remains unresolved rather than being converted into an assertion.

