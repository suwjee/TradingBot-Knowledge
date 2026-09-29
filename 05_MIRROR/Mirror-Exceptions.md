---
id: "mirror.exceptions"
type: "mirror"
status: "active"
authority: "executable"
title: "Current mirror boundary qualifications"
version: "current"
related_entities: ["algorithm.reset", "algorithm.s", "core.chronology", "mirror.contract"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py", "06_SOURCE/Code/engine/pipeline/a_zone_detector.py", "06_SOURCE/Code/engine/pipeline/s_zone_detector.py", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
---

# Current mirror boundary qualifications

## Internal color-role reflection

mirror_candle swaps GREEN/RED internal role tags,including the adapter role of a Doji,so one Bullish-coordinate state machine implements Bearish FirstGreen. Original market Doji remains GREEN. This is a coordinate qualification,not a second market classification.

## Owner-specific time windows

A confirmation intentionally scans Break-open via use_intrabar_start=False; S/E/public normally use intrabar_start. A source ends exact confirmation while E uses complete containing boundary main candles. These distinctions apply symmetrically and cannot be flattened into one generic mirror window.

## Symmetric Reset boundary

Current Unified initial,post-Reset and normal confirmation handling uses analysis.extreme both directions when available,stored BoxBottom/BoxTop only without analysis. There is no direction-only stored-edge exception in these current branches.

## Explicit inclusive gates

Blue pending intrabar penetration can come from decisive confirmation row itself. Shared S accepted Order stop can equal source main-candle open and must be strictly earlier than current decision. Current Source and canonical References specify both boundaries; strict price predicates remain strict in both directions. These are Source contract qualifications,not unresolved directional exceptions.
