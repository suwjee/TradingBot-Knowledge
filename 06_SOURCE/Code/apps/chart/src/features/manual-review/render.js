// Presentation-only review pieces for the served /info page. Behavior
// identities, prices and orders come exclusively from the supplied bridge
// payload, never chart inference. The page is generated fresh per export;
// no file is written and no candle cache is serialized.
import { PRIMARY_VISUAL_DEFAULTS, primaryMarkerLayout, primaryObjectId } from "../../chart/primary-structure.js";

const collections = {
  reactions: ["Reaction", "firstTime"], resets: ["Reset", "time"],
  blueLines: ["Blue Line", "sourceTime"], aZones: ["A", "sourceTime"],
  sZones: ["S", "sourceTime"], eZones: ["E", "sourceTime"],
  stopAlls: ["StopAll", "sourceTime"], orderReactions: ["Order reaction", "firstTime"],
  orderAudit: ["Order Audit", "firstTime"],
  primaryHighs: ["PH", "sourceTime"], primaryLows: ["PL", "sourceTime"],
  matchingBehaviorLegs: ["MBL", "sourceTime"],
};
const primaryKinds = { primaryHighs: "PH", primaryLows: "PL", matchingBehaviorLegs: "MBL" };
const primaryFamilies = new Set(Object.values(primaryKinds));
const defaultHiddenFamilies = new Set(["Reaction", "Reset", "Blue Line"]);
const primaryFamily = (family) => primaryKinds[family] || family;
const behaviorNumber = (value) => value != null && value !== "" && Number.isInteger(Number(value)) && Number(value) >= 0 ? Number(value) : null;
const numberedLabel = (family, number) => {
  if (number == null || family === "MBL") return family;
  return `${family}-${number}`;
};
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g,
  (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
const tehran = new Intl.DateTimeFormat("en-CA", {
  timeZone: "Asia/Tehran", year: "numeric", month: "2-digit", day: "2-digit",
  hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23",
});
export function reviewTime(epoch) {
  if (typeof epoch !== "number" || !Number.isFinite(epoch)) return "Undated";
  const parts = Object.fromEntries(tehran.formatToParts(new Date(epoch * 1000)).map((p) => [p.type, p.value]));
  return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}:${parts.second}`;
}
function labelFor(group, row) {
  return numberedLabel(collections[group]?.[0] || group, behaviorNumber(row.number));
}
function bridgeProjection(groups, group, index) {
  const projected = groups?.bridgeOutput?.[group]?.[index];
  return projected && typeof projected === "object" && !Array.isArray(projected) ? projected : null;
}
const filterToken = (value) => String(value).trim().toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const bridgeText = (value) => typeof value === "string" && value.trim() ? value.trim() : null;
const bridgeColorKey = (group, value) => `${group}:${String(value).toLowerCase()}`;
const bridgeChildCategory = (baseKey, family, label, colorKey = baseKey) => ({
  key: `${baseKey}:${filterToken(label)}`, family, label, colorKey,
});
function orderAuditFormation(projected) {
  const explicit = bridgeText(projected.formation);
  if (explicit) return explicit;
  const kinds = new Set(Array.isArray(projected.causes)
    ? projected.causes.map((cause) => cause?.kind)
    : []);
  const formations = [];
  if (kinds.has("parent-stop")) formations.push("Order_A");
  if (kinds.has("reset-leg")) formations.push("Order_B");
  return formations.length ? formations.join(" | ") : null;
}

// This is deliberately a display-only lookup: the finalized legacy row and
// its same-position bridge projection were constructed together by the bridge.
// It never establishes a behavior or Order identity from that position.
function bridgeCategory(group, row, direction, projected) {
  if (!projected) return null;
  if (group === "reactions") {
    const mode = projected.mode === "Leg Start" ? "Reset leg" : bridgeText(projected.mode);
    return mode ? bridgeChildCategory(`${group}:${direction}`, "Reaction", mode, `${group}:${direction}`) : null;
  }
  if (group === "sZones") {
    const color = bridgeText(projected.color)?.toLowerCase();
    if (color !== "blue" && color !== "red") return null;
    const formation = color === "red" ? "Simple" : bridgeText(projected.formation);
    return formation ? bridgeChildCategory(bridgeColorKey(group, color), `S ${color[0].toUpperCase()}${color.slice(1)}`, formation, bridgeColorKey(group, color)) : null;
  }
  if (group === "eZones") {
    const color = bridgeText(projected.color)?.toLowerCase();
    const number = Number.isInteger(projected.number) ? projected.number : null;
    if ((color !== "blue" && color !== "red") || number == null) return null;
    return bridgeChildCategory(bridgeColorKey(group, color), `E ${color[0].toUpperCase()}${color.slice(1)}`, `E${number}`, bridgeColorKey(group, color));
  }
  if (["blueLines", "aZones", "stopAlls"].includes(group)) {
    const formation = bridgeText(projected.formation);
    const family = collections[group]?.[0] || group;
    return formation ? bridgeChildCategory(group, family, formation) : null;
  }
  if (group === "orderAudit") {
    const formation = orderAuditFormation(projected);
    return formation ? bridgeChildCategory(group, "Order Audit", formation) : null;
  }
  return null;
}

export function reviewCategory(group, row, direction, projected = null) {
  const category = bridgeCategory(group, row, direction, projected);
  if (category) return category;
  if (group === "reactions") return { key: `${group}:${direction}`, family: "Reaction", label: `${direction === "bullish" ? "Bullish" : "Bearish"} Reaction` };
  if (group === "sZones" || group === "eZones") {
    const family = (group === "sZones" ? row?.color : row?.family) || "unknown";
    const familyLabel = `${group === "sZones" ? "S" : "E"} ${String(family).replace(/^./, (value) => value.toUpperCase())}`;
    return { key: `${group}:${family}`, family: familyLabel, label: group === "sZones" ? "S" : "E" };
  }
  const family = collections[group]?.[0] || group;
  return { key: group, family, label: family };
}
const colorSpec = {
  "reactions:bullish": ["bullBorder", "#15803d"], "reactions:bearish": ["bearBorder", "#dc2626"],
  "reaction:bullish": ["bullBorder", "#15803d"], "reaction:bearish": ["bearBorder", "#dc2626"],
  resets: ["resetColor", "#7c2d12"], blueLines: ["blueLineColor", "#0891b2"], aZones: ["aColor", "#7e22ce"],
  "sZones:blue": ["sBullColor", "#2563eb"], "sZones:red": ["sBearColor", "#be123c"],
  "eZones:blue": ["eBlueColor", "#1e3a8a"], "eZones:red": ["eRedColor", "#7f1d1d"],
  stopAlls: ["stopAllBorder", "#ff9800"], orderReactions: ["orderColor", "#111111"], orderAudit: ["orderColor", "#111111"],
};
const objectKinds = { reactions: "reaction", blueLines: "blue", aZones: "a", sZones: "s", eZones: "e", stopAlls: "stopall" };
const safeColor = (value) => typeof value === "string" && /^#[0-9a-f]{6}$/i.test(value);
export function reviewColor(record, snapshot = {}, objects = new Map((snapshot.indicatorObjects || []).map((item) => [item.id, item]))) {
  const kind = primaryKinds[record.group] || (primaryFamilies.has(record.category.family) ? record.category.family : null);
  if (kind) {
    const direction = String(record.direction || record.row?.direction || "bearish").toLowerCase();
    const object = objects.get(primaryObjectId(direction, kind, record.row || {}));
    const chartColor = kind === "MBL" ? snapshot.settings?.mblColor || PRIMARY_VISUAL_DEFAULTS.mblColor
      : primaryMarkerLayout(kind, direction, 0, 0, snapshot.settings).color;
    const chosen = object?.customized ? object.color : chartColor;
    return safeColor(chosen) ? chosen : kind === "MBL" ? PRIMARY_VISUAL_DEFAULTS.mblColor
      : primaryMarkerLayout(kind, direction, 0, 0).color;
  }
  const [setting, fallback] = colorSpec[record.category.colorKey || record.category.key] || ["", "#475569"];
  const object = objects.get(`indicator:${record.direction}:${objectKinds[record.group]}:${record.index}`);
  const chosen = object?.customized ? object.color : snapshot.settings?.[setting];
  return safeColor(chosen) ? chosen : fallback;
}
// Label boxes stay neutral; behavior identity is carried by the exact chart
// foreground color. Reactions and order records deliberately use black text.
export function reviewColorSurface() { return "#f3f5f7"; }
export function reviewLabelColor(record, chartColor) {
  return ["reactions", "orderReactions", "orderAudit"].includes(record.group)
    ? "#111827" : chartColor;
}
export function manualReviewFilename(date = new Date(), extension = "txt") {
  const two = (value) => String(value).padStart(2, "0");
  return `info-${date.getFullYear()}_${two(date.getMonth() + 1)}_${two(date.getDate())} ${two(date.getHours())}_${two(date.getMinutes())}_${two(date.getSeconds())}.${extension}`;
}
export function reviewRecords(payload) {
  if (Array.isArray(payload?.report)) {
    return payload.report.flatMap((item, index) => {
      const details = item?.details && typeof item.details === "object" ? item.details : {};
      const originalFamily = item?.category?.family || details.type || "Report";
      if (originalFamily === "primaryCycles" || item?.group === "primaryCycles") return [];
      const family = primaryFamily(originalFamily);
      return {
        id: String(item.id || `report:${index}`),
        direction: item.direction || details.direction || "",
        group: family,
        row: details,
        index,
        category: item.category ? { ...item.category, family,
          label: originalFamily !== family && (!item.category.label || item.category.label === originalFamily)
            ? family : item.category.label }
          : { key: family, family, label: item.label || family },
        epoch: item.time,
        time: item.time || "Undated",
        label: item.label || family,
        reportDetails: details,
      };
    }).sort((a, b) => String(a.time).localeCompare(String(b.time)) || a.id.localeCompare(b.id));
  }
  const records = [];
  for (const [direction, groups] of Object.entries(payload.directions || {})) {
    for (const [group, rows] of Object.entries(groups)) {
      if (!Array.isArray(rows) || group === "primaryCycles") continue;
      rows.forEach((row, index) => {
        const epoch = row?.[collections[group]?.[1] || "sourceTime"];
        records.push({ id: `${direction}:${group}:${index}`, direction, group, row, index, groups,
          category: reviewCategory(group, row, direction, bridgeProjection(groups, group, index)),
          epoch, time: reviewTime(epoch), label: labelFor(group, row || {}) });
      });
    }
  }
  return records.sort((a, b) => (a.epoch ?? Infinity) - (b.epoch ?? Infinity));
}

// Bulk review actions are intentionally scoped to one Tehran calendar day.
// A filtered-out record is never changed by a day action.
export function reviewTimeGroup(time) {
  return time === "Undated" ? "Undated" : String(time || "Undated").slice(0, 10);
}

export function visibleReviewTimeGroupIds(records, timeGroup) {
  return records
    .filter((record) => record?.timeGroup === timeGroup && !record.hidden)
    .map((record) => record.id);
}

const readableDirection = (value) => value === "bullish" ? "Bullish" : value === "bearish" ? "Bearish" : value;
const readableMode = (value) => value === "A" ? "Leg start" : value === "B" ? "Normal" : value;
const readableKind = (value) => ({
  scale: "Scale", reset: "Reset", simple: "Simple", advanced: "Advanced", type3: "Type 3",
  "parent-stop": "Parent stop", "reset-leg": "Reset leg", "carried-live": "Carried live",
  "sequence-group-stop": "Sequence group stop", "stopall-stop": "StopAll stop",
  Order_A: "Parent stop", Order_B: "Reset leg",
})[value] || value;
const timeValue = (value) => typeof value === "number" && Number.isFinite(value)
  ? { time: reviewTime(value) }
  : undefined;
const removeUndefined = (value) => {
  const output = {};
  for (const [key, item] of Object.entries(value)) {
    if (item === undefined) continue;
    if (Array.isArray(item)) {
      const values = item.map((entry) => entry && typeof entry === "object" && !Array.isArray(entry) ? removeUndefined(entry) : entry)
        .filter((entry) => entry !== undefined);
      if (values.length) output[key] = values;
      continue;
    }
    if (item && typeof item === "object") {
      const nested = removeUndefined(item);
      if (Object.keys(nested).length) output[key] = nested;
      continue;
    }
    output[key] = item;
  }
  return output;
};
const pricePoint = (price, time) => removeUndefined({
  time: typeof time === "number" && Number.isFinite(time) ? reviewTime(time) : undefined,
  price,
});
const stopPoint = (price, time) => typeof time === "number" && Number.isFinite(time)
  ? pricePoint(price, time)
  : undefined;
const causeObject = (cause) => {
  if (typeof cause === "string") return readableKind(cause);
  if (!cause || typeof cause !== "object") return cause;
  if (cause.kind === "parent-stop") return removeUndefined({
    kind: readableKind(cause.kind),
    parentType: cause.parentType,
    parentFamily: cause.parentFamily,
    parentFormedAt: timeValue(cause.parentSourceTime),
    parentStoppedAt: timeValue(cause.eventTime),
  });
  if (cause.kind === "reset-leg") return removeUndefined({
    kind: readableKind(cause.kind),
    resetAt: timeValue(cause.resetTime),
    boundaryBrokenAt: timeValue(cause.boundaryBreakTime),
  });
  return removeUndefined({ kind: readableKind(cause.kind) });
};
function orderObject(row) {
  if (row.orderFirstTime == null && row.orderBreakTime == null && row.orderStopLevel == null) return undefined;
  const causes = Array.isArray(row.orderCauses) ? row.orderCauses.map(causeObject) : undefined;
  return removeUndefined({
    direction: readableDirection(row.orderDirection),
    mode: readableMode(row.orderMode),
    causes,
    startedAt: timeValue(row.orderFirstTime),
    confirmedAt: timeValue(row.orderConfirmationTime ?? row.orderBreakTime),
    structure: removeUndefined({
      boxTop: pricePoint(row.orderBoxTop, row.orderBoxTopSourceTime),
      boxBottom: pricePoint(row.orderBoxBottom, row.orderBoxBottomSourceTime),
    }),
    stop: pricePoint(row.orderStopLevel, row.orderStopSourceTime),
    causeEvidence: removeUndefined({
      parentStoppedAt: timeValue(row.orderParentStopCauseTime),
      resetAt: timeValue(row.orderResetLegResetTime),
      boundaryBrokenAt: timeValue(row.orderResetLegBreakTime),
    }),
  });
}

// Create a human-readable, review-only projection. The supplied bridge row is
// never mutated and remains authoritative for chart rendering/calculation.
export function manualInfoObject(record) {
  if (record?.reportDetails && typeof record.reportDetails === "object") return record.reportDetails;
  const { group, index, row = {}, direction, groups = {} } = record;
  const projected = bridgeProjection(groups, group, index);
  if (projected) return projected;
  const base = { type: collections[group]?.[0] || group, direction: readableDirection(direction) };
  if (primaryKinds[group]) return { ...row, ...base };
  if (group === "reactions") return removeUndefined({
    ...base,
    mode: readableMode(row.mode),
    startedAt: timeValue(row.firstTime),
    structure: {
      boxTop: pricePoint(row.boxTop, row.boxTopSourceTime),
      boxBottom: pricePoint(row.boxBottom, row.boxBottomSourceTime),
    },
    confirmedAt: timeValue(row.breakTime),
  });
  if (group === "resets") {
    const owner = (groups.reactions || []).find((reaction) => reaction.firstIndex === row.fromFirstIndex);
    return removeUndefined({
      ...base,
      occurredAt: timeValue(row.secondTime ?? row.time),
      mainCandleAt: timeValue(row.time),
      brokenLevel: row.brokenLevel,
      reactionStartedAt: timeValue(owner?.firstTime),
    });
  }
  if (group === "blueLines") return removeUndefined({
    ...base,
    formation: readableKind(row.kind),
    formedAt: timeValue(row.sourceTime),
    line: removeUndefined({ price: row.linePrice, sourceExtreme: row.sourceExtreme }),
    stop: pricePoint(row.sourceExtreme, row.endTime),
  });
  if (group === "aZones") return removeUndefined({
    ...base,
    formedAt: timeValue(row.sourceTime),
    price: row.price,
    blueLines: {
      first: removeUndefined({ formedAt: timeValue(row.blue1SourceTime), stoppedAt: timeValue(row.blue1StopTime), stopLevel: row.blue1StopLevel }),
      second: removeUndefined({ formedAt: timeValue(row.blue2SourceTime), stoppedAt: timeValue(row.blue2StopTime), stopLevel: row.blue2StopLevel }),
    },
    continuation: pricePoint(row.continuationLevel, row.continuationSourceTime),
    triggeredAt: timeValue(row.triggerEventTime ?? row.triggerTime),
    reaction: removeUndefined({
      startedAt: timeValue(row.reactionFirstTime),
      confirmedAt: timeValue(row.reactionBreakTime),
    }),
    stop: stopPoint(row.price, (groups.sZones || []).find((item) => item.aSourceTime === row.sourceTime)?.aStopEventTime),
  });
  if (group === "sZones") return removeUndefined({
    ...base,
    color: row.color === "blue" ? "Blue" : row.color === "red" ? "Red" : row.color,
    formation: readableKind(row.formationType),
    formedAt: timeValue(row.sourceTime),
    price: row.price,
    parentA: removeUndefined({
      formedAt: timeValue(row.aSourceTime),
      price: row.aPrice,
      stoppedAt: timeValue(row.aStopEventTime ?? row.aStopTime),
    }),
    reset: row.formationType === "type3" ? timeValue(row.resetTime) : undefined,
    order: orderObject(row),
    decisionAt: timeValue(row.decisionEventTime ?? row.decisionTime),
    stop: stopPoint(row.price, (groups.eZones || []).find((item) => item.parentSourceTime === row.sourceTime)?.parentStopEventTime),
  });
  if (group === "eZones") return removeUndefined({
    ...base,
    family: row.family === "blue" ? "Blue" : row.family === "red" ? "Red" : row.family,
    formedAt: timeValue(row.sourceTime),
    price: row.price,
    parent: removeUndefined({
      type: row.parentType,
      formedAt: timeValue(row.parentSourceTime),
      price: row.parentPrice,
      stoppedAt: timeValue(row.parentStopEventTime ?? row.parentStopTime),
    }),
    order: orderObject(row),
    decisionAt: timeValue(row.decisionEventTime ?? row.decisionTime),
    stop: stopPoint(row.price, (groups.stopAlls || []).find((item) => item.underlyingEFamily === row.family && item.underlyingENumber === row.number)?.gateEventTime),
  });
  if (group === "stopAlls") return removeUndefined({
    ...base,
    formedAt: timeValue(row.sourceTime),
    price: row.price,
    gate: removeUndefined({
      type: readableKind(row.gateType),
      time: timeValue(row.gateEventTime),
      stopped: removeUndefined({
        type: row.stoppedBehaviorType,
        group: row.stoppedBehaviorKey,
        count: row.stoppedBehaviorCount,
      }),
    }),
    sourceE: removeUndefined({ family: row.underlyingEFamily }),
    order: orderObject(row),
    decisionAt: timeValue(row.decisionEventTime ?? row.decisionTime),
    stop: timeValue(row.stopEventTime ?? row.stopTime),
  });
  if (group === "orderAudit") return removeUndefined({
    ...base,
    mode: readableMode(row.reactionMode),
    startedAt: timeValue(row.firstTime),
    confirmedAt: timeValue(row.breakTime),
    stop: removeUndefined({
      level: row.stopLevel,
      sourceAt: timeValue(row.stopSourceTime),
      hitAt: timeValue(row.stopHitEventTime ?? row.stopHitTime),
    }),
    causes: Array.isArray(row.causes) ? row.causes.map(causeObject) : undefined,
  });
  if (group === "orderReactions") return removeUndefined({
    ...base,
    mode: readableMode(row.mode ?? row.reactionMode),
    startedAt: timeValue(row.firstTime),
    confirmedAt: timeValue(row.breakTime),
    consumed: row.consumed,
    stopHitAt: timeValue(row.stopHitEventTime ?? row.stopHitTime),
  });
  return removeUndefined({ ...base, occurredAt: timeValue(record.epoch), note: "No manual-review projection is defined for this collection." });
}

const infoCollectionNames = {
  reactions: "reactions", resets: "resets", blueLines: "blueLines",
  aZones: "aStructures", sZones: "sStructures", eZones: "eStructures",
  stopAlls: "stopAllEvents", orderReactions: "orderReactions", orderAudit: "orderAudit",
};
export function buildInfoPayload(payload) {
  const directions = {};
  for (const [direction, groups] of Object.entries(payload.directions || {})) {
    directions[direction] = {};
    for (const [group, rows] of Object.entries(groups)) {
      if (!Array.isArray(rows)) continue;
      const outputName = infoCollectionNames[group] || group;
      directions[direction][outputName] = rows.map((row, index) => manualInfoObject({
        direction, group, row, index, groups,
      }));
    }
  }
  return removeUndefined({
    source: removeUndefined({
      timezone: "Asia/Tehran",
      timeframeSeconds: payload.timeframe,
      range: removeUndefined({ from: timeValue(payload.actualFrom), to: timeValue(payload.actualTo) }),
    }),
    directions,
  });
}

const yamlScalar = (value) => {
  if (value === null) return "null";
  if (typeof value === "boolean" || typeof value === "number") return String(value);
  return JSON.stringify(String(value));
};
const isObject = (value) => value && typeof value === "object" && !Array.isArray(value);
function yamlLines(value, depth = 0) {
  const lines = [];
  const stack = [{ type: "value", value, depth }];
  while (stack.length) {
    const task = stack.pop();
    if (task.type === "line") { lines.push(task.value); continue; }
    if (task.type === "blank") { lines.push(""); continue; }
    const current = task.value;
    if (Array.isArray(current)) {
      for (let index = current.length - 1; index >= 0; index--) {
        const item = current[index];
        if (isObject(item) || Array.isArray(item)) {
          stack.push({ type: "value", value: item, depth: task.depth + 1 });
          stack.push({ type: "line", value: `${" ".repeat(task.depth * 4)}-` });
        } else stack.push({ type: "line", value: `${" ".repeat(task.depth * 4)}- ${yamlScalar(item)}` });
        if (index) stack.push({ type: "blank" });
      }
      continue;
    }
    const entries = Object.entries(current || {});
    const blankBefore = new Set();
    let previousComplex = false;
    entries.forEach(([, item], index) => {
      const complex = isObject(item) || Array.isArray(item);
      if (index && (complex || previousComplex)) blankBefore.add(index);
      previousComplex = complex;
    });
    for (let index = entries.length - 1; index >= 0; index--) {
      const [key, item] = entries[index];
      const complex = isObject(item) || Array.isArray(item);
      const prefix = " ".repeat(task.depth * 4);
      if (complex) {
        stack.push({ type: "value", value: item, depth: task.depth + 1 });
        stack.push({ type: "line", value: `${prefix}${key}:` });
      } else stack.push({ type: "line", value: `${prefix}${key}: ${yamlScalar(item)}` });
      if (blankBefore.has(index)) stack.push({ type: "blank" });
    }
  }
  return lines;
}
export const formatInfoYaml = (value) => yamlLines(value).join("\n");
const copyIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="11" height="11" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/></svg>';
const detail = (value) => {
  const lines = formatInfoYaml(value).split("\n").map((line) => {
    if (!line) return '<span class="yaml-line yaml-gap" aria-hidden="true"></span>';
    const depth = Math.min(5, Math.floor((line.match(/^ */)?.[0].length || 0) / 4));
    return `<span class="yaml-line yaml-depth-${depth}">${escapeHtml(line)}</span>`;
  }).join("\n");
  return `<div class="yaml-tools"><button class="yaml-copy" type="button" data-copy-yaml title="Copy Bridge output" aria-label="Copy Bridge output">${copyIcon}</button></div><pre class="bridge-yaml" aria-label="Bridge output in YAML">${lines}</pre>`;
};
const lazyDetail = (record) => `<details class="bridge-output" data-bridge-id="${escapeHtml(record.id)}"><summary>Bridge output</summary><div class="bridge-placeholder"></div></details>`;
function eventCard(record) {
  const { id, direction, row, time, label } = record;
  const visibleTime = time === "Undated" ? time : time.slice(11);
  const timeGroup = record.timeGroup || reviewTimeGroup(time);
  return `<article class="event" data-id="${escapeHtml(id)}" data-filter="${escapeHtml(record.category.key)}" data-time="${time}" data-time-group="${escapeHtml(timeGroup)}" data-label="${escapeHtml(`${direction} | ${label}`)}">
    <div class="state-control" role="group" aria-label="Review status">${["true", "false"].map((status) => `<label class="${status}-choice" title="Mark as ${status}"><input class="state" type="radio" name="${escapeHtml(id)}" value="${status}" aria-label="Mark ${escapeHtml(`${direction} ${label} ${time}`)} as ${status}"><span class="sr-only">Mark as ${status}</span></label>`).join("")}</div>
    <button class="event-time copy-line" type="button" title="Copy full timestamp and review status"><time datetime="${time === "Undated" ? "" : time.replace(" ", "T")}">${visibleTime}</time></button>
    <div><span class="chip" style="color:${reviewLabelColor(record, record.color)};background:${reviewColorSurface()}">${escapeHtml(label)}</span><small>${escapeHtml(direction)}</small></div>
    ${lazyDetail(record)}</article>`;
}

function timeGroupActions(day) {
  const encodedDay = escapeHtml(day);
  return `<div class="day-bulk-actions" role="group" aria-label="Review visible events on ${encodedDay}">
    <span>Visible events</span>
    <button type="button" data-time-group="${encodedDay}" data-time-group-status="true">Mark True</button>
    <button type="button" data-time-group="${encodedDay}" data-time-group-status="false">Mark False</button>
    <button type="button" class="quiet-action" data-time-group="${encodedDay}" data-time-group-status="">Clear</button>
  </div>`;
}

// Review behavior for the served page; it runs same-origin and stores verdicts
// in localStorage. It still makes no requests and stays entirely in the page.
function legacyReviewRuntime(initialBridgeData = null) {
  const q = (selector) => document.querySelector(selector);
  let bridgeData = initialBridgeData && typeof initialBridgeData === "object" ? initialBridgeData : {};
  if (!initialBridgeData) {
    try { bridgeData = JSON.parse(q("#bridge-data")?.value || "{}") || {}; } catch {}
  }
  q("#bridge-data")?.remove();
  const escapeBridgeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
  const bridgeScalar = (value) => value === null ? "null" : typeof value === "boolean" || typeof value === "number" ? String(value) : JSON.stringify(String(value));
  const bridgeObject = (value) => value && typeof value === "object" && !Array.isArray(value);
  const bridgeYaml = (value) => {
    const lines = [], stack = [{ type: "value", value, depth: 0 }];
    while (stack.length) {
      const task = stack.pop();
      if (task.type === "line") { lines.push(task.value); continue; }
      if (task.type === "blank") { lines.push(""); continue; }
      if (Array.isArray(task.value)) {
        for (let index = task.value.length - 1; index >= 0; index--) {
          const item = task.value[index], prefix = " ".repeat(task.depth * 4);
          if (bridgeObject(item) || Array.isArray(item)) { stack.push({ type: "value", value: item, depth: task.depth + 1 }); stack.push({ type: "line", value: `${prefix}-` }); }
          else stack.push({ type: "line", value: `${prefix}- ${bridgeScalar(item)}` });
          if (index) stack.push({ type: "blank" });
        }
        continue;
      }
      const entries = Object.entries(task.value || {}), blankBefore = new Set();
      let previousComplex = false;
      entries.forEach(([, item], index) => { const complex = bridgeObject(item) || Array.isArray(item); if (index && (complex || previousComplex)) blankBefore.add(index); previousComplex = complex; });
      for (let index = entries.length - 1; index >= 0; index--) {
        const [key, item] = entries[index], complex = bridgeObject(item) || Array.isArray(item), prefix = " ".repeat(task.depth * 4);
        if (complex) { stack.push({ type: "value", value: item, depth: task.depth + 1 }); stack.push({ type: "line", value: `${prefix}${key}:` }); }
        else stack.push({ type: "line", value: `${prefix}${key}: ${bridgeScalar(item)}` });
        if (blankBefore.has(index)) stack.push({ type: "blank" });
      }
    }
    return lines;
  };
  const renderBridgeOutput = (details) => {
    const target = details.querySelector(".bridge-placeholder"), value = bridgeData[details.dataset.bridgeId];
    if (!target || !value) return;
    const lines = bridgeYaml(value).map((line) => {
      if (!line) return '<span class="yaml-line yaml-gap" aria-hidden="true"></span>';
      const depth = Math.min(5, Math.floor((line.match(/^ */)?.[0].length || 0) / 4));
      return `<span class="yaml-line yaml-depth-${depth}">${escapeBridgeHtml(line)}</span>`;
    }).join("\n");
    target.innerHTML = `<div class="yaml-tools"><button class="yaml-copy" type="button" data-copy-yaml title="Copy Bridge output" aria-label="Copy Bridge output"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="11" height="11" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/></svg></button></div><pre class="bridge-yaml" aria-label="Bridge output in YAML">${lines}</pre>`;
    delete bridgeData[details.dataset.bridgeId];
  };
  const events = [...document.querySelectorAll(".event")];
  const references = [...document.querySelectorAll(".reference-row")];
  const filters = [...document.querySelectorAll(".category-filter")];
  const days = [...document.querySelectorAll(".day")];
  const key = `timeline-review-v4-${document.body.dataset.payloadHash}-${document.body.dataset.reviewId}`;
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(key) || "{}") || {}; } catch {}
  for (const event of events) {
    const status = saved[event.dataset.id];
    if (["true", "false"].includes(status)) event.querySelector(`input[value="${status}"]`).checked = true;
  }
  const statusOf = (event) => event.querySelector("input:checked")?.value;
  const line = (event) => `${event.dataset.time} | ${event.dataset.label} | ${statusOf(event) === "true" ? "True" : statusOf(event) === "false" ? "False" : "Unselected"}`;
  function update() {
    const from = q("#from").value.trim().replace("T", " "), to = q("#to").value.trim().replace("T", " ");
    const mode = q("#mode").value;
    const selected = new Set(filters.filter((input) => input.checked).map((input) => input.value));
    const invalid = !!(from && to && from > to);
    q("#range-error").hidden = !invalid;
    q("#to").setAttribute("aria-invalid", String(invalid));
    const hidden = (event) => invalid || !selected.has(event.dataset.filter) ||
      !!((from && event.dataset.time < from) || (to && event.dataset.time > to));
    const output = ["Indicator information review", "Timezone: Asia/Tehran", ""];
    const statuses = {};
    for (const event of events) {
      const status = statusOf(event);
      event.hidden = hidden(event);
      event.dataset.status = status || "";
      if (status) statuses[event.dataset.id] = status;
      if (!event.hidden && status && (mode === "all" || status === mode)) output.push(line(event));
    }
    for (const row of references) row.hidden = hidden(row);
    document.querySelectorAll(".collection").forEach((group) => { group.hidden = !group.querySelector(".reference-row:not([hidden])"); });
    days.forEach((day) => {
      const visible = [...day.querySelectorAll(".event:not([hidden])")];
      day.hidden = !visible.length;
      day.querySelector(".day-count").textContent = `${visible.length.toLocaleString()} events · ${visible.filter(statusOf).length.toLocaleString()} reviewed`;
    });
    const visibleCount = events.filter((event) => !event.hidden).length;
    q("#empty").hidden = visibleCount !== 0;
    const values = Object.values(statuses);
    q("#filter-note").textContent = `${visibleCount.toLocaleString()} of ${events.length.toLocaleString()} events visible · ${values.filter((v) => v === "true").length.toLocaleString()} True · ${values.filter((v) => v === "false").length.toLocaleString()} False · ${(events.length - values.length).toLocaleString()} unreviewed (all records).`;
    q("#report-text").value = output.join("\n");
    try {
      if (values.length) localStorage.setItem(key, JSON.stringify(statuses));
      else localStorage.removeItem(key);
    } catch { q("#storage-note").textContent = "Browser storage unavailable. Download the TXT report before closing this page."; }
  }
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); }
    catch {
      const input = document.createElement("textarea"); input.value = text;
      document.body.append(input); input.select(); document.execCommand("copy"); input.remove();
    }
  }
  if (typeof document.addEventListener === "function") {
    document.addEventListener("toggle", (event) => {
      const details = event.target;
      if (details instanceof HTMLDetailsElement && details.open && details.matches("[data-bridge-id]")) renderBridgeOutput(details);
    }, true);
    document.addEventListener("click", async (event) => {
      const copyButton = event.target.closest?.("[data-copy-yaml]");
      if (copyButton) {
        const text = copyButton.closest("details")?.querySelector(".bridge-yaml")?.textContent?.trimEnd();
        if (!text) return;
        await copy(text);
        copyButton.dataset.copied = "true";
        copyButton.title = "Copied Bridge output";
        copyButton.setAttribute("aria-label", "Bridge output copied");
        setTimeout(() => {
          copyButton.dataset.copied = "";
          copyButton.title = "Copy Bridge output";
          copyButton.setAttribute("aria-label", "Copy Bridge output");
        }, 1200);
        return;
      }
      const groupButton = event.target.closest?.("[data-time-group-status]");
      if (!groupButton) return;
      const status = groupButton.dataset.timeGroupStatus;
      if (!["true", "false", ""].includes(status)) return;
      const ids = new Set(visibleReviewTimeGroupIds(events.map((item) => ({
        id: item.dataset.id, timeGroup: item.dataset.timeGroup, hidden: item.hidden,
      })), groupButton.dataset.timeGroup));
      if (!ids.size) return;
      for (const item of events) {
        if (!ids.has(item.dataset.id)) continue;
        const input = item.querySelector(`input[value="${status}"]`);
        if (input) input.checked = true;
        else item.querySelectorAll("input").forEach((control) => { control.checked = false; });
      }
      update();
    });
  }
  events.forEach((event) => {
    event.querySelectorAll("input").forEach((input) => { input.onchange = update; });
    event.querySelector(".copy-line").onclick = () => copy(line(event));
  });
  q("#from").oninput = update; q("#to").oninput = update; q("#mode").onchange = update;
  filters.forEach((input) => { input.onchange = update; });
  q("#reset").onclick = () => { q("#from").value = ""; q("#to").value = ""; update(); };
  q("#copy").onclick = () => copy(q("#report-text").value);
  q("#download").onclick = () => {
    const url = URL.createObjectURL(new Blob([q("#report-text").value], { type: "text/plain;charset=utf-8" }));
    const a = document.createElement("a"); a.href = url;
    const date = new Date(), two = (value) => String(value).padStart(2, "0");
    a.download = `info-${date.getFullYear()}_${two(date.getMonth() + 1)}_${two(date.getDate())} ${two(date.getHours())}_${two(date.getMinutes())}_${two(date.getSeconds())}.txt`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };
  update();
}

const reportFamilyOrder = ["Reaction", "Reset", "Blue Line", "A", "S Blue", "S Red", "E Blue", "E Red", "StopAll", "Order Audit", "MBL", "PH", "PL"];
export const reportFamilyColor = {
  Reaction: "var(--report-reaction)", Reset: "var(--report-reset)",
  "Blue Line": "var(--report-blue-line)", A: "var(--report-a)",
  "S Blue": "var(--report-s-blue)", "S Red": "var(--report-s-red)",
  "E Blue": "var(--report-e-blue)", "E Red": "var(--report-e-red)",
  StopAll: "var(--report-stop-all)", "Order Audit": "var(--report-order-audit)",
  PH: PRIMARY_VISUAL_DEFAULTS.primaryArrowColor, PL: PRIMARY_VISUAL_DEFAULTS.primaryCircleColor,
  MBL: PRIMARY_VISUAL_DEFAULTS.mblColor,
};

export function reportCategoryColor(key, family) {
  if (/^reactions?:bearish(?::|$)/.test(key)) return "var(--report-reaction-bearish)";
  if (/^reactions?:bullish(?::|$)/.test(key)) return "var(--report-reaction-bullish)";
  return reportFamilyColor[family] || "var(--ui-text-secondary)";
}

function reportRecordColorKey(record) {
  const direction = String(record.direction || "").toLowerCase();
  return record.category.family === "Reaction" && ["bearish", "bullish"].includes(direction)
    ? `reactions:${direction}` : record.category.colorKey || record.category.key;
}

export function reportDisplayLabel(record) {
  const family = record?.category?.family || "";
  const projected = record?.reportDetails || bridgeProjection(record?.groups, record?.group, record?.index);
  let number = behaviorNumber(record?.row?.number ?? projected?.number);
  if (number == null) {
    const base = family.startsWith("E ") ? "E" : family.startsWith("S ") ? "S" : family;
    for (const label of [record?.label, record?.category?.label]) {
      const supplied = String(label || "").split(/\s*\/\s*/).at(-1).match(/^(E|S|A|StopAll|PH|PL)[ -]?(\d+)$/);
      if (supplied?.[1] === base) { number = behaviorNumber(supplied[2]); break; }
    }
  }
  if (family === "Reaction") return numberedLabel(String(record?.direction || "").toLowerCase() === "bearish" ? "Bearish Reaction" : "Bullish Reaction", number);
  if (family === "Order Audit") return record?.category?.label || record?.label || family;
  if (["Blue Line", "Reset", "A", "StopAll", "PH", "PL", "MBL"].includes(family)) return numberedLabel(family, number);
  if (family.startsWith("S ")) return numberedLabel("S", number);
  if (family.startsWith("E ")) return numberedLabel("E", number);
  return record?.label || family || "Report";
}

function reportFilterChildLabel(family, label) {
  const value = String(label || "");
  return value.replace(`${family} / `, "").replace(/^(E|S|A|StopAll|PH|PL)[ -]?(\d+)$/, "$1-$2");
}

function reportEventCard(record) {
  const { id, direction, time, category } = record;
  const safeTime = time || "Undated";
  const label = reportDisplayLabel(record);
  const color = primaryFamilies.has(category.family) ? record.color : reportCategoryColor(reportRecordColorKey(record), category.family);
  return `<article class="event"${defaultHiddenFamilies.has(category.family) ? " hidden" : ""} style="--event-color:${escapeHtml(color)}" data-id="${escapeHtml(id)}" data-filter="${escapeHtml(category.key)}" data-filter-family="${escapeHtml(category.family)}" data-report-family="${escapeHtml(category.family)}" data-time="${escapeHtml(safeTime)}" data-time-group="${escapeHtml(reviewTimeGroup(safeTime))}" data-label="${escapeHtml(`${direction} | ${label}`)}">
    <div class="state-control" role="group" aria-label="Review status"><label class="true-choice" title="Mark as true"><input class="state" type="radio" name="${escapeHtml(id)}" value="true" aria-label="Mark ${escapeHtml(`${direction} ${label} ${safeTime}`)} as true"><span class="sr-only">True</span></label><label class="false-choice" title="Mark as false"><input class="state" type="radio" name="${escapeHtml(id)}" value="false" aria-label="Mark ${escapeHtml(`${direction} ${label} ${safeTime}`)} as false"><span class="sr-only">False</span></label></div>
    <button class="event-time copy-line" type="button" title="Copy timestamp and review status"><time datetime="${safeTime === "Undated" ? "" : safeTime.replace(" ", "T")}">${escapeHtml(safeTime)}</time></button>
    <div class="event-label"><span class="chip" style="--chip-color:${escapeHtml(color)};--event-color:${escapeHtml(color)}">${escapeHtml(label)}</span><small>${escapeHtml(direction)}</small></div>
    <details class="bridge-output" data-bridge-id="${escapeHtml(id)}"><summary>Bridge output</summary><div class="bridge-placeholder"></div></details>
  </article>`;
}

function reportFilterMarkup(families) {
  const ordered = [...families.entries()].sort((a, b) => {
    const ai = reportFamilyOrder.indexOf(a[0]), bi = reportFamilyOrder.indexOf(b[0]);
    return (ai < 0 ? 99 : ai) - (bi < 0 ? 99 : bi) || a[0].localeCompare(b[0]);
  });
  return ordered.map(([family, group]) => {
    const children = [...group.children.values()].sort((a, b) => a.label.localeCompare(b.label));
    const childColors = [...new Set(children.map(child => reportCategoryColor(child.colorKey || child.key, family)))];
    const color = primaryFamilies.has(family) ? group.color : childColors.length === 1 ? childColors[0]
      : family === "Reaction" ? "var(--ui-text-secondary)" : reportFamilyColor[family] || "var(--ui-text-secondary)";
    const checked = defaultHiddenFamilies.has(family) ? "" : " checked";
    return `<details class="filter-group" data-filter-group="${escapeHtml(family)}" style="--family-color:${escapeHtml(color)}"><summary><input class="filter-group-checkbox" type="checkbox" data-filter-parent="${escapeHtml(family)}" aria-label="Select all ${escapeHtml(family)}"${checked}><span class="filter-group-title"><i class="filter-dot" style="background:${escapeHtml(color)}" aria-hidden="true"></i><strong>${escapeHtml(family)}</strong></span><span class="filter-group-count">${group.count.toLocaleString()}</span></summary><div class="filter-options"><label class="filter-option filter-parent"><input type="checkbox" data-filter-parent="${escapeHtml(family)}"${checked}><span>All</span><b>${group.count.toLocaleString()}</b></label>${children.map((child) => { const childColor = primaryFamilies.has(family) ? child.color : reportCategoryColor(child.colorKey || child.key, family); const childLabel = reportFilterChildLabel(family, child.label); return `<label class="filter-option" style="--option-color:${escapeHtml(childColor)}"><input class="category-filter" type="checkbox" data-filter-family="${escapeHtml(family)}" data-filter-key="${escapeHtml(child.key)}" value="${escapeHtml(child.key)}"${checked}><span>${escapeHtml(childLabel)}</span><b>${child.count.toLocaleString()}</b></label>`; }).join("")}</div></details>`;
  }).join("");
}

export function reviewRuntime(initialBridgeData = null) {
  const q = (selector) => document.querySelector(selector);
  let bridgeData = initialBridgeData && typeof initialBridgeData === "object" ? initialBridgeData : {};
  q("#bridge-data")?.remove();
  const bridgeObject = (value) => value && typeof value === "object" && !Array.isArray(value);
  const bridgeScalar = (value) => value === null ? "null" : typeof value === "boolean" || typeof value === "number" ? String(value) : JSON.stringify(String(value));
  const bridgeYaml = (value) => {
    const lines = [], stack = [{ type: "value", value, depth: 0 }];
    while (stack.length) {
      const task = stack.pop();
      if (task.type === "line") { lines.push(task.value); continue; }
      if (task.type === "blank") { lines.push(""); continue; }
      if (Array.isArray(task.value)) {
        for (let index = task.value.length - 1; index >= 0; index--) {
          const item = task.value[index], prefix = " ".repeat(task.depth * 4);
          if (bridgeObject(item) || Array.isArray(item)) { stack.push({ type: "value", value: item, depth: task.depth + 1 }); stack.push({ type: "line", value: `${prefix}-` }); }
          else stack.push({ type: "line", value: `${prefix}- ${bridgeScalar(item)}` });
          if (index) stack.push({ type: "blank" });
        }
        continue;
      }
      const entries = Object.entries(task.value || {}), blankBefore = new Set();
      let previousComplex = false;
      entries.forEach(([, item], index) => { const complex = bridgeObject(item) || Array.isArray(item); if (index && (complex || previousComplex)) blankBefore.add(index); previousComplex = complex; });
      for (let index = entries.length - 1; index >= 0; index--) {
        const [key, item] = entries[index], complex = bridgeObject(item) || Array.isArray(item), prefix = " ".repeat(task.depth * 4);
        if (complex) { stack.push({ type: "value", value: item, depth: task.depth + 1 }); stack.push({ type: "line", value: `${prefix}${key}:` }); }
        else stack.push({ type: "line", value: `${prefix}${key}: ${bridgeScalar(item)}` });
        if (blankBefore.has(index)) stack.push({ type: "blank" });
      }
    }
    return lines;
  };
  const renderBridgeOutput = (details) => {
    const value = bridgeData[details.dataset.bridgeId], target = details.querySelector(".bridge-placeholder");
    if (!target || !value) return;
    const lines = bridgeYaml(value).map((line) => {
      if (!line) return '<span class="yaml-line yaml-gap" aria-hidden="true"></span>';
      const depth = Math.min(8, Math.floor((line.match(/^ */)?.[0].length || 0) / 4));
      return `<span class="yaml-line yaml-depth-${depth}" style="--indent-px:${depth * 16}px">${escapeHtml(line)}</span>`;
    }).join("\n");
    target.innerHTML = `<div class="yaml-tools"><button class="yaml-copy" type="button" data-copy-yaml title="Copy Bridge output" aria-label="Copy Bridge output">${copyIcon}</button></div><pre class="bridge-yaml" aria-label="Bridge output in YAML">${lines}</pre>`;
    delete bridgeData[details.dataset.bridgeId];
  };
  const events = [...document.querySelectorAll(".event")];
  const days = [...document.querySelectorAll(".day")];
  const filters = [...document.querySelectorAll(".category-filter")];
  const parents = [...document.querySelectorAll("[data-filter-parent]")];
  const allFilters = q("#all-filters");
  const filterTreeToggle = q(".filter-all-toggle");
  const filterGroups = q("#filter-groups");
  const key = `tradingbot-minimal-review:${document.body.dataset.payloadHash || "standalone"}:${document.body.dataset.reviewId || "report"}`;
  let saved = {};
  try { saved = JSON.parse(localStorage.getItem(key) || "{}") || {}; } catch {}
  for (const event of events) {
    const status = saved[event.dataset.id];
    if (["true", "false"].includes(status)) event.querySelector(`input[value="${status}"]`).checked = true;
  }
  const statusOf = (event) => event.querySelector("input:checked")?.value;
  const line = (event) => `${event.dataset.time} | ${event.dataset.label} | ${statusOf(event) === "true" ? "True" : statusOf(event) === "false" ? "False" : "Unselected"}`;
  const metadata = [...document.querySelectorAll(".calculation-meta > div")].map((item) => [item.querySelector("dt")?.textContent || "", item.querySelector("dd")?.textContent || ""]);
  const refreshReport = () => {
    const accepted = q("#mode")?.value || "all";
    const reviewed = events.filter((event) => !event.hidden && (accepted === "visible"
      || statusOf(event) && (accepted === "all" || statusOf(event) === accepted)));
    const lines = [
      "CALCULATION REPORT - MANUAL REVIEW",
      ...metadata.map(([label, value]) => `${label}: ${value}`),
      `${accepted === "visible" ? "Visible" : "Reviewed"} events in current view: ${reviewed.length}`,
      "",
      ...reviewed.map((event) => `${event.dataset.time}\t${event.dataset.label.replace(/^\w+\s*\|\s*/, "")}\t${(statusOf(event) || "Unselected").toUpperCase()}`),
    ];
    const output = q("#report-text");
    if (output) output.value = lines.join("\n");
  };
  const updateParents = () => {
    parents.forEach((parent) => {
      const children = filters.filter((input) => input.dataset.filterFamily === parent.dataset.filterParent);
      const checked = children.filter((input) => input.checked).length;
      parent.checked = checked === children.length && children.length > 0;
      parent.indeterminate = checked > 0 && checked < children.length;
      parent.closest(".filter-group")?.classList.toggle("has-active", checked > 0);
    });
    if (allFilters) {
      const checked = filters.filter((input) => input.checked).length;
      allFilters.checked = checked === filters.length && filters.length > 0;
      allFilters.indeterminate = checked > 0 && checked < filters.length;
    }
  };
  const applySearch = () => {
    const query = q("#filter-search")?.value.trim().toLowerCase() || "";
    if (query && filterGroups?.hidden) {
      filterGroups.hidden = false;
      filterTreeToggle?.setAttribute("aria-expanded", "true");
      filterTreeToggle?.setAttribute("aria-label", "Collapse all filters");
    }
    document.querySelectorAll(".filter-group").forEach((group) => {
      const groupMatches = !query || group.dataset.filterGroup.toLowerCase().includes(query);
      const match = groupMatches || group.textContent.toLowerCase().includes(query);
      group.hidden = !match;
      group.querySelectorAll(".filter-option").forEach((row) => { row.hidden = !!query && !groupMatches && !row.textContent.toLowerCase().includes(query); });
      if (query && match) group.open = true;
    });
  };
  function update() {
    const from = q("#from")?.value.trim().replace("T", " ") || "", to = q("#to")?.value.trim().replace("T", " ") || "";
    const selected = new Set(filters.filter((input) => input.checked).map((input) => input.value));
    const invalid = !!(from && to && from > to);
    if (q("#range-error")) q("#range-error").hidden = !invalid;
    if (q("#to")) q("#to").setAttribute("aria-invalid", String(invalid));
    const hidden = (event) => invalid || !selected.has(event.dataset.filter) || !!((from && event.dataset.time < from) || (to && event.dataset.time > to));
    const statuses = {};
    for (const event of events) {
      const status = statusOf(event);
      event.hidden = hidden(event);
      event.dataset.status = status || "";
      if (status) statuses[event.dataset.id] = status;
    }
    days.forEach((day) => {
      const visible = [...day.querySelectorAll(".event:not([hidden])")];
      day.hidden = !visible.length;
      const count = day.querySelector(".day-count");
      if (count) count.textContent = `${visible.length.toLocaleString()} · ${visible.filter(statusOf).length.toLocaleString()}`;
    });
    const visibleCount = events.filter((event) => !event.hidden).length, values = Object.values(statuses);
    if (q("#empty")) q("#empty").hidden = visibleCount !== 0;
    if (q("#filter-note")) q("#filter-note").textContent = `${visibleCount.toLocaleString()} / ${events.length.toLocaleString()} events`;
    refreshReport();
    updateParents();
    try { if (values.length) localStorage.setItem(key, JSON.stringify(statuses)); else localStorage.removeItem(key); } catch {}
  }
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); }
    catch { const input = document.createElement("textarea"); input.value = text; document.body.append(input); input.select(); document.execCommand("copy"); input.remove(); }
  }
  document.addEventListener("toggle", (event) => { const details = event.target; if (details instanceof HTMLDetailsElement && details.open && details.matches("[data-bridge-id]")) renderBridgeOutput(details); }, true);
  document.addEventListener("click", async (event) => {
    if (event.target.closest?.(".filter-group-checkbox")) {
      event.stopPropagation();
      return;
    }
    const bridgeSummary = event.target.closest?.("details[data-bridge-id] > summary");
    if (bridgeSummary) {
      const details = bridgeSummary.parentElement;
      if (details?.open) renderBridgeOutput(details);
      else if (details) setTimeout(() => {
        if (details.open) renderBridgeOutput(details);
      }, 0);
      return;
    }
    const copyButton = event.target.closest?.("[data-copy-yaml]");
    if (copyButton) { const text = copyButton.closest("details")?.querySelector(".bridge-yaml")?.textContent?.trimEnd(); if (text) await copy(text); return; }
    const groupButton = event.target.closest?.("[data-time-group-status]");
    if (!groupButton) return;
    const status = groupButton.dataset.timeGroupStatus;
    for (const item of events.filter((entry) => entry.dataset.timeGroup === groupButton.dataset.timeGroup && !entry.hidden)) {
      item.querySelectorAll("input").forEach((control) => { control.checked = control.value === status; });
    }
    update();
  });
  filters.forEach((input) => { input.onchange = update; });
  parents.forEach((parent) => { parent.onchange = () => { filters.filter((input) => input.dataset.filterFamily === parent.dataset.filterParent).forEach((input) => { input.checked = parent.checked; }); update(); }; });
  allFilters && (allFilters.onchange = () => { filters.forEach((input) => { input.checked = allFilters.checked; }); update(); });
  filterTreeToggle && (filterTreeToggle.onclick = () => {
    const expanded = filterTreeToggle.getAttribute("aria-expanded") !== "true";
    filterTreeToggle.setAttribute("aria-expanded", String(expanded));
    filterTreeToggle.setAttribute("aria-label", expanded ? "Collapse all filters" : "Expand all filters");
    if (filterGroups) filterGroups.hidden = !expanded;
  });
  events.forEach((event) => { event.querySelectorAll(".state").forEach((input) => { input.onchange = update; }); event.querySelector(".copy-line").onclick = () => copy(line(event)); });
  q("#from") && (q("#from").oninput = update); q("#to") && (q("#to").oninput = update); q("#mode") && (q("#mode").onchange = update);
  q("#filter-search") && (q("#filter-search").oninput = applySearch);
  q("#clear-filters") && (q("#clear-filters").onclick = () => { filters.forEach((input) => { input.checked = false; }); update(); });
  q("#reset") && (q("#reset").onclick = () => { q("#from").value = ""; q("#to").value = ""; update(); });
  q("#copy") && (q("#copy").onclick = () => copy(q("#report-text").value));
  q("#download") && (q("#download").onclick = () => { const url = URL.createObjectURL(new Blob([q("#report-text").value], { type: "text/plain;charset=utf-8" })); const a = document.createElement("a"); a.href = url; a.download = manualReviewFilename(new Date(), "txt"); a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); });
  update();
}

// Build the review page body from the Bridge report payload. The raw direction
// collections remain a compatibility fallback for older cached calculations.
// export, minus the heavyweight duplication. The payload is embedded once as
// the <pre> reference copy; candle caches are never serialized here.
async function buildLegacyReviewBody(payload, snapshot = {}, cryptoApi = globalThis.crypto) {
  if (!payload || !payload.directions || typeof payload.directions !== "object") throw new Error("Invalid indicator payload");
  const raw = JSON.stringify(payload);
  const digest = await cryptoApi.subtle.digest("SHA-256", new TextEncoder().encode(raw));
  const hash = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  const records = reviewRecords(payload), days = new Map(), groups = new Map(), categories = new Map();
  const bridgeData = Object.create(null);
  const objects = new Map((snapshot.indicatorObjects || []).map((item) => [item.id, item]));
  for (const record of records) {
    bridgeData[record.id] = manualInfoObject(record);
    record.color = reviewColor(record, snapshot, objects);
    if (!categories.has(record.category.key)) categories.set(record.category.key, { ...record.category, color: record.color, count: 0 });
    categories.get(record.category.key).count++;
    const day = reviewTimeGroup(record.time);
    record.timeGroup = day;
    if (!days.has(day)) days.set(day, []);
    days.get(day).push(record);
    const group = `${record.direction} · ${collections[record.group]?.[0] || record.group}`;
    if (!groups.has(group)) groups.set(group, []);
    groups.get(group).push(record);
  }
  const calculation = snapshot.calculation || {};
  const rangeTime = (value) => typeof value === "number" && Number.isFinite(value) ? reviewTime(value) : "—";
  const reportMeta = [
    ["Symbol", calculation.symbol || calculation.source?.symbol || "—"],
    ["Source file", calculation.sourceFile || calculation.source?.id || "—"],
    ["Calculation timeframe", `${calculation.timeframe ?? payload.timeframe ?? "—"} seconds`],
    ["Direction", readableDirection(calculation.direction || Object.keys(payload.directions || {}).join(", "))],
    ["Range", `${rangeTime(calculation.from ?? payload.actualFrom)} → ${rangeTime(calculation.to ?? payload.actualTo)}`],
  ];
  const timeline = [...days].map(([day, rows]) => `<details class="day" data-time-group="${escapeHtml(day)}"><summary class="day-head"><h2>${escapeHtml(day)}</h2><span class="day-count">${rows.length.toLocaleString()} events</span></summary>${timeGroupActions(day)}<div class="events">${rows.map(eventCard).join("")}</div></details>`).join("");
  const features = [...groups].map(([group, rows]) => `<section class="feature"><strong>${escapeHtml(group)}</strong><small>${rows.length.toLocaleString()} records</small></section>`).join("");
  const categoryOrder = Object.keys(colorSpec);
  const filterControls = [...categories.values()].sort((a, b) => (categoryOrder.indexOf(a.key) < 0 ? 99 : categoryOrder.indexOf(a.key)) - (categoryOrder.indexOf(b.key) < 0 ? 99 : categoryOrder.indexOf(b.key)))
    .map((category) => `<label class="category-choice"><input class="category-filter" type="checkbox" value="${escapeHtml(category.key)}" checked><i class="swatch" style="background:${category.color}" aria-hidden="true"></i><span>${escapeHtml(category.label)}</span><small>${category.count.toLocaleString()}</small></label>`).join("");
  // Keep the legacy template tail inexpensive; the returned body below replaces
  // it with the lazy bridge-data store before it reaches the browser.
  const infoPayload = {};
  const body = `<a class="skip-link" href="#timeline">Skip to timeline</a><header><span class="eyebrow">INDICATOR INFO · ASIA/TEHRAN</span><h1>Indicator information</h1><dl class="calculation-meta" aria-label="Calculation details">${reportMeta.map(([label, value]) => `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`).join("")}</dl></header>
<main><section class="filters" aria-labelledby="filter-title"><div><span class="eyebrow">TIMELINE FILTER</span><h2 id="filter-title">Show a precise review window</h2></div><div class="filter-fields"><label>From<input id="from" type="datetime-local" step="1" aria-describedby="range-error"></label><label>To<input id="to" type="datetime-local" step="1" aria-describedby="range-error"></label><button id="reset" type="button">Reset</button></div><fieldset><legend>Behavior filters</legend><div class="category-options">${filterControls}</div></fieldset><p id="range-hint" hidden></p><p class="error" id="range-error" role="alert" hidden>From must not be later than To.</p><p id="filter-note" role="status" aria-live="polite"></p></section><section id="timeline" aria-labelledby="timeline-title"><span class="eyebrow">PRIMARY REVIEW SURFACE</span><h2 id="timeline-title">Chronological timeline</h2><p class="subtitle" hidden></p><p class="empty" id="empty" hidden>No matching events.</p>${timeline || "<p>No events.</p>"}</section>
<section class="report" id="review-report" aria-labelledby="report-title"><div><span class="eyebrow">AI HANDOFF</span><h2 id="report-title">Live review report</h2><p id="storage-note" hidden></p></div><div class="report-controls"><label>Include <select id="mode"><option value="all">All selected</option><option value="true">True only</option><option value="false">False only</option></select></label><button id="copy">Copy report</button><button id="download">Download TXT</button></div><textarea id="report-text" readonly aria-label="Review report"></textarea></section>
<h2>Record collections</h2>${features}</main>`;
  const optimizedBody = body;
  return { hash, reviewId: snapshot.exportedAt || "standalone", runtime: reviewRuntime.toString(), body: optimizedBody, bridgeData };
}

export async function buildReviewBody(payload, snapshot = {}, cryptoApi = globalThis.crypto) {
  if (!payload || !payload.directions || typeof payload.directions !== "object") throw new Error("Invalid indicator payload");
  const raw = JSON.stringify(payload);
  const digest = await cryptoApi.subtle.digest("SHA-256", new TextEncoder().encode(raw));
  const hash = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  const records = reviewRecords(payload), days = new Map(), families = new Map(), groups = new Map();
  const bridgeData = Object.create(null);
  const objects = new Map((snapshot.indicatorObjects || []).map((item) => [item.id, item]));
  for (const record of records) {
    bridgeData[record.id] = record.reportDetails || manualInfoObject(record);
    record.color = reviewColor(record, snapshot, objects);
    const category = record.category || { key: record.group, family: record.group, label: record.label };
    if (!families.has(category.family)) families.set(category.family, { count: 0, color: record.color, children: new Map() });
    const family = families.get(category.family);
    family.count++;
    if (!family.children.has(category.key)) family.children.set(category.key, { key: category.key, colorKey: reportRecordColorKey(record), label: category.label, color: record.color, count: 0 });
    family.children.get(category.key).count++;
    const day = reviewTimeGroup(record.time);
    record.timeGroup = day;
    if (!days.has(day)) days.set(day, []);
    days.get(day).push(record);
    const collection = category.family || record.group;
    if (!groups.has(collection)) groups.set(collection, 0);
    groups.set(collection, groups.get(collection) + 1);
  }
  const calculation = snapshot.calculation || {};
  const rangeTime = (value) => typeof value === "number" && Number.isFinite(value) ? reviewTime(value) : "—";
  const reportMeta = [
    ["Symbol", calculation.symbol || calculation.source?.symbol || "—"],
    ["Source file", calculation.sourceFile || calculation.source?.id || "—"],
    ["Timeframe", `${calculation.timeframe ?? payload.timeframe ?? "—"} seconds`],
    ["Direction", readableDirection(calculation.direction || Object.keys(payload.directions || {}).join(", "))],
    ["Range", `${rangeTime(calculation.from ?? payload.actualFrom)} → ${rangeTime(calculation.to ?? payload.actualTo)}`],
  ];
  const timeline = [...days].map(([day, rows]) => `<details class="day" data-time-group="${escapeHtml(day)}"><summary class="day-head"><h2>${escapeHtml(day)}</h2><span class="day-count">${rows.length.toLocaleString()}</span></summary>${timeGroupActions(day)}<div class="events">${rows.map(reportEventCard).join("")}</div></details>`).join("");
  const featureDetails = [...groups].map(([group, count]) => `<details class="feature"><summary><strong>${escapeHtml(group)}</strong><span>${count.toLocaleString()}</span></summary></details>`).join("");
  const body = `<a class="skip-link" href="#timeline">Skip to timeline</a><header><span class="eyebrow">CALCULATION REPORT</span><h1>Indicator information</h1><dl class="calculation-meta" aria-label="Calculation details">${reportMeta.map(([label, value]) => `<div><dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd></div>`).join("")}</dl></header>
<main class="report-shell"><aside class="filter-sidebar" aria-label="Behavior filters"><div class="filter-sidebar-head"><h2 class="filter-sidebar-title"><svg class="filter-heading-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16l-6.5 7.5v5.5l-3 2v-7.5L4 5Z"></path></svg>Behavior filters</h2><span class="filter-total-count">${records.length.toLocaleString()}</span><div class="filter-actions"><button id="clear-filters" class="quiet-action" type="button">Clear all</button></div></div><label class="filter-search"><span class="sr-only">Search filters</span><input id="filter-search" type="search" placeholder="Search filters…" autocomplete="off"></label><div class="filter-dates"><label>From<input id="from" type="datetime-local" step="1" aria-describedby="range-error"></label><label>To<input id="to" type="datetime-local" step="1" aria-describedby="range-error"></label><button id="reset" class="quiet-action" type="button">Reset dates</button></div><p class="error" id="range-error" role="alert" hidden>From must not be later than To.</p><div class="filter-tree"><div class="filter-all-row"><button class="filter-all-toggle" type="button" aria-controls="filter-groups" aria-expanded="true" aria-label="Collapse all filters"></button><label class="filter-all-label"><input id="all-filters" type="checkbox" checked><strong>All</strong><span class="filter-all-count">${records.length.toLocaleString()}</span></label></div><div class="filter-groups" id="filter-groups">${reportFilterMarkup(families)}</div></div><footer class="filter-footer"><span id="filter-note" role="status" aria-live="polite"></span></footer></aside><section class="report-content" id="timeline" aria-labelledby="timeline-title"><div class="section-head"><h2 id="timeline-title">Chronological timeline</h2><span id="empty" class="empty" hidden>No matching events.</span></div>${timeline || "<p class=\"empty\">No events.</p>"}</section></main>
<section class="report-export" id="review-report" aria-labelledby="report-title"><div class="report-export-head"><h2 id="report-title">Live review report</h2><div class="report-controls"><label>Include <select id="mode"><option value="all">All selected</option><option value="visible">All visible</option><option value="true">True only</option><option value="false">False only</option></select></label><button id="copy" type="button">Copy</button><button id="download" type="button">Download</button></div></div><textarea id="report-text" readonly aria-label="Review report"></textarea></section>
<section class="collections" aria-labelledby="collections-title"><h2 id="collections-title">Record collections</h2>${featureDetails}</section>`;
  return { hash, reviewId: snapshot.exportedAt || "standalone", runtime: reviewRuntime.toString(), body, bridgeData };
}
