"""Small behavior-neutral primitives shared by calculation engines."""

from __future__ import annotations

CORE_UTILS_VERSION = "1.0.0"

from decimal import Decimal
from typing import TypeAlias


def as_decimal(value: object) -> Decimal:
    """Preserve Decimal values and normalize other numeric inputs losslessly."""
    return value if isinstance(value, Decimal) else Decimal(str(value))


OrderIdentity: TypeAlias = tuple[int, int]


def order_identity(first_index: object, break_index: object) -> OrderIdentity:
    """Return the canonical physical Order/Reaction geometry identity."""
    return int(first_index), int(break_index)


def reaction_identity(reaction: object) -> OrderIdentity:
    """Return ``(FirstIndex, BreakIndex)`` for a Reaction-like object."""
    return order_identity(
        getattr(reaction, "first_idx"),
        getattr(reaction, "break_idx"),
    )
