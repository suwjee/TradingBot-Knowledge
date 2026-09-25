"""Cross-stage behavior lifecycle, visibility, priority, and StopAll ownership.

Owns the single shared behavior-priority table, accepted-vs-blocked Order
precedence, A/S/E/StopAll public ownership boundaries, Internal-Reaction output
filters, and StopAll detection/reconciliation. It does not reconstruct detector
geometry.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field, replace
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from core_utils import as_decimal, order_identity
from direction_policy import policy_for


STOP_ALL_VERSION = "1.15.6"
STOP_ALL_LAST_MODIFIED = "2026-09-24 03:54:00 +03:30"


SEQUENCE_PRIORITY = {
    ("s", "blue"): 1,
    ("e", "blue"): 2,
    ("s", "red"): 3,
    ("e", "red"): 4,
}


def sequence_priority(kind: str, family: str) -> int:
    """Return the single authoritative cross-stage behavior priority."""
    return SEQUENCE_PRIORITY[(str(kind).lower(), str(family).lower())]


@dataclass(frozen=True, slots=True)
class StopAll:
    direction: str
    number: int
    source_index: int
    source_time: datetime
    price: Decimal
    decision_index: int
    decision_time: datetime
    decision_event_time: datetime
    gate_type: str
    gate_event_time: datetime
    stopped_behavior_type: str
    stopped_behavior_key: str
    stopped_behavior_count: int
    underlying_e_family: str | None
    underlying_e_number: int | None
    order_direction: str | None
    order_reaction_number: int | None
    order_mode: str | None
    order_causes: tuple[str, ...]
    order_parent_stop_cause_time: datetime | None
    order_reset_leg_reset_time: datetime | None
    order_reset_leg_break_time: datetime | None
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
    stop_index: int | None
    stop_time: datetime | None
    stop_event_time: datetime | None
    # Immutable presentation provenance for the exact constructor donor. It is
    # intentionally separate from stopped_behavior_* (the lifecycle gate).
    # These fields never affect StopAll formation, priority, visibility, or
    # Order selection.
    donor_type: str | None = field(default=None, kw_only=True)
    donor_source_index: int | None = field(default=None, kw_only=True)
    donor_source_time: datetime | None = field(default=None, kw_only=True)
    donor_color: str | None = field(default=None, kw_only=True)
    donor_number: int | None = field(default=None, kw_only=True)
    donor_price: Decimal | None = field(default=None, kw_only=True)
    donor_stop_time: datetime | None = field(default=None, kw_only=True)
    donor_stop_event_time: datetime | None = field(default=None, kw_only=True)


class StopAllDetector:
    def __init__(
        self,
        direction: str,
        s_zones: Sequence[object],
        e_zones: Sequence[object],
        chronology: object,
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.s_zones = list(s_zones)
        self.e_zones = sorted(
            e_zones, key=lambda item: (item.source_time, item.source_index)
        )
        self.chronology = chronology
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index
        self.times = chronology.times

    def _strict_stop(
        self, start: datetime, level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        left = bisect_left(self.lower_times, start)
        right = len(self.lower)
        position = (
            self.lower_index.first_less(left, right, level)
            if self.direction == "bullish"
            else self.lower_index.first_greater(left, right, level)
        )
        if position is None:
            return None
        event = self.lower_times[position]
        index = self.chronology.main_index(event, clamp=True)
        return index, self.times[index], event

    @staticmethod
    def _e_key(item: object) -> tuple[str, int]:
        return str(item.family), int(item.number)

    @staticmethod
    def _dominates_e(new: tuple[str, int], old: tuple[str, int]) -> bool:
        new_family, new_number = new
        old_family, old_number = old
        if new_family == old_family:
            return new_number > old_number
        # Red is always the dominant E family. A higher-numbered Blue E must
        # not separate or replace an active Red group.
        return new_family == "red" and old_family == "blue"

    @classmethod
    def _sequence_priority(cls, kind: str, family: str) -> int:
        return sequence_priority(kind, family)

    @classmethod
    def _active_sequence_priority(
        cls, s_key: str | None, e_key: tuple[str, int] | None,
    ) -> int:
        if e_key is not None:
            return cls._sequence_priority("e", e_key[0])
        if s_key is not None:
            return cls._sequence_priority("s", s_key)
        return 0

    def _stopall_from_e(
        self,
        item: object,
        number: int,
        gate_type: str,
        gate_event: datetime,
        behavior_type: str,
        behavior_key: str,
        behavior_count: int,
    ) -> StopAll:
        return StopAll(
            direction=self.direction,
            number=number,
            source_index=int(item.source_index),
            source_time=item.source_time,
            price=as_decimal(item.price),
            decision_index=int(item.decision_index),
            decision_time=item.decision_time,
            decision_event_time=item.decision_event_time,
            gate_type=gate_type,
            gate_event_time=gate_event,
            stopped_behavior_type=behavior_type,
            stopped_behavior_key=behavior_key,
            stopped_behavior_count=behavior_count,
            underlying_e_family=str(item.family),
            underlying_e_number=int(item.number),
            order_direction=str(item.order_direction),
            order_reaction_number=int(item.order_reaction_number),
            order_mode=str(item.order_mode),
            order_causes=tuple(getattr(item, "order_causes", ())),
            order_parent_stop_cause_time=getattr(
                item, "order_parent_stop_cause_time", None
            ),
            order_reset_leg_reset_time=getattr(
                item, "order_reset_leg_reset_time", None
            ),
            order_reset_leg_break_time=getattr(
                item, "order_reset_leg_break_time", None
            ),
            order_first_index=int(item.order_first_index),
            order_first_time=item.order_first_time,
            order_break_index=int(item.order_break_index),
            order_break_time=item.order_break_time,
            order_confirmation_time=item.order_confirmation_time,
            order_box_top=as_decimal(item.order_box_top),
            order_box_top_source_index=int(item.order_box_top_source_index),
            order_box_top_source_time=item.order_box_top_source_time,
            order_box_bottom=as_decimal(item.order_box_bottom),
            order_box_bottom_source_index=int(item.order_box_bottom_source_index),
            order_box_bottom_source_time=item.order_box_bottom_source_time,
            order_stop_level=as_decimal(item.order_stop_level),
            order_stop_source_index=int(item.order_stop_source_index),
            order_stop_source_time=item.order_stop_source_time,
            stop_index=None,
            stop_time=None,
            stop_event_time=None,
            donor_type="E",
            donor_source_index=int(item.source_index),
            donor_source_time=item.source_time,
            donor_color=str(item.family),
            donor_number=int(item.number),
            donor_price=as_decimal(item.price),
        )

    @staticmethod
    def _optional_int(value: object | None) -> int | None:
        return None if value is None else int(value)

    @staticmethod
    def _optional_decimal(value: object | None) -> Decimal | None:
        return None if value is None else as_decimal(value)

    def _stopall_from_s(
        self,
        item: object,
        behavior_type: str,
        behavior_key: str,
        behavior_count: int,
        underlying_e_key: tuple[str, int] | None,
    ) -> StopAll:
        """Promote the accepted opposite-color S into a fresh StopAll1.

        This is the direction-invariant family reversal gate.  In both
        Bullish and Bearish calculations, only an accepted native Mode-B S Red
        is promoted after two accepted occurrences of the same Blue behavior
        group since the latest accepted Red or StopAll boundary.  The repeated
        group need not remain the current dominant owner.  Directional mirroring is handled
        by strict stop/reaction geometry; Red/Blue family
        labels themselves are invariant.  Type-3 S Blue has no formation
        Order, so StopAll Order provenance remains optional.
        """
        return StopAll(
            direction=self.direction,
            number=1,
            source_index=int(item.source_index),
            source_time=item.source_time,
            price=as_decimal(item.price),
            decision_index=int(item.decision_index),
            decision_time=item.decision_time,
            decision_event_time=item.decision_event_time,
            gate_type="opposite-s-group-stop",
            gate_event_time=item.decision_event_time,
            stopped_behavior_type=behavior_type,
            stopped_behavior_key=behavior_key,
            stopped_behavior_count=behavior_count,
            underlying_e_family=(
                underlying_e_key[0] if underlying_e_key is not None else None
            ),
            underlying_e_number=(
                underlying_e_key[1] if underlying_e_key is not None else None
            ),
            order_direction=getattr(item, "order_direction", None),
            order_reaction_number=self._optional_int(
                getattr(item, "order_reaction_number", None)
            ),
            order_mode=getattr(item, "order_mode", None),
            order_causes=(),
            order_parent_stop_cause_time=getattr(
                item, "a_stop_event_time", None
            ),
            order_reset_leg_reset_time=getattr(item, "reset_time", None),
            order_reset_leg_break_time=None,
            order_first_index=self._optional_int(
                getattr(item, "order_first_index", None)
            ),
            order_first_time=getattr(item, "order_first_time", None),
            order_break_index=self._optional_int(
                getattr(item, "order_break_index", None)
            ),
            order_break_time=getattr(item, "order_break_time", None),
            order_confirmation_time=getattr(
                item, "order_confirmation_time", None
            ),
            order_box_top=self._optional_decimal(
                getattr(item, "order_box_top", None)
            ),
            order_box_top_source_index=self._optional_int(
                getattr(item, "order_box_top_source_index", None)
            ),
            order_box_top_source_time=getattr(
                item, "order_box_top_source_time", None
            ),
            order_box_bottom=self._optional_decimal(
                getattr(item, "order_box_bottom", None)
            ),
            order_box_bottom_source_index=self._optional_int(
                getattr(item, "order_box_bottom_source_index", None)
            ),
            order_box_bottom_source_time=getattr(
                item, "order_box_bottom_source_time", None
            ),
            order_stop_level=self._optional_decimal(
                getattr(item, "order_stop_level", None)
            ),
            order_stop_source_index=self._optional_int(
                getattr(item, "order_stop_source_index", None)
            ),
            order_stop_source_time=getattr(
                item, "order_stop_source_time", None
            ),
            stop_index=None,
            stop_time=None,
            stop_event_time=None,
            donor_type="S",
            donor_source_index=int(item.source_index),
            donor_source_time=item.source_time,
            donor_color=str(item.color),
            donor_number=None,
            donor_price=as_decimal(item.price),
        )

    @staticmethod
    def _blue_repeat_key(kind: str, number: int | None = None) -> tuple[str, int | None]:
        """Return the pending-reversal exact Blue behavior-group key.

        S Blue is one group regardless of its internal subtype.  Each E number
        is a separate group: E1 Blue, E2 Blue, E5 Blue, ... .  Counts are
        accepted-occurrence counts since the most recent Red S/Red E/StopAll,
        not counts of dominant-owner transitions.
        """
        normalized = str(kind).upper()
        if normalized == "S":
            return ("S", None)
        if normalized != "E" or number is None:
            raise ValueError("Blue repeat key must be S or numbered E.")
        return ("E", int(number))

    @staticmethod
    def _record_blue_repeat(
        counts: dict[tuple[str, int | None], int],
        latest: dict[tuple[str, int | None], object],
        key: tuple[str, int | None],
        item: object,
    ) -> None:
        counts[key] = counts.get(key, 0) + 1
        latest[key] = item

    def _opposite_s_stopall_gate(
        self,
        s_item: object,
        blue_repeat_counts: dict[tuple[str, int | None], int],
        blue_repeat_latest: dict[tuple[str, int | None], object],
    ) -> tuple[str, str, int, tuple[str, int] | None] | None:
        """Return Blue-repeat metadata when accepted S Red must become StopAll.

        Accepted Blue occurrences accumulate per exact S/E group until the
        first accepted Red S, accepted Red E, or hard StopAll boundary.  A Red
        behavior resolves the prior Blue reversal opportunity; a later S Red
        cannot consume its stale evidence.  The incoming S Red must have a
        native Mode-B formation Order; different numbered E groups never add.
        E-driven StopAll counters/priority are independent of this reversal
        evidence and retain their existing semantics.
        """
        if str(getattr(s_item, "color", "")).lower() != "red":
            return None
        # An initial native Mode-A Order opens an independent A→S Red branch;
        # it cannot consume old Blue-repeat evidence to promote that S to
        # StopAll. A continued Mode-B Order may own the reversal gate in the
        # existing hard lifecycle, in either market direction.
        if str(getattr(s_item, "order_mode", "")).upper() != "B":
            return None

        qualified = [
            (key, count, blue_repeat_latest[key])
            for key, count in blue_repeat_counts.items()
            if count >= 2 and key in blue_repeat_latest
        ]
        if not qualified:
            return None

        key, count, _ = max(
            qualified,
            key=lambda entry: (
                getattr(entry[2], "source_time"),
                int(getattr(entry[2], "source_index", -1)),
                1 if entry[0][0] == "E" else 0,
                -1 if entry[0][1] is None else int(entry[0][1]),
            ),
        )
        if key[0] == "S":
            return ("S", "S blue", count, None)
        e_number = int(key[1])
        return ("E", f"E{e_number} blue", count, ("blue", e_number))

    def detect(self) -> list[StopAll]:
        s_events = sorted(
            self.s_zones, key=lambda item: (item.source_time, item.source_index)
        )
        s_position = 0
        s_key: str | None = None
        s_count = 0
        e_key: tuple[str, int] | None = None
        e_count = 0
        dominant_s_item: object | None = None
        dominant_e_item: object | None = None
        active: list[StopAll] = []
        output: list[StopAll] = []
        blue_repeat_counts: dict[tuple[str, int | None], int] = {}
        blue_repeat_latest: dict[tuple[str, int | None], object] = {}

        def reset_cycle_blue_repeats() -> None:
            blue_repeat_counts.clear()
            blue_repeat_latest.clear()

        def process_s_event(s_item: object) -> None:
            nonlocal s_key, s_count, e_key, e_count, dominant_s_item, dominant_e_item, active

            reversal = self._opposite_s_stopall_gate(
                s_item, blue_repeat_counts, blue_repeat_latest
            )
            if reversal is not None:
                behavior_type, behavior_key, behavior_count, underlying_e_key = reversal
                zone = self._stopall_from_s(
                    s_item,
                    behavior_type,
                    behavior_key,
                    behavior_count,
                    underlying_e_key,
                )
                output.append(zone)
                # The S-reversal StopAll starts a fresh lifecycle. Historical
                # StopAll objects remain in output, but no pre-boundary active
                # StopAll may influence numbering or ownership in the new cycle.
                active = [zone]
                s_key = e_key = None
                s_count = e_count = 0
                dominant_s_item = None
                dominant_e_item = None
                reset_cycle_blue_repeats()
                return

            color = str(s_item.color)
            # An accepted Red S resolves the pending Blue-repeat reversal
            # opportunity even if its native Order mode cannot promote it.
            # Later Red S may use only Blue occurrences accepted after it.
            if color == "red":
                reset_cycle_blue_repeats()
            if color == "blue":
                self._record_blue_repeat(
                    blue_repeat_counts,
                    blue_repeat_latest,
                    self._blue_repeat_key("S"),
                    s_item,
                )
            incoming_priority = self._sequence_priority("s", color)
            active_priority = self._active_sequence_priority(s_key, e_key)
            if e_key is None and s_key == color:
                s_count += 1
                dominant_s_item = s_item
            elif incoming_priority > active_priority:
                s_key, s_count = color, 1
                dominant_s_item = s_item
                e_key, e_count = None, 0
                dominant_e_item = None

        for e_item in self.e_zones:
            while s_position < len(s_events) and (
                s_events[s_position].source_time < e_item.source_time
            ):
                process_s_event(s_events[s_position])
                s_position += 1

            e_decision = e_item.decision_event_time
            stopped_active = []
            for item in active:
                stop = self._strict_stop(item.decision_event_time, item.price)
                if stop is not None and stop[2] <= e_decision:
                    stopped_active.append((item, stop))
            if stopped_active:
                highest = max(item.number for item, _ in stopped_active)
                gate_event = min(stop[2] for _, stop in stopped_active)
                zone = self._stopall_from_e(
                    e_item, highest + 1, "stopall-stop", gate_event,
                    "StopAll", f"StopAll{highest}", len(stopped_active),
                )
                stopped_ids = {id(item) for item, _ in stopped_active}
                active = [item for item in active if id(item) not in stopped_ids]
                output.append(zone)
                active.append(zone)
                s_key = e_key = None
                s_count = e_count = 0
                dominant_s_item = None
                dominant_e_item = None
                reset_cycle_blue_repeats()
                continue

            new_key = self._e_key(e_item)
            # Once a dominant group has stopped, this E supplies the winning
            # order only. Its family/number need not match the stopped group.
            qualifies_e = e_key is not None and e_count >= 2
            qualifies_s = (
                e_key is None
                and s_key is not None
                and s_count >= 2
            )
            if qualifies_e or qualifies_s:
                parent = max(
                    (
                        item for item in (
                            self.e_zones if qualifies_e else self.s_zones
                        )
                        if item.source_time < e_item.source_time
                        and (
                            self._e_key(item) == e_key if qualifies_e
                            else str(item.color) == s_key
                        )
                    ),
                    key=lambda item: item.source_time,
                )
                gate = self._strict_stop(
                    parent.decision_event_time, as_decimal(parent.price)
                )
                if gate is not None and gate[2] <= e_decision:
                    zone = self._stopall_from_e(
                        e_item, 1, "sequence-group-stop", gate[2],
                        "E" if qualifies_e else "S",
                        (
                            f"E{e_key[1]} {e_key[0]}" if qualifies_e
                            else f"S {s_key}"
                        ),
                        e_count if qualifies_e else s_count,
                    )
                    output.append(zone)
                    active.append(zone)
                    s_key = e_key = None
                    s_count = e_count = 0
                    dominant_s_item = None
                    dominant_e_item = None
                    reset_cycle_blue_repeats()
                    continue

            # Red E resolves earlier Blue-repeat evidence. It may be a
            # higher-stage replacement of Blue, but cannot leave a stale
            # Blue reversal armed for a later unrelated S Red. Do not reset
            # dominant sequence state: E-driven StopAll gates own that state.
            if new_key[0] == "red":
                reset_cycle_blue_repeats()
            # This E remains accepted after independent StopAll checks.
            if new_key[0] == "blue":
                self._record_blue_repeat(
                    blue_repeat_counts,
                    blue_repeat_latest,
                    self._blue_repeat_key("E", new_key[1]),
                    e_item,
                )

            # Stage ownership is A -> S -> E -> StopAll. When the first E
            # replaces an S owner, E starts a new dominant-stage occurrence;
            # the superseded S is not counted again in current-owner sequence
            # state. Pending Blue-repeat counting is independent above.
            if e_key == new_key:
                e_count += 1
                dominant_e_item = e_item
            else:
                incoming_priority = self._sequence_priority("e", new_key[0])
                active_priority = self._active_sequence_priority(s_key, e_key)
                replaces_active = incoming_priority > active_priority
                advances_e = (
                    e_key is not None
                    and incoming_priority == active_priority
                    and self._dominates_e(new_key, e_key)
                )
                if replaces_active or advances_e:
                    e_key, e_count = new_key, 1
                    dominant_e_item = e_item
                    s_key, s_count = None, 0
                    dominant_s_item = None
            # A lower-priority Sequence event remains valid output but cannot
            # replace or separate the active dominant group.

        # The reversal rule is driven by accepted S itself, so it must still
        # fire when the triggering S occurs after the final accepted E.
        while s_position < len(s_events):
            process_s_event(s_events[s_position])
            s_position += 1

        completed = []
        for item in output:
            stop = self._strict_stop(item.decision_event_time, item.price)
            completed.append(
                replace(
                    item,
                    stop_index=stop[0] if stop else None,
                    stop_time=stop[1] if stop else None,
                    stop_event_time=stop[2] if stop else None,
                )
            )
        return completed


def detect_stopalls(
    direction: str,
    s_zones: Sequence[object],
    e_zones: Sequence[object],
    chronology: object,
) -> list[StopAll]:
    return StopAllDetector(direction, s_zones, e_zones, chronology).detect()

# ---------------------------------------------------------------------------
# Cross-stage lifecycle ownership
# ---------------------------------------------------------------------------

def prepare_order_audit(
    detector,
    start_index: int,
    end_index: int,
    s_detector=None,
    accepted_a_sources: set[datetime] | None = None,
    required_identities: set[tuple[int, int]] | None = None,
):
    """Resolve calculation-valid Order Audit identities before serialization.

    Multiple causes may own the same physical ``(FirstIndex, BreakIndex)``
    Order.  This function keeps one identity, merges all accepted provenance,
    applies calculation eligibility, and resolves the canonical stop crossing.
    It intentionally returns native datetimes/prices; JSON formatting remains
    the pipeline serializer's responsibility.
    """
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
        causes: list[dict[str, object]] = []
        for cause in sorted(entry["causes"], key=str):
            if cause[0] == "parent-stop":
                causes.append({
                    "kind": cause[0],
                    "parentType": cause[1],
                    "parentFamily": cause[2],
                    "eventTime": cause[3],
                    "parentSourceTime": cause[4],
                })
            elif cause[0] == "blue-leg":
                causes.append({
                    "kind": "blue-leg",
                    "resetTime": cause[1],
                    "nextBreakoutTime": cause[2],
                    "legLevel": str(cause[3]),
                    "levelSourceIndex": cause[4],
                    "levelSourceTime": cause[5],
                    "blueSourceTime": cause[6],
                    "strictBreakTime": cause[7],
                    "blueFormationEventTime": cause[8],
                    "legStartBreakoutTime": cause[9],
                    "previousBreakoutTime": cause[10],
                })
            else:
                causes.append({
                    "kind": cause[0],
                    "resetTime": cause[1],
                    "boundaryBreakTime": cause[2],
                })
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

    # One exact parent-stop event can open only one physical Order.  Keep the
    # earliest confirmed Order that consumes that parent-stop provenance; a
    # later synthetic/direct reconstruction may still survive if it has an
    # independent cause (for example reset-leg), but it cannot spend the same
    # parent stop a second time.
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
        accepted_causes: list[dict[str, object]] = []
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
    output = deduped_output

    # Internal Reaction geometry remains calculation-valid for direct
    # parent-stop and carried-live Order ownership.  The explicit prohibition
    # is scoped to Reset-leg Order_B: if every accepted cause of this physical
    # Order is reset-leg and the owning Reaction is behavior-internal, reject
    # it.  Cause merging happens first so a valid parent-stop cause cannot be
    # erased by an internal reset-leg provenance on the same identity.
    return [
        item for item in output
        if not (
            str(getattr(item["reaction"], "mode", "")).upper() == "B"
            and bool(getattr(item["reaction"], "behavior_internal", False))
            and item["causes"]
            and all(cause.get("kind") == "reset-leg" for cause in item["causes"])
        )
    ]


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

def resolve_order_context(
    order_audit: dict,
    accepted_a_sources: set[datetime],
    inherited_blocked_first_times: set[datetime],
    invalid_a_zones: Sequence[object],
    pending_s_a_sources: set[datetime],
    opposite_reactions: Sequence[object],
    candles: Sequence[object],
    direction: str,
    stop_finder,
) -> tuple[dict, set[datetime]]:
    """Resolve accepted stopped-A Orders against provisional Order blocks.

    Calculation ownership is authoritative: a canonical Order already accepted
    from stopped-A audit provenance cannot also be vetoed by the provisional
    invalid-leg-head block.  Keep the complete identity-keyed audit entries
    while filtering causes to A sources that remain calculation-eligible.
    """
    accepted_orders = {
        key: accepted
        for key, value in order_audit.items()
        for accepted in [accepted_audit_entry(value, accepted_a_sources)]
        if accepted is not None
    }

    blocked_order_first_times = set(inherited_blocked_first_times)
    blocked_order_first_times.update(
        blocked_orders_while_invalid_leg_heads_are_live(
            [
                item for item in invalid_a_zones
                if getattr(item, "source_time") in pending_s_a_sources
            ],
            opposite_reactions,
            candles,
            direction,
            stop_finder,
        )
    )

    accepted_initial_first_times = {
        getattr(entry["reaction"], "first_time")
        for entry in accepted_orders.values()
    }
    accepted_initial_first_times = {
        datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        if isinstance(value, str) else value
        for value in accepted_initial_first_times
    }
    blocked_order_first_times.difference_update(accepted_initial_first_times)
    return accepted_orders, blocked_order_first_times


def visible_a_zones_after_s_stops(a_zones, s_zones, candles):
    """Suppress the A candle that contains an already-confirmed S stop.

    That candle is the S-stop/E transition candle. It may still carry the
    order box's BoxBottom, but it cannot receive a new A label.
    """
    times = [getattr(item, "timestamp") for item in candles]
    stop_indices = {
        bisect_left(times, getattr(item, "decision_event_time"))
        for item in s_zones
    }
    return [
        item for item in a_zones
        if int(getattr(item, "source_index")) not in stop_indices
    ]

def module_priority(item: object) -> int:
    """Return the confirmed behavioral ownership priority.

    StopAll > E red > S red > E blue > S blue.  A is intentionally absent:
    this helper is used only after A has become an S candidate.
    """
    if hasattr(item, "stopped_behavior_type"):
        return 5
    if hasattr(item, "family"):
        return 4 if str(getattr(item, "family")).lower() == "red" else 2
    if hasattr(item, "a_source_time"):
        return 3 if str(getattr(item, "color")).lower() == "red" else 1
    return 0

def module_identity(item: object) -> tuple[object, ...]:
    return (
        type(item).__name__,
        getattr(item, "family", getattr(item, "color", None)),
        getattr(item, "number", None),
        getattr(item, "source_time"),
        getattr(item, "source_index", None),
    )

def module_stop_event(item: object, stop_event_finder=None) -> datetime | None:
    """Resolve the strict one-second stop event of an S/E/StopAll object."""
    explicit = getattr(item, "stop_event_time", None)
    if explicit is not None:
        return explicit
    if stop_event_finder is None:
        return None
    found = stop_event_finder(item)
    if found is None:
        return None
    if isinstance(found, tuple):
        return found[-1]
    return found

def strictly_beyond_boundary(
    price: Decimal, boundary: Decimal, direction: str,
) -> bool:
    return policy_for(direction).strict_cross(price, boundary)

def dominant_module(modules: Sequence[object]) -> object:
    return max(
        modules,
        key=lambda item: (
            module_priority(item),
            int(getattr(item, "number", 0)),
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )



def split_a_zones_by_dominant_stops(
    a_zones, s_zones, e_zones, stopalls, candles, direction,
    stop_event_finder=None, trend_reactions=None, confirmation_finder=None,
    a_stop_event_finder=None, stage_invalid_a_identities=None,
):
    """Separate visible A labels from A objects allowed into downstream math.

    A/Reaction/Blue discovery remains independent inside every half-leg.  Once
    an accepted S/E/StopAll is strictly stopped, however, the main candle that
    contains that stop begins the next leg comparison.  An A whose source
    extreme is strictly beyond the highest-priority stopped owner is the
    leg-start candidate, but it cannot re-enter calculation as an equal or
    smaller behavior. That candidate consumes the closed owner for subsequent
    half-leg A discovery while remaining absent from the public output.

    Equality is deliberately valid.  Stop chronology is exact at one second,
    while leg ownership is assigned to the containing main candle.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    candle_times = [getattr(item, "timestamp") for item in candles]
    modules = sorted(
        [*s_zones, *e_zones, *stopalls],
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )
    stopped = []
    for module in modules:
        stop_event = module_stop_event(module, stop_event_finder)
        if stop_event is None:
            continue
        stop_index = bisect_right(candle_times, stop_event) - 1
        if stop_index < 0:
            continue
        stopped.append((module, stop_index, stop_event))

    # A is the smallest behavior in the lifecycle hierarchy.  A strict stop
    # therefore owns exactly the next equal/lower transition just like a
    # stopped S/E/StopAll does.  This prevents an A from immediately
    # re-entering after the previous A stop while still consuming the closed
    # owner so a later, genuinely new leg may form normally.
    a_owner_identities = set()
    if a_stop_event_finder is not None:
        for a_owner in a_zones:
            found = a_stop_event_finder(a_owner)
            if found is None:
                continue
            stop_event = found[-1] if isinstance(found, tuple) else found
            stop_index = bisect_right(candle_times, stop_event) - 1
            if stop_index < 0:
                continue
            stopped.append((a_owner, stop_index, stop_event))
            a_owner_identities.add(module_identity(a_owner))

    stop_indices = {
        module_identity(module): stop_index
        for module, stop_index, _stop_event in stopped
    }
    stop_events = {
        module_identity(module): stop_event
        for module, _stop_index, stop_event in stopped
    }

    valid = []
    invalid = []
    consumed = set()
    for a_zone in sorted(
        a_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ),
    ):
        source_index = int(getattr(a_zone, "source_index"))
        eligible = []
        for module, stop_index, _stop_event in stopped:
            identity = module_identity(module)
            if (
                getattr(module, "source_time") >= getattr(a_zone, "source_time")
                or stop_index > source_index
                or identity in consumed
            ):
                continue
            if identity in a_owner_identities:
                # A->A immediate re-entry is defined by chronology, not by a
                # permanent A owner.  If the new A trigger starts only after
                # the previous A strict stop, it belongs to a genuinely new
                # leg and the old A must not block it.  A trigger that starts
                # at/before that stop overlaps the closed A transition and is
                # calculation-invalid.
                trigger_event = getattr(
                    a_zone, "trigger_event_time", getattr(a_zone, "source_time")
                )
                if trigger_event > stop_events[identity]:
                    continue
            eligible.append(module)
        if not eligible:
            valid.append(a_zone)
            continue
        # A historical high-priority E cannot own every later leg forever.
        # The newest main candle containing a strict stop owns the transition;
        # priority and numbering resolve only owners stopped in that candle.
        dominant = max(
            eligible,
            key=lambda item: (
                stop_indices[module_identity(item)],
                module_priority(item),
                int(getattr(item, "number", 0)),
                getattr(item, "source_time"),
                int(getattr(item, "source_index", -1)),
            ),
        )
        crosses_dominant = strictly_beyond_boundary(
            Decimal(str(getattr(a_zone, "price"))),
            Decimal(str(getattr(dominant, "price"))),
            direction,
        )
        if not crosses_dominant:
            valid.append(a_zone)
            continue

        # A confirmed trend Reaction may establish a directional leg head
        # inside the closed owner's range before this A. Preserve that A as an
        # interior-leg behavior, while retaining the existing owner
        # consumption below. This is provenance-based and uses no fixture data.
        interior = False
        if (
            module_identity(dominant) not in a_owner_identities
            and trend_reactions is not None
            and confirmation_finder is not None
            and source_index > 0
            and getattr(a_zone, "reaction_first_time", None) is not None
        ):
            owner_stop = next(
                stop_event for module, stop_index, stop_event in stopped
                if module_identity(module) == module_identity(dominant)
            )
            owner_stop_index = bisect_right(candle_times, owner_stop) - 1
            first_trend_index = bisect_right(
                candle_times, getattr(a_zone, "reaction_first_time")
            ) - 1
            if 0 <= owner_stop_index <= first_trend_index < len(candles):
                extreme_name = "low" if direction == "bullish" else "high"
                head = (
                    min(
                        candles[owner_stop_index:first_trend_index + 1],
                        key=lambda candle: Decimal(str(getattr(candle, extreme_name))),
                    )
                    if direction == "bullish"
                    else max(
                        candles[owner_stop_index:first_trend_index + 1],
                        key=lambda candle: Decimal(str(getattr(candle, extreme_name))),
                    )
                )
                head_extreme = Decimal(str(getattr(head, extreme_name)))
                a_extreme = Decimal(str(getattr(a_zone, "price")))
                if (
                    int(getattr(head, "index", -1)) < source_index
                    and (
                        head_extreme < a_extreme
                        if direction == "bullish"
                        else head_extreme > a_extreme
                    )
                ):
                    interior = any(
                        int(getattr(reaction, "first_idx"))
                        >= int(getattr(head, "index"))
                        and int(getattr(reaction, "first_idx"))
                        <= first_trend_index
                        and int(getattr(reaction, "break_idx")) < source_index
                        and confirmation_finder(reaction, direction)
                        < getattr(a_zone, "source_time")
                        for reaction in trend_reactions
                    )
        if interior:
            valid.append(a_zone)
            # Continue into the common consumption logic below.
            dominant_priority = module_priority(dominant)
            for module in eligible:
                if module_priority(module) <= dominant_priority:
                    consumed.add(module_identity(module))
            continue

        invalid.append(a_zone)
        dominant_priority = module_priority(dominant)
        if hasattr(dominant, "a_source_time"):
            # Stage-order invariant: A -> S -> E -> StopAll.  When S owns the
            # transition, a rejected fallback A cannot consume that S merely
            # by being rejected; otherwise the next A can re-enter behind S
            # and fabricate a second S branch in the same stage.  Keep S as
            # owner until a genuinely later-stage behavior takes ownership.
            if stage_invalid_a_identities is not None:
                stage_invalid_a_identities.add(
                    (getattr(a_zone, "source_time"), int(getattr(a_zone, "source_index")))
                )
            continue
        for module in eligible:
            if module_priority(module) <= dominant_priority:
                consumed.add(module_identity(module))
    return valid, invalid

