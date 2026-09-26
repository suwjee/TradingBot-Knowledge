---
id: "mirror.algorithm_matrix"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Algorithm mirror matrix"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["algorithm.raw", "algorithm.reaction", "algorithm.reset", "algorithm.blue", "algorithm.a", "algorithm.s", "algorithm.e", "algorithm.order", "algorithm.lifecycle", "algorithm.serialization", "source.reaction_engine", "source.blue_line_detector", "source.a_zone_detector", "source.s_zone_detector", "source.e_zone_detector", "source.lifecycle_engine", "source.core_utils", "source.trading_pipeline"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L21"]
---

# Algorithm mirror matrix

> Scope: All nine main Engine modules are captured, but full HPZR6 references are optional external evidence. Current Order_B/C mirror behavior is diagnostic only until those routes are rewritten and accepted.

Classification below is provisional where a stage needs source omitted from this Vault. A Mixed row contains separate Directional and Invariant atomic rules; it does not place one atomic rule in two categories.

| Algorithm | Category | Directional component | Invariant component | Source owner / anchor |
|---|---|---|---|---|
| RAW | Invariant | None: the RAW rows are input, not mirrored data. | Physical OHLC/time parsing, candle color and chronology input identity. | `trading_pipeline.py#L120-L174`, `#L1732`; `reaction_engine.py#L91` |
| Reaction | Mixed | First/context role, box side, invalidation and confirmation comparison. | One Mode A/B state machine, Candidate identity, exact event order and ownership. | `reaction_engine.py#L174-L703`, `#L1376` |
| Reset | Mixed | Opposite-boundary price side and strict break. | Event identity, same-Break ownership and chronology. | `reaction_engine.py#L247-L267`, `#L1550-L1581` |
| Blue | Mixed | Fibonacci, strikes, directional line and stop price. | Scale/Reset identities and strike state. | `blue_line_detector.py#L75-L81`, `#L139-L299` |
| A | Mixed | Candidate extreme, Blue stop and trigger side. | A identity, Blue provenance and stage order. | `a_zone_detector.py#L97-L166`, `#L219-L311` |
| S | Mixed | Candidate/Order stop geometry and strict race. | Red/Blue and Type-1..4 identities, A/Order ownership. | `s_zone_detector.py#L223-L331`, `#L482-L638` |
| Order_A | Mixed | Opposite direction and source-owned strict stop geometry. | The first eligible opposite Reaction after an A stop owns the parent-stop cause; physical identity uses `(FirstIndex,BreakIndex)`. | `s_zone_detector.py#L274-L331`; `core_utils.py#L19-L29` |
| Lifecycle | Invariant | None in the *stage/priority/ownership rules*; detector price comparisons are delegated directional components. | A → S → E → StopAll stage cycle, priority, eligibility and visibility/lineage rules. | `lifecycle_engine.py#L25-L35`, `#L946-L1177`, `#L1708`; `trading_pipeline.py#L2549` |
| Serialization | Invariant | None in field/key structure; emitted values carry direction. | Shared collection keys, nullability, versions, Decimal string format and physical indexes. | `trading_pipeline.py#L239-L493`, `#L2776-L2950` |

StopAll itself is **Mixed** (see `Mixed-Rules.md`), even though the lifecycle controller row is Invariant. RAW invariance applies to engine input, not to external selection of a partial chart range; that external boundary is described in existing Vault integration notes and is not a mirror transformation. Both references §3 and §13; `lifecycle_engine.py#L115-L127`; `trading_pipeline.py#L1732`.
