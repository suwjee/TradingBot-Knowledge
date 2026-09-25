---
id: "system.retrieval"
type: "system"
status: "canonical"
authority: "normative"
title: "Retrieval policy"
---

# Retrieval policy

For every retrieval session, first load `system.authority` and this policy by ID; load `system.frontmatter` when editing metadata. These global policy notes are intentionally discoverable by ID rather than by a decorative edge from every trading entity. Resolve IDs through `_INDEX/entities.json`, open the owning Markdown, then follow only relations relevant to the question. Check status and authority before using a claim. Verify source symbols/lines against the current production file or hash-matched mirror; check `_INDEX/source-hashes.json` before treating a snapshot as current. The two V5.4.11 HPZR6 directional references are external, hash-pinned normative inputs under `D:/My-Projects/TradingBot/engine/algorithms/`. A Vault-only reader without those exact files must say that independent normative verification is unavailable. The future Plugin/MCP reader must have read access to those production references and verify their hashes; do not substitute a free-floating duplicate.

For a Behavior question, start at the specific behavior and `calculated_by` algorithm, then load shared route, prerequisite, lifecycle, and source-owner notes as needed. For “why S Blue Type-4 did not form,” use `behavior.s.blue.type4` -> `algorithm.s.type4` -> `algorithm.s`, then A, Reaction, Blue, Order deadline, lifecycle, `source.s_zone_detector`, and relevant chronology; avoid loading unrelated E/StopAll details unless the actual question reaches them. For E2 replacing E1, load E numbering, E reconciliation, lifecycle, parent/source evidence. For StopAll, load the specific gate type, shared StopAll algorithm, priority, and lifecycle. For strict crossing, use `market.crossing`, `core.precision`, `source.direction_policy`, and the consuming detector. For S serialization, use `algorithm.serialization` and the bridge serializer. For Order_C, use `algorithm.order.c` and its owning E source. For noncanonical knowledge, inspect `system.authority` and `algorithm.orderaudit` without promoting the latter.

Use `implemented_by` for actual rule owners. `orchestrates` identifies pass coordination; `supports` identifies a shared primitive. For chart result questions, inspect `source.integration_boundary` and the request input scope before applying the full-physical-RAW normative contract. Its external chart paths require production-repository access. If a needed relation or reference is absent, report that gap. If a source/reference hash changed, mark the affected answer stale until re-audited. Tests/cases may supplement future retrieval but cannot silently change a normative rule.
