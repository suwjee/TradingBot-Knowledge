---
id: "algorithm.serialization"
type: "algorithm"
status: "canonical"
authority: "normative"
title: "Public serialization"
implemented_by: ["source.trading_pipeline"]
depends_on: ["algorithm.visibility", "algorithm.raw"]
source_refs: ["engine/bridge/trading_pipeline.py#L254", "engine/bridge/trading_pipeline.py#L267", "engine/bridge/trading_pipeline.py#L1130", "engine/bridge/trading_pipeline.py#L1285"]
related_entities: ["test.source_validation"]
source_reference: ["engine/bridge/trading_pipeline.py#L254", "engine/bridge/trading_pipeline.py#L267", "engine/bridge/trading_pipeline.py#L1130", "engine/bridge/trading_pipeline.py#L1285"]
---

# Public serialization

The bridge serializes versioned direction collections after lifecycle and presentation clipping. Decimal prices are strings; datetime wall times are interpreted as Asia/Tehran for epoch output. Preserve physical full-input indexes and nullable fields. Reaction exposes First/Break, box edges/sources, and mode. Reset exposes index/time/secondTime/brokenLevel/fromFirstIndex. Blue exposes kind, strike/Fibonacci and semantic source/line. A/S/E/StopAll expose parent, source/decision, Order provenance, stop, and versioned stage fields.

The bridge also projects behavior views. A public formation maps ordinary/double-stop to Type-1/2 while A remains one behavior. S Blue maps simple/advanced/type3/type4 to Type-1/2/3/4; Red S formation is null. StopAll gate strings map sequence-group-stop/stopall-stop/opposite-s-group-stop to Type-1/2/3. Bridge output and lower-level stage collections should not be conflated. Serialization of current OrderAudit exists but its trading-rule authority is pending-fix; see algorithm.orderaudit.

## Verified public key inventory

The following outer JSON keys were extracted from the current bridge serializer and checked against the synchronized directional references. This inventory preserves exact spelling and field presence. Nested object/null semantics remain in the cited serializer and mirrored code. Current OrderAudit keys are intentionally excluded from normative schema claims because that component is pending-fix.

### Response envelope (trading_pipeline.py L2942)

engine, version, pipelineVersion, blueLineVersion, aVersion, sVersion, eVersion, stopAllVersion, blueLinesEnabled, aEnabled, sEnabled, eEnabled, stopAllEnabled, timeframe, actualFrom, actualTo, directions.

### Reaction (trading_pipeline.py L267)

firstIndex, firstTime, boxTopSourceIndex, boxTopSourceTime, boxTop, boxBottomSourceIndex, boxBottomSourceTime, boxBottom, breakIndex, breakTime, mode.

### Reset (trading_pipeline.py L254)

index, time, secondTime, brokenLevel, fromFirstIndex.

### Blue (trading_pipeline.py L283)

direction, kind, reactionNumber, previousStrikeCount, strikeCount, fibonacciLevel, sourceIndex, sourceTime, sourceExtreme, brokenLevel, linePrice, startTime, endTime.

### A (trading_pipeline.py L303)

direction, blue1Ordinal, blue2Ordinal, blue1SourceTime, blue2SourceTime, blue1StopTime, blue2StopTime, blue1StopLevel, blue2StopLevel, continuationLevel, continuationSourceIndex, continuationSourceTime, triggerIndex, triggerTime, triggerEventTime, reactionNumber, reactionFirstTime, reactionBreakTime, sourceIndex, sourceTime, price, calculationValid.

### S (trading_pipeline.py L330)

direction, color, formationType, aOrdinal, aSourceIndex, aSourceTime, aPrice, aStopIndex, aStopTime, aStopEventTime, orderDirection, orderReactionNumber, orderMode, orderFirstIndex, orderFirstTime, orderBreakIndex, orderBreakTime, orderConfirmationTime, orderBoxTop, orderBoxTopSourceIndex, orderBoxTopSourceTime, orderBoxBottom, orderBoxBottomSourceIndex, orderBoxBottomSourceTime, orderStopLevel, orderStopSourceIndex, orderStopSourceTime, resetReactionNumber, resetTime, sourceIndex, sourceTime, price, decisionIndex, decisionTime, decisionEventTime, calculationValid.

### E (trading_pipeline.py L395)

direction, family, number, parentType, parentSourceIndex, parentSourceTime, parentPrice, parentStopIndex, parentStopTime, parentStopEventTime, orderDirection, orderReactionNumber, orderMode, orderCauses, orderParentStopCauseTime, orderResetLegResetTime, orderResetLegBreakTime, orderFirstIndex, orderFirstTime, orderBreakIndex, orderBreakTime, orderConfirmationTime, orderBoxTop, orderBoxTopSourceIndex, orderBoxTopSourceTime, orderBoxBottom, orderBoxBottomSourceIndex, orderBoxBottomSourceTime, orderStopLevel, orderStopSourceIndex, orderStopSourceTime, sourceIndex, sourceTime, price, decisionIndex, decisionTime, decisionEventTime.

### StopAll (trading_pipeline.py L446)

direction, number, sourceIndex, sourceTime, price, decisionIndex, decisionTime, decisionEventTime, gateType, gateEventTime, stoppedBehaviorType, stoppedBehaviorKey, stoppedBehaviorCount, underlyingEFamily, underlyingENumber, orderDirection, orderReactionNumber, orderMode, orderCauses, orderParentStopCauseTime, orderResetLegResetTime, orderResetLegBreakTime, orderFirstIndex, orderFirstTime, orderBreakIndex, orderBreakTime, orderConfirmationTime, orderBoxTop, orderBoxTopSourceIndex, orderBoxTopSourceTime, orderBoxBottom, orderBoxBottomSourceIndex, orderBoxBottomSourceTime, orderStopLevel, orderStopSourceIndex, orderStopSourceTime, stopIndex, stopTime, stopEventTime.

### Bridge A (trading_pipeline.py L1040)

type, direction, formation, formedAt, blueLines, reaction, parent, currentOrder, stop.

### Bridge S (trading_pipeline.py L1130)

type, direction, color, formation, formedAt, parent, currentOrder, stop.

### Bridge E (trading_pipeline.py L1238)

type, direction, color, number, formedAt, parent, currentOrder, stop.

### Bridge StopAll (trading_pipeline.py L1285)

type, direction, number, formation, formedAt, parent, currentOrder, stop.

The response envelope also adds timings (phasesMs and bridgeTotalMs) after direction serialization. The direction payload contains reactions, resets, blueLines, aZones, sZones, eZones, stopAlls, orderAudit, and optional bridgeOutput. orderAudit is executable output only and remains non-canonical for trading-rule reasoning.

