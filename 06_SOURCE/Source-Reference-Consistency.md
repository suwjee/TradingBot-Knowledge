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
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1557", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L142", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L376", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py#L344", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L2542"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md"]
evidence_basis: "Fresh complete Source and directional Reference review; exact byte identity checked separately"
reference_agreement: "ambiguous"
reference_conflicts: ["REF-REACTION-SUCCESSOR"]
last_modified_at: "2026-10-28T18:07:57+03:30"
---
# Current Source and Reference semantic consistency

The 2026-10-27 review compares the current accepted Reference statements with exact in-scope live owner bytes. Source facts below describe executable behavior; Reference wording describes intended semantics under root AGENTS authority. No Source or live accepted Reference was edited. Historical revision results inside exact References are not fresh checks.

## Remaining narrative ambiguity

| Record | Current accepted Reference claim | Current executable fact | Handling |
| --- | --- | --- | --- |
| REF-REACTION-SUCCESSOR | Section4.4 permits a complete confirmation candle as the next First, while saying post-event chronology controls eligible new-boundary prices | UnifiedReactionDetector._candidate_from_confirmation_remainder first checks strictly later rows for Reset, then uses whole_confirmation_candle=True, all lower rows in that main candle and main-open intrabar_start for successor geometry. Initial confirmation now invokes the helper too. | Ambiguous boundary-price scope. Retain both claims and do not invent a post-event-only successor boundary or silently rewrite intended semantics. |

## Earlier discrepancy claims rechecked

| Earlier record | Current evidence | Status |
| --- | --- | --- |
| REF-BLUE-ENDPOINT | Blue count_scale_strikes computes the Break lower prefix through exact confirmation inclusive; pending helper also stops after that time. Current Reference5.2 uses the same prefix. | Resolved in current captured Source/Reference; old unconditional-scan warning removed. |
| REF-E-TIE-SCOPE | E._zone now races every eligible route candidate globally by exact stop then larger FirstIndex instead of reducing routes to one representative. Current Reference8.2 states the global scope. | Resolved; route-local sort descriptions are no longer a competing final rank. |
| REF-S-MODE-B | Reference12.4 and lifecycle detect distinguish direct accepted S Red donation in either mode at its decision from completed-stop Mode-B fallback. No independent Blue occurrence ledger remains. | Superseded former wording; current explicit route distinction replaces the old native-versus-final ambiguity. |
| Initial successor absence | Unified initial no-Reset confirmation now invokes the shared successor helper. Reference4.4 explicitly covers initial and later confirmations. | Resolved; complete-candle price-scope ambiguity above remains separate. |

## Source-comment and operation qualifications

The bounded post-Reset scanner docstring says an unfinished owner blocks nested completion, but its executable branch skips an unfinished bounded candidate. Reference4.7 expressly documents that completion-selection distinction. The adjacent-anchor append assigns its confirmation edge after exact eligibility without an additional no-shrink comparison. Raw direct-geometry selection ranks first confirming main then First index rather than a universal exact-lower-event order. These are owner-specific static facts, not demonstrated reachable market failures.

Optional Bridge projection calls native chronology confirmation/parent-stop methods which can scan. It validates the resulting exact lower row and never substitutes another event when proof fails; comments saying no new stop search must be read at mapper ownership scope. A detector deliberately uses use_intrabar_start=False for its own confirmation API; S/E/public Reaction callers retain their separate defaults.

Each StopAll reconciliation call makes one source-order pass; Order_B feedback can invoke another pass over recalculated accepted state when explicitly enabled. Final visibility uses identical enablement and supplements only absent accepted independent E donor physical sources before fixing hard boundaries. This static record does not prove future-input prefix invariance globally.

## Coverage limits

No new primary-structure knowledge or standalone detector is added. Complete current References preserve incidental excluded content exactly; source_scope and embedded-only integrity pins make that distinction explicit. RAW market regression, independent opposite-direction market correctness, full runtime branch coverage and excluded-feature semantic review are NOT RUN. Byte/schema/index/contract checks have separate statuses in the current validation report.
