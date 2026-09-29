---
id: "workflow.release"
type: "workflow"
status: "active"
authority: "executable"
title: "Release an authorized current change"
version: "current"
related_entities: ["workflow.operating"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Release an authorized current change

Require all applicable checks to complete, synchronize both current References and changed Source identities, review the intentional diff and preserve unrelated dirty work. Package all release-relevant changed artifacts and root readme.txt with previous/current versions, full timestamp to seconds, timezone, change class and actual regression status. Do not claim readiness when mandatory evidence is failed or incomplete. Push/publication requires explicit current-task authorization.
