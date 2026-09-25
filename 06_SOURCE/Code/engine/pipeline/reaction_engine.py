"""Authoritative Reaction geometry and shared market chronology.

Owns candle semantics, Bullish/Bearish Reaction and Reset detection, exact
lower-timeframe chronology, canonical Order-stop geometry, and
Internal-Reaction classification. It does not decide Blue/A/S/E/StopAll
visibility or lifecycle priority.
"""

from __future__ import annotations

import bisect
from array import array
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Iterable, Sequence

from direction_policy import policy_for


REACTION_ENGINE_VERSION = "9.8.0"
REACTION_ENGINE_LAST_MODIFIED = "2026-09-22 00:35:00 +03:30"

_SEQUENCE_TIME_INDEXES: dict[int, tuple[Sequence[Candle], list[datetime]]] = {}

@dataclass(frozen=True, slots=True)
class Candle:
    index: int
    timestamp: datetime
    display_time: str
    tag: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal


@dataclass(slots=True)
class Candidate:
    first_idx: int
    first_time: str
    box_top_source_idx: int
    box_top_source_time: str
    box_top: Decimal
    box_bottom_source_idx: int
    box_bottom_source_time: str
    box_bottom: Decimal
    mode: str
    anchor_idx: int | None = None
    anchor_value: Decimal | None = None
    leg_boundary_value: Decimal | None = None
    break_idx: int | None = None
    break_time: str | None = None
    intrabar_start: datetime | None = None
    cross_direction_origin: bool = False
    cross_direction_chain_owner: bool = False
    order_gate_decision: str | None = None
    behavior_public_number: int | None = None
    behavior_public_box_top: Decimal | None = None
    behavior_public_box_bottom: Decimal | None = None
    behavior_confirmation_time: datetime | None = None
    behavior_first_time: datetime | None = None
    behavior_internal: bool = False


@dataclass(frozen=True, slots=True)
class ResetEvent:
    index: int
    display_time: str
    second_time: str | None
    broken_level: Decimal
    from_first_idx: int


@dataclass(frozen=True, slots=True)
class IntrabarAnalysis:
    event_second: Candle
    extreme: Decimal
    extreme_source: Candle


@dataclass(frozen=True, slots=True)
class DetectionResult:
    direction: str
    reactions: list[Candidate]
    resets: list[ResetEvent]
    start_index: int
    end_index: int


def classify_candle_color(open_price: Decimal, close_price: Decimal) -> str:
    """Match Lightweight Charts: Open <= Close is an up/green candle."""
    return "GREEN" if open_price <= close_price else "RED"


def opposite_direction(direction: str) -> str:
    """Return the exact Bullish/Bearish mirror direction."""
    return policy_for(direction).opposite_direction


class DetectorBase:
    def __init__(
        self,
        candles: Sequence[Candle],
        one_second_candles: Sequence[Candle],
        start_index: int,
        end_index: int,
    ) -> None:
        self.candles = candles
        self.seconds = one_second_candles
        self.start_index = start_index
        self.end_index = end_index
        self.main_times = self._shared_time_index(candles)
        self.second_times = self._shared_time_index(one_second_candles)
        self.lower_index = shared_lower_timeframe_index(one_second_candles)
        self._reaction_break_index_cache: dict[str, tuple[int, list[int]]] = {}

        if len(candles) > 1:
            self.timeframe = candles[1].timestamp - candles[0].timestamp
        else:
            self.timeframe = timedelta(seconds=1)

        if self.timeframe.total_seconds() <= 0:
            raise ValueError("Main timeframe must be positive.")

    @staticmethod
    def _shared_time_index(candles: Sequence[Candle]) -> list[datetime]:
        """Build one immutable-source timestamp index per calculation process."""
        key = id(candles)
        cached = _SEQUENCE_TIME_INDEXES.get(key)
        if cached is not None and cached[0] is candles:
            return cached[1]
        times = [candle.timestamp for candle in candles]
        _SEQUENCE_TIME_INDEXES[key] = (candles, times)
        return times

    def seconds_between(self, start: datetime, end: datetime) -> Iterable[Candle]:
        left = bisect.bisect_left(self.second_times, start)
        right = bisect.bisect_left(self.second_times, end)
        return (self.seconds[index] for index in range(left, right))

    def main_source_for_time(self, timestamp: datetime) -> Candle | None:
        position = bisect.bisect_right(self.main_times, timestamp) - 1
        if position < self.start_index or position > self.end_index:
            return None
        end = (
            self.candles[position + 1].timestamp
            if position + 1 < len(self.candles)
            else self.candles[position].timestamp + self.timeframe
        )
        if timestamp < end:
            return self.candles[position]
        return None

    def minimum_low(self, start_index: int, end_index: int) -> tuple[Decimal, Candle]:
        source = self.candles[start_index]
        candles = self.candles
        for index in range(start_index + 1, end_index + 1):
            candle = candles[index]
            if candle.low < source.low:
                source = candle
        return source.low, source

    def maximum_high(self, start_index: int, end_index: int) -> tuple[Decimal, Candle]:
        source = self.candles[start_index]
        candles = self.candles
        for index in range(start_index + 1, end_index + 1):
            candle = candles[index]
            if candle.high > source.high:
                source = candle
        return source.high, source


