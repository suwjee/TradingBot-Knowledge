---
id: "source.a_zone_detector"
type: "source"
status: "active"
authority: "executable"
title: "A formation, paired Blue provenance and inherited stops"
version: "1.6.4"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/a_zone_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/a_zone_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/a_zone_detector.py"
sha256: "d7c33dd619ad7e4590027667a2c4e984c83be7b82fbfafeb5d7f944ddd521097"
---

# a_zone_detector.py

A formation, paired Blue provenance and inherited stops.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/a_zone_detector.py |
| SHA-256 | d7c33dd619ad7e4590027667a2c4e984c83be7b82fbfafeb5d7f944ddd521097 |
| Bytes | 31007 |
| Lines | 797 |
| Declared version | 1.6.4 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| BlueState | 25 | 34 | class |
| AZone | 38 | 64 | class |
| AZoneDetector | 67 | 788 | class |
| AZoneDetector.__init__ | 68 | 94 | self, direction: str, reactions: Sequence[object], blue_lines: Sequence[object], chronology: object |
| AZoneDetector.extreme_name | 97 | 98 | self |
| AZoneDetector._strict_cross | 100 | 101 | self, value: Decimal, level: Decimal |
| AZoneDetector._better | 103 | 104 | self, value: Decimal, current: Decimal |
| AZoneDetector._main_index | 106 | 107 | self, timestamp: datetime |
| AZoneDetector._lower_window | 109 | 112 | self, start: datetime, end: datetime \| None |
| AZoneDetector._first_crossing | 114 | 154 | self, level: Decimal, start: datetime, end: datetime \| None |
| AZoneDetector._range_extreme | 156 | 188 | self, start: datetime, end: datetime |
| AZoneDetector._formation | 190 | 205 | self, line: object |
| AZoneDetector._reset_formation_time | 207 | 217 | self, line: object, source_index: int |
| AZoneDetector._build_blue_states | 219 | 246 | self |
| AZoneDetector._double_stop_a_candidates | 248 | 309 | self |
| AZoneDetector._pair_trigger | 311 | 469 | self, previous: BlueState, current: BlueState, expires_at: datetime \| None |
| AZoneDetector._reaction_confirmation_time | 471 | 474 | self, reaction: object |
| AZoneDetector._first_reaction_after | 476 | 492 | self, trigger_event_time: datetime, *, not_before: datetime \| None=None |
| AZoneDetector._inherited_stop | 494 | 545 | self, previous: BlueState, current: BlueState |
| AZoneDetector._a_source | 547 | 566 | self, trigger_index: int, reaction: object |
| AZoneDetector._detect_ordinary_a | 568 | 687 | self, states: list[BlueState] |
| AZoneDetector._filter_special_a | 689 | 751 | self, special: list[AZone], ordinary: list[AZone] |
| AZoneDetector.detect | 753 | 763 | self |
| AZoneDetector._a_was_stopped_before | 765 | 788 | self, zone: AZone, end_time: datetime, *, not_before: datetime \| None=None |
| detect_a_zones | 791 | 797 | direction: str, reactions: Sequence[object], blue_lines: Sequence[object], chronology: object |
