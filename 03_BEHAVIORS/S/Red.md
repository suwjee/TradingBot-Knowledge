---
id: "behavior.s.red"
type: "behavior"
status: "canonical"
authority: "normative"
title: "S Red"
calculated_by: ["algorithm.s"]
implemented_by: ["source.s_zone_detector", "source.lifecycle_engine"]
depends_on: ["behavior.s", "algorithm.order"]
source_refs: ["engine/pipeline/s_zone_detector.py#L964", "engine/pipeline/lifecycle_engine.py#L356"]
---

# S Red

S Red is an S whose decision is owned by a strict stop of a calculation-accepted opposite physical Order. It may result from the original stopped-A Order or from shared accepted-Order stop reconciliation. Its parent is still the stopped A; accepted-live Order use does not transfer the Order's creation cause to that A.

Red S outranks E Blue and S Blue but not E Red or StopAll. An accepted Red S resolves pending exact-key Blue-repeat evidence. If its native forming Order is Mode B and a same exact Blue group has at least two accepted occurrences, the S is promoted to StopAll Type-3 before ordinary S replacement. A Mode A or absent Order leaves it S Red and still clears that pending evidence.
