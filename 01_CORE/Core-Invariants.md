---
id: "core.invariants"
type: "core"
status: "active"
authority: "executable"
title: "Current calculation invariants"
version: "current"
related_entities: ["core.determinism", "core.identity", "core.ownership", "core.pipeline", "mirror.invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Current calculation invariants

## Prices and market candles

JSON floating price lexemes enter directly as Decimal via parse_float=Decimal; as_decimal preserves Decimal or applies Decimal(str(value)). Doji is GREEN in both directions. Strict behavior cross is Low<level Bullish/High>level Bearish. Reaction confirmation and opposite Order stops use their respective opposite price side. Equality may preserve ownership or satisfy explicit inclusive time gates,never a strict price crossing.

## Chronology and identity

Configured calculation candles own eligibility gates unless the active rule explicitly requires exact intrabar ordering; then finest supplied lower rows decide the race. Lower windows are [start,end) unless owner explicitly includes exact confirmation row or complete boundary main candles. Physical Reaction/Order identity is FirstIndex/BreakIndex; parent labels/causes are provenance. Time,indexes,canonical numbering,family names and public schemas are invariant across direction.

## Ownership and determinism

Calculation evidence,acceptance,active ownership and visibility are distinct. Valid historical Order_A identity/cause survives consumer changes; invalid S never gains accepted parent-stop creation. StopAll is a hard prefix boundary. Strict-better source replacement normally keeps earliest equal extreme; specific S candidate owners choose last equality. Order_B requires canonical membership. Accepted stopped-A Order_A additionally admits independently complete confirmed physical geometry with reactionNumber=0 under its current explicit exception.

## Projection and evidence

Complete supplied input calculates before presentation clipping. Serializer projects finalized state and cannot infer replacement strict event/missing Order. Inclusive Blue confirmation-row and shared S source-main-time boundaries follow current synchronized Source/Reference contract. Timings remain separate measured values. Source regression,mirror parity and independent target real-data correctness are distinct claims; Source knowledge supplies no stored market evidence.
