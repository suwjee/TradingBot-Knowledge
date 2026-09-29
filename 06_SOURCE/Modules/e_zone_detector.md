---
id: "source.e_zone_detector"
type: "source"
status: "active"
authority: "executable"
title: "E parent-stop cycles, recursive families and reconciled Order-backed continuation"
version: "6.16.1"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/e_zone_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/e_zone_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/e_zone_detector.py"
sha256: "38834e96cc58931fe2e12096f4465ecaa046387d30fd40fecbd6891971020988"
---

# e_zone_detector.py

E parent-stop cycles, recursive families and reconciled Order-backed continuation.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/e_zone_detector.py |
| SHA-256 | 38834e96cc58931fe2e12096f4465ecaa046387d30fd40fecbd6891971020988 |
| Bytes | 44859 |
| Lines | 1033 |
| Declared version | 6.16.1 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| EZone | 31 | 66 | class |
| EZoneDetector | 69 | 1001 | class |
| EZoneDetector.__init__ | 70 | 210 | self, direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], s_zones: Sequence[object], opposite_resets: Sequence[object], chronology: object, start_index: int=0, end_index: int \| None=None, direct_geometry_finder: Callable[[str, int, int, datetime], object \| None] \| None=None, blocked_order_first_times: set[datetime] \| None=None, initial_order_audit: dict[tuple[int, int], dict[str, object]] \| None=None, sequence_resets: dict[datetime, int] \| None=None, sequence_priority: Callable[[str, str], int] \| None=None, invalid_s_root_identities: set[tuple[datetime, int]] \| None=None, order_b_legs: Sequence[OrderBResetLeg]=() |
| EZoneDetector.sequence_resets | 213 | 214 | self |
| EZoneDetector.sequence_resets | 217 | 224 | self, resets: dict[datetime, int] |
| EZoneDetector._reset_time | 226 | 227 | self, reset: object |
| EZoneDetector._main_index | 229 | 230 | self, value: datetime |
| EZoneDetector._first_cross_position | 233 | 248 | self, left: int, right: int, level: Decimal, *, less: bool |
| EZoneDetector._stop_value | 250 | 251 | self, item: object |
| EZoneDetector._first_parent_stop | 254 | 265 | self, source_time: datetime, level: Decimal |
| EZoneDetector._confirmation_for | 267 | 268 | self, reaction: object, direction: str |
| EZoneDetector._confirmation | 270 | 271 | self, reaction: object |
| EZoneDetector._reaction_first_time | 273 | 274 | self, reaction: object |
| EZoneDetector._parent_stop | 277 | 283 | self, parent_type: str, parent: object |
| EZoneDetector.parent_stop | 285 | 289 | self, parent_type: str, parent: object |
| EZoneDetector._extreme_between | 292 | 306 | self, start: datetime, end: datetime |
| EZoneDetector._zone | 308 | 408 | self, family: str, number: int, parent_type: str, parent: object, stop_event: datetime |
| EZoneDetector.set_consumed_s_evidence | 410 | 420 | self, evidence: Sequence[tuple[object, object]] |
| EZoneDetector._apply_consumed_s_evidence | 422 | 438 | self, zones: Sequence[EZone] |
| EZoneDetector.continuation_chain_from_s | 440 | 477 | self, owner: EZone, s_zone: object |
| EZoneDetector.replace_with_earlier_continuation | 479 | 520 | self, base_zones: Sequence[EZone], owner: EZone, continuation: Sequence[EZone] |
| EZoneDetector.replace_with_earlier_continuation.descends_from_owner | 488 | 502 | item: EZone |
| EZoneDetector.resolve_same_source_conflicts | 522 | 564 | self, zones: Sequence[EZone] |
| EZoneDetector.resolve_same_source_conflicts.outranks | 540 | 547 | candidate: EZone, current: EZone |
| EZoneDetector.restore_independent_s_roots | 566 | 624 | self, dominant_zones: Sequence[EZone] |
| EZoneDetector._discover_candidate_chains | 626 | 716 | self |
| EZoneDetector._reconcile_candidate_chains | 718 | 988 | self, candidates: list[EZone] |
| EZoneDetector._reconcile_candidate_chains.valid_order | 749 | 750 | zone: EZone |
| EZoneDetector._reconcile_candidate_chains.parent_active | 752 | 822 | zone: EZone, seen: set[tuple[int, datetime]] \| None=None |
| EZoneDetector._reconcile_candidate_chains.stopped_by | 824 | 829 | zone: EZone, prior: EZone |
| EZoneDetector._reconcile_candidate_chains.ownership_priority | 880 | 885 | item: EZone |
| EZoneDetector._reconcile_candidate_chains.collect_lineage | 966 | 978 | zone: EZone, seen: set[tuple[int, datetime]] |
| EZoneDetector.detect | 991 | 1001 | self |
| detect_e_zones | 1004 | 1033 | direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], s_zones: Sequence[object], opposite_resets: Sequence[object], chronology: object, start_index: int=0, end_index: int \| None=None, direct_geometry_finder: Callable[[str, int, int, datetime], object \| None] \| None=None, blocked_order_first_times: set[datetime] \| None=None, initial_order_audit: dict[tuple[int, int], dict[str, object]] \| None=None, sequence_priority: Callable[[str, str], int] \| None=None, invalid_s_root_identities: set[tuple[datetime, int]] \| None=None |
