---
id: "source.reference_registry"
type: "source"
status: "active"
authority: "executable"
title: "Current local directional Reference registry"
version: "current"
related_entities: ["source.reference_consistency", "source.source_manifest", "version.current"]
source_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Current directional Reference registry

| Direction | Exact local Reference | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| Bearish | 06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md | bfb201d3d6b4d4d52fcd28ef6b8d77918757d5ed14fe8df033d9abfd4d499baf | 743552 |
| Bullish | 06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md | 131a0edb6945a59f4161c12aa00ba2c4cf5f787840a3786dbc66b5b3e69b27f7 | 743524 |

The registry stores exact complete current accepted directional References and their declared version/direction. Existing active source/algorithm links address these current files. Older standalone copies are removed from current capture; the task baseline remains preserved outside the Vault in scratch evidence.

Standalone-captured embedded owners are compared byte-for-byte. Explicit embedded-only exclusions are checked against dedicated hash/byte pins and reported with coverage=embedded-only-excluded. These checks prove evidence integrity, not semantic coverage or market correctness. source.reference_consistency preserves the remaining current narrative ambiguity and the status of previously stale discrepancy claims.

An external checkout is optional additional cross-verification. A valid external file cannot replace a mismatched local Reference. Historical scope/results inside unchanged Reference bytes remain historical.
