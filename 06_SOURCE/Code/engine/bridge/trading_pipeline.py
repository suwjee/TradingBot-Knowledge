"""Production trading pipeline orchestration, input normalization, and serialization.

Owns request parsing, raw-range isolation, candle construction, engine loading,
stage orchestration, progress/timing telemetry, and JSON serialization. Trading
validity/ownership rules belong to their calculation engines; this module must
not reimplement them.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import orjson
from bisect import bisect_left
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from time import perf_counter
from zoneinfo import ZoneInfo

# This bridge lives in ``engine/bridge`` while the calculation modules live in
# the sibling ``engine/pipeline`` package.  Put that directory on the module
# search path before importing shared helpers or dynamically loading detectors.
# The detector files intentionally keep their flat local imports
# (``core_utils`` / ``direction_policy``), so this single bootstrap point keeps
# every production module aligned with the deployed folder structure.
_ENGINE_ROOT = Path(__file__).resolve().parents[1]
_PIPELINE_DIR = _ENGINE_ROOT / "pipeline"
_pipeline_dir_text = str(_PIPELINE_DIR)
if _pipeline_dir_text not in sys.path:
    sys.path.insert(0, _pipeline_dir_text)

from core_utils import as_decimal, order_identity

_DTFMT = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}"


TRADING_PIPELINE_VERSION = "1.5.1"
TRADING_PIPELINE_LAST_MODIFIED = "2026-09-24 03:54:00 +03:30"

TEHRAN = ZoneInfo("Asia/Tehran")


def emit_progress(status: str, label: str, duration_ms: float | None = None):
    """Send machine-readable lifecycle events without contaminating JSON stdout."""
    event = {"status": status, "label": label}
    if duration_ms is not None:
        event["durationMs"] = round(duration_ms, 2)
    print(f"QG_PROGRESS:{json.dumps(event, separators=(',', ':'))}", file=sys.stderr, flush=True)


def timed(timings: dict[str, float], label: str, work):
    """Measure an existing pipeline phase without changing its inputs or output."""
    started = perf_counter()
    emit_progress("started", label)
    try:
        return work()
    finally:
        duration_ms = (perf_counter() - started) * 1000
        timings[label] = timings.get(label, 0.0) + duration_ms
        emit_progress("completed", label, duration_ms)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load reaction engine: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_engine(path: Path):
    return load_module("reaction_engine", path)


_local_dt_cache: dict[int, datetime] = {}


def local_datetime(epoch: int) -> datetime:
    cached = _local_dt_cache.get(epoch)
    if cached is not None:
        return cached
    result = datetime.fromtimestamp(epoch, TEHRAN).replace(tzinfo=None)
    _local_dt_cache[epoch] = result
    return result


_epoch_cache: dict[datetime, int] = {}


def epoch(local: datetime) -> int:
    cached = _epoch_cache.get(local)
    if cached is not None:
        return cached
    result = int(local.replace(tzinfo=TEHRAN).timestamp())
    _epoch_cache[local] = result
    return result


_display_epoch_cache: dict[str, int] = {}


def display_epoch(value: str | datetime) -> int:
    """Convert an engine display/native timestamp once per pipeline process."""
    if isinstance(value, datetime):
        return epoch(value)
    cached = _display_epoch_cache.get(value)
    if cached is not None:
        return cached
    result = epoch(datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
    _display_epoch_cache[value] = result
    return result


def build_candle_buckets(rows: list[dict], timeframe: int):
    """Normalize raw rows once, preserving lower and selected-timeframe buckets."""
    second_buckets: list[dict] = []
    current_second = None
    buckets: list[dict] = []
    current = None
    to_decimal = as_decimal
    decimal_cache: dict[tuple[type, object], Decimal] = {}

    def cached_decimal(value: object) -> Decimal:
        # Raw prices repeat heavily. Cache by both type and value so values
        # such as ``10`` and ``10.0`` retain their exact string-normalized
        # Decimal representation instead of being conflated by Python's
        # numeric equality rules.
        key = (type(value), value)
        try:
            return decimal_cache[key]
        except KeyError:
            normalized = to_decimal(value)
            decimal_cache[key] = normalized
            return normalized

    for row in rows:
        timestamp = int(row["time"])
        o = cached_decimal(row["open"])
        high = cached_decimal(row["high"])
        low = cached_decimal(row["low"])
        close = cached_decimal(row["close"])
        if current_second is None or current_second["time"] != timestamp:
            current_second = {
                "time": timestamp,
                "open": o,
                "high": high,
                "low": low,
                "close": close,
            }
            second_buckets.append(current_second)
        else:
            current_second["high"] = max(current_second["high"], high)
            current_second["low"] = min(current_second["low"], low)
            current_second["close"] = close
        bucket_time = timestamp if timeframe == 1 else timestamp // timeframe * timeframe
        if current is None or current["time"] != bucket_time:
            current = {
                "time": bucket_time,
                "open": o,
                "high": high,
                "low": low,
                "close": close,
            }
            buckets.append(current)
        else:
            current["high"] = max(current["high"], high)
            current["low"] = min(current["low"], low)
            current["close"] = close
    return second_buckets, buckets


def build_candle_objects(engine, buckets: list[dict]):
    """Create maintained engine candles from already-normalized buckets."""
    candles = []
    append = candles.append
    candle_type = engine.Candle
    classify = engine.classify_candle_color
    local = local_datetime
    fmt = _DTFMT.format
    for index, item in enumerate(buckets):
        stamp = local(item["time"])
        append(candle_type(
            index=index,
            timestamp=stamp,
            display_time=fmt(
                stamp.year,
                stamp.month,
                stamp.day,
                stamp.hour,
                stamp.minute,
                stamp.second,
            ),
            tag=classify(item["open"], item["close"]),
            open=item["open"],
            high=item["high"],
            low=item["low"],
            close=item["close"],
        ))
    return candles


def _index_selected(index: object, start_index: int | None, end_index: int | None) -> bool:
    return (
        start_index is None
        or end_index is None
        or start_index <= int(index) <= end_index
    )


def select_reaction_serialization_items(
    result, start_index=None, end_index=None, reaction_transform=None,
):
    """Select the exact legacy Reaction/Reset sequence once for both views.

    This is a presentation selection only.  It retains the legacy filtering
    and ordering verbatim while exposing the same finalized source objects to
    the optional Bridge Output projector.
    """
    resets = [
        item
        for item in result.resets
        if _index_selected(item.index, start_index, end_index)
    ]
    reactions = []
    for item in result.reactions:
        if not _index_selected(item.first_idx, start_index, end_index):
            continue
        public_item = reaction_transform(item) if reaction_transform is not None else item
        reactions.append((item, public_item))
    return reactions, resets


def serialize(
    result,
    start_index=None,
    end_index=None,
    reaction_transform=None,
    selected_items=None,
):
    """Serialize legacy Reaction/Reset output without changing its contract."""
    selected_reactions, selected_resets = (
        selected_items
        if selected_items is not None
        else select_reaction_serialization_items(
            result, start_index, end_index, reaction_transform
        )
    )
    resets = [{
        "index": item.index,
        "time": display_epoch(item.display_time),
        "secondTime": (
            display_epoch(item.second_time)
            if item.second_time is not None
            else None
        ),
        "brokenLevel": str(item.broken_level),
        "fromFirstIndex": item.from_first_idx,
    } for item in selected_resets]
    reactions = []
    for _item, public_item in selected_reactions:
        reactions.append({
            "firstIndex": public_item.first_idx,
            "firstTime": display_epoch(public_item.first_time),
            "boxTopSourceIndex": public_item.box_top_source_idx,
            "boxTopSourceTime": display_epoch(public_item.box_top_source_time),
            "boxTop": str(public_item.box_top),
            "boxBottomSourceIndex": public_item.box_bottom_source_idx,
            "boxBottomSourceTime": display_epoch(public_item.box_bottom_source_time),
            "boxBottom": str(public_item.box_bottom),
            "breakIndex": public_item.break_idx,
            "breakTime": display_epoch(public_item.break_time),
            "mode": public_item.mode,
        })
    return reactions, resets


def serialize_blue_lines(items, start_index=None, end_index=None):
    return [{
        "direction": item.direction,
        "kind": item.kind,
        "reactionNumber": item.reaction_number,
        "previousStrikeCount": item.previous_strike_count,
        "strikeCount": item.strike_count,
        "fibonacciLevel": str(item.fibonacci_level) if item.fibonacci_level is not None else None,
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "sourceExtreme": str(item.source_extreme),
        "brokenLevel": str(item.broken_level) if item.broken_level is not None else None,
        "linePrice": str(item.line_price),
        "startTime": epoch(item.start_time),
        "endTime": epoch(item.end_time),
    } for item in items if _index_selected(
        getattr(item, "source_index"), start_index, end_index
    )]


def serialize_a_zones(items):
    return [{
        "direction": item.direction,
        "blue1Ordinal": item.blue_1_ordinal,
        "blue2Ordinal": item.blue_2_ordinal,
        "blue1SourceTime": epoch(item.blue_1_source_time),
        "blue2SourceTime": epoch(item.blue_2_source_time),
        "blue1StopTime": epoch(item.blue_1_stop_time),
        "blue2StopTime": epoch(item.blue_2_stop_time),
        "blue1StopLevel": str(item.blue_1_stop_level),
        "blue2StopLevel": str(item.blue_2_stop_level),
        "continuationLevel": str(item.continuation_level),
        "continuationSourceIndex": item.continuation_source_index,
        "continuationSourceTime": epoch(item.continuation_source_time),
        "triggerIndex": item.trigger_index,
        "triggerTime": epoch(item.trigger_time),
        "triggerEventTime": epoch(item.trigger_event_time),
        "reactionNumber": item.reaction_number,
        "reactionFirstTime": epoch(item.reaction_first_time),
        "reactionBreakTime": epoch(item.reaction_break_time),
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "calculationValid": True,
    } for item in items]


def serialize_s_zones(items):
    return [{
        "direction": item.direction,
        "color": item.color,
        "formationType": item.formation_type,
        "aOrdinal": item.a_ordinal,
        "aSourceIndex": item.a_source_index,
        "aSourceTime": epoch(item.a_source_time),
        "aPrice": str(item.a_price),
        "aStopIndex": item.a_stop_index,
        "aStopTime": epoch(item.a_stop_time),
        "aStopEventTime": epoch(item.a_stop_event_time),
        "orderDirection": item.order_direction,
        "orderReactionNumber": item.order_reaction_number,
        "orderMode": item.order_mode,
        "orderFirstIndex": item.order_first_index,
        "orderFirstTime": (
            epoch(item.order_first_time) if item.order_first_time is not None else None
        ),
        "orderBreakIndex": item.order_break_index,
        "orderBreakTime": (
            epoch(item.order_break_time) if item.order_break_time is not None else None
        ),
        "orderConfirmationTime": (
            epoch(item.order_confirmation_time)
            if item.order_confirmation_time is not None
            else None
        ),
        "orderBoxTop": str(item.order_box_top) if item.order_box_top is not None else None,
        "orderBoxTopSourceIndex": item.order_box_top_source_index,
        "orderBoxTopSourceTime": (
            epoch(item.order_box_top_source_time)
            if item.order_box_top_source_time is not None
            else None
        ),
        "orderBoxBottom": (
            str(item.order_box_bottom) if item.order_box_bottom is not None else None
        ),
        "orderBoxBottomSourceIndex": item.order_box_bottom_source_index,
        "orderBoxBottomSourceTime": (
            epoch(item.order_box_bottom_source_time)
            if item.order_box_bottom_source_time is not None
            else None
        ),
        "orderStopLevel": (
            str(item.order_stop_level) if item.order_stop_level is not None else None
        ),
        "orderStopSourceIndex": item.order_stop_source_index,
        "orderStopSourceTime": (
            epoch(item.order_stop_source_time)
            if item.order_stop_source_time is not None
            else None
        ),
        "resetReactionNumber": item.reset_reaction_number,
        "resetTime": epoch(item.reset_time) if item.reset_time is not None else None,
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "decisionIndex": item.decision_index,
        "decisionTime": epoch(item.decision_time),
        "decisionEventTime": epoch(item.decision_event_time),
        "calculationValid": True,
    } for item in items]


def serialize_e_zones(items):
    return [{
        "direction": item.direction,
        "family": item.family,
        "number": item.number,
        "parentType": item.parent_type,
        "parentSourceIndex": item.parent_source_index,
        "parentSourceTime": epoch(item.parent_source_time),
        "parentPrice": str(item.parent_price),
        "parentStopIndex": item.parent_stop_index,
        "parentStopTime": epoch(item.parent_stop_time),
        "parentStopEventTime": epoch(item.parent_stop_event_time),
        "orderDirection": item.order_direction,
        "orderReactionNumber": item.order_reaction_number,
        "orderMode": item.order_mode,
        "orderCauses": list(item.order_causes),
        "orderParentStopCauseTime": (
            epoch(item.order_parent_stop_cause_time)
            if item.order_parent_stop_cause_time is not None else None
        ),
        "orderResetLegResetTime": (
            epoch(item.order_reset_leg_reset_time)
            if item.order_reset_leg_reset_time is not None else None
        ),
        "orderResetLegBreakTime": (
            epoch(item.order_reset_leg_break_time)
            if item.order_reset_leg_break_time is not None else None
        ),
        "orderFirstIndex": item.order_first_index,
        "orderFirstTime": epoch(item.order_first_time),
        "orderBreakIndex": item.order_break_index,
        "orderBreakTime": epoch(item.order_break_time),
        "orderConfirmationTime": epoch(item.order_confirmation_time),
        "orderBoxTop": str(item.order_box_top),
        "orderBoxTopSourceIndex": item.order_box_top_source_index,
        "orderBoxTopSourceTime": epoch(item.order_box_top_source_time),
        "orderBoxBottom": str(item.order_box_bottom),
        "orderBoxBottomSourceIndex": item.order_box_bottom_source_index,
        "orderBoxBottomSourceTime": epoch(item.order_box_bottom_source_time),
        "orderStopLevel": str(item.order_stop_level),
        "orderStopSourceIndex": item.order_stop_source_index,
        "orderStopSourceTime": epoch(item.order_stop_source_time),
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "decisionIndex": item.decision_index,
        "decisionTime": epoch(item.decision_time),
        "decisionEventTime": epoch(item.decision_event_time),
    } for item in items]


def serialize_stopalls(items):
    return [{
        "direction": item.direction,
        "number": item.number,
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "decisionIndex": item.decision_index,
        "decisionTime": epoch(item.decision_time),
        "decisionEventTime": epoch(item.decision_event_time),
        "gateType": item.gate_type,
        "gateEventTime": epoch(item.gate_event_time),
        "stoppedBehaviorType": item.stopped_behavior_type,
        "stoppedBehaviorKey": item.stopped_behavior_key,
        "stoppedBehaviorCount": item.stopped_behavior_count,
        "underlyingEFamily": item.underlying_e_family,
        "underlyingENumber": item.underlying_e_number,
        "orderDirection": item.order_direction,
        "orderReactionNumber": item.order_reaction_number,
        "orderMode": item.order_mode,
        "orderCauses": list(item.order_causes),
        "orderParentStopCauseTime": (
            epoch(item.order_parent_stop_cause_time)
            if item.order_parent_stop_cause_time is not None else None
        ),
        "orderResetLegResetTime": (
            epoch(item.order_reset_leg_reset_time)
            if item.order_reset_leg_reset_time is not None else None
        ),
        "orderResetLegBreakTime": (
            epoch(item.order_reset_leg_break_time)
            if item.order_reset_leg_break_time is not None else None
        ),
        "orderFirstIndex": item.order_first_index,
        "orderFirstTime": (
            epoch(item.order_first_time) if item.order_first_time is not None else None
        ),
        "orderBreakIndex": item.order_break_index,
        "orderBreakTime": (
            epoch(item.order_break_time) if item.order_break_time is not None else None
        ),
        "orderConfirmationTime": (
            epoch(item.order_confirmation_time)
            if item.order_confirmation_time is not None else None
        ),
        "orderBoxTop": (
            str(item.order_box_top) if item.order_box_top is not None else None
        ),
        "orderBoxTopSourceIndex": item.order_box_top_source_index,
        "orderBoxTopSourceTime": (
            epoch(item.order_box_top_source_time)
            if item.order_box_top_source_time is not None else None
        ),
        "orderBoxBottom": (
            str(item.order_box_bottom) if item.order_box_bottom is not None else None
        ),
        "orderBoxBottomSourceIndex": item.order_box_bottom_source_index,
        "orderBoxBottomSourceTime": (
            epoch(item.order_box_bottom_source_time)
            if item.order_box_bottom_source_time is not None else None
        ),
        "orderStopLevel": (
            str(item.order_stop_level) if item.order_stop_level is not None else None
        ),
        "orderStopSourceIndex": item.order_stop_source_index,
        "orderStopSourceTime": (
            epoch(item.order_stop_source_time)
            if item.order_stop_source_time is not None else None
        ),
        "stopIndex": item.stop_index,
        "stopTime": epoch(item.stop_time) if item.stop_time else None,
        "stopEventTime": epoch(item.stop_event_time) if item.stop_event_time else None,
    } for item in items]


def bridge_datetime(value: object | None) -> str | None:
    """Format a native Tehran-local timestamp for the YAML-facing view."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if not isinstance(value, datetime):
        return None
    return _DTFMT.format(
        value.year, value.month, value.day,
        value.hour, value.minute, value.second,
    )


