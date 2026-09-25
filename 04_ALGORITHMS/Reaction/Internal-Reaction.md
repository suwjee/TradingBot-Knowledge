---
id: "algorithm.internal_reaction"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Internal Reaction"
implemented_by: ["source.reaction_engine"]
depends_on: ["algorithm.reaction"]
source_refs: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1202"]
related_entities: ["test.source_validation", "mirror.exceptions", "test.direction_tests"]
source_reference: ["06_SOURCE/Code/engine/pipeline/reaction_engine.py#L1202"]
---

# Internal Reaction

## Calculation logic

After both directional streams exist, classify a Reaction internal only when its First is strictly after an opposite Reaction First; its confirmation is no later than the opposite confirmation; its published box lies inside the opposite published box; and every lower event from inner First through confirmation remains inside that outer box.


## Contract interface

- **Purpose:** Classify source-grounded nested cross-direction Reactions.
- **Inputs:** Both directional Reaction streams, published boxes and exact lower chronology.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Internal classification and downstream visibility eligibility evidence.
- **Source ownership:** source.reaction_engine.
- **Validation relationship:** test.direction_tests; test.source_validation checks the line anchors and owner.
