---
id: "workflow.analyze_raw"
type: "workflow"
status: "active"
authority: "executable"
title: "Analyze future supplied RAW"
version: "current"
related_entities: ["workflow.operating"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Analyze future supplied RAW

Register only explicitly supplied immutable RAW. Verify schema, actual bytes/hash, resolution, timezone and chronology. State full file versus selected stream scope. Normalize through current parser, run the requested current pipeline and inspect exact lower-timeframe events. Report input validation separately from algorithm correctness. The current store contains no input to analyze.