def blocked_orders_while_invalid_leg_heads_are_live(
    invalid_a_zones, opposite_reactions, candles, direction, stop_finder,
):
    """Return order First times owned by a still-live invalid leg head.

    A strict dominant-boundary crossing can expose a new leg head without
    making its A calculation-valid. Until that head itself stops, an internal
    opposite Reaction cannot take over the larger owner's resumed E space.
    """
    blocked = set()
    for a_zone in invalid_a_zones:
        stop = stop_finder(a_zone)
        if stop is None:
            continue
        stop_event = stop[2]
        source_time = getattr(a_zone, "source_time")
        for reaction in opposite_reactions:
            first_time = getattr(candles[int(getattr(reaction, "first_idx"))], "timestamp")
            if source_time <= first_time < stop_event:
                blocked.add(first_time)
    return blocked


def consumed_s_evidence_after_larger_stop(
    s_candidates, accepted_s_zones, e_zones, direction, stop_event_finder, candles,
):
    """Return the earliest suppressed S evidence that continues each stopped E.

    A lower-priority S remains non-public when it belongs to the continuation
    of the current larger E lifecycle, but its stopped geometry must remain
    available to E.  The parent A must form strictly after the larger E's
    exact stop; an A that straddles that stop belongs to the older handoff and
    cannot advance the E chain.  The source candle must also continue strictly
    beyond the stop-main-candle Close.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    accepted = {
        (getattr(item, "a_source_time"), getattr(item, "source_time"))
        for item in accepted_s_zones
    }
    candle_times = [getattr(item, "timestamp") for item in candles]
    ordered_e = sorted(
        e_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )
    # One suppressed S may be downstream of several historical E objects.
    # Resolve the actual stopped owner at the A leg head, not the most recently
    # *formed* E. A later-formed, smaller E cannot renumber a transition
    # already owned by a larger E stopped in the latest stop-main-candle.
    # Cache exact stop events without changing their lower-timeframe semantics.
    stopped_e = []
    for owner in ordered_e:
        owner_stop = module_stop_event(owner, stop_event_finder)
        if owner_stop is None:
            continue
        stop_index = bisect_right(candle_times, owner_stop) - 1
        if 0 <= stop_index < len(candles):
            stopped_e.append((owner, owner_stop, stop_index))

    earliest_by_owner = {}
    for candidate in sorted(
        s_candidates,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    ):
        identity = (getattr(candidate, "a_source_time"), getattr(candidate, "source_time"))
        if identity in accepted:
            continue
        a_source_time = getattr(candidate, "a_source_time")
        source_index = int(getattr(candidate, "source_index"))
        if not 0 <= source_index < len(candles):
            continue
        source_close = Decimal(str(getattr(candles[source_index], "close")))
        candidate_priority = module_priority(candidate)
        eligible = []
        for owner, owner_stop, stop_index in stopped_e:
            if (
                getattr(owner, "source_time") >= a_source_time
                or owner_stop >= a_source_time
                or candidate_priority >= module_priority(owner)
            ):
                continue
            stop_close = Decimal(str(getattr(candles[stop_index], "close")))
            if not strictly_beyond_boundary(source_close, stop_close, direction):
                continue
            eligible.append((owner, owner_stop, stop_index))
        if not eligible:
            continue
        # The latest accepted E marks the current lifecycle; its formation is
        # not a stop prerequisite for a still-dominant overlapping E.  In
        # particular, a newer *smaller* E cannot prevent a stopped larger E
        # from advancing its own family/number.  An older owner may qualify
        # only if it is strictly higher-ranked and survived beyond the newer
        # E's accepted decision.  Earlier historical stops cannot be revived.
        latest_source = next(
            (item for item in reversed(ordered_e)
             if getattr(item, "source_time") < a_source_time),
            None,
        )
        if latest_source is None:
            continue
        latest_rank = (
            module_priority(latest_source),
            int(getattr(latest_source, "number", 0)),
        )
        latest_qualified = next(
            ((owner, owner_stop, stop_index) for owner, owner_stop, stop_index in eligible
             if owner is latest_source),
            None,
        )
        latest_decision = getattr(
            latest_source, "decision_event_time", latest_source.source_time
        )
        eligible = [
            entry for entry in eligible
            if entry[0] is latest_source
            or (
                (
                    module_priority(entry[0]),
                    int(getattr(entry[0], "number", 0)),
                ) > latest_rank
                and entry[1] > latest_decision
                and (
                    latest_qualified is None
                    or entry[2] >= latest_qualified[2]
                )
            )
        ]
        if not eligible:
            continue
        # Lifecycle ownership first follows the *latest stopped main candle*.
        # Within that boundary use the shared S/E priority and the accepted E
        # number. Neither family priority nor numbering is direction-mirrored.
        owner, _, _ = max(
            eligible,
            key=lambda entry: (
                entry[2],
                module_priority(entry[0]),
                int(getattr(entry[0], "number", 0)),
                getattr(entry[0], "source_time"),
                int(getattr(entry[0], "source_index", -1)),
            ),
        )
        owner_id = module_identity(owner)
        current = earliest_by_owner.get(owner_id)
        if current is None or (
            getattr(candidate, "source_time"), int(getattr(candidate, "source_index", -1))
        ) < (
            getattr(current[0], "source_time"), int(getattr(current[0], "source_index", -1))
        ):
            earliest_by_owner[owner_id] = (candidate, owner)
    return sorted(
        earliest_by_owner.values(),
        key=lambda pair: (
            getattr(pair[0], "source_time"),
            int(getattr(pair[0], "source_index", -1)),
        ),
    )

def s_zones_for_module_engines(s_zones, e_zones, direction):
    """Preserve the established S eligibility contract consumed by E/StopAll."""
    ordered_e = sorted(e_zones, key=lambda item: getattr(item, "source_time"))
    visible = []
    for s_zone in sorted(s_zones, key=lambda item: getattr(item, "source_time")):
        prior_modules = [
            item for item in [*ordered_e, *visible]
            if getattr(item, "source_time") < getattr(s_zone, "source_time")
        ]
        if prior_modules:
            prior = max(prior_modules, key=lambda item: getattr(item, "source_time"))
            # A strictly higher-priority behavior may supersede a lower one;
            # equal or lower priority remains owned by the prior lifecycle.
            # This preserves the original hierarchy contract while allowing
            # Red S to outrank Blue S / Blue E in either market direction.
            if module_priority(s_zone) <= module_priority(prior):
                if getattr(s_zone, "a_source_time") < getattr(prior, "source_time"):
                    continue
                boundary = Decimal(str(getattr(prior, "price")))
                if strictly_beyond_boundary(
                    Decimal(str(getattr(s_zone, "a_price"))), boundary, direction
                ):
                    continue
                if strictly_beyond_boundary(
                    Decimal(str(getattr(s_zone, "price"))), boundary, direction
                ):
                    continue
        visible.append(s_zone)
    return visible

def s_zones_for_stopall(s_zones, e_zones, direction):
    """Return accepted S state that may participate in StopAll grouping.

    E reconciliation still consumes the established S eligibility contract.
    StopAll adds one final same-source rule: when an accepted E owns the same
    physical source as an S candidate, E is final and the losing S must not
    be counted as another sequence member.
    """
    visible = s_zones_for_module_engines(s_zones, e_zones, direction)
    e_sources = {
        (int(getattr(item, "source_index")), getattr(item, "source_time"))
        for item in e_zones
    }
    return [
        item for item in visible
        if (int(getattr(item, "source_index")), getattr(item, "source_time"))
        not in e_sources
    ]

def visible_s_zones_after_module_resets(
    s_zones, e_zones, direction, stop_event_finder=None, source_event_finder=None,
    candles=None,
):
    """Apply dominant-behavior ownership to successive S candidates.

    Bullish/bearish half-leg calculations remain active under a larger
    behavior.  But once the currently dominant S/E/StopAll and the candidate
    S's parent A have both stopped, that A belongs to the next larger module
    lifecycle.  The would-be S is therefore consumed, while its historical
    inputs remain available for chart rendering and audits.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    ordered_external = sorted(
        e_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )
    visible = []
    consumed = set()
    for s_zone in sorted(
        s_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    ):
        a_stop_event = getattr(s_zone, "a_stop_event_time", None)
        ownership_event = a_stop_event
        if direction in {"bullish", "bearish"}:
            # The larger head may stop while the internal S search is open,
            # after A stops but before the candidate's own extreme forms.
            # A later stop after that extreme must not rewrite its ownership.
            ownership_event = (
                source_event_finder(s_zone) if source_event_finder is not None
                else getattr(s_zone, "source_time")
            )
        prior_modules = [
            item for item in [*ordered_external, *visible]
            if getattr(item, "source_time") < getattr(s_zone, "source_time")
            and module_identity(item) not in consumed
        ]
        # A newer E/StopAll source begins the current larger-module lifecycle.
        # Stops belonging to modules sourced before that owner are historical
        # and cannot suppress nested S candidates in the newer lifecycle.
        prior_external = [
            item for item in ordered_external
            if getattr(item, "source_time") < getattr(s_zone, "source_time")
        ]
        if prior_external:
            current_external = max(
                prior_external,
                key=lambda item: (
                    getattr(item, "source_time"),
                    int(getattr(item, "source_index", -1)),
                ),
            )
            lifecycle_start = getattr(current_external, "source_time")
            prior_modules = [
                item for item in prior_modules
                if getattr(item, "source_time") >= lifecycle_start
            ]
        if prior_modules and ownership_event is not None:
            stopped_prior = [
                module for module in prior_modules
                if (
                    module_stop := module_stop_event(module, stop_event_finder)
                ) is not None
                and module_stop <= ownership_event
            ]
            if stopped_prior:
                # A lower-priority S may not re-form inside the next lifecycle
                # of the most recent stopped larger module.  Use the latest
                # stopped E/StopAll owner for this continuation-boundary test;
                # do not let an older, higher-priority historical module steal
                # ownership from the current lifecycle.
                stopped_external = [
                    module for module in stopped_prior
                    if not hasattr(module, "a_source_time")
                ]
                if candles is not None and stopped_external:
                    latest_external = max(
                        stopped_external,
                        key=lambda item: (
                            getattr(item, "source_time"),
                            int(getattr(item, "source_index", -1)),
                        ),
                    )
                    if module_priority(s_zone) < module_priority(latest_external):
                        larger_stop = module_stop_event(
                            latest_external, stop_event_finder
                        )
                        if larger_stop is not None:
                            candle_times = [
                                getattr(candle, "timestamp") for candle in candles
                            ]
                            stop_index = bisect_right(candle_times, larger_stop) - 1
                            source_index = int(getattr(s_zone, "source_index"))
                            if (
                                0 <= stop_index < len(candles)
                                and 0 <= source_index < len(candles)
                            ):
                                stop_close = Decimal(str(
                                    getattr(candles[stop_index], "close")
                                ))
                                source_close = Decimal(str(
                                    getattr(candles[source_index], "close")
                                ))
                                if strictly_beyond_boundary(
                                    source_close, stop_close, direction
                                ):
                                    continue

                # Lifecycle ownership is chronological first.  An old
                # high-priority StopAll/E must not steal the transition from
                # the behavior that stopped most recently before this source.
                # Priority/number only resolve a true same-stop-event tie.
                dominant = max(
                    stopped_prior,
                    key=lambda item: (
                        module_stop_event(item, stop_event_finder),
                        module_priority(item),
                        int(getattr(item, "number", 0)),
                        getattr(item, "source_time"),
                        int(getattr(item, "source_index", -1)),
                    ),
                )
                # A newly confirmed higher-priority S family supersedes a
                # stopped lower-priority owner.  In particular, a Red S must
                # remain visible after a stopped Blue S when its own strict
                # directional extreme is reached.  The existing price/stop
                # consumption rule still applies when the candidate priority
                # is equal or lower, preserving the established lifecycle.
                if (
                    hasattr(s_zone, "a_source_time")
                    and hasattr(dominant, "a_source_time")
                    and module_priority(s_zone) > module_priority(dominant)
                ):
                    visible.append(s_zone)
                    continue
                # A stopped owner advances the lifecycle only when the new S
                # is itself the strict directional extreme of that leg.
                # Equality belongs to the earlier owner and remains valid.
                if not strictly_beyond_boundary(
                    Decimal(str(getattr(s_zone, "price"))),
                    Decimal(str(getattr(dominant, "price"))),
                    direction,
                ):
                    visible.append(s_zone)
                    continue
                # All lower/equal stopped owners involved in this transition
                # leave subsequent calculation ownership together.  The
                # highest-priority object determines the next module number.
                dominant_priority = module_priority(dominant)
                for module in stopped_prior:
                    module_stop = module_stop_event(module, stop_event_finder)
                    if (
                        module_priority(module) <= dominant_priority
                    ):
                        consumed.add(module_identity(module))
                continue
        # An active larger behavior does not disable the independent A/S
        # lifecycle inside the current half-leg.
        visible.append(s_zone)
    return visible

