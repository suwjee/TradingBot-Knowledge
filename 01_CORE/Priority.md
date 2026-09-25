---
id: "core.priority"
type: "core"
status: "canonical"
authority: "normative"
title: "Priority"
source_refs: ["engine/pipeline/lifecycle_engine.py#L23", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L877"]
---

# Priority

The direction-invariant sequence table is S Blue=1, E Blue=2, S Red=3, E Red=4. StopAll outranks these; A is below them. Priority resolves competing accepted owners at the relevant transition, but an old high-priority behavior does not own later chronology forever. For E candidates at one physical source, ownership priority precedes decision time and parent-stop time. Red E wins over Blue E at the same source, then higher number wins within one family.
