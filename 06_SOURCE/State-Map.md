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
---

# Current Source state map

All directly annotated class fields are extracted from exact current Source. Internal caches, accepted state and public serialization are distinct; see owning algorithm notes.

## trading_pipeline.py: BridgeProjection

Source line: 639.

No directly annotated class fields; methods are recorded in the module Source note.

## trading_pipeline.py: EngineBundle

Source line: 1578.

| Field | Type | Default | Line |
|---|---|---|---:|
| reaction | object | none | 1579 |
| blue_line | object | none | 1580 |
| a_zone | object | none | 1581 |
| s_zone | object | none | 1582 |
| e_zone | object \| None | none | 1583 |
| lifecycle | object \| None | none | 1584 |

## trading_pipeline.py: MarketContext

Source line: 1588.

| Field | Type | Default | Line |
|---|---|---|---:|
| seconds | list[object] | none | 1589 |
| candles | list[object] | none | 1590 |
| lower_index | object | none | 1591 |
| chronology | object | none | 1592 |
| start_index | int | none | 1593 |
| end_index | int | none | 1594 |

## trading_pipeline.py: PipelineState

Source line: 1784.

| Field | Type | Default | Line |
|---|---|---|---:|
| directions | tuple[str, ...] | none | 1787 |
| results | dict[str, object] | none | 1788 |
| reusable_full_context | bool | none | 1789 |
| initial_order_geometry | dict[str, object] | none | 1790 |
| internal_reaction_identities | dict[str, set[tuple[int, int]]] | none | 1791 |
| full_e_zones | dict[str, list[object]] | none | 1792 |
| full_e_detectors | dict[str, object] | none | 1793 |
| full_s_detectors | dict[str, object] | none | 1794 |
| full_lines_by_direction | dict[str, list[object]] | none | 1795 |
| full_a_by_direction | dict[str, list[object]] | none | 1796 |
| invalid_a_identities_by_direction | dict[str, set[tuple[datetime, int]]] | none | 1797 |
| invalid_s_identities_by_direction | dict[str, set[tuple[datetime, int]]] | none | 1798 |
| full_s_by_direction | dict[str, list[object]] | none | 1799 |
| full_s_candidates_by_direction | dict[str, list[object]] | none | 1800 |

## trading_pipeline.py: FullDirectionState

Source line: 1804.

| Field | Type | Default | Line |
|---|---|---|---:|
| e_zones | list[object] | none | 1807 |
| e_detector | object | none | 1808 |
| s_detector | object | none | 1809 |
| blue_lines | list[object] | none | 1810 |
| a_zones | list[object] | none | 1811 |
| invalid_a_identities | set[tuple[datetime, int]] | none | 1812 |
| invalid_s_identities | set[tuple[datetime, int]] | none | 1813 |
| s_zones | list[object] | none | 1814 |
| s_candidates | list[object] | none | 1815 |
| initial_s_zones | list[object] | none | 1816 |

## trading_pipeline.py: DirectionRangeState

Source line: 2347.

| Field | Type | Default | Line |
|---|---|---|---:|
| blue_lines | list[object] | none | 2350 |
| a_zones | list[object] | none | 2351 |
| s_candidates | list[object] | none | 2352 |
| accepted_s_zones | list[object] | none | 2353 |
| e_zones | list[object] | none | 2354 |
| invalid_a_identities | set[tuple[datetime, int]] | none | 2355 |
| invalid_s_identities | set[tuple[datetime, int]] | none | 2356 |

## trading_pipeline.py: DirectionVisibilityState

Source line: 2360.

| Field | Type | Default | Line |
|---|---|---|---:|
| blue_lines | list[object] | none | 2363 |
| a_zones | list[object] | none | 2364 |
| s_zones | list[object] | none | 2365 |
| e_zones | list[object] | none | 2366 |
| stopalls | list[object] | none | 2367 |
| prepared_order_audit | list[object] | none | 2368 |
| projection_s_zones | list[object] | none | 2372 |
| projection_e_zones | list[object] | none | 2373 |
| projection_stopalls | list[object] | none | 2374 |

## a_zone_detector.py: BlueState

Source line: 25.

| Field | Type | Default | Line |
|---|---|---|---:|
| ordinal | int | none | 26 |
| line | object | none | 27 |
| formation_index | int | none | 28 |
| formation_time | datetime | none | 29 |
| stop_index | int \| None | none | 30 |
| stop_time | datetime \| None | none | 31 |
| stop_event_time | datetime \| None | none | 32 |
| stop_level | Decimal | none | 33 |
| stop_event_extreme | Decimal \| None | none | 34 |

## a_zone_detector.py: AZone

Source line: 38.

