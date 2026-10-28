---
id: "core.chronology"
type: "core"
status: "active"
authority: "executable"
title: "Physical lower-timeframe chronology"
version: "current"
related_entities: ["algorithm.raw", "core.determinism", "core.pipeline", "core.precision"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md#L137"]
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Physical lower-timeframe chronology

MarketChronology maps exact event to main with bisect_right(main_times,event)-1. lower_bounds uses bisect_left start/end for [start,end). Finest supplied lower row chronology is authority; seconds class/variable names do not synthesize missing finer rows.

Reaction confirmation scans Break from valid intrabar_start or Break-open fallback. A intentionally sets use_intrabar_start=False; S/E/public Reaction normally use recorded intrabar start. If proof unavailable, confirmation helper returns Break-open fallback rather than guessed intrabar order.

A source includes exact confirmation row by extending end one microsecond; E source includes complete containing main boundaries. Post-confirmation Reset and Order_B post-Reset searches exclude starting event where strict-later owner requires it. Shared S reconciliation includes source main-open equality; Blue pending confirmation row also remains eligible. Source main time,candidate formation,decision main time and exact event are separate.

Reset second_time is preferred to main fallback. Native local naive datetime uses Asia/Tehran epoch conversion. Temporal values,physical source indexes and window ownership remain invariant under directional price reflection.

Order_B First eligibility and next-accepted-A expiry compare owning calculation candles. The exact lower crossing remains required after Reset and before opposite confirmation; it does not delay a same-main First gate. Blue Break source extrema and pending strikes stop at exact Reaction confirmation inclusive. A visibility maps an intrabar S decision with bisect_right(mainTimes,event)-1 to its containing main candle.
