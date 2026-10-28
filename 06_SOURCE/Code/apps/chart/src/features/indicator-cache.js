const INDICATOR_STORAGE_KEY = /(?:^|[:_-])indicator(?:$|[:_-])|reaction-indicator/i;
const INDICATOR_CACHE_NAME = /(?:indicator|reaction)/i;
const INDICATOR_DATABASE_NAME = /(?:indicator|reaction)/i;

export function cacheClearLayers(scope) {
  const layers = ["calculations", "browser-storage", "browser-cache", "indexeddb", "drawings"];
  return scope === "all" ? [...layers, "secret"] : layers;
}

export function selectedCacheLayers(scope, requested = []) {
  const available = cacheClearLayers(scope);
  const selected = Array.isArray(requested) ? requested : [];
  return selected.length ? available.filter((layer) => selected.includes(layer)) : available;
}

function browserObject(name, fallback) {
  return typeof globalThis !== "undefined" && globalThis[name]
    ? globalThis[name]
    : fallback;
}

export function isIndicatorStorageKey(key) {
  return INDICATOR_STORAGE_KEY.test(String(key || ""));
}

export function isDrawingStorageKey(key) {
  return /(?:^|:)drawings$/i.test(String(key || ""));
}

export function clearIndicatorStorage(storage, { scope = "all", fileId = "", fileIds = [] } = {}) {
  if (!storage) return 0;
  const scopedFileIds = [...new Set([fileId, ...fileIds].filter(Boolean))];
  const currentPrefixes = scopedFileIds.map((id) => `market-canvas:${id}:`);
  const keys = [];
  try {
    for (let index = 0; index < storage.length; index += 1) {
      const key = storage.key(index);
      if (!key || !isIndicatorStorageKey(key)) continue;
      if (
        scope === "all"
        || key === "market-canvas:reaction-indicator"
        || currentPrefixes.some((prefix) => key.startsWith(prefix))
      ) {
        keys.push(key);
      }
    }
  } catch {
    // Browser storage can be disabled or revoked while the page is open.
  }
  let removed = 0;
  keys.forEach((key) => {
    try {
      storage.removeItem(key);
      removed += 1;
    } catch {
      // Continue clearing independent keys after an isolated storage failure.
    }
  });
  return removed;
}

export function clearDrawingStorage(storage, { scope = "all", fileId = "", fileIds = [] } = {}) {
  if (!storage) return 0;
  const scopedFileIds = [...new Set([fileId, ...fileIds].filter(Boolean))];
  const keys = [];
  try {
    for (let index = 0; index < storage.length; index += 1) {
      const key = storage.key(index);
      if (!key || !isDrawingStorageKey(key)) continue;
      if (scope === "all" || scopedFileIds.some((id) => key === `market-canvas:${id}:drawings`)) keys.push(key);
    }
  } catch {}
  keys.forEach((key) => {
    try { storage.removeItem(key); } catch {}
  });
  return keys.length;
}

function requestUrl(request) {
  return typeof request === "string" ? request : request?.url || "";
}

export function isIndicatorRequest(request) {
  try {
    const url = new URL(requestUrl(request), globalThis.location?.origin || "http://localhost");
    return /\/api\/reactions(?:\/|$)/i.test(url.pathname);
  } catch {
    return false;
  }
}

function requestMatchesScope(request, scope, symbol) {
  if (scope === "all" || !symbol) return true;
  const url = requestUrl(request);
  return url.includes(encodeURIComponent(symbol)) || url.includes(symbol);
}

export async function clearIndicatorCacheStorage(
  cacheStorage = browserObject("caches"),
  { scope = "all", symbol = "" } = {},
) {
  if (!cacheStorage?.keys) return { entriesCleared: 0, cachesDeleted: 0 };
  let entriesCleared = 0;
  let cachesDeleted = 0;
  let names = [];
  try {
    names = await cacheStorage.keys();
  } catch {
    return { entriesCleared, cachesDeleted };
  }
  for (const name of names) {
    let cache;
    try {
      cache = await cacheStorage.open(name);
      const requests = await cache.keys();
      for (const request of requests) {
        if (!isIndicatorRequest(request) || !requestMatchesScope(request, scope, symbol)) continue;
        if (await cache.delete(request)) entriesCleared += 1;
      }
      if (scope === "all" && INDICATOR_CACHE_NAME.test(name) && await cacheStorage.delete(name)) {
        cachesDeleted += 1;
      }
    } catch {
      // A single inaccessible cache must not prevent the other stores clearing.
    }
  }
  return { entriesCleared, cachesDeleted };
}

function deleteDatabase(indexedDB, name) {
  return new Promise((resolve) => {
    let request;
    try {
      request = indexedDB.deleteDatabase(name);
    } catch {
      resolve(false);
      return;
    }
    request.onsuccess = () => resolve(true);
    request.onerror = request.onblocked = () => resolve(false);
  });
}

export async function clearIndicatorIndexedDb(
  indexedDB = browserObject("indexedDB"),
) {
  if (!indexedDB?.databases || !indexedDB?.deleteDatabase) return 0;
  let databases;
  try {
    databases = await indexedDB.databases();
  } catch {
    return 0;
  }
  let deleted = 0;
  for (const database of databases || []) {
    const name = database?.name;
    if (!name || !INDICATOR_DATABASE_NAME.test(name)) continue;
    if (await deleteDatabase(indexedDB, name)) deleted += 1;
  }
  return deleted;
}

export async function clearIndicatorBrowserState({
  scope = "all",
  fileId = "",
  fileIds = [],
  symbol = "",
  local = browserObject("localStorage"),
  session = browserObject("sessionStorage"),
  cacheStorage = browserObject("caches"),
  indexedDB = browserObject("indexedDB"),
  layers = cacheClearLayers(scope),
} = {}) {
  const storageSelected = layers.includes("browser-storage");
  const localStorageKeys = storageSelected ? clearIndicatorStorage(local, { scope, fileId, fileIds }) : 0;
  const sessionStorageKeys = storageSelected ? clearIndicatorStorage(session, { scope, fileId, fileIds }) : 0;
  const drawingsStorageKeys = layers.includes("drawings") ? clearDrawingStorage(local, { scope, fileId, fileIds }) : 0;
  const [cache, indexedDbDatabases] = await Promise.all([
    layers.includes("browser-cache") ? clearIndicatorCacheStorage(cacheStorage, { scope, symbol }) : { entriesCleared: 0, cachesDeleted: 0 },
    layers.includes("indexeddb") ? clearIndicatorIndexedDb(indexedDB) : 0,
  ]);
  return {
    localStorageKeys,
    sessionStorageKeys,
    drawingsStorageKeys,
    ...cache,
    indexedDbDatabases,
  };
}
