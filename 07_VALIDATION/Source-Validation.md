---
id: "test.source_validation"
type: "test"
status: "active"
authority: "executable"
title: "Current source validation method"
version: "current"
related_entities: ["source.reference_registry", "source.source_manifest"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
last_modified_at: "2026-10-27T20:15:57+03:30"
---
# Current source validation method

Compare every manifest entry to exact local snapshot bytes and then to its current Production origin. Check SHA-256, byte count, line count, actual version constants and complete inventory. Parse and compile Python in memory to avoid writing Production caches. Use the normal dynamic bridge loading path to check functional imports. The maintained engine.pipeline wrapper now establishes its sibling-import path; test that compatibility surface separately from supported dynamic bridge loading. Extract both raw Reference embedded blocks and compare every in-scope captured module byte-for-byte. Declared embedded-only exclusions must match their dedicated hash/byte pins and remain explicitly outside standalone reconstruction/semantic coverage.
