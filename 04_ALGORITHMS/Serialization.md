---
id: "algorithm.serialization"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Public serialization"
affected_by_known_invalid_order_route: true
implemented_by: ["source.trading_pipeline"]
depends_on: ["algorithm.visibility", "algorithm.raw"]
source_refs: []
related_entities: ["test.source_validation", "test.output_validation"]
source_reference: []
---

# Public serialization

The full bridge serializer is captured byte-exact at `06_SOURCE/Code/engine/bridge/trading_pipeline.py`. Its current output schema can be inspected as executable evidence. Fields carrying B/C causes remain affected by known-invalid route semantics; no former output sample is an approved regression baseline by itself.

The retained detector and RAW source snapshots establish only their own local input and object fields. Use `algorithm.order.a` for the currently retained physical Order creation route. Do not infer the public JSON contract from this note until the bridge source and algorithm reference are republished without excluded routes.
