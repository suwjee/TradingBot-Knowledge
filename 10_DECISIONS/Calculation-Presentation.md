---
id: "decision.calculation_presentation"
type: "decision"
status: "active"
authority: "executable"
title: "Current calculation/presentation separation"
version: "current"
related_entities: ["system.authority"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Current calculation/presentation separation

Python owns calculation state and exact chronology. Node owns supplied request scope and subprocess transport. The browser renders finalized output and cannot infer trading semantics. Serializers project finalized state and cannot repair an upstream rule.
