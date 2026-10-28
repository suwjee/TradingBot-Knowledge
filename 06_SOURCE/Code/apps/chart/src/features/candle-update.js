/**
 * Breaks a chronological candle append into transport-safe requests without
 * changing the order in which the server validates or persists candles.
 */
export function chunkCandleUpdates(candles, maximumCandlesPerRequest = 5_000) {
  if (!Array.isArray(candles) || candles.length === 0) return [];

  const requestedSize = Number(maximumCandlesPerRequest);
  const chunkSize = Number.isFinite(requestedSize) && requestedSize > 0
    ? Math.floor(requestedSize)
    : 5_000;
  const chunks = [];

  for (let start = 0; start < candles.length; start += chunkSize) {
    chunks.push(candles.slice(start, start + chunkSize));
  }

  return chunks;
}

/**
 * Builds the largest chronological candle requests that fit below a known
 * JSON-body limit.  Count-only batching made a 90k-candle repair perform many
 * full RAW-file rewrites; this keeps the endpoint safely bounded while making
 * each atomic write materially larger.
 */
export function chunkCandleUpdatesByBytes(candles, {
  maximumPayloadBytes = 12_000_000,
  requestOverheadBytes = 64_000,
} = {}) {
  if (!Array.isArray(candles) || candles.length === 0) return [];

  const maximum = Math.floor(Number(maximumPayloadBytes));
  const overhead = Math.max(0, Math.floor(Number(requestOverheadBytes)) || 0);
  if (!Number.isSafeInteger(maximum) || maximum <= overhead + 2) {
    throw new Error("The chart update payload limit is invalid.");
  }

  const encoder = new TextEncoder();
  const chunks = [];
  let batch = [];
  // JSON arrays include their two brackets, and every later row has one comma.
  let batchBytes = overhead + 2;
  for (const candle of candles) {
    const serialized = JSON.stringify(candle);
    const candleBytes = encoder.encode(serialized === undefined ? "null" : serialized).byteLength;
    const separatorBytes = batch.length ? 1 : 0;
    if (batch.length && batchBytes + separatorBytes + candleBytes > maximum) {
      chunks.push(batch);
      batch = [];
      batchBytes = overhead + 2;
    }
    if (batchBytes + candleBytes > maximum) {
      throw new Error("One candle exceeds the chart update payload limit.");
    }
    batch.push(candle);
    batchBytes += candleBytes + (batch.length > 1 ? 1 : 0);
  }
  if (batch.length) chunks.push(batch);
  return chunks;
}

export function buildChartUpdateRanges(candles, timeframeSeconds, nowSeconds = Date.now() / 1000) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  if (!Number.isSafeInteger(timeframe) || timeframe < 1) {
    throw new Error("The RAW candle timeframe is invalid.");
  }
  if (!Array.isArray(candles) || candles.length === 0) return [];

  const ranges = [];
  for (let index = 1; index < candles.length; index++) {
    const previousTime = Number(candles[index - 1]?.time);
    const nextTime = Number(candles[index]?.time);
    const difference = nextTime - previousTime;
    if (!Number.isSafeInteger(previousTime) || !Number.isSafeInteger(nextTime)
      || difference <= 0 || difference % timeframe !== 0) {
      throw new Error("The RAW candle timestamps do not match the file timeframe.");
    }
    if (difference > timeframe) {
      ranges.push({
        kind: "gap",
        from: previousTime + timeframe,
        to: nextTime - timeframe,
        missingCandles: difference / timeframe - 1,
      });
    }
  }

  const latestFrom = Number(candles.at(-1)?.time) + timeframe;
  const latestTo = Math.floor(Number(nowSeconds) / timeframe) * timeframe;
  if (Number.isSafeInteger(latestFrom) && Number.isSafeInteger(latestTo) && latestFrom <= latestTo) {
    ranges.push({
      kind: "latest",
      from: latestFrom,
      to: latestTo,
      missingCandles: (latestTo - latestFrom) / timeframe + 1,
    });
  }
  return ranges;
}

export function buildGapDetectionRanges(candles, timeframeSeconds, { mode = "full", checkedThrough = null } = {}) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  if (!Number.isSafeInteger(timeframe) || timeframe < 1) throw new Error("The RAW candle timeframe is invalid.");
  if (!Array.isArray(candles) || candles.length < 2) return [];
  const checkpoint = mode === "since" && Number.isSafeInteger(Number(checkedThrough)) ? Number(checkedThrough) : null;
  const gaps = [];
  for (let index = 1; index < candles.length; index++) {
    const previousTime = Number(candles[index - 1]?.time);
    const nextTime = Number(candles[index]?.time);
    const difference = nextTime - previousTime;
    if (!Number.isSafeInteger(previousTime) || !Number.isSafeInteger(nextTime) || difference <= 0 || difference % timeframe !== 0) {
      throw new Error("The RAW candle timestamps do not match the file timeframe.");
    }
    if (difference <= timeframe || (checkpoint !== null && nextTime <= checkpoint)) continue;
    const from = Math.max(previousTime + timeframe, checkpoint === null ? previousTime + timeframe : checkpoint + timeframe);
    const to = nextTime - timeframe;
    if (from <= to) gaps.push({ kind: "gap", from, to, missingCandles: (to - from) / timeframe + 1 });
  }
  return gaps;
}

