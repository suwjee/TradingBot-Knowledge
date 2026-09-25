---
id: "algorithm.e"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "E construction and recursive chains"
implemented_by: ["source.e_zone_detector"]
produces: ["behavior.e", "behavior.e.red", "behavior.e.blue"]
depends_on: ["algorithm.s", "algorithm.order"]
source_refs: []
relates_to: ["algorithm.reconciliation"]
related_entities: ["test.source_validation", "test.identity_invariants"]
source_reference: []
---

# E construction and recursive chains

## Calculation logic


Eligible representatives race on exact Order stop chronology; earliest strict stop wins with deterministic confirmation/First tie handling. E decisionEventTime=max(parentStopEventTime,winningOrderStopEventTime). E source/price is the trend directional extreme over complete main candles containing parent stop through winning Order stop, both endpoints inclusive. Do not trim boundary main OHLC at exact event seconds.

A provisional chain continues while each child has a valid zone/strict stop, source does not repeat, and no hard boundary interrupts. Suppressed lower-priority S may continue a stopped larger E under lifecycle rules; an earlier native continuation may replace only later descendants of that owner. Invalid-S cross-family same-source roots are narrowly suppressed, while same-family evidence remains. Reconciliation and numbering live in algorithm.reconciliation.

## Contract interface

- **Purpose:** Continue E families from stopped accepted S/E owners and physical Orders.
- **Inputs:** Stopped parent, accepted physical Order causes, exact decision events and lifecycle state.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Reconciled E candidates with family, number, parent, source and decision provenance.
- **Source ownership:** source.e_zone_detector.
- **Validation relationship:** test.identity_invariants; test.source_validation checks the line anchors and owner.
