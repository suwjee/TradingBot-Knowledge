# TradingBot Bearish Algorithm Reference — Current Standalone Specification

**Document Version:** `5.4.19-EX1`  
**Last Modified:** `2026-09-28 22:34:26 +0330`  
**Status:** `ACTIVE — Full Source-derived semantic rewrite, byte-exact Source-synchronized`  
**Target Direction:** `bearish`  
**Opposite Direction:** `bullish`  
**Production Source Behavioral Change:** `E / OrderAudit minimal invariant bug fixes`  
**Mirror Contract:** Current shared Production Source defines both directional paths. Price geometry is reflected; time, identity, provenance, Doji and lifecycle ordering remain invariant.

> Current Production Source defines executable behavior. This canonical Reference specifies the current audited and synchronized implementation. Section 16 embeds its exact Source bytes.

## 0. Revision scope

This current revision synchronizes the complete audited implementation after proven E/OrderAudit invariant fixes and corrects demonstrated narrative mismatches. Current Source module versions are independent from Reference version `5.4.19-EX1`. All current calculation and package files are reconstructed exactly. Empty RAW/Fixture stores and market-regression NOT_TESTED are explicit release constraints.

## 1. Source manifest

| Module | Owner | Version | Lines | Bytes | SHA-256 |
|---|---|---:|---:|---:|---|
| `__init__.py` | Package marker / unsupported wrapper | `unversioned package marker` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `bridge/__init__.py` | Package marker / unsupported wrapper | `unversioned package marker` | 1 | 64 | `2bc59770b9d4313c0e6306287d074487b9e1672dbaf3ada9a8be381e7123f0b8` |
| `bridge/trading_pipeline.py` | Pipeline / Serialization | `1.7.0 (impl 1.8.0)` | 2952 | 107807 | `ef5109f4ebb95bc0e04b3d964b14da5f764ae4472f3d10a1a9b7192d59fec683` |
| `pipeline/__init__.py` | Package marker / unsupported wrapper | `unversioned package marker` | 19 | 348 | `ca549e4cf5d9a070227498d0d210279e0f7edae66d62dadab7981cddaa1db5c3` |
| `pipeline/a_zone_detector.py` | A | `1.6.4` | 797 | 31007 | `d7c33dd619ad7e4590027667a2c4e984c83be7b82fbfafeb5d7f944ddd521097` |
| `pipeline/blue_line_detector.py` | Blue | `2.3.0` | 458 | 15802 | `6fa01d94bc98060b62bc7e68db0ec24a0b0159727d44043affee7130a9c11448` |
| `pipeline/core_utils.py` | Core Utilities | `1.0.0` | 29 | 885 | `3dae390ae77b72965f5799f7c132c4eba203775d5e72761fd7dd60c90f8578de` |
| `pipeline/direction_policy.py` | Direction Policy | `1.0.0` | 70 | 2282 | `a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea` |
| `pipeline/e_zone_detector.py` | E | `6.16.1 (impl 6.18.1)` | 1033 | 44859 | `38834e96cc58931fe2e12096f4465ecaa046387d30fd40fecbd6891971020988` |
| `pipeline/lifecycle_engine.py` | Lifecycle / StopAll | `1.17.0 (impl 1.18.0)` | 1555 | 64325 | `94feb038e1e78b291762cfc03dfc370e48bb94f3e1fe1171b7a5206301e8be13` |
| `pipeline/order_audit_engine.py` | Order / OrderAudit | `1.5.1` | 1863 | 75219 | `09cba00c0623ffcce0d7bc3460c1e963c4e2b14fb02a9172cc25dcca8ba9aedc` |
| `pipeline/reaction_engine.py` | Reaction / Reset | `9.8.0` | 2406 | 103120 | `bea0d5a5e95ee15ad54d024f6c01b8c777ba2abcc3c8e671118f1ae2df28f2a6` |
| `pipeline/s_zone_detector.py` | S | `4.20.0 (impl 4.21.0)` | 1444 | 60888 | `ef71a2e4176caaabc25d1ef0c1f0f24efb54ed3110982cdb7cf52d2449cca2ee` |

Current Source encoding and exact newline bytes are independently verified after extraction from Section 16.

## 2. Authoritative pipeline and ownership

The production execution contract is:

`Complete supplied input normalization → both directional Reaction/Reset contexts → cross-direction Internal Reaction classification → Blue → A → initial S → provisional E → S validity/rebuild and accepted A/Order context → final E/OrderAudit → shared physical Order stop reconciliation → consumed-S native continuation → accepted Order_B feedback → lifecycle/StopAll → visibility/lineage closure → final OrderAudit synchronization → serialization`

Order_B feedback may repeat S/E context construction up to eight passes, using exact reset-leg identities. A repeated non-convergent identity or pass overflow is an error. This feedback does not recalculate Reaction/Blue/A geometry. StopAll is reconciled once from accepted chronology; downstream boundary publication does not reinterpret historical E.

The bridge calculates the complete input it actually receives. The full-chart HTTP route supplies the original RAW file. A selected-range HTTP route supplies an in-memory stream filtered by inclusive chart-candle buckets; that calculation begins with empty state at the selected start and cannot use rows outside the supplied stream. Within that supplied input, CLI from/to bounds filter presentation after calculation. Neither frontend nor serialization independently implements trading rules.

Ownership boundaries are strict: Reaction/Reset is owned by `reaction_engine.py`; Blue by `blue_line_detector.py`; A by `a_zone_detector.py`; S by `s_zone_detector.py`; E by `e_zone_detector.py`; physical Order discovery/reuse/provenance by `order_audit_engine.py`; lifecycle/StopAll/visibility by `lifecycle_engine.py`; request/range orchestration and serialization by `bridge/trading_pipeline.py`. Serialization is a projection of finalized state and is not a second trading algorithm.

## 3. Global invariants

1. **Decimal:** every price-sensitive input is normalized with `Decimal(str(value))`; no binary-float decision is authoritative.
2. **Candle color:** `GREEN` iff `close >= open`; `RED` iff `close < open`; a Doji is always GREEN in both market directions.
3. **Strict crossing:** equality never satisfies a strict price crossing. For Bearish behavior-space stops the directional primitive is `High > Level`; the Bullish mirror uses the opposite strict comparator.
4. **Chronology:** exact event ordering comes from the finest selected lower timeframe. Range windows are half-open unless a component explicitly includes a complete main boundary candle. Time is never mirrored.
5. **Reaction identity:** physical Reaction/Order identity is `(FirstIndex, BreakIndex)`. Identity, provenance structure, stable ordering, lifecycle priority, behavior-family names and public schemas are direction-invariant.
6. **Determinism:** candidate ordering and tie-breaking are explicit. Equal main-candle extremes keep the earliest source unless the owning rule explicitly requests last-on-equality (S Type-3/Type-4 candidate construction).
7. **Canonical mirror:** the Bearish Reaction path mechanically reflects the shared Bullish coordinate state machine. Independently inspect explicit directional branches and policies. Reflect prices/roles; preserve time, state ownership, canonical identity, cause structure and lifecycle families.
8. **Calculation vs presentation:** internal/historical objects may remain necessary for later calculation even when they are not independently visible. Final filters cannot rewrite upstream truth.

## 4. Reaction / Reset — ACTIVE Bearish specification

### 4.1 Data and color contract

`Candle` carries `index`, native `timestamp`, display time, immutable market `tag`, and Decimal OHLC. `Candidate` carries First/box sources, Mode A/B, optional anchor and leg boundary, Break, intrabar start, cross-direction gate metadata, public box/number metadata and internal/public ownership flags. `ResetEvent` records main index/time, optional exact lower-TF second, broken level, and the owning Reaction First index.

### 4.2 Canonical directional geometry

For Bearish, the canonical First candle role is **FirstGreen** (`GREEN`) following the opposite context color `RED`. Confirmation is the first strict breakdown satisfying `Low < BoxBottom`. The confirmation edge is `BoxBottom`. The opposite box edge `BoxTop` may evolve only through chronology available up to the exact confirmation event.

The source does not maintain an independent hand-written Bearish state machine: Bearish geometry executes the Bullish reference state machine through exact Decimal sign/High-Low/color-role reflection. Therefore the initial leg, Mode-A invalidation, breakout/breakdown priority, Reset priority, post-confirmation handling, and lower-timeframe tie rules share one mechanical geometry contract. The reflected color role is internal coordinate machinery only; market Doji remains GREEN.

### 4.3 Mode A / leg-start ownership

Mode A is the first Reaction of a leg. The detector establishes the contiguous context run, builds the directional First candidate, preserves any qualifying adjacent anchor, and freezes the outer leg boundary. Before confirmation, strict outer-boundary invalidation owns the candidate ahead of confirmation when lower-TF chronology proves it first. In the standalone initial Mode-A WAITING state, an invalidated owner releases search and nested geometry cannot confirm while its selected structural owner remains unresolved. The bounded Unified post-Reset search has the separate completion-selection contract in Section 4.7.

### 4.4 Mode B / normal ownership

After a confirmed Reaction, normal search uses the running directional context and the required First color. A confirmation main candle may itself seed the next Mode-B First only when the post-confirmation remainder does not first Reset the just-confirmed structure. The complete confirmation candle can be the next First when its market color has the required role; post-event chronology still controls which prices are eligible for the new boundary.

### 4.5 Exact confirmation and published box

If the Break main candle owns the full-main-candle opposite extreme, only lower-TF prices at or before the first strict confirmation may define the published opposite edge. Later prices in that same main candle cannot retroactively alter Reaction/Order geometry. If lower-TF chronology cannot prove a refinement, detector geometry is retained rather than guessed. Equal eligible extremes retain the earliest main-candle owner.

### 4.6 Reset

A confirmed Bearish Reaction resets only on the first strict `High > confirmed BoxTop` event. Equality is not Reset. When Reset and confirmation/break activity share a main candle, selected lower-TF ordering decides which event owns the state transition. Reset reopens **same-direction** Reaction ownership; opposite-direction patterns do not gate that search. A Reset event with an exact lower-TF second exposes that exact second; otherwise the owning main-candle start is the fallback representation.

### 4.7 Post-Reset structural owner vs geometry-only evidence

After Reset, `_first_direct_same_direction_after_reset` scans eligible First candidates in chronological First-index order within the configured end index. It returns a candidate only if confirmation wins before strict loss of its frozen owning boundary. If invalidation wins first, candidates with First indexes at or before that invalidation main index are blocked. A candidate unfinished at the bounded end is skipped, so a later eligible candidate that completes healthily may be returned. The standalone initial Mode-A WAITING state retains its selected unfinished structural owner. The returned healthy result joins the canonical same-direction Reaction stream. `_first_geometry_after_reset` separately returns complete geometry without lifecycle acceptance; geometry alone cannot create Order_A.

### 4.8 Internal Reaction ownership

Cross-direction internal protection is determined after both directions exist. A candidate is internal only when its temporal/box structure is contained by a healthy opposite Reaction and the complete lower-timeframe physical path through its confirmation remains inside the protecting box. Internal identity affects behavior/public ownership; it does not delete historical calculation evidence or renumber the canonical Reaction stream.

## 5. Blue — ACTIVE Bearish specification

### 5.1 Inputs and reference level

Blue consumes canonical Bearish Reactions and Bearish Resets. For each Reaction, the scale reference is the Mode-A boundary when present; otherwise it is the previous Reaction opposite edge. The 0.618 level is `BoxBottom + 0.618 × (reference − BoxBottom)`.

### 5.2 Scale strikes

Within Reaction First..Break inclusive, a new strike requires a strictly higher `High` than the previous confirmed strike (or than the Fibonacci level for the first strike). Pending strikes confirm on a `RED` main candle. A pending strike reaching the Break candle may confirm intrabar only from lower-TF chronology through the strict Reaction confirmation lower-timeframe row, inclusive; the decisive extreme is the most directional eligible lower-TF extreme.

A Scale Blue is emitted when strike count increases and spacing ownership permits it (first Blue, or at least one healthy Reaction since the previous Blue). Its source is the decisive strike; line price is `High − (High − Low) / 3` and its drawing interval is one timeframe before/after the source time.

### 5.3 Reset Blue and double-stop calculation validity

A Reset Blue is sourced by the Reset main candle, with source extreme `High`, broken level from Reset, and line price `High − (High − Low) / 5`. If the prior Blue first strict-stops on that same Reset candle and the Reset source extends strictly farther in the Bearish direction than the prior Blue source extreme, the new Reset Blue is marked `calculation_valid=False`. That invalid line remains calculation evidence for the A double-stop route but is excluded from public Blue output.

### 5.4 Internal/public Blue

A Blue becomes behavior-internal when its owning Reaction is internal, or when both the source extreme and rendered line price lie strictly inside the same protected healthy Reaction. Drawing offset alone does not create internal ownership. Public Blue is exactly `calculation_valid and not behavior_internal`.

## 6. A — ACTIVE Bearish specification

### 6.1 Blue state and strict stops

A builds an immutable `BlueState` ledger from all Blue calculation state. Blue formation is exact: Scale Blue forms at its Reaction confirmation; Reset Blue uses the first strict lower-TF crossing of its broken level when available. Each Blue stop is the first strict Bearish crossing of its `source_extreme`; equality does not stop a Blue.

### 6.2 Ordinary adjacent-Blue route

Ordinary A evaluates adjacent calculation-valid Blue states. A pair may trigger through the established direct or inherited-stop route. When the first Blue stopped before the second formed, continuation geometry is frozen over the owning interval; inherited-stop ownership uses the complete stop-candle through the aligned Reaction Break candle. Directional source selection is the maximum High and strict comparisons preserve chronology. Exact equal-event ties use deterministic ordering; the second/current Blue may be reused for the next adjacent pair only when the current A's first strict stop and the next Blue formation satisfy the source lifecycle gate.

### 6.3 Double-stop route

A Reset Blue marked calculation-invalid by the Blue double-stop rule can create the special A route with the previous valid Blue only when the previous Blue's first strict stop belongs to the invalid Reset Blue source candle. The route then requires the first qualifying same-direction canonical Reaction after the trigger chronology. A special route cannot duplicate a Reaction already owned by ordinary A, and earlier ordinary A lifecycle may suppress the special route when its first stop already completed before the special Reaction.

### 6.4 Reaction confirmation and A source freeze

After a valid Blue-pair trigger, the first qualifying canonical Bearish Reaction confirms A. The A source/price is the maximum High from the trigger main-candle open through the exact lower-TF Reaction confirmation, inclusive. Prices later in the same Break candle are outside A ownership and cannot move the source retroactively. Ties retain the earliest source unless the owning helper explicitly states otherwise.

### 6.5 A stop and lifecycle handoff

A itself stops on the first strict Bearish crossing after its confirming Reaction. A historical stop before a route's `not_before` boundary belongs to the previous cycle; a later recross of the same level cannot be reinterpreted as the new cycle's first stop. The stop event opens S space.

## 7. S — ACTIVE Bearish specification

### 7.1 General A→S gate

Only A candidates outside an already-owned S continuation are eligible. S begins at A's first strict Bearish stop. If the next A confirmation is already reached at/before that handoff, the stale A does not open S. The detector audits the stopped A's first physical Order_A independently before choosing the S route.

A decided S normally owns subsequent A continuation. A newly built Reset-Blue/Reset-Blue pair may preempt that ownership only when both Blue sources are born after the S handoff, Blue-1 stops before Blue-2 forms, the A source is Blue-2's stop candle, and the pair is actually Reset/Reset. A trigger that begins strictly after the exact S ownership handoff is independently eligible.

### 7.2 Order-free Type-3 S Blue

Type-3 is an opposite-Reset-leg route available after A stop and before the first Order deadline. The opposite Reaction owning the Reset must have confirmed by the A-stop event and must not already have Reset before that A stop. Candidate geometry spans the **complete opposite Reaction Break main candle through the Reset main candle**, inclusive, and selects the maximum High with **last-candle ownership on equality**. After Reset, the first strict Bearish cross of that candidate wins only if at least one ordinary same-direction Reaction confirms after A stop and no later than the cross. Earliest valid Type-3 decision wins.

### 7.3 Order-free Type-4 S Blue

Type-4 is the same-direction Reaction continuation available after A stop only while no opposite Order has formed. For every aligned Bearish Reaction confirmed before the Order deadline, candidate geometry spans the A-stop main candle through that Reaction Break main candle, inclusive, selects the maximum High and assigns equality to the **last** candidate candle. Search begins at the maximum of A-stop event, aligned Reaction confirmation and candidate formation event. That lower-timeframe start is inclusive. The next aligned Reaction confirmation and Order deadline are exclusive upper bounds. The first strict Bearish cross creates S Blue only when a public calculation-valid Blue formed from the candidate source through that cross. If a candidate crosses without qualifying Blue, no S is created from it; the next aligned Reaction rebuilds a fresh candidate from the same A-stop origin.

Type-3 and Type-4 are independent. Earlier exact decision event wins; Type-3 owns only a true exact-event tie.

### 7.4 Order-backed Simple and Advanced routes

The first physical opposite Order_A owned by the stopped A is immutable for that A; later native Reactions do not refresh it merely because they are newer. Candidate timing first applies established price geometry. Exact event chronology may reclassify an apparent after-Order Simple candidate as pre-Order only when its candidate event is strictly before Order First; equality belongs to after-Order. A valid nested same-direction Reaction wholly contained in the physical opposite Order, with aligned confirmation at or before Order confirmation, owns the **Advanced** path and cannot be stolen by the pre-Order Simple chronology optimization.

For pre-Order Simple, candidate geometry spans A-stop through Order First with the A-stop candle restricted to lower-TF prices at/after the exact A-stop event. For post-Order Simple, the first aligned Reaction after Order confirmation is used and candidate geometry spans Order Break through aligned Reaction Break inclusive with last-on-equality ownership. Advanced uses the directionally relevant opposite Order box source after a nested aligned Reaction confirms.

### 7.5 S decision race

After Order confirmation, two strict lower-TF events compete:

- physical Order stop: `Low < OrderStop` → **S Red**;
- S candidate strict Bearish cross → **S Blue** only after an aligned Reset Blue formation or an ordinary aligned Reaction completion qualifies the candidate.

An exact same lower-TF position for both crossings produces no decision. Otherwise the earlier event wins. The legacy pre-Order Simple fallback may initially observe an unqualified candidate cross; if later qualification exists by that exact event it becomes Blue, otherwise the fallback path is rebuilt through normal ownership rather than inventing a family.

When a Red decision wins, Red source geometry is recalculated from Order Break through the Red decision main candle unless the accepted pre-Order source is itself authoritative.

### 7.6 Shared accepted-Order stop reconciliation

After E/OrderAudit accepts physical Orders, an open S may be converted to Red by **any** accepted physical Order whose strict stop occurs at or after the frozen S source main-candle start and strictly before S's current decision; the Order confirmation must be strictly earlier than its stop. Parent identity is irrelevant to use; physical identity is authoritative. Candidates are deduplicated by `(FirstIndex, BreakIndex)`, ordered by `(stopCrossEvent, confirmation, FirstIndex, BreakIndex)`, and provenance remains attached to the Order that created it.

## 8. E — ACTIVE Bearish specification

### 8.1 Parent stop and E-space opening

Every E cycle starts only after the first strict Bearish stop of an accepted S/E parent. For an E parent, a stop search begins at its decision event, so E cannot stop before the Order-stop event that confirmed it. Sequence/StopAll boundaries may later reinterpret parent type, but do not invent a different price event.

### 8.2 Physical Order choices

At each parent stop, E considers physical Orders from these routes: direct parent-stop Order_A, an S-carried unconsumed Order, a gate-owned initial A Order, carried-live accepted identity, post-stop accepted-live identity, and accepted Order_B reset-leg identities. `parent-stop` and `reset-leg` are creation causes; `carried-live` / `accepted-live` are use routes only. A candidate must possess an exact strict Order stop. Winner is earliest stop event; for an exact same stop event the larger Order First index wins (`-FirstIndex` tie key). Sequence reset boundaries may invalidate an Order crossing that would span a hard reset.

### 8.3 E source and decision

`decision_event = max(parent_stop_event, order_stop_event)`. The E source is the maximum High across the **complete main candle containing the parent stop through the complete main candle containing the Order stop**, inclusive. Lower-TF chronology decides whether stops occurred; it does not truncate either E boundary candle's OHLC. Strict-better replacement retains the earliest equal source.

### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

## 9. Order_A — ACTIVE canonical physical parent-stop rule

### 9.1 Creation gate

Order_A is the physical `parent-stop` route opened by an accepted strict behavior stop. A bounded/direct geometry candidate may create Order_A **only** when its `(FirstIndex, BreakIndex)` exists in the canonical opposite-direction (Bullish) Reaction stream. Geometry absent from that canonical registry remains internal evidence and cannot enter OrderAudit as Order_A or receive a synthetic reaction number.

After a stopped A, the first canonical opposite Order is immutable for that A. For S/E parent stops, direct bounded geometry may be evaluated, but canonical membership remains mandatory. One exact parent-stop cause may own at most one physical Order_A; when multiple candidates compete, earliest canonical confirmation, then FirstIndex, then BreakIndex owns the cause.

### 9.2 Canonical stop

Order stop provenance comes from `MarketChronology.canonical_order_stop`. For Mode A it uses the canonical leg-head/floor context required by that opposite Reaction; for Mode B it uses the previous healthy opposite Reaction's outer edge under the established chronology. The Order's exact strict stop uses the **opposite direction** predicate; for this Bearish calculation that is `Low < OrderStop`. Equality does not stop an Order.

### 9.3 Parent validity and retention

An S explicitly identified in invalid_s_root_identities is calculation evidence, not an accepted S parent, and cannot create or retain a `parent-stop` Order_A cause. Once a valid canonical Order_A enters the identity-keyed ledger, later E/lifecycle reconciliation may change who uses it but cannot delete that physical identity/provenance. A shared Order_B identity may add reset-leg provenance without erasing valid parent-stop provenance.

## 10. Order_B — ACTIVE Bearish reset-leg rule

### 10.1 Eligibility and post-stop owner

Order_B is eligible only after an accepted lifecycle stop (`A`, `S`, `E`, or `StopAll`) selected by the accepted lifecycle owner of the stopped main candle. The stop opens eligibility; it is **not** the geometric HH anchor.

### 10.2 Geometric behavior anchor

For each reset Bearish Reaction, choose the latest accepted behavior source that exists strictly before the Reaction FirstGreen candle, independent of current dominance. Valid anchor families are A/S/E/StopAll. When several lifecycle projections share exactly one source candle, lifecycle priority and number resolve only that exact-source tie.

### 10.3 HH construction and extension

Use the closed main-candle range from anchor behavior source through reset Reaction FirstGreen, inclusive:

`HH = maximum High(anchor candle .. reset Reaction FirstGreen)`

Only a strict better High replaces the current source, so equal extremes retain the earliest source. The HH source must be strictly before the reset Reaction FirstGreen. It must also extend beyond the anchor itself: the HH must be strictly above the anchor behavior `High`; equality invalidates the setup.

### 10.4 Reset and strict break

The reset Reaction must first produce its canonical Reset. Search **strictly after** that exact Reset event for the first lower-TF `High > HH`. Equality is not a break. This exact lower-TF timestamp is `strict_break_time`.

### 10.5 Accepted-A expiry

Let the next accepted A formation after the reset Reaction First be `A_next`. If `A_next <= strict_break_time`, the pending reset leg expires. A is upstream of Order_B feedback, so this hard expiry prevents a stale S/E/StopAll setup from firing inside a newer A lifecycle.

### 10.6 Physical canonical opposite Reaction

After the strict break, choose the first canonical Bullish Reaction satisfying both:

`strict_break_time <= FirstTime`

`strict_break_time < ConfirmationTime`

Thus **FirstTime equality is valid**, while the price break and confirmation remain strict. Canonical-Reaction membership is mandatory; geometry-only evidence cannot become Order_B.

### 10.7 Provenance and identity

Order_B records post-stop behavior, geometric anchor type/source/extreme, reset Reaction identity/confirmation, Reset index/broken level/time, frozen HH boundary/source, exact strict break, and final physical opposite Reaction identity/confirmation. Physical Order identity remains `(FirstIndex, BreakIndex)`. Multiple reset-leg causes may merge into one identity; they do not create duplicate physical Orders.

## 11. Order / OrderAudit architecture

1. The identity-keyed Order ledger is canonical; parent labels are provenance, not identity.
2. Creation causes are exactly `parent-stop` (Order_A) and `reset-leg` (Order_B). `carried-live` and `accepted-live` are consumption/use routes.
3. One exact parent-stop event has one physical Order_A owner. Cause deduplication ranks by confirmation, FirstIndex, BreakIndex.
4. `prepare_order_audit` merges S-stage and E-stage accepted ledgers, retains identities outside the presentation range when required by a visible behavior, deduplicates causes, and computes a strict stop only when it was not already authoritative.
5. `accepted_audit_entry` filters an A-owned identity to accepted A provenance without discarding the complete physical cause set used for presentation.
6. OrderAudit must not fabricate parentage: invalid/suppressed parents lose creation rights; valid historical parent-stop provenance survives later consumer reconciliation.
7. The active physical Order routes are Order_A and Order_B.

## 12. Lifecycle / StopAll — ACTIVE specification

### 12.1 Shared priority and directional invariance

Lifecycle family semantics are direction-invariant. The cross-stage priority is exactly:

`StopAll > E Red > S Red > E Blue > S Blue > A`

Within a stage/family, accepted number/source chronology supplies deterministic ties. Directional price movement enters only through the strict Bearish stop predicate.

### 12.2 Dominant S/E sequence state

Accepted S/E objects remain valid output even when lower priority prevents them from replacing current dominant sequence ownership. Repeated exact dominant S color or exact E `(family, number)` increments its occurrence count. A higher-priority incoming behavior replaces lower dominant state. For E within equal family priority, a larger same-family number advances the dominant E group; Red E dominates Blue E.

### 12.3 E-driven StopAll

If an existing active StopAll is strictly stopped before/equal to an incoming E decision, the incoming E constructs the next numbered StopAll and the stopped active StopAll leaves current active ownership. Separately, when the current dominant S or exact E group has at least two accepted occurrences and its owning behavior strictly stops at or before the incoming E decision, that E becomes `StopAll1` through the `sequence-group-stop` gate. The incoming E supplies the physical Order/provenance; its family need not equal the stopped group.

### 12.4 Exact Blue-repeat reversal gate

Blue-repeat evidence is **accepted-occurrence counting**, independent of dominant-owner transitions:

- all S Blue occurrences share exact key `S` regardless of S subtype;
- every numbered E Blue has its own key: `E1`, `E2`, `E3`, ...;
- different E numbers never add together;
- a key qualifies only at count `>= 2`;
- the incoming reversal must be an accepted **S Red with native Mode-B formation Order**;
- among qualified keys, the latest accepted qualifying occurrence owns deterministic metadata;
- any accepted Red S, accepted Red E, or hard StopAll boundary clears prior Blue-repeat evidence, so stale Blue evidence cannot be consumed later.

A qualifying S Red is promoted to fresh `StopAll1` through `opposite-s-group-stop`. S/Red/Blue labels are not direction-mirrored.

### 12.5 Hard StopAll boundary

StopAll is a hard historical boundary. Once decided from already-reconciled chronology, future state cannot retroactively remove or move that prefix boundary. Creation resets active sequence keys/counts, dominant owners and pending Blue-repeat evidence. Historical StopAll objects remain output; only current-cycle ownership resets. E receives the accepted StopAll source map through an atomic sequence-reset publication: the sorted boundary index is refreshed and candidate/carried context caches are invalidated once, while immutable physical crossing/stop caches and historical accepted causes remain retained. For downstream audit semantics, but StopAll reconciliation does not rebuild past E from future reset state.

### 12.6 Cross-stage A/S/E visibility ownership

A, S and E calculations continue to retain internal historical evidence. Public ownership is resolved from exact strict stops, source chronology and shared priority. A source that strictly extends beyond the newest stopped owner can be consumed as the closed owner's next leg head instead of re-entering as equal/smaller behavior; equality stays with the earlier owner. S under a stopped larger owner obeys analogous chronology-first ownership; a higher-priority Red S may supersede a stopped Blue S, while equal/lower candidates remain owned by the prior lifecycle. Final E/StopAll source occupancy removes duplicate A/S labels on the same physical source, while referenced historical parents are retained for lineage closure.

## 13. Serialization / API contract

### 13.1 Projection rule

Legacy serialization contains no trading recalculation. Decimal prices are stringified; native local datetimes are converted through the existing Tehran-local epoch contract. Stable source ordering is preserved. Presentation range filtering is applied after full calculation, and OrderAudit may retain a pre-range physical identity when an in-range public behavior references it. `calculationValid` is emitted as `true` for public A/S because invalid calculation objects have already been removed by the calculation/visibility owner.

### 13.2 Legacy JSON fields

- **Reaction:** `firstIndex`, `firstTime`, `boxTopSourceIndex`, `boxTopSourceTime`, `boxTop`, `boxBottomSourceIndex`, `boxBottomSourceTime`, `boxBottom`, `breakIndex`, `breakTime`, `mode`.
- **Reset:** `index`, `time`, `secondTime`, `brokenLevel`, `fromFirstIndex`.
- **BlueLine:** `direction`, `kind`, `reactionNumber`, `previousStrikeCount`, `strikeCount`, `fibonacciLevel`, `sourceIndex`, `sourceTime`, `sourceExtreme`, `brokenLevel`, `linePrice`, `startTime`, `endTime`.
- **A:** `direction`, `blue1Ordinal`, `blue2Ordinal`, `blue1SourceTime`, `blue2SourceTime`, `blue1StopTime`, `blue2StopTime`, `blue1StopLevel`, `blue2StopLevel`, `continuationLevel`, `continuationSourceIndex`, `continuationSourceTime`, `triggerIndex`, `triggerTime`, `triggerEventTime`, `reactionNumber`, `reactionFirstTime`, `reactionBreakTime`, `sourceIndex`, `sourceTime`, `price`, `calculationValid`.
- **S:** `direction`, `color`, `formationType`, `aOrdinal`, `aSourceIndex`, `aSourceTime`, `aPrice`, `aStopIndex`, `aStopTime`, `aStopEventTime`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `resetReactionNumber`, `resetTime`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`, `calculationValid`.
- **E:** `direction`, `family`, `number`, `parentType`, `parentSourceIndex`, `parentSourceTime`, `parentPrice`, `parentStopIndex`, `parentStopTime`, `parentStopEventTime`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderCauses`, `orderParentStopCauseTime`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`.
- **StopAll:** `direction`, `number`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`, `gateType`, `gateEventTime`, `stoppedBehaviorType`, `stoppedBehaviorKey`, `stoppedBehaviorCount`, `underlyingEFamily`, `underlyingENumber`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderCauses`, `orderParentStopCauseTime`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `stopIndex`, `stopTime`, `stopEventTime`.
- **OrderAudit:** `direction`, `reactionNumber`, `reactionMode`, `firstIndex`, `firstTime`, `boxTopSourceIndex`, `boxTopSourceTime`, `boxTop`, `boxBottomSourceIndex`, `boxBottomSourceTime`, `boxBottom`, `breakIndex`, `breakTime`, `stopLevel`, `stopSourceIndex`, `stopSourceTime`, `stopHitIndex`, `stopHitTime`, `stopHitEventTime`, `causes`.

### 13.3 Response envelope

The envelope contains `engine`, `version`, `pipelineVersion`, `blueLineVersion`, `aVersion`, `sVersion`, `eVersion`, `stopAllVersion`, enablement booleans, `timeframe`, `actualFrom`, `actualTo`, `directions`, and runtime `timings`. Each requested direction owns its own Reaction/Reset/Blue/A/S/E/StopAll/OrderAudit arrays.

### 13.4 Optional Bridge Output

`--bridge-output` adds a read-only projection built only from finalized calculation selections and canonical OrderAudit. It may validate a recorded strict event, but it must not search for a substitute trading event or mutate detector/lifecycle state. Physical Order joins use `(FirstIndex, BreakIndex)` and exact accepted causes, never list position.

### 13.5 Complete Source symbol and schema coverage

This inventory comes from the current Production AST after complete semantic review. AST addresses identify Source; they do not substitute for semantic validation. Package markers are retained for exact reconstruction; the production dynamic loader is the supported import surface.

#### `__init__.py`

**Module constants:** none.
**Top-level functions:** none.

#### `bridge/__init__.py`

**Module constants:** none.
**Top-level functions:** none.

#### `bridge/trading_pipeline.py`

**Module constants:** `_ENGINE_ROOT`, `_PIPELINE_DIR`, `_pipeline_dir_text`, `_DTFMT`, `TRADING_PIPELINE_VERSION`, `TRADING_PIPELINE_IMPLEMENTATION_VERSION`, `TRADING_PIPELINE_LAST_MODIFIED`, `TEHRAN`.
**Top-level functions:** `emit_progress()`, `timed()`, `load_module()`, `load_engine()`, `local_datetime()`, `epoch()`, `display_epoch()`, `build_candle_buckets()`, `build_candle_objects()`, `_index_selected()`, `select_reaction_serialization_items()`, `serialize()`, `serialize_blue_lines()`, `serialize_a_zones()`, `serialize_s_zones()`, `serialize_e_zones()`, `serialize_stopalls()`, `bridge_datetime()`, `bridge_direction()`, `bridge_mode()`, `bridge_color()`, `_bridge_horizon()`, `_bridge_in_horizon()`, `_bridge_proven_strict_event()`, `_bridge_stop_view()`, `_bridge_reaction_confirmation()`, `_bridge_order_identity()`, `_bridge_parent_stop()`, `_bridge_a_stop()`, `_bridge_behavior_stop()`, `_bridge_blue_formation()`, `_bridge_project_reaction()`, `_bridge_project_reset()`, `_bridge_project_blue()`, `_bridge_full_lines_by_ordinal()`, `_bridge_project_a()`, `_bridge_project_s()`, `_bridge_source_index()`, `_bridge_parent_behavior_for_e()`, `_bridge_project_e()`, `_bridge_project_stopall()`, `_bridge_audit_order_key()`, `build_bridge_output()`, `validate_order_audit_bridge()`, `serialize_order_audit()`, `parse_arguments()`, `load_engines()`, `prepare_market_context()`, `create_e_detector()`, `calculate_full_direction_state()`, `calculate_direction_with_order_b_feedback()`, `prepare_pipeline_state()`, `calculate_direction_range_state()`, `finalize_direction_visibility()`, `serialize_direction_payload()`, `build_direction_output()`, `build_response_payload()`, `main()`.
- **`BridgeProjection`** (source line 639)
  - methods: `__init__()`, `physical_order()`, `parent_order()`, `current_order()`, `order_audit()`
- **`EngineBundle`** (source line 1578)
  - fields: `reaction`, `blue_line`, `a_zone`, `s_zone`, `e_zone`, `lifecycle`
- **`MarketContext`** (source line 1588)
  - fields: `seconds`, `candles`, `lower_index`, `chronology`, `start_index`, `end_index`
- **`PipelineState`** (source line 1784)
  - fields: `directions`, `results`, `reusable_full_context`, `initial_order_geometry`, `internal_reaction_identities`, `full_e_zones`, `full_e_detectors`, `full_s_detectors`, `full_lines_by_direction`, `full_a_by_direction`, `invalid_a_identities_by_direction`, `invalid_s_identities_by_direction`, `full_s_by_direction`, `full_s_candidates_by_direction`
- **`FullDirectionState`** (source line 1804)
  - fields: `e_zones`, `e_detector`, `s_detector`, `blue_lines`, `a_zones`, `invalid_a_identities`, `invalid_s_identities`, `s_zones`, `s_candidates`, `initial_s_zones`
- **`DirectionRangeState`** (source line 2347)
  - fields: `blue_lines`, `a_zones`, `s_candidates`, `accepted_s_zones`, `e_zones`, `invalid_a_identities`, `invalid_s_identities`
- **`DirectionVisibilityState`** (source line 2360)
  - fields: `blue_lines`, `a_zones`, `s_zones`, `e_zones`, `stopalls`, `prepared_order_audit`, `projection_s_zones`, `projection_e_zones`, `projection_stopalls`

#### `pipeline/__init__.py`

**Module constants:** `__all__`.
**Top-level functions:** none.

#### `pipeline/a_zone_detector.py`

**Module constants:** `A_ZONE_VERSION`, `A_ZONE_LAST_MODIFIED_DATE`.
**Top-level functions:** `detect_a_zones()`.
- **`BlueState`** (source line 25)
  - fields: `ordinal`, `line`, `formation_index`, `formation_time`, `stop_index`, `stop_time`, `stop_event_time`, `stop_level`, `stop_event_extreme`
- **`AZone`** (source line 38)
  - fields: `direction`, `blue_1_ordinal`, `blue_2_ordinal`, `blue_1_source_time`, `blue_2_source_time`, `blue_1_stop_time`, `blue_2_stop_time`, `blue_1_stop_level`, `blue_2_stop_level`, `continuation_level`, `continuation_source_index`, `continuation_source_time`, `trigger_index`, `trigger_time`, `trigger_event_time`, `reaction_number`, `reaction_first_time`, `reaction_break_time`, `source_index`, `source_time`, `price`, `formation_route`, `blue_1_stop_event_time`, `blue_2_stop_event_time`
- **`AZoneDetector`** (source line 67)
  - methods: `__init__()`, `extreme_name()`, `_strict_cross()`, `_better()`, `_main_index()`, `_lower_window()`, `_first_crossing()`, `_range_extreme()`, `_formation()`, `_reset_formation_time()`, `_build_blue_states()`, `_double_stop_a_candidates()`, `_pair_trigger()`, `_reaction_confirmation_time()`, `_first_reaction_after()`, `_inherited_stop()`, `_a_source()`, `_detect_ordinary_a()`, `_filter_special_a()`, `detect()`, `_a_was_stopped_before()`

#### `pipeline/blue_line_detector.py`

**Module constants:** `BLUE_LINE_VERSION`, `FIBONACCI_RATIO`.
**Top-level functions:** `_is_color()`, `_main_candle()`, `_stops_on_index()`, `fibonacci_level()`, `_intrabar_pending_confirmation()`, `count_scale_strikes()`, `_build_scale_blue_line()`, `_build_reset_blue_line()`, `detect_blue_lines()`, `public_blue_lines()`, `mark_internal_blue_lines()`.
- **`ScaleStrike`** (source line 23)
  - fields: `source_index`, `source_time`, `extreme`
- **`BlueLine`** (source line 30)
  - fields: `direction`, `kind`, `reaction_number`, `previous_strike_count`, `strike_count`, `fibonacci_level`, `source_index`, `source_time`, `source_extreme`, `broken_level`, `line_price`, `start_time`, `end_time`, `calculation_valid`, `behavior_internal`

#### `pipeline/core_utils.py`

**Module constants:** `CORE_UTILS_VERSION`.
**Top-level functions:** `as_decimal()`, `order_identity()`, `reaction_identity()`.

#### `pipeline/direction_policy.py`

**Module constants:** `DIRECTION_POLICY_VERSION`, `Direction`, `BULLISH`, `BEARISH`.
**Top-level functions:** `policy_for()`.
- **`DirectionPolicy`** (source line 21)
  - fields: `direction`, `extreme_attr`, `opposite_extreme_attr`, `first_reaction_tag`, `context_tag`
  - methods: `opposite_direction()`, `strict_cross()`, `better_extreme()`, `choose_extreme()`, `confirmation_cross()`

#### `pipeline/e_zone_detector.py`

**Module constants:** `E_ZONE_VERSION`, `E_ZONE_IMPLEMENTATION_VERSION`, `E_ZONE_LAST_MODIFIED`.
**Top-level functions:** `detect_e_zones()`.
- **`EZone`** (source line 31)
  - fields: `direction`, `family`, `number`, `parent_type`, `parent_source_index`, `parent_source_time`, `parent_price`, `parent_stop_index`, `parent_stop_time`, `parent_stop_event_time`, `order_direction`, `order_reaction_number`, `order_mode`, `order_causes`, `order_parent_stop_cause_time`, `order_first_index`, `order_first_time`, `order_break_index`, `order_break_time`, `order_confirmation_time`, `order_box_top`, `order_box_top_source_index`, `order_box_top_source_time`, `order_box_bottom`, `order_box_bottom_source_index`, `order_box_bottom_source_time`, `order_stop_level`, `order_stop_source_index`, `order_stop_source_time`, `source_index`, `source_time`, `price`, `decision_index`, `decision_time`, `decision_event_time`
- **`EZoneDetector`** (source line 69)
  - methods: `__init__()`, `sequence_resets()`, `sequence_resets()`, `_reset_time()`, `_main_index()`, `_first_cross_position()`, `_stop_value()`, `_first_parent_stop()`, `_confirmation_for()`, `_confirmation()`, `_reaction_first_time()`, `_parent_stop()`, `parent_stop()`, `_extreme_between()`, `_zone()`, `set_consumed_s_evidence()`, `_apply_consumed_s_evidence()`, `continuation_chain_from_s()`, `replace_with_earlier_continuation()`, `resolve_same_source_conflicts()`, `restore_independent_s_roots()`, `_discover_candidate_chains()`, `_reconcile_candidate_chains()`, `detect()`

#### `pipeline/lifecycle_engine.py`

**Module constants:** `STOP_ALL_VERSION`, `STOP_ALL_IMPLEMENTATION_VERSION`, `STOP_ALL_LAST_MODIFIED`, `SEQUENCE_PRIORITY`.
**Top-level functions:** `sequence_priority()`, `detect_stopalls()`, `resolve_order_context()`, `visible_a_zones_after_s_stops()`, `module_priority()`, `module_identity()`, `module_stop_event()`, `strictly_beyond_boundary()`, `dominant_module()`, `split_a_zones_by_dominant_stops()`, `blocked_orders_while_invalid_leg_heads_are_live()`, `consumed_s_evidence_after_larger_stop()`, `s_zones_for_module_engines()`, `s_zones_for_stopall()`, `visible_s_zones_after_module_resets()`, `reconcile_stopall_lifecycle()`, `visible_a_zones_after_module_boundaries()`, `reaction_number_is_internal()`, `point_is_inside_healthy_reaction()`, `filter_internal_behavior_outputs()`, `finalize_behavior_visibility()`, `visible_a_zones()`.
- **`StopAll`** (source line 43)
  - fields: `direction`, `number`, `source_index`, `source_time`, `price`, `decision_index`, `decision_time`, `decision_event_time`, `gate_type`, `gate_event_time`, `stopped_behavior_type`, `stopped_behavior_key`, `stopped_behavior_count`, `underlying_e_family`, `underlying_e_number`, `order_direction`, `order_reaction_number`, `order_mode`, `order_causes`, `order_parent_stop_cause_time`, `order_first_index`, `order_first_time`, `order_break_index`, `order_break_time`, `order_confirmation_time`, `order_box_top`, `order_box_top_source_index`, `order_box_top_source_time`, `order_box_bottom`, `order_box_bottom_source_index`, `order_box_bottom_source_time`, `order_stop_level`, `order_stop_source_index`, `order_stop_source_time`, `stop_index`, `stop_time`, `stop_event_time`, `donor_type`, `donor_source_index`, `donor_source_time`, `donor_color`, `donor_number`, `donor_price`, `donor_stop_time`, `donor_stop_event_time`
- **`StopAllDetector`** (source line 95)
  - methods: `__init__()`, `_strict_stop()`, `_e_key()`, `_dominates_e()`, `_sequence_priority()`, `_active_sequence_priority()`, `_stopall_from_e()`, `_optional_int()`, `_optional_decimal()`, `_stopall_from_s()`, `_blue_repeat_key()`, `_record_blue_repeat()`, `_opposite_s_stopall_gate()`, `detect()`

#### `pipeline/order_audit_engine.py`

**Module constants:** `ORDER_AUDIT_ENGINE_VERSION`, `ORDER_AUDIT_ENGINE_LAST_MODIFIED`, `OrderMatch`.
**Top-level functions:** `dominant_post_behavior_stops()`, `order_b_reset_event_time()`, `discover_order_b_reset_legs()`, `discover_accepted_order_b_reset_legs()`, `order_b_leg_identity()`, `prepare_order_audit()`, `accepted_audit_entry()`, `order_identity_is_internal()`.
- **`PostBehaviorStop`** (source line 18)
  - fields: `behavior_type`, `behavior_source_index`, `behavior_source_time`, `event_time`
- **`OrderBBehaviorAnchor`** (source line 26)
  - fields: `behavior_type`, `behavior_source_index`, `behavior_source_time`, `priority`, `number`
- **`OrderBResetLeg`** (source line 35)
  - fields: `post_stop`, `anchor_behavior_type`, `anchor_behavior_source_index`, `anchor_behavior_source_time`, `anchor_behavior_extreme`, `reset_reaction`, `reset_confirmation_time`, `reset_source_index`, `reset_broken_level`, `reset_time`, `leg_boundary`, `leg_source_index`, `leg_source_time`, `strict_break_time`, `reaction_number`, `physical_reaction`, `physical_confirmation_time`
- **`OrderAuditEngineMixin`** (source line 437)
  - methods: `_order_stop()`, `order_stop()`, `_first_healthy_direct_geometry()`, `_trend_leg_direct_order()`, `_direct_parent_stop_order()`, `_merge_order_candidate()`, `_enforce_single_parent_stop_owner()`, `order_candidates()`, `_first_order()`, `_has_sequence_reset_between()`, `_index_order_audit_identity()`, `_clear_order_audit()`, `register_order_b_reset_legs()`, `_register_order_audit()`, `visual_order_lifecycle()`, `_cross_order()`, `cross_order()`, `_unconsumed_s_orders()`, `_initial_order_records()`, `_initial_record_match()`, `_initial_order_match()`, `_gate_owned_initial_order()`, `_carried_orders_for_parent()`, `_post_stop_accepted_orders_for_parent()`, `_blocked_by_gate_owned_order()`, `_rebuild_accepted_order_audit()`, `rebuild_accepted_order_audit()`, `ensure_accepted_order_audit()`
- **`SOrderAuditMixin`** (source line 1734)
  - methods: `_first_order_after()`, `_order_matches_after()`, `_record_a_order_audit()`, `_audit_stopped_a()`, `_order_stop()`, `_order_stop_crossed()`, `_shared_order_stop_cross()`

#### `pipeline/reaction_engine.py`

**Module constants:** `REACTION_ENGINE_VERSION`, `REACTION_ENGINE_LAST_MODIFIED`.
**Top-level functions:** `classify_candle_color()`, `opposite_direction()`, `mirror_candle()`, `mirror_candidate()`, `mirror_analysis()`, `_reflected_view()`, `published_reaction_candidate()`, `_decimal_value()`, `shared_lower_timeframe_index()`, `build_behavior_reaction_views()`, `directional_a_stop_order_finder()`.
- **`Candle`** (source line 27)
  - fields: `index`, `timestamp`, `display_time`, `tag`, `open`, `high`, `low`, `close`
- **`Candidate`** (source line 39)
  - fields: `first_idx`, `first_time`, `box_top_source_idx`, `box_top_source_time`, `box_top`, `box_bottom_source_idx`, `box_bottom_source_time`, `box_bottom`, `mode`, `anchor_idx`, `anchor_value`, `leg_boundary_value`, `break_idx`, `break_time`, `intrabar_start`, `cross_direction_origin`, `cross_direction_chain_owner`, `order_gate_decision`, `behavior_public_number`, `behavior_public_box_top`, `behavior_public_box_bottom`, `behavior_confirmation_time`, `behavior_first_time`, `behavior_internal`
- **`ResetEvent`** (source line 67)
  - fields: `index`, `display_time`, `second_time`, `broken_level`, `from_first_idx`
- **`IntrabarAnalysis`** (source line 76)
  - fields: `event_second`, `extreme`, `extreme_source`
- **`DetectionResult`** (source line 83)
  - fields: `direction`, `reactions`, `resets`, `start_index`, `end_index`
- **`DetectorBase`** (source line 101)
  - methods: `__init__()`, `_shared_time_index()`, `seconds_between()`, `main_source_for_time()`, `minimum_low()`, `maximum_high()`
- **`BullishDetector`** (source line 174)
  - methods: `green_run_peak_before()`, `breakout_analysis()`, `mode_a_invalidation_before_breakout()`, `confirmed_reset_before_breakout()`, `post_breakout_reset()`, `detect()`
- **`_ReflectedCandles`** (source line 608)
  - methods: `__init__()`, `__len__()`, `__getitem__()`
- **`BearishDetector`** (source line 646)
  - methods: `__init__()`, `red_run_bottom_before()`, `breakdown_analysis()`, `invalidation_high_break_before_breakdown()`, `confirmed_reset_before_breakdown()`, `post_breakdown_reset()`, `detect()`
- **`LowerTimeframeIndex`** (source line 809)
  - methods: `__init__()`, `first_less()`, `first_greater()`, `range_minimum()`, `range_maximum()`, `_range_query()`, `_first()`
- **`ReflectedLowerTimeframeIndex`** (source line 947)
  - methods: `__init__()`, `first_less()`, `first_greater()`, `range_minimum()`, `range_maximum()`
- **`MarketChronology`** (source line 971)
  - methods: `__init__()`, `opposite_direction()`, `main_index()`, `lower_bounds()`, `lower_window()`, `_reset_cache_key()`, `_reaction_cache_key()`, `reset_time()`, `reaction_confirmation()`, `canonical_order_stop()`
- **`UnifiedReactionDetector`** (source line 1376)
  - methods: `__init__()`, `bull()`, `bear()`, `_append_reaction()`, `_append_reset()`, `_refine()`, `_candidate_from_confirmation_remainder()`, `_first_initial()`, `_first_direct_same_direction_after_reset()`, `_first_geometry_after_reset()`, `first_geometry_after_reset()`, `_reaction_break_indices()`, `first_order_reaction_after_gate()`, `_earliest_confirmed_geometry()`, `_build_direct_candidate()`, `_scan_direct_candidate()`, `_owner_boundary_before_confirmation()`, `_result()`, `detect()`

#### `pipeline/s_zone_detector.py`

**Module constants:** `S_ZONE_VERSION`, `S_ZONE_IMPLEMENTATION_VERSION`, `S_ZONE_LAST_MODIFIED`.
**Top-level functions:** `detect_s_zones()`.
- **`SZone`** (source line 28)
  - fields: `direction`, `color`, `formation_type`, `a_ordinal`, `a_source_index`, `a_source_time`, `a_price`, `a_stop_index`, `a_stop_time`, `a_stop_event_time`, `order_direction`, `order_reaction_number`, `order_mode`, `order_first_index`, `order_first_time`, `order_break_index`, `order_break_time`, `order_confirmation_time`, `order_box_top`, `order_box_top_source_index`, `order_box_top_source_time`, `order_box_bottom`, `order_box_bottom_source_index`, `order_box_bottom_source_time`, `order_stop_level`, `order_stop_source_index`, `order_stop_source_time`, `reset_reaction_number`, `reset_time`, `source_index`, `source_time`, `price`, `decision_index`, `decision_time`, `decision_event_time`
- **`SZoneDetector`** (source line 66)
  - methods: `__init__()`, `_main_index()`, `_lower_window()`, `_reaction_confirmation_time()`, `reaction_confirmation_time()`, `_reset_time()`, `_a_confirmation_time()`, `_trend_extreme()`, `_a_stopped()`, `_first_a_stop()`, `first_a_stop()`, `_resolved_order_backed_zone()`, `_candidate_source()`, `_candidate_source_last()`, `_first_trend_reaction_after_order()`, `_nested_trend_reaction()`, `_simple_candidate()`, `_type3_reset_leg()`, `_type3_has_trend_reaction()`, `_first_type3()`, `_type4_has_blue()`, `_first_type4()`, `_build_type4_zone()`, `_candidate_after_order()`, `_a_source_event_time()`, `_a_owned_by_s()`, `_a_pair_is_reset_reset()`, `eligible_a_zones()`, `_candidate_timing()`, `_candidate_before_order()`, `_candidate_event_time()`, `candidate_event_time()`, `_blue_formation_time()`, `_candidate_cross_has_blue()`, `_has_ordinary_trend_reaction()`, `_candidate_crossed()`, `_decision()`, `_build_type3_zone()`, `_build_order_backed_zone()`, `detect()`, `reconcile_shared_order_stops()`

## 14. Verification scope for the current release

Current validation covers every current Python file, supported production initialization, both exact reconstructed trees, a full semantic function/branch/comparator review, independent primitive oracles, synthetic mirrored state sequences, current unit tests and frontend compatibility checks. The release validation report records actual command exits and measured counts. Static parsing, bounded synthetic parity and current retrieval integrity do not establish independent real-market correctness.

Market regression: **NOT_TESTED**. The current task deliberately keeps the Vault RAW and Fixture stores empty. No old market run, historical RAW filename, candle expectation or old regression hash is current release evidence.

The supported dynamic loader bypasses the legacy package-wrapper import surface. Generic `import engine.pipeline` is unsupported under the current project contract and is not counted as a production initialization failure.

## 15. Current revision record

### `5.4.19-EX1` — ACTIVE

The current patch fixes two demonstrated owning-layer defects: explicitly invalid S evidence cannot recreate or retain a parent-stop Order_A cause during audit reconstruction; publication of sequence-reset boundaries refreshes its sorted index and invalidates dependent context caches atomically. Valid historical Order_A and shared Order_B provenance remain retained. E and OrderAudit versions are recorded in Section 1.

Documentation now specifies the inclusive Blue confirmation row, inclusive S common-stop source start, inclusive Type-4 candidate search start, inclusive E-group StopAll event boundary, bounded post-Reset completion selection and actual supplied-input/pipeline ordering. Both directional documents share the same exact current Source snapshot and direction-invariant lifecycle, identity, Doji, ordering and serialization contracts. Old active correction overrides and historical market evidence are removed.

## 16. Exact Production Source snapshot

Every current Engine Python file is embedded below, including package files. Raw UTF-8 bytes, line endings, whitespace, comments and final-newline structure are preserved. Machine-readable markers permit independent extraction and byte comparison.

### 16.1 `__init__.py` — Package marker / unsupported wrapper

**SHA-256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`  
**Bytes:** `0`  
**LF count:** `0`

<!-- EXACT-SOURCE-BEGIN:__init__.py -->
````python
````
<!-- EXACT-SOURCE-END:__init__.py -->

### 16.2 `bridge/__init__.py` — Package marker / unsupported wrapper

**SHA-256:** `2bc59770b9d4313c0e6306287d074487b9e1672dbaf3ada9a8be381e7123f0b8`  
**Bytes:** `64`  
**LF count:** `1`

<!-- EXACT-SOURCE-BEGIN:bridge/__init__.py -->
````python
"""Bridge entrypoints for the TradingBot calculation engine."""
````
<!-- EXACT-SOURCE-END:bridge/__init__.py -->

### 16.3 `bridge/trading_pipeline.py` — Pipeline / Serialization

**SHA-256:** `ef5109f4ebb95bc0e04b3d964b14da5f764ae4472f3d10a1a9b7192d59fec683`  
**Bytes:** `107807`  
**LF count:** `2952`

<!-- EXACT-SOURCE-BEGIN:bridge/trading_pipeline.py -->
````python
"""Production trading pipeline orchestration, input normalization, and serialization.

Owns request parsing, raw-range isolation, candle construction, engine loading,
stage orchestration, progress/timing telemetry, and JSON serialization. Trading
validity/ownership rules belong to their calculation engines; this module must
not reimplement them.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import orjson
from bisect import bisect_left
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from time import perf_counter
from typing import Sequence
from zoneinfo import ZoneInfo

# This bridge lives in ``engine/bridge`` while the calculation modules live in
# the sibling ``engine/pipeline`` package.  Put that directory on the module
# search path before importing shared helpers or dynamically loading detectors.
# The detector files intentionally keep their flat local imports
# (``core_utils`` / ``direction_policy``), so this single bootstrap point keeps
# every production module aligned with the deployed folder structure.
_ENGINE_ROOT = Path(__file__).resolve().parents[1]
_PIPELINE_DIR = _ENGINE_ROOT / "pipeline"
_pipeline_dir_text = str(_PIPELINE_DIR)
if _pipeline_dir_text not in sys.path:
    sys.path.insert(0, _pipeline_dir_text)

from core_utils import as_decimal, order_identity
from order_audit_engine import order_b_leg_identity

_DTFMT = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}"


TRADING_PIPELINE_VERSION = "1.7.0"
TRADING_PIPELINE_IMPLEMENTATION_VERSION = "1.8.0"
TRADING_PIPELINE_LAST_MODIFIED = "2026-09-27 23:17:17 +03:30"

TEHRAN = ZoneInfo("Asia/Tehran")


def emit_progress(status: str, label: str, duration_ms: float | None = None):
    """Send machine-readable lifecycle events without contaminating JSON stdout."""
    event = {"status": status, "label": label}
    if duration_ms is not None:
        event["durationMs"] = round(duration_ms, 2)
    print(f"QG_PROGRESS:{json.dumps(event, separators=(',', ':'))}", file=sys.stderr, flush=True)


def timed(timings: dict[str, float], label: str, work):
    """Measure an existing pipeline phase without changing its inputs or output."""
    started = perf_counter()
    emit_progress("started", label)
    try:
        return work()
    finally:
        duration_ms = (perf_counter() - started) * 1000
        timings[label] = timings.get(label, 0.0) + duration_ms
        emit_progress("completed", label, duration_ms)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load reaction engine: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_engine(path: Path):
    return load_module("reaction_engine", path)


_local_dt_cache: dict[int, datetime] = {}


def local_datetime(epoch: int) -> datetime:
    cached = _local_dt_cache.get(epoch)
    if cached is not None:
        return cached
    result = datetime.fromtimestamp(epoch, TEHRAN).replace(tzinfo=None)
    _local_dt_cache[epoch] = result
    return result


_epoch_cache: dict[datetime, int] = {}


def epoch(local: datetime) -> int:
    cached = _epoch_cache.get(local)
    if cached is not None:
        return cached
    result = int(local.replace(tzinfo=TEHRAN).timestamp())
    _epoch_cache[local] = result
    return result


_display_epoch_cache: dict[str, int] = {}


def display_epoch(value: str | datetime) -> int:
    """Convert an engine display/native timestamp once per pipeline process."""
    if isinstance(value, datetime):
        return epoch(value)
    cached = _display_epoch_cache.get(value)
    if cached is not None:
        return cached
    result = epoch(datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
    _display_epoch_cache[value] = result
    return result


def build_candle_buckets(rows: list[dict], timeframe: int):
    """Normalize raw rows once, preserving lower and selected-timeframe buckets."""
    second_buckets: list[dict] = []
    current_second = None
    buckets: list[dict] = []
    current = None
    to_decimal = as_decimal
    decimal_cache: dict[tuple[type, object], Decimal] = {}

    def cached_decimal(value: object) -> Decimal:
        # Raw prices repeat heavily. Cache by both type and value so values
        # such as ``10`` and ``10.0`` retain their exact string-normalized
        # Decimal representation instead of being conflated by Python's
        # numeric equality rules.
        key = (type(value), value)
        try:
            return decimal_cache[key]
        except KeyError:
            normalized = to_decimal(value)
            decimal_cache[key] = normalized
            return normalized

    for row in rows:
        timestamp = int(row["time"])
        o = cached_decimal(row["open"])
        high = cached_decimal(row["high"])
        low = cached_decimal(row["low"])
        close = cached_decimal(row["close"])
        if current_second is None or current_second["time"] != timestamp:
            current_second = {
                "time": timestamp,
                "open": o,
                "high": high,
                "low": low,
                "close": close,
            }
            second_buckets.append(current_second)
        else:
            current_second["high"] = max(current_second["high"], high)
            current_second["low"] = min(current_second["low"], low)
            current_second["close"] = close
        bucket_time = timestamp if timeframe == 1 else timestamp // timeframe * timeframe
        if current is None or current["time"] != bucket_time:
            current = {
                "time": bucket_time,
                "open": o,
                "high": high,
                "low": low,
                "close": close,
            }
            buckets.append(current)
        else:
            current["high"] = max(current["high"], high)
            current["low"] = min(current["low"], low)
            current["close"] = close
    return second_buckets, buckets


def build_candle_objects(engine, buckets: list[dict]):
    """Create maintained engine candles from already-normalized buckets."""
    candles = []
    append = candles.append
    candle_type = engine.Candle
    classify = engine.classify_candle_color
    local = local_datetime
    fmt = _DTFMT.format
    for index, item in enumerate(buckets):
        stamp = local(item["time"])
        append(candle_type(
            index=index,
            timestamp=stamp,
            display_time=fmt(
                stamp.year,
                stamp.month,
                stamp.day,
                stamp.hour,
                stamp.minute,
                stamp.second,
            ),
            tag=classify(item["open"], item["close"]),
            open=item["open"],
            high=item["high"],
            low=item["low"],
            close=item["close"],
        ))
    return candles


def _index_selected(index: object, start_index: int | None, end_index: int | None) -> bool:
    return (
        start_index is None
        or end_index is None
        or start_index <= int(index) <= end_index
    )


def select_reaction_serialization_items(
    result, start_index=None, end_index=None, reaction_transform=None,
):
    """Select the exact legacy Reaction/Reset sequence once for both views.

    This is a presentation selection only.  It retains the legacy filtering
    and ordering verbatim while exposing the same finalized source objects to
    the optional Bridge Output projector.
    """
    resets = [
        item
        for item in result.resets
        if _index_selected(item.index, start_index, end_index)
    ]
    reactions = []
    for item in result.reactions:
        if not _index_selected(item.first_idx, start_index, end_index):
            continue
        public_item = reaction_transform(item) if reaction_transform is not None else item
        reactions.append((item, public_item))
    return reactions, resets


def serialize(
    result,
    start_index=None,
    end_index=None,
    reaction_transform=None,
    selected_items=None,
):
    """Serialize legacy Reaction/Reset output without changing its contract."""
    selected_reactions, selected_resets = (
        selected_items
        if selected_items is not None
        else select_reaction_serialization_items(
            result, start_index, end_index, reaction_transform
        )
    )
    resets = [{
        "index": item.index,
        "time": display_epoch(item.display_time),
        "secondTime": (
            display_epoch(item.second_time)
            if item.second_time is not None
            else None
        ),
        "brokenLevel": str(item.broken_level),
        "fromFirstIndex": item.from_first_idx,
    } for item in selected_resets]
    reactions = []
    for _item, public_item in selected_reactions:
        reactions.append({
            "firstIndex": public_item.first_idx,
            "firstTime": display_epoch(public_item.first_time),
            "boxTopSourceIndex": public_item.box_top_source_idx,
            "boxTopSourceTime": display_epoch(public_item.box_top_source_time),
            "boxTop": str(public_item.box_top),
            "boxBottomSourceIndex": public_item.box_bottom_source_idx,
            "boxBottomSourceTime": display_epoch(public_item.box_bottom_source_time),
            "boxBottom": str(public_item.box_bottom),
            "breakIndex": public_item.break_idx,
            "breakTime": display_epoch(public_item.break_time),
            "mode": public_item.mode,
        })
    return reactions, resets


def serialize_blue_lines(items, start_index=None, end_index=None):
    return [{
        "direction": item.direction,
        "kind": item.kind,
        "reactionNumber": item.reaction_number,
        "previousStrikeCount": item.previous_strike_count,
        "strikeCount": item.strike_count,
        "fibonacciLevel": str(item.fibonacci_level) if item.fibonacci_level is not None else None,
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "sourceExtreme": str(item.source_extreme),
        "brokenLevel": str(item.broken_level) if item.broken_level is not None else None,
        "linePrice": str(item.line_price),
        "startTime": epoch(item.start_time),
        "endTime": epoch(item.end_time),
    } for item in items if _index_selected(
        getattr(item, "source_index"), start_index, end_index
    )]


def serialize_a_zones(items):
    return [{
        "direction": item.direction,
        "blue1Ordinal": item.blue_1_ordinal,
        "blue2Ordinal": item.blue_2_ordinal,
        "blue1SourceTime": epoch(item.blue_1_source_time),
        "blue2SourceTime": epoch(item.blue_2_source_time),
        "blue1StopTime": epoch(item.blue_1_stop_time),
        "blue2StopTime": epoch(item.blue_2_stop_time),
        "blue1StopLevel": str(item.blue_1_stop_level),
        "blue2StopLevel": str(item.blue_2_stop_level),
        "continuationLevel": str(item.continuation_level),
        "continuationSourceIndex": item.continuation_source_index,
        "continuationSourceTime": epoch(item.continuation_source_time),
        "triggerIndex": item.trigger_index,
        "triggerTime": epoch(item.trigger_time),
        "triggerEventTime": epoch(item.trigger_event_time),
        "reactionNumber": item.reaction_number,
        "reactionFirstTime": epoch(item.reaction_first_time),
        "reactionBreakTime": epoch(item.reaction_break_time),
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "calculationValid": True,
    } for item in items]


def serialize_s_zones(items):
    return [{
        "direction": item.direction,
        "color": item.color,
        "formationType": item.formation_type,
        "aOrdinal": item.a_ordinal,
        "aSourceIndex": item.a_source_index,
        "aSourceTime": epoch(item.a_source_time),
        "aPrice": str(item.a_price),
        "aStopIndex": item.a_stop_index,
        "aStopTime": epoch(item.a_stop_time),
        "aStopEventTime": epoch(item.a_stop_event_time),
        "orderDirection": item.order_direction,
        "orderReactionNumber": item.order_reaction_number,
        "orderMode": item.order_mode,
        "orderFirstIndex": item.order_first_index,
        "orderFirstTime": (
            epoch(item.order_first_time) if item.order_first_time is not None else None
        ),
        "orderBreakIndex": item.order_break_index,
        "orderBreakTime": (
            epoch(item.order_break_time) if item.order_break_time is not None else None
        ),
        "orderConfirmationTime": (
            epoch(item.order_confirmation_time)
            if item.order_confirmation_time is not None
            else None
        ),
        "orderBoxTop": str(item.order_box_top) if item.order_box_top is not None else None,
        "orderBoxTopSourceIndex": item.order_box_top_source_index,
        "orderBoxTopSourceTime": (
            epoch(item.order_box_top_source_time)
            if item.order_box_top_source_time is not None
            else None
        ),
        "orderBoxBottom": (
            str(item.order_box_bottom) if item.order_box_bottom is not None else None
        ),
        "orderBoxBottomSourceIndex": item.order_box_bottom_source_index,
        "orderBoxBottomSourceTime": (
            epoch(item.order_box_bottom_source_time)
            if item.order_box_bottom_source_time is not None
            else None
        ),
        "orderStopLevel": (
            str(item.order_stop_level) if item.order_stop_level is not None else None
        ),
        "orderStopSourceIndex": item.order_stop_source_index,
        "orderStopSourceTime": (
            epoch(item.order_stop_source_time)
            if item.order_stop_source_time is not None
            else None
        ),
        "resetReactionNumber": item.reset_reaction_number,
        "resetTime": epoch(item.reset_time) if item.reset_time is not None else None,
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "decisionIndex": item.decision_index,
        "decisionTime": epoch(item.decision_time),
        "decisionEventTime": epoch(item.decision_event_time),
        "calculationValid": True,
    } for item in items]


def serialize_e_zones(items):
    return [{
        "direction": item.direction,
        "family": item.family,
        "number": item.number,
        "parentType": item.parent_type,
        "parentSourceIndex": item.parent_source_index,
        "parentSourceTime": epoch(item.parent_source_time),
        "parentPrice": str(item.parent_price),
        "parentStopIndex": item.parent_stop_index,
        "parentStopTime": epoch(item.parent_stop_time),
        "parentStopEventTime": epoch(item.parent_stop_event_time),
        "orderDirection": item.order_direction,
        "orderReactionNumber": item.order_reaction_number,
        "orderMode": item.order_mode,
        "orderCauses": list(item.order_causes),
        "orderParentStopCauseTime": (
            epoch(item.order_parent_stop_cause_time)
            if item.order_parent_stop_cause_time is not None else None
        ),
        "orderFirstIndex": item.order_first_index,
        "orderFirstTime": epoch(item.order_first_time),
        "orderBreakIndex": item.order_break_index,
        "orderBreakTime": epoch(item.order_break_time),
        "orderConfirmationTime": epoch(item.order_confirmation_time),
        "orderBoxTop": str(item.order_box_top),
        "orderBoxTopSourceIndex": item.order_box_top_source_index,
        "orderBoxTopSourceTime": epoch(item.order_box_top_source_time),
        "orderBoxBottom": str(item.order_box_bottom),
        "orderBoxBottomSourceIndex": item.order_box_bottom_source_index,
        "orderBoxBottomSourceTime": epoch(item.order_box_bottom_source_time),
        "orderStopLevel": str(item.order_stop_level),
        "orderStopSourceIndex": item.order_stop_source_index,
        "orderStopSourceTime": epoch(item.order_stop_source_time),
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "decisionIndex": item.decision_index,
        "decisionTime": epoch(item.decision_time),
        "decisionEventTime": epoch(item.decision_event_time),
    } for item in items]


def serialize_stopalls(items):
    return [{
        "direction": item.direction,
        "number": item.number,
        "sourceIndex": item.source_index,
        "sourceTime": epoch(item.source_time),
        "price": str(item.price),
        "decisionIndex": item.decision_index,
        "decisionTime": epoch(item.decision_time),
        "decisionEventTime": epoch(item.decision_event_time),
        "gateType": item.gate_type,
        "gateEventTime": epoch(item.gate_event_time),
        "stoppedBehaviorType": item.stopped_behavior_type,
        "stoppedBehaviorKey": item.stopped_behavior_key,
        "stoppedBehaviorCount": item.stopped_behavior_count,
        "underlyingEFamily": item.underlying_e_family,
        "underlyingENumber": item.underlying_e_number,
        "orderDirection": item.order_direction,
        "orderReactionNumber": item.order_reaction_number,
        "orderMode": item.order_mode,
        "orderCauses": list(item.order_causes),
        "orderParentStopCauseTime": (
            epoch(item.order_parent_stop_cause_time)
            if item.order_parent_stop_cause_time is not None else None
        ),
        "orderFirstIndex": item.order_first_index,
        "orderFirstTime": (
            epoch(item.order_first_time) if item.order_first_time is not None else None
        ),
        "orderBreakIndex": item.order_break_index,
        "orderBreakTime": (
            epoch(item.order_break_time) if item.order_break_time is not None else None
        ),
        "orderConfirmationTime": (
            epoch(item.order_confirmation_time)
            if item.order_confirmation_time is not None else None
        ),
        "orderBoxTop": (
            str(item.order_box_top) if item.order_box_top is not None else None
        ),
        "orderBoxTopSourceIndex": item.order_box_top_source_index,
        "orderBoxTopSourceTime": (
            epoch(item.order_box_top_source_time)
            if item.order_box_top_source_time is not None else None
        ),
        "orderBoxBottom": (
            str(item.order_box_bottom) if item.order_box_bottom is not None else None
        ),
        "orderBoxBottomSourceIndex": item.order_box_bottom_source_index,
        "orderBoxBottomSourceTime": (
            epoch(item.order_box_bottom_source_time)
            if item.order_box_bottom_source_time is not None else None
        ),
        "orderStopLevel": (
            str(item.order_stop_level) if item.order_stop_level is not None else None
        ),
        "orderStopSourceIndex": item.order_stop_source_index,
        "orderStopSourceTime": (
            epoch(item.order_stop_source_time)
            if item.order_stop_source_time is not None else None
        ),
        "stopIndex": item.stop_index,
        "stopTime": epoch(item.stop_time) if item.stop_time else None,
        "stopEventTime": epoch(item.stop_event_time) if item.stop_event_time else None,
    } for item in items]


def bridge_datetime(value: object | None) -> str | None:
    """Format a native Tehran-local timestamp for the YAML-facing view."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if not isinstance(value, datetime):
        return None
    return _DTFMT.format(
        value.year, value.month, value.day,
        value.hour, value.minute, value.second,
    )


def bridge_direction(direction: str) -> str:
    return str(direction).title()


def bridge_mode(mode: object) -> str | None:
    return {"A": "Leg Start", "B": "Normal"}.get(str(mode))


def bridge_color(value: object | None) -> str | None:
    if value in (None, ""):
        return None
    return str(value).title()


def _bridge_horizon(market: MarketContext) -> datetime:
    return (
        getattr(market.candles[market.end_index], "timestamp")
        + market.chronology.timeframe
    )


def _bridge_in_horizon(market: MarketContext, value: datetime | None) -> bool:
    return value is not None and value < _bridge_horizon(market)


def _bridge_proven_strict_event(
    market: MarketContext,
    direction: str,
    level: object | None,
    event_time: datetime | None,
) -> datetime | None:
    """Validate a recorded event without selecting a new trading event.

    A source helper has already selected ``event_time``.  This presentation
    guard only verifies that the exact recorded lower-timeframe candle satisfies
    that helper's existing directional strict-cross condition.  It never scans
    for a substitute event, so a main-candle fallback remains ``null`` here.
    """
    if (
        event_time is None
        or level is None
        or not _bridge_in_horizon(market, event_time)
    ):
        return None
    normalized = as_decimal(level)
    second_times = getattr(market.chronology, "second_times", None)
    if second_times is None:
        second_times = [getattr(item, "timestamp") for item in market.seconds]
    position = bisect_left(second_times, event_time)
    while (
        position < len(market.seconds)
        and getattr(market.seconds[position], "timestamp") == event_time
    ):
        item = market.seconds[position]
        crossed = (
            as_decimal(getattr(item, "high")) > normalized
            if direction == "bearish"
            else as_decimal(getattr(item, "low")) < normalized
        )
        if crossed:
            return event_time
        position += 1
    return None


def _bridge_stop_view(
    market: MarketContext,
    direction: str,
    price: object | None,
    stop_time: datetime | None,
    stop_event_time: datetime | None,
) -> dict[str, object]:
    """Format a known behavior/order stop while respecting the view horizon."""
    if stop_time is None or not _bridge_in_horizon(market, stop_time):
        return {"time": None, "eventTime": None}
    return {
        "time": bridge_datetime(stop_time),
        "eventTime": bridge_datetime(
            _bridge_proven_strict_event(
                market, direction, price, stop_event_time
            )
        ),
    }


def _bridge_reaction_confirmation(
    market: MarketContext,
    direction: str,
    reaction: object,
    *,
    use_intrabar_start: bool = True,
) -> datetime | None:
    """Return only an already-recorded, lower-timeframe-proven confirmation."""
    try:
        event_time = market.chronology.reaction_confirmation(
            direction, reaction, use_intrabar_start=use_intrabar_start
        )
        level = getattr(
            reaction, "box_top" if direction == "bullish" else "box_bottom"
        )
    except (AttributeError, IndexError, TypeError, ValueError):
        return None
    # Reaction confirmation crosses the *opposite* side from the directional
    # Stop predicate validated by this helper. Keep the recorded event immutable.
    return _bridge_proven_strict_event(
        market, market.chronology.opposite_direction(direction), level, event_time
    )


def _bridge_order_identity(item: object) -> tuple[int, int] | None:
    first_index = getattr(item, "order_first_index", None)
    break_index = getattr(item, "order_break_index", None)
    if first_index is None or break_index is None:
        return None
    return order_identity(int(first_index), int(break_index))


class BridgeProjection:
    """Read-only formatter for the optional, finalized Bridge Output mapping.

    The constructor receives only final selection/audit facts.  It owns newly
    allocated dictionaries and indexes and does not mutate detector data,
    lifecycle state, or legacy serializer output.
    """

    def __init__(
        self,
        *,
        direction: str,
        market: MarketContext,
        prepared_order_audit: list[object],
        order_direction: str,
    ) -> None:
        self.direction = direction
        self.market = market
        self.order_direction = order_direction
        self.audit_by_identity: dict[tuple[int, int], object] = {
            order_identity(
                int(getattr(item["reaction"], "first_idx")),
                int(getattr(item["reaction"], "break_idx")),
            ): item
            for item in prepared_order_audit
        }

    def physical_order(self, prepared: object | None) -> dict[str, object] | None:
        """Project one final accepted physical Order by canonical identity."""
        if prepared is None:
            return None
        entry = prepared["entry"]
        reaction = prepared["reaction"]
        first_index = int(getattr(reaction, "first_idx"))
        break_index = int(getattr(reaction, "break_idx"))
        if not (
            0 <= first_index < len(self.market.candles)
            and 0 <= break_index < len(self.market.candles)
        ):
            return None
        crossed = prepared.get("crossed")
        stop_time = crossed[1] if crossed is not None else None
        stop_event_time = crossed[2] if crossed is not None else None
        confirmation = _bridge_reaction_confirmation(
            self.market,
            self.order_direction,
            reaction,
        )
        return {
            "firstCandle": {
                "time": bridge_datetime(
                    getattr(self.market.candles[first_index], "timestamp")
                ),
            },
            "breakoutCandle": {
                "time": bridge_datetime(
                    getattr(self.market.candles[break_index], "timestamp")
                ),
                "eventTime": bridge_datetime(confirmation),
            },
            "stop": {
                "price": str(entry["stop_level"]),
                **_bridge_stop_view(
                    self.market,
                    self.order_direction,
                    entry["stop_level"],
                    stop_time,
                    stop_event_time,
                ),
            },
        }

    def parent_order(self, behavior: object) -> dict[str, object] | None:
        """Return a behavior's recorded formation/decision Order, if final."""
        identity = _bridge_order_identity(behavior)
        return self.physical_order(
            self.audit_by_identity.get(identity) if identity is not None else None
        )

    def current_order(
        self,
        behavior: object,
        parent_type: str,
        parent_family: str | None,
        strict_stop_event: datetime | None,
    ) -> dict[str, object] | None:
        """Resolve a creator Order from an exact final stop-linked cause.

        This intentionally declines to infer ownership from a behavior's
        formation Order, timestamps, row order, unrelated provenance, or a
        provisional Order.  A conflict or a missing exact cause returns null.
        """
        if strict_stop_event is None:
            return None
        source_time = getattr(behavior, "source_time", None)
        if source_time is None:
            return None
        matching: dict[tuple[int, int], object] = {}
        for identity, prepared in self.audit_by_identity.items():
            for cause in prepared["causes"]:
                kind = cause.get("kind")
                if kind == "parent-stop":
                    if (
                        cause.get("parentType") != parent_type
                        or cause.get("parentSourceTime") != source_time
                        or cause.get("eventTime") != strict_stop_event
                    ):
                        continue
                    recorded_family = cause.get("parentFamily")
                    if parent_family is None:
                        if recorded_family not in (None, ""):
                            continue
                    elif recorded_family != parent_family:
                        continue
                elif kind == "reset-leg":
                    post_type = cause.get("postBehaviorType")
                    matches_type = (
                        post_type == parent_type
                        or post_type == "E" and parent_type.startswith("E")
                        or post_type == "StopAll" and parent_type.startswith("StopAll")
                    )
                    if (
                        not matches_type
                        or cause.get("postBehaviorSourceTime") != source_time
                        or cause.get("postBehaviorStopTime") != strict_stop_event
                    ):
                        continue
                else:
                    continue
                matching[identity] = prepared
        if len(matching) != 1:
            return None
        return self.physical_order(next(iter(matching.values())))

    def order_audit(self, prepared: object) -> dict[str, object]:
        """Project final accepted audit evidence using the physical formatter."""
        entry = prepared["entry"]
        reaction = prepared["reaction"]
        physical = self.physical_order(prepared)
        if physical is None:
            raise RuntimeError("Bridge Output received an invalid final Order Audit")
        causes = []
        for cause in prepared["causes"]:
            if cause["kind"] == "parent-stop":
                causes.append({
                    "kind": "parent-stop",
                    "parentType": cause["parentType"],
                    "parentFamily": bridge_color(cause["parentFamily"]),
                    "eventTime": bridge_datetime(cause["eventTime"]),
                    "parentSourceTime": bridge_datetime(cause["parentSourceTime"]),
                })
            elif cause["kind"] == "reset-leg":
                causes.append({
                    key: bridge_datetime(value) if isinstance(value, datetime) else value
                    for key, value in cause.items()
                })
        return {
            "type": "Order Audit",
            "direction": bridge_direction(self.order_direction),
            "mode": bridge_mode(getattr(reaction, "mode")),
            "firstCandle": {
                "index": int(getattr(reaction, "first_idx")),
                **physical["firstCandle"],
            },
            "structure": {
                "boxTop": {
                    "time": bridge_datetime(
                        getattr(reaction, "box_top_source_time", None)
                    ),
                    "price": str(getattr(reaction, "box_top", None)),
                },
                "boxBottom": {
                    "time": bridge_datetime(
                        getattr(reaction, "box_bottom_source_time", None)
                    ),
                    "price": str(getattr(reaction, "box_bottom", None)),
                },
                "breakoutCandle": {
                    "index": int(getattr(reaction, "break_idx")),
                    **physical["breakoutCandle"],
                },
            },
            "stop": {
                "level": str(entry["stop_level"]),
                "sourceTime": bridge_datetime(entry["stop_source_time"]),
                "stoppedAt": {
                    "time": physical["stop"]["time"],
                    "eventTime": physical["stop"]["eventTime"],
                },
            },
            "causes": causes,
        }


def _bridge_parent_stop(
    projection: BridgeProjection,
    detector: object | None,
    parent_type: str,
    item: object,
) -> tuple[datetime | None, datetime | None]:
    """Read an existing E-lifecycle stop; never perform a new stop search."""
    if detector is None:
        return None, None
    try:
        found = detector.parent_stop(parent_type, item)
    except (AttributeError, TypeError, ValueError):
        return None, None
    if found is None:
        return None, None
    index, event_time = found
    if not 0 <= int(index) < len(projection.market.candles):
        return None, None
    return getattr(projection.market.candles[int(index)], "timestamp"), event_time


def _bridge_a_stop(
    projection: BridgeProjection,
    s_detector: object | None,
    item: object,
) -> tuple[datetime | None, datetime | None]:
    """Read the already-authoritative S-stage first A stop."""
    if s_detector is None:
        return None, None
    try:
        found = s_detector.first_a_stop(
            as_decimal(getattr(item, "price")),
            s_detector._a_confirmation_time(item),
        )
    except (AttributeError, IndexError, TypeError, ValueError):
        return None, None
    if found is None:
        return None, None
    _index, main_time, event_time = found
    return main_time, event_time


def _bridge_behavior_stop(
    projection: BridgeProjection,
    direction: str,
    price: object,
    stop_time: datetime | None,
    stop_event_time: datetime | None,
) -> dict[str, object]:
    return {
        **_bridge_stop_view(
            projection.market, direction, price, stop_time, stop_event_time
        ),
        "price": str(price),
    }


def _bridge_blue_formation(
    projection: BridgeProjection,
    direction: str,
    line: object,
    reactions: list[object],
) -> tuple[datetime | None, datetime | None]:
    if str(getattr(line, "kind", "")).lower() != "scale":
        return getattr(line, "source_time", None), None
    reaction_number = int(getattr(line, "reaction_number"))
    if not 1 <= reaction_number <= len(reactions):
        return None, None
    reaction = reactions[reaction_number - 1]
    break_index = int(getattr(reaction, "break_idx"))
    if not 0 <= break_index < len(projection.market.candles):
        return None, None
    return (
        getattr(projection.market.candles[break_index], "timestamp"),
        _bridge_reaction_confirmation(
            projection.market, direction, reaction, use_intrabar_start=False
        ),
    )


def _bridge_project_reaction(
    projection: BridgeProjection,
    direction: str,
    raw: object,
    public: object,
) -> dict[str, object]:
    first_index = int(getattr(raw, "first_idx"))
    break_index = int(getattr(raw, "break_idx"))
    return {
        "type": "Reaction",
        "direction": bridge_direction(direction),
        "mode": bridge_mode(getattr(public, "mode")),
        "firstCandle": {
            "color": bridge_color(
                getattr(projection.market.candles[first_index], "tag")
            ),
            "time": bridge_datetime(
                getattr(projection.market.candles[first_index], "timestamp")
            ),
        },
        "structure": {
            "boxTop": {
                "time": bridge_datetime(getattr(public, "box_top_source_time")),
                "price": str(getattr(public, "box_top")),
            },
            "boxBottom": {
                "time": bridge_datetime(getattr(public, "box_bottom_source_time")),
                "price": str(getattr(public, "box_bottom")),
            },
            "breakoutCandle": {
                "time": bridge_datetime(
                    getattr(projection.market.candles[break_index], "timestamp")
                ),
                "eventTime": bridge_datetime(
                    _bridge_reaction_confirmation(
                        projection.market, direction, raw
                    )
                ),
            },
        },
    }


def _bridge_project_reset(
    projection: BridgeProjection,
    direction: str,
    reset: object,
) -> dict[str, object]:
    first_index = int(getattr(reset, "from_first_idx"))
    previous_time = (
        getattr(projection.market.candles[first_index], "timestamp")
        if 0 <= first_index < len(projection.market.candles)
        else None
    )
    return {
        "type": "Reset",
        "direction": bridge_direction(direction),
        "occurredAt": {
            "time": bridge_datetime(getattr(reset, "display_time", None)),
            "eventTime": bridge_datetime(getattr(reset, "second_time", None)),
        },
        "previousReaction": {"firstCandle": {"time": bridge_datetime(previous_time)}},
        "brokenLevel": str(getattr(reset, "broken_level")),
    }


def _bridge_project_blue(
    projection: BridgeProjection,
    direction: str,
    line: object,
    reactions: list[object],
) -> dict[str, object]:
    formation_time, formation_event_time = _bridge_blue_formation(
        projection, direction, line, reactions
    )
    kind = str(getattr(line, "kind", "")).lower()
    output: dict[str, object] = {
        "type": "Blue Line",
        "direction": bridge_direction(direction),
        "formation": {"scale": "Scale", "reset": "Reset"}.get(kind),
        "formedAt": {
            "time": bridge_datetime(formation_time),
            "eventTime": bridge_datetime(formation_event_time),
        },
        "line": {
            "price": str(getattr(line, "line_price")),
            "sourceExtreme": str(getattr(line, "source_extreme")),
        },
        # The final bridge does not retain standalone BlueState stop evidence.
        # Returning null is deliberate: creating a detector here would be a
        # second calculation instead of a read-only projection.
        "stop": {
            "time": None,
            "eventTime": None,
            "price": str(getattr(line, "source_extreme")),
        },
    }
    if kind == "reset":
        output["brokenLevel"] = str(getattr(line, "broken_level"))
    return output


def _bridge_full_lines_by_ordinal(lines: list[object]) -> dict[int, object]:
    ordered = sorted(
        lines,
        key=lambda item: (
            int(getattr(item, "reaction_number")),
            getattr(item, "source_time"),
            str(getattr(item, "kind")),
        ),
    )
    return {ordinal: line for ordinal, line in enumerate(ordered, start=1)}


def _bridge_project_a(
    projection: BridgeProjection,
    direction: str,
    item: object,
    lines_by_ordinal: dict[int, object],
    reactions: list[object],
    s_detector: object | None,
) -> dict[str, object]:
    first_line = lines_by_ordinal.get(int(getattr(item, "blue_1_ordinal")))
    second_line = lines_by_ordinal.get(int(getattr(item, "blue_2_ordinal")))
    first_formation, _first_formation_event = (
        _bridge_blue_formation(projection, direction, first_line, reactions)
        if first_line is not None
        else (None, None)
    )
    second_formation, _second_formation_event = (
        _bridge_blue_formation(projection, direction, second_line, reactions)
        if second_line is not None
        else (None, None)
    )
    stop_time, stop_event_time = _bridge_a_stop(projection, s_detector, item)
    strict_stop_event = _bridge_proven_strict_event(
        projection.market, direction, getattr(item, "price"), stop_event_time
    )
    reaction_number = int(getattr(item, "reaction_number"))
    reaction = (
        reactions[reaction_number - 1]
        if 1 <= reaction_number <= len(reactions)
        else None
    )
    route = getattr(item, "formation_route", None)
    return {
        "type": "A",
        "direction": bridge_direction(direction),
        "formation": {"ordinary": "Type-1", "double-stop": "Type-2"}.get(route),
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "blueLines": {
            "first": {
                "formedAt": {"time": bridge_datetime(first_formation)},
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    getattr(item, "blue_1_stop_level"),
                    getattr(item, "blue_1_stop_time"),
                    getattr(item, "blue_1_stop_event_time", None),
                ),
                "stopLevel": str(getattr(item, "blue_1_stop_level")),
            },
            "second": {
                "formedAt": {"time": bridge_datetime(second_formation)},
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    getattr(item, "blue_2_stop_level"),
                    getattr(item, "blue_2_stop_time"),
                    getattr(item, "blue_2_stop_event_time", None),
                ),
                "stopLevel": str(getattr(item, "blue_2_stop_level")),
            },
        },
        "reaction": {
            "startedAt": {
                "time": bridge_datetime(getattr(item, "reaction_first_time")),
            },
            "confirmedAt": {
                "time": bridge_datetime(getattr(item, "reaction_break_time")),
                "eventTime": bridge_datetime(
                    _bridge_reaction_confirmation(
                        projection.market,
                        direction,
                        reaction,
                        use_intrabar_start=False,
                    )
                    if reaction is not None else None
                ),
            },
        },
        "parent": None,
        "currentOrder": projection.current_order(
            item, "A", None, strict_stop_event
        ),
        "stop": _bridge_behavior_stop(
            projection, direction, getattr(item, "price"), stop_time, stop_event_time
        ),
    }


def _bridge_project_s(
    projection: BridgeProjection,
    direction: str,
    item: object,
    e_detector: object | None,
) -> dict[str, object]:
    stop_time, stop_event_time = _bridge_parent_stop(
        projection, e_detector, "S", item
    )
    strict_stop_event = _bridge_proven_strict_event(
        projection.market, direction, getattr(item, "price"), stop_event_time
    )
    color = str(getattr(item, "color", "")).lower()
    formation = None
    if color == "blue":
        formation = {
            "simple": "Type-1",
            "advanced": "Type-2",
            "type3": "Type-3",
            "type4": "Type-4",
        }.get(str(getattr(item, "formation_type", "")).lower())
    return {
        "type": "S",
        "direction": bridge_direction(direction),
        "color": bridge_color(getattr(item, "color")),
        "formation": formation,
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "parent": {
            "behavior": {
                "type": "A",
                "formedAt": {
                    "time": bridge_datetime(getattr(item, "a_source_time")),
                    "price": str(getattr(item, "a_price")),
                },
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    getattr(item, "a_price"),
                    getattr(item, "a_stop_time"),
                    getattr(item, "a_stop_event_time"),
                ),
            },
            "order": projection.parent_order(item),
        },
        "currentOrder": projection.current_order(
            item, "S", str(getattr(item, "color")), strict_stop_event
        ),
        "stop": _bridge_behavior_stop(
            projection, direction, getattr(item, "price"), stop_time, stop_event_time
        ),
    }


def _bridge_source_index(item: object) -> tuple[int, datetime] | None:
    source_index = getattr(item, "source_index", None)
    source_time = getattr(item, "source_time", None)
    if source_index is None or source_time is None:
        return None
    return int(source_index), source_time


def _bridge_parent_behavior_for_e(
    projection: BridgeProjection,
    direction: str,
    item: object,
    s_by_source: dict[tuple[int, datetime], object],
    e_by_source: dict[tuple[int, datetime], object],
    stopall_by_source: dict[tuple[int, datetime], object],
) -> dict[str, object]:
    parent_type = str(getattr(item, "parent_type"))
    parent_identity = (
        int(getattr(item, "parent_source_index")),
        getattr(item, "parent_source_time"),
    )
    parent = None
    color = None
    number = None
    if parent_type == "S":
        parent = s_by_source.get(parent_identity)
        color = bridge_color(getattr(parent, "color", None))
    elif parent_type == "E":
        parent = e_by_source.get(parent_identity)
        color = bridge_color(getattr(parent, "family", None))
        number = getattr(parent, "number", None)
    elif parent_type == "StopAll":
        parent = stopall_by_source.get(parent_identity)
        number = getattr(parent, "number", None)
    return {
        "type": parent_type,
        "color": color,
        "number": number,
        "formedAt": {
            "time": bridge_datetime(getattr(item, "parent_source_time")),
            "price": str(getattr(item, "parent_price")),
        },
        "stoppedAt": _bridge_stop_view(
            projection.market,
            direction,
            getattr(item, "parent_price"),
            getattr(item, "parent_stop_time"),
            getattr(item, "parent_stop_event_time"),
        ),
    }


def _bridge_project_e(
    projection: BridgeProjection,
    direction: str,
    item: object,
    e_detector: object | None,
    s_by_source: dict[tuple[int, datetime], object],
    e_by_source: dict[tuple[int, datetime], object],
    stopall_by_source: dict[tuple[int, datetime], object],
) -> dict[str, object]:
    stop_time, stop_event_time = _bridge_parent_stop(
        projection, e_detector, "E", item
    )
    strict_stop_event = _bridge_proven_strict_event(
        projection.market, direction, getattr(item, "price"), stop_event_time
    )
    return {
        "type": "E",
        "direction": bridge_direction(direction),
        "color": bridge_color(getattr(item, "family")),
        "number": int(getattr(item, "number")),
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "parent": {
            "behavior": _bridge_parent_behavior_for_e(
                projection,
                direction,
                item,
                s_by_source,
                e_by_source,
                stopall_by_source,
            ),
            "order": projection.parent_order(item),
        },
        "currentOrder": projection.current_order(
            item,
            f"E{int(getattr(item, 'number'))}",
            str(getattr(item, "family")),
            strict_stop_event,
        ),
        "stop": _bridge_behavior_stop(
            projection, direction, getattr(item, "price"), stop_time, stop_event_time
        ),
    }


def _bridge_project_stopall(
    projection: BridgeProjection,
    direction: str,
    item: object,
) -> dict[str, object]:
    donor_type = getattr(item, "donor_type", None)
    donor_price = getattr(item, "donor_price", None)
    donor_stop_time = getattr(item, "donor_stop_time", None)
    donor_stop_event_time = getattr(item, "donor_stop_event_time", None)
    own_stop_event = _bridge_proven_strict_event(
        projection.market,
        direction,
        getattr(item, "price"),
        getattr(item, "stop_event_time"),
    )
    formation = {
        "sequence-group-stop": "Type-1",
        "stopall-stop": "Type-2",
        "opposite-s-group-stop": "Type-3",
    }.get(getattr(item, "gate_type", None))
    return {
        "type": "StopAll",
        "direction": bridge_direction(direction),
        "number": int(getattr(item, "number")),
        "formation": formation,
        "formedAt": {
            "time": bridge_datetime(getattr(item, "source_time")),
            "price": str(getattr(item, "price")),
        },
        "parent": {
            "behavior": {
                "type": donor_type,
                "color": bridge_color(getattr(item, "donor_color", None)),
                "number": getattr(item, "donor_number", None),
                "formedAt": {
                    "time": bridge_datetime(
                        getattr(item, "donor_source_time", None)
                    ),
                    "price": str(donor_price) if donor_price is not None else None,
                },
                # Donor stop metadata remains independent from the group-level
                # gate. Type-3 S-Red promotion consequently keeps this null
                # unless an actual donor stop was retained.
                "stoppedAt": _bridge_stop_view(
                    projection.market,
                    direction,
                    donor_price,
                    donor_stop_time,
                    donor_stop_event_time,
                ),
            },
            "order": projection.parent_order(item),
        },
        "currentOrder": projection.current_order(
            item,
            f"StopAll{int(getattr(item, 'number'))}",
            None,
            own_stop_event,
        ),
        "stop": _bridge_behavior_stop(
            projection,
            direction,
            getattr(item, "price"),
            getattr(item, "stop_time"),
            getattr(item, "stop_event_time"),
        ),
    }


def _bridge_audit_order_key(
    prepared: object, detector: object,
) -> tuple[int, int]:
    reaction = prepared["reaction"]
    return (
        epoch(detector.candles[int(getattr(reaction, "first_idx"))].timestamp),
        epoch(detector.candles[int(getattr(reaction, "break_idx"))].timestamp),
    )


def build_bridge_output(
    direction: str,
    market: MarketContext,
    state: PipelineState,
    visibility: DirectionVisibilityState,
    selected_reactions: list[tuple[object, object]],
    selected_resets: list[object],
    selected_blue_lines: list[object],
    selected_a_zones: list[object],
    selected_s_zones: list[object],
    selected_e_zones: list[object],
    selected_stopalls: list[object],
    selected_order_audit: list[object],
) -> dict[str, list[dict[str, object]]]:
    """Build the opt-in YAML-facing mapping from final legacy selections.

    Callers pass the exact lists used by every legacy serializer. Array
    positions are therefore display alignment only; behavior and Order joins
    use source identities and final audit causes rather than list indexes.
    """
    e_detector = state.full_e_detectors.get(direction)
    s_detector = state.full_s_detectors.get(direction)
    order_direction = (
        str(getattr(e_detector, "order_direction"))
        if e_detector is not None
        else ("bearish" if direction == "bullish" else "bullish")
    )
    projection = BridgeProjection(
        direction=direction,
        market=market,
        prepared_order_audit=selected_order_audit,
        order_direction=order_direction,
    )
    full_lines = state.full_lines_by_direction.get(direction, visibility.blue_lines)
    lines_by_ordinal = _bridge_full_lines_by_ordinal(list(full_lines))
    full_s = getattr(visibility, "projection_s_zones", selected_s_zones)
    full_e = getattr(visibility, "projection_e_zones", selected_e_zones)
    full_stopalls = getattr(visibility, "projection_stopalls", selected_stopalls)
    s_by_source = {
        identity: item
        for item in full_s
        for identity in [_bridge_source_index(item)]
        if identity is not None
    }
    e_by_source = {
        identity: item
        for item in [*full_e, *selected_e_zones]
        for identity in [_bridge_source_index(item)]
        if identity is not None
    }
    stopall_by_source = {
        identity: item
        for item in [*full_stopalls, *selected_stopalls]
        for identity in [_bridge_source_index(item)]
        if identity is not None
    }
    raw_reactions = state.results[direction].reactions
    return {
        "reactions": [
            _bridge_project_reaction(projection, direction, raw, public)
            for raw, public in selected_reactions
        ],
        "resets": [
            _bridge_project_reset(projection, direction, item)
            for item in selected_resets
        ],
        "blueLines": [
            _bridge_project_blue(projection, direction, item, raw_reactions)
            for item in selected_blue_lines
        ],
        "aZones": [
            _bridge_project_a(
                projection,
                direction,
                item,
                lines_by_ordinal,
                raw_reactions,
                s_detector,
            )
            for item in selected_a_zones
        ],
        "sZones": [
            _bridge_project_s(projection, direction, item, e_detector)
            for item in selected_s_zones
        ],
        "eZones": [
            _bridge_project_e(
                projection,
                direction,
                item,
                e_detector,
                s_by_source,
                e_by_source,
                stopall_by_source,
            )
            for item in selected_e_zones
        ],
        "stopAlls": [
            _bridge_project_stopall(projection, direction, item)
            for item in selected_stopalls
        ],
        "orderAudit": [projection.order_audit(item) for item in selected_order_audit],
    }


def validate_order_audit_bridge(
    prepared_items, s_zones, e_zones, stopalls,
) -> None:
    """Assert that public behavior Order provenance matches canonical OrderAudit.

    This is a bridge consistency invariant only; it does not choose, rank, or
    reconstruct Orders.  All trading ownership decisions remain in the
    calculation engines.  Every public S/E/StopAll carrying a physical Order
    identity must reference an identity retained by the already-resolved audit.
    The resolved audit must also keep one owner per exact parent-stop cause.
    """
    audit_identities = {
        order_identity(
            int(getattr(item["reaction"], "first_idx")),
            int(getattr(item["reaction"], "break_idx")),
        )
        for item in prepared_items
    }

    missing: list[str] = []
    for behavior_type, items in (
        ("S", s_zones), ("E", e_zones), ("StopAll", stopalls)
    ):
        for item in items:
            first_index = getattr(item, "order_first_index", None)
            break_index = getattr(item, "order_break_index", None)
            if first_index is None or break_index is None:
                continue
            identity = order_identity(int(first_index), int(break_index))
            if identity in audit_identities:
                continue
            missing.append(
                f"{behavior_type}@{getattr(item, 'source_time', None)!s}"
                f"->{identity}"
            )
    if missing:
        raise RuntimeError(
            "OrderAudit bridge invariant failed; public behavior references "
            "an Order identity absent from canonical audit: " + ", ".join(missing)
        )

    parent_owner: dict[tuple[object, object, object, object], tuple[int, int]] = {}
    duplicate_parent_causes: list[str] = []
    for prepared in prepared_items:
        reaction = prepared["reaction"]
        identity = order_identity(
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
        )
        for cause in prepared["causes"]:
            if cause.get("kind") != "parent-stop":
                continue
            key = (
                cause.get("parentType"),
                cause.get("parentFamily"),
                cause.get("eventTime"),
                cause.get("parentSourceTime"),
            )
            previous = parent_owner.setdefault(key, identity)
            if previous != identity:
                duplicate_parent_causes.append(f"{key!r}:{previous}->{identity}")
    if duplicate_parent_causes:
        raise RuntimeError(
            "OrderAudit bridge invariant failed; one exact parent-stop owns "
            "multiple physical Orders: " + ", ".join(duplicate_parent_causes)
        )


def serialize_order_audit(prepared_items, detector):
    """Serialize already-resolved Order Audit identities without business filtering."""
    output = []
    for prepared in prepared_items:
        entry = prepared["entry"]
        reaction = prepared["reaction"]
        crossed = prepared["crossed"]
        first_index = int(getattr(reaction, "first_idx"))
        causes = []
        for cause in prepared["causes"]:
            if cause["kind"] == "parent-stop":
                causes.append({
                    "kind": "parent-stop",
                    "parentType": cause["parentType"],
                    "parentFamily": cause["parentFamily"],
                    "eventTime": epoch(cause["eventTime"]),
                    "parentSourceTime": epoch(cause["parentSourceTime"]),
                })
            elif cause["kind"] == "reset-leg":
                causes.append({
                    key: epoch(value) if isinstance(value, datetime) else value
                    for key, value in cause.items()
                })
        output.append({
            "direction": detector.order_direction,
            "reactionNumber": int(
                getattr(reaction, "behavior_public_number", None)
                or entry["reaction_number"]
            ),
            "reactionMode": str(getattr(reaction, "mode")),
            "firstIndex": first_index,
            "firstTime": epoch(detector.candles[first_index].timestamp),
            "boxTopSourceIndex": int(getattr(reaction, "box_top_source_idx")),
            "boxTopSourceTime": display_epoch(getattr(reaction, "box_top_source_time")),
            "boxTop": str(getattr(reaction, "box_top")),
            "boxBottomSourceIndex": int(getattr(reaction, "box_bottom_source_idx")),
            "boxBottomSourceTime": display_epoch(getattr(reaction, "box_bottom_source_time")),
            "boxBottom": str(getattr(reaction, "box_bottom")),
            "breakIndex": int(getattr(reaction, "break_idx")),
            "breakTime": epoch(
                detector.candles[int(getattr(reaction, "break_idx"))].timestamp
            ),
            "stopLevel": str(entry["stop_level"]),
            "stopSourceIndex": entry["stop_source_index"],
            "stopSourceTime": epoch(entry["stop_source_time"]),
            "stopHitIndex": crossed[0] if crossed is not None else None,
            "stopHitTime": epoch(crossed[1]) if crossed is not None else None,
            "stopHitEventTime": epoch(crossed[2]) if crossed is not None else None,
            "causes": causes,
        })
    return sorted(output, key=lambda item: (item["firstTime"], item["breakTime"]))


@dataclass(frozen=True, slots=True)
class EngineBundle:
    reaction: object
    blue_line: object
    a_zone: object
    s_zone: object
    e_zone: object | None
    lifecycle: object | None


@dataclass(frozen=True, slots=True)
class MarketContext:
    seconds: list[object]
    candles: list[object]
    lower_index: object
    chronology: object
    start_index: int
    end_index: int


def parse_arguments(argv=None):
    """Parse and validate the production pipeline command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reaction-engine",
        "--engine",
        dest="reaction_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--blue-line-engine",
        "--blue-engine",
        dest="blue_line_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--a-zone-engine",
        "--a-engine",
        dest="a_zone_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--s-zone-engine",
        "--s-engine",
        dest="s_zone_engine",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--e-zone-engine",
        "--e-engine",
        dest="e_zone_engine",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--lifecycle-engine",
        "--stopall-engine",
        dest="lifecycle_engine",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--blue-lines", choices=("enabled", "disabled"), default="enabled"
    )
    parser.add_argument(
        "--a-zones", choices=("enabled", "disabled"), default="enabled"
    )
    parser.add_argument(
        "--s-zones", choices=("enabled", "disabled"), default="enabled"
    )
    parser.add_argument(
        "--bridge-output",
        action="store_true",
        help="Add the presentation-only Bridge Output projection.",
    )
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--timeframe", type=int, required=True)
    parser.add_argument("--from-time", type=int, required=True)
    parser.add_argument("--to-time", type=int, required=True)
    parser.add_argument(
        "--direction", choices=("bullish", "bearish", "both"), required=True
    )
    args = parser.parse_args(argv)
    if args.timeframe < 1:
        raise ValueError("Timeframe must be at least one second.")
    return args


def load_engines(args, timings: dict[str, float]) -> EngineBundle:
    """Load every configured calculation engine exactly once."""
    reaction = timed(
        timings, "Load Reaction engine", lambda: load_engine(args.reaction_engine)
    )
    blue_line = timed(
        timings,
        "Load Blue Line engine",
        lambda: load_module("blue_line_detector", args.blue_line_engine),
    )
    a_zone = timed(
        timings, "Load A engine", lambda: load_module("a_zone_detector", args.a_zone_engine)
    )
    s_zone = timed(
        timings, "Load S engine", lambda: load_module("s_zone_detector", args.s_zone_engine)
    )
    e_zone = (
        timed(
            timings,
            "Load E engine",
            lambda: load_module("e_zone_detector", args.e_zone_engine),
        )
        if args.e_zone_engine is not None
        else None
    )
    lifecycle_path = args.lifecycle_engine or (_PIPELINE_DIR / "lifecycle_engine.py")
    lifecycle = timed(
        timings,
        "Load Lifecycle engine",
        lambda: load_module("lifecycle_engine", lifecycle_path),
    )
    return EngineBundle(reaction, blue_line, a_zone, s_zone, e_zone, lifecycle)


def prepare_market_context(
    args, engines: EngineBundle, timings: dict[str, float]
) -> MarketContext:
    """Read, isolate, normalize and index the selected raw-data range."""
    source_bytes = timed(
        timings, "Read source file", lambda: args.data.read_bytes()
    )
    # Match the former ``utf-8-sig`` behavior without decoding the entire raw
    # payload to a Python string before orjson parses it.
    source_bytes = source_bytes.removeprefix(b"\xef\xbb\xbf")
    source_rows = timed(
        timings, "Parse source JSON", lambda: orjson.loads(source_bytes)
    )
    # A requested time range is a presentation window only.  Reaction state
    # can remain open past ``to_time`` and be resolved by later RAW chronology;
    # truncating calculation at the visible end manufactures provisional
    # Reactions/Blue/A state that does not exist in a full-file run.  Calculate
    # on the complete physical RAW and apply from/to only during serialization.
    rows = timed(
        timings,
        "Use full RAW calculation context",
        lambda: source_rows,
    )
    if not rows:
        raise ValueError("The selected range contains no raw candles.")

    second_buckets, timeframe_buckets = timed(
        timings,
        "Normalize raw candles",
        lambda: build_candle_buckets(rows, args.timeframe),
    )
    seconds = timed(
        timings,
        "Build lower candle views",
        lambda: build_candle_objects(engines.reaction, second_buckets),
    )
    lower_index = engines.reaction.shared_lower_timeframe_index(seconds)
    candles = (
        seconds
        if args.timeframe == 1
        else timed(
            timings,
            "Build timeframe candle views",
            lambda: build_candle_objects(engines.reaction, timeframe_buckets),
        )
    )
    chronology = engines.reaction.MarketChronology(
        candles, seconds, args.timeframe, lower_index
    )

    # Resolve the visible main-candle range inside the prefix calculation.
    # Bucket boundaries are epoch-aligned exactly as ``build_candle_buckets``
    # constructs them, which also keeps full-run source indexes/ordinals
    # stable in a short-window request.
    main_bucket_times = [int(item["time"]) for item in timeframe_buckets]
    requested_start_bucket = (
        args.from_time
        if args.timeframe == 1
        else args.from_time // args.timeframe * args.timeframe
    )
    requested_end_bucket = (
        args.to_time
        if args.timeframe == 1
        else args.to_time // args.timeframe * args.timeframe
    )
    start_index = bisect_left(main_bucket_times, requested_start_bucket)
    end_index = bisect_left(main_bucket_times, requested_end_bucket + args.timeframe) - 1
    if start_index >= len(candles) or end_index < start_index:
        raise ValueError("The selected range contains no timeframe candles.")
    end_index = min(end_index, len(candles) - 1)

    return MarketContext(
        seconds=seconds,
        candles=candles,
        lower_index=lower_index,
        chronology=chronology,
        start_index=start_index,
        end_index=end_index,
    )

@dataclass(slots=True)
class PipelineState:
    """Mutable calculation state shared across direction serialization passes."""

    directions: tuple[str, ...]
    results: dict[str, object]
    reusable_full_context: bool
    initial_order_geometry: dict[str, object]
    internal_reaction_identities: dict[str, set[tuple[int, int]]]
    full_e_zones: dict[str, list[object]]
    full_e_detectors: dict[str, object]
    full_s_detectors: dict[str, object]
    full_lines_by_direction: dict[str, list[object]]
    full_a_by_direction: dict[str, list[object]]
    invalid_a_identities_by_direction: dict[str, set[tuple[datetime, int]]]
    invalid_s_identities_by_direction: dict[str, set[tuple[datetime, int]]]
    full_s_by_direction: dict[str, list[object]]
    full_s_candidates_by_direction: dict[str, list[object]]


@dataclass(slots=True)
class FullDirectionState:
    """Authoritative full-range behavior state for one trend direction."""

    e_zones: list[object]
    e_detector: object
    s_detector: object
    blue_lines: list[object]
    a_zones: list[object]
    invalid_a_identities: set[tuple[datetime, int]]
    invalid_s_identities: set[tuple[datetime, int]]
    s_zones: list[object]
    s_candidates: list[object]
    initial_s_zones: list[object]


def create_e_detector(
    direction: str,
    e_engine,
    full_results: dict[str, object],
    s_zones: list[object],
    chronology,
    geometry_detectors: dict[str, object],
    initial_order_audit,
    lifecycle_engine,
    *,
    blocked_order_first_times: set[datetime] | None = None,
    invalid_s_root_identities: set[tuple[datetime, int]] | None = None,
    order_b_legs: Sequence[object] = (),
):
    """Construct one E detector from shared geometry and physical Orders."""
    opposite = chronology.opposite_direction(direction)
    end_index = len(chronology.candles) - 1

    def direct_geometry(
        geometry_direction, geometry_start, geometry_end, gate_event
    ):
        return geometry_detectors[geometry_direction].first_order_reaction_after_gate(
            geometry_direction,
            geometry_start,
            geometry_end,
            gate_event,
        )

    return e_engine.EZoneDetector(
        direction,
        full_results[direction].reactions,
        full_results[opposite].reactions,
        s_zones,
        full_results[opposite].resets,
        chronology,
        0,
        end_index,
        direct_geometry,
        blocked_order_first_times=blocked_order_first_times,
        initial_order_audit=initial_order_audit,
        sequence_priority=lifecycle_engine.sequence_priority,
        invalid_s_root_identities=invalid_s_root_identities,
        order_b_legs=order_b_legs,
    )


def calculate_full_direction_state(
    direction: str,
    engines: EngineBundle,
    market: MarketContext,
    full_results: dict[str, object],
    geometry_detectors: dict[str, object],
    initial_order_geometry: dict[str, object],
    timings: dict[str, float],
    order_b_legs: Sequence[object] = (),
    shared_stages: FullDirectionState | None = None,
) -> FullDirectionState:
    """Run Blue→A→S→E calculation and lifecycle reconciliation for one direction."""
    blue_engine = engines.blue_line
    a_engine = engines.a_zone
    s_engine = engines.s_zone
    e_engine = engines.e_zone
    lifecycle_engine = engines.lifecycle
    assert e_engine is not None
    candles = market.candles
    chronology = market.chronology
    opposite = engines.reaction.opposite_direction(direction)

    if shared_stages is None:
        blue_lines = timed(
            timings,
            f"Blue Line • {direction.title()}",
            lambda: blue_engine.detect_blue_lines(
                direction,
                full_results[direction].reactions,
                chronology,
                full_results[direction].resets,
            ),
        )
        a_zones = timed(
            timings,
            f"A • {direction.title()}",
            lambda: a_engine.detect_a_zones(
                direction,
                full_results[direction].reactions,
                blue_lines,
                chronology,
            ),
        )
        s_detector = s_engine.SZoneDetector(
            direction,
            full_results[direction].reactions,
            full_results[opposite].reactions,
            blue_lines,
            a_zones,
            chronology,
            0,
            len(candles) - 1,
            full_results[opposite].resets,
            initial_order_geometry=initial_order_geometry[direction],
        )
        s_zones = timed(timings, f"S • {direction.title()}", s_detector.detect)
        initial_s_zones = list(s_zones)
    else:
        # Reaction, Blue, A and the initial S pass do not depend on Order_B.
        blue_lines = shared_stages.blue_lines
        a_zones = shared_stages.a_zones
        s_detector = shared_stages.s_detector
        s_zones = list(shared_stages.initial_s_zones)
        initial_s_zones = shared_stages.initial_s_zones
    s_candidates = list(s_zones)



    e_detector = create_e_detector(
        direction,
        e_engine,
        full_results,
        s_zones,
        chronology,
        geometry_detectors,
        s_detector.order_audit,
        lifecycle_engine,
        order_b_legs=order_b_legs,
    )
    e_zones = timed(
        timings, f"E • {direction.title()} • initial", e_detector.detect
    )
    valid_s_zones = lifecycle_engine.s_zones_for_module_engines(
        s_zones, e_zones, direction
    )
    if len(valid_s_zones) != len(s_zones):
        e_detector = create_e_detector(
            direction,
            e_engine,
            full_results,
            valid_s_zones,
            chronology,
            geometry_detectors,
            s_detector.order_audit,
            lifecycle_engine,
            blocked_order_first_times={
                getattr(item, "source_time")
                for item in s_zones
                if item not in valid_s_zones
            },
            order_b_legs=order_b_legs,
        )
        e_zones = timed(
            timings,
            f"E • {direction.title()} • S reconciliation",
            e_detector.detect,
        )
        s_zones = valid_s_zones

    candidate_a = lifecycle_engine.visible_a_zones(
        s_detector.eligible_a_zones, s_zones
    )
    candidate_a = lifecycle_engine.visible_a_zones_after_s_stops(
        candidate_a, s_zones, candles
    )
    stage_invalid_a_identities: set[tuple[datetime, int]] = set()
    # Cycle validation must see every S-eligible A, even when a provisional
    # S candidate temporarily hides that A from presentation.  Otherwise a
    # later S reconciliation can remove the provisional S and accidentally
    # resurrect an A that should have been rejected by the stopped S/E owner.
    lifecycle_a_candidates = list(s_detector.eligible_a_zones)
    _calculation_a, invalid_a = lifecycle_engine.split_a_zones_by_dominant_stops(
        lifecycle_a_candidates,
        s_candidates,
        e_zones,
        [],
        candles,
        direction,
        lambda item: e_detector.parent_stop(
            "S" if hasattr(item, "a_source_time") else "E", item
        ),
        trend_reactions=s_detector.trend_reactions,
        confirmation_finder=s_detector.reaction_confirmation_time,
        a_stop_event_finder=lambda item: s_detector.first_a_stop(
            Decimal(str(getattr(item, "price"))),
            s_detector.reaction_confirmation_time(
                s_detector.trend_reactions[int(getattr(item, "reaction_number")) - 1],
                direction,
            ),
        ),
        stage_invalid_a_identities=stage_invalid_a_identities,
    )
    invalid_a_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in invalid_a
    }
    invalid_a_source_times = {source_time for source_time, _ in invalid_a_identities}
    invalid_s = [
        item for item in s_candidates
        if getattr(item, "a_source_time") in invalid_a_source_times
    ]
    invalid_s_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in invalid_s
    }
    stage_invalid_a_source_times = {
        source_time for source_time, _ in stage_invalid_a_identities
    }
    stage_invalid_s_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in s_candidates
        if getattr(item, "a_source_time") in stage_invalid_a_source_times
    }
    # Only S descendants of an A rejected specifically by S-stage ownership
    # are removed from later-stage calculation.  Other suppressed S evidence
    # keeps its established continuation semantics unchanged.
    s_zones = [
        item for item in s_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in stage_invalid_s_identities
    ]

    accepted_a_sources = {
        getattr(item, "source_time")
        for item in s_detector.eligible_a_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in invalid_a_identities
    }
    pending_s_a_sources = {getattr(item, "a_source_time") for item in s_candidates}
    accepted_orders, blocked_order_first_times = lifecycle_engine.resolve_order_context(
        s_detector.order_audit,
        accepted_a_sources,
        set(getattr(e_detector, "blocked_order_first_times", set())),
        invalid_a,
        pending_s_a_sources,
        full_results[opposite].reactions,
        candles,
        direction,
        lambda item: s_detector.first_a_stop(
            Decimal(str(getattr(item, "price"))),
            getattr(item, "source_time"),
        ),
    )
    e_detector = create_e_detector(
        direction,
        e_engine,
        full_results,
        s_zones,
        chronology,
        geometry_detectors,
        accepted_orders,
        lifecycle_engine,
        blocked_order_first_times=blocked_order_first_times,
        invalid_s_root_identities=invalid_s_identities,
        order_b_legs=order_b_legs,
    )
    e_zones = timed(
        timings, f"E • {direction.title()} • final audit", e_detector.detect
    )

    # A still-open S candidate may be decided by the strict stop of a later
    # calculation-accepted physical Order in the same chronology.  Reconcile
    # against accepted ledgers only; arbitrary opposite Reactions are never
    # promoted into Orders by this pass.  Rebuild E once when S provenance or
    # decision chronology changes because E consumes S as authoritative input.
    shared_order_entries = [
        *accepted_orders.values(),
        *e_detector.order_audit.values(),
    ]
    reconciled_s_zones = s_detector.reconcile_shared_order_stops(
        s_zones, shared_order_entries
    )
    if reconciled_s_zones != s_zones:
        s_zones = reconciled_s_zones
        reconciled_by_identity = {
            (getattr(item, "a_source_time"), getattr(item, "source_time")): item
            for item in s_zones
        }
        s_candidates = [
            reconciled_by_identity.get(
                (getattr(item, "a_source_time"), getattr(item, "source_time")),
                item,
            )
            for item in s_candidates
        ]
        e_detector = create_e_detector(
            direction,
            e_engine,
            full_results,
            s_zones,
            chronology,
            geometry_detectors,
            accepted_orders,
            lifecycle_engine,
            blocked_order_first_times=blocked_order_first_times,
            invalid_s_root_identities=invalid_s_identities,
            order_b_legs=order_b_legs,
        )
        e_zones = timed(
            timings,
            f"E • {direction.title()} • shared Order-stop reconciliation",
            e_detector.detect,
        )
        
    calculation_s_candidates = [
        item for item in s_candidates
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in stage_invalid_s_identities
    ]
    consumed_s_evidence = lifecycle_engine.consumed_s_evidence_after_larger_stop(
        calculation_s_candidates,
        s_zones,
        e_zones,
        direction,
        lambda item: e_detector.parent_stop("E", item),
        candles,
    )
    for evidence_s, original_owner in consumed_s_evidence:
        owner = next(
            (
                item for item in e_zones
                if int(getattr(item, "source_index")) == int(getattr(original_owner, "source_index"))
                and getattr(item, "source_time") == getattr(original_owner, "source_time")
            ),
            None,
        )
        if owner is None:
            continue
        continuation = e_detector.continuation_chain_from_s(owner, evidence_s)
        e_zones = e_detector.replace_with_earlier_continuation(
            e_zones, owner, continuation
        )

    # Continuation replacement happens after the detector's normal final audit.
    # Rebuild the accepted ledger from the actual final E state so OrderAudit
    # cannot lag behind a branch that the lifecycle has just made authoritative.
    e_zones = e_detector.rebuild_accepted_order_audit(
        e_zones, supplemental_s_zones=[item for item, _ in consumed_s_evidence]
    )

    s_zones = [
        item for item in s_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in invalid_s_identities
    ]

    return FullDirectionState(
        e_zones=e_zones,
        e_detector=e_detector,
        s_detector=s_detector,
        blue_lines=blue_lines,
        a_zones=a_zones,
        invalid_a_identities=invalid_a_identities,
        invalid_s_identities=invalid_s_identities,
        s_zones=s_zones,
        s_candidates=s_candidates,
        initial_s_zones=initial_s_zones,
    )


def calculate_direction_with_order_b_feedback(
    direction: str,
    engines: EngineBundle,
    market: MarketContext,
    full_results: dict[str, object],
    geometry_detectors: dict[str, object],
    initial_order_geometry: dict[str, object],
    timings: dict[str, float],
) -> FullDirectionState:
    """Recalculate only while proven Order_B causes change accepted state."""
    opposite = engines.reaction.opposite_direction(direction)
    order_b_legs: list[object] = []
    seen: set[tuple[object, ...]] = set()
    shared_stages: FullDirectionState | None = None
    for _pass in range(8):
        state = calculate_full_direction_state(
            direction, engines, market, full_results, geometry_detectors,
            initial_order_geometry, timings, order_b_legs=order_b_legs,
            shared_stages=shared_stages,
        )
        if shared_stages is None:
            shared_stages = state
        e_zones, stopalls = engines.lifecycle.reconcile_stopall_lifecycle(
            state.e_detector, state.s_zones, state.e_zones,
            market.chronology, direction,
        )
        e_zones = state.e_detector.restore_independent_s_roots(e_zones)
        e_zones = state.e_detector.ensure_accepted_order_audit(e_zones)
        discovered = engines.e_zone.discover_accepted_order_b_reset_legs(
            direction,
            market.chronology,
            full_results[direction].reactions,
            full_results[direction].resets,
            full_results[opposite].reactions,
            state.s_detector.eligible_a_zones,
            state.invalid_a_identities,
            state.s_zones,
            e_zones,
            stopalls,
            state.s_detector,
            state.e_detector,
            engines.lifecycle.module_priority,
        )

        old_identity = order_b_leg_identity(order_b_legs)
        new_identity = order_b_leg_identity(discovered)
        if new_identity == old_identity:
            return state
        if new_identity in seen:
            raise RuntimeError("Order_B lifecycle feedback did not converge.")
        seen.add(new_identity)
        order_b_legs = discovered
    raise RuntimeError("Order_B lifecycle feedback exceeded eight passes.")


def prepare_pipeline_state(
    args,
    engines: EngineBundle,
    market: MarketContext,
    timings: dict[str, float],
) -> PipelineState:
    """Run shared calculation stages once and retain reusable detector state."""
    engine = engines.reaction
    e_engine = engines.e_zone
    seconds = market.seconds
    candles = market.candles
    chronology = market.chronology
    initial_order_geometry = {
        direction: engine.directional_a_stop_order_finder(
            candles, seconds, direction
        )
        for direction in ("bullish", "bearish")
    }
    directions = ("bullish", "bearish") if args.direction == "both" else (args.direction,)
    behavior_modules_enabled = (
        args.blue_lines == "enabled"
        or args.a_zones == "enabled"
        or args.s_zones == "enabled"
    )
    required_directions = (
        ("bullish", "bearish") if behavior_modules_enabled else directions
    )
    reusable_full_context = e_engine is not None and args.s_zones == "enabled"

    full_e_zones: dict[str, list[object]] = {}
    full_e_detectors: dict[str, object] = {}
    full_s_detectors: dict[str, object] = {}
    full_lines_by_direction: dict[str, list[object]] = {}
    full_a_by_direction: dict[str, list[object]] = {}
    invalid_a_identities_by_direction: dict[str, set[tuple[datetime, int]]] = {}
    invalid_s_identities_by_direction: dict[str, set[tuple[datetime, int]]] = {}
    full_s_by_direction: dict[str, list[object]] = {}
    full_s_candidates_by_direction: dict[str, list[object]] = {}

    if reusable_full_context:
        geometry_detectors = {
            direction: engine.UnifiedReactionDetector(
                candles, seconds, 0, len(candles) - 1, direction
            )
            for direction in ("bullish", "bearish")
        }
        results = {
            direction: timed(
                timings,
                f"Reaction geometry • {direction.title()}",
                detector.detect,
            )
            for direction, detector in geometry_detectors.items()
        }
        _, _, internal_reaction_identities, _ = timed(
            timings,
            "Internal Reaction ownership",
            lambda: engine.build_behavior_reaction_views(results, chronology),
        )
        for direction in directions:
            state = calculate_direction_with_order_b_feedback(
                direction,
                engines,
                market,
                results,
                geometry_detectors,
                initial_order_geometry,
                timings,
            )
            full_e_zones[direction] = state.e_zones
            full_e_detectors[direction] = state.e_detector
            full_s_detectors[direction] = state.s_detector
            full_lines_by_direction[direction] = state.blue_lines
            full_a_by_direction[direction] = state.a_zones
            invalid_a_identities_by_direction[direction] = state.invalid_a_identities
            invalid_s_identities_by_direction[direction] = state.invalid_s_identities
            full_s_by_direction[direction] = state.s_zones
            full_s_candidates_by_direction[direction] = state.s_candidates
    else:
        results = {
            direction: timed(
                timings,
                f"Reaction • {direction.title()}",
                lambda direction=direction: engine.UnifiedReactionDetector(
                    candles, seconds, 0, len(candles) - 1, direction
                ).detect(),
            )
            for direction in required_directions
        }
        if behavior_modules_enabled:
            _, _, internal_reaction_identities, _ = timed(
                timings,
                "Internal Reaction ownership",
                lambda: engine.build_behavior_reaction_views(results, chronology),
            )
        else:
            internal_reaction_identities = {"bullish": set(), "bearish": set()}

    return PipelineState(
        directions=tuple(directions),
        results=results,
        reusable_full_context=reusable_full_context,
        initial_order_geometry=initial_order_geometry,
        internal_reaction_identities=internal_reaction_identities,
        full_e_zones=full_e_zones,
        full_e_detectors=full_e_detectors,
        full_s_detectors=full_s_detectors,
        full_lines_by_direction=full_lines_by_direction,
        full_a_by_direction=full_a_by_direction,
        invalid_a_identities_by_direction=invalid_a_identities_by_direction,
        invalid_s_identities_by_direction=invalid_s_identities_by_direction,
        full_s_by_direction=full_s_by_direction,
        full_s_candidates_by_direction=full_s_candidates_by_direction,
    )


@dataclass(slots=True)
class DirectionRangeState:
    """Unserialized calculation state for one requested direction/range."""

    blue_lines: list[object]
    a_zones: list[object]
    s_candidates: list[object]
    accepted_s_zones: list[object]
    e_zones: list[object]
    invalid_a_identities: set[tuple[datetime, int]]
    invalid_s_identities: set[tuple[datetime, int]]


@dataclass(slots=True)
class DirectionVisibilityState:
    """Final public behavior state after lifecycle and internal-Reaction rules."""

    blue_lines: list[object]
    a_zones: list[object]
    s_zones: list[object]
    e_zones: list[object]
    stopalls: list[object]
    prepared_order_audit: list[object]
    # Final accepted source collections retained only for Bridge Output parent
    # joins. They are never serialized as public legacy rows or fed back into
    # lifecycle decisions.
    projection_s_zones: list[object]
    projection_e_zones: list[object]
    projection_stopalls: list[object]


def calculate_direction_range_state(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    timings: dict[str, float],
) -> DirectionRangeState:
    """Collect detector output for one requested direction before visibility rules."""
    result = state.results[direction]
    opposite = engines.reaction.opposite_direction(direction)
    start_index = market.start_index
    end_index = market.end_index

    requires_blue_lines = (
        args.blue_lines == "enabled"
        or args.a_zones == "enabled"
        or args.s_zones == "enabled"
    )
    if state.reusable_full_context and requires_blue_lines:
        blue_lines = [
            item
            for item in state.full_lines_by_direction[direction]
            if start_index <= int(getattr(item, "source_index")) <= end_index
        ]
    elif requires_blue_lines:
        blue_lines = timed(
            timings,
            f"Blue Line - {direction.title()}",
            lambda: engines.blue_line.detect_blue_lines(
                direction,
                result.reactions,
                market.chronology,
                result.resets,
            ),
        )
    else:
        blue_lines = []

    requires_a_zones = args.a_zones == "enabled" or args.s_zones == "enabled"
    if state.reusable_full_context and requires_a_zones:
        a_zones = [
            item
            for item in state.full_a_by_direction[direction]
            if start_index <= int(getattr(item, "source_index")) <= end_index
        ]
    elif requires_a_zones:
        a_zones = timed(
            timings,
            f"A - {direction.title()}",
            lambda: engines.a_zone.detect_a_zones(
                direction,
                result.reactions,
                blue_lines,
                market.chronology,
            ),
        )
    else:
        a_zones = []

    s_candidates: list[object] = []
    accepted_s_zones: list[object] = []
    if args.s_zones == "enabled":
        if state.reusable_full_context:
            s_candidates = state.full_s_candidates_by_direction[direction]
            accepted_s_zones = state.full_s_by_direction[direction]
            a_zones = state.full_s_detectors[direction].eligible_a_zones
        else:
            s_detector = engines.s_zone.SZoneDetector(
                direction,
                result.reactions,
                state.results[opposite].reactions,
                blue_lines,
                a_zones,
                market.chronology,
                0,
                len(market.candles) - 1,
                state.results[opposite].resets,
                initial_order_geometry=state.initial_order_geometry[direction],
            )
            s_candidates = timed(
                timings, f"S - {direction.title()}", s_detector.detect
            )
            state.full_s_detectors[direction] = s_detector
            accepted_s_zones = s_candidates
            a_zones = s_detector.eligible_a_zones

    return DirectionRangeState(
        blue_lines=blue_lines,
        a_zones=a_zones,
        s_candidates=s_candidates,
        accepted_s_zones=accepted_s_zones,
        e_zones=list(state.full_e_zones.get(direction, [])),
        invalid_a_identities=state.invalid_a_identities_by_direction.get(
            direction, set()
        ),
        invalid_s_identities=state.invalid_s_identities_by_direction.get(
            direction, set()
        ),
    )


def finalize_direction_visibility(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    direction_state: DirectionRangeState,
    timings: dict[str, float],
) -> DirectionVisibilityState:
    """Apply lifecycle, range and Internal-Reaction rules to detector output."""
    lifecycle_engine = engines.lifecycle
    opposite = engines.reaction.opposite_direction(direction)
    start_index = market.start_index
    end_index = market.end_index

    visible_a_zones = lifecycle_engine.visible_a_zones(
        direction_state.a_zones, direction_state.accepted_s_zones
    )
    visible_a_zones = lifecycle_engine.visible_a_zones_after_s_stops(
        visible_a_zones,
        direction_state.accepted_s_zones,
        market.candles,
    )

    e_zones = list(direction_state.e_zones)
    stopalls: list[object] = []
    stopall_enabled = (
        args.lifecycle_engine is not None
        and engines.e_zone is not None
        and args.s_zones == "enabled"
    )
    if stopall_enabled and direction in state.full_e_detectors:
        e_zones, stopalls = lifecycle_engine.reconcile_stopall_lifecycle(
            state.full_e_detectors[direction],
            direction_state.accepted_s_zones,
            e_zones,
            market.chronology,
            direction,
            lambda label, work: timed(timings, label, work),
        )

    if direction in state.full_e_detectors:
        # Dominant E ownership drives StopAll.  After those hard boundaries are
        # fixed, restore direct E1 roots of accepted S behaviors so independent
        # E formation remains visible without letting lower-priority roots
        # rewrite the dominant StopAll sequence.
        detector = state.full_e_detectors[direction]
        e_zones = detector.restore_independent_s_roots(e_zones)
        # Root restoration is a calculation-valid acceptance step that occurs
        # after the detector's normal ledger rebuild.  Sync only missing audit
        # identities while preserving Orders already needed by StopAll/history.
        e_zones = detector.ensure_accepted_order_audit(e_zones)
        visibility_stop = lambda item: detector.parent_stop(
            "S" if hasattr(item, "a_source_time") else "E", item
        )

        reset_legs = timed(
            timings,
            f"Order_B reset legs - {direction.title()}",
            lambda: engines.e_zone.discover_accepted_order_b_reset_legs(
                direction,
                market.chronology,
                state.results[direction].reactions,
                state.results[direction].resets,
                state.results[opposite].reactions,
                direction_state.a_zones,
                direction_state.invalid_a_identities,
                direction_state.accepted_s_zones,
                e_zones,
                stopalls,
                state.full_s_detectors[direction],
                detector,
                lifecycle_engine.module_priority,
            ),
        )
        if order_b_leg_identity(reset_legs) != order_b_leg_identity(detector.order_b_legs):
            raise RuntimeError(
                "Final Order_B lifecycle causes differ from converged E feedback."
            )
        detector.register_order_b_reset_legs(reset_legs)
    else:
        visibility_stop = lambda item: state.full_s_detectors[direction].first_a_stop(
            Decimal(str(item.price)), item.decision_event_time
        )

    # Capture accepted objects before presentation range/internal filtering.
    # The Bridge projector may resolve a nested historical parent from these
    # immutable references, but it never republishes them as independent rows.
    projection_s_zones = list(direction_state.accepted_s_zones)
    projection_e_zones = list(e_zones)
    projection_stopalls = list(stopalls)

    e_zones, visible_s_zones, visible_a_zones = timed(
        timings,
        f"Apply visibility filters - {direction.title()}",
        lambda: lifecycle_engine.finalize_behavior_visibility(
            visible_a_zones,
            direction_state.s_candidates,
            e_zones,
            stopalls,
            direction,
            direction_state.invalid_s_identities,
            visibility_stop,
            lambda item: state.full_s_detectors[direction].candidate_event_time(
                item.source_index, item.price, item.source_time
            ),
            market.candles,
            all_a_zones=direction_state.a_zones,
        ),
    )

    visible_s_zones = [
        item
        for item in visible_s_zones
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]
    visible_a_zones = [
        item
        for item in visible_a_zones
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]
    e_zones = [
        item
        for item in e_zones
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]
    stopalls = [
        item
        for item in stopalls
        if start_index <= int(getattr(item, "source_index")) <= end_index
    ]

    display_a_zones = [
        item
        for item in visible_a_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in direction_state.invalid_a_identities
    ]
    display_s_zones = [
        item
        for item in visible_s_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in direction_state.invalid_s_identities
    ]
    # OrderAudit provenance is calculated on the full RAW, not clipped by the
    # presentation range.  A public S/E/StopAll inside the requested window may
    # legitimately reference an accepted A-owned Order whose First/A source is
    # before ``start_index``.  Keep all calculation-accepted A sources here;
    # presentation filtering is handled separately by required Order identities.
    order_audit_a_sources = {
        getattr(item, "source_time")
        for item in state.full_a_by_direction.get(direction, direction_state.a_zones)
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in direction_state.invalid_a_identities
    }

    all_behavior_reactions = [
        reaction
        for result_item in state.results.values()
        for reaction in result_item.reactions
    ]
    engines.blue_line.mark_internal_blue_lines(
        direction_state.blue_lines,
        state.results[direction].reactions,
        all_behavior_reactions,
    )
    display_a_zones, display_s_zones, e_zones, stopalls = (
        lifecycle_engine.filter_internal_behavior_outputs(
            display_a_zones,
            display_s_zones,
            e_zones,
            stopalls,
            state.results[opposite].reactions,
            state.internal_reaction_identities.get(opposite, set()),
            all_behavior_reactions,
        )
    )

    required_order_identities = {
        order_identity(int(first_index), int(break_index))
        for item in [*display_s_zones, *e_zones, *stopalls]
        for first_index, break_index in [(
            getattr(item, "order_first_index", None),
            getattr(item, "order_break_index", None),
        )]
        if first_index is not None and break_index is not None
    }
    prepared_order_audit = (
        lifecycle_engine.prepare_order_audit(
            state.full_e_detectors[direction],
            start_index,
            end_index,
            state.full_s_detectors.get(direction),
            order_audit_a_sources,
            required_order_identities,
        )
        if direction in state.full_e_detectors
        else []
    )
    if direction in state.full_e_detectors:
        validate_order_audit_bridge(
            prepared_order_audit, display_s_zones, e_zones, stopalls
        )
    return DirectionVisibilityState(
        blue_lines=engines.blue_line.public_blue_lines(direction_state.blue_lines),
        a_zones=display_a_zones,
        s_zones=display_s_zones,
        e_zones=e_zones,
        stopalls=stopalls,
        prepared_order_audit=prepared_order_audit,
        projection_s_zones=projection_s_zones,
        projection_e_zones=projection_e_zones,
        projection_stopalls=projection_stopalls,
    )


def serialize_direction_payload(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    visibility: DirectionVisibilityState,
    timings: dict[str, float],
):
    """Serialize one direction without applying any trading rule."""
    result = state.results[direction]
    if not getattr(args, "bridge_output", False):
        # Preserve the direct legacy path byte-for-byte in structure and
        # ordering when the additive projection is not requested.
        reactions, resets = timed(
            timings,
            f"Serialize Reaction - {direction.title()}",
            lambda: serialize(
                result,
                market.start_index,
                market.end_index,
                reaction_transform=lambda item: engines.reaction.published_reaction_candidate(
                    direction, item, market.chronology
                ),
            ),
        )

        def build_legacy_payload():
            return {
                "reactions": reactions,
                "resets": resets,
                "blueLines": serialize_blue_lines(
                    visibility.blue_lines if args.blue_lines == "enabled" else [],
                    market.start_index,
                    market.end_index,
                ),
                "aZones": serialize_a_zones(
                    visibility.a_zones if args.a_zones == "enabled" else []
                ),
                "sZones": serialize_s_zones(visibility.s_zones),
                "eZones": serialize_e_zones(visibility.e_zones),
                "stopAlls": serialize_stopalls(visibility.stopalls),
                "orderAudit": (
                    serialize_order_audit(
                        visibility.prepared_order_audit,
                        state.full_e_detectors[direction],
                    )
                    if direction in state.full_e_detectors
                    else []
                ),
            }

        return timed(
            timings, f"Serialize output - {direction.title()}", build_legacy_payload
        )

    reaction_transform = lambda item: engines.reaction.published_reaction_candidate(
        direction, item, market.chronology
    )
    def serialize_reactions_from_one_selection():
        selected = select_reaction_serialization_items(
            result,
            market.start_index,
            market.end_index,
            reaction_transform,
        )
        reactions, resets = serialize(result, selected_items=selected)
        return reactions, resets, selected

    reactions, resets, selected_reaction_items = timed(
        timings,
        f"Serialize Reaction - {direction.title()}",
        serialize_reactions_from_one_selection,
    )
    selected_reactions, selected_resets = selected_reaction_items
    selected_blue_lines = [
        item
        for item in (
            visibility.blue_lines if args.blue_lines == "enabled" else []
        )
        if _index_selected(
            getattr(item, "source_index"), market.start_index, market.end_index
        )
    ]
    selected_a_zones = (
        visibility.a_zones if args.a_zones == "enabled" else []
    )
    selected_s_zones = visibility.s_zones
    selected_e_zones = visibility.e_zones
    selected_stopalls = visibility.stopalls
    audit_detector = state.full_e_detectors.get(direction)
    selected_order_audit = (
        sorted(
            visibility.prepared_order_audit,
            key=lambda item: _bridge_audit_order_key(item, audit_detector),
        )
        if audit_detector is not None
        else []
    )

    def build_payload():
        payload = {
            "reactions": reactions,
            "resets": resets,
            "blueLines": serialize_blue_lines(
                selected_blue_lines,
            ),
            "aZones": serialize_a_zones(selected_a_zones),
            "sZones": serialize_s_zones(selected_s_zones),
            "eZones": serialize_e_zones(selected_e_zones),
            "stopAlls": serialize_stopalls(selected_stopalls),
            "orderAudit": (
                serialize_order_audit(
                    selected_order_audit,
                    audit_detector,
                )
                if audit_detector is not None
                else []
            ),
        }
        payload["bridgeOutput"] = build_bridge_output(
            direction,
            market,
            state,
            visibility,
            selected_reactions,
            selected_resets,
            selected_blue_lines,
            selected_a_zones,
            selected_s_zones,
            selected_e_zones,
            selected_stopalls,
            selected_order_audit,
        )
        return payload

    return timed(
        timings, f"Serialize output - {direction.title()}", build_payload
    )


def build_direction_output(
    direction: str,
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    timings: dict[str, float],
):
    """Calculate, finalize and serialize one requested trend direction."""
    direction_state = calculate_direction_range_state(
        direction, args, engines, market, state, timings
    )
    visibility = finalize_direction_visibility(
        direction,
        args,
        engines,
        market,
        state,
        direction_state,
        timings,
    )
    return serialize_direction_payload(
        direction, args, engines, market, state, visibility, timings
    )

def build_response_payload(
    args,
    engines: EngineBundle,
    market: MarketContext,
    state: PipelineState,
    timings: dict[str, float],
    pipeline_started: float,
) -> dict[str, object]:
    """Build the public response envelope around serialized direction outputs."""
    e_enabled = engines.e_zone is not None and args.s_zones == "enabled"
    stop_all_enabled = (
        args.lifecycle_engine is not None
        and engines.e_zone is not None
        and args.s_zones == "enabled"
    )
    payload: dict[str, object] = {
        "engine": "reaction_engine.py",
        "version": engines.reaction.REACTION_ENGINE_VERSION,
        "pipelineVersion": TRADING_PIPELINE_VERSION,
        "blueLineVersion": engines.blue_line.BLUE_LINE_VERSION,
        "aVersion": engines.a_zone.A_ZONE_VERSION,
        "sVersion": engines.s_zone.S_ZONE_VERSION,
        "eVersion": engines.e_zone.E_ZONE_VERSION if engines.e_zone else None,
        "stopAllVersion": (
            engines.lifecycle.STOP_ALL_VERSION
            if args.lifecycle_engine is not None
            else None
        ),
        "blueLinesEnabled": args.blue_lines == "enabled",
        "aEnabled": args.a_zones == "enabled",
        "sEnabled": args.s_zones == "enabled",
        "eEnabled": e_enabled,
        "stopAllEnabled": stop_all_enabled,
        "timeframe": args.timeframe,
        "actualFrom": epoch(market.candles[market.start_index].timestamp),
        "actualTo": epoch(market.candles[market.end_index].timestamp),
        "directions": {},
    }
    direction_payloads = payload["directions"]
    assert isinstance(direction_payloads, dict)
    for direction in state.directions:
        direction_payloads[direction] = build_direction_output(
            direction, args, engines, market, state, timings
        )
    payload["timings"] = {
        "phasesMs": {
            label: round(duration, 2) for label, duration in timings.items()
        },
        "bridgeTotalMs": round((perf_counter() - pipeline_started) * 1000, 2),
    }
    return payload


def main() -> int:
    pipeline_started = perf_counter()
    timings: dict[str, float] = {}
    validation_started = perf_counter()
    emit_progress("started", "Validate request")
    args = parse_arguments()
    validation_ms = (perf_counter() - validation_started) * 1000
    timings["Validate request"] = validation_ms
    emit_progress("completed", "Validate request", validation_ms)

    engines = load_engines(args, timings)
    market = prepare_market_context(args, engines, timings)
    state = prepare_pipeline_state(args, engines, market, timings)
    payload = build_response_payload(
        args, engines, market, state, timings, pipeline_started
    )

    emit_progress(
        "completed",
        "Calculation pipeline",
        (perf_counter() - pipeline_started) * 1000,
    )
    encoding_started = perf_counter()
    encoded_payload = json.dumps(payload, separators=(",", ":"))
    emit_progress(
        "completed",
        "Encode response JSON",
        (perf_counter() - encoding_started) * 1000,
    )
    print(encoded_payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        raise SystemExit(1)
````
<!-- EXACT-SOURCE-END:bridge/trading_pipeline.py -->

### 16.4 `pipeline/__init__.py` — Package marker / unsupported wrapper

**SHA-256:** `ca549e4cf5d9a070227498d0d210279e0f7edae66d62dadab7981cddaa1db5c3`  
**Bytes:** `348`  
**LF count:** `19`

<!-- EXACT-SOURCE-BEGIN:pipeline/__init__.py -->
````python
"""Maintained Blue Line algorithm package."""

from .blue_line_detector import (
    BlueLine,
    ScaleStrike,
    count_scale_strikes,
    detect_blue_lines,
    fibonacci_level,
    run_blue_line,
)

__all__ = [
    "BlueLine",
    "ScaleStrike",
    "count_scale_strikes",
    "detect_blue_lines",
    "fibonacci_level",
    "run_blue_line",
]
````
<!-- EXACT-SOURCE-END:pipeline/__init__.py -->

### 16.5 `pipeline/a_zone_detector.py` — A

**SHA-256:** `d7c33dd619ad7e4590027667a2c4e984c83be7b82fbfafeb5d7f944ddd521097`  
**Bytes:** `31007`  
**LF count:** `797`

<!-- EXACT-SOURCE-BEGIN:pipeline/a_zone_detector.py -->
````python
"""A-zone calculation from authoritative Reaction and Blue state.

Owns Blue-pair/double-stop A formation, trigger chronology, continuation
geometry, and A source selection. Downstream S/larger-module ownership is
handled by the S and lifecycle engines rather than rewritten here.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Sequence

from core_utils import as_decimal
from direction_policy import policy_for


A_ZONE_VERSION = "1.6.4"
A_ZONE_LAST_MODIFIED_DATE = "2026-09-21"


@dataclass(frozen=True, slots=True)
class BlueState:
    ordinal: int
    line: object
    formation_index: int
    formation_time: datetime
    stop_index: int | None
    stop_time: datetime | None
    stop_event_time: datetime | None
    stop_level: Decimal
    stop_event_extreme: Decimal | None


@dataclass(frozen=True, slots=True)
class AZone:
    direction: str
    blue_1_ordinal: int
    blue_2_ordinal: int
    blue_1_source_time: datetime
    blue_2_source_time: datetime
    blue_1_stop_time: datetime
    blue_2_stop_time: datetime
    blue_1_stop_level: Decimal
    blue_2_stop_level: Decimal
    continuation_level: Decimal
    continuation_source_index: int
    continuation_source_time: datetime
    trigger_index: int
    trigger_time: datetime
    trigger_event_time: datetime
    reaction_number: int
    reaction_first_time: datetime
    reaction_break_time: datetime
    source_index: int
    source_time: datetime
    price: Decimal
    # Immutable, presentation-only provenance. These fields never participate
    # in A acceptance, ordering, visibility, or downstream calculations.
    formation_route: str | None = field(default=None, kw_only=True)
    blue_1_stop_event_time: datetime | None = field(default=None, kw_only=True)
    blue_2_stop_event_time: datetime | None = field(default=None, kw_only=True)


class AZoneDetector:
    def __init__(
        self,
        direction: str,
        reactions: Sequence[object],
        blue_lines: Sequence[object],
        chronology: object,
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.policy = policy_for(direction)
        self.reactions = list(reactions)
        self.blue_lines = sorted(
            blue_lines,
            key=lambda item: (
                int(getattr(item, "reaction_number")),
                getattr(item, "source_time"),
                str(getattr(item, "kind")),
            ),
        )
        self.chronology = chronology
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.timeframe = chronology.timeframe
        self.candle_times = chronology.times
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index

    @property
    def extreme_name(self) -> str:
        return self.policy.extreme_attr

    def _strict_cross(self, value: Decimal, level: Decimal) -> bool:
        return self.policy.strict_cross(value, level)

    def _better(self, value: Decimal, current: Decimal) -> bool:
        return self.policy.better_extreme(value, current)

    def _main_index(self, timestamp: datetime) -> int:
        return self.chronology.main_index(timestamp)

    def _lower_window(
        self, start: datetime, end: datetime | None
    ) -> Sequence[object]:
        return self.chronology.lower_window(start, end)

    def _first_crossing(
        self,
        level: Decimal,
        start: datetime,
        end: datetime | None,
    ) -> tuple[int, datetime, Decimal] | None:
        left = bisect_left(self.lower_times, start)
        right = len(self.lower) if end is None else bisect_left(self.lower_times, end)
        if right > left and self.lower_index is not None:
            position = (
                self.lower_index.first_less(left, right, level)
                if self.direction == "bullish"
                else self.lower_index.first_greater(left, right, level)
            )
            if position is None:
                return None
            item = self.lower[position]
            event_time = getattr(item, "timestamp")
            value = as_decimal(getattr(item, self.extreme_name))
            return self._main_index(event_time), event_time, value

        lower_items = self.lower[left:right]
        for item in lower_items:
            value = as_decimal(getattr(item, self.extreme_name))
            if self._strict_cross(value, level):
                event_time = getattr(item, "timestamp")
                return self._main_index(event_time), event_time, value
        if lower_items:
            return None

        start_index = max(0, bisect_left(self.candle_times, start))
        end_index = (
            len(self.candles)
            if end is None
            else max(start_index, bisect_left(self.candle_times, end))
        )
        for item in self.candles[start_index:end_index]:
            value = as_decimal(getattr(item, self.extreme_name))
            if self._strict_cross(value, level):
                return int(getattr(item, "index")), getattr(item, "timestamp"), value
        return None

    def _range_extreme(
        self, start: datetime, end: datetime
    ) -> tuple[Decimal, int, datetime]:
        if end < start:
            raise ValueError("Extreme range end precedes its start.")
        lower_items = self._lower_window(start, end + timedelta(microseconds=1))
        if lower_items:
            source = lower_items[0]
            value = as_decimal(getattr(source, self.extreme_name))
            for item in lower_items[1:]:
                candidate = as_decimal(getattr(item, self.extreme_name))
                if self._better(candidate, value):
                    source = item
                    value = candidate
            source_index = self._main_index(getattr(source, "timestamp"))
            return (
                value,
                source_index,
                getattr(self.candles[source_index], "timestamp"),
            )
        start_index = max(0, bisect_right(self.candle_times, start) - 1)
        end_index = min(
            len(self.candles) - 1,
            max(start_index, bisect_right(self.candle_times, end) - 1),
        )
        source = self.candles[start_index]
        value = as_decimal(getattr(source, self.extreme_name))
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = as_decimal(getattr(item, self.extreme_name))
            if self._better(candidate, value):
                source = item
                value = candidate
        return value, int(getattr(source, "index")), getattr(source, "timestamp")

    def _formation(self, line: object) -> tuple[int, datetime, datetime]:
        reaction_number = int(getattr(line, "reaction_number"))
        if reaction_number < 1 or reaction_number > len(self.reactions):
            raise ValueError("Blue Line refers to a missing reaction.")
        if str(getattr(line, "kind")) == "scale":
            reaction = self.reactions[reaction_number - 1]
            index = int(getattr(reaction, "break_idx"))
            event_time = self._reaction_confirmation_time(reaction)
            stop_scan_time = event_time
        else:
            index = int(getattr(line, "source_index"))
            source_time = getattr(self.candles[index], "timestamp")
            event_time = self._reset_formation_time(line, index)
            stop_scan_time = source_time + self.timeframe
        candle = self.candles[index]
        return index, event_time, stop_scan_time

    def _reset_formation_time(self, line: object, source_index: int) -> datetime:
        """Return the exact strict Reset event that makes a Reset Blue exist."""
        source = self.candles[source_index]
        start = getattr(source, "timestamp")
        end = start + self.timeframe
        broken_level = as_decimal(getattr(line, "broken_level"))
        for item in self._lower_window(start, end):
            value = as_decimal(getattr(item, self.extreme_name))
            if self._strict_cross(value, broken_level):
                return getattr(item, "timestamp")
        return start

    def _build_blue_states(self) -> list[BlueState]:
        states: list[BlueState] = []
        for ordinal, line in enumerate(self.blue_lines, start=1):
            if not bool(getattr(line, "calculation_valid", True)):
                continue
            formation_index, formation_time, stop_scan_time = self._formation(line)
            stop_level = as_decimal(getattr(line, "source_extreme"))
            stop = self._first_crossing(
                stop_level,
                stop_scan_time,
                None,
            )
            states.append(
                BlueState(
                    ordinal=ordinal,
                    line=line,
                    formation_index=formation_index,
                    formation_time=formation_time,
                    stop_index=stop[0] if stop else None,
                    stop_time=(
                        getattr(self.candles[stop[0]], "timestamp") if stop else None
                    ),
                    stop_event_time=stop[1] if stop else None,
                    stop_level=stop_level,
                    stop_event_extreme=stop[2] if stop else None,
                )
            )
        return states

    def _double_stop_a_candidates(self) -> list[AZone]:
        result: list[AZone] = []
        previous: tuple[int, object] | None = None
        for ordinal, line in enumerate(self.blue_lines, start=1):
            if bool(getattr(line, "calculation_valid", True)):
                previous = (ordinal, line)
                continue
            if previous is None:
                continue
            previous_ordinal, previous_line = previous
            formation_index = int(getattr(line, "source_index"))
            formation_time = getattr(line, "source_time")
            source_time = getattr(self.candles[formation_index], "timestamp")
            crossing = self._first_crossing(
                as_decimal(getattr(previous_line, "source_extreme")),
                formation_time,
                source_time + self.timeframe,
            )
            if crossing is None or crossing[0] != formation_index:
                continue
            trigger_index, trigger_event_time, _ = crossing
            match = self._first_reaction_after(
                trigger_event_time,
                not_before=formation_time,
            )
            if match is None:
                continue
            reaction_number, reaction = match
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            source = self._a_source(trigger_index, reaction)
            if source is None:
                continue
            source_index, a_source_time, price = source
            result.append(
                AZone(
                    direction=self.direction,
                    blue_1_ordinal=previous_ordinal,
                    blue_2_ordinal=ordinal,
                    blue_1_source_time=getattr(previous_line, "source_time"),
                    blue_2_source_time=getattr(line, "source_time"),
                    blue_1_stop_time=source_time,
                    blue_2_stop_time=source_time,
                    blue_1_stop_level=as_decimal(getattr(previous_line, "source_extreme")),
                    blue_2_stop_level=as_decimal(getattr(line, "source_extreme")),
                    continuation_level=as_decimal(getattr(previous_line, "source_extreme")),
                    continuation_source_index=int(getattr(previous_line, "source_index")),
                    continuation_source_time=getattr(previous_line, "source_time"),
                    trigger_index=trigger_index,
                    trigger_time=getattr(self.candles[trigger_index], "timestamp"),
                    trigger_event_time=trigger_event_time,
                    reaction_number=reaction_number,
                    reaction_first_time=getattr(self.candles[first_index], "timestamp"),
                    reaction_break_time=getattr(self.candles[break_index], "timestamp"),
                    source_index=source_index,
                    source_time=a_source_time,
                    price=price,
                    formation_route="double-stop",
                )
            )
            previous = None
        return result

    def _pair_trigger(
        self,
        previous: BlueState,
        current: BlueState,
        expires_at: datetime | None,
    ) -> tuple[
        Decimal,
        int,
        datetime,
        int,
        datetime,
        datetime,
        datetime,
        datetime,
    ] | None:
        if previous.stop_event_time is None or previous.stop_time is None:
            return None
        if (
            expires_at is not None
            and previous.stop_event_time > expires_at
        ):
            return None

        # A following Blue Line inherits the stop level established by the
        # previous line's first aligned Reaction.  The level is the
        # directional extreme from the previous Blue candle through that
        # Reaction breakout, not the following line's own source extreme.
        inherited = self._inherited_stop(previous, current)
        if inherited is not None:
            level, level_index, level_time, reaction_break_time = inherited
            crossing = self._first_crossing(
                level,
                current.formation_time,
                expires_at,
            )
            if crossing is None:
                return None
            trigger_index, trigger_event_time, _ = crossing
            return (
                level,
                level_index,
                level_time,
                trigger_index,
                getattr(self.candles[trigger_index], "timestamp"),
                trigger_event_time,
                level_time,
                getattr(self.candles[trigger_index], "timestamp"),
            )

        if previous.stop_event_time < current.formation_time:
            current_source_time = getattr(
                self.candles[current.formation_index], "timestamp"
            )
            level, level_index, level_time = self._range_extreme(
                previous.stop_event_time,
                current_source_time - timedelta(microseconds=1),
            )
            formation_candle_end = (
                getattr(self.candles[current.formation_index], "timestamp")
                + self.timeframe
            )
            formation_window_end = (
                min(formation_candle_end, expires_at)
                if expires_at is not None
                else formation_candle_end
            )
            formation_crossing = self._first_crossing(
                level,
                current.formation_time,
                formation_window_end,
            )
            if formation_crossing is not None:
                trigger_index, trigger_event_time, _ = formation_crossing
                effective_stop_time = getattr(
                    self.candles[trigger_index], "timestamp"
                )
                return (
                    level,
                    level_index,
                    level_time,
                    trigger_index,
                    effective_stop_time,
                    trigger_event_time,
                    previous.stop_time,
                    effective_stop_time,
                )

            if current.stop_event_time is None or current.stop_time is None:
                return None
            if (
                expires_at is not None
                and current.stop_event_time > expires_at
            ):
                return None
            search_start = current.stop_event_time
            crossing = self._first_crossing(level, search_start, expires_at)
            if crossing is None:
                return None
            trigger_index, trigger_event_time, _ = crossing
            return (
                level,
                level_index,
                level_time,
                trigger_index,
                getattr(self.candles[trigger_index], "timestamp"),
                trigger_event_time,
                previous.stop_time,
                current.stop_time,
            )

        if current.stop_event_time is None or current.stop_time is None:
            return None
        if (
            expires_at is not None
            and current.stop_event_time > expires_at
        ):
            return None
        first, second = sorted(
            (previous, current),
            key=lambda item: (
                item.stop_event_time,
                item.stop_level if self.direction == "bearish" else -item.stop_level,
            ),
        )
        assert first.stop_event_time is not None
        assert second.stop_event_time is not None
        assert first.stop_event_extreme is not None
        assert second.stop_event_extreme is not None
        first_index = int(first.stop_index)
        level = first.stop_event_extreme
        level_time = getattr(self.candles[first_index], "timestamp")

        if first.stop_event_time == second.stop_event_time:
            trigger_index = int(second.stop_index)
            return (
                level,
                first_index,
                level_time,
                trigger_index,
                getattr(self.candles[trigger_index], "timestamp"),
                second.stop_event_time,
                previous.stop_time,
                current.stop_time,
            )

        crossing = self._first_crossing(level, second.stop_event_time, expires_at)
        if crossing is None:
            return None
        trigger_index, trigger_event_time, _ = crossing
        return (
            level,
            first_index,
            level_time,
            trigger_index,
            getattr(self.candles[trigger_index], "timestamp"),
            trigger_event_time,
            previous.stop_time,
            current.stop_time,
        )

    def _reaction_confirmation_time(self, reaction: object) -> datetime:
        return self.chronology.reaction_confirmation(
            self.direction, reaction, use_intrabar_start=False
        )

    def _first_reaction_after(
        self,
        trigger_event_time: datetime,
        *,
        not_before: datetime | None = None,
    ) -> tuple[int, object] | None:
        for number, reaction in enumerate(self.reactions, start=1):
            first_time = getattr(
                self.candles[int(getattr(reaction, "first_idx"))],
                "timestamp",
            )
            if (
                self._reaction_confirmation_time(reaction) >= trigger_event_time
                and (not_before is None or first_time >= not_before)
            ):
                return number, reaction
        return None

    def _inherited_stop(
        self,
        previous: BlueState,
        current: BlueState,
    ) -> tuple[Decimal, int, datetime, datetime] | None:
        if previous.formation_time >= current.formation_time:
            return None
        chained = (
            previous.stop_time is not None
            and previous.stop_event_time is not None
            and previous.stop_event_time < current.formation_time
            and not bool(getattr(previous.line, "behavior_internal", False))
            and not bool(getattr(current.line, "behavior_internal", False))
        )
        # A Scale Blue may not inherit a continuation stop from a Reaction
        # that completes before the following Blue while the Scale Blue itself
        # is still live. Its semantic sourceExtreme remains authoritative until
        # the Scale Blue actually strict-stops. Reset-Blue chaining keeps its
        # established pre-stop structural route. This rule is direction-neutral.
        if not chained and str(getattr(previous.line, "kind")) == "scale":
            return None
        window_start = previous.stop_time if chained else previous.formation_time
        for reaction in self.reactions:
            first_time = getattr(
                self.candles[int(getattr(reaction, "first_idx"))],
                "timestamp",
            )
            break_time = getattr(
                self.candles[int(getattr(reaction, "break_idx"))],
                "timestamp",
            )
            if first_time <= window_start:
                continue
            if break_time >= current.formation_time:
                continue
            # Exact directional mirror: once a prior Blue has strictly
            # stopped, its carried stop uses the directional extreme across
            # the complete stop-candle -> next same-direction Reaction
            # Breakout-candle interval. Bullish freezes the minimum Low;
            # Bearish freezes the maximum High. The complete Breakout main
            # candle is included for both directions.
            range_end = (
                break_time + self.timeframe - timedelta(microseconds=1)
                if chained
                else break_time
            )
            level, level_index, level_time = self._range_extreme(
                window_start,
                range_end,
            )
            return level, level_index, level_time, break_time
        return None

    def _a_source(
        self,
        trigger_index: int,
        reaction: object,
    ) -> tuple[int, datetime, Decimal] | None:
        """Return A ownership frozen at the exact confirming Reaction event.

        The Blue-pair trigger opens the candidate on its main candle.  The
        confirming Reaction validates that candidate, but later prices in the
        same Break candle already belong to subsequent chronology and may not
        retroactively move A.  Source/price are therefore selected from the
        trigger main-candle open through exact lower-timeframe confirmation,
        inclusive.
        """
        start = getattr(self.candles[trigger_index], "timestamp")
        end = self._reaction_confirmation_time(reaction)
        if end < start:
            return None
        value, source_index, source_time = self._range_extreme(start, end)
        return source_index, source_time, value

    def _detect_ordinary_a(self, states: list[BlueState]) -> list[AZone]:
        """Resolve the ordinary adjacent-Blue A lifecycle."""
        output: list[AZone] = []
        cycle_after_index = -1
        bridge_reuse_ordinal: int | None = None
        index = 0

        while index + 1 < len(states):
            previous = states[index]
            current = states[index + 1]
            bridge_pair = (
                bridge_reuse_ordinal is not None
                and previous.ordinal == bridge_reuse_ordinal
            )
            if (
                current.formation_index <= cycle_after_index
                or (
                    previous.formation_index <= cycle_after_index
                    and not bridge_pair
                )
            ):
                if bridge_pair:
                    bridge_reuse_ordinal = None
                index += 1
                continue

            expires_at = (
                states[index + 2].formation_time
                if index + 2 < len(states)
                else None
            )
            trigger = self._pair_trigger(previous, current, expires_at)
            if trigger is None:
                index += 1
                continue

            (
                continuation_level,
                continuation_source_index,
                continuation_source_time,
                trigger_index,
                trigger_time,
                trigger_event_time,
                blue_1_stop_time,
                blue_2_stop_time,
            ) = trigger
            match = self._first_reaction_after(
                trigger_event_time,
                not_before=max(blue_1_stop_time, blue_2_stop_time),
            )
            if match is None:
                break
            reaction_number, reaction = match
            source = self._a_source(trigger_index, reaction)
            if source is None:
                index += 1
                continue
            source_index, source_time, price = source
            break_index = int(getattr(reaction, "break_idx"))
            output.append(
                AZone(
                    direction=self.direction,
                    blue_1_ordinal=previous.ordinal,
                    blue_2_ordinal=current.ordinal,
                    blue_1_source_time=getattr(previous.line, "source_time"),
                    blue_2_source_time=getattr(current.line, "source_time"),
                    blue_1_stop_time=blue_1_stop_time,
                    blue_2_stop_time=blue_2_stop_time,
                    blue_1_stop_level=previous.stop_level,
                    blue_2_stop_level=current.stop_level,
                    continuation_level=continuation_level,
                    continuation_source_index=continuation_source_index,
                    continuation_source_time=continuation_source_time,
                    trigger_index=trigger_index,
                    trigger_time=trigger_time,
                    trigger_event_time=trigger_event_time,
                    reaction_number=reaction_number,
                    reaction_first_time=getattr(
                        self.candles[int(getattr(reaction, "first_idx"))],
                        "timestamp",
                    ),
                    reaction_break_time=getattr(
                        self.candles[break_index], "timestamp"
                    ),
                    source_index=source_index,
                    source_time=source_time,
                    price=price,
                    formation_route="ordinary",
                    blue_1_stop_event_time=(
                        previous.stop_event_time
                        if previous.stop_time == blue_1_stop_time
                        else None
                    ),
                    blue_2_stop_event_time=(
                        current.stop_event_time
                        if current.stop_time == blue_2_stop_time
                        else None
                    ),
                )
            )
            cycle_after_index = break_index

            confirmation_time = self._reaction_confirmation_time(reaction)
            first_stop = self._first_crossing(price, confirmation_time, None)
            allow_adjacent_reuse = (
                first_stop is not None
                and index + 2 < len(states)
                and states[index + 2].formation_time >= first_stop[1]
            )
            if allow_adjacent_reuse:
                bridge_reuse_ordinal = current.ordinal
                index += 1
            else:
                bridge_reuse_ordinal = None
                while (
                    index < len(states)
                    and states[index].formation_index <= cycle_after_index
                ):
                    index += 1
        return output

    def _filter_special_a(
        self,
        special: list[AZone],
        ordinary: list[AZone],
    ) -> tuple[list[AZone], list[AZone]]:
        """Resolve special double-stop A ownership against ordinary A state."""
        ordinary_reactions = {
            item.reaction_number
            for item in ordinary
            if item.reaction_number is not None
        }
        special = [
            item
            for item in special
            if item.reaction_number not in ordinary_reactions
        ]

        filtered_special: list[AZone] = []
        for item in special:
            prior_candidates = [
                prior
                for prior in ordinary
                if prior.source_time < item.source_time
            ]
            prior = max(
                prior_candidates,
                key=lambda zone: zone.source_time,
                default=None,
            )
            if prior is not None and self._a_was_stopped_before(
                prior,
                item.reaction_first_time,
                not_before=item.blue_1_source_time,
            ):
                continue
            filtered_special.append(item)
        special = filtered_special

        consumed_special = [
            (
                {
                    int(getattr(item, "blue_1_ordinal")),
                    int(getattr(item, "blue_2_ordinal")),
                },
                getattr(item, "trigger_event_time"),
            )
            for item in special
        ]
        if consumed_special:
            ordinary = [
                item
                for item in ordinary
                if not any(
                    getattr(item, "trigger_event_time") > trigger_event_time
                    and {
                        int(getattr(item, "blue_1_ordinal")),
                        int(getattr(item, "blue_2_ordinal")),
                    }
                    & consumed_ordinals
                    for consumed_ordinals, trigger_event_time in consumed_special
                )
            ]
        return ordinary, special

    def detect(self) -> list[AZone]:
        """Return ordinary and special A zones after one ownership resolution."""
        states = self._build_blue_states()
        ordinary = self._detect_ordinary_a(states)
        ordinary, special = self._filter_special_a(
            self._double_stop_a_candidates(), ordinary
        )
        return sorted(
            ordinary + special,
            key=lambda item: (item.source_time, item.trigger_event_time),
        )

    def _a_was_stopped_before(
        self,
        zone: AZone,
        end_time: datetime,
        *,
        not_before: datetime | None = None,
    ) -> bool:
        """Return whether A's *first* strict stop belongs to this lifecycle.

        A stop that happened before ``not_before`` completed the prior cycle.
        A later recross of the same price must not be mistaken for a new stop
        owned by the current Blue pair.
        """
        start = int(getattr(self.candles[zone.source_index], "index")) + 1
        if start >= len(self.candles):
            return False
        first_stop = self._first_crossing(
            zone.price,
            getattr(self.candles[start], "timestamp"),
            end_time,
        )
        if first_stop is None:
            return False
        return not_before is None or first_stop[1] >= not_before


def detect_a_zones(
    direction: str,
    reactions: Sequence[object],
    blue_lines: Sequence[object],
    chronology: object,
) -> list[AZone]:
    return AZoneDetector(direction, reactions, blue_lines, chronology).detect()
````
<!-- EXACT-SOURCE-END:pipeline/a_zone_detector.py -->

### 16.6 `pipeline/blue_line_detector.py` — Blue

**SHA-256:** `6fa01d94bc98060b62bc7e68db0ec24a0b0159727d44043affee7130a9c11448`  
**Bytes:** `15802`  
**LF count:** `458`

<!-- EXACT-SOURCE-BEGIN:pipeline/blue_line_detector.py -->
````python
"""Blue Line calculation over authoritative Reaction output.

Owns Scale and Reset Blue detection, strike/spacing state, Blue stop validity,
and the distinction between calculation state and public Blue visibility. It
does not decide A/S/E lifecycle ownership.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from direction_policy import policy_for


BLUE_LINE_VERSION = "2.3.0"
FIBONACCI_RATIO = Decimal("0.618")


@dataclass(frozen=True, slots=True)
class ScaleStrike:
    source_index: int
    source_time: datetime
    extreme: Decimal


@dataclass(frozen=True, slots=True)
class BlueLine:
    direction: str
    kind: str
    reaction_number: int
    previous_strike_count: int | None
    strike_count: int | None
    fibonacci_level: Decimal | None
    source_index: int
    source_time: datetime
    source_extreme: Decimal
    broken_level: Decimal | None
    line_price: Decimal
    start_time: datetime
    end_time: datetime
    calculation_valid: bool = True
    behavior_internal: bool = False


def _is_color(candle: object, color: str) -> bool:
    return str(getattr(candle, "tag")).upper() == color


def _main_candle(candles_by_index: dict[int, object], index: int) -> object:
    try:
        return candles_by_index[index]
    except KeyError as exc:
        raise ValueError(f"Missing main candle index {index}.") from exc


def _stops_on_index(
    direction: str,
    line: object,
    candles: Sequence[object],
    start_index: int,
    end_index: int,
) -> bool:
    policy = policy_for(direction)
    level = Decimal(getattr(line, "source_extreme"))
    for candle in candles[max(0, start_index) : end_index + 1]:
        extreme = Decimal(getattr(candle, policy.extreme_attr))
        if policy.strict_cross(extreme, level):
            return int(getattr(candle, "index")) == end_index
    return False


def fibonacci_level(direction: str, reaction: object, reference: Decimal) -> Decimal:
    policy = policy_for(direction)  # validates direction centrally
    if policy.direction == "bullish":
        top = Decimal(getattr(reaction, "box_top"))
        return top - FIBONACCI_RATIO * (top - reference)
    bottom = Decimal(getattr(reaction, "box_bottom"))
    return bottom + FIBONACCI_RATIO * (reference - bottom)


def _intrabar_pending_confirmation(
    direction: str,
    chronology: object,
    reaction: object,
    comparison_extreme: Decimal,
    start_time: datetime,
    break_time: datetime,
    candles_by_index: dict[int, object],
) -> ScaleStrike | None:
    policy = policy_for(direction)
    end_time = break_time + chronology.timeframe
    left, right = chronology.lower_bounds(start_time, end_time)
    relevant = chronology.seconds[left:right]
    if not relevant:
        return None

    break_level = Decimal(
        getattr(reaction, "box_top" if direction == "bullish" else "box_bottom")
    )
    eligible: list[object] = []
    for second in relevant:
        extreme = Decimal(getattr(second, policy.extreme_attr))
        penetrates = (
            extreme < comparison_extreme
            if direction == "bullish"
            else extreme > comparison_extreme
        )
        if penetrates:
            eligible.append(second)
        breaks = (
            Decimal(getattr(second, "high")) > break_level
            if direction == "bullish"
            else Decimal(getattr(second, "low")) < break_level
        )
        if breaks and eligible:
            decisive = (
                min(eligible, key=lambda item: Decimal(getattr(item, "low")))
                if direction == "bullish"
                else max(eligible, key=lambda item: Decimal(getattr(item, "high")))
            )
            decisive_time = getattr(decisive, "timestamp")
            source_position = chronology.main_index(decisive_time)
            source = candles_by_index.get(source_position)
            if source is None:
                raise ValueError("Cannot map decisive one-second candle to a main candle.")
            return ScaleStrike(
                source_index=int(getattr(source, "index")),
                source_time=getattr(source, "timestamp"),
                extreme=Decimal(
                    getattr(decisive, policy.extreme_attr)
                ),
            )
    return None


def count_scale_strikes(
    direction: str,
    reaction: object,
    chronology: object,
    reference: Decimal,
    candles_by_index: dict[int, object] | None = None,
) -> tuple[Decimal, list[ScaleStrike]]:
    """Return the exact 0.618 level and confirmed strikes for one reaction."""
    level = fibonacci_level(direction, reaction, reference)
    if candles_by_index is None:
        candles_by_index = {
            int(getattr(candle, "index")): candle for candle in chronology.candles
        }
    first_index = int(getattr(reaction, "first_idx"))
    break_index = int(getattr(reaction, "break_idx"))
    reaction_candles = [
        _main_candle(candles_by_index, index)
        for index in range(first_index, break_index + 1)
    ]
    confirming_color = "GREEN" if direction == "bullish" else "RED"
    strikes: list[ScaleStrike] = []
    pending: ScaleStrike | None = None

    for candle in reaction_candles:
        last_extreme = strikes[-1].extreme if strikes else level
        candle_extreme = Decimal(
            getattr(candle, "low" if direction == "bullish" else "high")
        )
        is_new = (
            candle_extreme < last_extreme
            if direction == "bullish"
            else candle_extreme > last_extreme
        )
        if is_new and (
            pending is None
            or (
                candle_extreme < pending.extreme
                if direction == "bullish"
                else candle_extreme > pending.extreme
            )
        ):
            pending = ScaleStrike(
                source_index=int(getattr(candle, "index")),
                source_time=getattr(candle, "timestamp"),
                extreme=candle_extreme,
            )

        if pending is not None and _is_color(candle, confirming_color):
            strikes.append(pending)
            pending = None

    if pending is not None:
        break_candle = reaction_candles[-1]
        intrabar = _intrabar_pending_confirmation(
            direction=direction,
            chronology=chronology,
            reaction=reaction,
            comparison_extreme=strikes[-1].extreme if strikes else level,
            start_time=pending.source_time,
            break_time=getattr(break_candle, "timestamp"),
            candles_by_index=candles_by_index,
        )
        if intrabar is not None:
            strikes.append(intrabar)

    return level, strikes


def _build_scale_blue_line(
    direction: str,
    reaction_number: int,
    previous_count: int,
    level: Decimal,
    strikes: Sequence[ScaleStrike],
    candles_by_index: dict[int, object],
    chronology: object,
    behavior_internal: bool,
) -> BlueLine:
    """Build one scale Blue from its decisive confirmed strike."""
    decisive = strikes[-1]
    source = _main_candle(candles_by_index, decisive.source_index)
    high = Decimal(getattr(source, "high"))
    low = Decimal(getattr(source, "low"))
    line_price = (
        low + (high - low) / Decimal(3)
        if direction == "bullish"
        else high - (high - low) / Decimal(3)
    )
    return BlueLine(
        direction=direction,
        kind="scale",
        reaction_number=reaction_number,
        previous_strike_count=previous_count,
        strike_count=len(strikes),
        fibonacci_level=level,
        source_index=decisive.source_index,
        source_time=decisive.source_time,
        source_extreme=decisive.extreme,
        broken_level=None,
        line_price=line_price,
        start_time=decisive.source_time - chronology.timeframe,
        end_time=decisive.source_time + chronology.timeframe,
        behavior_internal=behavior_internal,
    )


def _build_reset_blue_line(
    direction: str,
    reaction_number: int,
    reset: object,
    previous_line: BlueLine | None,
    candles: Sequence[object],
    candles_by_index: dict[int, object],
    chronology: object,
    behavior_internal: bool,
) -> BlueLine:
    """Build one Reset Blue while preserving the established double-stop rule."""
    reset_index = int(getattr(reset, "index"))
    source = _main_candle(candles_by_index, reset_index)
    high = Decimal(getattr(source, "high"))
    low = Decimal(getattr(source, "low"))
    line_price = (
        low + (high - low) / Decimal(5)
        if direction == "bullish"
        else high - (high - low) / Decimal(5)
    )
    source_time = getattr(source, "timestamp")
    calculation_valid = not (
        previous_line is not None
        and _stops_on_index(
            direction,
            previous_line,
            candles,
            int(getattr(previous_line, "source_index")) + 1,
            reset_index,
        )
        and (
            low < Decimal(getattr(previous_line, "source_extreme"))
            if direction == "bullish"
            else high > Decimal(getattr(previous_line, "source_extreme"))
        )
    )
    return BlueLine(
        direction=direction,
        kind="reset",
        reaction_number=reaction_number,
        previous_strike_count=None,
        strike_count=None,
        fibonacci_level=None,
        source_index=reset_index,
        source_time=source_time,
        source_extreme=low if direction == "bullish" else high,
        broken_level=Decimal(getattr(reset, "broken_level")),
        line_price=line_price,
        start_time=source_time - chronology.timeframe,
        end_time=source_time + chronology.timeframe,
        calculation_valid=calculation_valid,
        behavior_internal=behavior_internal,
    )

def detect_blue_lines(
    direction: str,
    reactions: Sequence[object],
    chronology: object,
    resets: Sequence[object] = (),
) -> list[BlueLine]:
    """Detect scale and Reset Blue Lines over authoritative engine events."""
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    candles = chronology.candles
    candles_by_index = {
        int(getattr(candle, "index")): candle for candle in candles
    }
    resets_by_first: dict[int, list[object]] = {}
    for reset in resets:
        resets_by_first.setdefault(
            int(getattr(reset, "from_first_idx")), []
        ).append(reset)

    output: list[BlueLine] = []
    previous_reaction: object | None = None
    previous_count: int | None = None
    has_blue_line = False
    healthy_reactions_since_blue = 0

    for reaction_number, reaction in enumerate(reactions, start=1):
        behavior_internal = bool(getattr(reaction, "behavior_internal", False))
        if str(getattr(reaction, "mode")) == "A":
            boundary = getattr(reaction, "anchor_value", None)
            if boundary is None:
                boundary = getattr(reaction, "leg_boundary_value", None)
            if boundary is None:
                raise ValueError(
                    "Leg-Start reaction is missing its leg-head boundary."
                )
            reference = Decimal(boundary)
            previous_count = None
        else:
            if previous_reaction is None:
                raise ValueError(
                    "A Normal reaction cannot precede the Leg-Start reaction."
                )
            reference = Decimal(
                getattr(
                    previous_reaction,
                    "box_bottom" if direction == "bullish" else "box_top",
                )
            )

        level, strikes = count_scale_strikes(
            direction,
            reaction,
            chronology,
            reference,
            candles_by_index,
        )
        scale_candidate = (
            previous_count is not None and len(strikes) > previous_count
        )
        scale_emitted = False
        if scale_candidate and (
            not has_blue_line or healthy_reactions_since_blue >= 1
        ):
            output.append(
                _build_scale_blue_line(
                    direction,
                    reaction_number,
                    previous_count,
                    level,
                    strikes,
                    candles_by_index,
                    chronology,
                    behavior_internal,
                )
            )
            has_blue_line = True
            healthy_reactions_since_blue = 0
            scale_emitted = True

        if has_blue_line and not scale_emitted:
            healthy_reactions_since_blue += 1

        for reset in resets_by_first.get(
            int(getattr(reaction, "first_idx")), []
        ):
            if has_blue_line and healthy_reactions_since_blue < 1:
                continue
            output.append(
                _build_reset_blue_line(
                    direction,
                    reaction_number,
                    reset,
                    output[-1] if output else None,
                    candles,
                    candles_by_index,
                    chronology,
                    behavior_internal,
                )
            )
            has_blue_line = True
            healthy_reactions_since_blue = 0

        previous_reaction = reaction
        previous_count = len(strikes)

    return output


def public_blue_lines(lines: Sequence[BlueLine]) -> list[BlueLine]:
    """Return only calculation-valid, public Blue Lines for serialization."""
    return [
        line
        for line in lines
        if bool(getattr(line, "calculation_valid", True))
        and not bool(getattr(line, "behavior_internal", False))
    ]

def mark_internal_blue_lines(
    lines: Sequence[BlueLine],
    owner_reactions: Sequence[object],
    all_behavior_reactions: Sequence[object],
) -> None:
    """Mark Blue Lines that are private to protected Reaction interiors.

    A Blue is internal when its owning Reaction is behavior-internal, or when
    both its calculation-owned ``source_extreme`` and rendered ``line_price``
    fall strictly inside the same healthy Reaction interior.  The drawing
    offset alone never changes ownership.
    """

    def owner_is_internal(line: BlueLine) -> bool:
        number = int(getattr(line, "reaction_number", 0) or 0)
        if number < 1 or number > len(owner_reactions):
            return False
        return bool(getattr(owner_reactions[number - 1], "behavior_internal", False))

    def geometry_is_internal(line: BlueLine) -> bool:
        source_time = getattr(line, "source_time", None)
        line_price = getattr(line, "line_price", None)
        source_extreme = getattr(line, "source_extreme", None)
        if source_time is None or line_price is None or source_extreme is None:
            return False
        rendered = Decimal(str(line_price))
        semantic = Decimal(str(source_extreme))
        for reaction in all_behavior_reactions:
            first = getattr(reaction, "behavior_first_time", None)
            confirmed = getattr(reaction, "behavior_confirmation_time", None)
            if first is None or confirmed is None:
                continue
            if source_time <= first or source_time > confirmed:
                continue
            bottom = Decimal(str(getattr(reaction, "behavior_public_box_bottom")))
            top = Decimal(str(getattr(reaction, "behavior_public_box_top")))
            if bottom < semantic < top and bottom < rendered < top:
                return True
        return False

    for line in lines:
        if owner_is_internal(line) or geometry_is_internal(line):
            object.__setattr__(line, "behavior_internal", True)
````
<!-- EXACT-SOURCE-END:pipeline/blue_line_detector.py -->

### 16.7 `pipeline/core_utils.py` — Core Utilities

**SHA-256:** `3dae390ae77b72965f5799f7c132c4eba203775d5e72761fd7dd60c90f8578de`  
**Bytes:** `885`  
**LF count:** `29`

<!-- EXACT-SOURCE-BEGIN:pipeline/core_utils.py -->
````python
"""Small behavior-neutral primitives shared by calculation engines."""

from __future__ import annotations

CORE_UTILS_VERSION = "1.0.0"

from decimal import Decimal
from typing import TypeAlias


def as_decimal(value: object) -> Decimal:
    """Preserve Decimal values and normalize other numeric inputs losslessly."""
    return value if isinstance(value, Decimal) else Decimal(str(value))


OrderIdentity: TypeAlias = tuple[int, int]


def order_identity(first_index: object, break_index: object) -> OrderIdentity:
    """Return the canonical physical Order/Reaction geometry identity."""
    return int(first_index), int(break_index)


def reaction_identity(reaction: object) -> OrderIdentity:
    """Return ``(FirstIndex, BreakIndex)`` for a Reaction-like object."""
    return order_identity(
        getattr(reaction, "first_idx"),
        getattr(reaction, "break_idx"),
    )
````
<!-- EXACT-SOURCE-END:pipeline/core_utils.py -->

### 16.8 `pipeline/direction_policy.py` — Direction Policy

**SHA-256:** `a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea`  
**Bytes:** `2282`  
**LF count:** `70`

<!-- EXACT-SOURCE-BEGIN:pipeline/direction_policy.py -->
````python
"""Shared, behavior-neutral Bullish/Bearish direction primitives.

This module deliberately contains only price-direction semantics.  It does not
own chronology, lifecycle, numbering, visibility, or trading state.  Keeping
these primitives in one place prevents Bullish/Bearish drift while preserving
the existing algorithms in their owning engines.
"""

from __future__ import annotations

DIRECTION_POLICY_VERSION = "1.0.0"

from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

Direction = Literal["bullish", "bearish"]


@dataclass(frozen=True, slots=True)
class DirectionPolicy:
    direction: Direction
    extreme_attr: Literal["low", "high"]
    opposite_extreme_attr: Literal["high", "low"]
    first_reaction_tag: Literal["RED", "GREEN"]
    context_tag: Literal["GREEN", "RED"]

    @property
    def opposite_direction(self) -> Direction:
        return "bearish" if self.direction == "bullish" else "bullish"

    def strict_cross(self, value: Decimal, level: Decimal) -> bool:
        return value < level if self.direction == "bullish" else value > level

    def better_extreme(self, value: Decimal, current: Decimal) -> bool:
        return value < current if self.direction == "bullish" else value > current

    def choose_extreme(self, left: Decimal, right: Decimal) -> Decimal:
        return min(left, right) if self.direction == "bullish" else max(left, right)

    def confirmation_cross(self, value: Decimal, level: Decimal) -> bool:
        """Reaction confirmation mirror: high>top vs low<bottom.

        ``value`` is the already-selected confirmation-side price.
        """
        return value > level if self.direction == "bullish" else value < level


def policy_for(direction: str) -> DirectionPolicy:
    if direction == "bullish":
        return BULLISH
    if direction == "bearish":
        return BEARISH
    raise ValueError("Direction must be 'bullish' or 'bearish'.")


BULLISH = DirectionPolicy(
    direction="bullish",
    extreme_attr="low",
    opposite_extreme_attr="high",
    first_reaction_tag="RED",
    context_tag="GREEN",
)
BEARISH = DirectionPolicy(
    direction="bearish",
    extreme_attr="high",
    opposite_extreme_attr="low",
    first_reaction_tag="GREEN",
    context_tag="RED",
)
````
<!-- EXACT-SOURCE-END:pipeline/direction_policy.py -->

### 16.9 `pipeline/e_zone_detector.py` — E

**SHA-256:** `38834e96cc58931fe2e12096f4465ecaa046387d30fd40fecbd6891971020988`  
**Bytes:** `44859`  
**LF count:** `1033`

<!-- EXACT-SOURCE-BEGIN:pipeline/e_zone_detector.py -->
````python
"""Recursive E-zone formation and reconciliation from accepted Order state.

The Order module owns physical creation, stops, reuse, and provenance. This
detector owns E source/decision geometry, chains, family, and numbering.
Cross-stage visibility and StopAll grouping remain lifecycle-owned.
"""

from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass, replace
from datetime import datetime
from decimal import Decimal
from typing import Callable, Sequence

from core_utils import as_decimal, reaction_identity
from direction_policy import policy_for
from order_audit_engine import (
    OrderAuditEngineMixin, OrderBResetLeg, OrderMatch, PostBehaviorStop,
    discover_accepted_order_b_reset_legs, discover_order_b_reset_legs,
    dominant_post_behavior_stops, order_b_reset_event_time,
)


E_ZONE_VERSION = "6.16.1"
E_ZONE_IMPLEMENTATION_VERSION = "6.18.1"
E_ZONE_LAST_MODIFIED = "2026-09-28 19:35:32 +03:30"


@dataclass(frozen=True, slots=True)
class EZone:
    direction: str
    family: str
    number: int
    parent_type: str
    parent_source_index: int
    parent_source_time: datetime
    parent_price: Decimal
    parent_stop_index: int
    parent_stop_time: datetime
    parent_stop_event_time: datetime
    order_direction: str
    order_reaction_number: int
    order_mode: str
    order_causes: tuple[str, ...]
    order_parent_stop_cause_time: datetime | None
    order_first_index: int
    order_first_time: datetime
    order_break_index: int
    order_break_time: datetime
    order_confirmation_time: datetime
    order_box_top: Decimal
    order_box_top_source_index: int
    order_box_top_source_time: datetime
    order_box_bottom: Decimal
    order_box_bottom_source_index: int
    order_box_bottom_source_time: datetime
    order_stop_level: Decimal
    order_stop_source_index: int
    order_stop_source_time: datetime
    source_index: int
    source_time: datetime
    price: Decimal
    decision_index: int
    decision_time: datetime
    decision_event_time: datetime


class EZoneDetector(OrderAuditEngineMixin):
    def __init__(
        self,
        direction: str,
        trend_reactions: Sequence[object],
        opposite_reactions: Sequence[object],
        s_zones: Sequence[object],
        opposite_resets: Sequence[object],
        chronology: object,
        start_index: int = 0,
        end_index: int | None = None,
        direct_geometry_finder: Callable[
            [str, int, int, datetime], object | None
        ] | None = None,
        blocked_order_first_times: set[datetime] | None = None,
        initial_order_audit: dict[tuple[int, int], dict[str, object]] | None = None,
        sequence_resets: dict[datetime, int] | None = None,
        sequence_priority: Callable[[str, str], int] | None = None,
        invalid_s_root_identities: set[tuple[datetime, int]] | None = None,
        order_b_legs: Sequence[OrderBResetLeg] = (),
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.policy = policy_for(direction)
        if sequence_priority is None:
            raise ValueError("EZoneDetector requires the shared sequence-priority resolver.")
        self.sequence_priority = sequence_priority
        self.invalid_s_root_identities = set(invalid_s_root_identities or set())
        self.sequence_resets = sequence_resets or {}
        self.order_direction = chronology.opposite_direction(direction)
        self.chronology = chronology
        self.trend_reactions = list(trend_reactions)
        self.opposite_reactions = list(opposite_reactions)
        self.s_zones = sorted(
            s_zones,
            key=lambda item: (
                getattr(item, "source_time"),
                int(getattr(item, "source_index")),
            ),
        )
        self.opposite_resets = sorted(opposite_resets, key=self._reset_time)
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index
        self.timeframe = chronology.timeframe
        self.times = chronology.times
        self.start_index = int(start_index)
        self.end_index = len(self.candles) - 1 if end_index is None else int(end_index)
        self.range_start = self.times[self.start_index]
        self.range_end = self.times[self.end_index] + self.timeframe
        self.direct_geometry_finder = direct_geometry_finder
        self.blocked_order_first_times = blocked_order_first_times or set()
        self.initial_order_audit = initial_order_audit or {}
        self.order_b_legs = tuple(order_b_legs)
        self._cross_order_cache: dict[
            tuple[datetime, Decimal], tuple[int, datetime, datetime] | None
        ] = {}
        # Performance implementation detail: canonical opposite Reactions are
        # immutable for one run, and their canonical Order stop depends only
        # on that canonical reaction number/geometry plus immutable chronology.
        # Cache only exact canonical objects; bounded/noncanonical Order_A
        # geometry intentionally stays on the authoritative uncached path.
        self._canonical_order_stop_cache: dict[
            int, tuple[Decimal, int, datetime]
        ] = {}
        # Performance implementation detail: the initial A-owned OrderAudit
        # ledger is immutable for one detector run. Materialize its expensive
        # strict-stop lookup once, then keep both chronological indexes and
        # the original physical identity semantics.
        self._initial_order_records_cache: tuple[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ], ...] | None = None
        self._initial_order_first_times: list[datetime] | None = None
        self._initial_order_confirmation_times: list[datetime] | None = None
        self._initial_order_confirmation_records: tuple[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ], ...] = ()
        self._initial_orders_by_first_time: dict[datetime, tuple[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ], ...]] | None = None
        self._order_candidates_cache: dict[
            tuple[datetime, datetime | None, bool, bool], tuple[OrderMatch, ...]
        ] = {}
        self._carried_orders_cache: dict[
            tuple[datetime, datetime], tuple[OrderMatch, ...]
        ] = {}
        self.order_audit: dict[tuple[int, int], dict[str, object]] = {}
        # Performance implementation detail: ``order_audit`` remains the
        # authoritative accepted ledger and preserves insertion/provenance
        # semantics. This secondary chronology index exists only to avoid a
        # full ledger scan when a parent can use only Orders confirmed after
        # its strict stop.
        self._order_audit_confirmation_index: list[
            tuple[datetime, int, int]
        ] = []
        self._trend_first_times = [
            self._reaction_first_time(item) for item in self.trend_reactions
        ]
        self._trend_confirmations = [
            self._confirmation_for(item, self.direction)
            for item in self.trend_reactions
        ]
        self._opposite_first_times = [
            self._reaction_first_time(item) for item in self.opposite_reactions
        ]
        self._opposite_confirmations = [
            self._confirmation(item) for item in self.opposite_reactions
        ]
        self._trend_by_confirmation = sorted(
            zip(
                self._trend_confirmations,
                self._trend_first_times,
                self.trend_reactions,
            ),
            key=lambda item: item[0],
        )
        self._trend_confirmation_times = [item[0] for item in self._trend_by_confirmation]
        self._opposite_reset_times_by_first: dict[int, list[datetime]] = {}
        for reset in self.opposite_resets:
            self._opposite_reset_times_by_first.setdefault(
                int(getattr(reset, "from_first_idx")), []
            ).append(self._reset_time(reset))
        self._opposite_by_first_index = {
            int(getattr(item, "first_idx")): item
            for item in self.opposite_reactions
        }
        # Performance implementation detail: retain the first canonical
        # position for each physical identity. Legacy linear searches used
        # ``next(...)``, so first-win semantics are preserved intentionally.
        self._opposite_identity_position: dict[tuple[int, int], int] = {}
        for position, item in enumerate(self.opposite_reactions):
            self._opposite_identity_position.setdefault(
                reaction_identity(item), position
            )
        self.visual_lifecycle_starts: set[datetime] = set()
        self._consumed_s_evidence: list[tuple[object, tuple[int, datetime]]] = []
        self._last_candidate_zones: list[EZone] = []

    @property
    def sequence_resets(self) -> dict[datetime, int]:
        return self._sequence_resets

    @sequence_resets.setter
    def sequence_resets(self, resets: dict[datetime, int]) -> None:
        """Publish hard boundaries and refresh their dependent query state once."""
        self._sequence_resets = dict(resets)
        self._sequence_reset_times = sorted(self._sequence_resets)
        for cache_name in ("_order_candidates_cache", "_carried_orders_cache"):
            cache = getattr(self, cache_name, None)
            if cache is not None:
                cache.clear()

    def _reset_time(self, reset: object) -> datetime:
        return self.chronology.reset_time(reset)

    def _main_index(self, value: datetime) -> int:
        return self.chronology.main_index(value, clamp=True)


    def _first_cross_position(
        self, left: int, right: int, level: Decimal, *, less: bool
    ) -> int | None:
        """Return the first strict lower-timeframe crossing in [left, right)."""
        if self.lower_index is not None:
            return (
                self.lower_index.first_less(left, right, level)
                if less
                else self.lower_index.first_greater(left, right, level)
            )
        field = "low" if less else "high"
        for position in range(left, right):
            value = as_decimal(getattr(self.lower[position], field))
            if value < level if less else value > level:
                return position
        return None

    def _stop_value(self, item: object) -> Decimal:
        return as_decimal(getattr(item, self.policy.extreme_attr))


    def _first_parent_stop(
        self, source_time: datetime, level: Decimal
    ) -> tuple[int, datetime] | None:
        left = bisect_left(self.lower_times, max(source_time, self.range_start))
        right = bisect_left(self.lower_times, self.range_end)
        position = self._first_cross_position(
            left, right, level, less=self.direction == "bullish"
        )
        if position is None:
            return None
        event = self.lower_times[position]
        return self._main_index(event), event

    def _confirmation_for(self, reaction: object, direction: str) -> datetime:
        return self.chronology.reaction_confirmation(direction, reaction)

    def _confirmation(self, reaction: object) -> datetime:
        return self._confirmation_for(reaction, self.order_direction)

    def _reaction_first_time(self, reaction: object) -> datetime:
        return getattr(self.candles[int(getattr(reaction, "first_idx"))], "timestamp")


    def _parent_stop(self, parent_type: str, parent: object) -> tuple[int, datetime] | None:
        if parent_type == "S":
            start = getattr(parent, "decision_event_time")
        else:
            # An E can only stop after the order-stop event that confirms it.
            start = getattr(parent, "decision_event_time")
        return self._first_parent_stop(start, as_decimal(getattr(parent, "price")))

    def parent_stop(
        self, parent_type: str, parent: object
    ) -> tuple[int, datetime] | None:
        """Public lifecycle API for the first strict parent stop."""
        return self._parent_stop(parent_type, parent)


    def _extreme_between(self, start: datetime, end: datetime) -> tuple[int, datetime, Decimal]:
        # E source ownership is candle-based: include the complete main candle
        # containing the parent stop and the complete main candle containing
        # the order stop. Lower-timeframe chronology decides whether each stop
        # happened, but it must not truncate either boundary candle's OHLC.
        start_index = max(self.start_index, self._main_index(start))
        end_index = min(self.end_index, self._main_index(end))
        source = self.candles[start_index]
        value = self._stop_value(source)
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = self._stop_value(item)
            better = candidate < value if self.direction == "bullish" else candidate > value
            if better:
                source, value = item, candidate
        return int(getattr(source, "index")), getattr(source, "timestamp"), value

    def _zone(
        self, family: str, number: int, parent_type: str,
        parent: object, stop_event: datetime,
    ) -> EZone | None:
        # Every E-space cycle starts at the strict parent stop. Parent-stop
        # and reset-leg are creation causes; carried/accepted are use routes.
        inherited = (
            self._unconsumed_s_orders(parent, stop_event)
            if parent_type == "S"
            else []
        )
        gate_owned = self._gate_owned_initial_order(stop_event)
        carried = self._carried_orders_for_parent(parent, stop_event)
        self._register_order_audit(parent_type, parent, stop_event)
        post_stop_accepted = self._post_stop_accepted_orders_for_parent(
            parent, stop_event
        )
        inherited_one = inherited[0] if inherited else None
        carried_one = carried[0] if carried else None
        post_stop_accepted_one = (
            post_stop_accepted[0] if post_stop_accepted else None
        )
        direct = self._first_order(
            stop_event,
            (
                inherited_one[6][2]
                if parent_type == "S" and carried_one is None
                and inherited_one is not None and inherited_one[6] is not None
                else self.range_end
                if parent_type == "S" and carried_one is None
                else None
            ),
            allow_bounded_continue=(parent_type == "S"),
            allow_trend_leg_continue=(parent_type == "E"),
        )
        choices = [
            item for item in (
                direct, inherited_one, carried_one, post_stop_accepted_one
            )
            if item is not None and item[6] is not None
        ]
        order_match = min(
            choices,
            key=lambda item: (item[6][2], -int(getattr(item[1], "first_idx"))),
            default=None,
        )
        if order_match is None:
            return None
        (
            order_number, order, order_confirmation, order_stop,
            stop_source, stop_source_time, crossed, order_causes,
            order_parent_stop_cause_time,
        ) = order_match
        if crossed is None:
            return None
        order_decision_index, order_decision_time, order_decision_event = crossed
        decision_event = max(stop_event, order_decision_event)
        decision_index = self._main_index(decision_event)
        decision_time = getattr(self.candles[decision_index], "timestamp")
        source_index, source_time, price = self._extreme_between(stop_event, decision_event)
        parent_stop_index = self._main_index(stop_event)
        order_first_index = int(getattr(order, "first_idx"))
        top_source = int(getattr(order, "box_top_source_idx"))
        bottom_source = int(getattr(order, "box_bottom_source_idx"))
        return EZone(
            direction=self.direction,
            family=family,
            number=number,
            parent_type=parent_type,
            parent_source_index=int(getattr(parent, "source_index")),
            parent_source_time=getattr(parent, "source_time"),
            parent_price=as_decimal(getattr(parent, "price")),
            parent_stop_index=parent_stop_index,
            parent_stop_time=getattr(self.candles[parent_stop_index], "timestamp"),
            parent_stop_event_time=stop_event,
            order_direction=self.order_direction,
            order_reaction_number=order_number,
            order_mode=str(getattr(order, "mode")),
            order_causes=order_causes,
            order_parent_stop_cause_time=order_parent_stop_cause_time,
            order_first_index=order_first_index,
            order_first_time=getattr(self.candles[order_first_index], "timestamp"),
            order_break_index=int(getattr(order, "break_idx")),
            order_break_time=getattr(self.candles[int(getattr(order, "break_idx"))], "timestamp"),
            order_confirmation_time=order_confirmation,
            order_box_top=as_decimal(getattr(order, "box_top")),
            order_box_top_source_index=top_source,
            order_box_top_source_time=getattr(self.candles[top_source], "timestamp"),
            order_box_bottom=as_decimal(getattr(order, "box_bottom")),
            order_box_bottom_source_index=bottom_source,
            order_box_bottom_source_time=getattr(self.candles[bottom_source], "timestamp"),
            order_stop_level=order_stop,
            order_stop_source_index=stop_source,
            order_stop_source_time=stop_source_time,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event,
        )

    def set_consumed_s_evidence(
        self, evidence: Sequence[tuple[object, object]],
    ) -> None:
        """Register non-public S evidence that continues a stopped larger E."""
        self._consumed_s_evidence = [
            (
                s_zone,
                (int(getattr(owner, "source_index")), getattr(owner, "source_time")),
            )
            for s_zone, owner in evidence
        ]

    def _apply_consumed_s_evidence(self, zones: Sequence[EZone]) -> list[EZone]:
        result = list(zones)
        for s_zone, owner_id in self._consumed_s_evidence:
            owner = next(
                (
                    item for item in result
                    if (item.source_index, item.source_time) == owner_id
                ),
                None,
            )
            if owner is None:
                continue
            continuation = self.continuation_chain_from_s(owner, s_zone)
            result = self.replace_with_earlier_continuation(
                result, owner, continuation
            )
        return result

    def continuation_chain_from_s(
        self, owner: EZone, s_zone: object,
    ) -> list[EZone]:
        """Build the E continuation opened by one S consumed by a stopped E.

        The S remains a calculation/evidence object, not a new public owner.
        Its first E inherits the stopped larger E's reconciled family and next
        number.  Recursive children are then rebuilt from the promoted E so
        Order discovery and stop chronology remain native E calculations.
        """
        stopped = self._parent_stop("S", s_zone)
        if stopped is None:
            return []
        _, stop_event = stopped
        family = str(getattr(owner, "family"))
        number = int(getattr(owner, "number")) + 1
        parent_type = "S"
        parent: object = s_zone
        chain: list[EZone] = []
        seen_sources: set[int] = set()
        while True:
            zone = self._zone(family, number, parent_type, parent, stop_event)
            if zone is None or zone.source_index in seen_sources:
                break
            parent_source_time = getattr(parent, "source_time")
            if self._has_sequence_reset_between(
                parent_source_time, zone.source_time
            ):
                break
            chain.append(zone)
            seen_sources.add(zone.source_index)
            next_stop = self._parent_stop("E", zone)
            if next_stop is None:
                break
            _, stop_event = next_stop
            parent_type, parent = "E", zone
            number += 1
        return chain

    def replace_with_earlier_continuation(
        self, base_zones: Sequence[EZone], owner: EZone, continuation: Sequence[EZone],
    ) -> list[EZone]:
        """Replace an owner's not-yet-decided descendant branch when an earlier one wins."""
        if not continuation:
            return list(base_zones)
        owner_id = (owner.source_index, owner.source_time)
        by_id = {(item.source_index, item.source_time): item for item in base_zones}

        def descends_from_owner(item: EZone) -> bool:
            current = item
            seen: set[tuple[int, datetime]] = set()
            while current.parent_type == "E":
                parent_id = (current.parent_source_index, current.parent_source_time)
                if parent_id == owner_id:
                    return True
                if parent_id in seen:
                    return False
                seen.add(parent_id)
                parent = by_id.get(parent_id)
                if parent is None:
                    return False
                current = parent
            return False

        direct_children = [
            item for item in base_zones
            if item.parent_type == "E"
            and (item.parent_source_index, item.parent_source_time) == owner_id
        ]
        first = continuation[0]
        if direct_children:
            winner = min(
                direct_children,
                key=lambda item: (item.decision_event_time, item.source_time),
            )
            if first.decision_event_time >= winner.decision_event_time:
                return list(base_zones)

        kept = [item for item in base_zones if not descends_from_owner(item)]
        merged = [*kept, *continuation]
        return self.resolve_same_source_conflicts(merged)

    def resolve_same_source_conflicts(
        self, zones: Sequence[EZone],
    ) -> list[EZone]:
        """Keep exactly one accepted E behavior for each physical source candle.

        Candidate discovery may legitimately reach the same source through
        multiple S/E lineages.  Those alternatives are evidence only; once E
        reconciliation has assigned an accepted family/number, a lower-ranked
        alternative at that *same physical source* is not a second behavior.

        Dominance is the shared project rule: Red E outranks Blue E regardless
        of number, and within the same family the higher E number outranks the
        lower number.  Exact ties preserve the earlier accepted object so this
        resolver never rewrites provenance merely to deduplicate output.
        """
        winners: dict[tuple[int, datetime], EZone] = {}
        order: list[tuple[int, datetime]] = []

        def outranks(candidate: EZone, current: EZone) -> bool:
            candidate_priority = self.sequence_priority("e", candidate.family)
            current_priority = self.sequence_priority("e", current.family)
            if candidate_priority != current_priority:
                return candidate_priority > current_priority
            if candidate.family == current.family and candidate.number != current.number:
                return candidate.number > current.number
            return False

        for zone in zones:
            identity = (int(zone.source_index), zone.source_time)
            current = winners.get(identity)
            if current is None:
                winners[identity] = zone
                order.append(identity)
            elif outranks(zone, current):
                winners[identity] = zone

        result = [winners[identity] for identity in order]
        result.sort(
            key=lambda item: (
                item.source_time, item.source_index, item.decision_event_time,
            )
        )
        return result

    def restore_independent_s_roots(
        self, dominant_zones: Sequence[EZone],
    ) -> list[EZone]:
        """Restore calculation-valid E1 roots owned directly by accepted S.

        E dominance chooses which chain owns larger-module continuation, but
        formation of a new E behavior is independent: every accepted, stopped
        S may still form its own direct E1.  A reconciled dominant zone that
        came from that same S is therefore replaced by the original direct
        root (family/number from the S chain), while missing roots are added.
        Suppressed S evidence consumed by a larger E is not in ``self.s_zones``
        and cannot manufacture a competing E1 through this path.
        """
        # A physical source already owned by an accepted E cannot also keep
        # an S parent alive for downstream E-root restoration. Public lifecycle
        # finality already gives that candle to E; applying the same ownership
        # here prevents a provisional same-source S from manufacturing a later
        # E1 after reconciliation.
        dominant_sources = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in dominant_zones
        }
        accepted_s = {
            (int(getattr(item, "source_index")), getattr(item, "source_time"))
            for item in self.s_zones
            if (int(getattr(item, "source_index")), getattr(item, "source_time"))
            not in dominant_sources
        }
        roots = [
            item for item in self._last_candidate_zones
            if item.parent_type == "S"
            and int(item.number) == 1
            and (item.parent_source_index, item.parent_source_time) in accepted_s
        ]
        result = list(dominant_zones)
        for root in roots:
            parent_id = (root.parent_source_index, root.parent_source_time)
            same_parent = [
                item for item in result
                if item.parent_type == "S"
                and (item.parent_source_index, item.parent_source_time) == parent_id
            ]
            if same_parent:
                winner = min(
                    same_parent,
                    key=lambda item: (item.decision_event_time, item.source_time),
                )
                result = [item for item in result if item is not winner]
                result.append(root)
            elif not any(
                item.source_index == root.source_index
                and item.source_time == root.source_time
                and item.parent_type == root.parent_type
                and item.parent_source_index == root.parent_source_index
                and item.parent_source_time == root.parent_source_time
                for item in result
            ):
                result.append(root)
        return self.resolve_same_source_conflicts(result)

    def _discover_candidate_chains(self) -> list[EZone]:
        """Build provisional recursive E chains from every stopped S parent.

        Calculation-invalid S geometry remains provisional discovery evidence.
        Its explicit invalid identity cannot create or retain a parent-stop
        Order_A cause or open a competing cross-family root over an occupied
        native E continuation. Valid historical S provenance and shared
        Order_B reset-leg causes remain eligible in the physical Order ledger.
        """
        # Discover S-owned orders before walking recursive E chains.  A valid
        # order formed inside an E parent's lifetime must remain available even
        # when that S branch is reconciled later than the E branch.
        for s_zone in self.s_zones:
            stop = self._parent_stop("S", s_zone)
            if stop is not None:
                self._register_order_audit("S", s_zone, stop[1])

        chains: list[tuple[object, list[EZone]]] = []
        candidates: list[EZone] = []
        for s_zone in self.s_zones:
            stop = self._parent_stop("S", s_zone)
            if stop is None:
                continue
            _, stop_event = stop

            # Every fully formed S starts an independent provisional E chain.
            # Final lifecycle eligibility is resolved after all candidate
            # continuations are visible, so exact same-source cross-family
            # collisions can be judged without timestamp/fixture exceptions.
            family = str(getattr(s_zone, "color"))
            number = 1

            parent_type: str = "S"
            parent: object = s_zone
            chain_sources: set[int] = set()
            chain: list[EZone] = []
            while True:
                zone = self._zone(family, number, parent_type, parent, stop_event)
                if zone is None:
                    break
                if zone.source_index in chain_sources:
                    break
                chain.append(zone)
                candidates.append(zone)
                chain_sources.add(zone.source_index)
                parent_type, parent = "E", zone
                next_stop = self._parent_stop("E", zone)
                if next_stop is None:
                    break
                _, stop_event = next_stop
                number += 1
            if chain:
                chains.append((s_zone, chain))

        if not self.invalid_s_root_identities or not candidates:
            return candidates

        continuation_families: dict[tuple[datetime, int], set[str]] = {}
        for zone in candidates:
            if zone.parent_type != "E":
                continue
            identity = (zone.source_time, int(zone.source_index))
            continuation_families.setdefault(identity, set()).add(zone.family)

        blocked_roots: set[tuple[datetime, int]] = set()
        for s_zone, _ in chains:
            identity = (
                getattr(s_zone, "source_time"),
                int(getattr(s_zone, "source_index")),
            )
            if identity not in self.invalid_s_root_identities:
                continue
            s_family = str(getattr(s_zone, "color"))
            if any(
                family != s_family
                for family in continuation_families.get(identity, set())
            ):
                blocked_roots.add(identity)

        if not blocked_roots:
            return candidates

        return [
            zone
            for s_zone, chain in chains
            if (
                getattr(s_zone, "source_time"),
                int(getattr(s_zone, "source_index")),
            ) not in blocked_roots
            for zone in chain
        ]

    def _reconcile_candidate_chains(
        self, candidates: list[EZone]
    ) -> list[EZone]:
        """Resolve competing E chains into the accepted chronological lifecycle."""
        # Resolve competing chains chronologically.  A stopped E is removed
        # from the active set immediately; it remains only as historical
        # output and cannot affect a later family or number.
        by_source: dict[int, list[EZone]] = {}
        for zone in candidates:
            by_source.setdefault(zone.source_index, []).append(zone)
        # A later E continuation can supersede a provisional E that was
        # started directly from an S before the continuation was confirmed.
        # Keep the later, deeper (bullish) / higher (bearish) structure.  This
        # This prevents a provisional S-owned object from consuming the active
        # chain before the later confirmed continuation.
        pending = sorted(
            by_source.values(),
            key=lambda item: (
                min(zone.source_time for zone in item),
                min(zone.decision_event_time for zone in item),
            ),
        )
        numbered: list[EZone] = []
        active: list[EZone] = []
        sequence_start: datetime | None = None

        candidates_by_source_time = {
            (item.source_index, item.source_time): item
            for item in candidates
        }

        def valid_order(zone: EZone) -> bool:
            return not self._blocked_by_gate_owned_order(zone)

        def parent_active(zone: EZone, seen: set[tuple[int, datetime]] | None = None) -> bool:
            if zone.parent_type == "S":
                parent_s = next(
                    (
                        item for item in self.s_zones
                        if int(getattr(item, "source_index"))
                        == zone.parent_source_index
                        and getattr(item, "source_time")
                        == zone.parent_source_time
                    ),
                    None,
                )
                if parent_s is None:
                    return False
                if sequence_start is not None and (
                    parent_s.source_time <= sequence_start
                    or parent_s.a_source_time < sequence_start
                ):
                    return False
                prior_e = [
                    item for item in numbered
                    if getattr(item, "source_time")
                    < zone.source_time
                    and (sequence_start is None or item.source_time > sequence_start)
                ]
                if not prior_e:
                    return True
                prior = max(
                    prior_e, key=lambda item: getattr(item, "source_time")
                )
                rebuilt_after_e = (
                    getattr(parent_s, "source_time")
                    > getattr(prior, "source_time")
                    and getattr(parent_s, "a_source_time")
                    >= getattr(prior, "source_time")
                )
                # A still-unconsumed Red S is not invalidated by a nested
                # Blue E. Its later strict stop owns the Red transition.
                dominant_s = (
                    str(getattr(parent_s, "color")) == "red"
                    and prior.family == "blue"
                    and parent_s.source_time < prior.source_time
                    and not any(
                        item.parent_type == "S"
                        and item.parent_source_time == zone.parent_source_time
                        for item in numbered
                    )
                )
                return rebuilt_after_e or dominant_s
            if zone.parent_source_time == sequence_start:
                # The StopAll source is a valid order gate, but never an
                # active E whose family/number could leak across the reset.
                return True
            if any(
                item.source_index == zone.parent_source_index
                and item.source_time == zone.parent_source_time
                for item in active
            ):
                return True
            identity = (zone.parent_source_index, zone.parent_source_time)
            if seen is None:
                seen = set()
            if identity in seen:
                return False
            seen.add(identity)
            skipped_parent = candidates_by_source_time.get(identity)
            return (
                skipped_parent is not None
                and not valid_order(skipped_parent)
                and parent_active(skipped_parent, seen)
            )

        def stopped_by(zone: EZone, prior: EZone) -> bool:
            if zone.decision_event_time <= prior.decision_event_time:
                return False
            if self.direction == "bullish":
                return zone.price < prior.price
            return zone.price > prior.price

        for group in pending:
            eligible = [
                item for item in group
                if valid_order(item) and parent_active(item)
            ]
            if not eligible:
                continue
            # A lower-priority S cannot steal an active E continuation.
            # Red S may supersede Blue E, but no S supersedes Red E.
            # Color follows the accepted stopped parent's reconciled family.
            eligible = [
                item
                for item in eligible
                if not (
                    item.parent_type == "S"
                    and any(
                        stopped_by(item, owner)
                        and (owner.family == "red" or item.family == "blue")
                        and any(
                            child.parent_type == "E"
                            and child.parent_source_index == owner.source_index
                            and child.parent_source_time == owner.source_time
                            and child.decision_event_time
                            >= item.decision_event_time
                            for child in candidates
                        )
                        for owner in active
                    )
                )
            ]
            if not eligible:
                continue
            current_owners = [
                item for item in eligible
                if not (
                    item.parent_type == "E"
                    and item.family == "blue"
                    and any(
                        str(getattr(s_zone, "color")) == "red"
                        and getattr(s_zone, "source_time")
                        > item.parent_source_time
                        and getattr(s_zone, "decision_event_time")
                        < item.parent_stop_event_time
                        for s_zone in self.s_zones
                    )
                )
            ]
            if current_owners:
                eligible = current_owners
            def ownership_priority(item: EZone) -> int:
                parent = next((prior for prior in active
                    if item.parent_type == "E"
                    and prior.source_time == item.parent_source_time), None)
                parent_family = parent.family if parent else item.family
                return self.sequence_priority(item.parent_type, parent_family)

            # One physical E source may be reachable through competing
            # Red/Blue S/E lineages.  Family priority is authoritative at the
            # physical source: Red outranks Blue even when the Blue candidate
            # happens to reach its decision a few lower-timeframe ticks
            # earlier.  Chronology remains the tie-breaker *within* the same
            # behavioral priority.  Applying this before chain reconciliation
            # prevents the dominant Red candidate from being discarded before
            # the final same-source resolver can see it.
            zone = min(
                eligible,
                key=lambda item: (
                    -ownership_priority(item),
                    item.decision_event_time,
                    item.parent_stop_event_time,
                ),
            )
            stopped_by_family: dict[str, list[EZone]] = {"red": [], "blue": []}
            for prior in active:
                if stopped_by(zone, prior):
                    stopped_by_family[prior.family].append(prior)

            parent_identity = (zone.parent_source_index, zone.parent_source_time)
            parent_is_active = (
                zone.parent_type == "S"
                or zone.parent_source_time == sequence_start
            ) or any(
                (item.source_index, item.source_time) == parent_identity
                for item in active
            )
            if not parent_is_active:
                # Without independent secondary Order creation causes, a child
                # cannot detach from an inactive parent lineage.
                continue

            owner = next((item for item in active
                          if zone.parent_type == "E"
                          and item.source_time == zone.parent_source_time), None)
            # Color follows the accepted stopped parent, not merely the most
            # recent S. A still-unbroken Red S does not recolor a nested E.
            parent_family = owner.family if owner is not None else zone.family

            if parent_family == "red":
                family = "red"
                number = (
                    max(item.number for item in stopped_by_family["red"]) + 1
                    if stopped_by_family["red"]
                    else 1
                )
            elif stopped_by_family["red"]:
                family = "red"
                number = max(item.number for item in stopped_by_family["red"]) + 1
            elif parent_family == "blue":
                family = "blue"
                number = (
                    max(item.number for item in stopped_by_family["blue"]) + 1
                    if stopped_by_family["blue"]
                    else 1
                )
            elif stopped_by_family["blue"]:
                family = "blue"
                number = max(item.number for item in stopped_by_family["blue"]) + 1
            else:
                family = zone.family
                number = 1
            stopped_ids = {
                (item.source_index, item.source_time)
                for values in stopped_by_family.values() for item in values
            }
            active = [
                item for item in active
                if (item.source_index, item.source_time) not in stopped_ids
            ]
            numbered_zone = replace(zone, family=family, number=number)
            numbered.append(numbered_zone)
            if zone.source_time in self.sequence_resets:
                active.clear()
                sequence_start = zone.source_time
            else:
                active.append(numbered_zone)
        def collect_lineage(zone: EZone, seen: set[tuple[int, datetime]]) -> None:
            identity = (zone.source_index, zone.source_time)
            if identity in seen:
                return
            seen.add(identity)
            self.visual_lifecycle_starts.add(zone.parent_stop_event_time)
            if zone.parent_type == "S":
                return
            parent = candidates_by_source_time.get(
                (zone.parent_source_index, zone.parent_source_time)
            )
            if parent is not None:
                collect_lineage(parent, seen)

        lineage_seen: set[tuple[int, datetime]] = set()
        for zone in numbered:
            collect_lineage(zone, lineage_seen)

        numbered = [replace(item, parent_type="StopAll")
                    if item.parent_type == "E"
                    and item.parent_source_time in self.sequence_resets
                    else item for item in numbered]
        return numbered


    def detect(self) -> list[EZone]:
        """Discover, reconcile and audit recursive E lifecycles."""
        self._clear_order_audit()
        self.register_order_b_reset_legs(self.order_b_legs)
        self.visual_lifecycle_starts.clear()
        candidates = self._discover_candidate_chains()
        self._last_candidate_zones = list(candidates)
        numbered = self._reconcile_candidate_chains(candidates)
        numbered = self._apply_consumed_s_evidence(numbered)
        numbered = self.resolve_same_source_conflicts(numbered)
        return self._rebuild_accepted_order_audit(numbered)


def detect_e_zones(
    direction: str,
    trend_reactions: Sequence[object],
    opposite_reactions: Sequence[object],
    s_zones: Sequence[object],
    opposite_resets: Sequence[object],
    chronology: object,
    start_index: int = 0,
    end_index: int | None = None,
    direct_geometry_finder: Callable[[str, int, int, datetime], object | None] | None = None,
    blocked_order_first_times: set[datetime] | None = None,
    initial_order_audit: dict[tuple[int, int], dict[str, object]] | None = None,
    sequence_priority: Callable[[str, str], int] | None = None,
    invalid_s_root_identities: set[tuple[datetime, int]] | None = None,
) -> list[EZone]:
    return EZoneDetector(
        direction,
        trend_reactions,
        opposite_reactions,
        s_zones,
        opposite_resets,
        chronology,
        start_index,
        end_index,
        direct_geometry_finder,
        blocked_order_first_times=blocked_order_first_times,
        initial_order_audit=initial_order_audit,
        sequence_priority=sequence_priority,
        invalid_s_root_identities=invalid_s_root_identities,
    ).detect()
````
<!-- EXACT-SOURCE-END:pipeline/e_zone_detector.py -->

### 16.10 `pipeline/lifecycle_engine.py` — Lifecycle / StopAll

**SHA-256:** `94feb038e1e78b291762cfc03dfc370e48bb94f3e1fe1171b7a5206301e8be13`  
**Bytes:** `64325`  
**LF count:** `1555`

<!-- EXACT-SOURCE-BEGIN:pipeline/lifecycle_engine.py -->
````python
"""Cross-stage behavior lifecycle, visibility, priority, and StopAll ownership.

Owns the single shared behavior-priority table, accepted-vs-blocked Order
precedence, A/S/E/StopAll public ownership boundaries, Internal-Reaction output
filters, and StopAll detection/reconciliation. It does not reconstruct detector
geometry.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field, replace
from datetime import datetime
from decimal import Decimal
from typing import Sequence

from core_utils import as_decimal, order_identity
from order_audit_engine import (
    accepted_audit_entry, order_identity_is_internal, prepare_order_audit,
)
from direction_policy import policy_for


STOP_ALL_VERSION = "1.17.0"
STOP_ALL_IMPLEMENTATION_VERSION = "1.18.0"
STOP_ALL_LAST_MODIFIED = "2026-09-27 23:17:17 +03:30"


SEQUENCE_PRIORITY = {
    ("s", "blue"): 1,
    ("e", "blue"): 2,
    ("s", "red"): 3,
    ("e", "red"): 4,
}


def sequence_priority(kind: str, family: str) -> int:
    """Return the single authoritative cross-stage behavior priority."""
    return SEQUENCE_PRIORITY[(str(kind).lower(), str(family).lower())]


@dataclass(frozen=True, slots=True)
class StopAll:
    direction: str
    number: int
    source_index: int
    source_time: datetime
    price: Decimal
    decision_index: int
    decision_time: datetime
    decision_event_time: datetime
    gate_type: str
    gate_event_time: datetime
    stopped_behavior_type: str
    stopped_behavior_key: str
    stopped_behavior_count: int
    underlying_e_family: str | None
    underlying_e_number: int | None
    order_direction: str | None
    order_reaction_number: int | None
    order_mode: str | None
    order_causes: tuple[str, ...]
    order_parent_stop_cause_time: datetime | None
    order_first_index: int | None
    order_first_time: datetime | None
    order_break_index: int | None
    order_break_time: datetime | None
    order_confirmation_time: datetime | None
    order_box_top: Decimal | None
    order_box_top_source_index: int | None
    order_box_top_source_time: datetime | None
    order_box_bottom: Decimal | None
    order_box_bottom_source_index: int | None
    order_box_bottom_source_time: datetime | None
    order_stop_level: Decimal | None
    order_stop_source_index: int | None
    order_stop_source_time: datetime | None
    stop_index: int | None
    stop_time: datetime | None
    stop_event_time: datetime | None
    # Immutable presentation provenance for the exact constructor donor. It is
    # intentionally separate from stopped_behavior_* (the lifecycle gate).
    # These fields never affect StopAll formation, priority, visibility, or
    # Order selection.
    donor_type: str | None = field(default=None, kw_only=True)
    donor_source_index: int | None = field(default=None, kw_only=True)
    donor_source_time: datetime | None = field(default=None, kw_only=True)
    donor_color: str | None = field(default=None, kw_only=True)
    donor_number: int | None = field(default=None, kw_only=True)
    donor_price: Decimal | None = field(default=None, kw_only=True)
    donor_stop_time: datetime | None = field(default=None, kw_only=True)
    donor_stop_event_time: datetime | None = field(default=None, kw_only=True)


class StopAllDetector:
    def __init__(
        self,
        direction: str,
        s_zones: Sequence[object],
        e_zones: Sequence[object],
        chronology: object,
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.s_zones = list(s_zones)
        self.e_zones = sorted(
            e_zones, key=lambda item: (item.source_time, item.source_index)
        )
        self.chronology = chronology
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index
        self.times = chronology.times

    def _strict_stop(
        self, start: datetime, level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        left = bisect_left(self.lower_times, start)
        right = len(self.lower)
        position = (
            self.lower_index.first_less(left, right, level)
            if self.direction == "bullish"
            else self.lower_index.first_greater(left, right, level)
        )
        if position is None:
            return None
        event = self.lower_times[position]
        index = self.chronology.main_index(event, clamp=True)
        return index, self.times[index], event

    @staticmethod
    def _e_key(item: object) -> tuple[str, int]:
        return str(item.family), int(item.number)

    @staticmethod
    def _dominates_e(new: tuple[str, int], old: tuple[str, int]) -> bool:
        new_family, new_number = new
        old_family, old_number = old
        if new_family == old_family:
            return new_number > old_number
        # Red is always the dominant E family. A higher-numbered Blue E must
        # not separate or replace an active Red group.
        return new_family == "red" and old_family == "blue"

    @classmethod
    def _sequence_priority(cls, kind: str, family: str) -> int:
        return sequence_priority(kind, family)

    @classmethod
    def _active_sequence_priority(
        cls, s_key: str | None, e_key: tuple[str, int] | None,
    ) -> int:
        if e_key is not None:
            return cls._sequence_priority("e", e_key[0])
        if s_key is not None:
            return cls._sequence_priority("s", s_key)
        return 0

    def _stopall_from_e(
        self,
        item: object,
        number: int,
        gate_type: str,
        gate_event: datetime,
        behavior_type: str,
        behavior_key: str,
        behavior_count: int,
    ) -> StopAll:
        return StopAll(
            direction=self.direction,
            number=number,
            source_index=int(item.source_index),
            source_time=item.source_time,
            price=as_decimal(item.price),
            decision_index=int(item.decision_index),
            decision_time=item.decision_time,
            decision_event_time=item.decision_event_time,
            gate_type=gate_type,
            gate_event_time=gate_event,
            stopped_behavior_type=behavior_type,
            stopped_behavior_key=behavior_key,
            stopped_behavior_count=behavior_count,
            underlying_e_family=str(item.family),
            underlying_e_number=int(item.number),
            order_direction=str(item.order_direction),
            order_reaction_number=int(item.order_reaction_number),
            order_mode=str(item.order_mode),
            order_causes=tuple(getattr(item, "order_causes", ())),
            order_parent_stop_cause_time=getattr(
                item, "order_parent_stop_cause_time", None
            ),
            order_first_index=int(item.order_first_index),
            order_first_time=item.order_first_time,
            order_break_index=int(item.order_break_index),
            order_break_time=item.order_break_time,
            order_confirmation_time=item.order_confirmation_time,
            order_box_top=as_decimal(item.order_box_top),
            order_box_top_source_index=int(item.order_box_top_source_index),
            order_box_top_source_time=item.order_box_top_source_time,
            order_box_bottom=as_decimal(item.order_box_bottom),
            order_box_bottom_source_index=int(item.order_box_bottom_source_index),
            order_box_bottom_source_time=item.order_box_bottom_source_time,
            order_stop_level=as_decimal(item.order_stop_level),
            order_stop_source_index=int(item.order_stop_source_index),
            order_stop_source_time=item.order_stop_source_time,
            stop_index=None,
            stop_time=None,
            stop_event_time=None,
            donor_type="E",
            donor_source_index=int(item.source_index),
            donor_source_time=item.source_time,
            donor_color=str(item.family),
            donor_number=int(item.number),
            donor_price=as_decimal(item.price),
        )

    @staticmethod
    def _optional_int(value: object | None) -> int | None:
        return None if value is None else int(value)

    @staticmethod
    def _optional_decimal(value: object | None) -> Decimal | None:
        return None if value is None else as_decimal(value)

    def _stopall_from_s(
        self,
        item: object,
        behavior_type: str,
        behavior_key: str,
        behavior_count: int,
        underlying_e_key: tuple[str, int] | None,
    ) -> StopAll:
        """Promote the accepted opposite-color S into a fresh StopAll1.

        This is the direction-invariant family reversal gate.  In both
        Bullish and Bearish calculations, only an accepted native Mode-B S Red
        is promoted after two accepted occurrences of the same Blue behavior
        group since the latest accepted Red or StopAll boundary.  The repeated
        group need not remain the current dominant owner.  Directional mirroring is handled
        by strict stop/reaction geometry; Red/Blue family
        labels themselves are invariant.  Type-3 S Blue has no formation
        Order, so StopAll Order provenance remains optional.
        """
        return StopAll(
            direction=self.direction,
            number=1,
            source_index=int(item.source_index),
            source_time=item.source_time,
            price=as_decimal(item.price),
            decision_index=int(item.decision_index),
            decision_time=item.decision_time,
            decision_event_time=item.decision_event_time,
            gate_type="opposite-s-group-stop",
            gate_event_time=item.decision_event_time,
            stopped_behavior_type=behavior_type,
            stopped_behavior_key=behavior_key,
            stopped_behavior_count=behavior_count,
            underlying_e_family=(
                underlying_e_key[0] if underlying_e_key is not None else None
            ),
            underlying_e_number=(
                underlying_e_key[1] if underlying_e_key is not None else None
            ),
            order_direction=getattr(item, "order_direction", None),
            order_reaction_number=self._optional_int(
                getattr(item, "order_reaction_number", None)
            ),
            order_mode=getattr(item, "order_mode", None),
            order_causes=(),
            order_parent_stop_cause_time=getattr(
                item, "a_stop_event_time", None
            ),
            order_first_index=self._optional_int(
                getattr(item, "order_first_index", None)
            ),
            order_first_time=getattr(item, "order_first_time", None),
            order_break_index=self._optional_int(
                getattr(item, "order_break_index", None)
            ),
            order_break_time=getattr(item, "order_break_time", None),
            order_confirmation_time=getattr(
                item, "order_confirmation_time", None
            ),
            order_box_top=self._optional_decimal(
                getattr(item, "order_box_top", None)
            ),
            order_box_top_source_index=self._optional_int(
                getattr(item, "order_box_top_source_index", None)
            ),
            order_box_top_source_time=getattr(
                item, "order_box_top_source_time", None
            ),
            order_box_bottom=self._optional_decimal(
                getattr(item, "order_box_bottom", None)
            ),
            order_box_bottom_source_index=self._optional_int(
                getattr(item, "order_box_bottom_source_index", None)
            ),
            order_box_bottom_source_time=getattr(
                item, "order_box_bottom_source_time", None
            ),
            order_stop_level=self._optional_decimal(
                getattr(item, "order_stop_level", None)
            ),
            order_stop_source_index=self._optional_int(
                getattr(item, "order_stop_source_index", None)
            ),
            order_stop_source_time=getattr(
                item, "order_stop_source_time", None
            ),
            stop_index=None,
            stop_time=None,
            stop_event_time=None,
            donor_type="S",
            donor_source_index=int(item.source_index),
            donor_source_time=item.source_time,
            donor_color=str(item.color),
            donor_number=None,
            donor_price=as_decimal(item.price),
        )

    @staticmethod
    def _blue_repeat_key(kind: str, number: int | None = None) -> tuple[str, int | None]:
        """Return the pending-reversal exact Blue behavior-group key.

        S Blue is one group regardless of its internal subtype.  Each E number
        is a separate group: E1 Blue, E2 Blue, E5 Blue, ... .  Counts are
        accepted-occurrence counts since the most recent Red S/Red E/StopAll,
        not counts of dominant-owner transitions.
        """
        normalized = str(kind).upper()
        if normalized == "S":
            return ("S", None)
        if normalized != "E" or number is None:
            raise ValueError("Blue repeat key must be S or numbered E.")
        return ("E", int(number))

    @staticmethod
    def _record_blue_repeat(
        counts: dict[tuple[str, int | None], int],
        latest: dict[tuple[str, int | None], object],
        key: tuple[str, int | None],
        item: object,
    ) -> None:
        counts[key] = counts.get(key, 0) + 1
        latest[key] = item

    def _opposite_s_stopall_gate(
        self,
        s_item: object,
        blue_repeat_counts: dict[tuple[str, int | None], int],
        blue_repeat_latest: dict[tuple[str, int | None], object],
    ) -> tuple[str, str, int, tuple[str, int] | None] | None:
        """Return Blue-repeat metadata when accepted S Red must become StopAll.

        Accepted Blue occurrences accumulate per exact S/E group until the
        first accepted Red S, accepted Red E, or hard StopAll boundary.  A Red
        behavior resolves the prior Blue reversal opportunity; a later S Red
        cannot consume its stale evidence.  The incoming S Red must have a
        native Mode-B formation Order; different numbered E groups never add.
        E-driven StopAll counters/priority are independent of this reversal
        evidence and retain their existing semantics.
        """
        if str(getattr(s_item, "color", "")).lower() != "red":
            return None
        # An initial native Mode-A Order opens an independent A→S Red branch;
        # it cannot consume old Blue-repeat evidence to promote that S to
        # StopAll. A continued Mode-B Order may own the reversal gate in the
        # existing hard lifecycle, in either market direction.
        if str(getattr(s_item, "order_mode", "")).upper() != "B":
            return None

        qualified = [
            (key, count, blue_repeat_latest[key])
            for key, count in blue_repeat_counts.items()
            if count >= 2 and key in blue_repeat_latest
        ]
        if not qualified:
            return None

        key, count, _ = max(
            qualified,
            key=lambda entry: (
                getattr(entry[2], "source_time"),
                int(getattr(entry[2], "source_index", -1)),
                1 if entry[0][0] == "E" else 0,
                -1 if entry[0][1] is None else int(entry[0][1]),
            ),
        )
        if key[0] == "S":
            return ("S", "S blue", count, None)
        e_number = int(key[1])
        return ("E", f"E{e_number} blue", count, ("blue", e_number))

    def detect(self) -> list[StopAll]:
        s_events = sorted(
            self.s_zones, key=lambda item: (item.source_time, item.source_index)
        )
        s_position = 0
        s_key: str | None = None
        s_count = 0
        e_key: tuple[str, int] | None = None
        e_count = 0
        dominant_s_item: object | None = None
        dominant_e_item: object | None = None
        active: list[StopAll] = []
        output: list[StopAll] = []
        blue_repeat_counts: dict[tuple[str, int | None], int] = {}
        blue_repeat_latest: dict[tuple[str, int | None], object] = {}

        def reset_cycle_blue_repeats() -> None:
            blue_repeat_counts.clear()
            blue_repeat_latest.clear()

        def process_s_event(s_item: object) -> None:
            nonlocal s_key, s_count, e_key, e_count, dominant_s_item, dominant_e_item, active

            reversal = self._opposite_s_stopall_gate(
                s_item, blue_repeat_counts, blue_repeat_latest
            )
            if reversal is not None:
                behavior_type, behavior_key, behavior_count, underlying_e_key = reversal
                zone = self._stopall_from_s(
                    s_item,
                    behavior_type,
                    behavior_key,
                    behavior_count,
                    underlying_e_key,
                )
                output.append(zone)
                # The S-reversal StopAll starts a fresh lifecycle. Historical
                # StopAll objects remain in output, but no pre-boundary active
                # StopAll may influence numbering or ownership in the new cycle.
                active = [zone]
                s_key = e_key = None
                s_count = e_count = 0
                dominant_s_item = None
                dominant_e_item = None
                reset_cycle_blue_repeats()
                return

            color = str(s_item.color)
            # An accepted Red S resolves the pending Blue-repeat reversal
            # opportunity even if its native Order mode cannot promote it.
            # Later Red S may use only Blue occurrences accepted after it.
            if color == "red":
                reset_cycle_blue_repeats()
            if color == "blue":
                self._record_blue_repeat(
                    blue_repeat_counts,
                    blue_repeat_latest,
                    self._blue_repeat_key("S"),
                    s_item,
                )
            incoming_priority = self._sequence_priority("s", color)
            active_priority = self._active_sequence_priority(s_key, e_key)
            if e_key is None and s_key == color:
                s_count += 1
                dominant_s_item = s_item
            elif incoming_priority > active_priority:
                s_key, s_count = color, 1
                dominant_s_item = s_item
                e_key, e_count = None, 0
                dominant_e_item = None

        for e_item in self.e_zones:
            while s_position < len(s_events) and (
                s_events[s_position].source_time < e_item.source_time
            ):
                process_s_event(s_events[s_position])
                s_position += 1

            e_decision = e_item.decision_event_time
            stopped_active = []
            for item in active:
                stop = self._strict_stop(item.decision_event_time, item.price)
                if stop is not None and stop[2] <= e_decision:
                    stopped_active.append((item, stop))
            if stopped_active:
                highest = max(item.number for item, _ in stopped_active)
                gate_event = min(stop[2] for _, stop in stopped_active)
                zone = self._stopall_from_e(
                    e_item, highest + 1, "stopall-stop", gate_event,
                    "StopAll", f"StopAll{highest}", len(stopped_active),
                )
                stopped_ids = {id(item) for item, _ in stopped_active}
                active = [item for item in active if id(item) not in stopped_ids]
                output.append(zone)
                active.append(zone)
                s_key = e_key = None
                s_count = e_count = 0
                dominant_s_item = None
                dominant_e_item = None
                reset_cycle_blue_repeats()
                continue

            new_key = self._e_key(e_item)
            # Once a dominant group has stopped, this E supplies the winning
            # order only. Its family/number need not match the stopped group.
            qualifies_e = e_key is not None and e_count >= 2
            qualifies_s = (
                e_key is None
                and s_key is not None
                and s_count >= 2
            )
            if qualifies_e or qualifies_s:
                parent = max(
                    (
                        item for item in (
                            self.e_zones if qualifies_e else self.s_zones
                        )
                        if item.source_time < e_item.source_time
                        and (
                            self._e_key(item) == e_key if qualifies_e
                            else str(item.color) == s_key
                        )
                    ),
                    key=lambda item: item.source_time,
                )
                gate = self._strict_stop(
                    parent.decision_event_time, as_decimal(parent.price)
                )
                if gate is not None and gate[2] <= e_decision:
                    zone = self._stopall_from_e(
                        e_item, 1, "sequence-group-stop", gate[2],
                        "E" if qualifies_e else "S",
                        (
                            f"E{e_key[1]} {e_key[0]}" if qualifies_e
                            else f"S {s_key}"
                        ),
                        e_count if qualifies_e else s_count,
                    )
                    output.append(zone)
                    active.append(zone)
                    s_key = e_key = None
                    s_count = e_count = 0
                    dominant_s_item = None
                    dominant_e_item = None
                    reset_cycle_blue_repeats()
                    continue

            # Red E resolves earlier Blue-repeat evidence. It may be a
            # higher-stage replacement of Blue, but cannot leave a stale
            # Blue reversal armed for a later unrelated S Red. Do not reset
            # dominant sequence state: E-driven StopAll gates own that state.
            if new_key[0] == "red":
                reset_cycle_blue_repeats()
            # This E remains accepted after independent StopAll checks.
            if new_key[0] == "blue":
                self._record_blue_repeat(
                    blue_repeat_counts,
                    blue_repeat_latest,
                    self._blue_repeat_key("E", new_key[1]),
                    e_item,
                )

            # Stage ownership is A -> S -> E -> StopAll. When the first E
            # replaces an S owner, E starts a new dominant-stage occurrence;
            # the superseded S is not counted again in current-owner sequence
            # state. Pending Blue-repeat counting is independent above.
            if e_key == new_key:
                e_count += 1
                dominant_e_item = e_item
            else:
                incoming_priority = self._sequence_priority("e", new_key[0])
                active_priority = self._active_sequence_priority(s_key, e_key)
                replaces_active = incoming_priority > active_priority
                advances_e = (
                    e_key is not None
                    and incoming_priority == active_priority
                    and self._dominates_e(new_key, e_key)
                )
                if replaces_active or advances_e:
                    e_key, e_count = new_key, 1
                    dominant_e_item = e_item
                    s_key, s_count = None, 0
                    dominant_s_item = None
            # A lower-priority Sequence event remains valid output but cannot
            # replace or separate the active dominant group.

        # The reversal rule is driven by accepted S itself, so it must still
        # fire when the triggering S occurs after the final accepted E.
        while s_position < len(s_events):
            process_s_event(s_events[s_position])
            s_position += 1

        completed = []
        for item in output:
            stop = self._strict_stop(item.decision_event_time, item.price)
            completed.append(
                replace(
                    item,
                    stop_index=stop[0] if stop else None,
                    stop_time=stop[1] if stop else None,
                    stop_event_time=stop[2] if stop else None,
                )
            )
        return completed


def detect_stopalls(
    direction: str,
    s_zones: Sequence[object],
    e_zones: Sequence[object],
    chronology: object,
) -> list[StopAll]:
    return StopAllDetector(direction, s_zones, e_zones, chronology).detect()

# ---------------------------------------------------------------------------
# Cross-stage lifecycle ownership
# ---------------------------------------------------------------------------


def resolve_order_context(
    order_audit: dict,
    accepted_a_sources: set[datetime],
    inherited_blocked_first_times: set[datetime],
    invalid_a_zones: Sequence[object],
    pending_s_a_sources: set[datetime],
    opposite_reactions: Sequence[object],
    candles: Sequence[object],
    direction: str,
    stop_finder,
) -> tuple[dict, set[datetime]]:
    """Resolve accepted stopped-A Orders against provisional Order blocks.

    Calculation ownership is authoritative: a canonical Order already accepted
    from stopped-A audit provenance cannot also be vetoed by the provisional
    invalid-leg-head block.  Keep the complete identity-keyed audit entries
    while filtering causes to A sources that remain calculation-eligible.
    """
    accepted_orders = {
        key: accepted
        for key, value in order_audit.items()
        for accepted in [accepted_audit_entry(value, accepted_a_sources)]
        if accepted is not None
    }

    blocked_order_first_times = set(inherited_blocked_first_times)
    blocked_order_first_times.update(
        blocked_orders_while_invalid_leg_heads_are_live(
            [
                item for item in invalid_a_zones
                if getattr(item, "source_time") in pending_s_a_sources
            ],
            opposite_reactions,
            candles,
            direction,
            stop_finder,
        )
    )

    accepted_initial_first_times = {
        getattr(entry["reaction"], "first_time")
        for entry in accepted_orders.values()
    }
    accepted_initial_first_times = {
        datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        if isinstance(value, str) else value
        for value in accepted_initial_first_times
    }
    blocked_order_first_times.difference_update(accepted_initial_first_times)
    return accepted_orders, blocked_order_first_times


def visible_a_zones_after_s_stops(a_zones, s_zones, candles):
    """Suppress the A candle that contains an already-confirmed S stop.

    That candle is the S-stop/E transition candle. It may still carry the
    order box's BoxBottom, but it cannot receive a new A label.
    """
    times = [getattr(item, "timestamp") for item in candles]
    stop_indices = {
        bisect_left(times, getattr(item, "decision_event_time"))
        for item in s_zones
    }
    return [
        item for item in a_zones
        if int(getattr(item, "source_index")) not in stop_indices
    ]

def module_priority(item: object) -> int:
    """Return the confirmed behavioral ownership priority.

    StopAll > E red > S red > E blue > S blue.  A is intentionally absent:
    this helper is used only after A has become an S candidate.
    """
    if hasattr(item, "stopped_behavior_type"):
        return 5
    if hasattr(item, "family"):
        return 4 if str(getattr(item, "family")).lower() == "red" else 2
    if hasattr(item, "a_source_time"):
        return 3 if str(getattr(item, "color")).lower() == "red" else 1
    return 0

def module_identity(item: object) -> tuple[object, ...]:
    return (
        type(item).__name__,
        getattr(item, "family", getattr(item, "color", None)),
        getattr(item, "number", None),
        getattr(item, "source_time"),
        getattr(item, "source_index", None),
    )

def module_stop_event(item: object, stop_event_finder=None) -> datetime | None:
    """Resolve the strict one-second stop event of an S/E/StopAll object."""
    explicit = getattr(item, "stop_event_time", None)
    if explicit is not None:
        return explicit
    if stop_event_finder is None:
        return None
    found = stop_event_finder(item)
    if found is None:
        return None
    if isinstance(found, tuple):
        return found[-1]
    return found

def strictly_beyond_boundary(
    price: Decimal, boundary: Decimal, direction: str,
) -> bool:
    return policy_for(direction).strict_cross(price, boundary)

def dominant_module(modules: Sequence[object]) -> object:
    return max(
        modules,
        key=lambda item: (
            module_priority(item),
            int(getattr(item, "number", 0)),
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )


def split_a_zones_by_dominant_stops(
    a_zones, s_zones, e_zones, stopalls, candles, direction,
    stop_event_finder=None, trend_reactions=None, confirmation_finder=None,
    a_stop_event_finder=None, stage_invalid_a_identities=None,
):
    """Separate visible A labels from A objects allowed into downstream math.

    A/Reaction/Blue discovery remains independent inside every half-leg.  Once
    an accepted S/E/StopAll is strictly stopped, however, the main candle that
    contains that stop begins the next leg comparison.  An A whose source
    extreme is strictly beyond the highest-priority stopped owner is the
    leg-start candidate, but it cannot re-enter calculation as an equal or
    smaller behavior. That candidate consumes the closed owner for subsequent
    half-leg A discovery while remaining absent from the public output.

    Equality is deliberately valid.  Stop chronology is exact at one second,
    while leg ownership is assigned to the containing main candle.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    candle_times = [getattr(item, "timestamp") for item in candles]
    modules = sorted(
        [*s_zones, *e_zones, *stopalls],
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )
    stopped = []
    for module in modules:
        stop_event = module_stop_event(module, stop_event_finder)
        if stop_event is None:
            continue
        stop_index = bisect_right(candle_times, stop_event) - 1
        if stop_index < 0:
            continue
        stopped.append((module, stop_index, stop_event))

    # A is the smallest behavior in the lifecycle hierarchy.  A strict stop
    # therefore owns exactly the next equal/lower transition just like a
    # stopped S/E/StopAll does.  This prevents an A from immediately
    # re-entering after the previous A stop while still consuming the closed
    # owner so a later, genuinely new leg may form normally.
    a_owner_identities = set()
    if a_stop_event_finder is not None:
        for a_owner in a_zones:
            found = a_stop_event_finder(a_owner)
            if found is None:
                continue
            stop_event = found[-1] if isinstance(found, tuple) else found
            stop_index = bisect_right(candle_times, stop_event) - 1
            if stop_index < 0:
                continue
            stopped.append((a_owner, stop_index, stop_event))
            a_owner_identities.add(module_identity(a_owner))

    stop_indices = {
        module_identity(module): stop_index
        for module, stop_index, _stop_event in stopped
    }
    stop_events = {
        module_identity(module): stop_event
        for module, _stop_index, stop_event in stopped
    }

    valid = []
    invalid = []
    consumed = set()
    for a_zone in sorted(
        a_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ),
    ):
        source_index = int(getattr(a_zone, "source_index"))
        eligible = []
        for module, stop_index, _stop_event in stopped:
            identity = module_identity(module)
            if (
                getattr(module, "source_time") >= getattr(a_zone, "source_time")
                or stop_index > source_index
                or identity in consumed
            ):
                continue
            if identity in a_owner_identities:
                # A->A immediate re-entry is defined by chronology, not by a
                # permanent A owner.  If the new A trigger starts only after
                # the previous A strict stop, it belongs to a genuinely new
                # leg and the old A must not block it.  A trigger that starts
                # at/before that stop overlaps the closed A transition and is
                # calculation-invalid.
                trigger_event = getattr(
                    a_zone, "trigger_event_time", getattr(a_zone, "source_time")
                )
                if trigger_event > stop_events[identity]:
                    continue
            eligible.append(module)
        if not eligible:
            valid.append(a_zone)
            continue
        # A historical high-priority E cannot own every later leg forever.
        # The newest main candle containing a strict stop owns the transition;
        # priority and numbering resolve only owners stopped in that candle.
        dominant = max(
            eligible,
            key=lambda item: (
                stop_indices[module_identity(item)],
                module_priority(item),
                int(getattr(item, "number", 0)),
                getattr(item, "source_time"),
                int(getattr(item, "source_index", -1)),
            ),
        )
        crosses_dominant = strictly_beyond_boundary(
            Decimal(str(getattr(a_zone, "price"))),
            Decimal(str(getattr(dominant, "price"))),
            direction,
        )
        if not crosses_dominant:
            valid.append(a_zone)
            continue

        # A confirmed trend Reaction may establish a directional leg head
        # inside the closed owner's range before this A. Preserve that A as an
        # interior-leg behavior, while retaining the existing owner
        # consumption below. This is provenance-based and uses no fixture data.
        interior = False
        if (
            module_identity(dominant) not in a_owner_identities
            and trend_reactions is not None
            and confirmation_finder is not None
            and source_index > 0
            and getattr(a_zone, "reaction_first_time", None) is not None
        ):
            owner_stop = next(
                stop_event for module, stop_index, stop_event in stopped
                if module_identity(module) == module_identity(dominant)
            )
            owner_stop_index = bisect_right(candle_times, owner_stop) - 1
            first_trend_index = bisect_right(
                candle_times, getattr(a_zone, "reaction_first_time")
            ) - 1
            if 0 <= owner_stop_index <= first_trend_index < len(candles):
                extreme_name = "low" if direction == "bullish" else "high"
                head = (
                    min(
                        candles[owner_stop_index:first_trend_index + 1],
                        key=lambda candle: Decimal(str(getattr(candle, extreme_name))),
                    )
                    if direction == "bullish"
                    else max(
                        candles[owner_stop_index:first_trend_index + 1],
                        key=lambda candle: Decimal(str(getattr(candle, extreme_name))),
                    )
                )
                head_extreme = Decimal(str(getattr(head, extreme_name)))
                a_extreme = Decimal(str(getattr(a_zone, "price")))
                if (
                    int(getattr(head, "index", -1)) < source_index
                    and (
                        head_extreme < a_extreme
                        if direction == "bullish"
                        else head_extreme > a_extreme
                    )
                ):
                    interior = any(
                        int(getattr(reaction, "first_idx"))
                        >= int(getattr(head, "index"))
                        and int(getattr(reaction, "first_idx"))
                        <= first_trend_index
                        and int(getattr(reaction, "break_idx")) < source_index
                        and confirmation_finder(reaction, direction)
                        < getattr(a_zone, "source_time")
                        for reaction in trend_reactions
                    )
        if interior:
            valid.append(a_zone)
            # Continue into the common consumption logic below.
            dominant_priority = module_priority(dominant)
            for module in eligible:
                if module_priority(module) <= dominant_priority:
                    consumed.add(module_identity(module))
            continue

        invalid.append(a_zone)
        dominant_priority = module_priority(dominant)
        if hasattr(dominant, "a_source_time"):
            # Stage-order invariant: A -> S -> E -> StopAll.  When S owns the
            # transition, a rejected fallback A cannot consume that S merely
            # by being rejected; otherwise the next A can re-enter behind S
            # and fabricate a second S branch in the same stage.  Keep S as
            # owner until a genuinely later-stage behavior takes ownership.
            if stage_invalid_a_identities is not None:
                stage_invalid_a_identities.add(
                    (getattr(a_zone, "source_time"), int(getattr(a_zone, "source_index")))
                )
            continue
        for module in eligible:
            if module_priority(module) <= dominant_priority:
                consumed.add(module_identity(module))
    return valid, invalid

def blocked_orders_while_invalid_leg_heads_are_live(
    invalid_a_zones, opposite_reactions, candles, direction, stop_finder,
):
    """Return order First times owned by a still-live invalid leg head.

    A strict dominant-boundary crossing can expose a new leg head without
    making its A calculation-valid. Until that head itself stops, an internal
    opposite Reaction cannot take over the larger owner's resumed E space.
    """
    blocked = set()
    for a_zone in invalid_a_zones:
        stop = stop_finder(a_zone)
        if stop is None:
            continue
        stop_event = stop[2]
        source_time = getattr(a_zone, "source_time")
        for reaction in opposite_reactions:
            first_time = getattr(candles[int(getattr(reaction, "first_idx"))], "timestamp")
            if source_time <= first_time < stop_event:
                blocked.add(first_time)
    return blocked


def consumed_s_evidence_after_larger_stop(
    s_candidates, accepted_s_zones, e_zones, direction, stop_event_finder, candles,
):
    """Return the earliest suppressed S evidence that continues each stopped E.

    A lower-priority S remains non-public when it belongs to the continuation
    of the current larger E lifecycle, but its stopped geometry must remain
    available to E.  The parent A must form strictly after the larger E's
    exact stop; an A that straddles that stop belongs to the older handoff and
    cannot advance the E chain.  The source candle must also continue strictly
    beyond the stop-main-candle Close.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    accepted = {
        (getattr(item, "a_source_time"), getattr(item, "source_time"))
        for item in accepted_s_zones
    }
    candle_times = [getattr(item, "timestamp") for item in candles]
    ordered_e = sorted(
        e_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )
    # One suppressed S may be downstream of several historical E objects.
    # Resolve the actual stopped owner at the A leg head, not the most recently
    # *formed* E. A later-formed, smaller E cannot renumber a transition
    # already owned by a larger E stopped in the latest stop-main-candle.
    # Cache exact stop events without changing their lower-timeframe semantics.
    stopped_e = []
    for owner in ordered_e:
        owner_stop = module_stop_event(owner, stop_event_finder)
        if owner_stop is None:
            continue
        stop_index = bisect_right(candle_times, owner_stop) - 1
        if 0 <= stop_index < len(candles):
            stopped_e.append((owner, owner_stop, stop_index))

    earliest_by_owner = {}
    for candidate in sorted(
        s_candidates,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    ):
        identity = (getattr(candidate, "a_source_time"), getattr(candidate, "source_time"))
        if identity in accepted:
            continue
        a_source_time = getattr(candidate, "a_source_time")
        source_index = int(getattr(candidate, "source_index"))
        if not 0 <= source_index < len(candles):
            continue
        source_close = Decimal(str(getattr(candles[source_index], "close")))
        candidate_priority = module_priority(candidate)
        eligible = []
        for owner, owner_stop, stop_index in stopped_e:
            if (
                getattr(owner, "source_time") >= a_source_time
                or owner_stop >= a_source_time
                or candidate_priority >= module_priority(owner)
            ):
                continue
            stop_close = Decimal(str(getattr(candles[stop_index], "close")))
            if not strictly_beyond_boundary(source_close, stop_close, direction):
                continue
            eligible.append((owner, owner_stop, stop_index))
        if not eligible:
            continue
        # The latest accepted E marks the current lifecycle; its formation is
        # not a stop prerequisite for a still-dominant overlapping E.  In
        # particular, a newer *smaller* E cannot prevent a stopped larger E
        # from advancing its own family/number.  An older owner may qualify
        # only if it is strictly higher-ranked and survived beyond the newer
        # E's accepted decision.  Earlier historical stops cannot be revived.
        latest_source = next(
            (item for item in reversed(ordered_e)
             if getattr(item, "source_time") < a_source_time),
            None,
        )
        if latest_source is None:
            continue
        latest_rank = (
            module_priority(latest_source),
            int(getattr(latest_source, "number", 0)),
        )
        latest_qualified = next(
            ((owner, owner_stop, stop_index) for owner, owner_stop, stop_index in eligible
             if owner is latest_source),
            None,
        )
        latest_decision = getattr(
            latest_source, "decision_event_time", latest_source.source_time
        )
        eligible = [
            entry for entry in eligible
            if entry[0] is latest_source
            or (
                (
                    module_priority(entry[0]),
                    int(getattr(entry[0], "number", 0)),
                ) > latest_rank
                and entry[1] > latest_decision
                and (
                    latest_qualified is None
                    or entry[2] >= latest_qualified[2]
                )
            )
        ]
        if not eligible:
            continue
        # Lifecycle ownership first follows the *latest stopped main candle*.
        # Within that boundary use the shared S/E priority and the accepted E
        # number. Neither family priority nor numbering is direction-mirrored.
        owner, _, _ = max(
            eligible,
            key=lambda entry: (
                entry[2],
                module_priority(entry[0]),
                int(getattr(entry[0], "number", 0)),
                getattr(entry[0], "source_time"),
                int(getattr(entry[0], "source_index", -1)),
            ),
        )
        owner_id = module_identity(owner)
        current = earliest_by_owner.get(owner_id)
        if current is None or (
            getattr(candidate, "source_time"), int(getattr(candidate, "source_index", -1))
        ) < (
            getattr(current[0], "source_time"), int(getattr(current[0], "source_index", -1))
        ):
            earliest_by_owner[owner_id] = (candidate, owner)
    return sorted(
        earliest_by_owner.values(),
        key=lambda pair: (
            getattr(pair[0], "source_time"),
            int(getattr(pair[0], "source_index", -1)),
        ),
    )

def s_zones_for_module_engines(s_zones, e_zones, direction):
    """Preserve the established S eligibility contract consumed by E/StopAll."""
    ordered_e = sorted(e_zones, key=lambda item: getattr(item, "source_time"))
    visible = []
    for s_zone in sorted(s_zones, key=lambda item: getattr(item, "source_time")):
        prior_modules = [
            item for item in [*ordered_e, *visible]
            if getattr(item, "source_time") < getattr(s_zone, "source_time")
        ]
        if prior_modules:
            prior = max(prior_modules, key=lambda item: getattr(item, "source_time"))
            # A strictly higher-priority behavior may supersede a lower one;
            # equal or lower priority remains owned by the prior lifecycle.
            # This preserves the original hierarchy contract while allowing
            # Red S to outrank Blue S / Blue E in either market direction.
            if module_priority(s_zone) <= module_priority(prior):
                if getattr(s_zone, "a_source_time") < getattr(prior, "source_time"):
                    continue
                boundary = Decimal(str(getattr(prior, "price")))
                if strictly_beyond_boundary(
                    Decimal(str(getattr(s_zone, "a_price"))), boundary, direction
                ):
                    continue
                if strictly_beyond_boundary(
                    Decimal(str(getattr(s_zone, "price"))), boundary, direction
                ):
                    continue
        visible.append(s_zone)
    return visible

def s_zones_for_stopall(s_zones, e_zones, direction):
    """Return accepted S state that may participate in StopAll grouping.

    E reconciliation still consumes the established S eligibility contract.
    StopAll adds one final same-source rule: when an accepted E owns the same
    physical source as an S candidate, E is final and the losing S must not
    be counted as another sequence member.
    """
    visible = s_zones_for_module_engines(s_zones, e_zones, direction)
    e_sources = {
        (int(getattr(item, "source_index")), getattr(item, "source_time"))
        for item in e_zones
    }
    return [
        item for item in visible
        if (int(getattr(item, "source_index")), getattr(item, "source_time"))
        not in e_sources
    ]

def visible_s_zones_after_module_resets(
    s_zones, e_zones, direction, stop_event_finder=None, source_event_finder=None,
    candles=None,
):
    """Apply dominant-behavior ownership to successive S candidates.

    Bullish/bearish half-leg calculations remain active under a larger
    behavior.  But once the currently dominant S/E/StopAll and the candidate
    S's parent A have both stopped, that A belongs to the next larger module
    lifecycle.  The would-be S is therefore consumed, while its historical
    inputs remain available for chart rendering and audits.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    ordered_external = sorted(
        e_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    )
    visible = []
    consumed = set()
    for s_zone in sorted(
        s_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index", -1)),
        ),
    ):
        a_stop_event = getattr(s_zone, "a_stop_event_time", None)
        ownership_event = a_stop_event
        if direction in {"bullish", "bearish"}:
            # The larger head may stop while the internal S search is open,
            # after A stops but before the candidate's own extreme forms.
            # A later stop after that extreme must not rewrite its ownership.
            ownership_event = (
                source_event_finder(s_zone) if source_event_finder is not None
                else getattr(s_zone, "source_time")
            )
        prior_modules = [
            item for item in [*ordered_external, *visible]
            if getattr(item, "source_time") < getattr(s_zone, "source_time")
            and module_identity(item) not in consumed
        ]
        # A newer E/StopAll source begins the current larger-module lifecycle.
        # Stops belonging to modules sourced before that owner are historical
        # and cannot suppress nested S candidates in the newer lifecycle.
        prior_external = [
            item for item in ordered_external
            if getattr(item, "source_time") < getattr(s_zone, "source_time")
        ]
        if prior_external:
            current_external = max(
                prior_external,
                key=lambda item: (
                    getattr(item, "source_time"),
                    int(getattr(item, "source_index", -1)),
                ),
            )
            lifecycle_start = getattr(current_external, "source_time")
            prior_modules = [
                item for item in prior_modules
                if getattr(item, "source_time") >= lifecycle_start
            ]
        if prior_modules and ownership_event is not None:
            stopped_prior = [
                module for module in prior_modules
                if (
                    module_stop := module_stop_event(module, stop_event_finder)
                ) is not None
                and module_stop <= ownership_event
            ]
            if stopped_prior:
                # A lower-priority S may not re-form inside the next lifecycle
                # of the most recent stopped larger module.  Use the latest
                # stopped E/StopAll owner for this continuation-boundary test;
                # do not let an older, higher-priority historical module steal
                # ownership from the current lifecycle.
                stopped_external = [
                    module for module in stopped_prior
                    if not hasattr(module, "a_source_time")
                ]
                if candles is not None and stopped_external:
                    latest_external = max(
                        stopped_external,
                        key=lambda item: (
                            getattr(item, "source_time"),
                            int(getattr(item, "source_index", -1)),
                        ),
                    )
                    if module_priority(s_zone) < module_priority(latest_external):
                        larger_stop = module_stop_event(
                            latest_external, stop_event_finder
                        )
                        if larger_stop is not None:
                            candle_times = [
                                getattr(candle, "timestamp") for candle in candles
                            ]
                            stop_index = bisect_right(candle_times, larger_stop) - 1
                            source_index = int(getattr(s_zone, "source_index"))
                            if (
                                0 <= stop_index < len(candles)
                                and 0 <= source_index < len(candles)
                            ):
                                stop_close = Decimal(str(
                                    getattr(candles[stop_index], "close")
                                ))
                                source_close = Decimal(str(
                                    getattr(candles[source_index], "close")
                                ))
                                if strictly_beyond_boundary(
                                    source_close, stop_close, direction
                                ):
                                    continue

                # Lifecycle ownership is chronological first.  An old
                # high-priority StopAll/E must not steal the transition from
                # the behavior that stopped most recently before this source.
                # Priority/number only resolve a true same-stop-event tie.
                dominant = max(
                    stopped_prior,
                    key=lambda item: (
                        module_stop_event(item, stop_event_finder),
                        module_priority(item),
                        int(getattr(item, "number", 0)),
                        getattr(item, "source_time"),
                        int(getattr(item, "source_index", -1)),
                    ),
                )
                # A newly confirmed higher-priority S family supersedes a
                # stopped lower-priority owner.  In particular, a Red S must
                # remain visible after a stopped Blue S when its own strict
                # directional extreme is reached.  The existing price/stop
                # consumption rule still applies when the candidate priority
                # is equal or lower, preserving the established lifecycle.
                if (
                    hasattr(s_zone, "a_source_time")
                    and hasattr(dominant, "a_source_time")
                    and module_priority(s_zone) > module_priority(dominant)
                ):
                    visible.append(s_zone)
                    continue
                # A stopped owner advances the lifecycle only when the new S
                # is itself the strict directional extreme of that leg.
                # Equality belongs to the earlier owner and remains valid.
                if not strictly_beyond_boundary(
                    Decimal(str(getattr(s_zone, "price"))),
                    Decimal(str(getattr(dominant, "price"))),
                    direction,
                ):
                    visible.append(s_zone)
                    continue
                # All lower/equal stopped owners involved in this transition
                # leave subsequent calculation ownership together.  The
                # highest-priority object determines the next module number.
                dominant_priority = module_priority(dominant)
                for module in stopped_prior:
                    module_stop = module_stop_event(module, stop_event_finder)
                    if (
                        module_priority(module) <= dominant_priority
                    ):
                        consumed.add(module_identity(module))
                continue
        # An active larger behavior does not disable the independent A/S
        # lifecycle inside the current half-leg.
        visible.append(s_zone)
    return visible

def reconcile_stopall_lifecycle(
    detector, s_zones, e_zones, chronology, direction, timed_step=None
):
    """Freeze StopAll boundaries from the accepted chronological E state.

    StopAll is a hard historical lifecycle boundary.  Once the accepted E/S
    chronology produces a StopAll, future sequence state may not feed back and
    delete or move that already-decided boundary.  The previous global
    fixed-point loop violated that prefix rule: rebuilding E with future reset
    maps could remove an earlier StopAll, then a later pass would recreate it.

    Detect the complete StopAll sequence once from the already reconciled E
    calculation state.  The StopAll detector itself processes events
    chronologically and resets its active sequence whenever a StopAll is
    created, so later StopAll numbers are derived from the hard boundaries in
    the same pass.  Publish the resulting reset map to E for downstream audit
    semantics, but never retroactively rebuild the E prefix from that map.
    """
    measure = timed_step or (lambda _label, work: work())
    visible_s = measure(
        f"Reconcile S visibility - {direction.title()}",
        lambda: s_zones_for_stopall(s_zones, e_zones, direction),
    )
    stopalls = measure(
        f"StopAll - {direction.title()}",
        lambda: detect_stopalls(direction, visible_s, e_zones, chronology),
    )
    detector.sequence_resets = {
        item.source_time: item.number for item in stopalls
    }
    return list(e_zones), stopalls


def visible_a_zones_after_module_boundaries(
    a_zones, s_zones, e_zones, direction, stop_event_finder=None,
):
    """Require A provenance to rebuild after the dominant strict stop.

    A price is deliberately not compared with the old module price.  Reactions
    and Blue Lines remain valid inside every half-leg; only provenance that
    straddles the dominant stop belongs to the closed lifecycle.
    """
    del direction  # Exact-stop ownership is directionally mirrored.
    modules = sorted(
        [*s_zones, *e_zones],
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ),
    )
    valid = []
    for a_zone in sorted(
        a_zones,
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ),
    ):
        stopped_prior = [
            module for module in modules
            if getattr(module, "source_time") <= getattr(a_zone, "source_time")
            and (
                stop_event := module_stop_event(module, stop_event_finder)
            ) is not None
            and stop_event <= getattr(a_zone, "source_time")
        ]
        if stopped_prior:
            dominant = dominant_module(stopped_prior)
            boundary_event = module_stop_event(dominant, stop_event_finder)
            provenance_times = (
                getattr(a_zone, "blue_1_source_time"),
                getattr(a_zone, "blue_2_source_time"),
                getattr(a_zone, "continuation_source_time"),
                getattr(a_zone, "reaction_first_time"),
            )
            if min(provenance_times) < boundary_event:
                continue
        valid.append(a_zone)
    return valid

def reaction_number_is_internal(items, number, identities):
    """Return whether a numbered Reaction resolves to a protected internal owner."""
    if number is None:
        return False
    number = int(number)
    if number < 1 or number > len(items):
        return False
    reaction = items[number - 1]
    return order_identity(
        getattr(reaction, "first_idx"),
        getattr(reaction, "break_idx"),
    ) in identities


def point_is_inside_healthy_reaction(source_time, price, reactions):
    """Return True only for a strict protected Reaction interior.

    First and published box edges are ownership boundaries, so equality and
    the First timestamp itself remain eligible.
    """
    if source_time is None or price is None:
        return False
    value = as_decimal(price)
    for reaction in reactions:
        first = getattr(reaction, "behavior_first_time", None)
        confirmed = getattr(reaction, "behavior_confirmation_time", None)
        if first is None or confirmed is None:
            continue
        if source_time <= first or source_time > confirmed:
            continue
        bottom = as_decimal(getattr(reaction, "behavior_public_box_bottom"))
        top = as_decimal(getattr(reaction, "behavior_public_box_top"))
        if bottom < value < top:
            return True
    return False


def filter_internal_behavior_outputs(
    a_zones,
    s_zones,
    e_zones,
    stopalls,
    opposite_reactions,
    opposite_internal_identities,
    all_behavior_reactions,
):
    """Return calculation-valid outputs without obsolete secondary-Order filtering."""
    del opposite_reactions, opposite_internal_identities, all_behavior_reactions
    return list(a_zones), list(s_zones), list(e_zones), list(stopalls)

def finalize_behavior_visibility(
    a_zones,
    s_zones,
    e_zones,
    stopalls,
    direction,
    invalid_s_identities,
    stop_event_finder,
    source_event_finder,
    candles,
    *,
    all_a_zones=None,
):
    """Resolve the final A/S/E lineage closure after StopAll reconciliation."""
    stopall_source_indices = {int(item.source_index) for item in stopalls}
    final_e_zones = [
        item for item in e_zones
        if int(getattr(item, "source_index")) not in stopall_source_indices
    ]
    e_source_indices = {
        int(getattr(item, "source_index")) for item in final_e_zones
    }
    final_s_zones = visible_s_zones_after_module_resets(
        s_zones,
        [*final_e_zones, *stopalls],
        direction,
        stop_event_finder,
        source_event_finder=source_event_finder,
        candles=candles,
    )

    # Presentation is a lineage closure over accepted calculations. If a final
    # E references an S parent, retain that historical S even if it no longer
    # owns downstream lifecycle calculation.
    referenced_s_sources = {
        getattr(item, "parent_source_time")
        for item in final_e_zones
        if str(getattr(item, "parent_type", "")).upper() == "S"
    }
    final_s_identities = {module_identity(item) for item in final_s_zones}
    final_s_zones.extend(
        item for item in s_zones
        if getattr(item, "source_time") in referenced_s_sources
        and module_identity(item) not in final_s_identities
    )
    final_s_zones.sort(
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        )
    )

    final_a_zones = visible_a_zones_after_module_boundaries(
        a_zones,
        final_s_zones,
        [*final_e_zones, *stopalls],
        direction,
        stop_event_finder,
    )
    referenced_a_sources = {getattr(item, "a_source_time") for item in final_s_zones}
    lineage_a_zones = a_zones if all_a_zones is None else all_a_zones
    final_a_identities = {
        (getattr(item, "source_time"), int(getattr(item, "source_index")))
        for item in final_a_zones
    }
    final_a_zones.extend(
        item for item in lineage_a_zones
        if getattr(item, "source_time") in referenced_a_sources
        and (
            getattr(item, "source_time"), int(getattr(item, "source_index"))
        ) not in final_a_identities
    )
    final_a_zones.sort(
        key=lambda item: (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        )
    )

    occupied = e_source_indices | stopall_source_indices
    final_a_zones = [
        item for item in final_a_zones
        if int(getattr(item, "source_index")) not in occupied
    ]
    final_s_zones = [
        item for item in final_s_zones
        if int(getattr(item, "source_index")) not in occupied
        and (
            getattr(item, "source_time"),
            int(getattr(item, "source_index")),
        ) not in invalid_s_identities
    ]
    return final_e_zones, final_s_zones, final_a_zones


def visible_a_zones(a_zones: Sequence[object], s_zones: Sequence[object]) -> list[object]:
    """Return A objects whose source candle is not occupied by a final S."""
    occupied = {int(getattr(item, "source_index")) for item in s_zones}
    return [
        item for item in a_zones
        if int(getattr(item, "source_index")) not in occupied
    ]
````
<!-- EXACT-SOURCE-END:pipeline/lifecycle_engine.py -->

### 16.11 `pipeline/order_audit_engine.py` — Order / OrderAudit

**SHA-256:** `09cba00c0623ffcce0d7bc3460c1e963c4e2b14fb02a9172cc25dcca8ba9aedc`  
**Bytes:** `75219`  
**LF count:** `1863`

<!-- EXACT-SOURCE-BEGIN:pipeline/order_audit_engine.py -->
````python
"""Central physical Order discovery, reuse, provenance, and audit ownership."""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from typing import Callable, Sequence

from core_utils import as_decimal, order_identity, reaction_identity

ORDER_AUDIT_ENGINE_VERSION = "1.5.1"
ORDER_AUDIT_ENGINE_LAST_MODIFIED = "2026-09-28 19:35:32 +03:30"

@dataclass(frozen=True, slots=True)
class PostBehaviorStop:
    behavior_type: str
    behavior_source_index: int
    behavior_source_time: datetime
    event_time: datetime


@dataclass(frozen=True, slots=True)
class OrderBBehaviorAnchor:
    behavior_type: str
    behavior_source_index: int
    behavior_source_time: datetime
    priority: int
    number: int


@dataclass(frozen=True, slots=True)
class OrderBResetLeg:
    post_stop: PostBehaviorStop
    anchor_behavior_type: str
    anchor_behavior_source_index: int
    anchor_behavior_source_time: datetime
    anchor_behavior_extreme: Decimal
    reset_reaction: object
    reset_confirmation_time: datetime
    reset_source_index: int
    reset_broken_level: Decimal
    reset_time: datetime
    leg_boundary: Decimal
    leg_source_index: int
    leg_source_time: datetime
    strict_break_time: datetime
    reaction_number: int
    physical_reaction: object
    physical_confirmation_time: datetime


def dominant_post_behavior_stops(
    chronology: object,
    lifetimes: Sequence[tuple[str, object, datetime | None]],
    priority: Callable[[object], int],
) -> list[PostBehaviorStop]:
    """Select the accepted lifecycle owner of each stopped main candle."""
    by_candle: dict[int, tuple[tuple[object, ...], PostBehaviorStop]] = {}
    for behavior_type, behavior, event_time in lifetimes:
        if event_time is None:
            continue
        active = [
            item for _type, item, end in lifetimes
            if (
                getattr(item, "trigger_event_time", None)
                or getattr(item, "decision_event_time", None)
                or getattr(item, "source_time")
            ) <= event_time
            and (end is None or event_time <= end)
        ]
        if not active:
            continue
        owner = max(active, key=lambda item: (
            priority(item), int(getattr(item, "number", 0)),
            getattr(item, "source_time"), int(getattr(item, "source_index")),
        ))
        if owner is not behavior:
            continue
        source_time = getattr(behavior, "source_time")
        source_index = int(getattr(behavior, "source_index"))
        stop_index = chronology.main_index(event_time, clamp=True)
        rank = (
            priority(behavior), int(getattr(behavior, "number", 0)),
            source_time, source_index, event_time,
        )
        selected = PostBehaviorStop(
            behavior_type, source_index, source_time, event_time,
        )
        previous = by_candle.get(stop_index)
        if previous is None or rank > previous[0]:
            by_candle[stop_index] = rank, selected
    return sorted(
        (item[1] for item in by_candle.values()),
        key=lambda item: (item.event_time, item.behavior_source_index),
    )


def order_b_reset_event_time(
    direction: str, chronology: object, reset: object,
) -> datetime | None:
    """Resolve a main-candle Reset to its first strict selected-RAW crossing."""
    precise = getattr(reset, "second_time", None)
    if precise:
        return chronology.reset_time(reset)
    reset_index = int(getattr(reset, "index"))
    start = chronology.times[reset_index]
    left = bisect_left(chronology.second_times, start)
    right = bisect_left(chronology.second_times, start + chronology.timeframe)
    level = as_decimal(getattr(reset, "broken_level"))
    if chronology.lower_index is not None:
        crossing = (
            chronology.lower_index.first_less(left, right, level)
            if direction == "bullish" else
            chronology.lower_index.first_greater(left, right, level)
        )
    else:
        attribute = "low" if direction == "bullish" else "high"
        crossing = next((
            index for index in range(left, right)
            if (
                as_decimal(getattr(chronology.seconds[index], attribute)) < level
                if direction == "bullish" else
                as_decimal(getattr(chronology.seconds[index], attribute)) > level
            )
        ), None)
    return None if crossing is None else chronology.second_times[crossing]


def discover_order_b_reset_legs(
    direction: str,
    chronology: object,
    trend_reactions: Sequence[object],
    resets: Sequence[object],
    opposite_reactions: Sequence[object],
    post_stops: Sequence[PostBehaviorStop],
    a_formation_times: Sequence[datetime],
    *,
    behavior_anchors: Sequence[OrderBBehaviorAnchor] = (),
) -> list[OrderBResetLeg]:
    """Find Order_B from post-stop HH/LL reset-leg geometry.

    The stop event opens eligibility, but the geometric anchor is the latest
    accepted behavior that already exists before the Reset Reaction First
    candle, regardless of whether that behavior is dominant.  Bearish uses
    the highest High from the anchor behavior candle through the Reset
    Reaction FirstGreen; Bullish mirrors it with the lowest Low through
    FirstRed.  The boundary must extend strictly beyond the anchor behavior
    candle, the reset Reaction must start strictly after that boundary source,
    and the physical opposite Reaction is the first canonical Reaction whose
    First candle starts at or after the exact strict lower-TF crossing of the
    frozen boundary following Reset, with confirmation strictly after it.
    """
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    if not post_stops or not behavior_anchors:
        return []

    candles = chronology.candles
    lower = chronology.seconds
    lower_times = chronology.second_times
    lower_index = chronology.lower_index
    opposite = chronology.opposite_direction(direction)
    attribute = "low" if direction == "bullish" else "high"

    same_direction = sorted(
        (
            chronology.reaction_confirmation(direction, reaction),
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
            ordinal,
            reaction,
        )
        for ordinal, reaction in enumerate(trend_reactions)
    )
    same_by_first: dict[int, list[tuple[datetime, int, int, int, object]]] = {}
    for item in same_direction:
        same_by_first.setdefault(item[1], []).append(item)

    opposite_direction = sorted(
        (
            chronology.reaction_confirmation(opposite, reaction),
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
            number,
            reaction,
        )
        for number, reaction in enumerate(opposite_reactions, start=1)
    )
    reset_events = sorted(
        (
            event_time,
            int(getattr(reset, "from_first_idx")), ordinal, reset,
        )
        for ordinal, reset in enumerate(resets)
        if (event_time := order_b_reset_event_time(direction, chronology, reset))
        is not None
    )
    stops = sorted(
        post_stops,
        key=lambda item: (
            item.event_time, item.behavior_source_time,
            item.behavior_source_index, item.behavior_type,
        ),
    )
    stop_times = [item.event_time for item in stops]
    anchors = sorted(
        behavior_anchors,
        key=lambda item: (
            item.behavior_source_time, item.behavior_source_index,
            item.priority, item.number, item.behavior_type,
        ),
    )
    anchor_times = [item.behavior_source_time for item in anchors]
    a_times = sorted(a_formation_times)

    found: list[OrderBResetLeg] = []
    for reset_time, reset_first, _ordinal, reset in reset_events:
        current_candidates = [
            item for item in same_by_first.get(reset_first, ())
            if item[0] < reset_time
        ]
        if not current_candidates:
            continue
        current = current_candidates[-1]
        current_first_time = chronology.times[current[1]]

        stop_position = bisect_left(stop_times, current_first_time) - 1
        if stop_position < 0:
            continue
        post_stop = stops[stop_position]

        anchor_position = bisect_left(anchor_times, current_first_time) - 1
        if anchor_position < 0:
            continue
        anchor = anchors[anchor_position]
        if anchor.behavior_source_index > current[1]:
            continue

        anchor_extreme = as_decimal(
            getattr(candles[anchor.behavior_source_index], attribute)
        )
        source_index = anchor.behavior_source_index
        boundary = anchor_extreme
        for index in range(anchor.behavior_source_index + 1, current[1] + 1):
            value = as_decimal(getattr(candles[index], attribute))
            if (value < boundary if direction == "bullish" else value > boundary):
                boundary, source_index = value, index

        extends_anchor = (
            boundary < anchor_extreme
            if direction == "bullish" else boundary > anchor_extreme
        )
        if not extends_anchor:
            continue
        # The Reset Reaction itself must occur after the LL/HH source.
        if source_index >= current[1]:
            continue

        left = bisect_right(lower_times, reset_time)
        right = len(lower_times)
        if left >= right:
            continue
        if lower_index is not None:
            crossing = (
                lower_index.first_less(left, right, boundary)
                if direction == "bullish"
                else lower_index.first_greater(left, right, boundary)
            )
        else:
            crossing = next((
                index for index in range(left, right)
                if (
                    as_decimal(getattr(lower[index], attribute)) < boundary
                    if direction == "bullish" else
                    as_decimal(getattr(lower[index], attribute)) > boundary
                )
            ), None)
        if crossing is None:
            continue
        strict_break_time = lower_times[crossing]

        # A newly formed A is an upstream, Order_B-independent lifecycle
        # boundary.  A reset-leg that was prepared before that A may not stay
        # pending and fire after it; the new A is now the behavior context for
        # subsequent Order logic.  Using A as the hard expiry also keeps the
        # Order_B feedback monotonic because S/E/StopAll may themselves depend
        # on Order_B while A does not.
        next_a_position = bisect_right(a_times, current_first_time)
        if (
            next_a_position < len(a_times)
            and a_times[next_a_position] <= strict_break_time
        ):
            continue

        physical = next((
            item for item in opposite_direction
            if strict_break_time <= chronology.times[item[1]]
            and strict_break_time < item[0]
        ), None)
        if physical is None:
            continue

        found.append(OrderBResetLeg(
            post_stop=post_stop,
            anchor_behavior_type=anchor.behavior_type,
            anchor_behavior_source_index=anchor.behavior_source_index,
            anchor_behavior_source_time=anchor.behavior_source_time,
            anchor_behavior_extreme=anchor_extreme,
            reset_reaction=current[4],
            reset_confirmation_time=current[0],
            reset_source_index=int(getattr(reset, "index")),
            reset_broken_level=as_decimal(getattr(reset, "broken_level")),
            reset_time=reset_time,
            leg_boundary=boundary,
            leg_source_index=source_index,
            leg_source_time=chronology.times[source_index],
            strict_break_time=strict_break_time,
            reaction_number=physical[3],
            physical_reaction=physical[4],
            physical_confirmation_time=physical[0],
        ))
    return found


def discover_accepted_order_b_reset_legs(
    direction: str,
    chronology: object,
    trend_reactions: Sequence[object],
    trend_resets: Sequence[object],
    opposite_reactions: Sequence[object],
    a_zones: Sequence[object],
    invalid_a_identities: set[tuple[datetime, int]],
    s_zones: Sequence[object],
    e_zones: Sequence[object],
    stopalls: Sequence[object],
    s_detector: object,
    e_detector: object,
    priority: Callable[[object], int],
) -> list[OrderBResetLeg]:
    """Build reset legs from calculation-accepted lifecycle owners."""
    accepted_a = [
        item for item in a_zones
        if (getattr(item, "source_time"), int(getattr(item, "source_index")))
        not in invalid_a_identities
    ]
    lifetimes: list[tuple[str, object, datetime | None]] = []
    for item in accepted_a:
        ordinal = int(getattr(item, "reaction_number"))
        confirmation = chronology.reaction_confirmation(
            direction, trend_reactions[ordinal - 1]
        )
        stopped = s_detector.first_a_stop(
            as_decimal(getattr(item, "price")), confirmation
        )
        lifetimes.append(("A", item, stopped[2] if stopped is not None else None))
    for behavior_type, items in (("S", s_zones), ("E", e_zones)):
        for item in items:
            stopped = e_detector.parent_stop(behavior_type, item)
            lifetimes.append((
                behavior_type, item, stopped[1] if stopped is not None else None
            ))
    lifetimes.extend(
        ("StopAll", item, item.stop_event_time)
        for item in stopalls
    )
    dominant = dominant_post_behavior_stops(chronology, lifetimes, priority)

    anchor_candidates: list[OrderBBehaviorAnchor] = []
    for behavior_type, items in (
        ("A", accepted_a), ("S", s_zones), ("E", e_zones),
        ("StopAll", stopalls),
    ):
        for item in items:
            anchor_candidates.append(OrderBBehaviorAnchor(
                behavior_type=behavior_type,
                behavior_source_index=int(getattr(item, "source_index")),
                behavior_source_time=getattr(item, "source_time"),
                priority=priority(item),
                number=int(getattr(item, "number", 0)),
            ))

    # A single source candle may represent several lifecycle projections
    # (for example A/E/StopAll).  The highest lifecycle priority owns only the
    # tie at that exact source; a later lower-priority behavior still becomes
    # the geometric anchor because the rule is explicitly dominant-neutral.
    anchors_by_source: dict[tuple[datetime, int], OrderBBehaviorAnchor] = {}
    for anchor in anchor_candidates:
        key = (anchor.behavior_source_time, anchor.behavior_source_index)
        previous = anchors_by_source.get(key)
        if previous is None or (anchor.priority, anchor.number, anchor.behavior_type) > (
            previous.priority, previous.number, previous.behavior_type
        ):
            anchors_by_source[key] = anchor

    return discover_order_b_reset_legs(
        direction, chronology, trend_reactions, trend_resets,
        opposite_reactions, dominant,
        [item.trigger_event_time for item in accepted_a],
        behavior_anchors=tuple(anchors_by_source.values()),
    )


OrderMatch = tuple[
    int, object, datetime, Decimal, int, datetime,
    tuple[int, datetime, datetime] | None, tuple[str, ...],
    datetime | None,
]


def order_b_leg_identity(items: Sequence[object]) -> tuple[object, ...]:
    """Identify every accepted HH/LL Order_B cause across lifecycle passes."""
    return tuple(sorted((
        leg.post_stop.behavior_type,
        leg.post_stop.behavior_source_index,
        leg.post_stop.event_time,
        leg.anchor_behavior_type,
        leg.anchor_behavior_source_index,
        leg.anchor_behavior_source_time,
        leg.anchor_behavior_extreme,
        int(getattr(leg.reset_reaction, "first_idx")),
        int(getattr(leg.reset_reaction, "break_idx")),
        leg.reset_source_index,
        leg.reset_broken_level,
        leg.reset_time,
        leg.leg_boundary,
        leg.leg_source_index,
        leg.strict_break_time,
        int(getattr(leg.physical_reaction, "first_idx")),
        int(getattr(leg.physical_reaction, "break_idx")),
    ) for leg in items))



class OrderAuditEngineMixin:
    """Order methods shared by the accepted E lifecycle detector."""

    def _order_stop(
        self, number: int, reaction: object, context_start: datetime | None = None,
    ) -> tuple[Decimal, int, datetime]:
        del context_start  # Provenance never manufactures a context-only stop.
        if (
            1 <= number <= len(self.opposite_reactions)
            and self.opposite_reactions[number - 1] is reaction
        ):
            cached = self._canonical_order_stop_cache.get(number)
            if cached is not None:
                return cached
            result = self.chronology.canonical_order_stop(
                self.order_direction,
                number,
                reaction,
                self.opposite_reactions,
                start_index=self.start_index,
            )
            self._canonical_order_stop_cache[number] = result
            return result
        return self.chronology.canonical_order_stop(
            self.order_direction,
            number,
            reaction,
            self.opposite_reactions,
            start_index=self.start_index,
        )


    def order_stop(
        self, reaction_number: int, reaction: object
    ) -> tuple[Decimal, int, datetime]:
        """Public audit API for canonical Order stop provenance."""
        return self._order_stop(reaction_number, reaction)


    def _first_healthy_direct_geometry(
        self, start: datetime, allow_bounded_continue: bool = False,
    ) -> tuple[int, object, datetime] | None:
        """Return the first healthy geometry after an A/S/E strict stop.

        A candidate completes normally when the active prior reaction is not
        Reset before its confirmation. If that prior reaction is Reset first,
        the search restarts strictly after the Reset candle and the first
        complete geometry owns the new leg.
        """
        if self.direct_geometry_finder is None:
            return None
        # Geometry needs its complete context candle at or after the exact
        # stop event. A First candle that already opened before the lower-time-
        # frame stop cannot be attributed to that stop.
        search_index = self._main_index(start)
        search_event = start
        restarted = False
        while search_index <= self.end_index:
            candidate = self.direct_geometry_finder(
                self.order_direction, search_index, self.end_index, search_event
            )
            if candidate is None:
                return None
            first = self._reaction_first_time(candidate)
            if (
                first in self.blocked_order_first_times
                and first == self.times[self._main_index(start)]
            ):
                search_index = int(getattr(candidate, "first_idx")) + 1
                search_event = first
                continue
            confirmation = self._confirmation_for(
                candidate, self.order_direction
            )
            owner_position = bisect_right(
                self._opposite_confirmations, search_event
            ) - 1
            prior = (
                self.opposite_reactions[owner_position]
                if owner_position >= 0 else None
            )
            reset_before_confirmation = None
            if prior is not None:
                for reset_time in self._opposite_reset_times_by_first.get(
                    int(getattr(prior, "first_idx")), []
                ):
                    if search_event < reset_time <= confirmation:
                        reset_before_confirmation = reset_time
                        break
            if reset_before_confirmation is not None:
                search_index = self._main_index(reset_before_confirmation)
                search_event = reset_before_confirmation
                restarted = True
                continue

            identity = (
                int(getattr(candidate, "first_idx")),
                int(getattr(candidate, "break_idx")),
            )
            canonical_position = self._opposite_identity_position.get(identity)
            if canonical_position is None:
                # Order_A is a physical Order and may only be created from a
                # canonical valid Reaction. Gate-bounded geometry can remain
                # internal continuation evidence, but it must never bypass
                # Reaction/Reset ownership and become Order_A. Canonical
                # fallback is handled by `_direct_parent_stop_order`.
                return None
            candidate = self.opposite_reactions[canonical_position]
            number = canonical_position + 1
            confirmation = self._opposite_confirmations[canonical_position]
            return number, candidate, confirmation
        return None


    def _trend_leg_direct_order(
        self, start: datetime,
    ) -> tuple[int, object, datetime] | None:
        """Return bounded direct Order_A after a newly confirmed trend leg.

        A stopped E may be followed by a fresh same-direction Reaction before
        the next opposite public Reaction exists.  That trend confirmation
        establishes the new forming-leg boundary.  The first bounded opposite
        geometry after that exact confirmation may own direct Order_A when the
        shared gate resolver proves ``continue``.  This is direct
        parent-stop Order_A provenance.
        """
        if self.direct_geometry_finder is None:
            return None
        position = bisect_right(self._trend_confirmation_times, start)
        while position < len(self._trend_by_confirmation):
            confirmation, first_time, trend = self._trend_by_confirmation[position]
            position += 1
            if first_time <= start:
                continue
            if bool(getattr(trend, "behavior_internal", False)):
                continue
            break_index = int(getattr(trend, "break_idx"))
            candidate = self.direct_geometry_finder(
                self.order_direction, break_index, self.end_index, confirmation
            )
            if candidate is None:
                continue
            if getattr(candidate, "order_gate_decision", None) != "continue":
                continue
            candidate_confirmation = self._confirmation_for(
                candidate, self.order_direction
            )
            if self._reaction_first_time(candidate) <= confirmation:
                continue
            identity = (
                int(getattr(candidate, "first_idx")),
                int(getattr(candidate, "break_idx")),
            )
            canonical_position = self._opposite_identity_position.get(identity)
            if canonical_position is not None:
                return (
                    canonical_position + 1,
                    self.opposite_reactions[canonical_position],
                    self._opposite_confirmations[canonical_position],
                )
            # A bounded geometry that is absent from the canonical opposite
            # Reaction stream is internal evidence only, not an Order_A.
            continue
        return None


    def _direct_parent_stop_order(
        self,
        start: datetime,
        continuous_deadline: datetime | None,
        allow_bounded_continue: bool,
    ) -> tuple[int, object, datetime] | None:
        """Select the direct parent-stop Order_A."""
        gate_time = self.times[self._main_index(start)]
        geometric_direct = self._first_healthy_direct_geometry(
            start, allow_bounded_continue
        )
        direct_position = bisect_left(self._opposite_first_times, gate_time)
        while (
            direct_position < len(self.opposite_reactions)
            and self._opposite_first_times[direct_position]
            in self.blocked_order_first_times
            and self._opposite_first_times[direct_position] == gate_time
        ):
            direct_position += 1

        independent = None
        if direct_position < len(self.opposite_reactions):
            independent = (
                direct_position + 1,
                self.opposite_reactions[direct_position],
                self._opposite_confirmations[direct_position],
            )
        geometric_gate_decision = (
            getattr(geometric_direct[1], "order_gate_decision", None)
            if geometric_direct is not None
            else None
        )
        prefer_geometric = (
            continuous_deadline is not None
            and geometric_direct is not None
            and geometric_gate_decision == "restart"
            and (
                continuous_deadline == self.range_end
                or continuous_deadline < geometric_direct[2]
            )
        )
        independent_cross = None
        if independent is not None:
            independent_level, _, _ = self._order_stop(
                independent[0], independent[1]
            )
            independent_cross = self._cross_order(
                independent[2], independent_level
            )

        direct_pool: list[tuple[int, object, datetime]] = []
        if prefer_geometric:
            direct_pool.append(geometric_direct)
        elif (
            geometric_direct is not None
            and independent_cross is None
            and (
                independent is None
                or self._reaction_first_time(geometric_direct[1])
                < self._reaction_first_time(independent[1])
            )
        ):
            direct_pool.append(geometric_direct)
        elif independent is not None:
            direct_pool.append(independent)

        if not direct_pool:
            return None
        return min(
            direct_pool,
            key=lambda item: (self._reaction_first_time(item[1]), item[2]),
        )


    def _merge_order_candidate(
        self,
        by_geometry: dict[tuple[int, int], OrderMatch],
        number: int,
        reaction: object,
        confirmation: datetime,
        *,
        parent_stop_cause_time: datetime,
    ) -> OrderMatch:
        """Register one parent-stop Order_A candidate by physical identity."""
        level, source, source_time = self._order_stop(number, reaction)
        crossed = self._cross_order(confirmation, level)
        key = reaction_identity(reaction)
        match: OrderMatch = (
            number,
            reaction,
            confirmation,
            level,
            source,
            source_time,
            crossed,
            ("parent-stop",),
            parent_stop_cause_time,
        )
        existing = by_geometry.get(key)
        if existing is None or (
            confirmation, int(getattr(reaction, "first_idx")), int(getattr(reaction, "break_idx"))
        ) < (
            existing[2], int(getattr(existing[1], "first_idx")), int(getattr(existing[1], "break_idx"))
        ):
            by_geometry[key] = match
        return by_geometry[key]


    def _enforce_single_parent_stop_owner(
        self, by_geometry: dict[tuple[int, int], OrderMatch]
    ) -> None:
        """Keep exactly one physical Order_A for one parent-stop event."""
        parent_candidates = [
            item for item in by_geometry.values() if "parent-stop" in item[7]
        ]
        if len(parent_candidates) <= 1:
            return
        owner = min(
            parent_candidates,
            key=lambda item: (
                item[2], int(getattr(item[1], "first_idx")),
                int(getattr(item[1], "break_idx")),
            ),
        )
        owner_identity = reaction_identity(owner[1])
        for identity, item in list(by_geometry.items()):
            if identity == owner_identity or "parent-stop" not in item[7]:
                continue
            remaining = tuple(cause for cause in item[7] if cause != "parent-stop")
            if remaining:
                by_geometry[identity] = (*item[:7], remaining, None)
            else:
                del by_geometry[identity]


    def order_candidates(
        self,
        start: datetime,
        continuous_deadline: datetime | None = None,
        allow_bounded_continue: bool = False,
        allow_trend_leg_continue: bool = False,
    ) -> list[OrderMatch]:
        """Return physical Order candidates formed before this E decision."""
        cache_key = (
            start,
            continuous_deadline,
            allow_bounded_continue,
            allow_trend_leg_continue,
        )
        cached = self._order_candidates_cache.get(cache_key)
        if cached is not None:
            return list(cached)

        by_geometry: dict[tuple[int, int], OrderMatch] = {}
        direct = self._direct_parent_stop_order(
            start, continuous_deadline, allow_bounded_continue
        )
        if direct is not None:
            self._merge_order_candidate(
                by_geometry,
                *direct,
                parent_stop_cause_time=start,
            )

        if allow_trend_leg_continue:
            trend_direct = self._trend_leg_direct_order(start)
            if trend_direct is not None:
                self._merge_order_candidate(
                    by_geometry,
                    *trend_direct,
                    parent_stop_cause_time=start,
                )

        # Reset-leg provenance is independent of the one-Order-per-parent
        # parent-stop rule, but shares the canonical physical identity.
        for leg in self.order_b_legs:
            reaction = leg.physical_reaction
            if self._reaction_first_time(reaction) <= start:
                continue
            identity = reaction_identity(reaction)
            previous = by_geometry.get(identity)
            if previous is not None:
                by_geometry[identity] = (
                    *previous[:7],
                    tuple(dict.fromkeys((*previous[7], "reset-leg"))),
                    previous[8],
                )
                continue
            level, source, source_time = self._order_stop(
                leg.reaction_number, reaction
            )
            by_geometry[identity] = (
                leg.reaction_number, reaction, leg.physical_confirmation_time,
                level, source, source_time,
                self._cross_order(leg.physical_confirmation_time, level),
                ("reset-leg",), None,
            )

        # One exact parent stop may create only one physical Order_A.
        self._enforce_single_parent_stop_owner(by_geometry)

        stopped = [
            item[6][2]
            for item in by_geometry.values()
            if item[6] is not None
        ]
        decision_deadline = min(stopped) if stopped else self.range_end
        if continuous_deadline is not None:
            decision_deadline = min(decision_deadline, continuous_deadline)
        eligible = [
            item for item in by_geometry.values()
            if item[2] <= decision_deadline
        ]
        result = sorted(
            eligible,
            key=lambda item: (
                item[6][2] if item[6] is not None else self.range_end,
                self._reaction_first_time(item[1]),
            ),
        )
        self._order_candidates_cache[cache_key] = tuple(result)
        return result


    def _first_order(
        self, start: datetime, continuous_deadline: datetime | None = None,
        allow_bounded_continue: bool = False,
        allow_trend_leg_continue: bool = False,
    ) -> OrderMatch | None:
        candidates = [
            item for item in self.order_candidates(
                start, continuous_deadline,
                allow_bounded_continue=allow_bounded_continue,
                allow_trend_leg_continue=allow_trend_leg_continue,
            )
            if item[6] is not None
        ]
        return candidates[0] if candidates else None


    def _has_sequence_reset_between(
        self, start: datetime, end: datetime,
    ) -> bool:
        """Return whether a known hard reset lies in ``(start, end]``."""
        position = bisect_right(self._sequence_reset_times, start)
        return (
            position < len(self._sequence_reset_times)
            and self._sequence_reset_times[position] <= end
        )


    def _index_order_audit_identity(
        self, identity: tuple[int, int], confirmation: datetime,
    ) -> None:
        """Index one newly accepted physical Order by confirmation chronology."""
        first_index, break_index = identity
        item = (confirmation, first_index, break_index)
        position = bisect_right(self._order_audit_confirmation_index, item)
        self._order_audit_confirmation_index.insert(position, item)


    def _clear_order_audit(self) -> None:
        self.order_audit.clear()
        self._order_audit_confirmation_index.clear()
        self._carried_orders_cache.clear()


    def register_order_b_reset_legs(
        self, legs: Sequence[OrderBResetLeg],
    ) -> None:
        """Merge proven reset-leg causes by canonical physical identity."""
        if legs:
            self._carried_orders_cache.clear()
        for leg in legs:
            reaction = leg.physical_reaction
            identity = reaction_identity(reaction)
            entry = self.order_audit.get(identity)
            if entry is None:
                level, source, source_time = self._order_stop(
                    leg.reaction_number, reaction
                )
                entry = {
                    "reaction_number": leg.reaction_number,
                    "reaction": reaction,
                    "confirmation_time": leg.physical_confirmation_time,
                    "stop_level": level,
                    "stop_source_index": source,
                    "stop_source_time": source_time,
                    "stop_cross": self._cross_order(
                        leg.physical_confirmation_time, level
                    ),
                    "causes": set(),
                }
                self.order_audit[identity] = entry
                self._index_order_audit_identity(
                    identity, leg.physical_confirmation_time
                )
            current = leg.reset_reaction
            cause = {
                "kind": "reset-leg",
                "postBehaviorType": leg.post_stop.behavior_type,
                "postBehaviorStopTime": leg.post_stop.event_time,
                "postBehaviorSourceIndex": leg.post_stop.behavior_source_index,
                "postBehaviorSourceTime": leg.post_stop.behavior_source_time,
                "anchorBehaviorType": leg.anchor_behavior_type,
                "anchorBehaviorSourceIndex": leg.anchor_behavior_source_index,
                "anchorBehaviorSourceTime": leg.anchor_behavior_source_time,
                "anchorBehaviorExtreme": str(leg.anchor_behavior_extreme),
                "resetReactionIdentity": [
                    int(getattr(current, "first_idx")),
                    int(getattr(current, "break_idx")),
                ],
                "resetReactionBreakoutTime": self.times[int(getattr(current, "break_idx"))],
                "resetReactionConfirmationTime": leg.reset_confirmation_time,
                "resetIndex": leg.reset_source_index,
                "resetBrokenLevel": str(leg.reset_broken_level),
                "resetTime": leg.reset_time,
                "legBoundary": str(leg.leg_boundary),
                "legBoundarySourceIndex": leg.leg_source_index,
                "legBoundarySourceTime": leg.leg_source_time,
                "strictBreakTime": leg.strict_break_time,
                "physicalOrderIdentity": [identity[0], identity[1]],
                "physicalOrderConfirmationTime": leg.physical_confirmation_time,
            }
            causes = entry.setdefault("order_b_causes", [])
            if cause not in causes:
                causes.append(cause)
                causes.sort(key=lambda item: (
                    item["postBehaviorStopTime"], item["resetTime"],
                    item["strictBreakTime"], item["physicalOrderIdentity"],
                ))


    def _register_order_audit(
        self, parent_type: str, parent: object, parent_stop: datetime,
    ) -> None:
        """Register only the physical Order_A created by this parent stop."""
        if parent_type == "S" and (
            parent.source_time, int(parent.source_index)
        ) in self.invalid_s_root_identities:
            return
        if self._has_sequence_reset_between(parent.source_time, parent_stop):
            return
        matches = self.order_candidates(
            parent_stop,
            None,
            allow_bounded_continue=(parent_type == "S"),
            allow_trend_leg_continue=(parent_type == "E"),
        )
        direct = self._direct_parent_stop_order(
            parent_stop, None, allow_bounded_continue=(parent_type == "S")
        )
        if direct is not None:
            direct_identity = reaction_identity(direct[1])
            if all(reaction_identity(item[1]) != direct_identity for item in matches):
                level, source, source_time = self._order_stop(direct[0], direct[1])
                matches.append((
                    direct[0], direct[1], direct[2], level, source, source_time,
                    self._cross_order(direct[2], level), ("parent-stop",),
                    parent_stop,
                ))

        self._carried_orders_cache.clear()
        for match in matches:
            number, reaction, confirmation, level, source, source_time = match[:6]
            crossed, causes = match[6], match[7]
            if "parent-stop" not in causes:
                continue
            key = reaction_identity(reaction)
            entry = self.order_audit.get(key)
            if entry is None:
                entry = {
                    "reaction_number": number,
                    "reaction": reaction,
                    "confirmation_time": confirmation,
                    "stop_level": level,
                    "stop_source_index": source,
                    "stop_source_time": source_time,
                    "stop_cross": crossed,
                    "causes": set(),
                }
                self.order_audit[key] = entry
                self._index_order_audit_identity(key, confirmation)
            audit_causes = entry["causes"]
            assert isinstance(audit_causes, set)
            family = str(getattr(parent, "color", getattr(parent, "family", "")))
            number_value = getattr(parent, "number", None)
            parent_label = parent_type
            if parent_type == "E" and number_value is not None:
                parent_label = f"E{number_value}"
            if parent.source_time in self.sequence_resets:
                parent_label = f"StopAll{self.sequence_resets[parent.source_time]}"
                family = ""
            audit_causes.add((
                "parent-stop", parent_label, family, parent_stop,
                getattr(parent, "source_time"),
            ))


    @staticmethod
    def visual_order_lifecycle(
        self, start: datetime,
    ) -> list[tuple[int, object, datetime, Decimal, int, datetime,
                    tuple[int, datetime, datetime] | None, bool]]:
        """Return the first parent-stop Order_A lifecycle after ``start``."""
        position = bisect_left(self._opposite_first_times, start)
        for order_position in range(position, len(self.opposite_reactions)):
            reaction = self.opposite_reactions[order_position]
            first = self._opposite_first_times[order_position]
            confirmation = self._opposite_confirmations[order_position]
            if first < start or confirmation < start:
                continue
            number = order_position + 1
            level, source, source_time = self._order_stop(number, reaction)
            crossed = self._cross_order(confirmation, level)
            return [(
                number, reaction, confirmation, level, source, source_time,
                crossed, False,
            )]
        return []


    def _cross_order(
        self, start: datetime, level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        cache_key = (start, level)
        if cache_key in self._cross_order_cache:
            return self._cross_order_cache[cache_key]
        left = bisect_left(self.lower_times, max(start, self.range_start))
        right = bisect_left(self.lower_times, self.range_end)
        position = self._first_cross_position(
            left, right, level, less=self.order_direction != "bearish"
        )
        if position is None:
            self._cross_order_cache[cache_key] = None
            return None
        event = self.lower_times[position]
        index = self._main_index(event)
        result = index, getattr(self.candles[index], "timestamp"), event
        self._cross_order_cache[cache_key] = result
        return result


    def cross_order(
        self, confirmation_time: datetime, stop_level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        """Public audit API for an Order stop crossing."""
        return self._cross_order(confirmation_time, stop_level)


    def _unconsumed_s_orders(
        self, parent: object, parent_stop: datetime
    ) -> list[OrderMatch]:
        """Return the carried A-owned Order whose stop did not decide S."""
        if (
            str(getattr(parent, "color")) != "blue"
            or getattr(parent, "order_confirmation_time", None) is None
            or getattr(parent, "order_stop_level", None) is None
        ):
            return []
        confirmation = getattr(parent, "order_confirmation_time")
        stop_level = as_decimal(getattr(parent, "order_stop_level"))
        crossed = self._cross_order(confirmation, stop_level)
        if crossed is None or crossed[2] < parent_stop:
            return []
        reaction = SimpleNamespace(
            mode=getattr(parent, "order_mode"),
            first_idx=getattr(parent, "order_first_index"),
            break_idx=getattr(parent, "order_break_index"),
            box_top=getattr(parent, "order_box_top"),
            box_top_source_idx=getattr(parent, "order_box_top_source_index"),
            box_bottom=getattr(parent, "order_box_bottom"),
            box_bottom_source_idx=getattr(parent, "order_box_bottom_source_index"),
        )
        return [(
            int(getattr(parent, "order_reaction_number")),
            reaction,
            confirmation,
            stop_level,
            int(getattr(parent, "order_stop_source_index")),
            getattr(parent, "order_stop_source_time"),
            crossed,
            ("carried-live",),
            None,
        )]


    def _initial_order_records(self) -> tuple[tuple[
        datetime, datetime, int, object, Decimal, int, datetime,
        tuple[int, datetime, datetime] | None,
    ], ...]:
        """Materialize immutable initial OrderAudit geometry once per run.

        Algorithm requirement: physical Order identity and exact strict stop
        chronology remain unchanged. Performance detail: the prior code
        recomputed ``_cross_order`` while rescanning this immutable ledger for
        every E parent. The precomputed records only remove repeated pure work.
        """
        cached = self._initial_order_records_cache
        if cached is not None:
            return cached

        records: list[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ]] = []
        for entry in self.initial_order_audit.values():
            reaction = entry["reaction"]
            first = self._reaction_first_time(reaction)
            confirmation = entry["confirmation_time"]
            level = as_decimal(entry["stop_level"])
            crossed = self._cross_order(confirmation, level)
            records.append((
                first, confirmation, int(entry["reaction_number"]), reaction,
                level, int(entry["stop_source_index"]),
                entry["stop_source_time"], crossed,
            ))

        records.sort(key=lambda item: (item[0], item[1], int(getattr(item[3], "first_idx")), int(getattr(item[3], "break_idx"))))
        cached = tuple(records)
        self._initial_order_records_cache = cached
        self._initial_order_first_times = [item[0] for item in cached]

        by_first: dict[datetime, list[tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ]]] = {}
        for item in cached:
            by_first.setdefault(item[0], []).append(item)
        self._initial_orders_by_first_time = {
            key: tuple(value) for key, value in by_first.items()
        }

        # A separate confirmation-sorted view supports the post-stop route.
        # The record objects are reused; no duplicate Order representation is
        # constructed.
        confirmation_sorted = sorted(
            cached,
            key=lambda item: (item[1], item[0], int(getattr(item[3], "first_idx")), int(getattr(item[3], "break_idx"))),
        )
        self._initial_order_confirmation_records = tuple(confirmation_sorted)
        self._initial_order_confirmation_times = [item[1] for item in confirmation_sorted]
        return cached


    @staticmethod
    @staticmethod
    def _initial_record_match(
        record: tuple[
            datetime, datetime, int, object, Decimal, int, datetime,
            tuple[int, datetime, datetime] | None,
        ],
        causes: tuple[str, ...],
    ) -> OrderMatch:
        _first, confirmation, number, reaction, level, source_index, source_time, crossed = record
        return (
            number, reaction, confirmation, level, source_index, source_time,
            crossed, causes, None,
        )


    def _initial_order_match(
        self, entry: dict[str, object], causes: tuple[str, ...],
    ) -> OrderMatch:
        """Return one immutable A-owned Order_A audit entry as an OrderMatch."""
        reaction = entry["reaction"]
        confirmation = entry["confirmation_time"]
        level = as_decimal(entry["stop_level"])
        crossed = self._cross_order(confirmation, level)
        return (
            int(entry["reaction_number"]), reaction, confirmation, level,
            int(entry["stop_source_index"]), entry["stop_source_time"],
            crossed, causes, None,
        )


    def _gate_owned_initial_order(
        self, parent_stop: datetime,
    ) -> OrderMatch | None:
        """Keep an A-owned order that starts in the parent-stop candle."""
        gate_time = self.times[self._main_index(parent_stop)]
        self._initial_order_records()
        assert self._initial_orders_by_first_time is not None
        matches: list[OrderMatch] = []
        for record in self._initial_orders_by_first_time.get(gate_time, ()):
            confirmation = record[1]
            if confirmation < parent_stop:
                continue
            crossed = record[7]
            if crossed is None or crossed[2] < parent_stop:
                continue
            matches.append(self._initial_record_match(record, ("carried-live",)))
        return min(
            matches,
            key=lambda item: (item[6][2], self._reaction_first_time(item[1])),
            default=None,
        )


    def _carried_orders_for_parent(
        self, parent: object, parent_stop: datetime,
    ) -> list[OrderMatch]:
        """Return accepted Order identities created and left live in this lifecycle."""
        lifecycle_start = getattr(parent, "decision_event_time", None)
        if lifecycle_start is None:
            return []
        key = lifecycle_start, parent_stop
        cached = self._carried_orders_cache.get(key)
        if cached is not None:
            return list(cached)
        matches: list[OrderMatch] = []
        for entry in self.order_audit.values():
            a_created_events = [
                cause[3]
                for cause in entry.get("causes", set())
                if cause[0] == "parent-stop"
            ]
            created_events = [min(a_created_events)] if a_created_events else []
            created_events.extend(
                cause["physicalOrderConfirmationTime"]
                for cause in entry.get("order_b_causes", ())
            )
            if not created_events:
                continue
            confirmation = entry["confirmation_time"]
            crossed = entry.get("stop_cross")
            if (
                not any(lifecycle_start < created < parent_stop for created in created_events)
                or confirmation > parent_stop
                or crossed is None
                or crossed[2] < parent_stop
            ):
                continue
            reaction = entry["reaction"]
            matches.append((
                int(entry["reaction_number"]), reaction, confirmation,
                as_decimal(entry["stop_level"]), int(entry["stop_source_index"]),
                entry["stop_source_time"], crossed, ("carried-live",), None,
            ))

        records = self._initial_order_records()
        assert self._initial_order_first_times is not None
        left = bisect_left(self._initial_order_first_times, lifecycle_start)
        right = bisect_right(self._initial_order_first_times, parent_stop)
        for record in records[left:right]:
            confirmation = record[1]
            if confirmation > parent_stop:
                continue
            crossed = record[7]
            if crossed is None or crossed[2] < parent_stop:
                continue
            matches.append(self._initial_record_match(record, ("carried-live",)))
        result = sorted(
            matches,
            key=lambda item: (item[6][2], -int(getattr(item[1], "first_idx"))),
        )
        self._carried_orders_cache[key] = tuple(result)
        return result


    def _post_stop_accepted_orders_for_parent(
        self, parent: object, parent_stop: datetime,
    ) -> list[OrderMatch]:
        """Return accepted physical Orders confirmed after this parent stop."""
        del parent
        matches_by_identity: dict[tuple[int, int], OrderMatch] = {}

        def add_match(match: OrderMatch) -> None:
            crossed = match[6]
            if crossed is None or crossed[2] <= parent_stop or crossed[2] <= match[2]:
                return
            if self._has_sequence_reset_between(parent_stop, crossed[2]):
                return
            identity = reaction_identity(match[1])
            current = matches_by_identity.get(identity)
            if current is None or (
                crossed[2], match[2], int(getattr(match[1], "first_idx"))
            ) < (
                current[6][2], current[2], int(getattr(current[1], "first_idx"))
            ):
                matches_by_identity[identity] = match

        self._initial_order_records()
        assert self._initial_order_confirmation_times is not None
        confirmation_records = self._initial_order_confirmation_records
        start = bisect_right(self._initial_order_confirmation_times, parent_stop)
        for record in confirmation_records[start:]:
            add_match(self._initial_record_match(record, ("accepted-live",)))

        audit_position = bisect_right(
            self._order_audit_confirmation_index,
            (parent_stop, 2**63 - 1, 2**63 - 1),
        )
        for _confirmation, first_index, break_index in (
            self._order_audit_confirmation_index[audit_position:]
        ):
            entry = self.order_audit.get((first_index, break_index))
            if entry is None:
                continue
            reaction = entry.get("reaction")
            confirmation = entry.get("confirmation_time")
            if reaction is None or not isinstance(confirmation, datetime):
                continue
            level_value = entry.get("stop_level")
            source_index = entry.get("stop_source_index")
            source_time = entry.get("stop_source_time")
            if level_value is None or source_index is None or source_time is None:
                continue
            crossed = entry.get("stop_cross")
            if not (
                isinstance(crossed, tuple)
                and len(crossed) >= 3
                and isinstance(crossed[2], datetime)
            ):
                crossed = self._cross_order(confirmation, as_decimal(level_value))
            add_match((
                int(entry.get("reaction_number", 0)), reaction, confirmation,
                as_decimal(level_value), int(source_index), source_time, crossed,
                ("accepted-live",), None,
            ))

        return sorted(
            matches_by_identity.values(),
            key=lambda item: (
                item[6][2], item[2], -int(getattr(item[1], "first_idx")),
            ),
        )


    def _blocked_by_gate_owned_order(self, zone: EZone) -> bool:
        """Reject a nested parent-stop Order_A when the gate-owned A Order wins."""
        if "parent-stop" not in zone.order_causes:
            return False
        gate_owned = self._gate_owned_initial_order(zone.parent_stop_event_time)
        return (
            gate_owned is not None
            and gate_owned[2] < zone.order_first_time
        )


    def _rebuild_accepted_order_audit(
        self, numbered: list[EZone], supplemental_s_zones: Sequence[object] = (),
    ) -> list[EZone]:
        """Rebuild accepted parent-stop and reset-leg physical provenance."""
        invalid_s_source_times = {
            source_time
            for source_time, _source_index in getattr(
                self, "invalid_s_root_identities", set()
            )
        }

        def valid_parent_stop_cause(cause: tuple[object, ...]) -> bool:
            if not cause or cause[0] != "parent-stop":
                return False
            # Suppressed/invalid S evidence may remain available internally for
            # E continuation geometry, but it never became an accepted S
            # behavior and therefore cannot create a physical parent-stop
            # Order_A.  Valid historical/non-public accepted S behaviors are
            # unaffected because only explicitly invalid S identities are
            # rejected here.
            return not (
                cause[1] == "S"
                and len(cause) > 4
                and cause[4] in invalid_s_source_times
            )

        prior_order_audit = {
            identity: {
                **entry,
                "causes": {
                    cause for cause in entry.get("causes", set())
                    if valid_parent_stop_cause(cause)
                },
            }
            for identity, entry in self.order_audit.items()
        }
        self._clear_order_audit()
        self.register_order_b_reset_legs(self.order_b_legs)
        accepted_parents: list[tuple[str, object]] = [
            ("S", item) for item in self.s_zones
        ] + [("StopAll" if item.source_time in self.sequence_resets else "E", item)
             for item in numbered]
        for parent_type, parent in accepted_parents:
            stop = self._parent_stop(parent_type, parent)
            if stop is None:
                continue
            self._register_order_audit(parent_type, parent, stop[1])

        # Carried-live and accepted-live are use routes, not creation causes.
        # Preserve the original parent-stop Order_A provenance when final
        # reconciliation keeps a physical Order whose creating parent is no
        # longer a public behavior.
        for zone in numbered:
            identity = order_identity(zone.order_first_index, zone.order_break_index)
            if identity in self.order_audit:
                continue

            prior_entry = prior_order_audit.get(identity)
            reaction = self._opposite_by_first_index.get(zone.order_first_index)
            if (
                reaction is None
                or int(getattr(reaction, "break_idx", -1)) != zone.order_break_index
            ):
                reaction = SimpleNamespace(
                    mode=zone.order_mode,
                    first_idx=zone.order_first_index,
                    break_idx=zone.order_break_index,
                    box_top=zone.order_box_top,
                    box_top_source_idx=zone.order_box_top_source_index,
                    box_top_source_time=zone.order_box_top_source_time,
                    box_bottom=zone.order_box_bottom,
                    box_bottom_source_idx=zone.order_box_bottom_source_index,
                    box_bottom_source_time=zone.order_box_bottom_source_time,
                    behavior_internal=False,
                )

            causes: set[tuple[object, ...]] = set()
            if prior_entry is not None:
                causes.update(
                    cause for cause in prior_entry.get("causes", set())
                    if cause and cause[0] == "parent-stop"
                )

            initial_entry = self.initial_order_audit.get(identity)
            if initial_entry is not None:
                a_causes = initial_entry.get("a_causes") or [(
                    initial_entry.get("a_source_time"),
                    initial_entry.get("a_stop_event_time"),
                )]
                for a_source_time, a_stop_time in a_causes:
                    if a_source_time is None or a_stop_time is None:
                        continue
                    causes.add((
                        "parent-stop", "A", None, a_stop_time, a_source_time
                    ))

            if (
                not causes
                and "carried-live" in zone.order_causes
                and zone.parent_type == "S"
            ):
                parent_s = next((
                    item for item in [*self.s_zones, *supplemental_s_zones]
                    if int(getattr(item, "source_index")) == zone.parent_source_index
                    and getattr(item, "source_time") == zone.parent_source_time
                    and getattr(item, "order_first_index", None) == zone.order_first_index
                    and getattr(item, "order_break_index", None) == zone.order_break_index
                ), None)
                if parent_s is not None:
                    causes.add((
                        "parent-stop",
                        "A",
                        None,
                        getattr(parent_s, "a_stop_event_time"),
                        getattr(parent_s, "a_source_time"),
                    ))

            if zone.order_parent_stop_cause_time is not None:
                parent_label = zone.parent_type
                if zone.parent_type == "E":
                    parent_zone = next((
                        item for item in numbered
                        if item.source_index == zone.parent_source_index
                        and item.source_time == zone.parent_source_time
                    ), None)
                    if parent_zone is not None:
                        parent_label = f"E{parent_zone.number}"
                if zone.parent_source_time in self.sequence_resets:
                    parent_label = f"StopAll{self.sequence_resets[zone.parent_source_time]}"
                causes.add((
                    "parent-stop",
                    parent_label,
                    "" if zone.parent_source_time in self.sequence_resets else zone.family,
                    zone.parent_stop_event_time,
                    zone.parent_source_time,
                ))

            causes = {cause for cause in causes if valid_parent_stop_cause(cause)}
            if not causes:
                continue

            exact_cross = self._cross_order(
                zone.order_confirmation_time, as_decimal(zone.order_stop_level)
            )
            self.order_audit[identity] = {
                "reaction_number": zone.order_reaction_number,
                "reaction": reaction,
                "confirmation_time": zone.order_confirmation_time,
                "stop_level": zone.order_stop_level,
                "stop_source_index": zone.order_stop_source_index,
                "stop_source_time": zone.order_stop_source_time,
                "stop_cross": exact_cross,
                "causes": causes,
            }
            self._index_order_audit_identity(identity, zone.order_confirmation_time)

        # Order_A retention invariant: once a valid parent-stop physical Order
        # has entered the canonical ledger, later lifecycle reconciliation may
        # change who consumes it but must never delete its identity/provenance.
        for identity, prior_entry in prior_order_audit.items():
            prior_causes = {
                cause for cause in prior_entry.get("causes", set())
                if valid_parent_stop_cause(cause)
            }
            if not prior_causes:
                continue
            current = self.order_audit.get(identity)
            if current is not None:
                current_causes = current.setdefault("causes", set())
                assert isinstance(current_causes, set)
                current_causes.update(prior_causes)
                continue
            restored = {**prior_entry, "causes": set(prior_causes)}
            self.order_audit[identity] = restored
            self._index_order_audit_identity(
                identity, restored["confirmation_time"]
            )

        return sorted(
            numbered,
            key=lambda item: (item.source_time, item.source_index),
        )


    def rebuild_accepted_order_audit(
        self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object] = (),
    ) -> list[EZone]:
        """Rebuild the canonical Order ledger after external E reconciliation.

        The pipeline may replace a final E branch with an earlier continuation
        built from consumed S evidence after ``detect()`` has completed.  That
        accepted branch must become authoritative for OrderAudit as well;
        the Order module keeps provenance out of the bridge projection.
        """
        return self._rebuild_accepted_order_audit(
            list(zones), supplemental_s_zones=supplemental_s_zones
        )


    def ensure_accepted_order_audit(
        self, zones: Sequence[EZone], supplemental_s_zones: Sequence[object] = (),
    ) -> list[EZone]:
        """Add audit coverage for externally restored accepted E zones.

        Visibility may restore an independent S-owned E root after StopAll
        reconciliation.  Rebuilding from only that post-StopAll E list would
        incorrectly discard physical Orders still needed by already-created
        StopAll/history, so rebuild the accepted subset and then merge back any
        previously canonical identities that were not superseded.
        """
        preserved = {
            identity: {**entry, "causes": set(entry.get("causes", set()))}
            for identity, entry in self.order_audit.items()
        }
        rebuilt = self._rebuild_accepted_order_audit(
            list(zones), supplemental_s_zones=supplemental_s_zones
        )
        for identity, entry in preserved.items():
            self.order_audit.setdefault(identity, entry)
        self._carried_orders_cache.clear()
        return rebuilt


def prepare_order_audit(
    detector,
    start_index: int,
    end_index: int,
    s_detector=None,
    accepted_a_sources: set[datetime] | None = None,
    required_identities: set[tuple[int, int]] | None = None,
):
    """Resolve final Order_A and Order_B identities before serialization."""
    combined: list[tuple[dict[str, object], list[dict[str, object]]]] = []
    required_identities = set(required_identities or set())

    if s_detector is not None:
        for entry in s_detector.order_audit.values():
            a_causes = entry.get("a_causes") or [(
                entry["a_source_time"], entry["a_stop_event_time"]
            )]
            if accepted_a_sources is not None:
                a_causes = [
                    cause for cause in a_causes
                    if cause[0] in accepted_a_sources
                ]
            if not a_causes:
                continue
            combined.append((entry, [
                {
                    "kind": "parent-stop",
                    "parentType": "A",
                    "parentFamily": None,
                    "eventTime": stop_time,
                    "parentSourceTime": source_time,
                }
                for source_time, stop_time in a_causes
            ]))

    for entry in detector.order_audit.values():
        causes = [
            {
                "kind": "parent-stop",
                "parentType": cause[1],
                "parentFamily": cause[2],
                "eventTime": cause[3],
                "parentSourceTime": cause[4],
            }
            for cause in sorted(entry["causes"], key=str)
            if cause[0] == "parent-stop"
        ]
        causes.extend(entry.get("order_b_causes", ()))
        if causes:
            combined.append((entry, causes))

    merged: dict[tuple[int, int], dict[str, object]] = {}
    output: list[dict[str, object]] = []
    for entry, supplied_causes in combined:
        reaction = entry["reaction"]
        first_index = int(getattr(reaction, "first_idx"))
        identity = order_identity(first_index, getattr(reaction, "break_idx"))
        if (
            not start_index <= first_index <= end_index
            and identity not in required_identities
        ):
            continue
        existing = merged.get(identity)
        if existing is not None:
            existing_causes = existing["causes"]
            existing_causes.extend(
                cause for cause in supplied_causes
                if cause not in existing_causes
            )
            continue
        crossed = entry.get("stop_cross")
        if "stop_cross" not in entry:
            crossed = detector.cross_order(
                entry["confirmation_time"], entry["stop_level"]
            )
        prepared = {
            "entry": entry,
            "reaction": reaction,
            "causes": list(supplied_causes),
            "crossed": crossed,
        }
        merged[identity] = prepared
        output.append(prepared)

    # One exact parent-stop event creates one physical Order_A.
    parent_owner: dict[tuple[object, object, object, object], dict[str, object]] = {}
    parent_rank: dict[tuple[object, object, object, object], tuple[object, int, int]] = {}
    for item in output:
        reaction = item["reaction"]
        rank = (
            item["entry"]["confirmation_time"],
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
        )
        for cause in item["causes"]:
            if cause.get("kind") != "parent-stop":
                continue
            key = (
                cause.get("parentType"),
                cause.get("parentFamily"),
                cause.get("eventTime"),
                cause.get("parentSourceTime"),
            )
            previous = parent_rank.get(key)
            if previous is None or rank < previous:
                parent_rank[key] = rank
                parent_owner[key] = item

    deduped_output: list[dict[str, object]] = []
    for item in output:
        accepted_causes = []
        for cause in item["causes"]:
            if cause.get("kind") != "parent-stop":
                accepted_causes.append(cause)
                continue
            key = (
                cause.get("parentType"),
                cause.get("parentFamily"),
                cause.get("eventTime"),
                cause.get("parentSourceTime"),
            )
            if parent_owner.get(key) is item:
                accepted_causes.append(cause)
        if accepted_causes:
            item["causes"] = accepted_causes
            deduped_output.append(item)
    return deduped_output


def accepted_audit_entry(
    entry: dict[str, object], accepted_sources: set
) -> dict[str, object] | None:
    """Return an E-facing A audit entry for one accepted A provenance.

    A physical order may be opened by more than one stopped A.  E still
    consumes one identity-keyed entry, so select the first accepted cause
    while retaining the complete cause list for presentation serialization.
    """
    causes = entry.get("a_causes") or [
        (entry["a_source_time"], entry["a_stop_event_time"])
    ]
    selected = next(
        ((source_time, stop_time) for source_time, stop_time in causes
         if source_time in accepted_sources),
        None,
    )
    if selected is None:
        return None
    if (
        selected[0] == entry.get("a_source_time")
        and selected[1] == entry.get("a_stop_event_time")
    ):
        return entry
    adjusted = dict(entry)
    adjusted["a_source_time"] = selected[0]
    adjusted["a_stop_event_time"] = selected[1]
    return adjusted


def order_identity_is_internal(item, internal_identities):
    """Return whether a behavior's physical Order Reaction is internal."""
    first_index = getattr(item, "order_first_index", None)
    break_index = getattr(item, "order_break_index", None)
    if first_index is None or break_index is None:
        return False
    return order_identity(first_index, break_index) in internal_identities


class SOrderAuditMixin:
    """Physical Order_A and shared Order stop operations for S."""

    def _first_order_after(
        self, a_stop_event_time: datetime
    ) -> tuple[int, object, datetime] | None:
        """Return the immutable first canonical opposite Order after A-stop.

        Each stopped A creates at most one parent-stop Order_A.  Subsequent
        native Mode-B Reactions cannot refresh that physical identity; they
        may be accepted only through independently valid creation causes.
        """
        matches = self._order_matches_after(a_stop_event_time)
        return matches[0] if matches else None


    def _order_matches_after(
        self, a_stop_event_time: datetime
    ) -> list[tuple[int, object, datetime]]:
        """Expose canonical opposite-Order chronology without changing ownership."""
        cached = self._order_matches_after_cache.get(a_stop_event_time)
        if cached is not None:
            return list(cached)

        gate_index = self._main_index(a_stop_event_time)
        position = bisect_right(
            self._opposite_order_confirmation_times, a_stop_event_time
        )
        matches = tuple(
            (number, reaction, confirmation)
            for confirmation, first_index, _break, number, reaction
            in self._opposite_order_matches[position:]
            if first_index >= gate_index
        )
        self._order_matches_after_cache[a_stop_event_time] = matches
        return list(matches)


    def _record_a_order_audit(
        self,
        zone: object,
        a_stop_event_time: datetime,
        order_match: tuple[int, object, datetime],
    ) -> None:
        """Attach one stopped-A creation cause to a physical Order identity."""
        source_time = getattr(zone, "source_time")
        order_number, order, order_confirmation_time = order_match
        (
            order_stop_level,
            order_stop_source_index,
            order_stop_source_time,
        ) = self._order_stop(order_number, order)
        identity = reaction_identity(order)
        cause = (source_time, a_stop_event_time)
        entry = self.order_audit.get(identity)
        if entry is None:
            entry = {
                "reaction_number": order_number,
                "reaction": order,
                "confirmation_time": order_confirmation_time,
                "stop_level": order_stop_level,
                "stop_source_index": order_stop_source_index,
                "stop_source_time": order_stop_source_time,
                "a_source_time": source_time,
                "a_stop_event_time": a_stop_event_time,
                "a_causes": [],
            }
            self.order_audit[identity] = entry
        a_causes = entry.setdefault("a_causes", [])
        if cause not in a_causes:
            a_causes.append(cause)


    def _audit_stopped_a(self, zone: object) -> None:
        """Record the independent physical Order created by one stopped A."""
        a_price = as_decimal(getattr(zone, "price"))
        a_stop = self._first_a_stop(a_price, self._a_confirmation_time(zone))
        if a_stop is None:
            return
        _, _, a_stop_event_time = a_stop
        order_match = self._first_order_after(a_stop_event_time)
        if order_match is None:
            return
        self._record_a_order_audit(zone, a_stop_event_time, order_match)


    def _order_stop(
        self, order_number: int, reaction: object
    ) -> tuple[Decimal, int, datetime]:
        return self.chronology.canonical_order_stop(
            self.order_direction,
            order_number,
            reaction,
            self.opposite_reactions,
            start_index=self.start_index,
        )


    def _order_stop_crossed(self, candle: object, level: Decimal) -> bool:
        if self.order_direction == "bearish":
            return as_decimal(getattr(candle, "high")) > level
        return as_decimal(getattr(candle, "low")) < level


    def _shared_order_stop_cross(
        self, confirmation: datetime, level: Decimal
    ) -> tuple[int, datetime, datetime] | None:
        """Return the first strict stop of an accepted Order after confirmation."""
        scan_start = max(confirmation, self.range_start)
        left = bisect_left(self.lower_times, scan_start)
        right = bisect_left(self.lower_times, self.range_end)
        if right > left and self.lower_index is not None:
            position = (
                self.lower_index.first_greater(left, right, level)
                if self.order_direction == "bearish"
                else self.lower_index.first_less(left, right, level)
            )
            if position is None:
                return None
            event_time = self.lower_times[position]
            index = self._main_index(event_time)
            return index, getattr(self.candles[index], "timestamp"), event_time

        for item in self.lower[left:right]:
            if self._order_stop_crossed(item, level):
                event_time = getattr(item, "timestamp")
                index = self._main_index(event_time)
                return index, getattr(self.candles[index], "timestamp"), event_time
        return None

````
<!-- EXACT-SOURCE-END:pipeline/order_audit_engine.py -->

### 16.12 `pipeline/reaction_engine.py` — Reaction / Reset

**SHA-256:** `bea0d5a5e95ee15ad54d024f6c01b8c777ba2abcc3c8e671118f1ae2df28f2a6`  
**Bytes:** `103120`  
**LF count:** `2406`

<!-- EXACT-SOURCE-BEGIN:pipeline/reaction_engine.py -->
````python
"""Authoritative Reaction geometry and shared market chronology.

Owns candle semantics, Bullish/Bearish Reaction and Reset detection, exact
lower-timeframe chronology, canonical Order-stop geometry, and
Internal-Reaction classification. It does not decide Blue/A/S/E/StopAll
visibility or lifecycle priority.
"""

from __future__ import annotations

import bisect
from array import array
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Iterable, Sequence

from direction_policy import policy_for


REACTION_ENGINE_VERSION = "9.8.0"
REACTION_ENGINE_LAST_MODIFIED = "2026-09-22 00:35:00 +03:30"

_SEQUENCE_TIME_INDEXES: dict[int, tuple[Sequence[Candle], list[datetime]]] = {}

@dataclass(frozen=True, slots=True)
class Candle:
    index: int
    timestamp: datetime
    display_time: str
    tag: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal


@dataclass(slots=True)
class Candidate:
    first_idx: int
    first_time: str
    box_top_source_idx: int
    box_top_source_time: str
    box_top: Decimal
    box_bottom_source_idx: int
    box_bottom_source_time: str
    box_bottom: Decimal
    mode: str
    anchor_idx: int | None = None
    anchor_value: Decimal | None = None
    leg_boundary_value: Decimal | None = None
    break_idx: int | None = None
    break_time: str | None = None
    intrabar_start: datetime | None = None
    cross_direction_origin: bool = False
    cross_direction_chain_owner: bool = False
    order_gate_decision: str | None = None
    behavior_public_number: int | None = None
    behavior_public_box_top: Decimal | None = None
    behavior_public_box_bottom: Decimal | None = None
    behavior_confirmation_time: datetime | None = None
    behavior_first_time: datetime | None = None
    behavior_internal: bool = False


@dataclass(frozen=True, slots=True)
class ResetEvent:
    index: int
    display_time: str
    second_time: str | None
    broken_level: Decimal
    from_first_idx: int


@dataclass(frozen=True, slots=True)
class IntrabarAnalysis:
    event_second: Candle
    extreme: Decimal
    extreme_source: Candle


@dataclass(frozen=True, slots=True)
class DetectionResult:
    direction: str
    reactions: list[Candidate]
    resets: list[ResetEvent]
    start_index: int
    end_index: int


def classify_candle_color(open_price: Decimal, close_price: Decimal) -> str:
    """Match Lightweight Charts: Open <= Close is an up/green candle."""
    return "GREEN" if open_price <= close_price else "RED"


def opposite_direction(direction: str) -> str:
    """Return the exact Bullish/Bearish mirror direction."""
    return policy_for(direction).opposite_direction


class DetectorBase:
    def __init__(
        self,
        candles: Sequence[Candle],
        one_second_candles: Sequence[Candle],
        start_index: int,
        end_index: int,
    ) -> None:
        self.candles = candles
        self.seconds = one_second_candles
        self.start_index = start_index
        self.end_index = end_index
        self.main_times = self._shared_time_index(candles)
        self.second_times = self._shared_time_index(one_second_candles)
        self.lower_index = shared_lower_timeframe_index(one_second_candles)
        self._reaction_break_index_cache: dict[str, tuple[int, list[int]]] = {}

        if len(candles) > 1:
            self.timeframe = candles[1].timestamp - candles[0].timestamp
        else:
            self.timeframe = timedelta(seconds=1)

        if self.timeframe.total_seconds() <= 0:
            raise ValueError("Main timeframe must be positive.")

    @staticmethod
    def _shared_time_index(candles: Sequence[Candle]) -> list[datetime]:
        """Build one immutable-source timestamp index per calculation process."""
        key = id(candles)
        cached = _SEQUENCE_TIME_INDEXES.get(key)
        if cached is not None and cached[0] is candles:
            return cached[1]
        times = [candle.timestamp for candle in candles]
        _SEQUENCE_TIME_INDEXES[key] = (candles, times)
        return times

    def seconds_between(self, start: datetime, end: datetime) -> Iterable[Candle]:
        left = bisect.bisect_left(self.second_times, start)
        right = bisect.bisect_left(self.second_times, end)
        return (self.seconds[index] for index in range(left, right))

    def main_source_for_time(self, timestamp: datetime) -> Candle | None:
        position = bisect.bisect_right(self.main_times, timestamp) - 1
        if position < self.start_index or position > self.end_index:
            return None
        end = (
            self.candles[position + 1].timestamp
            if position + 1 < len(self.candles)
            else self.candles[position].timestamp + self.timeframe
        )
        if timestamp < end:
            return self.candles[position]
        return None

    def minimum_low(self, start_index: int, end_index: int) -> tuple[Decimal, Candle]:
        source = self.candles[start_index]
        candles = self.candles
        for index in range(start_index + 1, end_index + 1):
            candle = candles[index]
            if candle.low < source.low:
                source = candle
        return source.low, source

    def maximum_high(self, start_index: int, end_index: int) -> tuple[Decimal, Candle]:
        source = self.candles[start_index]
        candles = self.candles
        for index in range(start_index + 1, end_index + 1):
            candle = candles[index]
            if candle.high > source.high:
                source = candle
        return source.high, source


class BullishDetector(DetectorBase):
    def green_run_peak_before(self, first_red_index: int) -> tuple[Decimal, Candle]:
        run_end = first_red_index - 1
        if run_end < self.start_index or self.candles[run_end].tag != "GREEN":
            raise ValueError("Mode-A FirstRed must immediately follow a GREEN candle.")

        run_start = run_end
        while run_start > self.start_index and self.candles[run_start - 1].tag == "GREEN":
            run_start -= 1
        return self.maximum_high(run_start, run_end)

    def breakout_analysis(
        self, candidate: Candidate, breakout_candle: Candle
    ) -> IntrabarAnalysis | None:
        start_index = (
            candidate.box_top_source_idx + 1
            if candidate.box_top_source_idx < candidate.first_idx
            else candidate.box_top_source_idx
        )
        start = candidate.intrabar_start or self.candles[start_index].timestamp
        end = breakout_candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, start)
        right = bisect.bisect_left(self.second_times, end)
        crossing = self.lower_index.first_greater(left, right, candidate.box_top)
        if crossing is None:
            return None
        minimum_low, minimum_position = self.lower_index.range_minimum(
            left, crossing + 1
        )
        minimum_time = self.second_times[minimum_position]
        source = self.main_source_for_time(minimum_time)
        if source is None:
            return None
        return IntrabarAnalysis(
            self.seconds[crossing], minimum_low, source
        )

    def mode_a_invalidation_before_breakout(
        self, candidate: Candidate, candle: Candle
    ) -> bool:
        # A Mode-A candidate belongs to the complete leg that opened at the
        # analysis/Reset boundary.  Later lower RED candles are internal
        # BoxBottom updates; only a strict break of the frozen leg floor can
        # invalidate the candidate before its BoxTop breaks.
        invalidation_level = (
            candidate.anchor_value
            if candidate.anchor_value is not None
            else candidate.leg_boundary_value
        )
        if invalidation_level is None:
            return False
        if candle.low >= invalidation_level:
            return False
        if candle.high <= candidate.box_top:
            return True

        end = candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, candle.timestamp)
        right = bisect.bisect_left(self.second_times, end)
        invalidation = self.lower_index.first_less(
            left, right, invalidation_level
        )
        breakout = self.lower_index.first_greater(
            left, right, candidate.box_top
        )
        if invalidation is None:
            return breakout is None
        if breakout is None:
            return True
        # The legacy loop checks Low first inside one lower-timeframe candle,
        # so invalidation wins a true same-second tie.
        return invalidation <= breakout

    def confirmed_reset_before_breakout(
        self, candidate: Candidate | None, candle: Candle, confirmed_bottom: Decimal
    ) -> bool:
        if candidate is None or candle.high <= candidate.box_top:
            return True

        end = candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, candle.timestamp)
        right = bisect.bisect_left(self.second_times, end)
        reset = self.lower_index.first_less(left, right, confirmed_bottom)
        breakout = self.lower_index.first_greater(
            left, right, candidate.box_top
        )
        if reset is None:
            return breakout is None
        if breakout is None:
            return True
        # Reset is checked before breakout within one lower-timeframe candle.
        return reset <= breakout

    def post_breakout_reset(
        self,
        analysis: IntrabarAnalysis | None,
        box_bottom: Decimal,
        breakout_candle: Candle,
    ) -> Candle | None:
        if analysis is None:
            return None
        start = analysis.event_second.timestamp + timedelta(microseconds=1)
        end = breakout_candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, start)
        right = bisect.bisect_left(self.second_times, end)
        position = self.lower_index.first_less(left, right, box_bottom)
        return None if position is None else self.seconds[position]

    def detect(self, *, first_only: bool = False) -> DetectionResult:
        reactions: list[Candidate] = []
        resets: list[ResetEvent] = []
        mode = "A"
        state = "SCANNING"
        last_confirmed_bottom: Decimal | None = None
        last_confirmed_first_idx: int | None = None
        running_peak: Decimal | None = None
        running_peak_src: int | None = None
        leg_open_low: Decimal | None = None
        leg_just_started = True
        anchor_red: Candle | None = None
        anchor_red_origin: str | None = None
        reset_context: Candle | None = None
        candidate: Candidate | None = None

        for index in range(self.start_index, self.end_index + 1):
            candle = self.candles[index]
            reset_detected = (
                last_confirmed_bottom is not None and candle.low < last_confirmed_bottom
            )
            reset_occurs_first = reset_detected
            if reset_detected and state == "WAITING":
                reset_occurs_first = self.confirmed_reset_before_breakout(
                    candidate, candle, last_confirmed_bottom
                )

            if reset_occurs_first:
                resets.append(
                    ResetEvent(
                        index=candle.index,
                        display_time=candle.display_time,
                        second_time=None,
                        broken_level=last_confirmed_bottom,
                        from_first_idx=last_confirmed_first_idx,
                    )
                )
                candidate = None
                last_confirmed_bottom = None
                last_confirmed_first_idx = None
                running_peak = None
                running_peak_src = None
                mode = "A"
                state = "SCANNING"
                leg_open_low = None
                leg_just_started = True
                anchor_red = candle if candle.tag == "RED" else None
                anchor_red_origin = "reset" if candle.tag == "RED" else None
                reset_context = candle
                continue

            if state == "WAITING":
                assert candidate is not None

                if (
                    candidate.mode == "A"
                    and self.mode_a_invalidation_before_breakout(candidate, candle)
                ):
                    candidate = None
                    state = "SCANNING"
                    anchor_red = candle if candle.tag == "RED" else None
                    anchor_red_origin = (
                        "candidate_invalidation" if candle.tag == "RED" else None
                    )
                    continue

                if candle.low < candidate.box_bottom:
                    candidate.box_bottom = candle.low
                    candidate.box_bottom_source_idx = candle.index
                    candidate.box_bottom_source_time = candle.display_time

                if candle.high > candidate.box_top:
                    candidate.break_idx = candle.index
                    candidate.break_time = candle.display_time
                    analysis = self.breakout_analysis(candidate, candle)

                    if (
                        candidate.box_bottom_source_idx == candle.index
                        and analysis is not None
                    ):
                        candidate.box_bottom = analysis.extreme
                        candidate.box_bottom_source_idx = analysis.extreme_source.index
                        candidate.box_bottom_source_time = (
                            analysis.extreme_source.display_time
                        )

                    confirmed = replace(candidate)
                    reactions.append(confirmed)
                    if first_only:
                        return DetectionResult(
                            direction="bullish",
                            reactions=reactions,
                            resets=resets,
                            start_index=self.start_index,
                            end_index=self.end_index,
                        )
                    last_confirmed_bottom = confirmed.box_bottom
                    last_confirmed_first_idx = confirmed.first_idx
                    running_peak = candle.high
                    running_peak_src = candle.index
                    mode = "B"
                    state = "SCANNING"
                    candidate = None

                    reset_second = self.post_breakout_reset(
                        analysis, last_confirmed_bottom, candle
                    )
                    if reset_second is not None:
                        resets.append(
                            ResetEvent(
                                index=candle.index,
                                display_time=candle.display_time,
                                second_time=reset_second.display_time,
                                broken_level=last_confirmed_bottom,
                                from_first_idx=last_confirmed_first_idx,
                            )
                        )
                        last_confirmed_bottom = None
                        last_confirmed_first_idx = None
                        running_peak = None
                        running_peak_src = None
                        mode = "A"
                        state = "SCANNING"
                        leg_open_low = None
                        leg_just_started = True
                        anchor_red = candle if candle.tag == "RED" else None
                        anchor_red_origin = "reset" if candle.tag == "RED" else None
                        reset_context = candle
                        continue

                    if candle.tag == "RED":
                        candidate = Candidate(
                            first_idx=candle.index,
                            first_time=candle.display_time,
                            box_top_source_idx=candle.index,
                            box_top_source_time=candle.display_time,
                            box_top=running_peak,
                            box_bottom_source_idx=candle.index,
                            box_bottom_source_time=candle.display_time,
                            box_bottom=candle.low,
                            mode="B",
                        )
                        state = "WAITING"
                continue

            if mode == "A":
                if leg_just_started:
                    leg_open_low = candle.low
                    leg_just_started = False
                    previous_reset = reset_context
                    reset_context = None
                    if candle.tag == "RED":
                        if (
                            previous_reset is not None
                            and previous_reset.tag == "GREEN"
                            and candle.low >= previous_reset.low
                        ):
                            green_high, green_source = self.green_run_peak_before(
                                candle.index
                            )
                            if green_high >= candle.high:
                                box_top = green_high
                                box_top_source = green_source
                            else:
                                box_top = candle.high
                                box_top_source = candle
                            candidate = Candidate(
                                first_idx=candle.index,
                                first_time=candle.display_time,
                                box_top_source_idx=box_top_source.index,
                                box_top_source_time=box_top_source.display_time,
                                box_top=box_top,
                                box_bottom_source_idx=candle.index,
                                box_bottom_source_time=candle.display_time,
                                box_bottom=candle.low,
                                mode="A",
                                leg_boundary_value=leg_open_low,
                            )
                            state = "WAITING"
                        else:
                            anchor_red = candle
                            anchor_red_origin = "leg_open"
                    continue

                previous = self.candles[index - 1]
                passes = False
                box_top: Decimal | None = None
                box_top_source: Candle | None = None

                if previous.tag == "GREEN" and candle.tag == "RED":
                    if (
                        anchor_red is not None
                        and anchor_red_origin == "candidate_invalidation"
                        and previous.low < anchor_red.low
                        and candle.low < anchor_red.low
                    ):
                        anchor_red = None
                        anchor_red_origin = None

                    if anchor_red is not None:
                        passes = candle.low >= anchor_red.low
                    elif candle.low >= previous.low or candle.low >= leg_open_low:
                        passes = True

                    if passes:
                        green_high, green_source = self.green_run_peak_before(candle.index)
                        if green_high >= candle.high:
                            box_top = green_high
                            box_top_source = green_source
                        else:
                            box_top = candle.high
                            box_top_source = candle

                if passes:
                    assert box_top is not None and box_top_source is not None
                    candidate = Candidate(
                        first_idx=candle.index,
                        first_time=candle.display_time,
                        box_top_source_idx=box_top_source.index,
                        box_top_source_time=box_top_source.display_time,
                        box_top=box_top,
                        box_bottom_source_idx=candle.index,
                        box_bottom_source_time=candle.display_time,
                        box_bottom=candle.low,
                        mode="A",
                        anchor_idx=anchor_red.index if anchor_red else None,
                        anchor_value=anchor_red.low if anchor_red else None,
                        leg_boundary_value=leg_open_low,
                    )
                    state = "WAITING"
                elif candle.tag == "RED":
                    anchor_red = candle
                    anchor_red_origin = "scan"
                elif candle.tag in {"DOJI", "NEUTRAL"}:
                    anchor_red = None
                    anchor_red_origin = None
            else:
                if candle.tag == "RED":
                    box_top = candle.high
                    box_top_source_idx = candle.index
                    if running_peak is not None and running_peak >= box_top:
                        box_top = running_peak
                        box_top_source_idx = running_peak_src

                    bottom_start = (
                        box_top_source_idx + 1
                        if box_top_source_idx < candle.index
                        else candle.index
                    )
                    bottom, bottom_source = self.minimum_low(bottom_start, candle.index)
                    candidate = Candidate(
                        first_idx=candle.index,
                        first_time=candle.display_time,
                        box_top_source_idx=box_top_source_idx,
                        box_top_source_time=self.candles[
                            box_top_source_idx
                        ].display_time,
                        box_top=box_top,
                        box_bottom_source_idx=bottom_source.index,
                        box_bottom_source_time=bottom_source.display_time,
                        box_bottom=bottom,
                        mode="B",
                    )
                    state = "WAITING"

                if running_peak is None or candle.high > running_peak:
                    running_peak = candle.high
                    running_peak_src = candle.index

        return DetectionResult(
            direction="bullish",
            reactions=reactions,
            resets=resets,
            start_index=self.start_index,
            end_index=self.end_index,
        )


def mirror_candle(candle: Candle) -> Candle:
    """Internal coordinate/role adapter; never reclassify a market candle here.

    Input dojis are GREEN in both market directions, matching the chart.
    Swapping that tag inside the Bullish reference makes its RED/FirstRed
    branch implement the original GREEN/FirstGreen Bearish branch. This is
    not permission to treat a market doji as RED or emit a changed chart color.
    """
    return Candle(
        index=candle.index,
        timestamp=candle.timestamp,
        display_time=candle.display_time,
        tag={"GREEN": "RED", "RED": "GREEN"}.get(candle.tag, candle.tag),
        open=candle.open.copy_negate(),
        high=candle.low.copy_negate(),
        low=candle.high.copy_negate(),
        close=candle.close.copy_negate(),
    )


def mirror_candidate(candidate: Candidate | None) -> Candidate | None:
    """Mirror geometry while preserving invariant dynamic gate state."""
    if candidate is None:
        return None
    mirrored = replace(
        candidate,
        box_top=candidate.box_bottom.copy_negate(),
        box_bottom=candidate.box_top.copy_negate(),
        box_top_source_idx=candidate.box_bottom_source_idx,
        box_top_source_time=candidate.box_bottom_source_time,
        box_bottom_source_idx=candidate.box_top_source_idx,
        box_bottom_source_time=candidate.box_top_source_time,
        anchor_value=(candidate.anchor_value.copy_negate()
                      if candidate.anchor_value is not None else None),
        leg_boundary_value=(candidate.leg_boundary_value.copy_negate()
                            if candidate.leg_boundary_value is not None else None),
    )
    return mirrored

def mirror_analysis(analysis: IntrabarAnalysis | None) -> IntrabarAnalysis | None:
    if analysis is None:
        return None
    return IntrabarAnalysis(
        mirror_candle(analysis.event_second), analysis.extreme.copy_negate(),
        mirror_candle(analysis.extreme_source),
    )


class _ReflectedCandles(Sequence[Candle]):
    """Read-only coordinate view with one-time mirror caching.

    Each source candle is mirrored at most once (on first access) and the
    result is cached, so repeated scans reuse the same object instead of
    allocating a fresh mirrored Candle on every access.
    """

    def __init__(self, source: Sequence[Candle]) -> None:
        self.source = source
        self._cache: list[Candle | None] = [None] * len(source)

    def __len__(self) -> int:
        return len(self.source)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self[i] for i in range(*index.indices(len(self.source)))]
        cached = self._cache[index]
        if cached is None:
            cached = mirror_candle(self.source[index])
            self._cache[index] = cached
        return cached


_REFLECTED_VIEWS: dict[int, tuple[Sequence[Candle], _ReflectedCandles]] = {}


def _reflected_view(source: Sequence[Candle]) -> _ReflectedCandles:
    key = id(source)
    cached = _REFLECTED_VIEWS.get(key)
    if cached is not None and cached[0] is source:
        return cached[1]
    view = _ReflectedCandles(source)
    _REFLECTED_VIEWS[key] = (source, view)
    return view


class BearishDetector(DetectorBase):
    """Execute the Bullish reference state machine in reflected coordinates.

    This is a coordinate adapter, not a second rule implementation. Both the
    initial Leg-Start and opposite-anchor queries use the same reference rules.
    Exact Decimal sign copying avoids context rounding during reflection.
    """

    def __init__(self, candles, one_second_candles, start_index, end_index):
        super().__init__(candles, one_second_candles, start_index, end_index)
        self.reference = BullishDetector(
            candles, one_second_candles, start_index, end_index,
        )
        # Time indexes are invariant under price reflection. Construct them
        # from the original rows; lazily transform OHLC only when consumed.
        # _ReflectedCandles caches each mirrored candle so repeated scans do
        # not re-allocate, while construction stays cheap (important because
        # _append_reaction builds a fresh BearishDetector per reaction).
        self.reference.candles = _reflected_view(candles)
        self.reference.seconds = _reflected_view(one_second_candles)
        self.reference.lower_index = ReflectedLowerTimeframeIndex(self.lower_index)

    def red_run_bottom_before(self, first_green_index):
        value, source = self.reference.green_run_peak_before(first_green_index)
        return value.copy_negate(), mirror_candle(source)

    def breakdown_analysis(self, candidate, breakdown_candle):
        return mirror_analysis(self.reference.breakout_analysis(
            mirror_candidate(candidate), mirror_candle(breakdown_candle),
        ))

    def invalidation_high_break_before_breakdown(self, candidate, candle):
        return self.reference.mode_a_invalidation_before_breakout(
            mirror_candidate(candidate), mirror_candle(candle),
        )

    def confirmed_reset_before_breakdown(self, candidate, candle, confirmed_top):
        return self.reference.confirmed_reset_before_breakout(
            mirror_candidate(candidate), mirror_candle(candle),
            confirmed_top.copy_negate(),
        )

    def post_breakdown_reset(self, analysis, box_top, breakdown_candle):
        result = self.reference.post_breakout_reset(
            mirror_analysis(analysis), box_top.copy_negate(),
            mirror_candle(breakdown_candle),
        )
        return mirror_candle(result) if result is not None else None

    def detect(self, *, first_only: bool = False) -> DetectionResult:
        result = self.reference.detect(first_only=first_only)
        return DetectionResult(
            direction="bearish",
            reactions=[mirror_candidate(candidate) for candidate in result.reactions],
            resets=[replace(reset, broken_level=reset.broken_level.copy_negate())
                    for reset in result.resets],
            start_index=result.start_index, end_index=result.end_index,
        )


def published_reaction_candidate(
    direction: str,
    candidate: Candidate,
    chronology: object,
) -> Candidate:
    """Return a presentation clone with Break-candle geometry frozen at confirmation.

    Detection/lifecycle ownership is intentionally not mutated here.  The public
    Reaction box must not include an opposite-edge extreme that happened later
    inside the same main Break candle after the Reaction had already confirmed.

    Main candles strictly before Break are fully eligible.  Only when the
    full-main-candle opposite extreme is owned by Break do we use one-second
    chronology to keep prices up to and including the first strict confirmation:

      Bullish -> published BoxBottom is the minimum eligible Low before the
                 first strict High > BoxTop breakout.
      Bearish -> published BoxTop is the maximum eligible High before the
                 first strict Low < BoxBottom breakdown.

    Equal extremes retain the earliest main-candle owner.  If lower-timeframe
    data cannot resolve the strict confirmation, preserve the detector geometry
    rather than guessing an intrabar order.
    """
    candles = chronology.candles
    one_second_candles = chronology.seconds
    published = replace(candidate)
    if candidate.break_idx is None:
        return published

    first_index = int(candidate.first_idx)
    break_index = int(candidate.break_idx)
    if first_index < 0 or break_index < first_index or break_index >= len(candles):
        return published

    break_candle = candles[break_index]
    timeframe = chronology.timeframe

    if direction == "bullish":
        # No Break-candle ownership -> the published full-range minimum was
        # already made before confirmation and is therefore chronology-safe.
        if int(candidate.box_bottom_source_idx) != break_index:
            return published
        value = candles[first_index].low
        source = candles[first_index]
        for index in range(first_index + 1, break_index):
            candle = candles[index]
            if candle.low < value:
                value, source = candle.low, candle
        threshold = candidate.box_top
    elif direction == "bearish":
        if int(candidate.box_top_source_idx) != break_index:
            return published
        value = candles[first_index].high
        source = candles[first_index]
        for index in range(first_index + 1, break_index):
            candle = candles[index]
            if candle.high > value:
                value, source = candle.high, candle
        threshold = candidate.box_bottom
    else:
        raise ValueError(f"Unsupported reaction direction: {direction}")

    lo, hi = chronology.lower_bounds(
        break_candle.timestamp, break_candle.timestamp + timeframe
    )
    confirmed = False

    for second in one_second_candles[lo:hi]:
        if direction == "bullish":
            if second.low < value:
                value = second.low
                source = break_candle
            if second.high > threshold:
                confirmed = True
                break
        else:
            if second.high > value:
                value = second.high
                source = break_candle
            if second.low < threshold:
                confirmed = True
                break

    if not confirmed:
        return published

    if direction == "bullish":
        published.box_bottom = value
        published.box_bottom_source_idx = source.index
        published.box_bottom_source_time = source.display_time
    else:
        published.box_top = value
        published.box_top_source_idx = source.index
        published.box_top_source_time = source.display_time
    return published


def _decimal_value(value: object) -> Decimal:
    """Normalize external numeric values without binary-float arithmetic."""
    return value if isinstance(value, Decimal) else Decimal(str(value))


class LowerTimeframeIndex:
    """Immutable segment index for exact first strict High/Low crossings.

    The index is direction-agnostic and shared by A/S/E so heavy 1-second
    inputs are not rescanned for every stop/trigger lookup.
    """

    def __init__(self, candles: Sequence[Candle]) -> None:
        self.candles = candles
        self.times = [getattr(item, "timestamp") for item in candles]
        size = 1
        while size < len(candles):
            size <<= 1
        self.size = size
        self.length = len(candles)
        self.minimum: list[Decimal | None] = [None] * (2 * size)
        self.maximum: list[Decimal | None] = [None] * (2 * size)
        self.minimum_position = array("i", [-1]) * (2 * size)
        self.maximum_position = array("i", [-1]) * (2 * size)
        for position, candle in enumerate(candles):
            node = size + position
            self.minimum[node] = _decimal_value(getattr(candle, "low"))
            self.maximum[node] = _decimal_value(getattr(candle, "high"))
            self.minimum_position[node] = position
            self.maximum_position[node] = position
        for node in range(size - 1, 0, -1):
            left, right = node * 2, node * 2 + 1
            low_left, low_right = self.minimum[left], self.minimum[right]
            high_left, high_right = self.maximum[left], self.maximum[right]
            if low_left is None:
                self.minimum[node] = low_right
                self.minimum_position[node] = self.minimum_position[right]
            elif low_right is None or low_left <= low_right:
                self.minimum[node] = low_left
                self.minimum_position[node] = self.minimum_position[left]
            else:
                self.minimum[node] = low_right
                self.minimum_position[node] = self.minimum_position[right]
            if high_left is None:
                self.maximum[node] = high_right
                self.maximum_position[node] = self.maximum_position[right]
            elif high_right is None or high_left >= high_right:
                self.maximum[node] = high_left
                self.maximum_position[node] = self.maximum_position[left]
            else:
                self.maximum[node] = high_right
                self.maximum_position[node] = self.maximum_position[right]

    def first_less(self, left: int, right: int, level: Decimal) -> int | None:
        return self._first(1, 0, self.size, left, right, level, True)

    def first_greater(self, left: int, right: int, level: Decimal) -> int | None:
        return self._first(1, 0, self.size, left, right, level, False)

    def range_minimum(self, left: int, right: int) -> tuple[Decimal, int]:
        """Return the minimum Low and earliest owning position in [left, right)."""
        return self._range_query(left, right, minimum=True)

    def range_maximum(self, left: int, right: int) -> tuple[Decimal, int]:
        """Return the maximum High and earliest owning position in [left, right)."""
        return self._range_query(left, right, minimum=False)

    def _range_query(
        self, left: int, right: int, *, minimum: bool
    ) -> tuple[Decimal, int]:
        if left < 0 or right > self.length or left >= right:
            raise ValueError("Range contains no lower-timeframe candles.")
        values = self.minimum if minimum else self.maximum
        positions = self.minimum_position if minimum else self.maximum_position
        left += self.size
        right += self.size
        best_value: Decimal | None = None
        best_position = -1
        while left < right:
            if left & 1:
                value = values[left]
                position = positions[left]
                if value is not None and (
                    best_value is None
                    or (value < best_value if minimum else value > best_value)
                    or (value == best_value and position < best_position)
                ):
                    best_value, best_position = value, position
                left += 1
            if right & 1:
                right -= 1
                value = values[right]
                position = positions[right]
                if value is not None and (
                    best_value is None
                    or (value < best_value if minimum else value > best_value)
                    or (value == best_value and position < best_position)
                ):
                    best_value, best_position = value, position
            left >>= 1
            right >>= 1
        if best_value is None or best_position < 0:
            raise ValueError("Range contains no lower-timeframe candles.")
        return best_value, best_position

    def _first(
        self, node: int, start: int, end: int, left: int, right: int,
        level: Decimal, less: bool,
    ) -> int | None:
        if end <= left or right <= start or start >= self.length:
            return None
        extreme = self.minimum[node] if less else self.maximum[node]
        if extreme is None or (extreme >= level if less else extreme <= level):
            return None
        if end - start == 1:
            return start
        middle = (start + end) // 2
        found = self._first(node * 2, start, middle, left, right, level, less)
        if found is not None:
            return found
        return self._first(
            node * 2 + 1, middle, end, left, right, level, less
        )


_LOWER_TIMEFRAME_INDEXES: dict[
    int, tuple[Sequence[Candle], LowerTimeframeIndex]
] = {}


def shared_lower_timeframe_index(
    candles: Sequence[Candle],
) -> LowerTimeframeIndex:
    """Reuse one immutable lower-timeframe index per source sequence."""
    key = id(candles)
    cached = _LOWER_TIMEFRAME_INDEXES.get(key)
    if cached is not None and cached[0] is candles:
        return cached[1]
    index = LowerTimeframeIndex(candles)
    _LOWER_TIMEFRAME_INDEXES[key] = (candles, index)
    return index


class ReflectedLowerTimeframeIndex:
    """Price-reflected view over a lower-timeframe index without rebuilding it."""

    __slots__ = ("base", "times")

    def __init__(self, base: LowerTimeframeIndex) -> None:
        self.base = base
        self.times = base.times

    def first_less(self, left: int, right: int, level: Decimal) -> int | None:
        return self.base.first_greater(left, right, level.copy_negate())

    def first_greater(self, left: int, right: int, level: Decimal) -> int | None:
        return self.base.first_less(left, right, level.copy_negate())

    def range_minimum(self, left: int, right: int) -> tuple[Decimal, int]:
        value, position = self.base.range_maximum(left, right)
        return value.copy_negate(), position

    def range_maximum(self, left: int, right: int) -> tuple[Decimal, int]:
        value, position = self.base.range_minimum(left, right)
        return value.copy_negate(), position


class MarketChronology:
    """Shared immutable market-time services for downstream behavior engines.

    Reaction owns chronology semantics.  A/S/E receive this object rather than
    rebuilding timestamp indexes, lower-timeframe windows, confirmation scans,
    and Reset timestamp parsing independently.
    """

    __slots__ = (
        "candles",
        "seconds",
        "times",
        "second_times",
        "timeframe",
        "lower_index",
        "_confirmation_cache",
        "_reset_time_cache",
    )

    def __init__(
        self,
        candles: Sequence[Candle],
        seconds: Sequence[Candle],
        timeframe_seconds: int,
        lower_index: LowerTimeframeIndex | None = None,
    ) -> None:
        if timeframe_seconds < 1:
            raise ValueError("Timeframe must be at least one second.")
        self.candles = candles
        self.seconds = seconds
        self.times = [getattr(item, "timestamp") for item in candles]
        self.second_times = (
            lower_index.times
            if lower_index is not None
            else [getattr(item, "timestamp") for item in seconds]
        )
        self.timeframe = timedelta(seconds=timeframe_seconds)
        self.lower_index = lower_index or shared_lower_timeframe_index(seconds)
        self._confirmation_cache: dict[tuple[object, ...], datetime] = {}
        self._reset_time_cache: dict[tuple[object, ...], datetime] = {}

    @staticmethod
    def opposite_direction(direction: str) -> str:
        """Expose the shared mirror-direction contract to downstream engines."""
        return opposite_direction(direction)

    def main_index(self, timestamp: datetime, *, clamp: bool = False) -> int:
        """Map an exact lower-timeframe timestamp to its owning main candle."""
        index = bisect.bisect_right(self.times, timestamp) - 1
        if index < 0:
            if clamp:
                return 0
            raise ValueError("Lower-timeframe event precedes the main candles.")
        return index

    def lower_bounds(
        self, start: datetime, end: datetime | None = None
    ) -> tuple[int, int]:
        left = bisect.bisect_left(self.second_times, start)
        right = (
            len(self.seconds)
            if end is None
            else bisect.bisect_left(self.second_times, end)
        )
        return left, right

    def lower_window(
        self, start: datetime, end: datetime | None = None
    ) -> Sequence[Candle]:
        left, right = self.lower_bounds(start, end)
        return self.seconds[left:right]

    @staticmethod
    def _reset_cache_key(reset: object) -> tuple[object, ...]:
        """Return a stable Reset identity suitable for chronology caches."""
        return (
            int(getattr(reset, "index", -1)),
            int(getattr(reset, "from_first_idx", -1)),
            getattr(reset, "second_time", None),
            getattr(reset, "display_time", None),
            getattr(reset, "timestamp", None),
            str(getattr(reset, "broken_level", "")),
        )

    @staticmethod
    def _reaction_cache_key(
        reaction: object, direction: str, use_intrabar_start: bool
    ) -> tuple[object, ...]:
        """Return a stable physical/geometry identity for confirmation caches."""
        return (
            direction,
            bool(use_intrabar_start),
            int(getattr(reaction, "first_idx")),
            int(getattr(reaction, "break_idx")),
            str(getattr(reaction, "box_top")),
            str(getattr(reaction, "box_bottom")),
            getattr(reaction, "intrabar_start", None) if use_intrabar_start else None,
        )

    def reset_time(self, reset: object) -> datetime:
        """Return the exact Reset event time, preserving legacy provenance."""
        cache_key = self._reset_cache_key(reset)
        cached = self._reset_time_cache.get(cache_key)
        if cached is not None:
            return cached
        second = getattr(reset, "second_time", None)
        if second:
            result = datetime.strptime(second, "%Y-%m-%d %H:%M:%S")
        else:
            display = getattr(reset, "display_time", None)
            result = (
                datetime.strptime(display, "%Y-%m-%d %H:%M:%S")
                if display
                else getattr(reset, "timestamp")
            )
        self._reset_time_cache[cache_key] = result
        return result

    def reaction_confirmation(
        self,
        direction: str,
        reaction: object,
        *,
        use_intrabar_start: bool = True,
    ) -> datetime:
        """Return the first strict lower-timeframe Reaction confirmation.

        ``use_intrabar_start=False`` preserves the established A-engine
        chronology contract, which starts its scan at the Break candle open.
        S/E and public Reaction chronology use the exact intrabar start when
        present.
        """
        cache_key = self._reaction_cache_key(
            reaction, direction, use_intrabar_start
        )
        cached = self._confirmation_cache.get(cache_key)
        if cached is not None:
            return cached
        break_index = int(getattr(reaction, "break_idx"))
        break_candle = self.candles[break_index]
        candle_start = getattr(break_candle, "timestamp")
        start = (
            getattr(reaction, "intrabar_start", None) or candle_start
            if use_intrabar_start
            else candle_start
        )
        candle_end = candle_start + self.timeframe
        if start < candle_start or start >= candle_end:
            start = candle_start
        level = _decimal_value(
            getattr(reaction, "box_top" if direction == "bullish" else "box_bottom")
        )
        left, right = self.lower_bounds(start, candle_end)
        field = "high" if direction == "bullish" else "low"
        for position in range(left, right):
            item = self.seconds[position]
            value = _decimal_value(getattr(item, field))
            confirms = value > level if direction == "bullish" else value < level
            if confirms:
                result = getattr(item, "timestamp")
                self._confirmation_cache[cache_key] = result
                return result
        self._confirmation_cache[cache_key] = candle_start
        return candle_start


    def canonical_order_stop(
        self,
        order_direction: str,
        reaction_number: int,
        reaction: object,
        opposite_reactions: Sequence[object],
        *,
        start_index: int = 0,
    ) -> tuple[Decimal, int, datetime]:
        """Return canonical opposite-Order stop provenance for S and E.

        Mode A owns the true leg head/floor from its anchor/context through
        Break inclusive. Mode B inherits the previous healthy opposite
        Reaction's semantic outer box edge. This is the single authoritative
        implementation used by every downstream behavior family.
        """
        if str(getattr(reaction, "mode")) == "A":
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            anchor_index = getattr(reaction, "anchor_idx", None)
            scan_start = (
                max(start_index, int(anchor_index))
                if anchor_index is not None
                else max(start_index, first_index - 1)
            )
            context_tag = "GREEN" if order_direction == "bearish" else "RED"
            while (
                scan_start > start_index
                and getattr(self.candles[scan_start - 1], "tag") == context_tag
            ):
                scan_start -= 1

            attribute = "high" if order_direction == "bearish" else "low"
            source_index = scan_start
            level = _decimal_value(getattr(self.candles[source_index], attribute))
            for candle in self.candles[scan_start + 1 : break_index + 1]:
                candidate = _decimal_value(getattr(candle, attribute))
                better = (
                    candidate > level
                    if order_direction == "bearish"
                    else candidate < level
                )
                if better:
                    source_index = int(getattr(candle, "index"))
                    level = candidate
            return level, source_index, getattr(self.candles[source_index], "timestamp")

        if reaction_number <= 1:
            raise ValueError("Mode-B order reaction has no previous healthy reaction.")
        previous = opposite_reactions[reaction_number - 2]
        if order_direction == "bearish":
            source_index = int(getattr(previous, "box_top_source_idx"))
            return (
                _decimal_value(getattr(previous, "box_top")),
                source_index,
                getattr(self.candles[source_index], "timestamp"),
            )
        source_index = int(getattr(previous, "box_bottom_source_idx"))
        return (
            _decimal_value(getattr(previous, "box_bottom")),
            source_index,
            getattr(self.candles[source_index], "timestamp"),
        )


def build_behavior_reaction_views(
    full_results: dict[str, object],
    chronology: MarketChronology,
):
    """Mark true cross-direction Reaction interiors for downstream behavior."""
    candles = chronology.candles
    seconds = chronology.seconds
    second_times = chronology.second_times
    public: dict[str, list[Candidate]] = {}
    confirmation: dict[str, list[datetime]] = {}
    for direction in ("bullish", "bearish"):
        public[direction] = [
            published_reaction_candidate(direction, item, chronology)
            for item in full_results[direction].reactions
        ]
        confirmation[direction] = [
            chronology.reaction_confirmation(direction, item)
            for item in full_results[direction].reactions
        ]

    def path_is_contained(
        first_time: datetime,
        confirmed_at: datetime,
        bottom: Decimal,
        top: Decimal,
    ) -> bool:
        left = bisect.bisect_left(second_times, first_time)
        right = bisect.bisect_right(second_times, confirmed_at)
        if left >= right:
            return False
        # Algorithm requirement: every physical lower-timeframe candle must
        # remain inside [bottom, top].  The immutable lower-timeframe range
        # index proves the exact same predicate via min(Low) and max(High),
        # without allocating/scanning the full slice for every Reaction pair.
        minimum_low, _ = chronology.lower_index.range_minimum(left, right)
        if minimum_low < bottom:
            return False
        maximum_high, _ = chronology.lower_index.range_maximum(left, right)
        return maximum_high <= top

    blocked: dict[str, set[tuple[int, int]]] = {
        "bullish": set(),
        "bearish": set(),
    }
    for direction in ("bullish", "bearish"):
        opposite = opposite_direction(direction)
        for number, reaction in enumerate(full_results[direction].reactions, start=1):
            reaction.behavior_public_number = number
            published = public[direction][number - 1]
            reaction.behavior_public_box_top = _decimal_value(published.box_top)
            reaction.behavior_public_box_bottom = _decimal_value(published.box_bottom)
            reaction.behavior_confirmation_time = confirmation[direction][number - 1]
            reaction.behavior_first_time = candles[int(getattr(reaction, "first_idx"))].timestamp

        for reaction, published, confirmed_at in zip(
            full_results[direction].reactions,
            public[direction],
            confirmation[direction],
        ):
            inner_first = candles[int(getattr(reaction, "first_idx"))].timestamp
            inner_top = _decimal_value(published.box_top)
            inner_bottom = _decimal_value(published.box_bottom)
            for outer, outer_published, outer_confirmed_at in zip(
                full_results[opposite].reactions,
                public[opposite],
                confirmation[opposite],
            ):
                outer_first = candles[int(getattr(outer, "first_idx"))].timestamp
                if inner_first <= outer_first or confirmed_at > outer_confirmed_at:
                    continue
                outer_top = _decimal_value(outer_published.box_top)
                outer_bottom = _decimal_value(outer_published.box_bottom)
                if (
                    inner_top <= outer_top
                    and inner_bottom >= outer_bottom
                    and path_is_contained(
                        inner_first,
                        confirmed_at,
                        outer_bottom,
                        outer_top,
                    )
                ):
                    blocked[direction].add(
                        (
                            int(getattr(reaction, "first_idx")),
                            int(getattr(reaction, "break_idx")),
                        )
                    )
                    break

    behavior_results = {}
    number_maps = {}
    blocked_first_times = {"bullish": set(), "bearish": set()}
    for direction in ("bullish", "bearish"):
        full = full_results[direction]
        for item in full.reactions:
            identity = (
                int(getattr(item, "first_idx")),
                int(getattr(item, "break_idx")),
            )
            item.behavior_internal = identity in blocked[direction]
        behavior_results[direction] = full
        number_maps[direction] = {
            number: number for number, _item in enumerate(full.reactions, start=1)
        }
        blocked_first_times[direction] = {
            candles[first_idx].timestamp for first_idx, _ in blocked[direction]
        }
    return behavior_results, number_maps, blocked, blocked_first_times


def directional_a_stop_order_finder(
    candles: Sequence[Candle],
    seconds: Sequence[Candle],
    direction: str,
):
    """Build the cached bounded opposite-Reaction resolver used after A stop."""
    if direction not in {"bullish", "bearish"}:
        raise ValueError("Direction must be 'bullish' or 'bearish'.")
    order_direction = opposite_direction(direction)
    first_tag = "GREEN" if order_direction == "bearish" else "RED"
    context_tag = "RED" if order_direction == "bearish" else "GREEN"
    cache: dict[tuple[int, int], Candidate | None] = {}
    detection_cache: dict[tuple[int, int], tuple[Candidate, ...]] = {}

    def find(gate_index: int, gate_event: datetime, end_index: int):
        key = (gate_index, end_index)
        if key in cache:
            return cache[key]
        first = next(
            (
                index
                for index in range(max(1, gate_index), end_index + 1)
                if candles[index].tag == first_tag
                and candles[index - 1].tag == context_tag
            ),
            None,
        )
        if first is None:
            cache[key] = None
            return None
        context = first - 1
        while context > 0 and candles[context - 1].tag == context_tag:
            context -= 1
        detection_key = (context, end_index)
        reactions = detection_cache.get(detection_key, ())
        order = next(
            (
                reaction
                for reaction in reactions
                if int(getattr(reaction, "first_idx")) >= gate_index
            ),
            None,
        )
        if order is None:
            result = UnifiedReactionDetector(
                candles, seconds, context, end_index, order_direction
            ).detect(stop_after_first_at_or_after=gate_index)
            reactions = tuple(result.reactions)
            detection_cache[detection_key] = reactions
            order = next(
                (
                    reaction
                    for reaction in reactions
                    if int(getattr(reaction, "first_idx")) >= gate_index
                ),
                None,
            )
        cache[key] = order
        return order

    return find


class UnifiedReactionDetector(DetectorBase):
    """Unified v9 directional post-Reset engine.

    The proven directional detectors supply only the initial Leg-Start. After
    that first confirmation this class owns Normal search and directional
    post-Reset continuation.  A Reset always searches for the first healthy
    reaction in the same direction as the requested/output leg; patterns in
    the opposite direction never gate or unlock that search.
    """

    def __init__(
        self,
        candles: Sequence[Candle],
        one_second_candles: Sequence[Candle],
        start_index: int,
        end_index: int,
        output_direction: str,
    ) -> None:
        super().__init__(candles, one_second_candles, start_index, end_index)
        self.output_direction = output_direction
        # Directional helpers are created lazily: a bullish-only run must not
        # pay the BearishDetector mirroring cost and vice versa.
        self._bull: BullishDetector | None = None
        self._bear: BearishDetector | None = None
        self.all_reactions: dict[str, list[Candidate]] = {
            "bullish": [],
            "bearish": [],
        }
        self.all_resets: dict[str, list[ResetEvent]] = {
            "bullish": [],
            "bearish": [],
        }
        self._geometry_after_reset_cache: dict[tuple, Candidate | None] = {}

    @property
    def bull(self) -> BullishDetector:
        if self._bull is None:
            self._bull = BullishDetector(
                self.candles, self.seconds, self.start_index, self.end_index
            )
        return self._bull

    @property
    def bear(self) -> BearishDetector:
        if self._bear is None:
            self._bear = BearishDetector(
                self.candles, self.seconds, self.start_index, self.end_index
            )
        return self._bear

    def _append_reaction(self, direction: str, candidate: Candidate) -> bool:
        # A confirmed adjacent opposite-direction Anchor may extend the outer
        # boundary, but it must never shrink the candidate's own box.
        opposite_anchor_is_confirmed = False
        if (
            candidate.break_idx is not None
            and candidate.anchor_idx is not None
            and candidate.anchor_idx + 1 == candidate.first_idx
            and self.all_resets[direction]
        ):
            reset_index = self.all_resets[direction][-1].index
            opposite_detector = (
                BullishDetector if direction == "bearish" else BearishDetector
            )(
                self.candles,
                self.seconds,
                reset_index,
                candidate.first_idx,
            )
            opposite_anchor_is_confirmed = any(
                reaction.break_idx == candidate.anchor_idx
                for reaction in opposite_detector.detect().reactions
            )

        if opposite_anchor_is_confirmed:
            anchor = self.candles[candidate.anchor_idx]
            first = self.candles[candidate.first_idx]
            if direction == "bearish":
                # A RED Leg-Start with a higher ceiling than FirstGreen owns
                # the leg boundary; FirstGreen must keep its own BoxBottom.
                if anchor.high <= first.high:
                    candidate.box_bottom = anchor.low
                    candidate.box_bottom_source_idx = anchor.index
                    candidate.box_bottom_source_time = anchor.display_time
            else:
                # Exact mirror: a GREEN Leg-Start whose floor is below
                # FirstRed owns the leg boundary; FirstRed keeps its BoxTop.
                if anchor.low >= first.low:
                    candidate.box_top = anchor.high
                    candidate.box_top_source_idx = anchor.index
                    candidate.box_top_source_time = anchor.display_time

        # Canonical confirmed-Reaction box ownership.  The directional
        # confirmation edge keeps the structure that discovered the Reaction:
        #   Bullish  -> BoxTop is the breakout edge.
        #   Bearish  -> BoxBottom is the breakdown edge.
        # The opposite edge belongs to First..exact-confirmation chronology.
        # Full main candles strictly before Break are eligible in full.  When
        # the Break candle itself owns the full-range opposite extreme, only
        # lower-timeframe prices up to and including the first strict
        # confirmation event may contribute.  Post-confirmation remainder
        # prices can never retroactively rewrite the Reaction/Order box.
        if candidate.break_idx is not None:
            first_index = int(candidate.first_idx)
            break_index = int(candidate.break_idx)
            break_candle = self.candles[break_index]
            if direction == "bullish":
                bottom, bottom_source = self.minimum_low(first_index, break_index)
                candidate.box_bottom = bottom
                candidate.box_bottom_source_idx = bottom_source.index
                candidate.box_bottom_source_time = bottom_source.display_time
                if bottom_source.index == break_index:
                    analysis = self.bull.breakout_analysis(candidate, break_candle)
                    if analysis is not None:
                        candidate.box_bottom = analysis.extreme
                        candidate.box_bottom_source_idx = analysis.extreme_source.index
                        candidate.box_bottom_source_time = analysis.extreme_source.display_time
            else:
                top, top_source = self.maximum_high(first_index, break_index)
                candidate.box_top = top
                candidate.box_top_source_idx = top_source.index
                candidate.box_top_source_time = top_source.display_time
                if top_source.index == break_index:
                    analysis = self.bear.breakdown_analysis(candidate, break_candle)
                    if analysis is not None:
                        candidate.box_top = analysis.extreme
                        candidate.box_top_source_idx = analysis.extreme_source.index
                        candidate.box_top_source_time = analysis.extreme_source.display_time

        self.all_reactions[direction].append(replace(candidate))
        return True

    def _append_reset(
        self,
        direction: str,
        candle: Candle,
        level: Decimal,
        first_idx: int,
        second_time: str | None = None,
    ) -> None:
        self.all_resets[direction].append(
            ResetEvent(
                index=candle.index,
                display_time=candle.display_time,
                second_time=second_time,
                broken_level=level,
                from_first_idx=first_idx,
            )
        )

    def _refine(
        self, direction: str, candidate: Candidate, candle: Candle
    ) -> IntrabarAnalysis | None:
        helper = self.bull if direction == "bullish" else self.bear
        analysis = (
            helper.breakout_analysis(candidate, candle)
            if direction == "bullish"
            else helper.breakdown_analysis(candidate, candle)
        )
        if analysis is None:
            return None
        if direction == "bullish" and candidate.box_bottom_source_idx == candle.index:
            candidate.box_bottom = analysis.extreme
            candidate.box_bottom_source_idx = analysis.extreme_source.index
            candidate.box_bottom_source_time = analysis.extreme_source.display_time
        if direction == "bearish" and candidate.box_top_source_idx == candle.index:
            candidate.box_top = analysis.extreme
            candidate.box_top_source_idx = analysis.extreme_source.index
            candidate.box_top_source_time = analysis.extreme_source.display_time
        return analysis

    def _candidate_from_confirmation_remainder(
        self,
        direction: str,
        confirmed: Candidate,
        candle: Candle,
        analysis: IntrabarAnalysis | None,
    ) -> Candidate | None:
        """Reuse a correctly colored confirmation candle for the next reaction."""
        required_tag = "RED" if direction == "bullish" else "GREEN"
        if candle.tag != required_tag or analysis is None:
            return None

        # The exact confirmation event splits the Break candle into two
        # ownership phases.  If its remainder strictly breaks the confirmed
        # opposite edge, that main candle belongs to Reset and cannot also be
        # reused as the First of the next Normal reaction.  ``analysis.extreme``
        # is the exact-confirmation opposite edge for both directions.
        remainder_start = analysis.event_second.timestamp + timedelta(microseconds=1)
        remainder_end = candle.timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, remainder_start)
        right = bisect.bisect_left(self.second_times, remainder_end)
        if direction == "bullish":
            if self.lower_index.first_less(left, right, analysis.extreme) is not None:
                return None
        else:
            if self.lower_index.first_greater(left, right, analysis.extreme) is not None:
                return None
        # A cross-direction Leg-Start confirmation candle may simultaneously
        # become the first candle of the next same-direction reaction. Its
        # decisive second belongs to the new box boundary, so no second,
        # still-more-extreme tick is required. Other confirmations retain the
        # ordinary fresh post-event boundary requirement.
        # Every confirmation opens Normal Search. If its main candle has the
        # required start color, that complete candle is the next First candle,
        # regardless of whether the confirmed reaction was Mode A or Mode B.
        whole_confirmation_candle = True
        remainder_start = (
            candle.timestamp
            if whole_confirmation_candle
            else analysis.event_second.timestamp + timedelta(microseconds=1)
        )
        remainder_end = candle.timestamp + self.timeframe
        seconds = list(self.seconds_between(remainder_start, remainder_end))
        if not seconds:
            return None
        if direction == "bullish":
            top_second = max(seconds, key=lambda item: (item.high, -item.timestamp.timestamp()))
            bottom_second = min(seconds, key=lambda item: (item.low, item.timestamp))
            if (
                not whole_confirmation_candle
                and top_second.high <= analysis.event_second.high
            ):
                return None
            return Candidate(
                first_idx=candle.index,
                first_time=candle.display_time,
                box_top_source_idx=candle.index,
                box_top_source_time=candle.display_time,
                box_top=top_second.high,
                box_bottom_source_idx=candle.index,
                box_bottom_source_time=candle.display_time,
                box_bottom=bottom_second.low,
                mode="B",
                intrabar_start=remainder_start,
            )
        bottom_second = min(seconds, key=lambda item: (item.low, item.timestamp))
        top_second = max(seconds, key=lambda item: (item.high, -item.timestamp.timestamp()))
        if (
            not whole_confirmation_candle
            and bottom_second.low >= analysis.event_second.low
        ):
            return None
        return Candidate(
            first_idx=candle.index,
            first_time=candle.display_time,
            box_top_source_idx=candle.index,
            box_top_source_time=candle.display_time,
            box_top=top_second.high,
            box_bottom_source_idx=candle.index,
            box_bottom_source_time=candle.display_time,
            box_bottom=bottom_second.low,
            mode="B",
            intrabar_start=remainder_start,
        )

    def _first_initial(self, direction: str) -> Candidate | None:
        initial_result = (
            self.bull.detect(first_only=True)
            if direction == "bullish"
            else self.bear.detect(first_only=True)
        )
        return (
            replace(initial_result.reactions[0])
            if initial_result.reactions
            else None
        )


    def _first_direct_same_direction_after_reset(
        self, direction: str, reset_index: int
    ) -> Candidate | None:
        """Return the first structurally owned reaction after Reset.

        The earliest eligible candidate owns the evolving leg until it either
        confirms or its outer leg boundary is strictly crossed. A nested local
        pattern cannot confirm while that owner is unresolved. If the boundary
        breaks first, restart strictly after that event. Bearish is the exact
        price/color mirror of Bullish.
        """
        context_tag = "GREEN" if direction == "bullish" else "RED"
        first_tag = "RED" if direction == "bullish" else "GREEN"
        blocked_through = reset_index

        for first_index in range(reset_index + 1, self.end_index + 1):
            first = self.candles[first_index]
            if first_index <= blocked_through:
                continue
            if first.tag != first_tag or self.candles[first_index - 1].tag != context_tag:
                continue

            candidate = self._build_direct_candidate(
                direction, reset_index, first_index
            )
            if candidate is None:
                continue
            confirmed, invalidation_index = self._scan_direct_candidate(
                direction, candidate, self.end_index
            )
            if confirmed is not None:
                return confirmed
            if invalidation_index is None:
                continue
            blocked_through = invalidation_index

        return None

    def _first_geometry_after_reset(
        self, direction: str, reset_index: int, end_index: int | None = None,
    ) -> Candidate | None:
        """Return the first complete raw Reaction geometry after a boundary.

        This bounded search intentionally ignores normal Reset/invalidation
        acceptance.  It is a geometry-only primitive: First/box/Break structure
        may be used as evidence even when normal Reaction lifecycle rules would
        later Reset or suppress that structure.
        """
        _lim = self.end_index if end_index is None else min(end_index, self.end_index)
        _ck = (direction, reset_index, _lim)
        if _ck in self._geometry_after_reset_cache:
            _cached = self._geometry_after_reset_cache[_ck]
            return replace(_cached) if _cached is not None else None
        first_tag = "RED" if direction == "bullish" else "GREEN"
        context_tag = "GREEN" if direction == "bullish" else "RED"
        limit = self.end_index if end_index is None else min(end_index, self.end_index)
        for first_index in range(reset_index + 1, limit + 1):
            if (
                self.candles[first_index].tag != first_tag
                or self.candles[first_index - 1].tag != context_tag
            ):
                continue
            candidate = self._build_direct_candidate(
                direction, reset_index, first_index
            )
            if candidate is None:
                continue
            for scan in range(first_index + 1, limit + 1):
                candle = self.candles[scan]
                if direction == "bullish":
                    if candle.low < candidate.box_bottom:
                        candidate.box_bottom = candle.low
                        candidate.box_bottom_source_idx = candle.index
                        candidate.box_bottom_source_time = candle.display_time
                    if candle.high > candidate.box_top:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        return candidate
                else:
                    if candle.high > candidate.box_top:
                        candidate.box_top = candle.high
                        candidate.box_top_source_idx = candle.index
                        candidate.box_top_source_time = candle.display_time
                    if candle.low < candidate.box_bottom:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        return candidate
        return None

    def first_geometry_after_reset(
        self, direction: str, reset_index: int, end_index: int
    ) -> Candidate | None:
        """Public lifecycle API for post-Reset geometry discovery."""
        return self._first_geometry_after_reset(direction, reset_index, end_index)


    def _reaction_break_indices(self, direction: str) -> list[int]:
        """Cached ascending `break_idx` values mirroring `all_reactions[direction]`.

        `all_reactions[direction]` is append-only and strictly non-decreasing
        in `break_idx`, so this index list can be reused via bisect instead of
        rescanning the full reaction history on every gate lookup.
        """
        reactions = self.all_reactions[direction]
        cached = self._reaction_break_index_cache.get(direction)
        if cached is not None and cached[0] == len(reactions):
            return cached[1]
        indices = [int(reaction.break_idx) for reaction in reactions]
        self._reaction_break_index_cache[direction] = (len(reactions), indices)
        return indices

    def first_order_reaction_after_gate(
        self,
        direction: str,
        gate_index: int,
        end_index: int | None = None,
        gate_event_time: datetime | None = None,
    ) -> Candidate | None:
        """Return direct Order_A geometry from continuous Reaction context."""
        limit = self.end_index if end_index is None else min(end_index, self.end_index)
        if gate_index < self.start_index or gate_index >= limit:
            return None

        def confirmed_no_later_than_gate(reaction: Candidate) -> bool:
            break_index = int(reaction.break_idx)
            if break_index < gate_index or gate_event_time is None:
                return break_index <= gate_index
            if break_index > gate_index:
                return False
            break_candle = self.candles[break_index]
            start = reaction.intrabar_start or break_candle.timestamp
            end = break_candle.timestamp + self.timeframe
            level = reaction.box_bottom if direction == "bearish" else reaction.box_top
            for lower in self.seconds_between(start, end):
                crossed = (
                    lower.low < level
                    if direction == "bearish"
                    else lower.high > level
                )
                if crossed:
                    return lower.timestamp <= gate_event_time
            return break_candle.timestamp <= gate_event_time

        reactions = self.all_reactions[direction]
        break_indices = self._reaction_break_indices(direction)
        # `break_indices` is non-decreasing and duplicate-free for this
        # engine's reaction stream. Keep only the owning position instead of
        # allocating the complete historical prefix on every gate lookup.
        cut = bisect.bisect_left(break_indices, gate_index)
        owner_position = cut - 1
        if cut < len(reactions) and break_indices[cut] == gate_index:
            if confirmed_no_later_than_gate(reactions[cut]):
                owner_position = cut
        search_start = gate_index + 1
        if owner_position < 0:
            result = self._earliest_confirmed_geometry(
                direction, search_start, limit
            )
            if result is not None:
                result.order_gate_decision = "no-history"
            return result

        owner = reactions[owner_position]
        boundary_end = max(int(owner.first_idx), gate_index - 1)
        gate = self.candles[gate_index]
        if direction == "bearish":
            outer_boundary, _ = self.maximum_high(
                int(owner.first_idx), boundary_end
            )
            gate_boundary = gate.low
        else:
            outer_boundary, _ = self.minimum_low(
                int(owner.first_idx), boundary_end
            )
            gate_boundary = gate.high

        event_start = gate_event_time or gate.timestamp
        event_end = self.candles[limit].timestamp + self.timeframe
        left = bisect.bisect_left(self.second_times, event_start)
        right = bisect.bisect_left(self.second_times, event_end)
        if left >= right:
            return None
        if direction == "bearish":
            outer_position = self.lower_index.first_greater(
                left, right, outer_boundary
            )
            gate_position = self.lower_index.first_less(
                left, right, gate_boundary
            )
        else:
            outer_position = self.lower_index.first_less(
                left, right, outer_boundary
            )
            gate_position = self.lower_index.first_greater(
                left, right, gate_boundary
            )
        if outer_position is None and gate_position is None:
            return None
        # Legacy loop checks the outer/restart predicate first inside each
        # lower-timeframe candle, so restart owns an exact-position tie.
        restart = outer_position is not None and (
            gate_position is None or outer_position <= gate_position
        )
        decision_position = outer_position if restart else gate_position
        assert decision_position is not None
        decision_time = self.second_times[decision_position]
        decision_kind = "restart" if restart else "continue"
        if decision_kind == "restart":
            source = self.main_source_for_time(decision_time)
            if source is None:
                return None
            search_start = int(source.index) + 1
        if search_start > limit:
            return None
        result = self._earliest_confirmed_geometry(
            direction, search_start, limit
        )
        if result is not None:
            result.order_gate_decision = decision_kind
            if decision_kind == "continue" and (
                result.anchor_idx is None or result.anchor_value is None
            ):
                # The gate-bounded geometry already carries the true current
                # forming-leg anchor when one was discovered.  Never overwrite
                # that provenance with an older Reset.  Reconstruction is only
                # a fallback for geometry that genuinely has no anchor.
                prior_resets = [
                    item for item in self.all_resets[direction]
                    if item.index < int(result.first_idx)
                ]
                if prior_resets:
                    reset_index = max(item.index for item in prior_resets)
                    if direction == "bullish":
                        boundary, source = self.minimum_low(
                            reset_index, int(result.first_idx) - 1
                        )
                    else:
                        boundary, source = self.maximum_high(
                            reset_index, int(result.first_idx) - 1
                        )
                    result.anchor_idx = source.index
                    result.anchor_value = boundary
                    result.leg_boundary_value = boundary
        return result

    def _earliest_confirmed_geometry(
        self, direction: str, start_index: int, end_index: int | None = None,
    ) -> Candidate | None:
        """Return the geometry whose strict confirmation occurs first.

        Multiple First candidates may overlap. Order-gender chronology belongs
        to the structure that completes first, not necessarily to the oldest
        still-unconfirmed First candle.
        """
        first_tag = "RED" if direction == "bullish" else "GREEN"
        context_tag = "GREEN" if direction == "bullish" else "RED"
        limit = self.end_index if end_index is None else min(end_index, self.end_index)
        active: list[Candidate] = []
        reset_index = max(self.start_index, start_index - 1)
        for scan in range(start_index, limit + 1):
            candle = self.candles[scan]
            if (
                scan > reset_index
                and candle.tag == first_tag
                and self.candles[scan - 1].tag == context_tag
            ):
                candidate = self._build_direct_candidate(
                    direction, reset_index, scan
                )
                if candidate is not None:
                    active.append(candidate)

            confirmed: list[Candidate] = []
            survivors: list[Candidate] = []
            for candidate in active:
                if scan <= candidate.first_idx:
                    survivors.append(candidate)
                    continue

                # Order geometry is still Reaction geometry.  A candidate that
                # strictly loses the floor/ceiling of the leg that owns it
                # before confirmation is dead; a later breakout/breakdown must
                # never resurrect that invalid structure as an Order Reaction.
                # When invalidation and confirmation compete inside one main
                # candle, the shared lower-timeframe resolver preserves exact
                # chronology (and invalidation-first on a finest-event tie).
                if self._owner_boundary_before_confirmation(
                    direction, candidate, candle
                ):
                    continue

                if direction == "bullish":
                    if candle.low < candidate.box_bottom:
                        candidate.box_bottom = candle.low
                        candidate.box_bottom_source_idx = candle.index
                        candidate.box_bottom_source_time = candle.display_time
                    if candle.high > candidate.box_top:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        confirmed.append(candidate)
                        continue
                else:
                    if candle.high > candidate.box_top:
                        candidate.box_top = candle.high
                        candidate.box_top_source_idx = candle.index
                        candidate.box_top_source_time = candle.display_time
                    if candle.low < candidate.box_bottom:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        self._refine(direction, candidate, candle)
                        confirmed.append(candidate)
                        continue
                survivors.append(candidate)
            active = survivors
            if confirmed:
                return min(confirmed, key=lambda item: item.first_idx)
        return None

    def _build_direct_candidate(
        self, direction: str, reset_index: int, first_index: int
    ) -> Candidate | None:
        context_tag = "GREEN" if direction == "bullish" else "RED"
        first_tag = "RED" if direction == "bullish" else "GREEN"
        first = self.candles[first_index]
        if (
            first_index <= reset_index
            or first.tag != first_tag
            or self.candles[first_index - 1].tag != context_tag
        ):
            return None

        context_start = first_index - 1
        while (
            context_start - 1 >= reset_index
            and self.candles[context_start - 1].tag == context_tag
        ):
            context_start -= 1
        local_start = context_start
        while (
            local_start - 1 >= reset_index
            and self.candles[local_start - 1].tag == first_tag
        ):
            local_start -= 1

        if direction == "bullish":
            local_floor, _ = self.minimum_low(local_start, first_index - 1)
            if first.low < local_floor:
                return None
            box_top, top_source = self.maximum_high(context_start, first_index)
            leg_boundary, leg_source = self.minimum_low(
                reset_index, first_index - 1
            )
            return Candidate(
                first_index, first.display_time,
                top_source.index, top_source.display_time, box_top,
                first_index, first.display_time, first.low,
                mode="A", anchor_idx=leg_source.index,
                anchor_value=leg_boundary, leg_boundary_value=leg_boundary,
            )

        local_ceiling, _ = self.maximum_high(local_start, first_index - 1)
        if first.high > local_ceiling:
            return None
        box_bottom, bottom_source = self.minimum_low(context_start, first_index)
        leg_boundary, leg_source = self.maximum_high(
            reset_index, first_index - 1
        )
        return Candidate(
            first_index, first.display_time,
            first_index, first.display_time, first.high,
            bottom_source.index, bottom_source.display_time, box_bottom,
            mode="A", anchor_idx=leg_source.index,
            anchor_value=leg_boundary, leg_boundary_value=leg_boundary,
        )


    def _scan_direct_candidate(
        self, direction: str, candidate: Candidate, stop_index: int
    ) -> tuple[Candidate | None, int | None]:
        for scan in range(candidate.first_idx + 1, stop_index + 1):
            candle = self.candles[scan]
            confirms = (
                candle.high > candidate.box_top
                if direction == "bullish"
                else candle.low < candidate.box_bottom
            )
            invalidates = self._owner_boundary_before_confirmation(
                direction, candidate, candle
            )
            if invalidates:
                return None, scan
            if direction == "bullish" and candle.low < candidate.box_bottom:
                candidate.box_bottom = candle.low
                candidate.box_bottom_source_idx = candle.index
                candidate.box_bottom_source_time = candle.display_time
            if direction == "bearish" and candle.high > candidate.box_top:
                candidate.box_top = candle.high
                candidate.box_top_source_idx = candle.index
                candidate.box_top_source_time = candle.display_time
            if confirms:
                candidate.break_idx = scan
                candidate.break_time = candle.display_time
                self._refine(direction, candidate, candle)
                return candidate, None
        return None, None

    def _owner_boundary_before_confirmation(
        self, direction: str, candidate: Candidate, candle: Candle
    ) -> bool:
        """Return whether structural alignment is lost before confirmation.

        A Bearish Leg-Start Top must not rise above its outer ceiling.
        A Bullish Leg-Start Bottom must not fall below its outer floor.
        Equality preserves the unresolved candidate. If a strict invalidation
        competes with confirmation in the same main candle, ordered one-second
        data decides which event occurred first.
        """
        boundary = candidate.leg_boundary_value
        if boundary is None:
            return False

        if direction == "bullish":
            reaches_boundary = candle.low < boundary
            confirms = candle.high > candidate.box_top
        else:
            reaches_boundary = candle.high > boundary
            confirms = candle.low < candidate.box_bottom
        if not reaches_boundary:
            return False
        if not confirms:
            return True

        end = candle.timestamp + self.timeframe
        for second in self.seconds_between(candle.timestamp, end):
            if direction == "bullish":
                if second.low < boundary:
                    return True
                if second.high > candidate.box_top:
                    return False
            else:
                if second.high > boundary:
                    return True
                if second.low < candidate.box_bottom:
                    return False
        return True


    def _result(self) -> DetectionResult:
        return DetectionResult(
            direction=self.output_direction,
            reactions=self.all_reactions[self.output_direction],
            resets=self.all_resets[self.output_direction],
            start_index=self.start_index,
            end_index=self.end_index,
        )

    def detect(
        self, *, stop_after_first_at_or_after: int | None = None
    ) -> DetectionResult:
        direction = self.output_direction
        initial = self._first_initial(direction)
        if initial is None:
            return DetectionResult(
                direction=direction,
                reactions=[],
                resets=[],
                start_index=self.start_index,
                end_index=self.end_index,
            )
        self._append_reaction(direction, initial)
        if (
            stop_after_first_at_or_after is not None
            and initial.first_idx >= stop_after_first_at_or_after
        ):
            return self._result()
        previous = initial
        index = initial.break_idx + 1
        running_value = (
            self.candles[initial.break_idx].high
            if direction == "bullish"
            else self.candles[initial.break_idx].low
        )
        running_source = initial.break_idx
        candidate: Candidate | None = None
        initial_break_candle = self.candles[initial.break_idx]
        initial_helper = self.bull if direction == "bullish" else self.bear
        initial_analysis = (
            initial_helper.breakout_analysis(initial, initial_break_candle)
            if direction == "bullish"
            else initial_helper.breakdown_analysis(initial, initial_break_candle)
        )
        # Exact-confirmation geometry owns the post-confirmation remainder in
        # both directions. ``_append_reaction`` may later expand the public
        # opposite edge with the complete Break main candle, but that later
        # presentation geometry must never erase a Reset that occurred after
        # exact confirmation inside the same candle.
        initial_reset_level = (
            initial_analysis.extreme
            if initial_analysis is not None
            else (initial.box_bottom if direction == "bullish" else initial.box_top)
        )
        initial_reset_second = (
            initial_helper.post_breakout_reset(
                initial_analysis, initial_reset_level, initial_break_candle
            )
            if direction == "bullish"
            else initial_helper.post_breakdown_reset(
                initial_analysis, initial_reset_level, initial_break_candle
            )
        )
        pending_reset_index = (
            initial.break_idx if initial_reset_second is not None else None
        )
        if initial_reset_second is not None:
            self._append_reset(
                direction,
                initial_break_candle,
                initial_reset_level,
                initial.first_idx,
                initial_reset_second.display_time,
            )

        while index <= self.end_index:
            candle = self.candles[index]
            reset = pending_reset_index is not None or (
                candle.low < previous.box_bottom
                if direction == "bullish"
                else candle.high > previous.box_top
            )
            candidate_break = candidate is not None and (
                candle.high > candidate.box_top
                if direction == "bullish"
                else candle.low < candidate.box_bottom
            )
            if reset and candidate_break:
                if direction == "bullish":
                    reset = self.bull.confirmed_reset_before_breakout(
                        candidate, candle, previous.box_bottom
                    )
                else:
                    reset = self.bear.confirmed_reset_before_breakdown(
                        candidate, candle, previous.box_top
                    )
            if reset:
                reset_index = (
                    pending_reset_index
                    if pending_reset_index is not None
                    else index
                )
                reset_candle = self.candles[reset_index]
                pending_reset_index = None
                level = previous.box_bottom if direction == "bullish" else previous.box_top
                already_recorded = (
                    self.all_resets[direction]
                    and self.all_resets[direction][-1].from_first_idx
                    == previous.first_idx
                )
                if not already_recorded:
                    self._append_reset(
                        direction, reset_candle, level, previous.first_idx
                    )
                # A Reset reopens the ordinary same-direction ownership gate.
                # The geometric relaxation belongs only to the cross-direction
                # structural/E path and must not relabel every normal Reset.
                direct_candidate = self._first_direct_same_direction_after_reset(
                    direction, reset_index
                )
                # Both paths are valid interpretations of the same requested-
                # direction restart. The chronologically first confirmation
                # wins; a later Anchor-based candidate must never hide an
                # already complete direct post-Reset color sequence.
                structural = direct_candidate
                if structural is None or structural.break_idx is None:
                    break
                structural.mode = "A"
                structural.cross_direction_origin = False
                structural.cross_direction_chain_owner = False
                if not self._append_reaction(direction, structural):
                    candidate = None
                    index = structural.break_idx + 1
                    pending_reset_index = structural.break_idx
                    continue
                if (
                    stop_after_first_at_or_after is not None
                    and structural.first_idx >= stop_after_first_at_or_after
                ):
                    return self._result()
                previous = structural
                index = structural.break_idx + 1
                running_value = (
                    self.candles[structural.break_idx].high
                    if direction == "bullish"
                    else self.candles[structural.break_idx].low
                )
                running_source = structural.break_idx
                break_candle = self.candles[structural.break_idx]
                helper = self.bull if direction == "bullish" else self.bear
                analysis = (
                    helper.breakout_analysis(structural, break_candle)
                    if direction == "bullish"
                    else helper.breakdown_analysis(structural, break_candle)
                )
                reset_level = (
                    analysis.extreme
                    if analysis is not None
                    else (
                        structural.box_bottom
                        if direction == "bullish"
                        else structural.box_top
                    )
                )
                post_reset_second = (
                    helper.post_breakout_reset(
                        analysis, reset_level, break_candle
                    )
                    if direction == "bullish"
                    else helper.post_breakdown_reset(
                        analysis, reset_level, break_candle
                    )
                )
                if post_reset_second is not None:
                    self._append_reset(
                        direction,
                        break_candle,
                        reset_level,
                        structural.first_idx,
                        post_reset_second.display_time,
                    )
                    # The confirmation candle has already reset the reaction
                    # after its exact intrabar confirmation. Its remainder
                    # cannot seed a Normal successor. Restart from the next
                    # main candle as a fresh Leg-Start search.
                    candidate = None
                    pending_reset_index = structural.break_idx
                else:
                    candidate = self._candidate_from_confirmation_remainder(
                        direction, structural, break_candle, analysis
                    )
                continue

            if candidate is not None:
                if direction == "bullish":
                    if candle.low < candidate.box_bottom:
                        candidate.box_bottom = candle.low
                        candidate.box_bottom_source_idx = candle.index
                        candidate.box_bottom_source_time = candle.display_time
                    if candle.high > candidate.box_top:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        analysis = self._refine(direction, candidate, candle)
                        reset_level = (
                            analysis.extreme if analysis is not None else candidate.box_bottom
                        )
                        post_reset_second = self.bull.post_breakout_reset(
                            analysis, reset_level, candle
                        )
                        self._append_reaction(direction, candidate)
                        if (
                            stop_after_first_at_or_after is not None
                            and candidate.first_idx >= stop_after_first_at_or_after
                        ):
                            return self._result()
                        previous = replace(candidate)
                        running_value = candle.high
                        running_source = candle.index
                        if post_reset_second is not None:
                            self._append_reset(
                                direction,
                                candle,
                                reset_level,
                                previous.first_idx,
                                post_reset_second.display_time,
                            )
                            candidate = None
                            pending_reset_index = candle.index
                        else:
                            candidate = self._candidate_from_confirmation_remainder(
                                direction, previous, candle, analysis
                            )
                else:
                    if candle.high > candidate.box_top:
                        candidate.box_top = candle.high
                        candidate.box_top_source_idx = candle.index
                        candidate.box_top_source_time = candle.display_time
                    if candle.low < candidate.box_bottom:
                        candidate.break_idx = candle.index
                        candidate.break_time = candle.display_time
                        analysis = self._refine(direction, candidate, candle)
                        reset_level = (
                            analysis.extreme if analysis is not None else candidate.box_top
                        )
                        post_reset_second = self.bear.post_breakdown_reset(
                            analysis, reset_level, candle
                        )
                        self._append_reaction(direction, candidate)
                        if (
                            stop_after_first_at_or_after is not None
                            and candidate.first_idx >= stop_after_first_at_or_after
                        ):
                            return self._result()
                        previous = replace(candidate)
                        running_value = candle.low
                        running_source = candle.index
                        if post_reset_second is not None:
                            self._append_reset(
                                direction,
                                candle,
                                reset_level,
                                previous.first_idx,
                                post_reset_second.display_time,
                            )
                            candidate = None
                            pending_reset_index = candle.index
                        else:
                            candidate = self._candidate_from_confirmation_remainder(
                                direction, previous, candle, analysis
                            )
            else:
                if direction == "bullish" and candle.tag == "RED":
                    top = max(running_value, candle.high)
                    top_source = running_source if running_value >= candle.high else candle.index
                    bottom_start = top_source + 1 if top_source < candle.index else candle.index
                    bottom, bottom_source = self.minimum_low(bottom_start, candle.index)
                    candidate = Candidate(
                        candle.index,
                        candle.display_time,
                        top_source,
                        self.candles[top_source].display_time,
                        top,
                        bottom_source.index,
                        bottom_source.display_time,
                        bottom,
                        mode="B",
                    )
                elif direction == "bearish" and candle.tag == "GREEN":
                    bottom = min(running_value, candle.low)
                    bottom_source = running_source if running_value <= candle.low else candle.index
                    top_start = bottom_source + 1 if bottom_source < candle.index else candle.index
                    top, top_source = self.maximum_high(top_start, candle.index)
                    candidate = Candidate(
                        candle.index,
                        candle.display_time,
                        top_source.index,
                        top_source.display_time,
                        top,
                        bottom_source,
                        self.candles[bottom_source].display_time,
                        bottom,
                        mode="B",
                    )
            if direction == "bullish" and (running_value is None or candle.high > running_value):
                running_value, running_source = candle.high, candle.index
            if direction == "bearish" and (running_value is None or candle.low < running_value):
                running_value, running_source = candle.low, candle.index
            index += 1

        return self._result()


````
<!-- EXACT-SOURCE-END:pipeline/reaction_engine.py -->

### 16.13 `pipeline/s_zone_detector.py` — S

**SHA-256:** `ef71a2e4176caaabc25d1ef0c1f0f24efb54ed3110982cdb7cf52d2449cca2ee`  
**Bytes:** `60888`  
**LF count:** `1444`

<!-- EXACT-SOURCE-BEGIN:pipeline/s_zone_detector.py -->
````python
"""S-zone calculation from authoritative A, Reaction, Blue, and Order state.

Owns A-to-S handoff, S Red/Blue Simple/Advanced/Type3 formation, S decision
chronology, and shared accepted-Order stop reconciliation. The Order module
owns physical creation and the initial audit of stopped A zones. Larger
E/StopAll arbitration remains lifecycle-owned.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Callable, Sequence

from core_utils import as_decimal
from order_audit_engine import SOrderAuditMixin
from direction_policy import policy_for


S_ZONE_VERSION = "4.20.0"
S_ZONE_IMPLEMENTATION_VERSION = "4.21.0"
S_ZONE_LAST_MODIFIED = "2026-09-27 23:17:17 +03:30"


@dataclass(frozen=True, slots=True)
class SZone:
    direction: str
    color: str
    formation_type: str
    a_ordinal: int
    a_source_index: int
    a_source_time: datetime
    a_price: Decimal
    a_stop_index: int
    a_stop_time: datetime
    a_stop_event_time: datetime
    order_direction: str | None
    order_reaction_number: int | None
    order_mode: str | None
    order_first_index: int | None
    order_first_time: datetime | None
    order_break_index: int | None
    order_break_time: datetime | None
    order_confirmation_time: datetime | None
    order_box_top: Decimal | None
    order_box_top_source_index: int | None
    order_box_top_source_time: datetime | None
    order_box_bottom: Decimal | None
    order_box_bottom_source_index: int | None
    order_box_bottom_source_time: datetime | None
    order_stop_level: Decimal | None
    order_stop_source_index: int | None
    order_stop_source_time: datetime | None
    reset_reaction_number: int | None
    reset_time: datetime | None
    source_index: int
    source_time: datetime
    price: Decimal
    decision_index: int
    decision_time: datetime
    decision_event_time: datetime


class SZoneDetector(SOrderAuditMixin):
    def __init__(
        self,
        direction: str,
        trend_reactions: Sequence[object],
        opposite_reactions: Sequence[object],
        trend_blue_lines: Sequence[object],
        a_zones: Sequence[object],
        chronology: object,
        start_index: int | None = None,
        end_index: int | None = None,
        opposite_resets: Sequence[object] = (),
        initial_order_geometry: Callable[[int, datetime, int], object | None] | None = None,
    ) -> None:
        if direction not in {"bullish", "bearish"}:
            raise ValueError("Direction must be 'bullish' or 'bearish'.")
        self.direction = direction
        self.policy = policy_for(direction)
        self.order_direction = chronology.opposite_direction(direction)
        self.trend_reactions = list(trend_reactions)
        self.opposite_reactions = list(opposite_reactions)
        self.opposite_resets = list(opposite_resets)
        self.initial_order_geometry = initial_order_geometry
        self.trend_blue_lines = list(trend_blue_lines)
        self.a_zones = sorted(
            a_zones,
            key=lambda item: (
                getattr(item, "reaction_break_time"),
                int(getattr(item, "source_index")),
            ),
        )
        self.chronology = chronology
        self.candles = chronology.candles
        self.lower = chronology.seconds
        self.timeframe = chronology.timeframe
        self.candle_times = chronology.times
        self.lower_times = chronology.second_times
        self.lower_index = chronology.lower_index
        self.start_index = 0 if start_index is None else int(start_index)
        self.end_index = (
            len(self.candles) - 1 if end_index is None else int(end_index)
        )
        if not 0 <= self.start_index <= self.end_index < len(self.candles):
            raise ValueError("Invalid S analysis range.")
        self.range_start = self.candle_times[self.start_index]
        self.range_end = self.candle_times[self.end_index] + self.timeframe
        self.order_audit: dict[tuple[int, int], dict[str, object]] = {}
        # The exact A-stop handoff and the post-decision live-S interval are
        # distinct ownership phases.  Pre-decision handoff keeps Behavior
        # Independence for candidates opened after the A stop; once S is
        # decided, ordinary A re-entry is blocked until the S strict stop.
        self.a_ownership_windows: list[tuple[datetime, datetime | None]] = []
        self._reset_blue_formation_by_reaction: dict[int, datetime] = {}
        self._opposite_by_first_index = {
            int(getattr(item, "first_idx")): (number, item)
            for number, item in enumerate(self.opposite_reactions, start=1)
        }
        # Performance implementation detail: the authoritative Order chronology
        # is immutable for this detector run. Build its exact legacy sort order
        # once, then bisect/cache A-stop lookups instead of re-scanning and
        # re-sorting the complete opposite-Reaction history for every A.
        self._opposite_order_matches = sorted(
            (
                self._reaction_confirmation_time(item, self.order_direction),
                int(getattr(item, "first_idx")),
                int(getattr(item, "break_idx")),
                number,
                item,
            )
            for number, item in enumerate(self.opposite_reactions, start=1)
        )
        self._opposite_order_confirmation_times = [
            item[0] for item in self._opposite_order_matches
        ]
        self._order_matches_after_cache: dict[
            datetime, tuple[tuple[int, object, datetime], ...]
        ] = {}

        for line in self.trend_blue_lines:
            if not bool(getattr(line, "calculation_valid", True)):
                continue
            if str(getattr(line, "kind")) != "reset":
                continue
            reaction_number = int(getattr(line, "reaction_number"))
            if reaction_number not in self._reset_blue_formation_by_reaction:
                self._reset_blue_formation_by_reaction[reaction_number] = (
                    self._blue_formation_time(line)
                )

        # Performance implementation detail: immutable chronology indexes.
        # They preserve the exact legacy sort keys and are scoped to this run.
        self._trend_ordered = sorted(
            (
                self._reaction_confirmation_time(item, self.direction),
                int(getattr(item, "first_idx")),
                int(getattr(item, "break_idx")),
                number,
                item,
            )
            for number, item in enumerate(self.trend_reactions, start=1)
        )
        self._trend_ordered_confirmation_times = [item[0] for item in self._trend_ordered]
        self._trend_confirmation_times_sorted = sorted(
            item[0] for item in self._trend_ordered
        )
        self._opposite_confirmation_by_first = {
            int(getattr(item, "first_idx")): self._reaction_confirmation_time(
                item, self.order_direction
            )
            for item in self.opposite_reactions
        }
        self._opposite_reset_events = sorted(
            ((self._reset_time(reset), reset) for reset in self.opposite_resets),
            key=lambda item: item[0],
        )
        self._opposite_reset_event_times = [item[0] for item in self._opposite_reset_events]
        self._opposite_reset_times_by_owner: dict[int, list[datetime]] = {}
        for reset_time, reset in self._opposite_reset_events:
            self._opposite_reset_times_by_owner.setdefault(
                int(getattr(reset, "from_first_idx")), []
            ).append(reset_time)
        self._public_blue_formation_times = sorted(
            self._blue_formation_time(line)
            for line in self.trend_blue_lines
            if bool(getattr(line, "calculation_valid", True))
            and not bool(getattr(line, "behavior_internal", False))
        )

    def _main_index(self, timestamp: datetime) -> int:
        return self.chronology.main_index(timestamp)

    def _lower_window(
        self, start: datetime, end: datetime | None
    ) -> Sequence[object]:
        return self.chronology.lower_window(start, end)

    def _reaction_confirmation_time(
        self, reaction: object, direction: str
    ) -> datetime:
        return self.chronology.reaction_confirmation(direction, reaction)

    def reaction_confirmation_time(
        self, reaction: object, direction: str
    ) -> datetime:
        """Public chronology API used by cross-stage lifecycle ownership."""
        return self._reaction_confirmation_time(reaction, direction)


    def _reset_time(self, reset: object) -> datetime:
        return self.chronology.reset_time(reset)

    def _a_confirmation_time(self, zone: object) -> datetime:
        number = int(getattr(zone, "reaction_number"))
        if number < 1 or number > len(self.trend_reactions):
            raise ValueError("A refers to a missing trend reaction.")
        return self._reaction_confirmation_time(
            self.trend_reactions[number - 1], self.direction
        )

    def _trend_extreme(self, candle: object) -> Decimal:
        return as_decimal(
            getattr(candle, self.policy.extreme_attr)
        )

    def _a_stopped(self, value: Decimal, level: Decimal) -> bool:
        return self.policy.strict_cross(value, level)

    def _first_a_stop(
        self, level: Decimal, start: datetime
    ) -> tuple[int, datetime, datetime] | None:
        scan_start = max(start, self.range_start)
        left = bisect_left(self.lower_times, scan_start)
        right = bisect_left(self.lower_times, self.range_end)
        if right > left and self.lower_index is not None:
            position = (
                self.lower_index.first_less(left, right, level)
                if self.direction == "bullish"
                else self.lower_index.first_greater(left, right, level)
            )
            if position is None:
                return None
            event_time = self.lower_times[position]
            index = self._main_index(event_time)
            return index, getattr(self.candles[index], "timestamp"), event_time

        lower_items = self.lower[left:right]
        for item in lower_items:
            if self._a_stopped(self._trend_extreme(item), level):
                event_time = getattr(item, "timestamp")
                index = self._main_index(event_time)
                return index, getattr(self.candles[index], "timestamp"), event_time
        if lower_items:
            return None
        start_index = max(self.start_index, bisect_left(self.candle_times, start))
        for item in self.candles[start_index : self.end_index + 1]:
            if self._a_stopped(self._trend_extreme(item), level):
                return (
                    int(getattr(item, "index")),
                    getattr(item, "timestamp"),
                    getattr(item, "timestamp"),
                )
        return None

    def first_a_stop(
        self, level: Decimal, start: datetime
    ) -> tuple[int, datetime, datetime] | None:
        """Public lifecycle API for the first strict A stop."""
        return self._first_a_stop(level, start)


    def _resolved_order_backed_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        first_order_match: tuple[int, object, datetime],
    ) -> SZone | None:
        """Resolve S using only the first physical Order_A owned by this A.

        The initial stopped-A OrderAudit retains its original parent-stop
        cause.  A later canonical Reaction never replaces the original
        Order_A, irrespective of its native Reaction Mode or S decision time.
        """
        return self._build_order_backed_zone(
            zone, a_ordinal, a_price, a_stop, first_order_match
        )


    def _candidate_source(
        self, start_index: int, end_index: int
    ) -> tuple[int, datetime, Decimal]:
        if end_index < start_index:
            raise ValueError("S candidate range ends before the A stop.")
        source = self.candles[start_index]
        value = self._trend_extreme(source)
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = self._trend_extreme(item)
            better = self.policy.better_extreme(candidate, value)
            if better:
                source = item
                value = candidate
        return int(getattr(source, "index")), getattr(source, "timestamp"), value

    def _candidate_source_last(
        self, start_index: int, end_index: int
    ) -> tuple[int, datetime, Decimal]:
        """Return the directional extreme, assigning equality to the last candle."""
        if end_index < start_index:
            raise ValueError("S candidate range ends before it starts.")
        source = self.candles[start_index]
        value = self._trend_extreme(source)
        for item in self.candles[start_index + 1 : end_index + 1]:
            candidate = self._trend_extreme(item)
            better_or_equal = (
                candidate <= value
                if self.direction == "bullish"
                else candidate >= value
            )
            if better_or_equal:
                source = item
                value = candidate
        return int(getattr(source, "index")), getattr(source, "timestamp"), value

    def _first_trend_reaction_after_order(
        self, order_confirmation_time: datetime
    ) -> tuple[int, object, datetime] | None:
        for number, reaction in enumerate(self.trend_reactions, start=1):
            confirmation = self._reaction_confirmation_time(
                reaction, self.direction
            )
            if confirmation > order_confirmation_time:
                return number, reaction, confirmation
        return None


    def _nested_trend_reaction(
        self, order: object, order_confirmation_time: datetime
    ) -> tuple[int, object, datetime] | None:
        order_first_index = int(getattr(order, "first_idx"))
        order_break_index = int(getattr(order, "break_idx"))
        order_first = getattr(self.candles[order_first_index], "timestamp")
        order_top = as_decimal(getattr(order, "box_top"))
        order_bottom = as_decimal(getattr(order, "box_bottom"))
        for number, reaction in enumerate(self.trend_reactions, start=1):
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            first = getattr(self.candles[first_index], "timestamp")
            if (
                first <= order_first
                or first_index <= order_first_index
                or break_index > order_break_index
                or first >= order_confirmation_time
            ):
                continue
            confirmation = self._reaction_confirmation_time(
                reaction, self.direction
            )
            wholly_inside = (
                as_decimal(getattr(reaction, "box_top")) <= order_top
                and as_decimal(getattr(reaction, "box_bottom")) >= order_bottom
            )
            if confirmation <= order_confirmation_time and wholly_inside:
                return number, reaction, confirmation
        return None

    def _simple_candidate(
        self, order: object, reaction: object
    ) -> tuple[int, datetime, Decimal]:
        """Use the inclusive order-Break to aligned-Break interval."""
        return self._candidate_source_last(
            int(getattr(order, "break_idx")),
            int(getattr(reaction, "break_idx")),
        )

    def _type3_reset_leg(
        self, reset: object
    ) -> tuple[int, datetime, Decimal] | None:
        """Return the independent Type-3 inclusive Break-to-Reset geometry."""
        owner_match = self._opposite_by_first_index.get(
            int(getattr(reset, "from_first_idx"))
        )
        if owner_match is None:
            return None
        _, owner = owner_match
        start_index = int(getattr(owner, "break_idx"))
        end_index = self._main_index(self._reset_time(reset))
        if end_index < start_index:
            return None
        return self._candidate_source_last(start_index, end_index)

    def _type3_has_trend_reaction(
        self, a_stop_event: datetime, crossing: datetime
    ) -> bool:
        position = bisect_right(self._trend_confirmation_times_sorted, a_stop_event)
        return (
            position < len(self._trend_confirmation_times_sorted)
            and self._trend_confirmation_times_sorted[position] <= crossing
        )

    def _first_type3(
        self,
        a_stop_event: datetime,
        deadline: datetime,
    ) -> tuple[int, datetime, Decimal, int, datetime, int, datetime, datetime] | None:
        """Find the first no-order Type-3 Reset-leg S decision before a new order."""
        winner = None
        left = bisect_right(self._opposite_reset_event_times, a_stop_event)
        right = bisect_left(self._opposite_reset_event_times, deadline)
        for reset_time, reset in self._opposite_reset_events[left:right]:
            owner_first = int(getattr(reset, "from_first_idx"))
            owner_confirmation = self._opposite_confirmation_by_first.get(owner_first)
            if owner_confirmation is None or owner_confirmation > a_stop_event:
                continue
            owner_resets = self._opposite_reset_times_by_owner.get(owner_first, ())
            if owner_resets and owner_resets[0] <= a_stop_event:
                continue
            leg = self._type3_reset_leg(reset)
            if leg is None:
                continue
            source_index, source_time, boundary = leg
            lower_left = bisect_left(self.lower_times, reset_time)
            lower_right = bisect_left(self.lower_times, deadline)
            crossing_position = (
                self.lower_index.first_less(lower_left, lower_right, boundary)
                if self.direction == "bullish"
                else self.lower_index.first_greater(lower_left, lower_right, boundary)
            )
            if crossing_position is None:
                continue
            crossing = self.lower_times[crossing_position]
            if not self._type3_has_trend_reaction(a_stop_event, crossing):
                continue
            decision_index = self._main_index(crossing)
            owner_number = self._opposite_by_first_index[owner_first][0]
            candidate = (
                source_index,
                source_time,
                boundary,
                decision_index,
                getattr(self.candles[decision_index], "timestamp"),
                owner_number,
                reset_time,
                crossing,
            )
            if winner is None or candidate[-1] < winner[-1]:
                winner = candidate
        return winner


    def _type4_has_blue(
        self, candidate_source_index: int, crossing_event: datetime
    ) -> bool:
        """Return whether a public calculation-valid Blue exists in Type-4 window."""
        window_start = self.candle_times[candidate_source_index]
        position = bisect_left(self._public_blue_formation_times, window_start)
        return (
            position < len(self._public_blue_formation_times)
            and self._public_blue_formation_times[position] <= crossing_event
        )

    def _first_type4(
        self,
        a_stop: tuple[int, datetime, datetime],
        deadline: datetime,
    ) -> tuple[int, datetime, Decimal, int, datetime, int, datetime] | None:
        """Find the first order-free S Blue Type-4 decision after A stop.

        Bearish: from the A-stop main candle through the Breakout main candle
        of the latest confirmed Bearish Reaction, the maximum High is the
        current S candidate. Bullish mirrors with minimum Low. The candidate is
        valid only while no opposite Order has formed. If it strict-crosses
        without a qualifying Blue, no S is emitted; a later aligned Reaction
        replaces it with a freshly calculated candidate over the same A-stop
        origin.
        """
        a_stop_index, _a_stop_time, a_stop_event = a_stop
        left = bisect_right(self._trend_ordered_confirmation_times, a_stop_event)
        right = bisect_left(self._trend_ordered_confirmation_times, deadline)
        aligned = [
            (confirmation, number, reaction)
            for confirmation, _first, break_index, number, reaction
            in self._trend_ordered[left:right]
            if break_index >= a_stop_index
        ]

        for position, (confirmation, reaction_number, reaction) in enumerate(aligned):
            break_index = int(getattr(reaction, "break_idx"))
            source_index, source_time, candidate_level = self._candidate_source_last(
                a_stop_index, break_index
            )
            candidate_event = self._candidate_event_time(
                source_index, candidate_level, a_stop_event
            )
            search_start = max(confirmation, candidate_event, a_stop_event)
            next_confirmation = (
                aligned[position + 1][0]
                if position + 1 < len(aligned)
                else deadline
            )
            search_end = min(deadline, next_confirmation)
            if search_start >= search_end:
                continue

            lower_left = bisect_left(self.lower_times, search_start)
            lower_right = bisect_left(self.lower_times, search_end)
            crossing_position = (
                self.lower_index.first_less(lower_left, lower_right, candidate_level)
                if self.direction == "bullish"
                else self.lower_index.first_greater(lower_left, lower_right, candidate_level)
            )
            if crossing_position is None:
                continue
            crossing_event = self.lower_times[crossing_position]
            if not self._type4_has_blue(source_index, crossing_event):
                # The candidate failed without Blue.  While no Order exists,
                # the next aligned Reaction will transfer/rebuild the candidate.
                continue

            decision_index = self._main_index(crossing_event)
            return (
                source_index,
                source_time,
                candidate_level,
                decision_index,
                getattr(self.candles[decision_index], "timestamp"),
                reaction_number,
                crossing_event,
            )
        return None

    def _build_type4_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        type4: tuple[int, datetime, Decimal, int, datetime, int, datetime],
    ) -> SZone:
        """Build the order-free Blue Type-4 continuation for one stopped A."""
        a_stop_index, a_stop_time, a_stop_event_time = a_stop
        (
            source_index, source_time, price, decision_index, decision_time,
            _trend_reaction_number, decision_event_time,
        ) = type4
        return SZone(
            direction=self.direction,
            color="blue",
            formation_type="type4",
            a_ordinal=a_ordinal,
            a_source_index=int(getattr(zone, "source_index")),
            a_source_time=getattr(zone, "source_time"),
            a_price=a_price,
            a_stop_index=a_stop_index,
            a_stop_time=a_stop_time,
            a_stop_event_time=a_stop_event_time,
            order_direction=None,
            order_reaction_number=None,
            order_mode=None,
            order_first_index=None,
            order_first_time=None,
            order_break_index=None,
            order_break_time=None,
            order_confirmation_time=None,
            order_box_top=None,
            order_box_top_source_index=None,
            order_box_top_source_time=None,
            order_box_bottom=None,
            order_box_bottom_source_index=None,
            order_box_bottom_source_time=None,
            order_stop_level=None,
            order_stop_source_index=None,
            order_stop_source_time=None,
            reset_reaction_number=None,
            reset_time=None,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event_time,
        )


    def _candidate_after_order(
        self,
        order_confirmation_time: datetime,
        reaction: object,
    ) -> tuple[int, datetime, Decimal]:
        """Find a candidate strictly after the order is confirmed.

        A reaction anchor is authoritative only when it is also after the
        order confirmation.  Otherwise the earliest extreme in the candles
        following the confirmation through the reaction First owns the
        candidate.
        """
        first_index = int(getattr(reaction, "first_idx"))
        start_index = bisect_left(self.candle_times, order_confirmation_time)
        start_index = max(self.start_index, min(start_index, first_index))
        anchor_index = getattr(reaction, "anchor_idx", None)
        anchor_value = getattr(reaction, "anchor_value", None)
        if anchor_index is not None and int(anchor_index) >= start_index:
            source = self.candles[int(anchor_index)]
            return (
                int(anchor_index),
                getattr(source, "timestamp"),
                as_decimal(anchor_value),
            )
        candidate = self._candidate_source(start_index, first_index)
        containing_index = self._main_index(order_confirmation_time)
        if containing_index < start_index:
            # Do not discard the valid remainder of an intrabar confirmation
            # candle, or import an extreme that occurred before confirmation.
            remainder = self._lower_window(
                order_confirmation_time,
                self.candle_times[containing_index] + self.timeframe,
            )
            for item in remainder:
                value = self._trend_extreme(item)
                if self._a_stopped(value, candidate[2]) or value == candidate[2]:
                    candidate = (
                        containing_index, self.candle_times[containing_index], value
                    )
        return candidate

    def _a_source_event_time(self, zone: object) -> datetime:
        """Locate the source extreme, including an A-stop main candle."""
        source = getattr(zone, "source_time")
        price = as_decimal(getattr(zone, "price"))
        for item in self._lower_window(source, source + self.timeframe):
            if self._trend_extreme(item) == price:
                return getattr(item, "timestamp")
        return source

    def _a_owned_by_s(self, zone: object) -> bool:
        event_time = self._a_source_event_time(zone)
        for start, end in self.a_ownership_windows:
            if not (start <= event_time and (end is None or event_time < end)):
                continue

            # The exact A-stop handoff owns only candidates whose own trigger
            # began at or before that boundary.  A new A structure whose
            # trigger begins strictly after the handoff is independently
            # eligible; the later lifecycle hierarchy still decides whether
            # it may survive as an equal/smaller behavior.
            trigger_event = getattr(zone, "trigger_event_time", None)
            if trigger_event is not None and trigger_event > start:
                return False

            # A decided S normally owns this continuation. A fresh Reset-Blue
            # pair may open a new A only when the entire pair is born after
            # that S ownership began, Blue-1 has already stopped before Blue-2
            # forms, and Blue-2's stop candle is the A source. Open/undecided S
            # windows never grant this preemption.
            blue_1_source = getattr(zone, "blue_1_source_time", None)
            blue_2_source = getattr(zone, "blue_2_source_time", None)
            blue_1_stop = getattr(zone, "blue_1_stop_time", None)
            blue_2_stop = getattr(zone, "blue_2_stop_time", None)
            source_time = getattr(zone, "source_time", None)
            if (
                end is not None
                and blue_1_source is not None
                and blue_2_source is not None
                and blue_1_stop is not None
                and blue_2_stop is not None
                and source_time is not None
                and start < blue_1_source
                and blue_1_stop < blue_2_source
                and source_time == blue_2_stop
                and self._a_pair_is_reset_reset(zone)
            ):
                return False
            return True
        return False

    def _a_pair_is_reset_reset(self, zone: object) -> bool:
        """Whether both Blue Lines that define A are Reset Blues."""
        first = int(getattr(zone, "blue_1_ordinal", 0)) - 1
        second = int(getattr(zone, "blue_2_ordinal", 0)) - 1
        if not (0 <= first < len(self.trend_blue_lines)):
            return False
        if not (0 <= second < len(self.trend_blue_lines)):
            return False
        return (
            str(getattr(self.trend_blue_lines[first], "kind", "")) == "reset"
            and str(getattr(self.trend_blue_lines[second], "kind", "")) == "reset"
        )

    @property
    def eligible_a_zones(self) -> list[object]:
        """A candidates outside stopped-parent S ownership, before rendering."""
        return [zone for zone in self.a_zones if not self._a_owned_by_s(zone)]

    def _candidate_timing(
        self,
        a_stop_index: int,
        order: object,
        order_confirmation_time: datetime,
        a_stop_event_time: datetime | None = None,
    ) -> str:
        """Resolve pre/post-Order ownership without stealing Advanced S.

        Existing nested same-direction geometry owns the Advanced branch and
        keeps the established price-geometry classification.  Otherwise, when
        that legacy classification says ``after``, exact event chronology may
        prove that the A-stop candidate actually formed strictly before the
        opposite Order First.  Equality remains after-Order.
        """
        stop_extreme = self._trend_extreme(self.candles[a_stop_index])
        boundary = as_decimal(
            getattr(
                order,
                "box_bottom" if self.direction == "bullish" else "box_top",
            )
        )
        if self.direction == "bullish":
            legacy = "after" if boundary <= stop_extreme else "before"
        else:
            legacy = "after" if boundary >= stop_extreme else "before"
        if legacy == "before":
            return legacy

        # Do not let Simple pre-Order chronology steal an already-valid
        # Advanced owner.  This preserves accepted Advanced S provenance.
        if self._nested_trend_reaction(order, order_confirmation_time) is not None:
            return legacy

        if a_stop_event_time is None:
            a_stop_event_time = self.candle_times[a_stop_index]
        candidate = self._candidate_before_order(
            a_stop_index, order, a_stop_event_time=a_stop_event_time
        )
        candidate_event = self._candidate_event_time(
            candidate[0], candidate[2], a_stop_event_time
        )
        order_first_time = self.candle_times[int(getattr(order, "first_idx"))]
        return "before" if candidate_event < order_first_time else "after"

    def _candidate_before_order(
        self,
        a_stop_index: int,
        order: object,
        a_stop_event_time: datetime | None = None,
    ) -> tuple[int, datetime, Decimal]:
        """Use the lowest/highest leg extreme from A-stop through order First."""
        if a_stop_event_time is None:
            a_stop_event_time = self.candle_times[a_stop_index]
        first_index = int(getattr(order, "first_idx"))
        candidate = self._candidate_source(a_stop_index, first_index)
        stop_candle_end = self.candle_times[a_stop_index] + self.timeframe
        eligible_stop_remainder = self._lower_window(
            a_stop_event_time, stop_candle_end
        )
        if not eligible_stop_remainder:
            return candidate
        source = eligible_stop_remainder[0]
        value = self._trend_extreme(source)
        for item in eligible_stop_remainder[1:]:
            item_value = self._trend_extreme(item)
            better = (
                item_value < value
                if self.direction == "bullish"
                else item_value > value
            )
            if better:
                source = item
                value = item_value
        later_candidate = (
            self._candidate_source(a_stop_index + 1, first_index)
            if first_index > a_stop_index
            else None
        )
        if later_candidate is not None:
            better = (
                later_candidate[2] < value
                if self.direction == "bullish"
                else later_candidate[2] > value
            )
            if better:
                return later_candidate
        return a_stop_index, self.candle_times[a_stop_index], value

    def _candidate_event_time(
        self,
        source_index: int,
        level: Decimal,
        not_before: datetime,
    ) -> datetime:
        """Return the first lower-timeframe event that forms the candidate."""
        source_time = self.candle_times[source_index]
        for item in self._lower_window(
            max(source_time, not_before), source_time + self.timeframe
        ):
            if self._trend_extreme(item) == level:
                return getattr(item, "timestamp")
        return max(source_time, not_before)

    def candidate_event_time(
        self, source_index: int, price: Decimal, fallback: datetime
    ) -> datetime:
        """Public lifecycle API for exact S candidate provenance."""
        return self._candidate_event_time(source_index, price, fallback)


    def _blue_formation_time(self, line: object) -> datetime:
        explicit = getattr(line, "formation_time", None)
        if explicit is not None:
            return explicit
        source_index = int(getattr(line, "source_index"))
        source_time = getattr(self.candles[source_index], "timestamp")
        if str(getattr(line, "kind")) != "reset":
            reaction_number = int(getattr(line, "reaction_number"))
            if 1 <= reaction_number <= len(self.trend_reactions):
                return self._reaction_confirmation_time(
                    self.trend_reactions[reaction_number - 1], self.direction
                )
            return source_time
        broken_level = getattr(line, "broken_level", None)
        if broken_level is None:
            return source_time
        end = source_time + self.timeframe
        for item in self._lower_window(source_time, end):
            value = as_decimal(
                getattr(item, "low" if self.direction == "bullish" else "high")
            )
            crossed = (
                value < as_decimal(broken_level)
                if self.direction == "bullish"
                else value > as_decimal(broken_level)
            )
            if crossed:
                return getattr(item, "timestamp")
        return source_time

    def _candidate_cross_has_blue(
        self,
        reaction_number: int,
        event_time: datetime,
    ) -> bool:
        """Return whether the candidate cross has its aligned Reset Blue.

        The Reset Blue belongs to the same-direction reaction, but it does
        not have to be drawn on the candidate candle or on the candle that
        crosses the candidate.  Its exact formation event only needs to be
        no later than the candidate crossing event.
        """
        if reaction_number < 1 or reaction_number > len(self.trend_reactions):
            return False
        formation_time = self._reset_blue_formation_by_reaction.get(reaction_number)
        return formation_time is not None and formation_time <= event_time

    def _has_ordinary_trend_reaction(
        self, behavior_start: datetime, event_time: datetime
    ) -> bool:
        """Return whether ordinary aligned geometry completed in the leg."""
        position = bisect_right(self._trend_confirmation_times_sorted, behavior_start)
        return (
            position < len(self._trend_confirmation_times_sorted)
            and self._trend_confirmation_times_sorted[position] <= event_time
        )


    def _candidate_crossed(self, candle: object, level: Decimal) -> bool:
        value = self._trend_extreme(candle)
        return self._a_stopped(value, level)


    def _decision(
        self,
        candidate_level: Decimal,
        order_stop_level: Decimal,
        start: datetime,
        trend_reaction_number: int,
        behavior_start: datetime,
        candidate_start: datetime | None = None,
        fallback_on_unqualified_cross: bool = False,
    ) -> tuple[str, int, datetime, datetime] | None:
        scan_start = max(start, self.range_start)
        left = bisect_left(self.lower_times, scan_start)
        right = bisect_left(self.lower_times, self.range_end)
        if right > left:
            # Order stop is independent of candidate qualification.
            order_position = (
                self.lower_index.first_greater(left, right, order_stop_level)
                if self.order_direction == "bearish"
                else self.lower_index.first_less(left, right, order_stop_level)
            )

            candidate_gate = max(scan_start, candidate_start or scan_start)
            if fallback_on_unqualified_cross:
                qualified_start = candidate_gate
                candidate_family = "fallback"
            else:
                blue_time = (
                    self._reset_blue_formation_by_reaction.get(trend_reaction_number)
                    if 1 <= trend_reaction_number <= len(self.trend_reactions)
                    else None
                )
                trend_position = bisect_right(
                    self._trend_confirmation_times_sorted, behavior_start
                )
                trend_time = (
                    self._trend_confirmation_times_sorted[trend_position]
                    if trend_position < len(self._trend_confirmation_times_sorted)
                    else None
                )
                qualifiers = [
                    value for value in (blue_time, trend_time) if value is not None
                ]
                if not qualifiers:
                    candidate_position = None
                else:
                    qualified_start = max(candidate_gate, min(qualifiers))
                    candidate_family = "blue"
                    candidate_left = bisect_left(self.lower_times, qualified_start, left, right)
                    candidate_position = (
                        self.lower_index.first_less(
                            candidate_left, right, candidate_level
                        )
                        if self.direction == "bullish"
                        else self.lower_index.first_greater(
                            candidate_left, right, candidate_level
                        )
                    )
            if fallback_on_unqualified_cross:
                candidate_left = bisect_left(self.lower_times, qualified_start, left, right)
                candidate_position = (
                    self.lower_index.first_less(candidate_left, right, candidate_level)
                    if self.direction == "bullish"
                    else self.lower_index.first_greater(candidate_left, right, candidate_level)
                )

            if order_position is None and candidate_position is None:
                return None
            if order_position is not None and candidate_position == order_position:
                return None
            if order_position is not None and (
                candidate_position is None or order_position < candidate_position
            ):
                event_time = self.lower_times[order_position]
                index = self._main_index(event_time)
                return (
                    "red", index, getattr(self.candles[index], "timestamp"), event_time
                )
            assert candidate_position is not None
            event_time = self.lower_times[candidate_position]
            if fallback_on_unqualified_cross and (
                self._candidate_cross_has_blue(trend_reaction_number, event_time)
                or self._has_ordinary_trend_reaction(behavior_start, event_time)
            ):
                candidate_family = "blue"
            index = self._main_index(event_time)
            return (
                candidate_family,
                index,
                getattr(self.candles[index], "timestamp"),
                event_time,
            )

        # Preserve the established no-lower-data main-candle fallback exactly.
        start_index = max(
            self.start_index, bisect_right(self.candle_times, start) - 1
        )
        for item in self.candles[start_index : self.end_index + 1]:
            event_time = getattr(item, "timestamp")
            candidate_cross = (
                self._candidate_crossed(item, candidate_level)
                and (candidate_start is None or event_time >= candidate_start)
            )
            order_cross = self._order_stop_crossed(item, order_stop_level)
            if candidate_cross and order_cross:
                return None
            if order_cross:
                return (
                    "red", int(getattr(item, "index")), event_time, event_time
                )
            if (
                candidate_cross
                and (
                    self._candidate_cross_has_blue(trend_reaction_number, event_time)
                    or self._has_ordinary_trend_reaction(behavior_start, event_time)
                )
            ):
                return (
                    "blue", int(getattr(item, "index")), event_time, event_time
                )
            if candidate_cross and fallback_on_unqualified_cross:
                return (
                    "fallback", int(getattr(item, "index")), event_time, event_time
                )
        return None


    def _build_type3_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        type3: tuple[int, datetime, Decimal, int, datetime, int, datetime, datetime],
    ) -> SZone:
        """Build the order-free Blue Type-3 continuation for one stopped A."""
        a_stop_index, a_stop_time, a_stop_event_time = a_stop
        (
            source_index,
            source_time,
            price,
            decision_index,
            decision_time,
            reset_reaction_number,
            reset_time,
            decision_event_time,
        ) = type3
        return SZone(
            direction=self.direction,
            color="blue",
            formation_type="type3",
            a_ordinal=a_ordinal,
            a_source_index=int(getattr(zone, "source_index")),
            a_source_time=getattr(zone, "source_time"),
            a_price=a_price,
            a_stop_index=a_stop_index,
            a_stop_time=a_stop_time,
            a_stop_event_time=a_stop_event_time,
            order_direction=None,
            order_reaction_number=None,
            order_mode=None,
            order_first_index=None,
            order_first_time=None,
            order_break_index=None,
            order_break_time=None,
            order_confirmation_time=None,
            order_box_top=None,
            order_box_top_source_index=None,
            order_box_top_source_time=None,
            order_box_bottom=None,
            order_box_bottom_source_index=None,
            order_box_bottom_source_time=None,
            order_stop_level=None,
            order_stop_source_index=None,
            order_stop_source_time=None,
            reset_reaction_number=reset_reaction_number,
            reset_time=reset_time,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event_time,
        )

    def _build_order_backed_zone(
        self,
        zone: object,
        a_ordinal: int,
        a_price: Decimal,
        a_stop: tuple[int, datetime, datetime],
        order_match: tuple[int, object, datetime],
    ) -> SZone | None:
        """Resolve Simple/Advanced S ownership after a stopped A finds an Order."""
        a_stop_index, a_stop_time, a_stop_event_time = a_stop
        order_number, order, order_confirmation_time = order_match
        order_stop_level, order_stop_source_index, order_stop_source_time = (
            self._order_stop(order_number, order)
        )
        candidate_timing = self._candidate_timing(
            a_stop_index, order, order_confirmation_time, a_stop_event_time
        )
        pre_order_candidate = (
            self._candidate_before_order(
                a_stop_index,
                order,
                a_stop_event_time=a_stop_event_time,
            )
            if candidate_timing == "before"
            else None
        )

        decision_behavior_start = a_stop_event_time
        decision = None
        use_pre_order_candidate = False
        if pre_order_candidate is not None:
            formation_type = "simple"
            source_index, source_time, price = pre_order_candidate
            red_source = pre_order_candidate
            trend_reaction_number = 0
            candidate_event_time = self._candidate_event_time(
                source_index, price, a_stop_event_time
            )
            decision_behavior_start = candidate_event_time
            decision = self._decision(
                price,
                order_stop_level,
                order_confirmation_time,
                trend_reaction_number,
                decision_behavior_start,
                candidate_event_time,
                fallback_on_unqualified_cross=True,
            )
            if decision is None:
                return None
            if decision[0] != "fallback":
                use_pre_order_candidate = True
            else:
                decision = None

        advanced_blue = False
        if not use_pre_order_candidate:
            decision_behavior_start = a_stop_event_time
            nested_match = self._nested_trend_reaction(
                order, order_confirmation_time
            )
            advanced_blue = nested_match is not None

        if not use_pre_order_candidate and advanced_blue:
            formation_type = "advanced"
            red_source = None
            trend_reaction_number, _, trend_confirmation_time = nested_match
            source_index = int(
                getattr(
                    order,
                    "box_bottom_source_idx"
                    if self.direction == "bullish"
                    else "box_top_source_idx",
                )
            )
            source_time = getattr(self.candles[source_index], "timestamp")
            price = self._trend_extreme(self.candles[source_index])
            decision_candidate_start = trend_confirmation_time
        elif not use_pre_order_candidate:
            formation_type = "simple"
            trend_match = self._first_trend_reaction_after_order(
                order_confirmation_time
            )
            if trend_match is None:
                return None
            trend_reaction_number, trend_reaction, trend_confirmation_time = (
                trend_match
            )
            source_index, source_time, price = self._simple_candidate(
                order, trend_reaction
            )
            red_source = (
                pre_order_candidate
                if pre_order_candidate is not None
                else self._candidate_after_order(
                    order_confirmation_time, trend_reaction
                )
            )
            decision_candidate_start = trend_confirmation_time

        if decision is None:
            decision = self._decision(
                price,
                order_stop_level,
                order_confirmation_time,
                trend_reaction_number,
                decision_behavior_start,
                decision_candidate_start,
            )
        if decision is None:
            return None

        color, decision_index, decision_time, decision_event_time = decision
        order_break_index = int(getattr(order, "break_idx"))
        if color == "red":
            if use_pre_order_candidate and red_source is not None:
                source_index, source_time, price = red_source
            else:
                source_index, source_time, price = self._candidate_source(
                    order_break_index, decision_index
                )

        order_first_index = int(getattr(order, "first_idx"))
        box_top_source_index = int(getattr(order, "box_top_source_idx"))
        box_bottom_source_index = int(getattr(order, "box_bottom_source_idx"))
        return SZone(
            direction=self.direction,
            color=color,
            formation_type=formation_type,
            a_ordinal=a_ordinal,
            a_source_index=int(getattr(zone, "source_index")),
            a_source_time=getattr(zone, "source_time"),
            a_price=a_price,
            a_stop_index=a_stop_index,
            a_stop_time=a_stop_time,
            a_stop_event_time=a_stop_event_time,
            order_direction=self.order_direction,
            order_reaction_number=order_number,
            order_mode=str(getattr(order, "mode")),
            order_first_index=order_first_index,
            order_first_time=getattr(
                self.candles[order_first_index], "timestamp"
            ),
            order_break_index=order_break_index,
            order_break_time=getattr(
                self.candles[order_break_index], "timestamp"
            ),
            order_confirmation_time=order_confirmation_time,
            order_box_top=as_decimal(getattr(order, "box_top")),
            order_box_top_source_index=box_top_source_index,
            order_box_top_source_time=getattr(
                self.candles[box_top_source_index], "timestamp"
            ),
            order_box_bottom=as_decimal(getattr(order, "box_bottom")),
            order_box_bottom_source_index=box_bottom_source_index,
            order_box_bottom_source_time=getattr(
                self.candles[box_bottom_source_index], "timestamp"
            ),
            order_stop_level=order_stop_level,
            order_stop_source_index=order_stop_source_index,
            order_stop_source_time=order_stop_source_time,
            reset_reaction_number=None,
            reset_time=None,
            source_index=source_index,
            source_time=source_time,
            price=price,
            decision_index=decision_index,
            decision_time=decision_time,
            decision_event_time=decision_event_time,
        )

    def detect(self) -> list[SZone]:
        output: list[SZone] = []
        self.a_ownership_windows.clear()
        self.order_audit.clear()
        for zone in self.a_zones:
            self._audit_stopped_a(zone)

        cycle_start_time = self.range_start
        for zone_offset, zone in enumerate(self.a_zones):
            a_ordinal = zone_offset + 1
            if self._a_owned_by_s(zone):
                continue
            source_time = getattr(zone, "source_time")
            if source_time < cycle_start_time or (
                source_time == cycle_start_time and output
            ):
                continue

            next_a_confirmation = (
                self._a_confirmation_time(self.a_zones[zone_offset + 1])
                if zone_offset + 1 < len(self.a_zones)
                else None
            )
            a_price = as_decimal(getattr(zone, "price"))
            a_stop = self._first_a_stop(a_price, self._a_confirmation_time(zone))
            if a_stop is None:
                continue
            _, _, a_stop_event_time = a_stop
            order_match = self._first_order_after(a_stop_event_time)
            if (
                next_a_confirmation is not None
                and a_stop_event_time >= next_a_confirmation
            ):
                continue

            self.a_ownership_windows.append((a_stop_event_time, None))
            no_order_deadline = (
                order_match[2] if order_match is not None else self.range_end
            )
            type3 = self._first_type3(a_stop_event_time, no_order_deadline)
            type4 = self._first_type4(a_stop, no_order_deadline)
            # Type-3 and Type-4 are independent order-free S-Blue routes.
            # Exact decision chronology owns the handoff; preserve established
            # Type-3 precedence only on a true exact-event tie.
            if type3 is not None and (type4 is None or type3[-1] <= type4[-1]):
                s_zone = self._build_type3_zone(
                    zone, a_ordinal, a_price, a_stop, type3
                )
            elif type4 is not None:
                s_zone = self._build_type4_zone(
                    zone, a_ordinal, a_price, a_stop, type4
                )
            elif order_match is not None:
                s_zone = self._resolved_order_backed_zone(
                    zone, a_ordinal, a_price, a_stop, order_match
                )
                if s_zone is None:
                    continue
            else:
                continue

            output.append(s_zone)
            cycle_start_time = s_zone.source_time
            self.a_ownership_windows[-1] = (
                a_stop_event_time,
                max(
                    a_stop_event_time,
                    s_zone.decision_event_time + timedelta(microseconds=1),
                ),
            )

        return sorted(
            output,
            key=lambda item: (item.source_time, item.decision_event_time),
        )


    def reconcile_shared_order_stops(
        self,
        zones: Sequence[SZone],
        order_entries: Sequence[dict[str, object]],
    ) -> list[SZone]:
        """Resolve open S candidates with any accepted physical Order stop.

        Order confirmation is parent-neutral.  The decisive Order does not have
        to originate from the A/S candidate currently being resolved.  Once a
        physical Order is calculation-accepted, it may decide an S candidate if
        the Order is live in that candidate window and its exact strict stop is
        after the frozen S source but before the candidate's current strict
        decision event.  Creation provenance remains attached to the Order and
        is never rewritten to the S candidate.

        This rule is direction invariant.  The strict Order stop itself is
        resolved by the shared mirrored lower-timeframe chronology.
        """
        deduped: dict[tuple[int, int], dict[str, object]] = {}
        for entry in order_entries:
            reaction = entry.get("reaction")
            if reaction is None:
                continue
            identity = (
                int(getattr(reaction, "first_idx")),
                int(getattr(reaction, "break_idx")),
            )
            current = deduped.get(identity)
            # Prefer the richer accepted E-audit form when it already carries
            # an exact stop crossing.  Physical identity, not parent identity,
            # is authoritative.
            if current is None or (
                current.get("stop_cross") is None
                and entry.get("stop_cross") is not None
            ):
                deduped[identity] = entry

        # Performance implementation detail: physical Order stop chronology is
        # immutable for this reconciliation pass.  The legacy implementation
        # recomputed the same strict crossing once per (S, Order) pair.  Build
        # each exact candidate once, preserve the authoritative winner key
        # (crossEvent, confirmation, FirstIndex, BreakIndex), then bisect by the
        # frozen S decision window.  This changes only lookup complexity.
        shared_candidates: list[tuple[
            datetime, datetime, int, int, dict[str, object],
            tuple[int, datetime, datetime]
        ]] = []
        for identity, entry in deduped.items():
            reaction = entry["reaction"]
            first_index = int(getattr(reaction, "first_idx"))
            confirmation = entry.get("confirmation_time")
            if not isinstance(confirmation, datetime):
                continue
            stop_level = as_decimal(entry["stop_level"])
            crossed = entry.get("stop_cross")
            if not (
                isinstance(crossed, tuple)
                and len(crossed) >= 3
                and isinstance(crossed[2], datetime)
            ):
                crossed = self._shared_order_stop_cross(confirmation, stop_level)
            if crossed is None or not confirmation < crossed[2]:
                continue
            shared_candidates.append((
                crossed[2], confirmation, first_index, identity[1], entry, crossed
            ))
        shared_candidates.sort(key=lambda item: item[:4])
        shared_cross_times = [item[0] for item in shared_candidates]

        output: list[SZone] = []
        for zone in zones:
            left = bisect_left(shared_cross_times, zone.source_time)
            winner = None
            if left < len(shared_candidates):
                candidate = shared_candidates[left]
                if candidate[0] < zone.decision_event_time:
                    winner = candidate

            if winner is None:
                output.append(zone)
                continue

            _, _, _, _, entry, crossed = winner
            reaction = entry["reaction"]
            first_index = int(getattr(reaction, "first_idx"))
            break_index = int(getattr(reaction, "break_idx"))
            top_source = int(getattr(reaction, "box_top_source_idx"))
            bottom_source = int(getattr(reaction, "box_bottom_source_idx"))
            output.append(replace(
                zone,
                color="red",
                order_reaction_number=int(entry.get("reaction_number", 0)),
                order_mode=str(getattr(reaction, "mode")),
                order_first_index=first_index,
                order_first_time=getattr(self.candles[first_index], "timestamp"),
                order_break_index=break_index,
                order_break_time=getattr(self.candles[break_index], "timestamp"),
                order_confirmation_time=entry["confirmation_time"],
                order_box_top=as_decimal(getattr(reaction, "box_top")),
                order_box_top_source_index=top_source,
                order_box_top_source_time=getattr(self.candles[top_source], "timestamp"),
                order_box_bottom=as_decimal(getattr(reaction, "box_bottom")),
                order_box_bottom_source_index=bottom_source,
                order_box_bottom_source_time=getattr(self.candles[bottom_source], "timestamp"),
                order_stop_level=as_decimal(entry["stop_level"]),
                order_stop_source_index=int(entry["stop_source_index"]),
                order_stop_source_time=entry["stop_source_time"],
                reset_reaction_number=None,
                reset_time=None,
                decision_index=int(crossed[0]),
                decision_time=crossed[1],
                decision_event_time=crossed[2],
            ))
        return output


def detect_s_zones(
    direction: str,
    trend_reactions: Sequence[object],
    opposite_reactions: Sequence[object],
    trend_blue_lines: Sequence[object],
    a_zones: Sequence[object],
    chronology: object,
    start_index: int | None = None,
    end_index: int | None = None,
    opposite_resets: Sequence[object] = (),
    initial_order_geometry: Callable[[int, datetime, int], object | None] | None = None,
) -> list[SZone]:
    return SZoneDetector(
        direction,
        trend_reactions,
        opposite_reactions,
        trend_blue_lines,
        a_zones,
        chronology,
        start_index,
        end_index,
        opposite_resets,
        initial_order_geometry,
    ).detect()
````
<!-- EXACT-SOURCE-END:pipeline/s_zone_detector.py -->

