---
id: "data.lineage"
type: "data"
data_kind: "lineage"
status: "canonical"
authority: "normative"
title: "Dataset to validation lineage"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.dataset_registry", "data.raw_model", "core.pipeline", "algorithm.raw", "algorithm.reaction", "algorithm.blue", "algorithm.a", "algorithm.s", "algorithm.e", "algorithm.stopall", "behavior.a", "behavior.s", "behavior.e", "behavior.stopall", "test.validation_contract", "test.regression_policy", "source.trading_pipeline"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L133", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L133", "engine/bridge/trading_pipeline.py#L1732", "engine/bridge/trading_pipeline.py#L2300"]
---

# Dataset to validation lineage

The trace is: **dataset entity → exact RAW path and SHA → bridge input scope → normalized lower/main candles → Reaction/Reset → Blue → A → S → E → StopAll/lifecycle → serialized behavior → fixture assertion → regression comparison**. `algorithm.raw` owns the first normalization step; the named stage algorithms and source modules own subsequent calculations. `behavior.a/s/e/stopall` name public semantics. Validation notes decide whether an observed output satisfies a current expectation.

Dataset notes link directly to the fixtures that use their exact hash, the RAW algorithm, behaviors evidenced by selected current fixture assertions, the regression policy and validation notes. That graph is a navigation aid: a data note does not define the behavior or prove a full output. Historical and Pending fixtures remain linked for provenance but cannot supply a current baseline. A dataset may support both Bullish and Bearish interpretation without separate copies.

Preserve the complete supplied input when comparing calculations. A selected chart range is a presentation filter after full bridge calculation; an upstream prefiltered stream becomes a different calculation input. Source indexes and later resolution can change when scope changes. See [RAW-Authority.md](Raw/RAW-Authority.md) and `test.baseline_policy`.
