---
id: "core.behavior_model"
type: "core"
status: "canonical"
authority: "normative"
title: "Behavior model"
source_refs: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L78", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L581"]
related_entities: ["algorithm.a", "algorithm.s", "algorithm.e", "algorithm.stopall", "test.behavior_invariants"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L78", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L581"]
---

# Behavior model

A is the smallest behavior, formed from Blue pair or special double-stop route. S begins after A strict stop and may be Red (Order stop) or Blue (candidate cross). E recursively follows a stopped S or E with an accepted physical Order; family/number are reconciled after discovery. StopAll is the hard boundary created by one of three exact gate strings. These are public semantic roles; detector routes are documented under 04_ALGORITHMS.