export function buildLatestCandleRange(candles, timeframeSeconds, nowSeconds = Date.now() / 1000) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  if (!Number.isSafeInteger(timeframe) || timeframe < 1) throw new Error("The RAW candle timeframe is invalid.");
  if (!Array.isArray(candles) || !candles.length) return null;
  const latestFrom = Number(candles.at(-1)?.time) + timeframe;
  const lastClosed = Math.floor(Number(nowSeconds) / timeframe) * timeframe - timeframe;
  if (!Number.isSafeInteger(latestFrom) || !Number.isSafeInteger(lastClosed) || latestFrom > lastClosed) return null;
  return { kind: "latest", from: latestFrom, to: lastClosed, missingCandles: (lastClosed - latestFrom) / timeframe + 1 };
}

function validCoverageRange(range, timeframeSeconds) {
  return Number.isSafeInteger(range?.from)
    && Number.isSafeInteger(range?.to)
    && range.from <= range.to
    && (range.to - range.from) % timeframeSeconds === 0;
}

function rangeWithCount(range, timeframeSeconds) {
  return {
    ...range,
    missingCandles: Math.floor((range.to - range.from) / timeframeSeconds) + 1,
  };
}

function subtractCoverageRange(range, coverage, timeframeSeconds) {
  if (coverage.to < range.from || coverage.from > range.to) return [range];
  const remaining = [];
  if (range.from < coverage.from) remaining.push({ ...range, to: coverage.from - timeframeSeconds });
  if (range.to > coverage.to) remaining.push({ ...range, from: coverage.to + timeframeSeconds });
  return remaining;
}

function subtractCheckedRanges(ranges, coverage, timeframeSeconds) {
  const checked = (coverage?.ranges || [])
    .filter((range) => validCoverageRange(range, timeframeSeconds))
    .sort((left, right) => left.from - right.from || left.to - right.to);
  let checkedIndex = 0;
  const pending = [];
  for (const range of ranges) {
    while (checkedIndex < checked.length && checked[checkedIndex].to < range.from) checkedIndex++;
    let cursor = range.from;
    for (let index = checkedIndex; index < checked.length && checked[index].from <= range.to; index++) {
      const verified = checked[index];
      if (verified.to < cursor) continue;
      if (cursor < verified.from) pending.push(rangeWithCount({ ...range, from: cursor, to: verified.from - timeframeSeconds }, timeframeSeconds));
      cursor = Math.max(cursor, verified.to + timeframeSeconds);
      if (cursor > range.to) break;
    }
    if (cursor <= range.to) pending.push(rangeWithCount({ ...range, from: cursor }, timeframeSeconds));
  }
  return pending;
}

/**
 * Drops only ranges that the FARAZ endpoint has already checked for this RAW
 * source timeframe. `source_missing` is retained in metadata too: it avoids
 * repeating a bounded request while leaving the visible local gap intact.
 */
export function buildUnverifiedChartUpdateRanges(candles, timeframeSeconds, nowSeconds, coverage = null) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  const allRanges = buildChartUpdateRanges(candles, timeframe, nowSeconds);
  if (!coverage || Math.trunc(Number(coverage.timeframeSeconds)) !== timeframe) return allRanges;
  return subtractCheckedRanges(allRanges, coverage, timeframe);
}

/** Audits every previously unchecked RAW source slot, including slots that
 * already contain candles. FARAZ coverage remains scoped to this one file. */
export function buildChartVerificationRanges(candles, timeframeSeconds, nowSeconds, coverage = null) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  if (!Number.isSafeInteger(timeframe) || timeframe < 1) throw new Error("The RAW candle timeframe is invalid.");
  if (!Array.isArray(candles) || !candles.length) return [];
  const first = Number(candles[0]?.time);
  const last = Number(candles.at(-1)?.time);
  const to = Math.floor(Number(nowSeconds) / timeframe) * timeframe;
  if (!Number.isSafeInteger(first) || !Number.isSafeInteger(last) || first > last) {
    throw new Error("The RAW candle timestamps are invalid.");
  }
  const ranges = [rangeWithCount({ kind: "audit", from: first, to: last }, timeframe)];
  if (Number.isSafeInteger(to) && last + timeframe <= to) {
    ranges.push(rangeWithCount({ kind: "latest", from: last + timeframe, to }, timeframe));
  }
  return coverage && Math.trunc(Number(coverage.timeframeSeconds)) === timeframe
    ? subtractCheckedRanges(ranges, coverage, timeframe)
    : ranges;
}

