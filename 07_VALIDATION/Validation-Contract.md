---
id: "test.validation_contract"
type: "test"
status: "canonical"
authority: "normative"
title: "TradingBot validation contract"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["core.pipeline","core.behavior_model","algorithm.serialization","mirror.contract","source.trading_pipeline","test.fixture_model"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L82","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L82","engine/bridge/trading_pipeline.py#L1732","engine/bridge/trading_pipeline.py#L2942"]
---

# TradingBot validation contract

Validation proves five separate claims: (1) calculation matches the accepted algorithm reference and exact source semantics; (2) public A/S/E/StopAll behavior, family, number and ownership are correct; (3) the cited source module and real function own each rule; (4) directional transformations preserve invariant rules; and (5) stable output remains equal to an approved baseline unless an algorithm change was approved. A unit test alone proves none of the other four claims.

The evidence chain is pinned RAW bytes → complete input/settings → both directional calculation contexts where required → stage objects → lifecycle/visibility → public serialization → expected fixture assertion. Record reference version, production source hash, dataset hash, exact event time, and outcome. The bridge owns this ordering at trading_pipeline.py lines 1732, 1903, 2300, 2549 and 2776; both V5.4.11 HPZR6 references §§15A and 19 describe the acceptance boundary.

A fixture is evidence, not a production rule. A confirmed output does not authorize a timestamp-, symbol-, price-, RAW-name- or expected-output-specific branch. Historical and pending assertions cannot replace current accepted rules. A disagreement between source and reference is unresolved until decided; see Mirror-Validation.md and the existing Mirror-Exceptions.md.

Read Fixture-Model.md for evidence authority, Test-Policy.md for execution, and Regression-Policy.md for change decisions. No run is claimed merely because this contract exists.

