const CONTEXT_KEYS = [
  "fileId",
  "symbol",
  "chartTimeframe",
  "analysisTimeframe",
  "from",
  "to",
  "direction",
];

export function restoreIndicatorLifecycle(saved) {
  return {
    form: saved?.form && typeof saved.form === "object" ? saved.form : null,
    from: typeof saved?.from === "string" ? saved.from : "",
    to: typeof saved?.to === "string" ? saved.to : "",
    active: false,
    resultContext: null,
  };
}

export function appliedContextMatches(applied, next) {
  return Boolean(applied && next)
    && CONTEXT_KEYS.every((key) => applied[key] === next[key]);
}

export function canReuseAppliedCalculation(applied, next, currentSourceFingerprint) {
  const hasIdentity = value => typeof value === "string" && value.trim().length > 0;
  return appliedContextMatches(applied, next)
    && hasIdentity(applied.sourceFingerprint)
    && hasIdentity(currentSourceFingerprint)
    && applied.sourceFingerprint === currentSourceFingerprint;
}

export function captureCalculationInputs({ file, chartTimeframe, raw, data, settings,
  from, to, enabled, results, resultContext }) {
  return Object.freeze({
    fileIdentity: JSON.stringify([file?.id, file?.chartId, file?.symbol, file?.timeframe,
      file?.from, file?.to, file?.count, file?.bytes, file?.savedAt]),
    chartTimeframe, raw, data,
    rawLength: raw?.length, rawFirst: raw?.[0]?.time, rawLast: raw?.[raw.length - 1]?.time,
    dataLength: data?.length, dataFirst: data?.[0]?.time, dataLast: data?.[data.length - 1]?.time,
    settingsIdentity: JSON.stringify(settings), from, to, enabled,
    results, resultContext, resultFingerprint: resultContext?.sourceFingerprint,
  });
}

export function calculationInputsMatch(snapshot, current) {
  return Boolean(snapshot && current)
    && Object.keys(snapshot).every(key => snapshot[key] === current[key]);
}
