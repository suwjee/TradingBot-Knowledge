---
id: "algorithm.reconciliation"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "E and lifecycle reconciliation"
implemented_by: ["source.e_zone_detector", "source.lifecycle_engine", "source.trading_pipeline"]
produces: ["behavior.e", "behavior.e.red", "behavior.e.blue", "core.e_numbering"]
depends_on: ["algorithm.e", "algorithm.lifecycle"]
source_refs: ["engine/pipeline/e_zone_detector.py#L2267", "engine/pipeline/e_zone_detector.py#L2463", "engine/pipeline/e_zone_detector.py#L2311"]
---

# E and lifecycle reconciliation

Discovery creates provisional Red/Blue E chains; accepted ownership is resolved chronologically with active parent state. At one physical source, rank candidates by (-behaviorPriority,decisionEventTime,parentStopEventTime), so family priority precedes chronology. An active accepted parent determines inherited family; otherwise candidate family applies. Partition active E owners strictly stopped by winner. Red parent or stopped Red owner yields Red with max stopped Red number +1, else Blue parent or stopped Blue yields Blue with max stopped Blue number +1, otherwise candidate family number 1.

An S can reopen after a prior E only when rebuilt after that E or a still-unconsumed Red S legitimately outranks Blue E; it cannot steal active Red E. Suppress a direct S candidate that would replace an active owner when that owner already has an E child at/no earlier than the candidate decision under the source rule. One sourceIndex/sourceTime accepts one E: Red > Blue; within family higher number > lower; exact tie keeps first accepted provenance. Final order is (sourceTime,sourceIndex,decisionEventTime).

After dominant reconciliation, restore eligible independent accepted-S E1 roots without rewriting StopAll history. A provisional invalid-S E1 chain is blocked only when its invalid S shares exact source with an accepted E-parent continuation of a different family. Historical rescues are presentation-only.
