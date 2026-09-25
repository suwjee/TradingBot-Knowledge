---
id: "system.ids"
type: "system"
status: "canonical"
authority: "normative"
title: "Stable ID conventions"
---

# Stable ID conventions

IDs are lowercase dotted names independent of folders. Prefixes identify kind: system.*, core.*, market.*, behavior.*, algorithm.*, source.*, mirror.*. A variant suffix identifies a real source distinction, not a new behavior inferred from a display label. Examples: behavior.s.blue.type4, algorithm.order.c, source.e_zone_detector.

Never reuse an ID for changed semantics. Rename paths by updating entities.json and relations, while retaining the ID. If meaning splits, retain the original as an umbrella or mark it superseded and create new IDs. StopAll Type-1/2/3 IDs follow the public bridge formation mapping: sequence-group-stop to Type-1, stopall-stop to Type-2, and opposite-s-group-stop to Type-3. The detector stores gate_type and the bridge projects the numbered formation.

