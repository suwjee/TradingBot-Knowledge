---
id: "source.map"
type: "source"
status: "pending"
authority: "non-canonical"
title: "Source map"
source_refs: []
relates_to: ["core.pipeline"]
related_entities: ["test.source_validation"]
source_reference: []
---

# Retained source map

The byte-exact `06_SOURCE/Code` inventory now contains all nine main Engine modules. The bridge, E detector and lifecycle module are mixed executable evidence: their B/C-dependent regions are known invalid, while unrelated regions remain reviewable. The comprehensive HPZR6 references are registered by hash in `06_SOURCE/References/registry.json` and optionally read from a production checkout. The Vault does not treat their B/C descriptions as normative.

| Knowledge | Retained source |
| --- | --- |
| Reaction and Reset | `reaction_engine.py` |
| Blue | `blue_line_detector.py` |
| A | `a_zone_detector.py` |
| S and stopped-A Order_A selection | `s_zone_detector.py` |
| E construction and current defective B/C routes | `e_zone_detector.py` |
| StopAll, lifecycle and visibility | `lifecycle_engine.py` |
| RAW parsing, orchestration and serialization | `trading_pipeline.py` |
| Decimal and physical identity | `core_utils.py` |
| Directional strictness | `direction_policy.py` |

The accepted `Order_A` note covers the immutable first stopped-A owner and evidenced direct E routes. The current B/C implementation is quarantined in `algorithm.order.b` and `algorithm.order.c`. E-stage continuation and final visibility can now be traced in local source, but any conclusion using the defective B/C creation causes is not an accepted regression baseline.
