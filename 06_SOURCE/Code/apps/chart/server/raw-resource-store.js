import fs from "node:fs";
import path from "node:path";
import { createHash, randomUUID } from "node:crypto";
import { mergeFarazCoverageRanges } from "../src/features/candle-update.js";
import { buildRawFilename, formatTehranMetadataTime, parseRawFilename, parseTehranMetadataTime } from "../src/features/raw-file-contract.js";

const CANDLE_KEYS = ["time", "open", "high", "low", "close"];

function segment(value, fallback) {
  const result = String(value || "").trim().replace(/[^a-zA-Z0-9._-]+/g, "_").replace(/^_+|_+$/g, "").slice(0, 80);
  return result || fallback;
}

function assertCandles(candles) {
  if (!Array.isArray(candles) || !candles.length) throw new Error("RAW candles must be a non-empty array.");
  candles.forEach((row, index) => {
    if (!row || Object.keys(row).length !== CANDLE_KEYS.length || !CANDLE_KEYS.every((key) => Object.hasOwn(row, key))) throw new Error(`RAW candle ${index + 1} has an invalid schema.`);
    const candle = Object.fromEntries(CANDLE_KEYS.map((key) => [key, Number(row[key])]));
    if (!Number.isSafeInteger(candle.time) || candle.time <= 0 || ![candle.open, candle.high, candle.low, candle.close].every(Number.isFinite)
      || candle.high < Math.max(candle.open, candle.close, candle.low) || candle.low > Math.min(candle.open, candle.close, candle.high)
      || (index && candle.time <= Number(candles[index - 1].time))) throw new Error(`RAW candle ${index + 1} failed chronology or OHLC validation.`);
  });
}

function atomicWrite(filePath, text) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const temporary = path.join(path.dirname(filePath), `.${path.basename(filePath)}.${randomUUID()}.tmp`);
  fs.writeFileSync(temporary, text, "utf8");
  try {
    if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
    fs.renameSync(temporary, filePath);
  } finally {
    if (fs.existsSync(temporary)) fs.unlinkSync(temporary);
  }
}

function safeId(id) {
  const normalized = String(id || "").replaceAll("\\", "/");
  if (!normalized || normalized.startsWith("/") || normalized.split("/").some((part) => !part || part === "." || part === "..")) return null;
  return normalized;
}

function sidecarPath(dataPath) { return `${dataPath}.meta.json`; }

function validChartId(value) {
  const id = String(value || "").trim();
  return /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id) ? id : null;
}

function readableRange(range) {
  if (!range || !Number.isSafeInteger(Number(range.from)) || !Number.isSafeInteger(Number(range.to))) return null;
  return { from: formatTehranMetadataTime(Number(range.from)), to: formatTehranMetadataTime(Number(range.to)) };
}

function runtimeRange(range) {
  if (!range) return null;
  const from = typeof range.from === "number" ? range.from : parseTehranMetadataTime(range.from);
  const to = typeof range.to === "number" ? range.to : parseTehranMetadataTime(range.to);
  return Number.isSafeInteger(from) && Number.isSafeInteger(to) ? { from, to } : null;
}

function readableCoverage(coverage) {
  if (!coverage) return undefined;
  return {
    ...coverage,
    checkedFrom: Number.isSafeInteger(coverage.checkedFrom) ? formatTehranMetadataTime(coverage.checkedFrom) : null,
    checkedTo: Number.isSafeInteger(coverage.checkedTo) ? formatTehranMetadataTime(coverage.checkedTo) : null,
    checkedThrough: Number.isSafeInteger(coverage.checkedThrough) ? formatTehranMetadataTime(coverage.checkedThrough) : null,
    verifiedAt: typeof coverage.verifiedAt === "string"
      ? coverage.verifiedAt
      : formatTehranMetadataTime(Math.floor(Date.now() / 1000)),
    ranges: (coverage.ranges || []).map((range) => ({ ...range, ...readableRange(range) })),
  };
}

function runtimeCoverage(coverage) {
  if (!coverage) return undefined;
  return {
    ...coverage,
    checkedFrom: typeof coverage.checkedFrom === "number" ? coverage.checkedFrom : parseTehranMetadataTime(coverage.checkedFrom),
    checkedTo: typeof coverage.checkedTo === "number" ? coverage.checkedTo : parseTehranMetadataTime(coverage.checkedTo),
    checkedThrough: typeof coverage.checkedThrough === "number" ? coverage.checkedThrough : parseTehranMetadataTime(coverage.checkedThrough),
    ranges: (coverage.ranges || []).map((range) => ({ ...range, ...runtimeRange(range) })).filter((range) => Number.isSafeInteger(range.from) && Number.isSafeInteger(range.to)),
  };
}

