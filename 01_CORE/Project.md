---
id: "core.project"
type: "core"
status: "active"
authority: "executable"
title: "Current project architecture"
version: "current"
related_entities: ["core.pipeline", "source.integration_boundary"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Current source and synchronized current references"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L49"]
---

# Current project architecture

TradingBot is a local Windows candlestick workstation. The native ES-module browser acquires and displays candles, drawings and indicator state. HTTP JSON and progress SSE connect the browser to Vite middleware. Vite supplies an explicit input scope and starts the Python bridge. The Engine owns Decimal calculation, Reaction/Reset, Blue, A, S, E, physical Orders, lifecycle, StopAll, visibility and final audit state. JSON serialization projects finalized state back to the UI.

Current chart package metadata is retained exactly in 06_SOURCE/Code/apps/chart/package.json. Module versions and Reference version are separate. A Git tag, package version or old audit snapshot cannot identify the exact dirty working-tree Engine bytes.