def bridge_direction(direction: str) -> str:
    return str(direction).title()


def bridge_mode(mode: object) -> str | None:
    return {"A": "Leg Start", "B": "Normal"}.get(str(mode))


def bridge_color(value: object | None) -> str | None:
    if value in (None, ""):
        return None
    return str(value).title()


def _bridge_horizon(market: MarketContext) -> datetime:
    return (
        getattr(market.candles[market.end_index], "timestamp")
        + market.chronology.timeframe
    )


def _bridge_in_horizon(market: MarketContext, value: datetime | None) -> bool:
    return value is not None and value < _bridge_horizon(market)


def _bridge_proven_strict_event(
    market: MarketContext,
    direction: str,
    level: object | None,
    event_time: datetime | None,
) -> datetime | None:
    """Validate a recorded event without selecting a new trading event.

    A source helper has already selected ``event_time``.  This presentation
    guard only verifies that the exact recorded lower-timeframe candle satisfies
    that helper's existing directional strict-cross condition.  It never scans
    for a substitute event, so a main-candle fallback remains ``null`` here.
    """
    if (
        event_time is None
        or level is None
        or not _bridge_in_horizon(market, event_time)
    ):
        return None
    normalized = as_decimal(level)
    second_times = getattr(market.chronology, "second_times", None)
    if second_times is None:
        second_times = [getattr(item, "timestamp") for item in market.seconds]
    position = bisect_left(second_times, event_time)
    while (
        position < len(market.seconds)
        and getattr(market.seconds[position], "timestamp") == event_time
    ):
        item = market.seconds[position]
        crossed = (
            as_decimal(getattr(item, "high")) > normalized
            if direction == "bearish"
            else as_decimal(getattr(item, "low")) < normalized
        )
        if crossed:
            return event_time
        position += 1
    return None


def _bridge_stop_view(
    market: MarketContext,
    direction: str,
    price: object | None,
    stop_time: datetime | None,
    stop_event_time: datetime | None,
) -> dict[str, object]:
    """Format a known behavior/order stop while respecting the view horizon."""
    if stop_time is None or not _bridge_in_horizon(market, stop_time):
        return {"time": None, "eventTime": None}
    return {
        "time": bridge_datetime(stop_time),
        "eventTime": bridge_datetime(
            _bridge_proven_strict_event(
                market, direction, price, stop_event_time
            )
        ),
    }


def _bridge_reaction_confirmation(
    market: MarketContext,
    direction: str,
    reaction: object,
    *,
    use_intrabar_start: bool = True,
) -> datetime | None:
    """Return only an already-recorded, lower-timeframe-proven confirmation."""
    try:
        event_time = market.chronology.reaction_confirmation(
            direction, reaction, use_intrabar_start=use_intrabar_start
        )
        level = getattr(
            reaction, "box_top" if direction == "bullish" else "box_bottom"
        )
    except (AttributeError, IndexError, TypeError, ValueError):
        return None
    # Reaction confirmation crosses the *opposite* side from the directional
    # Stop predicate validated by this helper. Keep the recorded event immutable.
    return _bridge_proven_strict_event(
        market, market.chronology.opposite_direction(direction), level, event_time
    )


def _bridge_order_identity(item: object) -> tuple[int, int] | None:
    first_index = getattr(item, "order_first_index", None)
    break_index = getattr(item, "order_break_index", None)
    if first_index is None or break_index is None:
        return None
    return order_identity(int(first_index), int(break_index))


