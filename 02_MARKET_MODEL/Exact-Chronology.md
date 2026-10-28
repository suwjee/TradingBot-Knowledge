---
id: "market.chronology"
type: "market"
status: "active"
authority: "executable"
title: "Exact lower-timeframe chronology"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1020", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L105", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L145", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L188"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Exact lower-timeframe chronology

MarketChronology and LowerTimeframeIndex index selected lower-timeframe rows with exact positions. Physical main-candle timestamp, precise confirmation/stop second and source formation event are distinct values. Resolve intrabar races from the finest supplied chronology; main OHLC can establish an extreme but cannot establish the order of competing price events. Time, native indexes and endpoint meanings are direction-invariant.


## Owner-specific chronology and cache preconditions

Ordered stable Candle sequences are chronology preconditions. Shared cached timestamp/extreme indexes are guarded by sequence object identity; mutation of an already indexed sequence is outside this cache contract. Detector source mapping checks the owning main interval, while MarketChronology.main_index only bisects main starts and handles prehistory; callers own any upper-close bound. Reaction analysis starts after an earlier confirmation-edge source unless an explicit intrabar_start overrides it, ends at Break close exclusive and includes the first strict confirmation row in eligible opposite geometry.

Exact lower chronology answers explicitly intrabar questions. The configured calculation candle still owns Order_B First eligibility and A expiry; main-timeframe gates must not be shifted by substituting the later lower-row timestamp.
