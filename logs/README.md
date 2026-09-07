# Dataset Change Logs

This folder tracks every change to `Pruned AI Models_Table.xlsx` (our pruned copy of
the [LifeArchitect.ai Models Table](https://lifearchitect.ai/models-table/)).

## Files

- `CHANGELOG.md` — reverse-chronological log of changes, plus a live specs snapshot.
  Both the specs block and the dated entries are maintained by the script below.
- `add_model.py` — inserts new model rows into the workbook from a small JSON spec,
  for when you know what shipped but have no fresh export to hand.
- `diff_dataset.py` — parses a fresh export, diffs it against the last snapshot, and
  logs the delta.
- `snapshots/latest.json` — the last recorded state of the dataset (the diff baseline).
  Committed so the next diff has something to compare against.
- `build_constellation.py` — builds the browser-ready constellation data in `dist/` from
  that snapshot (step 5 below).

## Why it's semi-manual

The Models Table CSV/JSON/XLSX exports are gated to Institutional subscribers, so there
is **no reliable public URL to auto-fetch**. You supply the new data — a fresh export, or
a short JSON spec for models you already know shipped — and the scripts handle the
placement, the diff and the logging. Alan Thompson updates the source by hand on each
model's launch day, so our copy drifts the moment a new model lands — re-run this whenever
you want to catch up.

## The routine

1. **Get the new models into the workbook.** Two ways in, depending on what you have:

   **(a) A fresh export.** From the Models Table, download the XLSX and save it over
   `Pruned AI Models_Table.xlsx` in the repo root (or keep it elsewhere and pass
   `--new PATH`). This is the authoritative path — it picks up edits to existing rows
   as well as new ones.

   **(b) A handful of models you already know about.** Write them into a JSON spec and
   let `add_model.py` place them:
   ```bash
   python logs/add_model.py --example > new.json   # see the shape
   python logs/add_model.py --spec new.json        # preview
   python logs/add_model.py --spec new.json --write
   ```
   It finds the right sorted position, copies the surrounding cell styles and number
   formats, normalises `Announced` to the first of the month, and extends the
   autofilter. Keys are the column names as listed in the **Columns** table in
   `CHANGELOG.md`; anything you leave out stays blank.

   Validation runs over the whole spec before a single row is written: unknown
   columns, a missing `Model`/`Lab`/`Announced`, a benchmark above 100, a `Public?`
   outside 🟢/🔴/🟡, a `Paper / Repo` that isn't a URL, or a model already in the
   sheet each abort the run with nothing changed. Models sharing a month keep the
   order you listed them in.

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

`add_model.py`:

| Flag | Meaning |
|---|---|
| `--spec PATH` | JSON file describing the model(s) to add, or `-` to read stdin |
| `--xlsx PATH` | Workbook to edit (default: `Pruned AI Models_Table.xlsx` in the repo root) |
| `--write` | Save the workbook (default: preview only) |
| `--allow-duplicate` | Permit a model whose name and lab already appear in the sheet |
| `--example` | Print a spec template and exit |

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
- `Count (rough)` is a rough ordinal carried down from the upstream source (919 → 1, with
  gaps), so `add_model.py` leaves it blank rather than inventing a number. Pass it
  explicitly if a fresh export ever tells you what it should be.
- `Announced` stores day 1 for every model; the sheet's two day-30/31 rows predate us and
  are left alone.
- Requires `openpyxl` (`pip install openpyxl`). No network access is used.

## Editing by hand

You can still edit `CHANGELOG.md` manually — just keep the
`<!-- SPECS:START -->` / `<!-- SPECS:END -->` and `<!-- CHANGES:START -->` markers in
place, since the script writes between them.
