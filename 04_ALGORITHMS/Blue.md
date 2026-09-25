---
id: "algorithm.blue"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Blue Line"
implemented_by: ["source.blue_line_detector"]
depends_on: ["algorithm.reaction", "algorithm.reset", "market.direction"]
source_refs: ["engine/pipeline/blue_line_detector.py#L75", "engine/pipeline/blue_line_detector.py#L139", "engine/pipeline/blue_line_detector.py#L299"]
related_entities: ["test.source_validation"]
source_reference: ["engine/pipeline/blue_line_detector.py#L75", "engine/pipeline/blue_line_detector.py#L139", "engine/pipeline/blue_line_detector.py#L299"]
---

# Blue Line

For each Reaction, compute F=Top-0.618*(Top-reference) Bullish, Bottom+0.618*(reference-Bottom) Bearish. From First through Break inclusive, a new pending Scale strike requires strictly better Low/min Bullish or High/max Bearish than the last confirmed strike or F. A better value replaces pending. GREEN Bullish or RED Bearish main candle confirms; a Break-pending strike may confirm intrabar before strict Reaction confirmation.

Emit Scale Blue when current confirmed strike count exceeds previous Reaction's and spacing permits: no prior Blue or at least one healthy Reaction since it. Source is decisive last strike. Drawing line is Bullish Low+range/3 or Bearish High-range/3; semantic stop uses sourceExtreme, not linePrice. A Reset may emit Reset Blue under the same spacing rule, line offset /5, source at Reset main candle, brokenLevel from Reset.

A Reset Blue is calculation-invalid for the special double-stop condition when the previous Blue first stops on the same Reset index and that candle strictly crosses its sourceExtreme. It remains structural evidence for special A. Internal Blue remains calculation evidence but public output requires calculation_valid and not behavior_internal.
