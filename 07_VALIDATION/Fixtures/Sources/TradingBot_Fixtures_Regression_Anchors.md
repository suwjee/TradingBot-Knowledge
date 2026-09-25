# Curated retained fixture anchors

This Vault-local copy excludes the superseded physical Order routes and their dependent cases.
The original mixed document is outside this Vault. Remaining assertions retain their section IDs,
but their source hash and line anchors refer to this curated copy only.

# TradingBot Fixtures / Regression Anchors

این فایل شامل تمام Fixtureها و Regression Anchorهایی است که از گفتگوهای قبلی و Referenceهای فعلی بازیابی شده‌اند.

نکته:
- موارد **Active** باید به‌عنوان Regression Anchor فعلی حفظ شوند.
- موارد **Historical / Superseded** فقط سابقه‌ی نسخه‌های قبلی هستند و نباید به‌عنوان Expected فعلی استفاده شوند.
- هیچ Fixture، timestamp، symbol، price یا RAW-specific branch نباید وارد Production Rule شود.

---

## 1. RAW: `RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json`
Main TF: 30s

### 1.1 2026-08-25 — Order_A ownership / immutable first Order
- Direction: Bearish
- A: `09:32:30`
- بعد از Stop شدن A، اولین Order معتبر مالک `parent-stop` می‌ماند.
- Physical identity قبلی: `(FirstIndex, BreakIndex) = (689,693)`
- Mode-Bهای بعدی حق ندارند Order_A را refresh کنند.
- Status: **Active current anchor**

### 1.4 2026-08-26 — A→S / native Mode-B eligibility anchor #1
- A: `10:55:30`
- Expected S Red: `11:04:00`
- Expected: **S Red, not StopAll1**
- Status: **Active regression anchor**

### 1.5 2026-08-26 — A→S / native Mode-B eligibility anchor #2
- A: `22:41:30`
- Expected S Red: `23:00:00`
- Expected: **S Red, not StopAll1**
- Status: **Active regression anchor**

### 1.6 2026-08-28 — A→S / native Mode-B eligibility anchor #3
- A: `08:31:30`
- Correct S candle: `08:56:30`
- Earlier `08:57:00` result was corrected by exact RAW chronology.
- Expected: **S Red, not StopAll1**
- Status: **Active regression anchor**

### 1.7 V5.4.2 lifecycle chain — Bearish
- Invalid A that must not exist: `11:07:00`
- Correct A: `11:15:30`
- S Red: `11:54:30`
- Second S Red: `12:47:00`
- StopAll1: `13:20:30`
- StopAll2: `15:20:30`
- Fresh cycle:
  - E1 Blue: `16:21:30`
  - A: `17:36:30`, then stops
  - S Red: `17:43:00`
  - E1 Red: `17:56:30`
- Expected: `S Red 17:43:00` must not immediately become StopAll from pre-StopAll state.
- Status: **Active lifecycle/StopAll boundary regression**

### 1.8 V5.4.3 dominant Red E / cycle ownership
- StopAll boundary: `2026-08-26 02:21:30`
- E1 Red repeats:
  - `2026-08-26 06:13:30`
  - `2026-08-26 09:00:30`
  - `2026-08-27 03:34:30`
- S Red: `2026-08-27 03:55:00`
- Expected: accepted S Red, **not StopAll**
- A `2026-08-27 04:41:30`: expected absent / cycle-invalid
- Status: **Active regression anchor**

### 1.9 Canonical Bullish Order geometry inside Bearish regression
- Date: `2026-08-27`
- Order First: `08:36:30`
- BoxTop: `4620.825`
- BoxTop source main: `08:36:00`
- BoxBottom: `4619.565`
- BoxBottom source main: `08:37:00`
- Exact lower event: `08:37:10`
- Breakout main: `08:37:30`
- Later low `08:37:50`: post-confirmation and must not rewrite BoxBottom
- Status: **Active exact-confirmation geometry fixture**

### 1.10 2026-08-28 — exact-key StopAll
- E3 Blue: only one occurrence
- S Red: `03:41:00`
- Expected: **not StopAll**
- E1→E2→E3 must not count as three occurrences of one Blue group.
- Status: **Active**

### 1.11 2026-08-28 — S Blue Type-4
- A: `06:22:00`, then Stop
- Bearish Reaction:
  - First: `06:31:30`
  - Breakout: `06:32:00`
