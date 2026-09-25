"""A-zone calculation from authoritative Reaction and Blue state.

Owns Blue-pair/double-stop A formation, trigger chronology, continuation
geometry, and A source selection. Downstream S/larger-module ownership is
handled by the S and lifecycle engines rather than rewritten here.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Sequence

from core_utils import as_decimal
from direction_policy import policy_for


A_ZONE_VERSION = "1.6.4"
A_ZONE_LAST_MODIFIED_DATE = "2026-09-21"


@dataclass(frozen=True, slots=True)
class BlueState:
    ordinal: int
    line: object
    formation_index: int
    formation_time: datetime
    stop_index: int | None
    stop_time: datetime | None
    stop_event_time: datetime | None
    stop_level: Decimal
    stop_event_extreme: Decimal | None


@dataclass(frozen=True, slots=True)
class AZone:
    direction: str
    blue_1_ordinal: int
    blue_2_ordinal: int
    blue_1_source_time: datetime
    blue_2_source_time: datetime
    blue_1_stop_time: datetime
    blue_2_stop_time: datetime
    blue_1_stop_level: Decimal
    blue_2_stop_level: Decimal
    continuation_level: Decimal
    continuation_source_index: int
    continuation_source_time: datetime
    trigger_index: int
    trigger_time: datetime
    trigger_event_time: datetime
    reaction_number: int
    reaction_first_time: datetime
    reaction_break_time: datetime
    source_index: int
    source_time: datetime
    price: Decimal
    # Immutable, presentation-only provenance. These fields never participate
    # in A acceptance, ordering, visibility, or downstream calculations.
    formation_route: str | None = field(default=None, kw_only=True)
    blue_1_stop_event_time: datetime | None = field(default=None, kw_only=True)
    blue_2_stop_event_time: datetime | None = field(default=None, kw_only=True)


class AZoneDetector:
    def __init__(
        self,
        direction: str,
        reactions: Sequence[object],
        blue_lines: Sequence[object],
        chronology: object,
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.policy = policy_for(direction)
        self.reactions = list(reactions)
        self.blue_lines = sorted(
            blue_lines,
            key=lambda item: (
                int(getattr(item, "reaction_number")),
                getattr(item, "source_time"),
                str(getattr(item, "kind")),
            ),
        )
        self.chronology = chronology
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.timeframe = chronology.timeframe
        self.candle_times = chronology.times
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index

    @property
    def extreme_name(self) -> str:
        return self.policy.extreme_attr

    def _strict_cross(self, value: Decimal, level: Decimal) -> bool:
        return self.policy.strict_cross(value, level)

    def _better(self, value: Decimal, current: Decimal) -> bool:
        return self.policy.better_extreme(value, current)

    def _main_index(self, timestamp: datetime) -> int:
        return self.chronology.main_index(timestamp)

    def _lower_window(
        self, start: datetime, end: datetime | None
    ) -> Sequence[object]:
        return self.chronology.lower_window(start, end)

    def _first_crossing(
        self,
        level: Decimal,
        start: datetime,
        end: datetime | None,
    ) -> tuple[int, datetime, Decimal] | None:
        left = bisect_left(self.lower_times, start)
        right = len(self.lower) if end is None else bisect_left(self.lower_times, end)
        if right > left and self.lower_index is not None:
            position = (
                self.lower_index.first_less(left, right, level)
                if self.direction == "bullish"
                else self.lower_index.first_greater(left, right, level)
            )
            if position is None:
                return None
            item = self.lower[position]
            event_time = getattr(item, "timestamp")
            value = as_decimal(getattr(item, self.extreme_name))
            return self._main_index(event_time), event_time, value

        lower_items = self.lower[left:right]
        for item in lower_items:
            value = as_decimal(getattr(item, self.extreme_name))
            if self._strict_cross(value, level):
                event_time = getattr(item, "timestamp")
                return self._main_index(event_time), event_time, value
        if lower_items:
            return None

        start_index = max(0, bisect_left(self.candle_times, start))
        end_index = (
            len(self.candles)
            if end is None
            else max(start_index, bisect_left(self.candle_times, end))
        )
        for item in self.candles[start_index:end_index]:
            value = as_decimal(getattr(item, self.extreme_name))
            if self._strict_cross(value, level):
                return int(getattr(item, "index")), getattr(item, "timestamp"), value
        return None

    def _range_extreme(
        self, start: datetime, end: datetime
    ) -> tuple[Decimal, int, datetime]:
        if end < start:
            raise ValueError("Extreme range end precedes its start.")
        lower_items = self._lower_window(start, end + timedelta(microseconds=1))
        if lower_items:
            source = lower_items[0]
            value = as_decimal(getattr(source, self.extreme_name))
            for item in lower_items[1:]:
                candidate = as_decimal(getattr(item, self.extreme_name))
                if self._better(candidate, value):
                    source = item
                    value = candidate
            source_index = self._main_index(getattr(source, "timestamp"))
            return (
                value,
                source_index,
                getattr(self.candles[source_index], "timestamp"),
            )
        start_index = max(0, bisect_right(self.candle_times, start) - 1)
        end_index = min(
            len(self.candles) - 1,
            max(start_index, bisect_right(self.candle_times, end) - 1),
        )
        source = self.candles[start_index]
        value = as_decimal(getattr(source, self.extreme_name))
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = as_decimal(getattr(item, self.extreme_name))
            if self._better(candidate, value):
                source = item
                value = candidate
        return value, int(getattr(source, "index")), getattr(source, "timestamp")

    def _formation(self, line: object) -> tuple[int, datetime, datetime]:
        reaction_number = int(getattr(line, "reaction_number"))
        if reaction_number < 1 or reaction_number > len(self.reactions):
            raise ValueError("Blue Line refers to a missing reaction.")
        if str(getattr(line, "kind")) == "scale":
            reaction = self.reactions[reaction_number - 1]
            index = int(getattr(reaction, "break_idx"))
            event_time = self._reaction_confirmation_time(reaction)
            stop_scan_time = event_time
        else:
            index = int(getattr(line, "source_index"))
            source_time = getattr(self.candles[index], "timestamp")
            event_time = self._reset_formation_time(line, index)
            stop_scan_time = source_time + self.timeframe
        candle = self.candles[index]
        return index, event_time, stop_scan_time

    def _reset_formation_time(self, line: object, source_index: int) -> datetime:
        """Return the exact strict Reset event that makes a Reset Blue exist."""
        source = self.candles[source_index]
        start = getattr(source, "timestamp")
        end = start + self.timeframe
        broken_level = as_decimal(getattr(line, "broken_level"))
        for item in self._lower_window(start, end):
            value = as_decimal(getattr(item, self.extreme_name))
            if self._strict_cross(value, broken_level):
                return getattr(item, "timestamp")
        return start

    def _build_blue_states(self) -> list[BlueState]:
        states: list[BlueState] = []
        for ordinal, line in enumerate(self.blue_lines, start=1):
            if not bool(getattr(line, "calculation_valid", True)):
                continue
            formation_index, formation_time, stop_scan_time = self._formation(line)
            stop_level = as_decimal(getattr(line, "source_extreme"))
            stop = self._first_crossing(
                stop_level,
                stop_scan_time,
                None,
            )
            states.append(
                BlueState(
                    ordinal=ordinal,
                    line=line,
                    formation_index=formation_index,
                    formation_time=formation_time,
                    stop_index=stop[0] if stop else None,
                    stop_time=(
                        getattr(self.candles[stop[0]], "timestamp") if stop else None
                    ),
                    stop_event_time=stop[1] if stop else None,
                    stop_level=stop_level,
                    stop_event_extreme=stop[2] if stop else None,
                )
            )
        return states

    def _double_stop_a_candidates(self) -> list[AZone]:
        result: list[AZone] = []
        previous: tuple[int, object] | None = None
        for ordinal, line in enumerate(self.blue_lines, start=1):
            if bool(getattr(line, "calculation_valid", True)):
                previous = (ordinal, line)
                continue
            if previous is None:
                continue
            previous_ordinal, previous_line = previous
            formation_index = int(getattr(line, "source_index"))
            formation_time = getattr(line, "source_time")
            source_time = getattr(self.candles[formation_index], "timestamp")
            crossing = self._first_crossing(
                as_decimal(getattr(previous_line, "source_extreme")),
                formation_time,
                source_time + self.timeframe,
            )
            if crossing is None or crossing[0] != formation_index:
                continue
            trigger_index, trigger_event_time, _ = crossing
            match = self._first_reaction_after(
                trigger_event_time,
                not_before=formation_time,
            )
            if match is None:
                continue
            reaction_number, reaction = match
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            source = self._a_source(trigger_index, reaction)
            if source is None:
                continue
            source_index, a_source_time, price = source
            result.append(
                AZone(
                    direction=self.direction,
                    blue_1_ordinal=previous_ordinal,
                    blue_2_ordinal=ordinal,
                    blue_1_source_time=getattr(previous_line, "source_time"),
                    blue_2_source_time=getattr(line, "source_time"),
                    blue_1_stop_time=source_time,
                    blue_2_stop_time=source_time,
                    blue_1_stop_level=as_decimal(getattr(previous_line, "source_extreme")),
                    blue_2_stop_level=as_decimal(getattr(line, "source_extreme")),
                    continuation_level=as_decimal(getattr(previous_line, "source_extreme")),
                    continuation_source_index=int(getattr(previous_line, "source_index")),
                    continuation_source_time=getattr(previous_line, "source_time"),
                    trigger_index=trigger_index,
                    trigger_time=getattr(self.candles[trigger_index], "timestamp"),
                    trigger_event_time=trigger_event_time,
                    reaction_number=reaction_number,
                    reaction_first_time=getattr(self.candles[first_index], "timestamp"),
                    reaction_break_time=getattr(self.candles[break_index], "timestamp"),
                    source_index=source_index,
                    source_time=a_source_time,
                    price=price,
                    formation_route="double-stop",
                )
            )
            previous = None
        return result

    def _pair_trigger(
        self,
        previous: BlueState,
        current: BlueState,
        expires_at: datetime | None,
    ) -> tuple[
        Decimal,
        int,
        datetime,
        int,
        datetime,
        datetime,
        datetime,
        datetime,
    ] | None:
        if previous.stop_event_time is None or previous.stop_time is None:
            return None
        if (
            expires_at is not None
            and previous.stop_event_time > expires_at
        ):
            return None

        # A following Blue Line inherits the stop level established by the
        # previous line's first aligned Reaction.  The level is the
        # directional extreme from the previous Blue candle through that
        # Reaction breakout, not the following line's own source extreme.
        inherited = self._inherited_stop(previous, current)
        if inherited is not None:
            level, level_index, level_time, reaction_break_time = inherited
            crossing = self._first_crossing(
                level,
                current.formation_time,
                expires_at,
            )
            if crossing is None:
                return None
            trigger_index, trigger_event_time, _ = crossing
            return (
                level,
                level_index,
                level_time,
                trigger_index,
                getattr(self.candles[trigger_index], "timestamp"),
                trigger_event_time,
                level_time,
                getattr(self.candles[trigger_index], "timestamp"),
            )

        if previous.stop_event_time < current.formation_time:
            current_source_time = getattr(
                self.candles[current.formation_index], "timestamp"
            )
            level, level_index, level_time = self._range_extreme(
                previous.stop_event_time,
                current_source_time - timedelta(microseconds=1),
            )
            formation_candle_end = (
                getattr(self.candles[current.formation_index], "timestamp")
                + self.timeframe
            )
            formation_window_end = (
                min(formation_candle_end, expires_at)
                if expires_at is not None
                else formation_candle_end
            )
            formation_crossing = self._first_crossing(
                level,
                current.formation_time,
                formation_window_end,
            )
            if formation_crossing is not None:
                trigger_index, trigger_event_time, _ = formation_crossing
                effective_stop_time = getattr(
                    self.candles[trigger_index], "timestamp"
                )
                return (
                    level,
                    level_index,
                    level_time,
                    trigger_index,
                    effective_stop_time,
                    trigger_event_time,
                    previous.stop_time,
                    effective_stop_time,
                )

            if current.stop_event_time is None or current.stop_time is None:
                return None
            if (
                expires_at is not None
                and current.stop_event_time > expires_at
            ):
                return None
            search_start = current.stop_event_time
            crossing = self._first_crossing(level, search_start, expires_at)
            if crossing is None:
                return None
            trigger_index, trigger_event_time, _ = crossing
            return (
                level,
                level_index,
                level_time,
                trigger_index,
                getattr(self.candles[trigger_index], "timestamp"),
                trigger_event_time,
                previous.stop_time,
                current.stop_time,
            )

        if current.stop_event_time is None or current.stop_time is None:
            return None
        if (
            expires_at is not None
            and current.stop_event_time > expires_at
        ):
            return None
        first, second = sorted(
            (previous, current),
            key=lambda item: (
                item.stop_event_time,
                item.stop_level if self.direction == "bearish" else -item.stop_level,
            ),
        )
        assert first.stop_event_time is not None
        assert second.stop_event_time is not None
        assert first.stop_event_extreme is not None
        assert second.stop_event_extreme is not None
        first_index = int(first.stop_index)
        level = first.stop_event_extreme
        level_time = getattr(self.candles[first_index], "timestamp")

        if first.stop_event_time == second.stop_event_time:
            trigger_index = int(second.stop_index)
            return (
                level,
                first_index,
                level_time,
                trigger_index,
                getattr(self.candles[trigger_index], "timestamp"),
                second.stop_event_time,
                previous.stop_time,
                current.stop_time,
            )

        crossing = self._first_crossing(level, second.stop_event_time, expires_at)
        if crossing is None:
            return None
        trigger_index, trigger_event_time, _ = crossing
        return (
            level,
            first_index,
            level_time,
            trigger_index,
            getattr(self.candles[trigger_index], "timestamp"),
            trigger_event_time,
            previous.stop_time,
            current.stop_time,
        )

    def _reaction_confirmation_time(self, reaction: object) -> datetime:
        return self.chronology.reaction_confirmation(
            self.direction, reaction, use_intrabar_start=False
        )

    def _first_reaction_after(
        self,
        trigger_event_time: datetime,
        *,
        not_before: datetime | None = None,
    ) -> tuple[int, object] | None:
        for number, reaction in enumerate(self.reactions, start=1):
            first_time = getattr(
                self.candles[int(getattr(reaction, "first_idx"))],
                "timestamp",
            )
            if (
                self._reaction_confirmation_time(reaction) >= trigger_event_time
                and (not_before is None or first_time >= not_before)
            ):
                return number, reaction
        return None

    def _inherited_stop(
        self,
        previous: BlueState,
        current: BlueState,
    ) -> tuple[Decimal, int, datetime, datetime] | None:
        if previous.formation_time >= current.formation_time:
            return None
        chained = (
            previous.stop_time is not None
            and previous.stop_event_time is not None
            and previous.stop_event_time < current.formation_time
            and not bool(getattr(previous.line, "behavior_internal", False))
            and not bool(getattr(current.line, "behavior_internal", False))
        )
        # A Scale Blue may not inherit a continuation stop from a Reaction
        # that completes before the following Blue while the Scale Blue itself
        # is still live. Its semantic sourceExtreme remains authoritative until
        # the Scale Blue actually strict-stops. Reset-Blue chaining keeps its
        # established pre-stop structural route. This rule is direction-neutral.
        if not chained and str(getattr(previous.line, "kind")) == "scale":
            return None
        window_start = previous.stop_time if chained else previous.formation_time
        for reaction in self.reactions:
            first_time = getattr(
                self.candles[int(getattr(reaction, "first_idx"))],
                "timestamp",
            )
            break_time = getattr(
                self.candles[int(getattr(reaction, "break_idx"))],
                "timestamp",
            )
            if first_time <= window_start:
                continue
            if break_time >= current.formation_time:
                continue
            # Exact directional mirror: once a prior Blue has strictly
            # stopped, its carried stop uses the directional extreme across
            # the complete stop-candle -> next same-direction Reaction
            # Breakout-candle interval. Bullish freezes the minimum Low;
            # Bearish freezes the maximum High. The complete Breakout main
            # candle is included for both directions.
            range_end = (
                break_time + self.timeframe - timedelta(microseconds=1)
                if chained
                else break_time
            )
            level, level_index, level_time = self._range_extreme(
                window_start,
                range_end,
            )
            return level, level_index, level_time, break_time
        return None

    def _a_source(
        self,
        trigger_index: int,
        reaction: object,
    ) -> tuple[int, datetime, Decimal] | None:
        """Return A ownership frozen at the exact confirming Reaction event.

        The Blue-pair trigger opens the candidate on its main candle.  The
        confirming Reaction validates that candidate, but later prices in the
        same Break candle already belong to subsequent chronology and may not
        retroactively move A.  Source/price are therefore selected from the
        trigger main-candle open through exact lower-timeframe confirmation,
        inclusive.
        """
        start = getattr(self.candles[trigger_index], "timestamp")
        end = self._reaction_confirmation_time(reaction)
        if end < start:
            return None
        value, source_index, source_time = self._range_extreme(start, end)
        return source_index, source_time, value

    def _detect_ordinary_a(self, states: list[BlueState]) -> list[AZone]:
        """Resolve the ordinary adjacent-Blue A lifecycle."""
        output: list[AZone] = []
        cycle_after_index = -1
        bridge_reuse_ordinal: int | None = None
        index = 0

        while index + 1 < len(states):
            previous = states[index]
            current = states[index + 1]
            bridge_pair = (
                bridge_reuse_ordinal is not None
                and previous.ordinal == bridge_reuse_ordinal
            )
            if (
                current.formation_index <= cycle_after_index
                or (
                    previous.formation_index <= cycle_after_index
                    and not bridge_pair
                )
            ):
                if bridge_pair:
                    bridge_reuse_ordinal = None
                index += 1
                continue

            expires_at = (
                states[index + 2].formation_time
                if index + 2 < len(states)
                else None
            )
            trigger = self._pair_trigger(previous, current, expires_at)
            if trigger is None:
                index += 1
                continue

            (
                continuation_level,
                continuation_source_index,
                continuation_source_time,
                trigger_index,
                trigger_time,
                trigger_event_time,
                blue_1_stop_time,
                blue_2_stop_time,
            ) = trigger
            match = self._first_reaction_after(
                trigger_event_time,
                not_before=max(blue_1_stop_time, blue_2_stop_time),
            )
            if match is None:
                break
            reaction_number, reaction = match
            source = self._a_source(trigger_index, reaction)
            if source is None:
                index += 1
                continue
            source_index, source_time, price = source
            break_index = int(getattr(reaction, "break_idx"))
            output.append(
                AZone(
                    direction=self.direction,
                    blue_1_ordinal=previous.ordinal,
                    blue_2_ordinal=current.ordinal,
                    blue_1_source_time=getattr(previous.line, "source_time"),
                    blue_2_source_time=getattr(current.line, "source_time"),
                    blue_1_stop_time=blue_1_stop_time,
                    blue_2_stop_time=blue_2_stop_time,
                    blue_1_stop_level=previous.stop_level,
                    blue_2_stop_level=current.stop_level,
                    continuation_level=continuation_level,
                    continuation_source_index=continuation_source_index,
                    continuation_source_time=continuation_source_time,
                    trigger_index=trigger_index,
                    trigger_time=trigger_time,
                    trigger_event_time=trigger_event_time,
                    reaction_number=reaction_number,
                    reaction_first_time=getattr(
                        self.candles[int(getattr(reaction, "first_idx"))],
                        "timestamp",
                    ),
                    reaction_break_time=getattr(
                        self.candles[break_index], "timestamp"
                    ),
                    source_index=source_index,
                    source_time=source_time,
                    price=price,
                    formation_route="ordinary",
                    blue_1_stop_event_time=(
                        previous.stop_event_time
                        if previous.stop_time == blue_1_stop_time
                        else None
                    ),
                    blue_2_stop_event_time=(
                        current.stop_event_time
                        if current.stop_time == blue_2_stop_time
                        else None
                    ),
                )
            )
            cycle_after_index = break_index

            confirmation_time = self._reaction_confirmation_time(reaction)
            first_stop = self._first_crossing(price, confirmation_time, None)
            allow_adjacent_reuse = (
                first_stop is not None
                and index + 2 < len(states)
                and states[index + 2].formation_time >= first_stop[1]
            )
            if allow_adjacent_reuse:
                bridge_reuse_ordinal = current.ordinal
                index += 1
            else:
                bridge_reuse_ordinal = None
                while (
                    index < len(states)
                    and states[index].formation_index <= cycle_after_index
                ):
                    index += 1
        return output

    def _filter_special_a(
        self,
        special: list[AZone],
        ordinary: list[AZone],
    ) -> tuple[list[AZone], list[AZone]]:
        """Resolve special double-stop A ownership against ordinary A state."""
        ordinary_reactions = {
            item.reaction_number
            for item in ordinary
            if item.reaction_number is not None
        }
        special = [
            item
            for item in special
            if item.reaction_number not in ordinary_reactions
        ]

        filtered_special: list[AZone] = []
        for item in special:
            prior_candidates = [
                prior
                for prior in ordinary
                if prior.source_time < item.source_time
            ]
            prior = max(
                prior_candidates,
                key=lambda zone: zone.source_time,
                default=None,
            )
            if prior is not None and self._a_was_stopped_before(
                prior,
                item.reaction_first_time,
                not_before=item.blue_1_source_time,
            ):
                continue
            filtered_special.append(item)
        special = filtered_special

        consumed_special = [
            (
                {
                    int(getattr(item, "blue_1_ordinal")),
                    int(getattr(item, "blue_2_ordinal")),
                },
                getattr(item, "trigger_event_time"),
            )
            for item in special
        ]
        if consumed_special:
            ordinary = [
                item
                for item in ordinary
                if not any(
                    getattr(item, "trigger_event_time") > trigger_event_time
                    and {
                        int(getattr(item, "blue_1_ordinal")),
                        int(getattr(item, "blue_2_ordinal")),
                    }
                    & consumed_ordinals
                    for consumed_ordinals, trigger_event_time in consumed_special
                )
            ]
        return ordinary, special

    def detect(self) -> list[AZone]:
        """Return ordinary and special A zones after one ownership resolution."""
        states = self._build_blue_states()
        ordinary = self._detect_ordinary_a(states)
        ordinary, special = self._filter_special_a(
            self._double_stop_a_candidates(), ordinary
        )
        return sorted(
            ordinary + special,
            key=lambda item: (item.source_time, item.trigger_event_time),
        )

    def _a_was_stopped_before(
        self,
        zone: AZone,
        end_time: datetime,
        *,
        not_before: datetime | None = None,
    ) -> bool:
        """Return whether A's *first* strict stop belongs to this lifecycle.

        A stop that happened before ``not_before`` completed the prior cycle.
        A later recross of the same price must not be mistaken for a new stop
        owned by the current Blue pair.
        """
        start = int(getattr(self.candles[zone.source_index], "index")) + 1
        if start >= len(self.candles):
            return False
        first_stop = self._first_crossing(
            zone.price,
            getattr(self.candles[start], "timestamp"),
            end_time,
        )
        if first_stop is None:
            return False
        return not_before is None or first_stop[1] >= not_before


def detect_a_zones(
    direction: str,
    reactions: Sequence[object],
    blue_lines: Sequence[object],
    chronology: object,
) -> list[AZone]:
    return AZoneDetector(direction, reactions, blue_lines, chronology).detect()
