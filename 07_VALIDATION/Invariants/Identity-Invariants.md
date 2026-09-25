---
id: "test.identity_invariants"
type: "test"
status: "canonical"
authority: "normative"
title: "Physical identity and provenance checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.invariant_validation","algorithm.order","core.e_numbering","source.core_utils","source.s_zone_detector","source.e_zone_detector","source.lifecycle_engine"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L299","engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L299","engine/pipeline/core_utils.py#L19","engine/pipeline/s_zone_detector.py#L277","engine/pipeline/lifecycle_engine.py#L728"]
---

# Physical identity and provenance checks

One physical Order is the opposite canonical Reaction identified by (FirstIndex, BreakIndex). Native Reaction Mode A/B is not Order_A/B/C. Parent-stop, reset-leg and blue-leg are independent creation causes; accepted-live and carried-live are use routes. Merge causes on one physical identity without fabricating a new Order. Both references §§6.12, 10.2, 11; core_utils.py lines 19–29; e_zone_detector.py lines 1143–1229.

The first canonical opposite Order after a stopped A owns that A's parent-stop cause permanently. Later native Mode-B confirmations cannot refresh this owner before or after S decision; only an independently proven creation cause can qualify another Order. Source fixture 1.1 tests identity (689,693), and historical 1.13 preserves the superseded V5.4.5 refresh outcome. Both references active V5.4.8 rule and §9.1; s_zone_detector.py lines 277–321.

Validate that a single exact parent-stop provenance maps to one physical Order, and all public S/E/StopAll Order references have a matching physical identity in the output ledger where that ledger is applicable. Existing Vault authority keeps OrderAudit pending-fix for trading-rule conclusions. The mixed-cause Internal-Reaction E/StopAll visibility rule remains unresolved between both references §14 and lifecycle_engine.py lines 1658–1678; do not encode either interpretation as an accepted identity exception.

