---
id: "source.raw_resources"
type: "source"
status: "active"
authority: "executable"
title: "Current RAW resources, identity and transfer"
version: "current"
related_entities: ["core.project","source.local_server","source.faraz","source.chart_workspace","source.integration_boundary"]
source_reference: ["06_SOURCE/Code/apps/chart/server/raw-resource-store.js","06_SOURCE/Code/apps/chart/server/chart-update-merge.js","06_SOURCE/Code/apps/chart/server/chart-transfer.js","06_SOURCE/Code/apps/chart/src/features/raw-file-contract.js","06_SOURCE/Code/apps/chart/src/features/candle-update.js","06_SOURCE/Code/apps/chart/vite.config.js#L357"]
evidence_basis: "Current live project Source captured for the 2026-10-27 synchronization"
created_at: "2026-10-27T20:16:20+03:30"
last_modified_at: "2026-10-27T20:16:20+03:30"
---

# Current RAW resources, identity and transfer

The RAW store owns validated local market-data resources and metadata. This describes data acquisition/persistence rather than intended trading semantics.

## Resource and metadata contract

A logical RAW ID resolves beneath the dedicated RAW root; absolute/traversal IDs and metadata-sidecar IDs are rejected. Resources are nested by broker and symbol. Readable filenames encode broker, symbol, source timeframe and first/last candle times in Asia/Tehran. The filename parser requires the maintained contract instead of treating every JSON file as a market resource.

Each candle contains exactly time, open, high, low and close. The store validates nonempty input, positive safe-integer chronology, strict ascending unique times, finite OHLC and OHLC bounds. It serializes compact candle JSON. An identical resource identity may be reused only when its serialized bytes agree; conflicting content at that identity is rejected.

The schema-versioned metadata sidecar includes a stable UUID chartId, broker/symbol/timeframe/source, filename, candle count, byte count, SHA-256, readable requested/actual ranges and creation/update times. Runtime consumers receive hydrated epoch ranges. Inventory validates files, heals missing or invalid metadata identity and caches validated entries by data/sidecar size and modification time. Inventory is therefore not a purely passive filesystem read: it may write repaired sidecars. Calculation execution independently verifies current RAW content.

## Explicit RAW operations

Inclusive cut supports replace and new modes. Replace retains chart identity and original creation provenance; a new resource gets a new identity. Empty/reversed selections and colliding destination identities are rejected. Deletion removes RAW and its sidecar; the Vite owner also clears matching drawing/calculation artifacts.

Chart update merges validated chronological rows without replacing saved rows at matching timestamps. Internal recovered candles and appended candles remain sorted. The server validates source-timeframe alignment and final merged time, replaces the RAW contents through a temporary output, renames the readable filename when its range changes, and rebuilds metadata while retaining chart identity. These are explicit user acquisition/edit operations, not permission to modify RAW during testing.

Per-file FARAZ coverage is separate metadata evidence. It can record complete and source_missing ranges, source timeframe, checkpoint and operation context without changing candle bytes. New overlapping coverage replaces earlier coverage for that range. A checked source absence remains a visible data gap; it is not a fabricated candle or proof of complete chronology.

## Chart transfer

The versioned tradingbot-chart-transfer bundle includes a manifest, RAW array, metadata and drawings. Validation checks the bundle kind/version, candle chronology/OHLC, safe manifest names/logical IDs and drawing objects. Import writes through the canonical RAW store and saves the supplied drawings through the receiving Chart owner. It retains valid supplied chart identity/provenance and normalizes destination metadata.

Transfer is a supported chart-level portability feature. It does not establish project-wide backup coverage for all local preferences, templates, reports, authentication, or historical evidence.