def reconcile_stopall_lifecycle(
    detector, s_zones, e_zones, chronology, direction, timed_step=None
):
    """Freeze StopAll boundaries from the accepted chronological E state.

    StopAll is a hard historical lifecycle boundary.  Once the accepted E/S
    chronology produces a StopAll, future sequence state may not feed back and
    delete or move that already-decided boundary.  The previous global
    fixed-point loop violated that prefix rule: rebuilding E with future reset
    maps could remove an earlier StopAll, then a later pass would recreate it.

    Detect the complete StopAll sequence once from the already reconciled E
    calculation state.  The StopAll detector itself processes events
    chronologically and resets its active sequence whenever a StopAll is
    created, so later StopAll numbers are derived from the hard boundaries in
    the same pass.  Publish the resulting reset map to E for downstream audit
    semantics, but never retroactively rebuild the E prefix from that map.
    """
    measure = timed_step or (lambda _label, work: work())
    visible_s = measure(
        f"Reconcile S visibility - {direction.title()}",
        lambda: s_zones_for_stopall(s_zones, e_zones, direction),
    )
    stopalls = measure(
        f"StopAll - {direction.title()}",
        lambda: detect_stopalls(direction, visible_s, e_zones, chronology),
    )
    detector.sequence_resets = {
        item.source_time: item.number for item in stopalls
    }
    return list(e_zones), stopalls


