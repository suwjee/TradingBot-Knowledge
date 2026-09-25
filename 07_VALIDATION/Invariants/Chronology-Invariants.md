---
id: "test.chronology_invariants"
type: "test"
status: "pending"
authority: "non-canonical"
title: "Chronology invariant checks"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["test.invariant_validation", "core.chronology", "market.exact_chronology", "algorithm.reaction", "algorithm.reset", "source.reaction_engine", "source.trading_pipeline"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1550"]
---

# Chronology invariant checks

Retained Reaction source supports exact event chronology for its own confirmation and Reset decisions. Complete RAW parsing, bucket construction, S/E/StopAll ordering, and presentation index claims require the absent bridge and lifecycle source; they remain pending in this Vault.

Test same-main-candle races by event time, including invalidation-first ties where the owning routine specifies them. A same-Break post-confirmation Reset uses the frozen exact-confirmation opposite edge and prevents that Break from simultaneously opening the next Mode-B First. This local rule is anchored in retained `reaction_engine.py` lines 1550–1581 and source fixture 4.1.

A selected presentation range is not a substitute for full RAW calculation. Check visible clipping only after state has been calculated over the input actually supplied. Source fixture 3.1 checks an exact 1s A/Reaction source, while 1.9 checks a later same-candle price that cannot rewrite a frozen box.
