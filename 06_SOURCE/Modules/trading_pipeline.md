---
id: "source.trading_pipeline"
type: "source"
status: "active"
authority: "executable"
title: "CLI input normalization, dynamic module loading, cross-stage coordination, OrderAudit preparation and JSON serialization"
version: "1.7.0"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/bridge/trading_pipeline.py"
mirror: "06_SOURCE/Code/engine/bridge/trading_pipeline.py"
sha256: "ef5109f4ebb95bc0e04b3d964b14da5f764ae4472f3d10a1a9b7192d59fec683"
---

# trading_pipeline.py

CLI input normalization, dynamic module loading, cross-stage coordination, OrderAudit preparation and JSON serialization.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/bridge/trading_pipeline.py |
| SHA-256 | ef5109f4ebb95bc0e04b3d964b14da5f764ae4472f3d10a1a9b7192d59fec683 |
| Bytes | 107807 |
| Lines | 2952 |
| Declared version | 1.7.0 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| emit_progress | 50 | 55 | status: str, label: str, duration_ms: float \| None=None |
| timed | 58 | 67 | timings: dict[str, float], label: str, work |
| load_module | 70 | 77 | name: str, path: Path |
| load_engine | 80 | 81 | path: Path |
| local_datetime | 87 | 93 | epoch: int |
| epoch | 99 | 105 | local: datetime |
| display_epoch | 111 | 120 | value: str \| datetime |
| build_candle_buckets | 123 | 178 | rows: list[dict], timeframe: int |
| build_candle_buckets.cached_decimal | 132 | 143 | value: object |
| build_candle_objects | 181 | 208 | engine, buckets: list[dict] |
| _index_selected | 211 | 216 | index: object, start_index: int \| None, end_index: int \| None |
| select_reaction_serialization_items | 219 | 239 | result, start_index=None, end_index=None, reaction_transform=None |
| serialize | 242 | 283 | result, start_index=None, end_index=None, reaction_transform=None, selected_items=None |
| serialize_blue_lines | 286 | 303 | items, start_index=None, end_index=None |
| serialize_a_zones | 306 | 330 | items |
| serialize_s_zones | 333 | 395 | items |
| serialize_e_zones | 398 | 438 | items |
| serialize_stopalls | 441 | 505 | items |
| bridge_datetime | 508 | 519 | value: object \| None |
| bridge_direction | 522 | 523 | direction: str |
| bridge_mode | 526 | 527 | mode: object |
| bridge_color | 530 | 533 | value: object \| None |
| _bridge_horizon | 536 | 540 | market: MarketContext |
| _bridge_in_horizon | 543 | 544 | market: MarketContext, value: datetime \| None |
| _bridge_proven_strict_event | 547 | 584 | market: MarketContext, direction: str, level: object \| None, event_time: datetime \| None |
| _bridge_stop_view | 587 | 604 | market: MarketContext, direction: str, price: object \| None, stop_time: datetime \| None, stop_event_time: datetime \| None |
| _bridge_reaction_confirmation | 607 | 628 | market: MarketContext, direction: str, reaction: object, *, use_intrabar_start: bool=True |
| _bridge_order_identity | 631 | 636 | item: object |
| BridgeProjection | 639 | 830 | class |
| BridgeProjection.__init__ | 647 | 664 | self, *, direction: str, market: MarketContext, prepared_order_audit: list[object], order_direction: str |
| BridgeProjection.physical_order | 666 | 709 | self, prepared: object \| None |
| BridgeProjection.parent_order | 711 | 716 | self, behavior: object |
| BridgeProjection.current_order | 718 | 771 | self, behavior: object, parent_type: str, parent_family: str \| None, strict_stop_event: datetime \| None |
| BridgeProjection.order_audit | 773 | 830 | self, prepared: object |
| _bridge_parent_stop | 833 | 851 | projection: BridgeProjection, detector: object \| None, parent_type: str, item: object |
| _bridge_a_stop | 854 | 872 | projection: BridgeProjection, s_detector: object \| None, item: object |
| _bridge_behavior_stop | 875 | 887 | projection: BridgeProjection, direction: str, price: object, stop_time: datetime \| None, stop_event_time: datetime \| None |
| _bridge_blue_formation | 890 | 910 | projection: BridgeProjection, direction: str, line: object, reactions: list[object] |
| _bridge_project_reaction | 913 | 953 | projection: BridgeProjection, direction: str, raw: object, public: object |
| _bridge_project_reset | 956 | 976 | projection: BridgeProjection, direction: str, reset: object |
| _bridge_project_blue | 979 | 1012 | projection: BridgeProjection, direction: str, line: object, reactions: list[object] |
| _bridge_full_lines_by_ordinal | 1015 | 1024 | lines: list[object] |
| _bridge_project_a | 1027 | 1114 | projection: BridgeProjection, direction: str, item: object, lines_by_ordinal: dict[int, object], reactions: list[object], s_detector: object \| None |
| _bridge_project_s | 1117 | 1170 | projection: BridgeProjection, direction: str, item: object, e_detector: object \| None |
| _bridge_source_index | 1173 | 1178 | item: object |
| _bridge_parent_behavior_for_e | 1181 | 1222 | projection: BridgeProjection, direction: str, item: object, s_by_source: dict[tuple[int, datetime], object], e_by_source: dict[tuple[int, datetime], object], stopall_by_source: dict[tuple[int, datetime], object] |
| _bridge_project_e | 1225 | 1269 | projection: BridgeProjection, direction: str, item: object, e_detector: object \| None, s_by_source: dict[tuple[int, datetime], object], e_by_source: dict[tuple[int, datetime], object], stopall_by_source: dict[tuple[int, datetime], object] |
| _bridge_project_stopall | 1272 | 1338 | projection: BridgeProjection, direction: str, item: object |
| _bridge_audit_order_key | 1341 | 1348 | prepared: object, detector: object |
| build_bridge_output | 1351 | 1453 | direction: str, market: MarketContext, state: PipelineState, visibility: DirectionVisibilityState, selected_reactions: list[tuple[object, object]], selected_resets: list[object], selected_blue_lines: list[object], selected_a_zones: list[object], selected_s_zones: list[object], selected_e_zones: list[object], selected_stopalls: list[object], selected_order_audit: list[object] |
| validate_order_audit_bridge | 1456 | 1521 | prepared_items, s_zones, e_zones, stopalls |
| serialize_order_audit | 1524 | 1574 | prepared_items, detector |
| EngineBundle | 1578 | 1584 | class |
| MarketContext | 1588 | 1594 | class |
| parse_arguments | 1597 | 1666 | argv=None |
| load_engines | 1669 | 1700 | args, timings: dict[str, float] |
| prepare_market_context | 1703 | 1781 | args, engines: EngineBundle, timings: dict[str, float] |
| PipelineState | 1784 | 1800 | class |
| FullDirectionState | 1804 | 1816 | class |
| create_e_detector | 1819 | 1862 | direction: str, e_engine, full_results: dict[str, object], s_zones: list[object], chronology, geometry_detectors: dict[str, object], initial_order_audit, lifecycle_engine, *, blocked_order_first_times: set[datetime] \| None=None, invalid_s_root_identities: set[tuple[datetime, int]] \| None=None, order_b_legs: Sequence[object]=() |
| create_e_detector.direct_geometry | 1837 | 1845 | geometry_direction, geometry_start, geometry_end, gate_event |
| calculate_full_direction_state | 1865 | 2172 | direction: str, engines: EngineBundle, market: MarketContext, full_results: dict[str, object], geometry_detectors: dict[str, object], initial_order_geometry: dict[str, object], timings: dict[str, float], order_b_legs: Sequence[object]=(), shared_stages: FullDirectionState \| None=None |
| calculate_direction_with_order_b_feedback | 2175 | 2227 | direction: str, engines: EngineBundle, market: MarketContext, full_results: dict[str, object], geometry_detectors: dict[str, object], initial_order_geometry: dict[str, object], timings: dict[str, float] |
| prepare_pipeline_state | 2230 | 2343 | args, engines: EngineBundle, market: MarketContext, timings: dict[str, float] |
| DirectionRangeState | 2347 | 2356 | class |
| DirectionVisibilityState | 2360 | 2374 | class |
| calculate_direction_range_state | 2377 | 2476 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, timings: dict[str, float] |
| finalize_direction_visibility | 2479 | 2692 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, direction_state: DirectionRangeState, timings: dict[str, float] |
| serialize_direction_payload | 2695 | 2833 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, visibility: DirectionVisibilityState, timings: dict[str, float] |
| serialize_direction_payload.build_legacy_payload | 2722 | 2745 |  |
| serialize_direction_payload.serialize_reactions_from_one_selection | 2754 | 2762 |  |
| serialize_direction_payload.build_payload | 2795 | 2829 |  |
| build_direction_output | 2836 | 2859 | direction: str, args, engines: EngineBundle, market: MarketContext, state: PipelineState, timings: dict[str, float] |
| build_response_payload | 2861 | 2911 | args, engines: EngineBundle, market: MarketContext, state: PipelineState, timings: dict[str, float], pipeline_started: float |
| main | 2914 | 2944 |  |
