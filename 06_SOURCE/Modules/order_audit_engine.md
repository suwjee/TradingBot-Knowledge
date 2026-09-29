---
id: "source.order_audit_engine"
type: "source"
status: "active"
authority: "executable"
title: "Physical Order_A and Order_B discovery, reset-leg anchors, immutable identity/provenance and accepted/live ledgers"
version: "1.5.1"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/order_audit_engine.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"
sha256: "09cba00c0623ffcce0d7bc3460c1e963c4e2b14fb02a9172cc25dcca8ba9aedc"
---

# order_audit_engine.py

Physical Order_A and Order_B discovery, reset-leg anchors, immutable identity/provenance and accepted/live ledgers.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/order_audit_engine.py |
| SHA-256 | 09cba00c0623ffcce0d7bc3460c1e963c4e2b14fb02a9172cc25dcca8ba9aedc |
| Bytes | 75219 |
| Lines | 1863 |
| Declared version | 1.5.1 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| PostBehaviorStop | 18 | 22 | class |
| OrderBBehaviorAnchor | 26 | 31 | class |
| OrderBResetLeg | 35 | 52 | class |
| dominant_post_behavior_stops | 55 | 98 | chronology: object, lifetimes: Sequence[tuple[str, object, datetime \| None]], priority: Callable[[object], int] |
| order_b_reset_event_time | 101 | 129 | direction: str, chronology: object, reset: object |
| discover_order_b_reset_legs | 132 | 325 | direction: str, chronology: object, trend_reactions: Sequence[object], resets: Sequence[object], opposite_reactions: Sequence[object], post_stops: Sequence[PostBehaviorStop], a_formation_times: Sequence[datetime], *, behavior_anchors: Sequence[OrderBBehaviorAnchor]=() |
| discover_accepted_order_b_reset_legs | 328 | 403 | direction: str, chronology: object, trend_reactions: Sequence[object], trend_resets: Sequence[object], opposite_reactions: Sequence[object], a_zones: Sequence[object], invalid_a_identities: set[tuple[datetime, int]], s_zones: Sequence[object], e_zones: Sequence[object], stopalls: Sequence[object], s_detector: object, e_detector: object, priority: Callable[[object], int] |
| order_b_leg_identity | 413 | 433 | items: Sequence[object] |
| OrderAuditEngineMixin | 437 | 1563 | class |
| OrderAuditEngineMixin._order_stop | 440 | 466 | self, number: int, reaction: object, context_start: datetime \| None=None |
| OrderAuditEngineMixin.order_stop | 469 | 473 | self, reaction_number: int, reaction: object |
| OrderAuditEngineMixin._first_healthy_direct_geometry | 476 | 548 | self, start: datetime, allow_bounded_continue: bool=False |
| OrderAuditEngineMixin._trend_leg_direct_order | 551 | 600 | self, start: datetime |
| OrderAuditEngineMixin._direct_parent_stop_order | 603 | 674 | self, start: datetime, continuous_deadline: datetime \| None, allow_bounded_continue: bool |
| OrderAuditEngineMixin._merge_order_candidate | 677 | 708 | self, by_geometry: dict[tuple[int, int], OrderMatch], number: int, reaction: object, confirmation: datetime, *, parent_stop_cause_time: datetime |
| OrderAuditEngineMixin._enforce_single_parent_stop_owner | 711 | 735 | self, by_geometry: dict[tuple[int, int], OrderMatch] |
| OrderAuditEngineMixin.order_candidates | 738 | 824 | self, start: datetime, continuous_deadline: datetime \| None=None, allow_bounded_continue: bool=False, allow_trend_leg_continue: bool=False |
| OrderAuditEngineMixin._first_order | 827 | 840 | self, start: datetime, continuous_deadline: datetime \| None=None, allow_bounded_continue: bool=False, allow_trend_leg_continue: bool=False |
| OrderAuditEngineMixin._has_sequence_reset_between | 843 | 851 | self, start: datetime, end: datetime |
| OrderAuditEngineMixin._index_order_audit_identity | 854 | 861 | self, identity: tuple[int, int], confirmation: datetime |
| OrderAuditEngineMixin._clear_order_audit | 864 | 867 | self |
| OrderAuditEngineMixin.register_order_b_reset_legs | 870 | 933 | self, legs: Sequence[OrderBResetLeg] |
| OrderAuditEngineMixin._register_order_audit | 936 | 999 | self, parent_type: str, parent: object, parent_stop: datetime |
| OrderAuditEngineMixin.visual_order_lifecycle | 1003 | 1022 | self, start: datetime |
| OrderAuditEngineMixin._cross_order | 1025 | 1043 | self, start: datetime, level: Decimal |
| OrderAuditEngineMixin.cross_order | 1046 | 1050 | self, confirmation_time: datetime, stop_level: Decimal |
| OrderAuditEngineMixin._unconsumed_s_orders | 1053 | 1087 | self, parent: object, parent_stop: datetime |
| OrderAuditEngineMixin._initial_order_records | 1090 | 1145 | self |
| OrderAuditEngineMixin._initial_record_match | 1150 | 1161 | record: tuple[datetime, datetime, int, object, Decimal, int, datetime, tuple[int, datetime, datetime] \| None], causes: tuple[str, ...] |
| OrderAuditEngineMixin._initial_order_match | 1164 | 1176 | self, entry: dict[str, object], causes: tuple[str, ...] |
| OrderAuditEngineMixin._gate_owned_initial_order | 1179 | 1199 | self, parent_stop: datetime |
| OrderAuditEngineMixin._carried_orders_for_parent | 1202 | 1260 | self, parent: object, parent_stop: datetime |
| OrderAuditEngineMixin._post_stop_accepted_orders_for_parent | 1263 | 1329 | self, parent: object, parent_stop: datetime |
| OrderAuditEngineMixin._post_stop_accepted_orders_for_parent.add_match | 1270 | 1283 | match: OrderMatch |
| OrderAuditEngineMixin._blocked_by_gate_owned_order | 1332 | 1340 | self, zone: EZone |
| OrderAuditEngineMixin._rebuild_accepted_order_audit | 1343 | 1524 | self, numbered: list[EZone], supplemental_s_zones: Sequence[object]=() |
| OrderAuditEngineMixin._rebuild_accepted_order_audit.valid_parent_stop_cause | 1354 | 1367 | cause: tuple[object, ...] |
| OrderAuditEngineMixin.rebuild_accepted_order_audit | 1527 | 1539 | self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object]=() |
| OrderAuditEngineMixin.ensure_accepted_order_audit | 1542 | 1563 | self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object]=() |
| prepare_order_audit | 1566 | 1692 | detector, start_index: int, end_index: int, s_detector=None, accepted_a_sources: set[datetime] \| None=None, required_identities: set[tuple[int, int]] \| None=None |
| accepted_audit_entry | 1695 | 1722 | entry: dict[str, object], accepted_sources: set |
| order_identity_is_internal | 1725 | 1731 | item, internal_identities |
| SOrderAuditMixin | 1734 | 1862 | class |
| SOrderAuditMixin._first_order_after | 1737 | 1747 | self, a_stop_event_time: datetime |
| SOrderAuditMixin._order_matches_after | 1750 | 1769 | self, a_stop_event_time: datetime |
| SOrderAuditMixin._record_a_order_audit | 1772 | 1804 | self, zone: object, a_stop_event_time: datetime, order_match: tuple[int, object, datetime] |
| SOrderAuditMixin._audit_stopped_a | 1807 | 1817 | self, zone: object |
| SOrderAuditMixin._order_stop | 1820 | 1829 | self, order_number: int, reaction: object |
| SOrderAuditMixin._order_stop_crossed | 1832 | 1835 | self, candle: object, level: Decimal |
| SOrderAuditMixin._shared_order_stop_cross | 1838 | 1862 | self, confirmation: datetime, level: Decimal |
