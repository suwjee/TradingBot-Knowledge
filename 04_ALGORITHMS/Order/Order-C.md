---
id: "algorithm.order.c"
type: "algorithm"
status: "pending-fix"
authority: "non-canonical"
title: "Order_C current implementation, quarantined"
implementation_validity: "known-invalid"
valid_for_reasoning: false
valid_for_validation: false
valid_for_regression_baseline: false
rewrite_required: true
implemented_by: ["source.e_zone_detector"]
depends_on: ["algorithm.order", "algorithm.reset", "algorithm.blue"]
source_refs: ["06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L674", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L727", "06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L830"]
related_entities: ["test.source_validation"]
source_reference: ["06_SOURCE/Code/engine/pipeline/e_zone_detector.py#L727"]
---

# Order_C

## وضعیت فعلی

Known-invalid by explicit project decision. The current Blue-qualified route is retained solely as defective executable and reference evidence, not as an approved future rule.

## Current Implementation Evidence

`EZoneDetector._order_c_leg` (line 674), `_first_order_c_reaction_after_break` (line 710), `_build_order_c_formations` (line 727), and `_order_c_candidates` (line 830) show the present construction and candidate path. The source also enriches audit data from this cause; the audit itself has no active Vault concept.

## Reference Evidence

Both registered HPZR6 references contain §10.3C describing the present Blue-qualified route. The sections are retained as reference evidence with known-invalid semantics. A present source/reference match is not approval.

## Known Validity State

`pending-fix` / `non-canonical` / `known-invalid`. Native Reaction modes and independent Order_C creation cause are distinct concepts. No corrected Order_C semantics have been supplied.

## Dependencies

The current source consults Reset ownership, a selected Leg Start, Blue formation, exact strict crossing, opposite Reaction chronology and physical Order identity. These are current-code dependencies only.

## Impact Surface

Current E candidate and cause selection, lifecycle decisions, bridge output and fixture expectations may depend on this route. B/C-dependent portions must be reviewed individually; unrelated E logic is not globally invalid.

## Validation Policy

Use this note only for diagnostics and drift checks. Do not promote B/C-dependent outputs to approved regression baselines. Future validation requires a revised accepted contract and independent direction tests.

## Rewrite Requirements

Specify the intended geometry, Blue qualification, event gates, identity, stop, tie and selection rules, mirror mapping, interactions with Order_A/B and lifecycle effects before modifying source or promoting this note.
