---
id: "source.order_audit_engine"
type: "source"
status: "active"
authority: "executable"
title: "Physical Order_A and Order_B discovery, reset-leg anchors, immutable identity/provenance and accepted/live ledgers"
version: "1.7.1"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/order_audit_engine.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"
mirror: "06_SOURCE/Code/engine/pipeline/order_audit_engine.py"
sha256: "f4e991a6a516ad84e0223c802f5baf611f5e20fb8d7965b9dcdf4ff949d89296"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# order_audit_engine.py

Physical Order_A and Order_B discovery, reset-leg anchors, immutable identity/provenance and accepted/live ledgers.

Exact bytes describe executable behavior; Source identity is not intended-semantic authority or independent market correctness. Supported dynamic Bridge loading and the maintained pipeline compatibility wrapper are distinct runtime surfaces. The manifest source_scope bounds audit/reconstruction completeness.

## Snapshot identity

| Property | Current captured evidence |
| --- | --- |
| Source | 06_SOURCE/Code/engine/pipeline/order_audit_engine.py |
| SHA-256 | f4e991a6a516ad84e0223c802f5baf611f5e20fb8d7965b9dcdf4ff949d89296 |
| Bytes | 89666 |
| Lines | 2175 |
| Declared version | 1.7.1 |

## Lexical Source symbols

Every lexical definition in this captured owner is indexed mechanically, including incidental out-of-scope feature helpers. A symbol row is navigation, not a separate concept or semantic approval.

| Symbol | Line | End |
| --- | ---: | ---: |
| relabel_primary_causes | 19 | 31 |
| PostBehaviorStop | 34 | 38 |
| OrderBBehaviorAnchor | 42 | 47 |
| OrderBResetLeg | 51 | 68 |
| dominant_post_behavior_stops | 71 | 114 |
| order_b_reset_event_time | 117 | 145 |
| discover_order_b_reset_legs | 148 | 349 |
| discover_accepted_order_b_reset_legs | 352 | 427 |
| order_b_leg_identity | 437 | 457 |
| OrderAuditEngineMixin | 461 | 1774 |
| OrderAuditEngineMixin._order_stop | 464 | 490 |
| OrderAuditEngineMixin.order_stop | 493 | 497 |
| OrderAuditEngineMixin._first_healthy_direct_geometry | 500 | 572 |
| OrderAuditEngineMixin._trend_leg_direct_order | 575 | 624 |
| OrderAuditEngineMixin._direct_parent_stop_order | 627 | 645 |
| OrderAuditEngineMixin._compute_direct_parent_stop_order | 647 | 736 |
| OrderAuditEngineMixin._merge_order_candidate | 739 | 770 |
| OrderAuditEngineMixin._enforce_single_parent_stop_owner | 773 | 797 |
| OrderAuditEngineMixin.order_candidates | 800 | 888 |
| OrderAuditEngineMixin._first_order | 891 | 904 |
| OrderAuditEngineMixin._has_sequence_reset_between | 907 | 915 |
| OrderAuditEngineMixin._index_order_audit_identity | 918 | 925 |
| OrderAuditEngineMixin._clear_order_audit | 928 | 932 |
| OrderAuditEngineMixin._invalidate_carried_order_caches | 934 | 939 |
| OrderAuditEngineMixin._invalidate_post_stop_order_cache | 941 | 942 |
| OrderAuditEngineMixin.register_order_b_reset_legs | 945 | 1009 |
| OrderAuditEngineMixin._reparent_primary_high_causes | 1012 | 1058 |
| OrderAuditEngineMixin.register_primary_high | 1060 | 1097 |
| OrderAuditEngineMixin.reconcile_primary_high_labels | 1099 | 1117 |
| OrderAuditEngineMixin._register_order_audit | 1119 | 1190 |
| OrderAuditEngineMixin.visual_order_lifecycle | 1194 | 1213 |
| OrderAuditEngineMixin._cross_order | 1216 | 1234 |
| OrderAuditEngineMixin.cross_order | 1237 | 1241 |
| OrderAuditEngineMixin._unconsumed_s_orders | 1244 | 1278 |
| OrderAuditEngineMixin._initial_order_records | 1281 | 1336 |
| OrderAuditEngineMixin._initial_record_match | 1340 | 1351 |
| OrderAuditEngineMixin._initial_order_match | 1354 | 1366 |
| OrderAuditEngineMixin._gate_owned_initial_order | 1369 | 1389 |
| OrderAuditEngineMixin._carried_orders_for_parent | 1392 | 1450 |
| OrderAuditEngineMixin._post_stop_accepted_orders_for_parent | 1453 | 1532 |
| OrderAuditEngineMixin._post_stop_accepted_orders_for_parent.add_match | 1467 | 1484 |
| OrderAuditEngineMixin._blocked_by_gate_owned_order | 1535 | 1543 |
| OrderAuditEngineMixin._rebuild_accepted_order_audit | 1546 | 1729 |
| OrderAuditEngineMixin._rebuild_accepted_order_audit.valid_parent_stop_cause | 1557 | 1570 |
| OrderAuditEngineMixin.rebuild_accepted_order_audit | 1732 | 1744 |
| OrderAuditEngineMixin.ensure_accepted_order_audit | 1747 | 1774 |
| _parent_stop_cause_key | 1777 | 1783 |
| _collect_s_ledger_entries | 1786 | 1815 |
| _collect_e_ledger_entries | 1818 | 1844 |
| _merge_prepared_identities | 1847 | 1887 |
| _single_owner_parent_stop_causes | 1890 | 1925 |
| prepare_order_audit | 1928 | 1945 |
| accepted_audit_entry | 1948 | 1978 |
| accepted_audit_entries | 1981 | 1991 |
| order_identity_is_internal | 1994 | 2000 |
| SOrderAuditMixin | 2003 | 2174 |
| SOrderAuditMixin._first_order_after | 2006 | 2059 |
| SOrderAuditMixin._order_matches_after | 2062 | 2081 |
| SOrderAuditMixin._record_a_order_audit | 2084 | 2116 |
| SOrderAuditMixin._audit_stopped_a | 2119 | 2129 |
| SOrderAuditMixin._order_stop | 2132 | 2141 |
| SOrderAuditMixin._order_stop_crossed | 2144 | 2147 |
| SOrderAuditMixin._shared_order_stop_cross | 2150 | 2174 |
