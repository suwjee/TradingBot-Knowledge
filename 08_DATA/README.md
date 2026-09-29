---
id: "data.policy"
type: "data"
status: "active"
authority: "executable"
title: "Intentionally empty current Data store"
version: "current"
related_entities: ["test.fixture_model", "workflow.analyze_raw"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
data_kind: "policy"
---

# Intentionally empty current Data store

Market Data Registry: EMPTY BY DESIGN. Real RAW dataset count: 0. Physical market-data file count: 0. Dataset registry entries: 0. Raw/ is an empty future input directory. No RAW evidence is currently stored.

Future Data must be explicitly supplied by the user. Preserve its immutable physical bytes, SHA-256, provider/instrument metadata, finest resolution, row count, monotonic native epochs and full display datetime with timezone. Record physical input and logical extraction windows separately; never infer an exact window hash from a physical-file hash.

Validate schema, OHLC consistency, duplicate seconds, gaps, resolution and timezone before invoking a calculation. A data-integrity PASS does not establish trading correctness. Future fixtures may link to verified input, but neither data nor a filename defines an algorithmic rule.
