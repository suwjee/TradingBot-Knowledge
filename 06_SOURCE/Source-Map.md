---
id: "source.source_map"
type: "source"
status: "active"
authority: "executable"
title: "Current Source navigation"
version: "current"
related_entities: ["source.reference_registry", "source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/__init__.py", "06_SOURCE/Code/engine/bridge/__init__.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/__init__.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Current Source symbol map

Current AST addresses identify exact reviewed owners. Dynamic pipeline order is in core.pipeline; symbol presence alone does not prove runtime correctness.

| Source | Symbol | Line | Signature or role |
|---|---|---:|---|
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | emit_progress | 50 | status: str, label: str, duration_ms: float \| None=None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | timed | 58 | timings: dict[str, float], label: str, work |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | load_module | 70 | name: str, path: Path |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | load_engine | 80 | path: Path |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | local_datetime | 87 | epoch: int |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | epoch | 99 | local: datetime |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | display_epoch | 111 | value: str \| datetime |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | build_candle_buckets | 123 | rows: list[dict], timeframe: int |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | build_candle_buckets.cached_decimal | 132 | value: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | build_candle_objects | 181 | engine, buckets: list[dict] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _index_selected | 211 | index: object, start_index: int \| None, end_index: int \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | select_reaction_serialization_items | 219 | result, start_index=None, end_index=None, reaction_transform=None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize | 242 | result, start_index=None, end_index=None, reaction_transform=None, selected_items=None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_blue_lines | 286 | items, start_index=None, end_index=None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_a_zones | 306 | items |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_s_zones | 333 | items |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_e_zones | 398 | items |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_stopalls | 441 | items |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | bridge_datetime | 508 | value: object \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | bridge_direction | 522 | direction: str |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | bridge_mode | 526 | mode: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | bridge_color | 530 | value: object \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_horizon | 536 | market: MarketContext |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_in_horizon | 543 | market: MarketContext, value: datetime \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_proven_strict_event | 547 | market: MarketContext, direction: str, level: object \| None, event_time: datetime \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_stop_view | 587 | market: MarketContext, direction: str, price: object \| None, stop_time: datetime \| None, stop_event_time: datetime \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_reaction_confirmation | 607 | market: MarketContext, direction: str, reaction: object, *, use_intrabar_start: bool=True |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_order_identity | 631 | item: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | BridgeProjection | 639 | class; bases:  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | BridgeProjection.__init__ | 647 | self, *, direction: str, market: MarketContext, prepared_order_audit: list[object], order_direction: str |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | BridgeProjection.physical_order | 666 | self, prepared: object \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | BridgeProjection.parent_order | 711 | self, behavior: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | BridgeProjection.current_order | 718 | self, behavior: object, parent_type: str, parent_family: str \| None, strict_stop_event: datetime \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | BridgeProjection.order_audit | 773 | self, prepared: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_parent_stop | 833 | projection: BridgeProjection, detector: object \| None, parent_type: str, item: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_a_stop | 854 | projection: BridgeProjection, s_detector: object \| None, item: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_behavior_stop | 875 | projection: BridgeProjection, direction: str, price: object, stop_time: datetime \| None, stop_event_time: datetime \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_blue_formation | 890 | projection: BridgeProjection, direction: str, line: object, reactions: list[object] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_project_reaction | 913 | projection: BridgeProjection, direction: str, raw: object, public: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_project_reset | 956 | projection: BridgeProjection, direction: str, reset: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_project_blue | 979 | projection: BridgeProjection, direction: str, line: object, reactions: list[object] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_full_lines_by_ordinal | 1015 | lines: list[object] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_project_a | 1027 | projection: BridgeProjection, direction: str, item: object, lines_by_ordinal: dict[int, object], reactions: list[object], s_detector: object \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_project_s | 1117 | projection: BridgeProjection, direction: str, item: object, e_detector: object \| None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_source_index | 1173 | item: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_parent_behavior_for_e | 1181 | projection: BridgeProjection, direction: str, item: object, s_by_source: dict[tuple[int, datetime], object], e_by_source: dict[tuple[int, datetime], object], stopall_by_source: dict[tuple[int, datetime], object] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_project_e | 1225 | projection: BridgeProjection, direction: str, item: object, e_detector: object \| None, s_by_source: dict[tuple[int, datetime], object], e_by_source: dict[tuple[int, datetime], object], stopall_by_source: dict[tuple[int, datetime], object] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_project_stopall | 1272 | projection: BridgeProjection, direction: str, item: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | _bridge_audit_order_key | 1341 | prepared: object, detector: object |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | build_bridge_output | 1351 | direction: str, market: MarketContext, state: PipelineState, visibility: DirectionVisibilityState, selected_reactions: list[tuple[object, object]], selected_resets: list[object], selected_blue_lines: list[object], selected_a_zones: list[object], selected_s_zones: list[object], selected_e_zones: list[object], selected_stopalls: list[object], selected_order_audit: list[object] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | validate_order_audit_bridge | 1456 | prepared_items, s_zones, e_zones, stopalls |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_order_audit | 1524 | prepared_items, detector |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | EngineBundle | 1578 | class; bases:  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | MarketContext | 1588 | class; bases:  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | parse_arguments | 1597 | argv=None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | load_engines | 1669 | args, timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | prepare_market_context | 1703 | args, engines: EngineBundle, timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | PipelineState | 1784 | class; bases:  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | FullDirectionState | 1804 | class; bases:  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | create_e_detector | 1819 | direction: str, e_engine, full_results: dict[str, object], s_zones: list[object], chronology, geometry_detectors: dict[str, object], initial_order_audit, lifecycle_engine, *, blocked_order_first_times: set[datetime] \| None=None, invalid_s_root_identities: set[tuple[datetime, int]] \| None=None, order_b_legs: Sequence[object]=() |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | create_e_detector.direct_geometry | 1837 | geometry_direction, geometry_start, geometry_end, gate_event |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | calculate_full_direction_state | 1865 | direction: str, engines: EngineBundle, market: MarketContext, full_results: dict[str, object], geometry_detectors: dict[str, object], initial_order_geometry: dict[str, object], timings: dict[str, float], order_b_legs: Sequence[object]=(), shared_stages: FullDirectionState \| None=None |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | calculate_direction_with_order_b_feedback | 2175 | direction: str, engines: EngineBundle, market: MarketContext, full_results: dict[str, object], geometry_detectors: dict[str, object], initial_order_geometry: dict[str, object], timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | prepare_pipeline_state | 2230 | args, engines: EngineBundle, market: MarketContext, timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | DirectionRangeState | 2347 | class; bases:  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | DirectionVisibilityState | 2360 | class; bases:  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | calculate_direction_range_state | 2377 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | finalize_direction_visibility | 2479 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, direction_state: DirectionRangeState, timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_direction_payload | 2695 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, visibility: DirectionVisibilityState, timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_direction_payload.serialize_reactions_from_one_selection | 2754 |  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | serialize_direction_payload.build_payload | 2795 |  |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | build_direction_output | 2836 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, timings: dict[str, float] |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | build_response_payload | 2861 | args, engines: EngineBundle, market: MarketContext, state: PipelineState, timings: dict[str, float], pipeline_started: float |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | main | 2914 |  |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | BlueState | 25 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZone | 38 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector | 67 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector.__init__ | 68 | self, direction: str, reactions: Sequence[object], blue_lines: Sequence[object], chronology: object |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector.extreme_name | 97 | self |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._strict_cross | 100 | self, value: Decimal, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._better | 103 | self, value: Decimal, current: Decimal |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._main_index | 106 | self, timestamp: datetime |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._lower_window | 109 | self, start: datetime, end: datetime \| None |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._first_crossing | 114 | self, level: Decimal, start: datetime, end: datetime \| None |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._range_extreme | 156 | self, start: datetime, end: datetime |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._formation | 190 | self, line: object |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._reset_formation_time | 207 | self, line: object, source_index: int |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._build_blue_states | 219 | self |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._double_stop_a_candidates | 248 | self |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._pair_trigger | 311 | self, previous: BlueState, current: BlueState, expires_at: datetime \| None |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._reaction_confirmation_time | 471 | self, reaction: object |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._first_reaction_after | 476 | self, trigger_event_time: datetime, *, not_before: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._inherited_stop | 494 | self, previous: BlueState, current: BlueState |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._a_source | 547 | self, trigger_index: int, reaction: object |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._detect_ordinary_a | 568 | self, states: list[BlueState] |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._filter_special_a | 689 | self, special: list[AZone], ordinary: list[AZone] |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector.detect | 753 | self |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | AZoneDetector._a_was_stopped_before | 765 | self, zone: AZone, end_time: datetime, *, not_before: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | detect_a_zones | 791 | direction: str, reactions: Sequence[object], blue_lines: Sequence[object], chronology: object |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | ScaleStrike | 23 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | BlueLine | 30 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | _is_color | 48 | candle: object, color: str |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | _main_candle | 52 | candles_by_index: dict[int, object], index: int |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | _stops_on_index | 59 | direction: str, line: object, candles: Sequence[object], start_index: int, end_index: int |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | fibonacci_level | 75 | direction: str, reaction: object, reference: Decimal |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | _intrabar_pending_confirmation | 84 | direction: str, chronology: object, reaction: object, comparison_extreme: Decimal, start_time: datetime, break_time: datetime, candles_by_index: dict[int, object] |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | count_scale_strikes | 139 | direction: str, reaction: object, chronology: object, reference: Decimal, candles_by_index: dict[int, object] \| None=None |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | _build_scale_blue_line | 207 | direction: str, reaction_number: int, previous_count: int, level: Decimal, strikes: Sequence[ScaleStrike], candles_by_index: dict[int, object], chronology: object, behavior_internal: bool |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | _build_reset_blue_line | 245 | direction: str, reaction_number: int, reset: object, previous_line: BlueLine \| None, candles: Sequence[object], candles_by_index: dict[int, object], chronology: object, behavior_internal: bool |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | detect_blue_lines | 299 | direction: str, reactions: Sequence[object], chronology: object, resets: Sequence[object]=() |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | public_blue_lines | 407 | lines: Sequence[BlueLine] |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | mark_internal_blue_lines | 416 | lines: Sequence[BlueLine], owner_reactions: Sequence[object], all_behavior_reactions: Sequence[object] |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | mark_internal_blue_lines.owner_is_internal | 429 | line: BlueLine |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | mark_internal_blue_lines.geometry_is_internal | 435 | line: BlueLine |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | as_decimal | 11 | value: object |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | order_identity | 19 | first_index: object, break_index: object |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | reaction_identity | 24 | reaction: object |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | DirectionPolicy | 21 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | DirectionPolicy.opposite_direction | 29 | self |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | DirectionPolicy.strict_cross | 32 | self, value: Decimal, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | DirectionPolicy.better_extreme | 35 | self, value: Decimal, current: Decimal |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | DirectionPolicy.choose_extreme | 38 | self, left: Decimal, right: Decimal |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | DirectionPolicy.confirmation_cross | 41 | self, value: Decimal, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | policy_for | 49 | direction: str |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZone | 31 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector | 69 | class; bases: OrderAuditEngineMixin |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.__init__ | 70 | self, direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], s_zones: Sequence[object], opposite_resets: Sequence[object], chronology: object, start_index: int=0, end_index: int \| None=None, direct_geometry_finder: Callable[[str, int, int, datetime], object \| None] \| None=None, blocked_order_first_times: set[datetime] \| None=None, initial_order_audit: dict[tuple[int, int], dict[str, object]] \| None=None, sequence_resets: dict[datetime, int] \| None=None, sequence_priority: Callable[[str, str], int] \| None=None, invalid_s_root_identities: set[tuple[datetime, int]] \| None=None, order_b_legs: Sequence[OrderBResetLeg]=() |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.sequence_resets | 213 | self |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.sequence_resets | 217 | self, resets: dict[datetime, int] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._reset_time | 226 | self, reset: object |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._main_index | 229 | self, value: datetime |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._first_cross_position | 233 | self, left: int, right: int, level: Decimal, *, less: bool |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._stop_value | 250 | self, item: object |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._first_parent_stop | 254 | self, source_time: datetime, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._confirmation_for | 267 | self, reaction: object, direction: str |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._confirmation | 270 | self, reaction: object |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._reaction_first_time | 273 | self, reaction: object |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._parent_stop | 277 | self, parent_type: str, parent: object |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.parent_stop | 285 | self, parent_type: str, parent: object |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._extreme_between | 292 | self, start: datetime, end: datetime |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._zone | 308 | self, family: str, number: int, parent_type: str, parent: object, stop_event: datetime |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.set_consumed_s_evidence | 410 | self, evidence: Sequence[tuple[object, object]] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._apply_consumed_s_evidence | 422 | self, zones: Sequence[EZone] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.continuation_chain_from_s | 440 | self, owner: EZone, s_zone: object |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.replace_with_earlier_continuation | 479 | self, base_zones: Sequence[EZone], owner: EZone, continuation: Sequence[EZone] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.replace_with_earlier_continuation.descends_from_owner | 488 | item: EZone |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.resolve_same_source_conflicts | 522 | self, zones: Sequence[EZone] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.resolve_same_source_conflicts.outranks | 540 | candidate: EZone, current: EZone |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.restore_independent_s_roots | 566 | self, dominant_zones: Sequence[EZone] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._discover_candidate_chains | 626 | self |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._reconcile_candidate_chains | 718 | self, candidates: list[EZone] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._reconcile_candidate_chains.valid_order | 749 | zone: EZone |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._reconcile_candidate_chains.parent_active | 752 | zone: EZone, seen: set[tuple[int, datetime]] \| None=None |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._reconcile_candidate_chains.stopped_by | 824 | zone: EZone, prior: EZone |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector._reconcile_candidate_chains.collect_lineage | 966 | zone: EZone, seen: set[tuple[int, datetime]] |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | EZoneDetector.detect | 991 | self |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | detect_e_zones | 1004 | direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], s_zones: Sequence[object], opposite_resets: Sequence[object], chronology: object, start_index: int=0, end_index: int \| None=None, direct_geometry_finder: Callable[[str, int, int, datetime], object \| None] \| None=None, blocked_order_first_times: set[datetime] \| None=None, initial_order_audit: dict[tuple[int, int], dict[str, object]] \| None=None, sequence_priority: Callable[[str, str], int] \| None=None, invalid_s_root_identities: set[tuple[datetime, int]] \| None=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | sequence_priority | 37 | kind: str, family: str |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAll | 43 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector | 95 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector.__init__ | 96 | self, direction: str, s_zones: Sequence[object], e_zones: Sequence[object], chronology: object |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._strict_stop | 117 | self, start: datetime, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._e_key | 134 | item: object |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._dominates_e | 138 | new: tuple[str, int], old: tuple[str, int] |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._sequence_priority | 148 | cls, kind: str, family: str |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._active_sequence_priority | 152 | cls, s_key: str \| None, e_key: tuple[str, int] \| None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._stopall_from_e | 161 | self, item: object, number: int, gate_type: str, gate_event: datetime, behavior_type: str, behavior_key: str, behavior_count: int |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._optional_int | 220 | value: object \| None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._optional_decimal | 224 | value: object \| None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._stopall_from_s | 227 | self, item: object, behavior_type: str, behavior_key: str, behavior_count: int, underlying_e_key: tuple[str, int] \| None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._blue_repeat_key | 325 | kind: str, number: int \| None=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._record_blue_repeat | 341 | counts: dict[tuple[str, int \| None], int], latest: dict[tuple[str, int \| None], object], key: tuple[str, int \| None], item: object |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector._opposite_s_stopall_gate | 350 | self, s_item: object, blue_repeat_counts: dict[tuple[str, int \| None], int], blue_repeat_latest: dict[tuple[str, int \| None], object] |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector.detect | 397 | self |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector.detect.reset_cycle_blue_repeats | 413 |  |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | StopAllDetector.detect.process_s_event | 417 | s_item: object |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | detect_stopalls | 603 | direction: str, s_zones: Sequence[object], e_zones: Sequence[object], chronology: object |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | resolve_order_context | 616 | order_audit: dict, accepted_a_sources: set[datetime], inherited_blocked_first_times: set[datetime], invalid_a_zones: Sequence[object], pending_s_a_sources: set[datetime], opposite_reactions: Sequence[object], candles: Sequence[object], direction: str, stop_finder |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | visible_a_zones_after_s_stops | 668 | a_zones, s_zones, candles |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | module_priority | 684 | item: object |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | module_identity | 698 | item: object |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | module_stop_event | 707 | item: object, stop_event_finder=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | strictly_beyond_boundary | 721 | price: Decimal, boundary: Decimal, direction: str |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | dominant_module | 726 | modules: Sequence[object] |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | split_a_zones_by_dominant_stops | 738 | a_zones, s_zones, e_zones, stopalls, candles, direction, stop_event_finder=None, trend_reactions=None, confirmation_finder=None, a_stop_event_finder=None, stage_invalid_a_identities=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | blocked_orders_while_invalid_leg_heads_are_live | 941 | invalid_a_zones, opposite_reactions, candles, direction, stop_finder |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | consumed_s_evidence_after_larger_stop | 964 | s_candidates, accepted_s_zones, e_zones, direction, stop_event_finder, candles |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | s_zones_for_module_engines | 1106 | s_zones, e_zones, direction |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | s_zones_for_stopall | 1136 | s_zones, e_zones, direction |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | visible_s_zones_after_module_resets | 1155 | s_zones, e_zones, direction, stop_event_finder=None, source_event_finder=None, candles=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | reconcile_stopall_lifecycle | 1324 | detector, s_zones, e_zones, chronology, direction, timed_step=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | visible_a_zones_after_module_boundaries | 1357 | a_zones, s_zones, e_zones, direction, stop_event_finder=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | reaction_number_is_internal | 1404 | items, number, identities |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | point_is_inside_healthy_reaction | 1418 | source_time, price, reactions |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | filter_internal_behavior_outputs | 1441 | a_zones, s_zones, e_zones, stopalls, opposite_reactions, opposite_internal_identities, all_behavior_reactions |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | finalize_behavior_visibility | 1454 | a_zones, s_zones, e_zones, stopalls, direction, invalid_s_identities, stop_event_finder, source_event_finder, candles, *, all_a_zones=None |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | visible_a_zones | 1549 | a_zones: Sequence[object], s_zones: Sequence[object] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | PostBehaviorStop | 18 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderBBehaviorAnchor | 26 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderBResetLeg | 35 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | dominant_post_behavior_stops | 55 | chronology: object, lifetimes: Sequence[tuple[str, object, datetime \| None]], priority: Callable[[object], int] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | order_b_reset_event_time | 101 | direction: str, chronology: object, reset: object |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | discover_order_b_reset_legs | 132 | direction: str, chronology: object, trend_reactions: Sequence[object], resets: Sequence[object], opposite_reactions: Sequence[object], post_stops: Sequence[PostBehaviorStop], a_formation_times: Sequence[datetime], *, behavior_anchors: Sequence[OrderBBehaviorAnchor]=() |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | discover_accepted_order_b_reset_legs | 328 | direction: str, chronology: object, trend_reactions: Sequence[object], trend_resets: Sequence[object], opposite_reactions: Sequence[object], a_zones: Sequence[object], invalid_a_identities: set[tuple[datetime, int]], s_zones: Sequence[object], e_zones: Sequence[object], stopalls: Sequence[object], s_detector: object, e_detector: object, priority: Callable[[object], int] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | order_b_leg_identity | 413 | items: Sequence[object] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin | 437 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._order_stop | 440 | self, number: int, reaction: object, context_start: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin.order_stop | 469 | self, reaction_number: int, reaction: object |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._first_healthy_direct_geometry | 476 | self, start: datetime, allow_bounded_continue: bool=False |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._trend_leg_direct_order | 551 | self, start: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._direct_parent_stop_order | 603 | self, start: datetime, continuous_deadline: datetime \| None, allow_bounded_continue: bool |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._merge_order_candidate | 677 | self, by_geometry: dict[tuple[int, int], OrderMatch], number: int, reaction: object, confirmation: datetime, *, parent_stop_cause_time: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._enforce_single_parent_stop_owner | 711 | self, by_geometry: dict[tuple[int, int], OrderMatch] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin.order_candidates | 738 | self, start: datetime, continuous_deadline: datetime \| None=None, allow_bounded_continue: bool=False, allow_trend_leg_continue: bool=False |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._first_order | 827 | self, start: datetime, continuous_deadline: datetime \| None=None, allow_bounded_continue: bool=False, allow_trend_leg_continue: bool=False |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._has_sequence_reset_between | 843 | self, start: datetime, end: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._index_order_audit_identity | 854 | self, identity: tuple[int, int], confirmation: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._clear_order_audit | 864 | self |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin.register_order_b_reset_legs | 870 | self, legs: Sequence[OrderBResetLeg] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._register_order_audit | 936 | self, parent_type: str, parent: object, parent_stop: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin.visual_order_lifecycle | 1003 | self, start: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._cross_order | 1025 | self, start: datetime, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin.cross_order | 1046 | self, confirmation_time: datetime, stop_level: Decimal |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._unconsumed_s_orders | 1053 | self, parent: object, parent_stop: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._initial_order_records | 1090 | self |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._initial_record_match | 1150 | record: tuple[datetime, datetime, int, object, Decimal, int, datetime, tuple[int, datetime, datetime] \| None], causes: tuple[str, ...] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._initial_order_match | 1164 | self, entry: dict[str, object], causes: tuple[str, ...] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._gate_owned_initial_order | 1179 | self, parent_stop: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._carried_orders_for_parent | 1202 | self, parent: object, parent_stop: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._post_stop_accepted_orders_for_parent | 1263 | self, parent: object, parent_stop: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._post_stop_accepted_orders_for_parent.add_match | 1270 | match: OrderMatch |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._blocked_by_gate_owned_order | 1332 | self, zone: EZone |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._rebuild_accepted_order_audit | 1343 | self, numbered: list[EZone], supplemental_s_zones: Sequence[object]=() |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin._rebuild_accepted_order_audit.valid_parent_stop_cause | 1354 | cause: tuple[object, ...] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin.rebuild_accepted_order_audit | 1527 | self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object]=() |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | OrderAuditEngineMixin.ensure_accepted_order_audit | 1542 | self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object]=() |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | prepare_order_audit | 1566 | detector, start_index: int, end_index: int, s_detector=None, accepted_a_sources: set[datetime] \| None=None, required_identities: set[tuple[int, int]] \| None=None |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | accepted_audit_entry | 1695 | entry: dict[str, object], accepted_sources: set |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | order_identity_is_internal | 1725 | item, internal_identities |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin | 1734 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin._first_order_after | 1737 | self, a_stop_event_time: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin._order_matches_after | 1750 | self, a_stop_event_time: datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin._record_a_order_audit | 1772 | self, zone: object, a_stop_event_time: datetime, order_match: tuple[int, object, datetime] |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin._audit_stopped_a | 1807 | self, zone: object |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin._order_stop | 1820 | self, order_number: int, reaction: object |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin._order_stop_crossed | 1832 | self, candle: object, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | SOrderAuditMixin._shared_order_stop_cross | 1838 | self, confirmation: datetime, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | Candle | 27 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | Candidate | 39 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | ResetEvent | 67 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | IntrabarAnalysis | 76 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectionResult | 83 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | classify_candle_color | 91 | open_price: Decimal, close_price: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | opposite_direction | 96 | direction: str |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectorBase | 101 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectorBase.__init__ | 102 | self, candles: Sequence[Candle], one_second_candles: Sequence[Candle], start_index: int, end_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectorBase._shared_time_index | 127 | candles: Sequence[Candle] |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectorBase.seconds_between | 137 | self, start: datetime, end: datetime |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectorBase.main_source_for_time | 142 | self, timestamp: datetime |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectorBase.minimum_low | 155 | self, start_index: int, end_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | DetectorBase.maximum_high | 164 | self, start_index: int, end_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BullishDetector | 174 | class; bases: DetectorBase |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BullishDetector.green_run_peak_before | 175 | self, first_red_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BullishDetector.breakout_analysis | 185 | self, candidate: Candidate, breakout_candle: Candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BullishDetector.mode_a_invalidation_before_breakout | 211 | self, candidate: Candidate, candle: Candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BullishDetector.confirmed_reset_before_breakout | 247 | self, candidate: Candidate \| None, candle: Candle, confirmed_bottom: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BullishDetector.post_breakout_reset | 267 | self, analysis: IntrabarAnalysis \| None, box_bottom: Decimal, breakout_candle: Candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BullishDetector.detect | 282 | self, *, first_only: bool=False |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | mirror_candle | 560 | candle: Candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | mirror_candidate | 580 | candidate: Candidate \| None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | mirror_analysis | 599 | analysis: IntrabarAnalysis \| None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | _ReflectedCandles | 608 | class; bases: Sequence[Candle] |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | _ReflectedCandles.__init__ | 616 | self, source: Sequence[Candle] |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | _ReflectedCandles.__len__ | 620 | self |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | _ReflectedCandles.__getitem__ | 623 | self, index |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | _reflected_view | 636 | source: Sequence[Candle] |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector | 646 | class; bases: DetectorBase |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector.__init__ | 654 | self, candles, one_second_candles, start_index, end_index |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector.red_run_bottom_before | 668 | self, first_green_index |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector.breakdown_analysis | 672 | self, candidate, breakdown_candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector.invalidation_high_break_before_breakdown | 677 | self, candidate, candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector.confirmed_reset_before_breakdown | 682 | self, candidate, candle, confirmed_top |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector.post_breakdown_reset | 688 | self, analysis, box_top, breakdown_candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | BearishDetector.detect | 695 | self, *, first_only: bool=False |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | published_reaction_candidate | 706 | direction: str, candidate: Candidate, chronology: object |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | _decimal_value | 804 | value: object |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex | 809 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex.__init__ | 816 | self, candles: Sequence[Candle] |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex.first_less | 857 | self, left: int, right: int, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex.first_greater | 860 | self, left: int, right: int, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex.range_minimum | 863 | self, left: int, right: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex.range_maximum | 867 | self, left: int, right: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex._range_query | 871 | self, left: int, right: int, *, minimum: bool |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | LowerTimeframeIndex._first | 909 | self, node: int, start: int, end: int, left: int, right: int, level: Decimal, less: bool |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | shared_lower_timeframe_index | 934 | candles: Sequence[Candle] |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | ReflectedLowerTimeframeIndex | 947 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | ReflectedLowerTimeframeIndex.__init__ | 952 | self, base: LowerTimeframeIndex |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | ReflectedLowerTimeframeIndex.first_less | 956 | self, left: int, right: int, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | ReflectedLowerTimeframeIndex.first_greater | 959 | self, left: int, right: int, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | ReflectedLowerTimeframeIndex.range_minimum | 962 | self, left: int, right: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | ReflectedLowerTimeframeIndex.range_maximum | 966 | self, left: int, right: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology | 971 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.__init__ | 990 | self, candles: Sequence[Candle], seconds: Sequence[Candle], timeframe_seconds: int, lower_index: LowerTimeframeIndex \| None=None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.opposite_direction | 1013 | direction: str |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.main_index | 1017 | self, timestamp: datetime, *, clamp: bool=False |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.lower_bounds | 1026 | self, start: datetime, end: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.lower_window | 1037 | self, start: datetime, end: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology._reset_cache_key | 1044 | reset: object |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology._reaction_cache_key | 1056 | reaction: object, direction: str, use_intrabar_start: bool |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.reset_time | 1070 | self, reset: object |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.reaction_confirmation | 1089 | self, direction: str, reaction: object, *, use_intrabar_start: bool=True |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | MarketChronology.canonical_order_stop | 1137 | self, order_direction: str, reaction_number: int, reaction: object, opposite_reactions: Sequence[object], *, start_index: int=0 |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | build_behavior_reaction_views | 1202 | full_results: dict[str, object], chronology: MarketChronology |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | build_behavior_reaction_views.path_is_contained | 1222 | first_time: datetime, confirmed_at: datetime, bottom: Decimal, top: Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | directional_a_stop_order_finder | 1313 | candles: Sequence[Candle], seconds: Sequence[Candle], direction: str |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | directional_a_stop_order_finder.find | 1327 | gate_index: int, gate_event: datetime, end_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector | 1376 | class; bases: DetectorBase |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector.__init__ | 1386 | self, candles: Sequence[Candle], one_second_candles: Sequence[Candle], start_index: int, end_index: int, output_direction: str |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector.bull | 1411 | self |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector.bear | 1419 | self |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._append_reaction | 1426 | self, direction: str, candidate: Candidate |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._append_reset | 1508 | self, direction: str, candle: Candle, level: Decimal, first_idx: int, second_time: str \| None=None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._refine | 1526 | self, direction: str, candidate: Candidate, candle: Candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._candidate_from_confirmation_remainder | 1547 | self, direction: str, confirmed: Candidate, candle: Candle, analysis: IntrabarAnalysis \| None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._first_initial | 1632 | self, direction: str |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._first_direct_same_direction_after_reset | 1645 | self, direction: str, reset_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._first_geometry_after_reset | 1683 | self, direction: str, reset_index: int, end_index: int \| None=None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector.first_geometry_after_reset | 1736 | self, direction: str, reset_index: int, end_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._reaction_break_indices | 1743 | self, direction: str |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector.first_order_reaction_after_gate | 1758 | self, direction: str, gate_index: int, end_index: int \| None=None, gate_event_time: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector.first_order_reaction_after_gate.confirmed_no_later_than_gate | 1770 | reaction: Candidate |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._earliest_confirmed_geometry | 1892 | self, direction: str, start_index: int, end_index: int \| None=None |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._build_direct_candidate | 1966 | self, direction: str, reset_index: int, first_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._scan_direct_candidate | 2024 | self, direction: str, candidate: Candidate, stop_index: int |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._owner_boundary_before_confirmation | 2054 | self, direction: str, candidate: Candidate, candle: Candle |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector._result | 2095 | self |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | UnifiedReactionDetector.detect | 2104 | self, *, stop_after_first_at_or_after: int \| None=None |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZone | 28 | class; bases:  |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector | 66 | class; bases: SOrderAuditMixin |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector.__init__ | 67 | self, direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], trend_blue_lines: Sequence[object], a_zones: Sequence[object], chronology: object, start_index: int \| None=None, end_index: int \| None=None, opposite_resets: Sequence[object]=(), initial_order_geometry: Callable[[int, datetime, int], object \| None] \| None=None |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._main_index | 194 | self, timestamp: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._lower_window | 197 | self, start: datetime, end: datetime \| None |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._reaction_confirmation_time | 202 | self, reaction: object, direction: str |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector.reaction_confirmation_time | 207 | self, reaction: object, direction: str |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._reset_time | 214 | self, reset: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._a_confirmation_time | 217 | self, zone: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._trend_extreme | 225 | self, candle: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._a_stopped | 230 | self, value: Decimal, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._first_a_stop | 233 | self, level: Decimal, start: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector.first_a_stop | 269 | self, level: Decimal, start: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._resolved_order_backed_zone | 276 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], first_order_match: tuple[int, object, datetime] |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_source | 295 | self, start_index: int, end_index: int |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_source_last | 310 | self, start_index: int, end_index: int |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._first_trend_reaction_after_order | 330 | self, order_confirmation_time: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._nested_trend_reaction | 342 | self, order: object, order_confirmation_time: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._simple_candidate | 372 | self, order: object, reaction: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._type3_reset_leg | 381 | self, reset: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._type3_has_trend_reaction | 397 | self, a_stop_event: datetime, crossing: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._first_type3 | 406 | self, a_stop_event: datetime, deadline: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._type4_has_blue | 456 | self, candidate_source_index: int, crossing_event: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._first_type4 | 467 | self, a_stop: tuple[int, datetime, datetime], deadline: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._build_type4_zone | 537 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], type4: tuple[int, datetime, Decimal, int, datetime, int, datetime] |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_after_order | 590 | self, order_confirmation_time: datetime, reaction: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._a_source_event_time | 631 | self, zone: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._a_owned_by_s | 640 | self, zone: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._a_pair_is_reset_reset | 681 | self, zone: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector.eligible_a_zones | 695 | self |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_timing | 699 | self, a_stop_index: int, order: object, order_confirmation_time: datetime, a_stop_event_time: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_before_order | 744 | self, a_stop_index: int, order: object, a_stop_event_time: datetime \| None=None |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_event_time | 788 | self, source_index: int, level: Decimal, not_before: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector.candidate_event_time | 803 | self, source_index: int, price: Decimal, fallback: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._blue_formation_time | 810 | self, line: object |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_cross_has_blue | 840 | self, reaction_number: int, event_time: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._has_ordinary_trend_reaction | 857 | self, behavior_start: datetime, event_time: datetime |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._candidate_crossed | 868 | self, candle: object, level: Decimal |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._decision | 873 | self, candidate_level: Decimal, order_stop_level: Decimal, start: datetime, trend_reaction_number: int, behavior_start: datetime, candidate_start: datetime \| None=None, fallback_on_unqualified_cross: bool=False |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._build_type3_zone | 999 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], type3: tuple[int, datetime, Decimal, int, datetime, int, datetime, datetime] |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector._build_order_backed_zone | 1057 | self, zone: object, a_ordinal: int, a_price: Decimal, a_stop: tuple[int, datetime, datetime], order_match: tuple[int, object, datetime] |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector.detect | 1228 | self |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | SZoneDetector.reconcile_shared_order_stops | 1305 | self, zones: Sequence[SZone], order_entries: Sequence[dict[str, object]] |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | detect_s_zones | 1421 | direction: str, trend_reactions: Sequence[object], opposite_reactions: Sequence[object], trend_blue_lines: Sequence[object], a_zones: Sequence[object], chronology: object, start_index: int \| None=None, end_index: int \| None=None, opposite_resets: Sequence[object]=(), initial_order_geometry: Callable[[int, datetime, int], object \| None] \| None=None |
