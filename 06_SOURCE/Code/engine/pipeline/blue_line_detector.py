"""Blue Line calculation over authoritative Reaction output.

Owns Scale and Reset Blue detection, strike/spacing state, Blue stop validity,
and the distinction between calculation state and public Blue visibility. It
does not decide A/S/E lifecycle ownership.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from direction_policy import policy_for


BLUE_LINE_VERSION = "2.3.0"
FIBONACCI_RATIO = Decimal("0.618")


@dataclass(frozen=True, slots=True)
class ScaleStrike:
    source_index: int
    source_time: datetime
    extreme: Decimal


@dataclass(frozen=True, slots=True)
class BlueLine:
    direction: str
    kind: str
    reaction_number: int
    previous_strike_count: int | None
    strike_count: int | None
    fibonacci_level: Decimal | None
    source_index: int
    source_time: datetime
    source_extreme: Decimal
    broken_level: Decimal | None
    line_price: Decimal
    start_time: datetime
    end_time: datetime
    calculation_valid: bool = True
    behavior_internal: bool = False


def _is_color(candle: object, color: str) -> bool:
    return str(getattr(candle, "tag")).upper() == color


def _main_candle(candles_by_index: dict[int, object], index: int) -> object:
    try:
        return candles_by_index[index]
    except KeyError as exc:
        raise ValueError(f"Missing main candle index {index}.") from exc


def _stops_on_index(
    direction: str,
    line: object,
    candles: Sequence[object],
    start_index: int,
    end_index: int,
) -> bool:
    policy = policy_for(direction)
    level = Decimal(getattr(line, "source_extreme"))
    for candle in candles[max(0, start_index) : end_index + 1]:
        extreme = Decimal(getattr(candle, policy.extreme_attr))
        if policy.strict_cross(extreme, level):
            return int(getattr(candle, "index")) == end_index
    return False


def fibonacci_level(direction: str, reaction: object, reference: Decimal) -> Decimal:
    policy = policy_for(direction)  # validates direction centrally
    if policy.direction == "bullish":
        top = Decimal(getattr(reaction, "box_top"))
        return top - FIBONACCI_RATIO * (top - reference)
    bottom = Decimal(getattr(reaction, "box_bottom"))
    return bottom + FIBONACCI_RATIO * (reference - bottom)


def _intrabar_pending_confirmation(
    direction: str,
    chronology: object,
    reaction: object,
    comparison_extreme: Decimal,
    start_time: datetime,
    break_time: datetime,
    candles_by_index: dict[int, object],
) -> ScaleStrike | None:
    policy = policy_for(direction)
    end_time = break_time + chronology.timeframe
    left, right = chronology.lower_bounds(start_time, end_time)
    relevant = chronology.seconds[left:right]
    if not relevant:
        return None

    break_level = Decimal(
        getattr(reaction, "box_top" if direction == "bullish" else "box_bottom")
    )
    eligible: list[object] = []
    for second in relevant:
        extreme = Decimal(getattr(second, policy.extreme_attr))
        penetrates = (
            extreme < comparison_extreme
            if direction == "bullish"
            else extreme > comparison_extreme
        )
        if penetrates:
            eligible.append(second)
        breaks = (
            Decimal(getattr(second, "high")) > break_level
            if direction == "bullish"
            else Decimal(getattr(second, "low")) < break_level
        )
        if breaks and eligible:
            decisive = (
                min(eligible, key=lambda item: Decimal(getattr(item, "low")))
                if direction == "bullish"
                else max(eligible, key=lambda item: Decimal(getattr(item, "high")))
            )
            decisive_time = getattr(decisive, "timestamp")
            source_position = chronology.main_index(decisive_time)
            source = candles_by_index.get(source_position)
            if source is None:
                raise ValueError("Cannot map decisive one-second candle to a main candle.")
            return ScaleStrike(
                source_index=int(getattr(source, "index")),
                source_time=getattr(source, "timestamp"),
                extreme=Decimal(
                    getattr(decisive, policy.extreme_attr)
                ),
            )
    return None


def count_scale_strikes(
    direction: str,
    reaction: object,
    chronology: object,
    reference: Decimal,
    candles_by_index: dict[int, object] | None = None,
) -> tuple[Decimal, list[ScaleStrike]]:
    """Return the exact 0.618 level and confirmed strikes for one reaction."""
    level = fibonacci_level(direction, reaction, reference)
    if candles_by_index is None:
        candles_by_index = {
            int(getattr(candle, "index")): candle for candle in chronology.candles
        }
    first_index = int(getattr(reaction, "first_idx"))
    break_index = int(getattr(reaction, "break_idx"))
    reaction_candles = [
        _main_candle(candles_by_index, index)
        for index in range(first_index, break_index + 1)
    ]
    confirming_color = "GREEN" if direction == "bullish" else "RED"
    strikes: list[ScaleStrike] = []
    pending: ScaleStrike | None = None

    for candle in reaction_candles:
        last_extreme = strikes[-1].extreme if strikes else level
        candle_extreme = Decimal(
            getattr(candle, "low" if direction == "bullish" else "high")
        )
        is_new = (
            candle_extreme < last_extreme
            if direction == "bullish"
            else candle_extreme > last_extreme
        )
        if is_new and (
            pending is None
            or (
                candle_extreme < pending.extreme
                if direction == "bullish"
                else candle_extreme > pending.extreme
            )
        ):
            pending = ScaleStrike(
                source_index=int(getattr(candle, "index")),
                source_time=getattr(candle, "timestamp"),
                extreme=candle_extreme,
            )

        if pending is not None and _is_color(candle, confirming_color):
            strikes.append(pending)
            pending = None

    if pending is not None:
        break_candle = reaction_candles[-1]
        intrabar = _intrabar_pending_confirmation(
            direction=direction,
            chronology=chronology,
            reaction=reaction,
            comparison_extreme=strikes[-1].extreme if strikes else level,
            start_time=pending.source_time,
            break_time=getattr(break_candle, "timestamp"),
            candles_by_index=candles_by_index,
        )
        if intrabar is not None:
            strikes.append(intrabar)

    return level, strikes


def _build_scale_blue_line(
    direction: str,
    reaction_number: int,
    previous_count: int,
    level: Decimal,
    strikes: Sequence[ScaleStrike],
    candles_by_index: dict[int, object],
    chronology: object,
    behavior_internal: bool,
) -> BlueLine:
    """Build one scale Blue from its decisive confirmed strike."""
    decisive = strikes[-1]
    source = _main_candle(candles_by_index, decisive.source_index)
    high = Decimal(getattr(source, "high"))
    low = Decimal(getattr(source, "low"))
    line_price = (
        low + (high - low) / Decimal(3)
        if direction == "bullish"
        else high - (high - low) / Decimal(3)
    )
    return BlueLine(
        direction=direction,
        kind="scale",
        reaction_number=reaction_number,
        previous_strike_count=previous_count,
        strike_count=len(strikes),
        fibonacci_level=level,
        source_index=decisive.source_index,
        source_time=decisive.source_time,
        source_extreme=decisive.extreme,
        broken_level=None,
        line_price=line_price,
        start_time=decisive.source_time - chronology.timeframe,
        end_time=decisive.source_time + chronology.timeframe,
        behavior_internal=behavior_internal,
    )


def _build_reset_blue_line(
    direction: str,
    reaction_number: int,
    reset: object,
    previous_line: BlueLine | None,
    candles: Sequence[object],
    candles_by_index: dict[int, object],
    chronology: object,
    behavior_internal: bool,
) -> BlueLine:
    """Build one Reset Blue while preserving the established double-stop rule."""
    reset_index = int(getattr(reset, "index"))
    source = _main_candle(candles_by_index, reset_index)
    high = Decimal(getattr(source, "high"))
    low = Decimal(getattr(source, "low"))
    line_price = (
        low + (high - low) / Decimal(5)
        if direction == "bullish"
        else high - (high - low) / Decimal(5)
    )
    source_time = getattr(source, "timestamp")
    calculation_valid = not (
        previous_line is not None
        and _stops_on_index(
            direction,
            previous_line,
            candles,
            int(getattr(previous_line, "source_index")) + 1,
            reset_index,
        )
        and (
            low < Decimal(getattr(previous_line, "source_extreme"))
            if direction == "bullish"
            else high > Decimal(getattr(previous_line, "source_extreme"))
        )
    )
    return BlueLine(
        direction=direction,
        kind="reset",
        reaction_number=reaction_number,
        previous_strike_count=None,
        strike_count=None,
        fibonacci_level=None,
        source_index=reset_index,
        source_time=source_time,
        source_extreme=low if direction == "bullish" else high,
        broken_level=Decimal(getattr(reset, "broken_level")),
        line_price=line_price,
        start_time=source_time - chronology.timeframe,
        end_time=source_time + chronology.timeframe,
        calculation_valid=calculation_valid,
        behavior_internal=behavior_internal,
    )

def detect_blue_lines(
    direction: str,
    reactions: Sequence[object],
    chronology: object,
    resets: Sequence[object] = (),
) -> list[BlueLine]:
    """Detect scale and Reset Blue Lines over authoritative engine events."""
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    candles = chronology.candles
    candles_by_index = {
        int(getattr(candle, "index")): candle for candle in candles
    }
    resets_by_first: dict[int, list[object]] = {}
    for reset in resets:
        resets_by_first.setdefault(
            int(getattr(reset, "from_first_idx")), []
        ).append(reset)

    output: list[BlueLine] = []
    previous_reaction: object | None = None
    previous_count: int | None = None
    has_blue_line = False
    healthy_reactions_since_blue = 0

    for reaction_number, reaction in enumerate(reactions, start=1):
        behavior_internal = bool(getattr(reaction, "behavior_internal", False))
        if str(getattr(reaction, "mode")) == "A":
            boundary = getattr(reaction, "anchor_value", None)
            if boundary is None:
                boundary = getattr(reaction, "leg_boundary_value", None)
            if boundary is None:
                raise ValueError(
                    "Leg-Start reaction is missing its leg-head boundary."
                )
            reference = Decimal(boundary)
            previous_count = None
        else:
            if previous_reaction is None:
                raise ValueError(
                    "A Normal reaction cannot precede the Leg-Start reaction."
                )
            reference = Decimal(
                getattr(
                    previous_reaction,
                    "box_bottom" if direction == "bullish" else "box_top",
                )
            )

        level, strikes = count_scale_strikes(
            direction,
            reaction,
            chronology,
            reference,
            candles_by_index,
        )
        scale_candidate = (
            previous_count is not None and len(strikes) > previous_count
        )
        scale_emitted = False
        if scale_candidate and (
            not has_blue_line or healthy_reactions_since_blue >= 1
        ):
            output.append(
                _build_scale_blue_line(
                    direction,
                    reaction_number,
                    previous_count,
                    level,
                    strikes,
                    candles_by_index,
                    chronology,
                    behavior_internal,
                )
            )
            has_blue_line = True
            healthy_reactions_since_blue = 0
            scale_emitted = True

        if has_blue_line and not scale_emitted:
            healthy_reactions_since_blue += 1

        for reset in resets_by_first.get(
            int(getattr(reaction, "first_idx")), []
        ):
            if has_blue_line and healthy_reactions_since_blue < 1:
                continue
            output.append(
                _build_reset_blue_line(
                    direction,
                    reaction_number,
                    reset,
                    output[-1] if output else None,
                    candles,
                    candles_by_index,
                    chronology,
                    behavior_internal,
                )
            )
            has_blue_line = True
            healthy_reactions_since_blue = 0

        previous_reaction = reaction
        previous_count = len(strikes)

    return output


def public_blue_lines(lines: Sequence[BlueLine]) -> list[BlueLine]:
    """Return only calculation-valid, public Blue Lines for serialization."""
    return [
        line
        for line in lines
        if bool(getattr(line, "calculation_valid", True))
        and not bool(getattr(line, "behavior_internal", False))
    ]

def mark_internal_blue_lines(
    lines: Sequence[BlueLine],
    owner_reactions: Sequence[object],
    all_behavior_reactions: Sequence[object],
) -> None:
    """Mark Blue Lines that are private to protected Reaction interiors.

    A Blue is internal when its owning Reaction is behavior-internal, or when
    both its calculation-owned ``source_extreme`` and rendered ``line_price``
    fall strictly inside the same healthy Reaction interior.  The drawing
    offset alone never changes ownership.
    """

    def owner_is_internal(line: BlueLine) -> bool:
        number = int(getattr(line, "reaction_number", 0) or 0)
        if number < 1 or number > len(owner_reactions):
            return False
        return bool(getattr(owner_reactions[number - 1], "behavior_internal", False))

    def geometry_is_internal(line: BlueLine) -> bool:
        source_time = getattr(line, "source_time", None)
        line_price = getattr(line, "line_price", None)
        source_extreme = getattr(line, "source_extreme", None)
        if source_time is None or line_price is None or source_extreme is None:
            return False
        rendered = Decimal(str(line_price))
        semantic = Decimal(str(source_extreme))
        for reaction in all_behavior_reactions:
            first = getattr(reaction, "behavior_first_time", None)
            confirmed = getattr(reaction, "behavior_confirmation_time", None)
            if first is None or confirmed is None:
                continue
            if source_time <= first or source_time > confirmed:
                continue
            bottom = Decimal(str(getattr(reaction, "behavior_public_box_bottom")))
            top = Decimal(str(getattr(reaction, "behavior_public_box_top")))
            if bottom < semantic < top and bottom < rendered < top:
                return True
        return False

    for line in lines:
        if owner_is_internal(line) or geometry_is_internal(line):
            object.__setattr__(line, "behavior_internal", True)
