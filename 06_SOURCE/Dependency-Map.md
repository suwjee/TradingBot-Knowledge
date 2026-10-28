---
id: "source.dependency_map"
type: "source"
status: "active"
authority: "executable"
title: "Current dependency map"
version: "current"
related_entities: ["source.reference_registry", "source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/__init__.py", "06_SOURCE/Code/engine/bridge/__init__.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/__init__.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/direction_policy.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Current captured dependency map

Lexical imports below come from exact captured Source. The Bridge dynamically loads owner modules from configured paths; literal imports alone do not define the complete runtime closure. Live discovery found the deliberately excluded added detector; source_scope records its absent standalone capture and exact embedded-only evidence.

| Source | Line | Import |
| --- | ---: | --- |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 9 | __future__ : annotations |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 11 | argparse |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 12 | importlib.util |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 13 | json |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 14 | sys |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 15 | bisect : bisect_left |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 16 | dataclasses : dataclass, field |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 17 | datetime : datetime |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 18 | decimal : Decimal |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 19 | pathlib : Path |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 20 | time : perf_counter |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 21 | typing : Sequence |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 22 | zoneinfo : ZoneInfo |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 36 | core_utils : as_decimal, order_identity |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 37 | order_audit_engine : accepted_audit_entries, order_b_leg_identity |
| 06_SOURCE/Code/engine/pipeline/__init__.py | 7 | sys |
| 06_SOURCE/Code/engine/pipeline/__init__.py | 8 | pathlib : Path |
| 06_SOURCE/Code/engine/pipeline/__init__.py | 14 | .blue_line_detector : BlueLine, ScaleStrike, count_scale_strikes, detect_blue_lines, fibonacci_level |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 8 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 10 | bisect : bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 11 | dataclasses : dataclass, field |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 12 | datetime : datetime, timedelta |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 13 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 14 | typing : Sequence |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 16 | core_utils : as_decimal |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 17 | direction_policy : policy_for |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 8 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 10 | dataclasses : dataclass |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 11 | datetime : datetime |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 12 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 13 | typing : Sequence |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 15 | direction_policy : policy_for |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | 3 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | 7 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | 8 | typing : TypeAlias |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 9 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 13 | dataclasses : dataclass |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 14 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 15 | typing : Literal |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 8 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 10 | bisect : bisect_left |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 11 | dataclasses : dataclass, replace |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 12 | datetime : datetime |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 13 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 14 | typing : Callable, Sequence |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 16 | core_utils : as_decimal, reaction_identity |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 17 | direction_policy : policy_for |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 18 | order_audit_engine : OrderAuditEngineMixin, OrderBResetLeg, OrderMatch, PostBehaviorStop, discover_accepted_order_b_reset_legs, discover_order_b_reset_legs, dominant_post_behavior_stops, order_b_reset_event_time |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 9 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 11 | bisect : bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 12 | dataclasses : dataclass, field, replace |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 13 | datetime : datetime |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 14 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 15 | typing : Sequence |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 17 | core_utils : as_decimal, order_identity |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 18 | order_audit_engine : accepted_audit_entry, prepare_order_audit |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 21 | direction_policy : policy_for |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 3 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 5 | bisect : bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 6 | copy : deepcopy |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 7 | dataclasses : dataclass |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 8 | datetime : datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 9 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 10 | types : SimpleNamespace |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 11 | typing : Callable, Sequence |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 13 | core_utils : as_decimal, order_identity, reaction_identity |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 9 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 11 | bisect |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 12 | array : array |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 13 | dataclasses : dataclass, replace |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 14 | datetime : datetime, timedelta |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 15 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 16 | typing : Iterable, Sequence |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 18 | direction_policy : policy_for |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 9 | __future__ : annotations |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 11 | bisect : bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 12 | dataclasses : dataclass, replace |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 13 | datetime : datetime, timedelta |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 14 | decimal : Decimal |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 15 | typing : Callable, Sequence |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 17 | core_utils : as_decimal |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 18 | order_audit_engine : SOrderAuditMixin |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 19 | direction_policy : policy_for |

Integration dependency closure is documented by source.local_server, source.raw_resources, source.faraz and source.chart_workspace. The configured calculation fingerprint hashes its configured production set; this is separate from complete future module discovery.