class BullishDetector(DetectorBase):
    def green_run_peak_before(self, first_red_index: int) -> tuple[Decimal, Candle]:
        run_end = first_red_index - 1
        if run_end < self.start_index or self.candles[run_end].tag != "GREEN":
            raise ValueError("Mode-A FirstRed must immediately follow a GREEN candle.")

        run_start = run_end
        while run_start > self.start_index and self.candles[run_start - 1].tag == "GREEN":
            run_start -= 1
        return self.maximum_high(run_start, run_end)

    def breakout_analysis(
        self, candidate: Candidate, breakout_candle: Candle
    ) -> IntrabarAnalysis | None:
        start_index = (
            candidate.box_top_source_idx + 1
            if candidate.box_top_source_idx < candidate.first_idx
            else candidate.box_top_source_idx
        )
        start = candidate.intrabar_start or self.candles[start_index].timestamp
        end = breakout_candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, start)
        right = bisect.bisect_left(self.second_times, end)
        crossing = self.lower_index.first_greater(left, right, candidate.box_top)
        if crossing is None:
            return None
        minimum_low, minimum_position = self.lower_index.range_minimum(
            left, crossing + 1
        )
        minimum_time = self.second_times[minimum_position]
        source = self.main_source_for_time(minimum_time)
        if source is None:
            return None
        return IntrabarAnalysis(
            self.seconds[crossing], minimum_low, source
        )

    def mode_a_invalidation_before_breakout(
        self, candidate: Candidate, candle: Candle
    ) -> bool:
        # A Mode-A candidate belongs to the complete leg that opened at the
        # analysis/Reset boundary.  Later lower RED candles are internal
        # BoxBottom updates; only a strict break of the frozen leg floor can
        # invalidate the candidate before its BoxTop breaks.
        invalidation_level = (
            candidate.anchor_value
            if candidate.anchor_value is not None
            else candidate.leg_boundary_value
        )
        if invalidation_level is None:
            return False
        if candle.low >= invalidation_level:
            return False
        if candle.high <= candidate.box_top:
            return True

        end = candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, candle.timestamp)
        right = bisect.bisect_left(self.second_times, end)
        invalidation = self.lower_index.first_less(
            left, right, invalidation_level
        )
        breakout = self.lower_index.first_greater(
            left, right, candidate.box_top
        )
        if invalidation is None:
            return breakout is None
        if breakout is None:
            return True
        # The legacy loop checks Low first inside one lower-timeframe candle,
        # so invalidation wins a true same-second tie.
        return invalidation <= breakout

    def confirmed_reset_before_breakout(
        self, candidate: Candidate | None, candle: Candle, confirmed_bottom: Decimal
    ) -> bool:
        if candidate is None or candle.high <= candidate.box_top:
            return True

        end = candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, candle.timestamp)
        right = bisect.bisect_left(self.second_times, end)
        reset = self.lower_index.first_less(left, right, confirmed_bottom)
        breakout = self.lower_index.first_greater(
            left, right, candidate.box_top
        )
        if reset is None:
            return breakout is None
        if breakout is None:
            return True
        # Reset is checked before breakout within one lower-timeframe candle.
        return reset <= breakout

    def post_breakout_reset(
        self,
        analysis: IntrabarAnalysis | None,
        box_bottom: Decimal,
        breakout_candle: Candle,
    ) -> Candle | None:
        if analysis is None:
            return None
        start = analysis.event_second.timestamp + timedelta(microseconds=1)
        end = breakout_candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, start)
        right = bisect.bisect_left(self.second_times, end)
        position = self.lower_index.first_less(left, right, box_bottom)
        return None if position is None else self.seconds[position]

    def detect(self, *, first_only: bool = False) -> DetectionResult:
        reactions: list[Candidate] = []
        resets: list[ResetEvent] = []
        mode = "A"
        state = "SCANNING"
        last_confirmed_bottom: Decimal | None = None
        last_confirmed_first_idx: int | None = None
        running_peak: Decimal | None = None
        running_peak_src: int | None = None
        leg_open_low: Decimal | None = None
        leg_just_started = True
        anchor_red: Candle | None = None
        anchor_red_origin: str | None = None
        reset_context: Candle | None = None
        candidate: Candidate | None = None

        for index in range(self.start_index, self.end_index + 1):
            candle = self.candles[index]
            reset_detected = (
                last_confirmed_bottom is not None and candle.low < last_confirmed_bottom
            )
            reset_occurs_first = reset_detected
            if reset_detected and state == "WAITING":
                reset_occurs_first = self.confirmed_reset_before_breakout(
                    candidate, candle, last_confirmed_bottom
                )

            if reset_occurs_first:
                resets.append(
                    ResetEvent(
                        index=candle.index,
                        display_time=candle.display_time,
                        second_time=None,
                        broken_level=last_confirmed_bottom,
                        from_first_idx=last_confirmed_first_idx,
                    )
                )
                candidate = None
                last_confirmed_bottom = None
                last_confirmed_first_idx = None
                running_peak = None
                running_peak_src = None
                mode = "A"
                state = "SCANNING"
                leg_open_low = None
                leg_just_started = True
                anchor_red = candle if candle.tag == "RED" else None
                anchor_red_origin = "reset" if candle.tag == "RED" else None
                reset_context = candle
                continue

            if state == "WAITING":
                assert candidate is not None

                if (
                    candidate.mode == "A"
                    and self.mode_a_invalidation_before_breakout(candidate, candle)
                ):
                    candidate = None
                    state = "SCANNING"
                    anchor_red = candle if candle.tag == "RED" else None
                    anchor_red_origin = (
                        "candidate_invalidation" if candle.tag == "RED" else None
                    )
                    continue

                if candle.low < candidate.box_bottom:
                    candidate.box_bottom = candle.low
                    candidate.box_bottom_source_idx = candle.index
                    candidate.box_bottom_source_time = candle.display_time

                if candle.high > candidate.box_top:
                    candidate.break_idx = candle.index
                    candidate.break_time = candle.display_time
                    analysis = self.breakout_analysis(candidate, candle)

                    if (
                        candidate.box_bottom_source_idx == candle.index
                        and analysis is not None
                    ):
                        candidate.box_bottom = analysis.extreme
                        candidate.box_bottom_source_idx = analysis.extreme_source.index
                        candidate.box_bottom_source_time = (
                            analysis.extreme_source.display_time
                        )

                    confirmed = replace(candidate)
                    reactions.append(confirmed)
                    if first_only:
                        return DetectionResult(
                            direction="bullish",
                            reactions=reactions,
                            resets=resets,
                            start_index=self.start_index,
                            end_index=self.end_index,
                        )
                    last_confirmed_bottom = confirmed.box_bottom
                    last_confirmed_first_idx = confirmed.first_idx
                    running_peak = candle.high
                    running_peak_src = candle.index
                    mode = "B"
                    state = "SCANNING"
                    candidate = None

                    reset_second = self.post_breakout_reset(
                        analysis, last_confirmed_bottom, candle
                    )
                    if reset_second is not None:
                        resets.append(
                            ResetEvent(
                                index=candle.index,
                                display_time=candle.display_time,
                                second_time=reset_second.display_time,
                                broken_level=last_confirmed_bottom,
                                from_first_idx=last_confirmed_first_idx,
                            )
                        )
                        last_confirmed_bottom = None
                        last_confirmed_first_idx = None
                        running_peak = None
                        running_peak_src = None
                        mode = "A"
                        state = "SCANNING"
                        leg_open_low = None
                        leg_just_started = True
                        anchor_red = candle if candle.tag == "RED" else None
                        anchor_red_origin = "reset" if candle.tag == "RED" else None
                        reset_context = candle
                        continue

                    if candle.tag == "RED":
                        candidate = Candidate(
                            first_idx=candle.index,
                            first_time=candle.display_time,
                            box_top_source_idx=candle.index,
                            box_top_source_time=candle.display_time,
                            box_top=running_peak,
                            box_bottom_source_idx=candle.index,
                            box_bottom_source_time=candle.display_time,
                            box_bottom=candle.low,
                            mode="B",
                        )
                        state = "WAITING"
                continue

            if mode == "A":
                if leg_just_started:
                    leg_open_low = candle.low
                    leg_just_started = False
                    previous_reset = reset_context
                    reset_context = None
                    if candle.tag == "RED":
                        if (
                            previous_reset is not None
                            and previous_reset.tag == "GREEN"
                            and candle.low >= previous_reset.low
                        ):
                            green_high, green_source = self.green_run_peak_before(
                                candle.index
                            )
                            if green_high >= candle.high:
                                box_top = green_high
                                box_top_source = green_source
                            else:
                                box_top = candle.high
                                box_top_source = candle
                            candidate = Candidate(
                                first_idx=candle.index,
                                first_time=candle.display_time,
                                box_top_source_idx=box_top_source.index,
                                box_top_source_time=box_top_source.display_time,
                                box_top=box_top,
                                box_bottom_source_idx=candle.index,
                                box_bottom_source_time=candle.display_time,
                                box_bottom=candle.low,
                                mode="A",
                                leg_boundary_value=leg_open_low,
                            )
                            state = "WAITING"
                        else:
                            anchor_red = candle
                            anchor_red_origin = "leg_open"
                    continue

                previous = self.candles[index - 1]
                passes = False
                box_top: Decimal | None = None
                box_top_source: Candle | None = None

                if previous.tag == "GREEN" and candle.tag == "RED":
                    if (
                        anchor_red is not None
                        and anchor_red_origin == "candidate_invalidation"
                        and previous.low < anchor_red.low
                        and candle.low < anchor_red.low
                    ):
                        anchor_red = None
                        anchor_red_origin = None

                    if anchor_red is not None:
                        passes = candle.low >= anchor_red.low
                    elif candle.low >= previous.low or candle.low >= leg_open_low:
                        passes = True

                    if passes:
                        green_high, green_source = self.green_run_peak_before(candle.index)
                        if green_high >= candle.high:
                            box_top = green_high
                            box_top_source = green_source
                        else:
                            box_top = candle.high
                            box_top_source = candle

                if passes:
                    assert box_top is not None and box_top_source is not None
                    candidate = Candidate(
                        first_idx=candle.index,
                        first_time=candle.display_time,
                        box_top_source_idx=box_top_source.index,
                        box_top_source_time=box_top_source.display_time,
                        box_top=box_top,
                        box_bottom_source_idx=candle.index,
                        box_bottom_source_time=candle.display_time,
                        box_bottom=candle.low,
                        mode="A",
                        anchor_idx=anchor_red.index if anchor_red else None,
                        anchor_value=anchor_red.low if anchor_red else None,
                        leg_boundary_value=leg_open_low,
                    )
                    state = "WAITING"
                elif candle.tag == "RED":
                    anchor_red = candle
                    anchor_red_origin = "scan"
                elif candle.tag in {"DOJI", "NEUTRAL"}:
                    anchor_red = None
                    anchor_red_origin = None
            else:
                if candle.tag == "RED":
                    box_top = candle.high
                    box_top_source_idx = candle.index
                    if running_peak is not None and running_peak >= box_top:
                        box_top = running_peak
                        box_top_source_idx = running_peak_src

                    bottom_start = (
                        box_top_source_idx + 1
                        if box_top_source_idx < candle.index
                        else candle.index
                    )
                    bottom, bottom_source = self.minimum_low(bottom_start, candle.index)
                    candidate = Candidate(
                        first_idx=candle.index,
                        first_time=candle.display_time,
                        box_top_source_idx=box_top_source_idx,
                        box_top_source_time=self.candles[
                            box_top_source_idx
                        ].display_time,
                        box_top=box_top,
                        box_bottom_source_idx=bottom_source.index,
                        box_bottom_source_time=bottom_source.display_time,
                        box_bottom=bottom,
                        mode="B",
                    )
                    state = "WAITING"

                if running_peak is None or candle.high > running_peak:
                    running_peak = candle.high
                    running_peak_src = candle.index

        return DetectionResult(
            direction="bullish",
            reactions=reactions,
            resets=resets,
            start_index=self.start_index,
            end_index=self.end_index,
        )


def mirror_candle(candle: Candle) -> Candle:
    """Internal coordinate/role adapter; never reclassify a market candle here.

    Input dojis are GREEN in both market directions, matching the chart.
    Swapping that tag inside the Bullish reference makes its RED/FirstRed
    branch implement the original GREEN/FirstGreen Bearish branch. This is
    not permission to treat a market doji as RED or emit a changed chart color.
    """
    return Candle(
        index=candle.index,
        timestamp=candle.timestamp,
        display_time=candle.display_time,
        tag={"GREEN": "RED", "RED": "GREEN"}.get(candle.tag, candle.tag),
        open=candle.open.copy_negate(),
        high=candle.low.copy_negate(),
        low=candle.high.copy_negate(),
        close=candle.close.copy_negate(),
    )


def mirror_candidate(candidate: Candidate | None) -> Candidate | None:
    """Mirror geometry while preserving invariant dynamic gate state."""
    if candidate is None:
        return None
    mirrored = replace(
        candidate,
        box_top=candidate.box_bottom.copy_negate(),
        box_bottom=candidate.box_top.copy_negate(),
        box_top_source_idx=candidate.box_bottom_source_idx,
        box_top_source_time=candidate.box_bottom_source_time,
        box_bottom_source_idx=candidate.box_top_source_idx,
        box_bottom_source_time=candidate.box_top_source_time,
        anchor_value=(candidate.anchor_value.copy_negate()
                      if candidate.anchor_value is not None else None),
        leg_boundary_value=(candidate.leg_boundary_value.copy_negate()
                            if candidate.leg_boundary_value is not None else None),
    )
    return mirrored

def mirror_analysis(analysis: IntrabarAnalysis | None) -> IntrabarAnalysis | None:
    if analysis is None:
        return None
    return IntrabarAnalysis(
        mirror_candle(analysis.event_second), analysis.extreme.copy_negate(),
        mirror_candle(analysis.extreme_source),
    )


class _ReflectedCandles(Sequence[Candle]):
    """Read-only coordinate view with one-time mirror caching.

    Each source candle is mirrored at most once (on first access) and the
    result is cached, so repeated scans reuse the same object instead of
    allocating a fresh mirrored Candle on every access.
    """

    def __init__(self, source: Sequence[Candle]) -> None:
        self.source = source
        self._cache: list[Candle | None] = [None] * len(source)

    def __len__(self) -> int:
        return len(self.source)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self.source)))]
        cached = self._cache[index]
        if cached is None:
            cached = mirror_candle(self.source[index])
            self._cache[index] = cached
        return cached


