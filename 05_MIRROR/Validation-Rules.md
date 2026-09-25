---
id: "mirror.validation_rules"
type: "mirror"
status: "pending"
authority: "non-canonical"
title: "Mirror validation requirements"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["mirror.contract", "mirror.direction_mapping", "mirror.invariants", "mirror.algorithm_matrix", "algorithm.reaction", "algorithm.lifecycle", "algorithm.serialization", "source.direction_policy", "source.trading_pipeline", "test.mirror_validation", "test.mirror_policy", "test.direction_tests", "test.symmetry_tests", "test.mirror_regression"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py#L32", "06_SOURCE/Code/engine/pipeline/reaction_engine.py#L560"]
---

# Mirror validation requirements

> Scope: This mirror description is provisional. Full directional references and mixed source modules are absent from this Vault; verify each rule against retained local source before use.

This is the Mirror contract used by the executed `07_VALIDATION` layer. `test.mirror_validation` and the registered fixtures define validation targets, but their existence does not claim a fresh two-direction pipeline run. Both references §19 and §24 provide acceptance/examples; current source anchors identify the fields to compare.

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

## Regression validation


The Validation layer now records 28 fixture cases, including Pending and Historical evidence. `test.direction_tests`, `test.symmetry_tests`, and `test.mirror_regression` route the corresponding execution evidence without duplicating the algorithms here. A full Mirror regression result still requires a current run with pinned RAW, source, settings and output; this note defines requirements and does not report such a result.
