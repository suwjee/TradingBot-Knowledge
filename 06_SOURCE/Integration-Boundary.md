---
id: "source.integration_boundary"
type: "source"
status: "pending"
authority: "non-canonical"
title: "Chart-to-bridge input scope"
relates_to: ["core.pipeline", "market.raw"]
source_refs: ["06_SOURCE/Code/apps/chart/vite.config.js#L581", "06_SOURCE/Code/apps/chart/vite.config.js#L611", "06_SOURCE/Code/apps/chart/server/indicator-range-input.js#L32", "06_SOURCE/Code/apps/chart/server/indicator-range-input.js#L113"]
external_source_paths: ["06_SOURCE/Code/apps/chart/vite.config.js", "06_SOURCE/Code/apps/chart/server/indicator-range-input.js"]
external_source_hashes: {"06_SOURCE/Code/apps/chart/vite.config.js": "9baf5c9745a96058e27b485b885dfc5a868e4256016d9ec38e14a442f7a5f58c", "06_SOURCE/Code/apps/chart/server/indicator-range-input.js": "bf9b2c5eac9457435f9aaed9615ca062dfabcb7541ca70fbf114c9dd2f1a419f"}
related_entities: ["test.source_validation"]
source_reference: []
---

# Chart-to-bridge input scope

## Specification / implementation difference

**Previously cited reference claim:** The former V5.4.11 HPZR6 directional references described calculation over the complete physical RAW file, with from/to selecting presentation output (sections 2 and 3A). Those references are absent from this scoped Vault, so this claim cannot currently be verified by a Vault-only reader or treated as an accepted normative contract.

**Retained chart implementation:** The Vite endpoint chooses inputScope=selected-range for a partial chart-candle interval. prepareIndicatorRangeInput filters RAW rows by inclusive chart bucket from..to. runIndicatorRangeCalculation streams that selected JSON through a Windows named pipe to the Python bridge. The bridge's calculation behavior was observed in the project audit, but its module is absent from this Vault and must be rechecked before an end-to-end claim.

**Inferred consequence from the retained chart path:** A partial chart request omits original RAW chronology outside the selected interval, so physical indexes and open state may differ from a complete-source run. The complete-source chart path passes the original RAW file. No paired runtime output comparison was performed in this audit; the bridge's from/to semantics remain pending within this Vault.

**Status:** Open integration question. The retained chart source shows that a selected-range request can pre-filter the RAW input. The bridge module and comprehensive references are absent from this Vault, so the full-physical-RAW contract and end-to-end effect remain pending review. Future retrieval must inspect the request's inputScope before applying full-file invariants to a chart result.

The chart evidence paths in `external_source_paths` now point to captured Vault files. A Vault-only reader can verify their bytes against `external_source_hashes` and inspect the cited lines. This proves the captured implementation path, not a later production state.