_REFLECTED_VIEWS: dict[int, tuple[Sequence[Candle], _ReflectedCandles]] = {}


def _reflected_view(source: Sequence[Candle]) -> _ReflectedCandles:
    key = id(source)
    cached = _REFLECTED_VIEWS.get(key)
    if cached is not None and cached[0] is source:
        return cached[1]
    view = _ReflectedCandles(source)
    _REFLECTED_VIEWS[key] = (source, view)
    return view


class BearishDetector(DetectorBase):
    """Execute the Bullish reference state machine in reflected coordinates.

    This is a coordinate adapter, not a second rule implementation. Both the
    initial Leg-Start and opposite-anchor queries use the same reference rules.
    Exact Decimal sign copying avoids context rounding during reflection.
    """

    def __init__(self, candles, one_second_candles, start_index, end_index):
        super().__init__(candles, one_second_candles, start_index, end_index)
        self.reference = BullishDetector(
            candles, one_second_candles, start_index, end_index,
        )
        # Time indexes are invariant under price reflection. Construct them
        # from the original rows; lazily transform OHLC only when consumed.
        # _ReflectedCandles caches each mirrored candle so repeated scans do
        # not re-allocate, while construction stays cheap (important because
        # _append_reaction builds a fresh BearishDetector per reaction).
        self.reference.candles = _reflected_view(candles)
        self.reference.seconds = _reflected_view(one_second_candles)
        self.reference.lower_index = ReflectedLowerTimeframeIndex(self.lower_index)

    def red_run_bottom_before(self, first_green_index):
        value, source = self.reference.green_run_peak_before(first_green_index)
        return value.copy_negate(), mirror_candle(source)

    def breakdown_analysis(self, candidate, breakdown_candle):
        return mirror_analysis(self.reference.breakout_analysis(
            mirror_candidate(candidate), mirror_candle(breakdown_candle),
        ))

    def invalidation_high_break_before_breakdown(self, candidate, candle):
        return self.reference.mode_a_invalidation_before_breakout(
            mirror_candidate(candidate), mirror_candle(candle),
        )

    def confirmed_reset_before_breakdown(self, candidate, candle, confirmed_top):
        return self.reference.confirmed_reset_before_breakout(
            mirror_candidate(candidate), mirror_candle(candle),
            confirmed_top.copy_negate(),
        )

    def post_breakdown_reset(self, analysis, box_top, breakdown_candle):
        result = self.reference.post_breakout_reset(
            mirror_analysis(analysis), box_top.copy_negate(),
            mirror_candle(breakdown_candle),
        )
        return mirror_candle(result) if result is not None else None

    def detect(self, *, first_only: bool = False) -> DetectionResult:
        result = self.reference.detect(first_only=first_only)
        return DetectionResult(
            direction="bearish",
            reactions=[mirror_candidate(candidate) for candidate in result.reactions],
            resets=[replace(reset, broken_level=reset.broken_level.copy_negate())
                    for reset in result.resets],
            start_index=result.start_index, end_index=result.end_index,
        )


def published_reaction_candidate(
    direction: str,
    candidate: Candidate,
    chronology: object,
) -> Candidate:
    """Return a presentation clone with Break-candle geometry frozen at confirmation.

    Detection/lifecycle ownership is intentionally not mutated here.  The public
    Reaction box must not include an opposite-edge extreme that happened later
    inside the same main Break candle after the Reaction had already confirmed.

    Main candles strictly before Break are fully eligible.  Only when the
    full-main-candle opposite extreme is owned by Break do we use one-second
    chronology to keep prices up to and including the first strict confirmation:

      Bullish -> published BoxBottom is the minimum eligible Low before the
                 first strict High > BoxTop breakout.
      Bearish -> published BoxTop is the maximum eligible High before the
                 first strict Low < BoxBottom breakdown.

    Equal extremes retain the earliest main-candle owner.  If lower-timeframe
    data cannot resolve the strict confirmation, preserve the detector geometry
    rather than guessing an intrabar order.
    """
    candles = chronology.candles
    one_second_candles = chronology.seconds
    published = replace(candidate)
    if candidate.break_idx is None:
        return published

    first_index = int(candidate.first_idx)
    break_index = int(candidate.break_idx)
    if first_index < 0 or break_index < first_index or break_index >= len(candles):
        return published

    break_candle = candles[break_index]
    timeframe = chronology.timeframe

    if direction == "bullish":
        # No Break-candle ownership -> the published full-range minimum was
        # already made before confirmation and is therefore chronology-safe.
        if int(candidate.box_bottom_source_idx) != break_index:
            return published
        value = candles[first_index].low
        source = candles[first_index]
        for index in range(first_index + 1, break_index):
            candle = candles[index]
            if candle.low < value:
                value, source = candle.low, candle
        threshold = candidate.box_top
    elif direction == "bearish":
        if int(candidate.box_top_source_idx) != break_index:
            return published
        value = candles[first_index].high
        source = candles[first_index]
        for index in range(first_index + 1, break_index):
            candle = candles[index]
            if candle.high > value:
                value, source = candle.high, candle
        threshold = candidate.box_bottom
    else:
        raise ValueError(f"Unsupported reaction direction: {direction}")

    lo, hi = chronology.lower_bounds(
        break_candle.timestamp, break_candle.timestamp + timeframe
    )
    confirmed = False

    for second in one_second_candles[lo:hi]:
        if direction == "bullish":
            if second.low < value:
                value = second.low
                source = break_candle
            if second.high > threshold:
                confirmed = True
                break
        else:
            if second.high > value:
                value = second.high
                source = break_candle
            if second.low < threshold:
                confirmed = True
                break

    if not confirmed:
        return published

    if direction == "bullish":
        published.box_bottom = value
        published.box_bottom_source_idx = source.index
        published.box_bottom_source_time = source.display_time
    else:
        published.box_top = value
        published.box_top_source_idx = source.index
        published.box_top_source_time = source.display_time
    return published


def _decimal_value(value: object) -> Decimal:
    """Normalize external numeric values without binary-float arithmetic."""
    return value if isinstance(value, Decimal) else Decimal(str(value))


class LowerTimeframeIndex:
    """Immutable segment index for exact first strict High/Low crossings.

    The index is direction-agnostic and shared by A/S/E so heavy 1-second
    inputs are not rescanned for every stop/trigger lookup.
    """

    def __init__(self, candles: Sequence[Candle]) -> None:
        self.candles = candles
        self.times = [getattr(item, "timestamp") for item in candles]
        size = 1
        while size < len(candles):
            size <<= 1
        self.size = size
        self.length = len(candles)
        self.minimum: list[Decimal | None] = [None] * (2 * size)
        self.maximum: list[Decimal | None] = [None] * (2 * size)
        self.minimum_position = array("i", [-1]) * (2 * size)
        self.maximum_position = array("i", [-1]) * (2 * size)
        for position, candle in enumerate(candles):
            node = size + position
            self.minimum[node] = _decimal_value(getattr(candle, "low"))
            self.maximum[node] = _decimal_value(getattr(candle, "high"))
            self.minimum_position[node] = position
            self.maximum_position[node] = position
        for node in range(size - 1, 0, -1):
            left, right = node * 2, node * 2 + 1
            low_left, low_right = self.minimum[left], self.minimum[right]
            high_left, high_right = self.maximum[left], self.maximum[right]
            if low_left is None:
                self.minimum[node] = low_right
                self.minimum_position[node] = self.minimum_position[right]
            elif low_right is None or low_left <= low_right:
                self.minimum[node] = low_left
                self.minimum_position[node] = self.minimum_position[left]
            else:
                self.minimum[node] = low_right
                self.minimum_position[node] = self.minimum_position[right]
            if high_left is None:
                self.maximum[node] = high_right
                self.maximum_position[node] = self.maximum_position[right]
            elif high_right is None or high_left >= high_right:
                self.maximum[node] = high_left
                self.maximum_position[node] = self.maximum_position[left]
            else:
                self.maximum[node] = high_right
                self.maximum_position[node] = self.maximum_position[right]

    def first_less(self, left: int, right: int, level: Decimal) -> int | None:
        return self._first(1, 0, self.size, left, right, level, True)

    def first_greater(self, left: int, right: int, level: Decimal) -> int | None:
        return self._first(1, 0, self.size, left, right, level, False)

    def range_minimum(self, left: int, right: int) -> tuple[Decimal, int]:
        """Return the minimum Low and earliest owning position in [left, right)."""
        return self._range_query(left, right, minimum=True)

    def range_maximum(self, left: int, right: int) -> tuple[Decimal, int]:
        """Return the maximum High and earliest owning position in [left, right)."""
        return self._range_query(left, right, minimum=False)

    def _range_query(
        self, left: int, right: int, *, minimum: bool
    ) -> tuple[Decimal, int]:
        if left < 0 or right > self.length or left >= right:
            raise ValueError("Range contains no lower-timeframe candles.")
        values = self.minimum if minimum else self.maximum
        positions = self.minimum_position if minimum else self.maximum_position
        left += self.size
        right += self.size
        best_value: Decimal | None = None
        best_position = -1
        while left < right:
            if left & 1:
                value = values[left]
                position = positions[left]
                if value is not None and (
                    best_value is None
                    or (value < best_value if minimum else value > best_value)
                    or (value == best_value and position < best_position)
                ):
                    best_value, best_position = value, position
                left += 1
            if right & 1:
                right -= 1
                value = values[right]
                position = positions[right]
                if value is not None and (
                    best_value is None
                    or (value < best_value if minimum else value > best_value)
                    or (value == best_value and position < best_position)
                ):
                    best_value, best_position = value, position
            left >>= 1
            right >>= 1
        if best_value is None or best_position < 0:
            raise ValueError("Range contains no lower-timeframe candles.")
        return best_value, best_position

    def _first(
        self, node: int, start: int, end: int, left: int, right: int,
        level: Decimal, less: bool,
    ) -> int | None:
        if end <= left or right <= start or start >= self.length:
            return None
        extreme = self.minimum[node] if less else self.maximum[node]
        if extreme is None or (extreme >= level if less else extreme <= level):
            return None
        if end - start == 1:
            return start
        middle = (start + end) // 2
        found = self._first(node * 2, start, middle, left, right, level, less)
        if found is not None:
            return found
        return self._first(
            node * 2 + 1, middle, end, left, right, level, less
        )


