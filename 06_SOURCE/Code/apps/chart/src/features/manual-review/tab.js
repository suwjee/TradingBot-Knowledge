export function calculationInfoPath(context = {}) {
  const id = String(context.calculationId || "");
  if (!/^[a-zA-Z0-9._-]+\/\d+s\/(bullish|bearish)\/\d+-\d+--[a-f0-9]{16}\.json$/.test(id)) {
    throw new Error("This calculation has no persisted report identity. Calculate again first.");
  }
  return `/info/${id}`;
}

export function openManualReviewTab(context, host = window) {
  return host.open(calculationInfoPath(context), "_blank");
}
