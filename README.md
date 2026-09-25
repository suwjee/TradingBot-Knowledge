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

This repository is a standalone, scoped knowledge snapshot. Its currently retained physical Order creation route is `Order_A`. Mixed source files and comprehensive directional references containing excluded creation routes are outside this Vault while those routes are rewritten in the project. Claims that lost local source evidence are marked pending. The Vault retains nine byte-pinned Python source files, chart input-boundary evidence, seven registered RAW datasets, three verified RAW windows, 22 curated fixture cases, schemas, and relationship indexes. Three superseded small RAWs remain on disk pending deletion. Reading this snapshot requires no separate TradingBot checkout.

The registered RAW hashes and windows verify, but the physical inventory is not yet clean: the three superseded files and their sidecars are still present. A plugin `verify` result therefore reports `verified_pins_ok: true`, `inventory_complete: false`, and overall `ok: false` until their removal is permitted.

## Quick check

From the Vault root, with Python 3.10 or newer and `jsonschema>=4.18,<5` installed:

```text
python -B _SCHEMA/build_indexes.py --check
```

AI hosts can read the Markdown and `_INDEX` files directly. A separate portable plugin can also read this Vault through a configured Vault root. The plugin executable and its dependencies are not stored here.

Start rule analysis with [Authority Model](00_SYSTEM/AUTHORITY_MODEL.md) and [Retrieval Policy](00_SYSTEM/RETRIEVAL_POLICY.md). The retained source is a pinned subset, so a pending rule is not validated by missing project code. The [Integration Boundary](06_SOURCE/Integration-Boundary.md) and [Fixture Registry](07_VALIDATION/Fixtures/Fixture-Registry.md) record remaining input and evidence limits.
