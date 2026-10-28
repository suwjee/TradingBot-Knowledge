const RAW_FILENAME_PATTERN = /^RAW ([A-Z0-9.-]+)_([A-Z0-9][A-Z0-9._-]*) (\d+[SMHD]) FROM (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}) TO (\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})\.json$/;

const tehranParts = new Intl.DateTimeFormat("en-CA", {
  timeZone: "Asia/Tehran", year: "numeric", month: "2-digit", day: "2-digit",
  hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23",
});

function partsAt(epochSeconds) {
  return tehranParts.formatToParts(new Date(Number(epochSeconds) * 1000))
    .reduce((result, part) => ((result[part.type] = part.value), result), {});
}

function safePart(value, label) {
  const result = String(value || "").trim().toUpperCase().replace(/:/g, "_");
  if (!result || !/^[A-Z0-9][A-Z0-9._-]*$/.test(result)) throw new Error(`The RAW ${label} is invalid.`);
  return result;
}

export function formatTehranFileTime(epochSeconds) {
  if (!Number.isSafeInteger(Number(epochSeconds)) || Number(epochSeconds) <= 0) throw new Error("The RAW candle time is invalid.");
  const parts = partsAt(epochSeconds);
  return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}-${parts.minute}-${parts.second}`;
}

export function formatTehranMetadataTime(epochSeconds) {
  return `${formatTehranFileTime(epochSeconds).replace(/ (\d{2})-(\d{2})-(\d{2})$/, " $1:$2:$3")} Asia/Tehran`;
}

export function parseTehranMetadataTime(value) {
  const match = String(value || "").trim().match(/^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) Asia\/Tehran$/);
  if (!match) return NaN;
  const desiredUtc = Date.UTC(+match[1], +match[2] - 1, +match[3], +match[4], +match[5], +match[6]);
  let candidate = Math.floor(desiredUtc / 1000);
  for (let attempt = 0; attempt < 2; attempt++) {
    const parts = partsAt(candidate);
    const renderedUtc = Date.UTC(+parts.year, +parts.month - 1, +parts.day, +parts.hour, +parts.minute, +parts.second);
    candidate += Math.round((desiredUtc - renderedUtc) / 1000);
  }
  return formatTehranMetadataTime(candidate) === String(value).trim() ? candidate : NaN;
}

export function buildRawFilename({ broker, symbol, timeframe, firstTime, lastTime }) {
  const normalizedBroker = safePart(broker, "broker");
  const normalizedSymbol = safePart(symbol, "symbol");
  const normalizedTimeframe = String(timeframe || "").trim().toUpperCase();
  if (!/^\d+[SMHD]$/.test(normalizedTimeframe)) throw new Error("The RAW timeframe is invalid.");
  return `RAW ${normalizedBroker}_${normalizedSymbol} ${normalizedTimeframe} FROM ${formatTehranFileTime(firstTime)} TO ${formatTehranFileTime(lastTime)}.json`;
}

export function parseRawFilename(filename) {
  const match = String(filename || "").match(RAW_FILENAME_PATTERN);
  if (!match || match[1] === "FARAZ") return null;
  return { broker: match[1], symbol: match[2], timeframe: match[3], fromTehran: match[4], toTehran: match[5] };
}
