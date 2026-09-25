"""S-zone calculation from authoritative A, Reaction, Blue, and Order state.

Owns A-to-S handoff, S Red/Blue Simple/Advanced/Type3 formation, S decision
chronology, shared accepted-Order stop reconciliation, and the initial Order
audit created by stopped A zones. Larger E/StopAll arbitration remains
lifecycle-owned.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable, Sequence

from core_utils import as_decimal, reaction_identity
from direction_policy import policy_for


S_ZONE_VERSION = "4.20.0"
S_ZONE_LAST_MODIFIED = "2026-09-23 10:19:31 +03:30"


@dataclass(frozen=True, slots=True)
class SZone:
    direction: str
    color: str
    formation_type: str
    a_ordinal: int
    a_source_index: int
    a_source_time: datetime
    a_price: Decimal
    a_stop_index: int
    a_stop_time: datetime
    a_stop_event_time: datetime
    order_direction: str | None
    order_reaction_number: int | None
    order_mode: str | None
    order_first_index: int | None
    order_first_time: datetime | None
    order_break_index: int | None
    order_break_time: datetime | None
    order_confirmation_time: datetime | None
    order_box_top: Decimal | None
    order_box_top_source_index: int | None
    order_box_top_source_time: datetime | None
    order_box_bottom: Decimal | None
    order_box_bottom_source_index: int | None
    order_box_bottom_source_time: datetime | None
    order_stop_level: Decimal | None
    order_stop_source_index: int | None
    order_stop_source_time: datetime | None
    reset_reaction_number: int | None
    reset_time: datetime | None
    source_index: int
    source_time: datetime
    price: Decimal
    decision_index: int
    decision_time: datetime
    decision_event_time: datetime


class SZoneDetector:
    def __init__(
        self,
        direction: str,
        trend_reactions: Sequence[object],
        opposite_reactions: Sequence[object],
        trend_blue_lines: Sequence[object],
        a_zones: Sequence[object],
        chronology: object,
        start_index: int | None = None,
        end_index: int | None = None,
        opposite_resets: Sequence[object] = (),
        initial_order_geometry: Callable[[int, datetime, int], object | None] | None = None,
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.policy = policy_for(direction)
        self.order_direction = chronology.opposite_direction(direction)
        self.trend_reactions = list(trend_reactions)
        self.opposite_reactions = list(opposite_reactions)
        self.opposite_resets = list(opposite_resets)
        self.initial_order_geometry = initial_order_geometry
        self.trend_blue_lines = list(trend_blue_lines)
        self.a_zones = sorted(
            a_zones,
            key=lambda item: (
                getattr(item, "reaction_break_time"),
                int(getattr(item, "source_index")),
            ),
        )
        self.chronology = chronology
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.timeframe = chronology.timeframe
        self.candle_times = chronology.times
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index
        self.start_index = 0 if start_index is None else int(start_index)
        self.end_index = (
            len(self.candles) - 1 if end_index is None else int(end_index)
        )
        if not 0 <= self.start_index <= self.end_index < len(self.candles):
            raise ValueError("Invalid S analysis range.")
        self.range_start = self.candle_times[self.start_index]
        self.range_end = self.candle_times[self.end_index] + self.timeframe
        self.order_audit: dict[tuple[int, int], dict[str, object]] = {}
        # The exact A-stop handoff and the post-decision live-S interval are
        # distinct ownership phases.  Pre-decision handoff keeps Behavior
        # Independence for candidates opened after the A stop; once S is
        # decided, ordinary A re-entry is blocked until the S strict stop.
        self.a_ownership_windows: list[tuple[datetime, datetime | None]] = []
        self._reset_blue_formation_by_reaction: dict[int, datetime] = {}
        self._opposite_by_first_index = {
            int(getattr(item, "first_idx")): (number, item)
            for number, item in enumerate(self.opposite_reactions, start=1)
        }
        # Performance implementation detail: the authoritative Order chronology
        # is immutable for this detector run. Build its exact legacy sort order
        # once, then bisect/cache A-stop lookups instead of re-scanning and
        # re-sorting the complete opposite-Reaction history for every A.
        self._opposite_order_matches = sorted(
            (
                self._reaction_confirmation_time(item, self.order_direction),
                int(getattr(item, "first_idx")),
                int(getattr(item, "break_idx")),
                number,
                item,
            )
            for number, item in enumerate(self.opposite_reactions, start=1)
        )
        self._opposite_order_confirmation_times = [
            item[0] for item in self._opposite_order_matches
        ]
        self._order_matches_after_cache: dict[
            datetime, tuple[tuple[int, object, datetime], ...]
        ] = {}

        for line in self.trend_blue_lines:
            if not bool(getattr(line, "calculation_valid", True)):
                continue
            if str(getattr(line, "kind")) != "reset":
                continue
            reaction_number = int(getattr(line, "reaction_number"))
            if reaction_number not in self._reset_blue_formation_by_reaction:
                self._reset_blue_formation_by_reaction[reaction_number] = (
                    self._blue_formation_time(line)
                )

        # Performance implementation detail: immutable chronology indexes.
        # They preserve the exact legacy sort keys and are scoped to this run.
        self._trend_ordered = sorted(
            (
                self._reaction_confirmation_time(item, self.direction),
                int(getattr(item, "first_idx")),
                int(getattr(item, "break_idx")),
                number,
                item,
            )
            for number, item in enumerate(self.trend_reactions, start=1)
        )
        self._trend_ordered_confirmation_times = [item[0] for item in self._trend_ordered]
        self._trend_confirmation_times_sorted = sorted(
            item[0] for item in self._trend_ordered
        )
        self._opposite_confirmation_by_first = {
            int(getattr(item, "first_idx")): self._reaction_confirmation_time(
                item, self.order_direction
            )
            for item in self.opposite_reactions
        }
        self._opposite_reset_events = sorted(
            ((self._reset_time(reset), reset) for reset in self.opposite_resets),
            key=lambda item: item[0],
        )
        self._opposite_reset_event_times = [item[0] for item in self._opposite_reset_events]
        self._opposite_reset_times_by_owner: dict[int, list[datetime]] = {}
        for reset_time, reset in self._opposite_reset_events:
            self._opposite_reset_times_by_owner.setdefault(
                int(getattr(reset, "from_first_idx")), []
            ).append(reset_time)
        self._public_blue_formation_times = sorted(
            self._blue_formation_time(line)
            for line in self.trend_blue_lines
            if bool(getattr(line, "calculation_valid", True))
            and not bool(getattr(line, "behavior_internal", False))
        )

    def _main_index(self, timestamp: datetime) -> int:
        return self.chronology.main_index(timestamp)

    def _lower_window(
        self, start: datetime, end: datetime | None
    ) -> Sequence[object]:
        return self.chronology.lower_window(start, end)

    def _reaction_confirmation_time(
        self, reaction: object, direction: str
    ) -> datetime:
        return self.chronology.reaction_confirmation(direction, reaction)

    def reaction_confirmation_time(
        self, reaction: object, direction: str
    ) -> datetime:
        """Public chronology API used by cross-stage lifecycle ownership."""
        return self._reaction_confirmation_time(reaction, direction)


    def _reset_time(self, reset: object) -> datetime:
        return self.chronology.reset_time(reset)

    def _a_confirmation_time(self, zone: object) -> datetime:
        number = int(getattr(zone, "reaction_number"))
        if number < 1 or number > len(self.trend_reactions):
            raise ValueError("A refers to a missing trend reaction.")
        return self._reaction_confirmation_time(
            self.trend_reactions[number - 1], self.direction
        )

    def _trend_extreme(self, candle: object) -> Decimal:
        return as_decimal(
            getattr(candle, self.policy.extreme_attr)
        )

    def _a_stopped(self, value: Decimal, level: Decimal) -> bool:
        return self.policy.strict_cross(value, level)

    def _first_a_stop(
        self, level: Decimal, start: datetime
    ) -> tuple[int, datetime, datetime] | None:
        scan_start = max(start, self.range_start)
        left = bisect_left(self.lower_times, scan_start)
        right = bisect_left(self.lower_times, self.range_end)
        if right > left and self.lower_index is not None:
            position = (
                self.lower_index.first_less(left, right, level)
                if self.direction == "bullish"
                else self.lower_index.first_greater(left, right, level)
            )
            if position is None:
                return None
            event_time = self.lower_times[position]
            index = self._main_index(event_time)
            return index, getattr(self.candles[index], "timestamp"), event_time

        lower_items = self.lower[left:right]
        for item in lower_items:
            if self._a_stopped(self._trend_extreme(item), level):
                event_time = getattr(item, "timestamp")
                index = self._main_index(event_time)
                return index, getattr(self.candles[index], "timestamp"), event_time
        if lower_items:
            return None
        start_index = max(self.start_index, bisect_left(self.candle_times, start))
        for item in self.candles[start_index : self.end_index + 1]:
            if self._a_stopped(self._trend_extreme(item), level):
                return (
                    int(getattr(item, "index")),
                    getattr(item, "timestamp"),
                    getattr(item, "timestamp"),
                )
        return None

    def first_a_stop(
        self, level: Decimal, start: datetime
    ) -> tuple[int, datetime, datetime] | None:
        """Public lifecycle API for the first strict A stop."""
        return self._first_a_stop(level, start)


    def _first_order_after(
        self, a_stop_event_time: datetime
    ) -> tuple[int, object, datetime] | None:
        """Return the immutable first canonical opposite Order after A-stop.

        Each stopped A creates at most one parent-stop Order_A.  Subsequent
        native Mode-B Reactions cannot refresh that physical identity; they
        may be accepted only through independently valid creation causes.
        """
        matches = self._order_matches_after(a_stop_event_time)
        return matches[0] if matches else None

    def _order_matches_after(
        self, a_stop_event_time: datetime
    ) -> list[tuple[int, object, datetime]]:
        """Expose canonical opposite-Order chronology without changing ownership."""
        cached = self._order_matches_after_cache.get(a_stop_event_time)
        if cached is not None:
            return list(cached)

        gate_index = self._main_index(a_stop_event_time)
        position = bisect_right(
            self._opposite_order_confirmation_times, a_stop_event_time
        )
        matches = tuple(
            (number, reaction, confirmation)
            for confirmation, first_index, _break, number, reaction
            in self._opposite_order_matches[position:]
            if first_index >= gate_index
        )
        self._order_matches_after_cache[a_stop_event_time] = matches
        return list(matches)

    def _resolved_order_backed_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        first_order_match: tuple[int, object, datetime],
    ) -> SZone | None:
        """Resolve S using only the first physical Order_A owned by this A.

        The initial stopped-A OrderAudit retains its original parent-stop
        cause.  A later canonical Reaction never replaces the original
        Order_A, irrespective of its native Reaction Mode or S decision time.
        """
        return self._build_order_backed_zone(
            zone, a_ordinal, a_price, a_stop, first_order_match
        )

    def _record_a_order_audit(
        self,
        zone: object,
        a_stop_event_time: datetime,
        order_match: tuple[int, object, datetime],
    ) -> None:
        """Attach one stopped-A creation cause to a physical Order identity."""
        source_time = getattr(zone, "source_time")
        order_number, order, order_confirmation_time = order_match
        (
            order_stop_level,
            order_stop_source_index,
            order_stop_source_time,
        ) = self._order_stop(order_number, order)
        identity = reaction_identity(order)
        cause = (source_time, a_stop_event_time)
        entry = self.order_audit.get(identity)
        if entry is None:
            entry = {
                "reaction_number": order_number,
                "reaction": order,
                "confirmation_time": order_confirmation_time,
                "stop_level": order_stop_level,
                "stop_source_index": order_stop_source_index,
                "stop_source_time": order_stop_source_time,
                "a_source_time": source_time,
                "a_stop_event_time": a_stop_event_time,
                "a_causes": [],
            }
            self.order_audit[identity] = entry
        a_causes = entry.setdefault("a_causes", [])
        if cause not in a_causes:
            a_causes.append(cause)

    def _audit_stopped_a(self, zone: object) -> None:
        """Record the independent order gender created by one stopped A."""
        a_price = as_decimal(getattr(zone, "price"))
        a_stop = self._first_a_stop(a_price, self._a_confirmation_time(zone))
        if a_stop is None:
            return
        _, _, a_stop_event_time = a_stop
        order_match = self._first_order_after(a_stop_event_time)
        if order_match is None:
            return
        self._record_a_order_audit(zone, a_stop_event_time, order_match)

    def _candidate_source(
        self, start_index: int, end_index: int
    ) -> tuple[int, datetime, Decimal]:
        if end_index < start_index:
            raise ValueError("S candidate range ends before the A stop.")
        source = self.candles[start_index]
        value = self._trend_extreme(source)
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = self._trend_extreme(item)
            better = self.policy.better_extreme(candidate, value)
            if better:
                source = item
                value = candidate
        return int(getattr(source, "index")), getattr(source, "timestamp"), value

    def _candidate_source_last(
        self, start_index: int, end_index: int
    ) -> tuple[int, datetime, Decimal]:
        """Return the directional extreme, assigning equality to the last candle."""
        if end_index < start_index:
            raise ValueError("S candidate range ends before it starts.")
        source = self.candles[start_index]
        value = self._trend_extreme(source)
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = self._trend_extreme(item)
            better_or_equal = (
                candidate <= value
                if self.direction == "bullish"
                else candidate >= value
            )
            if better_or_equal:
                source = item
                value = candidate
        return int(getattr(source, "index")), getattr(source, "timestamp"), value

    def _first_trend_reaction_after_order(
        self, order_confirmation_time: datetime
    ) -> tuple[int, object, datetime] | None:
        for number, reaction in enumerate(self.trend_reactions, start=1):
            confirmation = self._reaction_confirmation_time(
                reaction, self.direction
            )
            if confirmation > order_confirmation_time:
                return number, reaction, confirmation
        return None


    def _nested_trend_reaction(
        self, order: object, order_confirmation_time: datetime
    ) -> tuple[int, object, datetime] | None:
        order_first_index = int(getattr(order, "first_idx"))
        order_break_index = int(getattr(order, "break_idx"))
        order_first = getattr(self.candles[order_first_index], "timestamp")
        order_top = as_decimal(getattr(order, "box_top"))
        order_bottom = as_decimal(getattr(order, "box_bottom"))
        for number, reaction in enumerate(self.trend_reactions, start=1):
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            first = getattr(self.candles[first_index], "timestamp")
            if (
                first <= order_first
                or first_index <= order_first_index
                or break_index > order_break_index
                or first >= order_confirmation_time
            ):
                continue
            confirmation = self._reaction_confirmation_time(
                reaction, self.direction
            )
            wholly_inside = (
                as_decimal(getattr(reaction, "box_top")) <= order_top
                and as_decimal(getattr(reaction, "box_bottom")) >= order_bottom
            )
            if confirmation <= order_confirmation_time and wholly_inside:
                return number, reaction, confirmation
        return None

    def _simple_candidate(
        self, order: object, reaction: object
    ) -> tuple[int, datetime, Decimal]:
        """Use the inclusive order-Break to aligned-Break interval."""
        return self._candidate_source_last(
            int(getattr(order, "break_idx")),
            int(getattr(reaction, "break_idx")),
        )

    def _type3_reset_leg(
        self, reset: object
    ) -> tuple[int, datetime, Decimal] | None:
        """Return the independent Type-3 inclusive Break-to-Reset geometry."""
        owner_match = self._opposite_by_first_index.get(
            int(getattr(reset, "from_first_idx"))
        )
        if owner_match is None:
            return None
        _, owner = owner_match
        start_index = int(getattr(owner, "break_idx"))
        end_index = self._main_index(self._reset_time(reset))
        if end_index < start_index:
            return None
        return self._candidate_source_last(start_index, end_index)

    def _type3_has_trend_reaction(
        self, a_stop_event: datetime, crossing: datetime
    ) -> bool:
        position = bisect_right(self._trend_confirmation_times_sorted, a_stop_event)
        return (
            position < len(self._trend_confirmation_times_sorted)
            and self._trend_confirmation_times_sorted[position] <= crossing
        )

    def _first_type3(
        self,
        a_stop_event: datetime,
        deadline: datetime,
    ) -> tuple[int, datetime, Decimal, int, datetime, int, datetime, datetime] | None:
        """Find the first no-order Type-3 Reset-leg S decision before a new order."""
        winner = None
        left = bisect_right(self._opposite_reset_event_times, a_stop_event)
        right = bisect_left(self._opposite_reset_event_times, deadline)
        for reset_time, reset in self._opposite_reset_events[left:right]:
            owner_first = int(getattr(reset, "from_first_idx"))
            owner_confirmation = self._opposite_confirmation_by_first.get(owner_first)
            if owner_confirmation is None or owner_confirmation > a_stop_event:
                continue
            owner_resets = self._opposite_reset_times_by_owner.get(owner_first, ())
            if owner_resets and owner_resets[0] <= a_stop_event:
                continue
            leg = self._type3_reset_leg(reset)
            if leg is None:
                continue
            source_index, source_time, boundary = leg
            lower_left = bisect_left(self.lower_times, reset_time)
            lower_right = bisect_left(self.lower_times, deadline)
            crossing_position = (
                self.lower_index.first_less(lower_left, lower_right, boundary)
                if self.direction == "bullish"
                else self.lower_index.first_greater(lower_left, lower_right, boundary)
            )
            if crossing_position is None:
                continue
            crossing = self.lower_times[crossing_position]
            if not self._type3_has_trend_reaction(a_stop_event, crossing):
                continue
            decision_index = self._main_index(crossing)
            owner_number = self._opposite_by_first_index[owner_first][0]
            candidate = (
                source_index,
                source_time,
                boundary,
                decision_index,
                getattr(self.candles[decision_index], "timestamp"),
                owner_number,
                reset_time,
                crossing,
            )
            if winner is None or candidate[-1] < winner[-1]:
                winner = candidate
        return winner


    def _type4_has_blue(
        self, candidate_source_index: int, crossing_event: datetime
    ) -> bool:
        """Return whether a public calculation-valid Blue exists in Type-4 window."""
        window_start = self.candle_times[candidate_source_index]
        position = bisect_left(self._public_blue_formation_times, window_start)
        return (
            position < len(self._public_blue_formation_times)
            and self._public_blue_formation_times[position] <= crossing_event
        )

    def _first_type4(
        self,
        a_stop: tuple[int, datetime, datetime],
        deadline: datetime,
    ) -> tuple[int, datetime, Decimal, int, datetime, int, datetime] | None:
        """Find the first order-free S Blue Type-4 decision after A stop.

        Bearish: from the A-stop main candle through the Breakout main candle
        of the latest confirmed Bearish Reaction, the maximum High is the
        current S candidate. Bullish mirrors with minimum Low. The candidate is
        valid only while no opposite Order has formed. If it strict-crosses
        without a qualifying Blue, no S is emitted; a later aligned Reaction
        replaces it with a freshly calculated candidate over the same A-stop
        origin.
        """
        a_stop_index, _a_stop_time, a_stop_event = a_stop
        left = bisect_right(self._trend_ordered_confirmation_times, a_stop_event)
        right = bisect_left(self._trend_ordered_confirmation_times, deadline)
        aligned = [
            (confirmation, number, reaction)
            for confirmation, _first, break_index, number, reaction
            in self._trend_ordered[left:right]
            if break_index >= a_stop_index
        ]

        for position, (confirmation, reaction_number, reaction) in enumerate(aligned):
            break_index = int(getattr(reaction, "break_idx"))
            source_index, source_time, candidate_level = self._candidate_source_last(
                a_stop_index, break_index
            )
            candidate_event = self._candidate_event_time(
                source_index, candidate_level, a_stop_event
            )
            search_start = max(confirmation, candidate_event, a_stop_event)
            next_confirmation = (
                aligned[position + 1][0]
                if position + 1 < len(aligned)
                else deadline
            )
            search_end = min(deadline, next_confirmation)
            if search_start >= search_end:
                continue

            lower_left = bisect_left(self.lower_times, search_start)
            lower_right = bisect_left(self.lower_times, search_end)
            crossing_position = (
                self.lower_index.first_less(lower_left, lower_right, candidate_level)
                if self.direction == "bullish"
                else self.lower_index.first_greater(lower_left, lower_right, candidate_level)
            )
            if crossing_position is None:
                continue
            crossing_event = self.lower_times[crossing_position]
            if not self._type4_has_blue(source_index, crossing_event):
                # The candidate failed without Blue.  While no Order exists,
                # the next aligned Reaction will transfer/rebuild the candidate.
                continue

            decision_index = self._main_index(crossing_event)
            return (
                source_index,
                source_time,
                candidate_level,
                decision_index,
                getattr(self.candles[decision_index], "timestamp"),
                reaction_number,
                crossing_event,
            )
        return None

    def _build_type4_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        type4: tuple[int, datetime, Decimal, int, datetime, int, datetime],
    ) -> SZone:
        """Build the order-free Blue Type-4 continuation for one stopped A."""
        a_stop_index, a_stop_time, a_stop_event_time = a_stop
        (
            source_index, source_time, price, decision_index, decision_time,
            _trend_reaction_number, decision_event_time,
        ) = type4
        return SZone(
            direction=self.direction,
            color="blue",
            formation_type="type4",
            a_ordinal=a_ordinal,
            a_source_index=int(getattr(zone, "source_index")),
            a_source_time=getattr(zone, "source_time"),
            a_price=a_price,
            a_stop_index=a_stop_index,
            a_stop_time=a_stop_time,
            a_stop_event_time=a_stop_event_time,
            order_direction=None,
            order_reaction_number=None,
            order_mode=None,
            order_first_index=None,
            order_first_time=None,
            order_break_index=None,
            order_break_time=None,
            order_confirmation_time=None,
            order_box_top=None,
            order_box_top_source_index=None,
            order_box_top_source_time=None,
            order_box_bottom=None,
            order_box_bottom_source_index=None,
            order_box_bottom_source_time=None,
            order_stop_level=None,
            order_stop_source_index=None,
            order_stop_source_time=None,
            reset_reaction_number=None,
            reset_time=None,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event_time,
        )


    def _candidate_after_order(
        self,
        order_confirmation_time: datetime,
        reaction: object,
    ) -> tuple[int, datetime, Decimal]:
        """Find a candidate strictly after the order is confirmed.

        A reaction anchor is authoritative only when it is also after the
        order confirmation.  Otherwise the earliest extreme in the candles
        following the confirmation through the reaction First owns the
        candidate.
        """
        first_index = int(getattr(reaction, "first_idx"))
        start_index = bisect_left(self.candle_times, order_confirmation_time)
        start_index = max(self.start_index, min(start_index, first_index))
        anchor_index = getattr(reaction, "anchor_idx", None)
        anchor_value = getattr(reaction, "anchor_value", None)
        if anchor_index is not None and int(anchor_index) >= start_index:
            source = self.candles[int(anchor_index)]
            return (
                int(anchor_index),
                getattr(source, "timestamp"),
                as_decimal(anchor_value),
            )
        candidate = self._candidate_source(start_index, first_index)
        containing_index = self._main_index(order_confirmation_time)
        if containing_index < start_index:
            # Do not discard the valid remainder of an intrabar confirmation
            # candle, or import an extreme that occurred before confirmation.
            remainder = self._lower_window(
                order_confirmation_time,
                self.candle_times[containing_index] + self.timeframe,
            )
            for item in remainder:
                value = self._trend_extreme(item)
                if self._a_stopped(value, candidate[2]) or value == candidate[2]:
                    candidate = (
                        containing_index, self.candle_times[containing_index], value
                    )
        return candidate

    def _a_source_event_time(self, zone: object) -> datetime:
        """Locate the source extreme, including an A-stop main candle."""
        source = getattr(zone, "source_time")
        price = as_decimal(getattr(zone, "price"))
        for item in self._lower_window(source, source + self.timeframe):
            if self._trend_extreme(item) == price:
                return getattr(item, "timestamp")
        return source

    def _a_owned_by_s(self, zone: object) -> bool:
        event_time = self._a_source_event_time(zone)
        for start, end in self.a_ownership_windows:
            if not (start <= event_time and (end is None or event_time < end)):
                continue

            # The exact A-stop handoff owns only candidates whose own trigger
            # began at or before that boundary.  A new A structure whose
            # trigger begins strictly after the handoff is independently
            # eligible; the later lifecycle hierarchy still decides whether
            # it may survive as an equal/smaller behavior.
            trigger_event = getattr(zone, "trigger_event_time", None)
            if trigger_event is not None and trigger_event > start:
                return False

            # A decided S normally owns this continuation. A fresh Reset-Blue
            # pair may open a new A only when the entire pair is born after
            # that S ownership began, Blue-1 has already stopped before Blue-2
            # forms, and Blue-2's stop candle is the A source. Open/undecided S
            # windows never grant this preemption.
            blue_1_source = getattr(zone, "blue_1_source_time", None)
            blue_2_source = getattr(zone, "blue_2_source_time", None)
            blue_1_stop = getattr(zone, "blue_1_stop_time", None)
            blue_2_stop = getattr(zone, "blue_2_stop_time", None)
            source_time = getattr(zone, "source_time", None)
            if (
                end is not None
                and blue_1_source is not None
                and blue_2_source is not None
                and blue_1_stop is not None
                and blue_2_stop is not None
                and source_time is not None
                and start < blue_1_source
                and blue_1_stop < blue_2_source
                and source_time == blue_2_stop
                and self._a_pair_is_reset_reset(zone)
            ):
                return False
            return True
        return False

    def _a_pair_is_reset_reset(self, zone: object) -> bool:
        """Whether both Blue Lines that define A are Reset Blues."""
        first = int(getattr(zone, "blue_1_ordinal", 0)) - 1
        second = int(getattr(zone, "blue_2_ordinal", 0)) - 1
        if not (0 <= first < len(self.trend_blue_lines)):
            return False
        if not (0 <= second < len(self.trend_blue_lines)):
            return False
        return (
            str(getattr(self.trend_blue_lines[first], "kind", "")) == "reset"
            and str(getattr(self.trend_blue_lines[second], "kind", "")) == "reset"
        )

    @property
    def eligible_a_zones(self) -> list[object]:
        """A candidates outside stopped-parent S ownership, before rendering."""
        return [zone for zone in self.a_zones if not self._a_owned_by_s(zone)]

    def _candidate_timing(
        self,
        a_stop_index: int,
        order: object,
        order_confirmation_time: datetime,
        a_stop_event_time: datetime | None = None,
    ) -> str:
        """Resolve pre/post-Order ownership without stealing Advanced S.

        Existing nested same-direction geometry owns the Advanced branch and
        keeps the established price-geometry classification.  Otherwise, when
        that legacy classification says ``after``, exact event chronology may
        prove that the A-stop candidate actually formed strictly before the
        opposite Order First.  Equality remains after-Order.
        """
        stop_extreme = self._trend_extreme(self.candles[a_stop_index])
        boundary = as_decimal(
            getattr(
                order,
                "box_bottom" if self.direction == "bullish" else "box_top",
            )
        )
        if self.direction == "bullish":
            legacy = "after" if boundary <= stop_extreme else "before"
        else:
            legacy = "after" if boundary >= stop_extreme else "before"
        if legacy == "before":
            return legacy

        # Do not let Simple pre-Order chronology steal an already-valid
        # Advanced owner.  This preserves accepted Advanced S provenance.
        if self._nested_trend_reaction(order, order_confirmation_time) is not None:
            return legacy

        if a_stop_event_time is None:
            a_stop_event_time = self.candle_times[a_stop_index]
        candidate = self._candidate_before_order(
            a_stop_index, order, a_stop_event_time=a_stop_event_time
        )
        candidate_event = self._candidate_event_time(
            candidate[0], candidate[2], a_stop_event_time
        )
        order_first_time = self.candle_times[int(getattr(order, "first_idx"))]
        return "before" if candidate_event < order_first_time else "after"

    def _candidate_before_order(
        self,
        a_stop_index: int,
        order: object,
        a_stop_event_time: datetime | None = None,
    ) -> tuple[int, datetime, Decimal]:
        """Use the lowest/highest leg extreme from A-stop through order First."""
        if a_stop_event_time is None:
            a_stop_event_time = self.candle_times[a_stop_index]
        first_index = int(getattr(order, "first_idx"))
        candidate = self._candidate_source(a_stop_index, first_index)
        stop_candle_end = self.candle_times[a_stop_index] + self.timeframe
        eligible_stop_remainder = self._lower_window(
            a_stop_event_time, stop_candle_end
        )
        if not eligible_stop_remainder:
            return candidate
        source = eligible_stop_remainder[0]
        value = self._trend_extreme(source)
        for item in eligible_stop_remainder[1:]:
            item_value = self._trend_extreme(item)
            better = (
                item_value < value
                if self.direction == "bullish"
                else item_value > value
            )
            if better:
                source = item
                value = item_value
        later_candidate = (
            self._candidate_source(a_stop_index + 1, first_index)
            if first_index > a_stop_index
            else None
        )
        if later_candidate is not None:
            better = (
                later_candidate[2] < value
                if self.direction == "bullish"
                else later_candidate[2] > value
            )
            if better:
                return later_candidate
        return a_stop_index, self.candle_times[a_stop_index], value

    def _candidate_event_time(
        self,
        source_index: int,
        level: Decimal,
        not_before: datetime,
    ) -> datetime:
        """Return the first lower-timeframe event that forms the candidate."""
        source_time = self.candle_times[source_index]
        for item in self._lower_window(
            max(source_time, not_before), source_time + self.timeframe
        ):
            if self._trend_extreme(item) == level:
                return getattr(item, "timestamp")
        return max(source_time, not_before)

    def candidate_event_time(
        self, source_index: int, price: Decimal, fallback: datetime
    ) -> datetime:
        """Public lifecycle API for exact S candidate provenance."""
        return self._candidate_event_time(source_index, price, fallback)


    def _blue_formation_time(self, line: object) -> datetime:
        explicit = getattr(line, "formation_time", None)
        if explicit is not None:
            return explicit
        source_index = int(getattr(line, "source_index"))
        source_time = getattr(self.candles[source_index], "timestamp")
        if str(getattr(line, "kind")) != "reset":
            reaction_number = int(getattr(line, "reaction_number"))
            if 1 <= reaction_number <= len(self.trend_reactions):
                return self._reaction_confirmation_time(
                    self.trend_reactions[reaction_number - 1], self.direction
                )
            return source_time
        broken_level = getattr(line, "broken_level", None)
        if broken_level is None:
            return source_time
        end = source_time + self.timeframe
        for item in self._lower_window(source_time, end):
            value = as_decimal(
                getattr(item, "low" if self.direction == "bullish" else "high")
            )
            crossed = (
                value < as_decimal(broken_level)
                if self.direction == "bullish"
                else value > as_decimal(broken_level)
            )
            if crossed:
                return getattr(item, "timestamp")
        return source_time

    def _candidate_cross_has_blue(
        self,
        reaction_number: int,
        event_time: datetime,
    ) -> bool:
        """Return whether the candidate cross has its aligned Reset Blue.

        The Reset Blue belongs to the same-direction reaction, but it does
        not have to be drawn on the candidate candle or on the candle that
        crosses the candidate.  Its exact formation event only needs to be
        no later than the candidate crossing event.
        """
        if reaction_number < 1 or reaction_number > len(self.trend_reactions):
            return False
        formation_time = self._reset_blue_formation_by_reaction.get(reaction_number)
        return formation_time is not None and formation_time <= event_time

    def _has_ordinary_trend_reaction(
        self, behavior_start: datetime, event_time: datetime
    ) -> bool:
        """Return whether ordinary aligned geometry completed in the leg."""
        position = bisect_right(self._trend_confirmation_times_sorted, behavior_start)
        return (
            position < len(self._trend_confirmation_times_sorted)
            and self._trend_confirmation_times_sorted[position] <= event_time
        )


    def _order_stop(
        self, order_number: int, reaction: object
    ) -> tuple[Decimal, int, datetime]:
        return self.chronology.canonical_order_stop(
            self.order_direction,
            order_number,
            reaction,
            self.opposite_reactions,
            start_index=self.start_index,
        )

    def _candidate_crossed(self, candle: object, level: Decimal) -> bool:
        value = self._trend_extreme(candle)
        return self._a_stopped(value, level)

    def _order_stop_crossed(self, candle: object, level: Decimal) -> bool:
        if self.order_direction == "bearish":
            return as_decimal(getattr(candle, "high")) > level
        return as_decimal(getattr(candle, "low")) < level

    def _decision(
        self,
        candidate_level: Decimal,
        order_stop_level: Decimal,
        start: datetime,
        trend_reaction_number: int,
        behavior_start: datetime,
        candidate_start: datetime | None = None,
        fallback_on_unqualified_cross: bool = False,
    ) -> tuple[str, int, datetime, datetime] | None:
        scan_start = max(start, self.range_start)
        left = bisect_left(self.lower_times, scan_start)
        right = bisect_left(self.lower_times, self.range_end)
        if right > left:
            # Order stop is independent of candidate qualification.
            order_position = (
                self.lower_index.first_greater(left, right, order_stop_level)
                if self.order_direction == "bearish"
                else self.lower_index.first_less(left, right, order_stop_level)
            )

            candidate_gate = max(scan_start, candidate_start or scan_start)
            if fallback_on_unqualified_cross:
                qualified_start = candidate_gate
                candidate_family = "fallback"
            else:
                blue_time = (
                    self._reset_blue_formation_by_reaction.get(trend_reaction_number)
                    if 1 <= trend_reaction_number <= len(self.trend_reactions)
                    else None
                )
                trend_position = bisect_right(
                    self._trend_confirmation_times_sorted, behavior_start
                )
                trend_time = (
                    self._trend_confirmation_times_sorted[trend_position]
                    if trend_position < len(self._trend_confirmation_times_sorted)
                    else None
                )
                qualifiers = [
                    value for value in (blue_time, trend_time) if value is not None
                ]
                if not qualifiers:
                    candidate_position = None
                else:
                    qualified_start = max(candidate_gate, min(qualifiers))
                    candidate_family = "blue"
                    candidate_left = bisect_left(self.lower_times, qualified_start, left, right)
                    candidate_position = (
                        self.lower_index.first_less(
                            candidate_left, right, candidate_level
                        )
                        if self.direction == "bullish"
                        else self.lower_index.first_greater(
                            candidate_left, right, candidate_level
                        )
                    )
            if fallback_on_unqualified_cross:
                candidate_left = bisect_left(self.lower_times, qualified_start, left, right)
                candidate_position = (
                    self.lower_index.first_less(candidate_left, right, candidate_level)
                    if self.direction == "bullish"
                    else self.lower_index.first_greater(candidate_left, right, candidate_level)
                )

            if order_position is None and candidate_position is None:
                return None
            if order_position is not None and candidate_position == order_position:
                return None
            if order_position is not None and (
                candidate_position is None or order_position < candidate_position
            ):
                event_time = self.lower_times[order_position]
                index = self._main_index(event_time)
                return (
                    "red", index, getattr(self.candles[index], "timestamp"), event_time
                )
            assert candidate_position is not None
            event_time = self.lower_times[candidate_position]
            if fallback_on_unqualified_cross and (
                self._candidate_cross_has_blue(trend_reaction_number, event_time)
                or self._has_ordinary_trend_reaction(behavior_start, event_time)
            ):
                candidate_family = "blue"
            index = self._main_index(event_time)
            return (
                candidate_family,
                index,
                getattr(self.candles[index], "timestamp"),
                event_time,
            )

        # Preserve the established no-lower-data main-candle fallback exactly.
        start_index = max(
            self.start_index, bisect_right(self.candle_times, start) - 1
        )
        for item in self.candles[start_index : self.end_index + 1]:
            event_time = getattr(item, "timestamp")
            candidate_cross = (
                self._candidate_crossed(item, candidate_level)
                and (candidate_start is None or event_time >= candidate_start)
            )
            order_cross = self._order_stop_crossed(item, order_stop_level)
            if candidate_cross and order_cross:
                return None
            if order_cross:
                return (
                    "red", int(getattr(item, "index")), event_time, event_time
                )
            if (
                candidate_cross
                and (
                    self._candidate_cross_has_blue(trend_reaction_number, event_time)
                    or self._has_ordinary_trend_reaction(behavior_start, event_time)
                )
            ):
                return (
                    "blue", int(getattr(item, "index")), event_time, event_time
                )
            if candidate_cross and fallback_on_unqualified_cross:
                return (
                    "fallback", int(getattr(item, "index")), event_time, event_time
                )
        return None


    def _build_type3_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        type3: tuple[int, datetime, Decimal, int, datetime, int, datetime, datetime],
    ) -> SZone:
        """Build the order-free Blue Type-3 continuation for one stopped A."""
        a_stop_index, a_stop_time, a_stop_event_time = a_stop
        (
            source_index,
            source_time,
            price,
            decision_index,
            decision_time,
            reset_reaction_number,
            reset_time,
            decision_event_time,
        ) = type3
        return SZone(
            direction=self.direction,
            color="blue",
            formation_type="type3",
            a_ordinal=a_ordinal,
            a_source_index=int(getattr(zone, "source_index")),
            a_source_time=getattr(zone, "source_time"),
            a_price=a_price,
            a_stop_index=a_stop_index,
            a_stop_time=a_stop_time,
            a_stop_event_time=a_stop_event_time,
            order_direction=None,
            order_reaction_number=None,
            order_mode=None,
            order_first_index=None,
            order_first_time=None,
            order_break_index=None,
            order_break_time=None,
            order_confirmation_time=None,
            order_box_top=None,
            order_box_top_source_index=None,
            order_box_top_source_time=None,
            order_box_bottom=None,
            order_box_bottom_source_index=None,
            order_box_bottom_source_time=None,
            order_stop_level=None,
            order_stop_source_index=None,
            order_stop_source_time=None,
            reset_reaction_number=reset_reaction_number,
            reset_time=reset_time,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event_time,
        )

    def _build_order_backed_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        order_match: tuple[int, object, datetime],
    ) -> SZone | None:
        """Resolve Simple/Advanced S ownership after a stopped A finds an Order."""
        a_stop_index, a_stop_time, a_stop_event_time = a_stop
        order_number, order, order_confirmation_time = order_match
        order_stop_level, order_stop_source_index, order_stop_source_time = (
            self._order_stop(order_number, order)
        )
        candidate_timing = self._candidate_timing(
            a_stop_index, order, order_confirmation_time, a_stop_event_time
        )
        pre_order_candidate = (
            self._candidate_before_order(
                a_stop_index,
                order,
                a_stop_event_time=a_stop_event_time,
            )
            if candidate_timing == "before"
            else None
        )

        decision_behavior_start = a_stop_event_time
        decision = None
        use_pre_order_candidate = False
        if pre_order_candidate is not None:
            formation_type = "simple"
            source_index, source_time, price = pre_order_candidate
            red_source = pre_order_candidate
            trend_reaction_number = 0
            candidate_event_time = self._candidate_event_time(
                source_index, price, a_stop_event_time
            )
            decision_behavior_start = candidate_event_time
            decision = self._decision(
                price,
                order_stop_level,
                order_confirmation_time,
                trend_reaction_number,
                decision_behavior_start,
                candidate_event_time,
                fallback_on_unqualified_cross=True,
            )
            if decision is None:
                return None
            if decision[0] != "fallback":
                use_pre_order_candidate = True
            else:
                decision = None

        advanced_blue = False
        if not use_pre_order_candidate:
            decision_behavior_start = a_stop_event_time
            nested_match = self._nested_trend_reaction(
                order, order_confirmation_time
            )
            advanced_blue = nested_match is not None

        if not use_pre_order_candidate and advanced_blue:
            formation_type = "advanced"
            red_source = None
            trend_reaction_number, _, trend_confirmation_time = nested_match
            source_index = int(
                getattr(
                    order,
                    "box_bottom_source_idx"
                    if self.direction == "bullish"
                    else "box_top_source_idx",
                )
            )
            source_time = getattr(self.candles[source_index], "timestamp")
            price = self._trend_extreme(self.candles[source_index])
            decision_candidate_start = trend_confirmation_time
        elif not use_pre_order_candidate:
            formation_type = "simple"
            trend_match = self._first_trend_reaction_after_order(
                order_confirmation_time
            )
            if trend_match is None:
                return None
            trend_reaction_number, trend_reaction, trend_confirmation_time = (
                trend_match
            )
            source_index, source_time, price = self._simple_candidate(
                order, trend_reaction
            )
            red_source = (
                pre_order_candidate
                if pre_order_candidate is not None
                else self._candidate_after_order(
                    order_confirmation_time, trend_reaction
                )
            )
            decision_candidate_start = trend_confirmation_time

        if decision is None:
            decision = self._decision(
                price,
                order_stop_level,
                order_confirmation_time,
                trend_reaction_number,
                decision_behavior_start,
                decision_candidate_start,
            )
        if decision is None:
            return None

        color, decision_index, decision_time, decision_event_time = decision
        order_break_index = int(getattr(order, "break_idx"))
        if color == "red":
            if use_pre_order_candidate and red_source is not None:
                source_index, source_time, price = red_source
            else:
                source_index, source_time, price = self._candidate_source(
                    order_break_index, decision_index
                )

        order_first_index = int(getattr(order, "first_idx"))
        box_top_source_index = int(getattr(order, "box_top_source_idx"))
        box_bottom_source_index = int(getattr(order, "box_bottom_source_idx"))
        return SZone(
            direction=self.direction,
            color=color,
            formation_type=formation_type,
            a_ordinal=a_ordinal,
            a_source_index=int(getattr(zone, "source_index")),
            a_source_time=getattr(zone, "source_time"),
            a_price=a_price,
            a_stop_index=a_stop_index,
            a_stop_time=a_stop_time,
            a_stop_event_time=a_stop_event_time,
            order_direction=self.order_direction,
            order_reaction_number=order_number,
            order_mode=str(getattr(order, "mode")),
            order_first_index=order_first_index,
            order_first_time=getattr(
                self.candles[order_first_index], "timestamp"
            ),
            order_break_index=order_break_index,
            order_break_time=getattr(
                self.candles[order_break_index], "timestamp"
            ),
            order_confirmation_time=order_confirmation_time,
            order_box_top=as_decimal(getattr(order, "box_top")),
            order_box_top_source_index=box_top_source_index,
            order_box_top_source_time=getattr(
                self.candles[box_top_source_index], "timestamp"
            ),
            order_box_bottom=as_decimal(getattr(order, "box_bottom")),
            order_box_bottom_source_index=box_bottom_source_index,
            order_box_bottom_source_time=getattr(
                self.candles[box_bottom_source_index], "timestamp"
            ),
            order_stop_level=order_stop_level,
            order_stop_source_index=order_stop_source_index,
            order_stop_source_time=order_stop_source_time,
            reset_reaction_number=None,
            reset_time=None,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event_time,
        )

    def detect(self) -> list[SZone]:
        output: list[SZone] = []
        self.a_ownership_windows.clear()
        self.order_audit.clear()
        for zone in self.a_zones:
            self._audit_stopped_a(zone)

        cycle_start_time = self.range_start
        for zone_offset, zone in enumerate(self.a_zones):
            a_ordinal = zone_offset + 1
            if self._a_owned_by_s(zone):
                continue
            source_time = getattr(zone, "source_time")
            if source_time < cycle_start_time or (
                source_time == cycle_start_time and output
            ):
                continue

            next_a_confirmation = (
                self._a_confirmation_time(self.a_zones[zone_offset + 1])
                if zone_offset + 1 < len(self.a_zones)
                else None
            )
            a_price = as_decimal(getattr(zone, "price"))
            a_stop = self._first_a_stop(a_price, self._a_confirmation_time(zone))
            if a_stop is None:
                continue
            _, _, a_stop_event_time = a_stop
            order_match = self._first_order_after(a_stop_event_time)
            if (
                next_a_confirmation is not None
                and a_stop_event_time >= next_a_confirmation
            ):
                continue

            self.a_ownership_windows.append((a_stop_event_time, None))
            no_order_deadline = (
                order_match[2] if order_match is not None else self.range_end
            )
            type3 = self._first_type3(a_stop_event_time, no_order_deadline)
            type4 = self._first_type4(a_stop, no_order_deadline)
            # Type-3 and Type-4 are independent order-free S-Blue routes.
            # Exact decision chronology owns the handoff; preserve established
            # Type-3 precedence only on a true exact-event tie.
            if type3 is not None and (type4 is None or type3[-1] <= type4[-1]):
                s_zone = self._build_type3_zone(
                    zone, a_ordinal, a_price, a_stop, type3
                )
            elif type4 is not None:
                s_zone = self._build_type4_zone(
                    zone, a_ordinal, a_price, a_stop, type4
                )
            elif order_match is not None:
                s_zone = self._resolved_order_backed_zone(
                    zone, a_ordinal, a_price, a_stop, order_match
                )
                if s_zone is None:
                    continue
            else:
                continue

            output.append(s_zone)
            cycle_start_time = s_zone.source_time
            self.a_ownership_windows[-1] = (
                a_stop_event_time,
                max(
                    a_stop_event_time,
                    s_zone.decision_event_time + timedelta(microseconds=1),
                ),
            )

        return sorted(
            output,
            key=lambda item: (item.source_time, item.decision_event_time),
        )


    def _shared_order_stop_cross(
        self, confirmation: datetime, level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        """Return the first strict stop of an accepted Order after confirmation."""
        scan_start = max(confirmation, self.range_start)
        left = bisect_left(self.lower_times, scan_start)
        right = bisect_left(self.lower_times, self.range_end)
        if right > left and self.lower_index is not None:
            position = (
                self.lower_index.first_greater(left, right, level)
                if self.order_direction == "bearish"
                else self.lower_index.first_less(left, right, level)
            )
            if position is None:
                return None
            event_time = self.lower_times[position]
            index = self._main_index(event_time)
            return index, getattr(self.candles[index], "timestamp"), event_time

        for item in self.lower[left:right]:
            if self._order_stop_crossed(item, level):
                event_time = getattr(item, "timestamp")
                index = self._main_index(event_time)
                return index, getattr(self.candles[index], "timestamp"), event_time
        return None

    def reconcile_shared_order_stops(
        self,
        zones: Sequence[SZone],
        order_entries: Sequence[dict[str, object]],
    ) -> list[SZone]:
        """Resolve open S candidates with any accepted physical Order stop.

        Order confirmation is parent-neutral.  The decisive Order does not have
        to originate from the A/S candidate currently being resolved.  Once a
        physical Order is calculation-accepted, it may decide an S candidate if
        the Order is live in that candidate window and its exact strict stop is
        after the frozen S source but before the candidate's current strict
        decision event.  Creation provenance remains attached to the Order and
        is never rewritten to the S candidate.

        This rule is direction invariant.  The strict Order stop itself is
        resolved by the shared mirrored lower-timeframe chronology.
        """
        deduped: dict[tuple[int, int], dict[str, object]] = {}
        for entry in order_entries:
            reaction = entry.get("reaction")
            if reaction is None:
                continue
            identity = (
                int(getattr(reaction, "first_idx")),
                int(getattr(reaction, "break_idx")),
            )
            current = deduped.get(identity)
            # Prefer the richer accepted E-audit form when it already carries
            # an exact stop crossing.  Physical identity, not parent identity,
            # is authoritative.
            if current is None or (
                current.get("stop_cross") is None
                and entry.get("stop_cross") is not None
            ):
                deduped[identity] = entry

        # Performance implementation detail: physical Order stop chronology is
        # immutable for this reconciliation pass.  The legacy implementation
        # recomputed the same strict crossing once per (S, Order) pair.  Build
        # each exact candidate once, preserve the authoritative winner key
        # (crossEvent, confirmation, FirstIndex, BreakIndex), then bisect by the
        # frozen S decision window.  This changes only lookup complexity.
        shared_candidates: list[tuple[
            datetime, datetime, int, int, dict[str, object],
            tuple[int, datetime, datetime]
        ]] = []
        for identity, entry in deduped.items():
            reaction = entry["reaction"]
            first_index = int(getattr(reaction, "first_idx"))
            confirmation = entry.get("confirmation_time")
            if not isinstance(confirmation, datetime):
                continue
            stop_level = as_decimal(entry["stop_level"])
            crossed = entry.get("stop_cross")
            if not (
                isinstance(crossed, tuple)
                and len(crossed) >= 3
                and isinstance(crossed[2], datetime)
            ):
                crossed = self._shared_order_stop_cross(confirmation, stop_level)
            if crossed is None or not confirmation < crossed[2]:
                continue
            shared_candidates.append((
                crossed[2], confirmation, first_index, identity[1], entry, crossed
            ))
        shared_candidates.sort(key=lambda item: item[:4])
        shared_cross_times = [item[0] for item in shared_candidates]

        output: list[SZone] = []
        for zone in zones:
            left = bisect_left(shared_cross_times, zone.source_time)
            winner = None
            if left < len(shared_candidates):
                candidate = shared_candidates[left]
                if candidate[0] < zone.decision_event_time:
                    winner = candidate

            if winner is None:
                output.append(zone)
                continue

            _, _, _, _, entry, crossed = winner
            reaction = entry["reaction"]
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            top_source = int(getattr(reaction, "box_top_source_idx"))
            bottom_source = int(getattr(reaction, "box_bottom_source_idx"))
            output.append(replace(
                zone,
                color="red",
                order_reaction_number=int(entry.get("reaction_number", 0)),
                order_mode=str(getattr(reaction, "mode")),
                order_first_index=first_index,
                order_first_time=getattr(self.candles[first_index], "timestamp"),
                order_break_index=break_index,
                order_break_time=getattr(self.candles[break_index], "timestamp"),
                order_confirmation_time=entry["confirmation_time"],
                order_box_top=as_decimal(getattr(reaction, "box_top")),
                order_box_top_source_index=top_source,
                order_box_top_source_time=getattr(self.candles[top_source], "timestamp"),
                order_box_bottom=as_decimal(getattr(reaction, "box_bottom")),
                order_box_bottom_source_index=bottom_source,
                order_box_bottom_source_time=getattr(self.candles[bottom_source], "timestamp"),
                order_stop_level=as_decimal(entry["stop_level"]),
                order_stop_source_index=int(entry["stop_source_index"]),
                order_stop_source_time=entry["stop_source_time"],
                reset_reaction_number=None,
                reset_time=None,
                decision_index=int(crossed[0]),
                decision_time=crossed[1],
                decision_event_time=crossed[2],
            ))
        return output



def detect_s_zones(
    direction: str,
    trend_reactions: Sequence[object],
    opposite_reactions: Sequence[object],
    trend_blue_lines: Sequence[object],
    a_zones: Sequence[object],
    chronology: object,
    start_index: int | None = None,
    end_index: int | None = None,
    opposite_resets: Sequence[object] = (),
    initial_order_geometry: Callable[[int, datetime, int], object | None] | None = None,
) -> list[SZone]:
    return SZoneDetector(
        direction,
        trend_reactions,
        opposite_reactions,
        trend_blue_lines,
        a_zones,
        chronology,
        start_index,
        end_index,
        opposite_resets,
        initial_order_geometry,
    ).detect()
