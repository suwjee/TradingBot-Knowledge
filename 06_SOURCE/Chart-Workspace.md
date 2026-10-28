---
id: "source.chart_workspace"
type: "source"
status: "active"
authority: "executable"
title: "Current Chart workspace and review presentation"
version: "current"
related_entities: ["core.project","source.local_server","source.raw_resources","source.faraz","source.integration_boundary"]
source_reference: ["06_SOURCE/Code/apps/chart/src/main.js#L1665","06_SOURCE/Code/apps/chart/src/main.js#L2252","06_SOURCE/Code/apps/chart/src/main.js#L5770","06_SOURCE/Code/apps/chart/src/ui/workspace-state.js","06_SOURCE/Code/apps/chart/src/features/workspace-session.js","06_SOURCE/Code/apps/chart/src/features/indicator-lifecycle.js","06_SOURCE/Code/apps/chart/src/features/indicator-calculation-request.js","06_SOURCE/Code/apps/chart/src/features/indicator-cache.js","06_SOURCE/Code/apps/chart/src/chart/lod.js","06_SOURCE/Code/apps/chart/src/chart/view-transform.js","06_SOURCE/Code/apps/chart/src/chart/drawing-coordinates.js","06_SOURCE/Code/apps/chart/src/features/manual-review/entry.js","06_SOURCE/Code/apps/chart/src/features/manual-review/render.js#L736","06_SOURCE/Code/apps/chart/src/features/manual-review/tab.js"]
evidence_basis: "Current live project Source captured for the 2026-10-27 synchronization"
created_at: "2026-10-27T20:16:20+03:30"
last_modified_at: "2026-10-27T20:16:20+03:30"
---

# Current Chart workspace and review presentation

Chart is the native ES-module browser workstation. It owns interaction, display/workspace state, drawings and review of finalized results. Its presentation logic is not canonical trading authority.

## Workspaces and chart identity

The shared shell switches between Chart, FARAZ and Algorithm workspaces. Inactive header/footer groups are hidden, inert and aria-hidden. Fullscreen Chart uses its own chrome-visibility contract. The Algorithm surface is a convenience reference presentation; displayed explanations require independent authority/source verification before engineering use.

The tab URL can hold chartId and chart timeframe. A valid explicit tab identity/timeframe takes precedence over shared browser restoration. Saved workspace values, RAW identity and supported timeframe are validated against current choices. Stable chart identity is distinct from a readable RAW filename and can survive a range-changing acquisition operation.

Inventory refresh requests coalesce. Choosing a newer chart aborts the obsolete candle load; revision checks prevent late responses from replacing current selection. Loaded rows are normalized and validated for strict chronology and OHLC.

## Drawings and display density

Drawings use canonical time/price coordinates. Display-only aggregation and LOD preserve the original candle array for calculation, exports and exact lookup. Coordinate transforms map omitted display candles back to RAW time; density selection uses hysteresis and remains stable during gestures.

Drawing saves retain a browser recovery copy and use one ordered server-save queue so an older slow write cannot overwrite a newer edit. Loading prefers the server and falls back to compatible browser state. Stored geometry is validated; invalid recovered entries are quarantined separately while valid entries remain usable. Undo/redo restores indicator presentation snapshots only when their calculation identity still matches the active calculation.

## Calculation lifecycle

Restored form/range preferences never restore a live calculation. Changing chart/calculation context clears or invalidates incompatible results and in-flight operation ownership. Apply validates enabled state, selected direction and an available ordered inclusive candle range.

Requests carry RAW/chart identity, separate analysis/chart timeframes, inclusive range, direction, enabled calculation support and request identity. Chart tracks the owning operation and rejects stale asynchronous Source probes/results after input or selection changes. Presentation-only reuse requires matching applied context and a verified current calculation-Source fingerprint. The probe alone does not independently verify RAW freshness.

Successful server output becomes the active payload and is projected into visual objects. Visibility/style/offset/filter overrides remain presentation state. Errors remain observable in status/activity without creating an alternative trading decision.

## Manual Review

A persisted calculation identity opens a separate /info report document. The server returns the saved finalized payload and calculation metadata. Missing identities/reports produce an inline failure. The report is a historical calculation context and need not match later Source or RAW.

Review groups supplied events chronologically, supports category/date filtering, lazy expandable/copyable finalized Bridge detail, and True/False/Unselected human annotation. Annotation persistence is keyed by payload hash and report identity and never feeds a trading decision back to Engine. Day bulk actions affect currently visible events. Export/copy supports reviewed rows, True-only, False-only, and all visible rows including UNSELECTED.

## Persistence and scope

Browser state includes selected workspace/chart/timeframe, appearance, toolbar/panel preferences and review annotations. Server persistence includes drawings, templates and finalized calculation artifacts. Scoped cache controls distinguish calculations, browser storage/cache, IndexedDB, drawings and the global-only FARAZ session. User drawings/templates and RAW are not made disposable by their storage location.

These are source-backed contracts with current synthetic/unit evidence. Actual rendering, screen-reader behavior, full accessibility and external authentication require separately recorded runtime verification.

