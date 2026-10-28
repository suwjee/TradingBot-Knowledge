import fs from "node:fs";
import path from "node:path";
import { createHash, randomUUID } from "node:crypto";
import { execFile, execFileSync } from "node:child_process";
import { chromium } from "playwright-core";
import { fileURLToPath } from "node:url";
import { resolveLocalStatePaths } from "./local-state-paths.js";
import { createRawResourceStore } from "./raw-resource-store.js";
import { buildRawFilename, formatTehranMetadataTime, parseRawFilename } from "../src/features/raw-file-contract.js";
import { readBoundedBody } from "./request-body.js";
import { mergeChartUpdateCandles } from "./chart-update-merge.js";

const HISTORY_PATH = "/api/customer/trading-view/history";
const CHART_LIST_PATH = "/api/customer/chart-layout-v2/";
const AUTH_PROFILE_PATH = "/api/public/authentication/me";
const FARAZ_ORIGIN = "https://faraz.io";
const ALLOWED_HOSTS = new Set(["faraz.io", "ir3.faraz.io", "ir4.faraz.io"]);
const UNIT_SECONDS = { S: 1, M: 60, H: 3600, D: 86400, W: 604800 };
const MAX_PACKET_SIZE = 200_000;
const MAX_PACKETS = 200_000;
const MAX_RATE_LIMIT_MS = 60_000;
const MAX_PACKET_ATTEMPTS = 4;
const RETRY_BASE_DELAY_MS = 600;
const REQUEST_TIMEOUT_MS = 15_000;
const PRIMARY_CONCURRENCY = 6;
const MAX_COVERAGE_RECOVERY_ROUNDS = 3;
const CHART_UPDATE_PACKET_SIZE = 1_000;
const CHART_UPDATE_RATE_LIMIT_MS = 30;
const SESSION_FILE_VERSION = 3;
const LEGACY_DPAPI_SESSION_VERSION = 2;

export function parseResolutionToSeconds(value) {
  const resolution = String(value ?? "").trim().toUpperCase();
  if (/^\d+$/.test(resolution)) return Math.max(1, Number(resolution));
  const match = resolution.match(/^(\d+)(S|M|H|D|W)$/);
  if (!match || Number(match[1]) < 1) {
    throw new Error("Timeframe must look like 1S, 30S, 1M, 4H, 1D, or 1W.");
  }
  return Number(match[1]) * UNIT_SECONDS[match[2]];
}

export function normalizeHistoryPayload(payload) {
  return normalizeHistoryPayloadDetails(payload).candles;
}

export function normalizeHistoryPayloadDetails(payload) {
  const result = payload?.result && typeof payload.result === "object" ? payload.result : payload;
  if (result?.s === "no_data") return { candles: [], receivedRows: 0, rejectedRows: 0 };
  const t = Array.isArray(result?.t) ? result.t : [];
  const o = Array.isArray(result?.o) ? result.o : [];
  const h = Array.isArray(result?.h) ? result.h : [];
  const l = Array.isArray(result?.l) ? result.l : [];
  const c = Array.isArray(result?.c) ? result.c : [];
  const lengths = [t.length, o.length, h.length, l.length, c.length];
  if (!lengths.some(Boolean) && !Array.isArray(result?.t)) {
    throw new Error("FARAZ history response does not contain candle arrays.");
  }
  const rows = [];
  const receivedRows = Math.max(...lengths);
  let rejectedRows = receivedRows - Math.min(...lengths);
  for (let index = 0; index < Math.min(...lengths); index++) {
    const candle = { time: Math.trunc(Number(t[index])), open: Number(o[index]), high: Number(h[index]), low: Number(l[index]), close: Number(c[index]) };
    if (!Number.isSafeInteger(candle.time) || candle.time <= 0
      || ![candle.open, candle.high, candle.low, candle.close].every(Number.isFinite)
      || candle.high < Math.max(candle.open, candle.close, candle.low)
      || candle.low > Math.min(candle.open, candle.close, candle.high)) {
      rejectedRows++;
      continue;
    }
    rows.push(candle);
  }
  return { candles: rows, receivedRows, rejectedRows };
}

export function mergeCandles(chunks, from, to) {
  const sorted = [];
  for (const chunk of chunks) {
    for (const candle of chunk) {
      if (candle.time >= from && candle.time <= to) sorted.push(candle);
    }
  }
  sorted.sort((left, right) => left.time - right.time);
  const candles = [];
  let duplicates = 0;
  let conflicts = 0;
  for (const candle of sorted) {
    const previous = candles.at(-1);
    if (!previous || previous.time !== candle.time) {
      candles.push(candle);
      continue;
    }
    duplicates++;
    if (previous.open !== candle.open || previous.high !== candle.high || previous.low !== candle.low || previous.close !== candle.close) conflicts++;
  }
  return { candles, duplicates, conflicts };
}

/**
 * Return every expected source-timeframe slot that is missing from a selected
 * range.  Unlike an adjacent-row check, this includes the leading and
 * trailing edges, so a response that starts late can never pass as complete.
 */
export function findCandleCoverageGaps(candles, { from, to, timeframeSeconds } = {}) {
  const timeframe = Number(timeframeSeconds);
  if (!Number.isFinite(from) || !Number.isFinite(to) || !Number.isSafeInteger(timeframe) || timeframe < 1 || from > to) {
    throw new Error("Coverage range and timeframe are invalid.");
  }
  const firstExpected = Math.ceil(from / timeframe) * timeframe;
  const lastExpected = Math.floor(to / timeframe) * timeframe;
  if (firstExpected > lastExpected) return [];
  const gaps = [];
  let expected = firstExpected;
  for (const candle of candles) {
    if (!Number.isSafeInteger(candle?.time) || candle.time < expected) continue;
    if (candle.time > lastExpected) break;
    if (candle.time > expected) {
      const gapTo = candle.time - timeframe;
      gaps.push({
        key: `${expected}:${gapTo}:${timeframe}`,
        previousTime: expected - timeframe,
        nextTime: candle.time,
        from: expected,
        to: gapTo,
        missingCandles: (gapTo - expected) / timeframe + 1,
      });
    }
    expected = candle.time + timeframe;
  }
  if (expected <= lastExpected) {
    gaps.push({
      key: `${expected}:${lastExpected}:${timeframe}`,
      previousTime: expected - timeframe,
      nextTime: lastExpected + timeframe,
      from: expected,
      to: lastExpected,
      missingCandles: (lastExpected - expected) / timeframe + 1,
    });
  }
  return gaps;
}

export function buildCoverageRecoveryChunks(gaps, { from, to, timeframeSeconds, packetSize = 1000, startIndex = 0 } = {}) {
  const timeframe = Number(timeframeSeconds);
  const maximum = Math.max(1, Math.trunc(Number(packetSize) || 1000));
  if (!Number.isFinite(from) || !Number.isFinite(to) || !Number.isSafeInteger(timeframe) || timeframe < 1 || from > to) {
    throw new Error("Coverage recovery range and timeframe are invalid.");
  }
  const replayWindows = [];
  for (const gap of gaps || []) {
    const gapFrom = Math.max(from, Number(gap?.from));
    const gapTo = Math.min(to, Number(gap?.to));
    if (!Number.isFinite(gapFrom) || !Number.isFinite(gapTo) || gapFrom > gapTo) continue;
    replayWindows.push({
      from: Math.max(from, gapFrom - timeframe),
      to: Math.min(to, gapTo + timeframe),
    });
  }

  replayWindows.sort((left, right) => left.from - right.from || left.to - right.to);
  const mergedWindows = [];
  for (const window of replayWindows) {
    const previous = mergedWindows.at(-1);
    if (previous && window.from <= previous.to + timeframe) previous.to = Math.max(previous.to, window.to);
    else mergedWindows.push({ ...window });
  }

  const boundedWindows = [];
  for (const window of mergedWindows) {
    for (let cursor = window.from; cursor <= window.to;) {
      const chunkTo = Math.min(window.to, cursor + (maximum - 1) * timeframe);
      boundedWindows.push({ from: cursor, to: chunkTo });
      if (chunkTo >= window.to) break;
      cursor = chunkTo + timeframe;
    }
  }

  const packedWindows = [];
  for (const window of boundedWindows) {
    const previous = packedWindows.at(-1);
    const combinedSlots = previous ? Math.floor((window.to - previous.from) / timeframe) + 1 : Infinity;
    if (previous && combinedSlots <= maximum) previous.to = Math.max(previous.to, window.to);
    else packedWindows.push({ ...window });
  }

  let index = startIndex;
  return packedWindows.map((window) => ({
    index: index++, from: window.from, to: window.to,
    countback: Math.floor((window.to - window.from) / timeframe) + 1,
    firstDataRequest: false, latest: false, recovery: true,
  }));
}

function tehranDisplayTime(epochSeconds) {
  const value = Number(epochSeconds);
  return Number.isSafeInteger(value) && value > 0 ? formatTehranMetadataTime(value) : "—";
}

/**
 * This runs on the parsed temporary RAW file immediately before the atomic
 * move into data/raw.  Gaps are allowed (a market may have no candle),
 * but every present interval must be an integral multiple of the requested
 * timeframe and must stay inside the exact requested epoch bounds.
 */
