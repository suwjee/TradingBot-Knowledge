---
id: "behavior.e.red"
type: "behavior"
status: "canonical"
authority: "normative"
title: "E Red"
calculated_by: ["algorithm.e", "algorithm.reconciliation"]
implemented_by: ["source.e_zone_detector", "source.lifecycle_engine", "source.trading_pipeline"]
depends_on: ["behavior.e", "core.e_numbering"]
source_refs: ["engine/pipeline/e_zone_detector.py#L2463", "engine/pipeline/lifecycle_engine.py#L403"]
---

# E Red

E Red is a reconciled Red-family E, with family inherited from an active accepted parent or won through Red-priority reconciliation. It outranks S Red, E Blue, S Blue, and A, and remains below StopAll. It can advance recursive numbering after a stopped Red E. An accepted Red E clears pending Blue-repeat reversal evidence, but does not itself reset the independent E-driven StopAll owner counters unless a gate forms.
