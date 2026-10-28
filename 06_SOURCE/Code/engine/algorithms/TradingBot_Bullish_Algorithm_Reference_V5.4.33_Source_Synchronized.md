# TradingBot Bullish Algorithm Reference — Current Standalone Specification

**Document Version:** `5.4.33`  
**Last Modified:** `2026-10-26T19:42:22+03:30`  
**last_modified_at:** `2026-10-26T19:42:22+03:30`  
**document_role:** `reference`  
**lifecycle:** `maintained`  
**owner:** `engine/algorithms`  
**scope:** `accepted directional trading specification and exact Source; bearish PH/PL extension only`  
**Status:** `ACTIVE SOURCE-SYNCHRONIZED LOCAL EXTENSION — bearish PH/PL; UNRELEASED`  
**Target Direction:** `bullish`  
**Opposite Direction:** `bearish`  
**Production Source Behavioral Change:** `YES — approved bearish PH/PL/MBL extension; bullish primary calculation deferred`  
**Mirror Contract:** Existing upstream geometry retains its directional mirror contract. The new primary-structure calculation is bearish only by explicit instruction; no bullish PH/PL mirror is approved or inferred.

> **Historical baseline source lineage:** V5.4.33 starts from the exact newly uploaded V5.4.32 `engine(1).zip`. V5.4.32 remains the historical baseline; older unmerged branches are not silently introduced.

## 0. Revision scope

### Current local extension — bearish PH/PL/MBL (UNRELEASED)
<!-- PRIMARY-REVISION-BEGIN -->

- **Approved behavioral addition:** the user-taught bearish primary-structure state, immutable MBL, native accepted-audit Order race, cancellation/reset behavior and Chart presentation. See Section 13.4a for the complete rules and later teaching corrections.
- **Calculation scope:** bearish PH/PL only. Bullish primary calculation is expressly deferred; existing upstream directional calculations remain owned by their current engines.
- **Compatibility:** primary output and Source-aware cache invalidation; the later approved PH-over-StopAll classification and PH-stop Order_A extension intentionally update bearish StopAll/OrderAudit output. Other upstream arrays retain their original trading authority. Native OrderAudit owns all physical creation.
- **Revision identity:** this edits the maintained `5.4.33` Reference files in place. No new release, tag, package publication or cumulative historical branch merge is claimed.
- **Historical boundary:** prior version-specific verification claims below remain historical evidence. Current task checks are recorded separately in Section 14.0p.

- **Latest approved correction:** PH Order consumption uses confirmation at or after the exact crossing, including older First; PL and native fresh Order_A creation gates stay separate. MBL display cap is 100 candles and its default label is 9px.

- **Independent-cycle extension:** each qualifying activated setup owns separate logical PH/PL confirmation state and immutable MBL while older contexts remain active; globally chronological native callbacks and additive cycle provenance preserve shared physical Order identity.

- **PH number-priority correction:** one final PH per physical candle, larger local role wins, and strict higher-price continuation takes at least the preceding final number plus one. Preserve logical eligibility, native physical Orders, horizon boundaries and stable physical object IDs.

- **MBL formation correction:** require the owning cycle's first confirmed PH before exposing its frozen candidate as MBL; reject the entire pending cycle if its historical StopAll reference is already PH-owned. Dependent PH/PL/native causes are recalculated, not merely hidden.

<!-- PRIMARY-REVISION-END -->




### `5.4.33` — accepted independent E donor and main-candle strict-stop chronology (HISTORICAL BASELINE PATCH)

1. **Missing accepted E donors:** Bridge supplies independent direct S-root E identities that E chain reconciliation omitted from its dominant list to StopAll **before** hard boundaries are fixed. Existing physical E sources retain the preexisting dominant candidate's Order and provenance in StopAll. Final E independent-root presentation restoration remains after StopAll as before. No later E candidate can retroactively manufacture a parent or re-arm a displaced owner.
2. **Same-source-bucket owner stop:** The first strict 5s stop of the armed, *currently dominant* exact S/E owner may occur inside the physical donor E's main source candle, even if that E descends from another accepted S. The E source extreme must be strictly beyond the owner's stop level, the stop event must belong to that main candle and be no later than the donor E's decision, and the original direct-child exact-parent exception remains. A completed stop before E source remains eligible under the prior rule; a stop in any later candle does not gain this exception.
3. **Mirror:** Bullish requires strict `Low < owner.price` and `E.price < owner.price`; Bearish uses strict `High > owner.price` and `E.price > owner.price`. Owner identity, priority, count, chronology, source-bucket ownership, parent provenance and StopAll numbering remain invariant.
4. **Target evidence:** FXCM_USOIL 5s 2026-10-22..23, 30s Bullish, E1 Blue at 18:33 with stop level 101.842 (local `Asia/Tehran`). The first 5s Low below that level is 18:56:10 (101.808), the donor's 18:56:00 source Low is 101.798 at 18:56:20. The independently accepted physical E at 18:56:00 is now `StopAll1` (`sequence-group-stop`, owner key `E1 blue`, count `2`); 15:13 StopAll and all five listed S/E anchors remain exact.
5. **Provenance/compatibility:** No public field names, canonical Order identities, upstream Reaction/Reset/Blue/A or core E geometry are changed. Only `bridge/trading_pipeline.py` and `pipeline/lifecycle_engine.py` change production versions.

**Verification:** Full available seven RAW datasets (including the 354,698-row historical August–September XAUUSD Library RAW) at 30s in both directions before/after, 8 focused synthetic cases (both directions), and target deterministic repeat completed. The separate external regression fixture suite and external UI integration are not included in the supplied Engine package, so universal external coverage is not claimed. See release `readme.txt` and `REGRESSION_REPORT_V5.4.33.json`.

### `5.4.32` — corrected implementation and chronology contracts (BUGFIX PATCH)

1. **Optional StopAll feedback:** the accepted Order_B feedback pass and final visible-stage validation use the same explicit `--lifecycle-engine` enablement. The default disabled path no longer incorporates hidden StopAll anchors that the final stage cannot see. The enabled path retains the existing StopAll lifecycle contract.
2. **Physical OrderAudit:** restoring a previously accepted physical Order after canonical rebuild restores its exact chronological confirmation-index tuple as well as the ledger entry. Physical identity and causes are preserved; the indexed post-stop query can no longer omit the restored Order.
3. **Blue strike chronology:** Break main-candle extreme is computed solely from lower-timeframe rows up to and including the exact Reaction confirmation. Pending intrabar confirmation also stops there. Values after strict confirmation cannot create or extend a strike. The same prefix/strict comparator is mirrored for both directions.
4. **S/E physical Order provenance:** a shared Order stop converting a previously Blue S to Red records `order_direction` as the opposite trading direction, consistent with the accepted physical Order identity and other Order-backed S records.
5. **A visibility:** an exact S decision event maps to the calculation candle **containing** the event (`bisect_right − 1`), rather than incorrectly hiding the next candle when the event falls between main candle opens.
6. **Decimal input precision:** JSON prices enter as `Decimal` directly from their original lexical representation. No intermediate JSON binary floating-point conversion may move a strict boundary. Existing public serialization field names remain unchanged.
7. **Import compatibility:** the maintained package wrapper no longer imports a nonexistent symbol and its historical flat sibling imports are initialized explicitly. Ordinary Bridge entry behavior is unchanged.
8. **Mirror invariant:** the new rules are shared for Bullish and its exact opposite; only price comparisons and extrema transform. Timing, order identity, provenance, and feature gates never change with market direction.

**Verification:** local targeted synthetic regressions, full-file 5-second market input replay at 30-second calculation timeframe for both directions, and mirrored Source verification are recorded in the ZIP `readme.txt`. The historical external benchmark and unprovided older regression-anchor suite are not treated as verified merely because the provided RAW datasets execute. No claim of absolute absence of all possible bugs is made.

### `5.4.31` — restored first accepted S Red after armed exact Blue dominant owner (PATCH BRANCH)

1. A currently dominant, accepted **exact S/E Blue identity** with two or more occurrences is armed: `S Blue ×2` or `E(n) Blue ×2`, never mixed numbers or families. Its most recently accepted occurrence must have a **decision event strictly earlier** than the accepted incoming `S Red` decision event.
2. At the first eligible incoming accepted `S Red`, create `StopAll1` immediately through the existing `opposite-s-group-stop` gate, using the incoming S geometry, provenance and **S decision event time** as the gate event. Do **not** require the Blue owner to have crossed its strict price stop or the S to have Order Mode B; either Mode A or Mode B is eligible. The retrospective S source time is not its formation eligibility clock.
3. Clear the exact owner, repeat count and pending stop, and retain prior accepted/historical evidence for downstream lineage. Existing StopAll/E donor and completed-stop S Red Mode-B paths are not deleted. Higher-priority intervening E Red prevents the Blue group from remaining the current owner, even if previous Blue occurrences are public.
4. The shared code implements the same rule for both directions. The only price-sensitive stop comparator for unrelated routes remains Bullish strict `Low < level` / Bearish strict `High > level`. No timestamp-, symbol-, or dataset-dependent production checks were added.
5. This change **preserves all 5.4.30 `Order_A` code and Bridge APIs**. It selectively ports the approved `5.4.27` direct S Red rule and does not silently import other historical fixes from `5.4.28` or `5.4.29`.

**Version ownership:** `pipeline/lifecycle_engine.py` alone changed from the supplied branch baseline `1.18.2 (impl 1.20.2)` to `1.18.3 (impl 1.20.3)`. These are **branch-local** version identifiers; `5.4.29` used a separate `1.20.0` Lifecycle lineage and is not fully merged.

**Verification:** 10 focused rule and source-integrity tests (both directions); real 30-second OHLC replay for USOIL selected range (October 20 18:00 to file end), full USOIL October, XAUUSD October 8–9, XAUUSD September 28–October 6, USOIL September 24–October 3, and full 354,698-row XAUUSD August 25–September 23, before/after in both directions. The reported S Red at October 21 06:17 becomes `StopAll1`, `stoppedBehaviorKey=E2 blue`, `stoppedBehaviorCount=2`, S decision `06:21:35`. Upstream Reaction/Reset/Blue/A arrays match before/after in every pair. Exact completed cases and output differences are in `REGRESSION_REPORT_V5.4.31.json`.

### `5.4.30` — independent first opposite Order_A after A stop (PATCH BRANCH)

1. For each accepted stopped Bullish A, open an independent, exact-time opposite Order_A geometry search at that A's first strict stop. Opposite First geometry is eligible even when it is contained in a larger, earlier continuous opposite Reaction; the larger Reaction does not suppress this **post-stop Order geometry**.
2. Use the already-detected opposite-direction geometry engine's cached `first_order_reaction_after_gate` helper and its frozen leg boundary, strict lower-TF confirmation, and restart/continue chronology. Require First on/after the stop-owning main candle and exact confirmation strictly after the stop event. Compare the resulting First/confirmation with the first canonical native Order; earlier First wins. An identical native physical identity retains its existing canonical number/Reaction.
3. A fully confirmed independent physical Order absent from the canonical public Reaction stream is admitted **only to S OrderAudit / downstream S/E** with `reactionNumber=0`, indicating noncanonical Order geometry. The canonical Reaction/Reset stream is unchanged. The physical identity remains exactly `(FirstIndex, BreakIndex)`, never an invented shape.
4. S's existing Advanced/Type-2 route applies unchanged when a same-direction canonical Bullish Reaction is wholly nested inside that Order and confirms no later than the Order. Existing strict S-Blue/Red race, Order stop/anchor and parent-stop cause deduplication remain mandatory. No rule depends on symbol, prices or literal test timestamps.
5. The new gate is implemented direction-neutrally in `pipeline/order_audit_engine.py`; `bridge/trading_pipeline.py` supplies the preexisting complete opposite geometry engine. Bullish/Bearish are mirror paths.

**Branch/version warning:** `engine.zip` supplied in this task contains Reference `5.4.26` and earlier Lifecycle source, while Project Library contains Reference `5.4.29`. This release intentionally changes only the exact supplied package. The latest Library's `5.4.27`–`5.4.29` changes have not been rebased or regression-tested here. A cumulative production upgrade requires a verified merge; this release must not silently replace a running 5.4.29-based engine.

**Verification:** target RAW XAUUSD 5s (2026-09-22..29) at 30s, both directions, public audit/serialization, and independent USOIL and newer XAUUSD 5s RAWs at 30s in both directions ran successfully. Upstream Reaction, Blue and A SHA signatures are unchanged from the supplied package in every comparison. The targeted post-stop A/Order/S Blue test passed. Determinism rerun passed; full historical anchors, strict synthetic directional mirror transforms, and rebase against 5.4.29 were not run; overall status is **REGRESSION NOT VERIFIED**.

### `5.4.26` supplied-engine baseline — HISTORICAL

Reference `5.4.26` adds one user-approved general chronology correction on top of `5.4.25`:

1. **Order_B calculation-timeframe break ownership:** Order_B remains dependent on a strict post-Reset LL/HH break, but the configured calculation candle containing that strict break owns the physical-Reaction eligibility gate. A canonical opposite Reaction whose First belongs to that same calculation candle is eligible even when the exact lower-timeframe crossing occurs later inside the candle. Lower-timeframe RAW is retained only where exact intrabar ordering is explicitly required: proving that a same-candle boundary crossing occurs after the exact Reset, proving confirmation is strictly after the crossing, and preserving exact audit provenance.
2. **Accepted-A expiry uses the calculation candle:** when a pending reset-leg is compared with the next accepted A, both are compared by their owning calculation-timeframe candle. An A in the strict-break candle expires the pending setup.

The fix is general and contains no timestamp, symbol, price, fixture or RAW-name branch. `pipeline/order_audit_engine.py` is the only changed production module. RX-01, SE-01, accepted-final-A Order_A eligibility, A detection, S ownership, E tie policy, Reaction/Reset geometry and serialization schema remain unchanged.

The Source manifest and exact embedded Source are regenerated from the authoritative `engine.zip` Source tree. The stale virtual root `__init__.py` entry present in Reference `5.4.25` is removed because the authoritative package contains no such file; this is documentation/source-integrity synchronization only and has no runtime effect.

## 1. Source manifest

| Module | Owner | Version | Lines | Bytes | SHA-256 |
|---|---|---|---:|---:|---|
| `__init__.py` | Engine package marker | `unversioned` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `bridge/__init__.py` | Bridge package marker | `unversioned` | 1 | 64 | `2bc59770b9d4313c0e6306287d074487b9e1672dbaf3ada9a8be381e7123f0b8` |
| `bridge/trading_pipeline.py` | Pipeline / Serialization | `1.11.0 (impl 1.14.2)` | 3231 | 123325 | `d70481975d2b8e41c6271a02243862d967d5c906bbe1f2f23a432df6fc0f85a1` |
| `pipeline/__init__.py` | Compatibility package wrapper | `unversioned` | 28 | 653 | `d22a1b81495a6c97b5eccc4d921b1ba4b709bfbcd39be6ef34b9014690b9f460` |
| `pipeline/a_zone_detector.py` | A | `1.7.0` | 804 | 31373 | `83f08b06556eb59c6d1b3afd22b51c280315bd80f3a31bc3044ada349251a115` |
| `pipeline/blue_line_detector.py` | Blue | `2.4.1` | 481 | 16945 | `c6466c280504f82d8f2b189263ed0e9b9581c2f48edd8aaa12f016e55effc98c` |
| `pipeline/core_utils.py` | Core Utilities | `1.0.0` | 26 | 832 | `007e5329e14ab9695e555c630527badc84dd35a239dea1cf685141e4278265eb` |
| `pipeline/direction_policy.py` | Direction Policy | `1.0.0` | 70 | 2282 | `a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea` |
| `pipeline/e_zone_detector.py` | E | `6.16.2 (impl 6.18.5)` | 1144 | 48992 | `96ea351ff88c195937da5c32c5712356b9b876ba6f509d68cb16d37012958ad5` |
| `pipeline/lifecycle_engine.py` | Lifecycle / StopAll | `1.18.6 (impl 1.20.7)` | 1529 | 63174 | `760928f5480efad446b42bc6aa2fbea3e431de13ab92714bac05c09188519c26` |
| `pipeline/order_audit_engine.py` | Order / OrderAudit | `1.7.1` | 2175 | 89666 | `f4e991a6a516ad84e0223c802f5baf611f5e20fb8d7965b9dcdf4ff949d89296` |
| `pipeline/PL_PH_detector.py` | Primary High / Low / Matching Behavior Leg | `1.2.2` | 490 | 22048 | `4c03c016762c55006cba98b9dd565a5e0d37c9420c6e0cacdd1a060d4e8bd989` |
| `pipeline/reaction_engine.py` | Reaction / Reset | `9.8.1 (impl 9.9.1)` | 2439 | 105073 | `f62f7e3c6480750068c4550a8489806030aac16f021f349930bd5efb3ce54198` |
| `pipeline/s_zone_detector.py` | S | `4.20.1 (impl 4.21.1)` | 1445 | 60942 | `0c5864bc3bc6c17f72c5c38b04a1cd0b5b38c726d8834207a55d5351fdfa38fe` |

Generated Source-inventory evidence at `2026-10-26T19:42:22+03:30`. Discovery covers the live Engine package marker and every production Python file under its current Bridge and Pipeline roots; this observed inventory is not a permanent file-count requirement.

The empty live `engine/__init__.py` is included as zero exact bytes. Earlier package revisions that omitted that marker remain historical lineage; their omission is not applied to the current live tree.

Section 16 embeds the exact current bytes used for this manifest, including package markers and the new primary-structure module.

## 2. Authoritative pipeline and ownership

The production execution contract is:

`Complete supplied input normalization → both directional Reaction/Reset contexts → cross-direction Internal Reaction classification → Blue → A → initial S → provisional E → S validity/rebuild and accepted A/Order context → final E/OrderAudit → shared physical Order stop reconciliation → consumed-S native continuation → accepted Order_B feedback → lifecycle/StopAll → visibility/lineage closure → final OrderAudit synchronization → serialization`

Order_B feedback may repeat S/E context construction up to eight passes, using exact reset-leg identities. The optional StopAll acceptance gate is identical in feedback and final visibility, and is enabled only when `--lifecycle-engine` is supplied. A repeated non-convergent identity or pass overflow is an error. This feedback does not recalculate Reaction/Blue/A geometry. StopAll is reconciled once from accepted chronology, including previously omitted independent S-root E identities at new physical source candles; downstream boundary publication does not reinterpret historical E.

The bridge calculates the complete input it actually receives. The full-chart HTTP route supplies the original RAW file. A selected-range HTTP route supplies an in-memory stream filtered by inclusive chart-candle buckets; that calculation begins with empty state at the selected start and cannot use rows outside the supplied stream. Within that supplied input, CLI from/to bounds filter presentation after calculation. Neither frontend nor serialization independently implements trading rules.

Ownership boundaries are strict: Reaction/Reset is owned by `reaction_engine.py`; Blue by `blue_line_detector.py`; A by `a_zone_detector.py`; S by `s_zone_detector.py`; E by `e_zone_detector.py`; physical Order discovery/reuse/provenance by `order_audit_engine.py`; lifecycle/StopAll/visibility by `lifecycle_engine.py`; request/range orchestration and serialization by `bridge/trading_pipeline.py`. Serialization is a projection of finalized state and is not a second trading algorithm.

## 3. Global invariants

1. **Decimal:** JSON floating-number lexemes are parsed directly with `parse_float=Decimal`, then normalized with `Decimal(str(value))`; no binary-float decision is authoritative.
2. **Candle color:** `GREEN` iff `close >= open`; `RED` iff `close < open`; a Doji is always GREEN in both market directions.
3. **Strict crossing:** equality never satisfies a strict price crossing. For Bullish behavior-space stops the directional primitive is `Low < Level`; the Bearish mirror uses the opposite strict comparator.
4. **Chronology / calculation timeframe:** trading eligibility is evaluated on the configured calculation timeframe unless the active rule explicitly requires intrabar ordering. Lower-timeframe RAW is authoritative only for those explicit within-candle chronology questions and exact event provenance; it must not by itself move a main-timeframe eligibility gate to a later calculation candle. Time is never mirrored.
5. **Reaction identity:** physical Reaction/Order identity is `(FirstIndex, BreakIndex)`. Identity, provenance structure, stable ordering, lifecycle priority, behavior-family names and public schemas are direction-invariant.
6. **Determinism:** candidate ordering and tie-breaking are explicit. Equal main-candle extremes keep the earliest source unless the owning rule explicitly requests last-on-equality (S Type-3/Type-4 candidate construction).
7. **Canonical mirror:** the Bearish Reaction path mechanically reflects the shared Bullish coordinate state machine. Independently inspect explicit directional branches and policies. Reflect prices/roles; preserve time, state ownership, canonical identity, cause structure and lifecycle families.
8. **Calculation vs presentation:** internal/historical objects may remain necessary for later calculation even when they are not independently visible. Final filters cannot rewrite upstream truth.

## 4. Reaction / Reset — ACTIVE Bullish specification

### 4.1 Data and color contract

`Candle` carries `index`, native `timestamp`, display time, immutable market `tag`, and Decimal OHLC. `Candidate` carries First/box sources, Mode A/B, optional anchor and leg boundary, Break, intrabar start, cross-direction gate metadata, public box/number metadata and internal/public ownership flags. `ResetEvent` records main index/time, optional exact lower-TF second, broken level, and the owning Reaction First index.

### 4.2 Canonical directional geometry

For Bullish, the canonical First candle role is **FirstRed** (`RED`) following the opposite context color `GREEN`. Confirmation is the first strict breakout satisfying `High > BoxTop`. The confirmation edge is `BoxTop`. The opposite box edge `BoxBottom` may evolve only through chronology available up to the exact confirmation event.

The source does not maintain an independent hand-written Bearish state machine: Bearish geometry executes the Bullish reference state machine through exact Decimal sign/High-Low/color-role reflection. Therefore the initial leg, Mode-A invalidation, breakout/breakdown priority, Reset priority, post-confirmation handling, and lower-timeframe tie rules share one mechanical geometry contract. The reflected color role is internal coordinate machinery only; market Doji remains GREEN.

### 4.3 Mode A / leg-start ownership

Mode A is the first Reaction of a leg. The detector establishes the contiguous context run, builds the directional First candidate, preserves any qualifying adjacent anchor, and freezes the outer leg boundary. Before confirmation, strict outer-boundary invalidation owns the candidate ahead of confirmation when lower-TF chronology proves it first. In the standalone initial Mode-A WAITING state, an invalidated owner releases search and nested geometry cannot confirm while its selected structural owner remains unresolved. The bounded Unified post-Reset search has the separate completion-selection contract in Section 4.7.

### 4.4 Mode B / normal ownership

After a confirmed Reaction, normal search uses the running directional context and the required First color. A confirmation main candle may itself seed the next Mode-B First only when the post-confirmation remainder does not first Reset the just-confirmed structure. The complete confirmation candle can be the next First when its market color has the required role; post-event chronology still controls which prices are eligible for the new boundary.

This handoff applies identically to the **initial confirmed Reaction** and to every later confirmed Reaction. Initial-confirmation status is not a reason to discard an otherwise eligible same-candle continuation; a same-remainder Reset still owns precedence exactly as before.

### 4.5 Exact confirmation and published box

If the Break main candle owns the full-main-candle opposite extreme, only lower-TF prices at or before the first strict confirmation may define the published opposite edge. Later prices in that same main candle cannot retroactively alter Reaction/Order geometry. If lower-TF chronology cannot prove a refinement, detector geometry is retained rather than guessed. Equal eligible extremes retain the earliest main-candle owner.

### 4.6 Reset

A confirmed Bullish Reaction resets only on the first strict `Low < confirmed BoxBottom` event. Equality is not Reset. When Reset and confirmation/break activity share a main candle, selected lower-TF ordering decides which event owns the state transition. Reset reopens **same-direction** Reaction ownership; opposite-direction patterns do not gate that search. A Reset event with an exact lower-TF second exposes that exact second; otherwise the owning main-candle start is the fallback representation.

### 4.7 Post-Reset structural owner vs geometry-only evidence

After Reset, `_first_direct_same_direction_after_reset` scans eligible First candidates in chronological First-index order within the configured end index. It returns a candidate only if confirmation wins before strict loss of its frozen owning boundary. If invalidation wins first, candidates with First indexes at or before that invalidation main index are blocked. A candidate unfinished at the bounded end is skipped, so a later eligible candidate that completes healthily may be returned. The standalone initial Mode-A WAITING state retains its selected unfinished structural owner. The returned healthy result joins the canonical same-direction Reaction stream. `_first_geometry_after_reset` separately returns complete geometry without lifecycle acceptance; generic geometry alone cannot create Order_A. An unfinished or invalidated bounded geometry alone cannot create Order_A. The **special complete post-A-stop physical Order_A** is an explicit exception: it is independently confirmed, after the parent stop, and recorded by S OrderAudit without appending a new public canonical Reaction.

### 4.8 Internal Reaction ownership

Cross-direction internal protection is determined after both directions exist. A candidate is internal only when its temporal/box structure is contained by a healthy opposite Reaction and the complete lower-timeframe physical path through its confirmation remains inside the protecting box. Internal identity affects behavior/public ownership; it does not delete historical calculation evidence or renumber the canonical Reaction stream.

## 5. Blue — ACTIVE Bullish specification

### 5.1 Inputs and reference level

Blue consumes canonical Bullish Reactions and Bullish Resets. For each Reaction, the scale reference is the Mode-A boundary when present; otherwise it is the previous Reaction opposite edge. The 0.618 level is `BoxTop − 0.618 × (BoxTop − reference)`.

### 5.2 Scale strikes

Within Reaction First..Break inclusive, a new strike requires a strictly lower `Low` than the previous confirmed strike (or than the Fibonacci level for the first strike). Pending strikes confirm on a `GREEN` main candle. A Break main candle is eligible only with its lower-TF extreme through the strict Reaction confirmation row, inclusive; later main-candle extremes are excluded. A pending strike reaching the Break candle may confirm intrabar only from lower-TF chronology through that exact confirmation row, inclusive; the decisive extreme is the most directional eligible lower-TF extreme.

A Scale Blue is emitted when strike count increases and spacing ownership permits it (first Blue, or at least one healthy Reaction since the previous Blue). Its source is the decisive strike; line price is `Low + (High − Low) / 3` and its drawing interval is one timeframe before/after the source time.

### 5.3 Reset Blue and double-stop calculation validity

A Reset Blue is sourced by the Reset main candle, with source extreme `Low`, broken level from Reset, and line price `Low + (High − Low) / 5`. If the prior Blue first strict-stops on that same Reset candle and the Reset source extends strictly farther in the Bullish direction than the prior Blue source extreme, the new Reset Blue is marked `calculation_valid=False`. That invalid line remains calculation evidence for the A double-stop route but is excluded from public Blue output.

### 5.4 Internal/public Blue

A Blue becomes behavior-internal when its owning Reaction is internal, or when both the source extreme and rendered line price lie strictly inside the same protected healthy Reaction. Drawing offset alone does not create internal ownership. Public Blue is exactly `calculation_valid and not behavior_internal`.

## 6. A — ACTIVE Bullish specification

### 6.1 Blue state and strict stops

A builds an immutable `BlueState` ledger from all Blue calculation state. Blue formation is exact: Scale Blue forms at its Reaction confirmation; Reset Blue uses the first strict lower-TF crossing of its broken level when available. Each Blue stop is the first strict Bullish crossing of its `source_extreme`; equality does not stop a Blue.

### 6.2 Ordinary adjacent-Blue route

Ordinary A evaluates adjacent calculation-valid Blue states. A pair may trigger through the established direct or inherited-stop route. When the first Blue stopped before the second formed, continuation geometry is frozen over the owning interval; inherited-stop ownership uses the complete stop-candle through the aligned Reaction Break candle. Directional source selection is the minimum Low and strict comparisons preserve chronology. Exact equal-event ties use deterministic ordering; the second/current Blue may be reused for the next adjacent pair only when the current A's first strict stop and the next Blue formation satisfy the source lifecycle gate.

### 6.3 Double-stop route

A Reset Blue marked calculation-invalid by the Blue double-stop rule can create the special A route with the previous valid Blue only when the previous Blue's first strict stop belongs to the invalid Reset Blue source candle. The route then requires the first qualifying same-direction canonical Reaction after the trigger chronology. A special route cannot duplicate a Reaction already owned by ordinary A, and earlier ordinary A lifecycle may suppress the special route when its first stop already completed before the special Reaction.

### 6.4 Reaction confirmation and A source freeze

After a valid Blue-pair trigger, the first qualifying canonical Bullish Reaction confirms A. The A source/price is the minimum Low from the trigger main-candle open through the exact lower-TF Reaction confirmation, inclusive. Prices later in the same Break candle are outside A ownership and cannot move the source retroactively. Ties retain the earliest source unless the owning helper explicitly states otherwise.

### 6.5 A stop and lifecycle handoff

A itself stops on the first strict Bullish crossing after its confirming Reaction. A historical stop before a route's `not_before` boundary belongs to the previous cycle; a later recross of the same level cannot be reinterpreted as the new cycle's first stop. The stop event opens S space.

## 7. S — ACTIVE Bullish specification

### 7.1 General A→S gate

Only A candidates outside an already-owned S continuation are eligible. S begins at A's first strict Bullish stop. If the next A confirmation is already reached at/before that handoff, the stale A does not open S. The detector audits the stopped A's first physical Order_A independently before choosing the S route.

