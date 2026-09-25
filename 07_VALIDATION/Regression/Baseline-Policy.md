---
id: "test.baseline_policy"
type: "test"
status: "canonical"
authority: "normative"
title: "Trusted baseline policy"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.regression_policy","test.zero_difference","test.fixture_registry","test.regression_model","algorithm.serialization","source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1099","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1099","engine/bridge/trading_pipeline.py#L1732","engine/bridge/trading_pipeline.py#L2942"]
---

# Trusted baseline policy

Promote a baseline only after recording a complete successful run, its raw dataset SHA, full-input scope, timeframe, direction, enablement and bridge-output flags, source/reference hashes, exact output artifact SHA, and current rule version. Keep the original artifact immutable. The accepted reference and current source must agree for the asserted rule. Both references §§0.2, 19, 29G–29H; trading_pipeline.py lines 1732 and 2942.

A fixture document's Active label is a claim to check; it does not by itself supply a full serialized baseline. The supplied 2026-09-25 anchors include exact selected outputs, but most lack a saved full payload hash. They can validate their explicit assertions while whole-payload zero-difference remains unready. Pending items such as the date-unknown USOIL Order_A/Order_C chain and the conversation-only E5/E6 anchor are not canonical baselines.

Current V5.4.11 Order_C results supersede earlier 6.14.1 outcomes. V5.4.8 first-Order_A ownership supersedes V5.4.5 refresh output. Store both versions with explicit historical labels; never compare a new current run against a superseded expectation as if it were current. Timings are telemetry and do not supply a semantic baseline.

