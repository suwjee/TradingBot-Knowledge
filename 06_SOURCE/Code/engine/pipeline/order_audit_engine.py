"""Central physical Order discovery, reuse, provenance, and audit ownership."""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from typing import Callable, Sequence

from core_utils import as_decimal, order_identity, reaction_identity

ORDER_AUDIT_ENGINE_VERSION = "1.5.1"
ORDER_AUDIT_ENGINE_LAST_MODIFIED = "2026-09-28 19:35:32 +03:30"

@dataclass(frozen=True, slots=True)
class PostBehaviorStop:
    behavior_type: str
    behavior_source_index: int
    behavior_source_time: datetime
    event_time: datetime


@dataclass(frozen=True, slots=True)
class OrderBBehaviorAnchor:
    behavior_type: str
    behavior_source_index: int
    behavior_source_time: datetime
    priority: int
    number: int


@dataclass(frozen=True, slots=True)
class OrderBResetLeg:
    post_stop: PostBehaviorStop
    anchor_behavior_type: str
    anchor_behavior_source_index: int
    anchor_behavior_source_time: datetime
    anchor_behavior_extreme: Decimal
    reset_reaction: object
    reset_confirmation_time: datetime
    reset_source_index: int
    reset_broken_level: Decimal
    reset_time: datetime
    leg_boundary: Decimal
    leg_source_index: int
    leg_source_time: datetime
    strict_break_time: datetime
    reaction_number: int
    physical_reaction: object
    physical_confirmation_time: datetime


def dominant_post_behavior_stops(
    chronology: object,
    lifetimes: Sequence[tuple[str, object, datetime | None]],
    priority: Callable[[object], int],
) -> list[PostBehaviorStop]:
    """Select the accepted lifecycle owner of each stopped main candle."""
    by_candle: dict[int, tuple[tuple[object, ...], PostBehaviorStop]] = {}
    for behavior_type, behavior, event_time in lifetimes:
        if event_time is None:
            continue
        active = [
            item for _type, item, end in lifetimes
            if (
                getattr(item, "trigger_event_time", None)
                or getattr(item, "decision_event_time", None)
                or getattr(item, "source_time")
            ) <= event_time
            and (end is None or event_time <= end)
        ]
        if not active:
            continue
        owner = max(active, key=lambda item: (
            priority(item), int(getattr(item, "number", 0)),
            getattr(item, "source_time"), int(getattr(item, "source_index")),
        ))
        if owner is not behavior:
            continue
        source_time = getattr(behavior, "source_time")
        source_index = int(getattr(behavior, "source_index"))
        stop_index = chronology.main_index(event_time, clamp=True)
        rank = (
            priority(behavior), int(getattr(behavior, "number", 0)),
            source_time, source_index, event_time,
        )
        selected = PostBehaviorStop(
            behavior_type, source_index, source_time, event_time,
        )
        previous = by_candle.get(stop_index)
        if previous is None or rank > previous[0]:
            by_candle[stop_index] = rank, selected
    return sorted(
        (item[1] for item in by_candle.values()),
        key=lambda item: (item.event_time, item.behavior_source_index),
    )


def order_b_reset_event_time(
    direction: str, chronology: object, reset: object,
) -> datetime | None:
    """Resolve a main-candle Reset to its first strict selected-RAW crossing."""
    precise = getattr(reset, "second_time", None)
    if precise:
        return chronology.reset_time(reset)
    reset_index = int(getattr(reset, "index"))
    start = chronology.times[reset_index]
    left = bisect_left(chronology.second_times, start)
    right = bisect_left(chronology.second_times, start + chronology.timeframe)
    level = as_decimal(getattr(reset, "broken_level"))
    if chronology.lower_index is not None:
        crossing = (
            chronology.lower_index.first_less(left, right, level)
            if direction == "bullish" else
            chronology.lower_index.first_greater(left, right, level)
        )
    else:
        attribute = "low" if direction == "bullish" else "high"
        crossing = next((
            index for index in range(left, right)
            if (
                as_decimal(getattr(chronology.seconds[index], attribute)) < level
                if direction == "bullish" else
                as_decimal(getattr(chronology.seconds[index], attribute)) > level
            )
        ), None)
    return None if crossing is None else chronology.second_times[crossing]


