---
id: "algorithm.serialization"
type: "algorithm"
status: "active"
authority: "executable"
title: "Final public serialization and optional Bridge Output"
version: "current"
related_entities: ["algorithm.orderaudit", "algorithm.visibility"]
source_reference: ["06_SOURCE/Code/engine/bridge/trading_pipeline.py", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L1027", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L508", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L718", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L833", "06_SOURCE/Code/engine/bridge/trading_pipeline.py#L979", "06_SOURCE/Code/engine/pipeline/core_utils.py", "06_SOURCE/Code/engine/pipeline/lifecycle_engine.py", "06_SOURCE/Code/engine/pipeline/order_audit_engine.py", "06_SOURCE/Code/engine/pipeline/reaction_engine.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "direction-invariant or explicitly mixed"
implemented_by: ["source.trading_pipeline", "source.order_audit_engine", "source.reaction_engine", "source.lifecycle_engine", "source.core_utils"]
algorithm_reference: ["06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L309", "06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.19_EX1_Source_Synchronized.md#L309"]
mirror_links: ["mirror.contract"]
depends_on: ["algorithm.visibility", "algorithm.orderaudit"]
name: "Serialization"
aliases: ["Bridge Output"]
---

# Final public serialization and optional Bridge Output

## Bullish

#### 13.1 Projection rule

Legacy serialization contains no trading recalculation. Decimal prices are stringified; native local datetimes are converted through the existing Tehran-local epoch contract. Stable source ordering is preserved. Presentation range filtering is applied after full calculation, and OrderAudit may retain a pre-range physical identity when an in-range public behavior references it. `calculationValid` is emitted as `true` for public A/S because invalid calculation objects have already been removed by the calculation/visibility owner.

#### 13.2 Legacy JSON fields

- **Reaction:** `firstIndex`, `firstTime`, `boxTopSourceIndex`, `boxTopSourceTime`, `boxTop`, `boxBottomSourceIndex`, `boxBottomSourceTime`, `boxBottom`, `breakIndex`, `breakTime`, `mode`.
- **Reset:** `index`, `time`, `secondTime`, `brokenLevel`, `fromFirstIndex`.
- **BlueLine:** `direction`, `kind`, `reactionNumber`, `previousStrikeCount`, `strikeCount`, `fibonacciLevel`, `sourceIndex`, `sourceTime`, `sourceExtreme`, `brokenLevel`, `linePrice`, `startTime`, `endTime`.
- **A:** `direction`, `blue1Ordinal`, `blue2Ordinal`, `blue1SourceTime`, `blue2SourceTime`, `blue1StopTime`, `blue2StopTime`, `blue1StopLevel`, `blue2StopLevel`, `continuationLevel`, `continuationSourceIndex`, `continuationSourceTime`, `triggerIndex`, `triggerTime`, `triggerEventTime`, `reactionNumber`, `reactionFirstTime`, `reactionBreakTime`, `sourceIndex`, `sourceTime`, `price`, `calculationValid`.
- **S:** `direction`, `color`, `formationType`, `aOrdinal`, `aSourceIndex`, `aSourceTime`, `aPrice`, `aStopIndex`, `aStopTime`, `aStopEventTime`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `resetReactionNumber`, `resetTime`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`, `calculationValid`.
- **E:** `direction`, `family`, `number`, `parentType`, `parentSourceIndex`, `parentSourceTime`, `parentPrice`, `parentStopIndex`, `parentStopTime`, `parentStopEventTime`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderCauses`, `orderParentStopCauseTime`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`.
- **StopAll:** `direction`, `number`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`, `gateType`, `gateEventTime`, `stoppedBehaviorType`, `stoppedBehaviorKey`, `stoppedBehaviorCount`, `underlyingEFamily`, `underlyingENumber`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderCauses`, `orderParentStopCauseTime`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `stopIndex`, `stopTime`, `stopEventTime`.
- **OrderAudit:** `direction`, `reactionNumber`, `reactionMode`, `firstIndex`, `firstTime`, `boxTopSourceIndex`, `boxTopSourceTime`, `boxTop`, `boxBottomSourceIndex`, `boxBottomSourceTime`, `boxBottom`, `breakIndex`, `breakTime`, `stopLevel`, `stopSourceIndex`, `stopSourceTime`, `stopHitIndex`, `stopHitTime`, `stopHitEventTime`, `causes`.

#### 13.3 Response envelope

The envelope contains `engine`, `version`, `pipelineVersion`, `blueLineVersion`, `aVersion`, `sVersion`, `eVersion`, `stopAllVersion`, enablement booleans, `timeframe`, `actualFrom`, `actualTo`, `directions`, and runtime `timings`. Each requested direction owns its own Reaction/Reset/Blue/A/S/E/StopAll/OrderAudit arrays.

#### 13.4 Optional Bridge Output

`--bridge-output` adds a read-only projection built only from finalized calculation selections and canonical OrderAudit. It may validate a recorded strict event, but it must not search for a substitute trading event or mutate detector/lifecycle state. Physical Order joins use `(FirstIndex, BreakIndex)` and exact accepted causes, never list position.

## Bearish

#### 13.1 Projection rule

Legacy serialization contains no trading recalculation. Decimal prices are stringified; native local datetimes are converted through the existing Tehran-local epoch contract. Stable source ordering is preserved. Presentation range filtering is applied after full calculation, and OrderAudit may retain a pre-range physical identity when an in-range public behavior references it. `calculationValid` is emitted as `true` for public A/S because invalid calculation objects have already been removed by the calculation/visibility owner.

#### 13.2 Legacy JSON fields

- **Reaction:** `firstIndex`, `firstTime`, `boxTopSourceIndex`, `boxTopSourceTime`, `boxTop`, `boxBottomSourceIndex`, `boxBottomSourceTime`, `boxBottom`, `breakIndex`, `breakTime`, `mode`.
- **Reset:** `index`, `time`, `secondTime`, `brokenLevel`, `fromFirstIndex`.
- **BlueLine:** `direction`, `kind`, `reactionNumber`, `previousStrikeCount`, `strikeCount`, `fibonacciLevel`, `sourceIndex`, `sourceTime`, `sourceExtreme`, `brokenLevel`, `linePrice`, `startTime`, `endTime`.
- **A:** `direction`, `blue1Ordinal`, `blue2Ordinal`, `blue1SourceTime`, `blue2SourceTime`, `blue1StopTime`, `blue2StopTime`, `blue1StopLevel`, `blue2StopLevel`, `continuationLevel`, `continuationSourceIndex`, `continuationSourceTime`, `triggerIndex`, `triggerTime`, `triggerEventTime`, `reactionNumber`, `reactionFirstTime`, `reactionBreakTime`, `sourceIndex`, `sourceTime`, `price`, `calculationValid`.
- **S:** `direction`, `color`, `formationType`, `aOrdinal`, `aSourceIndex`, `aSourceTime`, `aPrice`, `aStopIndex`, `aStopTime`, `aStopEventTime`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `resetReactionNumber`, `resetTime`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`, `calculationValid`.
- **E:** `direction`, `family`, `number`, `parentType`, `parentSourceIndex`, `parentSourceTime`, `parentPrice`, `parentStopIndex`, `parentStopTime`, `parentStopEventTime`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderCauses`, `orderParentStopCauseTime`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`.
- **StopAll:** `direction`, `number`, `sourceIndex`, `sourceTime`, `price`, `decisionIndex`, `decisionTime`, `decisionEventTime`, `gateType`, `gateEventTime`, `stoppedBehaviorType`, `stoppedBehaviorKey`, `stoppedBehaviorCount`, `underlyingEFamily`, `underlyingENumber`, `orderDirection`, `orderReactionNumber`, `orderMode`, `orderCauses`, `orderParentStopCauseTime`, `orderFirstIndex`, `orderFirstTime`, `orderBreakIndex`, `orderBreakTime`, `orderConfirmationTime`, `orderBoxTop`, `orderBoxTopSourceIndex`, `orderBoxTopSourceTime`, `orderBoxBottom`, `orderBoxBottomSourceIndex`, `orderBoxBottomSourceTime`, `orderStopLevel`, `orderStopSourceIndex`, `orderStopSourceTime`, `stopIndex`, `stopTime`, `stopEventTime`.
- **OrderAudit:** `direction`, `reactionNumber`, `reactionMode`, `firstIndex`, `firstTime`, `boxTopSourceIndex`, `boxTopSourceTime`, `boxTop`, `boxBottomSourceIndex`, `boxBottomSourceTime`, `boxBottom`, `breakIndex`, `breakTime`, `stopLevel`, `stopSourceIndex`, `stopSourceTime`, `stopHitIndex`, `stopHitTime`, `stopHitEventTime`, `causes`.

#### 13.3 Response envelope

The envelope contains `engine`, `version`, `pipelineVersion`, `blueLineVersion`, `aVersion`, `sVersion`, `eVersion`, `stopAllVersion`, enablement booleans, `timeframe`, `actualFrom`, `actualTo`, `directions`, and runtime `timings`. Each requested direction owns its own Reaction/Reset/Blue/A/S/E/StopAll/OrderAudit arrays.

#### 13.4 Optional Bridge Output

`--bridge-output` adds a read-only projection built only from finalized calculation selections and canonical OrderAudit. It may validate a recorded strict event, but it must not search for a substitute trading event or mutate detector/lifecycle state. Physical Order joins use `(FirstIndex, BreakIndex)` and exact accepted causes, never list position.

## Source-level contract

Native local naive times use Asia/Tehran epoch conversion; optional projection formats full datetimes. Decimal prices stringify,nullables preserve JSON null,arrays preserve finalized ordering. Public calculationValid=true is acceptance outcome.

Reaction/Reset selections are shared by ordinary/optional payloads. Physical Order joins use exact First/Break and accepted causes. _bridge_proven_strict_event checks recorded exact lower row only,not substitute search. Unproven main fallback event stays null. donor_* is internal StopAll projection provenance,not new ordinary public fields. Runtime timings are separate measured values.


## Optional field mapping and cause identity

Optional `bridgeOutput` contains the same eight aligned collection keys as the selected legacy direction payload: `reactions`, `resets`, `blueLines`, `aZones`, `sZones`, `eZones`, `stopAlls`, `orderAudit`. Array alignment is presentation only. Joins use physical `(FirstIndex, BreakIndex)` or behavior `(sourceIndex, sourceTime)` and final accepted causes. Full accepted parent collections are captured before presentation clipping, so a nested historical parent may resolve without being republished as a separate row.

Projection labels are `Bullish`/`Bearish`, `Green`/`Red`/`Blue`, and Mode-A→`LegStart`, Mode-B→`Normal`. Datetimes are full Tehran-local `YYYY-MM-DD HH:MM:SS`, prices are strings and missing facts remain null. The visible upper horizon is the end of the final selected main candle; an exact event must be strictly before that horizon. A recorded event is proven only by a supplied lower row at that exact timestamp satisfying its strict directional price predicate. The projector does not substitute a later/earlier crossing when proof fails.

Reaction projection contains first-candle color/time and top/bottom source time/price plus breakout main time and proven confirmation event. Reset contains occurrence main/event time, prior Reaction First and broken level. Blue projection labels Scale/Reset, exposes formation, line/source extreme and Reset broken level, and deliberately leaves Blue stop time/event null because standalone Blue stop evidence is not retained by final bridge state. A formation maps `ordinary`→`Type-1`, `double-stop`→`Type-2`; it preserves two Blue formation/stops/levels, confirming Reaction, null parent and its own stop/current Order. Blue S maps native `simple`/`advanced`/`type3`/`type4`→`Type-1`/`Type-2`/`Type-3`/`Type-4`; Red S formation is null. S parent is A plus its decisive physical Order. E carries family/number, its source/price, parent S/E/StopAll source identity and its decisive physical Order. StopAll maps `sequence-group-stop`/`stopall-stop`/`opposite-s-group-stop`→`Type-1`/`Type-2`/`Type-3`, keeping immutable constructor donor as parent and keeping donor stop independent of the group gate.

`parent.order` is the selected behavior's recorded decisive physical Order joined to canonical audit identity. `currentOrder` is independent: it requires a proven strict stop of the projected behavior and an accepted creation cause matching the exact behavior source/stop. A `parent-stop` match requires exact parent type/source/event and compatible family. A `reset-leg` match requires exact post behavior source/stop and matching A/S type or the E/StopAll prefixed type. If these causes select exactly one physical audit identity it is projected; zero or multiple distinct identities return null. Neither list position nor a consumed physical Order invents creation rights.

Native chronology APIs are used to obtain Reaction confirmations and first A/S/E stops that are not stored directly in every selected object. Those APIs may perform a lookup or scan of the supplied chronology; projection then validates the returned event at its recorded timestamp. The optional mapper does not create Orders, change lifecycle acceptance or choose an alternative event to replace failed exact proof. Ordinary legacy serializers retain their existing field sets and do not expose internal `donor_*` fields.
