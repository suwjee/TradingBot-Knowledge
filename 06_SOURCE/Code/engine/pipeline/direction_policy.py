"""Shared, behavior-neutral Bullish/Bearish direction primitives.

This module deliberately contains only price-direction semantics.  It does not
own chronology, lifecycle, numbering, visibility, or trading state.  Keeping
these primitives in one place prevents Bullish/Bearish drift while preserving
the existing algorithms in their owning engines.
"""

from __future__ import annotations

DIRECTION_POLICY_VERSION = "1.0.0"

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

Direction = Literal["bullish", "bearish"]


@dataclass(frozen=True, slots=True)
class DirectionPolicy:
    direction: Direction
    extreme_attr: Literal["low", "high"]
    opposite_extreme_attr: Literal["high", "low"]
    first_reaction_tag: Literal["RED", "GREEN"]
    context_tag: Literal["GREEN", "RED"]

    @property
    def opposite_direction(self) -> Direction:
        return "bearish" if self.direction == "bullish" else "bullish"

    def strict_cross(self, value: Decimal, level: Decimal) -> bool:
        return value < level if self.direction == "bullish" else value > level

    def better_extreme(self, value: Decimal, current: Decimal) -> bool:
        return value < current if self.direction == "bullish" else value > current

    def choose_extreme(self, left: Decimal, right: Decimal) -> Decimal:
        return min(left, right) if self.direction == "bullish" else max(left, right)

    def confirmation_cross(self, value: Decimal, level: Decimal) -> bool:
        """Reaction confirmation mirror: high>top vs low<bottom.

        ``value`` is the already-selected confirmation-side price.
        """
        return value > level if self.direction == "bullish" else value < level


def policy_for(direction: str) -> DirectionPolicy:
    if direction == "bullish":
        return BULLISH
    if direction == "bearish":
        return BEARISH
    raise ValueError("Direction must be 'bullish' or 'bearish'.")


BULLISH = DirectionPolicy(
    direction="bullish",
    extreme_attr="low",
    opposite_extreme_attr="high",
    first_reaction_tag="RED",
    context_tag="GREEN",
)
BEARISH = DirectionPolicy(
    direction="bearish",
    extreme_attr="high",
    opposite_extreme_attr="low",
    first_reaction_tag="GREEN",
    context_tag="RED",
)
