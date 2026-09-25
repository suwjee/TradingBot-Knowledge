import net from "node:net";
import { randomUUID } from "node:crypto";

function bucketTime(value, timeframeSeconds) {
  return Math.floor(Number(value) / timeframeSeconds) * timeframeSeconds;
}

export function prepareIndicatorRangeInput(rows, { from, to, chartTimeframeSeconds } = {}) {
  const start = Number(from);
  const end = Number(to);
  const timeframe = Number(chartTimeframeSeconds);
  if (!Array.isArray(rows) || !rows.length) throw new Error("The selected RAW source contains no candles.");
  if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start > end) {
    throw new Error("The indicator range must use ordered candle times.");
  }
  if (!Number.isSafeInteger(timeframe) || timeframe < 1) {
    throw new Error("The chart timeframe must be a positive whole number of seconds.");
  }
  if (bucketTime(start, timeframe) !== start || bucketTime(end, timeframe) !== end) {
    throw new Error("The indicator range must use chart-candle boundaries.");
  }

  const sourceFrom = bucketTime(rows[0].time, timeframe);
  const sourceTo = bucketTime(rows.at(-1).time, timeframe);
  if (start < sourceFrom || end > sourceTo) {
    throw new Error("The indicator range is outside the available chart candles.");
  }
  if (start === sourceFrom && end === sourceTo) {
    return { rows, usesCompleteSource: true };
  }

  const selected = rows.filter((row) => {
    const bucket = bucketTime(row?.time, timeframe);
    return bucket >= start && bucket <= end;
  });
  if (!selected.length
    || bucketTime(selected[0].time, timeframe) !== start
    || bucketTime(selected.at(-1).time, timeframe) !== end) {
    throw new Error("The indicator range endpoints are no longer available. Reload the chart and select the range again.");
  }
  return { rows: selected, usesCompleteSource: false };
}

export async function withIndicatorRangePipe(rows, consume) {
  if (process.platform !== "win32") {
    throw new Error("In-memory ranged indicator input requires Windows named-pipe support.");
  }
  if (!Array.isArray(rows) || !rows.length || typeof consume !== "function") {
    throw new Error("A non-empty indicator range and consumer are required.");
  }

  const pipePath = `\\\\.\\pipe\\tradingbot-indicator-range-${process.pid}-${randomUUID()}`;
  const payload = Buffer.from(JSON.stringify(rows), "utf8");
  const sockets = new Set();
  let rejectTransport;
  let transportSettled = false;
  const transportFailure = new Promise((_, reject) => { rejectTransport = reject; });
  const failTransport = (error) => {
    if (transportSettled) return;
    const failure = new Error(`Indicator range pipe failed: ${error.message}`);
    failure.cause = error;
    rejectTransport(failure);
  };
  const server = net.createServer((socket) => {
    sockets.add(socket);
    socket.once("close", () => sockets.delete(socket));
    socket.once("error", failTransport);
    socket.end(payload);
  });

  await new Promise((resolve, reject) => {
    const onError = (error) => reject(error);
    server.once("error", onError);
    server.listen(pipePath, () => {
      server.off("error", onError);
      resolve();
    });
  });
  server.on("error", failTransport);

  try {
    return await Promise.race([
      Promise.resolve().then(() => consume(pipePath)),
      transportFailure,
    ]);
  } finally {
    transportSettled = true;
    for (const socket of sockets) socket.destroy();
    await new Promise((resolve) => server.close(resolve));
  }
}

export async function runIndicatorRangeCalculation({
  rows,
  sourcePath,
  from,
  to,
  chartTimeframeSeconds,
  onPrepared = () => {},
  run,
} = {}) {
  if (typeof sourcePath !== "string" || !sourcePath || typeof run !== "function") {
    throw new Error("The indicator calculation source and runner are required.");
  }
  const prepared = prepareIndicatorRangeInput(rows, { from, to, chartTimeframeSeconds });
  const bounds = {
    fromTime: Number(from),
    toTime: Number(prepared.rows.at(-1).time),
    usesCompleteSource: prepared.usesCompleteSource,
    rowCount: prepared.rows.length,
  };
  onPrepared(bounds);
  if (prepared.usesCompleteSource) return run(sourcePath, bounds);
  return withIndicatorRangePipe(prepared.rows, (pipePath) => run(pipePath, bounds));
}
