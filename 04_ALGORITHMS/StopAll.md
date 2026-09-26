---
id: "algorithm.stopall"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "StopAll gate state machine"
affected_by_known_invalid_order_route: true
implemented_by: ["source.lifecycle_engine"]
produces: ["behavior.stopall", "behavior.stopall.type1", "behavior.stopall.type2", "behavior.stopall.type3"]
depends_on: ["algorithm.lifecycle", "algorithm.e", "algorithm.s"]
source_refs: []
related_entities: ["test.source_validation", "test.lifecycle_invariants"]
source_reference: []
---

# StopAll gate state machine

## Calculation logic

Maintain dominant S key/count and E key/count under invariant priority S Blue=1, E Blue=2, S Red=3, E Red=4. Separately count pending accepted Blue by exact key: all S Blue together, each numbered E Blue separately. Before every E decision ingest earlier S by source time.

Gate Type-2 (stopall-stop) first: if active StopAll first strict-stopped no later than E decision, current E donates a new StopAll numbered highest stopped active +1. Otherwise Type-1 (sequence-group-stop): a dominant same-key E group with count >=2, or with no E key a same-color S group count >=2, must have a latest matching prior owner strictly stopped by E decision; current E donates StopAll1. An E not promoted updates owner state by priority, with Red E clearing pending Blue reversal evidence and Blue E incrementing its exact pending key.

Before ordinary S Red replacement, Type-3 (opposite-s-group-stop) checks native Mode-B forming Order and any pending exact Blue group count >=2; if qualified, promote that S Red to StopAll1, choosing newest qualified group's last accepted occurrence for metadata. Any accepted Red S or E resolves pending Blue evidence even without promotion. Every hard StopAll clears owner and pending counters. Finally compute each StopAll's own first strict directional stop. Bullish uses Low < price, Bearish High > price; gates, keys, family labels, and priority do not mirror.

## Contract interface

- **Purpose:** Detect hard sequence boundaries from accepted S/E gates.
- **Inputs:** Reconciled E/S, exact source/stop events, dominant keys and pending Blue repeats.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** StopAll gate object and sequence-reset ownership effect.
- **Source ownership:** source.lifecycle_engine.
- **Validation relationship:** test.lifecycle_invariants; test.source_validation checks the line anchors and owner.