function runtimeMetadata(metadata) {
  const actualRange = runtimeRange(metadata.actualRange || metadata.effectiveRange);
  return { ...metadata, actualRange, effectiveRange: actualRange, requestedRange: runtimeRange(metadata.requestedRange), farazCoverage: runtimeCoverage(metadata.farazCoverage) };
}

function persistedMetadata({ broker, symbol, timeframe, source, filename, candles, serialized, requestedRange = null, farazCoverage, createdAt, updatedAt, previousSha256, chartId }) {
  const now = formatTehranMetadataTime(Math.floor(Date.now() / 1000));
  const dataSha256 = createHash("sha256").update(serialized).digest("hex");
  return {
    schemaVersion: 2,
    chartId: validChartId(chartId) || randomUUID(),
    broker,
    symbol,
    timeframe,
    source,
    filename,
    candleCount: candles.length,
    count: candles.length,
    dataBytes: Buffer.byteLength(serialized),
    dataSha256,
    requestedRange: readableRange(requestedRange),
    actualRange: readableRange({ from: candles[0].time, to: candles.at(-1).time }),
    createdAt: createdAt || now,
    updatedAt: previousSha256 === dataSha256 && typeof updatedAt === "string" ? updatedAt : now,
    ...(farazCoverage ? { farazCoverage: readableCoverage(runtimeCoverage(farazCoverage)) } : {}),
  };
}

