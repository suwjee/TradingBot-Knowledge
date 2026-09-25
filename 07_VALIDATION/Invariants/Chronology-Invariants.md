---
id: "test.chronology_invariants"
type: "test"
status: "canonical"
authority: "normative"
title: "Chronology invariant checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.invariant_validation","core.chronology","market.exact_chronology","algorithm.reaction","algorithm.reset","source.reaction_engine","source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L209","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L209","engine/bridge/trading_pipeline.py#L120","engine/pipeline/reaction_engine.py#L1550"]
---

# Chronology invariant checks

RAW epoch seconds create exact lower candles; duplicate seconds collapse first Open, maximum High, minimum Low and last Close. Main candles bucket by the configured timeframe. Lower windows are half-open unless a rule explicitly includes an endpoint. Exact first lower events decide confirmation, Reset, breakout, strict stop, A trigger, S/E decision and StopAll; full-input physical indexes are not renumbered for presentation. Both references §§3, 5, 17; trading_pipeline.py lines 120–208 and 1732–1813.

Test same-main-candle races by event time, including invalidation-first ties where the owning routine specifies them. A same-Break post-confirmation Reset uses the frozen exact-confirmation opposite edge and prevents that Break from simultaneously opening the next Mode-B First. Source fixture 4.1; reaction_engine.py lines 1550–1581; both references §6.7.

A selected presentation range is not a substitute for full RAW calculation. Check visible clipping only after state has been calculated over the input actually supplied. Source fixture 3.1 checks an exact 1s A/Reaction source, while 1.9 checks a later same-candle price that cannot rewrite a frozen box.