| Field | Type | Default | Line |
|---|---|---|---:|
| direction | str | none | 39 |
| blue_1_ordinal | int | none | 40 |
| blue_2_ordinal | int | none | 41 |
| blue_1_source_time | datetime | none | 42 |
| blue_2_source_time | datetime | none | 43 |
| blue_1_stop_time | datetime | none | 44 |
| blue_2_stop_time | datetime | none | 45 |
| blue_1_stop_level | Decimal | none | 46 |
| blue_2_stop_level | Decimal | none | 47 |
| continuation_level | Decimal | none | 48 |
| continuation_source_index | int | none | 49 |
| continuation_source_time | datetime | none | 50 |
| trigger_index | int | none | 51 |
| trigger_time | datetime | none | 52 |
| trigger_event_time | datetime | none | 53 |
| reaction_number | int | none | 54 |
| reaction_first_time | datetime | none | 55 |
| reaction_break_time | datetime | none | 56 |
| source_index | int | none | 57 |
| source_time | datetime | none | 58 |
| price | Decimal | none | 59 |
| formation_route | str \| None | field(default=None, kw_only=True) | 62 |
| blue_1_stop_event_time | datetime \| None | field(default=None, kw_only=True) | 63 |
| blue_2_stop_event_time | datetime \| None | field(default=None, kw_only=True) | 64 |

## a_zone_detector.py: AZoneDetector

Source line: 67.

No directly annotated class fields; methods are recorded in the module Source note.

## blue_line_detector.py: ScaleStrike

Source line: 23.

| Field | Type | Default | Line |
|---|---|---|---:|
| source_index | int | none | 24 |
| source_time | datetime | none | 25 |
| extreme | Decimal | none | 26 |

## blue_line_detector.py: BlueLine

Source line: 30.

| Field | Type | Default | Line |
|---|---|---|---:|
| direction | str | none | 31 |
| kind | str | none | 32 |
| reaction_number | int | none | 33 |
| previous_strike_count | int \| None | none | 34 |
| strike_count | int \| None | none | 35 |
| fibonacci_level | Decimal \| None | none | 36 |
| source_index | int | none | 37 |
| source_time | datetime | none | 38 |
| source_extreme | Decimal | none | 39 |
| broken_level | Decimal \| None | none | 40 |
| line_price | Decimal | none | 41 |
| start_time | datetime | none | 42 |
| end_time | datetime | none | 43 |
| calculation_valid | bool | True | 44 |
| behavior_internal | bool | False | 45 |

## direction_policy.py: DirectionPolicy

Source line: 21.

| Field | Type | Default | Line |
|---|---|---|---:|
| direction | Direction | none | 22 |
| extreme_attr | Literal['low', 'high'] | none | 23 |
| opposite_extreme_attr | Literal['high', 'low'] | none | 24 |
| first_reaction_tag | Literal['RED', 'GREEN'] | none | 25 |
| context_tag | Literal['GREEN', 'RED'] | none | 26 |

## e_zone_detector.py: EZone

Source line: 31.

| Field | Type | Default | Line |
|---|---|---|---:|
| direction | str | none | 32 |
| family | str | none | 33 |
| number | int | none | 34 |
| parent_type | str | none | 35 |
| parent_source_index | int | none | 36 |
| parent_source_time | datetime | none | 37 |
| parent_price | Decimal | none | 38 |
| parent_stop_index | int | none | 39 |
| parent_stop_time | datetime | none | 40 |
| parent_stop_event_time | datetime | none | 41 |
| order_direction | str | none | 42 |
| order_reaction_number | int | none | 43 |
| order_mode | str | none | 44 |
| order_causes | tuple[str, ...] | none | 45 |
| order_parent_stop_cause_time | datetime \| None | none | 46 |
| order_first_index | int | none | 47 |
| order_first_time | datetime | none | 48 |
| order_break_index | int | none | 49 |
| order_break_time | datetime | none | 50 |
| order_confirmation_time | datetime | none | 51 |
| order_box_top | Decimal | none | 52 |
| order_box_top_source_index | int | none | 53 |
| order_box_top_source_time | datetime | none | 54 |
| order_box_bottom | Decimal | none | 55 |
| order_box_bottom_source_index | int | none | 56 |
| order_box_bottom_source_time | datetime | none | 57 |
| order_stop_level | Decimal | none | 58 |
| order_stop_source_index | int | none | 59 |
| order_stop_source_time | datetime | none | 60 |
| source_index | int | none | 61 |
| source_time | datetime | none | 62 |
| price | Decimal | none | 63 |
| decision_index | int | none | 64 |
| decision_time | datetime | none | 65 |
| decision_event_time | datetime | none | 66 |

## e_zone_detector.py: EZoneDetector

Source line: 69.

No directly annotated class fields; methods are recorded in the module Source note.

## lifecycle_engine.py: StopAll

Source line: 43.

