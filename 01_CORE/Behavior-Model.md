---
id: "core.behavior_model"
type: "core"
status: "active"
authority: "executable"
title: "Current behavior taxonomy"
version: "current"
related_entities: ["algorithm.e", "algorithm.order", "algorithm.s", "algorithm.stopall", "core.priority"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
last_modified_at: "2026-10-28T18:07:57+03:30"
---
# Current behavior taxonomy

## Accepted behavior families

A,S,numbered E,numbered StopAll define current lifecycle hierarchy. A is smallest. S family Red/Blue with native formation_type simple,advanced,type3,type4. Numbered E family Red/Blue follows reconciled stopped-parent lifecycle. StopAll is hard numbered-cycle behavior with three named gates.

## Supporting calculations

Reaction,Reset,Scale/Reset Blue,physical Order_A/Order_B and OrderAudit support those behaviors. Reaction mode A/B differs from Order_A/Order_B creation names. Rendered Blue line price is not behavior source stop level. Physical Order is an accepted opposite physical identity with cause/stop, not a behavior-family hierarchy. The accepted stopped-A Order_A route admits complete independently confirmed geometry with reactionNumber=0; Order_B retains canonical opposite-Reaction membership.

## Families and subtypes

S/E Red/Blue labels are invariant behavior roles,not chart GREEN/RED tags. Native Type-3/Type-4 create order-free Blue with null Order fields. Shared accepted-Order reconciliation may recolor while keeping native subtype/source. StopAll.number is cycle occurrence; gate_type is the subtype contract.

## State dimensions

Calculation candidate,accepted object,active owner,strictly stopped,consumed/historical and public visibility are distinct states. Final same-source occupancy/lineage never changes canonical physical Order identity or fabricates creating parentage.
