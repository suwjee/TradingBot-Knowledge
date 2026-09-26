---
id: "system.readme"
type: "system"
status: "active"
authority: "normative"
title: "Standalone TradingBot Knowledge Vault"
related_entities: ["system.manifest", "system.authority", "system.retrieval"]
source_reference: []
---

# TradingBot Knowledge Vault

This repository is a standalone, scoped knowledge snapshot. `Order_A` is accepted. Current `Order_B` and `Order_C` implementations are retained as known-invalid diagnostic knowledge, with explicit quarantine metadata. The Vault retains byte-exact copies of all nine main Engine modules plus three package initializers, chart input-boundary evidence, seven registered RAW datasets, three verified RAW windows, 22 curated fixture cases, schemas and relationship indexes. The full HPZR6 references are registered by hash as optional external evidence. Reading this Vault requires no separate TradingBot checkout.

The registered RAW hashes and windows verify. Three superseded small RAW files and sidecars were removed after their physical SHA-256 values matched exact registered windows within retained parent RAW files. The plugin now reports `verified_pins_ok: true`, `inventory_complete: true`, and overall `ok: true` for this local snapshot. The separate 309,906-row file remains because the larger overlapping file has one extra candle in that range.

## Quick check

From the Vault root, with Python 3.10 or newer and `jsonschema>=4.18,<5` installed:

```text
python -B _SCHEMA/build_indexes.py --check
```

AI hosts can read the Markdown and `_INDEX` files directly. A separate portable plugin can also read this Vault through a configured Vault root. The plugin executable and its dependencies are not stored here.

Start rule analysis with [Authority Model](00_SYSTEM/AUTHORITY_MODEL.md) and [Retrieval Policy](00_SYSTEM/RETRIEVAL_POLICY.md). The retained source is a pinned subset, so a pending rule is not validated by missing project code. The [Integration Boundary](06_SOURCE/Integration-Boundary.md) and [Fixture Registry](07_VALIDATION/Fixtures/Fixture-Registry.md) record remaining input and evidence limits.
