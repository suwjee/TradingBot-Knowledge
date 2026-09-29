---
id: "source.lifecycle_engine"
type: "source"
status: "active"
authority: "executable"
title: "Lifecycle ownership, StopAll gates, retained calculation lineage and final visibility"
version: "1.17.0"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"
sha256: "94feb038e1e78b291762cfc03dfc370e48bb94f3e1fe1171b7a5206301e8be13"
---

# lifecycle_engine.py

Lifecycle ownership, StopAll gates, retained calculation lineage and final visibility.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py |
| SHA-256 | 94feb038e1e78b291762cfc03dfc370e48bb94f3e1fe1171b7a5206301e8be13 |
| Bytes | 64325 |
| Lines | 1555 |
| Declared version | 1.17.0 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| sequence_priority | 37 | 39 | kind: str, family: str |
| StopAll | 43 | 92 | class |
| StopAllDetector | 95 | 600 | class |
| StopAllDetector.__init__ | 96 | 115 | self, direction: str, s_zones: Sequence[object], e_zones: Sequence[object], chronology: object |
| StopAllDetector._strict_stop | 117 | 131 | self, start: datetime, level: Decimal |
| StopAllDetector._e_key | 134 | 135 | item: object |
| StopAllDetector._dominates_e | 138 | 145 | new: tuple[str, int], old: tuple[str, int] |
| StopAllDetector._sequence_priority | 148 | 149 | cls, kind: str, family: str |
| StopAllDetector._active_sequence_priority | 152 | 159 | cls, s_key: str \| None, e_key: tuple[str, int] \| None |
| StopAllDetector._stopall_from_e | 161 | 217 | self, item: object, number: int, gate_type: str, gate_event: datetime, behavior_type: str, behavior_key: str, behavior_count: int |
| StopAllDetector._optional_int | 220 | 221 | value: object \| None |
| StopAllDetector._optional_decimal | 224 | 225 | value: object \| None |
| StopAllDetector._stopall_from_s | 227 | 322 | self, item: object, behavior_type: str, behavior_key: str, behavior_count: int, underlying_e_key: tuple[str, int] \| None |
| StopAllDetector._blue_repeat_key | 325 | 338 | kind: str, number: int \| None=None |
| StopAllDetector._record_blue_repeat | 341 | 348 | counts: dict[tuple[str, int \| None], int], latest: dict[tuple[str, int \| None], object], key: tuple[str, int \| None], item: object |
| StopAllDetector._opposite_s_stopall_gate | 350 | 395 | self, s_item: object, blue_repeat_counts: dict[tuple[str, int \| None], int], blue_repeat_latest: dict[tuple[str, int \| None], object] |
| StopAllDetector.detect | 397 | 600 | self |
| StopAllDetector.detect.reset_cycle_blue_repeats | 413 | 415 |  |
| StopAllDetector.detect.process_s_event | 417 | 466 | s_item: object |
| detect_stopalls | 603 | 609 | direction: str, s_zones: Sequence[object], e_zones: Sequence[object], chronology: object |
| resolve_order_context | 616 | 665 | order_audit: dict, accepted_a_sources: set[datetime], inherited_blocked_first_times: set[datetime], invalid_a_zones: Sequence[object], pending_s_a_sources: set[datetime], opposite_reactions: Sequence[object], candles: Sequence[object], direction: str, stop_finder |
| visible_a_zones_after_s_stops | 668 | 682 | a_zones, s_zones, candles |
| module_priority | 684 | 696 | item: object |
| module_identity | 698 | 705 | item: object |
| module_stop_event | 707 | 719 | item: object, stop_event_finder=None |
| strictly_beyond_boundary | 721 | 724 | price: Decimal, boundary: Decimal, direction: str |
| dominant_module | 726 | 735 | modules: Sequence[object] |
| split_a_zones_by_dominant_stops | 738 | 939 | a_zones, s_zones, e_zones, stopalls, candles, direction, stop_event_finder=None, trend_reactions=None, confirmation_finder=None, a_stop_event_finder=None, stage_invalid_a_identities=None |
| blocked_orders_while_invalid_leg_heads_are_live | 941 | 961 | invalid_a_zones, opposite_reactions, candles, direction, stop_finder |
| consumed_s_evidence_after_larger_stop | 964 | 1104 | s_candidates, accepted_s_zones, e_zones, direction, stop_event_finder, candles |
| s_zones_for_module_engines | 1106 | 1134 | s_zones, e_zones, direction |
| s_zones_for_stopall | 1136 | 1153 | s_zones, e_zones, direction |
| visible_s_zones_after_module_resets | 1155 | 1322 | s_zones, e_zones, direction, stop_event_finder=None, source_event_finder=None, candles=None |
| reconcile_stopall_lifecycle | 1324 | 1354 | detector, s_zones, e_zones, chronology, direction, timed_step=None |
| visible_a_zones_after_module_boundaries | 1357 | 1402 | a_zones, s_zones, e_zones, direction, stop_event_finder=None |
| reaction_number_is_internal | 1404 | 1415 | items, number, identities |
| point_is_inside_healthy_reaction | 1418 | 1438 | source_time, price, reactions |
| filter_internal_behavior_outputs | 1441 | 1452 | a_zones, s_zones, e_zones, stopalls, opposite_reactions, opposite_internal_identities, all_behavior_reactions |
| finalize_behavior_visibility | 1454 | 1546 | a_zones, s_zones, e_zones, stopalls, direction, invalid_s_identities, stop_event_finder, source_event_finder, candles, *, all_a_zones=None |
| visible_a_zones | 1549 | 1555 | a_zones: Sequence[object], s_zones: Sequence[object] |