_LOWER_TIMEFRAME_INDEXES: dict[
    int, tuple[Sequence[Candle], LowerTimeframeIndex]
] = {}


def shared_lower_timeframe_index(
    candles: Sequence[Candle],
) -> LowerTimeframeIndex:
    """Reuse one immutable lower-timeframe index per source sequence."""
    key = id(candles)
    cached = _LOWER_TIMEFRAME_INDEXES.get(key)
    if cached is not None and cached[0] is candles:
        return cached[1]
    index = LowerTimeframeIndex(candles)
    _LOWER_TIMEFRAME_INDEXES[key] = (candles, index)
    return index


class ReflectedLowerTimeframeIndex:
    """Price-reflected view over a lower-timeframe index without rebuilding it."""

    __slots__ = ("base", "times")

    def __init__(self, base: LowerTimeframeIndex) -> None:
        self.base = base
        self.times = base.times

    def first_less(self, left: int, right: int, level: Decimal) -> int | None:
        return self.base.first_greater(left, right, level.copy_negate())

    def first_greater(self, left: int, right: int, level: Decimal) -> int | None:
        return self.base.first_less(left, right, level.copy_negate())

    def range_minimum(self, left: int, right: int) -> tuple[Decimal, int]:
        value, position = self.base.range_maximum(left, right)
        return value.copy_negate(), position

    def range_maximum(self, left: int, right: int) -> tuple[Decimal, int]:
        value, position = self.base.range_minimum(left, right)
        return value.copy_negate(), position


class MarketChronology:
    """Shared immutable market-time services for downstream behavior engines.

    Reaction owns chronology semantics.  A/S/E receive this object rather than
    rebuilding timestamp indexes, lower-timeframe windows, confirmation scans,
    and Reset timestamp parsing independently.
    """

    __slots__ = (
        "candles",
        "seconds",
        "times",
        "second_times",
        "timeframe",
        "lower_index",
        "_confirmation_cache",
        "_reset_time_cache",
    )

    def __init__(
        self,
        candles: Sequence[Candle],
        seconds: Sequence[Candle],
        timeframe_seconds: int,
        lower_index: LowerTimeframeIndex | None = None,
    ) -> None:
        if timeframe_seconds < 1:
            raise ValueError("Timeframe must be at least one second.")
        self.candles = candles
        self.seconds = seconds
        self.times = [getattr(item, "timestamp") for item in candles]
        self.second_times = (
            lower_index.times
            if lower_index is not None
            else [getattr(item, "timestamp") for item in seconds]
        )
        self.timeframe = timedelta(seconds=timeframe_seconds)
        self.lower_index = lower_index or shared_lower_timeframe_index(seconds)
        self._confirmation_cache: dict[tuple[object, ...], datetime] = {}
        self._reset_time_cache: dict[tuple[object, ...], datetime] = {}

    @staticmethod
    def opposite_direction(direction: str) -> str:
        """Expose the shared mirror-direction contract to downstream engines."""
        return opposite_direction(direction)

    def main_index(self, timestamp: datetime, *, clamp: bool = False) -> int:
        """Map an exact lower-timeframe timestamp to its owning main candle."""
        index = bisect.bisect_right(self.times, timestamp) - 1
        if index < 0:
            if clamp:
                return 0
            raise ValueError("Lower-timeframe event precedes the main candles.")
        return index

    def lower_bounds(
        self, start: datetime, end: datetime | None = None
    ) -> tuple[int, int]:
        left = bisect.bisect_left(self.second_times, start)
        right = (
            len(self.seconds)
            if end is None
            else bisect.bisect_left(self.second_times, end)
        )
        return left, right

    def lower_window(
        self, start: datetime, end: datetime | None = None
    ) -> Sequence[Candle]:
        left, right = self.lower_bounds(start, end)
        return self.seconds[left:right]

    @staticmethod
    def _reset_cache_key(reset: object) -> tuple[object, ...]:
        """Return a stable Reset identity suitable for chronology caches."""
        return (
            int(getattr(reset, "index", -1)),
            int(getattr(reset, "from_first_idx", -1)),
            getattr(reset, "second_time", None),
            getattr(reset, "display_time", None),
            getattr(reset, "timestamp", None),
            str(getattr(reset, "broken_level", "")),
        )

    @staticmethod
    def _reaction_cache_key(
        reaction: object, direction: str, use_intrabar_start: bool
    ) -> tuple[object, ...]:
        """Return a stable physical/geometry identity for confirmation caches."""
        return (
            direction,
            bool(use_intrabar_start),
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
            str(getattr(reaction, "box_top")),
            str(getattr(reaction, "box_bottom")),
            getattr(reaction, "intrabar_start", None) if use_intrabar_start else None,
        )

    def reset_time(self, reset: object) -> datetime:
        """Return the exact Reset event time, preserving legacy provenance."""
        cache_key = self._reset_cache_key(reset)
        cached = self._reset_time_cache.get(cache_key)
        if cached is not None:
            return cached
        second = getattr(reset, "second_time", None)
        if second:
            result = datetime.strptime(second, "%Y-%m-%d %H:%M:%S")
        else:
            display = getattr(reset, "display_time", None)
            result = (
                datetime.strptime(display, "%Y-%m-%d %H:%M:%S")
                if display
                else getattr(reset, "timestamp")
            )
        self._reset_time_cache[cache_key] = result
        return result

    def reaction_confirmation(
        self,
        direction: str,
        reaction: object,
        *,
        use_intrabar_start: bool = True,
    ) -> datetime:
        """Return the first strict lower-timeframe Reaction confirmation.

        ``use_intrabar_start=False`` preserves the established A-engine
        chronology contract, which starts its scan at the Break candle open.
        S/E and public Reaction chronology use the exact intrabar start when
        present.
        """
        cache_key = self._reaction_cache_key(
            reaction, direction, use_intrabar_start
        )
        cached = self._confirmation_cache.get(cache_key)
        if cached is not None:
            return cached
        break_index = int(getattr(reaction, "break_idx"))
        break_candle = self.candles[break_index]
        candle_start = getattr(break_candle, "timestamp")
        start = (
            getattr(reaction, "intrabar_start", None) or candle_start
            if use_intrabar_start
            else candle_start
        )
        candle_end = candle_start + self.timeframe
        if start < candle_start or start >= candle_end:
            start = candle_start
        level = _decimal_value(
            getattr(reaction, "box_top" if direction == "bullish" else "box_bottom")
        )
        left, right = self.lower_bounds(start, candle_end)
        field = "high" if direction == "bullish" else "low"
        for position in range(left, right):
            item = self.seconds[position]
            value = _decimal_value(getattr(item, field))
            confirms = value > level if direction == "bullish" else value < level
            if confirms:
                result = getattr(item, "timestamp")
                self._confirmation_cache[cache_key] = result
                return result
        self._confirmation_cache[cache_key] = candle_start
        return candle_start


    def canonical_order_stop(
        self,
        order_direction: str,
        reaction_number: int,
        reaction: object,
        opposite_reactions: Sequence[object],
        *,
        start_index: int = 0,
    ) -> tuple[Decimal, int, datetime]:
        """Return canonical opposite-Order stop provenance for S and E.

        Mode A owns the true leg head/floor from its anchor/context through
        Break inclusive. Mode B inherits the previous healthy opposite
        Reaction's semantic outer box edge. This is the single authoritative
        implementation used by every downstream behavior family.
        """
        if str(getattr(reaction, "mode")) == "A":
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            anchor_index = getattr(reaction, "anchor_idx", None)
            scan_start = (
                max(start_index, int(anchor_index))
                if anchor_index is not None
                else max(start_index, first_index - 1)
            )
            context_tag = "GREEN" if order_direction == "bearish" else "RED"
            while (
                scan_start > start_index
                and getattr(self.candles[scan_start - 1], "tag") == context_tag
            ):
                scan_start -= 1

            attribute = "high" if order_direction == "bearish" else "low"
            source_index = scan_start
            level = _decimal_value(getattr(self.candles[source_index], attribute))
            for candle in self.candles[scan_start + 1 : break_index + 1]:
                candidate = _decimal_value(getattr(candle, attribute))
                better = (
                    candidate > level
                    if order_direction == "bearish"
                    else candidate < level
                )
                if better:
                    source_index = int(getattr(candle, "index"))
                    level = candidate
            return level, source_index, getattr(self.candles[source_index], "timestamp")

        if reaction_number <= 1:
            raise ValueError("Mode-B order reaction has no previous healthy reaction.")
        previous = opposite_reactions[reaction_number - 2]
        if order_direction == "bearish":
            source_index = int(getattr(previous, "box_top_source_idx"))
            return (
                _decimal_value(getattr(previous, "box_top")),
                source_index,
                getattr(self.candles[source_index], "timestamp"),
            )
        source_index = int(getattr(previous, "box_bottom_source_idx"))
        return (
            _decimal_value(getattr(previous, "box_bottom")),
            source_index,
            getattr(self.candles[source_index], "timestamp"),
        )


