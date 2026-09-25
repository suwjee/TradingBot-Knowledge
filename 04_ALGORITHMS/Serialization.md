---
id: "algorithm.serialization"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Public serialization"
implemented_by: ["source.trading_pipeline"]
depends_on: ["algorithm.visibility", "algorithm.raw"]
source_refs: []
related_entities: ["test.source_validation", "test.output_validation"]
source_reference: []
---

# Public serialization

The full bridge serializer is absent from this scoped Vault. Its complete output schema, including E and StopAll Order provenance, is pending source capture and review. No former field inventory or output sample is authoritative here.

The retained detector and RAW source snapshots establish only their own local input and object fields. Use `algorithm.order.a` for the currently retained physical Order creation route. Do not infer the public JSON contract from this note until the bridge source and algorithm reference are republished without excluded routes.
