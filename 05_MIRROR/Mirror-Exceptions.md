---
id: "mirror.exceptions"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Mirror exceptions and pending checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["algorithm.reaction", "algorithm.reset", "algorithm.order", "algorithm.e", "algorithm.stopall", "algorithm.internal_reaction", "algorithm.lifecycle", "core.e_numbering", "source.reaction_engine", "source.e_zone_detector", "source.lifecycle_engine"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L91", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1562"]
---

# Mirror exceptions and pending checks

> Scope: This mirror description is provisional. Full directional references and mixed source modules are absent from this Vault; verify each rule against retained local source before use.

These are candidate limits on a *simple* Low↔High / `<`↔`>` substitution, not market-specific overrides or new behaviors. Market color and same-Break Reset have retained local Reaction evidence; the first Order_A ownership rule has retained local S evidence. Other portions that cite absent E/lifecycle modules remain pending and cannot establish current behavior from this Vault alone.

| Reviewed area | Rule or proposed guard | Evidence |
|---|---|---|
| Market color versus detector role | Doji is GREEN in both market directions; only the reflected detector-internal role swaps color tags. Never serialize a mirrored market Doji as RED. | Both references §3.6, §6.2; `reaction_engine.py#L91-L93`, `#L560-L577` |
| Same-Break Reset | Exact confirmation `analysis.extreme` is the frozen opposite edge in **both** directions. The old Bearish BoxTop fallback is historical; the Break candle cannot also start the next Mode-B First when its remainder resets. | Both references §6.7–6.8; `reaction_engine.py#L1550-L1581` |
| Order_A owner | The first canonical opposite Reaction confirmed strictly after a stopped A owns that A's parent-stop cause. A later native Mode-B Reaction cannot refresh it merely because S is undecided. One physical identity may still carry multiple independently proved causes. | Both references §9.1, §11; `s_zone_detector.py#L277-L331`; `lifecycle_engine.py#L728-L776` |
| E numbering and source conflict | E number is lifecycle state; same-source reconciliation applies Red priority and family/number rules. Do not mirror E1 into a new Bearish algorithm or combine different numbered E Blue keys for StopAll evidence. | Both references §10.7–10.8, §13; `e_zone_detector.py#L2267-L2463`; `lifecycle_engine.py#L331-L355` |
| StopAll state | S-Red reversal needs an accepted native Mode-B Order and an exact pending Blue group count ≥2. All S Blue share one key; each numbered E Blue has its own key. Accepted Red resolves pending Blue evidence; hard StopAll clears pending and active owner state. E-driven gates retain separate counters. | Both references §13; `lifecycle_engine.py#L331-L455`, `#L487-L609` |
| Lifecycle protection | A/S/E eligibility and lineage can retain historical evidence without granting it active ownership. Apply stage order and exact event timing before priority; an old dominant owner cannot consume all later legs. | Both references §12, §14; `lifecycle_engine.py#L946-L1177`, `#L1708` |

## Unresolved source–reference conflict

The mixed-cause Internal-Reaction final visibility rule cannot be settled here because its E/lifecycle implementation and comprehensive references are absent. No symmetric pass expectation is accepted for that rule until both are restored and reconciled.

## Scope limits

The former Bearish same-Break BoxTop behavior is historical and must not be promoted to the current contract. Current OrderAudit output alone is not a Mirror rule; chart-selected input truncation is an integration boundary, not a Mirror exception. A newly suspected directional asymmetry needs its own two-reference and source trace before being added here. Both references §6.7, §11; `reaction_engine.py#L1562-L1577`.
