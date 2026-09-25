---
id: "source.trading_pipeline"
type: "source"
status: "active"
authority: "executable"
title: "trading pipeline"
source_path: "engine/bridge/trading_pipeline.py"
mirror: "06_SOURCE/Code/engine/bridge/trading_pipeline.py"
sha256: "a14b00ef08e3e97260b856ffe0dab8044cc70026d272e08e3d4350e9cff249cd"
implements: ["algorithm.raw", "algorithm.reconciliation", "algorithm.visibility", "algorithm.serialization", "algorithm.orderaudit"]
affects: ["behavior.a", "behavior.s", "behavior.e", "behavior.stopall"]
source_refs: ["engine/bridge/trading_pipeline.py#L1"]
orchestrates: ["algorithm.reaction", "algorithm.blue", "algorithm.a", "algorithm.s", "algorithm.e", "algorithm.lifecycle", "algorithm.stopall"]
---

# trading pipeline
## Identity and snapshot
Production: engine/bridge/trading_pipeline.py
Mirror: 06_SOURCE/Code/engine/bridge/trading_pipeline.py
SHA-256: a14b00ef08e3e97260b856ffe0dab8044cc70026d272e08e3d4350e9cff249cd
Declared versions: [('TRADING_PIPELINE_VERSION', '1.5.1')]

## Responsibility
Owns CLI, dynamic module loading, supplied RAW normalization, both-direction Reaction preparation, repeated full-direction stage passes, final visibility, bridge projection and JSON serialization.

## Classes and owned concepts
BridgeProjection (L652), EngineBundle (L1607), MarketContext (L1617), PipelineState (L1813), FullDirectionState (L1833), DirectionRangeState (L2417), DirectionVisibilityState (L2430)

## Important symbols
- build_candle_buckets: engine/bridge/trading_pipeline.py#L120
- load_engines: engine/bridge/trading_pipeline.py#L1698
- prepare_market_context: engine/bridge/trading_pipeline.py#L1732
- prepare_pipeline_state: engine/bridge/trading_pipeline.py#L2300
- calculate_full_direction_state: engine/bridge/trading_pipeline.py#L1903
- finalize_direction_visibility: engine/bridge/trading_pipeline.py#L2549
- serialize_direction_payload: engine/bridge/trading_pipeline.py#L2776
- build_bridge_output: engine/bridge/trading_pipeline.py#L1364
- build_response_payload: engine/bridge/trading_pipeline.py#L2942

## Inputs and outputs
CLI args plus supplied JSON -> versioned direction collections, bridge views, QG_PROGRESS and timings.

## State, direction, chronology, and invariants
PipelineState stores both Reaction streams and per-direction Blue/A/S/E, invalid identities and detectors. E may rebuild as upstream eligibility settles; StopAll runs after reconciliation. from/to are presentation bounds for complete received input.

## Upstream dependencies and downstream consumers
Upstream: RAW JSON; all engine/pipeline modules.

Downstream: JSON/stdout to Vite and chart, QG_PROGRESS/stderr to middleware.

## Relationships
Direct implementation ownership: algorithm.raw, algorithm.reconciliation, algorithm.visibility, algorithm.serialization; current non-canonical algorithm.orderaudit serialization/validation. Orchestrates algorithm.reaction, algorithm.blue, algorithm.a, algorithm.s, algorithm.e, algorithm.lifecycle, and algorithm.stopall without owning their detector rules.
Behaviors: behavior.a behavior.s behavior.e behavior.stopall.