class BridgeProjection:
    """Read-only formatter for the optional, finalized Bridge Output mapping.

    The constructor receives only final selection/audit facts.  It owns newly
    allocated dictionaries and indexes and does not mutate detector data,
    lifecycle state, or legacy serializer output.
    """

    def __init__(
        self,
        *,
        direction: str,
        market: MarketContext,
        prepared_order_audit: list[object],
        order_direction: str,
    ) -> None:
        self.direction = direction
        self.market = market
        self.order_direction = order_direction
        self.audit_by_identity: dict[tuple[int, int], object] = {
            order_identity(
                int(getattr(item["reaction"], "first_idx")),
                int(getattr(item["reaction"], "break_idx")),
            ): item
            for item in prepared_order_audit
        }

    def physical_order(self, prepared: object | None) -> dict[str, object] | None:
        """Project one final accepted physical Order by canonical identity."""
        if prepared is None:
            return None
        entry = prepared["entry"]
        reaction = prepared["reaction"]
        first_index = int(getattr(reaction, "first_idx"))
        break_index = int(getattr(reaction, "break_idx"))
        if not (
            0 <= first_index < len(self.market.candles)
            and 0 <= break_index < len(self.market.candles)
        ):
            return None
        crossed = prepared.get("crossed")
        stop_time = crossed[1] if crossed is not None else None
        stop_event_time = crossed[2] if crossed is not None else None
        confirmation = _bridge_reaction_confirmation(
            self.market,
            self.order_direction,
            reaction,
        )
        return {
            "firstCandle": {
                "time": bridge_datetime(
                    getattr(self.market.candles[first_index], "timestamp")
                ),
            },
            "breakoutCandle": {
                "time": bridge_datetime(
                    getattr(self.market.candles[break_index], "timestamp")
                ),
                "eventTime": bridge_datetime(confirmation),
            },
            "stop": {
                "price": str(entry["stop_level"]),
                **_bridge_stop_view(
                    self.market,
                    self.order_direction,
                    entry["stop_level"],
                    stop_time,
                    stop_event_time,
                ),
            },
        }

    def parent_order(self, behavior: object) -> dict[str, object] | None:
        """Return a behavior's recorded formation/decision Order, if final."""
        identity = _bridge_order_identity(behavior)
        return self.physical_order(
            self.audit_by_identity.get(identity) if identity is not None else None
        )

    def current_order(
        self,
        behavior: object,
        parent_type: str,
        parent_family: str | None,
        strict_stop_event: datetime | None,
    ) -> dict[str, object] | None:
        """Resolve a creator Order only from an exact final parent-stop cause.

        This intentionally declines to infer ownership from a behavior's
        formation Order, timestamps, row order, Reset-leg provenance, or a
        provisional Order.  A conflict or a missing exact cause returns null.
        """
        if strict_stop_event is None:
            return None
        source_time = getattr(behavior, "source_time", None)
        if source_time is None:
            return None
        matching: dict[tuple[int, int], object] = {}
        for identity, prepared in self.audit_by_identity.items():
            for cause in prepared["causes"]:
                if cause.get("kind") != "parent-stop":
                    continue
                if (
                    cause.get("parentType") != parent_type
                    or cause.get("parentSourceTime") != source_time
                    or cause.get("eventTime") != strict_stop_event
                ):
                    continue
                recorded_family = cause.get("parentFamily")
                if parent_family is None:
                    if recorded_family not in (None, ""):
                        continue
                elif recorded_family != parent_family:
                    continue
                matching[identity] = prepared
        if len(matching) != 1:
            return None
        return self.physical_order(next(iter(matching.values())))

    def order_audit(self, prepared: object) -> dict[str, object]:
        """Project final accepted audit evidence using the physical formatter."""
        entry = prepared["entry"]
        reaction = prepared["reaction"]
        physical = self.physical_order(prepared)
        if physical is None:
            raise RuntimeError("Bridge Output received an invalid final Order Audit")
        causes = []
        for cause in prepared["causes"]:
            if cause["kind"] == "parent-stop":
                causes.append({
                    "kind": "parent-stop",
                    "parentType": cause["parentType"],
                    "parentFamily": bridge_color(cause["parentFamily"]),
                    "eventTime": bridge_datetime(cause["eventTime"]),
                    "parentSourceTime": bridge_datetime(cause["parentSourceTime"]),
                })
            elif cause["kind"] == "blue-leg":
                causes.append({
                    "kind": "blue-leg",
                    "resetTime": bridge_datetime(cause["resetTime"]),
                    "nextBreakoutTime": bridge_datetime(cause["nextBreakoutTime"]),
                    "legLevel": cause["legLevel"],
                    "levelSourceIndex": cause["levelSourceIndex"],
                    "levelSourceTime": bridge_datetime(cause["levelSourceTime"]),
                    "blueSourceTime": bridge_datetime(cause["blueSourceTime"]),
                    "strictBreakTime": bridge_datetime(cause["strictBreakTime"]),
                    "blueFormationEventTime": bridge_datetime(cause["blueFormationEventTime"]),
                    "legStartBreakoutTime": bridge_datetime(cause["legStartBreakoutTime"]),
                    "previousBreakoutTime": bridge_datetime(cause["previousBreakoutTime"]),
                })
            else:
                causes.append({
                    "kind": "reset-leg",
                    "resetTime": bridge_datetime(cause["resetTime"]),
                    "boundaryBreakTime": bridge_datetime(cause["boundaryBreakTime"]),
                })
        return {
            "type": "Order Audit",
            "direction": bridge_direction(self.order_direction),
            "mode": bridge_mode(getattr(reaction, "mode")),
            "firstCandle": {
                "index": int(getattr(reaction, "first_idx")),
                **physical["firstCandle"],
            },
            "structure": {
                "boxTop": {
                    "time": bridge_datetime(
                        getattr(reaction, "box_top_source_time", None)
                    ),
                    "price": str(getattr(reaction, "box_top", None)),
                },
                "boxBottom": {
                    "time": bridge_datetime(
                        getattr(reaction, "box_bottom_source_time", None)
                    ),
                    "price": str(getattr(reaction, "box_bottom", None)),
                },
                "breakoutCandle": {
                    "index": int(getattr(reaction, "break_idx")),
                    **physical["breakoutCandle"],
                },
            },
            "stop": {
                "level": str(entry["stop_level"]),
                "sourceTime": bridge_datetime(entry["stop_source_time"]),
                "stoppedAt": {
                    "time": physical["stop"]["time"],
                    "eventTime": physical["stop"]["eventTime"],
                },
            },
            "causes": causes,
        }


def _bridge_parent_stop(
    projection: BridgeProjection,
    detector: object | None,
    parent_type: str,
    item: object,
) -> tuple[datetime | None, datetime | None]:
    """Read an existing E-lifecycle stop; never perform a new stop search."""
    if detector is None:
        return None, None
    try:
        found = detector.parent_stop(parent_type, item)
    except (AttributeError, TypeError, ValueError):
        return None, None
    if found is None:
        return None, None
    index, event_time = found
    if not 0 <= int(index) < len(projection.market.candles):
        return None, None
    return getattr(projection.market.candles[int(index)], "timestamp"), event_time


def _bridge_a_stop(
    projection: BridgeProjection,
    s_detector: object | None,
    item: object,
) -> tuple[datetime | None, datetime | None]:
    """Read the already-authoritative S-stage first A stop."""
    if s_detector is None:
        return None, None
    try:
        found = s_detector.first_a_stop(
            as_decimal(getattr(item, "price")),
            s_detector._a_confirmation_time(item),
        )
    except (AttributeError, IndexError, TypeError, ValueError):
        return None, None
    if found is None:
        return None, None
    _index, main_time, event_time = found
    return main_time, event_time


def _bridge_behavior_stop(
    projection: BridgeProjection,
    direction: str,
    price: object,
    stop_time: datetime | None,
    stop_event_time: datetime | None,
) -> dict[str, object]:
    return {
        **_bridge_stop_view(
            projection.market, direction, price, stop_time, stop_event_time
        ),
        "price": str(price),
    }


def _bridge_blue_formation(
    projection: BridgeProjection,
    direction: str,
    line: object,
    reactions: list[object],
) -> tuple[datetime | None, datetime | None]:
    if str(getattr(line, "kind", "")).lower() != "scale":
        return getattr(line, "source_time", None), None
    reaction_number = int(getattr(line, "reaction_number"))
    if not 1 <= reaction_number <= len(reactions):
        return None, None
    reaction = reactions[reaction_number - 1]
    break_index = int(getattr(reaction, "break_idx"))
    if not 0 <= break_index < len(projection.market.candles):
        return None, None
    return (
        getattr(projection.market.candles[break_index], "timestamp"),
        _bridge_reaction_confirmation(
            projection.market, direction, reaction, use_intrabar_start=False
        ),
    )


def _bridge_project_reaction(
    projection: BridgeProjection,
    direction: str,
    raw: object,
    public: object,
) -> dict[str, object]:
    first_index = int(getattr(raw, "first_idx"))
    break_index = int(getattr(raw, "break_idx"))
    return {
        "type": "Reaction",
        "direction": bridge_direction(direction),
        "mode": bridge_mode(getattr(public, "mode")),
        "firstCandle": {
            "color": bridge_color(
                getattr(projection.market.candles[first_index], "tag")
            ),
            "time": bridge_datetime(
                getattr(projection.market.candles[first_index], "timestamp")
            ),
        },
        "structure": {
            "boxTop": {
                "time": bridge_datetime(getattr(public, "box_top_source_time")),
                "price": str(getattr(public, "box_top")),
            },
            "boxBottom": {
                "time": bridge_datetime(getattr(public, "box_bottom_source_time")),
                "price": str(getattr(public, "box_bottom")),
            },
            "breakoutCandle": {
                "time": bridge_datetime(
                    getattr(projection.market.candles[break_index], "timestamp")
                ),
                "eventTime": bridge_datetime(
                    _bridge_reaction_confirmation(
                        projection.market, direction, raw
                    )
                ),
            },
        },
    }


def _bridge_project_reset(
    projection: BridgeProjection,
    direction: str,
    reset: object,
) -> dict[str, object]:
    first_index = int(getattr(reset, "from_first_idx"))
    previous_time = (
        getattr(projection.market.candles[first_index], "timestamp")
        if 0 <= first_index < len(projection.market.candles)
        else None
    )
    return {
        "type": "Reset",
        "direction": bridge_direction(direction),
        "occurredAt": {
            "time": bridge_datetime(getattr(reset, "display_time", None)),
            "eventTime": bridge_datetime(getattr(reset, "second_time", None)),
        },
        "previousReaction": {"firstCandle": {"time": bridge_datetime(previous_time)}},
        "brokenLevel": str(getattr(reset, "broken_level")),
    }


def _bridge_project_blue(
    projection: BridgeProjection,
    direction: str,
    line: object,
    reactions: list[object],
) -> dict[str, object]:
    formation_time, formation_event_time = _bridge_blue_formation(
        projection, direction, line, reactions
    )
    kind = str(getattr(line, "kind", "")).lower()
    output: dict[str, object] = {
        "type": "Blue Line",
        "direction": bridge_direction(direction),
        "formation": {"scale": "Scale", "reset": "Reset"}.get(kind),
        "formedAt": {
            "time": bridge_datetime(formation_time),
            "eventTime": bridge_datetime(formation_event_time),
        },
        "line": {
            "price": str(getattr(line, "line_price")),
            "sourceExtreme": str(getattr(line, "source_extreme")),
        },
        # The final bridge does not retain standalone BlueState stop evidence.
        # Returning null is deliberate: creating a detector here would be a
        # second calculation instead of a read-only projection.
        "stop": {
            "time": None,
            "eventTime": None,
            "price": str(getattr(line, "source_extreme")),
        },
    }
    if kind == "reset":
        output["brokenLevel"] = str(getattr(line, "broken_level"))
    return output


def _bridge_full_lines_by_ordinal(lines: list[object]) -> dict[int, object]:
    ordered = sorted(
        lines,
        key=lambda item: (
            int(getattr(item, "reaction_number")),
            getattr(item, "source_time"),
            str(getattr(item, "kind")),
        ),
    )
    return {ordinal: line for ordinal, line in enumerate(ordered, start=1)}


def _bridge_project_a(
    projection: BridgeProjection,
    direction: str,
    item: object,
    lines_by_ordinal: dict[int, object],
    reactions: list[object],
    s_detector: object | None,
) -> dict[str, object]:
    first_line = lines_by_ordinal.get(int(getattr(item, "blue_1_ordinal")))
    second_line = lines_by_ordinal.get(int(getattr(item, "blue_2_ordinal")))
    first_formation, _first_formation_event = (
        _bridge_blue_formation(projection, direction, first_line, reactions)
        if first_line is not None
        else (None, None)
    )
    second_formation, _second_formation_event = (
        _bridge_blue_formation(projection, direction, second_line, reactions)
        if second_line is not None
        else (None, None)
    )
    stop_time, stop_event_time = _bridge_a_stop(projection, s_detector, item)
    strict_stop_event = _bridge_proven_strict_event(
        projection.market, direction, getattr(item, "price"), stop_event_time
    )
    reaction_number = int(getattr(item, "reaction_number"))
    reaction = (
        reactions[reaction_number - 1]
        if 1 <= reaction_number <= len(reactions)
        else None
    )
    route = getattr(item, "formation_route", None)
    return {
        "type": "A",
        "direction": bridge_direction(direction),
        "formation": {"ordinary": "Type-1", "double-stop": "Type-2"}.get(route),
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "blueLines": {
            "first": {
                "formedAt": {"time": bridge_datetime(first_formation)},
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    getattr(item, "blue_1_stop_level"),
                    getattr(item, "blue_1_stop_time"),
                    getattr(item, "blue_1_stop_event_time", None),
                ),
                "stopLevel": str(getattr(item, "blue_1_stop_level")),
            },
            "second": {
                "formedAt": {"time": bridge_datetime(second_formation)},
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    getattr(item, "blue_2_stop_level"),
                    getattr(item, "blue_2_stop_time"),
                    getattr(item, "blue_2_stop_event_time", None),
                ),
                "stopLevel": str(getattr(item, "blue_2_stop_level")),
            },
        },
        "reaction": {
            "startedAt": {
                "time": bridge_datetime(getattr(item, "reaction_first_time")),
            },
            "confirmedAt": {
                "time": bridge_datetime(getattr(item, "reaction_break_time")),
                "eventTime": bridge_datetime(
                    _bridge_reaction_confirmation(
                        projection.market,
                        direction,
                        reaction,
                        use_intrabar_start=False,
                    )
                    if reaction is not None else None
                ),
            },
        },
        "parent": None,
        "currentOrder": projection.current_order(
            item, "A", None, strict_stop_event
        ),
        "stop": _bridge_behavior_stop(
            projection, direction, getattr(item, "price"), stop_time, stop_event_time
        ),
    }


