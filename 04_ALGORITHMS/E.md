---
id: "algorithm.e"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "E construction and recursive chains"
implemented_by: ["source.e_zone_detector"]
produces: ["behavior.e", "behavior.e.red", "behavior.e.blue"]
depends_on: ["algorithm.s", "algorithm.order"]
source_refs: ["engine/pipeline/e_zone_detector.py#L1901", "engine/pipeline/e_zone_detector.py#L2040", "engine/pipeline/e_zone_detector.py#L2371"]
relates_to: ["algorithm.reconciliation"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/e_zone_detector.py#L1901", "engine/pipeline/e_zone_detector.py#L2040", "engine/pipeline/e_zone_detector.py#L2371"]
---

# E construction and recursive chains

A stopped accepted S can open E1; a stopped accepted E can open E(n+1). Parent stop is the first strict trend-side crossing from its eligible source/decision chronology. Physical Order representatives include fresh parent-stop Order_A, already-live carried Order, parent-neutral accepted-live Order, Reset-leg Order_B, and Blue-leg Order_C. Accepted-live scans accepted stopped-A and E physical ledgers, deduplicates (FirstIndex,BreakIndex), and requires confirmation > parent stop, strict Order stop > both confirmation and parent stop, and no hard reset in (parentStopEvent,orderStopEvent]. It supplies use provenance only.

Eligible representatives race on exact Order stop chronology; earliest strict stop wins with deterministic confirmation/First tie handling. E decisionEventTime=max(parentStopEventTime,winningOrderStopEventTime). E source/price is the trend directional extreme over complete main candles containing parent stop through winning Order stop, both endpoints inclusive. Do not trim boundary main OHLC at exact event seconds.

A provisional chain continues while each child has a valid zone/strict stop, source does not repeat, and no hard boundary interrupts. Suppressed lower-priority S may continue a stopped larger E under lifecycle rules; an earlier native continuation may replace only later descendants of that owner. Invalid-S cross-family same-source roots are narrowly suppressed, while same-family evidence remains. Reconciliation and numbering live in algorithm.reconciliation.
