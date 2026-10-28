function numericTime(row) {
  return Number(row?.time);
}

export function rawIndexAtTime(rows, time) {
  if (!rows.length) return null;
  const target = Number(time);
  if (!Number.isFinite(target)) return null;
  if (rows.length === 1) return 0;
  if (target <= numericTime(rows[0])) {
    const span = numericTime(rows[1]) - numericTime(rows[0]) || 1;
    return (target - numericTime(rows[0])) / span;
  }
  const last = rows.length - 1;
  if (target >= numericTime(rows[last])) {
    const span = numericTime(rows[last]) - numericTime(rows[last - 1]) || 1;
    return last + (target - numericTime(rows[last])) / span;
  }
  let lo = 0;
  let hi = last;
  while (lo + 1 < hi) {
    const mid = (lo + hi) >> 1;
    if (numericTime(rows[mid]) <= target) lo = mid;
    else hi = mid;
  }
  const start = numericTime(rows[lo]);
  const span = numericTime(rows[hi]) - start || 1;
  return lo + (target - start) / span;
}

function interpolate(value, anchors, inputKey, outputKey) {
  if (!anchors?.length) return null;
  if (anchors.length === 1) return Number(anchors[0][outputKey]);
  let upper = anchors.findIndex((anchor) => Number(anchor[inputKey]) >= value);
  if (upper < 0) upper = anchors.length - 1;
  if (upper === 0) upper = 1;
  const left = anchors[upper - 1];
  const right = anchors[upper];
  const from = Number(left[inputKey]);
  const span = Number(right[inputKey]) - from;
  if (!Number.isFinite(span) || span === 0) return Number(left[outputKey]);
  const ratio = (value - from) / span;
  return Number(left[outputKey]) + ratio * (Number(right[outputKey]) - Number(left[outputKey]));
}

export function rawTimeToCoordinate(rows, time, anchors) {
  const rawIndex = rawIndexAtTime(rows, time);
  return rawIndex == null ? null : interpolate(rawIndex, anchors, "rawIndex", "coordinate");
}

export function coordinateToRawTime(rows, coordinate, anchors) {
  if (!rows.length || !Number.isFinite(Number(coordinate))) return null;
  const rawIndex = interpolate(Number(coordinate), anchors, "coordinate", "rawIndex");
  if (rawIndex == null) return null;
  const index = Math.max(0, Math.min(rows.length - 1, Math.round(rawIndex)));
  return numericTime(rows[index]);
}

export function createViewAnchorCache() {
  let entry = null;
  return {
    get(revision, display, build) {
      if (entry?.revision === revision && entry.display === display) return entry.anchors;
      const anchors = build();
      entry = { revision, display, anchors };
      return anchors;
    },
    invalidate() {
      entry = null;
    },
  };
}

export function selectDensityMode({ candlesPerPixel, previous = "exact", gestureActive = false }) {
  if (gestureActive) return previous;
  const density = Number(candlesPerPixel) || 0;
  if (previous === "extreme") return density < 6.4 ? (density < 1.6 ? "exact" : "dense") : "extreme";
  if (previous === "dense") return density >= 8 ? "extreme" : density < 1.6 ? "exact" : "dense";
  return density >= 8 ? "extreme" : density > 2 ? "dense" : "exact";
}
