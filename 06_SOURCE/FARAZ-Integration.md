---
id: "source.faraz"
type: "source"
status: "active"
authority: "executable"
title: "Current FARAZ session and acquisition integration"
version: "current"
related_entities: ["core.project","source.local_server","source.raw_resources","source.chart_workspace"]
source_reference: ["06_SOURCE/Code/apps/chart/server/faraz-candle-api.js#L388","06_SOURCE/Code/apps/chart/server/faraz-candle-api.js#L406","06_SOURCE/Code/apps/chart/server/faraz-candle-api.js#L760","06_SOURCE/Code/apps/chart/server/faraz-candle-api.js#L997","06_SOURCE/Code/apps/chart/server/faraz-candle-api.js#L1070","06_SOURCE/Code/apps/chart/server/faraz-candle-api.js#L1209","06_SOURCE/Code/apps/chart/src/features/candle-update.js","06_SOURCE/Code/apps/chart/server/chart-update-merge.js"]
evidence_basis: "Current live project Source captured for the 2026-10-27 synchronization"
created_at: "2026-10-27T20:16:20+03:30"
last_modified_at: "2026-10-27T20:16:20+03:30"
---

# Current FARAZ session and acquisition integration

FARAZ owns external market-data acquisition and session handling. It does not define trading rules. This note records executable integration behavior from pinned Source; it does not claim a live account or external service was tested.

## Session lifecycle

Sign-in is user-driven through an owned temporary Chromium browser. The supported flow captures reusable session state into the dedicated secret owner and closes the temporary browser. FARAZ_BROWSER_PATH can select an executable; otherwise the integration discovers a supported system/default browser.

The reusable artifact retains the legacy name faraz-session.dpapi.json, but the current writer uses editable clear-text format/version 3. It can contain cookies, access credentials, browser storage and captured history endpoint metadata. Legacy Windows current-user DPAPI version 2 can be migrated once. No real values belong in knowledge notes, tests, logs or deliverables.

Requests reread the saved file. Manual edits can change the credentials used, deleting the file removes session authority, and local logout closes the owned browser and clears local state without requiring website logout. Invalid/rejected saved files remain available for explicit correction or logout. Shutdown prevents new jobs, cancels active requests, waits for pending owned launches and closes owned browser resources.

## Acquisition and coverage

History service hosts are allowlisted to faraz.io, ir3.faraz.io and ir4.faraz.io. Chart history verification targets faraz.io. Captured endpoint metadata is reused only within the corresponding validated host boundary.

Exporter jobs support count and explicit range modes. Manual ranges are snapped inward to requested timeframe slots; count mode can extend backward to collect the requested count. Requests use bounded packets, up to six concurrent workers and paced starts. The captured implementation bounds exporter packets to 1000 candles and start spacing to at least 30 ms, with up to four attempts per failed packet and shared retry cooldown. The chart-history proxy similarly splits requests, paces starts and retries transport/HTTP/invalid-payload failures; a successful valid empty or partial response is returned for coverage classification.

Normalization rejects malformed/nonfinite/OHLC-invalid rows. Countback candles outside the requested packet are excluded. Merge preserves chronology and rejects conflicting duplicate candle values before export publication.

Coverage detection includes leading, internal and trailing missing source slots. Bounded replay includes neighboring context, merges replay windows and stops after its recovery bound or when no progress occurs. Missing data after replay pauses the job before saving. The explicit decision is cancel or continue_from_available. Continuation records the actual available interval and incomplete-coverage status; it does not manufacture missing candles.

Temporary saved JSON is reread and checked for schema/OHLC, chronology, bounds, timeframe intervals and matching written content digest before publication into RAW. Identical existing resources can be reused; different contents at the destination are rejected. Optional captured response bodies are diagnostics under temporary acquisition ownership and must be classified before sharing.

## Updating a loaded chart

Chart offers full gap detection, detection after a durable checkpoint, and newest closed-candle acquisition as distinct operations. It uses the RAW source timeframe, not display aggregation, and requests bounded packets in input order. Present rows retain ownership on timestamp ties. Byte-bounded save batches reduce repeated rewrites; partial successful saves remain reflected locally if a later batch fails.

Coverage checkpoints and ranges belong to the individual RAW resource. Recording checked missing slots updates metadata without inventing or altering candles. Source availability and acquisition evidence do not establish any Engine result.

