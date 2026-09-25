---
id: "source.state_map"
type: "source"
status: "active"
authority: "executable"
title: "State and ownership map"
implements: ["algorithm.raw", "algorithm.reaction", "algorithm.s", "algorithm.e", "algorithm.stopall"]
source_refs: ["engine/bridge/trading_pipeline.py#L1698", "engine/bridge/trading_pipeline.py#L1903"]
---

# State and ownership map

| Owner | State | Lifetime / authority |
| --- | --- | --- |
| bridge.MarketContext | complete received main/lower candles, shared lower index, chronology, presentation start/end indexes | one request |
| bridge.PipelineState | both Reaction streams; per-direction full Blue/A/S/E and invalid identity sets; detector references | one request, shared across direction serialization |
| bridge.FullDirectionState | authoritative full-range E/S/Blue/A and detector context | one direction, before presentation |
| reaction_engine.UnifiedReactionDetector | Mode A/B candidate, confirmed boundary, Reset/direct recovery | one directional detection |
| reaction_engine.LowerTimeframeIndex / MarketChronology | first crossing and range extrema, confirmation/Reset/Order stop chronology caches | immutable candle input |
| blue_line_detector | pending strike, previous strike count, Blue spacing and validity | one direction |
| a_zone_detector.AZoneDetector | sorted Blue states, pair trigger/cycle, special route | one direction |
| s_zone_detector.SZoneDetector | A ownership windows, sorted opposite Orders, Reset/Blue event indexes, initial stopped-A order_audit | one direction/run |
| e_zone_detector.EZoneDetector | physical Order ledger, B/C formation caches, candidate chain/active state, sequence boundaries, historical rescues | one E pass; rebuilt when accepted inputs change |
| lifecycle_engine.StopAllDetector | dominant S/E group counts, active StopAll, independent pending exact Blue-repeat counts | final reconciled pass |

Caches are performance structures; their source ordering and first-event tie semantics must be retained. E historical rescues are display-only and do not own active E/StopAll state. accepted-live/carried-live are Order use provenance, never creation ownership. Module-level bridge time-conversion caches are process-local; they do not make prior RAW history available to a later request.
