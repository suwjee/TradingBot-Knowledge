---
id: "source.integration_boundary"
type: "source"
status: "active"
authority: "executable"
title: "Current chart and bridge input boundary"
version: "current"
related_entities: ["core.pipeline", "source.trading_pipeline"]
source_reference: ["06_SOURCE/Code/apps/chart/vite.config.js", "06_SOURCE/Code/apps/chart/server/indicator-range-input.js", "06_SOURCE/Code/apps/chart/server/raw-resource-store.js"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Current chart and bridge input boundary

The direct bridge calculates from the entire supplied physical file or supplied stream and computes presentation bounds separately. It cannot reconstruct chronology that was never supplied. The chart server chooses full-path input for full-chart calculations, but selected-range calculations filter inclusive chart-candle buckets in Node memory and stream that selected JSON through a Windows named pipe. No second RAW file is written by this transport.

Therefore direct full-file engine behavior and a selected-range HTTP request have different supplied input scopes. A selected stream begins with empty calculation history at its own start and contains no chronology beyond its own end. Record this boundary when analyzing a chart result; do not claim a partial chart request includes a complete original RAW file merely because the Reference describes the direct bridge.

The local exact vite.config.js, indicator-range-input.js and raw-resource-store.js snapshots establish this integration boundary. Browser rendering remains presentation, while Python owns calculation decisions. This note introduces no change to either implementation.
