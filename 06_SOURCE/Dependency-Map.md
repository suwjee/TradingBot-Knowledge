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
---

# Current dependency map

Imports are exact current AST addresses; dynamic orchestration is described by core.pipeline. Imports identify dependencies without transferring algorithm ownership.

| Module | Line | Import |
|---|---:|---|
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 9 | from __future__ import annotations |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 11 | import argparse |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 12 | import importlib.util |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 13 | import json |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 14 | import sys |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 15 | import orjson |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 16 | from bisect import bisect_left |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 17 | from dataclasses import dataclass |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 18 | from datetime import datetime |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 19 | from decimal import Decimal |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 20 | from pathlib import Path |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 21 | from time import perf_counter |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 22 | from typing import Sequence |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 23 | from zoneinfo import ZoneInfo |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 37 | from core_utils import as_decimal, order_identity |
| 06_SOURCE/Code/engine/bridge/trading_pipeline.py | 38 | from order_audit_engine import order_b_leg_identity |
| 06_SOURCE/Code/engine/pipeline/__init__.py | 3 | from .blue_line_detector import BlueLine, ScaleStrike, count_scale_strikes, detect_blue_lines, fibonacci_level, run_blue_line |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 8 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 10 | from bisect import bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 11 | from dataclasses import dataclass, field |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 12 | from datetime import datetime, timedelta |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 13 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 14 | from typing import Sequence |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 16 | from core_utils import as_decimal |
| 06_SOURCE/Code/engine/pipeline/a_zone_detector.py | 17 | from direction_policy import policy_for |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 8 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 10 | from dataclasses import dataclass |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 11 | from datetime import datetime |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 12 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 13 | from typing import Sequence |
| 06_SOURCE/Code/engine/pipeline/blue_line_detector.py | 15 | from direction_policy import policy_for |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | 3 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | 7 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/core_utils.py | 8 | from typing import TypeAlias |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 9 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 13 | from dataclasses import dataclass |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 14 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/direction_policy.py | 15 | from typing import Literal |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 8 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 10 | from bisect import bisect_left |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 11 | from dataclasses import dataclass, replace |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 12 | from datetime import datetime |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 13 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 14 | from typing import Callable, Sequence |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 16 | from core_utils import as_decimal, reaction_identity |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 17 | from direction_policy import policy_for |
| 06_SOURCE/Code/engine/pipeline/e_zone_detector.py | 18 | from order_audit_engine import OrderAuditEngineMixin, OrderBResetLeg, OrderMatch, PostBehaviorStop, discover_accepted_order_b_reset_legs, discover_order_b_reset_legs, dominant_post_behavior_stops, order_b_reset_event_time |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 9 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 11 | from bisect import bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 12 | from dataclasses import dataclass, field, replace |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 13 | from datetime import datetime |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 14 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 15 | from typing import Sequence |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 17 | from core_utils import as_decimal, order_identity |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 18 | from order_audit_engine import accepted_audit_entry, order_identity_is_internal, prepare_order_audit |
| 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py | 21 | from direction_policy import policy_for |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 3 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 5 | from bisect import bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 6 | from dataclasses import dataclass |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 7 | from datetime import datetime |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 8 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 9 | from types import SimpleNamespace |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 10 | from typing import Callable, Sequence |
| 06_SOURCE/Code/engine/pipeline/order_audit_engine.py | 12 | from core_utils import as_decimal, order_identity, reaction_identity |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 9 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 11 | import bisect |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 12 | from array import array |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 13 | from dataclasses import dataclass, replace |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 14 | from datetime import datetime, timedelta |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 15 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 16 | from typing import Iterable, Sequence |
| 06_SOURCE/Code/engine/pipeline/reaction_engine.py | 18 | from direction_policy import policy_for |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 9 | from __future__ import annotations |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 11 | from bisect import bisect_left, bisect_right |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 12 | from dataclasses import dataclass, replace |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 13 | from datetime import datetime, timedelta |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 14 | from decimal import Decimal |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 15 | from typing import Callable, Sequence |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 17 | from core_utils import as_decimal |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 18 | from order_audit_engine import SOrderAuditMixin |
| 06_SOURCE/Code/engine/pipeline/s_zone_detector.py | 19 | from direction_policy import policy_for |
