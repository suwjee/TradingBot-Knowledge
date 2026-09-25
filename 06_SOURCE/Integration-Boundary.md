---
id: "source.integration_boundary"
type: "source"
status: "active"
authority: "executable"
title: "Chart-to-bridge input scope"
implements: ["algorithm.raw"]
relates_to: ["core.pipeline", "market.raw"]
source_refs: ["apps/chart/vite.config.js#L577", "apps/chart/vite.config.js#L593", "apps/chart/server/indicator-range-input.js#L10", "apps/chart/server/indicator-range-input.js#L93", "engine/bridge/trading_pipeline.py#L1732"]
---

# Chart-to-bridge input scope

## Specification / implementation difference

**Reference contract:** Both V5.4.11 HPZR6 directional algorithm references describe calculation over the complete physical RAW file, with from/to only selecting presentation output (section 2 and section 3A).

**Current chart integration:** The Vite endpoint chooses inputScope=selected-range for a partial chart-candle interval. prepareIndicatorRangeInput filters RAW rows by inclusive chart bucket from..to. runIndicatorRangeCalculation streams that selected JSON through a Windows named pipe to the Python bridge. The bridge then calculates over its entire received JSON input. It cannot access chronology that the chart server omitted.

**Observed difference:** The engine's from/to remain presentation bounds relative to its received input, but a partial chart request does not have the full original RAW calculation history. Physical indexes and open state can therefore differ from a complete-source run. The complete-source path passes the original RAW file.

**Status:** Open integration divergence. This Vault does not rewrite the normative engine reference or silently treat partial input as full-file equivalent. Future retrieval must inspect the request's inputScope before applying full-file invariants to a chart result. No production change was made in this task.
