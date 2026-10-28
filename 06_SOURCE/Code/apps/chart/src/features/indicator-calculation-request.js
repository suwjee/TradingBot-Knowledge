export function buildIndicatorCalculationRequest({
  file,
  analysisTimeframe,
  chartTimeframe,
  from,
  to,
  direction,
  requestId,
} = {}) {
  return {
    id: file?.id,
    chartId: file?.chartId || null,
    timeframe: analysisTimeframe,
    chartTimeframe,
    from,
    to,
    direction,
    blueLines: true,
    requestId,
  };
}