def visible_a_zones_after_module_boundaries(
    a_zones, s_zones, e_zones, direction, stop_event_finder=None,
):
    """Require A provenance to rebuild after the dominant strict stop.

    A price is deliberately not compared with the old module price.  Reactions
    and Blue Lines remain valid inside every half-leg; only provenance that
    straddles the dominant stop belongs to the closed lifecycle.
    """
    del direction  # Exact-stop ownership is directionally mirrored.
    modules = sorted(
        [*s_zones, *e_zones],
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ),
    )
    valid = []
    for a_zone in sorted(
        a_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ),
    ):
        stopped_prior = [
            module for module in modules
            if getattr(module, "source_time") <= getattr(a_zone, "source_time")
            and (
                stop_event := module_stop_event(module, stop_event_finder)
            ) is not None
            and stop_event <= getattr(a_zone, "source_time")
        ]
        if stopped_prior:
            dominant = dominant_module(stopped_prior)
            boundary_event = module_stop_event(dominant, stop_event_finder)
            provenance_times = (
                getattr(a_zone, "blue_1_source_time"),
                getattr(a_zone, "blue_2_source_time"),
                getattr(a_zone, "continuation_source_time"),
                getattr(a_zone, "reaction_first_time"),
            )
            if min(provenance_times) < boundary_event:
                continue
        valid.append(a_zone)
    return valid

