---
id: "test.lifecycle_invariants"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Lifecycle invariant checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.invariant_validation", "core.lifecycle", "core.priority", "behavior.stopall", "algorithm.lifecycle", "source.lifecycle_engine"]
source_reference: []
---

# Lifecycle invariant checks

Assert StopAll > E Red > S Red > E Blue > S Blue > A, but resolve eligibility at the most recent relevant exact stop transition before priority ties. The stage path is A → S → E → StopAll; after a hard StopAll boundary, active S/E owner state and pending exact Blue-repeat evidence are cleared before a new cycle. Both references §§12–13; lifecycle_engine.py lines 25–35, 403–455 and 946–1177.

Test that a rejected fallback A under accepted S neither consumes that S nor contributes S descendants to E/StopAll. Test that a historical parent restored for lineage cannot retake active ownership. Check same-source E wins over S for larger-module/StopAll participation while the allowed S lineage remains. Both references §§12.1–12.3, 14; lifecycle_engine.py lines 946–1177 and 1708–1803.

For StopAll reversal, S Blue is one exact key regardless of subtype; E1 Blue and E2 Blue are distinct keys. An accepted Red S/E clears pending Blue reversal counts; only native Mode-B accepted S Red can use a qualifying pending repeat, while E-driven gate counters remain separate. Both references §13; lifecycle_engine.py lines 331–455. Source fixtures 1.7, 1.8, 1.10, 1.12, 4.3 and 5.2 provide targeted examples, not production branches.