def build_behavior_reaction_views(
    full_results: dict[str, object],
    chronology: MarketChronology,
):
    """Mark true cross-direction Reaction interiors for downstream behavior."""
    candles = chronology.candles
    seconds = chronology.seconds
    second_times = chronology.second_times
    public: dict[str, list[Candidate]] = {}
    confirmation: dict[str, list[datetime]] = {}
    for direction in ("bullish", "bearish"):
        public[direction] = [
            published_reaction_candidate(direction, item, chronology)
            for item in full_results[direction].reactions
        ]
        confirmation[direction] = [
            chronology.reaction_confirmation(direction, item)
            for item in full_results[direction].reactions
        ]

    def path_is_contained(
        first_time: datetime,
        confirmed_at: datetime,
        bottom: Decimal,
        top: Decimal,
    ) -> bool:
        left = bisect.bisect_left(second_times, first_time)
        right = bisect.bisect_right(second_times, confirmed_at)
        if left >= right:
            return False
        # Algorithm requirement: every physical lower-timeframe candle must
        # remain inside [bottom, top].  The immutable lower-timeframe range
        # index proves the exact same predicate via min(Low) and max(High),
        # without allocating/scanning the full slice for every Reaction pair.
        minimum_low, _ = chronology.lower_index.range_minimum(left, right)
        if minimum_low < bottom:
            return False
        maximum_high, _ = chronology.lower_index.range_maximum(left, right)
        return maximum_high <= top

    blocked: dict[str, set[tuple[int, int]]] = {
        "bullish": set(),
        "bearish": set(),
    }
    for direction in ("bullish", "bearish"):
        opposite = opposite_direction(direction)
        for number, reaction in enumerate(full_results[direction].reactions, start=1):
            reaction.behavior_public_number = number
            published = public[direction][number - 1]
            reaction.behavior_public_box_top = _decimal_value(published.box_top)
            reaction.behavior_public_box_bottom = _decimal_value(published.box_bottom)
            reaction.behavior_confirmation_time = confirmation[direction][number - 1]
            reaction.behavior_first_time = candles[int(getattr(reaction, "first_idx"))].timestamp

        for reaction, published, confirmed_at in zip(
            full_results[direction].reactions,
            public[direction],
            confirmation[direction],
        ):
            inner_first = candles[int(getattr(reaction, "first_idx"))].timestamp
            inner_top = _decimal_value(published.box_top)
            inner_bottom = _decimal_value(published.box_bottom)
            for outer, outer_published, outer_confirmed_at in zip(
                full_results[opposite].reactions,
                public[opposite],
                confirmation[opposite],
            ):
                outer_first = candles[int(getattr(outer, "first_idx"))].timestamp
                if inner_first <= outer_first or confirmed_at > outer_confirmed_at:
                    continue
                outer_top = _decimal_value(outer_published.box_top)
                outer_bottom = _decimal_value(outer_published.box_bottom)
                if (
                    inner_top <= outer_top
                    and inner_bottom >= outer_bottom
                    and path_is_contained(
                        inner_first,
                        confirmed_at,
                        outer_bottom,
                        outer_top,
                    )
                ):
                    blocked[direction].add(
                        (
                            int(getattr(reaction, "first_idx")),
                            int(getattr(reaction, "break_idx")),
                        )
                    )
                    break

    behavior_results = {}
    number_maps = {}
    blocked_first_times = {"bullish": set(), "bearish": set()}
    for direction in ("bullish", "bearish"):
        full = full_results[direction]
        for item in full.reactions:
            identity = (
                int(getattr(item, "first_idx")),
                int(getattr(item, "break_idx")),
            )
            item.behavior_internal = identity in blocked[direction]
        behavior_results[direction] = full
        number_maps[direction] = {
            number: number for number, _item in enumerate(full.reactions, start=1)
        }
        blocked_first_times[direction] = {
            candles[first_idx].timestamp for first_idx, _ in blocked[direction]
        }
    return behavior_results, number_maps, blocked, blocked_first_times


def directional_a_stop_order_finder(
    candles: Sequence[Candle],
    seconds: Sequence[Candle],
    direction: str,
):
    """Build the cached bounded opposite-Reaction resolver used after A stop."""
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    order_direction = opposite_direction(direction)
    first_tag = "GREEN" if order_direction == "bearish" else "RED"
    context_tag = "RED" if order_direction == "bearish" else "GREEN"
    cache: dict[tuple[int, int], Candidate | None] = {}
    detection_cache: dict[tuple[int, int], tuple[Candidate, ...]] = {}

    def find(gate_index: int, gate_event: datetime, end_index: int):
        key = (gate_index, end_index)
        if key in cache:
            return cache[key]
        first = next(
            (
                index
                for index in range(max(1, gate_index), end_index + 1)
                if candles[index].tag == first_tag
                and candles[index - 1].tag == context_tag
            ),
            None,
        )
        if first is None:
            cache[key] = None
            return None
        context = first - 1
        while context > 0 and candles[context - 1].tag == context_tag:
            context -= 1
        detection_key = (context, end_index)
        reactions = detection_cache.get(detection_key, ())
        order = next(
            (
                reaction
                for reaction in reactions
                if int(getattr(reaction, "first_idx")) >= gate_index
            ),
            None,
        )
        if order is None:
            result = UnifiedReactionDetector(
                candles, seconds, context, end_index, order_direction
            ).detect(stop_after_first_at_or_after=gate_index)
            reactions = tuple(result.reactions)
            detection_cache[detection_key] = reactions
            order = next(
                (
                    reaction
                    for reaction in reactions
                    if int(getattr(reaction, "first_idx")) >= gate_index
                ),
                None,
            )
        cache[key] = order
        return order

    return find


