---
id: "algorithm.blue"
type: "algorithm"
status: "pending"
authority: "non-canonical"
title: "Blue Line"
implemented_by: ["source.blue_line_detector"]
depends_on: ["algorithm.reaction", "algorithm.reset", "market.direction"]
source_refs: ["06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L75", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L139", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L299"]
related_entities: ["test.source_validation", "test.precision_invariants"]
source_reference: ["06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L75", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L139", "06_SOURCE/Code/engine/pipeline/blue_line_detector.py#L299"]
---

# Blue Line

## Calculation logic

For each Reaction, compute F=Top-0.618*(Top-reference) Bullish, Bottom+0.618*(reference-Bottom) Bearish. From First through Break inclusive, a new pending Scale strike requires strictly better Low/min Bullish or High/max Bearish than the last confirmed strike or F. A better value replaces pending. GREEN Bullish or RED Bearish main candle confirms; a Break-pending strike may confirm intrabar before strict Reaction confirmation.

Emit Scale Blue when current confirmed strike count exceeds previous Reaction's and spacing permits: no prior Blue or at least one healthy Reaction since it. Source is decisive last strike. Drawing line is Bullish Low+range/3 or Bearish High-range/3; semantic stop uses sourceExtreme, not linePrice. A Reset may emit Reset Blue under the same spacing rule, line offset /5, source at Reset main candle, brokenLevel from Reset.

A Reset Blue is calculation-invalid for the special double-stop condition when the previous Blue first stops on the same Reset index and that candle strictly crosses its sourceExtreme. It remains structural evidence for special A. Internal Blue remains calculation evidence but public output requires calculation_valid and not behavior_internal.

## Contract interface

- **Purpose:** Calculate directional Scale and Reset Blue lines.
- **Inputs:** Reaction box and First/Break, Reset event, strict lower extrema and Decimal prices.
- **Calculation logic:** The source-grounded rule and its exact ordering are stated above.
- **Output:** Calculation-valid and public Blue states with formation, level, source and stop.
- **Source ownership:** source.blue_line_detector.
- **Validation relationship:** test.precision_invariants; test.source_validation checks the line anchors and owner.
