---
id: "data.dataset_template"
type: "data"
data_kind: "template"
status: "canonical"
authority: "normative"
title: "Dataset entity template contract"
created: "2026-09-25"
updated: "2026-09-25"
related_entities: ["data.dataset_registry", "data.hash_policy", "data.integrity", "data.data_validation", "test.fixture_model", "algorithm.raw"]
source_reference: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md#L145", "engine/bridge/trading_pipeline.py#L120", "engine/bridge/trading_pipeline.py#L1732"]
---

# Dataset entity template contract

Each real dataset note uses `type: data`, `data_kind: dataset`, and an ID `data.dataset_<first eight SHA-256 characters>`. The complete hash remains in `raw_sha256`. Required identity fields are `name`, `symbol`, `broker`, `market`, `source`, `instrument`, input `timeframe`, observed `resolution`, `start_time`, `end_time`, `timezone`, `raw_path`, all `raw_locations`, `raw_bytes`, `row_count`, `first_epoch` and `last_epoch`. Unknown provenance or instrument type is the literal `unknown`, not a broker-derived guess.

Required relationship fields are `direction_support`, `consumed_by_algorithms`, `produces_behaviors`, `used_by_fixtures`, `validated_by`, `chronology_model`, `regression_role`, `hash_reference` and `related_entities`. `used_by_fixtures` may include Historical/Pending case IDs for traceability; only current confirmed positive outputs may inform `produces_behaviors`, which is explicitly a *subset of fixture-evidenced behavior*, not an output inventory. A zero-length array means no such evidence, not that the engine can never produce that behavior.

An intact byte stream with verified stated metadata uses `status: active`, `authority: empirical`, `integrity_status: verified`. A known metadata conflict uses `draft`, `non-canonical`, `pending_metadata_conflict`. Neither state grants algorithm authority or a successful regression result. The builder checks paths, size, SHA-256 and case hash links. See `_SCHEMA/data.schema.json` for machine-readable required fields and [Dataset-Registry.md](Dataset-Registry.md) for concrete examples.
