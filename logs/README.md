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
- `skip.txt` — models the weekly check below should never propose. `last_check.txt` sits
  beside it once that check has run for the first time.
- `pinned.md` — models someone asked for that aren't in the sheet yet, such as image
  models, with the tag they get when they go in.

## Weekly check

The `weekly-model-update` skill (`.claude/skills/weekly-model-update/SKILL.md`) looks for
models the tracked labs have released, adds the ones a primary source confirms, runs the
routine below, and opens **one PR** for review. Nothing lands without that review, and the
skill only ever adds rows — fixes to existing rows go in the PR body as suggestions.

**It runs only when you ask it to.** Nothing is scheduled, so no check happens on its own:

- press **Run now** on the claude.ai routine, or
- ask for it in a session — "run the weekly model update", or anything that names it.

Weekly is the intended rhythm, not an enforced one.

- **`last_check.txt`** holds the date of the last check, one `YYYY-MM-DD` line, written at
  the end of each run. The next run searches from 14 days before it, so a longer gap
  between runs still gets covered. It doesn't exist until the first run, which starts at
  2026-07-01.
- **`skip.txt`** stops a model from being proposed again: one model name per line, `#` for
  comments. Add anything that keeps surfacing as a candidate but doesn't belong here.
- **`archive/`** holds a frozen copy of the dataset from before the first automated run, so
  there is always a known-good state to fall back to. See
  [`archive/README.md`](../archive/README.md).

The sections below are what a run does, step by step.

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

   A fresh export carries **every** lab in the Models Table, and this repo tracks a
   pruned subset, so `diff_dataset.py` applies a **lab allowlist to the new export
   before it diffs**. The default allowlist is the distinct `Lab` values already in
   `snapshots/latest.json`, which keeps the pruned set pruned without anyone restating
   it; rows from any other lab never reach the diff, the specs block or the new
   snapshot. The run prints how many rows the filter dropped, and which labs they came
   from:

   ```
   Lab filter: 15 lab(s) from logs/snapshots/latest.json · kept 403 row(s), dropped 128 row(s)
     31 lab(s) not on the allowlist:
       Cohere (12)
       AI21 (9)
       …
   ```

   Pass `--labs "A,B,C"` to use a different list (matched case-insensitively against the
   `Lab` column) — that is how a lab joins or leaves the tracked set. Widening it once,
   with `--labs` naming the current labs plus the new one, is enough: the next run's
   default allowlist is read back from the snapshot you just wrote.

   Whatever the allowlist, models in the baseline that the filtered export no longer
   carries are printed under a **WARNING** header before anything is written:

   ```
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   WARNING — 1 model(s) in the baseline are NOT in the filtered export.
   ...
     - GPT-6 Astra — OpenAI
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   ```

   Read that list before you `--write`. Rows added by hand with `add_model.py` are
   exactly the rows a fresh export can drop — a model Alan hasn't listed yet vanishes
   the moment you overwrite the workbook. Re-add any that should stay (step 1b) and run
   the diff again.

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

4. **Commit** the workbook, `CHANGELOG.md` and `snapshots/latest.json` together so the
   baseline stays in sync with both the log and the file it was parsed from.

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
| `--labs "OpenAI,Anthropic"` | Lab allowlist applied to the new export before the diff, matched case-insensitively (default: the distinct `Lab` values in `snapshots/latest.json`) |

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

A few conventions worth knowing:

- **`score` is null on every record.** The snapshot carries no Artificial Analysis index,
  so none is invented — the published ALScore rides in `alscore`, unrescaled.
- **`family` is deliberately conservative.** It groups sibling variants only via a fixed
  token allowlist (`Pro`, `Flash`, `Mini`, …) plus a shared stem and lab. Named sibling
  lines (Opus / Sonnet / Haiku) stay `null` by design; a wrong grouping is worse than none.
- **Release status follows LifeArchitect's legend.** The source `Public?` column is
  🟢 publicly accessible, 🟡 video or scripted demo only, 🔴 held in the lab and never
  released. Every record carries both:

  | `Public?` | `released` | `access` |
  |---|---|---|
  | 🟢 | `true` | `"public"` |
  | 🟡 | `false` | `"demo"` |
  | 🔴 | `false` | `"unreleased"` |

  Only 🟢 is `released: true` — a 🟡 demo is something you cannot use — and `access` is
  what tells a demo apart from a model still in the lab. A glyph outside the legend
  falls back to `released: true` / `access: "public"` and is listed under **Warnings**
  in `REPORT.md`; `released == (access == "public")` holds on every record either way.
- **`DATASET.source` carries the credit.** Every build stamps
  `Data: Dr Alan D. Thompson, LifeArchitect.ai Models Table (Sep/2026).` into the dataset
  block, so anything rendering this data has the attribution to hand. It is a constant in
  `build_constellation.py` — update it when the export vintage changes.

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

## Tags

`Tags` is a free-text, comma-separated column; the build splits it into a `tags` list.

| Tag | Meaning |
|---|---|
| `Reasoning` | Reasoning or thinking model |
| `Diffusion` | Diffusion language model |
| `SOTA` | The lab's own results show it leading major benchmarks at launch |
| `Image` | Image generation or editing model. None yet, see [`pinned.md`](pinned.md) |
| `Video` | Also generates video. Goes alongside `Image` |

## Editing by hand

You can still edit `CHANGELOG.md` manually — just keep the
`<!-- SPECS:START -->` / `<!-- SPECS:END -->` and `<!-- CHANGES:START -->` markers in
place, since the script writes between them.
