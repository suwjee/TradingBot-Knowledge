---
id: "source.trading_pipeline"
type: "source"
status: "active"
authority: "executable"
title: "CLI input normalization, dynamic module loading, cross-stage coordination, OrderAudit preparation and JSON serialization"
version: "1.11.0"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/bridge/trading_pipeline.py"
mirror: "06_SOURCE/Code/engine/bridge/trading_pipeline.py"
sha256: "d70481975d2b8e41c6271a02243862d967d5c906bbe1f2f23a432df6fc0f85a1"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# trading_pipeline.py

CLI input normalization, dynamic module loading, cross-stage coordination, OrderAudit preparation and JSON serialization.

Exact bytes describe executable behavior; Source identity is not intended-semantic authority or independent market correctness. Supported dynamic Bridge loading and the maintained pipeline compatibility wrapper are distinct runtime surfaces. The manifest source_scope bounds audit/reconstruction completeness.

## Snapshot identity

| Property | Current captured evidence |
| --- | --- |
| Source | 06_SOURCE/Code/engine/bridge/trading_pipeline.py |
| SHA-256 | d70481975d2b8e41c6271a02243862d967d5c906bbe1f2f23a432df6fc0f85a1 |
| Bytes | 123325 |
| Lines | 3231 |
| Declared version | 1.11.0 |

## Lexical Source symbols

Every lexical definition in this captured owner is indexed mechanically, including incidental out-of-scope feature helpers. A symbol row is navigation, not a separate concept or semantic approval.

| Symbol | Line | End |
| --- | ---: | ---: |
| emit_progress | 50 | 55 |
| timed | 58 | 67 |
| load_module | 70 | 77 |
| load_engine | 80 | 81 |
| local_datetime | 87 | 93 |
| epoch | 99 | 105 |
| display_epoch | 111 | 120 |
| build_candle_buckets | 123 | 178 |
| build_candle_buckets.cached_decimal | 132 | 143 |
| build_candle_objects | 181 | 208 |
| _index_selected | 211 | 216 |
| select_reaction_serialization_items | 219 | 239 |
| serialize | 242 | 283 |
| serialize_blue_lines | 286 | 303 |
| serialize_a_zones | 306 | 330 |
| serialize_s_zones | 333 | 395 |
| serialize_e_zones | 398 | 438 |
| serialize_stopalls | 441 | 505 |
| bridge_datetime | 508 | 519 |
| bridge_direction | 522 | 523 |
| bridge_mode | 526 | 527 |
| bridge_color | 530 | 533 |
| _bridge_horizon | 536 | 540 |
| _bridge_in_horizon | 543 | 544 |
| _bridge_proven_strict_event | 547 | 584 |
| _bridge_stop_view | 587 | 604 |
| _bridge_reaction_confirmation | 607 | 628 |
| _bridge_order_identity | 631 | 636 |
| BridgeProjection | 639 | 830 |
| BridgeProjection.__init__ | 647 | 664 |
| BridgeProjection.physical_order | 666 | 709 |
| BridgeProjection.parent_order | 711 | 716 |
| BridgeProjection.current_order | 718 | 771 |
| BridgeProjection.order_audit | 773 | 830 |
| _bridge_parent_stop | 833 | 851 |
| _bridge_a_stop | 854 | 872 |
| _bridge_behavior_stop | 875 | 887 |
| _bridge_blue_formation | 890 | 910 |
| _bridge_project_reaction | 913 | 953 |
| _bridge_project_reset | 956 | 976 |
| _bridge_project_blue | 979 | 1012 |
| _bridge_full_lines_by_ordinal | 1015 | 1024 |
| _bridge_project_a | 1027 | 1114 |
| _bridge_project_s | 1117 | 1170 |
| _bridge_source_index | 1173 | 1178 |
| _bridge_parent_behavior_for_e | 1181 | 1222 |
| _bridge_project_e | 1225 | 1269 |
| _bridge_project_stopall | 1272 | 1338 |
| _bridge_audit_order_key | 1341 | 1348 |
| build_bridge_output | 1351 | 1453 |
| validate_order_audit_bridge | 1456 | 1521 |
| serialize_order_audit | 1524 | 1574 |
| EngineBundle | 1578 | 1585 |
| MarketContext | 1589 | 1595 |
| parse_arguments | 1598 | 1668 |
| load_engines | 1671 | 1706 |
| prepare_market_context | 1709 | 1789 |
| PipelineState | 1792 | 1808 |
| FullDirectionState | 1812 | 1824 |
| create_e_detector | 1827 | 1872 |
| create_e_detector.direct_geometry | 1846 | 1854 |
| calculate_full_direction_state | 1875 | 2207 |
| calculate_direction_with_order_b_feedback | 2210 | 2269 |
| prepare_pipeline_state | 2272 | 2405 |
| DirectionRangeState | 2409 | 2418 |
| DirectionVisibilityState | 2422 | 2437 |
| calculate_direction_range_state | 2440 | 2539 |
| finalize_direction_visibility | 2542 | 2776 |
| serialize_direction_payload | 2779 | 2917 |
| serialize_direction_payload.build_legacy_payload | 2806 | 2829 |
| serialize_direction_payload.serialize_reactions_from_one_selection | 2838 | 2846 |
| serialize_direction_payload.build_payload | 2879 | 2913 |
| serialize_primary_order | 2920 | 2946 |
| serialize_primary_order.value | 2923 | 2928 |
| serialize_primary_structures | 2949 | 3050 |
| serialize_primary_structures.point | 2955 | 2978 |
| calculate_primary_structures | 3053 | 3096 |
| calculate_primary_structures.commit_high | 3074 | 3080 |
| build_direction_output | 3099 | 3137 |
| build_response_payload | 3139 | 3190 |
| main | 3193 | 3223 |