A decided S normally owns subsequent A continuation. A newly built Reset-Blue/Reset-Blue pair may preempt that ownership only when both Blue sources are born after the S handoff, Blue-1 stops before Blue-2 forms, the A source is Blue-2's stop candle, and the pair is actually Reset/Reset. A trigger that begins strictly after the exact S ownership handoff is independently eligible.

A detection remains provisional until S ownership is resolved. If a detected A is consumed by an already-owned S continuation and therefore is not in the accepted A set, its later strict price stop cannot create or retain A-owned `parent-stop` Order_A provenance. This rule changes Order eligibility only; A geometry/detection and S ownership rules are unchanged.

### 7.2 Order-free Type-3 S Blue

Type-3 is an opposite-Reset-leg route available after A stop and before the first Order deadline. The opposite Reaction owning the Reset must have confirmed by the A-stop event and must not already have Reset before that A stop. Candidate geometry spans the **complete opposite Reaction Break main candle through the Reset main candle**, inclusive, and selects the minimum Low with **last-candle ownership on equality**. After Reset, the first strict Bullish cross of that candidate wins only if at least one ordinary same-direction Reaction confirms after A stop and no later than the cross. Earliest valid Type-3 decision wins.

### 7.3 Order-free Type-4 S Blue

Type-4 is the same-direction Reaction continuation available after A stop only while no opposite Order has formed. For every aligned Bullish Reaction confirmed before the Order deadline, candidate geometry spans the A-stop main candle through that Reaction Break main candle, inclusive, selects the minimum Low and assigns equality to the **last** candidate candle. Search begins at the maximum of A-stop event, aligned Reaction confirmation and candidate formation event. That lower-timeframe start is inclusive. The next aligned Reaction confirmation and Order deadline are exclusive upper bounds. The first strict Bullish cross creates S Blue only when a public calculation-valid Blue formed from the candidate source through that cross. If a candidate crosses without qualifying Blue, no S is created from it; the next aligned Reaction rebuilds a fresh candidate from the same A-stop origin.

Type-3 and Type-4 are independent. Earlier exact decision event wins; Type-3 owns only a true exact-event tie.

### 7.4 Order-backed Simple and Advanced routes

**First post-A-stop opposite Order_A gate:** independently confirmed opposite geometry is eligible when its First belongs to the stop-owning or later main candle and its exact confirmation is strictly after the A stop. An earlier continuously owned opposite Reaction must not suppress this physical Order. Use the existing canonical Reaction for an identical physical identity; otherwise emit a geometry-only OrderAudit identity with `reactionNumber=0` while keeping public canonical Reaction numbering untouched. The first eligible post-stop First/confirmation pair owns the immutable Order_A. Ordinary same-direction nested Reaction geometry may qualify this Order for Advanced/Type-2 without being independently published as an opposite Reaction.

The first physical opposite Order_A owned by the stopped A is immutable for that A; later native Reactions do not refresh it merely because they are newer. Candidate timing first applies established price geometry. Exact event chronology may reclassify an apparent after-Order Simple candidate as pre-Order only when its candidate event is strictly before Order First; equality belongs to after-Order. A valid nested same-direction Reaction wholly contained in the physical opposite Order, with aligned confirmation at or before Order confirmation, owns the **Advanced** path and cannot be stolen by the pre-Order Simple chronology optimization.

For pre-Order Simple, candidate geometry spans A-stop through Order First with the A-stop candle restricted to lower-TF prices at/after the exact A-stop event. For post-Order Simple, the first aligned Reaction after Order confirmation is used and candidate geometry spans Order Break through aligned Reaction Break inclusive with last-on-equality ownership. Advanced uses the directionally relevant opposite Order box source after a nested aligned Reaction confirms.

### 7.5 S decision race

After Order confirmation, two strict lower-TF events compete:

- physical Order stop: `High > OrderStop` → **S Red**;
- S candidate strict Bullish cross → **S Blue** only after an aligned Reset Blue formation or an ordinary aligned Reaction completion qualifies the candidate.

An exact same lower-TF position for both crossings produces no decision. Otherwise the earlier event wins. The legacy pre-Order Simple fallback may initially observe an unqualified candidate cross; if later qualification exists by that exact event it becomes Blue, otherwise the fallback path is rebuilt through normal ownership rather than inventing a family.

When a Red decision wins, Red source geometry is recalculated from Order Break through the Red decision main candle unless the accepted pre-Order source is itself authoritative.

### 7.6 Shared accepted-Order stop reconciliation

After E/OrderAudit accepts physical Orders, an open S may be converted to Red by **any** accepted physical Order whose strict stop occurs at or after the frozen S source main-candle start and strictly before S's current decision; the Order confirmation must be strictly earlier than its stop. Parent identity is irrelevant to use; physical identity is authoritative. Candidates are deduplicated by `(FirstIndex, BreakIndex)`, ordered by `(stopCrossEvent, confirmation, FirstIndex, BreakIndex)`, and provenance remains attached to the Order that created it.

## 8. E — ACTIVE Bullish specification

### 8.1 Parent stop and E-space opening

Every E cycle starts only after the first strict Bullish stop of an accepted S/E parent. For an E parent, a stop search begins at its decision event, so E cannot stop before the Order-stop event that confirmed it. Sequence/StopAll boundaries may later reinterpret parent type, but do not invent a different price event.

### 8.2 Physical Order choices

At each parent stop, E considers physical Orders from these routes: direct parent-stop Order_A, an S-carried unconsumed Order, a gate-owned initial A Order, carried-live accepted identity, post-stop accepted-live identity, and accepted Order_B reset-leg identities. `parent-stop` and `reset-leg` are creation causes; `carried-live` / `accepted-live` are use routes only. A candidate must possess an exact strict Order stop. Winner is earliest stop event; for an exact same stop event the larger Order First index wins (`-FirstIndex` tie key). Sequence reset boundaries may invalidate an Order crossing that would span a hard reset.

E performs this comparison over one complete eligible candidate set spanning all direct, inherited, carried and post-stop accepted routes. No route may reduce to a single candidate before the global `(exact stop event, -FirstIndex)` adjudication. This E-consumption tie rule does not change physical Order creation ordering.

### 8.3 E source and decision

`decision_event = max(parent_stop_event, order_stop_event)`. The E source is the minimum Low across the **complete main candle containing the parent stop through the complete main candle containing the Order stop**, inclusive. Lower-TF chronology decides whether stops occurred; it does not truncate either E boundary candle's OHLC. Strict-better replacement retains the earliest equal source.

### 8.4 Recursive family/number lifecycle

Every fully formed accepted S starts a provisional E1 chain in S color. Recursive children are built after the preceding E's strict stop. Reconciliation is chronological: a stopped E leaves the active set but remains historical output. Family follows the accepted stopped parent. Red family outranks Blue at a shared physical source; within equal behavioral priority exact decision chronology is the tie-breaker. When stopped members of the same accepted family exist, the next number is `max(stopped family number)+1`; otherwise the family starts at 1. An active Red E cannot be superseded by S; a Red S may supersede a Blue E under the source lifecycle rules, while Blue S cannot steal an active E continuation.

### 8.5 Consumed S evidence and independent roots

A suppressed/non-public S can remain calculation evidence for continuation of a stopped larger E when lifecycle ownership proves it belongs to that continuation. Its first E inherits the stopped larger E's reconciled family and next number, then recursive children are rebuilt natively. Separately, each accepted stopped S may retain an independent direct E1 root. A same-source accepted E owns that physical source and prevents a provisional S at that source from manufacturing a competing later root. Explicitly invalid S evidence cannot create cross-family competing root provenance when native E continuation already owns the source.

### 8.6 Same-source reconciliation and OrderAudit rebuild

At one physical E source, Red E outranks Blue E; within the same family higher number wins; exact remaining ties preserve the earlier accepted object. After reconciliation, the canonical Order ledger is rebuilt from the accepted E state. Valid parent-stop Order_A identities are retained even if later visibility changes their consuming owner. External restoration/continuation replacement must resynchronize OrderAudit before serialization.

## 9. Order_A — ACTIVE canonical physical parent-stop rule

### 9.1 Creation gate

Order_A is the physical `parent-stop` route opened by an accepted strict behavior stop. Ordinarily a bounded/direct Order candidate must match a canonical opposite-direction (Bearish) Reaction identity `(FirstIndex, BreakIndex)`. **Approved 5.4.30 exception:** after an accepted A stop, independently confirmed complete physical opposite Order geometry may enter S OrderAudit even when it is absent from the public opposite Reaction stream. It receives `reactionNumber=0`, not a synthetic canonical Reaction, and retains its real physical First/Break identity and exact confirmation. An incomplete, unconfirmed, or otherwise invalid geometry cannot enter the accepted audit.

After a stopped A, the first eligible physically confirmed opposite Order is immutable for that A. For S/E parent stops, direct bounded geometry may be evaluated subject to the existing canonical acceptance contract. One exact parent-stop cause may own at most one physical Order_A; when multiple candidates compete, earliest canonical confirmation, then FirstIndex, then BreakIndex owns the cause.

For an A parent, “accepted” means the A survives S ownership and current invalid-A lifecycle filtering into the finalized A behavior set. A provisional/detected A that is S-owned, consumed, filtered or invalid cannot open an A-owned Order_A and cannot be retained as an A `parent-stop` cause in the final OrderAudit. Other independently valid creation causes on the same physical Order identity remain valid.

A shared accepted physical Order stop that changes S Blue to S Red must preserve its opposite `order_direction`, identity, First/Break, confirmation, and exact stop provenance.

### 9.2 Canonical stop

Order stop provenance comes from `MarketChronology.canonical_order_stop`. For Mode A it uses the canonical leg-head/floor context required by that opposite Reaction; for Mode B it uses the previous healthy opposite Reaction's outer edge under the established chronology. The Order's exact strict stop uses the **opposite direction** predicate; for this Bullish calculation that is `High > OrderStop`. Equality does not stop an Order.

### 9.3 Parent validity and retention

An S explicitly identified in invalid_s_root_identities is calculation evidence, not an accepted S parent, and cannot create or retain a `parent-stop` Order_A cause. An E derived from that S may be accepted only when its chosen physical Order has a valid creating cause independent of the invalid S. This applies to ordinary chain reconciliation, consumed-S continuation, and independent-root restoration; provisional geometry alone cannot publish an E or StopAll. Once a valid canonical Order_A enters the identity-keyed ledger, later E/lifecycle reconciliation may change who uses it but cannot delete that physical identity/provenance. A shared Order_B identity may add reset-leg provenance without erasing valid parent-stop provenance.

The same acceptance rule applies during every OrderAudit rebuild/reconciliation pass: nonaccepted A causes are removed before a physical identity is retained on A provenance. This prevents a provisional A cause from being reintroduced after downstream E reconciliation while preserving independent valid S/E or reset-leg provenance for the same physical Order.

## 10. Order_B — ACTIVE Bullish reset-leg rule

### 10.1 Eligibility and post-stop owner

Order_B is eligible only after an accepted lifecycle stop (`A`, `S`, `E`, or `StopAll`) selected by the accepted lifecycle owner of the stopped main candle. The stop opens eligibility; it is **not** the geometric LL anchor.

### 10.2 Geometric behavior anchor

For each reset Bullish Reaction, choose the latest accepted behavior source that exists strictly before the Reaction FirstRed candle, independent of current dominance. Valid anchor families are A/S/E/StopAll. When several lifecycle projections share exactly one source candle, lifecycle priority and number resolve only that exact-source tie.

### 10.3 LL construction and extension

Use the closed main-candle range from anchor behavior source through reset Reaction FirstRed, inclusive:

`LL = minimum Low(anchor candle .. reset Reaction FirstRed)`

Only a strict better Low replaces the current source, so equal extremes retain the earliest source. The LL source must be strictly before the reset Reaction FirstRed. It must also extend beyond the anchor itself: the LL must be strictly below the anchor behavior `Low`; equality invalidates the setup.

### 10.4 Reset and calculation-timeframe strict-break candle

The reset Reaction must first produce its canonical Reset. A strict `Low < LL` must occur after that Reset. The **configured calculation candle containing the first valid post-Reset strict crossing** is the Order_B break candle. Equality is not a break.

Lower-timeframe RAW is consulted only when exact intrabar chronology is required: to prove that a crossing in the Reset candle happened after the exact Reset, to retain the exact crossing timestamp as `strict_break_time`, and to prove any same-candle confirmation occurs strictly after that crossing. The exact lower-timeframe timestamp does **not** postpone the Order_B First-candle gate beyond its owning calculation candle.

### 10.5 Accepted-A expiry

Let the next accepted A formation after the reset Reaction First be `A_next`. Compare `A_next` and the strict break by their owning calculation-timeframe candles. If the A candle is at or before the strict-break candle, the pending reset leg expires. A is upstream of Order_B feedback, so this hard expiry prevents a stale S/E/StopAll setup from firing inside a newer A lifecycle.

### 10.6 Physical canonical opposite Reaction

Let `BreakCandleIndex` be the main calculation-candle index containing `strict_break_time`. Choose the first canonical Bearish Reaction satisfying both:

`FirstIndex >= BreakCandleIndex`

`strict_break_time < ConfirmationTime`

Therefore a Bearish Reaction whose First is the **same main candle** as the strict LL break is eligible even if its candle opened before the exact lower-timeframe crossing. Exact lower-TF chronology remains relevant only to the strict confirmation-after-crossing condition. Canonical-Reaction membership is mandatory; geometry-only evidence cannot become Order_B.

### 10.7 Provenance and identity

Order_B records post-stop behavior, geometric anchor type/source/extreme, reset Reaction identity/confirmation, Reset index/broken level/time, frozen LL boundary/source, exact strict break, and final physical opposite Reaction identity/confirmation. Physical Order identity remains `(FirstIndex, BreakIndex)`. Multiple reset-leg causes may merge into one identity; they do not create duplicate physical Orders.

## 11. Order / OrderAudit architecture

1. The identity-keyed Order ledger is canonical; parent labels are provenance, not identity.
2. Creation causes are exactly `parent-stop` (Order_A) and `reset-leg` (Order_B). `carried-live` and `accepted-live` are consumption/use routes.
3. One exact parent-stop event has one physical Order_A owner. Cause deduplication ranks by confirmation, FirstIndex, BreakIndex.
4. `prepare_order_audit` merges S-stage and E-stage accepted ledgers, retains identities outside the presentation range when required by a visible behavior, deduplicates causes, and computes a strict stop only when it was not already authoritative.
5. `accepted_audit_entry` filters an A-owned identity to accepted A provenance without discarding the complete physical cause set used for presentation.
6. OrderAudit must not fabricate parentage: invalid/suppressed parents lose creation rights; valid historical parent-stop provenance survives later consumer reconciliation.
7. The active physical Order routes are Order_A and Order_B.

## 12. Lifecycle / StopAll — ACTIVE specification

### 12.1 Exact S/E dominance priority

The complete dominance priority for S/E behavior is `S Blue < E Blue < S Red < E Red`. `A` is not a member of this ranking and cannot become its highest behavior, increment its count, or arm its StopAll rule. StopAll is a hard lifecycle boundary, not a competing S/E behavior. Separate A/S/E/StopAll visibility and Order_B ownership rules retain their own scopes.

This priority and exact-identity rule are identical in Bullish and Bearish. Only the strict price stop is directional: Bullish uses `Low < owner price` and Bearish uses `High > owner price`; equality is not a stop.

### 12.2 Highest existing behavior and armed owner

The first accepted S/E occurrence immediately becomes the highest existing exact behavior with count `1`. It is not armed. A repeated occurrence increments only the same exact identity: `S Blue`, `S Red`, or an E identity with the same family and number such as `E1 Blue` or `E1 Red`. Different E numbers and colors never combine. The current exact owner is armed for StopAll at count `>= 2`; its latest accepted occurrence supplies the strict stop level and search start. A third or later exact occurrence remains armed while it still owns the highest state.

An accepted unrelated higher-priority behavior replaces the owner at its source time and starts at count `1`. A direct E child first resolves the strict stop of its exact armed parent, even when its retrospectively chosen source candle begins at or before that stop. An accepted independent E sourced from a different S parent may also donate the currently armed owner stop when the first strict crossing belongs to that very E source candle and its directional source extreme strictly penetrates the owner price. A larger number within the same E family advances the E owner; a smaller number does not. Lower-priority accepted objects may remain valid calculation/output objects, but cannot count, remain armed, or trigger StopAll behind the current owner. There is one active exact owner and no independent Blue repetition ledger.

### 12.3 Chronological strict stop and E donor

The armed owner's stop is the first strict 5-second crossing at or after its latest occurrence's decision event. A stop must precede replacement by an unrelated higher-priority behavior to belong to the former owner; an E directly caused by that stop is resolved as a donor before it replaces its parent. A completed earlier stop is frozen as pending historical evidence if no eligible donor exists at that transition; later replacement cannot cancel it. This pending completed gate is not a second occurrence counter and cannot re-arm a displaced behavior.

At an incoming E, a completed owner stop strictly before the E source time creates `StopAll1` through `sequence-group-stop`; the incoming E supplies physical geometry and Order provenance regardless of family. Two causal exceptions also admit an owner stop at/after retrospective E source time **and no later than E's decision**: (1) exact direct child of the armed owner, whose `parentStopEventTime` equals its first strict stop and whose parent type/source identity/price exactly match the owner's latest occurrence; or (2) an independently accepted E at a new physical source whose directional source extreme strictly penetrates the armed owner's price, and the owner's **first** strict stop belongs to that exact 30s (or configured) E source candle `[sourceTime, sourceTime + timeframe)`. The second route does not depend on E ancestry or require the parent S to postdate the dominant E: independent E parents can predate the owner. An unrelated E cannot consume a stop in a *later* main candle merely because its E decision is later. No earlier displaced owner is revived and no parallel Blue counter is introduced. Bridge includes only otherwise-omitted accepted independent S-root E identities as extra StopAll donor candidates, preserving the preexisting E candidate and Order provenance at every already-admitted physical source. An existing active StopAll that strictly stops at or before the incoming E decision continues to create the next numbered StopAll through `stopall-stop` under its separate historical contract. Its gate precedes the S/E owner gate.

**Superseded by V5.4.33:** the V5.4.32 sentence limiting *all* retrospective E donor exceptions to exact direct children alone. That direct-child rule remains active; the same-source-candle independent-E route is the additional narrowly bounded general exception.

### 12.4 S Red donor and legacy gate name

**ACTIVE (5.4.31 direct accepted-S Red rule):** When the currently dominant exact S/E behavior is Blue, its count is `>= 2`, and its latest accepted occurrence was confirmed **strictly before** the decision event of an accepted `S Red`, the **first eligible S Red itself** immediately produces `StopAll1`. No strict Blue price stop is required. Either Order Mode A or Mode B is valid. Formation must be checked at the incoming S **decision event**, not merely its retrospective source candle. The new `gateEventTime` is exactly the S decision event, and `stoppedBehaviorKey` preserves `S blue` or the precise `E(n) blue` owner and its count. The S is the donor; the StopAll resets the current dominant owner and pending stop state. This direct accepted-S Red gate has precedence inside S handling over the older completed-stop-only path. A previously displaced lower-priority Blue cannot trigger it.

**HISTORICAL LEGACY ROUTE (still executable as fallback):** When the direct gate is not eligible, an accepted S Red of Mode B may still consume an already-completed strict stop of an earlier armed Blue owner using the existing pending-stop rule. This fallback gate event is the earlier physical stop; Mode A does not consume that fallback. The two routes reuse the legacy serialized name `opposite-s-group-stop` but differ in gate chronology. Neither fallback nor other StopAll/E donor paths is removed.



**HISTORICAL / SUPERSEDED (`5.4.22` and earlier):** accepted Blue occurrences were counted in a parallel ledger independent of dominant-owner transitions. That ledger could promote a lower-priority Blue group after a higher-priority Red owner had formed, or promote without a strict stop. It is not an active rule.

### 12.5 Hard StopAll boundary

Materializing StopAll resets the active exact owner, its count/armed state, and any pending completed stop. Historical S/E and StopAll objects remain available as calculation and output evidence. E receives the accepted StopAll source map through the existing atomic sequence-reset publication; its dependent candidate/carried context caches refresh while immutable physical stop/cross caches and historical accepted causes remain retained. A later lifecycle cannot inherit an earlier count or resurrect a displaced owner.

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

### 13.4a Bearish primary structures — approved current extension
<!-- PRIMARY-STRUCTURES-BEGIN -->

#### Scope, ownership and terminology

`pipeline/PL_PH_detector.py` owns the newly taught **bearish** Primary-High (`PH`), Primary-Low (`PL`) and **matching behavior leg (`MBL`)** state. `MBLL` / `matching_behavior_leg_low` are superseded training names; a bearish MBL still represents the original leg's minimum Low. The new module consumes finalized calculation-accepted behavior state and the existing accepted physical OrderAudit. It does not repair Reaction/Reset/Order eligibility, invent additional physical Orders, or delegate trading decisions to the Chart or serializer.

**Bullish PH/PL calculation is explicitly deferred by the user.** Existing Bullish Reaction/Reset/Blue/A/S/E/StopAll and native Orders remain available as upstream dependencies of the bearish calculation. Their continued execution is not a bullish primary-structure implementation. Both directional References contain the same complete shared Source, while this new normative state machine remains bearish only. The pre-existing mirror matrices do not authorize a bullish primary mirror.

#### Matching setup and first PH gate

1. The accepted StopAll sequence must reach at least `StopAll3`; later numbered StopAll events may precede qualification.
2. At or after that boundary, accept at least two **exact dominant** S/E occurrences under `lifecycle_engine.advance_dominant_behavior`, the same owner/count resolver used by StopAll. S identity is `(S, color)`; E identity is `(E, family, number)`. Shared priority is S Blue < E Blue < S Red < E Red, with the existing higher-E-number rule within one family. A lower-priority intervening occurrence does not replace the owner; a higher-priority owner replacement restarts its count. Use accepted final events: an E/S source belonging to StopAll is not simultaneously an independent matching occurrence, and an invalid calculation event does not count.
3. Retain the last qualifying StopAll **before each matching leg**, the second accepted matching occurrence's main source candle, and the qualification event. Qualification becomes available no earlier than the reference StopAll decision and both matching decisions; do not treat a retrospective source timestamp as confirmation. A subsequent StopAll does not by itself invalidate an already qualified pair. Keep that pair pending while also evaluating newly qualified legs; an earlier unbroken reference must not block later valid setups.
4. For each pending qualified leg, find its first authoritative RAW `High > reference StopAll main-candle High`. Equality does not open PH space. **Every activated qualified leg starts an independent cycle**, even while older cycles remain active or their MBLs remain unbroken. An eligible activation freezes an internal candidate leg; it does not yet form a public MBL. Earlier qualification does not block a later setup that crosses first. Its owning calculation candle is the initial PH trigger candle. Activation order follows exact break time, then qualification time, reference source index and second-behavior source index for deterministic ties.
5. Resolve only eligible accepted conceptual Bearish Orders of creation type Order_A or Order_B. The first eligible exact Order stop confirms PH-1; its source and its later confirmation are separate events.

#### Independent cycle ownership and exact shared chronology

The user explicitly superseded the one-global-cycle interpretation. Each qualifying historical reference StopAll and its first exact dominant matching pair can start its own PH-1/PL sequence and immutable MBL. Do not wait for an older MBL to break or an older cycle to finish. New-cycle activation does not cancel, reset or overwrite earlier cycles. PH/PL logical confirmation counters and PH-reset flags remain local to each cycle. Final physical PH numbering is reconciled across these roles by the higher-number precedence rule below. Additional repetitions under the same already-qualified reference do not create extra cycles. Duplicate physical accepted input records cannot manufacture matching counts or duplicate cycle activations.

Accepted historical StopAll/S/E state remains causal evidence and is not retroactively rebuilt. However, a historical StopAll already promoted to a confirmed PH cannot be reused as the reference of a new independent cycle. At the pending strict activation event, reject the entire setup if the reference's exact source index/time is already PH-owned. It must create no checkpoint, PH, PL, MBL or native PH-parent callback. Continue existing valid cycles and unrelated later setups. Final candle ownership remains PH over StopAll. Logical cycles may consume the same canonical physical Order; the native Order ledger remains shared and physically deduplicated. A newly accepted PH-parent cause from one context can legitimately make a physical Order eligible in another context. Sharing does not merge local confirmation states or MBLs; final physical PH names follow the precedence below.

Process activation and confirmed PH/PL transitions in global exact RAW chronology. Prospective per-cycle checkpoints may evaluate future seek/cancellation routes but cannot commit native PH ownership. Commit only the globally earliest confirmed point, then update the shared native audit. A PH commit invalidates every pending prospective decision, including cycles currently waiting without an accepted Order, so a new valid physical Order can wake an older context before its previously projected future cancellation. Never run one cycle through its entire future before beginning another against that future-mutated ledger. Exact activation/decision ties activate contexts first; decision ties retain deterministic activation order. There is no arbitrary cycle count or feedback-loop cap.

`PrimaryPoint.cycle_id` and each cycle's `PrimaryResult.cycle_id` identify the logical context. Aggregate `PrimaryResult.cycles` retains all separate results; internal aggregate highs/lows retain all logical roles in global decision order. Final physical PH ownership is resolved by the primary Engine before Bridge projection. The old aggregate `.mbl` is only an internal first-cycle candidate compatibility view. `formed_matching_legs` owns the complete confirmed MBL collection for the requested horizon. Earliest exact qualification provenance is retained independently of source ordering, including qualified-but-unbroken setups.

#### Final physical PH number precedence

The user's later correction supersedes publishing each local PH counter as a
separate chart label. `PL_PH_detector.resolve_primary_highs` first filters out
roles confirmed after the requested horizon, groups exact physical source
candles, and chooses the largest local number for each candle. Ties use exact
confirmation chronology and deterministic cycle activation order. Confirmed
physical groups follow global decision chronology, including retrospective
source candles; source-candle position cannot reorder a later confirmation.

For a distinct next physical PH whose Decimal High is **strictly greater**
than the preceding finalized PH-n, its final number is at least n+1. Keep a
larger already-qualified local number. Thus a qualifying/reset PH-1 above the
previous PH-n continues as PH-(n+1), while an equal/lower new PH may retain its
local reset number. Coincident roles use one larger number without incrementing
again for each duplicate role. This is an Engine ownership rule, not a Chart
overlap workaround. Keep independent MBLs, PL state, strict crossings, native
Order selection, confirmation events and logical reset eligibility unchanged.

Final PH aliases in native parent-stop and reset-leg provenance use the same
source-to-number mapping. `OrderAuditEngineMixin.reconcile_primary_high_labels`
only reconciles names and duplicate aliases; it cannot move/recreate Orders or
change their physical identity, geometry or chronology. Frozen structure Order
snapshots receive the same alias mapping without mutating their source data.
Final numbering is calculated before the presentation start filter, so hiding
earlier candles cannot restart the visible sequence.


#### MBL formation requires a confirmed PH

The approved prerequisites are cumulative: an accepted StopAll sequence at or
beyond StopAll3, two exact dominant matching behaviors, an eligible strict
reference break, and at least one confirmed PH belonging to that valid cycle.
Qualification and activation alone cannot form an MBL. Another cycle's PH or
a future PH outside the requested horizon cannot confirm this cycle's leg.

The frozen minimum boundary is retained internally as a candidate for existing
Order/cancellation chronology. `PL_PH_detector.formed_matching_legs` promotes
that candidate to the formed output only when the owning cycle's earliest PH
confirmation is within the requested end horizon. Source, price, strict break
and 100-candle cap stay unchanged; PH resets do not generate another MBL.
An already-broken candidate is not made unbroken by later PH confirmation.

PH ownership is committed before any strictly later reference breakout. If a
proposed reference broke earlier, that higher candle would lie in the inclusive
PH-maximum interval and the old reference could not remain its PH extreme
source. Thus activation-time rejection preserves exact chronology without
letting an invalid reference cycle create native Order side effects.

#### Immutable MBL

The MBL is the minimum main-candle Low from the **second matching behavior's source candle through the reference-StopAll breakout candle, inclusive**. Equal minimum values retain the earliest candle in that closed range. Preserve its source identity, Decimal price, reference StopAll, second matching behavior and exact breakout provenance.

There is one immutable candidate **per valid independent cycle**; a cycle exposes its MBL only after its own first PH confirms. Several valid confirmed cycles can expose several MBLs at once. **PH reset does not create another MBL and never recomputes its price or source.** The former training sentence describing a new MBL after PH reset is superseded. Its first subsequent authoritative RAW `Low < MBL.price` is its strict break; equality is not a break.

#### Native Order direction, creation and eligibility

Distinguish **conceptual owner direction** from the native Order's **opposite physical Reaction direction**:

| Structure being confirmed | Conceptual owner / audit group | Native physical `direction` | Native strict Order stop |
|---|---|---|---|
| PH in this bearish market algorithm | `bearish` | `bullish` | `Low < stopLevel` |
| PL in this bearish market algorithm | `bullish` | `bearish` | `High > stopLevel` |

This is the existing native Order contract, not a changed price comparator. The PL teaching's Bullish Reset / LL / opposite Bearish physical Reaction belongs to the **Bullish owner** path. Never reinterpret its conceptual name by swapping its already resolved stop.

