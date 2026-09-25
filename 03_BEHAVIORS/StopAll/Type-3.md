---
id: "behavior.stopall.type3"
type: "behavior"
status: "pending"
authority: "non-canonical"
title: "StopAll Type-3"
calculated_by: ["algorithm.stopall"]
implemented_by: ["source.lifecycle_engine"]
depends_on: ["behavior.stopall", "behavior.s.red"]
source_gate_type: "opposite-s-group-stop"
source_refs: []
related_entities: ["test.lifecycle_invariants"]
source_reference: []
---

# StopAll Type-3

Public Type-3 maps exactly to gate_type=opposite-s-group-stop. Accepted Blue occurrences accumulate by exact group: all S Blue in one group; each numbered E Blue in its own group. A group with count >=2 arms the reversal. The first accepted S Red with a native Mode-B forming Order promotes to StopAll1 before ordinary S replacement. A Red S with Mode A/no Order, or an accepted Red E, clears pending Blue evidence without promotion; StopAll also clears it. Different E numbers never combine. The newest qualifying group's last occurrence selects deterministic metadata.