export function createRawResourceStore({ rootDir }) {
  const root = path.resolve(rootDir);
  const inventoryCache = new Map();

  function inventorySignature(dataPath, metaPath) {
    const data = fs.statSync(dataPath);
    const metadata = fs.existsSync(metaPath) ? fs.statSync(metaPath) : null;
    return `${data.size}:${data.mtimeMs}:${metadata?.size || 0}:${metadata?.mtimeMs || 0}`;
  }

  function resolve(id) {
    const logicalId = safeId(id);
    if (!logicalId || !logicalId.toLowerCase().endsWith(".json") || logicalId.toLowerCase().endsWith(".meta.json")) return null;
    const dataPath = path.resolve(root, ...logicalId.split("/"));
    if (!dataPath.startsWith(`${root}${path.sep}`) || !fs.existsSync(dataPath)) return null;
    return { id: logicalId, dataPath, metaPath: sidecarPath(dataPath) };
  }

  function write({ broker, symbol, timeframe, candles, requestedRange = null, source = "local", chartId = null, farazCoverage = undefined, createdAt = undefined }) {
    assertCandles(candles);
    const brokerSegment = segment(broker, "UNKNOWN").toUpperCase();
    const symbolSegment = segment(symbol, "UNNAMED").toUpperCase();
    const normalizedTimeframe = String(timeframe || "UNKNOWN").toUpperCase();
    const filename = buildRawFilename({ broker: brokerSegment, symbol: symbolSegment, timeframe: normalizedTimeframe, firstTime: candles[0].time, lastTime: candles.at(-1).time });
    const id = `${brokerSegment}/${symbolSegment}/${filename}`;
    const dataPath = path.join(root, brokerSegment, symbolSegment, filename);
    const serialized = JSON.stringify(candles);
    if (fs.existsSync(dataPath)) {
      if (fs.readFileSync(dataPath, "utf8") !== serialized) throw new Error(`A different RAW file already exists at ${id}.`);
    } else {
      atomicWrite(dataPath, serialized);
    }
    let existing = {};
    const metadataPath = sidecarPath(dataPath);
    if (fs.existsSync(metadataPath)) {
      try { existing = JSON.parse(fs.readFileSync(metadataPath, "utf8")) || {}; } catch { existing = {}; }
    }
    const metadata = persistedMetadata({
      broker: brokerSegment, symbol: symbolSegment, timeframe: normalizedTimeframe, source, filename, candles, serialized, requestedRange,
      farazCoverage: farazCoverage ?? existing.farazCoverage, chartId: chartId || existing.chartId, createdAt: createdAt || existing.createdAt,
      updatedAt: existing.updatedAt, previousSha256: existing.dataSha256,
    });
    atomicWrite(sidecarPath(dataPath), `${JSON.stringify(metadata, null, 2)}\n`);
    inventoryCache.delete(id);
    return { id, dataPath, metaPath: sidecarPath(dataPath), ...runtimeMetadata(metadata), chartId: metadata.chartId, count: candles.length, bytes: Buffer.byteLength(serialized) };
  }

  function list() {
    if (!fs.existsSync(root)) return [];
    const items = [];
    const seen = new Set();
    const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).forEach((entry) => {
      const target = path.join(dir, entry.name);
      if (entry.isDirectory()) return walk(target);
      if (!entry.isFile() || !entry.name.endsWith(".json") || entry.name.endsWith(".meta.json")) return;
      const id = path.relative(root, target).split(path.sep).join("/");
      const identity = parseRawFilename(entry.name);
      if (!safeId(id) || !identity) return;
      seen.add(id);
      const metaPath = sidecarPath(target);
      const signature = inventorySignature(target, metaPath);
      const cached = inventoryCache.get(id);
      if (cached?.signature === signature) {
        if (cached.item) items.push(cached.item);
        return;
      }
      try {
        const serialized = fs.readFileSync(target, "utf8");
        const candles = JSON.parse(serialized);
        assertCandles(candles);
        let previous = {};
        if (fs.existsSync(metaPath)) {
          try { previous = JSON.parse(fs.readFileSync(metaPath, "utf8")) || {}; } catch { previous = {}; }
        }
        const hydratedPrevious = runtimeMetadata(previous);
        const metadata = persistedMetadata({ broker: identity.broker, symbol: identity.symbol, timeframe: identity.timeframe, source: previous.source || "import", filename: entry.name, candles, serialized, requestedRange: hydratedPrevious.requestedRange, farazCoverage: previous.farazCoverage, chartId: previous.chartId, createdAt: typeof previous.createdAt === "string" ? previous.createdAt : undefined, updatedAt: previous.updatedAt, previousSha256: previous.dataSha256 });
        if (JSON.stringify(previous) !== JSON.stringify(metadata)) atomicWrite(metaPath, `${JSON.stringify(metadata, null, 2)}\n`);
        const stat = fs.statSync(target);
        const item = { id, dataPath: target, metaPath, broker: identity.broker, symbol: identity.symbol, timeframe: identity.timeframe, chartId: metadata.chartId, from: candles[0].time, to: candles.at(-1).time, count: candles.length, bytes: stat.size, savedAt: stat.mtimeMs, metadata: runtimeMetadata(metadata), createdAt: metadata.createdAt, updatedAt: metadata.updatedAt };
        inventoryCache.set(id, { signature: inventorySignature(target, metaPath), item });
        items.push(item);
      } catch {
        inventoryCache.set(id, { signature, item: null });
      }
    });
    walk(root);
    for (const id of inventoryCache.keys()) {
      if (!seen.has(id)) inventoryCache.delete(id);
    }
    return items.sort((a, b) => a.symbol.localeCompare(b.symbol) || b.savedAt - a.savedAt || a.id.localeCompare(b.id));
  }

  function read(id) {
    const item = resolve(id);
    if (!item) return null;
    const candles = JSON.parse(fs.readFileSync(item.dataPath, "utf8"));
    assertCandles(candles);
    return candles;
  }

  function cut(id, { from, to, mode = "replace" } = {}) {
    if (!Number.isSafeInteger(Number(from)) || !Number.isSafeInteger(Number(to)) || Number(from) > Number(to)) {
      throw new Error("The cut range must be ordered and use valid candle times.");
    }
    if (!["replace", "new"].includes(mode)) throw new Error("The cut mode is invalid.");
    const item = resolve(id);
    if (!item) throw new Error("Candle file was not found.");
    const identity = parseRawFilename(path.basename(item.dataPath));
    if (!identity) throw new Error("The existing RAW filename does not follow the required contract.");
    const candles = read(id);
    const selected = candles.filter((candle) => candle.time >= Number(from) && candle.time <= Number(to));
    if (!selected.length) throw new Error("The cut range contains no candles.");
    const filename = buildRawFilename({
      broker: identity.broker,
      symbol: identity.symbol,
      timeframe: identity.timeframe,
      firstTime: selected[0].time,
      lastTime: selected.at(-1).time,
    });
    const directoryId = path.posix.dirname(item.id);
    const newId = directoryId === "." ? filename : `${directoryId}/${filename}`;
    if (mode === "new" && newId === item.id) throw new Error("A new cut file must change the selected range.");
    if (newId !== item.id && resolve(newId)) throw new Error("A candle file with the cut range already exists.");
    let previous = {};
    if (fs.existsSync(item.metaPath)) {
      try { previous = JSON.parse(fs.readFileSync(item.metaPath, "utf8")) || {}; } catch { previous = {}; }
    }
    const written = write({
      broker: identity.broker,
      symbol: identity.symbol,
      timeframe: identity.timeframe,
      candles: selected,
      source: previous.source || "cut",
      chartId: mode === "replace" ? previous.chartId : null,
      createdAt: mode === "replace" ? previous.createdAt : undefined,
    });
    if (mode === "replace" && newId !== item.id) {
      if (fs.existsSync(item.dataPath)) fs.unlinkSync(item.dataPath);
      if (fs.existsSync(item.metaPath)) fs.unlinkSync(item.metaPath);
    }
    const result = list().find((candidate) => candidate.id === written.id) || written;
    return { oldId: item.id, newId: result.id, mode, chartId: result.chartId, count: result.count, metadata: result.metadata };
  }

  function recordFarazCoverage(id, { timeframeSeconds, retryCount = 0, ranges = [], effectiveRange = null, checkedThrough = null, mode = null } = {}) {
    const item = resolve(id);
    const timeframe = Math.trunc(Number(timeframeSeconds));
    if (!item || !Number.isSafeInteger(timeframe) || timeframe < 1) return null;
    const candles = read(id);
    let previous = {};
    if (fs.existsSync(item.metaPath)) {
      try { previous = JSON.parse(fs.readFileSync(item.metaPath, "utf8")) || {}; } catch { previous = {}; }
    }
    const hydrated = runtimeMetadata(previous);
    const priorRanges = hydrated.farazCoverage?.timeframeSeconds === timeframe ? hydrated.farazCoverage.ranges || [] : [];
    const incoming = ranges.map((range) => ({ from: Math.trunc(Number(range?.from)), to: Math.trunc(Number(range?.to)), status: range?.status === "complete" ? "complete" : "source_missing", retryCount: Math.max(0, Math.trunc(Number(retryCount) || 0)) }));
    const mergedRanges = mergeFarazCoverageRanges(priorRanges, incoming, timeframe);
    const checkedFrom = mergedRanges.length ? Math.min(...mergedRanges.map((range) => range.from)) : null;
    const checkedTo = mergedRanges.length ? Math.max(...mergedRanges.map((range) => range.to)) : null;
    const fileRange = runtimeRange(effectiveRange) || { from: candles[0].time, to: candles.at(-1).time };
    let contiguousThrough = fileRange.from;
    for (const range of mergedRanges) {
      if (range.to < contiguousThrough) continue;
      if (range.from > contiguousThrough) break;
      contiguousThrough = Math.max(contiguousThrough, range.to + timeframe);
      if (contiguousThrough > fileRange.to) break;
    }
    const durableCheckpoint = checkedThrough !== null && checkedThrough !== "" && Number.isSafeInteger(Number(checkedThrough))
      ? Number(checkedThrough)
      : Number.isSafeInteger(hydrated.farazCoverage?.checkedThrough) ? hydrated.farazCoverage.checkedThrough : null;
    const chartUpToDate = durableCheckpoint !== null ? durableCheckpoint >= fileRange.to : contiguousThrough > fileRange.to;
    const coverage = { schemaVersion: 2, timeframeSeconds: timeframe, chartUpToDate, status: chartUpToDate ? "faraz_checked" : "unchecked_ranges_remain", checkedFrom, checkedTo, checkedThrough: durableCheckpoint, lastMode: mode || hydrated.farazCoverage?.lastMode || null, retryCount: Math.max(0, Math.trunc(Number(retryCount) || 0)), ranges: mergedRanges };
    const identity = parseRawFilename(path.basename(item.dataPath));
    const serialized = fs.readFileSync(item.dataPath, "utf8");
    const metadata = persistedMetadata({ broker: identity.broker, symbol: identity.symbol, timeframe: identity.timeframe, source: previous.source || "local", filename: path.basename(item.dataPath), candles, serialized, requestedRange: hydrated.requestedRange, farazCoverage: coverage, chartId: previous.chartId, createdAt: previous.createdAt });
    atomicWrite(item.metaPath, `${JSON.stringify(metadata, null, 2)}\n`);
    inventoryCache.delete(item.id);
    return runtimeMetadata(metadata);
  }

  function remove(id) {
    const item = resolve(id);
    if (!item) return false;
    fs.unlinkSync(item.dataPath);
    if (fs.existsSync(item.metaPath)) fs.unlinkSync(item.metaPath);
    inventoryCache.delete(item.id);
    return true;
  }
  return { root, resolve, write, list, read, cut, recordFarazCoverage, remove };
}
