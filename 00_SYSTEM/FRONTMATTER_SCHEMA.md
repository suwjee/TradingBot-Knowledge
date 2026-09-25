---
id: "system.frontmatter"
type: "system"
status: "canonical"
authority: "normative"
title: "Frontmatter schema"
---

# Frontmatter schema

Every populated note has id, type, status, authority, title. Typed relations use arrays of IDs. source_refs is an array of repository-relative path#line strings. Behavior notes use calculated_by and implemented_by; algorithm notes use produces, depends_on, and implemented_by; source notes use path and implements. A pending-fix note may link executable source but must not have normative authority.

The frontmatter is restricted to JSON scalar or JSON-array values in YAML-compatible key: value lines. This supports deterministic parsing without implicit YAML types. The machine schemas in _SCHEMA constrain required fields and enums. Indexes are generated from frontmatter; handwritten index changes are discarded.
