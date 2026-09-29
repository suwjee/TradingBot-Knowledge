---
id: "system.manifest"
type: "system"
status: "active"
authority: "normative"
title: "Current-only Vault manifest"
version: "current"
related_entities: ["data.policy", "source.reference_consistency", "source.reference_registry", "source.source_manifest", "system.authority", "test.validation_contract", "version.current"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Current-only Vault manifest

This Vault represents the current audited TradingBot implementation with exact Reference version 5.4.19-EX1 evidence. Narrative scope discrepancies are registered in source.reference_consistency. Legacy active rules, old Reference copies, correction overrides and market examples are removed. Source inventory contains 13 exact current Python files, including package files. Current hashes and per-owner versions are in source-hashes.json and version.current; Reference versions are independent.

RAW datasets, windows and regression cases are zero: EMPTY_BY_DESIGN. Market regression is NOT_REQUIRED_THIS_PHASE under the current task. Empty future directories are documented by Data/Fixture policies. Indexes and graph are derived navigation and never authority.

The current-contract declaration in _INDEX/source-hashes.json pins the reviewed active entity inventory, statuses and owners. Generic validation rejects missing/extra current concepts or status/owner drift. Exact source/reference inventories are checked without baked-in counts or versions. Full metadata is preserved in generated entity rows and validated by the Plugin.

Read _GENERATED/Current-Validation.md for completed command exits, counts, integrity/mirror scope and readiness. Until the final matrix completes, release status is INCOMPLETE. This manifest does not turn a pending check into PASS.
