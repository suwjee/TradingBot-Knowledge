---
id: "mirror.exceptions"
type: "mirror"
status: "active"
authority: "canonical"
title: "Source-confirmed mirror exceptions"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["algorithm.reaction", "algorithm.reset", "algorithm.order", "algorithm.e", "algorithm.stopall", "algorithm.internal_reaction", "algorithm.lifecycle", "core.e_numbering", "source.reaction_engine", "source.e_zone_detector", "source.lifecycle_engine"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L23", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L23", "engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L638", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L638", "engine/pipeline/reaction_engine.py#L91", "engine/pipeline/reaction_engine.py#L1562", "engine/pipeline/e_zone_detector.py#L393", "engine/pipeline/lifecycle_engine.py#L356", "engine/pipeline/lifecycle_engine.py#L777", "engine/pipeline/lifecycle_engine.py#L1658"]
---

# Source-confirmed mirror exceptions

These are limits on a *simple* Low↔High / `<`↔`>` substitution. They are verified source rules, not market-specific overrides or new behaviors.

| Reviewed area | Confirmed exception / guard | Evidence |
|---|---|---|
| Market color versus detector role | Doji is GREEN in both market directions; only the reflected detector-internal role swaps color tags. Never serialize a mirrored market Doji as RED. | Both references §3.6, §6.2; `reaction_engine.py#L91-L93`, `#L560-L577` |
| Same-Break Reset | Exact confirmation `analysis.extreme` is the frozen opposite edge in **both** directions. The old Bearish BoxTop fallback is historical; the Break candle cannot also start the next Mode-B First when its remainder resets. | Both references §6.7–6.8; `reaction_engine.py#L1550-L1581` |
| Native Mode B versus Order_B | Native Reaction mode `B` is a state-machine mode. Order_B is an independent reset-leg creation cause. The StopAll S-Red reversal gate checks the native `order_mode == B`, not whether an Order_B cause exists. | Both references §13; `lifecycle_engine.py#L356-L380`; `e_zone_detector.py#L393-L550` |
| Order_A owner | The first canonical opposite Reaction confirmed strictly after a stopped A owns that A's parent-stop cause. A later native Mode-B Reaction cannot refresh it merely because S is undecided. One physical identity may still carry multiple independently proved causes. | Both references §9.1, §11; `s_zone_detector.py#L277-L331`; `lifecycle_engine.py#L728-L776` |
| Order_C Leg Start | Native Mode-A Reset owner is itself the Leg Start; a Mode-B owner uses its latest prior Mode A. The level is the closed previous-Reaction Breakout → selected Leg-Start Breakout range, not an open-ended Reset→next-Reaction range. The direction mirrors the price extreme only. | Both references §10.3C (active HPZR5); `e_zone_detector.py#L727-L830` |
| Internal Reaction visibility | Internal geometry remains calculation-valid. The accepted physical-Order ledger rejects an internal native Mode-B Order when **all** surviving causes are reset-leg. The separate final E/StopAll visibility predicate disagrees with the reference in a mixed-cause case; see unresolved item below. | Both references §6.14, §14; `lifecycle_engine.py#L777-L800`, `#L1658-L1708` |
| E numbering and source conflict | E number is lifecycle state; same-source reconciliation applies Red priority and family/number rules. Do not mirror E1 into a new Bearish algorithm or combine different numbered E Blue keys for StopAll evidence. | Both references §10.7–10.8, §13; `e_zone_detector.py#L2267-L2463`; `lifecycle_engine.py#L331-L355` |
| StopAll state | S-Red reversal needs an accepted native Mode-B Order and an exact pending Blue group count ≥2. All S Blue share one key; each numbered E Blue has its own key. Accepted Red resolves pending Blue evidence; hard StopAll clears pending and active owner state. E-driven gates retain separate counters. | Both references §13; `lifecycle_engine.py#L331-L455`, `#L487-L609` |
| Lifecycle protection | A/S/E eligibility and lineage can retain historical evidence without granting it active ownership. Apply stage order and exact event timing before priority; an old dominant owner cannot consume all later legs. | Both references §12, §14; `lifecycle_engine.py#L946-L1177`, `#L1708` |

## Unresolved source–reference conflict

Both synchronized references §14 (line 638) say final Internal-Reaction filtering hides native Mode-B E/StopAll owners only when their surviving Order causes are **reset-leg-only**. Current `lifecycle_engine.py#L1658-L1678` (`forbidden_internal_order_b`) instead returns true if `"reset-leg" in causes` **or** `order_reset_leg_reset_time` is set, even when another cause exists. `filter_internal_behavior_outputs` applies that predicate to E and StopAll at `#L1687-L1708`. The earlier physical-Order ledger filter at `#L777-L800` does require all causes to be reset-leg. The mixed-cause final-output rule is unresolved; do not promote either behavior to canonical Mirror knowledge without a domain decision and a targeted reachable case.

## Scope limits

The former Bearish same-Break BoxTop behavior is historical and must not be promoted to the current contract. Current OrderAudit output alone is not a Mirror rule; chart-selected input truncation is an integration boundary, not a Mirror exception. A newly suspected directional asymmetry needs its own two-reference and source trace before being added here. Both references §6.7, §11; `reaction_engine.py#L1562-L1577`.
