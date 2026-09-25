---
id: "algorithm.order.a"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Order_A parent-stop cause"
implemented_by: ["source.s_zone_detector", "source.e_zone_detector", "source.reaction_engine"]
depends_on: ["algorithm.order", "algorithm.a", "algorithm.e"]
source_refs: ["engine/pipeline/s_zone_detector.py#L274", "engine/pipeline/e_zone_detector.py#L1058", "engine/pipeline/e_zone_detector.py#L1186"]
---

# Order_A parent-stop cause

After an eligible A strict stop, the stopped-A S route selects the earliest canonical opposite Reaction with First main index >= A-stop main index and exact confirmation > aStopEventTime. Rank (confirmationTime,FirstIndex,BreakIndex). That first physical Order is immutable for that stopped A; no later Mode A/B Reaction can refresh it while S remains undecided. Its parent-stop cause is attached to that identity.

For accepted A/S/E/StopAll strict stops, E independently discovers the first new direct opposite Order_A from each exact parent stop. Existing carried/inherited Orders may remain live, but cannot defer the new discovery. Order selection for an E decision is a later race. If several physical Orders claim one exact parent-stop provenance, the earliest (confirmationTime,FirstIndex,BreakIndex) keeps the cause; others survive only with another independent cause. Use provenance remains separate.
