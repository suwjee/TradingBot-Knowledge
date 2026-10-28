---
id: "source.reaction_engine"
type: "source"
status: "active"
authority: "executable"
title: "Reaction, Reset, reflected direction geometry, exact lower-timeframe chronology and internal Reaction classification"
version: "9.8.1"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/reaction_engine.py"
sha256: "f62f7e3c6480750068c4550a8489806030aac16f021f349930bd5efb3ce54198"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# reaction_engine.py

Reaction, Reset, reflected direction geometry, exact lower-timeframe chronology and internal Reaction classification.

Exact bytes describe executable behavior; Source identity is not intended-semantic authority or independent market correctness. Supported dynamic Bridge loading and the maintained pipeline compatibility wrapper are distinct runtime surfaces. The manifest source_scope bounds audit/reconstruction completeness.

## Snapshot identity

| Property | Current captured evidence |
| --- | --- |
| Source | 06_SOURCE/Code/engine/pipeline/reaction_engine.py |
| SHA-256 | f62f7e3c6480750068c4550a8489806030aac16f021f349930bd5efb3ce54198 |
| Bytes | 105073 |
| Lines | 2439 |
| Declared version | 9.8.1 |

## Lexical Source symbols

Every lexical definition in this captured owner is indexed mechanically, including incidental out-of-scope feature helpers. A symbol row is navigation, not a separate concept or semantic approval.

| Symbol | Line | End |
| --- | ---: | ---: |
| Candle | 30 | 38 |
| Candidate | 42 | 66 |
| ResetEvent | 70 | 75 |
| IntrabarAnalysis | 79 | 82 |
| DetectionResult | 86 | 91 |
| classify_candle_color | 94 | 96 |
| opposite_direction | 99 | 101 |
| DetectorBase | 104 | 174 |
| DetectorBase.__init__ | 105 | 127 |
| DetectorBase._shared_time_index | 130 | 138 |
| DetectorBase.seconds_between | 140 | 143 |
| DetectorBase.main_source_for_time | 145 | 156 |
| DetectorBase.minimum_low | 158 | 165 |
| DetectorBase.maximum_high | 167 | 174 |
| BullishDetector | 177 | 560 |
| BullishDetector.green_run_peak_before | 178 | 186 |
| BullishDetector.breakout_analysis | 188 | 212 |
| BullishDetector.mode_a_invalidation_before_breakout | 214 | 248 |
| BullishDetector.confirmed_reset_before_breakout | 250 | 268 |
| BullishDetector.post_breakout_reset | 270 | 283 |
| BullishDetector.detect | 285 | 560 |
| mirror_candle | 563 | 580 |
| mirror_candidate | 583 | 600 |
| mirror_analysis | 602 | 608 |
| _ReflectedCandles | 611 | 633 |
| _ReflectedCandles.__init__ | 619 | 621 |
| _ReflectedCandles.__len__ | 623 | 624 |
| _ReflectedCandles.__getitem__ | 626 | 633 |
| _reflected_view | 639 | 646 |
| BearishDetector | 649 | 706 |
| BearishDetector.__init__ | 657 | 669 |
| BearishDetector.red_run_bottom_before | 671 | 673 |
| BearishDetector.breakdown_analysis | 675 | 678 |
| BearishDetector.invalidation_high_break_before_breakdown | 680 | 683 |
| BearishDetector.confirmed_reset_before_breakdown | 685 | 689 |
| BearishDetector.post_breakdown_reset | 691 | 696 |
| BearishDetector.detect | 698 | 706 |
| published_reaction_candidate | 709 | 804 |
| _decimal_value | 807 | 809 |
| LowerTimeframeIndex | 812 | 929 |
| LowerTimeframeIndex.__init__ | 819 | 858 |
| LowerTimeframeIndex.first_less | 860 | 861 |
| LowerTimeframeIndex.first_greater | 863 | 864 |
| LowerTimeframeIndex.range_minimum | 866 | 868 |
| LowerTimeframeIndex.range_maximum | 870 | 872 |
| LowerTimeframeIndex._range_query | 874 | 910 |
| LowerTimeframeIndex._first | 912 | 929 |
| shared_lower_timeframe_index | 937 | 947 |
| ReflectedLowerTimeframeIndex | 950 | 971 |
| ReflectedLowerTimeframeIndex.__init__ | 955 | 957 |
| ReflectedLowerTimeframeIndex.first_less | 959 | 960 |
| ReflectedLowerTimeframeIndex.first_greater | 962 | 963 |
| ReflectedLowerTimeframeIndex.range_minimum | 965 | 967 |
| ReflectedLowerTimeframeIndex.range_maximum | 969 | 971 |
| MarketChronology | 974 | 1202 |
| MarketChronology.__init__ | 993 | 1013 |
| MarketChronology.opposite_direction | 1016 | 1018 |
| MarketChronology.main_index | 1020 | 1027 |
| MarketChronology.lower_bounds | 1029 | 1038 |
| MarketChronology.lower_window | 1040 | 1044 |
| MarketChronology._reset_cache_key | 1047 | 1056 |
| MarketChronology._reaction_cache_key | 1059 | 1071 |
| MarketChronology.reset_time | 1073 | 1090 |
| MarketChronology.reaction_confirmation | 1092 | 1137 |
| MarketChronology.canonical_order_stop | 1140 | 1202 |
| build_behavior_reaction_views | 1205 | 1313 |
| build_behavior_reaction_views.path_is_contained | 1225 | 1243 |
| directional_a_stop_order_finder | 1316 | 1376 |
| directional_a_stop_order_finder.find | 1330 | 1374 |
| UnifiedReactionDetector | 1379 | 2437 |
| UnifiedReactionDetector.__init__ | 1389 | 1418 |
| UnifiedReactionDetector.bull | 1421 | 1426 |
| UnifiedReactionDetector.bear | 1429 | 1434 |
| UnifiedReactionDetector._append_reaction | 1436 | 1516 |
| UnifiedReactionDetector._append_reset | 1518 | 1534 |
| UnifiedReactionDetector._refine | 1536 | 1555 |
| UnifiedReactionDetector._candidate_from_confirmation_remainder | 1557 | 1640 |
| UnifiedReactionDetector._first_initial | 1642 | 1652 |
| UnifiedReactionDetector._first_direct_same_direction_after_reset | 1655 | 1691 |
| UnifiedReactionDetector._first_geometry_after_reset | 1693 | 1744 |
| UnifiedReactionDetector.first_geometry_after_reset | 1746 | 1750 |
| UnifiedReactionDetector._reaction_break_indices | 1753 | 1766 |
| UnifiedReactionDetector.first_order_reaction_after_gate | 1768 | 1915 |
| UnifiedReactionDetector.first_order_reaction_after_gate.cache_result | 1784 | 1793 |
| UnifiedReactionDetector.first_order_reaction_after_gate.confirmed_no_later_than_gate | 1795 | 1813 |
| UnifiedReactionDetector._earliest_confirmed_geometry | 1917 | 1989 |
| UnifiedReactionDetector._build_direct_candidate | 1991 | 2046 |
| UnifiedReactionDetector._scan_direct_candidate | 2049 | 2077 |
| UnifiedReactionDetector._owner_boundary_before_confirmation | 2079 | 2117 |
| UnifiedReactionDetector._result | 2120 | 2127 |
| UnifiedReactionDetector.detect | 2129 | 2437 |