def reaction_number_is_internal(items, number, identities):
    """Return whether a numbered Reaction resolves to a protected internal owner."""
    if number is None:
        return False
    number = int(number)
    if number < 1 or number > len(items):
        return False
    reaction = items[number - 1]
    return order_identity(
        getattr(reaction, "first_idx"),
        getattr(reaction, "break_idx"),
    ) in identities


def order_identity_is_internal(item, internal_identities):
    """Return whether a behavior's physical Order Reaction is internal."""
    first_index = getattr(item, "order_first_index", None)
    break_index = getattr(item, "order_break_index", None)
    if first_index is None or break_index is None:
        return False
    return order_identity(first_index, break_index) in internal_identities


def point_is_inside_healthy_reaction(source_time, price, reactions):
    """Return True only for a strict protected Reaction interior.

    First and published box edges are ownership boundaries, so equality and
    the First timestamp itself remain eligible.
    """
    if source_time is None or price is None:
        return False
    value = as_decimal(price)
    for reaction in reactions:
        first = getattr(reaction, "behavior_first_time", None)
        confirmed = getattr(reaction, "behavior_confirmation_time", None)
        if first is None or confirmed is None:
            continue
        if source_time <= first or source_time > confirmed:
            continue
        bottom = as_decimal(getattr(reaction, "behavior_public_box_bottom"))
        top = as_decimal(getattr(reaction, "behavior_public_box_top"))
        if bottom < value < top:
            return True
    return False


