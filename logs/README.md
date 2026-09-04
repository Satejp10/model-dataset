# Dataset Change Logs

This folder tracks every change to `Pruned AI Models_Table.xlsx` (our pruned copy of
the [LifeArchitect.ai Models Table](https://lifearchitect.ai/models-table/)).

## Files

- `CHANGELOG.md` — reverse-chronological log of changes, plus a live specs snapshot.
  Both the specs block and the dated entries are maintained by the script below.
- `diff_dataset.py` — parses a fresh export, diffs it against the last snapshot, and
  logs the delta.
- `snapshots/latest.json` — the last recorded state of the dataset (the diff baseline).
  Committed so the next diff has something to compare against.
- `build_constellation.py` — builds the browser-ready constellation data in `dist/` from
  that snapshot (step 5 below).

## Why it's semi-manual

The Models Table CSV/JSON/XLSX exports are gated to Institutional subscribers, so there
is **no reliable public URL to auto-fetch**. You download a fresh export yourself; the
script handles the diff and the logging. Alan Thompson updates the source by hand on each
model's launch day, so our copy drifts the moment a new model lands — re-run this whenever
you want to catch up.

## The routine

1. **Get a fresh export.** From the Models Table, download the XLSX and save it over
   `Pruned AI Models_Table.xlsx` in the repo root (or keep it elsewhere and pass
   `--new PATH`).

2. **Preview the delta** (writes nothing):
   ```bash
   python logs/diff_dataset.py
   ```
   Prints models added / removed / changed, with old → new values for every changed cell,
   plus the new model/lab/column counts.

3. **Record it:**
   ```bash
   python logs/diff_dataset.py --write
   ```
   This will
   - prepend a dated `### YYYY-MM-DD — Update (+A / -R / ~C)` entry to `CHANGELOG.md`,
   - refresh the **Current dataset specs** block, and
   - overwrite `snapshots/latest.json` with the new baseline.

4. **Commit** `CHANGELOG.md` and `snapshots/latest.json` together so the baseline stays in
   sync with the log.

5. **Rebuild the constellation data** from the new snapshot:
   ```bash
   python logs/build_constellation.py
   ```
   This reads `snapshots/latest.json` only — it never touches the xlsx, `diff_dataset.py`,
   `CHANGELOG.md`, or the snapshot itself — and writes three files into `dist/`:

   | File | What it is |
   |---|---|
   | `constellation-data.json` | The records as pure JSON (2-space indent, sorted keys, readable diffs) |
   | `constellation-data.js` | The same data as three browser globals — `window.DATASET`, `window.METRICS`, `window.MODELS` — loadable as a classic `<script>` |
   | `REPORT.md` | What was emitted, what was skipped, every family formed, every id collision, and every judgment the build made |

   Commit `dist/` alongside the snapshot so the published data matches the baseline it
   came from.

### Options

`diff_dataset.py`:

| Flag | Meaning |
|---|---|
| `--new PATH` | Export to diff (default: `Pruned AI Models_Table.xlsx` in the repo root) |
| `--write` | Apply the delta to `CHANGELOG.md` and save the new baseline (default: preview only) |
| `--date YYYY-MM-DD` | Date stamp for the entry/snapshot (default: today) |

`build_constellation.py`:

| Flag | Meaning |
|---|---|
| `--snapshot PATH` | Snapshot to read (default: `logs/snapshots/latest.json`) |
| `--out DIR` | Output directory (default: `dist`) |
| `--labs "OpenAI,Anthropic"` | Keep only these labs (matches the aliased `lab` or the original `labRaw`) |
| `--since YYYY-MM` | Keep only records dated that month or later |
| `--check` | Validate and print the report without writing anything |

The build is **deterministic** — two runs on the same snapshot produce byte-identical
output, and the only date it emits is the snapshot's own `captured` field. It **fails
rather than degrades**: on any validation error it writes nothing, prints every problem,
and exits 1. Standard library only; no network access.

Two conventions worth knowing:

- **`score` is null on every record.** The snapshot carries no Artificial Analysis index,
  so none is invented — the published ALScore rides in `alscore`, unrescaled.
- **`family` is deliberately conservative.** It groups sibling variants only via a fixed
  token allowlist (`Pro`, `Flash`, `Mini`, …) plus a shared stem and lab. Named sibling
  lines (Opus / Sonnet / Haiku) stay `null` by design; a wrong grouping is worse than none.

## Notes on parsing

- The real header is on **row 2** (row 1 holds permalinks/metadata); data starts on row 3.
- Header cells are cleaned of sort glyphs and line-wraps (`MMLU\n-Pro` → `MMLU-Pro`).
- The blank spacer column is skipped automatically (only named columns are tracked).
- Models are keyed by name; duplicate names are disambiguated by lab (`Name ‹Lab›`).
- Requires `openpyxl` (`pip install openpyxl`). No network access is used.

## Editing by hand

You can still edit `CHANGELOG.md` manually — just keep the
`<!-- SPECS:START -->` / `<!-- SPECS:END -->` and `<!-- CHANGES:START -->` markers in
place, since the script writes between them.
