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
---

# Current source validation method

Compare every manifest entry to exact local snapshot bytes and then to its current Production origin. Check SHA-256, byte count, line count, actual version constants and complete inventory. Parse and compile Python in memory to avoid writing Production caches. Use the normal dynamic bridge loading path to check functional imports. Unsupported flat package imports are reported separately from the successful production entry path. Extract both raw Reference embedded blocks and compare all 13 current Python copies per direction byte-for-byte before claiming synchronization.