- Type-4 candidate:
  - Main source: `06:30:30`
  - Price: `4587.505`
- Blue: `06:34:00`
- Exact strict crossing: `06:34:15`
- Expected: `S Blue Type-4`
- Status: **Active Type-4 fixture**

### 1.12 2026-09-04 02:36:00 — repeated-Blue reversal StopAll
- Current valid direction: Bearish
- Expected: `StopAll1`
- Gate: `opposite-s-group-stop`
- Incoming S Red has native Mode-B formation Order
- Historical Bullish version of the same timestamp is not current expected
- Status: **Active Bearish anchor / Bullish version superseded**

### 1.13 2026-09-09 — historical Mode-B refresh chain
- A: `03:33:30`
- Consecutive opposite native Mode-B Order Firsts:
  - `04:16:00`
  - `04:17:30`
  - `04:20:30`
  - `04:24:00`
- Historical final Order stop source: `04:21:00`
- Under old V5.4.5:
  - final owner = `04:24:00`
  - S Red = `04:29:30`
  - S Blue `04:45:00` removed
  - E1 Red = `05:15:30`
  - StopAll = `06:23:00`
- Under current V5.4.8+:
  - Order_A remains First `04:16:00`
  - `04:24:00` cannot inherit its parent-stop
  - `S Red 04:29:30` is not current expected
  - current full-RAW emits `S Blue 04:45:00`
- Status: **Historical / Superseded, retained as regression provenance**

---

## 2. RAW: `RAW FOREXCOM_XAUUSD 5S FROM 2026-09-03 18-44-00 TO 2026-09-19 00-29-35.json`
Main TF: 30s

Note: older Reference text sometimes names the same source with suffix `(1).json`.

### 2.3 2026-09-17 — Exact-source E continuation
- Direction: Bullish chain
- E1 Blue: `07:50:00`
- E2 Blue: `08:00:00`
- E3 Blue: `08:54:00`
- Calculation-invalid S Red at `08:00:00` may remain evidence/Order provenance
- It must not open competing cross-family E1
- Incorrect E1 Red `08:54:00`: must not exist
- Status: **Active same-source ownership fixture**

### 2.4 2026-09-17 — downstream StopAll consequence
- Historical incorrect StopAll: `18:30:30`
- Expected current: **absent**
- Reason: invalid Red E root no longer exists
- Status: **Active negative regression fixture**

### 2.5 2026-09-17 — S reversal historical example
- S Red: `16:15:00`
- Previously described as StopAll
- Current expected: ordinary `S Red` with native Mode-A Order
- Status: **Historical / Superseded StopAll expectation**

---

## 3. RAW: `RAW FOREXCOM_XAUUSD 1S FROM 2026-09-03 19-05-40 TO 2026-09-08 03-18-28.json`

### 3.1 2026-09-04 — exact lower-TF Reaction confirmation / A ownership
- Direction: Bearish
- A source: `16:57:30`
- Bearish Reaction FirstGreen: `16:58:00`
- BoxBottom source: `16:57:30`
- BoxTop source: `16:58:00`
- Exact 1s breakdown confirmation: `16:58:38`
- Expected: A source freezes at exact confirmation
- Wrong candidate: moving A to `16:58:30`
- Status: **Active exact chronology fixture**

### 3.2 2026-09-07 — bounded Mode-A anchor
- Direction: Bearish
- Reference Order: `10:14:00`
- Stop source: `10:13:30`
- Expected: resolved current-leg Mode-A anchor remains authoritative
- An older Reset must not overwrite it merely because historical Reset provenance exists
- Status: **Active geometry/anchor fixture**

---

## 4. RAW: `RAW FXCM_USOIL 5S FROM 2026-09-08 07-23-20 TO 2026-09-12 00-14-55.json`
Main TF: 30s

### 4.1 2026-09-09 — same-Break Bullish confirmation/reset
- Bullish Reaction Break main candle: `19:09:30`
- Exact confirmation: `19:09:45`
- Later lower event in same main candle: `19:09:50`
- Expected: `19:09:30` remains Reset boundary
- It cannot simultaneously become next normal Bullish FirstRed
- Status: **Active Reaction/Reset chronology fixture**

