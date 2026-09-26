---
id: "source.trading_pipeline"
type: "source"
status: "active"
authority: "executable"
title: "Bridge orchestration and serialization: mixed source evidence"
source_path: "06_SOURCE/Code/engine/bridge/trading_pipeline.py"
mirror: "06_SOURCE/Code/engine/bridge/trading_pipeline.py"
sha256: "a14b00ef08e3e97260b856ffe0dab8044cc70026d272e08e3d4350e9cff249cd"
implementation_validity: "mixed"
affected_by_known_invalid_order_route: true
implements: ["algorithm.raw", "algorithm.reconciliation", "algorithm.serialization", "algorithm.visibility"]
source_refs: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py#L77", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L120", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L1903", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L2549"]
related_entities: ["test.source_validation"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py#L77"]
---

# Bridge orchestration and serialization

The byte-exact bridge dynamically loads the engine (line 77), forms candle buckets (line 120), orchestrates full direction state (line 1903), and finalizes visibility (line 2549). `calculate_full_direction_state` includes a B-dependent branch (line 1968); its effects are not an accepted rule or regression baseline. The source also serializes audit output, but the Vault has no active audit knowledge entity. Input scope and full-file chronology must be read from the actual bridge and chart request, not inferred from this note.
