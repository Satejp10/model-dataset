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

### Options

| Flag | Meaning |
|---|---|
| `--new PATH` | Export to diff (default: `Pruned AI Models_Table.xlsx` in the repo root) |
| `--write` | Apply the delta to `CHANGELOG.md` and save the new baseline (default: preview only) |
| `--date YYYY-MM-DD` | Date stamp for the entry/snapshot (default: today) |

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