- Reuse full-history `prepare_order_audit(detector, 0, final_index, s_detector, accepted_a_sources)`. It merges accepted S/E ledgers, removes rejected A creation causes, deduplicates exact physical `(FirstIndex, BreakIndex)` and applies the established one-physical-Order_A-per-parent-stop cause rule.
- **Order_A** is accepted `parent-stop` provenance. **Order_B** is accepted `reset-leg` provenance. Native physical Reaction **Mode A/B is independent of creation type**; a Mode-B physical Reaction carrying only `parent-stop` is Order_A.
- An unconfirmed structure crossing does **not** manufacture a physical Order or Order_B. The strict stop of an already confirmed PH is a genuine parent-stop event and creates native bearish-owner Order_A through the existing OrderAudit owner, as specified below. Order_B must already satisfy accepted A/S/E/StopAll lifecycle stop ownership, the correct directional Reset, the accepted geometric anchor and strictly extending LL/HH boundary, strict post-Reset boundary break, accepted-A expiry, canonical opposite physical Reaction, confirmation and native strict Order stop.
- Logical initial PH-1 and logical PH-1 following a reset admit accepted Order_A and Order_B. Logical PH-2 and every later same-cycle PH admit accepted Order_A. Final physical renumbering does not change this Order eligibility or replay the race.
- **Every specified PL, including PL-1, admits both conceptual Bullish Order_A and Order_B.** This supersedes earlier B-only PL-1 teaching. For PL Order_A, the first eligible accepted canonical Bearish physical Reaction after the trigger supplies the direct candidate, even if its Order is still open; a later stopped Order_A must not replace this first valid candidate. Do not substitute an arbitrary unaccepted canonical Reaction; do not label noncanonical order-only geometry as a canonical PL candidate. Continue evaluating all eligible accepted Order_B candidates in the same race.
- **PH consumption gate:** an already accepted native Order is eligible when its exact confirmation is **at or after** the structure crossing. Its physical First may precede that crossing. A joint confirmation/crossing in one finest RAW timestamp is eligible; do not invent an ordering between these compatible same-direction events. An Order confirmed strictly before the new crossing is not admitted by this rule. This applies to initial/reset PH-1 and subsequent PH with their existing creation-type restrictions. **PL keeps its existing gate:** First belongs to the trigger main candle or later, and confirmation is strictly after the crossing. The selected exact Order stop remains strictly after confirmation and the crossing. This consumption gate does not loosen the separate native creation rule for a new Order_A caused by stopping a confirmed PH.
- Choose the earliest eligible **exact stop event**, regardless of creation time, proximity, public Reaction number or A/B type. Retain all accepted creation types on a shared physical identity. Exact Order-stop ties use deterministic physical identity ordering, without an A/B type preference.

#### PH replaces StopAll and owns its subsequent Order_A

Once PH is confirmed, its exact `(source_index, source_time)` candle has final behavior **PH**, not StopAll. Remove that candle from the final accepted/public StopAll collection, including the optional Bridge output, before serialization. A PH confirmed after the requested presentation horizon does not erase a StopAll from an earlier window. Preserve historical StopAll boundaries, identities and sequence-reset evidence used before PH confirmation; final classification does not retroactively rebuild that accepted prefix or renumber historical identities.

Each PH is committed to native OrderAudit immediately after confirmation and before selecting a later structure Order. Its first strictly later authoritative RAW `High > PH.price` is the PH stop. Equality is not a stop. That event creates conceptual bearish **Order_A** from existing native canonical physical Bullish Reaction rules, with First in the stop's main candle or later and confirmation strictly after the exact stop. Skip canonical candidates confirmed at or before the stop and continue to the first eligible canonical candidate. Keep native stop geometry, physical identity, blocked-First eligibility, Decimal values and full creation provenance. An open native Order_A is retained; it does not confirm a new PH until its own strict stop occurs. There is one physical Order_A owner per PH parent-stop cause.

Record `parent-stop` creation with parent `PHn`, its source and exact stop event. Historical StopAll reset maps cannot veto this PH parent or rename it back to StopAll. If an obsolete StopAll cause belongs to the same actual PH stop, only the eligible native PH direct identity can own the transferred cause. Remove that obsolete cause from an ineligible former identity; retain its independent creation causes if any. A fully cause-less physical identity is removed from the native ledger and confirmation index, and affected accepted-order/reuse caches are invalidated.

Independent valid Reset routes retain creation type **Order_B**. Their post-stop owner is PH only when the same source's actual PH stop occurred after PH confirmation. Their geometric anchor owner is PH only when PH was already confirmed at the Reset Reaction's First main timestamp. Earlier roles retain historical StopAll provenance. Reparenting does not change Reset geometry or convert a Reset cause into Order_A. Re-prepare accepted audits after each PH commitment, and revalidate final public behavior references after PH/StopAll ownership resolution.

#### PH continuation and unlimited same-cycle numbering

After confirming PH-n, wait for the first strict `High > PH-n.price`. That main candle opens PH-(n+1). Use the earliest eligible accepted Order_A stop after that gate. The new PH price is the maximum High from the breakout main candle through the selected Order-stop main candle, **including both whole candles**; earliest equal-maximum candle owns the source. PH source is retrospective; its exact confirmation is the later selected Order stop. PH-2 and later highs remain above the same original MBL.

The previous three-PH cap is explicitly superseded: **PH-1, PH-2, PH-3, PH-4, ...** follow the shared continuation rule until a taught cancellation/reset transition changes the state. Do not add a numeric cap or use a fixture timestamp as a boundary.

#### PL-1, PL-2 and PL-3

| PL stage | Required strict trigger | Eligible conceptual Bullish Orders |
|---|---|---|
| PL-1 | first `Low < MBL.price` | accepted Order_A and Order_B |
| PL-2 | after PL-1 confirmation, first `Low < PL-1.price` | accepted Order_A and Order_B |
| PL-3 | after PL-2 confirmation, first `Low < PL-2.price` | accepted Order_A and Order_B |

The strict break of an existing PL is its stop and opens the next PL stage. Each PL price is the minimum Low from **its own trigger main candle through its selected Order-stop main candle, inclusive**. Select the earliest equal-minimum candle. The selected stop confirms the structure; source, trigger and confirmation identities/times remain distinct.

After PH reset and a new PH-1, the next PL remains **previous PL number + 1**. Its trigger is the strict break of the **last PL's Low**, not another break of the already fixed MBL. In particular `PH-1 → PL-1 → new PH-1 → PL-2` is the taught sequence. Do not reset the PL counter when resetting PH.

#### Cancellation and PH reset

1. Before a pending PH is confirmed, a strict MBL break cancels that pending PH and enters the PL path. This applies to PH-1, PH-2, PH-3 and the shared later-PH continuation. A later stop of the cancelled PH's old Order cannot confirm it.
2. A subsequent PL still requires its own previous-PL-Low break; cancellation must not invent that price break when price has only crossed MBL.
3. If PL is pending but no new PL has confirmed since the latest PH, a strict break above that PH's High cancels pending PL and resumes the same PH cycle at the next PH number.
4. Once a PL has confirmed, the next eligible upward PH gate restarts the local confirmation state at **PH-1**, with accepted conceptual Bearish A/B Orders. Its final public number is still subject to higher-number precedence, including strict-price continuation. This applies after an existing PH-1, PH-2 or later PH. The PH range again starts at that new upward breakout, while the MBL remains unchanged and PL numbering survives.
5. Use the finest supplied RAW chronology for competing boundaries and Order stops. If opposing events occupy exactly the same authoritative RAW timestamp and their order is unresolvable, report `ambiguous-raw-boundary-order` rather than inventing an intrabar OHLC path or type priority.

#### After strict break of PL-3

The latest supplied formal algorithm defines another native conceptual Bullish Order_A search from the first valid Bearish physical Reaction and continued eligible Order_B evaluation after strict `Low < PL-3.price`. **It does not define PL-4 formation.** Preserve these eligible orders as post-PL3 evidence, but do not create a fourth PL from them. An eligible subsequent upward PH reset remains a separate taught transition. Earlier generic counting language must not override this later explicit PL-4 boundary.

#### Full-history calculation and additive public contract

The complete supplied RAW means the authoritative input stream: the existing selected-range HTTP route can supply only the selected candle buckets, while the complete-source route supplies the original file. This feature preserves that transport scope. Calculate accepted matching, MBL, structure state and native Order candidates on that complete supplied stream; apply the presentation window only after calculation. Calculation Source identity includes the new module so a stale cached result cannot silently omit its output. Existing reaction, reset, Blue, A, S, E, StopAll and OrderAudit arrays retain their original ownership and serialization.

The bearish group adds `primaryHighs`, `primaryLows`, `matchingBehaviorLegs`, `primaryStatus`, `primaryCycles` and `postPL3Orders`; the envelope adds `primaryVersion`. Prices remain Decimal strings; public times use the existing Tehran-local epoch conversion.

- **Primary point:** stable `id`, owning `cycleId`, market `direction`, `kind`, final `number`, `sourceIndex/sourceTime/price`, `triggerIndex/triggerTime/triggerEventTime`, `decisionIndex/decisionTime/decisionEventTime`, and the selected native `order`.
- **Selected Order / post-PL3 Order:** conceptual `ownerDirection` and opposite physical `direction`; `reactionNumber`, physical `firstIndex/firstTime`, `breakIndex/breakTime`, `confirmationEventTime`, `stopLevel`, `stopSourceIndex/stopSourceTime`, `stopHitIndex/stopHitTime/stopHitEventTime`, accepted creation-kind `causes`, readable creation `types`, native `reactionMode`, isolated complete `auditCauses`, and box geometry. Stable physical identity and the creation-type/Reaction-Mode distinction must survive projection.
- **MBL:** stable `id`, additive `cycleId`, `direction`, `sourceIndex/sourceTime/price`, `referenceStopAllIndex`, `secondBehaviorIndex`, `triggerIndex/triggerTime/triggerEventTime`, earliest owning-PH `confirmationIndex/confirmationTime/confirmationEventTime`, nullable `stopIndex/stopTime/stopEventTime`, and `capTime` for 100 subsequent analysis candles. A future confirmation or crossing beyond the presentation horizon must not be presented as already confirmed inside the window.
- **Status:** explicit waiting state, unresolved authoritative RAW ordering, or `post-pl3-orders-only`. A missing valid Order cannot be replaced with a provisional point.

The Section 13.5 AST index and Section 16 exact Source provide complete current dataclass fields, function contracts and serializer implementation; they are regenerated after Source edits.


`primaryCycles` contains each activated context's stable `id`, direction, final supplied-stream status, reference/second-behavior source indexes, trigger index/times, and presentation-selected logical high/low counts. `highIds` joins each context to its final physical PH objects; a PH shared by several contexts is published once and exposes all participating `cycleIds`. Cycles activated beyond the requested end are omitted. Top-level `primaryStatus` belongs to the latest visible cycle; before any visible activation, exact qualification provenance determines waiting-for-matching-behaviors versus waiting-for-stopall-break. Per-cycle statuses describe the complete supplied calculation, not reconstructed snapshots of every earlier lifecycle instant.

A physical PH keeps the ID of its earliest confirmed logical role, with deterministic activation-order ties; first-cycle legacy IDs are preserved. An additional-cycle origin includes its cycle identity. A later winning role or final number change must not change that ID and lose Hide/Appearance settings. `PrimaryPoint.identity_source` separates physical identity provenance from the winning semantic role. Logical cycle memberships remain available even though coincident PH roles no longer create overprinted labels. MBL IDs retain reference/second-source identity and all legs are serialized. Post-PL3 logical Order uses include cycleId; shared physical identity is not manufactured a second time.

#### Chart presentation and settings

The Chart receives final calculation truth. It never reconstructs matching, crossings, Orders or structure numbering.

| Market direction | PH marker / label | PL marker / label |
|---|---|---|
| Bearish | downward double chevron above candle; label above marker | filled circle below candle; label below marker |
| Bullish appearance only, calculation deferred | filled circle above candle; label above marker | upward double chevron below candle; label below marker |

Default arrow extent and label font are `12px`, color `#056656`. Filled circles have radius `12px` (diameter `24px`), color `#ec407a`, opacity `100%`; their label font is `12px` and the same pink. Candle-to-nearest-marker-edge gap is `12px`; marker-to-visible-label-edge gap is `10px`. Text is `PH-n` / `PL-n` using the finalized number; repeated PH-1 after reset retains a distinct stable object identity.

MBL uses the finalized source/price and strict end event, dotted line size `2`, color `#b22833`, and centered `MBL` text at `9px`, with a label gap in the line. Without a strict break, display 100 subsequent analysis candles. The latest existing MBL may extend to a later actual break; an older MBL must not extend beyond 100 analysis candles when newer legs exist. A PH reset does not itself create such a newer MBL. Source `capTime` preserves actual main-candle chronology across market-data gaps; the Chart does not scan prices for a substitute end.

Configure contains a PH/PL section with marker/label visibility switches for PH, PL and MBL. Appearance exposes colors, marker/label sizes, circle opacity/radius, gaps and line style/width using the same persistence and reset patterns as existing controls. Per-object hide/unhide uses the existing object tree and stable IDs. All stated appearance values are defaults, not fixed calculation rules.

The Info panel reports finalized PH, PL and MBL counts and the Engine's current primary status. A zero count remains a valid result and its waiting state is shown explicitly. Before reusing an in-browser result for appearance changes, the Chart checks the current opaque calculation-Source fingerprint through the local server. Missing, failed or changed Source identity requires the normal calculation request. This identity check does not independently validate RAW bytes or infer trading state.

#### Bounded authoritative-RAW acceptance example

The user-provided XAUUSD 5s RAW example, calculated at 30 seconds, has reference StopAll6 at `2026-09-29 17:52:00`, High `4175.180`, and matching S Red sources `18:28:00` and `20:06:30`. Its first strict reference breakout belongs to main candle `22:09:00`. The MBL is main source `21:28:00`, price `4142.445`.

The earliest accepted eligible bearish-owner Order stop is physical Bullish identity `(3045, 3046)`, First `23:07:00`, confirmation `23:07:50`, stop level `4170.765`, exact stop `23:12:15` in main candle `23:12:00`. This physical Reaction has Mode B but accepted parent-stop creation provenance, hence creation type Order_A. Its A cause source is `22:59:30`, stopped at `23:05:50`. The inclusive PH range `22:09:00 .. 23:12:00` has maximum `4175.755`, main source `22:10:00`. Physical Bullish Order First `22:23:30` is accepted but stops later and does not win this race.

This is bounded acceptance evidence of the general accepted-audit, chronological race and inclusive-extrema rules. None of these timestamps, indices, prices or RAW names is a production branch or universal market rule.

#### Bounded USOIL joint-confirmation acceptance example

On the user-selected USOIL RAW chart identity `107aa8c4-ca51-47b7-925f-401df4200f0c`, supplied from October 1 through October 23 and calculated bearish at 30 seconds, reference StopAll5 is `2026-10-06 08:21:00`, High `90.028`. The first two matching S Red sources after it are `11:45:30` and `14:37:00`; repeating the same source in a written list does not create a second physical behavior. The immutable MBL remains `2026-10-06 15:50:30`, price `86.867`.

The reference breaks strictly at `2026-10-07 00:13:45`, belonging to main candle `00:13:30`. The accepted bearish-owner physical Bullish Order has First `00:10:30`, exact confirmation `00:13:45`, native stop `89.803`, and exact stop `01:31:00`. It has physical Reaction Mode B but accepted creation type Order_A. The user explicitly confirmed that this older-First, jointly confirmed Order validates PH-1. The inclusive whole-candle range has maximum `90.034` on `00:13:30`, so that candle owns PH-1; `01:31:00` is its confirmation, not its source. The MBL unbroken-display cap is `16:40:30`, 100 actual analysis candles after its source.

The previous gate required First at or after the crossing candle and confirmation strictly later than the crossing; it wrongly excluded this accepted Order and selected `03:55:30` as the first PH source. The general PH confirmation gate above corrects that earliest divergence. These timestamps, prices and the chart identity are bounded acceptance evidence only; production contains no corresponding special case.

#### Bounded independent USOIL October 22 acceptance example

In the **same full** USOIL107AA8C4 calculation, reference StopAll9 is `2026-10-22 12:05:30`, High `100.068`; matching S Red sources are `13:20:00` and `15:42:00`. Their qualified leg strictly breaks at `21:20:35`, belonging to main candle `21:20:30`. Its independent PH-1 source is `21:20:30`, High `100.149`, confirmed at `21:47:25`. Its own immutable MBL is `18:56:30`, price `97.883`.

This cycle must coexist with the October6/7 cycle above, whose MBL remains unbroken and whose numbering continues locally. The October22 PH source is no longer a public StopAll10. Both independent PH-1 objects and both MBLs must have distinct object identities and support independent hide/unhide. MBL remains dotted red, with a 100-analysis-candle unbroken cap and 9px default label; older legs use their capped presentation when newer cycles exist. None of these bounded fixture dates/prices/chart identities participates in production conditionals.


#### Bounded USOIL PH number-priority acceptance example

The later explicit invalid-cycle rule supersedes the previous PH-5 example
at October8 11:25:30: that point depended on a PH-owned StopAll reference and
its whole cycle is invalid. After recalculation, October7 17:09 remains PH-4;
October8 12:30 is PH-5 and14:21 is PH-6. The general physical number-precedence
rule remains unchanged; invalid cycle roles no longer participate in it.

#### Bounded USOIL rejected MBL examples

Reject the candidate MBL source `2026-10-07 11:51:30`: reference index8894 is
the PH-3 source at04:47, confirmed04:55:05 before its would-be activation.
Reject candidate source `2026-10-08 18:01:00`: reference index12832 is an
already-confirmed PH source at14:41:30. Neither historical StopAll may seed a
new independent cycle. These identities are test evidence only, not production
conditions. Preserve the valid original MBL at October6 15:50:30 and independent
October22 MBL at18:56:30, each confirmed by its own PH.

<!-- PRIMARY-STRUCTURES-END -->

### 13.5 Complete module/class symbol and schema coverage

This index is regenerated mechanically from the exact current Source AST. It covers module assignments/type aliases, top-level functions, classes, annotated schema fields, methods/properties and nested function definitions. Imports, local variables and lambda bodies remain preserved in the exact Source snapshot. Line numbers address each Source file, not this Reference.

The index is descriptive integrity/navigation evidence, not trading-semantic authority.

#### `__init__.py`
- **Module-level symbols/assignments:** _none_
- **Top-level functions:** _none_
- **Classes / schemas:**
  - _none_
- **Nested implementation functions/closures:** _none_

#### `bridge/__init__.py`
- **Module-level symbols/assignments:** _none_
- **Top-level functions:** _none_
- **Classes / schemas:**
  - _none_
- **Nested implementation functions/closures:** _none_

#### `bridge/trading_pipeline.py`
- **Module-level symbols/assignments:** `_ENGINE_ROOT` (L30), `_PIPELINE_DIR` (L31), `_pipeline_dir_text` (L32), `_DTFMT` (L39), `TRADING_PIPELINE_VERSION` (L42), `TRADING_PIPELINE_IMPLEMENTATION_VERSION` (L43), `TRADING_PIPELINE_LAST_MODIFIED` (L44), `MBL_EXTENSION_CANDLES` (L45), `TEHRAN` (L47), `_local_dt_cache: dict[int, datetime]` (L84), `_epoch_cache: dict[datetime, int]` (L96), `_display_epoch_cache: dict[str, int]` (L108)
- **Top-level functions:** `emit_progress` (L50), `timed` (L58), `load_module` (L70), `load_engine` (L80), `local_datetime` (L87), `epoch` (L99), `display_epoch` (L111), `build_candle_buckets` (L123), `build_candle_objects` (L181), `_index_selected` (L211), `select_reaction_serialization_items` (L219), `serialize` (L242), `serialize_blue_lines` (L286), `serialize_a_zones` (L306), `serialize_s_zones` (L333), `serialize_e_zones` (L398), `serialize_stopalls` (L441), `bridge_datetime` (L508), `bridge_direction` (L522), `bridge_mode` (L526), `bridge_color` (L530), `_bridge_horizon` (L536), `_bridge_in_horizon` (L543), `_bridge_proven_strict_event` (L547), `_bridge_stop_view` (L587), `_bridge_reaction_confirmation` (L607), `_bridge_order_identity` (L631), `_bridge_parent_stop` (L833), `_bridge_a_stop` (L854), `_bridge_behavior_stop` (L875), `_bridge_blue_formation` (L890), `_bridge_project_reaction` (L913), `_bridge_project_reset` (L956), `_bridge_project_blue` (L979), `_bridge_full_lines_by_ordinal` (L1015), `_bridge_project_a` (L1027), `_bridge_project_s` (L1117), `_bridge_source_index` (L1173), `_bridge_parent_behavior_for_e` (L1181), `_bridge_project_e` (L1225), `_bridge_project_stopall` (L1272), `_bridge_audit_order_key` (L1341), `build_bridge_output` (L1351), `validate_order_audit_bridge` (L1456), `serialize_order_audit` (L1524), `parse_arguments` (L1598), `load_engines` (L1671), `prepare_market_context` (L1709), `create_e_detector` (L1827), `calculate_full_direction_state` (L1875), `calculate_direction_with_order_b_feedback` (L2210), `prepare_pipeline_state` (L2272), `calculate_direction_range_state` (L2440), `finalize_direction_visibility` (L2542), `serialize_direction_payload` (L2779), `serialize_primary_order` (L2920), `serialize_primary_structures` (L2949), `calculate_primary_structures` (L3053), `build_direction_output` (L3099), `build_response_payload` (L3139), `main` (L3193)
- **Classes / schemas:**
  - `BridgeProjection` (L639)
    - fields: _none_
    - methods/properties: `__init__` (L647), `physical_order` (L666), `parent_order` (L711), `current_order` (L718), `order_audit` (L773)
  - `EngineBundle` (L1578)
    - fields: `reaction: object` (L1579), `blue_line: object` (L1580), `a_zone: object` (L1581), `s_zone: object` (L1582), `e_zone: object | None` (L1583), `lifecycle: object | None` (L1584), `primary: object | None` (L1585)
    - methods/properties: _none_
  - `MarketContext` (L1589)
    - fields: `seconds: list[object]` (L1590), `candles: list[object]` (L1591), `lower_index: object` (L1592), `chronology: object` (L1593), `start_index: int` (L1594), `end_index: int` (L1595)
    - methods/properties: _none_
  - `PipelineState` (L1792)
    - fields: `directions: tuple[str, ...]` (L1795), `results: dict[str, object]` (L1796), `reusable_full_context: bool` (L1797), `initial_order_geometry: dict[str, object]` (L1798), `internal_reaction_identities: dict[str, set[tuple[int, int]]]` (L1799), `full_e_zones: dict[str, list[object]]` (L1800), `full_e_detectors: dict[str, object]` (L1801), `full_s_detectors: dict[str, object]` (L1802), `full_lines_by_direction: dict[str, list[object]]` (L1803), `full_a_by_direction: dict[str, list[object]]` (L1804), `invalid_a_identities_by_direction: dict[str, set[tuple[datetime, int]]]` (L1805), `invalid_s_identities_by_direction: dict[str, set[tuple[datetime, int]]]` (L1806), `full_s_by_direction: dict[str, list[object]]` (L1807), `full_s_candidates_by_direction: dict[str, list[object]]` (L1808)
    - methods/properties: _none_
  - `FullDirectionState` (L1812)
    - fields: `e_zones: list[object]` (L1815), `e_detector: object` (L1816), `s_detector: object` (L1817), `blue_lines: list[object]` (L1818), `a_zones: list[object]` (L1819), `invalid_a_identities: set[tuple[datetime, int]]` (L1820), `invalid_s_identities: set[tuple[datetime, int]]` (L1821), `s_zones: list[object]` (L1822), `s_candidates: list[object]` (L1823), `initial_s_zones: list[object]` (L1824)
    - methods/properties: _none_
  - `DirectionRangeState` (L2409)
    - fields: `blue_lines: list[object]` (L2412), `a_zones: list[object]` (L2413), `s_candidates: list[object]` (L2414), `accepted_s_zones: list[object]` (L2415), `e_zones: list[object]` (L2416), `invalid_a_identities: set[tuple[datetime, int]]` (L2417), `invalid_s_identities: set[tuple[datetime, int]]` (L2418)
    - methods/properties: _none_
  - `DirectionVisibilityState` (L2422)
    - fields: `blue_lines: list[object]` (L2425), `a_zones: list[object]` (L2426), `s_zones: list[object]` (L2427), `e_zones: list[object]` (L2428), `stopalls: list[object]` (L2429), `prepared_order_audit: list[object]` (L2430), `projection_s_zones: list[object]` (L2434), `projection_e_zones: list[object]` (L2435), `projection_stopalls: list[object]` (L2436), `primary_groups: dict[str, list[object]]` (L2437)
    - methods/properties: _none_
- **Nested implementation functions/closures:** `build_candle_buckets.cached_decimal` (L132), `create_e_detector.direct_geometry` (L1846), `serialize_direction_payload.build_legacy_payload` (L2806), `serialize_direction_payload.serialize_reactions_from_one_selection` (L2838), `serialize_direction_payload.build_payload` (L2879), `serialize_primary_order.value` (L2923), `serialize_primary_structures.point` (L2955), `calculate_primary_structures.commit_high` (L3074)

#### `pipeline/__init__.py`
- **Module-level symbols/assignments:** `_pipeline_dir` (L10), `__all__` (L22)
- **Top-level functions:** _none_
- **Classes / schemas:**
  - _none_
- **Nested implementation functions/closures:** _none_

#### `pipeline/a_zone_detector.py`
- **Module-level symbols/assignments:** `A_ZONE_VERSION` (L20), `A_ZONE_LAST_MODIFIED_DATE` (L21)
- **Top-level functions:** `detect_a_zones` (L798)
- **Classes / schemas:**
  - `BlueState` (L25)
    - fields: `ordinal: int` (L26), `line: object` (L27), `formation_index: int` (L28), `formation_time: datetime` (L29), `stop_index: int | None` (L30), `stop_time: datetime | None` (L31), `stop_event_time: datetime | None` (L32), `stop_level: Decimal` (L33), `stop_event_extreme: Decimal | None` (L34)
    - methods/properties: _none_
  - `AZone` (L38)
    - fields: `direction: str` (L39), `blue_1_ordinal: int` (L40), `blue_2_ordinal: int` (L41), `blue_1_source_time: datetime` (L42), `blue_2_source_time: datetime` (L43), `blue_1_stop_time: datetime` (L44), `blue_2_stop_time: datetime` (L45), `blue_1_stop_level: Decimal` (L46), `blue_2_stop_level: Decimal` (L47), `continuation_level: Decimal` (L48), `continuation_source_index: int` (L49), `continuation_source_time: datetime` (L50), `trigger_index: int` (L51), `trigger_time: datetime` (L52), `trigger_event_time: datetime` (L53), `reaction_number: int` (L54), `reaction_first_time: datetime` (L55), `reaction_break_time: datetime` (L56), `source_index: int` (L57), `source_time: datetime` (L58), `price: Decimal` (L59), `formation_route: str | None` (L62), `blue_1_stop_event_time: datetime | None` (L63), `blue_2_stop_event_time: datetime | None` (L64)
    - methods/properties: _none_
  - `AZoneDetector` (L67)
    - fields: _none_
    - methods/properties: `__init__` (L68), `extreme_name` (L108), `_strict_cross` (L111), `_better` (L114), `_main_index` (L117), `_lower_window` (L120), `_first_crossing` (L125), `_range_extreme` (L167), `_formation` (L201), `_reset_formation_time` (L218), `_build_blue_states` (L230), `_double_stop_a_candidates` (L259), `_pair_trigger` (L322), `_reaction_confirmation_time` (L482), `_first_reaction_after` (L487), `_inherited_stop` (L504), `_a_source` (L554), `_detect_ordinary_a` (L575), `_filter_special_a` (L696), `detect` (L760), `_a_was_stopped_before` (L772)
- **Nested implementation functions/closures:** _none_

#### `pipeline/blue_line_detector.py`
- **Module-level symbols/assignments:** `BLUE_LINE_VERSION` (L18), `FIBONACCI_RATIO` (L19)
- **Top-level functions:** `_is_color` (L48), `_main_candle` (L52), `_stops_on_index` (L59), `fibonacci_level` (L75), `_intrabar_pending_confirmation` (L84), `count_scale_strikes` (L142), `_build_scale_blue_line` (L230), `_build_reset_blue_line` (L268), `detect_blue_lines` (L322), `public_blue_lines` (L430), `mark_internal_blue_lines` (L439)
- **Classes / schemas:**
  - `ScaleStrike` (L23)
    - fields: `source_index: int` (L24), `source_time: datetime` (L25), `extreme: Decimal` (L26)
    - methods/properties: _none_
  - `BlueLine` (L30)
    - fields: `direction: str` (L31), `kind: str` (L32), `reaction_number: int` (L33), `previous_strike_count: int | None` (L34), `strike_count: int | None` (L35), `fibonacci_level: Decimal | None` (L36), `source_index: int` (L37), `source_time: datetime` (L38), `source_extreme: Decimal` (L39), `broken_level: Decimal | None` (L40), `line_price: Decimal` (L41), `start_time: datetime` (L42), `end_time: datetime` (L43), `calculation_valid: bool` (L44), `behavior_internal: bool` (L45)
    - methods/properties: _none_
- **Nested implementation functions/closures:** `mark_internal_blue_lines.owner_is_internal` (L452), `mark_internal_blue_lines.geometry_is_internal` (L458)

#### `pipeline/core_utils.py`
- **Module-level symbols/assignments:** `CORE_UTILS_VERSION` (L5), `OrderIdentity: TypeAlias` (L16)
- **Top-level functions:** `as_decimal` (L11), `order_identity` (L19), `reaction_identity` (L24)
- **Classes / schemas:**
  - _none_
