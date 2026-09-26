---
id: "behavior.s.blue.type3"
type: "behavior"
status: "pending"
authority: "non-canonical"
title: "S Blue Type-3"
calculated_by: ["algorithm.s.type3"]
implemented_by: ["source.s_zone_detector"]
depends_on: ["behavior.s.blue", "algorithm.reset"]
source_refs: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L457", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L482", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1090", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1355"]
related_entities: ["test.behavior_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L457", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L482", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1090", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1355"]
---

# S Blue Type-3

Type-3 is the order-free Reset-leg member of the public S Blue family. It continues one stopped A only when the eligible decision occurs before a newly selected opposite Order confirms, or before the received calculation range ends when no such Order exists. Its public result is always `S Blue` with `formationType=type3`; it is not an Order-backed S route.

The emitted S retains its stopped-A parent and stop provenance, the selected source/decision provenance, and the qualifying opposite Reset provenance (`reset_reaction_number` and `reset_time`). It has no forming Order geometry or forming-Order identity. It remains one ordinary S Blue occurrence for lifecycle purposes, including the shared S Blue group used by the StopAll Type-3 gate.

The Bullish HPZR6 §9.2 describes the directional source as Low and the Bearish HPZR6 §9.2 as High; both require last-candle ownership on an equal extreme and a same-direction confirmation after the A stop no later than the strict crossing. The hash-pinned references agree that this is a Reset-provenance S Blue without Order geometry. `algorithm.s.type3` owns the exact owner, time-window, crossing, and Type-3/Type-4 precedence mechanics.