def _bridge_project_s(
    projection: BridgeProjection,
    direction: str,
    item: object,
    e_detector: object | None,
) -> dict[str, object]:
    stop_time, stop_event_time = _bridge_parent_stop(
        projection, e_detector, "S", item
    )
    strict_stop_event = _bridge_proven_strict_event(
        projection.market, direction, getattr(item, "price"), stop_event_time
    )
    color = str(getattr(item, "color", "")).lower()
    formation = None
    if color == "blue":
        formation = {
            "simple": "Type-1",
            "advanced": "Type-2",
            "type3": "Type-3",
            "type4": "Type-4",
        }.get(str(getattr(item, "formation_type", "")).lower())
    return {
        "type": "S",
        "direction": bridge_direction(direction),
        "color": bridge_color(getattr(item, "color")),
        "formation": formation,
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "parent": {
            "behavior": {
                "type": "A",
                "formedAt": {
                    "time": bridge_datetime(getattr(item, "a_source_time")),
                    "price": str(getattr(item, "a_price")),
                },
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    getattr(item, "a_price"),
                    getattr(item, "a_stop_time"),
                    getattr(item, "a_stop_event_time"),
                ),
            },
            "order": projection.parent_order(item),
        },
        "currentOrder": projection.current_order(
            item, "S", str(getattr(item, "color")), strict_stop_event
        ),
        "stop": _bridge_behavior_stop(
            projection, direction, getattr(item, "price"), stop_time, stop_event_time
        ),
    }


def _bridge_source_index(item: object) -> tuple[int, datetime] | None:
    source_index = getattr(item, "source_index", None)
    source_time = getattr(item, "source_time", None)
    if source_index is None or source_time is None:
        return None
    return int(source_index), source_time


def _bridge_parent_behavior_for_e(
    projection: BridgeProjection,
    direction: str,
    item: object,
    s_by_source: dict[tuple[int, datetime], object],
    e_by_source: dict[tuple[int, datetime], object],
    stopall_by_source: dict[tuple[int, datetime], object],
) -> dict[str, object]:
    parent_type = str(getattr(item, "parent_type"))
    parent_identity = (
        int(getattr(item, "parent_source_index")),
        getattr(item, "parent_source_time"),
    )
    parent = None
    color = None
    number = None
    if parent_type == "S":
        parent = s_by_source.get(parent_identity)
        color = bridge_color(getattr(parent, "color", None))
    elif parent_type == "E":
        parent = e_by_source.get(parent_identity)
        color = bridge_color(getattr(parent, "family", None))
        number = getattr(parent, "number", None)
    elif parent_type == "StopAll":
        parent = stopall_by_source.get(parent_identity)
        number = getattr(parent, "number", None)
    return {
        "type": parent_type,
        "color": color,
        "number": number,
        "formedAt": {
            "time": bridge_datetime(getattr(item, "parent_source_time")),
            "price": str(getattr(item, "parent_price")),
        },
        "stoppedAt": _bridge_stop_view(
            projection.market,
            direction,
            getattr(item, "parent_price"),
            getattr(item, "parent_stop_time"),
            getattr(item, "parent_stop_event_time"),
        ),
    }


def _bridge_project_e(
    projection: BridgeProjection,
    direction: str,
    item: object,
    e_detector: object | None,
    s_by_source: dict[tuple[int, datetime], object],
    e_by_source: dict[tuple[int, datetime], object],
    stopall_by_source: dict[tuple[int, datetime], object],
) -> dict[str, object]:
    stop_time, stop_event_time = _bridge_parent_stop(
        projection, e_detector, "E", item
    )
    strict_stop_event = _bridge_proven_strict_event(
        projection.market, direction, getattr(item, "price"), stop_event_time
    )
    return {
        "type": "E",
        "direction": bridge_direction(direction),
        "color": bridge_color(getattr(item, "family")),
        "number": int(getattr(item, "number")),
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "parent": {
            "behavior": _bridge_parent_behavior_for_e(
                projection,
                direction,
                item,
                s_by_source,
                e_by_source,
                stopall_by_source,
            ),
            "order": projection.parent_order(item),
        },
        "currentOrder": projection.current_order(
            item,
            f"E{int(getattr(item, 'number'))}",
            str(getattr(item, "family")),
            strict_stop_event,
        ),
        "stop": _bridge_behavior_stop(
            projection, direction, getattr(item, "price"), stop_time, stop_event_time
        ),
    }


def _bridge_project_stopall(
    projection: BridgeProjection,
    direction: str,
    item: object,
) -> dict[str, object]:
    donor_type = getattr(item, "donor_type", None)
    donor_price = getattr(item, "donor_price", None)
    donor_stop_time = getattr(item, "donor_stop_time", None)
    donor_stop_event_time = getattr(item, "donor_stop_event_time", None)
    own_stop_event = _bridge_proven_strict_event(
        projection.market,
        direction,
        getattr(item, "price"),
        getattr(item, "stop_event_time"),
    )
    formation = {
        "sequence-group-stop": "Type-1",
        "stopall-stop": "Type-2",
        "opposite-s-group-stop": "Type-3",
    }.get(getattr(item, "gate_type", None))
    return {
        "type": "StopAll",
        "direction": bridge_direction(direction),
        "number": int(getattr(item, "number")),
        "formation": formation,
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "parent": {
            "behavior": {
                "type": donor_type,
                "color": bridge_color(getattr(item, "donor_color", None)),
                "number": getattr(item, "donor_number", None),
                "formedAt": {
                    "time": bridge_datetime(
                        getattr(item, "donor_source_time", None)
                    ),
                    "price": str(donor_price) if donor_price is not None else None,
                },
                # Donor stop metadata remains independent from the group-level
                # gate. Type-3 S-Red promotion consequently keeps this null
                # unless an actual donor stop was retained.
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    donor_price,
                    donor_stop_time,
                    donor_stop_event_time,
                ),
            },
            "order": projection.parent_order(item),
        },
        "currentOrder": projection.current_order(
            item,
            f"StopAll{int(getattr(item, 'number'))}",
            None,
            own_stop_event,
        ),
        "stop": _bridge_behavior_stop(
            projection,
            direction,
            getattr(item, "price"),
            getattr(item, "stop_time"),
            getattr(item, "stop_event_time"),
        ),
    }


def _bridge_audit_order_key(
    prepared: object, detector: object,
) -> tuple[int, int]:
    reaction = prepared["reaction"]
    return (
        epoch(detector.candles[int(getattr(reaction, "first_idx"))].timestamp),
        epoch(detector.candles[int(getattr(reaction, "break_idx"))].timestamp),
    )


def build_bridge_output(
    direction: str,
    market: MarketContext,
    state: PipelineState,
    visibility: DirectionVisibilityState,
    selected_reactions: list[tuple[object, object]],
    selected_resets: list[object],
    selected_blue_lines: list[object],
    selected_a_zones: list[object],
    selected_s_zones: list[object],
    selected_e_zones: list[object],
    selected_stopalls: list[object],
    selected_order_audit: list[object],
) -> dict[str, list[dict[str, object]]]:
    """Build the opt-in YAML-facing mapping from final legacy selections.

    Callers pass the exact lists used by every legacy serializer. Array
    positions are therefore display alignment only; behavior and Order joins
    use source identities and final audit causes rather than list indexes.
    """
    e_detector = state.full_e_detectors.get(direction)
    s_detector = state.full_s_detectors.get(direction)
    order_direction = (
        str(getattr(e_detector, "order_direction"))
        if e_detector is not None
        else ("bearish" if direction == "bullish" else "bullish")
    )
    projection = BridgeProjection(
        direction=direction,
        market=market,
        prepared_order_audit=selected_order_audit,
        order_direction=order_direction,
    )
    full_lines = state.full_lines_by_direction.get(direction, visibility.blue_lines)
    lines_by_ordinal = _bridge_full_lines_by_ordinal(list(full_lines))
    full_s = getattr(visibility, "projection_s_zones", selected_s_zones)
    full_e = getattr(visibility, "projection_e_zones", selected_e_zones)
    full_stopalls = getattr(visibility, "projection_stopalls", selected_stopalls)
    s_by_source = {
        identity: item
        for item in full_s
        for identity in [_bridge_source_index(item)]
        if identity is not None
    }
    e_by_source = {
        identity: item
        for item in [*full_e, *selected_e_zones]
        for identity in [_bridge_source_index(item)]
        if identity is not None
    }
    stopall_by_source = {
        identity: item
        for item in [*full_stopalls, *selected_stopalls]
        for identity in [_bridge_source_index(item)]
        if identity is not None
    }
    raw_reactions = state.results[direction].reactions
    return {
        "reactions": [
            _bridge_project_reaction(projection, direction, raw, public)
            for raw, public in selected_reactions
        ],
        "resets": [
            _bridge_project_reset(projection, direction, item)
            for item in selected_resets
        ],
        "blueLines": [
            _bridge_project_blue(projection, direction, item, raw_reactions)
            for item in selected_blue_lines
        ],
        "aZones": [
            _bridge_project_a(
                projection,
                direction,
                item,
                lines_by_ordinal,
                raw_reactions,
                s_detector,
            )
            for item in selected_a_zones
        ],
        "sZones": [
            _bridge_project_s(projection, direction, item, e_detector)
            for item in selected_s_zones
        ],
        "eZones": [
            _bridge_project_e(
                projection,
                direction,
                item,
                e_detector,
                s_by_source,
                e_by_source,
                stopall_by_source,
            )
            for item in selected_e_zones
        ],
        "stopAlls": [
            _bridge_project_stopall(projection, direction, item)
            for item in selected_stopalls
        ],
        "orderAudit": [projection.order_audit(item) for item in selected_order_audit],
    }


def validate_order_audit_bridge(
    prepared_items, s_zones, e_zones, stopalls,
) -> None:
    """Assert that public behavior Order provenance matches canonical OrderAudit.

    This is a bridge consistency invariant only; it does not choose, rank, or
    reconstruct Orders.  All trading ownership decisions remain in the
    calculation engines.  Every public S/E/StopAll carrying a physical Order
    identity must reference an identity retained by the already-resolved audit.
    The resolved audit must also keep one owner per exact parent-stop cause.
    """
    audit_identities = {
        order_identity(
            int(getattr(item["reaction"], "first_idx")),
            int(getattr(item["reaction"], "break_idx")),
        )
        for item in prepared_items
    }

    missing: list[str] = []
    for behavior_type, items in (
        ("S", s_zones), ("E", e_zones), ("StopAll", stopalls)
    ):
        for item in items:
            first_index = getattr(item, "order_first_index", None)
            break_index = getattr(item, "order_break_index", None)
            if first_index is None or break_index is None:
                continue
            identity = order_identity(int(first_index), int(break_index))
            if identity in audit_identities:
                continue
            missing.append(
                f"{behavior_type}@{getattr(item, 'source_time', None)!s}"
                f"->{identity}"
            )
    if missing:
        raise RuntimeError(
            "OrderAudit bridge invariant failed; public behavior references "
            "an Order identity absent from canonical audit: " + ", ".join(missing)
        )

    parent_owner: dict[tuple[object, object, object, object], tuple[int, int]] = {}
    duplicate_parent_causes: list[str] = []
    for prepared in prepared_items:
        reaction = prepared["reaction"]
        identity = order_identity(
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
        )
        for cause in prepared["causes"]:
            if cause.get("kind") != "parent-stop":
                continue
            key = (
                cause.get("parentType"),
                cause.get("parentFamily"),
                cause.get("eventTime"),
                cause.get("parentSourceTime"),
            )
            previous = parent_owner.setdefault(key, identity)
            if previous != identity:
                duplicate_parent_causes.append(f"{key!r}:{previous}->{identity}")
    if duplicate_parent_causes:
        raise RuntimeError(
            "OrderAudit bridge invariant failed; one exact parent-stop owns "
            "multiple physical Orders: " + ", ".join(duplicate_parent_causes)
        )


