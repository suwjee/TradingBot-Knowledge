# Current Phase-1 Vault and Plugin validation

Captured: 2026-09-29 12:52:09 +0330 (Asia/Tehran)

Phase: 2026-09-29 current Source/Reference/Vault/Plugin audit. Engine Source Modified: NO. Reference Bytes Modified: NO. Source semantics were inspected, not executed. This report replaces the previous phase report; old Engine repairs or market checks are not evidence for this phase.

| Check | Actual result |
| --- | --- |
| Current protected Source | 13/13 baseline hashes and captured mirrors exact; safe compilation PASS |
| Complete semantic inspection | 346 functions; 383 class/function units covered; STATIC_REVIEW_ONLY |
| Both current References | 5.4.19-EX1; independent reconstruction 13/13 each; exact bytes |
| Reference narrative agreement | Four disclosed conditional/scope discrepancies; no intended-rule resolution |
| Vault | 119 entities, 453 relations; 33 schema tests PASS |
| Generation | Two independent seven-output generations and --check byte-identical |
| Plugin | 0.3.8; 104 discovered, 103 passed, 0 failed, 1 environment skip |
| Actual MCP | 604 successful calls; eight tools; zero Vault byte mutations |
| Operational | Editable and official 25-file package; local/external modes; four ready=true doctors |
| Protected mutation | Final boundary is recorded in the external final-snapshot.json and verification.json |
| RAW / fixtures / market regression | NOT_REQUIRED_THIS_PHASE; stores EMPTY_BY_DESIGN |

| Category | Command | Tests | Passed | Failed | Skipped | Exit Code | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| unit | python -B -m unittest discover -s tests/unit -t . -v | 73 | 73 | 0 | 0 | 0 | PASS |
| contract | python -B -m unittest discover -s tests/contract -t . -v | 5 | 5 | 0 | 0 | 0 | PASS |
| security | python -B -m unittest discover -s tests/security -t . -v | 11 | 10 | 0 | 1 | 0 | PASS |
| integration | python -B -m unittest discover -s tests/integration -t . -v | 9 | 9 | 0 | 0 | 0 | PASS |
| mcp | python -B -m unittest discover -s tests/mcp -t . -v | 3 | 3 | 0 | 0 | 0 | PASS |
| operational | python -B -m unittest discover -s tests/operational -t . -v | 3 | 3 | 0 | 0 | 0 | PASS |
| full | python -B -m unittest discover -s tests -t . -v | 104 | 103 | 0 | 1 | 0 | PASS |
| schema | python -B -m unittest discover -s _SCHEMA/tests -v | 33 | 33 | 0 | 0 | 0 | PASS |

Plugin categories run from `D:\My-Projects\TradingBot-Intelligence-Plugin`; schema from `D:\My-Projects\TradingBot-Knowledge`. The exact executable is `C:\Users\msadr\AppData\Local\Python\pythoncore-3.14-64\python.exe`. Process-only dependency path: `C:\Users\msadr\.codex\scratch\tradingbot-end-to-end-20260928\release-runtime`. Category rows are subsets of the full Plugin run, not additional unique tests. The combined unique Plugin/schema result is 137 discovered, 136 passed, 0 failed, 1 skipped. The final Behavior wording clarification was followed by a fresh 9-test real-root integration run and 19 real MCP calls; it changed no Plugin runtime or schema code.

PASS for traversal/absolute/drive/UNC rejection, allowed-root checks before protected reads, Source-ID and path currentness, registered Reference provenance, indexed-note byte identity, strict JSON/schema/manifest integrity, alias collision rejection, relation-neighbor evidence validation, declared current entity contracts, canonical external Engine mappings, a real Windows Source junction and a real bootstrap _INDEX junction/canary. The existing file-symlink test skipped because Windows returned WinError 1314; it was not weakened or disabled. There is no claim about arbitrary concurrent filesystem races or cryptographic authentication of a completely replaced coordinated Vault. These are outside the declared unsigned local evidence contract.

Final reports and post-assembly archive integrity are under `C:\Users\msadr\.codex\artifacts\tradingbot-vault-plugin-phase1-20260929`. No Git reset/clean/stash/stage/commit/push, Graphify execution, install-cache mutation or trading calculation occurred.
