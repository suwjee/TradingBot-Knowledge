---
id: "market.timeframe"
type: "market"
status: "pending"
authority: "non-canonical"
title: "Timeframe"
source_refs: []
related_entities: ["data.timeframe_registry", "algorithm.raw", "source.trading_pipeline"]
source_reference: []
---

# Timeframe

For T seconds, main bucket timestamp is time for T=1 and floor(time/T)*T otherwise. The bridge's lower candle stream is built from the supplied RAW rows after same-second aggregation; its available event resolution is bounded by the input. The registered local RAW files include nominal 1-second and 5-second inputs, so a 5-second file does not provide unrecorded one-second events. Main-candle source indexes and closed extrema ranges cannot be reconstructed by clipping or renumbering a presentation window. See `data.timeframe_registry` for the inspected inputs and `algorithm.raw` for bucket construction.
