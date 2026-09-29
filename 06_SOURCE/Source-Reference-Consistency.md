---
id: "source.reference_consistency"
type: "source"
status: "active"
authority: "executable"
title: "Current Source and Reference semantic consistency"
name: "Source Reference Consistency"
aliases: ["Source Reference Conflicts"]
version: "current"
related_entities: ["algorithm.blue", "algorithm.reaction", "algorithm.e", "algorithm.stopall.blue_reversal", "algorithm.serialization", "source.reference_registry"]
source_reference: ["06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L84", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1554", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L308", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py#L816", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L366", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py#L1393", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L833"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md"]
evidence_basis: "Fresh complete Source and directional Reference review; exact byte identity checked separately"
reference_agreement: "conflict"
reference_conflicts: ["REF-BLUE-ENDPOINT", "REF-REACTION-SUCCESSOR", "REF-E-TIE-SCOPE", "REF-S-MODE-B"]
---


# Current Source and Reference semantic consistency

Review date: 2026-09-29. VERIFIED STATIC SOURCE FACTS below describe current executable branches. DOCUMENTED CLAIMS preserve the current References' narrative wording. Exact Source reconstruction is PASS for each Reference; it does not prove narrative agreement. No Engine or Reference edits, trading execution or market outcome validation occurred in this phase.

| Record | Documented claim in both References | Current Source fact | Classification and rule handling |
|---|---|---|---|
| REF-BLUE-ENDPOINT | Section 5.2, line 104 bounds pending Blue at the first strict Reaction confirmation row inclusive | Blue lines 84-136 return at a crossing only when eligible penetrations are nonempty; an empty-set crossing does not end the scan | Conditional mismatch. Retain decisive-row inclusion, use the actual conditional helper as executable knowledge, and keep unconditional intent unresolved |
| REF-REACTION-SUCCESSOR | Section 4.4, line 78 says post-event chronology controls eligible new-boundary prices | Reaction lines 1554-1630 separate post-event Reset reuse gating from full confirmation-candle successor geometry; initial branch lines 2108-2170 does not seed a successor | Ambiguous boundary scope. Record complete-candle geometry and branch-specific seeding; do not infer a post-event-only successor boundary |
| REF-E-TIE-SCOPE | Section 8.2, line 185 says exact stop ties prefer larger FirstIndex | Order lines 816-840 choose direct/reset-leg representative by stop then earlier FirstTime; carried and post-stop ranks differ; E lines 325-353 races representatives by stop then larger FirstIndex | Ambiguous route scope. The larger-First rule is final-race-specific, not a universal underlying pool sort |
| REF-S-MODE-B | Section 12.4, line 295 requires a native Mode-B formation Order | Lifecycle lines 366-373 tests final color Red and order_mode=B; S lines 1393-1417 can replace that Order field after native order-free formation | Ambiguous original-versus-final ownership. Record final-field predicate and preserve stronger native wording separately |

No new intended trading rule is chosen by these records. Determining intended behavior beyond the executable facts requires a separately authorized semantic clarification. A particular market realization of these differences is NOT_REQUIRED_THIS_PHASE. Active/executable algorithm notes retain current Source authority and expose Reference warnings; the disputed stronger narrative interpretation is not promoted to normative authority.

## Source comment scope

The post-Reset scanner's docstring says an unfinished owner blocks nested completion, while Reaction lines 1677-1678 skip the unfinished bounded candidate. The canonical bounded completion-selection note follows the executed branch and matches Reference section 4.7.

Optional Bridge Output comments describing no new stop search need owner scope: bridge parent-stop and A-stop helpers call native E/S chronology methods that may scan. The mapper validates the returned exact event, creates no physical Order or lifecycle acceptance, and selects no substitute event after proof fails. These are comment-versus-operation qualifications, not authorized Source corrections.

## Feedback and evidence scope

StopAll reconciliation makes one source-order pass per call. Order_B feedback calls it during each dependent pass, then final visibility calls it after convergence. The Reference's hard-boundary intent is preserved as a documented claim; this static phase does not prove global future-input prefix invariance through changing feedback state. Exact implementation scope is recorded in algorithm.reconciliation.

## Additional Source-comment qualifications

Canonical adjacent-anchor append directly assigns the confirmation edge after its exact eligibility proof; its no-shrink comment has no explicit edge-extension comparison in that branch. The overlapping direct-geometry helper selects earliest confirming main and then smallest First index, not exact lower confirmation time. These owner facts are qualified in algorithm.reaction and algorithm.order.a; no reachable shrinking or event-reordering market case is claimed.

Lifecycle visible_a_zones_after_s_stops excludes bisect_left(main_times, S decision_event_time), which can map an intrabar decision to the next main index; the comment describing a containing S stop must not replace that exact predicate. S._a_confirmation_time uses default chronology confirmation and does not impose A detector's separate use_intrabar_start=False formation API usage.