export function verifySavedCandles(candles, { from, to, timeframeSeconds } = {}) {
  const rows = Array.isArray(candles) ? candles : [];
  const validRow = (candle) => candle && Object.keys(candle).length === 5
    && ["time", "open", "high", "low", "close"].every((key) => Object.hasOwn(candle, key))
    && Number.isSafeInteger(candle.time) && candle.time > 0
    && [candle.open, candle.high, candle.low, candle.close].every(Number.isFinite)
    && candle.high >= Math.max(candle.open, candle.close, candle.low)
    && candle.low <= Math.min(candle.open, candle.close, candle.high);
  const chronological = rows.length > 0 && rows.every((candle, index) => validRow(candle)
    && (!index || candle.time > rows[index - 1].time));
  const first = rows[0]?.time;
  const last = rows.at(-1)?.time;
  const bounds = Number.isFinite(from) && Number.isFinite(to)
    && rows.length > 0 && rows.every((candle) => candle.time >= from && candle.time <= to);
  const timeframe = Number(timeframeSeconds);
  const timeframeValid = Number.isSafeInteger(timeframe) && timeframe > 0 && rows.length > 0
    && rows.every((candle, index) => !index || (candle.time - rows[index - 1].time) % timeframe === 0);
  const checks = [
    { key: "chronology", label: "Timestamp order", passed: chronological, detail: chronological ? "Strict ascending timestamps; no duplicates." : "Rows are not strictly chronological or contain invalid data." },
    { key: "firstLast", label: "First and last candle", passed: Number.isFinite(first) && Number.isFinite(last), detail: Number.isFinite(first) && Number.isFinite(last) ? `First ${tehranDisplayTime(first)} · Last ${tehranDisplayTime(last)}` : "The saved file does not contain a valid first and last candle." },
    { key: "range", label: "Requested range", passed: bounds, detail: `Requested ${tehranDisplayTime(from)} → ${tehranDisplayTime(to)} · stored ${tehranDisplayTime(first)} → ${tehranDisplayTime(last)}` },
    { key: "integrity", label: "Saved OHLC integrity", passed: rows.length > 0 && rows.every(validRow), detail: rows.length ? `${rows.length.toLocaleString("en-US")} rows have exact fields and valid OHLC bounds.` : "No candles were saved." },
    { key: "timeframe", label: "Requested timeframe", passed: timeframeValid, detail: timeframeValid ? `Every adjacent stored interval is a multiple of ${timeframe} seconds; market gaps are retained.` : `Stored intervals do not match the requested ${timeframe || "unknown"}-second timeframe.` },
  ];
  return { valid: checks.every((check) => check.passed), checks };
}

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "no-store");
  res.end(JSON.stringify(body));
}

async function readJson(req, limit = 100_000) {
  const body = await readBoundedBody(req, limit, "Request is too large.");
  try { return JSON.parse(body || "{}"); }
  catch { throw new Error("Request body must be valid JSON."); }
}

function replaceFileWithRetry(sourcePath, targetPath) {
  let lastError;
  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      fs.renameSync(sourcePath, targetPath);
      return;
    } catch (error) {
      lastError = error;
      if (!["EPERM", "EACCES", "EEXIST", "ENOTEMPTY"].includes(error?.code)) throw error;
      try {
        // Windows cannot atomically rename over an existing file. copyFile
        // performs the replacement while preserving the destination path.
        fs.copyFileSync(sourcePath, targetPath);
        fs.unlinkSync(sourcePath);
        return;
      } catch (copyError) {
        lastError = copyError;
      }
      if (attempt < 4) {
        const waitUntil = Date.now() + 80 * (attempt + 1);
        while (Date.now() < waitUntil) {}
      }
    }
  }
  throw lastError;
}

function moveFileWithRetry(sourcePath, targetPath) {
  let lastError;
  for (let attempt = 0; attempt < 5; attempt++) {
    try {
      fs.renameSync(sourcePath, targetPath);
      return;
    } catch (error) {
      lastError = error;
      if (!["EPERM", "EACCES", "EEXIST", "ENOTEMPTY"].includes(error?.code)) throw error;
      try {
        fs.copyFileSync(sourcePath, targetPath);
        fs.unlinkSync(sourcePath);
        return;
      } catch (copyError) {
        lastError = copyError;
      }
      if (attempt < 4) {
        const waitUntil = Date.now() + 80 * (attempt + 1);
        while (Date.now() < waitUntil) {}
      }
    }
  }
  throw lastError;
}

function registryDefaultBrowserExecutable() {
  if (process.platform !== "win32") return null;
  try {
    const association = execFileSync("reg.exe", ["query", "HKCU\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice", "/v", "ProgId"], { encoding: "utf8", windowsHide: true });
    const progId = association.match(/^\s*ProgId\s+REG_SZ\s+(.+)$/im)?.[1]?.trim();
    if (!progId) return null;
    const command = execFileSync("reg.exe", ["query", `HKCR\\${progId}\\shell\\open\\command`, "/ve"], { encoding: "utf8", windowsHide: true });
    const commandValue = command.match(/^\s*\(Default\)\s+REG_SZ\s+(.+)$/im)?.[1]?.trim();
    const executable = commandValue?.match(/^"([^"]+\.exe)"/i)?.[1] || commandValue?.match(/^([^\s]+\.exe)/i)?.[1];
    return executable && fs.existsSync(executable) ? executable : null;
  } catch {
    return null;
  }
}

function browserExecutable() {
  const explicit = process.env.FARAZ_BROWSER_PATH;
  if (explicit && fs.existsSync(explicit)) return explicit;
  const systemDefault = registryDefaultBrowserExecutable();
  if (systemDefault) {
    if (/\b(?:chrome|msedge|brave|vivaldi|chromium)\.exe$/i.test(systemDefault)) return systemDefault;
    throw new Error(`The Windows default browser (${path.basename(systemDefault)}) is not Chromium-based and cannot expose a FARAZ session to this local app.`);
  }
  const candidates = [
    process.platform === "win32" ? "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" : null,
    process.platform === "win32" ? "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" : null,
    process.platform === "win32" ? "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" : null,
    process.platform === "darwin" ? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" : null,
    process.platform === "linux" ? "/usr/bin/google-chrome" : null,
    process.platform === "linux" ? "/usr/bin/chromium" : null,
  ].filter(Boolean);
  const executable = candidates.find((candidate) => fs.existsSync(candidate));
  if (!executable) throw new Error("A Chromium-based system browser was not found. Set FARAZ_BROWSER_PATH to its executable.");
  return executable;
}

function runDpapi(script, input) {
  if (process.platform !== "win32") throw new Error("Legacy FARAZ DPAPI migration requires the original Windows user.");
  return execFileSync("powershell.exe", ["-NoLogo", "-NoProfile", "-NonInteractive", "-Command", script], {
    encoding: "utf8", input, windowsHide: true, maxBuffer: 20_000_000,
  }).trim();
}

function unprotectForCurrentWindowsUser(cipherText) {
  return runDpapi("Add-Type -AssemblyName System.Security;$value=[Console]::In.ReadToEnd().Trim();$protected=[Convert]::FromBase64String($value);$bytes=[Security.Cryptography.ProtectedData]::Unprotect($protected,$null,[Security.Cryptography.DataProtectionScope]::CurrentUser);[Text.Encoding]::UTF8.GetString($bytes)", cipherText);
}

function safeHost(value) {
  const host = String(value || "faraz.io").toLowerCase();
  if (!ALLOWED_HOSTS.has(host)) throw new Error("Unsupported FARAZ history host.");
  return host;
}

function chunkRange(from, to, timeframeSeconds, packetSize, startIndex = 0) {
  if (!Number.isFinite(from) || !Number.isFinite(to) || from > to) throw new Error("The selected range is invalid.");
  const maximum = Math.max(1, Math.trunc(Number(packetSize) || 1));
  const chunks = [];
  for (let cursor = from, index = startIndex; cursor <= to; index++) {
    if (chunks.length >= MAX_PACKETS) throw new Error("The request exceeds the packet safety limit.");
    const chunkTo = Math.min(to, cursor + (maximum - 1) * timeframeSeconds);
    chunks.push({ index, from: cursor, to: chunkTo, countback: Math.floor((chunkTo - cursor) / timeframeSeconds) + 1, firstDataRequest: index === 0, latest: chunkTo >= to });
    cursor = chunkTo + timeframeSeconds;
  }
  return chunks;
}

export function buildCandleFilename(symbolName, resolution, firstTime, lastTime) {
  const identity = marketIdentity(symbolName);
  return buildRawFilename({ broker: identity.broker, symbol: identity.symbol, timeframe: resolution, firstTime, lastTime });
}

function marketIdentity(symbolName) {
  const parts = String(symbolName || "").trim().toUpperCase().replace(/:/g, "_").split("_").filter(Boolean);
  if (parts[0] === "FARAZ" && parts.length > 2) parts.shift();
  if (parts.length < 2) throw new Error("The market symbol must include broker and symbol.");
  return { broker: parts.shift(), symbol: parts.join("_") };
}

function readCookieValue(cookieHeader, name) {
  const match = String(cookieHeader || "").match(new RegExp(`(?:^|;\\s*)${name}=([^;]*)`, "i"));
  return match ? match[1] : "";
}

function clearTextCredentials(value = {}) {
  return {
    xAccessToken: String(value["x-access-token"] || value.xAccessToken || "").trim(),
    farazSession: String(value.farazSession || "").trim(),
  };
}

// This is the editable on-disk session format. Legacy DPAPI envelopes are
// decoded only once during migration; all later reads and writes stay clear text.
export function normalizeClearTextSession(value) {
  if (!value || typeof value !== "object") return null;
  const credentials = clearTextCredentials(value);
  const storageState = value.storageState && typeof value.storageState === "object"
    ? structuredClone(value.storageState)
    : { cookies: [], origins: [] };
  storageState.cookies = Array.isArray(storageState.cookies) ? storageState.cookies : [];
  storageState.origins = Array.isArray(storageState.origins) ? storageState.origins : [];
  if (credentials.farazSession) {
    const sessionCookie = storageState.cookies.find((cookie) => cookie?.name === "farazSession" && /(^|\.)faraz\.io$/i.test(cookie.domain || ""));
    if (sessionCookie) sessionCookie.value = credentials.farazSession;
    else storageState.cookies.push({ name: "farazSession", value: credentials.farazSession, domain: ".faraz.io", path: "/", expires: -1, httpOnly: false, secure: true, sameSite: "Lax" });
  }
  const historyAuth = value.historyAuth && ALLOWED_HOSTS.has(value.historyAuth.host) ? value.historyAuth : null;
  if (!credentials.xAccessToken && !credentials.farazSession && !storageState.cookies.some((cookie) => /(^|\.)faraz\.io$/i.test(cookie?.domain || ""))) return null;
  return { storageState, credentials, historyAuth };
}