def discover_order_b_reset_legs(
    direction: str,
    chronology: object,
    trend_reactions: Sequence[object],
    resets: Sequence[object],
    opposite_reactions: Sequence[object],
    post_stops: Sequence[PostBehaviorStop],
    a_formation_times: Sequence[datetime],
    *,
    behavior_anchors: Sequence[OrderBBehaviorAnchor] = (),
) -> list[OrderBResetLeg]:
    """Find Order_B from post-stop HH/LL reset-leg geometry.

    The stop event opens eligibility, but the geometric anchor is the latest
    accepted behavior that already exists before the Reset Reaction First
    candle, regardless of whether that behavior is dominant.  Bearish uses
    the highest High from the anchor behavior candle through the Reset
    Reaction FirstGreen; Bullish mirrors it with the lowest Low through
    FirstRed.  The boundary must extend strictly beyond the anchor behavior
    candle, the reset Reaction must start strictly after that boundary source,
    and the physical opposite Reaction is the first canonical Reaction whose
    First candle starts at or after the exact strict lower-TF crossing of the
    frozen boundary following Reset, with confirmation strictly after it.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    if not post_stops or not behavior_anchors:
        return []

    candles = chronology.candles
    lower = chronology.seconds
    lower_times = chronology.second_times
    lower_index = chronology.lower_index
    opposite = chronology.opposite_direction(direction)
    attribute = "low" if direction == "bullish" else "high"

    same_direction = sorted(
        (
            chronology.reaction_confirmation(direction, reaction),
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
            ordinal,
            reaction,
        )
        for ordinal, reaction in enumerate(trend_reactions)
    )
    same_by_first: dict[int, list[tuple[datetime, int, int, int, object]]] = {}
    for item in same_direction:
        same_by_first.setdefault(item[1], []).append(item)

    opposite_direction = sorted(
        (
            chronology.reaction_confirmation(opposite, reaction),
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
            number,
            reaction,
        )
        for number, reaction in enumerate(opposite_reactions, start=1)
    )
    reset_events = sorted(
        (
            event_time,
            int(getattr(reset, "from_first_idx")), ordinal, reset,
        )
        for ordinal, reset in enumerate(resets)
        if (event_time := order_b_reset_event_time(direction, chronology, reset))
        is not None
    )
    stops = sorted(
        post_stops,
        key=lambda item: (
            item.event_time, item.behavior_source_time,
            item.behavior_source_index, item.behavior_type,
        ),
    )
    stop_times = [item.event_time for item in stops]
    anchors = sorted(
        behavior_anchors,
        key=lambda item: (
            item.behavior_source_time, item.behavior_source_index,
            item.priority, item.number, item.behavior_type,
        ),
    )
    anchor_times = [item.behavior_source_time for item in anchors]
    a_times = sorted(a_formation_times)

    found: list[OrderBResetLeg] = []
    for reset_time, reset_first, _ordinal, reset in reset_events:
        current_candidates = [
            item for item in same_by_first.get(reset_first, ())
            if item[0] < reset_time
        ]
        if not current_candidates:
            continue
        current = current_candidates[-1]
        current_first_time = chronology.times[current[1]]

        stop_position = bisect_left(stop_times, current_first_time) - 1
        if stop_position < 0:
            continue
        post_stop = stops[stop_position]

        anchor_position = bisect_left(anchor_times, current_first_time) - 1
        if anchor_position < 0:
            continue
        anchor = anchors[anchor_position]
        if anchor.behavior_source_index > current[1]:
            continue

        anchor_extreme = as_decimal(
            getattr(candles[anchor.behavior_source_index], attribute)
        )
        source_index = anchor.behavior_source_index
        boundary = anchor_extreme
        for index in range(anchor.behavior_source_index + 1, current[1] + 1):
            value = as_decimal(getattr(candles[index], attribute))
            if (value < boundary if direction == "bullish" else value > boundary):
                boundary, source_index = value, index

        extends_anchor = (
            boundary < anchor_extreme
            if direction == "bullish" else boundary > anchor_extreme
        )
        if not extends_anchor:
            continue
        # The Reset Reaction itself must occur after the LL/HH source.
        if source_index >= current[1]:
            continue

        left = bisect_right(lower_times, reset_time)
        right = len(lower_times)
        if left >= right:
            continue
        if lower_index is not None:
            crossing = (
                lower_index.first_less(left, right, boundary)
                if direction == "bullish"
                else lower_index.first_greater(left, right, boundary)
            )
        else:
            crossing = next((
                index for index in range(left, right)
                if (
                    as_decimal(getattr(lower[index], attribute)) < boundary
                    if direction == "bullish" else
                    as_decimal(getattr(lower[index], attribute)) > boundary
                )
            ), None)
        if crossing is None:
            continue
        strict_break_time = lower_times[crossing]

        # A newly formed A is an upstream, Order_B-independent lifecycle
        # boundary.  A reset-leg that was prepared before that A may not stay
        # pending and fire after it; the new A is now the behavior context for
        # subsequent Order logic.  Using A as the hard expiry also keeps the
        # Order_B feedback monotonic because S/E/StopAll may themselves depend
        # on Order_B while A does not.
        next_a_position = bisect_right(a_times, current_first_time)
        if (
            next_a_position < len(a_times)
            and a_times[next_a_position] <= strict_break_time
        ):
            continue

        physical = next((
            item for item in opposite_direction
            if strict_break_time <= chronology.times[item[1]]
            and strict_break_time < item[0]
        ), None)
        if physical is None:
            continue

        found.append(OrderBResetLeg(
            post_stop=post_stop,
            anchor_behavior_type=anchor.behavior_type,
            anchor_behavior_source_index=anchor.behavior_source_index,
            anchor_behavior_source_time=anchor.behavior_source_time,
            anchor_behavior_extreme=anchor_extreme,
            reset_reaction=current[4],
            reset_confirmation_time=current[0],
            reset_source_index=int(getattr(reset, "index")),
            reset_broken_level=as_decimal(getattr(reset, "broken_level")),
            reset_time=reset_time,
            leg_boundary=boundary,
            leg_source_index=source_index,
            leg_source_time=chronology.times[source_index],
            strict_break_time=strict_break_time,
            reaction_number=physical[3],
            physical_reaction=physical[4],
            physical_confirmation_time=physical[0],
        ))
    return found


def discover_accepted_order_b_reset_legs(
    direction: str,
    chronology: object,
    trend_reactions: Sequence[object],
    trend_resets: Sequence[object],
    opposite_reactions: Sequence[object],
    a_zones: Sequence[object],
    invalid_a_identities: set[tuple[datetime, int]],
    s_zones: Sequence[object],
    e_zones: Sequence[object],
    stopalls: Sequence[object],
    s_detector: object,
    e_detector: object,
    priority: Callable[[object], int],
) -> list[OrderBResetLeg]:
    """Build reset legs from calculation-accepted lifecycle owners."""
    accepted_a = [
        item for item in a_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in invalid_a_identities
    ]
    lifetimes: list[tuple[str, object, datetime | None]] = []
    for item in accepted_a:
        ordinal = int(getattr(item, "reaction_number"))
        confirmation = chronology.reaction_confirmation(
            direction, trend_reactions[ordinal - 1]
        )
        stopped = s_detector.first_a_stop(
            as_decimal(getattr(item, "price")), confirmation
        )
        lifetimes.append(("A", item, stopped[2] if stopped is not None else None))
    for behavior_type, items in (("S", s_zones), ("E", e_zones)):
        for item in items:
            stopped = e_detector.parent_stop(behavior_type, item)
            lifetimes.append((
                behavior_type, item, stopped[1] if stopped is not None else None
            ))
    lifetimes.extend(
        ("StopAll", item, item.stop_event_time)
        for item in stopalls
    )
    dominant = dominant_post_behavior_stops(chronology, lifetimes, priority)

    anchor_candidates: list[OrderBBehaviorAnchor] = []
    for behavior_type, items in (
        ("A", accepted_a), ("S", s_zones), ("E", e_zones),
        ("StopAll", stopalls),
    ):
        for item in items:
            anchor_candidates.append(OrderBBehaviorAnchor(
                behavior_type=behavior_type,
                behavior_source_index=int(getattr(item, "source_index")),
                behavior_source_time=getattr(item, "source_time"),
                priority=priority(item),
                number=int(getattr(item, "number", 0)),
            ))

    # A single source candle may represent several lifecycle projections
    # (for example A/E/StopAll).  The highest lifecycle priority owns only the
    # tie at that exact source; a later lower-priority behavior still becomes
    # the geometric anchor because the rule is explicitly dominant-neutral.
    anchors_by_source: dict[tuple[datetime, int], OrderBBehaviorAnchor] = {}
    for anchor in anchor_candidates:
        key = (anchor.behavior_source_time, anchor.behavior_source_index)
        previous = anchors_by_source.get(key)
        if previous is None or (anchor.priority, anchor.number, anchor.behavior_type) > (
            previous.priority, previous.number, previous.behavior_type
        ):
            anchors_by_source[key] = anchor

    return discover_order_b_reset_legs(
        direction, chronology, trend_reactions, trend_resets,
        opposite_reactions, dominant,
        [item.trigger_event_time for item in accepted_a],
        behavior_anchors=tuple(anchors_by_source.values()),
    )


OrderMatch = tuple[
    int, object, datetime, Decimal, int, datetime,
    tuple[int, datetime, datetime] | None, tuple[str, ...],
    datetime | None,
]


def order_b_leg_identity(items: Sequence[object]) -> tuple[object, ...]:
    """Identify every accepted HH/LL Order_B cause across lifecycle passes."""
    return tuple(sorted((
        leg.post_stop.behavior_type,
        leg.post_stop.behavior_source_index,
        leg.post_stop.event_time,
        leg.anchor_behavior_type,
        leg.anchor_behavior_source_index,
        leg.anchor_behavior_source_time,
        leg.anchor_behavior_extreme,
        int(getattr(leg.reset_reaction, "first_idx")),
        int(getattr(leg.reset_reaction, "break_idx")),
        leg.reset_source_index,
        leg.reset_broken_level,
        leg.reset_time,
        leg.leg_boundary,
        leg.leg_source_index,
        leg.strict_break_time,
        int(getattr(leg.physical_reaction, "first_idx")),
        int(getattr(leg.physical_reaction, "break_idx")),
    ) for leg in items))



class OrderAuditEngineMixin:
    """Order methods shared by the accepted E lifecycle detector."""

    def _order_stop(
        self, number: int, reaction: object, context_start: datetime | None = None,
    ) -> tuple[Decimal, int, datetime]:
        del context_start  # Provenance never manufactures a context-only stop.
        if (
            1 <= number <= len(self.opposite_reactions)
            and self.opposite_reactions[number - 1] is reaction
        ):
            cached = self._canonical_order_stop_cache.get(number)
            if cached is not None:
                return cached
            result = self.chronology.canonical_order_stop(
                self.order_direction,
                number,
                reaction,
                self.opposite_reactions,
                start_index=self.start_index,
            )
            self._canonical_order_stop_cache[number] = result
            return result
        return self.chronology.canonical_order_stop(
            self.order_direction,
            number,
            reaction,
            self.opposite_reactions,
            start_index=self.start_index,
        )


    def order_stop(
        self, reaction_number: int, reaction: object
    ) -> tuple[Decimal, int, datetime]:
        """Public audit API for canonical Order stop provenance."""
        return self._order_stop(reaction_number, reaction)


    def _first_healthy_direct_geometry(
        self, start: datetime, allow_bounded_continue: bool = False,
    ) -> tuple[int, object, datetime] | None:
        """Return the first healthy geometry after an A/S/E strict stop.

        A candidate completes normally when the active prior reaction is not
        Reset before its confirmation. If that prior reaction is Reset first,
        the search restarts strictly after the Reset candle and the first
        complete geometry owns the new leg.
        """
        if self.direct_geometry_finder is None:
            return None
        # Geometry needs its complete context candle at or after the exact
        # stop event. A First candle that already opened before the lower-time-
        # frame stop cannot be attributed to that stop.
        search_index = self._main_index(start)
        search_event = start
        restarted = False
        while search_index <= self.end_index:
            candidate = self.direct_geometry_finder(
                self.order_direction, search_index, self.end_index, search_event
            )
            if candidate is None:
                return None
            first = self._reaction_first_time(candidate)
            if (
                first in self.blocked_order_first_times
                and first == self.times[self._main_index(start)]
            ):
                search_index = int(getattr(candidate, "first_idx")) + 1
                search_event = first
                continue
            confirmation = self._confirmation_for(
                candidate, self.order_direction
            )
            owner_position = bisect_right(
                self._opposite_confirmations, search_event
            ) - 1
            prior = (
                self.opposite_reactions[owner_position]
                if owner_position >= 0 else None
            )
            reset_before_confirmation = None
            if prior is not None:
                for reset_time in self._opposite_reset_times_by_first.get(
                    int(getattr(prior, "first_idx")), []
                ):
                    if search_event < reset_time <= confirmation:
                        reset_before_confirmation = reset_time
                        break
            if reset_before_confirmation is not None:
                search_index = self._main_index(reset_before_confirmation)
                search_event = reset_before_confirmation
                restarted = True
                continue

            identity = (
                int(getattr(candidate, "first_idx")),
                int(getattr(candidate, "break_idx")),
            )
            canonical_position = self._opposite_identity_position.get(identity)
            if canonical_position is None:
                # Order_A is a physical Order and may only be created from a
                # canonical valid Reaction. Gate-bounded geometry can remain
                # internal continuation evidence, but it must never bypass
                # Reaction/Reset ownership and become Order_A. Canonical
                # fallback is handled by `_direct_parent_stop_order`.
                return None
            candidate = self.opposite_reactions[canonical_position]
            number = canonical_position + 1
            confirmation = self._opposite_confirmations[canonical_position]
            return number, candidate, confirmation
        return None


    def _trend_leg_direct_order(
        self, start: datetime,
    ) -> tuple[int, object, datetime] | None:
        """Return bounded direct Order_A after a newly confirmed trend leg.

        A stopped E may be followed by a fresh same-direction Reaction before
        the next opposite public Reaction exists.  That trend confirmation
        establishes the new forming-leg boundary.  The first bounded opposite
        geometry after that exact confirmation may own direct Order_A when the
        shared gate resolver proves ``continue``.  This is direct
        parent-stop Order_A provenance.
        """
        if self.direct_geometry_finder is None:
            return None
        position = bisect_right(self._trend_confirmation_times, start)
        while position < len(self._trend_by_confirmation):
            confirmation, first_time, trend = self._trend_by_confirmation[position]
            position += 1
            if first_time <= start:
                continue
            if bool(getattr(trend, "behavior_internal", False)):
                continue
            break_index = int(getattr(trend, "break_idx"))
            candidate = self.direct_geometry_finder(
                self.order_direction, break_index, self.end_index, confirmation
            )
            if candidate is None:
                continue
            if getattr(candidate, "order_gate_decision", None) != "continue":
                continue
            candidate_confirmation = self._confirmation_for(
                candidate, self.order_direction
            )
            if self._reaction_first_time(candidate) <= confirmation:
                continue
            identity = (
                int(getattr(candidate, "first_idx")),
                int(getattr(candidate, "break_idx")),
            )
            canonical_position = self._opposite_identity_position.get(identity)
            if canonical_position is not None:
                return (
                    canonical_position + 1,
                    self.opposite_reactions[canonical_position],
                    self._opposite_confirmations[canonical_position],
                )
            # A bounded geometry that is absent from the canonical opposite
            # Reaction stream is internal evidence only, not an Order_A.
            continue
        return None


    def _direct_parent_stop_order(
        self,
        start: datetime,
        continuous_deadline: datetime | None,
        allow_bounded_continue: bool,
    ) -> tuple[int, object, datetime] | None:
        """Select the direct parent-stop Order_A."""
        gate_time = self.times[self._main_index(start)]
        geometric_direct = self._first_healthy_direct_geometry(
            start, allow_bounded_continue
        )
        direct_position = bisect_left(self._opposite_first_times, gate_time)
        while (
            direct_position < len(self.opposite_reactions)
            and self._opposite_first_times[direct_position]
            in self.blocked_order_first_times
            and self._opposite_first_times[direct_position] == gate_time
        ):
            direct_position += 1

        independent = None
        if direct_position < len(self.opposite_reactions):
            independent = (
                direct_position + 1,
                self.opposite_reactions[direct_position],
                self._opposite_confirmations[direct_position],
            )
        geometric_gate_decision = (
            getattr(geometric_direct[1], "order_gate_decision", None)
            if geometric_direct is not None
            else None
        )
        prefer_geometric = (
            continuous_deadline is not None
            and geometric_direct is not None
            and geometric_gate_decision == "restart"
            and (
                continuous_deadline == self.range_end
                or continuous_deadline < geometric_direct[2]
            )
        )
        independent_cross = None
        if independent is not None:
            independent_level, _, _ = self._order_stop(
                independent[0], independent[1]
            )
            independent_cross = self._cross_order(
                independent[2], independent_level
            )

        direct_pool: list[tuple[int, object, datetime]] = []
        if prefer_geometric:
            direct_pool.append(geometric_direct)
        elif (
            geometric_direct is not None
            and independent_cross is None
            and (
                independent is None
                or self._reaction_first_time(geometric_direct[1])
                < self._reaction_first_time(independent[1])
            )
        ):
            direct_pool.append(geometric_direct)
        elif independent is not None:
            direct_pool.append(independent)

        if not direct_pool:
            return None
        return min(
            direct_pool,
            key=lambda item: (self._reaction_first_time(item[1]), item[2]),
        )


    def _merge_order_candidate(
        self,
        by_geometry: dict[tuple[int, int], OrderMatch],
        number: int,
        reaction: object,
        confirmation: datetime,
        *,
        parent_stop_cause_time: datetime,
    ) -> OrderMatch:
        """Register one parent-stop Order_A candidate by physical identity."""
        level, source, source_time = self._order_stop(number, reaction)
        crossed = self._cross_order(confirmation, level)
        key = reaction_identity(reaction)
        match: OrderMatch = (
            number,
            reaction,
            confirmation,
            level,
            source,
            source_time,
            crossed,
            ("parent-stop",),
            parent_stop_cause_time,
        )
        existing = by_geometry.get(key)
        if existing is None or (
            confirmation, int(getattr(reaction, "first_idx")), int(getattr(reaction, "break_idx"))
        ) < (
            existing[2], int(getattr(existing[1], "first_idx")), int(getattr(existing[1], "break_idx"))
        ):
            by_geometry[key] = match
        return by_geometry[key]


    def _enforce_single_parent_stop_owner(
        self, by_geometry: dict[tuple[int, int], OrderMatch]
    ) -> None:
        """Keep exactly one physical Order_A for one parent-stop event."""
        parent_candidates = [
            item for item in by_geometry.values() if "parent-stop" in item[7]
        ]
        if len(parent_candidates) <= 1:
            return
        owner = min(
            parent_candidates,
            key=lambda item: (
                item[2], int(getattr(item[1], "first_idx")),
                int(getattr(item[1], "break_idx")),
            ),
        )
        owner_identity = reaction_identity(owner[1])
        for identity, item in list(by_geometry.items()):
            if identity == owner_identity or "parent-stop" not in item[7]:
                continue
            remaining = tuple(cause for cause in item[7] if cause != "parent-stop")
            if remaining:
                by_geometry[identity] = (*item[:7], remaining, None)
            else:
                del by_geometry[identity]


    def order_candidates(
        self,
        start: datetime,
        continuous_deadline: datetime | None = None,
        allow_bounded_continue: bool = False,
        allow_trend_leg_continue: bool = False,
    ) -> list[OrderMatch]:
        """Return physical Order candidates formed before this E decision."""
        cache_key = (
            start,
            continuous_deadline,
            allow_bounded_continue,
            allow_trend_leg_continue,
        )
        cached = self._order_candidates_cache.get(cache_key)
        if cached is not None:
            return list(cached)

        by_geometry: dict[tuple[int, int], OrderMatch] = {}
        direct = self._direct_parent_stop_order(
            start, continuous_deadline, allow_bounded_continue
        )
        if direct is not None:
            self._merge_order_candidate(
                by_geometry,
                *direct,
                parent_stop_cause_time=start,
            )

        if allow_trend_leg_continue:
            trend_direct = self._trend_leg_direct_order(start)
            if trend_direct is not None:
                self._merge_order_candidate(
                    by_geometry,
                    *trend_direct,
                    parent_stop_cause_time=start,
                )

        # Reset-leg provenance is independent of the one-Order-per-parent
        # parent-stop rule, but shares the canonical physical identity.
        for leg in self.order_b_legs:
            reaction = leg.physical_reaction
            if self._reaction_first_time(reaction) <= start:
                continue
            identity = reaction_identity(reaction)
            previous = by_geometry.get(identity)
            if previous is not None:
                by_geometry[identity] = (
                    *previous[:7],
                    tuple(dict.fromkeys((*previous[7], "reset-leg"))),
                    previous[8],
                )
                continue
            level, source, source_time = self._order_stop(
                leg.reaction_number, reaction
            )
            by_geometry[identity] = (
                leg.reaction_number, reaction, leg.physical_confirmation_time,
                level, source, source_time,
                self._cross_order(leg.physical_confirmation_time, level),
                ("reset-leg",), None,
            )

        # One exact parent stop may create only one physical Order_A.
        self._enforce_single_parent_stop_owner(by_geometry)

        stopped = [
            item[6][2]
            for item in by_geometry.values()
            if item[6] is not None
        ]
        decision_deadline = min(stopped) if stopped else self.range_end
        if continuous_deadline is not None:
            decision_deadline = min(decision_deadline, continuous_deadline)
        eligible = [
            item for item in by_geometry.values()
            if item[2] <= decision_deadline
        ]
        result = sorted(
            eligible,
            key=lambda item: (
                item[6][2] if item[6] is not None else self.range_end,
                self._reaction_first_time(item[1]),
            ),
        )
        self._order_candidates_cache[cache_key] = tuple(result)
        return result


    def _first_order(
        self, start: datetime, continuous_deadline: datetime | None = None,
        allow_bounded_continue: bool = False,
        allow_trend_leg_continue: bool = False,
    ) -> OrderMatch | None:
        candidates = [
            item for item in self.order_candidates(
                start, continuous_deadline,
                allow_bounded_continue=allow_bounded_continue,
                allow_trend_leg_continue=allow_trend_leg_continue,
            )
            if item[6] is not None
        ]
        return candidates[0] if candidates else None


    def _has_sequence_reset_between(
        self, start: datetime, end: datetime,
    ) -> bool:
        """Return whether a known hard reset lies in ``(start, end]``."""
        position = bisect_right(self._sequence_reset_times, start)
        return (
            position < len(self._sequence_reset_times)
            and self._sequence_reset_times[position] <= end
        )


    def _index_order_audit_identity(
        self, identity: tuple[int, int], confirmation: datetime,
    ) -> None:
        """Index one newly accepted physical Order by confirmation chronology."""
        first_index, break_index = identity
        item = (confirmation, first_index, break_index)
        position = bisect_right(self._order_audit_confirmation_index, item)
        self._order_audit_confirmation_index.insert(position, item)


    def _clear_order_audit(self) -> None:
        self.order_audit.clear()
        self._order_audit_confirmation_index.clear()
        self._carried_orders_cache.clear()


    def register_order_b_reset_legs(
        self, legs: Sequence[OrderBResetLeg],
    ) -> None:
        """Merge proven reset-leg causes by canonical physical identity."""
        if legs:
            self._carried_orders_cache.clear()
        for leg in legs:
            reaction = leg.physical_reaction
            identity = reaction_identity(reaction)
            entry = self.order_audit.get(identity)
            if entry is None:
                level, source, source_time = self._order_stop(
                    leg.reaction_number, reaction
                )
                entry = {
                    "reaction_number": leg.reaction_number,
                    "reaction": reaction,
                    "confirmation_time": leg.physical_confirmation_time,
                    "stop_level": level,
                    "stop_source_index": source,
                    "stop_source_time": source_time,
                    "stop_cross": self._cross_order(
                        leg.physical_confirmation_time, level
                    ),
                    "causes": set(),
                }
                self.order_audit[identity] = entry
                self._index_order_audit_identity(
                    identity, leg.physical_confirmation_time
                )
            current = leg.reset_reaction
            cause = {
                "kind": "reset-leg",
                "postBehaviorType": leg.post_stop.behavior_type,
                "postBehaviorStopTime": leg.post_stop.event_time,
                "postBehaviorSourceIndex": leg.post_stop.behavior_source_index,
                "postBehaviorSourceTime": leg.post_stop.behavior_source_time,
                "anchorBehaviorType": leg.anchor_behavior_type,
                "anchorBehaviorSourceIndex": leg.anchor_behavior_source_index,
                "anchorBehaviorSourceTime": leg.anchor_behavior_source_time,
                "anchorBehaviorExtreme": str(leg.anchor_behavior_extreme),
                "resetReactionIdentity": [
                    int(getattr(current, "first_idx")),
                    int(getattr(current, "break_idx")),
                ],
                "resetReactionBreakoutTime": self.times[int(getattr(current, "break_idx"))],
                "resetReactionConfirmationTime": leg.reset_confirmation_time,
                "resetIndex": leg.reset_source_index,
                "resetBrokenLevel": str(leg.reset_broken_level),
                "resetTime": leg.reset_time,
                "legBoundary": str(leg.leg_boundary),
                "legBoundarySourceIndex": leg.leg_source_index,
                "legBoundarySourceTime": leg.leg_source_time,
                "strictBreakTime": leg.strict_break_time,
                "physicalOrderIdentity": [identity[0], identity[1]],
                "physicalOrderConfirmationTime": leg.physical_confirmation_time,
            }
            causes = entry.setdefault("order_b_causes", [])
            if cause not in causes:
                causes.append(cause)
                causes.sort(key=lambda item: (
                    item["postBehaviorStopTime"], item["resetTime"],
                    item["strictBreakTime"], item["physicalOrderIdentity"],
                ))


    def _register_order_audit(
        self, parent_type: str, parent: object, parent_stop: datetime,
    ) -> None:
        """Register only the physical Order_A created by this parent stop."""
        if parent_type == "S" and (
            parent.source_time, int(parent.source_index)
        ) in self.invalid_s_root_identities:
            return
        if self._has_sequence_reset_between(parent.source_time, parent_stop):
            return
        matches = self.order_candidates(
            parent_stop,
            None,
            allow_bounded_continue=(parent_type == "S"),
            allow_trend_leg_continue=(parent_type == "E"),
        )
        direct = self._direct_parent_stop_order(
            parent_stop, None, allow_bounded_continue=(parent_type == "S")
        )
        if direct is not None:
            direct_identity = reaction_identity(direct[1])
            if all(reaction_identity(item[1]) != direct_identity for item in matches):
                level, source, source_time = self._order_stop(direct[0], direct[1])
                matches.append((
                    direct[0], direct[1], direct[2], level, source, source_time,
                    self._cross_order(direct[2], level), ("parent-stop",),
                    parent_stop,
                ))

        self._carried_orders_cache.clear()
        for match in matches:
            number, reaction, confirmation, level, source, source_time = match[:6]
            crossed, causes = match[6], match[7]
            if "parent-stop" not in causes:
                continue
            key = reaction_identity(reaction)
            entry = self.order_audit.get(key)
            if entry is None:
                entry = {
                    "reaction_number": number,
                    "reaction": reaction,
                    "confirmation_time": confirmation,
                    "stop_level": level,
                    "stop_source_index": source,
                    "stop_source_time": source_time,
                    "stop_cross": crossed,
                    "causes": set(),
                }
                self.order_audit[key] = entry
                self._index_order_audit_identity(key, confirmation)
            audit_causes = entry["causes"]
            assert isinstance(audit_causes, set)
            family = str(getattr(parent, "color", getattr(parent, "family", "")))
            number_value = getattr(parent, "number", None)
            parent_label = parent_type
            if parent_type == "E" and number_value is not None:
                parent_label = f"E{number_value}"
            if parent.source_time in self.sequence_resets:
                parent_label = f"StopAll{self.sequence_resets[parent.source_time]}"
                family = ""
            audit_causes.add((
                "parent-stop", parent_label, family, parent_stop,
                getattr(parent, "source_time"),
            ))


    @staticmethod
    def visual_order_lifecycle(
        self, start: datetime,
    ) -> list[tuple[int, object, datetime, Decimal, int, datetime,
                    tuple[int, datetime, datetime] | None, bool]]:
        """Return the first parent-stop Order_A lifecycle after ``start``."""
        position = bisect_left(self._opposite_first_times, start)
        for order_position in range(position, len(self.opposite_reactions)):
            reaction = self.opposite_reactions[order_position]
            first = self._opposite_first_times[order_position]
            confirmation = self._opposite_confirmations[order_position]
            if first < start or confirmation < start:
                continue
            number = order_position + 1
            level, source, source_time = self._order_stop(number, reaction)
            crossed = self._cross_order(confirmation, level)
            return [(
                number, reaction, confirmation, level, source, source_time,
                crossed, False,
            )]
        return []


    def _cross_order(
        self, start: datetime, level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        cache_key = (start, level)
        if cache_key in self._cross_order_cache:
            return self._cross_order_cache[cache_key]
        left = bisect_left(self.lower_times, max(start, self.range_start))
        right = bisect_left(self.lower_times, self.range_end)
        position = self._first_cross_position(
            left, right, level, less=self.order_direction != "bearish"
        )
        if position is None:
            self._cross_order_cache[cache_key] = None
            return None
        event = self.lower_times[position]
        index = self._main_index(event)
        result = index, getattr(self.candles[index], "timestamp"), event
        self._cross_order_cache[cache_key] = result
        return result


    def cross_order(
        self, confirmation_time: datetime, stop_level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        """Public audit API for an Order stop crossing."""
        return self._cross_order(confirmation_time, stop_level)


    def _unconsumed_s_orders(
        self, parent: object, parent_stop: datetime
    ) -> list[OrderMatch]:
        """Return the carried A-owned Order whose stop did not decide S."""
        if (
            str(getattr(parent, "color")) != "blue"
            or getattr(parent, "order_confirmation_time", None) is None
            or getattr(parent, "order_stop_level", None) is None
        ):
            return []
        confirmation = getattr(parent, "order_confirmation_time")
        stop_level = as_decimal(getattr(parent, "order_stop_level"))
        crossed = self._cross_order(confirmation, stop_level)
        if crossed is None or crossed[2] < parent_stop:
            return []
        reaction = SimpleNamespace(
            mode=getattr(parent, "order_mode"),
            first_idx=getattr(parent, "order_first_index"),
            break_idx=getattr(parent, "order_break_index"),
            box_top=getattr(parent, "order_box_top"),
            box_top_source_idx=getattr(parent, "order_box_top_source_index"),
            box_bottom=getattr(parent, "order_box_bottom"),
            box_bottom_source_idx=getattr(parent, "order_box_bottom_source_index"),
        )
        return [(
            int(getattr(parent, "order_reaction_number")),
            reaction,
            confirmation,
            stop_level,
            int(getattr(parent, "order_stop_source_index")),
            getattr(parent, "order_stop_source_time"),
            crossed,
            ("carried-live",),
            None,
        )]


    def _initial_order_records(self) -> tuple[tuple[
        datetime, datetime, int, object, Decimal, int, datetime,
        tuple[int, datetime, datetime] | None,
    ], ...]:
        """Materialize immutable initial OrderAudit geometry once per run.

        Algorithm requirement: physical Order identity and exact strict stop
        chronology remain unchanged. Performance detail: the prior code
        recomputed ``_cross_order`` while rescanning this immutable ledger for
        every E parent. The precomputed records only remove repeated pure work.
        """
        cached = self._initial_order_records_cache
        if cached is not None:
            return cached

        records: list[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ]] = []
        for entry in self.initial_order_audit.values():
            reaction = entry["reaction"]
            first = self._reaction_first_time(reaction)
            confirmation = entry["confirmation_time"]
            level = as_decimal(entry["stop_level"])
            crossed = self._cross_order(confirmation, level)
            records.append((
                first, confirmation, int(entry["reaction_number"]), reaction,
                level, int(entry["stop_source_index"]),
                entry["stop_source_time"], crossed,
            ))

        records.sort(key=lambda item: (item[0], item[1], int(getattr(item[3], "first_idx")), int(getattr(item[3], "break_idx"))))
        cached = tuple(records)
        self._initial_order_records_cache = cached
        self._initial_order_first_times = [item[0] for item in cached]

        by_first: dict[datetime, list[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ]]] = {}
        for item in cached:
            by_first.setdefault(item[0], []).append(item)
        self._initial_orders_by_first_time = {
            key: tuple(value) for key, value in by_first.items()
        }

        # A separate confirmation-sorted view supports the post-stop route.
        # The record objects are reused; no duplicate Order representation is
        # constructed.
        confirmation_sorted = sorted(
            cached,
            key=lambda item: (item[1], item[0], int(getattr(item[3], "first_idx")), int(getattr(item[3], "break_idx"))),
        )
        self._initial_order_confirmation_records = tuple(confirmation_sorted)
        self._initial_order_confirmation_times = [item[1] for item in confirmation_sorted]
        return cached


    @staticmethod
    @staticmethod
    def _initial_record_match(
        record: tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ],
        causes: tuple[str, ...],
    ) -> OrderMatch:
        _first, confirmation, number, reaction, level, source_index, source_time, crossed = record
        return (
            number, reaction, confirmation, level, source_index, source_time,
            crossed, causes, None,
        )


    def _initial_order_match(
        self, entry: dict[str, object], causes: tuple[str, ...],
    ) -> OrderMatch:
        """Return one immutable A-owned Order_A audit entry as an OrderMatch."""
        reaction = entry["reaction"]
        confirmation = entry["confirmation_time"]
        level = as_decimal(entry["stop_level"])
        crossed = self._cross_order(confirmation, level)
        return (
            int(entry["reaction_number"]), reaction, confirmation, level,
            int(entry["stop_source_index"]), entry["stop_source_time"],
            crossed, causes, None,
        )


    def _gate_owned_initial_order(
        self, parent_stop: datetime,
    ) -> OrderMatch | None:
        """Keep an A-owned order that starts in the parent-stop candle."""
        gate_time = self.times[self._main_index(parent_stop)]
        self._initial_order_records()
        assert self._initial_orders_by_first_time is not None
        matches: list[OrderMatch] = []
        for record in self._initial_orders_by_first_time.get(gate_time, ()):
            confirmation = record[1]
            if confirmation < parent_stop:
                continue
            crossed = record[7]
            if crossed is None or crossed[2] < parent_stop:
                continue
            matches.append(self._initial_record_match(record, ("carried-live",)))
        return min(
            matches,
            key=lambda item: (item[6][2], self._reaction_first_time(item[1])),
            default=None,
        )


    def _carried_orders_for_parent(
        self, parent: object, parent_stop: datetime,
    ) -> list[OrderMatch]:
        """Return accepted Order identities created and left live in this lifecycle."""
        lifecycle_start = getattr(parent, "decision_event_time", None)
        if lifecycle_start is None:
            return []
        key = lifecycle_start, parent_stop
        cached = self._carried_orders_cache.get(key)
        if cached is not None:
            return list(cached)
        matches: list[OrderMatch] = []
        for entry in self.order_audit.values():
            a_created_events = [
                cause[3]
                for cause in entry.get("causes", set())
                if cause[0] == "parent-stop"
            ]
            created_events = [min(a_created_events)] if a_created_events else []
            created_events.extend(
                cause["physicalOrderConfirmationTime"]
                for cause in entry.get("order_b_causes", ())
            )
            if not created_events:
                continue
            confirmation = entry["confirmation_time"]
            crossed = entry.get("stop_cross")
            if (
                not any(lifecycle_start < created < parent_stop for created in created_events)
                or confirmation > parent_stop
                or crossed is None
                or crossed[2] < parent_stop
            ):
                continue
            reaction = entry["reaction"]
            matches.append((
                int(entry["reaction_number"]), reaction, confirmation,
                as_decimal(entry["stop_level"]), int(entry["stop_source_index"]),
                entry["stop_source_time"], crossed, ("carried-live",), None,
            ))

        records = self._initial_order_records()
        assert self._initial_order_first_times is not None
        left = bisect_left(self._initial_order_first_times, lifecycle_start)
        right = bisect_right(self._initial_order_first_times, parent_stop)
        for record in records[left:right]:
            confirmation = record[1]
            if confirmation > parent_stop:
                continue
            crossed = record[7]
            if crossed is None or crossed[2] < parent_stop:
                continue
            matches.append(self._initial_record_match(record, ("carried-live",)))
        result = sorted(
            matches,
            key=lambda item: (item[6][2], -int(getattr(item[1], "first_idx"))),
        )
        self._carried_orders_cache[key] = tuple(result)
        return result


    def _post_stop_accepted_orders_for_parent(
        self, parent: object, parent_stop: datetime,
    ) -> list[OrderMatch]:
        """Return accepted physical Orders confirmed after this parent stop."""
        del parent
        matches_by_identity: dict[tuple[int, int], OrderMatch] = {}

        def add_match(match: OrderMatch) -> None:
            crossed = match[6]
            if crossed is None or crossed[2] <= parent_stop or crossed[2] <= match[2]:
                return
            if self._has_sequence_reset_between(parent_stop, crossed[2]):
                return
            identity = reaction_identity(match[1])
            current = matches_by_identity.get(identity)
            if current is None or (
                crossed[2], match[2], int(getattr(match[1], "first_idx"))
            ) < (
                current[6][2], current[2], int(getattr(current[1], "first_idx"))
            ):
                matches_by_identity[identity] = match

        self._initial_order_records()
        assert self._initial_order_confirmation_times is not None
        confirmation_records = self._initial_order_confirmation_records
        start = bisect_right(self._initial_order_confirmation_times, parent_stop)
        for record in confirmation_records[start:]:
            add_match(self._initial_record_match(record, ("accepted-live",)))

        audit_position = bisect_right(
            self._order_audit_confirmation_index,
            (parent_stop, 2**63 - 1, 2**63 - 1),
        )
        for _confirmation, first_index, break_index in (
            self._order_audit_confirmation_index[audit_position:]
        ):
            entry = self.order_audit.get((first_index, break_index))
            if entry is None:
                continue
            reaction = entry.get("reaction")
            confirmation = entry.get("confirmation_time")
            if reaction is None or not isinstance(confirmation, datetime):
                continue
            level_value = entry.get("stop_level")
            source_index = entry.get("stop_source_index")
            source_time = entry.get("stop_source_time")
            if level_value is None or source_index is None or source_time is None:
                continue
            crossed = entry.get("stop_cross")
            if not (
                isinstance(crossed, tuple)
                and len(crossed) >= 3
                and isinstance(crossed[2], datetime)
            ):
                crossed = self._cross_order(confirmation, as_decimal(level_value))
            add_match((
                int(entry.get("reaction_number", 0)), reaction, confirmation,
                as_decimal(level_value), int(source_index), source_time, crossed,
                ("accepted-live",), None,
            ))

        return sorted(
            matches_by_identity.values(),
            key=lambda item: (
                item[6][2], item[2], -int(getattr(item[1], "first_idx")),
            ),
        )


    def _blocked_by_gate_owned_order(self, zone: EZone) -> bool:
        """Reject a nested parent-stop Order_A when the gate-owned A Order wins."""
        if "parent-stop" not in zone.order_causes:
            return False
        gate_owned = self._gate_owned_initial_order(zone.parent_stop_event_time)
        return (
            gate_owned is not None
            and gate_owned[2] < zone.order_first_time
        )


    def _rebuild_accepted_order_audit(
        self, numbered: list[EZone], supplemental_s_zones: Sequence[object] = (),
    ) -> list[EZone]:
        """Rebuild accepted parent-stop and reset-leg physical provenance."""
        invalid_s_source_times = {
            source_time
            for source_time, _source_index in getattr(
                self, "invalid_s_root_identities", set()
            )
        }

        def valid_parent_stop_cause(cause: tuple[object, ...]) -> bool:
            if not cause or cause[0] != "parent-stop":
                return False
            # Suppressed/invalid S evidence may remain available internally for
            # E continuation geometry, but it never became an accepted S
            # behavior and therefore cannot create a physical parent-stop
            # Order_A.  Valid historical/non-public accepted S behaviors are
            # unaffected because only explicitly invalid S identities are
            # rejected here.
            return not (
                cause[1] == "S"
                and len(cause) > 4
                and cause[4] in invalid_s_source_times
            )

        prior_order_audit = {
            identity: {
                **entry,
                "causes": {
                    cause for cause in entry.get("causes", set())
                    if valid_parent_stop_cause(cause)
                },
            }
            for identity, entry in self.order_audit.items()
        }
        self._clear_order_audit()
        self.register_order_b_reset_legs(self.order_b_legs)
        accepted_parents: list[tuple[str, object]] = [
            ("S", item) for item in self.s_zones
        ] + [("StopAll" if item.source_time in self.sequence_resets else "E", item)
             for item in numbered]
        for parent_type, parent in accepted_parents:
            stop = self._parent_stop(parent_type, parent)
            if stop is None:
                continue
            self._register_order_audit(parent_type, parent, stop[1])

        # Carried-live and accepted-live are use routes, not creation causes.
        # Preserve the original parent-stop Order_A provenance when final
        # reconciliation keeps a physical Order whose creating parent is no
        # longer a public behavior.
        for zone in numbered:
            identity = order_identity(zone.order_first_index, zone.order_break_index)
            if identity in self.order_audit:
                continue

            prior_entry = prior_order_audit.get(identity)
            reaction = self._opposite_by_first_index.get(zone.order_first_index)
            if (
                reaction is None
                or int(getattr(reaction, "break_idx", -1)) != zone.order_break_index
            ):
                reaction = SimpleNamespace(
                    mode=zone.order_mode,
                    first_idx=zone.order_first_index,
                    break_idx=zone.order_break_index,
                    box_top=zone.order_box_top,
                    box_top_source_idx=zone.order_box_top_source_index,
                    box_top_source_time=zone.order_box_top_source_time,
                    box_bottom=zone.order_box_bottom,
                    box_bottom_source_idx=zone.order_box_bottom_source_index,
                    box_bottom_source_time=zone.order_box_bottom_source_time,
                    behavior_internal=False,
                )

            causes: set[tuple[object, ...]] = set()
            if prior_entry is not None:
                causes.update(
                    cause for cause in prior_entry.get("causes", set())
                    if cause and cause[0] == "parent-stop"
                )

            initial_entry = self.initial_order_audit.get(identity)
            if initial_entry is not None:
                a_causes = initial_entry.get("a_causes") or [(
                    initial_entry.get("a_source_time"),
                    initial_entry.get("a_stop_event_time"),
                )]
                for a_source_time, a_stop_time in a_causes:
                    if a_source_time is None or a_stop_time is None:
                        continue
                    causes.add((
                        "parent-stop", "A", None, a_stop_time, a_source_time
                    ))

            if (
                not causes
                and "carried-live" in zone.order_causes
                and zone.parent_type == "S"
            ):
                parent_s = next((
                    item for item in [*self.s_zones, *supplemental_s_zones]
                    if int(getattr(item, "source_index")) == zone.parent_source_index
                    and getattr(item, "source_time") == zone.parent_source_time
                    and getattr(item, "order_first_index", None) == zone.order_first_index
                    and getattr(item, "order_break_index", None) == zone.order_break_index
                ), None)
                if parent_s is not None:
                    causes.add((
                        "parent-stop",
                        "A",
                        None,
                        getattr(parent_s, "a_stop_event_time"),
                        getattr(parent_s, "a_source_time"),
                    ))

            if zone.order_parent_stop_cause_time is not None:
                parent_label = zone.parent_type
                if zone.parent_type == "E":
                    parent_zone = next((
                        item for item in numbered
                        if item.source_index == zone.parent_source_index
                        and item.source_time == zone.parent_source_time
                    ), None)
                    if parent_zone is not None:
                        parent_label = f"E{parent_zone.number}"
                if zone.parent_source_time in self.sequence_resets:
                    parent_label = f"StopAll{self.sequence_resets[zone.parent_source_time]}"
                causes.add((
                    "parent-stop",
                    parent_label,
                    "" if zone.parent_source_time in self.sequence_resets else zone.family,
                    zone.parent_stop_event_time,
                    zone.parent_source_time,
                ))

            causes = {cause for cause in causes if valid_parent_stop_cause(cause)}
            if not causes:
                continue

            exact_cross = self._cross_order(
                zone.order_confirmation_time, as_decimal(zone.order_stop_level)
            )
            self.order_audit[identity] = {
                "reaction_number": zone.order_reaction_number,
                "reaction": reaction,
                "confirmation_time": zone.order_confirmation_time,
                "stop_level": zone.order_stop_level,
                "stop_source_index": zone.order_stop_source_index,
                "stop_source_time": zone.order_stop_source_time,
                "stop_cross": exact_cross,
                "causes": causes,
            }
            self._index_order_audit_identity(identity, zone.order_confirmation_time)

        # Order_A retention invariant: once a valid parent-stop physical Order
        # has entered the canonical ledger, later lifecycle reconciliation may
        # change who consumes it but must never delete its identity/provenance.
        for identity, prior_entry in prior_order_audit.items():
            prior_causes = {
                cause for cause in prior_entry.get("causes", set())
                if valid_parent_stop_cause(cause)
            }
            if not prior_causes:
                continue
            current = self.order_audit.get(identity)
            if current is not None:
                current_causes = current.setdefault("causes", set())
                assert isinstance(current_causes, set)
                current_causes.update(prior_causes)
                continue
            restored = {**prior_entry, "causes": set(prior_causes)}
            self.order_audit[identity] = restored
            self._index_order_audit_identity(
                identity, restored["confirmation_time"]
            )

        return sorted(
            numbered,
            key=lambda item: (item.source_time, item.source_index),
        )


    def rebuild_accepted_order_audit(
        self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object] = (),
    ) -> list[EZone]:
        """Rebuild the canonical Order ledger after external E reconciliation.

        The pipeline may replace a final E branch with an earlier continuation
        built from consumed S evidence after ``detect()`` has completed.  That
        accepted branch must become authoritative for OrderAudit as well;
        the Order module keeps provenance out of the bridge projection.
        """
        return self._rebuild_accepted_order_audit(
            list(zones), supplemental_s_zones=supplemental_s_zones
        )


    def ensure_accepted_order_audit(
        self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object] = (),
    ) -> list[EZone]:
        """Add audit coverage for externally restored accepted E zones.

        Visibility may restore an independent S-owned E root after StopAll
        reconciliation.  Rebuilding from only that post-StopAll E list would
        incorrectly discard physical Orders still needed by already-created
        StopAll/history, so rebuild the accepted subset and then merge back any
        previously canonical identities that were not superseded.
        """
        preserved = {
            identity: {**entry, "causes": set(entry.get("causes", set()))}
            for identity, entry in self.order_audit.items()
        }
        rebuilt = self._rebuild_accepted_order_audit(
            list(zones), supplemental_s_zones=supplemental_s_zones
        )
        for identity, entry in preserved.items():
            self.order_audit.setdefault(identity, entry)
        self._carried_orders_cache.clear()
        return rebuilt


def prepare_order_audit(
    detector,
    start_index: int,
    end_index: int,
    s_detector=None,
    accepted_a_sources: set[datetime] | None = None,
    required_identities: set[tuple[int, int]] | None = None,
):
    """Resolve final Order_A and Order_B identities before serialization."""
    combined: list[tuple[dict[str, object], list[dict[str, object]]]] = []
    required_identities = set(required_identities or set())

    if s_detector is not None:
        for entry in s_detector.order_audit.values():
            a_causes = entry.get("a_causes") or [(
                entry["a_source_time"], entry["a_stop_event_time"]
            )]
            if accepted_a_sources is not None:
                a_causes = [
                    cause for cause in a_causes
                    if cause[0] in accepted_a_sources
                ]
            if not a_causes:
                continue
            combined.append((entry, [
                {
                    "kind": "parent-stop",
                    "parentType": "A",
                    "parentFamily": None,
                    "eventTime": stop_time,
                    "parentSourceTime": source_time,
                }
                for source_time, stop_time in a_causes
            ]))

    for entry in detector.order_audit.values():
        causes = [
            {
                "kind": "parent-stop",
                "parentType": cause[1],
                "parentFamily": cause[2],
                "eventTime": cause[3],
                "parentSourceTime": cause[4],
            }
            for cause in sorted(entry["causes"], key=str)
            if cause[0] == "parent-stop"
        ]
        causes.extend(entry.get("order_b_causes", ()))
        if causes:
            combined.append((entry, causes))

    merged: dict[tuple[int, int], dict[str, object]] = {}
    output: list[dict[str, object]] = []
    for entry, supplied_causes in combined:
        reaction = entry["reaction"]
        first_index = int(getattr(reaction, "first_idx"))
        identity = order_identity(first_index, getattr(reaction, "break_idx"))
        if (
            not start_index <= first_index <= end_index
            and identity not in required_identities
        ):
            continue
        existing = merged.get(identity)
        if existing is not None:
            existing_causes = existing["causes"]
            existing_causes.extend(
                cause for cause in supplied_causes
                if cause not in existing_causes
            )
            continue
        crossed = entry.get("stop_cross")
        if "stop_cross" not in entry:
            crossed = detector.cross_order(
                entry["confirmation_time"], entry["stop_level"]
            )
        prepared = {
            "entry": entry,
            "reaction": reaction,
            "causes": list(supplied_causes),
            "crossed": crossed,
        }
        merged[identity] = prepared
        output.append(prepared)

    # One exact parent-stop event creates one physical Order_A.
    parent_owner: dict[tuple[object, object, object, object], dict[str, object]] = {}
    parent_rank: dict[tuple[object, object, object, object], tuple[object, int, int]] = {}
    for item in output:
        reaction = item["reaction"]
        rank = (
            item["entry"]["confirmation_time"],
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
        )
        for cause in item["causes"]:
            if cause.get("kind") != "parent-stop":
                continue
            key = (
                cause.get("parentType"),
                cause.get("parentFamily"),
                cause.get("eventTime"),
                cause.get("parentSourceTime"),
            )
            previous = parent_rank.get(key)
            if previous is None or rank < previous:
                parent_rank[key] = rank
                parent_owner[key] = item

    deduped_output: list[dict[str, object]] = []
    for item in output:
        accepted_causes = []
        for cause in item["causes"]:
            if cause.get("kind") != "parent-stop":
                accepted_causes.append(cause)
                continue
            key = (
                cause.get("parentType"),
                cause.get("parentFamily"),
                cause.get("eventTime"),
                cause.get("parentSourceTime"),
            )
            if parent_owner.get(key) is item:
                accepted_causes.append(cause)
        if accepted_causes:
            item["causes"] = accepted_causes
            deduped_output.append(item)
    return deduped_output


def accepted_audit_entry(
    entry: dict[str, object], accepted_sources: set
) -> dict[str, object] | None:
    """Return an E-facing A audit entry for one accepted A provenance.

    A physical order may be opened by more than one stopped A.  E still
    consumes one identity-keyed entry, so select the first accepted cause
    while retaining the complete cause list for presentation serialization.
    """
    causes = entry.get("a_causes") or [
        (entry["a_source_time"], entry["a_stop_event_time"])
    ]
    selected = next(
        ((source_time, stop_time) for source_time, stop_time in causes
         if source_time in accepted_sources),
        None,
    )
    if selected is None:
        return None
    if (
        selected[0] == entry.get("a_source_time")
        and selected[1] == entry.get("a_stop_event_time")
    ):
        return entry
    adjusted = dict(entry)
    adjusted["a_source_time"] = selected[0]
    adjusted["a_stop_event_time"] = selected[1]
    return adjusted


def order_identity_is_internal(item, internal_identities):
    """Return whether a behavior's physical Order Reaction is internal."""
    first_index = getattr(item, "order_first_index", None)
    break_index = getattr(item, "order_break_index", None)
    if first_index is None or break_index is None:
        return False
    return order_identity(first_index, break_index) in internal_identities


class SOrderAuditMixin:
    """Physical Order_A and shared Order stop operations for S."""

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
        """Record the independent physical Order created by one stopped A."""
        a_price = as_decimal(getattr(zone, "price"))
        a_stop = self._first_a_stop(a_price, self._a_confirmation_time(zone))
        if a_stop is None:
            return
        _, _, a_stop_event_time = a_stop
        order_match = self._first_order_after(a_stop_event_time)
        if order_match is None:
            return
        self._record_a_order_audit(zone, a_stop_event_time, order_match)


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


    def _order_stop_crossed(self, candle: object, level: Decimal) -> bool:
        if self.order_direction == "bearish":
            return as_decimal(getattr(candle, "high")) > level
        return as_decimal(getattr(candle, "low")) < level


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