def serialize_order_audit(prepared_items, detector):
    """Serialize already-resolved Order Audit identities without business filtering."""
    output = []
    for prepared in prepared_items:
        entry = prepared["entry"]
        reaction = prepared["reaction"]
        crossed = prepared["crossed"]
        first_index = int(getattr(reaction, "first_idx"))
        causes = []
        for cause in prepared["causes"]:
            if cause["kind"] == "parent-stop":
                causes.append({
                    "kind": cause["kind"],
                    "parentType": cause["parentType"],
                    "parentFamily": cause["parentFamily"],
                    "eventTime": epoch(cause["eventTime"]),
                    "parentSourceTime": epoch(cause["parentSourceTime"]),
                })
            elif cause["kind"] == "blue-leg":
                causes.append({
                    "kind": "blue-leg",
                    "resetTime": epoch(cause["resetTime"]),
                    "nextBreakoutTime": (epoch(cause["nextBreakoutTime"])
                                         if cause["nextBreakoutTime"] is not None else None),
                    "legLevel": cause["legLevel"],
                    "levelSourceIndex": cause["levelSourceIndex"],
                    "levelSourceTime": epoch(cause["levelSourceTime"]),
                    "blueSourceTime": epoch(cause["blueSourceTime"]),
                    "strictBreakTime": epoch(cause["strictBreakTime"]),
                    "blueFormationEventTime": epoch(cause["blueFormationEventTime"]),
                    "legStartBreakoutTime": epoch(cause["legStartBreakoutTime"]),
                    "previousBreakoutTime": epoch(cause["previousBreakoutTime"]),
                })
            else:
                causes.append({
                    "kind": cause["kind"],
                    "resetTime": epoch(cause["resetTime"]),
                    "boundaryBreakTime": epoch(cause["boundaryBreakTime"]),
                })
        output.append({
            "direction": detector.order_direction,
            "reactionNumber": int(
                getattr(reaction, "behavior_public_number", None)
                or entry["reaction_number"]
            ),
            "reactionMode": str(getattr(reaction, "mode")),
            "firstIndex": first_index,
            "firstTime": epoch(detector.candles[first_index].timestamp),
            "boxTopSourceIndex": int(getattr(reaction, "box_top_source_idx")),
            "boxTopSourceTime": display_epoch(getattr(reaction, "box_top_source_time")),
            "boxTop": str(getattr(reaction, "box_top")),
            "boxBottomSourceIndex": int(getattr(reaction, "box_bottom_source_idx")),
            "boxBottomSourceTime": display_epoch(getattr(reaction, "box_bottom_source_time")),
            "boxBottom": str(getattr(reaction, "box_bottom")),
            "breakIndex": int(getattr(reaction, "break_idx")),
            "breakTime": epoch(
                detector.candles[int(getattr(reaction, "break_idx"))].timestamp
            ),
            "stopLevel": str(entry["stop_level"]),
            "stopSourceIndex": entry["stop_source_index"],
            "stopSourceTime": epoch(entry["stop_source_time"]),
            "stopHitIndex": crossed[0] if crossed is not None else None,
            "stopHitTime": epoch(crossed[1]) if crossed is not None else None,
            "stopHitEventTime": epoch(crossed[2]) if crossed is not None else None,
            "causes": causes,
        })
    return sorted(output, key=lambda item: (item["firstTime"], item["breakTime"]))


@dataclass(frozen=True, slots=True)
class EngineBundle:
    reaction: object
    blue_line: object
    a_zone: object
    s_zone: object
    e_zone: object | None
    lifecycle: object | None


@dataclass(frozen=True, slots=True)
class MarketContext:
    seconds: list[object]
    candles: list[object]
    lower_index: object
    chronology: object
    start_index: int
    end_index: int


