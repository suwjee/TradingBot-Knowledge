---
id: "core.precision"
type: "core"
status: "active"
authority: "executable"
title: "Current Decimal semantics"
version: "current"
related_entities: ["core.invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Current Decimal semantics

as_decimal preserves an existing Decimal and normalizes other values with Decimal(str(value)). Price-sensitive comparisons, extrema, stops and derived levels retain Decimal semantics. Serialization converts finalized values into the public format; a float used for time measurement or presentation is not a price-decision authority.

The bridge parses JSON floating lexemes directly with json.loads(..., parse_float=Decimal). Conversion through binary float before as_decimal would lose original price precision and is not the current input contract.
