---
id: "source.local_server"
type: "source"
status: "active"
authority: "executable"
title: "Current local server and calculation coordination"
version: "current"
related_entities: ["core.project","source.integration_boundary","source.raw_resources","source.chart_workspace","source.faraz"]
source_reference: ["06_SOURCE/Code/apps/chart/vite.config.js#L52","06_SOURCE/Code/apps/chart/vite.config.js#L240","06_SOURCE/Code/apps/chart/vite.config.js#L587","06_SOURCE/Code/apps/chart/server/calculation-coordinator.js","06_SOURCE/Code/apps/chart/server/calculation-cache.js","06_SOURCE/Code/apps/chart/server/progress-channels.js","06_SOURCE/Code/apps/chart/server/raw-input-identity.js","06_SOURCE/Code/apps/chart/server/request-body.js","06_SOURCE/Code/apps/chart/server/local-state-paths.js","06_SOURCE/Code/apps/chart/server/candle-file-response.js"]
evidence_basis: "Current live project Source captured for the 2026-10-27 synchronization"
created_at: "2026-10-27T20:16:20+03:30"
last_modified_at: "2026-10-27T20:16:20+03:30"
---

# Current local server and calculation coordination

This is an executable architecture description of the captured implementation. It supplies no new intended trading rule. Vite middleware validates local requests, resolves RAW resources, coordinates Python children, persists finalized payloads and exposes progress/review resources. Python remains the trading-calculation owner.

## Calculation identity and execution

The calculation route validates the selected RAW logical ID, optional stable chart ID, direction, positive whole-number analysis/chart timeframes, ordered safe-integer range and available inclusive chart-candle boundaries. See source.integration_boundary for the input actually supplied to Python.

The configured calculation-Source fingerprint hashes file names and content digests of the configured calculation files. It is content-based rather than a version-label or timestamp check. The configured list must be rediscovered from current Vite Source when it changes; this note does not claim automatic discovery of future Engine modules.

The public cache key includes that fingerprint, chart/resource identity, RAW modification time, analysis/chart timeframes, range, direction, options and supplied-input scope. A second execution identity adds the captured RAW SHA-256. The FIFO coordinator defaults to one active calculation. TRADINGBOT_MAX_ENGINE_CONCURRENCY accepts one integer from 1 through 8; invalid configuration rejects initialization. Equal in-flight execution identities share one job and replay bounded progress to independent callers; failed jobs release their slot and can be retried.

## RAW and persisted-result guards

RAW capture hashes the file between before/after stat checks. The initial digest must match inventory metadata. A cache result is accepted only with its matching .raw-sha256 stamp. If changed RAW bytes retain the previous modification time, the result uses a digest-specific calculation path so the old stamped report remains separately addressable.

RAW is rechecked when queued work starts and before a result is cached, or before a cache hit is returned. The configured calculation-Source fingerprint is also rechecked. A detected change rejects the request instead of persisting a stale result. The server stores serialized Python output and an information sidecar under the readable symbol/timeframe/direction/range calculation tree; it does not repair the payload.

## Progress, lifecycle and local resources

Python stdout carries the final JSON and prefixed stderr records carry progress. The coordinator and SSE channels each bound retained history to 120 events. Late subscribers receive the retained ordered history. An observed finished channel is released when its last client disconnects; unobserved terminal history remains replayable in the process. Shutdown rejects queued work, aborts active owned work, terminates owned Python children and closes progress clients.

Bounded request-body reading counts received bytes, handles split UTF-8, rejects oversize/aborted streams and drains rejected bodies safely. Candle delivery streams the selected file with private cache revalidation; its HTTP ETag uses file size and modification time, separately from calculation SHA identity.

The shared local-state resolver permits only apps/chart/state or its descendants, including physical containment checks. Vite denies direct static access to state, tests and historical/verification areas. Explicit APIs own inventory/candles, drawings, templates, cache layers, RAW actions, transfer and persisted review. Drawings/templates may contain user work and are not interchangeable with rebuildable calculation cache.

## Evidence limits

Source and focused synthetic tests establish these contracts. They do not prove live FARAZ availability, browser rendering, market-data correctness, or a trading regression. A saved report identifies a prior calculation context; reading it does not establish that it matches later RAW or Source.

