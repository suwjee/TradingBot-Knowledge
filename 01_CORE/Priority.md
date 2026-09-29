---
id: "core.priority"
type: "core"
status: "active"
authority: "executable"
title: "Shared lifecycle priority and chronology"
version: "current"
related_entities: ["algorithm.lifecycle", "algorithm.reconciliation", "algorithm.stopall"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49"]
---

# Shared lifecycle priority and chronology

Shared exact hierarchy is StopAll>E Red>S Red>E Blue>S Blue>A,represented 5,4,3,2,1,0. sequence_priority covers S/E. Family names and hierarchy are direction-invariant.

Priority does not make every old high-level object permanent owner. Closed A transitions use latest stopped main candle,then same-boundary priority/number/source. S ownership uses exact stopped-owner and source-event chronology.

Same-source E Red outranks Blue regardless of number; same-family larger number wins; exact remaining tie preserves prior provenance. Active Red E cannot be stolen by S; accepted Red S may supersede Blue E under lifecycle gates.

Dominant occurrence counters and independent accepted Blue-repeat counters differ. Lower-priority accepted events can remain output without replacing dominant. Same-family larger E advances dominant E group; different Blue E numbers cannot combine in reversal key.
