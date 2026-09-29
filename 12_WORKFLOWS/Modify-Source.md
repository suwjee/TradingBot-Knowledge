---
id: "workflow.modify_source"
type: "workflow"
status: "active"
authority: "executable"
title: "Modify current Source safely"
version: "current"
related_entities: ["workflow.operating"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Modify current Source safely

Confirm exact current owner/version and freeze stable output/input/source identity. Preserve dirty work. Design a small behavior-correct change with efficient data flow, explicit ownership, Decimal semantics and complete cache scope. Test the owning rule and unaffected upstream/downstream state. Version only changed modules and synchronize durable references. Exact Vault snapshots are replaced by copying verified current source, never manually patched.
