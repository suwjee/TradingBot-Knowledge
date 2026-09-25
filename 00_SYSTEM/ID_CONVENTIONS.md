---
id: "system.ids"
type: "system"
status: "canonical"
authority: "normative"
title: "Stable ID conventions"
related_entities: []
source_reference: []
---

# Stable ID conventions

IDs are lowercase dotted semantic names independent of folders and source paths. Populated prefixes are `system.*`, `core.*`, `market.*`, `behavior.*`, `algorithm.*`, `source.*`, `mirror.*`, `test.*`, `case.*`, and `data.*`. Examples: `behavior.s.blue.type4`, `algorithm.order.c`, `source.e_zone_detector`, `data.dataset_f5bc29e3`. A variant suffix names a real source/public distinction, not a new behavior inferred from a display label. Dataset IDs use the first eight characters of a verified SHA-256 and retain the complete hash in metadata.

Never reuse an ID for changed meaning. Moving a note changes its locator in regenerated indexes while retaining the ID. If meaning splits, retain the original as an umbrella or mark it superseded and migrate every relation atomically. A changed RAW hash gets a new dataset ID, not an overwrite of the old byte identity. Future decision/version/workflow/plugin/policy prefixes require a documented schema revision when their phases are implemented; do not assign them preemptively from empty folders.

StopAll Type-1/2/3 IDs follow the public bridge formation mapping: `sequence-group-stop` -> Type-1, `stopall-stop` -> Type-2, and `opposite-s-group-stop` -> Type-3. S Blue Type-1/2/3/4 map `simple`/`advanced`/`type3`/`type4`. E numbers are state, not distinct algorithm IDs.