### 4.3 2026-09-10 — stage ownership / invalid fallback
- Direction: Bullish
- Competing S Red: `13:51:00` → expected rejected
- E1 Blue: `13:56:00`
- E2 Blue: `14:26:30`
- Expected continuation: `E1 Blue → E2 Blue`
- Rejected A/S fallback cannot reopen accepted later-stage ownership
- Status: **Active A→S→E ownership regression**

---

## 5. RAW: `RAW FXCM_USOIL 5S FROM 2026-09-11 02-53-30 TO 2026-09-15 11-03-45.json`
Main TF: 30s

### 5.1 2026-09-11 — Bearish chained Blue carried-stop
- Blue reference: `09:23:00`
- For a stopped Bearish Blue:
  - locate first valid Bearish Reaction after stop
  - compute maximum High from Blue stop main candle through complete next Bearish Reaction Breakout main candle inclusive
- Status: **Active mirror geometry anchor**

### 5.2 2026-09-11 — stage ownership
- Accepted S Blue: `17:43:00`
- Would-be fallback A: `18:01:30`
- Expected: A `18:01:30` rejected / absent
- Accepted S Blue must not be consumed by rejected A
- Status: **Active stage-order regression**

## 6. RAW: `RAW FOREXCOM_XAUUSD 5S FROM 2026-09-22 11-00-00 TO 2026-09-24 00-05-40.json`
Main TF: 30s

### 6.1 2026-09-22 — stopped dominant E must advance +1
- Direction: Bearish
- E4 Red: `16:02:00`
- E2 stop exact RAW event: `21:22:25`
- E4 stop exact RAW event: `21:22:35`
- S: `21:42:00`
- Correct later E: `E5 Red @ 21:46:00`
- Next: `E6 @ 23:07:30`
- Fixture purpose:
  - after valid dominant En stops
  - a valid continuation must advance to `E(n+1)`
  - it must not repeat E4 or break numbering
- Status: **Active conversation regression anchor**

---

## 7. Three V5.4.6 S Red ≠ StopAll fixtures

All use:
- RAW: `RAW FOREXCOM_XAUUSD 5S FROM 2026-08-25 03-53-30 TO 2026-09-19 00-29-30.json`
- Direction: Bearish
- Main TF: 30s

### Fixture 1
- A: `2026-08-26 10:55:30`
- S Red: `11:04:00`

### Fixture 2
- A: `2026-08-26 22:41:30`
- S Red: `23:00:00`

### Fixture 3
- A: `2026-08-28 08:31:30`
- S Red: `08:56:30`

### Shared expected behavior
- All three remain ordinary `S Red`
- They must not become `StopAll1` merely from stale/repeated Blue history
- Incoming native Order Mode and Red-boundary state must be respected
- Status: **Active regression set**

---

## 8. Historical / Superseded fixtures that must still be preserved

### 8.1 `2026-09-04 02:36:00` Bullish StopAll
- Historical 5.4.4 example
- **Not current expected**
- Bearish StopAll1 at same timestamp remains current retained anchor

### 8.2 `2026-09-09 03:33:30 → 04:24:00 → 04:29:30 → 05:15:30 → 06:23:00`
- Historical V5.4.5 Mode-B refresh chain
- Current V5.4.8+ expected differs

### 8.3 `2026-09-17 16:15:00` Bullish S Red→StopAll
- Historical
- Current: ordinary S Red

### 8.4 `2026-09-17 18:30:30` downstream StopAll
- Historical incorrect consequence
- Current: absent

## Current Reference status

Current standalone Algorithm Reference:
- Version: `5.4.11-HPZR5`
- Full 309,906-row XAUUSD run was verified in both directions.
- Important explicitly retained current anchors include:
  - Bearish native Mode-A Reset `2026-08-26 10:08:00`
  - Bearish `StopAll1 @ 2026-09-04 02:36:00`

---

## Fixture policy

Every fixture above is test/regression evidence only.

Production code must never contain:
- timestamp-specific branches
- symbol-specific branches
- price-specific branches
- RAW filename-specific branches
- fixture-specific branches
- expected-output-specific branches

Every fix must remain a general algorithmic rule and must be checked against:
- RAW chronology
- Reaction / Reset
- Blue
- A
- S
- E
- Lifecycle
- StopAll
- serialization
- Decimal semantics
- strict crossing
- Bullish/Bearish mirror
- lifecycle boundary
- physical Order identity/provenance
- previous regression anchors
