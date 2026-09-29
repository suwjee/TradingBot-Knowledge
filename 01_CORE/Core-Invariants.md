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
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49"]
---

# Current calculation invariants

## Prices and market candles

Price decisions remain Decimal; external normalization is Decimal(str(value)). Doji is GREEN in both directions. Strict behavior cross is Low<level Bullish/High>level Bearish. Reaction confirmation and opposite Order stops use their respective opposite price side. Equality may preserve ownership or satisfy explicit inclusive time gates,never a strict price crossing.

## Chronology and identity

Finest supplied lower rows decide first events/same-main ordering. Lower windows are [start,end) unless owner explicitly includes exact confirmation row or complete boundary main candles. Physical Reaction/Order identity is FirstIndex/BreakIndex; parent labels/causes are provenance. Time,indexes,canonical numbering,family names and public schemas are invariant across direction.

## Ownership and determinism

Calculation evidence,acceptance,active ownership and visibility are distinct. Valid historical Order_A identity/cause survives consumer changes; invalid S never gains accepted parent-stop creation. StopAll is a hard prefix boundary. Strict-better source replacement normally keeps earliest equal extreme; specific S candidate owners choose last equality. Noncanonical geometry cannot become physical Order.

## Projection and evidence

Complete supplied input calculates before presentation clipping. Serializer projects finalized state and cannot infer replacement strict event/missing Order. Inclusive Blue confirmation-row and shared S source-main-time boundaries follow current synchronized Source/Reference contract. Timings remain separate measured values. Source regression,mirror parity and independent target real-data correctness are distinct claims; Source knowledge supplies no stored market evidence.
