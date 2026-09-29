---
id: "source.direction_policy"
type: "source"
status: "active"
authority: "executable"
title: "Shared direction-sensitive geometry, strict comparisons, extrema and confirmation"
version: "1.0.0"
related_entities: ["source.source_manifest"]
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
source_path: "06_SOURCE/Code/engine/pipeline/direction_policy.py"
mirror: "06_SOURCE/Code/engine/pipeline/direction_policy.py"
sha256: "a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea"
---

# direction_policy.py

Shared direction-sensitive geometry, strict comparisons, extrema and confirmation.

Current working-tree bytes are executable evidence; Source identity alone is not independent market correctness. The supported bridge dynamically loads owners; the legacy ordinary package wrapper is unsupported.

| Property | Current value |
|---|---|
| Source | 06_SOURCE/Code/engine/pipeline/direction_policy.py |
| SHA-256 | a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea |
| Bytes | 2282 |
| Lines | 70 |
| Declared version | 1.0.0 |

## Current symbols

Every lexical class/function is listed, including nested definitions inside control blocks. Qualified name plus source line identifies repeated property accessors.

| Symbol | Source line | End line | Signature or role |
|---|---:|---:|---|
| DirectionPolicy | 21 | 46 | class |
| DirectionPolicy.opposite_direction | 29 | 30 | self |
| DirectionPolicy.strict_cross | 32 | 33 | self, value: Decimal, level: Decimal |
| DirectionPolicy.better_extreme | 35 | 36 | self, value: Decimal, current: Decimal |
| DirectionPolicy.choose_extreme | 38 | 39 | self, left: Decimal, right: Decimal |
| DirectionPolicy.confirmation_cross | 41 | 46 | self, value: Decimal, level: Decimal |
| policy_for | 49 | 54 | direction: str |
