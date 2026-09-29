---
id: "source.reference_registry"
type: "source"
status: "active"
authority: "executable"
title: "Current local directional Reference registry"
version: "current"
related_entities: ["source.reference_consistency", "source.source_manifest", "version.current"]
source_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Current local directional Reference registry

Both canonical 5.4.19-EX1 References are exact local current copies. Each reconstructs every current Python file, including package files; the current embedded inventory is derived from the Source manifest. No historical market examples or compensating clarification is active.

| Direction | Local reference | SHA-256 | Bytes |
|---|---|---|---:|
| Bearish | 06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md | 109753d7d056b6b9ee173cc7f47472b53a77174d26e89f38b00b81061f310e18 | 569305 |
| Bullish | 06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md | d3a0b89c59f1304ddefe6f6931cedf7ea2e17a15893c63d652c89489f3e6387f | 569275 |

Version, filename, direction, SHA-256, bytes, current status, local availability and exact reconstruction status are pinned in registry.json. Local reference retrieval is primary; an external checkout is optional verified evidence. Semantic/mirror validation and byte reconstruction are separate gates.


## Byte reconstruction and narrative review

Each directional Reference reconstructs all 13 current Python files byte-for-byte. Narrative semantic review found four documented scope discrepancies, recorded in source.reference_consistency and exposed by retrieval warnings. Registry authority_scope covers preserved Reference evidence, not a blanket narrative agreement claim. Production and local raw Reference copies remain unchanged.