| Field | Type | Default | Line |
|---|---|---|---:|
| direction | str | none | 44 |
| number | int | none | 45 |
| source_index | int | none | 46 |
| source_time | datetime | none | 47 |
| price | Decimal | none | 48 |
| decision_index | int | none | 49 |
| decision_time | datetime | none | 50 |
| decision_event_time | datetime | none | 51 |
| gate_type | str | none | 52 |
| gate_event_time | datetime | none | 53 |
| stopped_behavior_type | str | none | 54 |
| stopped_behavior_key | str | none | 55 |
| stopped_behavior_count | int | none | 56 |
| underlying_e_family | str \| None | none | 57 |
| underlying_e_number | int \| None | none | 58 |
| order_direction | str \| None | none | 59 |
| order_reaction_number | int \| None | none | 60 |
| order_mode | str \| None | none | 61 |
| order_causes | tuple[str, ...] | none | 62 |
| order_parent_stop_cause_time | datetime \| None | none | 63 |
| order_first_index | int \| None | none | 64 |
| order_first_time | datetime \| None | none | 65 |
| order_break_index | int \| None | none | 66 |
| order_break_time | datetime \| None | none | 67 |
| order_confirmation_time | datetime \| None | none | 68 |
| order_box_top | Decimal \| None | none | 69 |
| order_box_top_source_index | int \| None | none | 70 |
| order_box_top_source_time | datetime \| None | none | 71 |
| order_box_bottom | Decimal \| None | none | 72 |
| order_box_bottom_source_index | int \| None | none | 73 |
| order_box_bottom_source_time | datetime \| None | none | 74 |
| order_stop_level | Decimal \| None | none | 75 |
| order_stop_source_index | int \| None | none | 76 |
| order_stop_source_time | datetime \| None | none | 77 |
| stop_index | int \| None | none | 78 |
| stop_time | datetime \| None | none | 79 |
| stop_event_time | datetime \| None | none | 80 |
| donor_type | str \| None | field(default=None, kw_only=True) | 85 |
| donor_source_index | int \| None | field(default=None, kw_only=True) | 86 |
| donor_source_time | datetime \| None | field(default=None, kw_only=True) | 87 |
| donor_color | str \| None | field(default=None, kw_only=True) | 88 |
| donor_number | int \| None | field(default=None, kw_only=True) | 89 |
| donor_price | Decimal \| None | field(default=None, kw_only=True) | 90 |
| donor_stop_time | datetime \| None | field(default=None, kw_only=True) | 91 |
| donor_stop_event_time | datetime \| None | field(default=None, kw_only=True) | 92 |

## lifecycle_engine.py: StopAllDetector

Source line: 95.

No directly annotated class fields; methods are recorded in the module Source note.

## order_audit_engine.py: PostBehaviorStop

Source line: 18.

| Field | Type | Default | Line |
|---|---|---|---:|
| behavior_type | str | none | 19 |
| behavior_source_index | int | none | 20 |
| behavior_source_time | datetime | none | 21 |
| event_time | datetime | none | 22 |

## order_audit_engine.py: OrderBBehaviorAnchor

Source line: 26.

| Field | Type | Default | Line |
|---|---|---|---:|
| behavior_type | str | none | 27 |
| behavior_source_index | int | none | 28 |
| behavior_source_time | datetime | none | 29 |
| priority | int | none | 30 |
| number | int | none | 31 |

## order_audit_engine.py: OrderBResetLeg

Source line: 35.

| Field | Type | Default | Line |
|---|---|---|---:|
| post_stop | PostBehaviorStop | none | 36 |
| anchor_behavior_type | str | none | 37 |
| anchor_behavior_source_index | int | none | 38 |
| anchor_behavior_source_time | datetime | none | 39 |
| anchor_behavior_extreme | Decimal | none | 40 |
| reset_reaction | object | none | 41 |
| reset_confirmation_time | datetime | none | 42 |
| reset_source_index | int | none | 43 |
| reset_broken_level | Decimal | none | 44 |
| reset_time | datetime | none | 45 |
| leg_boundary | Decimal | none | 46 |
| leg_source_index | int | none | 47 |
| leg_source_time | datetime | none | 48 |
| strict_break_time | datetime | none | 49 |
| reaction_number | int | none | 50 |
| physical_reaction | object | none | 51 |
| physical_confirmation_time | datetime | none | 52 |

## order_audit_engine.py: OrderAuditEngineMixin

Source line: 437.

No directly annotated class fields; methods are recorded in the module Source note.

## order_audit_engine.py: SOrderAuditMixin

Source line: 1734.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: Candle

Source line: 27.

| Field | Type | Default | Line |
|---|---|---|---:|
| index | int | none | 28 |
| timestamp | datetime | none | 29 |
| display_time | str | none | 30 |
| tag | str | none | 31 |
| open | Decimal | none | 32 |
| high | Decimal | none | 33 |
| low | Decimal | none | 34 |
| close | Decimal | none | 35 |

