---
id: "test.output_validation"
type: "test"
status: "canonical"
authority: "normative"
title: "Public output validation"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.validation_contract","test.regression_policy","algorithm.serialization","algorithm.visibility","algorithm.order","source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1044","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1044","engine/bridge/trading_pipeline.py#L239","engine/bridge/trading_pipeline.py#L2776","engine/bridge/trading_pipeline.py#L2942"]
---

# Public output validation

Compare the response envelope, direction payload and ordered stage arrays after final lifecycle visibility. Inspect Reaction/Reset/Blue and A/S/E/StopAll separately. Preserve exact first/break/source/decision/stop times, physical indexes, parent and Order causes, E family/number, StopAll gate/number, version fields, nullable fields, and Decimal prices as strings. Both references §16; trading_pipeline.py lines 239–493, 2549 and 2776–2995.

For a selected display range, distinguish calculation scope from serialization clipping. The engine bridge builds complete physical-input state and then selects visible objects. A caller that prefilters RAW supplies a different physical input; do not treat those two requests as equivalent without checking the integration boundary. trading_pipeline.py lines 1732, 2300 and 2776.

Current OrderAudit fields can be compared as executable output and used to detect identity/provenance drift; existing Vault authority keeps its trading-rule status pending-fix. Do not promote an observed OrderAudit discrepancy into an accepted S/E/StopAll rule. A fixture must state the stable output it checks; a count alone is insufficient when object identities or chronology may have changed.

Timing values are telemetry. Verify the timing keys/shape, and compare semantic payload fields exactly for zero-difference claims. See Regression-Policy.md.

