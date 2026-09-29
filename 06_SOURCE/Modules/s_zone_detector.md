---
id: "source.s_zone_detector"
type: "source"
status: "active"
authority: "executable"
title: "S candidate races, source geometry, color decisions and shared accepted-Order stop reconciliation"
version: "4.20.0"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"
sha256: "ef71a2e4176caaabc25d1ef0c1f0f24efb54ed3110982cdb7cf52d2449cca2ee"
---

# s_zone_detector.py

S candidate races, source geometry, color decisions and shared accepted-Order stop reconciliation.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/s_zone_detector.py |
| SHA-256 | ef71a2e4176caaabc25d1ef0c1f0f24efb54ed3110982cdb7cf52d2449cca2ee |
| Bytes | 60888 |
| Lines | 1444 |
| Declared version | 4.20.0 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| SZone | 28 | 63 | class |
| SZoneDetector | 66 | 1418 | class |
| SZoneDetector.__init__ | 67 | 192 | self, direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], trend_blue_lines: Sequence[object], a_zones: Sequence[object], chronology: object, start_index: int \| None=None, end_index: int \| None=None, opposite_resets: Sequence[object]=(), initial_order_geometry: Callable[[int, datetime, int], object \| None] \| None=None |
| SZoneDetector._main_index | 194 | 195 | self, timestamp: datetime |
| SZoneDetector._lower_window | 197 | 200 | self, start: datetime, end: datetime \| None |
| SZoneDetector._reaction_confirmation_time | 202 | 205 | self, reaction: object, direction: str |
| SZoneDetector.reaction_confirmation_time | 207 | 211 | self, reaction: object, direction: str |
| SZoneDetector._reset_time | 214 | 215 | self, reset: object |
| SZoneDetector._a_confirmation_time | 217 | 223 | self, zone: object |
| SZoneDetector._trend_extreme | 225 | 228 | self, candle: object |
| SZoneDetector._a_stopped | 230 | 231 | self, value: Decimal, level: Decimal |
| SZoneDetector._first_a_stop | 233 | 267 | self, level: Decimal, start: datetime |
| SZoneDetector.first_a_stop | 269 | 273 | self, level: Decimal, start: datetime |
| SZoneDetector._resolved_order_backed_zone | 276 | 292 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], first_order_match: tuple[int, object, datetime] |
| SZoneDetector._candidate_source | 295 | 308 | self, start_index: int, end_index: int |
| SZoneDetector._candidate_source_last | 310 | 328 | self, start_index: int, end_index: int |
| SZoneDetector._first_trend_reaction_after_order | 330 | 339 | self, order_confirmation_time: datetime |
| SZoneDetector._nested_trend_reaction | 342 | 370 | self, order: object, order_confirmation_time: datetime |
| SZoneDetector._simple_candidate | 372 | 379 | self, order: object, reaction: object |
| SZoneDetector._type3_reset_leg | 381 | 395 | self, reset: object |
| SZoneDetector._type3_has_trend_reaction | 397 | 404 | self, a_stop_event: datetime, crossing: datetime |
| SZoneDetector._first_type3 | 406 | 453 | self, a_stop_event: datetime, deadline: datetime |
| SZoneDetector._type4_has_blue | 456 | 465 | self, candidate_source_index: int, crossing_event: datetime |
| SZoneDetector._first_type4 | 467 | 535 | self, a_stop: tuple[int, datetime, datetime], deadline: datetime |
| SZoneDetector._build_type4_zone | 537 | 587 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], type4: tuple[int, datetime, Decimal, int, datetime, int, datetime] |
| SZoneDetector._candidate_after_order | 590 | 629 | self, order_confirmation_time: datetime, reaction: object |
| SZoneDetector._a_source_event_time | 631 | 638 | self, zone: object |
| SZoneDetector._a_owned_by_s | 640 | 679 | self, zone: object |
| SZoneDetector._a_pair_is_reset_reset | 681 | 692 | self, zone: object |
| SZoneDetector.eligible_a_zones | 695 | 697 | self |
| SZoneDetector._candidate_timing | 699 | 742 | self, a_stop_index: int, order: object, order_confirmation_time: datetime, a_stop_event_time: datetime \| None=None |
| SZoneDetector._candidate_before_order | 744 | 786 | self, a_stop_index: int, order: object, a_stop_event_time: datetime \| None=None |
| SZoneDetector._candidate_event_time | 788 | 801 | self, source_index: int, level: Decimal, not_before: datetime |
| SZoneDetector.candidate_event_time | 803 | 807 | self, source_index: int, price: Decimal, fallback: datetime |
| SZoneDetector._blue_formation_time | 810 | 838 | self, line: object |
| SZoneDetector._candidate_cross_has_blue | 840 | 855 | self, reaction_number: int, event_time: datetime |
| SZoneDetector._has_ordinary_trend_reaction | 857 | 865 | self, behavior_start: datetime, event_time: datetime |
| SZoneDetector._candidate_crossed | 868 | 870 | self, candle: object, level: Decimal |
| SZoneDetector._decision | 873 | 996 | self, candidate_level: Decimal, order_stop_level: Decimal, start: datetime, trend_reaction_number: int, behavior_start: datetime, candidate_start: datetime \| None=None, fallback_on_unqualified_cross: bool=False |
| SZoneDetector._build_type3_zone | 999 | 1055 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], type3: tuple[int, datetime, Decimal, int, datetime, int, datetime, datetime] |
| SZoneDetector._build_order_backed_zone | 1057 | 1226 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], order_match: tuple[int, object, datetime] |
| SZoneDetector.detect | 1228 | 1302 | self |
| SZoneDetector.reconcile_shared_order_stops | 1305 | 1418 | self, zones: Sequence[SZone], order_entries: Sequence[dict[str, object]] |
| detect_s_zones | 1421 | 1444 | direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], trend_blue_lines: Sequence[object], a_zones: Sequence[object], chronology: object, start_index: int \| None=None, end_index: int \| None=None, opposite_resets: Sequence[object]=(), initial_order_geometry: Callable[[int, datetime, int], object \| None] \| None=None |
