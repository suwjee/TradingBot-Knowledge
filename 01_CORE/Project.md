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
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Current project architecture

TradingBot is a local Windows candlestick workstation. The native ES-module browser acquires and displays candles, drawings and indicator state. HTTP JSON and progress SSE connect the browser to Vite middleware. Vite supplies an explicit input scope and starts the Python bridge. The Engine owns Decimal calculation, Reaction/Reset, Blue, A, S, E, physical Orders, lifecycle, StopAll, visibility and final audit state. JSON serialization projects finalized state back to the UI.

Current chart package metadata is retained exactly in 06_SOURCE/Code/apps/chart/package.json. Module versions and Reference version are separate. A Git tag, package version or old audit snapshot cannot identify the exact dirty working-tree Engine bytes.

## Current integration navigation

source.local_server owns dispatch/cache/progress evidence; source.raw_resources owns RAW identity/transfer/update; source.faraz owns external acquisition/session; source.chart_workspace owns workspace/drawing/review behavior. workflow.project_release follows the maintained local release subsystem. These descriptions are executable architecture evidence, subordinate to the intended-semantic authority order. Current source_scope explicitly excludes added-feature knowledge; this note does not claim complete Engine feature coverage.