class UnifiedReactionDetector(DetectorBase):
    """Unified v9 directional post-Reset engine.

    The proven directional detectors supply only the initial Leg-Start. After
    that first confirmation this class owns Normal search and directional
    post-Reset continuation.  A Reset always searches for the first healthy
    reaction in the same direction as the requested/output leg; patterns in
    the opposite direction never gate or unlock that search.
    """

    def __init__(
        self,
        candles: Sequence[Candle],
        one_second_candles: Sequence[Candle],
        start_index: int,
        end_index: int,
        output_direction: str,
    ) -> None:
        super().__init__(candles, one_second_candles, start_index, end_index)
        self.output_direction = output_direction
        # Directional helpers are created lazily: a bullish-only run must not
        # pay the BearishDetector mirroring cost and vice versa.
        self._bull: BullishDetector | None = None
        self._bear: BearishDetector | None = None
        self.all_reactions: dict[str, list[Candidate]] = {
            "bullish": [],
            "bearish": [],
        }
        self.all_resets: dict[str, list[ResetEvent]] = {
            "bullish": [],
            "bearish": [],
        }
        self._geometry_after_reset_cache: dict[tuple, Candidate | None] = {}

    @property
    def bull(self) -> BullishDetector:
        if self._bull is None:
            self._bull = BullishDetector(
                self.candles, self.seconds, self.start_index, self.end_index
            )
        return self._bull

    @property
    def bear(self) -> BearishDetector:
        if self._bear is None:
            self._bear = BearishDetector(
                self.candles, self.seconds, self.start_index, self.end_index
            )
        return self._bear

    def _append_reaction(self, direction: str, candidate: Candidate) -> bool:
        # A confirmed adjacent opposite-direction Anchor may extend the outer
        # boundary, but it must never shrink the candidate's own box.
        opposite_anchor_is_confirmed = False
        if (
            candidate.break_idx is not None
            and candidate.anchor_idx is not None
            and candidate.anchor_idx + 1 == candidate.first_idx
            and self.all_resets[direction]
        ):
            reset_index = self.all_resets[direction][-1].index
            opposite_detector = (
                BullishDetector if direction == "bearish" else BearishDetector
            )(
                self.candles,
                self.seconds,
                reset_index,
                candidate.first_idx,
            )
            opposite_anchor_is_confirmed = any(
                reaction.break_idx == candidate.anchor_idx
                for reaction in opposite_detector.detect().reactions
            )

        if opposite_anchor_is_confirmed:
            anchor = self.candles[candidate.anchor_idx]
            first = self.candles[candidate.first_idx]
            if direction == "bearish":
                # A RED Leg-Start with a higher ceiling than FirstGreen owns
                # the leg boundary; FirstGreen must keep its own BoxBottom.
                if anchor.high <= first.high:
                    candidate.box_bottom = anchor.low
                    candidate.box_bottom_source_idx = anchor.index
                    candidate.box_bottom_source_time = anchor.display_time
            else:
                # Exact mirror: a GREEN Leg-Start whose floor is below
                # FirstRed owns the leg boundary; FirstRed keeps its BoxTop.
                if anchor.low >= first.low:
                    candidate.box_top = anchor.high
                    candidate.box_top_source_idx = anchor.index
                    candidate.box_top_source_time = anchor.display_time

        # Canonical confirmed-Reaction box ownership.  The directional
        # confirmation edge keeps the structure that discovered the Reaction:
        #   Bullish  -> BoxTop is the breakout edge.
        #   Bearish  -> BoxBottom is the breakdown edge.
        # The opposite edge belongs to First..exact-confirmation chronology.
        # Full main candles strictly before Break are eligible in full.  When
        # the Break candle itself owns the full-range opposite extreme, only
        # lower-timeframe prices up to and including the first strict
        # confirmation event may contribute.  Post-confirmation remainder
        # prices can never retroactively rewrite the Reaction/Order box.
        if candidate.break_idx is not None:
            first_index = int(candidate.first_idx)
            break_index = int(candidate.break_idx)
            break_candle = self.candles[break_index]
            if direction == "bullish":
                bottom, bottom_source = self.minimum_low(first_index, break_index)
                candidate.box_bottom = bottom
                candidate.box_bottom_source_idx = bottom_source.index
                candidate.box_bottom_source_time = bottom_source.display_time
                if bottom_source.index == break_index:
                    analysis = self.bull.breakout_analysis(candidate, break_candle)
                    if analysis is not None:
                        candidate.box_bottom = analysis.extreme
                        candidate.box_bottom_source_idx = analysis.extreme_source.index
                        candidate.box_bottom_source_time = analysis.extreme_source.display_time
            else:
                top, top_source = self.maximum_high(first_index, break_index)
                candidate.box_top = top
                candidate.box_top_source_idx = top_source.index
                candidate.box_top_source_time = top_source.display_time
                if top_source.index == break_index:
                    analysis = self.bear.breakdown_analysis(candidate, break_candle)
                    if analysis is not None:
                        candidate.box_top = analysis.extreme
                        candidate.box_top_source_idx = analysis.extreme_source.index
                        candidate.box_top_source_time = analysis.extreme_source.display_time

        self.all_reactions[direction].append(replace(candidate))
        return True

    def _append_reset(
        self,
        direction: str,
        candle: Candle,
        level: Decimal,
        first_idx: int,
        second_time: str | None = None,
    ) -> None:
        self.all_resets[direction].append(
            ResetEvent(
                index=candle.index,
                display_time=candle.display_time,
                second_time=second_time,
                broken_level=level,
                from_first_idx=first_idx,
            )
        )

    def _refine(
        self, direction: str, candidate: Candidate, candle: Candle
    ) -> IntrabarAnalysis | None:
        helper = self.bull if direction == "bullish" else self.bear
        analysis = (
            helper.breakout_analysis(candidate, candle)
            if direction == "bullish"
            else helper.breakdown_analysis(candidate, candle)
        )
        if analysis is None:
            return None
        if direction == "bullish" and candidate.box_bottom_source_idx == candle.index:
            candidate.box_bottom = analysis.extreme
            candidate.box_bottom_source_idx = analysis.extreme_source.index
            candidate.box_bottom_source_time = analysis.extreme_source.display_time
        if direction == "bearish" and candidate.box_top_source_idx == candle.index:
            candidate.box_top = analysis.extreme
            candidate.box_top_source_idx = analysis.extreme_source.index
            candidate.box_top_source_time = analysis.extreme_source.display_time
        return analysis

    def _candidate_from_confirmation_remainder(
        self,
        direction: str,
        confirmed: Candidate,
        candle: Candle,
        analysis: IntrabarAnalysis | None,
    ) -> Candidate | None:
        """Reuse a correctly colored confirmation candle for the next reaction."""
        required_tag = "RED" if direction == "bullish" else "GREEN"
        if candle.tag != required_tag or analysis is None:
            return None

        # The exact confirmation event splits the Break candle into two
        # ownership phases.  If its remainder strictly breaks the confirmed
        # opposite edge, that main candle belongs to Reset and cannot also be
        # reused as the First of the next Normal reaction.  ``analysis.extreme``
        # is the exact-confirmation opposite edge for both directions.
        remainder_start = analysis.event_second.timestamp + timedelta(microseconds=1)
        remainder_end = candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, remainder_start)
        right = bisect.bisect_left(self.second_times, remainder_end)
        if direction == "bullish":
            if self.lower_index.first_less(left, right, analysis.extreme) is not None:
                return None
        else:
            if self.lower_index.first_greater(left, right, analysis.extreme) is not None:
                return None
        # A cross-direction Leg-Start confirmation candle may simultaneously
        # become the first candle of the next same-direction reaction. Its
        # decisive second belongs to the new box boundary, so no second,
        # still-more-extreme tick is required. Other confirmations retain the
        # ordinary fresh post-event boundary requirement.
        # Every confirmation opens Normal Search. If its main candle has the
        # required start color, that complete candle is the next First candle,
        # regardless of whether the confirmed reaction was Mode A or Mode B.
        whole_confirmation_candle = True
        remainder_start = (
            candle.timestamp
            if whole_confirmation_candle
            else analysis.event_second.timestamp + timedelta(microseconds=1)
        )
        remainder_end = candle.timestamp + self.timeframe
        seconds = list(self.seconds_between(remainder_start, remainder_end))
        if not seconds:
            return None
        if direction == "bullish":
            top_second = max(seconds, key=lambda item: (item.high, -item.timestamp.timestamp()))
            bottom_second = min(seconds, key=lambda item: (item.low, item.timestamp))
            if (
                not whole_confirmation_candle
                and top_second.high <= analysis.event_second.high
            ):
                return None
            return Candidate(
                first_idx=candle.index,
                first_time=candle.display_time,
                box_top_source_idx=candle.index,
                box_top_source_time=candle.display_time,
                box_top=top_second.high,
                box_bottom_source_idx=candle.index,
                box_bottom_source_time=candle.display_time,
                box_bottom=bottom_second.low,
                mode="B",
                intrabar_start=remainder_start,
            )
        bottom_second = min(seconds, key=lambda item: (item.low, item.timestamp))
        top_second = max(seconds, key=lambda item: (item.high, -item.timestamp.timestamp()))
        if (
            not whole_confirmation_candle
            and bottom_second.low >= analysis.event_second.low
        ):
            return None
        return Candidate(
            first_idx=candle.index,
            first_time=candle.display_time,
            box_top_source_idx=candle.index,
            box_top_source_time=candle.display_time,
            box_top=top_second.high,
            box_bottom_source_idx=candle.index,
            box_bottom_source_time=candle.display_time,
            box_bottom=bottom_second.low,
            mode="B",
            intrabar_start=remainder_start,
        )

    def _first_initial(self, direction: str) -> Candidate | None:
        initial_result = (
            self.bull.detect(first_only=True)
            if direction == "bullish"
            else self.bear.detect(first_only=True)
        )
        return (
            replace(initial_result.reactions[0])
            if initial_result.reactions
            else None
        )


    def _first_direct_same_direction_after_reset(
        self, direction: str, reset_index: int
    ) -> Candidate | None:
        """Return the first structurally owned reaction after Reset.

        The earliest eligible candidate owns the evolving leg until it either
        confirms or its outer leg boundary is strictly crossed. A nested local
        pattern cannot confirm while that owner is unresolved. If the boundary
        breaks first, restart strictly after that event. Bearish is the exact
        price/color mirror of Bullish.
        """
        context_tag = "GREEN" if direction == "bullish" else "RED"
        first_tag = "RED" if direction == "bullish" else "GREEN"
        blocked_through = reset_index

        for first_index in range(reset_index + 1, self.end_index + 1):
            first = self.candles[first_index]
            if first_index <= blocked_through:
                continue
            if first.tag != first_tag or self.candles[first_index - 1].tag != context_tag:
                continue

            candidate = self._build_direct_candidate(
                direction, reset_index, first_index
            )
            if candidate is None:
                continue
            confirmed, invalidation_index = self._scan_direct_candidate(
                direction, candidate, self.end_index
            )
            if confirmed is not None:
                return confirmed
            if invalidation_index is None:
                continue
            blocked_through = invalidation_index

        return None

    def _first_geometry_after_reset(
        self, direction: str, reset_index: int, end_index: int | None = None,
    ) -> Candidate | None:
        """Return the first complete raw Reaction geometry after a boundary.

        This bounded search intentionally ignores normal Reset/invalidation
        acceptance.  It is a geometry-only primitive: First/box/Break structure
        may be used as evidence even when normal Reaction lifecycle rules would
        later Reset or suppress that structure.
        """
        _lim = self.end_index if end_index is None else min(end_index, self.end_index)
        _ck = (direction, reset_index, _lim)
        if _ck in self._geometry_after_reset_cache:
            _cached = self._geometry_after_reset_cache[_ck]
            return replace(_cached) if _cached is not None else None
        first_tag = "RED" if direction == "bullish" else "GREEN"
        context_tag = "GREEN" if direction == "bullish" else "RED"
        limit = self.end_index if end_index is None else min(end_index, self.end_index)
        for first_index in range(reset_index + 1, limit + 1):
            if (
                self.candles[first_index].tag != first_tag
                or self.candles[first_index - 1].tag != context_tag
            ):
                continue
            candidate = self._build_direct_candidate(
                direction, reset_index, first_index
            )
            if candidate is None:
                continue
            for scan in range(first_index + 1, limit + 1):
                candle = self.candles[scan]
                if direction == "bullish":
                    if candle.low < candidate.box_bottom:
                        candidate.box_bottom = candle.low
                        candidate.box_bottom_source_idx = candle.index
                        candidate.box_bottom_source_time = candle.display_time
                    if candle.high > candidate.box_top:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        return candidate
                else:
                    if candle.high > candidate.box_top:
                        candidate.box_top = candle.high
                        candidate.box_top_source_idx = candle.index
                        candidate.box_top_source_time = candle.display_time
                    if candle.low < candidate.box_bottom:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        return candidate
        return None

    def first_geometry_after_reset(
        self, direction: str, reset_index: int, end_index: int
    ) -> Candidate | None:
        """Public lifecycle API for post-Reset geometry discovery."""
        return self._first_geometry_after_reset(direction, reset_index, end_index)


    def _reaction_break_indices(self, direction: str) -> list[int]:
        """Cached ascending `break_idx` values mirroring `all_reactions[direction]`.

        `all_reactions[direction]` is append-only and strictly non-decreasing
        in `break_idx`, so this index list can be reused via bisect instead of
        rescanning the full reaction history on every gate lookup.
        """
        reactions = self.all_reactions[direction]
        cached = self._reaction_break_index_cache.get(direction)
        if cached is not None and cached[0] == len(reactions):
            return cached[1]
        indices = [int(reaction.break_idx) for reaction in reactions]
        self._reaction_break_index_cache[direction] = (len(reactions), indices)
        return indices

    def first_order_reaction_after_gate(
        self,
        direction: str,
        gate_index: int,
        end_index: int | None = None,
        gate_event_time: datetime | None = None,
    ) -> Candidate | None:
        """Return direct Order_A geometry from continuous Reaction context."""
        limit = self.end_index if end_index is None else min(end_index, self.end_index)
        if gate_index < self.start_index or gate_index >= limit:
            return None

        def confirmed_no_later_than_gate(reaction: Candidate) -> bool:
            break_index = int(reaction.break_idx)
            if break_index < gate_index or gate_event_time is None:
                return break_index <= gate_index
            if break_index > gate_index:
                return False
            break_candle = self.candles[break_index]
            start = reaction.intrabar_start or break_candle.timestamp
            end = break_candle.timestamp + self.timeframe
            level = reaction.box_bottom if direction == "bearish" else reaction.box_top
            for lower in self.seconds_between(start, end):
                crossed = (
                    lower.low < level
                    if direction == "bearish"
                    else lower.high > level
                )
                if crossed:
                    return lower.timestamp <= gate_event_time
            return break_candle.timestamp <= gate_event_time

        reactions = self.all_reactions[direction]
        break_indices = self._reaction_break_indices(direction)
        # `break_indices` is non-decreasing and duplicate-free for this
        # engine's reaction stream. Keep only the owning position instead of
        # allocating the complete historical prefix on every gate lookup.
        cut = bisect.bisect_left(break_indices, gate_index)
        owner_position = cut - 1
        if cut < len(reactions) and break_indices[cut] == gate_index:
            if confirmed_no_later_than_gate(reactions[cut]):
                owner_position = cut
        search_start = gate_index + 1
        if owner_position < 0:
            result = self._earliest_confirmed_geometry(
                direction, search_start, limit
            )
            if result is not None:
                result.order_gate_decision = "no-history"
            return result

        owner = reactions[owner_position]
        boundary_end = max(int(owner.first_idx), gate_index - 1)
        gate = self.candles[gate_index]
        if direction == "bearish":
            outer_boundary, _ = self.maximum_high(
                int(owner.first_idx), boundary_end
            )
            gate_boundary = gate.low
        else:
            outer_boundary, _ = self.minimum_low(
                int(owner.first_idx), boundary_end
            )
            gate_boundary = gate.high

        event_start = gate_event_time or gate.timestamp
        event_end = self.candles[limit].timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, event_start)
        right = bisect.bisect_left(self.second_times, event_end)
        if left >= right:
            return None
        if direction == "bearish":
            outer_position = self.lower_index.first_greater(
                left, right, outer_boundary
            )
            gate_position = self.lower_index.first_less(
                left, right, gate_boundary
            )
        else:
            outer_position = self.lower_index.first_less(
                left, right, outer_boundary
            )
            gate_position = self.lower_index.first_greater(
                left, right, gate_boundary
            )
        if outer_position is None and gate_position is None:
            return None
        # Legacy loop checks the outer/restart predicate first inside each
        # lower-timeframe candle, so restart owns an exact-position tie.
        restart = outer_position is not None and (
            gate_position is None or outer_position <= gate_position
        )
        decision_position = outer_position if restart else gate_position
        assert decision_position is not None
        decision_time = self.second_times[decision_position]
        decision_kind = "restart" if restart else "continue"
        if decision_kind == "restart":
            source = self.main_source_for_time(decision_time)
            if source is None:
                return None
            search_start = int(source.index) + 1
        if search_start > limit:
            return None
        result = self._earliest_confirmed_geometry(
            direction, search_start, limit
        )
        if result is not None:
            result.order_gate_decision = decision_kind
            if decision_kind == "continue" and (
                result.anchor_idx is None or result.anchor_value is None
            ):
                # The gate-bounded geometry already carries the true current
                # forming-leg anchor when one was discovered.  Never overwrite
                # that provenance with an older Reset.  Reconstruction is only
                # a fallback for geometry that genuinely has no anchor.
                prior_resets = [
                    item for item in self.all_resets[direction]
                    if item.index < int(result.first_idx)
                ]
                if prior_resets:
                    reset_index = max(item.index for item in prior_resets)
                    if direction == "bullish":
                        boundary, source = self.minimum_low(
                            reset_index, int(result.first_idx) - 1
                        )
                    else:
                        boundary, source = self.maximum_high(
                            reset_index, int(result.first_idx) - 1
                        )
                    result.anchor_idx = source.index
                    result.anchor_value = boundary
                    result.leg_boundary_value = boundary
        return result

    def _earliest_confirmed_geometry(
        self, direction: str, start_index: int, end_index: int | None = None,
    ) -> Candidate | None:
        """Return the geometry whose strict confirmation occurs first.

        Multiple First candidates may overlap. Order-gender chronology belongs
        to the structure that completes first, not necessarily to the oldest
        still-unconfirmed First candle.
        """
        first_tag = "RED" if direction == "bullish" else "GREEN"
        context_tag = "GREEN" if direction == "bullish" else "RED"
        limit = self.end_index if end_index is None else min(end_index, self.end_index)
        active: list[Candidate] = []
        reset_index = max(self.start_index, start_index - 1)
        for scan in range(start_index, limit + 1):
            candle = self.candles[scan]
            if (
                scan > reset_index
                and candle.tag == first_tag
                and self.candles[scan - 1].tag == context_tag
            ):
                candidate = self._build_direct_candidate(
                    direction, reset_index, scan
                )
                if candidate is not None:
                    active.append(candidate)

            confirmed: list[Candidate] = []
            survivors: list[Candidate] = []
            for candidate in active:
                if scan <= candidate.first_idx:
                    survivors.append(candidate)
                    continue

                # Order geometry is still Reaction geometry.  A candidate that
                # strictly loses the floor/ceiling of the leg that owns it
                # before confirmation is dead; a later breakout/breakdown must
                # never resurrect that invalid structure as an Order Reaction.
                # When invalidation and confirmation compete inside one main
                # candle, the shared lower-timeframe resolver preserves exact
                # chronology (and invalidation-first on a finest-event tie).
                if self._owner_boundary_before_confirmation(
                    direction, candidate, candle
                ):
                    continue

                if direction == "bullish":
                    if candle.low < candidate.box_bottom:
                        candidate.box_bottom = candle.low
                        candidate.box_bottom_source_idx = candle.index
                        candidate.box_bottom_source_time = candle.display_time
                    if candle.high > candidate.box_top:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        confirmed.append(candidate)
                        continue
                else:
                    if candle.high > candidate.box_top:
                        candidate.box_top = candle.high
                        candidate.box_top_source_idx = candle.index
                        candidate.box_top_source_time = candle.display_time
                    if candle.low < candidate.box_bottom:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        confirmed.append(candidate)
                        continue
                survivors.append(candidate)
            active = survivors
            if confirmed:
                return min(confirmed, key=lambda item: item.first_idx)
        return None

    def _build_direct_candidate(
        self, direction: str, reset_index: int, first_index: int
    ) -> Candidate | None:
        context_tag = "GREEN" if direction == "bullish" else "RED"
        first_tag = "RED" if direction == "bullish" else "GREEN"
        first = self.candles[first_index]
        if (
            first_index <= reset_index
            or first.tag != first_tag
            or self.candles[first_index - 1].tag != context_tag
        ):
            return None

        context_start = first_index - 1
        while (
            context_start - 1 >= reset_index
            and self.candles[context_start - 1].tag == context_tag
        ):
            context_start -= 1
        local_start = context_start
        while (
            local_start - 1 >= reset_index
            and self.candles[local_start - 1].tag == first_tag
        ):
            local_start -= 1

        if direction == "bullish":
            local_floor, _ = self.minimum_low(local_start, first_index - 1)
            if first.low < local_floor:
                return None
            box_top, top_source = self.maximum_high(context_start, first_index)
            leg_boundary, leg_source = self.minimum_low(
                reset_index, first_index - 1
            )
            return Candidate(
                first_index, first.display_time,
                top_source.index, top_source.display_time, box_top,
                first_index, first.display_time, first.low,
                mode="A", anchor_idx=leg_source.index,
                anchor_value=leg_boundary, leg_boundary_value=leg_boundary,
            )

        local_ceiling, _ = self.maximum_high(local_start, first_index - 1)
        if first.high > local_ceiling:
            return None
        box_bottom, bottom_source = self.minimum_low(context_start, first_index)
        leg_boundary, leg_source = self.maximum_high(
            reset_index, first_index - 1
        )
        return Candidate(
            first_index, first.display_time,
            first_index, first.display_time, first.high,
            bottom_source.index, bottom_source.display_time, box_bottom,
            mode="A", anchor_idx=leg_source.index,
            anchor_value=leg_boundary, leg_boundary_value=leg_boundary,
        )


    def _scan_direct_candidate(
        self, direction: str, candidate: Candidate, stop_index: int
    ) -> tuple[Candidate | None, int | None]:
        for scan in range(candidate.first_idx + 1, stop_index + 1):
            candle = self.candles[scan]
            confirms = (
                candle.high > candidate.box_top
                if direction == "bullish"
                else candle.low < candidate.box_bottom
            )
            invalidates = self._owner_boundary_before_confirmation(
                direction, candidate, candle
            )
            if invalidates:
                return None, scan
            if direction == "bullish" and candle.low < candidate.box_bottom:
                candidate.box_bottom = candle.low
                candidate.box_bottom_source_idx = candle.index
                candidate.box_bottom_source_time = candle.display_time
            if direction == "bearish" and candle.high > candidate.box_top:
                candidate.box_top = candle.high
                candidate.box_top_source_idx = candle.index
                candidate.box_top_source_time = candle.display_time
            if confirms:
                candidate.break_idx = scan
                candidate.break_time = candle.display_time
                self._refine(direction, candidate, candle)
                return candidate, None
        return None, None

    def _owner_boundary_before_confirmation(
        self, direction: str, candidate: Candidate, candle: Candle
    ) -> bool:
        """Return whether structural alignment is lost before confirmation.

        A Bearish Leg-Start Top must not rise above its outer ceiling.
        A Bullish Leg-Start Bottom must not fall below its outer floor.
        Equality preserves the unresolved candidate. If a strict invalidation
        competes with confirmation in the same main candle, ordered one-second
        data decides which event occurred first.
        """
        boundary = candidate.leg_boundary_value
        if boundary is None:
            return False

        if direction == "bullish":
            reaches_boundary = candle.low < boundary
            confirms = candle.high > candidate.box_top
        else:
            reaches_boundary = candle.high > boundary
            confirms = candle.low < candidate.box_bottom
        if not reaches_boundary:
            return False
        if not confirms:
            return True

        end = candle.timestamp + self.timeframe
        for second in self.seconds_between(candle.timestamp, end):
            if direction == "bullish":
                if second.low < boundary:
                    return True
                if second.high > candidate.box_top:
                    return False
            else:
                if second.high > boundary:
                    return True
                if second.low < candidate.box_bottom:
                    return False
        return True


    def _result(self) -> DetectionResult:
        return DetectionResult(
            direction=self.output_direction,
            reactions=self.all_reactions[self.output_direction],
            resets=self.all_resets[self.output_direction],
            start_index=self.start_index,
            end_index=self.end_index,
        )

    def detect(
        self, *, stop_after_first_at_or_after: int | None = None
    ) -> DetectionResult:
        direction = self.output_direction
        initial = self._first_initial(direction)
        if initial is None:
            return DetectionResult(
                direction=direction,
                reactions=[],
                resets=[],
                start_index=self.start_index,
                end_index=self.end_index,
            )
        self._append_reaction(direction, initial)
        if (
            stop_after_first_at_or_after is not None
            and initial.first_idx >= stop_after_first_at_or_after
        ):
            return self._result()
        previous = initial
        index = initial.break_idx + 1
        running_value = (
            self.candles[initial.break_idx].high
            if direction == "bullish"
            else self.candles[initial.break_idx].low
        )
        running_source = initial.break_idx
        candidate: Candidate | None = None
        initial_break_candle = self.candles[initial.break_idx]
        initial_helper = self.bull if direction == "bullish" else self.bear
        initial_analysis = (
            initial_helper.breakout_analysis(initial, initial_break_candle)
            if direction == "bullish"
            else initial_helper.breakdown_analysis(initial, initial_break_candle)
        )
        # Exact-confirmation geometry owns the post-confirmation remainder in
        # both directions. ``_append_reaction`` may later expand the public
        # opposite edge with the complete Break main candle, but that later
        # presentation geometry must never erase a Reset that occurred after
        # exact confirmation inside the same candle.
        initial_reset_level = (
            initial_analysis.extreme
            if initial_analysis is not None
            else (initial.box_bottom if direction == "bullish" else initial.box_top)
        )
        initial_reset_second = (
            initial_helper.post_breakout_reset(
                initial_analysis, initial_reset_level, initial_break_candle
            )
            if direction == "bullish"
            else initial_helper.post_breakdown_reset(
                initial_analysis, initial_reset_level, initial_break_candle
            )
        )
        pending_reset_index = (
            initial.break_idx if initial_reset_second is not None else None
        )
        if initial_reset_second is not None:
            self._append_reset(
                direction,
                initial_break_candle,
                initial_reset_level,
                initial.first_idx,
                initial_reset_second.display_time,
            )

        while index <= self.end_index:
            candle = self.candles[index]
            reset = pending_reset_index is not None or (
                candle.low < previous.box_bottom
                if direction == "bullish"
                else candle.high > previous.box_top
            )
            candidate_break = candidate is not None and (
                candle.high > candidate.box_top
                if direction == "bullish"
                else candle.low < candidate.box_bottom
            )
            if reset and candidate_break:
                if direction == "bullish":
                    reset = self.bull.confirmed_reset_before_breakout(
                        candidate, candle, previous.box_bottom
                    )
                else:
                    reset = self.bear.confirmed_reset_before_breakdown(
                        candidate, candle, previous.box_top
                    )
            if reset:
                reset_index = (
                    pending_reset_index
                    if pending_reset_index is not None
                    else index
                )
                reset_candle = self.candles[reset_index]
                pending_reset_index = None
                level = previous.box_bottom if direction == "bullish" else previous.box_top
                already_recorded = (
                    self.all_resets[direction]
                    and self.all_resets[direction][-1].from_first_idx
                    == previous.first_idx
                )
                if not already_recorded:
                    self._append_reset(
                        direction, reset_candle, level, previous.first_idx
                    )
                # A Reset reopens the ordinary same-direction ownership gate.
                # The geometric relaxation belongs only to the cross-direction
                # structural/E path and must not relabel every normal Reset.
                direct_candidate = self._first_direct_same_direction_after_reset(
                    direction, reset_index
                )
                # Both paths are valid interpretations of the same requested-
                # direction restart. The chronologically first confirmation
                # wins; a later Anchor-based candidate must never hide an
                # already complete direct post-Reset color sequence.
                structural = direct_candidate
                if structural is None or structural.break_idx is None:
                    break
                structural.mode = "A"
                structural.cross_direction_origin = False
                structural.cross_direction_chain_owner = False
                if not self._append_reaction(direction, structural):
                    candidate = None
                    index = structural.break_idx + 1
                    pending_reset_index = structural.break_idx
                    continue
                if (
                    stop_after_first_at_or_after is not None
                    and structural.first_idx >= stop_after_first_at_or_after
                ):
                    return self._result()
                previous = structural
                index = structural.break_idx + 1
                running_value = (
                    self.candles[structural.break_idx].high
                    if direction == "bullish"
                    else self.candles[structural.break_idx].low
                )
                running_source = structural.break_idx
                break_candle = self.candles[structural.break_idx]
                helper = self.bull if direction == "bullish" else self.bear
                analysis = (
                    helper.breakout_analysis(structural, break_candle)
                    if direction == "bullish"
                    else helper.breakdown_analysis(structural, break_candle)
                )
                reset_level = (
                    analysis.extreme
                    if analysis is not None
                    else (
                        structural.box_bottom
                        if direction == "bullish"
                        else structural.box_top
                    )
                )
                post_reset_second = (
                    helper.post_breakout_reset(
                        analysis, reset_level, break_candle
                    )
                    if direction == "bullish"
                    else helper.post_breakdown_reset(
                        analysis, reset_level, break_candle
                    )
                )
                if post_reset_second is not None:
                    self._append_reset(
                        direction,
                        break_candle,
                        reset_level,
                        structural.first_idx,
                        post_reset_second.display_time,
                    )
                    # The confirmation candle has already reset the reaction
                    # after its exact intrabar confirmation. Its remainder
                    # cannot seed a Normal successor. Restart from the next
                    # main candle as a fresh Leg-Start search.
                    candidate = None
                    pending_reset_index = structural.break_idx
                else:
                    candidate = self._candidate_from_confirmation_remainder(
                        direction, structural, break_candle, analysis
                    )
                continue

            if candidate is not None:
                if direction == "bullish":
                    if candle.low < candidate.box_bottom:
                        candidate.box_bottom = candle.low
                        candidate.box_bottom_source_idx = candle.index
                        candidate.box_bottom_source_time = candle.display_time
                    if candle.high > candidate.box_top:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        analysis = self._refine(direction, candidate, candle)
                        reset_level = (
                            analysis.extreme if analysis is not None else candidate.box_bottom
                        )
                        post_reset_second = self.bull.post_breakout_reset(
                            analysis, reset_level, candle
                        )
                        self._append_reaction(direction, candidate)
                        if (
                            stop_after_first_at_or_after is not None
                            and candidate.first_idx >= stop_after_first_at_or_after
                        ):
                            return self._result()
                        previous = replace(candidate)
                        running_value = candle.high
                        running_source = candle.index
                        if post_reset_second is not None:
                            self._append_reset(
                                direction,
                                candle,
                                reset_level,
                                previous.first_idx,
                                post_reset_second.display_time,
                            )
                            candidate = None
                            pending_reset_index = candle.index
                        else:
                            candidate = self._candidate_from_confirmation_remainder(
                                direction, previous, candle, analysis
                            )
                else:
                    if candle.high > candidate.box_top:
                        candidate.box_top = candle.high
                        candidate.box_top_source_idx = candle.index
                        candidate.box_top_source_time = candle.display_time
                    if candle.low < candidate.box_bottom:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        analysis = self._refine(direction, candidate, candle)
                        reset_level = (
                            analysis.extreme if analysis is not None else candidate.box_top
                        )
                        post_reset_second = self.bear.post_breakdown_reset(
                            analysis, reset_level, candle
                        )
                        self._append_reaction(direction, candidate)
                        if (
                            stop_after_first_at_or_after is not None
                            and candidate.first_idx >= stop_after_first_at_or_after
                        ):
                            return self._result()
                        previous = replace(candidate)
                        running_value = candle.low
                        running_source = candle.index
                        if post_reset_second is not None:
                            self._append_reset(
                                direction,
                                candle,
                                reset_level,
                                previous.first_idx,
                                post_reset_second.display_time,
                            )
                            candidate = None
                            pending_reset_index = candle.index
                        else:
                            candidate = self._candidate_from_confirmation_remainder(
                                direction, previous, candle, analysis
                            )
            else:
                if direction == "bullish" and candle.tag == "RED":
                    top = max(running_value, candle.high)
                    top_source = running_source if running_value >= candle.high else candle.index
                    bottom_start = top_source + 1 if top_source < candle.index else candle.index
                    bottom, bottom_source = self.minimum_low(bottom_start, candle.index)
                    candidate = Candidate(
                        candle.index,
                        candle.display_time,
                        top_source,
                        self.candles[top_source].display_time,
                        top,
                        bottom_source.index,
                        bottom_source.display_time,
                        bottom,
                        mode="B",
                    )
                elif direction == "bearish" and candle.tag == "GREEN":
                    bottom = min(running_value, candle.low)
                    bottom_source = running_source if running_value <= candle.low else candle.index
                    top_start = bottom_source + 1 if bottom_source < candle.index else candle.index
                    top, top_source = self.maximum_high(top_start, candle.index)
                    candidate = Candidate(
                        candle.index,
                        candle.display_time,
                        top_source.index,
                        top_source.display_time,
                        top,
                        bottom_source,
                        self.candles[bottom_source].display_time,
                        bottom,
                        mode="B",
                    )
            if direction == "bullish" and (running_value is None or candle.high > running_value):
                running_value, running_source = candle.high, candle.index
            if direction == "bearish" and (running_value is None or candle.low < running_value):
                running_value, running_source = candle.low, candle.index
            index += 1

        return self._result()