export function createFarazCandleApi({ workspaceRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", ".."), localStateRoot, launchBrowser, fetchImpl = globalThis.fetch } = {}) {
  const localState = resolveLocalStatePaths(workspaceRoot, localStateRoot);
  const secretDir = localState.secret;
  const secretPath = path.join(secretDir, "faraz-session.dpapi.json");
  const inputDir = localState.raw;
  const outputDir = localState.raw;
  const rawStore = createRawResourceStore({ rootDir: inputDir });
  const temporaryOutputDir = path.join(localState.tmp, "faraz-candle-exports");
  const jobs = new Map();
  let browser = null;
  let context = null;
  let authPage = null;
  let contextHeadless = null;
  let browserServer = null;
  let browserPid = null;
  let historyAuth = null;
  let credentials = { xAccessToken: "", farazSession: "" };
  let storedStorageState = { cookies: [], origins: [] };
  let sessionCapturePending = null;
  let authCaptureArmed = false;
  let loginBrowser = null;
  let nextChartHistoryRequestAt = 0;
  let shutdownPromise = null;
  let shuttingDown = false;
  const pendingLaunches = new Set();
  const observedHistoryPages = new WeakSet();

  async function waitForChartHistoryRequestSlot() {
    const now = Date.now();
    const scheduledAt = Math.max(now, nextChartHistoryRequestAt);
    nextChartHistoryRequestAt = scheduledAt + CHART_UPDATE_RATE_LIMIT_MS;
    if (scheduledAt > now) await new Promise((resolve) => setTimeout(resolve, scheduledAt - now));
  }

  function loadStoredSession() {
    if (!fs.existsSync(secretPath)) return null;
    const envelope = JSON.parse(fs.readFileSync(secretPath, "utf8"));
    let decoded;
    let migrateLegacyDpapi = false;
    if (envelope.version === LEGACY_DPAPI_SESSION_VERSION && envelope.protection === "windows-dpapi-current-user" && typeof envelope.payload === "string") {
      decoded = JSON.parse(unprotectForCurrentWindowsUser(envelope.payload));
      migrateLegacyDpapi = true;
    } else if (envelope.format === "clear-text") {
      decoded = envelope;
    } else {
      throw new Error("The stored FARAZ session file has an unsupported format.");
    }
    const restored = normalizeClearTextSession(decoded);
    if (!restored) throw new Error("The stored FARAZ session file is empty or has an unsupported format.");
    credentials = restored.credentials;
    historyAuth = restored.historyAuth;
    storedStorageState = restored.storageState;
    if (migrateLegacyDpapi) persistStorageState(storedStorageState);
    return storedStorageState;
  }

  function persistStorageState(storageState) {
    fs.mkdirSync(secretDir, { recursive: true, mode: 0o700 });
    storedStorageState = storageState;
    const session = {
      format: "clear-text",
      version: SESSION_FILE_VERSION,
      updatedAt: new Date().toISOString(),
      "x-access-token": credentials.xAccessToken,
      farazSession: credentials.farazSession,
      storageState,
      historyAuth,
    };
    const temporaryPath = path.join(secretDir, `.faraz-session-${randomUUID()}.json.tmp`);
    fs.writeFileSync(temporaryPath, `${JSON.stringify(session, null, 2)}\n`, { encoding: "utf8", mode: 0o600, flag: "wx" });
    try {
      replaceFileWithRetry(temporaryPath, secretPath);
    } finally {
      if (fs.existsSync(temporaryPath)) fs.unlinkSync(temporaryPath);
    }
  }

  async function persistSession() {
    if (!authCaptureArmed || !context) return;
    const storageState = await context.storageState({ indexedDB: true });
    const sessionCookie = storageState.cookies.find((cookie) => cookie?.name === "farazSession" && /(^|\.)faraz\.io$/i.test(cookie.domain || ""));
    if (sessionCookie?.value) credentials.farazSession = sessionCookie.value;
    if (!credentials.xAccessToken && authPage && !authPage.isClosed()) {
      const pageToken = await authPage.evaluate(() => {
        const values = Object.values(localStorage);
        return values.map((value) => String(value).match(/eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+/)?.[0]).find(Boolean) || "";
      }).catch(() => "");
      if (pageToken) credentials.xAccessToken = pageToken;
    }
    persistStorageState(storageState);
    authCaptureArmed = false;
  }

  async function finalizeCapturedSession() {
    await persistSession();
    if (!fs.existsSync(secretPath)) throw new Error("FARAZ session was not saved locally.");
    await closeBrowserContext();
  }

  function killBrowserProcessTree(pid) {
    if (process.platform !== "win32" || !Number.isSafeInteger(pid) || pid <= 0) return;
    try { execFileSync("taskkill.exe", ["/PID", String(pid), "/T", "/F"], { windowsHide: true, stdio: "ignore" }); }
    catch {}
  }

  async function closeBrowserContext({ forceKill = false } = {}) {
    const closingBrowser = browser;
    const closingServer = browserServer;
    const closingPid = browserPid;
    if (loginBrowser === closingBrowser) loginBrowser = null;
    authCaptureArmed = false;
    browser = null;
    browserServer = null;
    browserPid = null;
    context = null;
    authPage = null;
    contextHeadless = null;
    if (closingBrowser?.isConnected()) await closingBrowser.close().catch(() => {});
    await closingServer?.close().catch(() => {});
    if (forceKill) {
      await closingServer?.kill().catch(() => {});
      killBrowserProcessTree(closingPid);
    }
  }

  async function clearStoredSession() {
    await closeBrowserContext();
    historyAuth = null;
    credentials = { xAccessToken: "", farazSession: "" };
    storedStorageState = { cookies: [], origins: [] };
    if (fs.existsSync(secretPath)) fs.unlinkSync(secretPath);
  }

  function openSavedFile(outputPath) {
    if (!outputPath || !fs.existsSync(outputPath)) throw new Error("Saved RAW file was not found.");
    if (process.platform !== "win32") throw new Error("Opening saved RAW files is currently supported on Windows only.");
    return new Promise((resolve, reject) => {
      // Encoded PowerShell keeps the exact known path as one literal argument.
      const literalPath = outputPath.replaceAll("'", "''");
      const command = `Start-Process -FilePath '${literalPath}'`;
      const encoded = Buffer.from(command, "utf16le").toString("base64");
      execFile("powershell.exe", ["-NoLogo", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded], { windowsHide: true }, (error) => error ? reject(error) : resolve());
    });
  }

  function sessionHeaders() {
    const storageState = loadStoredSession();
    if (!storageState) throw new Error("The FARAZ session file is missing. Sign in again.");
    const now = Date.now() / 1000;
    const cookie = (storageState?.cookies || [])
      .filter((item) => item?.name && item?.value && /(^|\.)faraz\.io$/i.test(item.domain || "") && (!Number.isFinite(item.expires) || item.expires < 0 || item.expires > now))
      .map((item) => `${item.name}=${item.value}`)
      .join("; ");
    return {
      Accept: "application/json, text/plain, */*",
      ...(cookie ? { Cookie: cookie } : {}),
      ...(credentials.xAccessToken ? { "x-access-token": credentials.xAccessToken } : {}),
    };
  }

  async function directRequest(url, { timeoutMs = REQUEST_TIMEOUT_MS, controller = new AbortController() } = {}) {
    const timeout = setTimeout(() => controller.abort(), timeoutMs);
    try {
      return await fetchImpl(url, { method: "GET", signal: controller.signal, headers: sessionHeaders() });
    } finally {
      clearTimeout(timeout);
    }
  }

  async function probeStoredSession(symbolName = "FXCM:USOIL") {
    const host = safeHost(historyAuth?.host);
    const url = new URL(historyAuth?.endpoint && new URL(historyAuth.endpoint).host === host
      ? historyAuth.endpoint
      : `https://${host}${HISTORY_PATH}`);
    const to = Math.floor(Date.now() / 1000);
    for (const [key, value] of Object.entries({
      symbolName: endpointSymbolName(symbolName), resolution: historyAuth?.resolution || "30S",
      from: to - 86_400, to, countback: 1, firstDataRequest: true, latest: true,
      adjustType: historyAuth?.adjustType || "2", json: true,
    })) url.searchParams.set(key, String(value));
    const startedAt = Date.now();
    const response = await directRequest(url);
    const contentType = response.headers?.get?.("content-type") || "";
    return {
      connected: response.status !== 401 && response.status !== 403 && response.ok && /(?:application|text)\/json/i.test(contentType),
      status: response.status,
      pingMs: Date.now() - startedAt,
    };
  }

  async function readAuthenticatedProfile() {
    const response = await directRequest(new URL(`${FARAZ_ORIGIN}${AUTH_PROFILE_PATH}`));
    if (!response.ok) {
      const error = new Error(`FARAZ profile request failed with HTTP ${response.status}.`);
      error.status = response.status;
      throw error;
    }
    let payload;
    try { payload = JSON.parse(await response.text()); }
    catch { throw new Error("FARAZ profile response was not valid JSON."); }
    return {
      userId: typeof payload?._id === "string" ? payload._id : null,
      userName: typeof payload?.name === "string" ? payload.name : null,
      phone: typeof payload?.phone === "string" ? payload.phone : null,
    };
  }

  function captureHistoryRequest(request) {
    try {
      const url = new URL(request.url());
      if (!ALLOWED_HOSTS.has(url.host) || url.pathname !== HISTORY_PATH) return;
      historyAuth = {
        host: url.host,
        protocol: url.protocol,
        symbolName: url.searchParams.get("symbolName") || "",
        resolution: url.searchParams.get("resolution") || "",
        endpoint: `${url.origin}${url.pathname}`,
        adjustType: url.searchParams.get("adjustType") || "2",
        countback: Math.max(1, Number.parseInt(url.searchParams.get("countback"), 10) || 0),
        capturedAt: Date.now(),
      };
      const headers = request.headers();
      credentials = {
        xAccessToken: String(headers["x-access-token"] || headers.authorization || credentials.xAccessToken || "").replace(/^Bearer\s+/i, ""),
        farazSession: readCookieValue(headers.cookie, "farazSession") || credentials.farazSession,
      };
    } catch {}
  }

  function captureHistoryResponse(response) {
    try {
      const url = new URL(response.url());
      if (!ALLOWED_HOSTS.has(url.host) || url.pathname !== HISTORY_PATH || !response.ok) return;
      if (sessionCapturePending || !authCaptureArmed || loginBrowser !== browser || fs.existsSync(secretPath)) return;
      sessionCapturePending = (async () => {
        await finalizeCapturedSession();
      })().catch(() => {}).finally(() => { sessionCapturePending = null; });
    } catch {}
  }

  function observeHistoryRequests(page) {
    if (!page || observedHistoryPages.has(page)) return;
    observedHistoryPages.add(page);
    page.on("request", captureHistoryRequest);
    page.on("response", captureHistoryResponse);
  }

  function endpointSymbolName(symbolName) {
    const requested = String(symbolName || "").trim();
    const normalized = requested.replace(/:/g, "_").toUpperCase();
    if (historyAuth?.symbolName?.replace(/:/g, "_").toUpperCase() === normalized) return historyAuth.symbolName;
    return normalized;
  }

  async function ensureContext({ showLogin = false, showBrowser = false } = {}) {
    if (shuttingDown) throw new Error("FARAZ service is shutting down.");
    if (context && (showLogin || showBrowser) && !authCaptureArmed && !fs.existsSync(secretPath)) {
      await closeBrowserContext();
      credentials = { xAccessToken: "", farazSession: "" };
      storedStorageState = { cookies: [], origins: [] };
      historyAuth = null;
    }
    if (context && (showLogin || showBrowser) && contextHeadless) await closeBrowserContext();
    if (!context) {
      if (pendingLaunches.size) {
        await pendingLaunches.values().next().value;
      } else {
        const executablePath = launchBrowser ? (process.env.FARAZ_BROWSER_PATH || null) : browserExecutable();
        const storageState = loadStoredSession();
        if ((showLogin || showBrowser) && !storageState) authCaptureArmed = true;
        const headless = !showLogin && !showBrowser;
        const launch = launchBrowser || (async ({ executablePath }) => {
          const launchedServer = await chromium.launchServer({
            executablePath, headless,
            args: headless ? ["--no-first-run", "--no-default-browser-check"] : ["--start-maximized", "--no-first-run", "--no-default-browser-check"],
          });
          let launchedBrowser;
          try {
            launchedBrowser = await chromium.connect(launchedServer.wsEndpoint());
            const launchedContext = await launchedBrowser.newContext({ storageState: storageState || undefined, viewport: null });
            return { browser: launchedBrowser, context: launchedContext, browserServer: launchedServer, browserPid: launchedServer.process()?.pid || null };
          } catch (error) {
            await launchedBrowser?.close().catch(() => {});
            await launchedServer.kill().catch(() => {});
            throw error;
          }
        });
        const launching = (async () => {
          const launched = await launch({ executablePath, headless, storageState });
          browser = launched.browser;
          if (authCaptureArmed && (showLogin || showBrowser)) loginBrowser = launched.browser;
          context = launched.context;
          browserServer = launched.browserServer || null;
          browserPid = Number(launched.browserPid) || null;
          contextHeadless = headless;
          try {
            if (shuttingDown) throw new Error("FARAZ service is shutting down.");
            if (credentials.xAccessToken) await context.setExtraHTTPHeaders({ "x-access-token": credentials.xAccessToken });
            context.on?.("page", observeHistoryRequests);
            context.pages().forEach(observeHistoryRequests);
            browser.on?.("disconnected", () => {
              if (browser === launched.browser) {
                if (loginBrowser === launched.browser) loginBrowser = null;
                authCaptureArmed = false;
                browser = null;
                context = null;
                authPage = null;
                contextHeadless = null;
              }
            });
          } catch (error) {
            await closeBrowserContext({ forceKill: true });
            throw error;
          }
        })();
        pendingLaunches.add(launching);
        try { await launching; }
        finally { pendingLaunches.delete(launching); }
      }
    }
    if (shuttingDown) throw new Error("FARAZ service is shutting down.");
    const pages = context.pages();
    authPage = pages.find((page) => /^https:\/\/([^.]+\.)?faraz\.io\//i.test(page.url())) || pages[0] || await context.newPage();
    observeHistoryRequests(authPage);
    if (showLogin) {
      await authPage.goto(`${FARAZ_ORIGIN}/account/login`, { waitUntil: "domcontentloaded" });
    } else if (!/^https:\/\/([^.]+\.)?faraz\.io\//i.test(authPage.url())) {
      await authPage.goto(FARAZ_ORIGIN, { waitUntil: "domcontentloaded" });
    }
    if (showLogin || showBrowser) {
      await authPage.bringToFront();
    }
    return authPage;
  }

  async function capturePendingBrowserLogin(symbolName) {
    if (!authCaptureArmed || !context || loginBrowser !== browser || !authPage || authPage.isClosed()) return false;
    const cookies = await context.cookies([FARAZ_ORIGIN]);
    if (!cookies.some((cookie) => /(^|\.)faraz\.io$/i.test(cookie?.domain || ""))) return false;
    if (!/^https:\/\/([^.]+\.)?faraz\.io\//i.test(authPage.url())) await authPage.goto(FARAZ_ORIGIN, { waitUntil: "domcontentloaded" });
    const probe = await authPage.evaluate(async ({ endpoint }) => {
      const response = await fetch(endpoint, { credentials: "include", cache: "no-store", headers: { Accept: "application/json, text/plain, */*" } });
      return {
        status: response.status,
        ok: response.ok,
        contentType: response.headers.get("content-type") || "",
        redirectedToLogin: response.redirected && /\/account\/login/i.test(response.url),
      };
    }, { endpoint: `${FARAZ_ORIGIN}${AUTH_PROFILE_PATH}` });
    if (!probe.ok || probe.status === 401 || probe.status === 403 || !/(?:application|text)\/json/i.test(probe.contentType) || probe.redirectedToLogin) return false;
    await finalizeCapturedSession();
    return fs.existsSync(secretPath);
  }

  async function authStatus(symbolName = "FXCM:USOIL") {
    try {
      if (!fs.existsSync(secretPath)) {
        if (authCaptureArmed && await capturePendingBrowserLogin(symbolName)) {
          // Browser data is only used to create the file; the status below is
          // decided by re-reading that file and probing with its credentials.
        } else if (authCaptureArmed) {
          return { connected: false, state: "waiting_for_login" };
        } else {
          if (context) await closeBrowserContext();
          credentials = { xAccessToken: "", farazSession: "" };
          storedStorageState = { cookies: [], origins: [] };
          historyAuth = null;
          return { connected: false, state: "not_connected" };
        }
      }
      const storageState = loadStoredSession();
      const probe = await probeStoredSession(symbolName);
      if (probe.status === 401) {
        return { connected: false, state: "expired_session", httpStatus: probe.status };
      }
      const profile = probe.connected ? await readAuthenticatedProfile().catch(() => ({})) : {};
      return {
        connected: probe.connected,
        state: probe.connected ? "saved_session" : "expired_session",
        checkedAt: Date.now(),
        host: historyAuth?.host || "faraz.io",
        historyHost: historyAuth?.host || null,
        endpoint: historyAuth?.endpoint || null,
        httpStatus: probe.status,
        pingMs: probe.pingMs,
        ...profile,
        credentialStorage: "Editable clear-text secret cache",
        savedCookies: storageState.cookies.filter((cookie) => /(^|\.)faraz\.io$/i.test(cookie?.domain || "")).length,
      };
    } catch (error) {
      if (!fs.existsSync(secretPath) && !authCaptureArmed) {
        await clearStoredSession();
        return { connected: false, state: "not_connected" };
      }
      return { connected: false, state: authCaptureArmed ? "waiting_for_login" : "expired_session", error: error.message };
    }
  }

  async function logoutFromLoginBrowser() {
    await clearStoredSession();
  }

  function publicJob(job) {
    if (!job) return null;
    const { outputPath, abort, chunks, page, requestController, requestControllers, nextRequestAt, retryCooldownUntil, pendingCandles, ...safe } = job;
    return { ...safe, totalPackets: safe.totalPackets || chunks?.length || 0, openUrl: job.done && outputPath ? `/api/faraz/candles/open?id=${encodeURIComponent(job.id)}` : null };
  }

  function log(job, level, message) {
    job.logs.push({ time: Date.now(), level, message });
    job.updatedAt = Date.now();
  }

  function captureHistoryResponse(job, chunk, response, text) {
    if (!job.responseAuditPath) return;
    try {
      const record = {
        capturedAt: new Date().toISOString(),
        stage: job.stage,
        request: {
          from: chunk.from,
          to: chunk.to,
          countback: chunk.countback,
          firstDataRequest: Boolean(chunk.firstDataRequest),
          latest: Boolean(chunk.latest),
        },
        response: { status: response.status, ok: response.ok, body: text },
      };
      fs.appendFileSync(job.responseAuditPath, `${JSON.stringify(record)}\n`, "utf8");
      job.capturedResponseCount = (job.capturedResponseCount || 0) + 1;
    } catch (error) {
      // Diagnostics must never turn an otherwise valid export into a failure.
      if (!job.responseAuditWriteFailed) {
        job.responseAuditWriteFailed = true;
        log(job, "warn", `Response audit could not be written: ${describeError(error)}.`);
      }
    }
  }

  function logPacketProgress(job, packetNumber, rows) {
    // Keep the browser responsive for long exports.  Packet-level successes
    // are sampled to at most 26 lines; failures and HTTP retries are never
    // sampled and retain their full diagnostic context.
    const total = job.chunks.length;
    const step = Math.max(1, Math.ceil(total / 24));
    if (packetNumber !== 1 && packetNumber !== total && packetNumber % step) return;
    const percent = total ? Math.round(packetNumber / total * 100) : 0;
    log(job, "success", `Primary progress ${Math.min(packetNumber, total)}/${total} (${percent}%): latest packet returned ${rows.length} in-range valid candle(s); total rows received ${job.receivedRows.toLocaleString("en-US")}.`);
  }

  function describeJobRequest(job, chunk) {
    return `stage=${job.stage}; endpoint=${job.endpoint}; symbol=${job.endpointSymbolName}; resolution=${job.resolution}; adjustType=${job.adjustType}; range=${tehranDisplayTime(chunk.from)}→${tehranDisplayTime(chunk.to)}`;
  }

  function describeError(error) {
    const cause = error?.cause?.message ? `; cause=${error.cause.message}` : "";
    const status = Number.isFinite(error?.status) ? `; httpStatus=${error.status}` : "";
    return `${error?.name || "Error"}: ${error?.message || "Unknown failure"}${status}${cause}`;
  }

  async function cancellableDelay(job, delayMs) {
    const deadline = Date.now() + delayMs;
    while (Date.now() < deadline) {
      if (job.abort.cancelled) throw new Error("Extraction cancelled.");
      await new Promise((resolve) => setTimeout(resolve, Math.min(100, deadline - Date.now())));
    }
  }

  async function paceRequest(job) {
    const now = Date.now();
    // The scheduler is shared by all workers: requests stay concurrent in
    // flight, while starts are smooth and a server-protection cooldown applies
    // globally instead of causing a retry burst.
    const scheduledAt = Math.max(now, Number(job.nextRequestAt) || now, Number(job.retryCooldownUntil) || now);
    job.nextRequestAt = scheduledAt + job.rateLimitMs;
    if (scheduledAt > now) await cancellableDelay(job, scheduledAt - now);
  }

  async function runConcurrent(job, entries, concurrency, worker) {
    const results = new Array(entries.length);
    let cursor = 0;
    const workers = Array.from({ length: Math.min(Math.max(1, concurrency), entries.length) }, async () => {
      while (!job.abort.cancelled) {
        const index = cursor++;
        if (index >= entries.length) return;
        results[index] = await worker(entries[index], index);
      }
      throw new Error("Extraction cancelled.");
    });
    await Promise.all(workers);
    return results;
  }

  async function fetchChunkOnce(job, chunk) {
    const url = new URL(job.endpoint);
    for (const [key, value] of Object.entries({
      symbolName: job.endpointSymbolName, resolution: job.resolution, from: chunk.from, to: chunk.to,
      countback: chunk.countback, firstDataRequest: chunk.firstDataRequest, latest: chunk.latest,
      adjustType: job.adjustType, json: true,
    })) url.searchParams.set(key, String(value));
    let response;
    const requestController = new AbortController();
    job.requestController = requestController;
    job.requestControllers?.add(requestController);
    try {
      await paceRequest(job);
      response = await directRequest(url, { controller: requestController });
    } catch (cause) {
      if (job.abort.cancelled) throw new Error("Extraction cancelled.");
      const error = new Error(cause?.name === "AbortError" ? "FARAZ history request timed out." : `FARAZ network error: ${cause?.message || "Network error"}`);
      error.cause = cause;
      throw error;
    } finally {
      if (job.requestController === requestController) job.requestController = null;
      job.requestControllers?.delete(requestController);
    }
    const text = await response.text();
    captureHistoryResponse(job, chunk, response, text);
    if (!response.ok) {
      const error = new Error(`FARAZ history request failed with HTTP ${response.status}: ${text}`);
      error.status = response.status;
      throw error;
    }
    let payload;
    try { payload = JSON.parse(text); }
    catch {
      const error = new Error("FARAZ returned invalid JSON with HTTP 200.");
      error.status = 200;
      throw error;
    }
    const normalized = normalizeHistoryPayloadDetails(payload);
    if (normalized.rejectedRows) {
      throw new Error(`FARAZ packet ${chunk.index + 1} contained ${normalized.rejectedRows} malformed or invalid candle row(s).`);
    }
    const inRange = normalized.candles.filter((candle) => candle.time >= chunk.from && candle.time <= chunk.to);
    const outsideRange = normalized.candles.length - inRange.length;
    if (outsideRange) {
      job.outsideRangePackets = (job.outsideRangePackets || 0) + 1;
      job.outsideRangeRows = (job.outsideRangeRows || 0) + outsideRange;
      const sampleStep = Math.max(1, Math.ceil(job.chunks.length / 12));
      if (job.outsideRangePackets <= 2 || job.outsideRangePackets % sampleStep === 0) {
        log(job, "warn", `${chunk.label || `Packet ${chunk.index + 1}/${job.chunks.length}`} returned ${outsideRange} countback candle(s) outside its requested range; they were excluded from validation and storage. Total excluded so far: ${job.outsideRangeRows}.`);
      }
    }
    return inRange;
  }

  async function fetchChunk(job, chunk) {
    for (let attempt = 1; attempt <= MAX_PACKET_ATTEMPTS; attempt++) {
      try {
        const rows = await fetchChunkOnce(job, chunk);
        if (!rows.length) log(job, "info", `${chunk.label || `Packet ${chunk.index + 1}/${job.chunks.length}`} received HTTP 200 with a valid empty response; FARAZ has no candle for this interval.`);
        return rows;
      } catch (error) {
        if (job.abort.cancelled || error?.name === "AbortError") throw new Error("Extraction cancelled.");
        if (attempt === MAX_PACKET_ATTEMPTS) {
          throw new Error(`${chunk.label || `Packet ${chunk.index + 1}/${job.chunks.length}`} failed after ${MAX_PACKET_ATTEMPTS} attempts: ${describeError(error)}; ${describeJobRequest(job, chunk)}.`);
        }
        const delay = RETRY_BASE_DELAY_MS * 2 ** (attempt - 1) + Math.floor(Math.random() * RETRY_BASE_DELAY_MS);
        const label = chunk.label || `Packet ${chunk.index + 1}/${job.chunks.length}`;
        job.retryCooldownUntil = Math.max(Number(job.retryCooldownUntil) || 0, Date.now() + delay);
        log(job, "retry", `${label} failed attempt ${attempt}/${MAX_PACKET_ATTEMPTS}: ${describeError(error)}; ${describeJobRequest(job, chunk)}. Retry is queued after a shared ${delay} ms cooldown.`);
      }
    }
    throw new Error("FARAZ history request failed.");
  }

  function remainingCoverageForGap(gap, remainingGaps, timeframeSeconds) {
    return remainingGaps.reduce((total, remaining) => {
      const from = Math.max(gap.from, remaining.from);
      const to = Math.min(gap.to, remaining.to);
      return from > to ? total : total + Math.floor((to - from) / timeframeSeconds) + 1;
    }, 0);
  }

  function shutdown() {
    if (shutdownPromise) return shutdownPromise;
    shuttingDown = true;
    shutdownPromise = (async () => {
      for (const job of jobs.values()) {
        if (!job.running && !job.awaitingCoverageDecision) continue;
        job.abort.cancelled = true;
        job.requestController?.abort();
        for (const controller of job.requestControllers || []) controller.abort();
      }
      await Promise.allSettled([...pendingLaunches]);
      await closeBrowserContext({ forceKill: true });
    })();
    return shutdownPromise;
  }

  async function recoverCoverageGaps(job, initialCandles) {
    const originalGaps = findCandleCoverageGaps(initialCandles, {
      from: job.requestedFrom, to: job.requestedTo, timeframeSeconds: job.timeframeSeconds,
    });
    if (!originalGaps.length) return { candles: initialCandles, records: [], coverageComplete: true };

    log(job, "warn", `${originalGaps.length} source-timeframe coverage gap interval(s) were detected, including request boundaries. Replaying the missing intervals before saving.`);
    const supplemental = [];
    let candles = initialCandles;
    let remainingGaps = originalGaps;
    let attempts = 0;
    while (remainingGaps.length && attempts < MAX_COVERAGE_RECOVERY_ROUNDS) {
      attempts++;
      const missingBeforeReplay = remainingGaps.reduce((total, gap) => total + gap.missingCandles, 0);
      const chunks = buildCoverageRecoveryChunks(remainingGaps, {
        from: job.requestedFrom, to: job.requestedTo, timeframeSeconds: job.timeframeSeconds,
        packetSize: job.packetSize, startIndex: job.totalPackets,
      }).map((chunk, index) => ({ ...chunk, label: `Coverage replay ${attempts}.${index + 1}` }));
      if (!chunks.length) break;
      job.totalPackets += chunks.length;
      log(job, "info", `Coverage replay ${attempts}/${MAX_COVERAGE_RECOVERY_ROUNDS} started for ${remainingGaps.length} interval(s) using ${chunks.length} precise packet(s).`);
      const rowsByChunk = await runConcurrent(job, chunks, PRIMARY_CONCURRENCY, async (chunk) => {
        job.sentPackets++;
        const rows = await fetchChunk(job, chunk);
        job.receivedPackets++;
        job.receivedRows += rows.length;
        return rows;
      });
      supplemental.push(...rowsByChunk);
      const merged = mergeCandles([initialCandles, ...supplemental], job.requestedFrom, job.requestedTo);
      if (merged.conflicts) throw new Error(`Coverage replay found ${merged.conflicts} conflicting duplicate candle(s); nothing was saved.`);
      candles = merged.candles;
      remainingGaps = findCandleCoverageGaps(candles, {
        from: job.requestedFrom, to: job.requestedTo, timeframeSeconds: job.timeframeSeconds,
      });
      const recovered = originalGaps.reduce((total, gap) => total + gap.missingCandles, 0)
        - remainingGaps.reduce((total, gap) => total + gap.missingCandles, 0);
      log(job, remainingGaps.length ? "warn" : "success", `Coverage replay ${attempts} recovered ${recovered.toLocaleString("en-US")} candle(s); ${remainingGaps.length} gap interval(s) remain.`);
      const missingAfterReplay = remainingGaps.reduce((total, gap) => total + gap.missingCandles, 0);
      if (missingAfterReplay >= missingBeforeReplay) {
        log(job, "warn", `Coverage replay ${attempts} made no progress; the remaining intervals are treated as unavailable source data instead of being requested again.`);
        break;
      }
    }
    const records = originalGaps.map((gap) => {
      const remainingCandles = remainingCoverageForGap(gap, remainingGaps, job.timeframeSeconds);
      return {
        ...gap,
        attempts,
        recoveredCandles: gap.missingCandles - remainingCandles,
        remainingCandles,
        status: remainingCandles ? "source_gap" : "recovered",
      };
    });
    return { candles, records, coverageComplete: !remainingGaps.length };
  }

  function verifyCollectedCandles(job, candles, coverageComplete) {
    const verification = verifySavedCandles(candles, {
      from: job.mode === "count" ? candles[0]?.time : job.requestedFrom,
      to: job.requestedTo,
      timeframeSeconds: job.timeframeSeconds,
    });
    if (!verification.valid) {
      const failed = verification.checks.filter((check) => !check.passed).map((check) => `${check.label}: ${check.detail}`).join("; ");
      throw new Error(`Primary packet integrity verification failed: ${failed}`);
    }
    log(job, coverageComplete ? "success" : "warn", coverageComplete
      ? `Packet integrity and source-timeframe coverage verification passed for ${candles.length.toLocaleString("en-US")} candle(s).`
      : `Packet integrity passed for ${candles.length.toLocaleString("en-US")} candle(s), but source-timeframe coverage remains incomplete after precise replays.`);
    return candles;
  }

  function saveExtractedCandles(job, candles, { coverageComplete, effectiveRequestedFrom }) {
    const saveFrom = Number(effectiveRequestedFrom);
    if (!Number.isSafeInteger(saveFrom) || !candles.length || candles[0].time < saveFrom) {
      throw new Error("The selected FARAZ continuation range is invalid.");
    }
    let gaps = 0;
    for (let index = 1; index < candles.length; index++) if (candles[index].time - candles[index - 1].time > job.timeframeSeconds) gaps++;
    fs.mkdirSync(outputDir, { recursive: true });
    fs.mkdirSync(temporaryOutputDir, { recursive: true });
    const filename = buildCandleFilename(job.symbolName, job.resolution, candles[0].time, candles.at(-1).time);
    const { broker, symbol } = marketIdentity(job.symbolName);
    job.outputPath = path.join(outputDir, broker.toUpperCase(), symbol.toUpperCase(), filename);
    const serialized = JSON.stringify(candles);
    if (fs.existsSync(job.outputPath)) {
      const existing = fs.readFileSync(job.outputPath, "utf8");
      if (existing !== serialized) throw new Error(`A different candle file already exists at data/raw/${filename}.`);
      const validation = verifySavedCandles(JSON.parse(existing), {
        from: saveFrom, to: job.requestedTo, timeframeSeconds: job.timeframeSeconds,
      });
      job.validation = validation.checks;
      if (!validation.valid) throw new Error("Existing RAW file validation failed; it was not reused.");
    } else {
      const temporaryPath = path.join(temporaryOutputDir, `${job.id}.json.tmp`);
      let published = false;
      try {
        fs.writeFileSync(temporaryPath, serialized, { encoding: "utf8", flag: "wx" });
        const validation = verifySavedCandles(JSON.parse(fs.readFileSync(temporaryPath, "utf8")), {
          from: saveFrom, to: job.requestedTo, timeframeSeconds: job.timeframeSeconds,
        });
        job.validation = validation.checks;
        if (!validation.valid) {
          for (const check of validation.checks.filter((item) => !item.passed)) log(job, "error", `Saved-file check failed: ${check.label}. ${check.detail}`);
          throw new Error("Saved RAW file validation failed; it was not moved into data/raw.");
        }
        const written = fs.readFileSync(temporaryPath);
        const expectedHash = createHash("sha256").update(serialized).digest("hex");
        const writtenHash = createHash("sha256").update(written).digest("hex");
        if (expectedHash !== writtenHash) throw new Error("Saved RAW file hash verification failed; the temporary file was not published.");
        fs.mkdirSync(path.dirname(job.outputPath), { recursive: true });
        fs.renameSync(temporaryPath, job.outputPath);
        published = true;
      } finally {
        if (!published && fs.existsSync(temporaryPath)) fs.unlinkSync(temporaryPath);
      }
    }
    const resource = rawStore.write({ broker, symbol, timeframe: job.resolution, candles,
      requestedRange: { from: job.requestedFrom, to: job.requestedTo },
      effectiveRange: { from: candles[0].time, to: candles.at(-1).time }, source: "faraz" });
    job.outputPath = resource.dataPath;
    Object.assign(job, {
      running: false,
      done: true,
      completedAt: Date.now(),
      stage: coverageComplete ? "Saved to data/raw" : "Saved from first available source candle",
      status: coverageComplete ? "Done" : "Saved from available source data",
      coverageComplete,
      continuedFromAvailable: !coverageComplete,
      awaitingCoverageDecision: false,
      candleCountResult: candles.length,
      gaps,
      fileName: filename,
      savedPath: `data/raw/${resource.id}`,
      finalFrom: candles[0].time,
      finalTo: candles.at(-1).time,
      effectiveRequestedFrom: saveFrom,
    });
    log(job, coverageComplete ? "success" : "warn", `${candles.length} candles were saved to data/raw/${resource.id}.`);
  }

  async function runJob(job) {
    loadStoredSession();
    const status = await authStatus(job.symbolName);
    if (!status.connected) throw new Error("FARAZ authentication is required.");
    const collected = [];
    let cursor = 0;
    while (cursor < job.chunks.length) {
      if (job.abort.cancelled) throw new Error("Extraction cancelled.");
      job.stage = "Fetching candles";
      const batchStart = cursor;
      const batch = job.chunks.slice(cursor);
      log(job, "info", `Primary collection started for ${batch.length} packet(s) using ${PRIMARY_CONCURRENCY} concurrent worker(s); request starts are paced every ${job.rateLimitMs} ms.`);
      const rowsByChunk = await runConcurrent(job, batch, PRIMARY_CONCURRENCY, async (chunk, index) => {
        const packetNumber = batchStart + index + 1;
        job.sentPackets++;
        const rows = await fetchChunk(job, chunk);
        job.receivedPackets++;
        job.receivedRows += rows.length;
        logPacketProgress(job, packetNumber, rows);
        return rows;
      });
      collected.push(...rowsByChunk);
      cursor += batch.length;
      const primarySoFar = mergeCandles(collected, job.requestedFrom, job.requestedTo);
      if (primarySoFar.conflicts) throw new Error(`Extraction found ${primarySoFar.conflicts} conflicting duplicate candle(s); nothing was saved.`);
      if (cursor === job.chunks.length && job.mode === "count") {
        const merged = primarySoFar;
        if (merged.candles.length < job.candleCount) {
          const missing = job.candleCount - merged.candles.length;
          const currentSlots = Math.max(1, (job.requestedTo - job.requestedFrom) / job.timeframeSeconds);
          const density = merged.candles.length / currentSlots;
          const extensionSlots = Math.max(job.packetSize, Math.ceil((missing / Math.max(0.05, density)) * 1.15));
          const expandedFrom = job.requestedFrom - extensionSlots * job.timeframeSeconds;
          const extra = chunkRange(expandedFrom, job.requestedFrom, job.timeframeSeconds, job.packetSize, job.chunks.length);
          if (job.chunks.length + extra.length > MAX_PACKETS) throw new Error("The request exceeds the packet safety limit.");
          job.requestedFrom = expandedFrom;
          for (const extraChunk of extra) job.chunks.push(extraChunk);
          log(job, "warn", `${merged.candles.length}/${job.candleCount} candles collected; appended ${extra.length} older packet(s).`);
        }
      }
    }
    const primaryMerged = mergeCandles(collected, job.requestedFrom, job.requestedTo);
    const coverageRecovery = await recoverCoverageGaps(job, primaryMerged.candles);
    const merged = mergeCandles([coverageRecovery.candles], job.requestedFrom, job.requestedTo);
    let candles = merged.candles;
    if (job.mode === "count") candles = candles.slice(-job.candleCount);
    if (!candles.length) throw new Error("No valid candles were returned for the requested range.");
    if (job.mode === "count" && candles.length !== job.candleCount) throw new Error(`Only ${candles.length}/${job.candleCount} candles were available.`);
    if (merged.conflicts) throw new Error(`Extraction found ${merged.conflicts} conflicting duplicate candle(s); nothing was saved.`);
    job.stage = "Verifying completeness";
    candles = verifyCollectedCandles(job, candles, coverageRecovery.coverageComplete);
    if (job.mode === "count") candles = candles.slice(-job.candleCount);
    Object.assign(job, { duplicates: merged.duplicates, conflicts: merged.conflicts, suspiciousGaps: coverageRecovery.records });
    if (!coverageRecovery.coverageComplete) {
      Object.assign(job, {
        running: false,
        done: false,
        awaitingCoverageDecision: true,
        stage: "Source data unavailable",
        status: "Decision required",
        coverageComplete: false,
        continueFrom: candles[0].time,
        pendingCandles: candles,
      });
      log(job, "warn", `FARAZ has no data for part of the requested range. No file was saved; choose whether to cancel or continue from ${tehranDisplayTime(candles[0].time)}.`);
      return;
    }
    saveExtractedCandles(job, candles, { coverageComplete: true, effectiveRequestedFrom: job.requestedFrom });
  }

  function resolveCoverageDecision(job, decision) {
    if (!job?.awaitingCoverageDecision) throw new Error("This extraction is not waiting for a source-data decision.");
    if (decision === "cancel") {
      delete job.pendingCandles;
      Object.assign(job, {
        awaitingCoverageDecision: false,
        cancelledByUser: true,
        cancelledAt: Date.now(),
        stage: "Cancelled before saving",
        status: "Cancelled",
      });
      log(job, "warn", "Extraction cancelled by the user because FARAZ has no data for part of the requested range. No file was saved.");
      return publicJob(job);
    }
    if (decision !== "continue_from_available") throw new Error("Choose cancel or continue_from_available.");
    const candles = job.pendingCandles?.filter((candle) => candle.time >= job.continueFrom) || [];
    if (!candles.length) throw new Error("No FARAZ candles are available after the selected continuation point.");
    saveExtractedCandles(job, candles, { coverageComplete: false, effectiveRequestedFrom: job.continueFrom });
    delete job.pendingCandles;
    log(job, "warn", `The user continued the export from the first available FARAZ candle at ${tehranDisplayTime(job.continueFrom)}.`);
    return publicJob(job);
  }

  async function startJob(params) {
    if (shuttingDown) throw new Error("FARAZ service is shutting down.");
    const symbolName = String(params.symbolName || "").trim();
    const resolution = String(params.resolution || "").trim().toUpperCase();
    if (!symbolName) throw new Error("Symbol is required.");
    const timeframeSeconds = parseResolutionToSeconds(resolution);
    const packetSize = Math.min(1000, Math.max(1, Math.trunc(Number(params.packetSize) || 1000)));
    const rateLimitValue = Number(params.rateLimitMs);
    const rateLimitMs = Math.min(MAX_RATE_LIMIT_MS, Math.max(30, Number.isFinite(rateLimitValue) ? Math.trunc(rateLimitValue) : 30));
    const mode = params.mode === "range" ? "range" : "count";
    const originalRequestedTo = Math.trunc(Number(params.to));
    const candleCount = mode === "count" ? Math.max(1, Math.trunc(Number(params.candleCount) || 1000)) : null;
    const originalRequestedFrom = mode === "count"
      ? originalRequestedTo - Math.ceil(candleCount * timeframeSeconds * 1.35)
      : Math.trunc(Number(params.from));
    if (!Number.isFinite(originalRequestedTo) || originalRequestedTo <= 0) throw new Error("End timestamp must be a valid Unix epoch.");
    if (mode === "range" && (!Number.isFinite(originalRequestedFrom) || originalRequestedFrom >= originalRequestedTo)) throw new Error("From timestamp must be earlier than To.");
    const requestedFrom = mode === "range" ? Math.ceil(originalRequestedFrom / timeframeSeconds) * timeframeSeconds : originalRequestedFrom;
    const requestedTo = Math.floor(originalRequestedTo / timeframeSeconds) * timeframeSeconds;
    if (requestedFrom > requestedTo) throw new Error("The selected range contains no complete timeframe slot.");
    const chunks = chunkRange(requestedFrom, requestedTo, timeframeSeconds, packetSize);
    const id = randomUUID();
    const host = safeHost(params.host || historyAuth?.host);
    const capturedEndpoint = historyAuth?.endpoint && new URL(historyAuth.endpoint).host === host ? historyAuth.endpoint : null;
    const captureResponses = Boolean(params.captureResponses);
    const responseAuditPath = captureResponses ? path.join(temporaryOutputDir, `${id}.faraz-responses.ndjson`) : null;
    if (responseAuditPath) fs.mkdirSync(temporaryOutputDir, { recursive: true });
    const job = { id, running: true, done: false, error: null, stage: "Preparing", status: "Starting", mode, symbolName, endpointSymbolName: endpointSymbolName(symbolName), resolution, timeframeSeconds, packetSize, rateLimitMs, candleCount, requestedFrom, originalRequestedFrom, requestedTo, originalRequestedTo, rangeAdjusted: requestedFrom !== originalRequestedFrom || requestedTo !== originalRequestedTo, host, endpoint: capturedEndpoint || `https://${host}${HISTORY_PATH}`, adjustType: historyAuth?.adjustType || "2", primaryConcurrency: PRIMARY_CONCURRENCY, retryConcurrency: PRIMARY_CONCURRENCY, sentPackets: 0, receivedPackets: 0, receivedRows: 0, outsideRangePackets: 0, outsideRangeRows: 0, totalPackets: chunks.length, coverageComplete: null, captureResponses, responseAuditPath, capturedResponseCount: 0, createdAt: Date.now(), updatedAt: Date.now(), chunks, logs: [], validation: [], abort: { cancelled: false }, cancelRequested: false, requestControllers: new Set(), nextRequestAt: Date.now(), retryCooldownUntil: 0 };
    jobs.set(id, job);
    log(job, "info", `Extraction prepared with ${chunks.length} packet(s).`);
    runJob(job).catch((error) => {
      Object.assign(job, { running: false, done: false, failedAt: Date.now(), stage: error.message === "Extraction cancelled." ? "Cancelled" : "Error", status: "Failed", error: error.message });
      log(job, error.message === "Extraction cancelled." ? "warn" : "error", `${describeError(error)}; jobId=${job.id}; symbol=${job.endpointSymbolName}; resolution=${job.resolution}; endpoint=${job.endpoint}; requestedRange=${tehranDisplayTime(job.requestedFrom)}→${tehranDisplayTime(job.requestedTo)}; sentPackets=${job.sentPackets}; receivedPackets=${job.receivedPackets}; receivedRows=${job.receivedRows}.`);
    }).finally(() => {
      job.requestController = null;
      job.requestControllers?.clear();
    });
    return publicJob(job);
  }

  return {
    name: "faraz-candle-export-api",
    shutdown,
    configureServer(server) {
      server.watcher?.once("close", () => { void shutdown(); });
      server.httpServer?.once("close", () => { void shutdown(); });
      // Authentication is intentionally user-driven. Status checks inspect a
      // saved file without a browser and migrate legacy DPAPI files once.
      server.middlewares.use("/api/faraz/auth/open", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try { await ensureContext({ showLogin: true }); json(res, 200, { ok: true, state: "waiting_for_login" }); }
        catch (error) { json(res, 500, { error: error.message }); }
      });
      server.middlewares.use("/api/faraz/auth/browser", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try { await ensureContext({ showBrowser: true }); json(res, 200, { ok: true }); }
        catch (error) { json(res, 500, { error: error.message }); }
      });
      server.middlewares.use("/api/faraz/auth/status", async (req, res) => {
        const symbol = new URL(req.url || "", "http://localhost").searchParams.get("symbolName") || undefined;
        json(res, 200, await authStatus(symbol));
      });
      server.middlewares.use("/api/faraz/auth/logout", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try { await logoutFromLoginBrowser(); json(res, 200, { ok: true, state: "not_connected" }); }
        catch (error) { json(res, 500, { error: error.message }); }
      });
      server.middlewares.use("/api/faraz/candles/start", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try {
          const status = await authStatus();
          if (!status.connected) return json(res, 401, { error: "Sign in to FARAZ before starting extraction." });
          json(res, 202, await startJob(await readJson(req)));
        } catch (error) { json(res, 400, { error: error.message }); }
      });
      server.middlewares.use("/api/faraz/candles/status", (req, res) => {
        const id = new URL(req.url || "", "http://localhost").searchParams.get("id");
        const job = jobs.get(id);
        job ? json(res, 200, publicJob(job)) : json(res, 404, { error: "Extraction was not found." });
      });
      server.middlewares.use("/api/faraz/candles/cancel", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try {
          const { id } = await readJson(req);
          const job = jobs.get(id);
          if (!job) return json(res, 404, { error: "Extraction was not found." });
          job.abort.cancelled = true;
          job.cancelRequested = true;
          job.requestController?.abort();
          for (const controller of job.requestControllers || []) controller.abort();
          json(res, 200, { ok: true });
        } catch (error) { json(res, 400, { error: error.message }); }
      });
      server.middlewares.use("/api/faraz/candles/coverage-decision", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try {
          const { id, decision } = await readJson(req);
          const job = jobs.get(id);
          if (!job) return json(res, 404, { error: "Extraction was not found." });
          json(res, 200, resolveCoverageDecision(job, decision));
        } catch (error) { json(res, 400, { error: error.message }); }
      });
      server.middlewares.use("/api/faraz/candles/open", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        const id = new URL(req.url || "", "http://localhost").searchParams.get("id");
        const job = jobs.get(id);
        try {
          if (!job?.done || !job.outputPath) throw new Error("Export file is not ready.");
          await openSavedFile(job.outputPath);
          json(res, 200, { ok: true });
        } catch (error) { json(res, 404, { error: error.message }); }
      });
      server.middlewares.use("/api/faraz/candles/download", (req, res) => {
        const id = new URL(req.url || "", "http://localhost").searchParams.get("id");
        const job = jobs.get(id);
        if (!job?.done || !job.outputPath || !fs.existsSync(job.outputPath)) return json(res, 404, { error: "Export file is not ready." });
        res.setHeader("Content-Type", "application/json; charset=utf-8");
        res.setHeader("Content-Disposition", `attachment; filename*=UTF-8''${encodeURIComponent(job.fileName)}`);
        res.setHeader("Cache-Control", "no-store");
        fs.createReadStream(job.outputPath).pipe(res);
      });

      // ---- Update Chart Data Endpoint ----
      // Appends new candles to an existing file and renames it with updated TO timestamp.
      server.middlewares.use("/api/candle-files/update", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try {
          // A multi-hour 1S update can legitimately contain thousands of
          // candles. Keep the normal API body limit small, but allow this
          // validated endpoint enough room for a bounded candle batch.
          const params = await readJson(req, 25_000_000);
          const fileId = String(params.id || "").trim();
          const newCandles = Array.isArray(params.newCandles) ? params.newCandles.map((row) => ({
            time: Math.trunc(Number(row?.time)),
            open: Number(row?.open),
            high: Number(row?.high),
            low: Number(row?.low),
            close: Number(row?.close),
          })) : [];
          const lastCandleTime = Math.trunc(Number(params.lastCandleTime));

          if (!fileId) return json(res, 400, { error: "File ID is required." });
          if (!Array.isArray(newCandles) || !newCandles.length) return json(res, 400, { error: "No new candles provided." });
          if (!Number.isFinite(lastCandleTime) || lastCandleTime <= 0) return json(res, 400, { error: "Invalid lastCandleTime." });

          const resource = rawStore.resolve(fileId);
          if (!resource) return json(res, 404, { error: "Candle file was not found or its logical ID is invalid." });
          const filePath = resource.dataPath;
          const existingCandles = JSON.parse(fs.readFileSync(filePath, "utf8"));
          if (!Array.isArray(existingCandles) || !existingCandles.length) return json(res, 400, { error: "Invalid candle file format." });
          const timeframeMatch = fileId.match(/(?:^|[\s_])(\d+[SMHD])(?:[\s_]|FROM|$)/i);
          if (!timeframeMatch) return json(res, 400, { error: "The candle file timeframe could not be determined." });
          const timeframeSeconds = parseResolutionToSeconds(timeframeMatch[1]);
          const validCandle = (row) => Number.isSafeInteger(row.time) && row.time > 0
            && [row.open, row.high, row.low, row.close].every(Number.isFinite)
            && row.high >= Math.max(row.open, row.close, row.low)
            && row.low <= Math.min(row.open, row.close, row.high);
          if (!newCandles.every(validCandle)) return json(res, 400, { error: "One or more new candles are invalid." });
          if (newCandles.some((row, index) => index && row.time <= newCandles[index - 1].time
            || index && (row.time - newCandles[index - 1].time) % timeframeSeconds !== 0)) {
            return json(res, 400, { error: "New candles are not chronological at the source timeframe." });
          }
          const firstExistingTime = Number(existingCandles[0]?.time);
          const existingLastTime = Number(existingCandles.at(-1)?.time);
          const existingValidation = verifySavedCandles(existingCandles, {
            from: firstExistingTime, to: existingLastTime, timeframeSeconds,
          });
          if (!existingValidation.valid) return json(res, 409, { error: "The existing RAW candle file is invalid." });
          if (newCandles.some((row) => (row.time - firstExistingTime) % timeframeSeconds !== 0)) {
            return json(res, 400, { error: "One or more candles do not align with the RAW file timeframe." });
          }

          const { candles: merged, added, ignoredExisting } = mergeChartUpdateCandles(existingCandles, newCandles);
          const mergedLastTime = Number(merged.at(-1)?.time);
          if (lastCandleTime !== mergedLastTime) return json(res, 409, { error: "lastCandleTime must match the final merged candle." });

          const identity = parseRawFilename(path.basename(fileId));
          if (!identity) return json(res, 409, { error: "The existing RAW filename does not follow the required readable contract." });
          const newName = buildCandleFilename(`${identity.broker}:${identity.symbol}`, identity.timeframe, firstExistingTime, mergedLastTime).replace(/\.json$/, "");
          const directoryId = path.posix.dirname(fileId);
          const newFileId = directoryId === "." ? `${newName}.json` : `${directoryId}/${newName}.json`;
          const newFilePath = path.join(inputDir, ...newFileId.split("/"));
          if (newFileId !== fileId && fs.existsSync(newFilePath)) return json(res, 409, { error: "A candle file with the updated name already exists." });

          const serialized = JSON.stringify(merged);
          const temporaryPath = path.join(temporaryOutputDir, `update-${randomUUID()}.json.tmp`);
          fs.mkdirSync(temporaryOutputDir, { recursive: true });
          fs.writeFileSync(temporaryPath, serialized, { encoding: "utf8", flag: "wx" });
          try {
            const validation = verifySavedCandles(merged, {
              from: firstExistingTime, to: mergedLastTime, timeframeSeconds,
            });
            if (!validation.valid) throw new Error("Merged candle validation failed.");
            replaceFileWithRetry(temporaryPath, filePath);
          } finally {
            if (fs.existsSync(temporaryPath)) fs.unlinkSync(temporaryPath);
          }

          if (newFileId !== fileId) {
            moveFileWithRetry(filePath, newFilePath);
            if (fs.existsSync(resource.metaPath)) moveFileWithRetry(resource.metaPath, `${newFilePath}.meta.json`);
          }

          // Rebuild the sidecar through the resource store so every persisted
          // date stays human-readable and the content hash/count stay current.
          rawStore.list();

          json(res, 200, {
            ok: true,
            message: `Chart updated with ${added} recovered or new candles.`,
            received: newCandles.length,
            added,
            ignoredExisting,
            total: merged.length,
            newId: newFileId !== fileId ? newFileId : undefined,
          });
        } catch (error) {
          json(res, 500, { error: error.message });
        }
      });
      // Records the exact source-timeframe slots that the authenticated FARAZ
      // proxy has checked. This is deliberately separate from candle writes:
      // an empty but retried response is still durable evidence and must not
      // trigger the same expensive request on the next chart update.
      server.middlewares.use("/api/candle-files/verification", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try {
          const params = await readJson(req, 25_000_000);
          const fileId = String(params.id || "").trim();
          const timeframeSeconds = Math.trunc(Number(params.timeframeSeconds));
          const ranges = Array.isArray(params.ranges) ? params.ranges : [];
          if (!fileId) return json(res, 400, { error: "File ID is required." });
          if (!Number.isSafeInteger(timeframeSeconds) || timeframeSeconds < 1) return json(res, 400, { error: "A valid source timeframe is required." });
          const candles = rawStore.read(fileId);
          if (!candles) return json(res, 404, { error: "Candle file was not found or its logical ID is invalid." });
          const first = Number(candles[0]?.time);
          const last = Number(candles.at(-1)?.time);
          const metadata = rawStore.recordFarazCoverage(fileId, {
            timeframeSeconds,
            retryCount: params.retryCount,
            ranges,
            candleCount: candles.length,
            effectiveRange: { from: first, to: last },
            checkedThrough: params.checkedThrough,
            mode: params.mode,
          });
          if (!metadata) return json(res, 404, { error: "Candle metadata could not be recorded." });
          json(res, 200, { ok: true, farazCoverage: metadata.farazCoverage });
        } catch (error) {
          json(res, 400, { error: error.message });
        }
      });
      // ---- Faraz History Proxy ----
      // Server-side proxy to faraz.io history endpoint (avoids CORS).
      // Accepts POST { symbolName, resolution, from, to } and returns raw candle data.
      server.middlewares.use("/api/faraz/history", async (req, res) => {
        if (req.method !== "POST") return json(res, 405, { error: "POST is required." });
        try {
          const params = await readJson(req);
          const symbolName = String(params.symbolName || "").trim();
          const resolution = String(params.resolution || "1S").trim().toUpperCase();
          const timeframeSeconds = parseResolutionToSeconds(resolution);
          const from = Math.trunc(Number(params.from));
          const to = Math.trunc(Number(params.to));
          if (!symbolName) return json(res, 400, { error: "symbolName is required." });
          if (!Number.isFinite(from) || from <= 0) return json(res, 400, { error: "Invalid from." });
          if (!Number.isFinite(to) || to < from) return json(res, 400, { error: "Invalid to." });

          // The local session file is authoritative on every chart packet.
          // Sending a separate history/profile probe for each packet multiplied
          // the network round trips on large RAW audits.
          if (!fs.existsSync(secretPath) || !loadStoredSession()) {
            return json(res, 401, { error: "Sign in to FARAZ first.", needAuth: true });
          }

          // Chart gap verification is always against the requested source host,
          // independent of an exporter capture on an ir3/ir4 history mirror.
          const host = "faraz.io";
          const endpoint = historyAuth?.endpoint && new URL(historyAuth.endpoint).host === host
            ? historyAuth.endpoint
            : `https://${host}${HISTORY_PATH}`;

          // Update ranges are split into bounded requests so the FARAZ server
          // receives the same packet shape as the exporter instead of one
          // unbounded history request.
          const requestPacket = async (packet) => {
            const url = new URL(endpoint);
            for (const [key, value] of Object.entries({
              symbolName: endpointSymbolName(symbolName),
              resolution, from: packet.from, to: packet.to,
              countback: packet.countback,
              firstDataRequest: false,
              latest: packet.latest,
              adjustType: historyAuth?.adjustType || "2",
              json: true,
            })) url.searchParams.set(key, String(value));
            let lastError = null;
            for (let attempt = 1; attempt <= MAX_PACKET_ATTEMPTS; attempt++) {
              await waitForChartHistoryRequestSlot();
              try {
                const response = await directRequest(url, { timeoutMs: 30_000 });
                const text = await response.text();
                if (response.status !== 200) {
                  const error = new Error(`FARAZ returned HTTP ${response.status}: ${text}`);
                  error.status = response.status;
                  throw error;
                }
                let payload;
                try { payload = JSON.parse(text); }
                catch {
                  const error = new Error("FARAZ returned invalid JSON with HTTP 200.");
                  error.status = 200;
                  throw error;
                }
                const normalized = normalizeHistoryPayloadDetails(payload);
                if (normalized.rejectedRows) {
                  const error = new Error(`FARAZ returned ${normalized.rejectedRows} malformed candle row(s).`);
                  error.status = 200;
                  throw error;
                }
                return normalized.candles;
              } catch (error) {
                lastError = error;
                if (attempt < MAX_PACKET_ATTEMPTS) {
                  await new Promise((resolve) => setTimeout(resolve, RETRY_BASE_DELAY_MS * attempt));
                }
              }
            }
            const error = new Error(`FARAZ packet ${tehranDisplayTime(packet.from)}→${tehranDisplayTime(packet.to)} failed after ${MAX_PACKET_ATTEMPTS} attempts: ${lastError?.message || "Unknown error"}`);
            error.status = lastError?.status;
            throw error;
          };

          const collected = [];
          for (const packet of chunkRange(from, to, timeframeSeconds, CHART_UPDATE_PACKET_SIZE)) {
            const rows = await requestPacket(packet);
            if (!Array.isArray(rows)) return;
            collected.push(rows);
          }
          json(res, 200, mergeCandles(collected, from, to).candles);
        } catch (error) {
          json(res, error.status === 401 || error.status === 403 ? 401 : 502, { error: error.message, needAuth: error.status === 401 || error.status === 403 });
        }
      });

    },
  };
}

export default createFarazCandleApi();