/**
 * Splits one FARAZ response into exact checked source-timeframe runs. This
 * makes an empty response durable evidence for its requested slots without
 * misrepresenting it as complete data.
 */
export function classifyFarazCoverage(candles, { from, to, timeframeSeconds } = {}) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  const first = Math.trunc(Number(from));
  const last = Math.trunc(Number(to));
  if (!Number.isSafeInteger(timeframe) || timeframe < 1
    || !Number.isSafeInteger(first) || !Number.isSafeInteger(last) || first > last
    || (last - first) % timeframe !== 0) {
    throw new Error("The FARAZ coverage range is invalid.");
  }
  const present = new Set((candles || [])
    .map((candle) => Number(candle?.time))
    .filter((time) => Number.isSafeInteger(time) && time >= first && time <= last && (time - first) % timeframe === 0));
  const ranges = [];
  let start = first;
  let status = present.has(first) ? "complete" : "source_missing";
  for (let time = first + timeframe; time <= last; time += timeframe) {
    const nextStatus = present.has(time) ? "complete" : "source_missing";
    if (nextStatus === status) continue;
    ranges.push({ from: start, to: time - timeframe, status });
    start = time;
    status = nextStatus;
  }
  ranges.push({ from: start, to: last, status });
  return ranges;
}

/** Keep the newest verification authoritative whenever a later check overlaps it. */
export function mergeFarazCoverageRanges(existingRanges, incomingRanges, timeframeSeconds) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  if (!Number.isSafeInteger(timeframe) || timeframe < 1) throw new Error("The FARAZ coverage timeframe is invalid.");
  let merged = (existingRanges || []).filter((range) => validCoverageRange(range, timeframe)).map((range) => ({ ...range }));
  for (const incoming of (incomingRanges || []).filter((range) => validCoverageRange(range, timeframe))) {
    merged = merged.flatMap((range) => subtractCoverageRange(range, incoming, timeframe));
    merged.push({ ...incoming });
  }
  return merged.sort((left, right) => left.from - right.from || left.to - right.to);
}

/** Executes independent FARAZ packets at a bounded concurrency in input order. */
export async function mapWithConcurrency(items, worker, maximumConcurrency = 6) {
  const queue = Array.isArray(items) ? items : [];
  const concurrency = Math.max(1, Math.min(queue.length || 1, Math.trunc(Number(maximumConcurrency)) || 1));
  const results = new Array(queue.length);
  let nextIndex = 0;
  await Promise.all(Array.from({ length: concurrency }, async () => {
    while (nextIndex < queue.length) {
      const index = nextIndex++;
      results[index] = await worker(queue[index], index);
    }
  }));
  return results;
}

export function buildChartUpdatePackets(ranges, timeframeSeconds, maximumCandlesPerPacket = 1_000) {
  const timeframe = Math.trunc(Number(timeframeSeconds));
  const maximum = Math.trunc(Number(maximumCandlesPerPacket));
  if (!Number.isSafeInteger(timeframe) || timeframe < 1
    || !Number.isSafeInteger(maximum) || maximum < 1) {
    throw new Error("The chart update packet settings are invalid.");
  }

  const pending = (ranges || [])
    .filter((range) => Number.isSafeInteger(range?.from) && Number.isSafeInteger(range?.to) && range.from <= range.to)
    .map((range) => ({ ...range }))
    .sort((left, right) => left.from - right.from);
  const packets = [];

  while (pending.length) {
    const packetFrom = pending[0].from;
    const packetLimit = packetFrom + (maximum - 1) * timeframe;
    const kinds = new Set();
    let packetTo = packetFrom;
    let targetMissingCandles = 0;

    while (pending.length && pending[0].from <= packetLimit) {
      const range = pending[0];
      const overlapTo = Math.min(range.to, packetLimit);
      targetMissingCandles += Math.floor((overlapTo - range.from) / timeframe) + 1;
      packetTo = Math.max(packetTo, overlapTo);
      kinds.add(range.kind);
      if (range.to <= packetLimit) pending.shift();
      else {
        range.from = overlapTo + timeframe;
        break;
      }
    }

    packets.push({
      from: packetFrom,
      to: packetTo,
      requestedCandles: Math.floor((packetTo - packetFrom) / timeframe) + 1,
      targetMissingCandles,
      kinds: [...kinds],
    });
  }

  return packets;
}

export function mergeChartCandles(existingCandles, incomingCandles) {
  const byTime = new Map();
  for (const candle of existingCandles || []) byTime.set(candle.time, candle);
  for (const candle of incomingCandles || []) {
    if (!byTime.has(candle.time)) byTime.set(candle.time, candle);
  }
  return [...byTime.values()].sort((left, right) => left.time - right.time);
}