- **Nested implementation functions/closures:** _none_

#### `pipeline/direction_policy.py`
- **Module-level symbols/assignments:** `DIRECTION_POLICY_VERSION` (L11), `Direction` (L17), `BULLISH` (L57), `BEARISH` (L64)
- **Top-level functions:** `policy_for` (L49)
- **Classes / schemas:**
  - `DirectionPolicy` (L21)
    - fields: `direction: Direction` (L22), `extreme_attr: Literal['low', 'high']` (L23), `opposite_extreme_attr: Literal['high', 'low']` (L24), `first_reaction_tag: Literal['RED', 'GREEN']` (L25), `context_tag: Literal['GREEN', 'RED']` (L26)
    - methods/properties: `opposite_direction` (L29), `strict_cross` (L32), `better_extreme` (L35), `choose_extreme` (L38), `confirmation_cross` (L41)
- **Nested implementation functions/closures:** _none_

#### `pipeline/e_zone_detector.py`
- **Module-level symbols/assignments:** `E_ZONE_VERSION` (L25), `E_ZONE_IMPLEMENTATION_VERSION` (L26), `E_ZONE_LAST_MODIFIED` (L27)
- **Top-level functions:** `detect_e_zones` (L1115)
- **Classes / schemas:**
  - `EZone` (L31)
    - fields: `direction: str` (L32), `family: str` (L33), `number: int` (L34), `parent_type: str` (L35), `parent_source_index: int` (L36), `parent_source_time: datetime` (L37), `parent_price: Decimal` (L38), `parent_stop_index: int` (L39), `parent_stop_time: datetime` (L40), `parent_stop_event_time: datetime` (L41), `order_direction: str` (L42), `order_reaction_number: int` (L43), `order_mode: str` (L44), `order_causes: tuple[str, ...]` (L45), `order_parent_stop_cause_time: datetime | None` (L46), `order_first_index: int` (L47), `order_first_time: datetime` (L48), `order_break_index: int` (L49), `order_break_time: datetime` (L50), `order_confirmation_time: datetime` (L51), `order_box_top: Decimal` (L52), `order_box_top_source_index: int` (L53), `order_box_top_source_time: datetime` (L54), `order_box_bottom: Decimal` (L55), `order_box_bottom_source_index: int` (L56), `order_box_bottom_source_time: datetime` (L57), `order_stop_level: Decimal` (L58), `order_stop_source_index: int` (L59), `order_stop_source_time: datetime` (L60), `source_index: int` (L61), `source_time: datetime` (L62), `price: Decimal` (L63), `decision_index: int` (L64), `decision_time: datetime` (L65), `decision_event_time: datetime` (L66)
    - methods/properties: _none_
  - `EZoneDetector` (L69)
    - fields: _none_
    - methods/properties: `__init__` (L70), `sequence_resets` (L228), `sequence_resets` (L232), `_reset_time` (L246), `_main_index` (L249), `_first_cross_position` (L253), `_stop_value` (L270), `_build_extreme_sparse` (L273), `_extreme_position` (L302), `_first_parent_stop` (L322), `_confirmation_for` (L335), `_confirmation` (L338), `_reaction_first_time` (L341), `_parent_stop` (L345), `parent_stop` (L353), `_extreme_between` (L360), `_zone` (L376), `set_consumed_s_evidence` (L481), `_apply_consumed_s_evidence` (L493), `continuation_chain_from_s` (L511), `replace_with_earlier_continuation` (L561), `resolve_same_source_conflicts` (L604), `restore_independent_s_roots` (L648), `_invalid_s_without_order_cause` (L709), `_discover_candidate_chains` (L733), `_reconcile_candidate_chains` (L825), `detect` (L1102)
- **Nested implementation functions/closures:** `EZoneDetector.replace_with_earlier_continuation.descends_from_owner` (L570), `EZoneDetector.resolve_same_source_conflicts.outranks` (L622), `EZoneDetector._reconcile_candidate_chains.valid_order` (L856), `EZoneDetector._reconcile_candidate_chains.parent_active` (L862), `EZoneDetector._reconcile_candidate_chains.stopped_by` (L935), `EZoneDetector._reconcile_candidate_chains.ownership_priority` (L991), `EZoneDetector._reconcile_candidate_chains.collect_lineage` (L1077)

#### `pipeline/lifecycle_engine.py`
- **Module-level symbols/assignments:** `STOP_ALL_VERSION` (L24), `STOP_ALL_IMPLEMENTATION_VERSION` (L25), `STOP_ALL_LAST_MODIFIED` (L26), `SEQUENCE_PRIORITY` (L29)
- **Top-level functions:** `sequence_priority` (L37), `advance_dominant_behavior` (L121), `detect_stopalls` (L530), `resolve_order_context` (L543), `visible_a_zones_after_s_stops` (L632), `module_priority` (L649), `module_identity` (L663), `module_stop_event` (L672), `strictly_beyond_boundary` (L686), `dominant_module` (L691), `split_a_zones_by_dominant_stops` (L703), `blocked_orders_while_invalid_leg_heads_are_live` (L906), `consumed_s_evidence_after_larger_stop` (L929), `s_zones_for_module_engines` (L1071), `s_zones_for_stopall` (L1101), `visible_s_zones_after_module_resets` (L1120), `reconcile_stopall_lifecycle` (L1298), `visible_a_zones_after_module_boundaries` (L1331), `reaction_number_is_internal` (L1378), `point_is_inside_healthy_reaction` (L1392), `filter_internal_behavior_outputs` (L1415), `finalize_behavior_visibility` (L1428), `visible_a_zones` (L1523)
- **Classes / schemas:**
  - `StopAll` (L43)
    - fields: `direction: str` (L44), `number: int` (L45), `source_index: int` (L46), `source_time: datetime` (L47), `price: Decimal` (L48), `decision_index: int` (L49), `decision_time: datetime` (L50), `decision_event_time: datetime` (L51), `gate_type: str` (L52), `gate_event_time: datetime` (L53), `stopped_behavior_type: str` (L54), `stopped_behavior_key: str` (L55), `stopped_behavior_count: int` (L56), `underlying_e_family: str | None` (L57), `underlying_e_number: int | None` (L58), `order_direction: str | None` (L59), `order_reaction_number: int | None` (L60), `order_mode: str | None` (L61), `order_causes: tuple[str, ...]` (L62), `order_parent_stop_cause_time: datetime | None` (L63), `order_first_index: int | None` (L64), `order_first_time: datetime | None` (L65), `order_break_index: int | None` (L66), `order_break_time: datetime | None` (L67), `order_confirmation_time: datetime | None` (L68), `order_box_top: Decimal | None` (L69), `order_box_top_source_index: int | None` (L70), `order_box_top_source_time: datetime | None` (L71), `order_box_bottom: Decimal | None` (L72), `order_box_bottom_source_index: int | None` (L73), `order_box_bottom_source_time: datetime | None` (L74), `order_stop_level: Decimal | None` (L75), `order_stop_source_index: int | None` (L76), `order_stop_source_time: datetime | None` (L77), `stop_index: int | None` (L78), `stop_time: datetime | None` (L79), `stop_event_time: datetime | None` (L80), `donor_type: str | None` (L85), `donor_source_index: int | None` (L86), `donor_source_time: datetime | None` (L87), `donor_color: str | None` (L88), `donor_number: int | None` (L89), `donor_price: Decimal | None` (L90), `donor_stop_time: datetime | None` (L91), `donor_stop_event_time: datetime | None` (L92)
    - methods/properties: _none_
  - `_DominantBehavior` (L96)
    - fields: `kind: str` (L99), `family: str` (L100), `number: int | None` (L101), `count: int` (L102), `latest: object` (L103)
    - methods/properties: `priority` (L106), `armed` (L110), `key` (L114)
  - `StopAllDetector` (L142)
    - fields: _none_
    - methods/properties: `__init__` (L143), `_strict_stop` (L164), `_dominates_e` (L181), `_stopall_from_e` (L190), `_optional_int` (L249), `_optional_decimal` (L253), `_stopall_from_s` (L256), `detect` (L344)
- **Nested implementation functions/closures:** `StopAllDetector.detect.armed_stop_before` (L356), `StopAllDetector.detect.accept` (L406), `StopAllDetector.detect.process_s_event` (L410), `visible_s_zones_after_module_resets.cached_stop_event` (L1149)

#### `pipeline/order_audit_engine.py`
- **Module-level symbols/assignments:** `ORDER_AUDIT_ENGINE_VERSION` (L15), `ORDER_AUDIT_ENGINE_LAST_MODIFIED` (L16), `OrderMatch` (L430)
- **Top-level functions:** `relabel_primary_causes` (L19), `dominant_post_behavior_stops` (L71), `order_b_reset_event_time` (L117), `discover_order_b_reset_legs` (L148), `discover_accepted_order_b_reset_legs` (L352), `order_b_leg_identity` (L437), `_parent_stop_cause_key` (L1777), `_collect_s_ledger_entries` (L1786), `_collect_e_ledger_entries` (L1818), `_merge_prepared_identities` (L1847), `_single_owner_parent_stop_causes` (L1890), `prepare_order_audit` (L1928), `accepted_audit_entry` (L1948), `accepted_audit_entries` (L1981), `order_identity_is_internal` (L1994)
- **Classes / schemas:**
  - `PostBehaviorStop` (L34)
    - fields: `behavior_type: str` (L35), `behavior_source_index: int` (L36), `behavior_source_time: datetime` (L37), `event_time: datetime` (L38)
    - methods/properties: _none_
  - `OrderBBehaviorAnchor` (L42)
    - fields: `behavior_type: str` (L43), `behavior_source_index: int` (L44), `behavior_source_time: datetime` (L45), `priority: int` (L46), `number: int` (L47)
    - methods/properties: _none_
  - `OrderBResetLeg` (L51)
    - fields: `post_stop: PostBehaviorStop` (L52), `anchor_behavior_type: str` (L53), `anchor_behavior_source_index: int` (L54), `anchor_behavior_source_time: datetime` (L55), `anchor_behavior_extreme: Decimal` (L56), `reset_reaction: object` (L57), `reset_confirmation_time: datetime` (L58), `reset_source_index: int` (L59), `reset_broken_level: Decimal` (L60), `reset_time: datetime` (L61), `leg_boundary: Decimal` (L62), `leg_source_index: int` (L63), `leg_source_time: datetime` (L64), `strict_break_time: datetime` (L65), `reaction_number: int` (L66), `physical_reaction: object` (L67), `physical_confirmation_time: datetime` (L68)
    - methods/properties: _none_
  - `OrderAuditEngineMixin` (L461)
    - fields: _none_
    - methods/properties: `_order_stop` (L464), `order_stop` (L493), `_first_healthy_direct_geometry` (L500), `_trend_leg_direct_order` (L575), `_direct_parent_stop_order` (L627), `_compute_direct_parent_stop_order` (L647), `_merge_order_candidate` (L739), `_enforce_single_parent_stop_owner` (L773), `order_candidates` (L800), `_first_order` (L891), `_has_sequence_reset_between` (L907), `_index_order_audit_identity` (L918), `_clear_order_audit` (L928), `_invalidate_carried_order_caches` (L934), `_invalidate_post_stop_order_cache` (L941), `register_order_b_reset_legs` (L945), `_reparent_primary_high_causes` (L1012), `register_primary_high` (L1060), `reconcile_primary_high_labels` (L1099), `_register_order_audit` (L1119), `visual_order_lifecycle` (L1194), `_cross_order` (L1216), `cross_order` (L1237), `_unconsumed_s_orders` (L1244), `_initial_order_records` (L1281), `_initial_record_match` (L1340), `_initial_order_match` (L1354), `_gate_owned_initial_order` (L1369), `_carried_orders_for_parent` (L1392), `_post_stop_accepted_orders_for_parent` (L1453), `_blocked_by_gate_owned_order` (L1535), `_rebuild_accepted_order_audit` (L1546), `rebuild_accepted_order_audit` (L1732), `ensure_accepted_order_audit` (L1747)
  - `SOrderAuditMixin` (L2003)
    - fields: _none_
    - methods/properties: `_first_order_after` (L2006), `_order_matches_after` (L2062), `_record_a_order_audit` (L2084), `_audit_stopped_a` (L2119), `_order_stop` (L2132), `_order_stop_crossed` (L2144), `_shared_order_stop_cross` (L2150)
- **Nested implementation functions/closures:** `OrderAuditEngineMixin._post_stop_accepted_orders_for_parent.add_match` (L1467), `OrderAuditEngineMixin._rebuild_accepted_order_audit.valid_parent_stop_cause` (L1557)

#### `pipeline/PL_PH_detector.py`
- **Module-level symbols/assignments:** `PL_PH_VERSION` (L20), `PL_PH_LAST_MODIFIED` (L21)
- **Top-level functions:** `resolve_primary_highs` (L83), `relabel_primary_order` (L118), `formed_matching_legs` (L124), `resolve_stopall_ownership` (L140), `order_meets_structure_gate` (L152), `strict_cross` (L163), `_extreme` (L176), `_matching_seeds` (L185), `detect_bearish` (L224), `_activate_cycle` (L321), `_next_point` (L339)
- **Classes / schemas:**
  - `StructureOrder` (L25)
    - fields: `direction: str` (L26), `reaction_number: int` (L27), `first_index: int` (L28), `break_index: int` (L29), `confirmation_event_time: datetime` (L30), `stop_level: Decimal` (L31), `stop_source_index: int` (L32), `stop_index: int` (L33), `stop_event_time: datetime` (L34), `causes: tuple[str, ...]` (L35), `box_top: Decimal | None` (L36), `box_bottom: Decimal | None` (L37), `reaction_mode: str | None` (L38), `audit_causes: tuple[dict[str, object], ...]` (L39)
    - methods/properties: _none_
  - `PrimaryPoint` (L43)
    - fields: `kind: str` (L44), `number: int` (L45), `source_index: int` (L46), `source_time: datetime` (L47), `price: Decimal` (L48), `trigger_index: int` (L49), `trigger_event_time: datetime` (L50), `decision_index: int` (L51), `decision_event_time: datetime` (L52), `order: StructureOrder` (L53), `cycle_id: str | None` (L54), `identity_source: PrimaryPoint | None` (L55)
    - methods/properties: _none_
  - `MatchingBehaviorLeg` (L59)
    - fields: `source_index: int` (L60), `source_time: datetime` (L61), `price: Decimal` (L62), `reference_stopall_index: int` (L63), `second_behavior_index: int` (L64), `trigger_index: int` (L65), `trigger_event_time: datetime` (L66), `stop_index: int | None` (L67), `stop_event_time: datetime | None` (L68)
    - methods/properties: _none_
  - `PrimaryResult` (L72)
    - fields: `highs: list[PrimaryPoint]` (L73), `lows: list[PrimaryPoint]` (L74), `mbl: MatchingBehaviorLeg | None` (L75), `status: str` (L76), `post_pl3_orders: list[StructureOrder]` (L77), `cycle_id: str | None` (L78), `cycles: list[PrimaryResult]` (L79), `qualification_event_time: datetime | None` (L80)
    - methods/properties: _none_
  - `_CycleCheckpoint` (L312)
    - fields: `result: PrimaryResult` (L313), `reference_price: Decimal` (L314), `gate_index: int` (L315), `cursor: datetime` (L316), `phase: str` (L317), `reset_high: bool` (L318)
    - methods/properties: _none_
  - `NativePrimaryOrders` (L435)
    - fields: _none_
    - methods/properties: `__init__` (L445), `confirm_high` (L449), `__call__` (L454)
- **Nested implementation functions/closures:** `resolve_primary_highs.role_order` (L104)

#### `pipeline/reaction_engine.py`
- **Module-level symbols/assignments:** `REACTION_ENGINE_VERSION` (L21), `REACTION_ENGINE_IMPLEMENTATION_VERSION` (L22), `REACTION_ENGINE_LAST_MODIFIED` (L23), `_ORDER_GATE_CACHE_MAX_ENTRIES` (L25), `_SEQUENCE_TIME_INDEXES: dict[int, tuple[Sequence[Candle], list[datetime]]]` (L27), `_REFLECTED_VIEWS: dict[int, tuple[Sequence[Candle], _ReflectedCandles]]` (L636), `_LOWER_TIMEFRAME_INDEXES: dict[int, tuple[Sequence[Candle], LowerTimeframeIndex]]` (L932)
- **Top-level functions:** `classify_candle_color` (L94), `opposite_direction` (L99), `mirror_candle` (L563), `mirror_candidate` (L583), `mirror_analysis` (L602), `_reflected_view` (L639), `published_reaction_candidate` (L709), `_decimal_value` (L807), `shared_lower_timeframe_index` (L937), `build_behavior_reaction_views` (L1205), `directional_a_stop_order_finder` (L1316)
- **Classes / schemas:**
  - `Candle` (L30)
    - fields: `index: int` (L31), `timestamp: datetime` (L32), `display_time: str` (L33), `tag: str` (L34), `open: Decimal` (L35), `high: Decimal` (L36), `low: Decimal` (L37), `close: Decimal` (L38)
    - methods/properties: _none_
  - `Candidate` (L42)
    - fields: `first_idx: int` (L43), `first_time: str` (L44), `box_top_source_idx: int` (L45), `box_top_source_time: str` (L46), `box_top: Decimal` (L47), `box_bottom_source_idx: int` (L48), `box_bottom_source_time: str` (L49), `box_bottom: Decimal` (L50), `mode: str` (L51), `anchor_idx: int | None` (L52), `anchor_value: Decimal | None` (L53), `leg_boundary_value: Decimal | None` (L54), `break_idx: int | None` (L55), `break_time: str | None` (L56), `intrabar_start: datetime | None` (L57), `cross_direction_origin: bool` (L58), `cross_direction_chain_owner: bool` (L59), `order_gate_decision: str | None` (L60), `behavior_public_number: int | None` (L61), `behavior_public_box_top: Decimal | None` (L62), `behavior_public_box_bottom: Decimal | None` (L63), `behavior_confirmation_time: datetime | None` (L64), `behavior_first_time: datetime | None` (L65), `behavior_internal: bool` (L66)
    - methods/properties: _none_
  - `ResetEvent` (L70)
    - fields: `index: int` (L71), `display_time: str` (L72), `second_time: str | None` (L73), `broken_level: Decimal` (L74), `from_first_idx: int` (L75)
    - methods/properties: _none_
  - `IntrabarAnalysis` (L79)
    - fields: `event_second: Candle` (L80), `extreme: Decimal` (L81), `extreme_source: Candle` (L82)
    - methods/properties: _none_
  - `DetectionResult` (L86)
    - fields: `direction: str` (L87), `reactions: list[Candidate]` (L88), `resets: list[ResetEvent]` (L89), `start_index: int` (L90), `end_index: int` (L91)
    - methods/properties: _none_
  - `DetectorBase` (L104)
    - fields: _none_
    - methods/properties: `__init__` (L105), `_shared_time_index` (L130), `seconds_between` (L140), `main_source_for_time` (L145), `minimum_low` (L158), `maximum_high` (L167)
  - `BullishDetector` (L177)
    - fields: _none_
    - methods/properties: `green_run_peak_before` (L178), `breakout_analysis` (L188), `mode_a_invalidation_before_breakout` (L214), `confirmed_reset_before_breakout` (L250), `post_breakout_reset` (L270), `detect` (L285)
  - `_ReflectedCandles` (L611)
    - fields: _none_
    - methods/properties: `__init__` (L619), `__len__` (L623), `__getitem__` (L626)
  - `BearishDetector` (L649)
    - fields: _none_
    - methods/properties: `__init__` (L657), `red_run_bottom_before` (L671), `breakdown_analysis` (L675), `invalidation_high_break_before_breakdown` (L680), `confirmed_reset_before_breakdown` (L685), `post_breakdown_reset` (L691), `detect` (L698)
  - `LowerTimeframeIndex` (L812)
    - fields: _none_
    - methods/properties: `__init__` (L819), `first_less` (L860), `first_greater` (L863), `range_minimum` (L866), `range_maximum` (L870), `_range_query` (L874), `_first` (L912)
  - `ReflectedLowerTimeframeIndex` (L950)
    - fields: _none_
    - methods/properties: `__init__` (L955), `first_less` (L959), `first_greater` (L962), `range_minimum` (L965), `range_maximum` (L969)
  - `MarketChronology` (L974)
    - fields: _none_
    - methods/properties: `__init__` (L993), `opposite_direction` (L1016), `main_index` (L1020), `lower_bounds` (L1029), `lower_window` (L1040), `_reset_cache_key` (L1047), `_reaction_cache_key` (L1059), `reset_time` (L1073), `reaction_confirmation` (L1092), `canonical_order_stop` (L1140)
  - `UnifiedReactionDetector` (L1379)
    - fields: _none_
    - methods/properties: `__init__` (L1389), `bull` (L1421), `bear` (L1429), `_append_reaction` (L1436), `_append_reset` (L1518), `_refine` (L1536), `_candidate_from_confirmation_remainder` (L1557), `_first_initial` (L1642), `_first_direct_same_direction_after_reset` (L1655), `_first_geometry_after_reset` (L1693), `first_geometry_after_reset` (L1746), `_reaction_break_indices` (L1753), `first_order_reaction_after_gate` (L1768), `_earliest_confirmed_geometry` (L1917), `_build_direct_candidate` (L1991), `_scan_direct_candidate` (L2049), `_owner_boundary_before_confirmation` (L2079), `_result` (L2120), `detect` (L2129)
- **Nested implementation functions/closures:** `build_behavior_reaction_views.path_is_contained` (L1225), `directional_a_stop_order_finder.find` (L1330), `UnifiedReactionDetector.first_order_reaction_after_gate.cache_result` (L1784), `UnifiedReactionDetector.first_order_reaction_after_gate.confirmed_no_later_than_gate` (L1795)

#### `pipeline/s_zone_detector.py`
- **Module-level symbols/assignments:** `S_ZONE_VERSION` (L22), `S_ZONE_IMPLEMENTATION_VERSION` (L23), `S_ZONE_LAST_MODIFIED` (L24)
- **Top-level functions:** `detect_s_zones` (L1422)
- **Classes / schemas:**
  - `SZone` (L28)
    - fields: `direction: str` (L29), `color: str` (L30), `formation_type: str` (L31), `a_ordinal: int` (L32), `a_source_index: int` (L33), `a_source_time: datetime` (L34), `a_price: Decimal` (L35), `a_stop_index: int` (L36), `a_stop_time: datetime` (L37), `a_stop_event_time: datetime` (L38), `order_direction: str | None` (L39), `order_reaction_number: int | None` (L40), `order_mode: str | None` (L41), `order_first_index: int | None` (L42), `order_first_time: datetime | None` (L43), `order_break_index: int | None` (L44), `order_break_time: datetime | None` (L45), `order_confirmation_time: datetime | None` (L46), `order_box_top: Decimal | None` (L47), `order_box_top_source_index: int | None` (L48), `order_box_top_source_time: datetime | None` (L49), `order_box_bottom: Decimal | None` (L50), `order_box_bottom_source_index: int | None` (L51), `order_box_bottom_source_time: datetime | None` (L52), `order_stop_level: Decimal | None` (L53), `order_stop_source_index: int | None` (L54), `order_stop_source_time: datetime | None` (L55), `reset_reaction_number: int | None` (L56), `reset_time: datetime | None` (L57), `source_index: int` (L58), `source_time: datetime` (L59), `price: Decimal` (L60), `decision_index: int` (L61), `decision_time: datetime` (L62), `decision_event_time: datetime` (L63)
    - methods/properties: _none_
  - `SZoneDetector` (L66)
    - fields: _none_
    - methods/properties: `__init__` (L67), `_main_index` (L194), `_lower_window` (L197), `_reaction_confirmation_time` (L202), `reaction_confirmation_time` (L207), `_reset_time` (L214), `_a_confirmation_time` (L217), `_trend_extreme` (L225), `_a_stopped` (L230), `_first_a_stop` (L233), `first_a_stop` (L269), `_resolved_order_backed_zone` (L276), `_candidate_source` (L295), `_candidate_source_last` (L310), `_first_trend_reaction_after_order` (L330), `_nested_trend_reaction` (L342), `_simple_candidate` (L372), `_type3_reset_leg` (L381), `_type3_has_trend_reaction` (L397), `_first_type3` (L406), `_type4_has_blue` (L456), `_first_type4` (L467), `_build_type4_zone` (L537), `_candidate_after_order` (L590), `_a_source_event_time` (L631), `_a_owned_by_s` (L640), `_a_pair_is_reset_reset` (L681), `eligible_a_zones` (L695), `_candidate_timing` (L699), `_candidate_before_order` (L744), `_candidate_event_time` (L788), `candidate_event_time` (L803), `_blue_formation_time` (L810), `_candidate_cross_has_blue` (L840), `_has_ordinary_trend_reaction` (L857), `_candidate_crossed` (L868), `_decision` (L873), `_build_type3_zone` (L999), `_build_order_backed_zone` (L1057), `detect` (L1228), `reconcile_shared_order_stops` (L1305)
- **Nested implementation functions/closures:** _none_

### 13.6 Master Bullish ↔ Bearish directional mirror matrix

This pre-existing matrix governs upstream directional transformation only; it does not define the explicitly deferred bullish PH/PL calculation. This matrix is normative for directional transformation. Bullish is the canonical geometry; Bearish is derived mechanically. A row marked **directional** must transform exactly as shown. A concept listed in Section 13.7 is invariant and must not be direction-flipped.

| Rule / primitive | Bullish | Bearish | Classification |
|---|---|---|---|
| Direction name | `bullish` | `bearish` | directional |
| Directional extreme field | `Low` / `low` | `High` / `high` | directional |
| Opposite extreme field | `High` / `high` | `Low` / `low` | directional |
| Better directional extreme | lower (`<`) | higher (`>`) | directional |
| Directional aggregate | `minimum` / `min` | `maximum` / `max` | directional |
| First Reaction role | `FirstRed` / `RED` | `FirstGreen` / `GREEN` | directional |
| Pre-First context role | `GREEN` | `RED` | directional |
| Reaction confirmation | first strict `High > BoxTop` | first strict `Low < BoxBottom` | directional |
| Reaction confirmation edge | `BoxTop` | `BoxBottom` | directional |
| Opposite evolving box edge | `BoxBottom` | `BoxTop` | directional |
| Reaction Reset | first strict `Low < confirmed BoxBottom` | first strict `High > confirmed BoxTop` | directional |
| Blue Fibonacci level | `BoxTop − 0.618 × (BoxTop − reference)` | `BoxBottom + 0.618 × (reference − BoxBottom)` | directional |
| New Scale strike | strictly lower `Low` | strictly higher `High` | directional |
| Scale-strike confirmation color | `GREEN` | `RED` | directional |
| Scale Blue source extreme | decisive `Low` | decisive `High` | directional |
| Scale Blue line price | `Low + (High − Low) / 3` | `High − (High − Low) / 3` | directional |
| Reset Blue source extreme | Reset-candle `Low` | Reset-candle `High` | directional |
| Reset Blue line price | `Low + (High − Low) / 5` | `High − (High − Low) / 5` | directional |
| Blue strict stop | first directional `Low < source_extreme` | first directional `High > source_extreme` | directional |
| Ordinary A source selection | minimum `Low` | maximum `High` | directional |
| A frozen source after trigger | minimum `Low` through exact confirmation | maximum `High` through exact confirmation | directional |
| A strict stop | directional strict lower penetration | directional strict upper penetration | directional |
| S Type-3 source | minimum `Low`, last owner on equality | maximum `High`, last owner on equality | directional |
| S Type-4 source | minimum `Low`, last owner on equality | maximum `High`, last owner on equality | directional |
| S Blue candidate crossing | strict lower directional cross | strict upper directional cross | directional |
| Physical opposite Order direction used by current behavior | Bearish Reaction/Order | Bullish Reaction/Order | directional |
| Physical Order strict stop in current calculation | `High > OrderStop` | `Low < OrderStop` | directional |
| S Red race event | physical Order `High > OrderStop` | physical Order `Low < OrderStop` | directional |
| E parent/behavior strict stop | lower directional penetration | upper directional penetration | directional |
| Armed S/E owner strict stop | first lower-TF `Low < owner price` | first lower-TF `High > owner price` | directional |
| Direct E-child donor | exact owner identity and parent-stop provenance | exact owner identity and parent-stop provenance | invariant |
| E source | minimum `Low` across complete boundary candles | maximum `High` across complete boundary candles | directional |
| Order_B reset Reaction role | Bullish reset Reaction / `FirstRed` | Bearish reset Reaction / `FirstGreen` | directional |
| Order_B frozen boundary | `LL = minimum Low(...)` | `HH = maximum High(...)` | directional |
| Order_B anchor extension | `LL < anchor Low` | `HH > anchor High` | directional |
| Order_B strict break after Reset | first calculation candle containing post-Reset `Low < LL` | first calculation candle containing post-Reset `High > HH` | directional |
| Order_B canonical opposite Reaction | first canonical Bearish Reaction | first canonical Bullish Reaction | directional |
| DirectionPolicy `strict_cross` | `<` | `>` | directional |
| DirectionPolicy `better_extreme` | `<` | `>` | directional |
| DirectionPolicy `choose_extreme` | `min` | `max` | directional |
| DirectionPolicy `confirmation_cross` | `>` | `<` | directional |
| Reaction mechanical reflection used internally | `O,H,L,C` canonical coordinates | `O'=-O, H'=-L, L'=-H, C'=-C` plus role reflection | implementation mirror |

