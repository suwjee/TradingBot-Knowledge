---
id: "source.reaction_engine"
type: "source"
status: "active"
authority: "executable"
title: "Reaction, Reset, reflected direction geometry, exact lower-timeframe chronology and internal Reaction classification"
version: "9.8.0"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
sha256: "bea0d5a5e95ee15ad54d024f6c01b8c777ba2abcc3c8e671118f1ae2df28f2a6"
---

# reaction_engine.py

Reaction, Reset, reflected direction geometry, exact lower-timeframe chronology and internal Reaction classification.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/reaction_engine.py |
| SHA-256 | bea0d5a5e95ee15ad54d024f6c01b8c777ba2abcc3c8e671118f1ae2df28f2a6 |
| Bytes | 103120 |
| Lines | 2406 |
| Declared version | 9.8.0 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| Candle | 27 | 35 | class |
| Candidate | 39 | 63 | class |
| ResetEvent | 67 | 72 | class |
| IntrabarAnalysis | 76 | 79 | class |
| DetectionResult | 83 | 88 | class |
| classify_candle_color | 91 | 93 | open_price: Decimal, close_price: Decimal |
| opposite_direction | 96 | 98 | direction: str |
| DetectorBase | 101 | 171 | class |
| DetectorBase.__init__ | 102 | 124 | self, candles: Sequence[Candle], one_second_candles: Sequence[Candle], start_index: int, end_index: int |
| DetectorBase._shared_time_index | 127 | 135 | candles: Sequence[Candle] |
| DetectorBase.seconds_between | 137 | 140 | self, start: datetime, end: datetime |
| DetectorBase.main_source_for_time | 142 | 153 | self, timestamp: datetime |
| DetectorBase.minimum_low | 155 | 162 | self, start_index: int, end_index: int |
| DetectorBase.maximum_high | 164 | 171 | self, start_index: int, end_index: int |
| BullishDetector | 174 | 557 | class |
| BullishDetector.green_run_peak_before | 175 | 183 | self, first_red_index: int |
| BullishDetector.breakout_analysis | 185 | 209 | self, candidate: Candidate, breakout_candle: Candle |
| BullishDetector.mode_a_invalidation_before_breakout | 211 | 245 | self, candidate: Candidate, candle: Candle |
| BullishDetector.confirmed_reset_before_breakout | 247 | 265 | self, candidate: Candidate \| None, candle: Candle, confirmed_bottom: Decimal |
| BullishDetector.post_breakout_reset | 267 | 280 | self, analysis: IntrabarAnalysis \| None, box_bottom: Decimal, breakout_candle: Candle |
| BullishDetector.detect | 282 | 557 | self, *, first_only: bool=False |
| mirror_candle | 560 | 577 | candle: Candle |
| mirror_candidate | 580 | 597 | candidate: Candidate \| None |
| mirror_analysis | 599 | 605 | analysis: IntrabarAnalysis \| None |
| _ReflectedCandles | 608 | 630 | class |
| _ReflectedCandles.__init__ | 616 | 618 | self, source: Sequence[Candle] |
| _ReflectedCandles.__len__ | 620 | 621 | self |
| _ReflectedCandles.__getitem__ | 623 | 630 | self, index |
| _reflected_view | 636 | 643 | source: Sequence[Candle] |
| BearishDetector | 646 | 703 | class |
| BearishDetector.__init__ | 654 | 666 | self, candles, one_second_candles, start_index, end_index |
| BearishDetector.red_run_bottom_before | 668 | 670 | self, first_green_index |
| BearishDetector.breakdown_analysis | 672 | 675 | self, candidate, breakdown_candle |
| BearishDetector.invalidation_high_break_before_breakdown | 677 | 680 | self, candidate, candle |
| BearishDetector.confirmed_reset_before_breakdown | 682 | 686 | self, candidate, candle, confirmed_top |
| BearishDetector.post_breakdown_reset | 688 | 693 | self, analysis, box_top, breakdown_candle |
| BearishDetector.detect | 695 | 703 | self, *, first_only: bool=False |
| published_reaction_candidate | 706 | 801 | direction: str, candidate: Candidate, chronology: object |
| _decimal_value | 804 | 806 | value: object |
| LowerTimeframeIndex | 809 | 926 | class |
| LowerTimeframeIndex.__init__ | 816 | 855 | self, candles: Sequence[Candle] |
| LowerTimeframeIndex.first_less | 857 | 858 | self, left: int, right: int, level: Decimal |
| LowerTimeframeIndex.first_greater | 860 | 861 | self, left: int, right: int, level: Decimal |
| LowerTimeframeIndex.range_minimum | 863 | 865 | self, left: int, right: int |
| LowerTimeframeIndex.range_maximum | 867 | 869 | self, left: int, right: int |
| LowerTimeframeIndex._range_query | 871 | 907 | self, left: int, right: int, *, minimum: bool |
| LowerTimeframeIndex._first | 909 | 926 | self, node: int, start: int, end: int, left: int, right: int, level: Decimal, less: bool |
| shared_lower_timeframe_index | 934 | 944 | candles: Sequence[Candle] |
| ReflectedLowerTimeframeIndex | 947 | 968 | class |
| ReflectedLowerTimeframeIndex.__init__ | 952 | 954 | self, base: LowerTimeframeIndex |
| ReflectedLowerTimeframeIndex.first_less | 956 | 957 | self, left: int, right: int, level: Decimal |
| ReflectedLowerTimeframeIndex.first_greater | 959 | 960 | self, left: int, right: int, level: Decimal |
| ReflectedLowerTimeframeIndex.range_minimum | 962 | 964 | self, left: int, right: int |
| ReflectedLowerTimeframeIndex.range_maximum | 966 | 968 | self, left: int, right: int |
| MarketChronology | 971 | 1199 | class |
| MarketChronology.__init__ | 990 | 1010 | self, candles: Sequence[Candle], seconds: Sequence[Candle], timeframe_seconds: int, lower_index: LowerTimeframeIndex \| None=None |
| MarketChronology.opposite_direction | 1013 | 1015 | direction: str |
| MarketChronology.main_index | 1017 | 1024 | self, timestamp: datetime, *, clamp: bool=False |
| MarketChronology.lower_bounds | 1026 | 1035 | self, start: datetime, end: datetime \| None=None |
| MarketChronology.lower_window | 1037 | 1041 | self, start: datetime, end: datetime \| None=None |
| MarketChronology._reset_cache_key | 1044 | 1053 | reset: object |
| MarketChronology._reaction_cache_key | 1056 | 1068 | reaction: object, direction: str, use_intrabar_start: bool |
| MarketChronology.reset_time | 1070 | 1087 | self, reset: object |
| MarketChronology.reaction_confirmation | 1089 | 1134 | self, direction: str, reaction: object, *, use_intrabar_start: bool=True |
| MarketChronology.canonical_order_stop | 1137 | 1199 | self, order_direction: str, reaction_number: int, reaction: object, opposite_reactions: Sequence[object], *, start_index: int=0 |
| build_behavior_reaction_views | 1202 | 1310 | full_results: dict[str, object], chronology: MarketChronology |
| build_behavior_reaction_views.path_is_contained | 1222 | 1240 | first_time: datetime, confirmed_at: datetime, bottom: Decimal, top: Decimal |
| directional_a_stop_order_finder | 1313 | 1373 | candles: Sequence[Candle], seconds: Sequence[Candle], direction: str |
| directional_a_stop_order_finder.find | 1327 | 1371 | gate_index: int, gate_event: datetime, end_index: int |
| UnifiedReactionDetector | 1376 | 2404 | class |
| UnifiedReactionDetector.__init__ | 1386 | 1408 | self, candles: Sequence[Candle], one_second_candles: Sequence[Candle], start_index: int, end_index: int, output_direction: str |
| UnifiedReactionDetector.bull | 1411 | 1416 | self |
| UnifiedReactionDetector.bear | 1419 | 1424 | self |
| UnifiedReactionDetector._append_reaction | 1426 | 1506 | self, direction: str, candidate: Candidate |
| UnifiedReactionDetector._append_reset | 1508 | 1524 | self, direction: str, candle: Candle, level: Decimal, first_idx: int, second_time: str \| None=None |
| UnifiedReactionDetector._refine | 1526 | 1545 | self, direction: str, candidate: Candidate, candle: Candle |
| UnifiedReactionDetector._candidate_from_confirmation_remainder | 1547 | 1630 | self, direction: str, confirmed: Candidate, candle: Candle, analysis: IntrabarAnalysis \| None |
| UnifiedReactionDetector._first_initial | 1632 | 1642 | self, direction: str |
| UnifiedReactionDetector._first_direct_same_direction_after_reset | 1645 | 1681 | self, direction: str, reset_index: int |
| UnifiedReactionDetector._first_geometry_after_reset | 1683 | 1734 | self, direction: str, reset_index: int, end_index: int \| None=None |
| UnifiedReactionDetector.first_geometry_after_reset | 1736 | 1740 | self, direction: str, reset_index: int, end_index: int |
| UnifiedReactionDetector._reaction_break_indices | 1743 | 1756 | self, direction: str |
| UnifiedReactionDetector.first_order_reaction_after_gate | 1758 | 1890 | self, direction: str, gate_index: int, end_index: int \| None=None, gate_event_time: datetime \| None=None |
| UnifiedReactionDetector.first_order_reaction_after_gate.confirmed_no_later_than_gate | 1770 | 1788 | reaction: Candidate |
| UnifiedReactionDetector._earliest_confirmed_geometry | 1892 | 1964 | self, direction: str, start_index: int, end_index: int \| None=None |
| UnifiedReactionDetector._build_direct_candidate | 1966 | 2021 | self, direction: str, reset_index: int, first_index: int |
| UnifiedReactionDetector._scan_direct_candidate | 2024 | 2052 | self, direction: str, candidate: Candidate, stop_index: int |
| UnifiedReactionDetector._owner_boundary_before_confirmation | 2054 | 2092 | self, direction: str, candidate: Candidate, candle: Candle |
| UnifiedReactionDetector._result | 2095 | 2102 | self |
| UnifiedReactionDetector.detect | 2104 | 2404 | self, *, stop_after_first_at_or_after: int \| None=None |
