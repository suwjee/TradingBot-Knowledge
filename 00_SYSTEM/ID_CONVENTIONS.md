---
id: "system.ids"
type: "system"
status: "canonical"
authority: "normative"
title: "Stable ID conventions"
---

# Stable ID conventions

IDs are lowercase dotted semantic names independent of folders and source paths. Existing prefixes are `system.*`, `core.*`, `market.*`, `behavior.*`, `algorithm.*`, and `source.*`; `mirror.*`, `test.*`, and `case.*` are reserved. Examples: `behavior.s.blue.type4`, `algorithm.order.c`, `source.e_zone_detector`. A variant suffix names a real source/public distinction, not a new behavior inferred from a display label.

Never reuse an ID for changed meaning. Moving a note changes its locator in regenerated indexes while retaining the ID. If meaning splits, retain the original as an umbrella or mark it superseded and migrate every relation atomically. Future data/decision/version/workflow/plugin/policy prefixes require a documented schema revision when their phases are implemented; do not assign them preemptively from empty folders.

StopAll Type-1/2/3 IDs follow the public bridge formation mapping: `sequence-group-stop` -> Type-1, `stopall-stop` -> Type-2, and `opposite-s-group-stop` -> Type-3. S Blue Type-1/2/3/4 map `simple`/`advanced`/`type3`/`type4`. E numbers are state, not distinct algorithm IDs.
