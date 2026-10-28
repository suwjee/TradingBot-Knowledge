const TRANSFER_KIND = "tradingbot-chart-transfer";
const TRANSFER_VERSION = 1;
const CANDLE_KEYS = ["time", "open", "high", "low", "close"];

function invalid(message) {
  throw new Error(`Invalid chart transfer bundle: ${message}`);
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function safeBundleFile(value) {
  return typeof value === "string"
    && value.length > 0
    && value.length <= 180
    && value.endsWith(".json")
    && !value.includes("/")
    && !value.includes("\\")
    && value !== ".json"
    && value !== "..json";
}

function safeSourceId(value) {
  if (typeof value !== "string" || !value || value.startsWith("/") || value.includes("\\")) return false;
  return value.split("/").every((part) => part && part !== "." && part !== "..");
}

function validCandles(candles) {
  if (!Array.isArray(candles) || !candles.length) return false;
  return candles.every((row, index) => {
    if (!isPlainObject(row) || Object.keys(row).length !== CANDLE_KEYS.length || !CANDLE_KEYS.every((key) => Object.hasOwn(row, key))) return false;
    const values = CANDLE_KEYS.map((key) => Number(row[key]));
    const [time, open, high, low, close] = values;
    return Number.isSafeInteger(time) && time > 0
      && [open, high, low, close].every(Number.isFinite)
      && high >= Math.max(open, close, low)
      && low <= Math.min(open, close, high)
      && (!index || time > Number(candles[index - 1].time));
  });
}

export function createChartTransferBundle({ item, candles, drawings, drawingFilename = "drawings.json" }) {
  if (!isPlainObject(item) || typeof item.id !== "string" || !safeSourceId(item.id)) invalid("RAW identity is missing");
  if (typeof item.broker !== "string" || typeof item.symbol !== "string" || typeof item.timeframe !== "string") invalid("chart identity is incomplete");
  if (!validCandles(candles)) invalid("RAW candles are invalid");
  if (!Array.isArray(drawings)) invalid("drawings must be an array");
  if (!safeBundleFile(drawingFilename)) invalid("drawing filename is unsafe");
  return {
    kind: TRANSFER_KIND,
    version: TRANSFER_VERSION,
    manifest: {
      broker: item.broker,
      symbol: item.symbol,
      timeframe: item.timeframe,
      sourceId: item.id,
      sourceFilename: item.id.split("/").at(-1),
      rawFile: item.id.split("/").at(-1),
      metadataFile: `${item.id.split("/").at(-1)}.meta.json`,
      drawingsFile: drawingFilename,
    },
    raw: candles,
    metadata: isPlainObject(item.metadata) ? item.metadata : {},
    drawings,
  };
}

export function validateChartTransferBundle(bundle) {
  if (!isPlainObject(bundle) || bundle.kind !== TRANSFER_KIND || bundle.version !== TRANSFER_VERSION
    || !isPlainObject(bundle.manifest) || !validCandles(bundle.raw) || !Array.isArray(bundle.drawings)
    || !isPlainObject(bundle.metadata)) invalid("kind, version, manifest, RAW, metadata, or drawings are invalid");
  const { broker, symbol, timeframe, sourceId, rawFile, metadataFile, drawingsFile } = bundle.manifest;
  if ([broker, symbol, timeframe].some((value) => typeof value !== "string" || !value.trim())
    || !safeSourceId(sourceId)
    || !safeBundleFile(rawFile)
    || !safeBundleFile(metadataFile)
    || !safeBundleFile(drawingsFile)) invalid("manifest identity or filenames are unsafe");
  if (bundle.drawings.some((drawing) => !isPlainObject(drawing))) invalid("drawings must contain objects");
  return bundle;
}

export function importChartTransferBundle({ bundle, rawStore, saveDrawings }) {
  const validated = validateChartTransferBundle(bundle);
  if (!rawStore || typeof rawStore.write !== "function" || typeof saveDrawings !== "function") {
    throw new Error("Invalid chart transfer destination");
  }
  const item = rawStore.write({
    broker: validated.manifest.broker,
    symbol: validated.manifest.symbol,
    timeframe: validated.manifest.timeframe,
    candles: validated.raw,
    requestedRange: validated.metadata.requestedRange || null,
    chartId: validated.metadata.chartId || null,
    farazCoverage: validated.metadata.farazCoverage,
    createdAt: validated.metadata.createdAt,
    source: "transfer",
  });
  saveDrawings(item, validated.drawings);
  return { item, drawings: validated.drawings.length };
}

export const chartTransferConstants = Object.freeze({ kind: TRANSFER_KIND, version: TRANSFER_VERSION });
