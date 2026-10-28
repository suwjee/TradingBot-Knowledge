---
id: "source.state_map"
type: "source"
status: "active"
authority: "executable"
title: "Current state map"
version: "current"
related_entities: ["source.reference_registry", "source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/__init__.py", "06_SOURCE/Code/engine/bridge/__init__.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/__init__.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Current captured dataclass and state fields

This mechanical annotated-class-field map preserves physical Source names and line addresses. It is scoped navigation, not a competing public schema or semantic authority.

## trading_pipeline.py: EngineBundle

Source: 06_SOURCE/Code/engine/bridge/trading_pipeline.py#L1578.

| Field | Annotation | Line |
| --- | --- | ---: |
| reaction | object | 1579 |
| blue_line | object | 1580 |
| a_zone | object | 1581 |
| s_zone | object | 1582 |
| e_zone | object \| None | 1583 |
| lifecycle | object \| None | 1584 |
| primary | object \| None | 1585 |

## trading_pipeline.py: MarketContext

Source: 06_SOURCE/Code/engine/bridge/trading_pipeline.py#L1589.

| Field | Annotation | Line |
| --- | --- | ---: |
| seconds | list[object] | 1590 |
| candles | list[object] | 1591 |
| lower_index | object | 1592 |
| chronology | object | 1593 |
| start_index | int | 1594 |
| end_index | int | 1595 |

## trading_pipeline.py: PipelineState

Source: 06_SOURCE/Code/engine/bridge/trading_pipeline.py#L1792.

| Field | Annotation | Line |
| --- | --- | ---: |
| directions | tuple[str, ...] | 1795 |
| results | dict[str, object] | 1796 |
| reusable_full_context | bool | 1797 |
| initial_order_geometry | dict[str, object] | 1798 |
| internal_reaction_identities | dict[str, set[tuple[int, int]]] | 1799 |
| full_e_zones | dict[str, list[object]] | 1800 |
| full_e_detectors | dict[str, object] | 1801 |
| full_s_detectors | dict[str, object] | 1802 |
| full_lines_by_direction | dict[str, list[object]] | 1803 |
| full_a_by_direction | dict[str, list[object]] | 1804 |
| invalid_a_identities_by_direction | dict[str, set[tuple[datetime, int]]] | 1805 |
| invalid_s_identities_by_direction | dict[str, set[tuple[datetime, int]]] | 1806 |
| full_s_by_direction | dict[str, list[object]] | 1807 |
| full_s_candidates_by_direction | dict[str, list[object]] | 1808 |

## trading_pipeline.py: FullDirectionState

Source: 06_SOURCE/Code/engine/bridge/trading_pipeline.py#L1812.

| Field | Annotation | Line |
| --- | --- | ---: |
| e_zones | list[object] | 1815 |
| e_detector | object | 1816 |
| s_detector | object | 1817 |
| blue_lines | list[object] | 1818 |
| a_zones | list[object] | 1819 |
| invalid_a_identities | set[tuple[datetime, int]] | 1820 |
| invalid_s_identities | set[tuple[datetime, int]] | 1821 |
| s_zones | list[object] | 1822 |
| s_candidates | list[object] | 1823 |
| initial_s_zones | list[object] | 1824 |

## trading_pipeline.py: DirectionRangeState

Source: 06_SOURCE/Code/engine/bridge/trading_pipeline.py#L2409.

| Field | Annotation | Line |
| --- | --- | ---: |
| blue_lines | list[object] | 2412 |
| a_zones | list[object] | 2413 |
| s_candidates | list[object] | 2414 |
| accepted_s_zones | list[object] | 2415 |
| e_zones | list[object] | 2416 |
| invalid_a_identities | set[tuple[datetime, int]] | 2417 |
| invalid_s_identities | set[tuple[datetime, int]] | 2418 |

## trading_pipeline.py: DirectionVisibilityState

Source: 06_SOURCE/Code/engine/bridge/trading_pipeline.py#L2422.

| Field | Annotation | Line |
| --- | --- | ---: |
| blue_lines | list[object] | 2425 |
| a_zones | list[object] | 2426 |
| s_zones | list[object] | 2427 |
| e_zones | list[object] | 2428 |
| stopalls | list[object] | 2429 |
| prepared_order_audit | list[object] | 2430 |
| projection_s_zones | list[object] | 2434 |
| projection_e_zones | list[object] | 2435 |
| projection_stopalls | list[object] | 2436 |
| primary_groups | dict[str, list[object]] | 2437 |

## a_zone_detector.py: BlueState

Source: 06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L25.

| Field | Annotation | Line |
| --- | --- | ---: |
| ordinal | int | 26 |
| line | object | 27 |
| formation_index | int | 28 |
| formation_time | datetime | 29 |
| stop_index | int \| None | 30 |
| stop_time | datetime \| None | 31 |
| stop_event_time | datetime \| None | 32 |
| stop_level | Decimal | 33 |
| stop_event_extreme | Decimal \| None | 34 |

## a_zone_detector.py: AZone

Source: 06_SOURCE/Code/engine/pipeline/a_zone_detector.py#L38.

| Field | Annotation | Line |
| --- | --- | ---: |
| direction | str | 39 |
| blue_1_ordinal | int | 40 |
| blue_2_ordinal | int | 41 |
| blue_1_source_time | datetime | 42 |
| blue_2_source_time | datetime | 43 |
| blue_1_stop_time | datetime | 44 |
| blue_2_stop_time | datetime | 45 |
| blue_1_stop_level | Decimal | 46 |
| blue_2_stop_level | Decimal | 47 |
| continuation_level | Decimal | 48 |
| continuation_source_index | int | 49 |
| continuation_source_time | datetime | 50 |
| trigger_index | int | 51 |
| trigger_time | datetime | 52 |
| trigger_event_time | datetime | 53 |
| reaction_number | int | 54 |
| reaction_first_time | datetime | 55 |
| reaction_break_time | datetime | 56 |
| source_index | int | 57 |
| source_time | datetime | 58 |
| price | Decimal | 59 |
| formation_route | str \| None | 62 |
| blue_1_stop_event_time | datetime \| None | 63 |
| blue_2_stop_event_time | datetime \| None | 64 |

## blue_line_detector.py: ScaleStrike

Source: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L23.

| Field | Annotation | Line |
| --- | --- | ---: |
| source_index | int | 24 |
| source_time | datetime | 25 |
| extreme | Decimal | 26 |

## blue_line_detector.py: BlueLine

Source: 06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L30.

| Field | Annotation | Line |
| --- | --- | ---: |
| direction | str | 31 |
| kind | str | 32 |
| reaction_number | int | 33 |
| previous_strike_count | int \| None | 34 |
| strike_count | int \| None | 35 |
| fibonacci_level | Decimal \| None | 36 |
| source_index | int | 37 |
| source_time | datetime | 38 |
| source_extreme | Decimal | 39 |
| broken_level | Decimal \| None | 40 |
| line_price | Decimal | 41 |
| start_time | datetime | 42 |
| end_time | datetime | 43 |
| calculation_valid | bool | 44 |
| behavior_internal | bool | 45 |

## direction_policy.py: DirectionPolicy

Source: 06_SOURCE/Code/engine/pipeline/direction_policy.py#L21.

| Field | Annotation | Line |
| --- | --- | ---: |
| direction | Direction | 22 |
| extreme_attr | Literal['low', 'high'] | 23 |
| opposite_extreme_attr | Literal['high', 'low'] | 24 |
| first_reaction_tag | Literal['RED', 'GREEN'] | 25 |
| context_tag | Literal['GREEN', 'RED'] | 26 |

## e_zone_detector.py: EZone

Source: 06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L31.

| Field | Annotation | Line |
| --- | --- | ---: |
| direction | str | 32 |
| family | str | 33 |
| number | int | 34 |
| parent_type | str | 35 |
| parent_source_index | int | 36 |
| parent_source_time | datetime | 37 |
| parent_price | Decimal | 38 |
| parent_stop_index | int | 39 |
| parent_stop_time | datetime | 40 |
| parent_stop_event_time | datetime | 41 |
| order_direction | str | 42 |
| order_reaction_number | int | 43 |
| order_mode | str | 44 |
| order_causes | tuple[str, ...] | 45 |
| order_parent_stop_cause_time | datetime \| None | 46 |
| order_first_index | int | 47 |
| order_first_time | datetime | 48 |
| order_break_index | int | 49 |
| order_break_time | datetime | 50 |
| order_confirmation_time | datetime | 51 |
| order_box_top | Decimal | 52 |
| order_box_top_source_index | int | 53 |
| order_box_top_source_time | datetime | 54 |
| order_box_bottom | Decimal | 55 |
| order_box_bottom_source_index | int | 56 |
| order_box_bottom_source_time | datetime | 57 |
| order_stop_level | Decimal | 58 |
| order_stop_source_index | int | 59 |
| order_stop_source_time | datetime | 60 |
| source_index | int | 61 |
| source_time | datetime | 62 |
| price | Decimal | 63 |
| decision_index | int | 64 |
| decision_time | datetime | 65 |
| decision_event_time | datetime | 66 |

## lifecycle_engine.py: StopAll

Source: 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L43.

| Field | Annotation | Line |
| --- | --- | ---: |
| direction | str | 44 |
| number | int | 45 |
| source_index | int | 46 |
| source_time | datetime | 47 |
| price | Decimal | 48 |
| decision_index | int | 49 |
| decision_time | datetime | 50 |
| decision_event_time | datetime | 51 |
| gate_type | str | 52 |
| gate_event_time | datetime | 53 |
| stopped_behavior_type | str | 54 |
| stopped_behavior_key | str | 55 |
| stopped_behavior_count | int | 56 |
| underlying_e_family | str \| None | 57 |
| underlying_e_number | int \| None | 58 |
| order_direction | str \| None | 59 |
| order_reaction_number | int \| None | 60 |
| order_mode | str \| None | 61 |
| order_causes | tuple[str, ...] | 62 |
| order_parent_stop_cause_time | datetime \| None | 63 |
| order_first_index | int \| None | 64 |
| order_first_time | datetime \| None | 65 |
| order_break_index | int \| None | 66 |
| order_break_time | datetime \| None | 67 |
| order_confirmation_time | datetime \| None | 68 |
| order_box_top | Decimal \| None | 69 |
| order_box_top_source_index | int \| None | 70 |
| order_box_top_source_time | datetime \| None | 71 |
| order_box_bottom | Decimal \| None | 72 |
| order_box_bottom_source_index | int \| None | 73 |
| order_box_bottom_source_time | datetime \| None | 74 |
| order_stop_level | Decimal \| None | 75 |
| order_stop_source_index | int \| None | 76 |
| order_stop_source_time | datetime \| None | 77 |
| stop_index | int \| None | 78 |
| stop_time | datetime \| None | 79 |
| stop_event_time | datetime \| None | 80 |
| donor_type | str \| None | 85 |
| donor_source_index | int \| None | 86 |
| donor_source_time | datetime \| None | 87 |
| donor_color | str \| None | 88 |
| donor_number | int \| None | 89 |
| donor_price | Decimal \| None | 90 |
| donor_stop_time | datetime \| None | 91 |
| donor_stop_event_time | datetime \| None | 92 |

## lifecycle_engine.py: _DominantBehavior

Source: 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L96.

| Field | Annotation | Line |
| --- | --- | ---: |
| kind | str | 99 |
| family | str | 100 |
| number | int \| None | 101 |
| count | int | 102 |
| latest | object | 103 |

## order_audit_engine.py: PostBehaviorStop

Source: 06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L34.

| Field | Annotation | Line |
| --- | --- | ---: |
| behavior_type | str | 35 |
| behavior_source_index | int | 36 |
| behavior_source_time | datetime | 37 |
| event_time | datetime | 38 |

## order_audit_engine.py: OrderBBehaviorAnchor

Source: 06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L42.

| Field | Annotation | Line |
| --- | --- | ---: |
| behavior_type | str | 43 |
| behavior_source_index | int | 44 |
| behavior_source_time | datetime | 45 |
| priority | int | 46 |
| number | int | 47 |

## order_audit_engine.py: OrderBResetLeg

Source: 06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L51.

| Field | Annotation | Line |
| --- | --- | ---: |
| post_stop | PostBehaviorStop | 52 |
| anchor_behavior_type | str | 53 |
| anchor_behavior_source_index | int | 54 |
| anchor_behavior_source_time | datetime | 55 |
| anchor_behavior_extreme | Decimal | 56 |
| reset_reaction | object | 57 |
| reset_confirmation_time | datetime | 58 |
| reset_source_index | int | 59 |
| reset_broken_level | Decimal | 60 |
| reset_time | datetime | 61 |
| leg_boundary | Decimal | 62 |
| leg_source_index | int | 63 |
| leg_source_time | datetime | 64 |
| strict_break_time | datetime | 65 |
| reaction_number | int | 66 |
| physical_reaction | object | 67 |
| physical_confirmation_time | datetime | 68 |

## reaction_engine.py: Candle

Source: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L30.

| Field | Annotation | Line |
| --- | --- | ---: |
| index | int | 31 |
| timestamp | datetime | 32 |
| display_time | str | 33 |
| tag | str | 34 |
| open | Decimal | 35 |
| high | Decimal | 36 |
| low | Decimal | 37 |
| close | Decimal | 38 |

## reaction_engine.py: Candidate

Source: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L42.

| Field | Annotation | Line |
| --- | --- | ---: |
| first_idx | int | 43 |
| first_time | str | 44 |
| box_top_source_idx | int | 45 |
| box_top_source_time | str | 46 |
| box_top | Decimal | 47 |
| box_bottom_source_idx | int | 48 |
| box_bottom_source_time | str | 49 |
| box_bottom | Decimal | 50 |
| mode | str | 51 |
| anchor_idx | int \| None | 52 |
| anchor_value | Decimal \| None | 53 |
| leg_boundary_value | Decimal \| None | 54 |
| break_idx | int \| None | 55 |
| break_time | str \| None | 56 |
| intrabar_start | datetime \| None | 57 |
| cross_direction_origin | bool | 58 |
| cross_direction_chain_owner | bool | 59 |
| order_gate_decision | str \| None | 60 |
| behavior_public_number | int \| None | 61 |
| behavior_public_box_top | Decimal \| None | 62 |
| behavior_public_box_bottom | Decimal \| None | 63 |
| behavior_confirmation_time | datetime \| None | 64 |
| behavior_first_time | datetime \| None | 65 |
| behavior_internal | bool | 66 |

## reaction_engine.py: ResetEvent

Source: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L70.

| Field | Annotation | Line |
| --- | --- | ---: |
| index | int | 71 |
| display_time | str | 72 |
| second_time | str \| None | 73 |
| broken_level | Decimal | 74 |
| from_first_idx | int | 75 |

## reaction_engine.py: IntrabarAnalysis

Source: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L79.

| Field | Annotation | Line |
| --- | --- | ---: |
| event_second | Candle | 80 |
| extreme | Decimal | 81 |
| extreme_source | Candle | 82 |

## reaction_engine.py: DetectionResult

Source: 06_SOURCE/Code/engine/pipeline/reaction_engine.py#L86.

| Field | Annotation | Line |
| --- | --- | ---: |
| direction | str | 87 |
| reactions | list[Candidate] | 88 |
| resets | list[ResetEvent] | 89 |
| start_index | int | 90 |
| end_index | int | 91 |

## s_zone_detector.py: SZone

Source: 06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L28.

| Field | Annotation | Line |
| --- | --- | ---: |
| direction | str | 29 |
| color | str | 30 |
| formation_type | str | 31 |
| a_ordinal | int | 32 |
| a_source_index | int | 33 |
| a_source_time | datetime | 34 |
| a_price | Decimal | 35 |
| a_stop_index | int | 36 |
| a_stop_time | datetime | 37 |
| a_stop_event_time | datetime | 38 |
| order_direction | str \| None | 39 |
| order_reaction_number | int \| None | 40 |
| order_mode | str \| None | 41 |
| order_first_index | int \| None | 42 |
| order_first_time | datetime \| None | 43 |
| order_break_index | int \| None | 44 |
| order_break_time | datetime \| None | 45 |
| order_confirmation_time | datetime \| None | 46 |
| order_box_top | Decimal \| None | 47 |
| order_box_top_source_index | int \| None | 48 |
| order_box_top_source_time | datetime \| None | 49 |
| order_box_bottom | Decimal \| None | 50 |
| order_box_bottom_source_index | int \| None | 51 |
| order_box_bottom_source_time | datetime \| None | 52 |
| order_stop_level | Decimal \| None | 53 |
| order_stop_source_index | int \| None | 54 |
| order_stop_source_time | datetime \| None | 55 |
| reset_reaction_number | int \| None | 56 |
| reset_time | datetime \| None | 57 |
| source_index | int | 58 |
| source_time | datetime | 59 |
| price | Decimal | 60 |
| decision_index | int | 61 |
| decision_time | datetime | 62 |
| decision_event_time | datetime | 63 |
