---
id: "algorithm.orderaudit"
type: "algorithm"
status: "pending-fix"
authority: "non-canonical"
title: "OrderAudit (pending fix)"
implemented_by: ["source.s_zone_detector", "source.e_zone_detector", "source.lifecycle_engine", "source.trading_pipeline"]
depends_on: ["algorithm.order"]
source_refs: ["engine/pipeline/s_zone_detector.py#L325", "engine/pipeline/e_zone_detector.py#L1395", "engine/pipeline/lifecycle_engine.py#L621", "engine/bridge/trading_pipeline.py#L1469"]
---

# OrderAudit (pending fix)

Current implementation locations only: SZoneDetector._record_a_order_audit and _audit_stopped_a; EZoneDetector._register_order_audit, _rebuild_accepted_order_audit and related enrichment; lifecycle_engine.prepare_order_audit; bridge validate_order_audit_bridge and serialize_order_audit. The current code emits an OrderAudit and maintains physical identity/provenance ledgers, but the user has designated this component incomplete/problematic. Its current behavior is executable evidence, not canonical trading logic.

No normative OrderAudit algorithm is specified in this phase. Do not use this note or current audit output to derive S/E/StopAll trading rules. A future corrected implementation and reference must establish the contract before this note may become canonical.