def forbidden_internal_order_b(item, internal_identities):
    """Reject only an internal Reset-leg *Mode-B* Order owner.

    The internal-Reaction prohibition is scoped to Reset-leg Order_B.  A
    Reset-leg provenance can legitimately carry Mode-A geometry after a hard
    lifecycle restart; treating every reset-leg cause as Order_B incorrectly
    deletes valid E/StopAll output. Direct parent-stop and carried-live Orders
    keep their native lifecycle rules as before.
    """
    if str(getattr(item, "order_mode", "")).upper() != "B":
        return False
    if not order_identity_is_internal(item, internal_identities):
        return False
    causes = {str(value) for value in getattr(item, "order_causes", ())}
    return (
        "reset-leg" in causes
        or getattr(item, "order_reset_leg_reset_time", None) is not None
    )


def filter_internal_behavior_outputs(
    a_zones,
    s_zones,
    e_zones,
    stopalls,
    opposite_reactions,
    opposite_internal_identities,
    all_behavior_reactions,
):
    """Apply only the scoped Internal-Reaction Order_B prohibition.

    Internal Reaction geometry and its eligible evidence remain calculation
    valid.  A/S/E/StopAll are not hidden merely because their source point lies
    inside a healthy Reaction interior, and an S is not rejected merely because
    a referenced Reset Reaction is internal.  The explicit prohibition that
    remains is an internal Reset-leg Mode-B Order_B owner for E/StopAll.
    """
    del opposite_reactions, all_behavior_reactions
    visible_a = list(a_zones)
    visible_s = list(s_zones)
    visible_e = [
        item for item in e_zones
        if not forbidden_internal_order_b(item, opposite_internal_identities)
    ]
    visible_stopalls = [
        item for item in stopalls
        if not forbidden_internal_order_b(item, opposite_internal_identities)
    ]
    return visible_a, visible_s, visible_e, visible_stopalls