All strict rows remain strict. Equality is not converted into a crossing in either direction.

### 13.7 Direction-invariant contract matrix

The following semantics are intentionally identical in Bullish and Bearish. Mirroring any of these merely because price direction changes is an error.

| Invariant | Exact contract |
|---|---|
| Time / chronology | configured calculation-timeframe ownership is invariant; lower-TF chronology is used only for explicitly required within-candle ordering/provenance and is not mirrored |
| Doji | `close == open` is always `GREEN` |
| Decimal | price-sensitive decisions use Decimal semantics; direction does not change numeric representation |
| Strict equality | equality never satisfies a strict crossing |
| Exact StopAll owner | one exact S/E identity; count `1` is highest but unarmed; count `>=2` arms the latest occurrence |
| Replacement and chronology | unrelated higher formation disarms lower future eligibility; a completed earlier strict stop remains valid |
| Retrospective E source | exact direct child may reuse its matched parent stop; independent accepted E may donate the current armed owner stop only in its own source candle with strict source extreme, before E decision; later-bucket stop ineligible |
| Physical identity | canonical Reaction/Order identity is `(FirstIndex, BreakIndex)` |
| Provenance concepts | `parent-stop`, `reset-leg`, `carried-live`, `accepted-live` retain the same meanings |
| Stage ownership | Reaction, Blue, A, S, E, OrderAudit, Lifecycle/StopAll owners remain the same modules |
| Behavior-family names | `S Blue`, `S Red`, `E Blue`, `E Red`, and `StopAll` names are not color-swapped |
| S/E dominance priority | `S Blue < E Blue < S Red < E Red`; A is excluded and StopAll is a boundary |
| Numbering | Reaction, E and StopAll numbering rules remain structurally identical |
| Stable ordering | deterministic tie keys retain the same semantic ordering contract |
| Public/internal meaning | visibility/internal-state semantics do not reverse with market direction |
| Serialization schema | public field names and response shape are identical across directions |
| Hard StopAll boundary | historical boundary/reset semantics are identical |
| Calculation vs presentation | internal historical evidence may survive even when not public |
| Canonical membership | geometry-only evidence cannot become a physical canonical Order in either direction |
| Invalid S parentage | an explicitly invalid S cannot create/retain `parent-stop` cause in either direction |
| Order cause merge | multiple causes may attach to one physical identity without duplicating the Order |
| E same-source priority | Red E outranks Blue E; within family, higher number wins; remaining exact ties preserve earlier accepted object |
| S Type-3/Type-4 tie | earlier exact decision event wins; Type-3 owns only a true exact-event tie |
| S decision same-position race | exact same lower-TF position for Order stop and candidate cross produces no S decision |

### 13.8 Reconstruction-quality stage contract

This table makes the stage chain reconstructable without relying on examples. The detailed prose in Sections 4–12 remains normative; this table is a compact cross-stage contract and must agree with it.

| Stage | Authoritative inputs / prior state | Opening trigger / gate | Source or selection rule | Chronology / tie rule | Stop / terminal rule | Downstream ownership |
|---|---|---|---|---|---|---|
| Reaction / Reset | normalized main candles, selected lower-TF chronology, directional state | required First role after opposite context; strict confirmation | directional box geometry; opposite edge may evolve only through chronology available by confirmation | lower-TF order resolves confirmation vs invalidation/reset; equal eligible opposite extremes retain earliest owner | confirmed Reaction resets only on first strict directional break of confirmed opposite edge | publishes canonical Reaction/Reset stream; cross-direction internal classification occurs after both directions exist |
| Blue | canonical same-direction Reactions and Resets | scale strike growth or Reset event | Fibonacci reference from Mode-A boundary or previous opposite edge; decisive directional strike/source | Break-candle intrabar confirmation only through exact Reaction-confirmation lower-TF row inclusive | first strict directional crossing of `source_extreme`; double-stop Reset Blue may remain calculation-invalid evidence | calculation Blue ledger feeds A; public Blue requires `calculation_valid and not behavior_internal` |
| A | immutable Blue calculation ledger + canonical Reactions | ordinary adjacent valid Blue pair or approved double-stop route | directional extreme from trigger main-candle open through exact confirming Reaction event | exact chronology and deterministic tie ownership; equal source retains earliest unless helper explicitly differs | first strict directional A stop after confirming Reaction; stale pre-`not_before` stop cannot be reused | stop opens S space |
| S | accepted A, A stop, canonical physical Order context, Reactions/Resets/Blue | post-A-stop eligibility; choose order-free Type-3/4 or order-backed route | Type-3/4 and Simple/Advanced source rules in Section 7 | exact event race; Type-3 vs Type-4 earlier event wins, Type-3 only on exact tie; Order-stop/candidate same-position race gives no decision | S Blue on qualified candidate strict cross; S Red on accepted physical Order strict stop; accepted-Order reconciliation may convert open S to Red | accepted S begins provisional E1 chain; historical/invalid evidence may remain calculation context but not fabricate parentage |
| E | accepted S/E parent, exact parent stop, canonical Order ledger | first strict parent stop + physical Order with exact strict stop | directional extreme over complete main candles containing parent stop through Order stop | winner Order is earliest stop; same stop uses larger FirstIndex; `decision_event=max(parent_stop,order_stop)` | recursive child starts only after preceding E strict stop; sequence reset may invalidate crossings spanning hard boundary | reconciled E feeds lifecycle/StopAll and canonical OrderAudit rebuild |
| Order_A | accepted final strict behavior stop + canonical opposite-direction Reaction registry | parent-stop direct/bounded geometry that is canonically registered; A parent must survive S ownership/current invalid-A filtering | canonical Reaction identity; canonical Order stop from `MarketChronology` | competing parent-stop candidates: earliest confirmation, then FirstIndex, then BreakIndex | exact opposite-direction strict Order stop | identity-keyed physical Order with accepted `parent-stop` provenance; nonaccepted A cause is removed |
| Order_B | accepted lifecycle stop + later reset same-direction Reaction + canonical Reset | eligible post-stop reset leg with accepted behavior anchor strictly before reset Reaction First | LL/HH from closed anchor-source .. reset-First range; strict extension beyond anchor | first calculation candle containing a strict post-Reset break owns the gate; next accepted A in/earlier than that main candle expires setup; opposite Reaction First may be in that same break candle while exact confirmation must remain after the strict crossing | physical Order then follows canonical opposite Order stop rules | adds `reset-leg` provenance to canonical physical identity; exact lower-TF break remains audit provenance and same-candle ordering evidence |
| Lifecycle / StopAll | accepted S/E chronology and lower-TF strict stops | one exact highest owner; count `>=2` arms it; an E or qualified S Red donates StopAll after a completed stop | priority, exact identity, direct E-parent proof or independent same-bucket donor proof are direction-invariant; only strict price comparison mirrors | prior stop survives unrelated replacement; direct E child or qualifying independent physical E may use a stop inside its retrospectively labeled source candle | StopAll hard boundary clears owner/count/pending completed stop but retains history | final visibility/lineage closure and StopAll source map |
| OrderAudit | physical identity ledger + accepted S/E/A causes + lifecycle results | merge accepted ledgers and reconcile current accepted causes | dedupe by `(FirstIndex, BreakIndex)`; provenance is attached to identity | stable cause/order sorting; retain pre-range identity when a visible behavior references it | strict stop computed only when not already authoritative; invalid parent cannot fabricate cause | canonical serialized physical Order history |
| Serialization | finalized calculation state only | requested direction/presentation range | projection only; Decimal values stringified under existing contract | stable source ordering; presentation filtering occurs after calculation | never recalculates trading decisions | response envelope + optional read-only Bridge Output |

### 13.9 Historical package/source integrity notes

**Patch branch note:** All 12 real Python Source paths from the uploaded engine.zip are embedded byte-exact; the legacy historical Source audit below refers only to the 5.4.26 baseline and is not new regression evidence.

1. The authoritative supplied Engine tree contains the **12** Python Source paths in Section 1. It does not contain a root `__init__.py`; the stale virtual zero-byte entry from Reference `5.4.25` is removed in this synchronization.
2. Section 16 embeds each current production Python file byte-for-byte.
3. The historical missing `run_blue_line` package wrapper import is repaired in 5.4.32. The production Bridge path is the supported calculation entry.
4. Unit, targeted and full RAW regression evidence for this revision is recorded in Section 14. Prior verification claims remain historical evidence for their own Source revisions.

## 14. Verification scope and historical evidence

### 14.0p Current PH/PL task verification boundary
<!-- PRIMARY-VERIFICATION-BEGIN -->

This is bounded evidence for the approved bearish MBL formation correction.
Earlier task counts and dependent PH-5 examples are superseded by the explicit
whole-cycle rejection rule above; they are not reused as current PASS results.

- **PASS:** full current Engine suite,193 tests. Regression cases cover exact
  PH-reference identity, qualification before PH promotion but activation after
  it, absence of invalid native callbacks, unrelated independent continuation,
  pending/no-PH MBL suppression, per-cycle confirmation and requested horizons.
- **PASS:** full current Chart suite,249 tests. No frontend production Source
  change participates in the calculation correction.
- **PASS (complete supplied RAW):** original full XAUUSD September28..October6
  and USOIL October1..23 5-second streams at30seconds, both directions. USOIL
  has27 physical PHs,0 PLs and3 confirmed cycle legs; XAUUSD has16 physical PHs,
  8 PLs and4 confirmed cycle legs. Both user-rejected MBLs are absent. Original
  XAUUSD and USOIL PH-1/MBL anchors and independent October22 anchor remain.
- **PASS:** all bullish legacy outputs and bearish Reaction/Reset/Blue/A/S/E
  arrays equal the prior approved baseline. Native physical Order identities,
  geometry and strict-stop chronology remain equal; PH provenance and final
  StopAll ownership reflect removal of invalid cycles. Previous PH/PL counts
  derived from those cycles are intentionally changed.
- **PASS (real HTTP/browser):** current Engine1.2.2 returns27PH/0PL/3MBL on the
  full USOIL chart. Both rejected MBL object IDs are absent from the Chart
  object tree; original and October22 MBL IDs remain. No browser application
  error was observed. This is runtime evidence, not global trading correctness.
- **PASS (independent read-only review):**77 focused tests plus chronology and
  confirmation-horizon probes; saved full-output comparisons found no physical
  native Order geometry change or orphan PH provenance. RAW pipelines/browser
  were not rerun independently by that reviewer.
- **NOT APPLICABLE:** bullish primary calculation remains explicitly deferred.
- Canonical Plugin/Vault tools are unavailable. Current explicit user teaching
  and the accepted references govern the local extension. No release,
  publication or RAW mutation was requested or performed.

<!-- PRIMARY-VERIFICATION-END -->


### 14.0 V5.4.33 baseline verification — HISTORICAL

- **PASS:** 8 focused chronology, strict/equality, arming, decision-time, same-bucket, and mirror scenarios (16 directional subcases), `python -m unittest discover -s tests -v`.
- **PASS:** 7 complete available continuous RAW datasets at 30s × both directions, with baseline-vs-patched serialized stage comparison (14 direction-pairs): six datasets byte-equivalent in all eight output stages, seventh (2026-10-22..23 USOIL) only one E→StopAll transition in Bullish. Reaction/Reset/Blue/A/S/OrderAudit and Bearish stay exact for all 14 pairs. The historical XAUUSD August–September dataset (354,698 rows) completed both full pipelines with exact zero differences in all eight stages of both directions.
- **PASS:** FXCM_USOIL 2026-10-23 control anchors 15:13 StopAll, 16:11:30 S, 16:32 E, 18:00 S, 18:22:30 S, 18:33 E; new 18:56 StopAll strict crossing at 18:56:10; stable deterministic rerun in both directions.
- **PASS:** complete source import and compilation, current Source snapshot byte hashes and mirrored Reference text (see release readme for final scope).
- **PASS:** historic August XAUUSD full 354,698-row continuous 30s calculation in both directions, compared before/after. Historical available RX-01, SE-01 and S Red 2026-10-21 06:17 anchors are present and preserved.
- **NOT RUN:** separate external historical fixture-suite beyond available uploaded/Library RAW and external UI integration outside archive.
- **Final status:** `REGRESSION NOT VERIFIED` for *unbundled external fixture-suite/UI coverage*, notwithstanding all seven RAW datasets and targeted tests PASS.

### 14.0c V5.4.32 verification — HISTORICAL

- V5.4.32 Source integrity / chronology bugfix evidence is superseded as the Current verification scope. See the original V5.4.32 release for its exact test coverage and limitations.


### 14.0b V5.4.31 verification — HISTORICAL

- **PASS:** 10 test cases: 8 focused prior-approved direct S-Red StopAll scenarios (both directions) and 2 complete Reference integrity/mirror checks.
- **PASS:** full supported pipeline/serializer, six RAW-derived input scenarios × two directions × before/after = **24 completed runs**, with stable Reaction, Reset, Blue, A output unchanged in all **12** before/after pairs.
- **PASS:** from original FXCM_USOIL 5s October 16–21, calculation restricted by input to October 20 18:00 onward: two `E2 Blue` occurrences (`21:34`, `23:54`) then accepted `S Red` (`06:17`) convert to `StopAll1` with accepted decision event `06:21:35`. `StopAll1` donor is an accepted S Red, owner key `E2 blue`, owner count `2`, gate event = S decision event.
- **PASS:** full-range USOIL October and both directions, XAUUSD October 8–9, XAUUSD September 28–October 6, USOIL September 24–October 3 and largest 354,698-row XAUUSD August 25–September 23, with permitted downstream S/E/StopAll/OrderAudit changes attributable to the approved direct gate.
- **PASS:** 5.4.30 production Bridge, OrderAudit and all other unaffected Source bytes remain unchanged; no serializer schema changes. Both References embed identical complete production Source.
- **NOT RUN:** independent external UI selected-range caller integration and the complete exhaustive historical user-anchor matrix. The current 5.4.30 Bridge does not expose the `5.4.28` selected-range CLI option; the selected calculation starts at the supplied input boundary.
- **Scope limitation:** the 5.4.29 synchronized-group-E-Parent patch remains outside this targeted merge; this is not a cumulative 5.4.29 rebase.

### 14.0a Previous `5.4.30` verification — HISTORICAL

- **PASS:** compile/import all supported Source, main-chart 30s and complete RAW history, XAUUSD Sep 22–29 both directions.
- **PASS:** targeted 3-case regression including immutable A-stop chronology, independent First, nested Advanced S Blue, public OrderAudit cause/identity.
- **PASS:** separate FXCM USOIL 5s and FOREXCOM XAUUSD Oct 8–9 5s RAW, both directions, full calculation and serializer.
- **PASS:** before/after upstream Reaction/Reset/Blue/A hash equality for all three datasets, both directions.
- **PASS:** production bridge OrderAudit identity consistency; unchanged exported schemas; Source/Reference byte synchronization.
- **PASS:** repeated target 30s full-context calculation in both directions; upstream and downstream S/E/OrderAudit signatures are identical.
- **NOT RUN:** complete historical regression-anchor suite (not packaged), exact synthetic price-transform mirror invariant suite, cumulative Library 5.4.29 rebase equivalence.
- **Final status: REGRESSION NOT VERIFIED** for replacing a newer 5.4.29-derived Current deployment.

### 14.1 Historical `5.4.26` verification claims — NOT RE-RUN for this patch

- **PASS — Source compile/runtime:** all 11 actual Python Source files compile; the supported production Bridge executes successfully. The historical unsupported package wrapper issue was unchanged at 5.4.26 and repaired in 5.4.32.
- **PASS — targeted Order_B regression:** on `RAW FOREXCOM_XAUUSD 5S FROM 2026-09-28 20-44-00 TO 2026-10-03 00-29-35.json`, 30-second Bullish calculation maps the exact LL crossing `2026-09-29 20:26:40` to main candle `20:26:30`; canonical Bearish Reaction `20:26:30 → 20:28:30` now receives the `reset-leg` / Order_B cause. The stale later `20:32:00` reset-leg selection is removed. The subsequent canonical Bearish Reaction `20:44:00 → 20:45:30` receives the reset-leg belonging to Bullish Reaction `20:29:30`.
- **PASS — preserved Order_A rule:** the valid parent-stop Order_A supported by E1 Blue `2026-09-29 19:51:30` remains present, while nonaccepted detected A `2026-09-29 20:15:30` still cannot create A-owned `parent-stop` provenance.
- **PASS — RX-01 regression:** Bullish Reaction `2026-09-16 22:44:00 → 22:44:30` remains present on the dedicated XAUUSD fixture.
- **PASS — SE-01 regression:** all four known final-visible E tie anchors retain the corrected later-First Order selection: Bullish `2026-09-29 21:28:00`, Bullish `2026-09-30 12:37:30`, Bearish `2026-09-29 21:03:30`, Bearish `2026-10-02 08:02:00`.
- **PASS — full continuous RAW Before/After execution:** 9 executable RAW datasets × 2 directions × baseline/fixed = **36 complete 30-second runs**, all exit code `0` with valid JSON output.
- **PASS — upstream zero-drift invariant:** across all 18 baseline/fixed direction pairs, `Reaction`, `Reset`, `Blue`, and `A` outputs are byte-equivalent at the serialized stage level. All differences begin in Order_B ownership/feedback or its permitted downstream S/E/StopAll consequences.
- **PASS — Order_B causal differential:** 73 common reset-leg causes moved to an earlier physical Order; in all 73, the new Order First is exactly the 30-second candle containing the strict lower-TF break evidence. Additional added/removed reset-leg causes arise only through accepted lifecycle feedback under the same corrected gate.
- **PASS — deterministic stable output:** repeated complete target-RAW execution is identical in Bullish and Bearish after removal of non-stable timing telemetry.
- **PASS — performance sanity:** largest XAUUSD RAW (`2026-08-25→09-23`) baseline/fixed wall times were Bullish `69.891s→69.781s` and Bearish `49.474s→49.880s`; no material performance regression was observed.
- **PASS — Bullish/Bearish mirror:** the same main-candle break gate and exact-confirmation safeguard are shared in both directions; all nine RAW datasets completed in both directions.
- **PASS — Source/Reference synchronization:** manifest hashes and Section 16 embedded bytes are regenerated from the Current Source; both directional References embed identical production Source bytes.

### 14.2 Previous `5.4.25` verification — HISTORICAL / SUPERSEDED

Reference `5.4.25` and its recorded verification remain historical evidence for the immediately preceding Source. Its exact lower-TF Order_B First-time gate is superseded by the user-approved calculation-timeframe break-candle rule in `5.4.26`.

## 15. Current and historical revision record

### Current PH/PL local extension — UNRELEASED

- **Modified:** `2026-10-26T19:42:22+03:30`.
- **Rule owner:** current approved bearish teaching; complete active rules are in Section 13.4a.
- **Source ownership:** new primary-state module; shared Lifecycle matching helper; Bridge full-history invocation/serialization. Existing OrderAudit remains the sole physical Order/provenance owner.
- **Mirror scope:** bullish primary calculation deferred; both References embed the same shared production Source.
- **Verification:** current bounded evidence and limitations are in Section 14.0p; historical release claims below are not current feature verification.


### `5.4.33` independent accepted-E StopAll donor and strict source-candle chronology

- **Modified:** `2026-10-23 19:33:06 +02:00`.
- **Baseline:** exact uploaded `engine(1).zip` V5.4.32 (SHA256 recorded in release readme).
- **Changed Source:** `bridge/trading_pipeline.py` `1.10.2 (impl 1.11.2)` → `1.10.3 (impl 1.11.3)`; `pipeline/lifecycle_engine.py` `1.18.5 (impl 1.20.5)` → `1.18.6 (impl 1.20.6)`.
- **Rule:** uniquely missing accepted independent S-root E source may donate to current armed dominant StopAll if the owner's first strict crossing is within that E source bucket, its source extreme strictly penetrates the owner's price, and the crossing precedes E decision. Existing E sources/provenance and direct child rule remain unchanged.
- **Output:** target `2026-10-23 18:56:00` Bullish `E1 Blue` becomes `StopAll1` from armed `E1 Blue ×2`, `gateEvent=18:56:10`; every other stable stage across six available RAW datasets/both directions is unchanged.
- **Mirror:** common function with Bullish `<` / Bearish `>` strict comparisons; equal threshold not a stop.
- **Verification:** seven complete available RAW datasets (including full August XAUUSD Library RAW) × both directions 30s, 8 focused cases × both directions, deterministic target replay, available historical anchors, and full Source snapshot integrity PASS. Separate unbundled external historical test suite / UI integration NOT RUN; exhaustive external REGRESSION NOT VERIFIED.


### `5.4.32` Source integrity and chronology bugfix patch

- **Modified:** 2026-10-23 12:29:10 +02:00.
- **Baseline:** exact user-supplied `engine.zip` V5.4.31, not a cumulative historical merge.
- **Changed:** Bridge/Decimal/StopAll feature gate, OrderAudit physical confirmation index, Blue exact confirmation, S physical direction, Lifecycle S-stop containing-candle ownership, and compatibility package wrapper.
- **Mirroring:** shared direction-invariant code, exact opposite strict geometry; both directional references embed identical production source.
- **Verification:** see ZIP `readme.txt`, including any incomplete historical anchors and tests.

### `5.4.31` direct accepted S Red after armed Blue exact owner — PATCH BRANCH / BEHAVIORAL RESTORATION

- **Modified:** `2026-10-21 18:35:00 +03:30`.
- **Source baseline:** exact supplied `engine.zip` V5.4.30, not an inferred cumulative merge.
- **Changed production file:** `pipeline/lifecycle_engine.py` `1.18.2 (impl 1.20.2)` → `1.18.3 (impl 1.20.3)` on this branch only.
- **Behavior:** accepted S Red (either mode) after `>=2` exactly identical dominant Blue S/E occurrences creates StopAll1 at the S decision event; no Blue Strict Stop prerequisite. Historical Mode-B stopped-owner gate remains as fallback.
- **Preserved:** native V5.4.30 A-stop independent Order_A and unchanged Bridge/other detector Source; all existing public schema fields.
- **Not merged:** 5.4.28 selected-range CLI and 5.4.29 synchronized-parent E StopAll change.
- **Mirror:** direction-invariant Lifecycle code; both directions tested.
- **Verification:** 10 tests and six RAW-derived scenarios in both directions for before/after (24 runs), upstream serialized equality, no deletion of any pre-existing StopAll source, complete Source/Reference byte check; external exhaustive UI integration NOT RUN.

### `5.4.30` stopped-A independent physical Order_A — PATCH BRANCH / BEHAVIORAL RULE

- **Modified:** `2026-10-18 12:31:00 +03:30`.
- **Source baseline:** supplied `engine.zip` containing `5.4.26` Reference, not Project Library `5.4.29`.
- **Changed Source:** `bridge/trading_pipeline.py` `1.8.1 (impl 1.9.1) → 1.10.0 (impl 1.11.0)`; `pipeline/order_audit_engine.py` `1.5.5 → 1.6.0`.
- **Behavior:** first independently complete opposite Order_A after accepted A stop is eligible despite enclosing earlier same-direction opposite Reaction. Exact First, confirmation, source, strict stop, physical identity and cause remain authoritative. `S Advanced` follows unchanged nested-trend-Reaction test.
- **Output:** new geometry-only physical Orders may have `reactionNumber=0`; no change to canonical Reaction numbering; downstream S/E/OrderAudit outputs can change by design.
- **Mirroring:** one direction-invariant shared implementation; Bullish A → Bearish FirstGreen with reflected price comparators.
- **Verification:** compile/import, target and independent RAW full-context 30s both-direction pipeline/serialization, targeted three-case tests PASS; deterministic target rerun PASS; upstream hash equivalence PASS; exact historical/cumulative Reference 5.4.29 regression NOT RUN. **REGRESSION NOT VERIFIED**.

### `5.4.26` Order_B calculation-timeframe break-candle correction — HISTORICAL BASELINE

- **Document version:** `5.4.26`
- **Previous Reference:** `5.4.25`
- **Modified:** `2026-10-07 02:18:23 +03:30`
- **Changed Source:** `pipeline/order_audit_engine.py` `1.5.4 → 1.5.5` only.
- **General rule:** Order_B First eligibility is owned by the configured calculation candle containing the strict post-Reset LL/HH break. A canonical opposite Reaction whose First is that same main candle is eligible; exact lower-TF crossing remains evidence for Reset-before-break, confirmation-after-break, and audit provenance rather than a later First-candle gate.
- **Accepted-A expiry:** compared by owning calculation candle to the Order_B break candle.
- **Intentional target differences:** the 30-second XAUUSD Bullish case now produces Order_B at `2026-09-29 20:26:30` and `20:44:00`; the previous reset-leg Order at `20:32:00` is no longer selected for the `20:20:30` reset setup.
- **Unchanged:** RX-01, SE-01, accepted-final-A Order_A eligibility, A/S/Reaction/Blue rules, Decimal/strict-price semantics, physical identity, serialization schema.
- **Mirror impact:** Bullish `Low < LL` and Bearish `High > HH` share identical main-candle ownership and exact intrabar safeguard semantics.
- **Documentation integrity:** the stale root `__init__.py` virtual snapshot entry is removed because it is absent from the authoritative supplied package; no production file is added or deleted by this documentation correction.

### `5.4.25` RX-01 + SE-01 + accepted-final-A Order_A correction — HISTORICAL / SUPERSEDED

- **Document version:** `5.4.25`
- **Previous Reference:** `5.4.24`
- **Modified:** `2026-10-07 00:59:53 +03:30`
- **Changed Source:** `pipeline/reaction_engine.py` `9.8.0→9.8.1` (impl `9.9.0→9.9.1`); `pipeline/e_zone_detector.py` `6.16.1→6.16.2` (impl `6.18.2→6.18.3`); `pipeline/order_audit_engine.py` `1.5.3→1.5.4`; `bridge/trading_pipeline.py` `1.8.0→1.8.1` (impl `1.9.0→1.9.1`).
- **Unchanged behavioral owners:** A detector, S detector/ownership, Blue, Lifecycle/StopAll, core utilities and direction policy.
- **Trading-output changes:** restores valid initial confirmation-candle Reaction continuation; corrects E exact-stop Order ties by larger FirstIndex; prevents nonaccepted A behavior from creating/retaining A-owned Order_A provenance.
- **Mirror impact:** identical state/identity/chronology/tie semantics in both directions with directional price predicates mechanically mirrored.
- **Serialization/API shape:** unchanged; only accepted identities/provenance and their downstream corrected results may differ.


### `5.4.24` direct E-child StopAll correction — HISTORICAL / SUPERSEDED

- **Document version:** `5.4.24`
- **Previous Reference:** `5.4.23`
- **Modified:** `2026-10-04 21:40:18 +03:30`
- **Production Source behavioral change:** `pipeline/lifecycle_engine.py` only, `1.18.1 → 1.18.2` and implementation `1.20.1 → 1.20.2`.
- **Serialization/API shape:** unchanged; the causal E donor still uses `sequence-group-stop` and existing provenance fields.
- **Trading-output change:** a direct E child materializes a completed strict stop of its armed exact parent even when its retrospective source timestamp equals or precedes the parent stop. Unrelated higher E replacements retain the strict source-time cutoff.
- **Mirror impact:** identical parent identity, chronology and donor checks; only Bullish `Low < price` versus Bearish `High > price` differs.

### `5.4.23` exact-owner StopAll correction — HISTORICAL / SUPERSEDED

- **Document version:** `5.4.23`
- **Previous Reference:** `5.4.22`
- **Modified:** `2026-10-04 21:01:35 +03:30`
- **Production Source behavioral change:** `pipeline/lifecycle_engine.py` only, `1.18.0 → 1.18.1` and implementation `1.20.0 → 1.20.1`.
- **Serialization/API shape:** unchanged; legacy `opposite-s-group-stop` name is retained only for semantically valid transitions.
- **Trading-output change:** invalid lower-priority or unstopped Blue promotions are removed; valid completed owner stops use the existing donor contracts. Downstream S/E/StopAll/OrderAudit may change after the first corrected boundary.
- **Mirror impact:** identical identity, priority, arming, replacement, chronology, donor and reset rules; Bullish `Low < price` mirrors Bearish `High > price`.
- **Manifest correction:** include the zero-byte root `__init__.py` present in both the inspected archive and live Engine tree.

### `5.4.22` documentation completeness synchronization — HISTORICAL / SUPERSEDED

- **Document version:** `5.4.22`
- **Previous Reference:** `5.4.21`
- **Modified:** `2026-10-04 13:12:49 +00:00`
- **Production Source behavioral changes:** `NONE`
- **Production Source module version changes:** `NONE`
- **Serialization/API changes:** `NONE`
- **Trading-output changes caused by this revision:** `NONE`
- **Mirror impact:** semantic mirror is unchanged; documentation now exposes it explicitly and exhaustively in one master matrix.
- **Corrections:** remove the nonexistent zero-byte root `__init__.py` from the manifest/snapshot; regenerate symbol coverage so `_invalid_s_without_order_cause` and the previously omitted Reaction module caches/indexes are represented.
- **Completeness additions:** mechanical AST symbol/schema index, Master Bullish↔Bearish Mirror Matrix, direction-invariant matrix, reconstruction-quality cross-stage contract, archive/source-integrity notes, explicit current verification status, and known wrapper defect disclosure.
- **Known unresolved Source issue:** the unsupported legacy `pipeline/__init__.py` wrapper imports missing `run_blue_line`; this documentation-only revision does not change that API/package Source.
- **Verification limitation:** the standalone unit suite is absent from the supplied package, so the historical `49 passed, 2 xfailed` result is not re-executed here.

