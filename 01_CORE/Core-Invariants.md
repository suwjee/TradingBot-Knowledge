---
id: "core.invariants"
type: "core"
status: "canonical"
authority: "normative"
title: "Core invariants"
source_refs: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L82", "engine/pipeline/lifecycle_engine.py#L23"]
---

# Core invariants

All price decisions use Decimal(str(value)) unless already Decimal. GREEN iff close >= open, so every Doji is GREEN. Strict crossing excludes equality. Lower-timeframe first-event chronology decides same-main-candle ordering; main candle extrema still own explicitly closed source ranges.

Both direction Reaction streams feed opposite-Order geometry. Internal Reaction is often calculation-visible although public output may hide it. The full received engine input determines calculation state; from/to are bridge presentation bounds. Stage ownership is A -> S -> E -> StopAll. Priority is StopAll > E Red > S Red > E Blue > S Blue > A. A StopAll is a hard lifecycle boundary. Creation cause and use provenance for Orders remain distinct.