def finalize_behavior_visibility(
    a_zones,
    s_zones,
    e_zones,
    stopalls,
    direction,
    invalid_s_identities,
    stop_event_finder,
    source_event_finder,
    candles,
    *,
    all_a_zones=None,
):
    """Resolve the final A/S/E lineage closure after StopAll reconciliation."""
    stopall_source_indices = {int(item.source_index) for item in stopalls}
    final_e_zones = [
        item for item in e_zones
        if int(getattr(item, "source_index")) not in stopall_source_indices
    ]
    e_source_indices = {
        int(getattr(item, "source_index")) for item in final_e_zones
    }
    final_s_zones = visible_s_zones_after_module_resets(
        s_zones,
        [*final_e_zones, *stopalls],
        direction,
        stop_event_finder,
        source_event_finder=source_event_finder,
        candles=candles,
    )

    # Presentation is a lineage closure over accepted calculations. If a final
    # E references an S parent, retain that historical S even if it no longer
    # owns downstream lifecycle calculation.
    referenced_s_sources = {
        getattr(item, "parent_source_time")
        for item in final_e_zones
        if str(getattr(item, "parent_type", "")).upper() == "S"
    }
    final_s_identities = {module_identity(item) for item in final_s_zones}
    final_s_zones.extend(
        item for item in s_zones
        if getattr(item, "source_time") in referenced_s_sources
        and module_identity(item) not in final_s_identities
    )
    final_s_zones.sort(
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        )
    )

    final_a_zones = visible_a_zones_after_module_boundaries(
        a_zones,
        final_s_zones,
        [*final_e_zones, *stopalls],
        direction,
        stop_event_finder,
    )
    referenced_a_sources = {getattr(item, "a_source_time") for item in final_s_zones}
    lineage_a_zones = a_zones if all_a_zones is None else all_a_zones
    final_a_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in final_a_zones
    }
    final_a_zones.extend(
        item for item in lineage_a_zones
        if getattr(item, "source_time") in referenced_a_sources
        and (
            getattr(item, "source_time"), int(getattr(item, "source_index"))
        ) not in final_a_identities
    )
    final_a_zones.sort(
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        )
    )

    occupied = e_source_indices | stopall_source_indices
    final_a_zones = [
        item for item in final_a_zones
        if int(getattr(item, "source_index")) not in occupied
    ]
    final_s_zones = [
        item for item in final_s_zones
        if int(getattr(item, "source_index")) not in occupied
        and (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ) not in invalid_s_identities
    ]
    return final_e_zones, final_s_zones, final_a_zones


def visible_a_zones(a_zones: Sequence[object], s_zones: Sequence[object]) -> list[object]:
    """Return A objects whose source candle is not occupied by a final S."""
    occupied = {int(getattr(item, "source_index")) for item in s_zones}
    return [
        item for item in a_zones
        if int(getattr(item, "source_index")) not in occupied
    ]
