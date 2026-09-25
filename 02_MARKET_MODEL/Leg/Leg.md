---
id: "market.leg"
type: "market"
status: "draft"
authority: "non-canonical"
title: "General Leg model pending"
related_entities: ["algorithm.order.c", "algorithm.reaction", "market.model", "test.source_validation"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L552", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L552", "engine/pipeline/e_zone_detector.py#L675"]
---

# General Leg model pending

The current Vault has no independently established, reusable rule for recognizing or calculating a general market Leg. This note records that boundary; it does not define a new trading object or calculation.

The implemented Order_C route uses a **specific** Leg Start: its Reset owner when that Reaction is native Mode A, or the latest earlier native Mode A when the owner is Mode B. `e_zone_detector.py#L675-L711` then freezes the preceding Reaction Breakout through that selected Leg-Start Breakout range. Those steps belong to `algorithm.order.c`; they do not establish a universal Leg model. Reaction Mode A/B is described by `algorithm.reaction`.

General recognition and calculation remain pending. `Recognition.md` and `Calculation.md` are intentionally empty until a source/reference-grounded general contract exists. No fixture or downstream rule may treat this draft note as a canonical Leg definition.
