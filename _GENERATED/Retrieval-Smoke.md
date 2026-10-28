# Current retrieval validation

Verified 2026-10-28T18:17:57+03:30 using installed Plugin 0.3.9 against the refreshed Vault.

Status: PASS for a freshly started installed MCP process. Doctor initialized the connection, listed and called all eight tools: search_knowledge, get_knowledge, trace_relations, get_dataset, get_raw_window, read_source_evidence, read_algorithm_reference_evidence and verify_vault. Dataset/window calls returned the expected ENTITY_NOT_FOUND for EMPTY_BY_DESIGN stores; the other tools succeeded.

The 109-test full Plugin suite passed with one unavailable Windows symlink-privilege skip. It exercised current canonical Order metadata, alias/relation/source linkage, exact local References, configured external Engine cross-check, read-only public operations, fresh review-state/scope metadata, supported pinned text formats, malformed/tampered evidence and containment. LF/CRLF note handling now normalizes retrieved text only after physical hash and byte validation. Actual Windows junction tests passed.

Additional fresh installed-MCP get_knowledge calls retrieved version.current=5.4.33, source.reference_consistency with REF-REACTION-SUCCESSOR and its warning, and workflow.project_release. All reported reviewed-scoped-with-disclosed-ambiguity. These facts do not resolve the narrative ambiguity or prove market correctness.

Host limitation: the existing chat's already-bound old 0.3.8 process still rejects CRLF and has not hot-reloaded. Its direct retrieval failure is not relabeled PASS. Start a new chat to load the installed 0.3.9 runtime and skill definitions. Installed-byte comparison (25 files), fresh runtime doctor and fresh MCP retrieval passed independently. No installed cache file was manually patched.
