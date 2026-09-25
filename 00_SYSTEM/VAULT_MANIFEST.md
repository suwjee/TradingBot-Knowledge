---
id: "system.manifest"
type: "system"
status: "canonical"
authority: "normative"
title: "Vault manifest"
source_refs: ["engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md", "engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.11_HPZR6_Forensic_Synchronized.md", "engine/bridge/trading_pipeline.py#L1732"]
---

# Vault manifest

This Vault records the current TradingBot calculation contract for AI retrieval. Canonical rules live in Markdown notes with stable IDs. _INDEX is derived; 06_SOURCE/Code is a byte-exact evidence snapshot; engine/ is executable authority. The nine Python modules and two V5.4.11 HPZR6 references were inspected for this build. The reference documents embed source whose declared SHA-256 hashes match the current nine modules at inspection.

Phase 1 covers system controls and the minimum core/market model. Phase 2 covers A, S, E, StopAll. Phase 3 covers the calculation path. Phase 4 maps source modules and captures hashes. Empty future directories have no authority.

Read 00_SYSTEM/AUTHORITY_MODEL.md before resolving any rule. Read 01_CORE/Pipeline.md before tracing a stage. Resolve IDs through _INDEX/entities.json when present, then open canonical Markdown. An index never overrides its note.

Production root: D:/My-Projects/TradingBot. Vault root: D:/My-Projects/TradingBot-Knowledge. Current source is a dirty working tree; do not infer source identity from Git HEAD alone. The older root AGENTS.md project summary describes earlier versions and is not the authority for current V5.4.11 rules.

Current Open Issue: the chart server may send a selected-range stream to the bridge. The bridge calculates over its complete received input. The engine reference's full-physical-RAW guarantee applies when the bridge receives the complete RAW file; do not infer identical history for a prefiltered input.
