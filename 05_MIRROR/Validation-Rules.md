---
id: "mirror.validation_rules"
type: "mirror"
status: "active"
authority: "canonical"
title: "Mirror validation requirements"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["mirror.contract", "mirror.direction_mapping", "mirror.invariants", "mirror.algorithm_matrix", "algorithm.reaction", "algorithm.lifecycle", "algorithm.serialization", "source.direction_policy", "source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1099", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L1099", "engine/pipeline/direction_policy.py#L32", "engine/pipeline/reaction_engine.py#L560", "engine/pipeline/lifecycle_engine.py#L25", "engine/bridge/trading_pipeline.py#L2776"]
---

# Mirror validation requirements

This is a contract for future `07_VALIDATION` work. It does not claim that the tests below have been executed or that an empty validation placeholder is evidence. Both references §19 and §24 provide acceptance/examples; current source anchors identify the fields to compare.

## Direction validation

- For identical physical RAW input, run Bullish and Bearish through the same bridge settings. Check each source-confirmed mapping in `Direction-Mapping.md`: Low/High, min/max, strict stop, opposite confirmation, First/context role, Blue level/line and Order opposite direction. `direction_policy.py#L21-L70`; `reaction_engine.py#L560-L703`; `blue_line_detector.py#L75-L81`.
- Include equality cases: `Low == level` and `High == level` must not count as strict crossings; confirmation equality must not confirm. `direction_policy.py#L32-L46`.
- Compare exact lower-event order when confirmation, invalidation, Reset or stop occur in one main candle. Preserve source indexes/times and the same-Break `analysis.extreme` edge. Both references §5, §6.3, §6.7; `reaction_engine.py#L1550-L1581`.

## Invariant validation

- Assert one A/S/E/StopAll taxonomy, shared S Blue Type-1..4, one E numbering model and physical Order identity `(FirstIndex,BreakIndex)` across both directions. Both references §0.1, §10.7, §11; `core_utils.py#L19-L29`; `e_zone_detector.py#L2267-L2463`.
- Assert `StopAll > E Red > S Red > E Blue > S Blue > A`, A → S → E → StopAll eligibility, hard StopAll reset, exact Blue-repeat keys, and invariant family labels. Both references §12–13; `lifecycle_engine.py#L25-L35`, `#L331-L455`.
- Assert chronology, owner/cause provenance, Decimal calculation and public JSON key/null/version structure remain stable. Both references §3, §5, §11, §16; `core_utils.py#L11-L29`; `trading_pipeline.py#L239-L493`, `#L2776-L2950`.

## Source validation

- Trace every documented rule to the hash-pinned V5.4.11 HPZR6 references and current nine-module source snapshot. Verify `source_reference` paths/line anchors and `related_entities` targets with the Vault index builder. `direction_policy.py` owns shared predicates; Reaction reflection and module-specific geometry stay in their source owners. Both references §0.2 and §20; `direction_policy.py#L1-L10`; `reaction_engine.py#L560-L703`.
- If source and references diverge, mark that rule unresolved with both anchors before changing canonical Mirror knowledge. The mixed-cause Internal-Reaction E/StopAll filter is such a case: both references §14 line 638 require reset-leg-only, whereas `lifecycle_engine.py#L1658-L1678` checks for any reset-leg cause or timestamp. Do not infer the answer from OrderAudit output alone.

## Regression validation

For every implementation change, compare pre-change and post-change **full continuous input** payloads for both directions under identical settings. Mirror behavior must remain equal unless an approved algorithm change explicitly authorizes the difference; then record the changed rule, affected source/line, provenance, and expected output delta. Compare stage collections and final visibility, not only chart counts. Include targeted same-Break, Order_A/B/C, native Mode-B StopAll, internal-Reaction visibility (especially mixed reset-leg plus independent cause) and E-number cases. Both references §19, §24; `trading_pipeline.py#L1903`, `#L2549`, `#L2776`.

Validation is incomplete until the future `07_VALIDATION` layer contains runnable cases and their results. This file defines requirements only.
