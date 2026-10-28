const WORKSPACES = new Set(["chart", "faraz", "algorithm"]);

export function resolveChartTabState(search, { inventory = [], timeframes = [] } = {}) {
  const params = new URLSearchParams(String(search || "").replace(/^[^?]*\?/, ""));
  const requestedChartId = params.get("chartId") || "";
  const item = inventory.find((candidate) => String(candidate?.chartId || "") === requestedChartId);
  const requestedTimeframe = Number(params.get("tf"));
  return {
    chartId: item?.chartId || null,
    fileId: item?.id || null,
    timeframe: timeframes.includes(requestedTimeframe) ? requestedTimeframe : null,
  };
}

export function chartTabUrl(currentUrl, { chartId = null, timeframe = null } = {}) {
  const url = new URL(String(currentUrl || "/"), "http://localhost");
  if (chartId) url.searchParams.set("chartId", String(chartId));
  else url.searchParams.delete("chartId");
  if (Number.isSafeInteger(Number(timeframe)) && Number(timeframe) > 0) {
    url.searchParams.set("tf", String(Number(timeframe)));
  } else {
    url.searchParams.delete("tf");
  }
  return `${url.pathname}${url.search}${url.hash}`;
}

export function resolveWorkspaceRefreshState(saved, { fileIds = [], timeframes = [] } = {}) {
  const value = saved && typeof saved === "object" ? saved : {};
  const workspace = WORKSPACES.has(value.workspace) ? value.workspace : "chart";
  const fileId = fileIds.includes(value.fileId) ? value.fileId : null;
  const timeframe = timeframes.includes(Number(value.timeframe)) ? Number(value.timeframe) : null;
  return { workspace, fileId, timeframe };
}
