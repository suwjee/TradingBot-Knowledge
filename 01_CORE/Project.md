---
id: "core.project"
type: "core"
status: "canonical"
authority: "normative"
title: "TradingBot project"
source_refs: ["engine/bridge/trading_pipeline.py#L1698", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L129"]
related_entities: ["system.manifest"]
source_reference: ["engine/bridge/trading_pipeline.py#L1698", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L129"]
---

# TradingBot project

TradingBot is a local chart and calculation workstation. The browser and Vite middleware supply RAW candles and display results. The Python engine under engine/bridge and engine/pipeline owns trading calculations. The bridge dynamically loads flat-import detector modules, constructs chronology, computes both directional Reaction streams when dependent stages run, reconciles A/S/E/StopAll, and serializes JSON.

The current engine source is nine production Python modules. Browser range filtering may change what input reaches the bridge; distinguish the full input received by the engine from the original RAW resource. See Pipeline and 06_SOURCE/Source-Map.
