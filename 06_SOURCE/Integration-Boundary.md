---
id: "source.integration_boundary"
type: "source"
status: "active"
authority: "executable"
title: "Chart-to-bridge input scope"
relates_to: ["core.pipeline", "market.raw"]
source_refs: ["apps/chart/vite.config.js#L581", "apps/chart/vite.config.js#L611", "apps/chart/server/indicator-range-input.js#L32", "apps/chart/server/indicator-range-input.js#L113", "engine/bridge/trading_pipeline.py#L1732"]
external_source_paths: ["apps/chart/vite.config.js", "apps/chart/server/indicator-range-input.js"]
external_source_hashes: {"apps/chart/vite.config.js": "9baf5c9745a96058e27b485b885dfc5a868e4256016d9ec38e14a442f7a5f58c", "apps/chart/server/indicator-range-input.js": "bf9b2c5eac9457435f9aaed9615ca062dfabcb7541ca70fbf114c9dd2f1a419f"}
related_entities: ["test.source_validation"]
source_reference: ["engine/bridge/trading_pipeline.py#L1732"]
---

# Chart-to-bridge input scope

## Specification / implementation difference

**Reference contract:** Both V5.4.11 HPZR6 directional algorithm references describe calculation over the complete physical RAW file, with from/to only selecting presentation output (section 2 and section 3A).

**Current chart integration:** The Vite endpoint chooses inputScope=selected-range for a partial chart-candle interval. prepareIndicatorRangeInput filters RAW rows by inclusive chart bucket from..to. runIndicatorRangeCalculation streams that selected JSON through a Windows named pipe to the Python bridge. The bridge then calculates over its entire received JSON input. It cannot access chronology that the chart server omitted.

**Inferred consequence from the code paths:** The engine's from/to remain presentation bounds relative to its received input. A partial chart request omits original RAW chronology outside the selected interval, so physical indexes and open state can differ from a complete-source run. The complete-source path passes the original RAW file. No paired runtime output comparison was performed in this audit.

**Status:** Open integration divergence. The normative contract requires complete physical RAW. The current bridge computes over its complete received input; the chart selected-range path can pre-filter that input. Prefiltering does not redefine the normative full-RAW contract. Future retrieval must inspect the request's inputScope before applying full-file invariants to a chart result.

The chart evidence paths in `external_source_paths` are production-repository-only dependencies, not mirrored Vault files. A Vault-only reader cannot independently verify this integration claim; it must read those production files and match the `external_source_hashes` values, or mark the claim unverified.
