---
id: "source.lifecycle_engine"
type: "source"
status: "active"
authority: "executable"
title: "Lifecycle ownership, StopAll gates, retained calculation lineage and final visibility"
version: "1.18.6"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py"
sha256: "760928f5480efad446b42bc6aa2fbea3e431de13ab92714bac05c09188519c26"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# lifecycle_engine.py

Lifecycle ownership, StopAll gates, retained calculation lineage and final visibility.

Exact bytes describe executable behavior; Source identity is not intended-semantic authority or independent market correctness. Supported dynamic Bridge loading and the maintained pipeline compatibility wrapper are distinct runtime surfaces. The manifest source_scope bounds audit/reconstruction completeness.

## Snapshot identity

| Property | Current captured evidence |
| --- | --- |
| Source | 06_SOURCE/Code/engine/pipeline/lifecycle_engine.py |
| SHA-256 | 760928f5480efad446b42bc6aa2fbea3e431de13ab92714bac05c09188519c26 |
| Bytes | 63174 |
| Lines | 1529 |
| Declared version | 1.18.6 |

## Lexical Source symbols

Every lexical definition in this captured owner is indexed mechanically, including incidental out-of-scope feature helpers. A symbol row is navigation, not a separate concept or semantic approval.

| Symbol | Line | End |
| --- | ---: | ---: |
| sequence_priority | 37 | 39 |
| StopAll | 43 | 92 |
| _DominantBehavior | 96 | 118 |
| _DominantBehavior.priority | 106 | 107 |
| _DominantBehavior.armed | 110 | 111 |
| _DominantBehavior.key | 114 | 118 |
| advance_dominant_behavior | 121 | 139 |
| StopAllDetector | 142 | 527 |
| StopAllDetector.__init__ | 143 | 162 |
| StopAllDetector._strict_stop | 164 | 178 |
| StopAllDetector._dominates_e | 181 | 188 |
| StopAllDetector._stopall_from_e | 190 | 246 |
| StopAllDetector._optional_int | 249 | 250 |
| StopAllDetector._optional_decimal | 253 | 254 |
| StopAllDetector._stopall_from_s | 256 | 342 |
| StopAllDetector.detect | 344 | 527 |
| StopAllDetector.detect.armed_stop_before | 356 | 404 |
| StopAllDetector.detect.accept | 406 | 408 |
| StopAllDetector.detect.process_s_event | 410 | 461 |
| detect_stopalls | 530 | 536 |
| resolve_order_context | 543 | 629 |
| visible_a_zones_after_s_stops | 632 | 647 |
| module_priority | 649 | 661 |
| module_identity | 663 | 670 |
| module_stop_event | 672 | 684 |
| strictly_beyond_boundary | 686 | 689 |
| dominant_module | 691 | 700 |
| split_a_zones_by_dominant_stops | 703 | 904 |
| blocked_orders_while_invalid_leg_heads_are_live | 906 | 926 |
| consumed_s_evidence_after_larger_stop | 929 | 1069 |
| s_zones_for_module_engines | 1071 | 1099 |
| s_zones_for_stopall | 1101 | 1118 |
| visible_s_zones_after_module_resets | 1120 | 1296 |
| visible_s_zones_after_module_resets.cached_stop_event | 1149 | 1153 |
| reconcile_stopall_lifecycle | 1298 | 1328 |
| visible_a_zones_after_module_boundaries | 1331 | 1376 |
| reaction_number_is_internal | 1378 | 1389 |
| point_is_inside_healthy_reaction | 1392 | 1412 |
| filter_internal_behavior_outputs | 1415 | 1426 |
| finalize_behavior_visibility | 1428 | 1520 |
| visible_a_zones | 1523 | 1529 |