def parse_arguments(argv=None):
    """Parse and validate the production pipeline command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reaction-engine",
        "--engine",
        dest="reaction_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--blue-line-engine",
        "--blue-engine",
        dest="blue_line_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--a-zone-engine",
        "--a-engine",
        dest="a_zone_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--s-zone-engine",
        "--s-engine",
        dest="s_zone_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--e-zone-engine",
        "--e-engine",
        dest="e_zone_engine",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--lifecycle-engine",
        "--stopall-engine",
        dest="lifecycle_engine",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--blue-lines", choices=("enabled", "disabled"), default="enabled"
    )
    parser.add_argument(
        "--a-zones", choices=("enabled", "disabled"), default="enabled"
    )
    parser.add_argument(
        "--s-zones", choices=("enabled", "disabled"), default="enabled"
    )
    parser.add_argument(
        "--bridge-output",
        action="store_true",
        help="Add the presentation-only Bridge Output projection.",
    )
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--timeframe", type=int, required=True)
    parser.add_argument("--from-time", type=int, required=True)
    parser.add_argument("--to-time", type=int, required=True)
    parser.add_argument(
        "--direction", choices=("bullish", "bearish", "both"), required=True
    )
    args = parser.parse_args(argv)
    if args.timeframe < 1:
        raise ValueError("Timeframe must be at least one second.")
    return args


def load_engines(args, timings: dict[str, float]) -> EngineBundle:
    """Load every configured calculation engine exactly once."""
    reaction = timed(
        timings, "Load Reaction engine", lambda: load_engine(args.reaction_engine)
    )
    blue_line = timed(
        timings,
        "Load Blue Line engine",
        lambda: load_module("blue_line_detector", args.blue_line_engine),
    )
    a_zone = timed(
        timings, "Load A engine", lambda: load_module("a_zone_detector", args.a_zone_engine)
    )
    s_zone = timed(
        timings, "Load S engine", lambda: load_module("s_zone_detector", args.s_zone_engine)
    )
    e_zone = (
        timed(
            timings,
            "Load E engine",
            lambda: load_module("e_zone_detector", args.e_zone_engine),
        )
        if args.e_zone_engine is not None
        else None
    )
    lifecycle_path = args.lifecycle_engine or (_PIPELINE_DIR / "lifecycle_engine.py")
    lifecycle = timed(
        timings,
        "Load Lifecycle engine",
        lambda: load_module("lifecycle_engine", lifecycle_path),
    )
    return EngineBundle(reaction, blue_line, a_zone, s_zone, e_zone, lifecycle)


def prepare_market_context(
    args, engines: EngineBundle, timings: dict[str, float]
) -> MarketContext:
    """Read, isolate, normalize and index the selected raw-data range."""
    source_bytes = timed(
        timings, "Read source file", lambda: args.data.read_bytes()
    )
    # Match the former ``utf-8-sig`` behavior without decoding the entire raw
    # payload to a Python string before orjson parses it.
    source_bytes = source_bytes.removeprefix(b"\xef\xbb\xbf")
    source_rows = timed(
        timings, "Parse source JSON", lambda: orjson.loads(source_bytes)
    )
    # A requested time range is a presentation window only.  Reaction state
    # can remain open past ``to_time`` and be resolved by later RAW chronology;
    # truncating calculation at the visible end manufactures provisional
    # Reactions/Blue/A state that does not exist in a full-file run.  Calculate
    # on the complete physical RAW and apply from/to only during serialization.
    rows = timed(
        timings,
        "Use full RAW calculation context",
        lambda: source_rows,
    )
    if not rows:
        raise ValueError("The selected range contains no raw candles.")

    second_buckets, timeframe_buckets = timed(
        timings,
        "Normalize raw candles",
        lambda: build_candle_buckets(rows, args.timeframe),
    )
    seconds = timed(
        timings,
        "Build lower candle views",
        lambda: build_candle_objects(engines.reaction, second_buckets),
    )
    lower_index = engines.reaction.shared_lower_timeframe_index(seconds)
    candles = (
        seconds
        if args.timeframe == 1
        else timed(
            timings,
            "Build timeframe candle views",
            lambda: build_candle_objects(engines.reaction, timeframe_buckets),
        )
    )
    chronology = engines.reaction.MarketChronology(
        candles, seconds, args.timeframe, lower_index
    )

    # Resolve the visible main-candle range inside the prefix calculation.
    # Bucket boundaries are epoch-aligned exactly as ``build_candle_buckets``
    # constructs them, which also keeps full-run source indexes/ordinals
    # stable in a short-window request.
    main_bucket_times = [int(item["time"]) for item in timeframe_buckets]
    requested_start_bucket = (
        args.from_time
        if args.timeframe == 1
        else args.from_time // args.timeframe * args.timeframe
    )
    requested_end_bucket = (
        args.to_time
        if args.timeframe == 1
        else args.to_time // args.timeframe * args.timeframe
    )
    start_index = bisect_left(main_bucket_times, requested_start_bucket)
    end_index = bisect_left(main_bucket_times, requested_end_bucket + args.timeframe) - 1
    if start_index >= len(candles) or end_index < start_index:
        raise ValueError("The selected range contains no timeframe candles.")
    end_index = min(end_index, len(candles) - 1)

    return MarketContext(
        seconds=seconds,
        candles=candles,
        lower_index=lower_index,
        chronology=chronology,
        start_index=start_index,
        end_index=end_index,
    )

@dataclass(slots=True)
class PipelineState:
    """Mutable calculation state shared across direction serialization passes."""

    directions: tuple[str, ...]
    results: dict[str, object]
    reusable_full_context: bool
    initial_order_geometry: dict[str, object]
    internal_reaction_identities: dict[str, set[tuple[int, int]]]
    full_e_zones: dict[str, list[object]]
    full_e_detectors: dict[str, object]
    full_s_detectors: dict[str, object]
    full_lines_by_direction: dict[str, list[object]]
    full_a_by_direction: dict[str, list[object]]
    invalid_a_identities_by_direction: dict[str, set[tuple[datetime, int]]]
    invalid_s_identities_by_direction: dict[str, set[tuple[datetime, int]]]
    full_s_by_direction: dict[str, list[object]]
    full_s_candidates_by_direction: dict[str, list[object]]


@dataclass(slots=True)
class FullDirectionState:
    """Authoritative full-range behavior state for one trend direction."""

    e_zones: list[object]
    e_detector: object
    s_detector: object
    blue_lines: list[object]
    a_zones: list[object]
    invalid_a_identities: set[tuple[datetime, int]]
    invalid_s_identities: set[tuple[datetime, int]]
    s_zones: list[object]
    s_candidates: list[object]


def create_e_detector(
    direction: str,
    e_engine,
    full_results: dict[str, object],
    s_zones: list[object],
    chronology,
    geometry_detectors: dict[str, object],
    initial_order_audit,
    lifecycle_engine,
    *,
    blocked_order_first_times: set[datetime] | None = None,
    invalid_s_root_identities: set[tuple[datetime, int]] | None = None,
    trend_blue_lines: Sequence[object] = (),
):
    """Construct one E detector from the shared geometry/lifecycle contract."""
    opposite = chronology.opposite_direction(direction)
    end_index = len(chronology.candles) - 1

    def bounded_geometry(geometry_direction, geometry_start, geometry_end):
        """Return raw Reaction geometry inside a closed main-candle range."""
        return geometry_detectors[geometry_direction].first_geometry_after_reset(
            geometry_direction,
            max(0, geometry_start - 1),
            geometry_end,
        )

    def direct_geometry(
        geometry_direction, geometry_start, geometry_end, gate_event
    ):
        return geometry_detectors[geometry_direction].first_order_reaction_after_gate(
            geometry_direction,
            geometry_start,
            geometry_end,
            gate_event,
        )

    return e_engine.EZoneDetector(
        direction,
        full_results[direction].reactions,
        full_results[opposite].reactions,
        s_zones,
        full_results[direction].resets,
        full_results[opposite].resets,
        chronology,
        0,
        end_index,
        bounded_geometry,
        direct_geometry,
        blocked_order_first_times=blocked_order_first_times,
        initial_order_audit=initial_order_audit,
        sequence_priority=lifecycle_engine.sequence_priority,
        invalid_s_root_identities=invalid_s_root_identities,
        trend_blue_lines=trend_blue_lines,
    )


def calculate_full_direction_state(
    direction: str,
    engines: EngineBundle,
    market: MarketContext,
    full_results: dict[str, object],
    geometry_detectors: dict[str, object],
    initial_order_geometry: dict[str, object],
    timings: dict[str, float],
) -> FullDirectionState:
    """Run Blue→A→S→E calculation and lifecycle reconciliation for one direction."""
    blue_engine = engines.blue_line
    a_engine = engines.a_zone
    s_engine = engines.s_zone
    e_engine = engines.e_zone
    lifecycle_engine = engines.lifecycle
    assert e_engine is not None
    candles = market.candles
    chronology = market.chronology
    opposite = engines.reaction.opposite_direction(direction)

    blue_lines = timed(
        timings,
        f"Blue Line • {direction.title()}",
        lambda: blue_engine.detect_blue_lines(
            direction,
            full_results[direction].reactions,
            chronology,
            full_results[direction].resets,
        ),
    )
    a_zones = timed(
        timings,
        f"A • {direction.title()}",
        lambda: a_engine.detect_a_zones(
            direction,
            full_results[direction].reactions,
            blue_lines,
            chronology,
        ),
    )
    s_detector = s_engine.SZoneDetector(
        direction,
        full_results[direction].reactions,
        full_results[opposite].reactions,
        blue_lines,
        a_zones,
        chronology,
        0,
        len(candles) - 1,
        full_results[opposite].resets,
        initial_order_geometry=initial_order_geometry[direction],
    )
    s_zones = timed(timings, f"S • {direction.title()}", s_detector.detect)
    s_candidates = list(s_zones)

    historical_e_rescues: list[object] = []
    accepted_e_history: list[object] = []

    def collect_accepted_e_history(zones) -> None:
        existing = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in accepted_e_history
        }
        for item in zones:
            # Keep this safeguard intentionally narrow: only E-parented Blue
            # Orders carrying the independent Order_B/reset-leg cause are
            # eligible for later-pass historical preservation.
            if str(getattr(item, "parent_type", "")).upper() != "E":
                continue
            if str(getattr(item, "family", "")).lower() != "blue":
                continue
            if "reset-leg" not in {
                str(value) for value in getattr(item, "order_causes", ())
            }:
                continue
            identity = (
                int(getattr(item, "source_index")),
                getattr(item, "source_time"),
            )
            if identity not in existing:
                accepted_e_history.append(item)
                existing.add(identity)

    def collect_historical_e_rescues(detector) -> None:
        existing = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in historical_e_rescues
        }
        for item in getattr(detector, "historical_rescued_zones", []):
            identity = (
                int(getattr(item, "source_index")),
                getattr(item, "source_time"),
            )
            if identity not in existing:
                historical_e_rescues.append(item)
                existing.add(identity)

    e_detector = create_e_detector(
        direction,
        e_engine,
        full_results,
        s_zones,
        chronology,
        geometry_detectors,
        s_detector.order_audit,
        lifecycle_engine,
        trend_blue_lines=blue_lines,
    )
    e_zones = timed(
        timings, f"E • {direction.title()} • initial", e_detector.detect
    )
    collect_historical_e_rescues(e_detector)
    collect_accepted_e_history(e_zones)
    valid_s_zones = lifecycle_engine.s_zones_for_module_engines(
        s_zones, e_zones, direction
    )
    if len(valid_s_zones) != len(s_zones):
        e_detector = create_e_detector(
            direction,
            e_engine,
            full_results,
            valid_s_zones,
            chronology,
            geometry_detectors,
            s_detector.order_audit,
            lifecycle_engine,
            blocked_order_first_times={
                getattr(item, "source_time")
                for item in s_zones
                if item not in valid_s_zones
            },
            trend_blue_lines=blue_lines,
        )
        e_zones = timed(
            timings,
            f"E • {direction.title()} • S reconciliation",
            e_detector.detect,
        )
        collect_historical_e_rescues(e_detector)
        collect_accepted_e_history(e_zones)
        s_zones = valid_s_zones

    candidate_a = lifecycle_engine.visible_a_zones(
        s_detector.eligible_a_zones, s_zones
    )
    candidate_a = lifecycle_engine.visible_a_zones_after_s_stops(
        candidate_a, s_zones, candles
    )
    stage_invalid_a_identities: set[tuple[datetime, int]] = set()
    # Cycle validation must see every S-eligible A, even when a provisional
    # S candidate temporarily hides that A from presentation.  Otherwise a
    # later S reconciliation can remove the provisional S and accidentally
    # resurrect an A that should have been rejected by the stopped S/E owner.
    lifecycle_a_candidates = list(s_detector.eligible_a_zones)
    _calculation_a, invalid_a = lifecycle_engine.split_a_zones_by_dominant_stops(
        lifecycle_a_candidates,
        s_candidates,
        e_zones,
        [],
        candles,
        direction,
        lambda item: e_detector.parent_stop(
            "S" if hasattr(item, "a_source_time") else "E", item
        ),
        trend_reactions=s_detector.trend_reactions,
        confirmation_finder=s_detector.reaction_confirmation_time,
        a_stop_event_finder=lambda item: s_detector.first_a_stop(
            Decimal(str(getattr(item, "price"))),
            s_detector.reaction_confirmation_time(
                s_detector.trend_reactions[int(getattr(item, "reaction_number")) - 1],
                direction,
            ),
        ),
        stage_invalid_a_identities=stage_invalid_a_identities,
    )
    invalid_a_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in invalid_a
    }
    invalid_a_source_times = {source_time for source_time, _ in invalid_a_identities}
    invalid_s = [
        item for item in s_candidates
        if getattr(item, "a_source_time") in invalid_a_source_times
    ]
    invalid_s_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in invalid_s
    }
    stage_invalid_a_source_times = {
        source_time for source_time, _ in stage_invalid_a_identities
    }
    stage_invalid_s_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in s_candidates
        if getattr(item, "a_source_time") in stage_invalid_a_source_times
    }
    # Only S descendants of an A rejected specifically by S-stage ownership
    # are removed from later-stage calculation.  Other suppressed S evidence
    # keeps its established continuation semantics unchanged.
    s_zones = [
        item for item in s_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in stage_invalid_s_identities
    ]

    accepted_a_sources = {
        getattr(item, "source_time")
        for item in s_detector.eligible_a_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in invalid_a_identities
    }
    pending_s_a_sources = {getattr(item, "a_source_time") for item in s_candidates}
    accepted_orders, blocked_order_first_times = lifecycle_engine.resolve_order_context(
        s_detector.order_audit,
        accepted_a_sources,
        set(getattr(e_detector, "blocked_order_first_times", set())),
        invalid_a,
        pending_s_a_sources,
        full_results[opposite].reactions,
        candles,
        direction,
        lambda item: s_detector.first_a_stop(
            Decimal(str(getattr(item, "price"))),
            getattr(item, "source_time"),
        ),
    )
    e_detector = create_e_detector(
        direction,
        e_engine,
        full_results,
        s_zones,
        chronology,
        geometry_detectors,
        accepted_orders,
        lifecycle_engine,
        blocked_order_first_times=blocked_order_first_times,
        invalid_s_root_identities=invalid_s_identities,
        trend_blue_lines=blue_lines,
    )
    e_zones = timed(
        timings, f"E • {direction.title()} • final audit", e_detector.detect
    )
    collect_historical_e_rescues(e_detector)
    collect_accepted_e_history(e_zones)

    # A still-open S candidate may be decided by the strict stop of a later
    # calculation-accepted physical Order in the same chronology.  Reconcile
    # against accepted ledgers only; arbitrary opposite Reactions are never
    # promoted into Orders by this pass.  Rebuild E once when S provenance or
    # decision chronology changes because E consumes S as authoritative input.
    shared_order_entries = [
        *accepted_orders.values(),
        *e_detector.order_audit.values(),
    ]
    reconciled_s_zones = s_detector.reconcile_shared_order_stops(
        s_zones, shared_order_entries
    )
    if reconciled_s_zones != s_zones:
        s_zones = reconciled_s_zones
        reconciled_by_identity = {
            (getattr(item, "a_source_time"), getattr(item, "source_time")): item
            for item in s_zones
        }
        s_candidates = [
            reconciled_by_identity.get(
                (getattr(item, "a_source_time"), getattr(item, "source_time")),
                item,
            )
            for item in s_candidates
        ]
        e_detector = create_e_detector(
            direction,
            e_engine,
            full_results,
            s_zones,
            chronology,
            geometry_detectors,
            accepted_orders,
            lifecycle_engine,
            blocked_order_first_times=blocked_order_first_times,
            invalid_s_root_identities=invalid_s_identities,
            trend_blue_lines=blue_lines,
        )
        e_zones = timed(
            timings,
            f"E • {direction.title()} • shared Order-stop reconciliation",
            e_detector.detect,
        )
        collect_historical_e_rescues(e_detector)
        collect_accepted_e_history(e_zones)

    calculation_s_candidates = [
        item for item in s_candidates
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in stage_invalid_s_identities
    ]
    consumed_s_evidence = lifecycle_engine.consumed_s_evidence_after_larger_stop(
        calculation_s_candidates,
        s_zones,
        e_zones,
        direction,
        lambda item: e_detector.parent_stop("E", item),
        candles,
    )
    for evidence_s, original_owner in consumed_s_evidence:
        owner = next(
            (
                item for item in e_zones
                if int(getattr(item, "source_index")) == int(getattr(original_owner, "source_index"))
                and getattr(item, "source_time") == getattr(original_owner, "source_time")
            ),
            None,
        )
        if owner is None:
            continue
        continuation = e_detector.continuation_chain_from_s(owner, evidence_s)
        e_zones = e_detector.replace_with_earlier_continuation(
            e_zones, owner, continuation
        )

    # Continuation replacement happens after the detector's normal final audit.
    # Rebuild the accepted ledger from the actual final E state so OrderAudit
    # cannot lag behind a branch that the lifecycle has just made authoritative.
    e_zones = e_detector.rebuild_accepted_order_audit(
        e_zones, supplemental_s_zones=[item for item, _ in consumed_s_evidence]
    )

    s_zones = [
        item for item in s_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in invalid_s_identities
    ]

    # Preserve presentation-only historical E acceptance without changing
    # calculation ownership. An earlier accepted E that disappears during a
    # later detector rebuild is recoverable only when it is not merely a
    # hidden intermediate parent of a surviving final E. Hidden intermediate
    # parents remain intentionally non-public; independent accepted history is
    # retained for reporting.
    if accepted_e_history:
        historical_e_rescues.extend(accepted_e_history)
    if historical_e_rescues:
        historical_e_rescues = e_detector.resolve_same_source_conflicts(
            historical_e_rescues
        )
        final_e_ids = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in e_zones
        }
        referenced_e_parent_ids = {
            (
                int(getattr(item, "parent_source_index")),
                getattr(item, "parent_source_time"),
            )
            for item in e_zones
            if str(getattr(item, "parent_type", "")).upper() == "E"
        }
        def blocked_by_dominant_final_e(item) -> bool:
            candidate_priority = lifecycle_engine.sequence_priority(
                "e", str(getattr(item, "family"))
            )
            candidate_decision = getattr(item, "decision_event_time")
            for owner in e_zones:
                if getattr(owner, "source_time") >= getattr(item, "source_time"):
                    continue
                owner_priority = lifecycle_engine.sequence_priority(
                    "e", str(getattr(owner, "family"))
                )
                if owner_priority <= candidate_priority:
                    continue
                stop = e_detector.parent_stop("E", owner)
                if stop is None or stop[1] >= candidate_decision:
                    return True
            return False

        e_detector.historical_rescued_zones = [
            item for item in historical_e_rescues
            if (int(getattr(item, "source_index")), getattr(item, "source_time"))
            not in final_e_ids
            and (int(getattr(item, "source_index")), getattr(item, "source_time"))
            not in referenced_e_parent_ids
            and not blocked_by_dominant_final_e(item)
        ]

    return FullDirectionState(
        e_zones=e_zones,
        e_detector=e_detector,
        s_detector=s_detector,
        blue_lines=blue_lines,
        a_zones=a_zones,
        invalid_a_identities=invalid_a_identities,
        invalid_s_identities=invalid_s_identities,
        s_zones=s_zones,
        s_candidates=s_candidates,
    )


def prepare_pipeline_state(
    args,
    engines: EngineBundle,
    market: MarketContext,
    timings: dict[str, float],
) -> PipelineState:
    """Run shared calculation stages once and retain reusable detector state."""
    engine = engines.reaction
    e_engine = engines.e_zone
    seconds = market.seconds
    candles = market.candles
    chronology = market.chronology
    initial_order_geometry = {
        direction: engine.directional_a_stop_order_finder(
            candles, seconds, direction
        )
        for direction in ("bullish", "bearish")
    }
    directions = ("bullish", "bearish") if args.direction == "both" else (args.direction,)
    behavior_modules_enabled = (
        args.blue_lines == "enabled"
        or args.a_zones == "enabled"
        or args.s_zones == "enabled"
    )
    required_directions = (
        ("bullish", "bearish") if behavior_modules_enabled else directions
    )
    reusable_full_context = e_engine is not None and args.s_zones == "enabled"

    full_e_zones: dict[str, list[object]] = {}
    full_e_detectors: dict[str, object] = {}
    full_s_detectors: dict[str, object] = {}
    full_lines_by_direction: dict[str, list[object]] = {}
    full_a_by_direction: dict[str, list[object]] = {}
    invalid_a_identities_by_direction: dict[str, set[tuple[datetime, int]]] = {}
    invalid_s_identities_by_direction: dict[str, set[tuple[datetime, int]]] = {}
    full_s_by_direction: dict[str, list[object]] = {}
    full_s_candidates_by_direction: dict[str, list[object]] = {}

    if reusable_full_context:
        geometry_detectors = {
            direction: engine.UnifiedReactionDetector(
                candles, seconds, 0, len(candles) - 1, direction
            )
            for direction in ("bullish", "bearish")
        }
        results = {
            direction: timed(
                timings,
                f"Reaction geometry • {direction.title()}",
                detector.detect,
            )
            for direction, detector in geometry_detectors.items()
        }
        _, _, internal_reaction_identities, _ = timed(
            timings,
            "Internal Reaction ownership",
            lambda: engine.build_behavior_reaction_views(results, chronology),
        )
        for direction in directions:
            state = calculate_full_direction_state(
                direction,
                engines,
                market,
                results,
                geometry_detectors,
                initial_order_geometry,
                timings,
            )
            full_e_zones[direction] = state.e_zones
            full_e_detectors[direction] = state.e_detector
            full_s_detectors[direction] = state.s_detector
            full_lines_by_direction[direction] = state.blue_lines
            full_a_by_direction[direction] = state.a_zones
            invalid_a_identities_by_direction[direction] = state.invalid_a_identities
            invalid_s_identities_by_direction[direction] = state.invalid_s_identities
            full_s_by_direction[direction] = state.s_zones
            full_s_candidates_by_direction[direction] = state.s_candidates
    else:
        results = {
            direction: timed(
                timings,
                f"Reaction • {direction.title()}",
                lambda direction=direction: engine.UnifiedReactionDetector(
                    candles, seconds, 0, len(candles) - 1, direction
                ).detect(),
            )
            for direction in required_directions
        }
        if behavior_modules_enabled:
            _, _, internal_reaction_identities, _ = timed(
                timings,
                "Internal Reaction ownership",
                lambda: engine.build_behavior_reaction_views(results, chronology),
            )
        else:
            internal_reaction_identities = {"bullish": set(), "bearish": set()}

    return PipelineState(
        directions=tuple(directions),
        results=results,
        reusable_full_context=reusable_full_context,
        initial_order_geometry=initial_order_geometry,
        internal_reaction_identities=internal_reaction_identities,
        full_e_zones=full_e_zones,
        full_e_detectors=full_e_detectors,
        full_s_detectors=full_s_detectors,
        full_lines_by_direction=full_lines_by_direction,
        full_a_by_direction=full_a_by_direction,
        invalid_a_identities_by_direction=invalid_a_identities_by_direction,
        invalid_s_identities_by_direction=invalid_s_identities_by_direction,
        full_s_by_direction=full_s_by_direction,
        full_s_candidates_by_direction=full_s_candidates_by_direction,
    )


@dataclass(slots=True)
class DirectionRangeState:
    """Unserialized calculation state for one requested direction/range."""

    blue_lines: list[object]
    a_zones: list[object]
    s_candidates: list[object]
    accepted_s_zones: list[object]
    e_zones: list[object]
    invalid_a_identities: set[tuple[datetime, int]]
    invalid_s_identities: set[tuple[datetime, int]]


@dataclass(slots=True)
class DirectionVisibilityState:
    """Final public behavior state after lifecycle and internal-Reaction rules."""

    blue_lines: list[object]
    a_zones: list[object]
    s_zones: list[object]
    e_zones: list[object]
    stopalls: list[object]
    prepared_order_audit: list[object]
    # Final accepted source collections retained only for Bridge Output parent
    # joins. They are never serialized as public legacy rows or fed back into
    # lifecycle decisions.
    projection_s_zones: list[object]
    projection_e_zones: list[object]
    projection_stopalls: list[object]


def calculate_direction_range_state(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    timings: dict[str, float],
) -> DirectionRangeState:
    """Collect detector output for one requested direction before visibility rules."""
    result = state.results[direction]
    opposite = engines.reaction.opposite_direction(direction)
    start_index = market.start_index
    end_index = market.end_index

    requires_blue_lines = (
        args.blue_lines == "enabled"
        or args.a_zones == "enabled"
        or args.s_zones == "enabled"
    )
    if state.reusable_full_context and requires_blue_lines:
        blue_lines = [
            item
            for item in state.full_lines_by_direction[direction]
            if start_index <= int(getattr(item, "source_index")) <= end_index
        ]
    elif requires_blue_lines:
        blue_lines = timed(
            timings,
            f"Blue Line - {direction.title()}",
            lambda: engines.blue_line.detect_blue_lines(
                direction,
                result.reactions,
                market.chronology,
                result.resets,
            ),
        )
    else:
        blue_lines = []

    requires_a_zones = args.a_zones == "enabled" or args.s_zones == "enabled"
    if state.reusable_full_context and requires_a_zones:
        a_zones = [
            item
            for item in state.full_a_by_direction[direction]
            if start_index <= int(getattr(item, "source_index")) <= end_index
        ]
    elif requires_a_zones:
        a_zones = timed(
            timings,
            f"A - {direction.title()}",
            lambda: engines.a_zone.detect_a_zones(
                direction,
                result.reactions,
                blue_lines,
                market.chronology,
            ),
        )
    else:
        a_zones = []

    s_candidates: list[object] = []
    accepted_s_zones: list[object] = []
    if args.s_zones == "enabled":
        if state.reusable_full_context:
            s_candidates = state.full_s_candidates_by_direction[direction]
            accepted_s_zones = state.full_s_by_direction[direction]
            a_zones = state.full_s_detectors[direction].eligible_a_zones
        else:
            s_detector = engines.s_zone.SZoneDetector(
                direction,
                result.reactions,
                state.results[opposite].reactions,
                blue_lines,
                a_zones,
                market.chronology,
                0,
                len(market.candles) - 1,
                state.results[opposite].resets,
                initial_order_geometry=state.initial_order_geometry[direction],
            )
            s_candidates = timed(
                timings, f"S - {direction.title()}", s_detector.detect
            )
            state.full_s_detectors[direction] = s_detector
            accepted_s_zones = s_candidates
            a_zones = s_detector.eligible_a_zones

    return DirectionRangeState(
        blue_lines=blue_lines,
        a_zones=a_zones,
        s_candidates=s_candidates,
        accepted_s_zones=accepted_s_zones,
        e_zones=list(state.full_e_zones.get(direction, [])),
        invalid_a_identities=state.invalid_a_identities_by_direction.get(
            direction, set()
        ),
        invalid_s_identities=state.invalid_s_identities_by_direction.get(
            direction, set()
        ),
    )


def finalize_direction_visibility(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    direction_state: DirectionRangeState,
    timings: dict[str, float],
) -> DirectionVisibilityState:
    """Apply lifecycle, range and Internal-Reaction rules to detector output."""
    lifecycle_engine = engines.lifecycle
    opposite = engines.reaction.opposite_direction(direction)
    start_index = market.start_index
    end_index = market.end_index

    visible_a_zones = lifecycle_engine.visible_a_zones(
        direction_state.a_zones, direction_state.accepted_s_zones
    )
    visible_a_zones = lifecycle_engine.visible_a_zones_after_s_stops(
        visible_a_zones,
        direction_state.accepted_s_zones,
        market.candles,
    )

    e_zones = list(direction_state.e_zones)
    stopalls: list[object] = []
    stopall_enabled = (
        args.lifecycle_engine is not None
        and engines.e_zone is not None
        and args.s_zones == "enabled"
    )
    if stopall_enabled and direction in state.full_e_detectors:
        e_zones, stopalls = lifecycle_engine.reconcile_stopall_lifecycle(
            state.full_e_detectors[direction],
            direction_state.accepted_s_zones,
            e_zones,
            market.chronology,
            direction,
            lambda label, work: timed(timings, label, work),
        )

    if direction in state.full_e_detectors:
        # Dominant E ownership drives StopAll.  After those hard boundaries are
        # fixed, restore direct E1 roots of accepted S behaviors so independent
        # E formation remains visible without letting lower-priority roots
        # rewrite the dominant StopAll sequence.
        detector = state.full_e_detectors[direction]
        e_zones = detector.restore_independent_s_roots(e_zones)
        # Root restoration is a calculation-valid acceptance step that occurs
        # after the detector's normal ledger rebuild.  Sync only missing audit
        # identities while preserving Orders already needed by StopAll/history.
        e_zones = detector.ensure_accepted_order_audit(e_zones)
        visibility_stop = lambda item: detector.parent_stop(
            "S" if hasattr(item, "a_source_time") else "E", item
        )
    else:
        visibility_stop = lambda item: state.full_s_detectors[direction].first_a_stop(
            Decimal(str(item.price)), item.decision_event_time
        )

    # Capture accepted objects before presentation range/internal filtering.
    # The Bridge projector may resolve a nested historical parent from these
    # immutable references, but it never republishes them as independent rows.
    projection_s_zones = list(direction_state.accepted_s_zones)
    projection_e_zones = list(e_zones)
    projection_stopalls = list(stopalls)

    e_zones, visible_s_zones, visible_a_zones = timed(
        timings,
        f"Apply visibility filters - {direction.title()}",
        lambda: lifecycle_engine.finalize_behavior_visibility(
            visible_a_zones,
            direction_state.s_candidates,
            e_zones,
            stopalls,
            direction,
            direction_state.invalid_s_identities,
            visibility_stop,
            lambda item: state.full_s_detectors[direction].candidate_event_time(
                item.source_index, item.price, item.source_time
            ),
            market.candles,
            all_a_zones=direction_state.a_zones,
        ),
    )

    visible_s_zones = [
        item
        for item in visible_s_zones
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]
    visible_a_zones = [
        item
        for item in visible_a_zones
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]
    e_zones = [
        item
        for item in e_zones
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]
    stopalls = [
        item
        for item in stopalls
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]

    display_a_zones = [
        item
        for item in visible_a_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in direction_state.invalid_a_identities
    ]
    display_s_zones = [
        item
        for item in visible_s_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in direction_state.invalid_s_identities
    ]
    # OrderAudit provenance is calculated on the full RAW, not clipped by the
    # presentation range.  A public S/E/StopAll inside the requested window may
    # legitimately reference an accepted A-owned Order whose First/A source is
    # before ``start_index``.  Keep all calculation-accepted A sources here;
    # presentation filtering is handled separately by required Order identities.
    order_audit_a_sources = {
        getattr(item, "source_time")
        for item in state.full_a_by_direction.get(direction, direction_state.a_zones)
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in direction_state.invalid_a_identities
    }

    all_behavior_reactions = [
        reaction
        for result_item in state.results.values()
        for reaction in result_item.reactions
    ]
    engines.blue_line.mark_internal_blue_lines(
        direction_state.blue_lines,
        state.results[direction].reactions,
        all_behavior_reactions,
    )
    display_a_zones, display_s_zones, e_zones, stopalls = (
        lifecycle_engine.filter_internal_behavior_outputs(
            display_a_zones,
            display_s_zones,
            e_zones,
            stopalls,
            state.results[opposite].reactions,
            state.internal_reaction_identities.get(opposite, set()),
            all_behavior_reactions,
        )
    )

    # Historical rescue is presentation-only.  It runs after all lifecycle,
    # StopAll, visibility, and OrderAudit ownership calculations so restoring a
    # fully formed historical E can never rewrite an already-correct behavior,
    # number, parent, StopAll sequence, or physical Order provenance.
    if direction in state.full_e_detectors:
        detector = state.full_e_detectors[direction]
        occupied_e_sources = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in e_zones
        }
        occupied_stopall_sources = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in stopalls
        }
        rescued_e_zones = [
            item
            for item in getattr(detector, "historical_rescued_zones", [])
            if start_index <= int(getattr(item, "source_index")) <= end_index
            and (int(getattr(item, "source_index")), getattr(item, "source_time"))
                not in occupied_e_sources
            and (int(getattr(item, "source_index")), getattr(item, "source_time"))
                not in occupied_stopall_sources
            and not lifecycle_engine.forbidden_internal_order_b(
                item, state.internal_reaction_identities.get(opposite, set())
            )
        ]
        if rescued_e_zones:
            e_zones = sorted(
                [*e_zones, *rescued_e_zones],
                key=lambda item: (
                    getattr(item, "source_time"),
                    int(getattr(item, "source_index")),
                    getattr(item, "decision_event_time"),
                ),
            )

    required_order_identities = {
        order_identity(int(first_index), int(break_index))
        for item in [*display_s_zones, *e_zones, *stopalls]
        for first_index, break_index in [(
            getattr(item, "order_first_index", None),
            getattr(item, "order_break_index", None),
        )]
        if first_index is not None and break_index is not None
    }
    prepared_order_audit = (
        lifecycle_engine.prepare_order_audit(
            state.full_e_detectors[direction],
            start_index,
            end_index,
            state.full_s_detectors.get(direction),
            order_audit_a_sources,
            required_order_identities,
        )
        if direction in state.full_e_detectors
        else []
    )
    if direction in state.full_e_detectors:
        validate_order_audit_bridge(
            prepared_order_audit, display_s_zones, e_zones, stopalls
        )
    return DirectionVisibilityState(
        blue_lines=engines.blue_line.public_blue_lines(direction_state.blue_lines),
        a_zones=display_a_zones,
        s_zones=display_s_zones,
        e_zones=e_zones,
        stopalls=stopalls,
        prepared_order_audit=prepared_order_audit,
        projection_s_zones=projection_s_zones,
        projection_e_zones=projection_e_zones,
        projection_stopalls=projection_stopalls,
    )


def serialize_direction_payload(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    visibility: DirectionVisibilityState,
    timings: dict[str, float],
):
    """Serialize one direction without applying any trading rule."""
    result = state.results[direction]
    if not getattr(args, "bridge_output", False):
        # Preserve the direct legacy path byte-for-byte in structure and
        # ordering when the additive projection is not requested.
        reactions, resets = timed(
            timings,
            f"Serialize Reaction - {direction.title()}",
            lambda: serialize(
                result,
                market.start_index,
                market.end_index,
                reaction_transform=lambda item: engines.reaction.published_reaction_candidate(
                    direction, item, market.chronology
                ),
            ),
        )

        def build_legacy_payload():
            return {
                "reactions": reactions,
                "resets": resets,
                "blueLines": serialize_blue_lines(
                    visibility.blue_lines if args.blue_lines == "enabled" else [],
                    market.start_index,
                    market.end_index,
                ),
                "aZones": serialize_a_zones(
                    visibility.a_zones if args.a_zones == "enabled" else []
                ),
                "sZones": serialize_s_zones(visibility.s_zones),
                "eZones": serialize_e_zones(visibility.e_zones),
                "stopAlls": serialize_stopalls(visibility.stopalls),
                "orderAudit": (
                    serialize_order_audit(
                        visibility.prepared_order_audit,
                        state.full_e_detectors[direction],
                    )
                    if direction in state.full_e_detectors
                    else []
                ),
            }

        return timed(
            timings, f"Serialize output - {direction.title()}", build_legacy_payload
        )

    reaction_transform = lambda item: engines.reaction.published_reaction_candidate(
        direction, item, market.chronology
    )
    def serialize_reactions_from_one_selection():
        selected = select_reaction_serialization_items(
            result,
            market.start_index,
            market.end_index,
            reaction_transform,
        )
        reactions, resets = serialize(result, selected_items=selected)
        return reactions, resets, selected

    reactions, resets, selected_reaction_items = timed(
        timings,
        f"Serialize Reaction - {direction.title()}",
        serialize_reactions_from_one_selection,
    )
    selected_reactions, selected_resets = selected_reaction_items
    selected_blue_lines = [
        item
        for item in (
            visibility.blue_lines if args.blue_lines == "enabled" else []
        )
        if _index_selected(
            getattr(item, "source_index"), market.start_index, market.end_index
        )
    ]
    selected_a_zones = (
        visibility.a_zones if args.a_zones == "enabled" else []
    )
    selected_s_zones = visibility.s_zones
    selected_e_zones = visibility.e_zones
    selected_stopalls = visibility.stopalls
    audit_detector = state.full_e_detectors.get(direction)
    selected_order_audit = (
        sorted(
            visibility.prepared_order_audit,
            key=lambda item: _bridge_audit_order_key(item, audit_detector),
        )
        if audit_detector is not None
        else []
    )

    def build_payload():
        payload = {
            "reactions": reactions,
            "resets": resets,
            "blueLines": serialize_blue_lines(
                selected_blue_lines,
            ),
            "aZones": serialize_a_zones(selected_a_zones),
            "sZones": serialize_s_zones(selected_s_zones),
            "eZones": serialize_e_zones(selected_e_zones),
            "stopAlls": serialize_stopalls(selected_stopalls),
            "orderAudit": (
                serialize_order_audit(
                    selected_order_audit,
                    audit_detector,
                )
                if audit_detector is not None
                else []
            ),
        }
        payload["bridgeOutput"] = build_bridge_output(
            direction,
            market,
            state,
            visibility,
            selected_reactions,
            selected_resets,
            selected_blue_lines,
            selected_a_zones,
            selected_s_zones,
            selected_e_zones,
            selected_stopalls,
            selected_order_audit,
        )
        return payload

    return timed(
        timings, f"Serialize output - {direction.title()}", build_payload
    )


def build_direction_output(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    timings: dict[str, float],
):
    """Calculate, finalize and serialize one requested trend direction."""
    direction_state = calculate_direction_range_state(
        direction, args, engines, market, state, timings
    )
    visibility = finalize_direction_visibility(
        direction,
        args,
        engines,
        market,
        state,
        direction_state,
        timings,
    )
    return serialize_direction_payload(
        direction, args, engines, market, state, visibility, timings
    )

def build_response_payload(
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    timings: dict[str, float],
    pipeline_started: float,
) -> dict[str, object]:
    """Build the public response envelope around serialized direction outputs."""
    e_enabled = engines.e_zone is not None and args.s_zones == "enabled"
    stop_all_enabled = (
        args.lifecycle_engine is not None
        and engines.e_zone is not None
        and args.s_zones == "enabled"
    )
    payload: dict[str, object] = {
        "engine": "reaction_engine.py",
        "version": engines.reaction.REACTION_ENGINE_VERSION,
        "pipelineVersion": TRADING_PIPELINE_VERSION,
        "blueLineVersion": engines.blue_line.BLUE_LINE_VERSION,
        "aVersion": engines.a_zone.A_ZONE_VERSION,
        "sVersion": engines.s_zone.S_ZONE_VERSION,
        "eVersion": engines.e_zone.E_ZONE_VERSION if engines.e_zone else None,
        "stopAllVersion": (
            engines.lifecycle.STOP_ALL_VERSION
            if args.lifecycle_engine is not None
            else None
        ),
        "blueLinesEnabled": args.blue_lines == "enabled",
        "aEnabled": args.a_zones == "enabled",
        "sEnabled": args.s_zones == "enabled",
        "eEnabled": e_enabled,
        "stopAllEnabled": stop_all_enabled,
        "timeframe": args.timeframe,
        "actualFrom": epoch(market.candles[market.start_index].timestamp),
        "actualTo": epoch(market.candles[market.end_index].timestamp),
        "directions": {},
    }
    direction_payloads = payload["directions"]
    assert isinstance(direction_payloads, dict)
    for direction in state.directions:
        direction_payloads[direction] = build_direction_output(
            direction, args, engines, market, state, timings
        )
    payload["timings"] = {
        "phasesMs": {
            label: round(duration, 2) for label, duration in timings.items()
        },
        "bridgeTotalMs": round((perf_counter() - pipeline_started) * 1000, 2),
    }
    return payload


def main() -> int:
    pipeline_started = perf_counter()
    timings: dict[str, float] = {}
    validation_started = perf_counter()
    emit_progress("started", "Validate request")
    args = parse_arguments()
    validation_ms = (perf_counter() - validation_started) * 1000
    timings["Validate request"] = validation_ms
    emit_progress("completed", "Validate request", validation_ms)

    engines = load_engines(args, timings)
    market = prepare_market_context(args, engines, timings)
    state = prepare_pipeline_state(args, engines, market, timings)
    payload = build_response_payload(
        args, engines, market, state, timings, pipeline_started
    )

    emit_progress(
        "completed",
        "Calculation pipeline",
        (perf_counter() - pipeline_started) * 1000,
    )
    encoding_started = perf_counter()
    encoded_payload = json.dumps(payload, separators=(",", ":"))
    emit_progress(
        "completed",
        "Encode response JSON",
        (perf_counter() - encoding_started) * 1000,
    )
    print(encoded_payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        raise SystemExit(1)
