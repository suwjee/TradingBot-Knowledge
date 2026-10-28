---
id: "source.integration_boundary"
type: "source"
status: "active"
authority: "executable"
title: "Current chart and bridge input boundary"
version: "current"
related_entities: ["core.pipeline", "source.trading_pipeline", "source.local_server", "source.raw_resources", "source.chart_workspace"]
source_reference: ["06_SOURCE/Code/apps/chart/vite.config.js", "06_SOURCE/Code/apps/chart/server/indicator-range-input.js", "06_SOURCE/Code/apps/chart/server/raw-resource-store.js"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
last_modified_at: "2026-10-27T20:16:20+03:30"
---

# Current chart and bridge input boundary

The direct bridge calculates from the entire supplied physical file or supplied stream and computes presentation bounds separately. It cannot reconstruct chronology that was never supplied. The chart server chooses full-path input for full-chart calculations, but selected-range calculations filter inclusive chart-candle buckets in Node memory and stream that selected JSON through a Windows named pipe. No second RAW file is written by this transport.

Therefore direct full-file engine behavior and a selected-range HTTP request have different supplied input scopes. A selected stream begins with empty calculation history at its own start and contains no chronology beyond its own end. Record this boundary when analyzing a chart result; do not claim a partial chart request includes a complete original RAW file merely because the Reference describes the direct bridge.

The local exact vite.config.js, indicator-range-input.js and raw-resource-store.js snapshots establish this integration boundary. Browser rendering remains presentation, while Python owns calculation decisions. This note introduces no change to either implementation.

The selected range is validated against available inclusive chart-candle buckets. The end passed to Python is the last physical RAW row in the selected final bucket, which preserves the full selected candle when analysis timeframe is finer than chart timeframe. The complete-source path retains the original RAW input; a partial request uses binary-search bucket boundaries and a uniquely named Windows pipe. The pipe and its sockets are released after consumption or transport failure. Input preparation assumes the RAW store has already established strict chronology.

The supplied-input scope is part of the server cache identity and is exposed in the response. Separate request ownership, RAW-content guards and cache/progress coordination are documented in source.local_server; they do not restore omitted market history or redefine Engine state.