## reaction_engine.py: Candidate

Source line: 39.

| Field | Type | Default | Line |
|---|---|---|---:|
| first_idx | int | none | 40 |
| first_time | str | none | 41 |
| box_top_source_idx | int | none | 42 |
| box_top_source_time | str | none | 43 |
| box_top | Decimal | none | 44 |
| box_bottom_source_idx | int | none | 45 |
| box_bottom_source_time | str | none | 46 |
| box_bottom | Decimal | none | 47 |
| mode | str | none | 48 |
| anchor_idx | int \| None | None | 49 |
| anchor_value | Decimal \| None | None | 50 |
| leg_boundary_value | Decimal \| None | None | 51 |
| break_idx | int \| None | None | 52 |
| break_time | str \| None | None | 53 |
| intrabar_start | datetime \| None | None | 54 |
| cross_direction_origin | bool | False | 55 |
| cross_direction_chain_owner | bool | False | 56 |
| order_gate_decision | str \| None | None | 57 |
| behavior_public_number | int \| None | None | 58 |
| behavior_public_box_top | Decimal \| None | None | 59 |
| behavior_public_box_bottom | Decimal \| None | None | 60 |
| behavior_confirmation_time | datetime \| None | None | 61 |
| behavior_first_time | datetime \| None | None | 62 |
| behavior_internal | bool | False | 63 |

## reaction_engine.py: ResetEvent

Source line: 67.

| Field | Type | Default | Line |
|---|---|---|---:|
| index | int | none | 68 |
| display_time | str | none | 69 |
| second_time | str \| None | none | 70 |
| broken_level | Decimal | none | 71 |
| from_first_idx | int | none | 72 |

## reaction_engine.py: IntrabarAnalysis

Source line: 76.

| Field | Type | Default | Line |
|---|---|---|---:|
| event_second | Candle | none | 77 |
| extreme | Decimal | none | 78 |
| extreme_source | Candle | none | 79 |

## reaction_engine.py: DetectionResult

Source line: 83.

| Field | Type | Default | Line |
|---|---|---|---:|
| direction | str | none | 84 |
| reactions | list[Candidate] | none | 85 |
| resets | list[ResetEvent] | none | 86 |
| start_index | int | none | 87 |
| end_index | int | none | 88 |

## reaction_engine.py: DetectorBase

Source line: 101.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: BullishDetector

Source line: 174.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: _ReflectedCandles

Source line: 608.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: BearishDetector

Source line: 646.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: LowerTimeframeIndex

Source line: 809.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: ReflectedLowerTimeframeIndex

Source line: 947.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: MarketChronology

Source line: 971.

No directly annotated class fields; methods are recorded in the module Source note.

## reaction_engine.py: UnifiedReactionDetector

Source line: 1376.

No directly annotated class fields; methods are recorded in the module Source note.

## s_zone_detector.py: SZone

Source line: 28.

| Field | Type | Default | Line |
|---|---|---|---:|
| direction | str | none | 29 |
| color | str | none | 30 |
| formation_type | str | none | 31 |
| a_ordinal | int | none | 32 |
| a_source_index | int | none | 33 |
| a_source_time | datetime | none | 34 |
| a_price | Decimal | none | 35 |
| a_stop_index | int | none | 36 |
| a_stop_time | datetime | none | 37 |
| a_stop_event_time | datetime | none | 38 |
| order_direction | str \| None | none | 39 |
| order_reaction_number | int \| None | none | 40 |
| order_mode | str \| None | none | 41 |
| order_first_index | int \| None | none | 42 |
| order_first_time | datetime \| None | none | 43 |
| order_break_index | int \| None | none | 44 |
| order_break_time | datetime \| None | none | 45 |
| order_confirmation_time | datetime \| None | none | 46 |
| order_box_top | Decimal \| None | none | 47 |
| order_box_top_source_index | int \| None | none | 48 |
| order_box_top_source_time | datetime \| None | none | 49 |
| order_box_bottom | Decimal \| None | none | 50 |
| order_box_bottom_source_index | int \| None | none | 51 |
| order_box_bottom_source_time | datetime \| None | none | 52 |
| order_stop_level | Decimal \| None | none | 53 |
| order_stop_source_index | int \| None | none | 54 |
| order_stop_source_time | datetime \| None | none | 55 |
| reset_reaction_number | int \| None | none | 56 |
| reset_time | datetime \| None | none | 57 |
| source_index | int | none | 58 |
| source_time | datetime | none | 59 |
| price | Decimal | none | 60 |
| decision_index | int | none | 61 |
| decision_time | datetime | none | 62 |
| decision_event_time | datetime | none | 63 |

## s_zone_detector.py: SZoneDetector

Source line: 66.

No directly annotated class fields; methods are recorded in the module Source note.
