---
id: "behavior.stopall.type3"
type: "behavior"
status: "canonical"
authority: "normative"
title: "StopAll Type-3"
calculated_by: ["algorithm.stopall"]
implemented_by: ["source.lifecycle_engine", "source.trading_pipeline"]
depends_on: ["behavior.stopall", "behavior.s.red"]
source_gate_type: "opposite-s-group-stop"
source_refs: ["engine/pipeline/lifecycle_engine.py#L331", "engine/pipeline/lifecycle_engine.py#L356", "engine/bridge/trading_pipeline.py#L1300"]
---

# StopAll Type-3

Public Type-3 maps exactly to gate_type=opposite-s-group-stop. Accepted Blue occurrences accumulate by exact group: all S Blue in one group; each numbered E Blue in its own group. A group with count >=2 arms the reversal. The first accepted S Red with a native Mode-B forming Order promotes to StopAll1 before ordinary S replacement. A Red S with Mode A/no Order, or an accepted Red E, clears pending Blue evidence without promotion; StopAll also clears it. Different E numbers never combine. The newest qualifying group's last occurrence selects deterministic metadata.
