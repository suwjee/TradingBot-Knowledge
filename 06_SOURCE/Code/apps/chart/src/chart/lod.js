export function lowerBoundTime(rows, time) {
  let low = 0;
  let high = rows.length;
  while (low < high) {
    const middle = low + Math.floor((high - low) / 2);
    if (Number(rows[middle].time) < time) low = middle + 1;
    else high = middle;
  }
  return low;
}

export function chooseLodStride(visibleCount, viewportWidth, targetBarsPerPixel = 2) {
  const target = Math.max(1, Math.floor(Number(viewportWidth) * targetBarsPerPixel));
  const required = Math.max(1, Math.ceil(Number(visibleCount) / target));
  return 2 ** Math.ceil(Math.log2(required));
}

// This is display-only aggregation. The original candle array remains the
// canonical source for exports, calculations, dates, and exact OHLC lookup.
export function buildCandleLod(rows, startIndex, endIndex, stride) {
  const start = Math.max(0, Math.floor(startIndex / stride) * stride);
  const end = Math.min(rows.length, Math.max(start, endIndex));
  if (stride <= 1) return rows.slice(start, end);
  const output = [];
  for (let index = start; index < end; index += stride) {
    const first = rows[index];
    if (!first) continue;
    let high = Number(first.high);
    let low = Number(first.low);
    let last = first;
    const limit = Math.min(end, index + stride);
    for (let cursor = index + 1; cursor < limit; cursor++) {
      const candle = rows[cursor];
      high = Math.max(high, Number(candle.high));
      low = Math.min(low, Number(candle.low));
      last = candle;
    }
    output.push({
      time: Number(first.time),
      open: Number(first.open),
      high,
      low,
      close: Number(last.close),
    });
  }
  return output;
}
