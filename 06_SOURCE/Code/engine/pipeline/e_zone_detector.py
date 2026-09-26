"""Recursive E-zone and Order calculation from authoritative S/Reaction state.

Owns parent-stop, carried-live, accepted-live, and Reset-leg Order discovery;
recursive E chains; accepted Order causes; and E family/number reconciliation.
Cross-stage public visibility and StopAll grouping are delegated to the lifecycle
engine.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from decimal import Decimal
from types import SimpleNamespace
from typing import Callable, Sequence

from core_utils import as_decimal, order_identity, reaction_identity
from direction_policy import policy_for


E_ZONE_VERSION = "6.14.2"
E_ZONE_LAST_MODIFIED = "2026-09-24 04:30:00 +03:30"


@dataclass(frozen=True, slots=True)
class EZone:
    direction: str
    family: str
    number: int
    parent_type: str
    parent_source_index: int
    parent_source_time: datetime
    parent_price: Decimal
    parent_stop_index: int
    parent_stop_time: datetime
    parent_stop_event_time: datetime
    order_direction: str
    order_reaction_number: int
    order_mode: str
    order_causes: tuple[str, ...]
    order_parent_stop_cause_time: datetime | None
    order_reset_leg_reset_time: datetime | None
    order_reset_leg_break_time: datetime | None
    order_first_index: int
    order_first_time: datetime
    order_break_index: int
    order_break_time: datetime
    order_confirmation_time: datetime
    order_box_top: Decimal
    order_box_top_source_index: int
    order_box_top_source_time: datetime
    order_box_bottom: Decimal
    order_box_bottom_source_index: int
    order_box_bottom_source_time: datetime
    order_stop_level: Decimal
    order_stop_source_index: int
    order_stop_source_time: datetime
    source_index: int
    source_time: datetime
    price: Decimal
    decision_index: int
    decision_time: datetime
    decision_event_time: datetime


OrderMatch = tuple[
    int, object, datetime, Decimal, int, datetime,
    tuple[int, datetime, datetime] | None, tuple[str, ...],
    datetime | None, datetime | None, datetime | None,
]


@dataclass(frozen=True, slots=True)
class OrderBFormation:
    """One complete reset-leg Order_B setup under the canonical mirror rule."""

    reset_time: datetime
    reset_index: int
    owner_first_index: int
    owner_break_index: int
    trigger_level: Decimal
    trigger_source_index: int
    trigger_source_time: datetime
    strict_break_index: int
    strict_break_time: datetime
    strict_break_event_time: datetime
    opposite_extreme: Decimal
    opposite_extreme_source_index: int
    opposite_extreme_source_time: datetime
    evidence_first_index: int
    evidence_break_index: int
    order_reaction_number: int
    order_reaction: object
    order_confirmation_time: datetime


@dataclass(frozen=True, slots=True)
class OrderCFormation:
    """Blue-qualified leg from Reset through next aligned Reaction breakout."""

    reset_time: datetime
    next_breakout_time: datetime | None
    leg_start_breakout_time: datetime
    previous_breakout_time: datetime
    leg_level: Decimal
    level_source_index: int
    level_source_time: datetime
    blue_source_time: datetime
    blue_formation_event_time: datetime
    strict_break_event_time: datetime
    strict_break_index: int
    order_reaction_number: int
    order_reaction: object
    order_confirmation_time: datetime


class EZoneDetector:
    def __init__(
        self,
        direction: str,
        trend_reactions: Sequence[object],
        opposite_reactions: Sequence[object],
        s_zones: Sequence[object],
        trend_resets: Sequence[object],
        opposite_resets: Sequence[object],
        chronology: object,
        start_index: int = 0,
        end_index: int | None = None,
        geometry_finder: Callable[[str, int, int], object | None] | None = None,
        direct_geometry_finder: Callable[
            [str, int, int, datetime], object | None
        ] | None = None,
        blocked_order_first_times: set[datetime] | None = None,
        initial_order_audit: dict[tuple[int, int], dict[str, object]] | None = None,
        sequence_resets: dict[datetime, int] | None = None,
        sequence_priority: Callable[[str, str], int] | None = None,
        invalid_s_root_identities: set[tuple[datetime, int]] | None = None,
        trend_blue_lines: Sequence[object] = (),
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.policy = policy_for(direction)
        if sequence_priority is None:
            raise ValueError("EZoneDetector requires the shared sequence-priority resolver.")
        self.sequence_priority = sequence_priority
        self.invalid_s_root_identities = set(invalid_s_root_identities or set())
        self.sequence_resets = dict(sequence_resets or {})
        self._sequence_reset_times = sorted(self.sequence_resets)
        self.order_direction = chronology.opposite_direction(direction)
        self.chronology = chronology
        self.trend_reactions = list(trend_reactions)
        self.opposite_reactions = list(opposite_reactions)
        self.s_zones = sorted(
            s_zones,
            key=lambda item: (
                getattr(item, "source_time"),
                int(getattr(item, "source_index")),
            ),
        )
        red_s_events = [
            (getattr(item, "source_time"), getattr(item, "decision_event_time"))
            for item in self.s_zones
            if str(getattr(item, "color")) == "red"
        ]
        self._red_s_source_times = [item[0] for item in red_s_events]
        self._red_s_suffix_min_decision: list[datetime] = []
        suffix_min: datetime | None = None
        for _, decision_time in reversed(red_s_events):
            if suffix_min is None or decision_time < suffix_min:
                suffix_min = decision_time
            self._red_s_suffix_min_decision.append(suffix_min)
        self._red_s_suffix_min_decision.reverse()
        self.trend_blue_lines = sorted(
            (item for item in trend_blue_lines
             if bool(getattr(item, "calculation_valid", True))
             and not bool(getattr(item, "behavior_internal", False))),
            key=lambda item: getattr(item, "source_time"),
        )
        # Blue source geometry and the event that makes it a valid Blue are
        # different timestamps (especially for Scale strikes inside a Reaction).
        self._blue_formation_cache: list[tuple[datetime, object]] | None = None
        self._blue_formation_times: list[datetime] | None = None
        self._trend_ordinal_by_first_index = {
            int(getattr(item, "first_idx")): position
            for position, item in enumerate(self.trend_reactions, 1)
        }
        self._order_c_formations_cache: list[OrderCFormation] | None = None
        self._order_c_by_identity: dict[tuple[int, int], OrderCFormation] = {}
        self.trend_resets = sorted(trend_resets, key=self._reset_time)
        self.opposite_resets = sorted(opposite_resets, key=self._reset_time)
        self._trend_reset_event_by_identity: dict[tuple[int, int], datetime] = {}
        for reset in self.trend_resets:
            self._trend_reset_event_by_identity.setdefault(
                (int(getattr(reset, "index")), int(getattr(reset, "from_first_idx"))),
                self._reset_time(reset),
            )
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index
        self.timeframe = chronology.timeframe
        self.times = chronology.times
        self.start_index = int(start_index)
        self.end_index = len(self.candles) - 1 if end_index is None else int(end_index)
        self.range_start = self.times[self.start_index]
        self.range_end = self.times[self.end_index] + self.timeframe
        self.geometry_finder = geometry_finder
        self.direct_geometry_finder = direct_geometry_finder or geometry_finder
        self.blocked_order_first_times = blocked_order_first_times or set()
        self.initial_order_audit = initial_order_audit or {}
        self._cross_order_cache: dict[
            tuple[datetime, Decimal], tuple[int, datetime, datetime] | None
        ] = {}
        # Performance implementation detail: canonical opposite Reactions are
        # immutable for one run, and their canonical Order stop depends only
        # on that canonical reaction number/geometry plus immutable chronology.
        # Cache only exact canonical objects; bounded/noncanonical Order_A
        # geometry intentionally stays on the authoritative uncached path.
        self._canonical_order_stop_cache: dict[
            int, tuple[Decimal, int, datetime]
        ] = {}
        # Performance implementation detail: the initial A-owned OrderAudit
        # ledger is immutable for one detector run. Materialize its expensive
        # strict-stop lookup once, then keep both chronological indexes and
        # the original physical identity semantics.
        self._initial_order_records_cache: tuple[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ], ...] | None = None
        self._initial_order_first_times: list[datetime] | None = None
        self._initial_order_confirmation_times: list[datetime] | None = None
        self._initial_order_confirmation_records: tuple[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ], ...] = ()
        self._initial_orders_by_first_time: dict[datetime, tuple[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ], ...]] | None = None
        self._order_b_formations_cache: list[OrderBFormation] | None = None
        self._order_b_confirmation_times: list[datetime] | None = None
        self._order_b_by_identity: dict[
            tuple[int, int], tuple[OrderBFormation, ...]
        ] | None = None
        self._order_b_candidate_records: tuple[
            tuple[datetime, int, int, OrderMatch], ...
        ] | None = None
        self._order_b_candidate_confirmation_times: list[datetime] | None = None
        self._order_candidates_cache: dict[
            tuple[datetime, datetime | None, bool, bool, bool], tuple[OrderMatch, ...]
        ] = {}
        self.order_audit: dict[tuple[int, int], dict[str, object]] = {}
        # Performance implementation detail: ``order_audit`` remains the
        # authoritative accepted ledger and preserves insertion/provenance
        # semantics. This secondary chronology index exists only to avoid a
        # full ledger scan when a parent can use only Orders confirmed after
        # its strict stop.
        self._order_audit_confirmation_index: list[
            tuple[datetime, int, int]
        ] = []
        self._trend_first_times = [
            self._reaction_first_time(item) for item in self.trend_reactions
        ]
        self._trend_confirmations = [
            self._confirmation_for(item, self.direction)
            for item in self.trend_reactions
        ]
        self._opposite_first_times = [
            self._reaction_first_time(item) for item in self.opposite_reactions
        ]
        self._opposite_confirmations = [
            self._confirmation(item) for item in self.opposite_reactions
        ]
        self._trend_by_confirmation = sorted(
            zip(
                self._trend_confirmations,
                self._trend_first_times,
                self.trend_reactions,
            ),
            key=lambda item: item[0],
        )
        self._trend_confirmation_times = [item[0] for item in self._trend_by_confirmation]
        self._trend_by_first_index = {
            int(getattr(item, "first_idx")): item
            for item in self.trend_reactions
        }
        self._trend_reset_events = [
            (self._reset_time(item), item) for item in self.trend_resets
        ]
        self._trend_reset_times = [item[0] for item in self._trend_reset_events]
        self._opposite_reset_times_by_first: dict[int, list[datetime]] = {}
        for reset in self.opposite_resets:
            self._opposite_reset_times_by_first.setdefault(
                int(getattr(reset, "from_first_idx")), []
            ).append(self._reset_time(reset))
        self._opposite_by_first_index = {
            int(getattr(item, "first_idx")): item
            for item in self.opposite_reactions
        }
        # Performance implementation detail: retain the first canonical
        # position for each physical identity. Legacy linear searches used
        # ``next(...)``, so first-win semantics are preserved intentionally.
        self._opposite_identity_position: dict[tuple[int, int], int] = {}
        for position, item in enumerate(self.opposite_reactions):
            self._opposite_identity_position.setdefault(
                reaction_identity(item), position
            )
        self.visual_lifecycle_starts: set[datetime] = set()
        # Historical-only E objects that were fully formed but suppressed by
        # a descendant conflict.  They are exposed for presentation only and
        # never participate in lifecycle ownership, StopAll, numbering, or
        # OrderAudit reconstruction.
        self.historical_rescued_zones: list[EZone] = []
        self._consumed_s_evidence: list[tuple[object, tuple[int, datetime]]] = []
        self._last_candidate_zones: list[EZone] = []

    def _reset_time(self, reset: object) -> datetime:
        return self.chronology.reset_time(reset)

    def _main_index(self, value: datetime) -> int:
        return self.chronology.main_index(value, clamp=True)


    def _first_cross_position(
        self, left: int, right: int, level: Decimal, *, less: bool
    ) -> int | None:
        """Return the first strict lower-timeframe crossing in [left, right)."""
        if self.lower_index is not None:
            return (
                self.lower_index.first_less(left, right, level)
                if less
                else self.lower_index.first_greater(left, right, level)
            )
        field = "low" if less else "high"
        for position in range(left, right):
            value = as_decimal(getattr(self.lower[position], field))
            if value < level if less else value > level:
                return position
        return None

    def _stop_value(self, item: object) -> Decimal:
        return as_decimal(getattr(item, self.policy.extreme_attr))


    def _first_parent_stop(
        self, source_time: datetime, level: Decimal
    ) -> tuple[int, datetime] | None:
        left = bisect_left(self.lower_times, max(source_time, self.range_start))
        right = bisect_left(self.lower_times, self.range_end)
        position = self._first_cross_position(
            left, right, level, less=self.direction == "bullish"
        )
        if position is None:
            return None
        event = self.lower_times[position]
        return self._main_index(event), event

    def _confirmation_for(self, reaction: object, direction: str) -> datetime:
        return self.chronology.reaction_confirmation(direction, reaction)

    def _confirmation(self, reaction: object) -> datetime:
        return self._confirmation_for(reaction, self.order_direction)

    def _reaction_first_time(self, reaction: object) -> datetime:
        return getattr(self.candles[int(getattr(reaction, "first_idx"))], "timestamp")

    def _main_range_extreme(
        self,
        start_index: int,
        end_index: int,
        attribute: str,
        *,
        choose_minimum: bool,
    ) -> tuple[Decimal, int, datetime]:
        """Return the first candle owning the requested closed-range extreme."""
        if end_index < start_index:
            raise ValueError("Order_B extreme range ends before it starts.")
        source = self.candles[start_index]
        value = as_decimal(getattr(source, attribute))
        for candle in self.candles[start_index + 1 : end_index + 1]:
            candidate = as_decimal(getattr(candle, attribute))
            better = candidate < value if choose_minimum else candidate > value
            if better:
                source = candle
                value = candidate
        return value, int(getattr(source, "index")), getattr(source, "timestamp")

    def _order_b_reset_leg(
        self, reset: object, reset_time: datetime,
    ) -> tuple[object, Decimal, int, datetime] | None:
        """Return the same-direction Reset owner and its trigger extreme.

        Bearish: from the owner's Breakout candle through the Reset candle,
        inclusive, the minimum Low is the reset-leg floor.
        Bullish: exact mirror, maximum High is the reset-leg ceiling.
        """
        owner = self._trend_by_first_index.get(
            int(getattr(reset, "from_first_idx"))
        )
        if owner is None:
            return None
        break_index = int(getattr(owner, "break_idx"))
        reset_index = int(getattr(reset, "index"))
        if reset_index < break_index:
            return None
        if self.direction == "bearish":
            level, source_index, source_time = self._main_range_extreme(
                break_index, reset_index, "low", choose_minimum=True
            )
        else:
            level, source_index, source_time = self._main_range_extreme(
                break_index, reset_index, "high", choose_minimum=False
            )
        return owner, level, source_index, source_time

    def _order_b_strict_break(
        self, reset_time: datetime, level: Decimal,
    ) -> tuple[int, datetime, datetime] | None:
        """Return the first exact strict break of the reset-leg trigger level.

        Bearish Order_B: Low < reset-leg floor.
        Bullish Order_B: High > reset-leg ceiling.
        """
        left = bisect_left(self.lower_times, max(reset_time, self.range_start))
        right = bisect_left(self.lower_times, self.range_end)
        position = self._first_cross_position(
            left,
            right,
            level,
            less=self.direction == "bearish",
        )
        if position is None:
            return None
        event_time = self.lower_times[position]
        index = self._main_index(event_time)
        return index, self.times[index], event_time

    def _order_b_opposite_extreme(
        self, trigger_source_index: int, strict_break_index: int,
    ) -> tuple[Decimal, int, datetime]:
        """Return the other reset-leg edge on the closed trigger->break range."""
        if self.direction == "bearish":
            return self._main_range_extreme(
                trigger_source_index,
                strict_break_index,
                "high",
                choose_minimum=False,
            )
        return self._main_range_extreme(
            trigger_source_index,
            strict_break_index,
            "low",
            choose_minimum=True,
        )

    def _order_b_geometry_evidence(
        self, trigger_source_index: int, strict_break_index: int,
    ) -> object | None:
        """Return raw opposite Reaction geometry inside the closed leg range.

        Reset validity, lifecycle acceptance, public visibility, and Internal
        status are deliberately ignored for this evidence test.  Geometry
        alone is sufficient, exactly as required by the Order_B contract.
        """
        if self.geometry_finder is None:
            return None
        geometry = self.geometry_finder(
            self.order_direction,
            trigger_source_index,
            strict_break_index,
        )
        if geometry is None:
            return None
        if int(getattr(geometry, "first_idx")) < trigger_source_index:
            return None
        if int(getattr(geometry, "break_idx")) > strict_break_index:
            return None
        return geometry

    def _first_order_b_reaction_after_break(
        self, strict_break_index: int, strict_break_event: datetime,
    ) -> tuple[int, object, datetime] | None:
        """Return the first canonical opposite Reaction after the Order_B gate."""
        gate_time = self.times[strict_break_index]
        position = bisect_left(self._opposite_first_times, gate_time)
        for order_position in range(position, len(self.opposite_reactions)):
            reaction = self.opposite_reactions[order_position]
            first_time = self._opposite_first_times[order_position]
            confirmation = self._opposite_confirmations[order_position]
            if first_time < gate_time:
                continue
            if confirmation <= strict_break_event:
                continue
            return order_position + 1, reaction, confirmation
        return None

    def _build_order_b_formations(self) -> list[OrderBFormation]:
        """Build every Order_B from same-direction Reset-leg geometry.

        Bearish mirror:
          Bearish Reaction Reset -> minimum Low from Breakout..Reset -> first
          strict Low below that floor -> require at least one raw Bullish
          Reaction geometry from the floor candle through the strict-break
          candle, inclusive -> first canonical Bullish Reaction after the gate.

        Bullish is the exact directional mirror using maximum High, strict
        High above it, raw Bearish geometry, and the first canonical Bearish
        Reaction after the gate.
        """
        if self._order_b_formations_cache is not None:
            return self._order_b_formations_cache
        formations: list[OrderBFormation] = []
        for reset_time, reset in self._trend_reset_events:
            leg = self._order_b_reset_leg(reset, reset_time)
            if leg is None:
                continue
            owner, trigger_level, trigger_source_index, trigger_source_time = leg
            strict_break = self._order_b_strict_break(reset_time, trigger_level)
            if strict_break is None:
                continue
            strict_break_index, strict_break_time, strict_break_event = strict_break
            if strict_break_index < trigger_source_index:
                continue
            evidence = self._order_b_geometry_evidence(
                trigger_source_index, strict_break_index
            )
            if evidence is None:
                continue
            order_match = self._first_order_b_reaction_after_break(
                strict_break_index, strict_break_event
            )
            if order_match is None:
                continue
            order_number, order_reaction, order_confirmation = order_match
            opposite_extreme, opposite_source_index, opposite_source_time = (
                self._order_b_opposite_extreme(
                    trigger_source_index, strict_break_index
                )
            )
            formations.append(OrderBFormation(
                reset_time=reset_time,
                reset_index=int(getattr(reset, "index")),
                owner_first_index=int(getattr(owner, "first_idx")),
                owner_break_index=int(getattr(owner, "break_idx")),
                trigger_level=trigger_level,
                trigger_source_index=trigger_source_index,
                trigger_source_time=trigger_source_time,
                strict_break_index=strict_break_index,
                strict_break_time=strict_break_time,
                strict_break_event_time=strict_break_event,
                opposite_extreme=opposite_extreme,
                opposite_extreme_source_index=opposite_source_index,
                opposite_extreme_source_time=opposite_source_time,
                evidence_first_index=int(getattr(evidence, "first_idx")),
                evidence_break_index=int(getattr(evidence, "break_idx")),
                order_reaction_number=order_number,
                order_reaction=order_reaction,
                order_confirmation_time=order_confirmation,
            ))
        formations.sort(key=lambda item: (
            item.order_confirmation_time,
            int(getattr(item.order_reaction, "first_idx")),
            int(getattr(item.order_reaction, "break_idx")),
            item.reset_time,
        ))
        self._order_b_formations_cache = formations
        self._order_b_confirmation_times = [
            item.order_confirmation_time for item in formations
        ]
        by_identity: dict[tuple[int, int], list[OrderBFormation]] = {}
        for item in formations:
            by_identity.setdefault(
                reaction_identity(item.order_reaction), []
            ).append(item)
        self._order_b_by_identity = {
            identity: tuple(items) for identity, items in by_identity.items()
        }

        # Algorithm requirement: several valid Reset-leg origins may map to
        # one physical Order, and the latest valid Reset-leg cause is
        # authoritative. Every origin for one physical canonical Order shares
        # the same reaction number and confirmation time, so collapse that
        # already-established final winner once instead of re-merging duplicate
        # formations inside every parent query.
        latest_by_identity = {
            identity: items[-1]
            for identity, items in self._order_b_by_identity.items()
        }
        candidate_records: list[tuple[datetime, int, int, OrderMatch]] = []
        for identity, item in latest_by_identity.items():
            level, source, source_time = self._order_stop(
                item.order_reaction_number, item.order_reaction
            )
            crossed = self._cross_order(item.order_confirmation_time, level)
            match: OrderMatch = (
                item.order_reaction_number,
                item.order_reaction,
                item.order_confirmation_time,
                level,
                source,
                source_time,
                crossed,
                ("reset-leg",),
                None,
                item.reset_time,
                item.strict_break_event_time,
            )
            candidate_records.append((
                item.order_confirmation_time, identity[0], identity[1], match
            ))
        candidate_records.sort(key=lambda value: value[:3])
        self._order_b_candidate_records = tuple(candidate_records)
        self._order_b_candidate_confirmation_times = [
            item[0] for item in candidate_records
        ]
        return formations

    def _order_b_orders(
        self, start: datetime,
    ) -> list[tuple[int, object, datetime, datetime, datetime]]:
        """Return canonical Order_B Orders whose Reaction forms at/after start."""
        formations = self._build_order_b_formations()
        confirmation_times = self._order_b_confirmation_times or []
        position = bisect_left(confirmation_times, start)
        return [
            (
                item.order_reaction_number,
                item.order_reaction,
                item.order_confirmation_time,
                item.reset_time,
                item.strict_break_event_time,
            )
            for item in formations[position:]
        ]

    def _order_b_candidate_matches(
        self, start: datetime,
    ) -> tuple[tuple[datetime, int, int, OrderMatch], ...]:
        """Return one final Reset-leg candidate per physical Order after start."""
        self._build_order_b_formations()
        records = self._order_b_candidate_records or ()
        times = self._order_b_candidate_confirmation_times or []
        position = bisect_left(times, start)
        return records[position:]

    def _blue_formation_events(self) -> list[tuple[datetime, object]]:
        """Resolve exact Blue formation chronology; never confuse source with event."""
        if self._blue_formation_cache is not None:
            return self._blue_formation_cache
        events: list[tuple[datetime, object]] = []
        for blue in self.trend_blue_lines:
            ordinal = int(getattr(blue, "reaction_number", 0))
            if not 1 <= ordinal <= len(self.trend_reactions):
                continue
            reaction = self.trend_reactions[ordinal - 1]
            if str(getattr(blue, "kind", "")).lower() == "scale":
                formation = self._confirmation_for(
                    reaction, self.direction
                )
            else:
                formation = self._trend_reset_event_by_identity.get((
                    int(getattr(blue, "source_index")),
                    int(getattr(reaction, "first_idx")),
                ))
                if formation is None:
                    continue
            events.append((formation, blue))
        self._blue_formation_cache = sorted(events, key=lambda item: item[0])
        self._blue_formation_times = [item[0] for item in self._blue_formation_cache]
        return self._blue_formation_cache

    def _order_c_leg(self, reset: object) -> tuple[Decimal, int, datetime, datetime, datetime] | None:
        """Use the owner's Mode-A leg, or the latest earlier Mode-A for Normal.

        The range includes both the previous Reaction Breakout and selected
        Leg-Start Breakout main candles. No post-Reset price changes its level.
        """
        ordinal = self._trend_ordinal_by_first_index.get(
            int(getattr(reset, "from_first_idx"))
        )
        if ordinal is None:
            return None
        owner_index = ordinal - 1
        if str(getattr(self.trend_reactions[owner_index], "mode")) == "A":
            leg_index = owner_index
        else:
            leg_index = next(
                (i for i in range(owner_index - 1, -1, -1)
                 if str(getattr(self.trend_reactions[i], "mode")) == "A"),
                None,
            )
        if leg_index is None or leg_index == 0:
            return None
        preceding = self.trend_reactions[leg_index - 1]
        leg_start = self.trend_reactions[leg_index]
        first_break = int(getattr(preceding, "break_idx"))
        last_break = int(getattr(leg_start, "break_idx"))
        if last_break < first_break or last_break >= len(self.candles):
            return None
        level, source_index, source_time = self._main_range_extreme(
            first_break, last_break,
            "high" if self.direction == "bearish" else "low",
            choose_minimum=self.direction == "bullish",
        )
        return (level, source_index, source_time,
                self.times[first_break], self.times[last_break])

    def _first_order_c_reaction_after_break(
        self, strict_break_event: datetime,
    ) -> tuple[int, object, datetime] | None:
        """First may open within the crossing candle; Confirmation must follow.

        An opposite Reaction beginning in an earlier main candle is ineligible.
        The exact lower-TF crossing event is authoritative for Confirmation.
        """
        crossing_candle_time = self.times[self._main_index(strict_break_event)]
        position = bisect_left(self._opposite_first_times, crossing_candle_time)
        for index in range(position, len(self.opposite_reactions)):
            reaction = self.opposite_reactions[index]
            confirmation = self._opposite_confirmations[index]
            if confirmation > strict_break_event:
                return index + 1, reaction, confirmation
        return None

    def _build_order_c_formations(self) -> list[OrderCFormation]:
        """Independently prove Blue-qualified Order_C using the selected Leg Start.

        The owner itself is the Leg Start if native Mode A, otherwise use the
        latest earlier Mode A. Bearish uses High/max/> and Bullish Low/min/<.
        After post-Reset Blue and exact strict crossing, choose the first
        opposite Reaction beginning in that main candle or later, confirmed
        strictly after the exact crossing.
        """
        if self._order_c_formations_cache is not None:
            return self._order_c_formations_cache
        formations: list[OrderCFormation] = []
        blue_events = self._blue_formation_events()
        blue_times = self._blue_formation_times or []
        for reset_time, reset in self._trend_reset_events:
            leg = self._order_c_leg(reset)
            if leg is None:
                continue
            level, source_index, source_time, previous_break, leg_break = leg
            owner_ordinal = self._trend_ordinal_by_first_index.get(
                int(getattr(reset, "from_first_idx"))
            )
            if owner_ordinal is None:
                continue
            # A Reset Blue created by this same exact Reset event is eligible.
            # Blue must exist before the strict break; its source candle alone
            # is not proof that a Scale Blue has formed.
            blue_evidence = None
            for blue_position in range(bisect_left(blue_times, reset_time), len(blue_events)):
                event, blue = blue_events[blue_position]
                if int(getattr(blue, "reaction_number")) >= owner_ordinal:
                    blue_evidence = (event, blue)
                    break
            if blue_evidence is None:
                continue
            blue_event, blue = blue_evidence
            # Leg geometry is frozen no later than its completed Breakout
            # candle; no partial-candle lookahead is permitted.
            freeze_time = leg_break + self.timeframe
            scan_start = max(reset_time, blue_event + timedelta(microseconds=1),
                             freeze_time, self.range_start)
            left = bisect_left(self.lower_times, scan_start)
            right = bisect_left(self.lower_times, self.range_end)
            position = self._first_cross_position(
                left, right, level, less=self.direction == "bullish"
            )
            if position is None:
                continue
            strict_event = self.lower_times[position]
            gate_index = self._main_index(strict_event)
            order = self._first_order_c_reaction_after_break(strict_event)
            if order is None:
                continue
            number, reaction, confirmation = order
            if self._has_sequence_reset_between(reset_time, confirmation):
                continue
            # Legacy nextBreakoutTime is retained strictly as optional audit
            # metadata. No next trend Reaction is required for the new gate.
            next_breakout = None
            search_position = bisect_right(self._trend_confirmation_times, reset_time)
            reset_index = int(getattr(reset, "index"))
            for next_confirmation, first_time, candidate in self._trend_by_confirmation[search_position:]:
                if next_confirmation > confirmation:
                    break
                if int(getattr(candidate, "first_idx")) == int(getattr(reset, "from_first_idx")):
                    continue
                if first_time < self.times[reset_index]:
                    continue
                if int(getattr(candidate, "break_idx")) < reset_index:
                    continue
                next_breakout = self.times[int(getattr(candidate, "break_idx"))]
                break
            formations.append(OrderCFormation(
                reset_time=reset_time,
                next_breakout_time=next_breakout,
                leg_start_breakout_time=leg_break,
                previous_breakout_time=previous_break,
                leg_level=level, level_source_index=source_index,
                level_source_time=source_time,
                blue_source_time=blue.source_time,
                blue_formation_event_time=blue_event,
                strict_break_event_time=strict_event,
                strict_break_index=gate_index,
                order_reaction_number=number,
                order_reaction=reaction,
                order_confirmation_time=confirmation,
            ))
        formations.sort(key=lambda x: (
            x.order_confirmation_time,
            int(getattr(x.order_reaction, "first_idx")),
            int(getattr(x.order_reaction, "break_idx")),
            x.reset_time,
        ))
        for formation in formations:
            identity = reaction_identity(formation.order_reaction)
            old = self._order_c_by_identity.get(identity)
            if old is None or (
                formation.reset_time, formation.strict_break_event_time
            ) > (old.reset_time, old.strict_break_event_time):
                self._order_c_by_identity[identity] = formation
        self._order_c_formations_cache = formations
        return formations

    def _order_c_candidates(self, start: datetime) -> list[OrderMatch]:
        """Physical Order_C is independently created; do not relabel as Order_A/B."""
        self._build_order_c_formations()
        matches: list[OrderMatch] = []
        for item in self._order_c_by_identity.values():
            if item.order_confirmation_time < start:
                continue
            level, source, source_time = self._order_stop(
                item.order_reaction_number, item.order_reaction
            )
            matches.append((
                item.order_reaction_number, item.order_reaction,
                item.order_confirmation_time, level, source, source_time,
                self._cross_order(item.order_confirmation_time, level),
                ("blue-leg",), None, None, None,
            ))
        return matches

    def _order_b_evidence(
        self, reaction: object, context_start: datetime,
    ) -> tuple[datetime, datetime] | None:
        """Return the latest eligible Order_B cause for one physical Reaction."""
        identity = reaction_identity(reaction)
        self._build_order_b_formations()
        by_identity = self._order_b_by_identity or {}
        evidence = [
            item for item in by_identity.get(identity, ())
            if item.order_confirmation_time >= context_start
        ]
        if not evidence:
            return None
        owner = max(
            evidence,
            key=lambda item: (
                item.reset_time,
                item.strict_break_event_time,
            ),
        )
        return owner.reset_time, owner.strict_break_event_time

    def _replacement_order(
        self,
        owner: object,
        owner_confirmation: datetime,
        owner_stop_event: datetime,
    ) -> tuple[int, object, datetime, datetime] | None:
        """Return the first later Order_B that forms before the owner stops."""
        owner_identity = reaction_identity(owner)
        formations = self._build_order_b_formations()
        confirmation_times = self._order_b_confirmation_times or []
        position = bisect_right(confirmation_times, owner_confirmation)
        for item in formations[position:]:
            if item.order_confirmation_time >= owner_stop_event:
                break
            if reaction_identity(item.order_reaction) == owner_identity:
                continue
            return (
                item.order_reaction_number,
                item.order_reaction,
                item.order_confirmation_time,
                item.reset_time,
            )
        return None


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
                # Only the S->E parent-stop path may admit a noncanonical
                # bounded Reaction, and only when exact gate chronology proves
                # continuation of the already-open post-Reset leg.
                if (
                    allow_bounded_continue
                    and getattr(candidate, "order_gate_decision", None) == "continue"
                ):
                    return 0, candidate, confirmation
                search_index = int(getattr(candidate, "first_idx")) + 1
                search_event = first
                continue
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
        parent-stop Order_A provenance and is independent of Order_B.
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
            return 0, candidate, candidate_confirmation
        return None

    def _direct_parent_stop_order(
        self,
        start: datetime,
        continuous_deadline: datetime | None,
        allow_bounded_continue: bool,
    ) -> tuple[int, object, datetime] | None:
        """Select the direct parent-stop Order without Order_B evidence."""
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
            allow_bounded_continue
            and geometric_direct is not None
            and geometric_direct[0] == 0
            and geometric_gate_decision == "continue"
            and (
                independent is None
                or self._reaction_first_time(geometric_direct[1])
                < self._reaction_first_time(independent[1])
            )
        ):
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
        cause: str,
        *,
        parent_stop_cause_time: datetime | None = None,
        reset_time: datetime | None = None,
        reset_break: datetime | None = None,
    ) -> OrderMatch:
        """Merge one provenance cause into a single physical Order identity."""
        level, source, source_time = self._order_stop(number, reaction)
        crossed = self._cross_order(confirmation, level)
        key = reaction_identity(reaction)
        existing = by_geometry.get(key)
        existing_causes = existing[7] if existing is not None else ()
        causes = tuple(dict.fromkeys((*existing_causes, cause)))
        if cause == "parent-stop":
            parent_cause = parent_stop_cause_time
            reset_cause_time = existing[9] if existing is not None else None
            reset_cause_break = existing[10] if existing is not None else None
        else:
            parent_cause = existing[8] if existing is not None else None
            reset_cause_time = reset_time
            reset_cause_break = reset_break
        match: OrderMatch = (
            number,
            reaction,
            confirmation,
            level,
            source,
            source_time,
            crossed,
            causes,
            parent_cause,
            reset_cause_time,
            reset_cause_break,
        )
        by_geometry[key] = match
        return match

    def _enforce_single_parent_stop_owner(
        self, by_geometry: dict[tuple[int, int], OrderMatch]
    ) -> None:
        """Keep one physical Order owner for the exact parent-stop cause.

        A single parent stop may open only one physical Order.  When direct
        parent-stop discovery and the E-only fresh-trend route produce
        different identities for the same stop event, the earliest confirmed
        physical Order owns that parent-stop provenance.  A later identity may
        survive only through an independent cause already merged onto it (for
        example Reset-leg); in that case only the duplicate parent-stop cause
        is removed.
        """
        parent_candidates = [
            item for item in by_geometry.values()
            if "parent-stop" in item[7]
        ]
        if len(parent_candidates) <= 1:
            return

        owner = min(
            parent_candidates,
            key=lambda item: (
                item[2],
                int(getattr(item[1], "first_idx")),
                int(getattr(item[1], "break_idx")),
            ),
        )
        owner_identity = reaction_identity(owner[1])
        for identity, item in list(by_geometry.items()):
            if identity == owner_identity or "parent-stop" not in item[7]:
                continue
            remaining_causes = tuple(
                cause for cause in item[7] if cause != "parent-stop"
            )
            if not remaining_causes:
                del by_geometry[identity]
                continue
            by_geometry[identity] = (
                item[0], item[1], item[2], item[3], item[4], item[5], item[6],
                remaining_causes, None, item[9], item[10],
            )

    def order_candidates(
        self,
        start: datetime,
        continuous_deadline: datetime | None = None,
        audit_legacy: bool = False,
        allow_bounded_continue: bool = False,
        allow_trend_leg_continue: bool = False,
    ) -> list[OrderMatch]:
        """Return every valid E-space Order formed before this E decision."""
        cache_key = (
            start,
            continuous_deadline,
            audit_legacy,
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
                "parent-stop",
                parent_stop_cause_time=start,
            )

        if allow_trend_leg_continue:
            trend_direct = self._trend_leg_direct_order(start)
            if trend_direct is not None:
                self._merge_order_candidate(
                    by_geometry,
                    *trend_direct,
                    "parent-stop",
                    parent_stop_cause_time=start,
                )

        # Order_B is independent Reset-leg provenance.  Calculation and
        # audit use the same canonical formation algorithm; ``audit_legacy``
        # is retained only for public API compatibility.
        for _confirmation, first_index, break_index, order_b_match in (
            self._order_b_candidate_matches(start)
        ):
            identity = (first_index, break_index)
            existing = by_geometry.get(identity)
            if existing is None:
                by_geometry[identity] = order_b_match
                continue
            # Match the legacy `_merge_order_candidate` overwrite semantics:
            # Order_B supplies canonical geometry/stop, while an existing
            # parent-stop cause and its exact provenance remain attached.
            existing_causes = existing[7]
            causes = tuple(dict.fromkeys((*existing_causes, "reset-leg")))
            by_geometry[identity] = (
                order_b_match[0], order_b_match[1], order_b_match[2],
                order_b_match[3], order_b_match[4], order_b_match[5],
                order_b_match[6], causes, existing[8],
                order_b_match[9], order_b_match[10],
            )

        for order_c_match in self._order_c_candidates(start):
            identity = reaction_identity(order_c_match[1])
            old = by_geometry.get(identity)
            if old is None:
                by_geometry[identity] = order_c_match
            else:
                by_geometry[identity] = (
                    *old[:7], tuple(dict.fromkeys((*old[7], "blue-leg"))),
                    *old[8:],
                )

        # Parent-stop provenance is single-consumption.  Resolve that ownership
        # before any candidate stop is allowed to shrink the E decision horizon;
        # otherwise a later fresh-trend Order can incorrectly win merely because
        # its own stop occurs earlier than the true first Order opened by the
        # same parent stop.  Independent Reset-leg provenance is preserved.
        self._enforce_single_parent_stop_owner(by_geometry)

        known_stops = [
            item[6][2]
            for item in by_geometry.values()
            if item[6] is not None
        ]
        provisional_deadline = min(known_stops) if known_stops else self.range_end
        if continuous_deadline is not None:
            provisional_deadline = min(
                provisional_deadline, continuous_deadline
            )
        stopped = [
            item[6][2]
            for item in by_geometry.values()
            if item[6] is not None
        ]
        decision_deadline = min(stopped) if stopped else self.range_end
        if continuous_deadline is not None:
            decision_deadline = min(decision_deadline, continuous_deadline)
        eligible = [
            item
            for item in by_geometry.values()
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

    def _blue_parent_superseded(self, parent: object, parent_stop: datetime) -> bool:
        """A confirmed later Red S closes an older Blue-E order lifecycle."""
        if str(getattr(parent, "family")) != "blue":
            return False
        position = bisect_right(
            self._red_s_source_times, getattr(parent, "source_time")
        )
        return (
            position < len(self._red_s_suffix_min_decision)
            and self._red_s_suffix_min_decision[position] < parent_stop
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

    def _register_order_audit(
        self, parent_type: str, parent: object, parent_stop: datetime,
    ) -> None:
        if self._has_sequence_reset_between(parent.source_time, parent_stop):
            return
        if (
            parent_type == "E"
            and self._blue_parent_superseded(parent, parent_stop)
        ):
            # Enforce the same ownership rule during provisional discovery
            # and final audit. Otherwise a closed branch can seed a carried
            # order into another parent before final reconciliation.
            return
        inherited_owners: list[OrderMatch] = []
        if parent_type == "S":
            inherited_owners = self._unconsumed_s_orders(parent, parent_stop)
        carried_owners = self._carried_orders_for_parent(parent, parent_stop)
        # Exact mirror contract: Bullish and Bearish use the same lifecycle
        # representative/deadline rule; only underlying price comparisons flip.
        inherited_owner = inherited_owners[0] if inherited_owners else None
        carried_owner = carried_owners[0] if carried_owners else None
        continuous_deadline = None
        if parent_type == "S" and carried_owner is None:
            continuous_deadline = (
                inherited_owner[6][2]
                if inherited_owner is not None and inherited_owner[6] is not None
                else self.range_end
            )
        # Creation of a new physical parent-stop Order is independent of an
        # existing carried-live Order and its future strict stop. The carried
        # Order remains a separate *use* route in the E decision race.
        matches = self.order_candidates(
            parent_stop, None,
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
                    parent_stop, None, None,
                ))
        # Gate-owned and carried-live Orders affect E selection, NOT whether
        # a distinct physical Order was created by this accepted parent stop.
        for match in matches:
            number, reaction, confirmation, level, source, source_time = match[:6]
            crossed, causes = match[6], match[7]
            reset_evidence = None
            if "reset-leg" in causes:
                reset_evidence = (
                    (match[9], match[10])
                    if match[9] is not None and match[10] is not None
                    else self._order_b_evidence(reaction, parent_stop)
                )
            # Order_B always resolves to a canonical opposite Reaction.
            # Audit accepts it only when the new same-direction Reset-leg
            # formation cause is proven.
            blue_leg = self._order_c_by_identity.get(reaction_identity(reaction)) if "blue-leg" in causes else None
            if "parent-stop" not in causes and reset_evidence is None and blue_leg is None:
                continue
            key = (
                int(getattr(reaction, "first_idx")),
                int(getattr(reaction, "break_idx")),
            )
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
            if "parent-stop" in causes:
                family = str(getattr(parent, "color", getattr(parent, "family", "")))
                number_value = getattr(parent, "number", None)
                parent_label = parent_type
                if parent_type == "E" and number_value is not None:
                    parent_label = f"E{number_value}"
                if parent.source_time in self.sequence_resets:
                    parent_label = f"StopAll{self.sequence_resets[parent.source_time]}"
                    family = ""
                audit_causes.add(
                    (
                        "parent-stop", parent_label, family, parent_stop,
                        getattr(parent, "source_time"),
                    )
                )
            if reset_evidence is not None:
                audit_causes.add((
                    "reset-leg", reset_evidence[0], reset_evidence[1],
                ))
            if blue_leg is not None:
                audit_causes.add(self._order_c_cause(blue_leg))

    @staticmethod
    def _order_c_cause(item: OrderCFormation) -> tuple[object, ...]:
        return (
            "blue-leg", item.reset_time, item.next_breakout_time,
            item.leg_level, item.level_source_index, item.level_source_time,
            item.blue_source_time, item.strict_break_event_time,
            item.blue_formation_event_time,
            item.leg_start_breakout_time, item.previous_breakout_time,
        )

    def _enrich_order_audit_blue_leg_causes(self) -> None:
        """Retain every complete physical Order_C until its own strict stop.

        This is independent formation provenance, not an instruction to make
        an E or to make historical/hidden geometry publicly visible.
        """
        self._build_order_c_formations()
        for identity, item in self._order_c_by_identity.items():
            entry = self.order_audit.get(identity)
            if entry is None:
                level, source, source_time = self._order_stop(
                    item.order_reaction_number, item.order_reaction
                )
                entry = {
                    "reaction_number": item.order_reaction_number,
                    "reaction": item.order_reaction,
                    "confirmation_time": item.order_confirmation_time,
                    "stop_level": level,
                    "stop_source_index": source,
                    "stop_source_time": source_time,
                    "stop_cross": self._cross_order(item.order_confirmation_time, level),
                    "causes": set(),
                }
                self.order_audit[identity] = entry
                self._index_order_audit_identity(identity, item.order_confirmation_time)
            audit_causes = entry["causes"]
            assert isinstance(audit_causes, set)
            for cause in list(audit_causes):
                if cause[0] == "blue-leg":
                    audit_causes.discard(cause)
            audit_causes.add(self._order_c_cause(item))

    def _enrich_order_audit_reset_causes(self) -> None:
        """Register every independently proven physical Order_B.

        Order_B is an independent creation cause, so selecting another Order
        for an S/E decision does not erase it.  Each physical identity keeps
        its own canonical stop chronology until that stop or a hard StopAll
        boundary.  When one physical Order has several valid Order_B origins,
        only the latest reset-leg cause is authoritative for that cause family.
        """
        latest: dict[tuple[int, int], OrderBFormation] = {}
        for item in self._build_order_b_formations():
            # Once independently formed, a physical Order_B is not invalidated
            # by selection of a different Order for an S/E decision. StopAll
            # remains a hard formation/provenance boundary.
            if self._has_sequence_reset_between(
                item.reset_time, item.order_confirmation_time
            ):
                continue
            identity = reaction_identity(item.order_reaction)
            current = latest.get(identity)
            if current is None or (
                item.reset_time,
                item.strict_break_event_time,
            ) > (
                current.reset_time,
                current.strict_break_event_time,
            ):
                latest[identity] = item

        for identity, item in latest.items():
            entry = self.order_audit.get(identity)
            if entry is None:
                level, source, source_time = self._order_stop(
                    item.order_reaction_number, item.order_reaction
                )
                entry = {
                    "reaction_number": item.order_reaction_number,
                    "reaction": item.order_reaction,
                    "confirmation_time": item.order_confirmation_time,
                    "stop_level": level,
                    "stop_source_index": source,
                    "stop_source_time": source_time,
                    "stop_cross": self._cross_order(
                        item.order_confirmation_time, level
                    ),
                    "causes": set(),
                }
                self.order_audit[identity] = entry
                self._index_order_audit_identity(
                    identity, item.order_confirmation_time
                )
            causes = entry["causes"]
            assert isinstance(causes, set)
            for cause in [cause for cause in causes if cause[0] == "reset-leg"]:
                causes.discard(cause)
            causes.add((
                "reset-leg",
                item.reset_time,
                item.strict_break_event_time,
            ))

    def visual_order_lifecycle(
        self, start: datetime,
    ) -> list[tuple[int, object, datetime, Decimal, int, datetime,
                    tuple[int, datetime, datetime] | None, bool]]:
        """Return only orders admitted by the E lifecycle, including live ones.

        This is presentation/audit output.  It follows the same direct and
        Order_B replacement gates as ``_first_order`` but does not require a
        stop crossing, so a valid still-live order can be drawn without
        changing E calculation.
        """
        position = bisect_left(self._opposite_first_times, start)
        owner = None
        for order_position in range(position, len(self.opposite_reactions)):
            reaction = self.opposite_reactions[order_position]
            first = self._opposite_first_times[order_position]
            confirmation = self._opposite_confirmations[order_position]
            if first >= start and confirmation >= start:
                owner = (order_position + 1, reaction, confirmation, start)
                break
        if owner is None:
            return []

        lifecycle = []
        is_replacement = False
        while owner is not None:
            number, reaction, confirmation, context = owner
            level, source, source_time = self._order_stop(
                number, reaction, context
            )
            crossed = self._cross_order(confirmation, level)
            lifecycle.append(
                (
                    number, reaction, confirmation, level, source,
                    source_time, crossed, is_replacement,
                )
            )
            deadline = crossed[2] if crossed is not None else self.range_end
            owner = self._replacement_order(reaction, confirmation, deadline)
            is_replacement = True
        return lifecycle

    def _parent_stop(self, parent_type: str, parent: object) -> tuple[int, datetime] | None:
        if parent_type == "S":
            start = getattr(parent, "decision_event_time")
        else:
            # An E can only stop after the order-stop event that confirms it.
            start = getattr(parent, "decision_event_time")
        return self._first_parent_stop(start, as_decimal(getattr(parent, "price")))

    def parent_stop(
        self, parent_type: str, parent: object
    ) -> tuple[int, datetime] | None:
        """Public lifecycle API for the first strict parent stop."""
        return self._parent_stop(parent_type, parent)


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
        """Return every Blue-S Order whose stop did not decide the S itself."""
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
            ("carried-live",), None, None, None,
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
            crossed, causes, None, None, None,
        )

    def _initial_order_match(
        self, entry: dict[str, object], causes: tuple[str, ...],
    ) -> OrderMatch:
        # Retained for compatibility callers. Hot E paths use the immutable
        # initial-ledger records above so the strict stop is not recomputed.
        reaction = entry["reaction"]
        confirmation = entry["confirmation_time"]
        level = as_decimal(entry["stop_level"])
        crossed = self._cross_order(confirmation, level)
        return (
            int(entry["reaction_number"]), reaction, confirmation, level,
            int(entry["stop_source_index"]), entry["stop_source_time"],
            crossed, causes, None, None, None,
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
        """Return every Order formed and left live inside this parent lifecycle."""
        lifecycle_start = getattr(parent, "decision_event_time", None)
        if lifecycle_start is None:
            return []
        matches: list[OrderMatch] = []
        for entry in self.order_audit.values():
            created_events: list[datetime] = []
            reset_evidence: tuple[datetime, datetime] | None = None
            has_blue_leg = False
            for cause in entry.get("causes", set()):
                if cause[0] == "parent-stop":
                    created_events.append(cause[3])
                elif cause[0] == "reset-leg":
                    created_events.append(cause[1])
                    reset_evidence = (cause[1], cause[2])
                elif cause[0] == "blue-leg":
                    created_events.append(cause[7])
                    has_blue_leg = True
            if not created_events:
                continue
            created = min(created_events)
            confirmation = entry["confirmation_time"]
            crossed = entry.get("stop_cross")
            if (
                created <= lifecycle_start
                or created >= parent_stop
                or confirmation > parent_stop
                or crossed is None
                or crossed[2] < parent_stop
            ):
                continue
            causes = tuple(("carried-live",)
                           + (("reset-leg",) if reset_evidence is not None else ())
                           + (("blue-leg",) if has_blue_leg else ()))
            reaction = entry["reaction"]
            matches.append((
                int(entry["reaction_number"]), reaction, confirmation,
                as_decimal(entry["stop_level"]), int(entry["stop_source_index"]),
                entry["stop_source_time"], crossed, causes, None,
                reset_evidence[0] if reset_evidence is not None else None,
                reset_evidence[1] if reset_evidence is not None else None,
            ))

        # Initial A-owned Orders are immutable. Restrict the scan to physical
        # First times inside the same legacy eligibility window, then preserve
        # the exact final stop/First ordering below.
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
        return sorted(
            matches,
            key=lambda item: (item[6][2], -int(getattr(item[1], "first_idx"))),
        )

    def _post_stop_accepted_orders_for_parent(
        self, parent: object, parent_stop: datetime,
    ) -> list[OrderMatch]:
        """Return accepted physical Orders confirmed after this parent stopped."""
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

        # Initial ledger: confirmation and exact strict stop are both already
        # materialized, so no per-parent `_cross_order` work remains.
        self._initial_order_records()
        assert self._initial_order_confirmation_times is not None
        confirmation_records = self._initial_order_confirmation_records
        start = bisect_right(self._initial_order_confirmation_times, parent_stop)
        for record in confirmation_records[start:]:
            add_match(self._initial_record_match(record, ("accepted-live",)))

        # Current E-pass ledger is mutable, but accepted identities are also
        # kept in a confirmation-sorted side index. Only the suffix that can
        # satisfy ``confirmation > parent_stop`` is visited; the authoritative
        # ledger entry/provenance remains the dict above.
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

            reset_evidence: tuple[datetime, datetime] | None = None
            has_blue_leg = False
            for cause in entry.get("causes", set()):
                if isinstance(cause, tuple) and cause[0] == "blue-leg":
                    has_blue_leg = True
                if (
                    isinstance(cause, tuple) and len(cause) >= 3
                    and cause[0] == "reset-leg"
                    and isinstance(cause[1], datetime) and isinstance(cause[2], datetime)
                ):
                    evidence = (cause[1], cause[2])
                    if reset_evidence is None or evidence > reset_evidence:
                        reset_evidence = evidence
            causes = tuple(("accepted-live",)
                           + (("reset-leg",) if reset_evidence is not None else ())
                           + (("blue-leg",) if has_blue_leg else ()))
            add_match((
                int(entry.get("reaction_number", 0)), reaction, confirmation,
                as_decimal(level_value), int(source_index), source_time, crossed,
                causes, None,
                reset_evidence[0] if reset_evidence is not None else None,
                reset_evidence[1] if reset_evidence is not None else None,
            ))

        return sorted(
            matches_by_identity.values(),
            key=lambda item: (
                item[6][2], item[2], -int(getattr(item[1], "first_idx")),
            ),
        )


    def _blocked_by_gate_owned_order(self, zone: EZone) -> bool:
        """Reject only a nested Order_A, while preserving its child lineage."""
        if "parent-stop" not in zone.order_causes or "reset-leg" in zone.order_causes:
            return False
        gate_owned = self._gate_owned_initial_order(zone.parent_stop_event_time)
        return (
            gate_owned is not None
            and gate_owned[2] < zone.order_first_time
        )

    def _reset_evidence_for_order(
        self, first_index: int, break_index: int,
    ) -> tuple[datetime, datetime] | None:
        matching = [
            item for item in self._build_order_b_formations()
            if int(getattr(item.order_reaction, "first_idx")) == first_index
            and int(getattr(item.order_reaction, "break_idx")) == break_index
        ]
        if not matching:
            return None
        item = max(
            matching,
            key=lambda value: (
                value.reset_time,
                value.strict_break_event_time,
            ),
        )
        return item.reset_time, item.strict_break_event_time

    def _extreme_between(self, start: datetime, end: datetime) -> tuple[int, datetime, Decimal]:
        # E source ownership is candle-based: include the complete main candle
        # containing the parent stop and the complete main candle containing
        # the order stop. Lower-timeframe chronology decides whether each stop
        # happened, but it must not truncate either boundary candle's OHLC.
        start_index = max(self.start_index, self._main_index(start))
        end_index = min(self.end_index, self._main_index(end))
        source = self.candles[start_index]
        value = self._stop_value(source)
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = self._stop_value(item)
            better = candidate < value if self.direction == "bullish" else candidate > value
            if better:
                source, value = item, candidate
        return int(getattr(source, "index")), getattr(source, "timestamp"), value

    def _zone(
        self, family: str, number: int, parent_type: str,
        parent: object, stop_event: datetime,
    ) -> EZone | None:
        # Every E-space cycle starts at the strict parent stop. The order First
        # must itself strictly cross the active parent/reset boundary.
        inherited = (
            self._unconsumed_s_orders(parent, stop_event)
            if parent_type == "S"
            else []
        )
        gate_owned = self._gate_owned_initial_order(stop_event)
        carried = self._carried_orders_for_parent(parent, stop_event)
        self._register_order_audit(parent_type, parent, stop_event)
        # Parent-neutral shared accepted-Order route: an accepted Order may be
        # confirmed only after this parent stopped and still decide the E when
        # its own strict stop wins chronology.  Its original creation cause is
        # preserved; it is not relabeled as belonging to this parent.
        post_stop_accepted = self._post_stop_accepted_orders_for_parent(
            parent, stop_event
        )
        # A stopped E opens a new direct search at its own stop candle. An
        # older order formed before that event cannot replace the first valid
        # post-stop order. S may still pass its explicitly unconsumed Blue
        # order through the dedicated inheritance rule above.
        # Exact mirror contract: one representative per creation path in both
        # directions, followed by the shared final stop-event race.
        inherited_one = inherited[0] if inherited else None
        carried_one = carried[0] if carried else None
        post_stop_accepted_one = (
            post_stop_accepted[0] if post_stop_accepted else None
        )
        direct = self._first_order(
            stop_event,
            (
                inherited_one[6][2]
                if parent_type == "S" and carried_one is None
                and inherited_one is not None and inherited_one[6] is not None
                else self.range_end
                if parent_type == "S" and carried_one is None
                else None
            ),
            allow_bounded_continue=(parent_type == "S"),
            allow_trend_leg_continue=(parent_type == "E"),
        )
        choices = [
            item for item in (
                direct, inherited_one, carried_one, post_stop_accepted_one
            )
            if item is not None and item[6] is not None
        ]
        order_match = min(
            choices,
            key=lambda item: (item[6][2], -int(getattr(item[1], "first_idx"))),
            default=None,
        )
        if order_match is None:
            return None
        (
            order_number, order, order_confirmation, order_stop,
            stop_source, stop_source_time, crossed, order_causes,
            order_parent_stop_cause_time, order_reset_leg_reset_time,
            order_reset_leg_break_time,
        ) = order_match
        if crossed is None:
            return None
        order_decision_index, order_decision_time, order_decision_event = crossed
        decision_event = max(stop_event, order_decision_event)
        decision_index = self._main_index(decision_event)
        decision_time = getattr(self.candles[decision_index], "timestamp")
        source_index, source_time, price = self._extreme_between(stop_event, decision_event)
        parent_stop_index = self._main_index(stop_event)
        order_first_index = int(getattr(order, "first_idx"))
        top_source = int(getattr(order, "box_top_source_idx"))
        bottom_source = int(getattr(order, "box_bottom_source_idx"))
        return EZone(
            direction=self.direction,
            family=family,
            number=number,
            parent_type=parent_type,
            parent_source_index=int(getattr(parent, "source_index")),
            parent_source_time=getattr(parent, "source_time"),
            parent_price=as_decimal(getattr(parent, "price")),
            parent_stop_index=parent_stop_index,
            parent_stop_time=getattr(self.candles[parent_stop_index], "timestamp"),
            parent_stop_event_time=stop_event,
            order_direction=self.order_direction,
            order_reaction_number=order_number,
            order_mode=str(getattr(order, "mode")),
            order_causes=order_causes,
            order_parent_stop_cause_time=order_parent_stop_cause_time,
            order_reset_leg_reset_time=order_reset_leg_reset_time,
            order_reset_leg_break_time=order_reset_leg_break_time,
            order_first_index=order_first_index,
            order_first_time=getattr(self.candles[order_first_index], "timestamp"),
            order_break_index=int(getattr(order, "break_idx")),
            order_break_time=getattr(self.candles[int(getattr(order, "break_idx"))], "timestamp"),
            order_confirmation_time=order_confirmation,
            order_box_top=as_decimal(getattr(order, "box_top")),
            order_box_top_source_index=top_source,
            order_box_top_source_time=getattr(self.candles[top_source], "timestamp"),
            order_box_bottom=as_decimal(getattr(order, "box_bottom")),
            order_box_bottom_source_index=bottom_source,
            order_box_bottom_source_time=getattr(self.candles[bottom_source], "timestamp"),
            order_stop_level=order_stop,
            order_stop_source_index=stop_source,
            order_stop_source_time=stop_source_time,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event,
        )

    def set_consumed_s_evidence(
        self, evidence: Sequence[tuple[object, object]],
    ) -> None:
        """Register non-public S evidence that continues a stopped larger E."""
        self._consumed_s_evidence = [
            (
                s_zone,
                (int(getattr(owner, "source_index")), getattr(owner, "source_time")),
            )
            for s_zone, owner in evidence
        ]

    def _apply_consumed_s_evidence(self, zones: Sequence[EZone]) -> list[EZone]:
        result = list(zones)
        for s_zone, owner_id in self._consumed_s_evidence:
            owner = next(
                (
                    item for item in result
                    if (item.source_index, item.source_time) == owner_id
                ),
                None,
            )
            if owner is None:
                continue
            continuation = self.continuation_chain_from_s(owner, s_zone)
            result = self.replace_with_earlier_continuation(
                result, owner, continuation
            )
        return result

    def continuation_chain_from_s(
        self, owner: EZone, s_zone: object,
    ) -> list[EZone]:
        """Build the E continuation opened by one S consumed by a stopped E.

        The S remains a calculation/evidence object, not a new public owner.
        Its first E inherits the stopped larger E's reconciled family and next
        number.  Recursive children are then rebuilt from the promoted E so
        Order discovery and stop chronology remain native E calculations.
        """
        stopped = self._parent_stop("S", s_zone)
        if stopped is None:
            return []
        _, stop_event = stopped
        family = str(getattr(owner, "family"))
        number = int(getattr(owner, "number")) + 1
        parent_type = "S"
        parent: object = s_zone
        chain: list[EZone] = []
        seen_sources: set[int] = set()
        while True:
            zone = self._zone(family, number, parent_type, parent, stop_event)
            if zone is None or zone.source_index in seen_sources:
                break
            parent_source_time = getattr(parent, "source_time")
            if self._has_sequence_reset_between(
                parent_source_time, zone.source_time
            ):
                break
            chain.append(zone)
            seen_sources.add(zone.source_index)
            next_stop = self._parent_stop("E", zone)
            if next_stop is None:
                break
            _, stop_event = next_stop
            parent_type, parent = "E", zone
            number += 1
        return chain

    def replace_with_earlier_continuation(
        self, base_zones: Sequence[EZone], owner: EZone, continuation: Sequence[EZone],
    ) -> list[EZone]:
        """Replace an owner's not-yet-decided descendant branch when an earlier one wins."""
        if not continuation:
            return list(base_zones)
        owner_id = (owner.source_index, owner.source_time)
        by_id = {(item.source_index, item.source_time): item for item in base_zones}

        def descends_from_owner(item: EZone) -> bool:
            current = item
            seen: set[tuple[int, datetime]] = set()
            while current.parent_type == "E":
                parent_id = (current.parent_source_index, current.parent_source_time)
                if parent_id == owner_id:
                    return True
                if parent_id in seen:
                    return False
                seen.add(parent_id)
                parent = by_id.get(parent_id)
                if parent is None:
                    return False
                current = parent
            return False

        direct_children = [
            item for item in base_zones
            if item.parent_type == "E"
            and (item.parent_source_index, item.parent_source_time) == owner_id
        ]
        first = continuation[0]
        if direct_children:
            winner = min(
                direct_children,
                key=lambda item: (item.decision_event_time, item.source_time),
            )
            if first.decision_event_time >= winner.decision_event_time:
                return list(base_zones)

        kept = [item for item in base_zones if not descends_from_owner(item)]
        merged = [*kept, *continuation]
        return self.resolve_same_source_conflicts(merged)

    def resolve_same_source_conflicts(
        self, zones: Sequence[EZone],
    ) -> list[EZone]:
        """Keep exactly one accepted E behavior for each physical source candle.

        Candidate discovery may legitimately reach the same source through
        multiple S/E lineages.  Those alternatives are evidence only; once E
        reconciliation has assigned an accepted family/number, a lower-ranked
        alternative at that *same physical source* is not a second behavior.

        Dominance is the shared project rule: Red E outranks Blue E regardless
        of number, and within the same family the higher E number outranks the
        lower number.  Exact ties preserve the earlier accepted object so this
        resolver never rewrites provenance merely to deduplicate output.
        """
        winners: dict[tuple[int, datetime], EZone] = {}
        order: list[tuple[int, datetime]] = []

        def outranks(candidate: EZone, current: EZone) -> bool:
            candidate_priority = self.sequence_priority("e", candidate.family)
            current_priority = self.sequence_priority("e", current.family)
            if candidate_priority != current_priority:
                return candidate_priority > current_priority
            if candidate.family == current.family and candidate.number != current.number:
                return candidate.number > current.number
            return False

        for zone in zones:
            identity = (int(zone.source_index), zone.source_time)
            current = winners.get(identity)
            if current is None:
                winners[identity] = zone
                order.append(identity)
            elif outranks(zone, current):
                winners[identity] = zone

        result = [winners[identity] for identity in order]
        result.sort(
            key=lambda item: (
                item.source_time, item.source_index, item.decision_event_time,
            )
        )
        return result

    def restore_independent_s_roots(
        self, dominant_zones: Sequence[EZone],
    ) -> list[EZone]:
        """Restore calculation-valid E1 roots owned directly by accepted S.

        E dominance chooses which chain owns larger-module continuation, but
        formation of a new E behavior is independent: every accepted, stopped
        S may still form its own direct E1.  A reconciled dominant zone that
        came from that same S is therefore replaced by the original direct
        root (family/number from the S chain), while missing roots are added.
        Suppressed S evidence consumed by a larger E is not in ``self.s_zones``
        and cannot manufacture a competing E1 through this path.
        """
        # A physical source already owned by an accepted E cannot also keep
        # an S parent alive for downstream E-root restoration. Public lifecycle
        # finality already gives that candle to E; applying the same ownership
        # here prevents a provisional same-source S from manufacturing a later
        # E1 after reconciliation.
        dominant_sources = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in dominant_zones
        }
        accepted_s = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in self.s_zones
            if (int(getattr(item, "source_index")), getattr(item, "source_time"))
            not in dominant_sources
        }
        roots = [
            item for item in self._last_candidate_zones
            if item.parent_type == "S"
            and int(item.number) == 1
            and (item.parent_source_index, item.parent_source_time) in accepted_s
        ]
        result = list(dominant_zones)
        for root in roots:
            parent_id = (root.parent_source_index, root.parent_source_time)
            same_parent = [
                item for item in result
                if item.parent_type == "S"
                and (item.parent_source_index, item.parent_source_time) == parent_id
            ]
            if same_parent:
                winner = min(
                    same_parent,
                    key=lambda item: (item.decision_event_time, item.source_time),
                )
                result = [item for item in result if item is not winner]
                result.append(root)
            elif not any(
                item.source_index == root.source_index
                and item.source_time == root.source_time
                and item.parent_type == root.parent_type
                and item.parent_source_index == root.parent_source_index
                and item.parent_source_time == root.parent_source_time
                for item in result
            ):
                result.append(root)
        return self.resolve_same_source_conflicts(result)

    def _discover_candidate_chains(self) -> list[EZone]:
        """Build provisional recursive E chains from every stopped S parent.

        Calculation-invalid S evidence is still audited normally.  It loses
        only the right to open a *competing cross-family E root* when its exact
        physical source is already occupied by a native E continuation.  This
        prevents a dead A→S branch from retroactively deleting/recoloring the
        existing E chain while preserving same-family provenance and OrderAudit.
        """
        # Discover S-owned orders before walking recursive E chains.  A valid
        # order formed inside an E parent's lifetime must remain available even
        # when that S branch is reconciled later than the E branch.
        for s_zone in self.s_zones:
            stop = self._parent_stop("S", s_zone)
            if stop is not None:
                self._register_order_audit("S", s_zone, stop[1])

        chains: list[tuple[object, list[EZone]]] = []
        candidates: list[EZone] = []
        for s_zone in self.s_zones:
            stop = self._parent_stop("S", s_zone)
            if stop is None:
                continue
            _, stop_event = stop

            # Every fully formed S starts an independent provisional E chain.
            # Final lifecycle eligibility is resolved after all candidate
            # continuations are visible, so exact same-source cross-family
            # collisions can be judged without timestamp/fixture exceptions.
            family = str(getattr(s_zone, "color"))
            number = 1

            parent_type: str = "S"
            parent: object = s_zone
            chain_sources: set[int] = set()
            chain: list[EZone] = []
            while True:
                zone = self._zone(family, number, parent_type, parent, stop_event)
                if zone is None:
                    break
                if zone.source_index in chain_sources:
                    break
                chain.append(zone)
                candidates.append(zone)
                chain_sources.add(zone.source_index)
                parent_type, parent = "E", zone
                next_stop = self._parent_stop("E", zone)
                if next_stop is None:
                    break
                _, stop_event = next_stop
                number += 1
            if chain:
                chains.append((s_zone, chain))

        if not self.invalid_s_root_identities or not candidates:
            return candidates

        continuation_families: dict[tuple[datetime, int], set[str]] = {}
        for zone in candidates:
            if zone.parent_type != "E":
                continue
            identity = (zone.source_time, int(zone.source_index))
            continuation_families.setdefault(identity, set()).add(zone.family)

        blocked_roots: set[tuple[datetime, int]] = set()
        for s_zone, _ in chains:
            identity = (
                getattr(s_zone, "source_time"),
                int(getattr(s_zone, "source_index")),
            )
            if identity not in self.invalid_s_root_identities:
                continue
            s_family = str(getattr(s_zone, "color"))
            if any(
                family != s_family
                for family in continuation_families.get(identity, set())
            ):
                blocked_roots.add(identity)

        if not blocked_roots:
            return candidates

        return [
            zone
            for s_zone, chain in chains
            if (
                getattr(s_zone, "source_time"),
                int(getattr(s_zone, "source_index")),
            ) not in blocked_roots
            for zone in chain
        ]

    def _reconcile_candidate_chains(
        self, candidates: list[EZone]
    ) -> list[EZone]:
        """Resolve competing E chains into the accepted chronological lifecycle."""
        # Resolve competing chains chronologically.  A stopped E is removed
        # from the active set immediately; it remains only as historical
        # output and cannot affect a later family or number.
        by_source: dict[int, list[EZone]] = {}
        for zone in candidates:
            by_source.setdefault(zone.source_index, []).append(zone)
        # A later E continuation can supersede a provisional E that was
        # started directly from an S before the continuation was confirmed.
        # Keep the later, deeper (bullish) / higher (bearish) structure.  This
        # This prevents a provisional S-owned object from consuming the active
        # chain before the later confirmed continuation.
        pending = sorted(
            by_source.values(),
            key=lambda item: (
                min(zone.source_time for zone in item),
                min(zone.decision_event_time for zone in item),
            ),
        )
        numbered: list[EZone] = []
        active: list[EZone] = []
        sequence_start: datetime | None = None

        candidates_by_source_time = {
            (item.source_index, item.source_time): item
            for item in candidates
        }

        children_by_parent: dict[tuple[int, object], list[EZone]] = {}
        s_children_by_source: dict[tuple[int, object], list[EZone]] = {}
        for item in candidates:
            if item.parent_type == "E":
                children_by_parent.setdefault(
                    (item.parent_source_index, item.parent_source_time), []
                ).append(item)
            elif item.parent_type == "S":
                s_children_by_source.setdefault(
                    (item.source_index, item.source_time), []
                ).append(item)

        def valid_order(zone: EZone) -> bool:
            if self._blocked_by_gate_owned_order(zone):
                return False
            if (
                zone.parent_type == "S"
                or "reset-leg" not in zone.order_causes
                or zone.family != "blue"
            ):
                return True
            children = children_by_parent.get(
                (zone.source_index, zone.source_time), []
            )
            for child in children:
                for competing in s_children_by_source.get(
                    (child.source_index, child.source_time), []
                ):
                    if competing.decision_event_time <= child.decision_event_time:
                        return False
            return True

        def invalidated_only_by_future_s(zone: EZone) -> bool:
            if valid_order(zone) or zone.parent_type != "E":
                return False
            children = children_by_parent.get(
                (zone.source_index, zone.source_time), []
            )
            parent_times = {
                competing.parent_source_time
                for child in children
                for competing in s_children_by_source.get(
                    (child.source_index, child.source_time), []
                )
                if competing.decision_event_time <= child.decision_event_time
            }
            return any(value > zone.source_time for value in parent_times)

        def parent_active(zone: EZone, seen: set[tuple[int, datetime]] | None = None) -> bool:
            if zone.parent_type == "S":
                parent_s = next(
                    (
                        item for item in self.s_zones
                        if int(getattr(item, "source_index"))
                        == zone.parent_source_index
                        and getattr(item, "source_time")
                        == zone.parent_source_time
                    ),
                    None,
                )
                if parent_s is None:
                    return False
                if sequence_start is not None and (
                    parent_s.source_time <= sequence_start
                    or parent_s.a_source_time < sequence_start
                ):
                    return False
                prior_e = [
                    item for item in numbered
                    if getattr(item, "source_time")
                    < zone.source_time
                    and (sequence_start is None or item.source_time > sequence_start)
                ]
                if not prior_e:
                    return True
                prior = max(
                    prior_e, key=lambda item: getattr(item, "source_time")
                )
                rebuilt_after_e = (
                    getattr(parent_s, "source_time")
                    > getattr(prior, "source_time")
                    and getattr(parent_s, "a_source_time")
                    >= getattr(prior, "source_time")
                )
                # A still-unconsumed Red S is not invalidated by a nested
                # Blue E. Its later strict stop owns the Red transition.
                dominant_s = (
                    str(getattr(parent_s, "color")) == "red"
                    and prior.family == "blue"
                    and parent_s.source_time < prior.source_time
                    and not any(
                        item.parent_type == "S"
                        and item.parent_source_time == zone.parent_source_time
                        for item in numbered
                    )
                )
                return rebuilt_after_e or dominant_s
            if zone.parent_source_time == sequence_start:
                # The StopAll source is a valid order gate, but never an
                # active E whose family/number could leak across the reset.
                return True
            if any(
                item.source_index == zone.parent_source_index
                and item.source_time == zone.parent_source_time
                for item in active
            ):
                return True
            identity = (zone.parent_source_index, zone.parent_source_time)
            if seen is None:
                seen = set()
            if identity in seen:
                return False
            seen.add(identity)
            skipped_parent = candidates_by_source_time.get(identity)
            return (
                skipped_parent is not None
                and not valid_order(skipped_parent)
                and parent_active(skipped_parent, seen)
            )

        def stopped_by(zone: EZone, prior: EZone) -> bool:
            if zone.decision_event_time <= prior.decision_event_time:
                return False
            if self.direction == "bullish":
                return zone.price < prior.price
            return zone.price > prior.price

        for group in pending:
            eligible = [
                item for item in group
                if valid_order(item) and parent_active(item)
            ]
            if not eligible:
                continue
            # A lower-priority S cannot steal an active E continuation.
            # Red S may supersede Blue E, but no S supersedes Red E.
            # Color follows the accepted stopped parent's reconciled family.
            eligible = [
                item
                for item in eligible
                if not (
                    item.parent_type == "S"
                    and any(
                        stopped_by(item, owner)
                        and (owner.family == "red" or item.family == "blue")
                        and any(
                            child.parent_type == "E"
                            and child.parent_source_index == owner.source_index
                            and child.parent_source_time == owner.source_time
                            and child.decision_event_time
                            >= item.decision_event_time
                            for child in candidates
                        )
                        for owner in active
                    )
                )
            ]
            if not eligible:
                continue
            current_owners = [
                item for item in eligible
                if not (
                    item.parent_type == "E"
                    and item.family == "blue"
                    and any(
                        str(getattr(s_zone, "color")) == "red"
                        and getattr(s_zone, "source_time")
                        > item.parent_source_time
                        and getattr(s_zone, "decision_event_time")
                        < item.parent_stop_event_time
                        for s_zone in self.s_zones
                    )
                )
            ]
            if current_owners:
                eligible = current_owners
            def ownership_priority(item: EZone) -> int:
                parent = next((prior for prior in active
                    if item.parent_type == "E"
                    and prior.source_time == item.parent_source_time), None)
                parent_family = parent.family if parent else item.family
                return self.sequence_priority(item.parent_type, parent_family)

            # One physical E source may be reachable through competing
            # Red/Blue S/E lineages.  Family priority is authoritative at the
            # physical source: Red outranks Blue even when the Blue candidate
            # happens to reach its decision a few lower-timeframe ticks
            # earlier.  Chronology remains the tie-breaker *within* the same
            # behavioral priority.  Applying this before chain reconciliation
            # prevents the dominant Red candidate from being discarded before
            # the final same-source resolver can see it.
            zone = min(
                eligible,
                key=lambda item: (
                    -ownership_priority(item),
                    item.decision_event_time,
                    item.parent_stop_event_time,
                ),
            )
            stopped_by_family: dict[str, list[EZone]] = {"red": [], "blue": []}
            for prior in active:
                if stopped_by(zone, prior):
                    stopped_by_family[prior.family].append(prior)

            parent_identity = (zone.parent_source_index, zone.parent_source_time)
            parent_is_active = (
                zone.parent_type == "S"
                or zone.parent_source_time == sequence_start
            ) or any(
                (item.source_index, item.source_time) == parent_identity
                for item in active
            )
            if not parent_is_active:
                reset_evidence = self._reset_evidence_for_order(
                    zone.order_first_index, zone.order_break_index
                )
                if reset_evidence is not None:
                    zone = replace(
                        zone,
                        order_causes=("reset-leg",),
                        order_parent_stop_cause_time=None,
                        order_reset_leg_reset_time=reset_evidence[0],
                        order_reset_leg_break_time=reset_evidence[1],
                    )

            owner = next((item for item in active
                          if zone.parent_type == "E"
                          and item.source_time == zone.parent_source_time), None)
            # Color follows the accepted stopped parent, not merely the most
            # recent S. A still-unbroken Red S does not recolor a nested E.
            parent_family = owner.family if owner is not None else zone.family

            if parent_family == "red":
                family = "red"
                number = (
                    max(item.number for item in stopped_by_family["red"]) + 1
                    if stopped_by_family["red"]
                    else 1
                )
            elif stopped_by_family["red"]:
                family = "red"
                number = max(item.number for item in stopped_by_family["red"]) + 1
            elif parent_family == "blue":
                family = "blue"
                number = (
                    max(item.number for item in stopped_by_family["blue"]) + 1
                    if stopped_by_family["blue"]
                    else 1
                )
            elif stopped_by_family["blue"]:
                family = "blue"
                number = max(item.number for item in stopped_by_family["blue"]) + 1
            else:
                family = zone.family
                number = 1
            stopped_ids = {
                (item.source_index, item.source_time)
                for values in stopped_by_family.values() for item in values
            }
            active = [
                item for item in active
                if (item.source_index, item.source_time) not in stopped_ids
            ]
            numbered_zone = replace(zone, family=family, number=number)
            numbered.append(numbered_zone)
            if zone.source_time in self.sequence_resets:
                active.clear()
                sequence_start = zone.source_time
            else:
                active.append(numbered_zone)
        def collect_lineage(zone: EZone, seen: set[tuple[int, datetime]]) -> None:
            identity = (zone.source_index, zone.source_time)
            if identity in seen:
                return
            seen.add(identity)
            self.visual_lifecycle_starts.add(zone.parent_stop_event_time)
            if zone.parent_type == "S":
                return
            parent = candidates_by_source_time.get(
                (zone.parent_source_index, zone.parent_source_time)
            )
            if parent is not None:
                collect_lineage(parent, seen)

        numbered_ids = {
            (item.source_index, item.source_time) for item in numbered
        }
        numbered.extend(
            item for item in candidates
            if invalidated_only_by_future_s(item)
            and (item.source_index, item.source_time) not in numbered_ids
            and not self._has_sequence_reset_between(
                item.parent_source_time, item.source_time
            )
        )

        lineage_seen: set[tuple[int, datetime]] = set()
        for zone in numbered:
            collect_lineage(zone, lineage_seen)

        numbered = [replace(item, parent_type="StopAll")
                    if item.parent_type == "E"
                    and item.parent_source_time in self.sequence_resets
                    else item for item in numbered]
        return numbered

    def _historical_rescue_candidates(
        self, candidates: Sequence[EZone], accepted: Sequence[EZone]
    ) -> list[EZone]:
        """Return presentation-only historical E objects suppressed by future conflicts.

        Primary reconciliation is authoritative and remains byte-for-byte
        behaviorally unchanged.  This pass only restores a candidate when:
        * it is an E-parented Blue Order_B object;
        * its Order is not blocked by a gate-owned prohibition;
        * the suppressing S lineage itself formed after this E, so the conflict is truly future-only;
        * its direct E parent is already accepted historical output;
        * no sequence reset lies between parent and candidate; and
        * no accepted behavior already owns the same physical E source.

        Rescued objects are intentionally excluded from calculation ownership.
        """
        children_by_parent: dict[tuple[int, object], list[EZone]] = {}
        s_children_by_source: dict[tuple[int, object], list[EZone]] = {}
        for item in candidates:
            if item.parent_type == "E":
                children_by_parent.setdefault(
                    (item.parent_source_index, item.parent_source_time), []
                ).append(item)
            elif item.parent_type == "S":
                s_children_by_source.setdefault(
                    (item.source_index, item.source_time), []
                ).append(item)

        def suppressed_by_future_child_conflict(zone: EZone) -> bool:
            if zone.parent_type != "E":
                return False
            if "reset-leg" not in zone.order_causes or zone.family != "blue":
                return False
            if self._blocked_by_gate_owned_order(zone):
                return False
            children = children_by_parent.get(
                (zone.source_index, zone.source_time), []
            )
            return any(
                competing.decision_event_time <= child.decision_event_time
                and competing.parent_source_time > zone.source_time
                for child in children
                for competing in s_children_by_source.get(
                    (child.source_index, child.source_time), []
                )
            )

        accepted_ids = {
            (item.source_index, item.source_time) for item in accepted
        }
        rescued: list[EZone] = []
        rescued_ids: set[tuple[int, datetime]] = set()

        while True:
            batch = [
                item for item in candidates
                if suppressed_by_future_child_conflict(item)
                and (item.source_index, item.source_time) not in accepted_ids
                and (item.source_index, item.source_time) not in rescued_ids
                and (item.parent_source_index, item.parent_source_time)
                    in accepted_ids | rescued_ids
                and not self._has_sequence_reset_between(
                    item.parent_source_time, item.source_time
                )
            ]
            if not batch:
                break
            batch = self.resolve_same_source_conflicts(batch)
            added = False
            for item in batch:
                identity = (item.source_index, item.source_time)
                if identity in accepted_ids or identity in rescued_ids:
                    continue
                rescued.append(item)
                rescued_ids.add(identity)
                added = True
            if not added:
                break

        rescued.sort(
            key=lambda item: (
                item.source_time, item.source_index, item.decision_event_time
            )
        )
        return rescued


    def _rebuild_accepted_order_audit(
        self, numbered: list[EZone], supplemental_s_zones: Sequence[object] = (),
    ) -> list[EZone]:
        """Rebuild Order Audit from accepted S/E/StopAll state only."""
        # Audit only accepted S/E state. Provisional candidate chains must not
        # create visible or reported order genders.  Preserve a snapshot of the
        # pre-reconciliation ledger so an accepted carried-live Order can keep
        # its original creation cause even when that creating parent is no
        # longer a public behavior.
        prior_order_audit = {
            identity: {
                **entry,
                "causes": set(entry.get("causes", set())),
            }
            for identity, entry in self.order_audit.items()
        }
        self._clear_order_audit()
        self._build_order_c_formations()
        accepted_parents: list[tuple[str, object]] = [
            ("S", item) for item in self.s_zones
        ] + [("StopAll" if item.source_time in self.sequence_resets else "E", item)
             for item in numbered]
        for parent_type, parent in accepted_parents:
            stop = self._parent_stop(parent_type, parent)
            if stop is None:
                continue
            if parent_type == "E":
                # A later accepted Red S owns the behavioral color and closes
                # older Blue-E continuation state. The historical E remains
                # visible, but its later price crossing cannot open an order.
                if self._blue_parent_superseded(parent, stop[1]):
                    continue
            self._register_order_audit(parent_type, parent, stop[1])

        # Every physical Order embedded in an accepted E must remain present in
        # the canonical ledger.  This includes two cases that cannot be rebuilt
        # from final public parents alone:
        #   1) carried-live Orders whose original creating parent became
        #      historical/non-public during reconciliation; and
        #   2) valid bounded fresh-trend geometry with reaction number 0, which
        #      has no canonical opposite-Reaction object.
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
                causes.update(prior_entry.get("causes", set()))

            # An E may carry an A-owned Order that was already accepted before
            # S/E reconciliation.  Initial A audit uses ``a_causes`` rather
            # than the generic E-ledger cause tuple, so translate that original
            # creation provenance when the carried physical Order would
            # otherwise become cause-less after final-parent rebuilding.
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
                    parent_zone = next(
                        (
                            item for item in numbered
                            if item.source_index == zone.parent_source_index
                            and item.source_time == zone.parent_source_time
                        ),
                        None,
                    )
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
            order_c = self._order_c_by_identity.get(identity)
            if order_c is not None and "blue-leg" in zone.order_causes:
                causes.add(self._order_c_cause(order_c))
            if (
                zone.order_reset_leg_reset_time is not None
                and zone.order_reset_leg_break_time is not None
            ):
                causes.add((
                    "reset-leg",
                    zone.order_reset_leg_reset_time,
                    zone.order_reset_leg_break_time,
                ))

            # carried-live / accepted-live labels are use provenance, not
            # creation causes. Their original accepted parent-stop/reset-leg
            # cause must therefore come from the preserved ledgers above. If
            # no creation cause can be proven, do not fabricate one.
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
            self._index_order_audit_identity(
                identity, zone.order_confirmation_time
            )

        self._enrich_order_audit_reset_causes()
        self._enrich_order_audit_blue_leg_causes()

        # A retained order can have Reset-leg evidence predating its new
        # StopAll gate. Preserve that proven secondary cause in the emitted
        # object as well as the ledger; it never changes selection or weight.
        for index, zone in enumerate(numbered):
            if zone.parent_type != "StopAll":
                continue
            entry = self.order_audit.get(
                order_identity(zone.order_first_index, zone.order_break_index)
            )
            reset_causes = sorted(cause for cause in entry["causes"]
                                  if cause[0] == "reset-leg") if entry else []
            if reset_causes and "reset-leg" not in zone.order_causes:
                cause = reset_causes[0]
                numbered[index] = replace(
                    zone, order_causes=(*zone.order_causes, "reset-leg"),
                    order_reset_leg_reset_time=cause[1],
                    order_reset_leg_break_time=cause[2],
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
        accepted branch must become authoritative for OrderAudit as well; this
        public hook keeps calculation ownership in the E engine instead of
        forcing the bridge to reconstruct trading provenance.
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
        return rebuilt

    def detect(self) -> list[EZone]:
        """Discover, reconcile and audit recursive E lifecycles."""
        self._clear_order_audit()
        self.visual_lifecycle_starts.clear()
        candidates = self._discover_candidate_chains()
        self._last_candidate_zones = list(candidates)
        numbered = self._reconcile_candidate_chains(candidates)
        numbered = self._apply_consumed_s_evidence(numbered)
        numbered = self.resolve_same_source_conflicts(numbered)
        numbered = self._rebuild_accepted_order_audit(numbered)
        self.historical_rescued_zones = self._historical_rescue_candidates(
            candidates, numbered
        )
        return numbered


def detect_e_zones(
    direction: str,
    trend_reactions: Sequence[object],
    opposite_reactions: Sequence[object],
    s_zones: Sequence[object],
    trend_resets: Sequence[object],
    opposite_resets: Sequence[object],
    chronology: object,
    start_index: int = 0,
    end_index: int | None = None,
    geometry_finder: Callable[[str, int, int], object | None] | None = None,
    direct_geometry_finder: Callable[[str, int, int, datetime], object | None] | None = None,
    blocked_order_first_times: set[datetime] | None = None,
    initial_order_audit: dict[tuple[int, int], dict[str, object]] | None = None,
    sequence_priority: Callable[[str, str], int] | None = None,
    invalid_s_root_identities: set[tuple[datetime, int]] | None = None,
    trend_blue_lines: Sequence[object] = (),
) -> list[EZone]:
    return EZoneDetector(
        direction,
        trend_reactions,
        opposite_reactions,
        s_zones,
        trend_resets,
        opposite_resets,
        chronology,
        start_index,
        end_index,
        geometry_finder,
        direct_geometry_finder,
        blocked_order_first_times,
        initial_order_audit,
        sequence_priority=sequence_priority,
        invalid_s_root_identities=invalid_s_root_identities,
        trend_blue_lines=trend_blue_lines,
    ).detect()
