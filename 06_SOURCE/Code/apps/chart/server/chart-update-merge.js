// Both inputs have passed strict chronological validation before this merge.
// Existing RAW owns timestamp ties, matching the previous Map-based update.
export function mergeChartUpdateCandles(existing, incoming) {
  const candles = [];
  let oldIndex = 0;
  let newIndex = 0;
  let added = 0;
  let ignoredExisting = 0;

  while (oldIndex < existing.length && newIndex < incoming.length) {
    const oldRow = existing[oldIndex];
    const newRow = incoming[newIndex];
    if (oldRow.time <= newRow.time) {
      candles.push(oldRow);
      oldIndex++;
      if (oldRow.time === newRow.time) {
        ignoredExisting++;
        newIndex++;
      }
    } else {
      candles.push(newRow);
      newIndex++;
      added++;
    }
  }
  while (oldIndex < existing.length) candles.push(existing[oldIndex++]);
  while (newIndex < incoming.length) {
    candles.push(incoming[newIndex++]);
    added++;
  }
  return { candles, added, ignoredExisting };
}
