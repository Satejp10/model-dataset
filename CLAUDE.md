# CLAUDE.md

Guidance for Claude Code working in this repo. See [`README.md`](README.md) for what the
repo is and [`logs/README.md`](logs/README.md) for the update routine.

## Never guess a figure

Every number in the dataset has to come from a primary source that states it. If no
source states it, **leave the field blank** — a blank cell is a known gap, a guessed one
is a wrong fact that looks like a right one. Don't infer a figure from a benchmark score,
a competitor's specs, a press estimate, or arithmetic on other fields, and don't carry a
number over from a similar model. Same for dates, parameter counts and benchmark
results.

## `archive/` is read-only

`archive/` holds frozen copies of the dataset. Never edit, regenerate or delete anything
under it — including `archive/README.md`. Read from it freely; to work from a frozen
copy, copy it out first (see [`archive/README.md`](archive/README.md)).

## Add new models with the weekly-model-update skill

New models go in through the `weekly-model-update` skill
(`.claude/skills/weekly-model-update/SKILL.md`), which sources the facts, writes the row
with `logs/add_model.py`, logs the change, rebuilds `dist/` and opens one PR. Don't type
rows into the workbook by hand and don't hand-edit the generated files in `dist/`.

Before a run, read [`logs/pinned.md`](logs/pinned.md). It lists models someone asked for
that aren't in the sheet yet (image models, for now) and the tag they get when they go in.

## The scripts in `logs/` need openpyxl

`pip install openpyxl` — `add_model.py` and `diff_dataset.py` both exit immediately
without it. (`build_constellation.py` is standard library only; it reads the snapshot,
not the workbook.) None of the scripts use the network.
