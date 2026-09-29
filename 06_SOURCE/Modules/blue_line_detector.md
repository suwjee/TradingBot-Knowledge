---
id: "source.blue_line_detector"
type: "source"
status: "active"
authority: "executable"
title: "Scale and Reset Blue construction and public/calculation-valid Blue ownership"
version: "2.3.0"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/blue_line_detector.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/blue_line_detector.py"
mirror: "06_SOURCE/Code/engine/pipeline/blue_line_detector.py"
sha256: "6fa01d94bc98060b62bc7e68db0ec24a0b0159727d44043affee7130a9c11448"
---

# blue_line_detector.py

Scale and Reset Blue construction and public/calculation-valid Blue ownership.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/blue_line_detector.py |
| SHA-256 | 6fa01d94bc98060b62bc7e68db0ec24a0b0159727d44043affee7130a9c11448 |
| Bytes | 15802 |
| Lines | 458 |
| Declared version | 2.3.0 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| ScaleStrike | 23 | 26 | class |
| BlueLine | 30 | 45 | class |
| _is_color | 48 | 49 | candle: object, color: str |
| _main_candle | 52 | 56 | candles_by_index: dict[int, object], index: int |
| _stops_on_index | 59 | 72 | direction: str, line: object, candles: Sequence[object], start_index: int, end_index: int |
| fibonacci_level | 75 | 81 | direction: str, reaction: object, reference: Decimal |
| _intrabar_pending_confirmation | 84 | 136 | direction: str, chronology: object, reaction: object, comparison_extreme: Decimal, start_time: datetime, break_time: datetime, candles_by_index: dict[int, object] |
| count_scale_strikes | 139 | 204 | direction: str, reaction: object, chronology: object, reference: Decimal, candles_by_index: dict[int, object] \| None=None |
| _build_scale_blue_line | 207 | 242 | direction: str, reaction_number: int, previous_count: int, level: Decimal, strikes: Sequence[ScaleStrike], candles_by_index: dict[int, object], chronology: object, behavior_internal: bool |
| _build_reset_blue_line | 245 | 297 | direction: str, reaction_number: int, reset: object, previous_line: BlueLine \| None, candles: Sequence[object], candles_by_index: dict[int, object], chronology: object, behavior_internal: bool |
| detect_blue_lines | 299 | 404 | direction: str, reactions: Sequence[object], chronology: object, resets: Sequence[object]=() |
| public_blue_lines | 407 | 414 | lines: Sequence[BlueLine] |
| mark_internal_blue_lines | 416 | 458 | lines: Sequence[BlueLine], owner_reactions: Sequence[object], all_behavior_reactions: Sequence[object] |
| mark_internal_blue_lines.owner_is_internal | 429 | 433 | line: BlueLine |
| mark_internal_blue_lines.geometry_is_internal | 435 | 454 | line: BlueLine |