### `5.4.21` Source behavior baseline — HISTORICAL

This was the executable calculation baseline for `5.4.22`. Reference `5.4.23` supersedes its StopAll eligibility behavior while retaining the unrelated accepted OrderAudit invariant repair.

### Earlier `5.4.20` / intermediate `5.4.21` calculation changes — HISTORICAL / SUPERSEDED

The later Blue-consumption feedback, Blue publication suppression, and dominant S-Red continuation exception that changed results relative to the supplied pre-refactor Engine are not active in this Source snapshot. Historical records remain evidence only.

## 16. Exact Production Source snapshot

Every currently discovered production Python file in the live Engine package, Bridge and Pipeline roots is embedded below. Preserve raw UTF-8 Source bytes, comments, whitespace and final-newline structure. Reconstruct by machine-readable markers, not Markdown reformatting. Section 1 and Section 13.5 are regenerated from this same discovered Source set.

### 16.1 `__init__.py` — Engine package marker

**SHA-256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`  
**Bytes:** `0`  
**LF count:** `0`

<!-- EXACT-SOURCE-BEGIN:__init__.py -->
````python
````
<!-- EXACT-SOURCE-END:__init__.py -->

### 16.2 `bridge/__init__.py` — Bridge package marker

**SHA-256:** `2bc59770b9d4313c0e6306287d074487b9e1672dbaf3ada9a8be381e7123f0b8`  
**Bytes:** `64`  
**LF count:** `1`

<!-- EXACT-SOURCE-BEGIN:bridge/__init__.py -->
````python
"""Bridge entrypoints for the TradingBot calculation engine."""
````
<!-- EXACT-SOURCE-END:bridge/__init__.py -->

### 16.3 `bridge/trading_pipeline.py` — Pipeline / Serialization

**SHA-256:** `d70481975d2b8e41c6271a02243862d967d5c906bbe1f2f23a432df6fc0f85a1`  
**Bytes:** `123325`  
**LF count:** `3231`

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
from bisect import bisect_left
from dataclasses import dataclass, field
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
from order_audit_engine import accepted_audit_entries, order_b_leg_identity

_DTFMT = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}"


TRADING_PIPELINE_VERSION = "1.11.0"
TRADING_PIPELINE_IMPLEMENTATION_VERSION = "1.14.2"
TRADING_PIPELINE_LAST_MODIFIED = "2026-10-26T19:31:03+03:30"
MBL_EXTENSION_CANDLES = 100

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
    primary: object | None = None


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
    parser.add_argument("--pl-ph", choices=("enabled", "disabled"), default="enabled")
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
    primary = (
        load_module("PL_PH_detector", _PIPELINE_DIR / "PL_PH_detector.py")
        if getattr(args, "pl_ph", "disabled") == "enabled" else None
    )
    return EngineBundle(reaction, blue_line, a_zone, s_zone, e_zone, lifecycle, primary)


def prepare_market_context(
    args, engines: EngineBundle, timings: dict[str, float]
) -> MarketContext:
    """Read, isolate, normalize and index the selected raw-data range."""
    source_bytes = timed(
        timings, "Read source file", lambda: args.data.read_bytes()
    )
    # Price lexemes must remain exact: orjson converts all JSON decimals to
    # binary float before the downstream Decimal(str(value)) normalization.
    # This can silently change strict crossings near a price boundary.
    source_bytes = source_bytes.removeprefix(b"\xef\xbb\xbf")
    source_rows = timed(
        timings, "Parse source JSON",
        lambda: json.loads(source_bytes, parse_float=Decimal),
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
    e_parent_order_first_exceptions: frozenset[tuple[datetime, datetime]] = frozenset(),
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
        e_parent_order_first_exceptions=e_parent_order_first_exceptions,
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

    # A detection is provisional. Only A that survives S ownership may create
    # a parent-stop Order_A used by downstream E/Order state. Later lifecycle
    # invalidation applies the same accepted-cause filter again.
    s_accepted_a_sources = {
        getattr(item, "source_time") for item in s_detector.eligible_a_zones
    }
    s_accepted_order_audit = accepted_audit_entries(
        s_detector.order_audit, s_accepted_a_sources
    )

    e_detector = create_e_detector(
        direction,
        e_engine,
        full_results,
        s_zones,
        chronology,
        geometry_detectors,
        s_accepted_order_audit,
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
            s_accepted_order_audit,
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
    e_parent_exceptions: set[tuple[datetime, datetime]] = set()
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
        accepted_e_stop_events={
            stopped[1]
            for e_zone in e_zones
            if (stopped := e_detector.parent_stop("E", e_zone)) is not None
        },
        opposite_confirmation_finder=lambda reaction: chronology.reaction_confirmation(
            opposite, reaction
        ),
        e_parent_order_first_exceptions_out=e_parent_exceptions,
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
        e_parent_order_first_exceptions=e_parent_exceptions,
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
            e_parent_order_first_exceptions=e_parent_exceptions,
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
    # Preserve only physical Order identities already backed by accepted A
    # provenance. Provisional/S-owned A candidates must not reopen Order_A.
    independent_a_order_identities = frozenset(accepted_orders)
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
        continuation = e_detector.continuation_chain_from_s(
            owner, evidence_s, independent_a_order_identities
        )
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
    *,
    stopall_enabled: bool,
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
        # The feedback pass and final visibility must use the SAME optional
        # StopAll contract. Otherwise the converged Order_B causes can name a
        # StopAll owner which the final pass intentionally never calculates.
        if stopall_enabled:
            e_zones, stopalls = engines.lifecycle.reconcile_stopall_lifecycle(
                state.e_detector, state.s_zones, state.e_zones,
                market.chronology, direction,
            )
        else:
            e_zones, stopalls = list(state.e_zones), []
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
        # A-stop Order_A geometry has its own independent post-stop First gate.
        # Reuse the already-detected opposite-direction engine and its cached
        # lower-TF chronology; continuous public Reaction ownership must not
        # suppress a complete nested post-stop Order geometry.
        initial_order_geometry = {
            direction: (
                lambda gate_index, gate_event, end_index,
                order_direction=engine.opposite_direction(direction):
                    geometry_detectors[order_direction].first_order_reaction_after_gate(
                        order_direction, gate_index, end_index, gate_event
                    )
            )
            for direction in ("bullish", "bearish")
        }
        calculation_directions = (
            ("bullish", "bearish")
            if engines.primary is not None and "bearish" in directions
            else directions
        )
        for direction in calculation_directions:
            state = calculate_direction_with_order_b_feedback(
                direction,
                engines,
                market,
                results,
                geometry_detectors,
                initial_order_geometry,
                timings,
                stopall_enabled=(args.lifecycle_engine is not None),
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
        initial_order_geometry = {
            direction: engine.directional_a_stop_order_finder(
                candles, seconds, direction
            )
            for direction in ("bullish", "bearish")
        }
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
    primary_groups: dict[str, list[object]] = field(default_factory=dict, kw_only=True)


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
    stopall_e_zones = e_zones
    detector = state.full_e_detectors.get(direction)
    if detector is not None:
        # E reconciliation can omit an otherwise accepted independent S root.
        # An omitted physical source must still be available as a StopAll donor.
        # Preserve existing dominant E objects/provenance: restoration may
        # replace an E at an already-accepted source, but that replacement is
        # only the final visibility decision, not a new StopAll donor.
        accepted_sources = {
            (item.source_index, item.source_time) for item in e_zones
        }
        independent = detector.restore_independent_s_roots(e_zones)
        missing = [
            item for item in independent
            if (item.source_index, item.source_time) not in accepted_sources
        ]
        if missing:
            stopall_e_zones = [*e_zones, *missing]
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
            stopall_e_zones,
            market.chronology,
            direction,
            lambda label, work: timed(timings, label, work),
        )

    if direction in state.full_e_detectors:
        # Preserve the preexisting final independent-root visibility policy.
        # Only missing physical donor identities were supplemented for StopAll.
        detector = state.full_e_detectors[direction]
        e_zones = detector.restore_independent_s_roots(e_zones)
        # Root restoration occurs after the detector's normal ledger rebuild.
        # Sync missing audit identities without deleting historical Orders.
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

    primary_groups = {
        "A": [item for item in direction_state.a_zones
              if (item.source_time, int(item.source_index)) not in direction_state.invalid_a_identities],
        "S": list(visible_s_zones), "E": list(e_zones), "StopAll": list(stopalls),
    }
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
        for item in state.full_s_detectors[direction].eligible_a_zones
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
        primary_groups=primary_groups,
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


def serialize_primary_order(order, market, owner_direction):
    """Preserve physical direction separately from the conceptual owner."""
    stamp = lambda index: epoch(market.candles[index].timestamp)
    def value(item):
        if isinstance(item, datetime):
            return epoch(item)
        if isinstance(item, Decimal):
            return str(item)
        return item
    return {
        "ownerDirection": owner_direction, "direction": order.direction,
        "reactionNumber": order.reaction_number,
        "reactionMode": order.reaction_mode,
        "types": [label for cause, label in (("parent-stop", "Order_A"), ("reset-leg", "Order_B"))
                  if cause in order.causes],
        "auditCauses": [{key: value(item) for key, item in cause.items()}
                        for cause in order.audit_causes],
        "firstIndex": order.first_index, "firstTime": stamp(order.first_index),
        "breakIndex": order.break_index, "breakTime": stamp(order.break_index),
        "confirmationEventTime": epoch(order.confirmation_event_time),
        "stopLevel": str(order.stop_level), "stopSourceIndex": order.stop_source_index,
        "stopSourceTime": stamp(order.stop_source_index),
        "stopHitIndex": order.stop_index, "stopHitTime": stamp(order.stop_index),
        "stopHitEventTime": epoch(order.stop_event_time), "causes": list(order.causes),
        "boxTop": str(order.box_top) if order.box_top is not None else None,
        "boxBottom": str(order.box_bottom) if order.box_bottom is not None else None,
    }


def serialize_primary_structures(primary, market):
    """Project finalized structure state without price or lifecycle decisions."""
    from PL_PH_detector import resolve_primary_highs, relabel_primary_order, formed_matching_legs
    final_highs = resolve_primary_highs(primary, through_index=market.end_index)
    cycles = getattr(primary, "cycles", None) or [primary]
    first_cycle_id = getattr(cycles[0], "cycle_id", None)
    def point(item):
        order = relabel_primary_order(item.order, final_highs)
        cycle_id = getattr(item, "cycle_id", None)
        origin = getattr(item, "identity_source", None) or item
        identity = f"bearish:{origin.kind}:{origin.number}:{origin.trigger_index}:{origin.decision_index}"
        origin_cycle_id = getattr(origin, "cycle_id", None)
        if origin_cycle_id is not None and origin_cycle_id != first_cycle_id:
            identity += f":{origin_cycle_id}"
        row = {
            "id": identity,
            "direction": "bearish", "kind": item.kind, "number": item.number,
            "sourceIndex": item.source_index, "sourceTime": epoch(item.source_time),
            "price": str(item.price), "triggerIndex": item.trigger_index,
            "triggerTime": epoch(market.candles[item.trigger_index].timestamp),
            "triggerEventTime": epoch(item.trigger_event_time),
            "decisionIndex": item.decision_index,
            "decisionTime": epoch(market.candles[item.decision_index].timestamp),
            "decisionEventTime": epoch(item.decision_event_time),
            "order": serialize_primary_order(order, market,
                                              "bearish" if item.kind == "PH" else "bullish"),
        }
        if cycle_id is not None:
            row["cycleId"] = cycle_id
        return row
    selected = lambda items: [point(item) for item in items
        if market.start_index <= item.source_index <= market.end_index
        and item.decision_index <= market.end_index]
    legs = []
    visible_cycles = []
    for cycle in cycles:
        leg = cycle.mbl
        if leg is None or leg.trigger_index > market.end_index:
            continue
        visible_cycles.append(cycle)
    for cycle, confirmation in formed_matching_legs(primary, through_index=market.end_index):
        leg = cycle.mbl
        row = {
            "id": f"bearish:MBL:{leg.reference_stopall_index}:{leg.second_behavior_index}",
            "direction": "bearish", "sourceIndex": leg.source_index,
            "sourceTime": epoch(leg.source_time), "price": str(leg.price),
            "referenceStopAllIndex": leg.reference_stopall_index,
            "secondBehaviorIndex": leg.second_behavior_index,
            "capTime": epoch(market.candles[leg.source_index + MBL_EXTENSION_CANDLES].timestamp)
                if leg.source_index + MBL_EXTENSION_CANDLES < len(market.candles)
                else epoch(market.candles[-1].timestamp +
                           market.chronology.timeframe * (leg.source_index + MBL_EXTENSION_CANDLES + 1 - len(market.candles))),
            "triggerIndex": leg.trigger_index,
            "triggerTime": epoch(market.candles[leg.trigger_index].timestamp),
            "triggerEventTime": epoch(leg.trigger_event_time),
            "confirmationIndex": confirmation.decision_index,
            "confirmationTime": epoch(market.candles[confirmation.decision_index].timestamp),
            "confirmationEventTime": epoch(confirmation.decision_event_time),
            "stopIndex": leg.stop_index if leg.stop_index is not None and leg.stop_index <= market.end_index else None,
            "stopTime": epoch(market.candles[leg.stop_index].timestamp) if leg.stop_index is not None and leg.stop_index <= market.end_index else None,
            "stopEventTime": epoch(leg.stop_event_time) if leg.stop_index is not None and leg.stop_index <= market.end_index else None,
        }
        if getattr(cycle, "cycle_id", None) is not None:
            row["cycleId"] = cycle.cycle_id
        legs.append(row)
    highs, lows = selected(final_highs), selected(primary.lows)
    high_by_source = {(row["sourceIndex"], row["sourceTime"]): row for row in highs}
    for row in highs:
        row["cycleIds"] = list(dict.fromkeys(
            item.cycle_id for item in primary.highs
            if item.source_index == row["sourceIndex"] and epoch(item.source_time) == row["sourceTime"]
            and item.decision_index <= market.end_index and getattr(item, "cycle_id", None) is not None))
    cycle_rows = [{
        "id": cycle.cycle_id, "direction": "bearish", "status": cycle.status,
        "referenceStopAllIndex": cycle.mbl.reference_stopall_index,
        "secondBehaviorIndex": cycle.mbl.second_behavior_index,
        "triggerIndex": cycle.mbl.trigger_index,
        "triggerTime": epoch(market.candles[cycle.mbl.trigger_index].timestamp),
        "triggerEventTime": epoch(cycle.mbl.trigger_event_time),
        "highCount": len(selected(cycle.highs)),
        "highIds": list(dict.fromkeys(high_by_source[(item.source_index, epoch(item.source_time))]["id"]
            for item in cycle.highs if item.decision_index <= market.end_index
            and (item.source_index, epoch(item.source_time)) in high_by_source)),
        "lowCount": sum(row.get("cycleId") == cycle.cycle_id for row in lows),
    } for cycle in visible_cycles if getattr(cycle, "cycle_id", None) is not None]
    post_orders = []
    for cycle in visible_cycles:
        for order in cycle.post_pl3_orders:
            if order.stop_index > market.end_index:
                continue
            row = serialize_primary_order(relabel_primary_order(order, final_highs), market, "bullish")
            if getattr(cycle, "cycle_id", None) is not None:
                row["cycleId"] = cycle.cycle_id
            post_orders.append(row)
    qualification = getattr(primary, "qualification_event_time", None)
    horizon = market.candles[market.end_index].timestamp + market.chronology.timeframe
    status = (visible_cycles[-1].status if visible_cycles else
              "waiting-for-stopall-break" if qualification is not None and qualification < horizon
              else "waiting-for-matching-behaviors")
    return {"primaryHighs": highs, "primaryLows": lows,
            "matchingBehaviorLegs": legs, "primaryStatus": status,
            "primaryCycles": cycle_rows, "postPL3Orders": post_orders}


def calculate_primary_structures(args, engines, market, state, visibility, timings):
    """Connect finalized full-history behaviors to existing native Order services."""
    groups = {"bearish": visibility.primary_groups}
    opposite_state = calculate_direction_range_state(
        "bullish", args, engines, market, state, timings
    )
    opposite_visibility = finalize_direction_visibility(
        "bullish", args, engines, market, state, opposite_state, timings
    )
    groups["bullish"] = opposite_visibility.primary_groups
    accepted_by_owner = {}
    for owner in ("bullish", "bearish"):
        detector = state.full_e_detectors[owner]
        s_detector = state.full_s_detectors[owner]
        accepted_sources = {item.source_time for item in s_detector.eligible_a_zones
            if (item.source_time, int(item.source_index))
            not in state.invalid_a_identities_by_direction[owner]}
        accepted_by_owner[owner] = accepted_sources
        groups[owner]["OrderAudit"] = engines.lifecycle.prepare_order_audit(
            detector, 0, len(market.candles)-1, s_detector, accepted_sources
        )
    def commit_high(point):
        detector = state.full_e_detectors["bearish"]
        detector.register_primary_high(point)
        groups["bearish"]["OrderAudit"] = engines.lifecycle.prepare_order_audit(
            detector, 0, len(market.candles)-1, state.full_s_detectors["bearish"],
            accepted_by_owner["bearish"],
        )

    resolver = engines.primary.NativePrimaryOrders(market.chronology, groups, on_high=commit_high)
    primary = engines.primary.detect_bearish(
        market.chronology, groups["bearish"]["S"], groups["bearish"]["E"],
        groups["bearish"]["StopAll"], resolver,
    )
    state.full_e_detectors["bearish"].reconcile_primary_high_labels(
        engines.primary.resolve_primary_highs(primary, through_index=market.end_index)
    )
    required = {order_identity(item["reaction"].first_idx, item["reaction"].break_idx)
                for item in visibility.prepared_order_audit}
    visibility.prepared_order_audit = engines.lifecycle.prepare_order_audit(
        state.full_e_detectors["bearish"], market.start_index, market.end_index,
        state.full_s_detectors["bearish"], accepted_by_owner["bearish"], required,
    )
    return primary


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
    primary = None
    if (direction == "bearish" and engines.primary is not None
            and direction in state.full_e_detectors and args.lifecycle_engine is not None):
        primary = timed(timings, "PH/PL - Bearish", lambda: calculate_primary_structures(
            args, engines, market, state, visibility, timings))
        visibility.stopalls = engines.primary.resolve_stopall_ownership(
            visibility.stopalls, primary, through_index=market.end_index,
        )
        validate_order_audit_bridge(
            visibility.prepared_order_audit, visibility.s_zones,
            visibility.e_zones, visibility.stopalls,
        )
    payload = serialize_direction_payload(
        direction, args, engines, market, state, visibility, timings
    )
    if primary is not None:
        payload.update(serialize_primary_structures(primary, market))
    return payload

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
        "primaryVersion": engines.primary.PL_PH_VERSION if engines.primary is not None else None,
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

### 16.4 `pipeline/__init__.py` — Compatibility package wrapper

**SHA-256:** `d22a1b81495a6c97b5eccc4d921b1ba4b709bfbcd39be6ef34b9014690b9f460`  
**Bytes:** `653`  
**LF count:** `28`

<!-- EXACT-SOURCE-BEGIN:pipeline/__init__.py -->
````python
"""Compatibility import surface for maintained Blue Line helpers.

Production detector modules use flat sibling imports; expose that directory
before importing their package-wrapped API. The normal Bridge path is unchanged.
"""

import sys
from pathlib import Path

_pipeline_dir = str(Path(__file__).resolve().parent)
if _pipeline_dir not in sys.path:
    sys.path.insert(0, _pipeline_dir)

from .blue_line_detector import (
    BlueLine,
    ScaleStrike,
    count_scale_strikes,
    detect_blue_lines,
    fibonacci_level,
)

__all__ = [
    "BlueLine",
    "ScaleStrike",
    "count_scale_strikes",
    "detect_blue_lines",
    "fibonacci_level",
]
````
<!-- EXACT-SOURCE-END:pipeline/__init__.py -->

### 16.5 `pipeline/a_zone_detector.py` — A

**SHA-256:** `83f08b06556eb59c6d1b3afd22b51c280315bd80f3a31bc3044ada349251a115`  
**Bytes:** `31373`  
**LF count:** `804`

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


A_ZONE_VERSION = "1.7.0"
A_ZONE_LAST_MODIFIED_DATE = "2026-09-30"


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
        self._reaction_first_times = [
            self.candle_times[int(getattr(reaction, "first_idx"))]
            for reaction in self.reactions
        ]
        self._reaction_break_times = [
            self.candle_times[int(getattr(reaction, "break_idx"))]
            for reaction in self.reactions
        ]
        self._reaction_confirmations = [
            self._reaction_confirmation_time(reaction) for reaction in self.reactions
        ]

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
        reactions = self.reactions
        first_times = self._reaction_first_times
        confirmations = self._reaction_confirmations
        for number in range(len(reactions)):
            if (
                confirmations[number] >= trigger_event_time
                and (not_before is None or first_times[number] >= not_before)
            ):
                return number + 1, reactions[number]
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
        reactions = self.reactions
        first_times = self._reaction_first_times
        break_times = self._reaction_break_times
        for number in range(len(reactions)):
            first_time = first_times[number]
            break_time = break_times[number]
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

**SHA-256:** `c6466c280504f82d8f2b189263ed0e9b9581c2f48edd8aaa12f016e55effc98c`  
**Bytes:** `16945`  
**LF count:** `481`

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


BLUE_LINE_VERSION = "2.4.1"
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
    confirmation_time = chronology.reaction_confirmation(direction, reaction)
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
        if second.timestamp > confirmation_time:
            break
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
    # Reaction Break is an exact lower-timeframe event, not the end of the
    # published main OHLC candle. Later prices cannot create scale strikes.
    break_candle = reaction_candles[-1]
    confirmation_time = chronology.reaction_confirmation(direction, reaction)
    break_left, break_right = chronology.lower_bounds(
        break_candle.timestamp, break_candle.timestamp + chronology.timeframe
    )
    available_break_rows = [
        item for item in chronology.seconds[break_left:break_right]
        if item.timestamp <= confirmation_time
    ]
    break_extreme = (
        (min if direction == "bullish" else max)(
            Decimal(getattr(item, "low" if direction == "bullish" else "high"))
            for item in available_break_rows
        ) if available_break_rows else None
    )
    strikes: list[ScaleStrike] = []
    pending: ScaleStrike | None = None

    for candle in reaction_candles:
        last_extreme = strikes[-1].extreme if strikes else level
        candle_extreme = (
            break_extreme if int(getattr(candle, "index")) == break_index
            else Decimal(getattr(candle, "low" if direction == "bullish" else "high"))
        )
        if candle_extreme is None:
            continue  # A missing lower-TF prefix cannot prove a new strike.
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

**SHA-256:** `007e5329e14ab9695e555c630527badc84dd35a239dea1cf685141e4278265eb`  
**Bytes:** `832`  
**LF count:** `26`

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
    return int(reaction.first_idx), int(reaction.break_idx)
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

**SHA-256:** `96ea351ff88c195937da5c32c5712356b9b876ba6f509d68cb16d37012958ad5`  
**Bytes:** `48992`  
**LF count:** `1144`

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


E_ZONE_VERSION = "6.16.2"
E_ZONE_IMPLEMENTATION_VERSION = "6.18.5"
E_ZONE_LAST_MODIFIED = "2026-10-24T17:28:55+03:30"


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
        e_parent_order_first_exceptions: frozenset[tuple[datetime, datetime]] = frozenset(),
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
        self._stop_values = [
            as_decimal(getattr(candle, self.policy.extreme_attr))
            for candle in self.candles
        ]
        self._candle_codes = [int(getattr(candle, "index")) for candle in self.candles]
        self._extreme_sparse = self._build_extreme_sparse()
        self.direct_geometry_finder = direct_geometry_finder
        self.blocked_order_first_times = blocked_order_first_times or set()
        self.e_parent_order_first_exceptions = e_parent_order_first_exceptions
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
        self._post_stop_orders_cache: dict[
            tuple[datetime, int], list[OrderMatch]
        ] = {}
        self._direct_parent_stop_cache: dict[
            tuple[datetime, datetime | None, bool, bool, datetime | None],
            tuple[int, object, datetime] | None,
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
        for cache_name in (
            "_order_candidates_cache",
            "_carried_orders_cache",
            "_post_stop_orders_cache",
            "_direct_parent_stop_cache",
        ):
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

    def _build_extreme_sparse(self) -> list[list[int]]:
        """Sparse table of first extreme candle positions over the main series."""
        values = self._stop_values
        n = len(values)
        if n == 0:
            return []
        less = self.direction == "bullish"
        st: list[list[int]] = [list(range(n))]
        k = 1
        while (1 << k) <= n:
            prev = st[-1]
            span = 1 << (k - 1)
            width = n - (1 << k) + 1
            cur = [0] * width
            for i in range(width):
                left = prev[i]
                right = prev[i + span]
                lv = values[left]
                rv = values[right]
                if (lv < rv) if less else (lv > rv):
                    cur[i] = left
                elif (rv < lv) if less else (rv > lv):
                    cur[i] = right
                else:
                    cur[i] = left if left <= right else right
            st.append(cur)
            k += 1
        return st

    def _extreme_position(self, left: int, right: int) -> int:
        """Return the first extreme candle position in ``[left, right]``."""
        values = self._stop_values
        less = self.direction == "bullish"
        length = right - left + 1
        if length <= 0:
            return left
        k = length.bit_length() - 1
        st = self._extreme_sparse
        i1 = st[k][left]
        i2 = st[k][right - (1 << k) + 1]
        lv = values[i1]
        rv = values[i2]
        if (lv < rv) if less else (lv > rv):
            return i1
        if (rv < lv) if less else (rv > lv):
            return i2
        return i1 if i1 <= i2 else i2


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
        return self.times[int(getattr(reaction, "first_idx"))]


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
        if end_index < start_index:
            end_index = start_index
        position = self._extreme_position(start_index, end_index)
        return (
            self._candle_codes[position],
            self.times[position],
            self._stop_values[position],
        )

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
        inherited_stop_events = [
            item[6][2] for item in inherited if item[6] is not None
        ]
        continuous_deadline = (
            min(inherited_stop_events)
            if parent_type == "S" and not carried and inherited_stop_events
            else self.range_end
            if parent_type == "S" and not carried
            else None
        )
        direct = self.order_candidates(
            stop_event,
            continuous_deadline,
            allow_bounded_continue=(parent_type == "S"),
            allow_trend_leg_continue=(parent_type == "E"),
            e_parent=(parent_type == "E"),
        )
        # E consumption owns one global adjudication across every eligible
        # physical Order route. Route-local reductions must not discard a
        # later First before the canonical exact-stop tie-break can run.
        choices = [
            item
            for route in (direct, inherited, carried, post_stop_accepted)
            for item in route
            if item[6] is not None
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
        decision_time = self.times[decision_index]
        source_index, source_time, price = self._extreme_between(stop_event, decision_event)
        parent_stop_index = self._main_index(stop_event)
        order_first_index = int(getattr(order, "first_idx"))
        top_source = int(getattr(order, "box_top_source_idx"))
        bottom_source = int(getattr(order, "box_bottom_source_idx"))
        order_break_index = int(getattr(order, "break_idx"))
        return EZone(
            direction=self.direction,
            family=family,
            number=number,
            parent_type=parent_type,
            parent_source_index=int(getattr(parent, "source_index")),
            parent_source_time=getattr(parent, "source_time"),
            parent_price=as_decimal(getattr(parent, "price")),
            parent_stop_index=parent_stop_index,
            parent_stop_time=self.times[parent_stop_index],
            parent_stop_event_time=stop_event,
            order_direction=self.order_direction,
            order_reaction_number=order_number,
            order_mode=str(getattr(order, "mode")),
            order_causes=order_causes,
            order_parent_stop_cause_time=order_parent_stop_cause_time,
            order_first_index=order_first_index,
            order_first_time=self.times[order_first_index],
            order_break_index=order_break_index,
            order_break_time=self.times[order_break_index],
            order_confirmation_time=order_confirmation,
            order_box_top=as_decimal(getattr(order, "box_top")),
            order_box_top_source_index=top_source,
            order_box_top_source_time=self.times[top_source],
            order_box_bottom=as_decimal(getattr(order, "box_bottom")),
            order_box_bottom_source_index=bottom_source,
            order_box_bottom_source_time=self.times[bottom_source],
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
        independent_a_order_identities: frozenset[tuple[int, int]] = frozenset(),
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
            # The stopped-A ledger can hold a physical Order before that
            # independent cause reaches this detector's filtered E ledger.
            # An invalid S cannot create its own cause, but it may continue a
            # larger E with an Order already created by a stopped A.
            if (
                self._invalid_s_without_order_cause(zone)
                and (zone.order_first_index, zone.order_break_index)
                not in independent_a_order_identities
            ):
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
            and not self._invalid_s_without_order_cause(item)
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

    def _invalid_s_without_order_cause(self, zone: EZone) -> bool:
        """Reject an invalid S root unless its Order has another creation cause."""
        if zone.parent_type != "S" or (
            zone.parent_source_time, zone.parent_source_index
        ) not in self.invalid_s_root_identities:
            return False
        identity = (zone.order_first_index, zone.order_break_index)
        if identity in self.initial_order_audit:
            return False
        entry = self.order_audit.get(identity)
        if entry is None:
            return True
        if entry.get("order_b_causes"):
            return False
        invalid_s_times = {
            source_time for source_time, _ in self.invalid_s_root_identities
        }
        return not any(
            cause[0] == "parent-stop" and not (
                cause[1] == "S" and cause[4] in invalid_s_times
            )
            for cause in entry.get("causes", ())
        )

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
            return (
                not self._blocked_by_gate_owned_order(zone)
                and not self._invalid_s_without_order_cause(zone)
            )

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
                and not self._invalid_s_without_order_cause(skipped_parent)
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

**SHA-256:** `760928f5480efad446b42bc6aa2fbea3e431de13ab92714bac05c09188519c26`  
**Bytes:** `63174`  
**LF count:** `1529`

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
    accepted_audit_entry, prepare_order_audit,
)
from direction_policy import policy_for


STOP_ALL_VERSION = "1.18.6"
STOP_ALL_IMPLEMENTATION_VERSION = "1.20.7"
STOP_ALL_LAST_MODIFIED = "2026-10-24T12:06:51+03:30"


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


@dataclass(frozen=True, slots=True)
class _DominantBehavior:
    """The only active exact S/E owner and its StopAll occurrence count."""

    kind: str
    family: str
    number: int | None
    count: int
    latest: object

    @property
    def priority(self) -> int:
        return sequence_priority(self.kind, self.family)

    @property
    def armed(self) -> bool:
        return self.count >= 2

    @property
    def key(self) -> str:
        return (
            f"E{self.number} {self.family}"
            if self.kind == "E" else f"S {self.family}"
        )


def advance_dominant_behavior(
    owner: _DominantBehavior | None, kind: str, family: str,
    number: int | None, item: object,
) -> _DominantBehavior:
    """Accept one finalized S/E occurrence using the shared exact-owner rule."""
    incoming = _DominantBehavior(kind, family, number, 1, item)
    if owner is None:
        return incoming
    if (owner.kind, owner.family, owner.number) == (kind, family, number):
        return replace(owner, count=owner.count + 1, latest=item)
    if incoming.priority > owner.priority or (
        incoming.priority == owner.priority
        and kind == owner.kind == "E"
        and StopAllDetector._dominates_e(
            (family, int(number)), (owner.family, int(owner.number))
        )
    ):
        return incoming
    return owner


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
    def _dominates_e(new: tuple[str, int], old: tuple[str, int]) -> bool:
        new_family, new_number = new
        old_family, old_number = old
        if new_family == old_family:
            return new_number > old_number
        # Red is always the dominant E family. A higher-numbered Blue E must
        # not separate or replace an active Red group.
        return new_family == "red" and old_family == "blue"

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
        gate_event: datetime,
    ) -> StopAll:
        """Materialize StopAll from an accepted S Red and eligible Blue owner."""
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
            gate_event_time=gate_event,
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

    def detect(self) -> list[StopAll]:
        s_events = sorted(
            self.s_zones, key=lambda item: (item.source_time, item.source_index)
        )
        s_position = 0
        owner: _DominantBehavior | None = None
        # A completed stop is frozen historical evidence awaiting an existing
        # S-Red Mode-B or E donor. It cannot arm a displaced behavior again.
        pending_stop: tuple[_DominantBehavior, datetime] | None = None
        active: list[StopAll] = []
        output: list[StopAll] = []

        def armed_stop_before(
            boundary: datetime, donor_e: object | None = None,
        ) -> datetime | None:
            if owner is None or not owner.armed:
                return None
            stop = self._strict_stop(
                owner.latest.decision_event_time, as_decimal(owner.latest.price)
            )
            if stop is None:
                return None
            if stop[2] < boundary:
                return stop[2]
            if donor_e is None or stop[2] > donor_e.decision_event_time:
                return None
            # An independently accepted E can donate its physical source when
            # its extreme strictly stops the armed owner *inside that source
            # candle*.  Its earlier source timestamp is only a bucket label;
            # the authoritative lower-timeframe stop must be inside the bucket
            # and no later than E's decision event.  This is independent of
            # the E parent: its parent may predate the dominant owner.
            source_index = int(donor_e.source_index)
            if (
                self.chronology.main_index(stop[2], clamp=True) == source_index
                and donor_e.source_time <= stop[2]
                and stop[2] < donor_e.source_time + self.chronology.timeframe
                and (
                    as_decimal(donor_e.price) < as_decimal(owner.latest.price)
                    if self.direction == "bullish"
                    else as_decimal(donor_e.price) > as_decimal(owner.latest.price)
                )
            ):
                return stop[2]
            # E source geometry is retrospective and may use the main candle
            # containing its own parent's strict stop. Match that physical
            # parent exactly before allowing a stop at/after E source time.
            parent_index = getattr(donor_e, "parent_source_index", None)
            parent_price = getattr(donor_e, "parent_price", None)
            if (
                str(getattr(donor_e, "parent_type", "")).upper() == owner.kind
                and parent_index is not None
                and int(parent_index) == int(owner.latest.source_index)
                and getattr(donor_e, "parent_source_time", None)
                == owner.latest.source_time
                and parent_price is not None
                and as_decimal(parent_price) == as_decimal(owner.latest.price)
                and getattr(donor_e, "parent_stop_event_time", None) == stop[2]
            ):
                return stop[2]
            return None

        def accept(kind: str, family: str, number: int | None, item: object) -> None:
            nonlocal owner
            owner = advance_dominant_behavior(owner, kind, family, number, item)

        def process_s_event(s_item: object) -> None:
            nonlocal owner, pending_stop, active
            color = str(s_item.color).lower()
            # An armed exact Blue owner reverses directly on the first
            # accepted S Red. Neither a prior price stop nor Order Mode B
            # is required; S decision chronology, not retrospective source,
            # determines whether the second Blue had already confirmed.
            if (
                color == "red"
                and owner is not None
                and owner.family == "blue"
                and owner.armed
                and owner.latest.decision_event_time < s_item.decision_event_time
            ):
                zone = self._stopall_from_s(
                    s_item, owner.kind, owner.key, owner.count,
                    (owner.family, int(owner.number))
                    if owner.kind == "E" else None,
                    s_item.decision_event_time,
                )
                output.append(zone)
                active = [zone]
                owner = None
                pending_stop = None
                return

            gate_event = armed_stop_before(s_item.source_time)
            completed = pending_stop or (
                (owner, gate_event) if owner is not None and gate_event is not None
                else None
            )
            if (
                color == "red" and completed is not None
                and completed[0].family == "blue"
                and str(getattr(s_item, "order_mode", "")).upper() == "B"
            ):
                stopped_owner, stopped_at = completed
                zone = self._stopall_from_s(
                    s_item, stopped_owner.kind, stopped_owner.key,
                    stopped_owner.count,
                    (stopped_owner.family, int(stopped_owner.number))
                    if stopped_owner.kind == "E" else None,
                    stopped_at,
                )
                output.append(zone)
                active = [zone]
                owner = None
                pending_stop = None
                return
            if pending_stop is None and completed is not None:
                pending_stop = completed
            accept("S", color, None, s_item)

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
                owner = None
                pending_stop = None
                continue

            gate_event = armed_stop_before(e_item.source_time, e_item)
            completed = pending_stop or (
                (owner, gate_event) if owner is not None and gate_event is not None
                else None
            )
            if completed is not None:
                stopped_owner, stopped_at = completed
                zone = self._stopall_from_e(
                    e_item, 1, "sequence-group-stop", stopped_at,
                    stopped_owner.kind, stopped_owner.key, stopped_owner.count,
                )
                output.append(zone)
                active.append(zone)
                owner = None
                pending_stop = None
                continue

            accept("E", str(e_item.family).lower(), int(e_item.number), e_item)

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
    *,
    accepted_e_stop_events: set[datetime] | None = None,
    opposite_confirmation_finder=None,
    e_parent_order_first_exceptions_out: set[tuple[datetime, datetime]] | None = None,
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

    # This is NOT a global unblock.  Preserve the invalid-A and inherited-S
    # First vetoes for every A/S order route.  Only the accepted E parent whose
    # exact strict stop also ends that invalid A may use a canonical opposite
    # Reaction started in the stop-owning main candle and confirmed afterward.
    # The exception is keyed by both exact E stop event and physical First.
    exceptions: set[tuple[datetime, datetime]] = set()
    if accepted_e_stop_events and opposite_confirmation_finder is not None:
        candle_times = [getattr(item, "timestamp") for item in candles]
        reactions_by_first_index: dict[int, list[object]] = {}
        for reaction in opposite_reactions:
            reactions_by_first_index.setdefault(
                int(getattr(reaction, "first_idx")), []
            ).append(reaction)
        for invalid_a in invalid_a_zones:
            if getattr(invalid_a, "source_time") not in pending_s_a_sources:
                continue
            stop = stop_finder(invalid_a)
            if stop is None or stop[2] not in accepted_e_stop_events:
                continue
            exact_stop = stop[2]
            stop_candle = bisect_right(candle_times, exact_stop) - 1
            if stop_candle < 0:
                continue
            for reaction in reactions_by_first_index.get(stop_candle, ()):
                first_time = candle_times[stop_candle]
                if (first_time in blocked_order_first_times
                        and first_time not in inherited_blocked_first_times
                        and getattr(invalid_a, "source_time") <= first_time < exact_stop
                        and opposite_confirmation_finder(reaction) > exact_stop):
                    exceptions.add((exact_stop, first_time))
    if e_parent_order_first_exceptions_out is not None:
        e_parent_order_first_exceptions_out.update(exceptions)
    return accepted_orders, blocked_order_first_times


def visible_a_zones_after_s_stops(a_zones, s_zones, candles):
    """Suppress the A candle that contains an already-confirmed S stop.

    That candle is the S-stop/E transition candle. It may still carry the
    order box's BoxBottom, but it cannot receive a new A label.
    """
    times = [getattr(item, "timestamp") for item in candles]
    stop_indices = {
        bisect_right(times, getattr(item, "decision_event_time")) - 1
        for item in s_zones
    }
    stop_indices.discard(-1)
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
    # Immutable per invocation. Building this inside the S loop made the
    # visibility pass O(S*C) allocations on large RAW histories.
    candle_times = (
        [getattr(candle, "timestamp") for candle in candles]
        if candles is not None else None
    )
    stop_event_cache: dict[int, datetime | None] = {}

    def cached_stop_event(module: object) -> datetime | None:
        key = id(module)
        if key not in stop_event_cache:
            stop_event_cache[key] = module_stop_event(module, stop_event_finder)
        return stop_event_cache[key]

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
                    module_stop := cached_stop_event(module)
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
                if candle_times is not None and stopped_external:
                    latest_external = max(
                        stopped_external,
                        key=lambda item: (
                            getattr(item, "source_time"),
                            int(getattr(item, "source_index", -1)),
                        ),
                    )
                    if module_priority(s_zone) < module_priority(latest_external):
                        larger_stop = cached_stop_event(latest_external)
                        if larger_stop is not None:
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
                        cached_stop_event(item),
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
                    module_stop = cached_stop_event(module)
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

**SHA-256:** `f4e991a6a516ad84e0223c802f5baf611f5e20fb8d7965b9dcdf4ff949d89296`  
**Bytes:** `89666`  
**LF count:** `2175`

<!-- EXACT-SOURCE-BEGIN:pipeline/order_audit_engine.py -->
````python
"""Central physical Order discovery, reuse, provenance, and audit ownership."""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from typing import Callable, Sequence

from core_utils import as_decimal, order_identity, reaction_identity

ORDER_AUDIT_ENGINE_VERSION = "1.7.1"
ORDER_AUDIT_ENGINE_LAST_MODIFIED = "2026-10-24T23:30:27+03:30"


def relabel_primary_causes(causes, labels):
    """Resolve PH aliases by physical source without changing Order provenance."""
    result = []
    for cause in causes:
        row = deepcopy(cause)
        for name, source in (("parentType", "parentSourceTime"),
                             ("postBehaviorType", "postBehaviorSourceTime"),
                             ("anchorBehaviorType", "anchorBehaviorSourceTime")):
            if str(row.get(name, "")).startswith("PH") and row.get(source) in labels:
                row[name] = labels[row[source]]
        if row not in result:
            result.append(row)
    return result

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
    candle and the reset Reaction must start strictly after that boundary
    source.  Order_B selection is owned by the calculation timeframe: the
    first main candle containing a strict post-Reset boundary crossing opens
    the opposite-Reaction gate, and a canonical opposite Reaction whose First
    is that same main candle is eligible.  Lower-timeframe chronology is kept
    only to prove that the crossing occurs after the exact Reset and, when
    needed, that confirmation occurs strictly after the crossing.
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
        strict_break_index = chronology.main_index(strict_break_time, clamp=True)

        # Order_B is a calculation-timeframe rule.  The exact lower-TF crossing
        # proves the break happened after Reset and remains audit provenance,
        # but it must not disqualify a canonical opposite Reaction whose First
        # belongs to the same calculation candle as that strict break.
        #
        # A newly formed accepted A is likewise compared by its owning main
        # candle.  This keeps lifecycle expiry on the configured calculation
        # timeframe while preserving lower-TF chronology only where exact
        # within-candle ordering is genuinely required.
        next_a_position = bisect_right(a_times, current_first_time)
        if (
            next_a_position < len(a_times)
            and chronology.main_index(a_times[next_a_position], clamp=True)
            <= strict_break_index
        ):
            continue

        physical = next((
            item for item in opposite_direction
            if strict_break_index <= item[1]
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
        e_parent: bool = False,
        *, confirmation_after: datetime | None = None,
    ) -> tuple[int, object, datetime] | None:
        """Select the direct parent-stop Order_A."""
        cache_key = (start, continuous_deadline, allow_bounded_continue, e_parent, confirmation_after)
        cached = self._direct_parent_stop_cache.get(cache_key)
        if cached is not None or cache_key in self._direct_parent_stop_cache:
            return cached
        result = self._compute_direct_parent_stop_order(
            start, continuous_deadline, allow_bounded_continue, e_parent,
            confirmation_after=confirmation_after,
        )
        self._direct_parent_stop_cache[cache_key] = result
        return result

    def _compute_direct_parent_stop_order(
        self,
        start: datetime,
        continuous_deadline: datetime | None,
        allow_bounded_continue: bool,
        e_parent: bool = False,
        *, confirmation_after: datetime | None = None,
    ) -> tuple[int, object, datetime] | None:
        gate_time = self.times[self._main_index(start)]
        geometric_direct = self._first_healthy_direct_geometry(
            start, allow_bounded_continue
        )
        if (geometric_direct is not None and confirmation_after is not None
                and geometric_direct[2] <= confirmation_after):
            geometric_direct = None
        direct_position = bisect_left(self._opposite_first_times, gate_time)
        if confirmation_after is not None:
            while (direct_position < len(self.opposite_reactions)
                   and self._opposite_confirmations[direct_position] <= confirmation_after):
                direct_position += 1
        while (
            direct_position < len(self.opposite_reactions)
            and self._opposite_first_times[direct_position]
            in self.blocked_order_first_times
            and self._opposite_first_times[direct_position] == gate_time
        ):
            # The invalid-A First veto remains in force except for a native
            # Order_A consumed by this accepted E stop. Exact A/E simultaneous
            # stop and strict post-stop confirmation are required; inherited
            # unrelated blocks cannot be bypassed by a later E stop.
            if (
                e_parent
                and (start, gate_time) in self.e_parent_order_first_exceptions
                and self._opposite_confirmations[direct_position] > start
            ):
                break
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
        e_parent: bool = False,
    ) -> list[OrderMatch]:
        """Return physical Order candidates formed before this E decision."""
        cache_key = (
            start,
            continuous_deadline,
            allow_bounded_continue,
            allow_trend_leg_continue,
            e_parent,
        )
        cached = self._order_candidates_cache.get(cache_key)
        if cached is not None:
            return list(cached)

        by_geometry: dict[tuple[int, int], OrderMatch] = {}
        direct = self._direct_parent_stop_order(
            start, continuous_deadline, allow_bounded_continue, e_parent
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
        self._invalidate_post_stop_order_cache()

    def _invalidate_carried_order_caches(self) -> None:
        # Carried results depend on creation causes, so they must drop when a
        # cause is added. Post-stop results depend only on the confirmation
        # index length (included in its cache key), so cause-only mutations
        # must not wipe that cache.
        self._carried_orders_cache.clear()

    def _invalidate_post_stop_order_cache(self) -> None:
        self._post_stop_orders_cache.clear()


    def register_order_b_reset_legs(
        self, legs: Sequence[OrderBResetLeg],
    ) -> None:
        """Merge proven reset-leg causes by canonical physical identity."""
        if legs:
            self._invalidate_carried_order_caches()
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
                self._invalidate_carried_order_caches()


    def _reparent_primary_high_causes(self, parent, stop_event, direct_identity):
        """Replace only StopAll roles owned by an already confirmed PH."""
        label = f"PH{parent.number}"
        source = (int(parent.source_index), parent.source_time)
        changed = False
        revoked = set()
        for identity, entry in self.order_audit.items():
            previous = entry.get("causes", set())
            current = set()
            for cause in previous:
                replaced = (cause[0] == "parent-stop" and str(cause[1]).startswith("StopAll")
                    and cause[4] == parent.source_time and stop_event is not None
                    and cause[3] == stop_event and cause[3] > parent.decision_event_time)
                if not replaced:
                    current.add(cause)
                elif identity == direct_identity:
                    current.add((cause[0], label, "", cause[3], cause[4]))
            if current != previous:
                entry["causes"] = current
                changed = True
            for cause in entry.get("order_b_causes", ()):
                if (str(cause.get("postBehaviorType", "")).startswith("StopAll")
                        and (cause.get("postBehaviorSourceIndex"), cause.get("postBehaviorSourceTime")) == source
                        and stop_event is not None
                        and cause.get("postBehaviorStopTime") == stop_event
                        and stop_event > parent.decision_event_time):
                    cause["postBehaviorType"] = label
                    changed = True
                reset_identity = cause.get("resetReactionIdentity")
                if (str(cause.get("anchorBehaviorType", "")).startswith("StopAll")
                        and (cause.get("anchorBehaviorSourceIndex"), cause.get("anchorBehaviorSourceTime")) == source
                        and reset_identity
                        and self.times[int(reset_identity[0])] >= parent.decision_event_time):
                    cause["anchorBehaviorType"] = label
                    changed = True
            if not current and not entry.get("order_b_causes"):
                revoked.add(identity)
        for identity in revoked:
            del self.order_audit[identity]
        if revoked:
            self._order_audit_confirmation_index[:] = [
                item for item in self._order_audit_confirmation_index
                if (item[1], item[2]) not in revoked
            ]
            self._invalidate_post_stop_order_cache()
        if changed or revoked:
            self._invalidate_carried_order_caches()

    def register_primary_high(self, parent):
        """Create the native bearish-owner Order_A after a confirmed PH stop.

        PH replaces the final StopAll owner without deleting the historical
        sequence boundaries that were needed before PH confirmation.
        """
        if self.direction != "bearish" or getattr(parent, "kind", None) != "PH":
            raise ValueError("Primary-High Order_A is specified for the bearish owner only.")
        left = bisect_right(self.lower_times, parent.decision_event_time)
        right = bisect_left(self.lower_times, self.range_end)
        position = self._first_cross_position(left, right, as_decimal(parent.price), less=False)
        stop_event = self.lower_times[position] if position is not None else None
        direct = self._direct_parent_stop_order(
            stop_event, None, False, confirmation_after=stop_event,
        ) if stop_event is not None else None
        self._reparent_primary_high_causes(
            parent, stop_event, reaction_identity(direct[1]) if direct is not None else None,
        )
        if direct is None:
            return None
        number, reaction, confirmation = direct
        identity = reaction_identity(reaction)
        entry = self.order_audit.get(identity)
        if entry is None:
            level, source, source_time = self._order_stop(number, reaction)
            entry = {
                "reaction_number": number, "reaction": reaction,
                "confirmation_time": confirmation, "stop_level": level,
                "stop_source_index": source, "stop_source_time": source_time,
                "stop_cross": self._cross_order(confirmation, level), "causes": set(),
            }
            self.order_audit[identity] = entry
            self._index_order_audit_identity(identity, confirmation)
        cause = ("parent-stop", f"PH{parent.number}", "", stop_event, parent.source_time)
        if cause not in entry["causes"]:
            entry["causes"].add(cause)
            self._invalidate_carried_order_caches()
        return identity

    def reconcile_primary_high_labels(self, highs):
        """Publish one final PH name without rediscovering or moving Orders."""
        labels = {point.source_time: f"PH{point.number}" for point in highs}
        changed = False
        for entry in self.order_audit.values():
            previous = entry.get("causes", set())
            current = {(kind, labels.get(source, label) if str(label).startswith("PH") else label,
                        family, event, source)
                       for kind, label, family, event, source in previous}
            if current != previous:
                entry["causes"] = current
                changed = True
            previous_b = entry.get("order_b_causes", [])
            current_b = relabel_primary_causes(previous_b, labels)
            if current_b != previous_b:
                entry["order_b_causes"] = current_b
                changed = True
        if changed:
            self._invalidate_carried_order_caches()

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
            e_parent=(parent_type == "E"),
        )
        direct = self._direct_parent_stop_order(
            parent_stop, None, allow_bounded_continue=(parent_type == "S"),
            e_parent=(parent_type == "E"),
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

        changed = False
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
                changed = True
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
            cause = (
                "parent-stop", parent_label, family, parent_stop,
                getattr(parent, "source_time"),
            )
            if cause not in audit_causes:
                audit_causes.add(cause)
                changed = True
        if changed:
            self._invalidate_carried_order_caches()


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
        # Safe cache key: confirmation-index length changes whenever a new
        # accepted Order enters the live ledger. Cause-only mutations do not
        # change the post-stop result set.
        cache_key = (parent_stop, len(self._order_audit_confirmation_index))
        cached = self._post_stop_orders_cache.get(cache_key)
        if cached is not None:
            return list(cached)
        matches_by_identity: dict[tuple[int, int], OrderMatch] = {}

        def add_match(match: OrderMatch) -> None:
            crossed = match[6]
            if crossed is None:
                return
            crossed_time = crossed[2]
            if crossed_time <= parent_stop or crossed_time <= match[2]:
                return
            if self._has_sequence_reset_between(parent_stop, crossed_time):
                return
            reaction = match[1]
            identity = (int(getattr(reaction, "first_idx")), int(getattr(reaction, "break_idx")))
            current = matches_by_identity.get(identity)
            if current is None or (
                crossed_time, match[2], int(getattr(reaction, "first_idx"))
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

        result = sorted(
            matches_by_identity.values(),
            key=lambda item: (
                item[6][2], item[2], -int(getattr(item[1], "first_idx")),
            ),
        )
        self._post_stop_orders_cache[cache_key] = result
        return list(result)


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
            self._index_order_audit_identity(
                identity, zone.order_confirmation_time
            )

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
            if identity in self.order_audit:
                continue
            self.order_audit[identity] = entry
            # The rebuild clears both ledger and index. Restoring only the
            # ledger makes the physical Order invisible to chronological
            # post-stop queries and downstream E/Order_B consumers.
            self._index_order_audit_identity(identity, entry["confirmation_time"])
        self._invalidate_carried_order_caches()
        return rebuilt


def _parent_stop_cause_key(cause: dict[str, object]) -> tuple[object, object, object, object]:
    return (
        cause.get("parentType"),
        cause.get("parentFamily"),
        cause.get("eventTime"),
        cause.get("parentSourceTime"),
    )


def _collect_s_ledger_entries(
    s_detector,
    accepted_a_sources: set[datetime] | None,
) -> list[tuple[dict[str, object], list[dict[str, object]]]]:
    """Collect A-owned Order_A entries with accepted creation causes."""
    combined: list[tuple[dict[str, object], list[dict[str, object]]]] = []
    if s_detector is None:
        return combined
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
    return combined


def _collect_e_ledger_entries(
    detector,
    accepted_a_sources: set[datetime] | None = None,
) -> list[tuple[dict[str, object], list[dict[str, object]]]]:
    """Collect E-stage Order entries using only accepted A parent-stop causes."""
    combined: list[tuple[dict[str, object], list[dict[str, object]]]] = []
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
            and not (
                cause[1] == "A"
                and accepted_a_sources is not None
                and cause[4] not in accepted_a_sources
            )
        ]
        causes.extend(entry.get("order_b_causes", ()))
        if causes:
            combined.append((entry, causes))
    return combined


def _merge_prepared_identities(
    combined: list[tuple[dict[str, object], list[dict[str, object]]]],
    detector,
    start_index: int,
    end_index: int,
    required_identities: set[tuple[int, int]],
) -> list[dict[str, object]]:
    """Merge ledger rows by physical identity inside the presentation window."""
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
    return output


def _single_owner_parent_stop_causes(
    output: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Keep one physical Order_A owner per exact parent-stop cause key."""
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
            key = _parent_stop_cause_key(cause)
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
            key = _parent_stop_cause_key(cause)
            if parent_owner.get(key) is item:
                accepted_causes.append(cause)
        if accepted_causes:
            item["causes"] = accepted_causes
            deduped_output.append(item)
    return deduped_output


def prepare_order_audit(
    detector,
    start_index: int,
    end_index: int,
    s_detector=None,
    accepted_a_sources: set[datetime] | None = None,
    required_identities: set[tuple[int, int]] | None = None,
):
    """Resolve final Order_A and Order_B identities before serialization."""
    required_identities = set(required_identities or set())
    combined = [
        *_collect_s_ledger_entries(s_detector, accepted_a_sources),
        *_collect_e_ledger_entries(detector, accepted_a_sources),
    ]
    output = _merge_prepared_identities(
        combined, detector, start_index, end_index, required_identities
    )
    return _single_owner_parent_stop_causes(output)


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
    accepted_causes = [
        (source_time, stop_time)
        for source_time, stop_time in causes
        if source_time in accepted_sources
    ]
    if not accepted_causes:
        return None
    selected = accepted_causes[0]
    if (
        selected[0] == entry.get("a_source_time")
        and selected[1] == entry.get("a_stop_event_time")
        and accepted_causes == list(causes)
    ):
        return entry
    adjusted = dict(entry)
    adjusted["a_source_time"] = selected[0]
    adjusted["a_stop_event_time"] = selected[1]
    adjusted["a_causes"] = accepted_causes
    return adjusted


def accepted_audit_entries(
    order_audit: dict[tuple[int, int], dict[str, object]],
    accepted_sources: set[datetime],
) -> dict[tuple[int, int], dict[str, object]]:
    """Return Order_A entries whose creating A remains calculation-accepted."""
    return {
        identity: accepted
        for identity, entry in order_audit.items()
        for accepted in [accepted_audit_entry(entry, accepted_sources)]
        if accepted is not None
    }


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
        """Resolve the first physical Order_A independently after each A stop.

        Opposite Order geometry must not inherit the normal same-direction
        Reaction stream's previous-First ownership.  A valid post-stop First
        can be nested inside an earlier, still-open opposite Reaction.  Keep
        the canonical identity/number when the geometry is already present;
        otherwise use reaction number zero (no invented public Reaction).
        The same immutable chosen physical identity is shared by S and E audit.
        """
        canonical = self._order_matches_after(a_stop_event_time)
        native = canonical[0] if canonical else None
        if self.initial_order_geometry is None:
            return native

        gate_index = self._main_index(a_stop_event_time)
        physical = self.initial_order_geometry(
            gate_index, a_stop_event_time, self.end_index
        )
        if physical is None or getattr(physical, "break_idx", None) is None:
            return native
        first_index = int(getattr(physical, "first_idx"))
        if first_index < gate_index:
            return native
        confirmation = self._reaction_confirmation_time(
            physical, self.order_direction
        )
        if confirmation <= a_stop_event_time:
            return native

        identity = reaction_identity(physical)
        mapped = self._opposite_by_first_index.get(first_index)
        if mapped is not None and reaction_identity(mapped[1]) == identity:
            number, physical = mapped
            confirmation = self._reaction_confirmation_time(
                physical, self.order_direction
            )
        else:
            # Order-only physical geometry is not a new canonical Reaction.
            number = 0
        independent = (number, physical, confirmation)
        if native is None:
            return independent
        # A stopped parent owns its first post-stop First, not whichever
        # unrelated continuous-stream Reaction happens to be published.
        if (
            first_index, confirmation
        ) < (
            int(getattr(native[1], "first_idx")), native[2]
        ):
            return independent
        return native


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

### 16.12 `pipeline/PL_PH_detector.py` — Primary High / Low / Matching Behavior Leg

**SHA-256:** `4c03c016762c55006cba98b9dd565a5e0d37c9420c6e0cacdd1a060d4e8bd989`  
**Bytes:** `22048`  
**LF count:** `490`

<!-- EXACT-SOURCE-BEGIN:pipeline/PL_PH_detector.py -->
````python
"""Bearish Primary-High/Low state and the immutable matching behavior leg.

Only the bearish algorithm has been specified. Native Reaction, Reset,
dominance, physical Order identity and stop geometry remain owned by their
existing engines. No bullish primary calculation is inferred here.
"""
from __future__ import annotations

from bisect import bisect_right
from copy import deepcopy
from dataclasses import dataclass, field, replace
from datetime import datetime
from decimal import Decimal
from typing import Callable, Sequence

from core_utils import as_decimal
from lifecycle_engine import advance_dominant_behavior
from order_audit_engine import relabel_primary_causes

PL_PH_VERSION = "1.2.2"
PL_PH_LAST_MODIFIED = "2026-10-26T19:31:03+03:30"


@dataclass(frozen=True, slots=True)
class StructureOrder:
    direction: str
    reaction_number: int
    first_index: int
    break_index: int
    confirmation_event_time: datetime
    stop_level: Decimal
    stop_source_index: int
    stop_index: int
    stop_event_time: datetime
    causes: tuple[str, ...]
    box_top: Decimal | None = None
    box_bottom: Decimal | None = None
    reaction_mode: str | None = None
    audit_causes: tuple[dict[str, object], ...] = ()


@dataclass(frozen=True, slots=True)
class PrimaryPoint:
    kind: str
    number: int
    source_index: int
    source_time: datetime
    price: Decimal
    trigger_index: int
    trigger_event_time: datetime
    decision_index: int
    decision_event_time: datetime
    order: StructureOrder
    cycle_id: str | None = field(default=None, kw_only=True)
    identity_source: PrimaryPoint | None = field(default=None, kw_only=True)


@dataclass(frozen=True, slots=True)
class MatchingBehaviorLeg:
    source_index: int
    source_time: datetime
    price: Decimal
    reference_stopall_index: int
    second_behavior_index: int
    trigger_index: int
    trigger_event_time: datetime
    stop_index: int | None
    stop_event_time: datetime | None


@dataclass(slots=True)
class PrimaryResult:
    highs: list[PrimaryPoint] = field(default_factory=list)
    lows: list[PrimaryPoint] = field(default_factory=list)
    mbl: MatchingBehaviorLeg | None = None
    status: str = "waiting-for-matching-behaviors"
    post_pl3_orders: list[StructureOrder] = field(default_factory=list)
    cycle_id: str | None = None
    cycles: list[PrimaryResult] = field(default_factory=list)
    qualification_event_time: datetime | None = None


def resolve_primary_highs(primary, *, through_index):
    """Resolve physical PH ownership after independent logical confirmation.

    Each candle has one final number. The greatest coincident local number
    wins; a strictly higher subsequent high continues the preceding final
    number. Logical cycle/reset states and their Order eligibility stay intact.
    Filter confirmations before reconciliation so future roles cannot rename
    an earlier requested horizon.
    """
    physical = {}
    cycle_order = {cycle.cycle_id: index for index, cycle in
                   enumerate(getattr(primary, "cycles", ()))}
    for point in primary.highs:
        if point.decision_index <= through_index:
            physical.setdefault((point.source_index, point.source_time), []).append(point)
    groups = sorted(physical.values(), key=lambda rows: (
        min(point.decision_event_time for point in rows), rows[0].source_time,
        rows[0].source_index,
    ))
    result = []
    for rows in groups:
        def role_order(point):
            return (point.decision_event_time,
            cycle_order.get(point.cycle_id, len(cycle_order)), point.cycle_id or "",
            point.trigger_index, point.number)
        identity = min(rows, key=role_order)
        winner = min(rows, key=lambda point: (-point.number, *role_order(point)))
        number = winner.number
        if result and winner.price > result[-1].price:
            number = max(number, result[-1].number + 1)
        result.append(replace(winner, number=number,
                              identity_source=identity.identity_source or identity))
    return result


def relabel_primary_order(order, highs):
    """Keep frozen structure Order snapshots aligned with final PH names."""
    labels = {point.source_time: f"PH{point.number}" for point in highs}
    return replace(order, audit_causes=tuple(relabel_primary_causes(order.audit_causes, labels)))


def formed_matching_legs(primary, *, through_index):
    """A qualified candidate becomes MBL only after its first confirmed PH.

    Keep the frozen candidate internally for cancellation/Order chronology;
    neither activation alone nor a future PH confirms a leg at this horizon.
    """
    for cycle in getattr(primary, "cycles", None) or [primary]:
        if cycle.mbl is None or cycle.mbl.trigger_index > through_index:
            continue
        confirmation = min((point for point in cycle.highs
                            if point.decision_index <= through_index),
                           key=lambda point: point.decision_event_time, default=None)
        if confirmation is not None:
            yield cycle, confirmation


def resolve_stopall_ownership(stopalls, primary: PrimaryResult, *, through_index: int):
    """A confirmed PH owns its candle; retain the causal StopAll history.

    A future PH confirmation must not remove the StopAll from an earlier
    requested horizon. The supplied historical collection is never mutated.
    """
    promoted = {(point.source_index, point.source_time) for point in primary.highs
                if point.decision_index <= through_index}
    return [item for item in stopalls
            if (int(item.source_index), item.source_time) not in promoted]


def order_meets_structure_gate(kind, first_index, confirmation, gate_index, event):
    """PH eligibility follows Order confirmation, including a joint RAW event.

    An accepted PH Order can begin before the structure crossing. PL retains
    its separately specified First-candle and strict confirmation gates.
    """
    if kind == "PH":
        return confirmation >= event
    return first_index >= gate_index and confirmation > event


def strict_cross(chronology, event: datetime, level: Decimal, above: bool):
    """Find the first strictly later selected-RAW crossing, preserving equality."""
    left = bisect_right(chronology.second_times, event)
    index = chronology.lower_index
    position = (index.first_greater if above else index.first_less)(
        left, len(chronology.seconds), level
    )
    if position is None:
        return None
    instant = chronology.second_times[position]
    return chronology.main_index(instant, clamp=True), instant


def _extreme(chronology, left: int, right: int, high: bool):
    attribute = "high" if high else "low"
    # Python min/max retain the first index on equality, as specified.
    chooser = max if high else min
    source = chooser(range(left, right + 1),
                     key=lambda i: as_decimal(getattr(chronology.candles[i], attribute)))
    return source, as_decimal(getattr(chronology.candles[source], attribute))


def _matching_seeds(s_zones, e_zones, stopalls):
    """Keep qualified legs pending until their first actual strict breakout."""
    occupied = {int(item.source_index) for item in stopalls}
    events = [(item.source_time, 0, "StopAll", item) for item in stopalls]
    events.extend((item.source_time, rank, kind, item)
                  for kind, rank, items in (("S", 1, s_zones), ("E", 2, e_zones))
                  for item in items
                  if int(item.source_index) not in occupied
                  and getattr(item, "calculation_valid", True) is not False)
    owner = reference = None
    qualified = False
    seen_events = set()
    confirmations: list[datetime] = []
    for _, _, kind, item in sorted(events, key=lambda row: (row[0], row[1], row[3].source_index)):
        identity = (kind, int(item.source_index), item.source_time)
        if identity in seen_events:
            continue
        seen_events.add(identity)
        if kind == "StopAll":
            reference = item if int(item.number) >= 3 else None
            owner, confirmations = None, []
            qualified = False
            continue
        if reference is None or qualified:
            continue
        family = str(item.color if kind == "S" else item.family).lower()
        number = None if kind == "S" else int(item.number)
        previous = owner
        owner = advance_dominant_behavior(owner, kind, family, number, item)
        if owner is previous:
            continue
        if previous is None or owner.count == 1:
            confirmations = []
        confirmations.append(item.decision_event_time)
        if owner.armed:
            qualified = True
            yield reference, item, max(reference.decision_event_time, *confirmations)


def detect_bearish(
    chronology, s_zones: Sequence[object], e_zones: Sequence[object],
    stopalls: Sequence[object],
    orders: Callable[[str, int, int, datetime], Sequence[StructureOrder]],
) -> PrimaryResult:
    """Merge independent cycles on exact chronology and one native Order ledger.

    A proposal never commits PH ownership. Only the globally earliest decision
    may mutate the native ledger; that mutation invalidates every pending
    proposal, including cycles waiting without an accepted Order.
    """
    result = PrimaryResult()
    activated = []
    qualified = False
    seen = set()
    for reference, second, qualification in _matching_seeds(s_zones, e_zones, stopalls):
        qualified = True
        if result.qualification_event_time is None or qualification < result.qualification_event_time:
            result.qualification_event_time = qualification
        identity = (int(reference.source_index), int(second.source_index))
        if identity in seen:
            continue
        seen.add(identity)
        level = as_decimal(chronology.candles[int(reference.source_index)].high)
        crossed = strict_cross(chronology, qualification, level, True)
        if crossed is not None:
            activated.append((crossed, reference, second, qualification))
    if not activated:
        if qualified:
            result.status = "waiting-for-stopall-break"
        return result
    activated.sort(key=lambda row: (
        row[0][1], row[3], row[1].source_index, row[2].source_index,
    ))
    checkpoints = []
    pending = {}
    promoted_sources = set()
    activation_index = 0
    while True:
        for index, checkpoint in enumerate(checkpoints):
            if index not in pending:
                pending[index] = _next_point(chronology, checkpoint, orders)
        decisions = [(point.decision_event_time, index)
                     for index, (_, point) in pending.items() if point is not None]
        decision = min(decisions, default=None)
        if activation_index < len(activated) and (
            decision is None or activated[activation_index][0][1] <= decision[0]
        ):
            # Activate all contexts at an instant before committing its points;
            # ties between points retain deterministic activation order.
            activation = activated[activation_index]
            activation_index += 1
            reference = activation[1]
            if (int(reference.source_index), reference.source_time) in promoted_sources:
                # The historical StopAll is already a confirmed PH. Its stop
                # belongs to PH continuation, not an independent matching leg.
                continue
            checkpoints.append(_activate_cycle(chronology, activation))
            continue
        if decision is None:
            break
        _, index = decision
        checkpoint, point = pending.pop(index)
        checkpoints[index] = checkpoint
        target = checkpoint.result.highs if point.kind == "PH" else checkpoint.result.lows
        target.append(point)
        (result.highs if point.kind == "PH" else result.lows).append(point)
        if point.kind == "PH":
            promoted_sources.add((point.source_index, point.source_time))
            commit_high = getattr(orders, "confirm_high", None)
            if commit_high is not None:
                commit_high(point)
                pending.clear()

    result.cycles = [pending[index][0].result for index in range(len(checkpoints))]
    result.mbl = result.cycles[0].mbl
    result.status = result.cycles[-1].status
    physical_orders = {}
    for cycle in result.cycles:
        for order in cycle.post_pl3_orders:
            physical_orders.setdefault((order.direction, order.first_index, order.break_index), order)
    result.post_pl3_orders = sorted(physical_orders.values(), key=lambda item: (
        item.stop_event_time, -item.first_index, item.break_index,
    ))
    return result


@dataclass(slots=True)
class _CycleCheckpoint:
    result: PrimaryResult
    reference_price: Decimal
    gate_index: int
    cursor: datetime
    phase: str = "PH"
    reset_high: bool = False


def _activate_cycle(chronology, activation):
    crossed, reference, second, qualification = activation
    result = PrimaryResult(
        cycle_id=f"bearish:cycle:{reference.source_index}:{second.source_index}",
        qualification_event_time=qualification,
    )
    reference_price = as_decimal(chronology.candles[int(reference.source_index)].high)
    gate_index, cursor = crossed
    source, floor = _extreme(chronology, int(second.source_index), gate_index, False)
    broken = strict_cross(chronology, cursor, floor, False)
    result.mbl = MatchingBehaviorLeg(
        source, chronology.times[source], floor, int(reference.source_index),
        int(second.source_index), gate_index, cursor,
        broken[0] if broken else None, broken[1] if broken else None,
    )
    return _CycleCheckpoint(result, reference_price, gate_index, cursor)


def _next_point(chronology, checkpoint, orders):
    """Prospect from committed state without changing shared native ownership.

    Cancel/seek transitions are replayable: a later global PH commitment may
    admit an Order before a previously projected future cancellation.
    """
    result = replace(checkpoint.result, highs=list(checkpoint.result.highs),
                     lows=list(checkpoint.result.lows),
                     post_pl3_orders=list(checkpoint.result.post_pl3_orders))
    phase, reset_high = checkpoint.phase, checkpoint.reset_high
    gate_index, cursor = checkpoint.gate_index, checkpoint.cursor
    reference_price, floor = checkpoint.reference_price, result.mbl.price
    prospective = replace(checkpoint, result=result)
    # Every iteration consumes a strictly later RAW event. No arbitrary
    # maximum PH/PL number or feedback-pass cap is part of this algorithm.
    while True:
        high_level = result.highs[-1].price if result.highs else reference_price
        low_level = result.lows[-1].price if result.lows else floor
        high_number = 1 if reset_high or not result.highs else result.highs[-1].number + 1
        low_number = result.lows[-1].number + 1 if result.lows else 1
        if phase == "seek":
            up = strict_cross(chronology, cursor, high_level, True)
            down = strict_cross(chronology, cursor, low_level, False)
            if up is None and down is None:
                result.status = "waiting-for-structure-break"
                return prospective, None
            if up and down and up[1] == down[1]:
                result.status = "ambiguous-raw-boundary-order"
                return prospective, None
            phase = "PH" if up and (down is None or up[1] < down[1]) else "PL"
            gate_index, cursor = up if phase == "PH" else down

        number = high_number if phase == "PH" else low_number
        candidates = [item for item in orders(phase, number, gate_index, cursor)
                      if order_meets_structure_gate(phase, item.first_index,
                          item.confirmation_event_time, gate_index, cursor)
                      and item.stop_event_time > item.confirmation_event_time]
        winner = min(candidates, key=lambda item: (
            item.stop_event_time, -item.first_index, item.break_index
        ), default=None)
        cancel = strict_cross(chronology, cursor,
                              floor if phase == "PH" else high_level,
                              phase == "PL")
        cancel_is_next = cancel and (
            (phase == "PL" and number > 3)
            or winner is None or cancel[1] < winner.stop_event_time
        )
        if cancel_is_next:
            raw_position = bisect_right(chronology.second_times, cancel[1]) - 1
            raw = chronology.seconds[raw_position]
            opposing = (as_decimal(raw.high) > high_level if phase == "PH"
                        else as_decimal(raw.low) < floor)
            if opposing:
                result.status = "ambiguous-raw-boundary-order"
                return prospective, None
        if phase == "PL" and number > 3:
            # The taught post-PL3 stage evaluates native Orders but does not
            # define PL4. A later upward break may still start a new PH.
            result.post_pl3_orders = [item for item in candidates
                if cancel is None or item.stop_event_time < cancel[1]]
            if cancel is None:
                result.status = "post-pl3-orders-only"
                return prospective, None
            gate_index, cursor = cancel
            phase = "PH"
            continue
        if cancel and winner and cancel[1] == winner.stop_event_time:
            result.status = "ambiguous-raw-boundary-order"
            return prospective, None
        if cancel and (winner is None or cancel[1] < winner.stop_event_time):
            gate_index, cursor = cancel
            if phase == "PL":
                phase = "PH"
            elif result.lows:
                # Cancelling a pending PH cannot manufacture a break of an
                # existing PL: later PL still requires that previous Low.
                if as_decimal(chronology.seconds[bisect_right(chronology.second_times, cursor)-1].low) < low_level:
                    phase = "PL"
                else:
                    phase = "seek"
            else:
                phase = "PL"
            continue
        if winner is None:
            result.status = f"waiting-for-{phase.lower()}-order-stop"
            return prospective, None
        source, price = _extreme(chronology, gate_index, winner.stop_index, phase == "PH")
        point = PrimaryPoint(phase, number, source, chronology.times[source], price,
                             gate_index, cursor, winner.stop_index,
                             winner.stop_event_time, winner, cycle_id=result.cycle_id)
        prospective.gate_index = gate_index
        prospective.cursor, prospective.phase = winner.stop_event_time, "seek"
        prospective.reset_high = phase == "PL"
        return prospective, point


class NativePrimaryOrders:
    """Read accepted native audit and commit PH parents to its Order owner.

    The owner bucket is the conceptual order direction in the user rules.
    Its native order_direction field names the opposite physical Reaction.
    Reaction Mode A/B is distinct from parent-stop/reset-leg creation type.
    Confirmed PH stops create Order_A through that native owner; unconfirmed
    structure crossings cannot manufacture physical Orders here.
    """

    def __init__(self, chronology, groups, *, on_high=None):
        self.chronology, self.groups = chronology, groups
        self.on_high = on_high

    def confirm_high(self, point):
        """Commit PH ownership before subsequent native Order selection."""
        if self.on_high is not None:
            self.on_high(point)

    def __call__(self, kind, number, gate_index, event):
        owner = "bearish" if kind == "PH" else "bullish"
        physical_direction = self.chronology.opposite_direction(owner)
        eligible = []
        records = []
        for prepared in self.groups[owner].get("OrderAudit", ()):
            reaction, entry = prepared["reaction"], prepared["entry"]
            first, breakout = int(reaction.first_idx), int(reaction.break_idx)
            confirmation = self.chronology.reaction_confirmation(physical_direction, reaction)
            stopped = prepared["crossed"]
            causes = tuple(dict.fromkeys(cause["kind"] for cause in prepared["causes"]))
            if not order_meets_structure_gate(kind, first, confirmation, gate_index, event):
                continue
            # PL Order_A's first valid downward Reaction must be canonical.
            if kind == "PL" and int(entry["reaction_number"]) <= 0:
                continue
            if kind == "PH" and number > 1 and "parent-stop" not in causes:
                continue
            records.append((prepared, first, breakout, confirmation, causes))
        direct = [row for row in records if "parent-stop" in row[4]]
        first_direct = min(direct, key=lambda row: (row[1], row[3], row[2]), default=None)
        for record in records:
            prepared, first, breakout, confirmation, causes = record
            reaction, entry, stopped = prepared["reaction"], prepared["entry"], prepared["crossed"]
            if (kind == "PL" and "reset-leg" not in causes and record is not first_direct):
                continue
            if stopped is None or stopped[2] <= max(confirmation, event):
                continue
            eligible.append(StructureOrder(
                physical_direction, int(entry["reaction_number"]), first, breakout,
                confirmation, as_decimal(entry["stop_level"]),
                int(entry["stop_source_index"]), int(stopped[0]), stopped[2],
                causes, as_decimal(reaction.box_top), as_decimal(reaction.box_bottom),
                reaction_mode=str(reaction.mode),
                audit_causes=tuple(deepcopy(cause) for cause in prepared["causes"]),
            ))
        return eligible
````
<!-- EXACT-SOURCE-END:pipeline/PL_PH_detector.py -->

### 16.13 `pipeline/reaction_engine.py` — Reaction / Reset

**SHA-256:** `f62f7e3c6480750068c4550a8489806030aac16f021f349930bd5efb3ce54198`  
**Bytes:** `105073`  
**LF count:** `2439`

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


REACTION_ENGINE_VERSION = "9.8.1"
REACTION_ENGINE_IMPLEMENTATION_VERSION = "9.9.1"
REACTION_ENGINE_LAST_MODIFIED = "2026-10-07 00:56:52 +03:30"

_ORDER_GATE_CACHE_MAX_ENTRIES = 32_768

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
        # Run-scoped performance caches. Order-gate geometry is queried many
        # times by iterative E/OrderAudit reconciliation with identical immutable
        # chronology and gate inputs. Cache raw geometry and clone on return so
        # callers retain the historical fresh-Candidate mutation semantics.
        self._order_gate_geometry_cache: dict[
            tuple[str, int, int, datetime | None], Candidate | None
        ] = {}

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
        cache_key = (direction, gate_index, limit, gate_event_time)
        if cache_key in self._order_gate_geometry_cache:
            cached = self._order_gate_geometry_cache[cache_key]
            return replace(cached) if cached is not None else None

        def cache_result(result: Candidate | None) -> Candidate | None:
            # The cache is run-scoped and bounded. FIFO eviction is sufficient
            # because cache order never participates in trading semantics.
            if len(self._order_gate_geometry_cache) >= _ORDER_GATE_CACHE_MAX_ENTRIES:
                oldest = next(iter(self._order_gate_geometry_cache))
                del self._order_gate_geometry_cache[oldest]
            self._order_gate_geometry_cache[cache_key] = (
                replace(result) if result is not None else None
            )
            return result

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
            return cache_result(result)

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
            return cache_result(None)
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
            return cache_result(None)
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
                return cache_result(None)
            search_start = int(source.index) + 1
        if search_start > limit:
            return cache_result(None)
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
        return cache_result(result)

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
        else:
            # Initial confirmation opens the same Normal-search handoff as
            # every later confirmed Reaction. Reuse the shared confirmation-
            # candle candidate rule so an eligible same-candle First is not
            # lost merely because this was the first Reaction of the run.
            candidate = self._candidate_from_confirmation_remainder(
                direction, initial, initial_break_candle, initial_analysis
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

### 16.14 `pipeline/s_zone_detector.py` — S

**SHA-256:** `0c5864bc3bc6c17f72c5c38b04a1cd0b5b38c726d8834207a55d5351fdfa38fe`  
**Bytes:** `60942`  
**LF count:** `1445`

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


S_ZONE_VERSION = "4.20.1"
S_ZONE_IMPLEMENTATION_VERSION = "4.21.1"
S_ZONE_LAST_MODIFIED = "2026-10-23 12:23:13 +02:00"


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
                order_direction=self.order_direction,
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

## 17. Historical verification and reconstructability annex

> **Historical evidence only:** this annex preserves earlier package verification and reproduction claims. It is not current PH/PL feature verification and does not override the live Source inventory, Section 13.4a or Section 14.0p.


**Annex modified:** `2026-10-23 12:49:29 +02:00`. This annex supplements the complete Source snapshot in Section 16 and does not modify or introduce any trading rule. Source module versions, exact Source content, embedded hashes, and document version remain `5.4.32`. Only available evidence is marked verified; the two References must have identical production Source but directional normative text.

### 17.1 Implementation-to-spec map

| Stage | Authoritative code | Input ownership | Output and contract |
|---|---|---|---|
| Input, timezone, output | `bridge/trading_pipeline.py`, `pipeline/core_utils.py` | Full supplied 5s RAW; Decimal prices; Tehran-native local times | Main/lower-TF Candle, directional projection, stable JSON |
| Directional symmetry | `pipeline/direction_policy.py`, `pipeline/reaction_engine.py` | Canonical sign/High-Low transform, GREEN Doji invariant | First/Break/Reset identity and exact event time |
| Reaction and Reset | `pipeline/reaction_engine.py` | Canonical First candidate, Break, strict Reset, lower-TF chronology | Ordered Reaction/Reset streams and internal ownership |
| Blue | `pipeline/blue_line_detector.py` | Confirmed Reaction/Reset, Fibonacci, exact confirmation prefix | Calculation-valid/public Blue lines and source/price |
| A | `pipeline/a_zone_detector.py` | BlueState and first-stop/inherited/double-stop routes | Accepted A source, formation and strict stop |
| S | `pipeline/s_zone_detector.py` | Accepted A stop, aligned Reaction, physical opposite Order | S Blue/Red, Type-3/4, Simple/Advanced and decision event |
| E | `pipeline/e_zone_detector.py` | S/E/Order lineage and parent stops | Accepted E family/number/source/order lineage |
| Order_A / Order_B audit | `pipeline/order_audit_engine.py` | Physical Order identity and cause ledger | Parent-stop and reset-leg accepted Orders, confirmations, stops and provenance |
| Lifecycle and StopAll | `pipeline/lifecycle_engine.py` | Final S/E dominance, accepted strict behavior stops | StopAll; lifecycle suppression/visibility; accepted owner |
| Public output | `bridge/trading_pipeline.py` | Final reconciled calculation objects | Canonical serialized schema; no independent trading decisions |

### 17.2 Formal Bullish ↔ Bearish mirror checklist

| Concern | Bullish canonical behavior | Bearish counterpart | Non-directional guard |
|---|---|---|---|
| Physical Reaction First role | `FirstRed` | `FirstGreen` | Absolute timing, First/Break indices unchanged under sign reflection |
| Confirm Reaction | strict `High > BoxTop` | strict `Low < BoxBottom` | Equality excluded; exact lower-TF confirmation eligible |
| Reset Reaction / stop directional owner | strict `Low < BoxBottom` | strict `High > BoxTop` | Doji remains GREEN in both original market coordinate systems |
| Scale Blue strike | increasingly lower `Low`, confirmed GREEN | increasingly higher `High`, confirmed RED | Break candle restricted to exact Reaction confirmation prefix |
| Scale Blue level | `BoxTop - 0.618 * (BoxTop-reference)` | `BoxBottom + 0.618 * (reference-BoxBottom)` | Price-sign transformation, no float |
| Scale / Reset Blue display | `Low+(High-Low)/3` / `Low+(High-Low)/5` | `High-(High-Low)/3` / `High-(High-Low)/5` | Source candle and interval invariant |
| A source extrema | minimum eligible `Low` | maximum eligible `High` | Freeze at Reaction confirmation; preserve tie policy |
| S source candidate extrema | minimum eligible `Low` | maximum eligible `High` | Type-3/Type-4 last-on-equality where specified |
| Opposite Order strict stop | `High > OrderStop` | `Low < OrderStop` | Physical Order identity, provenance, same-candle ownership invariant |
| Order_B reset leg | `LL=min Low` and strict `Low<LL` | `HH=max High` and strict `High>HH` | Must respect reset then strict break and A-expiry TF candle |
| E/StopAll priority | `S Blue < E Blue < S Red < E Red` | Same | Behavioral family, numbering and owner identity invariant |
| Direct StopAll | armed `S/E Blue x2` → next eligible accepted `S Red` | Same | Decision event time controls eligibility; no direction-specific shortcut |

**Doji caveat:** exact sign-inverted original market candle Doji remains GREEN on both sides; color swapping is valid only for strictly non-Doji candles. Runtime synthetic mirror fixtures exclude exact Doji at both lower/main timeframe so no intentional Doji asymmetry is mistaken for directional drift. Real RAW tests retain all original Doji unchanged.

### 17.3 End-to-end executed test matrix

Inputs: five immutable XAUUSD/USOIL 5-second RAW JSON files totaling **337,611 physical source rows**. Each complete history ran under **15s, 30s, 60s and 300s** calculation timeframes, with **both directions in each run** and StopAll enabled/disabled. This yields **40 full-RAW dual-direction configurations**. Runtime reports and SHA digests are in `verification_matrix.json`; the full algorithm's serialized outputs are not claimed correct merely because execution succeeds.

Separate tests include 65 targeted Unit/boundary cases, 8 5,500-row paired synthetic full-stage mirror cases, 4 visible-window comparisons, 10 standalone-direction equivalence runs, and 5 repeat deterministic runs.

| Regression category | Result | Evidence or limitation |
|---|---|---|
| Source syntax and imports | **PASS** | 12 production modules: AST/compile/import completed |
| Targeted and numerical boundary tests | **PASS** | 65 pytest cases, strict price comparisons and equality, Doji, Decimal, OrderAudit, S, Blue, Lifecycle |
| Full history execution | **PASS** | 40 full-RAW dual-direction configurations, 337,611 available 5s rows |
| Directional runtime paths | **PASS** | 100 direction executions in full-matrix runner (includes standalone/repeat cases) |
| Current-version stable anchor hashes | **PASS** | 10/10 exact byte-canonical V5.4.32 baseline output digests (30s) |
| Single vs combined mode | **PASS** | 10 standalone vs two-direction output equivalence checks |
| Determinism | **PASS** | 5 repeat full-dataset stable output comparisons |
| Exact synthetic mirror | **PASS** | 8 independent XAUUSD/USOIL × timeframe combinations; all 8 stages, all nested provenance, price fields and times mirrored |
| Window projection | **PASS** | 4 full-history vs selected visible-window subset comparisons |
| Reference/Source fidelity | **PASS** | 2 References × 12 Python modules: manifest SHA-256 and exact embedded UTF-8 bytes |
| RAW integrity | **PASS** | Five source datasets unchanged; 10,185 overlapping XAUUSD 5s OHLC rows agree |
| Historical full repository anchor suite | **NOT RUN** | The provided engine.zip contains neither historical repository unit suite nor confirmed historical anchor fixture bundle |
| Downstream root-cause reconciliation | **INCOMPLETE** | 13 stage-pair changes from 5.4.31 to 5.4.32 were enumerated; not every changed physical trading event is independently approved |
| Application/web end-to-end | **NOT RUN** | UI and HTTP application not provided inside engine.zip |
| All possible market histories and timeframes | **NOT APPLICABLE** | Finite supplied data and discrete tested timeframe set cannot prove universal absence of defects |

### 17.4 Reproduction commands (working directory: engine package root)

```bash
python -m pytest -q tests/unit
python tests/verification/verify_order_references.py
python tests/verification/verify_raw_integrity.py --raw-dir /path/to/RAW-directory
python tests/verification/verify_full_raw_matrix.py --raw-dir /path/to/RAW-directory --timeframes 15,30,60,300
python tests/verification/verify_extended_mirror.py --data /path/to/xau_raw.json /path/to/usoil_raw.json --timeframes 15,30,60,300
python tests/verification/verify_window_projection.py --data /path/to/xau_raw.json /path/to/usoil_raw.json
```

### 17.5 Historical branch and acceptance boundary

1. This is the source-synchronized `5.4.32` patch derived from the explicitly uploaded `5.4.31` package, **not** an automatic cumulative merge from historical 5.4.28 or 5.4.29 branches.
2. The historical GitHub regression-anchor suite, complete application/HTTP tests, and all earlier/unprovided 1-second market RAW were **not contained** in that package. Their correctness is not certified by the completed five-file 5-second runs.
3. The detailed 5.4.31→5.4.32 first-difference register, including intentionally changed Blue and downstream A/S/OrderAudit candidates, is in `verification_baseline_differences.json`. A changed result may be causally expected from the exact Blue confirmation-prefix bugfix, but user-approved independent event-level expected anchors were not provided for every affected event.
4. **Final regression status: REGRESSION NOT VERIFIED.** All executed tests above passed, but historical anchor and event-level causal acceptance remain incomplete. No claim of universal zero-defect behavior is implied.
